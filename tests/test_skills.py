import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("collection_cli", SOURCE / "scripts/skills.py")
cli = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cli
SPEC.loader.exec_module(cli)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.home = self.base / "home"
        self.home.mkdir()
        self.root = self.base / "checkout"
        self.target = self.home / ".agents/skills"
        self.legacy = self.home / ".codex/skills"
        self.environment = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(self.home / ".codex"), PYTHONDONTWRITEBYTECODE="1")
        self.root.mkdir()
        (self.root / "scripts").mkdir()
        shutil.copy2(SOURCE / "scripts/skills.py", self.root / "scripts/skills.py")
        shutil.copy2(SOURCE / "scripts/plugin.schema.json", self.root / "scripts/plugin.schema.json")
        self.defaults = dict(default_model="inherit-parent", roles={}, panel_size=2)
        self.write_json(self.root / "codex-config.json", self.defaults)
        self.write_json(self.root / "plugin.json", json.loads((SOURCE / "plugin.json").read_text()))
        shutil.copy2(SOURCE / "codex-port.json", self.root / "codex-port.json")
        for name in ("poteto-mode", "poteto-pr-description", "prepare-goal", "research-to-goal"):
            self.skill(self.root / "skills" / name, name)
        script = self.root / "skills/poteto-mode/scripts/check-plan.mjs"
        script.parent.mkdir()
        script.write_text("export {};\n")
        self.populate_legacy()
        self.receipt = self.make_receipt()
        self.write_json(self.root / "import-receipt.json", self.receipt)
        shutil.rmtree(self.legacy)

    def write_json(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + "\n")

    def skill(self, directory, name):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(f"---\nname: {name}\ndescription: A test skill.\n---\n\n# Example\n")

    def populate_legacy(self):
        self.write_json(self.legacy / "pstack/codex-config.json", self.defaults)
        self.skill(self.legacy / "pstack/skills/poteto-mode", "poteto-mode")
        for name in cli.LEGACY[1:]:
            self.skill(self.legacy / name, name)

    def make_receipt(self):
        files = {str(p.relative_to(self.legacy)): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.legacy.rglob("*") if p.is_file()}
        return dict(format=1, sources=list(cli.LEGACY), files=files)

    def command(self, *args, root=None, success=True):
        result = subprocess.run([sys.executable, str((root or self.root) / "scripts/skills.py"), *args], env=self.environment, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def install(self, *args, **kwargs):
        return self.command("install", "--target-dir", str(self.target), *args, **kwargs)

    def test_install_is_repeatable_and_uninstall_preserves_unrelated_skill(self):
        self.skill(self.target / "other", "other")
        self.install()
        self.install()
        self.assertEqual((self.target / cli.BUNDLE).resolve(), self.root / "skills")
        self.command("uninstall", "--target-dir", str(self.target))
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertFalse((self.target / cli.BUNDLE).is_symlink())
        self.assertTrue((self.target / "other/SKILL.md").is_file())
        self.assertTrue((self.root / "skills/poteto-mode/SKILL.md").is_file())

    def test_dry_run_has_no_filesystem_effect(self):
        self.populate_legacy()
        before = sorted(str(p.relative_to(self.base)) for p in self.base.rglob("*"))
        result = self.install("--migrate-from", str(self.legacy), "--dry-run")
        self.assertIn("backup:", result.stdout)
        self.assertEqual(before, sorted(str(p.relative_to(self.base)) for p in self.base.rglob("*")))

    def test_refuses_unmanaged_destinations(self):
        self.target.mkdir(parents=True)
        dest = self.target / cli.BUNDLE
        for kind in ("file", "directory", "broken-link", "other-link"):
            with self.subTest(kind=kind):
                if kind == "file":
                    dest.write_text("keep")
                elif kind == "directory":
                    dest.mkdir()
                    (dest / "keep").write_text("keep")
                else:
                    dest.symlink_to(self.base / "absent" if kind == "broken-link" else self.root)
                self.install(success=False)
                self.assertTrue(cli.exists(dest))
                if dest.is_dir() and not dest.is_symlink():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()

    def test_duplicate_name_in_target_or_global_root_stops_install(self):
        for location in (self.target / "custom-name", self.legacy / "custom-name"):
            with self.subTest(location=location):
                self.skill(location, "poteto-mode")
                result = self.install(success=False)
                self.assertIn("Skill name collision", result.stderr)
                self.assertFalse(cli.exists(self.target / cli.BUNDLE))
                shutil.rmtree(location)

    def test_unrelated_metadata_does_not_require_our_skill_conventions(self):
        location = self.target / "third-party"
        location.mkdir(parents=True)
        (location / "SKILL.md").write_text("---\nname: vendor:custom\n---\n")
        self.install()
        self.assertTrue((location / "SKILL.md").exists())

    def test_duplicate_name_behind_bundle_symlink_stops_install(self):
        alias = self.base / "alias"
        self.skill(alias / "nested", "poteto-mode")
        self.target.mkdir(parents=True)
        (self.target / "alias").symlink_to(alias)
        self.install(success=False)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_switch_and_rollback_require_managed_link(self):
        other = self.base / "release"
        shutil.copytree(self.root, other)
        self.install()
        self.install(root=other)
        self.assertEqual((self.target / cli.BUNDLE).resolve(), other / "skills")
        self.command("uninstall", "--target-dir", str(self.target), success=False)
        self.assertTrue((self.target / cli.BUNDLE).is_symlink())
        self.install()
        self.assertEqual((self.target / cli.BUNDLE).resolve(), self.root / "skills")

    def test_switch_rejects_tampered_managed_link(self):
        self.install()
        dest = self.target / cli.BUNDLE
        dest.unlink()
        dest.symlink_to(self.base / "missing")
        self.install(success=False)
        self.assertEqual(os.readlink(dest), str(self.base / "missing"))

    def test_migration_preserves_runtime_config_and_unrelated_siblings(self):
        self.populate_legacy()
        runtime = self.legacy / "pstack/.pstack/history"
        runtime.parent.mkdir()
        runtime.write_text("personal state")
        dependency = self.legacy / "pstack/node_modules/dependency.js"
        dependency.parent.mkdir()
        dependency.write_text("dependency")
        self.skill(self.legacy / "unrelated", "unrelated")
        original_config = (self.legacy / "pstack/codex-config.json").read_bytes()
        self.install("--migrate-from", str(self.legacy))
        self.install("--migrate-from", str(self.legacy))
        self.assertEqual((self.root / "codex-config.local.json").read_bytes(), original_config)
        backups = list((cli.state_dir(self.target) / "backups").glob("*/pstack"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / ".pstack/history").read_text(), "personal state")
        self.assertEqual((backups[0] / "node_modules/dependency.js").read_text(), "dependency")
        self.assertTrue((self.legacy / "unrelated/SKILL.md").is_file())
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertTrue(backups[0].exists())
        self.assertTrue((self.root / "codex-config.local.json").exists())

    def test_modified_or_added_legacy_source_stops_all_moves(self):
        for change in ("modified", "added", "removed"):
            with self.subTest(change=change):
                self.populate_legacy()
                path = self.legacy / "pstack/skills/poteto-mode/SKILL.md"
                if change == "modified":
                    path.write_text(path.read_text() + "A local change.\n")
                elif change == "added":
                    (path.parent / "custom-script.py").write_text("print('keep')\n")
                else:
                    path.unlink()
                self.install("--migrate-from", str(self.legacy), success=False)
                self.assertTrue((self.legacy / "pstack").exists())
                self.assertTrue((self.legacy / "prepare-goal/SKILL.md").exists())
                self.assertFalse((self.root / "codex-config.local.json").exists())
                self.assertFalse(cli.exists(self.target / cli.BUNDLE))
                shutil.rmtree(self.legacy)

    def test_differing_override_stops_migration_without_overwrite(self):
        self.populate_legacy()
        override = dict(self.defaults, panel_size=3)
        self.write_json(self.root / "codex-config.local.json", override)
        self.install("--migrate-from", str(self.legacy), success=False)
        self.assertEqual(json.loads((self.root / "codex-config.local.json").read_text()), override)
        self.assertTrue((self.legacy / "pstack").exists())
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_symlinked_legacy_entry_is_never_moved(self):
        self.populate_legacy()
        source = self.legacy / "prepare-goal"
        source.rename(self.base / "external-source")
        source.symlink_to(self.base / "external-source")
        self.install("--migrate-from", str(self.legacy), success=False)
        self.assertTrue(source.is_symlink())
        self.assertTrue((self.legacy / "pstack").exists())

    def test_partial_migration_can_resume_from_retained_plan(self):
        self.populate_legacy()
        collection = cli.load_collection(self.root)
        with patch.dict(os.environ, self.environment):
            changes = cli.plan_install(collection, self.target, self.legacy)
        original_rename = Path.rename
        def interrupt(path, destination):
            if path == self.legacy / "prepare-goal":
                raise OSError("simulated interruption")
            return original_rename(path, destination)
        with cli.installation_lock(self.target), patch.object(Path, "rename", interrupt):
            with self.assertRaises(OSError):
                cli.apply_install(collection, self.target, self.legacy, changes)
        self.assertFalse((self.legacy / "pstack").exists())
        self.assertTrue((cli.state_dir(self.target) / "pending.json").exists())
        self.install("--migrate-from", str(self.legacy))
        self.assertEqual((self.target / cli.BUNDLE).resolve(), self.root / "skills")
        self.assertFalse((cli.state_dir(self.target) / "pending.json").exists())
        self.assertTrue(next((cli.state_dir(self.target) / "backups").glob("*/pstack/codex-config.json")).exists())

    def test_configuration_copy_interruption_never_publishes_partial_file(self):
        self.populate_legacy()
        collection = cli.load_collection(self.root)
        with patch.dict(os.environ, self.environment):
            changes = cli.plan_install(collection, self.target, self.legacy)
        original_open = Path.open
        class PartialWriter:
            def __init__(self, stream):
                self.stream = stream
            def __enter__(self):
                self.stream.__enter__()
                return self
            def __exit__(self, *args):
                return self.stream.__exit__(*args)
            def write(self, data):
                self.stream.write(data[:5])
                self.stream.flush()
                raise KeyboardInterrupt("simulated interrupted write")
        def interrupted_open(path, *args, **kwargs):
            stream = original_open(path, *args, **kwargs)
            return PartialWriter(stream) if path.name.startswith(".preserve-config-") else stream
        with cli.installation_lock(self.target), patch.object(Path, "open", interrupted_open):
            with self.assertRaises(KeyboardInterrupt):
                cli.apply_install(collection, self.target, self.legacy, changes)
        self.assertFalse((self.root / "codex-config.local.json").exists())
        self.assertFalse(list(self.root.glob(".preserve-config-*")))
        self.install("--migrate-from", str(self.legacy))
        self.assertEqual(json.loads((self.root / "codex-config.local.json").read_text()), self.defaults)
        self.assertEqual((self.target / cli.BUNDLE).resolve(), self.root / "skills")

    def test_configuration_publish_never_overwrites_new_override(self):
        self.populate_legacy()
        source = self.legacy / "pstack/codex-config.json"
        destination = self.root / "codex-config.local.json"
        override = dict(self.defaults, panel_size=4)
        original_link = os.link
        def competing_override(source, target):
            self.write_json(destination, override)
            return original_link(source, target)
        with patch.object(os, "link", competing_override):
            with self.assertRaises(cli.Invalid):
                cli.preserve_config(source, destination)
        self.assertEqual(json.loads(destination.read_text()), override)
        self.assertFalse(list(self.root.glob(".preserve-config-*")))

    def test_disappearing_legacy_source_cannot_skip_its_backup(self):
        self.populate_legacy()
        collection = cli.load_collection(self.root)
        with patch.dict(os.environ, self.environment):
            changes = cli.plan_install(collection, self.target, self.legacy)
        (self.legacy / "prepare-goal").rename(self.base / "moved-elsewhere")
        with cli.installation_lock(self.target):
            with self.assertRaises(cli.Invalid):
                cli.apply_install(collection, self.target, self.legacy, changes)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))
        self.assertTrue((cli.state_dir(self.target) / "pending.json").exists())

    def test_lock_stops_concurrent_installation(self):
        with cli.installation_lock(self.target):
            result = self.install(success=False)
            self.assertIn("Installation lock exists", result.stderr)
            self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_nested_discovery_target_cannot_hide_backups_in_global_skills(self):
        self.target = self.legacy / "nested"
        result = self.install(success=False)
        self.assertIn("inside a discovery root", result.stderr)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_invalid_local_config_is_not_ignored(self):
        (self.root / "codex-config.local.json").write_text("{broken")
        self.command("validate", success=False)
        self.install(success=False)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_uninstall_works_with_broken_source_metadata(self):
        self.install()
        (self.root / "codex-config.local.json").write_text("{broken")
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_validator_checks_yaml_names_and_links_but_skips_code_examples(self):
        self.command("validate")
        path = self.root / "skills/poteto-mode/SKILL.md"
        original = path.read_text()
        path.write_text(original + "\n```md\n[example](missing.md)\n```\n`[example](missing.md)`\n")
        self.command("validate")
        path.write_text(original + "\n[broken](missing.md)\n")
        self.command("validate", success=False)
        path.write_text(original.replace("description: A test skill.", "description: invalid: scalar"))
        self.command("validate", success=False)
        path.write_text(original.replace("name: poteto-mode", "name: prepare-goal"))
        self.command("validate", success=False)

    def test_manifest_schema_rejects_invalid_fields_and_allows_new_versions(self):
        path = self.root / "plugin.json"
        manifest = json.loads(path.read_text())
        manifest["description"] = 123
        self.write_json(path, manifest)
        self.command("validate", success=False)
        manifest["description"] = "Collection"
        manifest["version"] = "0.2.0"
        self.write_json(path, manifest)
        self.command("validate")
        manifest["skills"] = "./skills"
        self.write_json(path, manifest)
        self.command("validate", success=False)

    def test_validator_checks_anchors_and_optional_invocation_policy(self):
        path = self.root / "skills/poteto-mode/SKILL.md"
        path.write_text(path.read_text() + "\n[valid](#example)\n")
        metadata = path.parent / "agents/openai.yaml"
        metadata.parent.mkdir()
        metadata.write_text("interface:\n  display_name: Example\n")
        self.command("validate")
        metadata.write_text("policy:\n  allow_implicit_invocation: 'false'\n")
        self.command("validate", success=False)
        metadata.write_text("policy:\n  allow_implicit_invocation: false\n")
        self.command("validate")
        path.write_text(path.read_text() + "\n[invalid](#absent)\n")
        self.command("validate", success=False)


if __name__ == "__main__":
    unittest.main()
