#!/usr/bin/env python3
"""Build a deterministic native plugin ZIP from tracked working-tree files."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
DIRECTORIES = frozenset(("skills", "providers", "prompts", "docs", "scripts", "tests", "assets"))
FILES = frozenset((
    "README.md", "LICENSE", "agent-config.json", "skill-names.json",
    "import-receipt.json", "upstream.json", "requirements.txt", "plugin.json",
    ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
    ".agents/plugins/marketplace.json", ".cursor-plugin/marketplace.json",
))
FORBIDDEN = frozenset((
    "config.local.json", "codex-config.local.json", "node_modules", ".venv",
    ".git", ".pstack", ".audit", "dist", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".cache",
))


class Invalid(ValueError):
    pass


@dataclass(frozen=True)
class PackageFile:
    path: PurePosixPath
    contents: bytes
    executable: bool


@dataclass(frozen=True)
class Package:
    name: str
    version: str
    files: tuple[PackageFile, ...]


def forbidden(path: PurePosixPath) -> bool:
    return any(part in FORBIDDEN or part.startswith(".env") for part in path.parts) or path.suffix in {".pyc", ".pyo"}


def selected(path: PurePosixPath) -> bool:
    return str(path) in FILES or len(path.parts) > 1 and path.parts[0] in DIRECTORIES


def tracked_files(root: Path) -> dict[PurePosixPath, str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--stage", "-z"],
        capture_output=True, check=True,
    )
    tracked = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, _oid, stage = metadata.decode().split()
        path = PurePosixPath(os.fsdecode(raw_path))
        if stage != "0":
            raise Invalid(f"Resolve unmerged tracked file before packaging: {path}")
        if path.is_absolute() or ".." in path.parts:
            raise Invalid(f"Unsafe tracked path: {path}")
        if forbidden(path):
            raise Invalid(f"Forbidden tracked content must be removed from Git before release: {path}")
        tracked[path] = mode
    return tracked


def source_file(root: Path, path: PurePosixPath, members: dict[PurePosixPath, str]) -> Path:
    seen = set()
    current = path
    while True:
        if current in seen:
            raise Invalid(f"Symlink cycle: {path}")
        seen.add(current)
        source = root / current
        if any(parent.is_symlink() for parent in source.parents if parent != root and root in parent.parents):
            raise Invalid(f"Directory symlinks cannot be packaged: {path}")
        if source.is_symlink():
            target = Path(os.path.abspath(source.parent / source.readlink()))
            try:
                current = PurePosixPath(target.relative_to(root).as_posix())
            except ValueError as error:
                raise Invalid(f"Symlink escapes package root: {path}") from error
            if target.is_dir():
                raise Invalid(f"Directory symlinks cannot be packaged: {path}")
            if current not in members:
                raise Invalid(f"Symlink target must be a selected tracked file: {path} -> {current}")
            continue
        if not source.is_file():
            raise Invalid(f"Missing or non-regular tracked file: {current}")
        return source


def manifest(files: dict[str, PackageFile], path: str) -> dict:
    try:
        value = json.loads(files[path].contents)
    except (KeyError, ValueError, UnicodeError) as error:
        raise Invalid(f"Missing or invalid JSON manifest: {path}") from error
    if not isinstance(value, dict):
        raise Invalid(f"Manifest must be an object: {path}")
    return value


def collect_package(root: Path) -> Package:
    root = root.resolve(strict=True)
    members = {path: mode for path, mode in tracked_files(root).items() if selected(path)}
    files = []
    for path in sorted(members):
        if members[path] not in {"100644", "100755", "120000"}:
            raise Invalid(f"Unsupported tracked file mode {members[path]}: {path}")
        source = source_file(root, path, members)
        executable = members[PurePosixPath(source.relative_to(root).as_posix())] == "100755"
        files.append(PackageFile(path, source.read_bytes(), executable))
    canonical = manifest({str(file.path): file for file in files}, "plugin.json")
    package = Package(canonical.get("name"), canonical.get("version"), tuple(files))
    validate_package(package)
    return package


def validate_package(package: Package) -> None:
    files = {str(file.path): file for file in package.files}
    if len(files) != len(package.files):
        raise Invalid("Package contains duplicate paths")
    for file in package.files:
        if file.path.is_absolute() or ".." in file.path.parts or forbidden(file.path) or not selected(file.path):
            raise Invalid(f"Unsafe package member: {file.path}")
    canonical = manifest(files, "plugin.json")
    if package.name != "agent-skills" or not isinstance(package.version, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", package.version):
        raise Invalid("plugin.json: expected agent-skills identity and semantic version")
    if (canonical.get("name"), canonical.get("version")) != (package.name, package.version):
        raise Invalid("Package identity differs from plugin.json")
    claude = manifest(files, ".claude-plugin/plugin.json")
    if (claude.get("name"), claude.get("version")) != (package.name, package.version):
        raise Invalid("Claude plugin identity and version must match plugin.json")
    for path in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json", ".cursor-plugin/marketplace.json"):
        catalog = manifest(files, path)
        entries = catalog.get("plugins")
        if catalog.get("name") != "nanide" or not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
            raise Invalid(f"{path}: expected the nanide marketplace with one plugin")
        entry = entries[0]
        source = {"source": "local", "path": "./"} if path.startswith(".agents/") else "./"
        if entry.get("name") != package.name or entry.get("source") != source:
            raise Invalid(f"{path}: expected agent-skills@nanide with local source ./")
        if "version" in entry and entry["version"] != package.version:
            raise Invalid(f"{path}: version must match plugin.json")
        if path.startswith(".agents/"):
            if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
                raise Invalid(f"{path}: expected AVAILABLE installation and ON_INSTALL authentication policy")
        else:
            owner = catalog.get("owner")
            if not isinstance(owner, dict) or not isinstance(owner.get("name"), str) or not owner["name"].strip():
                raise Invalid(f"{path}: marketplace owner.name is required")
    extensions = canonical.get("extensions", {})
    openai = extensions.get("com.openai", {}) if isinstance(extensions, dict) else None
    if not isinstance(openai, dict):
        raise Invalid("plugin.json: extensions.com.openai must be an object")
    interface = openai.get("interface")
    if not isinstance(interface, dict):
        raise Invalid("plugin.json: extensions.com.openai.interface is required")
    paths = {key: interface.get(key) for key in ("logo", "composerIcon")}
    if "onboardingSkill" in openai:
        paths["onboardingSkill"] = openai["onboardingSkill"]
    for key, value in paths.items():
        if not isinstance(value, str) or not value.startswith("./"):
            raise Invalid(f"plugin.json: {key} must be a local file path starting with ./")
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts:
            raise Invalid(f"plugin.json: unsafe {key} path {value}")
        if str(path) not in files:
            raise Invalid(f"plugin.json: missing {key} path {value}")


def write_package(package: Package, destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f"{package.name}-{package.version}.zip"
    with tempfile.NamedTemporaryFile(dir=destination, prefix=".plugin-", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
            for file in sorted(package.files, key=lambda item: item.path):
                info = zipfile.ZipInfo(str(file.path), date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | (0o755 if file.executable else 0o644)) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                output.writestr(info, file.contents, compresslevel=9)
        digest = hashlib.sha256(temporary_path.read_bytes()).hexdigest()
        os.replace(temporary_path, archive)
    finally:
        temporary_path.unlink(missing_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="ascii", dir=destination, prefix=".digest-", delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        temporary_path.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
        os.replace(temporary_path, archive.with_suffix(".zip.sha256"))
    finally:
        temporary_path.unlink(missing_ok=True)
    return archive


def validate_collection(package: Package) -> None:
    import skills

    with tempfile.TemporaryDirectory(prefix="nanide-package-") as directory:
        root = Path(directory)
        for file in package.files:
            path = root / file.path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(file.contents)
            path.chmod(0o755 if file.executable else 0o644)
        skills.validate(skills.load_collection(root))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--check", action="store_true", help="Validate the selected package without writing release files")
    args = parser.parse_args(argv)
    try:
        package = collect_package(ROOT)
        validate_collection(package)
        if args.check:
            print(f"Validated {package.name} {package.version} with {len(package.files)} files")
        else:
            print(write_package(package, args.output_dir))
    except (Invalid, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Package error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
