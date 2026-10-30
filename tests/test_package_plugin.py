import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile

SOURCE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_plugin", SOURCE / "scripts/package_plugin.py")
package_cli = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = package_cli
SPEC.loader.exec_module(package_cli)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "checkout"
        self.root.mkdir()
        self.git("init", "--quiet")
        self.write_json("plugin.json", {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "nanide", "version": "0.2.0", "license": "MIT",
            "extensions": {"com.openai": {"interface": {"logo": "./assets/icon.svg", "composerIcon": "./assets/icon.svg"}}},
        })
        self.write_json(".claude-plugin/plugin.json", {"name": "nanide", "version": "0.2.0"})
        for path in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json", ".cursor-plugin/marketplace.json"):
            source = {"source": "local", "path": "./"} if path.startswith(".agents/") else "./"
            catalog = {"name": "nanide", "plugins": [{"name": "nanide", "source": source}]}
            if path.startswith(".agents/"):
                catalog["plugins"][0]["policy"] = {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
            else:
                catalog["owner"] = {"name": "Maintainer"}
            self.write_json(path, catalog)
        self.write("assets/icon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32"/></svg>\n')
        self.write("skills/mode/SKILL.md", "---\nname: mode\ndescription: Test skill.\n---\n\n[Helper](references/pr-titles.md)\n")
        self.write("skills/mode/scripts/check-plan.mjs", "export {};\n")
        for name in ("pr-titles.md", "pr-descriptions.md", "pr-metadata.md"):
            self.write(f"skills/mode/references/{name}", "# Reference\n")
        self.write("README.md", "# Test collection\n\n[Skill](skills/mode/SKILL.md)\n")
        self.write("LICENSE", "MIT\n")
        self.write("prompts/example.md", "# Prompt\n")
        self.write("docs/example.md", "[Prompt](../prompts/example.md)\n")
        self.write("requirements.txt", (SOURCE / "requirements.txt").read_text())
        self.write_json("agent-config.json", {"default_model": "inherit-parent", "roles": {}, "panel_size": 2})
        self.write_json("skill-names.json", {"poteto-mode": "mode"})
        sources = ["pstack", "poteto-pr-description", "prepare-goal", "research-to-goal"]
        self.write_json("import-receipt.json", {"format": 1, "sources": sources, "files": {f"{name}/SKILL.md": "a" * 64 for name in sources}})
        self.write_json("upstream.json", {"source": "https://example.com/upstream", "commit": "b" * 40})
        for provider in ("codex", "cursor", "claude"):
            self.write_json(f"providers/{provider}/adapter.json", {
                "discovery_directory": f".{provider}/skills", "additional_discovery_directories": [],
                "environment_discovery_directories": {}, "entry_points": ["mode"],
            })
        for name in ("package_plugin.py", "skills.py", "plugin.schema.json"):
            self.write(f"scripts/{name}", (SOURCE / "scripts" / name).read_text())
        result = subprocess.run([sys.executable, str(self.root / "scripts/skills.py"), "generate-source-adapters"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.git("add", ".")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True, text=True)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def write_json(self, name, value):
        return self.write(name, json.dumps(value) + "\n")

    def run_cli(self, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/package_plugin.py"), *args],
            capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def test_archive_contains_tracked_working_tree_files_and_preserves_caller_files(self):
        self.write("docs/untracked.md", "untracked\n")
        self.write("scratch.txt", "unselected\n")
        self.git("add", "scratch.txt")
        self.write("docs/example.md", "working tree change\n")
        package = package_cli.collect_package(self.root)
        output = self.base / "release"
        output.mkdir()
        sentinel = output / "keep.txt"
        sentinel.write_text("keep\n")
        archive = package_cli.write_package(package, output)
        self.assertEqual(archive.name, "nanide-0.2.0.zip")
        with zipfile.ZipFile(archive) as release:
            names = set(release.namelist())
            self.assertIn("plugin.json", names)
            self.assertIn("prompts/example.md", names)
            self.assertIn(".agents/plugins/marketplace.json", names)
            self.assertNotIn("docs/untracked.md", names)
            self.assertNotIn("scratch.txt", names)
            self.assertEqual(release.read("docs/example.md"), b"working tree change\n")
        self.assertEqual(sentinel.read_text(), "keep\n")
        sidecar = archive.with_suffix(".zip.sha256").read_text()
        self.assertEqual(sidecar, f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")

    def test_repeated_build_is_deterministic_with_normalized_modes_and_snapshot_bytes(self):
        script = self.root / "scripts/skills.py"
        script.chmod(0o755)
        self.git("add", "scripts/skills.py")
        package = package_cli.collect_package(self.root)
        first = package_cli.write_package(package, self.base / "first")
        original = first.read_bytes()
        self.write("README.md", "changed after collection\n")
        for path in self.root.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                os.utime(path, (1700000000, 1700000000))
        second = package_cli.write_package(package, self.base / "second")
        self.assertEqual(original, second.read_bytes())
        with zipfile.ZipFile(second) as release:
            self.assertEqual(release.namelist(), sorted(release.namelist()))
            self.assertEqual({info.date_time for info in release.infolist()}, {(1980, 1, 1, 0, 0, 0)})
            self.assertEqual(stat.S_IMODE(release.getinfo("scripts/skills.py").external_attr >> 16), 0o755)
            self.assertEqual(stat.S_IMODE(release.getinfo("README.md").external_attr >> 16), 0o644)
            self.assertIn(b"Test collection", release.read("README.md"))
        self.write("README.md", "# Test collection\n\n[Skill](skills/mode/SKILL.md)\n")
        third = package_cli.write_package(package_cli.collect_package(self.root), self.base / "third")
        self.assertEqual(original, third.read_bytes())

    def test_tracked_private_content_is_rejected_even_outside_selected_roots(self):
        for name in ("providers/codex/config.local.json", "codex-config.local.json", "docs/.env.example", "outside/.env", "docs/node_modules/file", "docs/.pstack/state", "dist/old.zip", ".audit/state", "scripts/__pycache__/file.pyc", ".venv/file", "docs/.cache/file"):
            with self.subTest(path=name):
                self.write(name, "private\n")
                self.git("add", "-f", name)
                with self.assertRaisesRegex(package_cli.Invalid, "Forbidden tracked"):
                    package_cli.collect_package(self.root)
                self.git("rm", "--cached", "--", name)

    def test_untracked_private_configuration_is_omitted(self):
        self.write("providers/codex/config.local.json", "private\n")
        package = package_cli.collect_package(self.root)
        self.assertNotIn("providers/codex/config.local.json", {str(file.path) for file in package.files})

    def test_file_symlinks_become_regular_files_in_archive(self):
        link = self.root / "skills/mode/agents/openai.yaml"
        link.parent.mkdir()
        self.write("providers/codex/openai.yaml", "policy:\n  allow_implicit_invocation: false\n")
        link.symlink_to("../../../providers/codex/openai.yaml")
        self.git("add", ".")
        archive = package_cli.write_package(package_cli.collect_package(self.root), self.base / "release")
        with zipfile.ZipFile(archive) as release:
            info = release.getinfo("skills/mode/agents/openai.yaml")
            self.assertEqual(stat.S_IFMT(info.external_attr >> 16), stat.S_IFREG)
            self.assertEqual(release.read(info), b"policy:\n  allow_implicit_invocation: false\n")

    def test_unsafe_symlinks_are_rejected(self):
        external = self.base / "external.md"
        external.write_text("outside\n")
        self.write("scratch.txt", "excluded\n")
        self.git("add", "scratch.txt")
        self.write("providers/codex/config.local.json", "private\n")
        self.write("docs/untracked.md", "untracked\n")
        link = self.root / "docs/link.md"
        for target in (str(external), "../scratch.txt", "../providers/codex/config.local.json", "missing.md", "untracked.md", "../skills", "link.md"):
            with self.subTest(target=target):
                link.symlink_to(target)
                self.git("add", "docs/link.md")
                with self.assertRaises(package_cli.Invalid):
                    package_cli.collect_package(self.root)
                link.unlink()
                self.git("rm", "--cached", "docs/link.md")

    def test_missing_tracked_file_fails_before_release_write(self):
        (self.root / "README.md").unlink()
        with self.assertRaisesRegex(package_cli.Invalid, "Missing"):
            package_cli.collect_package(self.root)

    def test_manifest_drift_and_missing_assets_are_rejected(self):
        mutations = (
            (".claude-plugin/plugin.json", {"name": "nanide", "version": "9.0.0"}),
            (".claude-plugin/plugin.json", {"name": "other", "version": "0.2.0"}),
            (".claude-plugin/marketplace.json", {"name": "other", "plugins": []}),
            (".agents/plugins/marketplace.json", {"name": "nanide", "plugins": [{"name": "nanide", "source": "./"}]}),
            (".cursor-plugin/marketplace.json", {"name": "nanide", "plugins": [{"name": "nanide", "source": "../"}]}),
        )
        for path, value in mutations:
            original = (self.root / path).read_text()
            with self.subTest(path=path):
                self.write_json(path, value)
                with self.assertRaises(package_cli.Invalid):
                    package_cli.collect_package(self.root)
            self.write(path, original)
        (self.root / "assets/icon.svg").unlink()
        self.git("rm", "--cached", "assets/icon.svg")
        with self.assertRaisesRegex(package_cli.Invalid, "missing logo"):
            package_cli.collect_package(self.root)

    def test_openai_interface_requires_both_existing_local_icon_files(self):
        original = (self.root / "plugin.json").read_text()
        for key in ("logo", "composerIcon"):
            for value in (None, "", "assets/icon.svg", "https://example.com/icon.svg", "./assets/missing.svg", "./assets/../../outside.svg", "./assets"):
                with self.subTest(key=key, value=value):
                    data = json.loads(original)
                    interface = data["extensions"]["com.openai"]["interface"]
                    if value is None:
                        del interface[key]
                    else:
                        interface[key] = value
                    self.write_json("plugin.json", data)
                    with self.assertRaisesRegex(package_cli.Invalid, key):
                        package_cli.collect_package(self.root)
        data = json.loads(original)
        data["extensions"]["com.openai"] = {"logo": "./assets/icon.svg", "composerIcon": "./assets/icon.svg"}
        self.write_json("plugin.json", data)
        with self.assertRaisesRegex(package_cli.Invalid, "interface"):
            package_cli.collect_package(self.root)

    def test_optional_onboarding_requires_a_local_existing_file(self):
        original = (self.root / "plugin.json").read_text()
        for value in (None, "skills/mode/SKILL.md", "./skills/nanide-mode", "./skills/missing/SKILL.md", "./../outside.md"):
            with self.subTest(value=value):
                data = json.loads(original)
                data["extensions"]["com.openai"]["onboardingSkill"] = value
                self.write_json("plugin.json", data)
                with self.assertRaisesRegex(package_cli.Invalid, "onboardingSkill"):
                    package_cli.collect_package(self.root)
        data["extensions"]["com.openai"]["onboardingSkill"] = "./skills/mode/SKILL.md"
        self.write_json("plugin.json", data)
        package_cli.collect_package(self.root)

    def test_marketplace_owner_and_installation_policy_are_required(self):
        for path in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json", ".cursor-plugin/marketplace.json"):
            original = (self.root / path).read_text()
            with self.subTest(path=path):
                data = json.loads(original)
                if path.startswith(".agents/"):
                    del data["plugins"][0]["policy"]
                    expected = "policy"
                else:
                    data["owner"] = {"name": " "}
                    expected = "owner.name"
                self.write_json(path, data)
                with self.assertRaisesRegex(package_cli.Invalid, expected):
                    package_cli.collect_package(self.root)
                self.write(path, original)

    def test_check_writes_no_release_and_cli_build_validates_relocated_collection(self):
        output = self.base / "release"
        self.run_cli("--check", "--output-dir", str(output))
        self.assertFalse(output.exists())
        self.run_cli("--output-dir", str(output))
        relocated = self.base / "relocated"
        with zipfile.ZipFile(output / "nanide-0.2.0.zip") as release:
            release.extractall(relocated)
        shutil.rmtree(self.root)
        result = subprocess.run([sys.executable, str(relocated / "scripts/skills.py"), "validate"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validated 1 skills", result.stdout)
        native = relocated / "skills/mode/SKILL.md"
        self.assertIn("name: mode\n", native.read_text())
        self.assertFalse((relocated / "skills/nanide-mode").exists())
        router = relocated / "providers/prefixed-skills/nanide-mode/SKILL.md"
        self.assertIn("name: nanide-mode\n", router.read_text())
        self.assertEqual((router.parent / "../../../skills/mode/SKILL.md").resolve(), native.resolve())
        self.assertIn("[Helper](references/pr-titles.md)", native.read_text())
        self.assertTrue((native.parent / "references/pr-titles.md").is_file())

    def test_cli_rejects_missing_local_dependency_before_output_creation(self):
        self.write("docs/example.md", "[Missing](missing-helper.md)\n")
        output = self.base / "release"
        result = self.run_cli("--output-dir", str(output), success=False)
        self.assertIn("missing local link", result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
