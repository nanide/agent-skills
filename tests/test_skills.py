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
        mapping = json.loads((SOURCE / "skill-names.json").read_text())
        for name in (*mapping.values(), "how"):
            self.skill(self.root / "skills" / name, name)
        script = self.root / "skills/nanide-mode/scripts/check-plan.mjs"
        script.parent.mkdir()
        script.write_text("export {};\n")
        self.write_json(self.root / "skill-names.json", mapping)
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
        for name in ("poteto-mode", "poteto-help", "poteto-audit", "poteto-goal", "how", "setup-pstack"):
            self.skill(self.legacy / "pstack/skills" / name, name)
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
        self.assertTrue((self.root / "skills/nanide-mode/SKILL.md").is_file())

    def test_normal_install_coexists_with_known_baseline_without_changing_it(self):
        self.populate_legacy()
        mapping = json.loads((SOURCE / "skill-names.json").read_text())
        baseline = self.make_receipt()["files"]
        personal_config = dict(self.defaults, panel_size=3)
        self.write_json(self.root / "codex-config.local.json", personal_config)
        self.install()
        self.install()
        self.assertEqual(self.make_receipt()["files"], baseline)
        self.assertEqual(json.loads((self.root / "codex-config.local.json").read_text()), personal_config)
        self.assertFalse((cli.state_dir(self.target) / "backups").exists())
        discovered = list(cli.discovery_skills(self.legacy, set())) + list(cli.discovery_skills(self.target, set()))
        names = [skill.name for skill in discovered]
        personal_names = {skill.name for skill in cli.load_collection(self.root).skills}
        self.assertEqual(set(names), set(mapping) | personal_names | {"prepare-goal", "research-to-goal"})
        self.assertEqual({name for name in names if names.count(name) == 2}, {"how"})
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertEqual(self.make_receipt()["files"], baseline)

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
        for name in ("nanide-mode", "audit"):
            for location in (self.target / "custom-name", self.legacy / "custom-name"):
                with self.subTest(name=name, location=location):
                    self.skill(location, name)
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
        self.skill(alias / "nested", "nanide-mode")
        self.target.mkdir(parents=True)
        (self.target / "alias").symlink_to(alias)
        self.install(success=False)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_generic_helpers_reject_unrelated_duplicates_and_baseline_aliases(self):
        self.populate_legacy()
        for location in (self.target / "custom-how", self.legacy / "custom-how"):
            with self.subTest(location=location):
                self.skill(location, "how")
                self.assertIn("Skill name collision", self.install(success=False).stderr)
                shutil.rmtree(location)
        self.target.mkdir(parents=True, exist_ok=True)
        (self.target / "baseline-alias").symlink_to(self.legacy / "pstack")
        self.assertIn("Skill name collision", self.install(success=False).stderr)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_known_baseline_helper_requires_recorded_hash_and_real_path(self):
        self.populate_legacy()
        path = self.legacy / "pstack/skills/how/SKILL.md"
        original = path.read_text()
        path.write_text(original + "A local change.\n")
        self.assertIn("Skill name collision", self.install(success=False).stderr)
        path.unlink()
        copy = self.base / "how.md"
        copy.write_text(original)
        path.symlink_to(copy)
        self.assertIn("Skill name collision", self.install(success=False).stderr)

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

    def test_migration_keeps_standalone_goal_helpers_discoverable(self):
        self.populate_legacy()
        originals = {}
        for name in ("prepare-goal", "research-to-goal"):
            path = self.legacy / name / "SKILL.md"
            path.write_text(path.read_text() + "A local standalone change.\n")
            originals[name] = path.read_bytes()
        self.install("--migrate-from", str(self.legacy))
        self.install("--migrate-from", str(self.legacy))
        for name, contents in originals.items():
            self.assertEqual((self.legacy / name / "SKILL.md").read_bytes(), contents)
        discovered = list(cli.discovery_skills(self.legacy, set())) + list(cli.discovery_skills(self.target, set()))
        for name in originals:
            self.assertEqual([skill.name for skill in discovered].count(name), 1)
        self.assertFalse((self.legacy / "pstack").exists())
        self.assertFalse((self.legacy / "poteto-pr-description").exists())
        backups = cli.state_dir(self.target) / "backups"
        self.assertEqual({path.name for path in backups.glob("*/*")}, {"pstack", "poteto-pr-description"})
        self.command("uninstall", "--target-dir", str(self.target))
        for name, contents in originals.items():
            self.assertEqual((self.legacy / name / "SKILL.md").read_bytes(), contents)

    def test_old_pending_standalone_backups_stop_before_any_changes(self):
        self.populate_legacy()
        collection = cli.load_collection(self.root)
        baseline = self.make_receipt()["files"]
        state = cli.state_dir(self.target)
        pending = state / "pending.json"
        for name in ("prepare-goal", "research-to-goal"):
            with self.subTest(name=name):
                with patch.dict(os.environ, self.environment):
                    changes = cli.plan_install(collection, self.target, self.legacy)
                unsafe = cli.Change("backup", self.legacy / name, state / "backups/old-plan" / name)
                journal = dict(root=str(self.root), target=str(self.target), migration=str(self.legacy), changes=[c.record() for c in (*changes, unsafe)])
                self.write_json(pending, journal)
                result = self.install("--migrate-from", str(self.legacy), success=False)
                self.assertIn("Unsafe interrupted action", result.stderr)
                self.assertEqual(self.make_receipt()["files"], baseline)
                self.assertEqual(json.loads(pending.read_text()), journal)
                self.assertFalse((state / "backups").exists())
                self.assertFalse((self.root / "codex-config.local.json").exists())
                self.assertFalse(cli.exists(self.target / cli.BUNDLE))
                pending.unlink()

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
                self.assertTrue((self.legacy / "poteto-pr-description/SKILL.md").exists())
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
        source = self.legacy / "poteto-pr-description"
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
            if path == self.legacy / "poteto-pr-description":
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
        (self.legacy / "poteto-pr-description").rename(self.base / "moved-elsewhere")
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
        path = self.root / "skills/nanide-mode/SKILL.md"
        original = path.read_text()
        path.write_text(original + "\n```md\n[example](missing.md)\n```\n`[example](missing.md)`\n")
        self.command("validate")
        path.write_text(original + "\n[broken](missing.md)\n")
        self.command("validate", success=False)
        path.write_text(original.replace("description: A test skill.", "description: invalid: scalar"))
        self.command("validate", success=False)
        path.write_text(original.replace("name: nanide-mode", "name: prepare-goal"))
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
        path = self.root / "skills/nanide-mode/SKILL.md"
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

    def test_rename_map_preserves_mapped_names_and_allows_new_personal_skills(self):
        self.skill(self.root / "skills/nanide-new-workflow", "nanide-new-workflow")
        self.command("validate")
        self.skill(self.root / "skills/unprefixed", "unprefixed")
        self.command("validate")
        shutil.rmtree(self.root / "skills/nanide-help")
        result = self.command("validate", success=False)
        self.assertIn("mapped skill names must be unique and present", result.stderr)

    def test_collection_renames_source_brands_and_retains_generic_helpers(self):
        receipt = json.loads((SOURCE / "import-receipt.json").read_text())
        originals = {Path(path).parent.name for path in receipt["files"] if Path(path).name == "SKILL.md" and (path.startswith("pstack/skills/") or len(Path(path).parts) == 2)}
        mapping = json.loads((SOURCE / "skill-names.json").read_text())
        expected_mapping = {name: name.replace("poteto-", "nanide-", 1) for name in originals if name.startswith("poteto-")}
        expected_mapping["poteto-audit"] = "audit"
        expected_mapping["setup-pstack"] = "setup-nanide-skills"
        self.assertEqual(len(expected_mapping), 6)
        self.assertEqual(mapping, expected_mapping)
        generic = {Path(path).parent.name for path in receipt["files"] if path.startswith("pstack/skills/") and Path(path).name == "SKILL.md"} - mapping.keys()
        self.assertEqual(len(generic), 54)
        skills = cli.load_collection(SOURCE).skills
        self.assertEqual({skill.name for skill in skills}, generic | set(mapping.values()))
        self.assertTrue(all((SOURCE / "skills" / name / "SKILL.md").is_file() for name in generic))
        path = self.root / "skill-names.json"
        self.write_json(path, {**mapping, "how": "nanide-how"})
        self.assertIn("invalid rename for how", self.command("validate", success=False).stderr)

    def test_rename_map_requires_audit_and_preserves_other_personal_names(self):
        path = self.root / "skill-names.json"
        mapping = json.loads(path.read_text())
        for original, replacement in (("poteto-audit", "nanide-audit"), ("poteto-audit", "review"), ("poteto-goal", "goal"), ("setup-pstack", "setup-skills")):
            with self.subTest(original=original, replacement=replacement):
                self.write_json(path, {**mapping, original: replacement})
                result = self.command("validate", success=False)
                self.assertIn(f"invalid rename for {original}", result.stderr)
        self.write_json(path, mapping)
        self.command("validate")

    def test_personal_skill_cannot_route_to_original_namespace(self):
        path = self.root / "skills/nanide-mode/SKILL.md"
        original = path.read_text()
        for reference in ("Use $poteto-mode.", "Read ../poteto-mode/SKILL.md.", "Use $setup-pstack.", "Read ../setup-pstack/SKILL.md."):
            path.write_text(original + reference + "\n")
            result = self.command("validate", success=False)
            self.assertIn("personal skill references the original namespace", result.stderr)
        path.write_text(original + "Use $nanide-mode and read ../nanide-mode/SKILL.md.\n")
        self.command("validate")


if __name__ == "__main__":
    unittest.main()
