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
        shutil.copytree(SOURCE / "providers", self.root / "providers", ignore=shutil.ignore_patterns("config.local.json", "*.md"))
        self.defaults = dict(default_model="inherit-parent", roles={}, panel_size=2)
        self.write_json(self.root / "agent-config.json", self.defaults)
        self.write_json(self.root / "plugin.json", json.loads((SOURCE / "plugin.json").read_text()))
        shutil.copy2(SOURCE / "upstream.json", self.root / "upstream.json")
        mapping = json.loads((SOURCE / "skill-names.json").read_text())
        for name in mapping.values():
            self.skill(self.root / "skills" / name, name)
        script = self.root / "skills/mode/scripts/check-plan.mjs"
        script.parent.mkdir()
        script.write_text("export {};\n")
        for name in ("pr-titles.md", "pr-descriptions.md", "pr-metadata.md"):
            reference = self.root / "skills/mode/references" / name
            reference.parent.mkdir(exist_ok=True)
            reference.write_text("# PR instructions\n")
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
        for name, public in json.loads((SOURCE / "skill-names.json").read_text()).items():
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

    def test_each_provider_installs_its_discovery_set_without_copying(self):
        for provider in cli.PROVIDERS:
            target = self.home / {"codex": ".agents", "cursor": ".cursor", "claude": ".claude"}[provider] / "skills"
            for _ in range(2):
                self.command("install", "--provider", provider)
            adapter = json.loads((self.root / "providers" / provider / "adapter.json").read_text())
            expected = set(adapter.get("entry_points", json.loads((self.root / "skill-names.json").read_text()).values()))
            self.assertEqual({p.name for p in target.iterdir()}, expected)
            for name in expected:
                self.assertTrue((target / name).is_symlink())
                self.assertEqual((target / name / "SKILL.md").resolve(), self.root / "skills" / name / "SKILL.md")
            self.command("uninstall", "--provider", provider)
            self.command("uninstall", "--provider", provider)
            self.assertEqual(list(target.iterdir()), [])

    def test_all_providers_share_sources_and_repeat_safely(self):
        original = sorted(self.home.rglob("*"))
        self.command("install", "--provider", "all", "--dry-run")
        self.assertEqual(sorted(self.home.rglob("*")), original)
        for _ in range(2):
            self.command("install", "--provider", "all")
        for provider, directory in zip(cli.PROVIDERS, (".agents", ".cursor", ".claude")):
            target = self.home / directory / "skills"
            expected = set(json.loads((self.root / "providers" / provider / "adapter.json").read_text())["entry_points"])
            self.assertEqual({path.name for path in target.iterdir()}, expected)
            for name in expected:
                self.assertEqual((target / name / "SKILL.md").resolve(), self.root / "skills" / name / "SKILL.md")
        self.command("uninstall", "--provider", "all", "--dry-run")
        self.assertTrue((self.target / "mode").is_symlink())
        for _ in range(2):
            self.command("uninstall", "--provider", "all")
        for directory in (".agents", ".cursor", ".claude"):
            self.assertEqual(list((self.home / directory / "skills").iterdir()), [])

    def test_provider_upgrade_removes_only_owned_helper_links(self):
        for provider, directory in zip(cli.PROVIDERS, (".agents", ".cursor", ".claude")):
            target = self.home / directory / "skills"
            path = self.root / "providers" / provider / "adapter.json"
            adapter = json.loads(path.read_text())
            self.write_json(path, {key: value for key, value in adapter.items() if key != "entry_points"})
            self.command("install", "--provider", provider)
            self.assertTrue((target / "how").is_symlink())
            self.skill(target / "unrelated", "unrelated")
            self.write_json(path, adapter)
            before = sorted(target.iterdir())
            self.command("install", "--provider", provider, "--dry-run")
            self.assertEqual(sorted(target.iterdir()), before)
            for _ in range(2):
                self.command("install", "--provider", provider)
            self.assertEqual({skill.name for skill in cli.discovery_skills(target, set())}, set(adapter["entry_points"]) | {"unrelated"})
            mode = (target / "mode/SKILL.md").resolve()
            self.assertTrue((mode.parent.parent / "how/SKILL.md").is_file())
            self.assertTrue((mode.parent.parent / "principle-prove-it-works/SKILL.md").is_file())
            receipt = json.loads((cli.state_dir(target) / "provider-install.json").read_text())
            self.assertEqual(set(receipt["links"]), set(adapter["entry_points"]))
            self.command("uninstall", "--provider", provider)
            self.assertTrue((target / "unrelated/SKILL.md").is_file())
            self.assertTrue(mode.is_file())

    def test_entry_points_reject_invalid_or_unknown_names_before_installing(self):
        path = self.root / "providers/codex/adapter.json"
        adapter = json.loads(path.read_text())
        for entries in ([], None, "mode", [1], ["mode", "mode"], ["../mode"], ["nanide-missing"]):
            with self.subTest(entries=entries):
                self.write_json(path, {**adapter, "entry_points": entries})
                self.assertIn("entry_points", self.command("install", "--provider", "codex", success=False).stderr)
                self.assertFalse(self.target.exists())

    def test_all_provider_preflight_rejects_last_host_collision_before_writes(self):
        collision = self.home / ".claude/skills/mode"
        self.skill(collision, "mode")
        self.assertIn("unmanaged", self.command("install", "--provider", "all", success=False).stderr)
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse((self.home / ".cursor").exists())
        self.assertTrue((collision / "SKILL.md").is_file())
        self.assertFalse(cli.state_dir(collision.parent).exists())

    def test_all_provider_uninstall_preflight_preserves_other_hosts(self):
        self.command("install", "--provider", "all")
        target = self.home / ".claude/skills/mode"
        target.unlink()
        target.symlink_to(self.base / "other")
        self.assertIn("Managed link changed", self.command("uninstall", "--provider", "all", success=False).stderr)
        self.assertTrue((self.home / ".agents/skills/mode").is_symlink())
        self.assertTrue((self.home / ".cursor/skills/mode").is_symlink())
        self.assertEqual(target.readlink(), self.base / "other")

    def test_all_provider_rejects_non_global_options(self):
        original = sorted(self.home.rglob("*"))
        for arguments in (("install", "--target-dir", str(self.target)), ("install", "--migrate-from", str(self.legacy)), ("validate",), ("migrate-config",)):
            self.command(*arguments, "--provider", "all", success=False)
        self.assertEqual(sorted(self.home.rglob("*")), original)

    @patch("builtins.print")
    def test_provider_switch_recovers_after_interruption(self, _print):
        with patch.dict(os.environ, self.environment):
            collection = cli.load_collection(self.root)
            cli.install_provider(collection, "claude", self.target, "install", False)
            other = self.base / "release"
            shutil.copytree(self.root, other, symlinks=True)
            replacement = cli.load_collection(other)
            original_replace = os.replace
            calls = 0
            def interrupt(source, destination):
                nonlocal calls
                if Path(source).name.startswith(".agent-skills-link-"):
                    calls += 1
                    if calls == 2:
                        raise OSError("simulated interruption")
                return original_replace(source, destination)
            for _ in range(2):
                calls = 0
                with patch.object(os, "replace", interrupt):
                    with self.assertRaises(OSError):
                        cli.install_provider(replacement, "claude", self.target, "install", False)
            with self.assertRaises(cli.Invalid):
                cli.install_provider(collection, "claude", self.target, "install", False)
            cli.install_provider(replacement, "claude", self.target, "install", False)
            for skill in replacement.skills:
                if skill.name not in cli.adapter_config(other, "claude")["entry_points"]:
                    continue
                self.assertEqual((self.target / skill.name).resolve(), skill.source)
            with self.assertRaises(cli.Invalid):
                cli.install_provider(collection, "claude", self.target, "uninstall", False)
            cli.install_provider(replacement, "claude", self.target, "uninstall", False)
            self.assertEqual(list(self.target.iterdir()), [])

    def test_provider_install_dry_run_and_unmanaged_entries(self):
        for provider in cli.PROVIDERS:
            target = self.base / provider / "skills"
            self.command("install", "--provider", provider, "--target-dir", str(target), "--dry-run")
            self.assertFalse(target.parent.exists())
            self.skill(target / "mode", "mode")
            result = self.command("install", "--provider", provider, "--target-dir", str(target), success=False)
            self.assertIn("unmanaged", result.stderr)
            self.assertTrue((target / "mode/SKILL.md").is_file())

    def test_provider_install_preserves_tampered_links(self):
        self.command("install", "--provider", "claude")
        target = self.home / ".claude/skills/mode"
        target.unlink()
        target.symlink_to(self.base / "other")
        self.assertIn("Managed link changed", self.command("uninstall", "--provider", "claude", success=False).stderr)
        self.assertEqual(os.readlink(target), str(self.base / "other"))

    def test_root_local_config_migration_preserves_bytes_and_rejects_conflicts(self):
        old = self.root / "codex-config.local.json"
        new = self.root / "providers/codex/config.local.json"
        self.write_json(old, dict(self.defaults, panel_size=4))
        before = old.read_bytes()
        self.command("migrate-config", "--dry-run")
        self.assertFalse(new.exists())
        self.assertEqual(old.read_bytes(), before)
        self.command("migrate-config")
        self.command("migrate-config")
        self.assertFalse(old.exists())
        self.assertEqual(new.read_bytes(), before)
        self.write_json(old, dict(self.defaults, panel_size=5))
        self.command("migrate-config", success=False)
        self.assertEqual(new.read_bytes(), before)
        self.assertTrue(old.exists())

    def test_provider_collisions_are_scoped_to_the_selected_host(self):
        self.skill(self.home / ".codex/skills/custom", "mode")
        self.assertIn("Skill name collision", self.command("install", "--provider", "codex", success=False).stderr)
        self.command("install", "--provider", "cursor")
        self.command("install", "--provider", "claude")
        self.skill(self.home / ".cursor/skills/duplicate", "mode")
        self.command("install", "--provider", "cursor", "--target-dir", str(self.base / "project/skills"), success=False)

    def test_old_pending_migration_config_destination_can_resume(self):
        self.populate_legacy()
        collection = cli.load_collection(self.root)
        with patch.dict(os.environ, self.environment):
            changes = cli.plan_install(collection, self.target, self.legacy)
        old_config = self.root / "codex-config.local.json"
        changes = tuple(cli.Change(c.kind, c.source, old_config) if c.kind == "preserve-config" else c for c in changes)
        self.write_json(cli.state_dir(self.target) / "pending.json", dict(root=str(self.root), target=str(self.target), migration=str(self.legacy), changes=[c.record() for c in changes]))
        self.install("--migrate-from", str(self.legacy))
        self.assertEqual(json.loads((self.root / "providers/codex/config.local.json").read_text()), self.defaults)
        self.assertFalse(old_config.exists())
        self.assertFalse((cli.state_dir(self.target) / "pending.json").exists())

    def test_validator_rejects_unsafe_provider_discovery_paths(self):
        path = self.root / "providers/claude/adapter.json"
        adapter = json.loads(path.read_text())
        for invalid in ("/tmp/skills", "../skills", ""):
            self.write_json(path, {**adapter, "discovery_directory": invalid})
            self.assertIn("Invalid discovery directory", self.command("validate", success=False).stderr)

    def test_provider_rules_must_live_outside_shared_instructions(self):
        path = self.root / "skills/mode/SKILL.md"
        original = path.read_text()
        path.write_text(original + "Use Codex collaboration tools.\n")
        self.assertIn("provider-specific instructions", self.command("validate", success=False).stderr)
        path.write_text(original)
        adapter = self.root / "providers/codex/runtime.md"
        adapter.write_text("Use Codex collaboration tools.\n")
        self.command("validate")

    def test_install_is_repeatable_and_uninstall_preserves_unrelated_skill(self):
        self.skill(self.target / "other", "other")
        self.install()
        self.install()
        self.assertEqual((self.target / cli.BUNDLE).resolve(), self.root / "skills")
        self.command("uninstall", "--target-dir", str(self.target))
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertFalse((self.target / cli.BUNDLE).is_symlink())
        self.assertTrue((self.target / "other/SKILL.md").is_file())
        self.assertTrue((self.root / "skills/mode/SKILL.md").is_file())

    def test_short_source_names_reject_full_pstack_collision_without_changing_it(self):
        self.populate_legacy()
        baseline = self.make_receipt()["files"]
        self.assertIn("Skill name collision", self.install(success=False).stderr)
        self.assertEqual(self.make_receipt()["files"], baseline)
        self.assertFalse((self.target / cli.BUNDLE).exists())
        self.assertFalse((cli.state_dir(self.target) / "backups").exists())

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
        for name in ("mode", "audit", "how"):
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
        self.skill(alias / "nested", "mode")
        self.target.mkdir(parents=True)
        (self.target / "alias").symlink_to(alias)
        self.install(success=False)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_updated_pstack_collision_preserves_upstream_source(self):
        self.populate_legacy()
        path = self.legacy / "pstack/skills/how/SKILL.md"
        path.write_text(path.read_text() + "An upstream update.\n")
        contents = path.read_text()
        self.assertIn("Skill name collision", self.install(success=False).stderr)
        self.assertEqual(path.read_text(), contents)
        self.assertFalse((self.target / cli.BUNDLE).exists())

    def test_identical_nanide_duplicate_is_rejected_with_or_without_symlink(self):
        source = self.root / "skills/how"
        duplicate = self.target / "external-copy"
        duplicate.parent.mkdir(parents=True)
        shutil.copytree(source, duplicate)
        self.assertIn("Skill name collision", self.install(success=False).stderr)
        shutil.rmtree(duplicate)
        duplicate.symlink_to(source)
        self.assertIn("Skill name collision", self.install(success=False).stderr)
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
        self.assertEqual((self.root / "providers/codex/config.local.json").read_bytes(), original_config)
        backups = list((cli.state_dir(self.target) / "backups").glob("*/pstack"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / ".pstack/history").read_text(), "personal state")
        self.assertEqual((backups[0] / "node_modules/dependency.js").read_text(), "dependency")
        self.assertTrue((self.legacy / "unrelated/SKILL.md").is_file())
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertTrue(backups[0].exists())
        self.assertTrue((self.root / "providers/codex/config.local.json").exists())

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
                self.assertFalse((self.root / "providers/codex/config.local.json").exists())
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
                self.assertFalse((self.root / "providers/codex/config.local.json").exists())
                self.assertFalse(cli.exists(self.target / cli.BUNDLE))
                shutil.rmtree(self.legacy)

    def test_differing_override_stops_migration_without_overwrite(self):
        self.populate_legacy()
        override = dict(self.defaults, panel_size=3)
        self.write_json(self.root / "providers/codex/config.local.json", override)
        self.install("--migrate-from", str(self.legacy), success=False)
        self.assertEqual(json.loads((self.root / "providers/codex/config.local.json").read_text()), override)
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
        self.assertFalse((self.root / "providers/codex/config.local.json").exists())
        self.assertFalse(list(self.root.glob(".preserve-config-*")))
        self.install("--migrate-from", str(self.legacy))
        self.assertEqual(json.loads((self.root / "providers/codex/config.local.json").read_text()), self.defaults)
        self.assertEqual((self.target / cli.BUNDLE).resolve(), self.root / "skills")

    def test_configuration_publish_never_overwrites_new_override(self):
        self.populate_legacy()
        source = self.legacy / "pstack/codex-config.json"
        destination = self.root / "providers/codex/config.local.json"
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
        (self.root / "providers/codex/config.local.json").write_text("{broken")
        self.command("validate", success=False)
        self.install(success=False)
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_uninstall_works_with_broken_source_metadata(self):
        self.install()
        (self.root / "providers/codex/config.local.json").write_text("{broken")
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertFalse(cli.exists(self.target / cli.BUNDLE))

    def test_validator_checks_yaml_names_and_links_but_skips_code_examples(self):
        self.command("validate")
        path = self.root / "skills/mode/SKILL.md"
        original = path.read_text()
        path.write_text(original + "\n```md\n[example](missing.md)\n```\n`[example](missing.md)`\n")
        self.command("validate")
        path.write_text(original + "\n[broken](missing.md)\n")
        self.command("validate", success=False)
        path.write_text(original.replace("description: A test skill.", "description: invalid: scalar"))
        self.command("validate", success=False)
        path.write_text(original.replace("name: mode", "name: prepare-goal"))
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
        path = self.root / "skills/mode/SKILL.md"
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

    def test_registry_requires_exact_coverage_and_allows_native_identity_entries(self):
        path = self.root / "skill-names.json"
        mapping = json.loads(path.read_text())
        self.skill(self.root / "skills/new-workflow", "new-workflow")
        self.assertIn("exactly cover", self.command("validate", success=False).stderr)
        self.write_json(path, {**mapping, "new-workflow": "new-workflow"})
        self.command("validate")
        self.install()

    def test_registry_rejects_missing_extra_invalid_duplicate_and_prefixed_ids(self):
        path = self.root / "skill-names.json"
        mapping = json.loads(path.read_text())
        missing = dict(mapping)
        del missing["how"]
        cases = {
            "missing": missing,
            "extra": {**mapping, "extra": "nanide-absent"},
            "invalid source": {**mapping, "Bad_Source": "nanide-extra"},
            "invalid public": {**mapping, "how": "Nanide_How"},
            "nontext public": {**mapping, "how": ["nanide-how"]},
            "duplicate": {**mapping, "why": "how"},
            "prefixed": {**mapping, "how": "nanide-how"},
        }
        for label, registry in cases.items():
            with self.subTest(case=label):
                self.write_json(path, registry)
                self.assertIn("skill-names.json", self.command("validate", success=False).stderr)
        self.write_json(path, mapping)
        self.skill(self.root / "skills/nanide-extra", "nanide-extra")
        self.write_json(path, {**mapping, "extra": "nanide-extra"})
        self.assertIn("short canonical name", self.command("validate", success=False).stderr)

    def test_collection_registry_names_every_live_skill_and_preserves_source_ids(self):
        mapping = json.loads((SOURCE / "skill-names.json").read_text())
        original_brands = {
            "poteto-audit": "audit",
            "poteto-goal": "goal",
            "poteto-help": "help",
            "poteto-mode": "mode",
            "setup-pstack": "setup",
        }
        self.assertEqual({name: mapping[name] for name in original_brands}, original_brands)
        receipt = json.loads((SOURCE / "import-receipt.json").read_text())
        historical = {Path(path).parent.name for path in receipt["files"] if path.startswith("pstack/skills/") and Path(path).name == "SKILL.md"} | {"poteto-pr-description"}
        self.assertIn("poteto-pr-description/SKILL.md", receipt["files"])
        self.assertIn("poteto-pr-description", receipt["sources"])
        self.assertNotIn("poteto-pr-description", mapping)
        self.assertEqual(set(mapping), historical - {"poteto-pr-description"})
        self.assertTrue(all(public == source for source, public in mapping.items() if source not in original_brands))
        self.assertEqual(set(mapping.values()), {skill.name for skill in cli.load_collection(SOURCE).skills})
        for name in cli.RETIRED_SKILLS:
            self.assertNotIn(name, mapping.values())
            self.assertFalse((SOURCE / "skills" / name).exists())
        self.assertTrue((SOURCE / "skills/audit").exists())
        self.assertTrue((SOURCE / "skills/how").exists())

    def test_obsolete_selectors_and_paths_fail_but_shell_variables_do_not(self):
        path = self.root / "skills/mode/SKILL.md"
        original = path.read_text()
        for reference in ("Use $poteto-pr-description.", "Read ../poteto-pr-description/SKILL.md.", "Read skills/poteto-pr-description/references/descriptions.md.", "Use $nanide-pr.", "Read ../nanide-pr/SKILL.md.", "Read ../nanide-pr/references/titles.md.", "Use $nanide-pr-description.", "Read ../nanide-pr-description/SKILL.md.", "Use $poteto-mode.", "Read ../poteto-mode/SKILL.md.", "Use $setup-pstack.", "Read ../setup-pstack/SKILL.md.", "Read ../nanide-how/SKILL.md.", "Read skills/nanide-audit/."):
            with self.subTest(reference=reference):
                path.write_text(original + reference + "\n")
                self.assertIn("obsolete local skill", self.command("validate", success=False).stderr)
        path.write_text(original + "[Original helper](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md).\nUse $how and read ../how/SKILL.md.\n```sh\nhow=example\nprintf '%s' \"$how\"\n```\nExplain how this works and why.\n")
        self.command("validate")

    def test_prompt_templates_retain_collection_validation(self):
        path = self.root / "prompts/delegate.md"
        path.parent.mkdir()
        for content, message in (
            ("Use $poteto-mode.\n", "obsolete local skill"),
            ("Use Codex collaboration tools.\n", "provider-specific instructions"),
        ):
            with self.subTest(content=content):
                path.write_text(content)
                self.assertIn(message, self.command("validate", success=False).stderr)
        path.write_text("Use $mode.\n")
        self.command("validate")

    def test_registry_rejects_retired_skills_even_if_recreated(self):
        path = self.root / "skill-names.json"
        mapping = json.loads(path.read_text())
        for source, public in (("poteto-pr-description", "nanide-new-pr"), ("nanide-pr-description", "nanide-pr-description"), ("nanide-pr", "nanide-pr")):
            with self.subTest(source=source):
                self.skill(self.root / "skills" / public, public)
                self.write_json(path, {**mapping, source: public})
                self.assertIn("retired skill", self.command("validate", success=False).stderr)
                shutil.rmtree(self.root / "skills" / public)
        self.write_json(path, mapping)
        self.command("validate")

    def test_required_pr_references_cannot_be_missing(self):
        for name in ("pr-titles.md", "pr-descriptions.md", "pr-metadata.md"):
            path = self.root / "skills/mode/references" / name
            original = path.read_text()
            with self.subTest(reference=name):
                path.unlink()
                self.assertIn("Missing required reference " + str(path.relative_to(self.root)), self.command("validate", success=False).stderr)
                path.write_text(original)
        self.command("validate")

    def test_renamed_sibling_paths_resolve_through_installed_symlink(self):
        shutil.rmtree(self.root / "skills")
        shutil.copytree(SOURCE / "skills", self.root / "skills", symlinks=True)
        shutil.copytree(SOURCE / "providers", self.root / "providers", dirs_exist_ok=True, ignore=shutil.ignore_patterns("config.local.json"))
        shutil.copytree(SOURCE / "docs", self.root / "docs")
        shutil.copytree(SOURCE / "prompts", self.root / "prompts")
        shutil.copy2(SOURCE / "README.md", self.root / "README.md")
        shutil.copy2(SOURCE / "LICENSE", self.root / "LICENSE")
        self.install()
        entry = self.target / cli.BUNDLE / "mode/SKILL.md"
        real = entry.resolve()
        self.assertEqual(real, self.root / "skills/mode/SKILL.md")
        canonical = real
        discovered = list(cli.discovery_skills(self.target, set()))
        names = [skill.name for skill in discovered]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), set(json.loads((self.root / "skill-names.json").read_text()).values()))
        self.assertFalse(set(names) & set(cli.RETIRED_SKILLS))
        for name in ("pr-titles.md", "pr-descriptions.md", "pr-metadata.md"):
            reference = canonical.parent / "references" / name
            self.assertTrue(reference.is_file())
            self.assertEqual(reference.resolve(), canonical.parent / "references" / name)
        self.assertEqual(cli.markdown_links(self.root), [])
        for public in json.loads((self.root / "skill-names.json").read_text()).values():
            sibling = canonical.parent / ".." / public / "SKILL.md"
            self.assertTrue(sibling.is_file(), str(sibling))
            self.assertEqual(cli.frontmatter(sibling)["name"], public)

    def test_short_source_install_reads_live_canonical_body_and_policy(self):
        canonical = self.root / "skills/mode/SKILL.md"
        metadata = canonical.parent / "agents/openai.yaml"
        metadata.parent.mkdir()
        metadata.write_text("policy:\n  allow_implicit_invocation: false\n")
        self.command("install", "--provider", "codex")
        installed = self.target / "mode/SKILL.md"
        self.assertEqual(installed.resolve(), canonical)
        self.assertEqual(cli.frontmatter(installed)["name"], "mode")
        self.assertEqual((installed.parent / "agents/openai.yaml").read_bytes(), metadata.read_bytes())
        canonical.write_text(canonical.read_text() + "A newly edited workflow body.\n")
        self.assertIn("A newly edited workflow body.", installed.read_text())

    def test_provider_upgrade_removes_owned_long_links_from_old_layouts(self):
        for source_directory in ("skills", "providers/source-skills"):
            with self.subTest(source_directory=source_directory):
                self.target.mkdir(parents=True, exist_ok=True)
                links = {}
                for name in ("nanide-mode", "nanide-help", "setup-nanide-skills"):
                    source = self.root / source_directory / name
                    (self.target / name).symlink_to(source, target_is_directory=True)
                    links[name] = str(source)
                self.write_json(cli.state_dir(self.target) / "provider-install.json", dict(provider="codex", root=str(self.root), target=str(self.target), links=links))
                self.command("install", "--provider", "codex")
                self.assertEqual({path.name for path in self.target.iterdir()}, {"mode", "help", "goal", "audit", "setup"})
                self.assertEqual((self.target / "mode/SKILL.md").resolve(), self.root / "skills/mode/SKILL.md")
                self.command("uninstall", "--provider", "codex")

    def test_interim_router_bundle_can_upgrade_or_uninstall(self):
        self.target.mkdir(parents=True)
        destination = self.target / cli.BUNDLE
        interim = self.root / "providers/source-skills"
        destination.symlink_to(interim, target_is_directory=True)
        self.write_json(cli.state_dir(self.target) / "install.json", dict(source=str(interim), target=str(destination)))
        self.install()
        self.assertEqual(destination.resolve(), self.root / "skills")
        self.command("uninstall", "--target-dir", str(self.target))
        destination.symlink_to(interim, target_is_directory=True)
        self.command("uninstall", "--target-dir", str(self.target))
        self.assertFalse(destination.is_symlink())


if __name__ == "__main__":
    unittest.main()
