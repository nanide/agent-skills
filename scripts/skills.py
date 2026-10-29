#!/usr/bin/env python3
"""Validate shared skills and manage provider discovery links."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Literal
from urllib.parse import unquote, urlsplit
import uuid

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = "agent-skills"
PROVIDERS = ("codex", "cursor", "claude")
LEGACY = ("pstack", "poteto-pr-description", "prepare-goal", "research-to-goal")
MIGRATION_SOURCES = ("pstack", "poteto-pr-description")
RETIRED_SKILLS = ("poteto-pr-description", "nanide-pr-description", "nanide-pr")


class Invalid(ValueError):
    pass


@dataclass(frozen=True)
class Skill:
    name: str
    source: Path


@dataclass(frozen=True)
class Collection:
    root: Path
    skills: tuple[Skill, ...]


@dataclass(frozen=True)
class Change:
    kind: Literal["preserve-config", "backup", "link", "unlink"]
    source: Path
    destination: Path

    def record(self):
        return dict(kind=self.kind, source=str(self.source), destination=str(self.destination))


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise Invalid(f"{path}: {error}") from error


def frontmatter(path: Path, strict: bool = True):
    try:
        import yaml
    except ImportError as error:
        raise Invalid("Install the declared dependencies with python3 -m pip install -r requirements.txt") from error
    try:
        text = path.read_text()
        lines = text.splitlines()
        if not lines or lines[0] != "---":
            raise Invalid(f"{path}: missing YAML frontmatter")
        end = lines.index("---", 1)
        data = yaml.safe_load("\n".join(lines[1:end]))
    except (OSError, ValueError, yaml.YAMLError) as error:
        raise Invalid(f"{path}: invalid YAML frontmatter: {error}") from error
    if not isinstance(data, dict):
        raise Invalid(f"{path}: frontmatter must be a mapping")
    name = data.get("name")
    if not isinstance(name, str) or not name.strip() or (strict and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)):
        raise Invalid(f"{path}: name must be lowercase kebab-case")
    if strict and (not isinstance(data.get("description"), str) or not data["description"].strip()):
        raise Invalid(f"{path}: description must be nonempty text")
    return data


def config(path: Path):
    data = read_json(path)
    if not isinstance(data, dict) or set(data) != {"default_model", "panel_size", "roles"}:
        raise Invalid(f"{path}: expected default_model, panel_size, and roles")
    if type(data["panel_size"]) is not int or data["panel_size"] < 1:
        raise Invalid(f"{path}: panel_size must be a positive integer")
    if data["default_model"] not in ("auto", "inherit-parent"):
        raise Invalid(f"{path}: default_model must be auto or inherit-parent")
    if not isinstance(data["roles"], dict):
        raise Invalid(f"{path}: roles must be an object")
    for role, choice in data["roles"].items():
        if not role.strip():
            raise Invalid(f"{path}: empty role name")
        choices = choice if isinstance(choice, list) else [choice]
        if not choices:
            raise Invalid(f"{path}: empty panel for {role}")
        for item in choices:
            if item in ("auto", "inherit-parent"):
                continue
            if not isinstance(item, dict) or not set(item) <= {"model", "reasoning_effort"}:
                raise Invalid(f"{path}: invalid model choice for {role}")
            if not isinstance(item.get("model"), str) or not item["model"].strip():
                raise Invalid(f"{path}: missing model for {role}")
            if "reasoning_effort" in item and item["reasoning_effort"] not in ("low", "medium", "high", "xhigh", "max", "ultra", "minimal", "none"):
                raise Invalid(f"{path}: invalid reasoning_effort for {role}")
    return data


def load_collection(root: Path) -> Collection:
    root = root.resolve()
    skills = []
    names = set()
    for path in sorted((root / "skills").rglob("SKILL.md")):
        data = frontmatter(path)
        if data["name"] != path.parent.name or data["name"] in names:
            raise Invalid(f"{path}: duplicate name or name differs from directory")
        names.add(data["name"])
        skills.append(Skill(data["name"], path.parent))
    if not skills:
        raise Invalid(f"{root}: no skills found")
    config(root / "agent-config.json")
    if exists(root / "codex-config.local.json"):
        config(root / "codex-config.local.json")
    for provider in PROVIDERS:
        for name in ("config.json", "config.local.json"):
            path = root / "providers" / provider / name
            if exists(path):
                config(path)
    return Collection(root, tuple(skills))


def import_receipt(root: Path):
    receipt = read_json(root / "import-receipt.json")
    if not isinstance(receipt, dict) or receipt.get("format") != 1 or receipt.get("sources") != list(LEGACY) or not isinstance(receipt.get("files"), dict):
        raise Invalid("Unsupported import receipt")
    for name, digest in receipt["files"].items():
        path = Path(name)
        if path.is_absolute() or not path.parts or ".." in path.parts or path.parts[0] not in LEGACY or not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise Invalid(f"Unsafe import receipt entry: {name}")
    if any(not any(Path(p).parts[0] == source for p in receipt["files"]) for source in LEGACY):
        raise Invalid("Import receipt must cover every legacy source")
    return receipt


def validate_skill_names(collection: Collection):
    mapping = read_json(collection.root / "skill-names.json")
    if not isinstance(mapping, dict) or not mapping:
        raise Invalid("skill-names.json: expected a source-to-public skill registry")
    kebab = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
    for source, public in mapping.items():
        if not isinstance(source, str) or not kebab.fullmatch(source) or not isinstance(public, str) or not kebab.fullmatch(public):
            raise Invalid("skill-names.json: source and public IDs must be lowercase kebab-case")
        if source in RETIRED_SKILLS or public in RETIRED_SKILLS:
            raise Invalid(f"skill-names.json: retired skill is reference material, not a public skill: {source}")
        if not public.startswith("nanide-") and public != "setup-nanide-skills":
            raise Invalid(f"skill-names.json: public ID must use the Nanide namespace: {public}")
    names = {skill.name for skill in collection.skills}
    if len(set(mapping.values())) != len(mapping) or set(mapping.values()) != names:
        raise Invalid("skill-names.json: public IDs must be unique and exactly cover discovered skill names")
    obsolete = (set(mapping) - names) | {"audit", *RETIRED_SKILLS}
    identifiers = "|".join(re.escape(name) for name in sorted(obsolete, key=len, reverse=True))
    selector = re.compile(rf"\$(?:{identifiers})(?![\w-])")
    local_path = re.compile(rf"(?:(?:\.\./)+|(?<![\w/])skills/)(?:{identifiers})/|/(?:{identifiers})/(?:SKILL\.md|(?:references|scripts|agents)/)")
    from markdown_it import MarkdownIt
    parser = MarkdownIt()
    documents = [collection.root / "README.md"]
    for folder in ("skills", "docs", "agents"):
        documents.extend((collection.root / folder).rglob("*"))
    for path in documents:
        if not path.is_file() or path.suffix not in {".md", ".yaml", ".sh", ".ts", ".mjs"} or any(part in {"node_modules", ".git", ".pstack"} for part in path.relative_to(collection.root).parts):
            continue
        text = path.read_text()
        selectable = text if path.suffix == ".yaml" else ""
        if path.suffix == ".md":
            selectable = "\n".join(token.content for token in parser.parse(text) if token.type == "inline" or token.type == "fence" and token.info.strip() in {"", "text", "md", "markdown"})
        local_text = re.sub(r"https?://[^\s)>]+", "", text)
        if local_path.search(local_text) or selector.search(selectable):
            raise Invalid(f"{path}: obsolete local skill selector or path")


def markdown_links(root: Path):
    try:
        from markdown_it import MarkdownIt
    except ImportError as error:
        raise Invalid("Install the declared dependencies with python3 -m pip install -r requirements.txt") from error
    parser = MarkdownIt()
    documents = [p for p in root.rglob("*.md") if not any(part in {"node_modules", ".git", ".venv", ".pstack"} for part in p.relative_to(root).parts)]
    parsed = {p: parser.parse(p.read_text()) for p in documents}
    errors = []
    for path, tokens in parsed.items():
        for token in tokens:
            for child in token.children or []:
                href = child.attrGet("href") if child.type == "link_open" else child.attrGet("src") if child.type == "image" else None
                if not href:
                    continue
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                if not target.exists():
                    errors.append(f"{path.relative_to(root)}: missing local link {href}")
                elif url.fragment and target.suffix.lower() == ".md":
                    target_tokens = parsed.get(target) or parser.parse(target.read_text())
                    slugs = set()
                    counts = {}
                    for i, heading in enumerate(target_tokens):
                        if heading.type == "heading_open":
                            title = target_tokens[i + 1].content
                            title = re.sub(r"<[^>]+>", "", title).lower()
                            slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
                            n = counts.get(slug, 0)
                            counts[slug] = n + 1
                            slugs.add(f"{slug}-{n}" if n else slug)
                    slugs.update(re.findall(r'(?:id|name)=[\"\']([^\"\']+)[\"\']', target.read_text()))
                    if unquote(url.fragment) not in slugs:
                        errors.append(f"{path.relative_to(root)}: missing anchor {href}")
    return errors


def provider_boundaries(root: Path):
    errors = []
    provider_terms = re.compile(r"\b(?:codex|claude|openai|anthropic)\b|\.cursor\b", re.IGNORECASE)
    for directory in ("skills", "agents"):
        for path in (root / directory).rglob("*"):
            if path.is_symlink() or not path.is_file() or path.suffix not in {".md", ".yaml", ".json", ".sh", ".py", ".mjs", ".ts"}:
                continue
            if any(part in {"node_modules", ".pstack"} for part in path.relative_to(root).parts):
                continue
            text = re.sub(r"https?://[^\s)>]+", "", path.read_text())
            # Adapter links identify their destination without prescribing provider behavior.
            text = re.sub(r"(?:\.\./)*providers/[^\s)`]+", "", text)
            if provider_terms.search(text) or path.suffix == ".md" and re.search(r"\bCursor\b", text):
                errors.append(f"{path.relative_to(root)}: provider-specific instructions belong in providers/")
    return errors


def validate(collection: Collection):
    import yaml
    root = collection.root
    errors = markdown_links(root) + provider_boundaries(root)
    for path in (root / "skills").rglob("SKILL.md"):
        frontmatter(path)
    for path in (root / "skills").glob("*/agents/openai.yaml"):
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as error:
            raise Invalid(f"{path}: invalid YAML: {error}") from error
        if not isinstance(data, dict) or ("policy" in data and (not isinstance(data["policy"], dict) or ("allow_implicit_invocation" in data["policy"] and type(data["policy"]["allow_implicit_invocation"]) is not bool))):
            errors.append(f"{path}: policy.allow_implicit_invocation must be boolean")
    for provider in PROVIDERS:
        adapter = adapter_config(root, provider)
        unknown = set(adapter.get("entry_points", [])) - {skill.name for skill in collection.skills}
        if unknown:
            errors.append(f"{provider}: unknown entry_points: {', '.join(sorted(unknown))}")
    manifest = read_json(root / "plugin.json")
    try:
        from jsonschema import Draft202012Validator
    except ImportError as error:
        raise Invalid("Install the declared dependencies with python3 -m pip install -r requirements.txt") from error
    schema = read_json(root / "scripts/plugin.schema.json")
    errors.extend(f"plugin.json: {error.message}" for error in Draft202012Validator(schema).iter_errors(manifest))
    if isinstance(manifest, dict) and (manifest.get("name") != BUNDLE or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", str(manifest.get("version", "")))):
        errors.append("plugin.json: expected agent-skills identity and semantic version")
    provenance = read_json(root / "upstream.json")
    if not isinstance(provenance, dict) or not isinstance(provenance.get("source"), str) or not provenance["source"].startswith("https://") or not re.fullmatch(r"[a-f0-9]{40}", provenance.get("commit", "")):
        errors.append("upstream.json: source URL and pinned upstream commit are required")
    import_receipt(root)
    validate_skill_names(collection)
    required = ("skills/nanide-mode/SKILL.md", "skills/nanide-mode/scripts/check-plan.mjs", "skills/nanide-mode/references/pr-titles.md", "skills/nanide-mode/references/pr-descriptions.md", "skills/nanide-mode/references/pr-metadata.md")
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing required reference {name}")
    if errors:
        raise Invalid("\n".join(errors))


def absolute(path: Path) -> Path:
    return Path(os.path.abspath(path.expanduser()))


def state_dir(target: Path) -> Path:
    return target.parent / ".agent-skills" / target.name


def exists(path: Path):
    return path.exists() or path.is_symlink()


def discovery_skills(directory: Path, excluded: set[Path]):
    def walk(path: Path, ancestors: frozenset[Path]):
        if path in excluded:
            return
        real = path.resolve()
        if real in ancestors:
            raise Invalid(f"Discovery symlink cycle at {path}")
        if path.is_symlink() and not path.exists():
            raise Invalid(f"Broken discovery link {path}")
        if not path.is_dir():
            return
        skill = path / "SKILL.md"
        if skill.is_file():
            yield Skill(frontmatter(skill, strict=False)["name"], skill)
        else:
            for child in sorted(path.iterdir()):
                if not child.name.startswith(".") and (child.is_dir() or child.is_symlink()):
                    yield from walk(child, ancestors | {real})
    if directory.exists():
        yield from walk(directory, frozenset())


def verify_legacy(collection: Collection, source: Path, name: str):
    receipt = import_receipt(collection.root)["files"]
    for relative, digest in receipt.items():
        parts = Path(relative).parts
        if parts[0] != name:
            continue
        path = source.joinpath(*parts[1:])
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise Invalid(f"Legacy source differs from import receipt: {path}. Preserve and review the change before migration.")
    excluded = {"node_modules", "__pycache__", ".cache", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".DS_Store", "dist", ".pstack", ".git"}
    for folder, directories, files in os.walk(source):
        directories[:] = [d for d in directories if d not in excluded]
        for entry in directories + files:
            path = Path(folder) / entry
            if entry in excluded or path.suffix in {".pyc", ".tsbuildinfo"}:
                continue
            if path.is_symlink():
                raise Invalid(f"Unimported legacy symlink: {path}")
            if path.is_file() and str(Path(name) / path.relative_to(source)) not in receipt:
                raise Invalid(f"Unimported legacy source: {path}. Preserve and import it before migration.")


def check_collisions(collection: Collection, target: Path, excluded: set[Path], migration: Path | None):
    codex_skills = absolute(Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills")
    roots = {target, absolute(Path.home() / ".agents/skills"), codex_skills}
    if migration:
        roots.add(migration)
    wanted = {s.name for s in collection.skills}
    for directory in sorted(roots):
        for skill in discovery_skills(directory, excluded):
            if skill.name in wanted:
                raise Invalid(f"Skill name collision: {skill.name} at {skill.source}. Move or rename that skill before installing.")


def plan_install(collection: Collection, target: Path, migration: Path | None) -> tuple[Change, ...]:
    if target.is_symlink():
        raise Invalid(f"Discovery directory must not be a symlink: {target}")
    dest = target / BUNDLE
    state = state_dir(target)
    discovery_roots = {target, absolute(Path.home() / ".agents/skills"), absolute(Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills")}
    if migration:
        discovery_roots.add(migration)
    if any(state.resolve() == directory.resolve() or directory.resolve() in state.resolve().parents for directory in discovery_roots):
        raise Invalid(f"Installer state and backups would be inside a discovery root: {state}. Choose a separate target directory.")
    current = read_json(state / "install.json") if (state / "install.json").exists() else None
    if exists(dest) and not (dest.is_symlink() and dest.resolve() == collection.root / "skills"):
        if not (dest.is_symlink() and current and current.get("source") == str(dest.resolve()) and current.get("target") == str(dest)):
            raise Invalid(f"Refusing to replace unmanaged entry {dest}")
    pending = state / "pending.json"
    if pending.exists():
        journal = read_json(pending)
        if journal.get("root") != str(collection.root) or journal.get("target") != str(target) or journal.get("migration") != (str(migration) if migration else None):
            raise Invalid(f"An interrupted installation needs the original command. Review {pending}")
        changes = tuple(Change(item["kind"], Path(item["source"]), Path(item["destination"])) for item in journal["changes"])
        for change in changes:
            valid = change.kind == "link" and change.source == collection.root / "skills" and change.destination == dest
            valid |= change.kind == "preserve-config" and migration is not None and change.source == migration / "pstack/codex-config.json" and change.destination in {collection.root / "providers/codex/config.local.json", collection.root / "codex-config.local.json"}
            valid |= change.kind == "backup" and migration is not None and change.source.parent == migration and change.source.name in MIGRATION_SOURCES and change.destination.name == change.source.name and change.destination.parent.parent == state / "backups"
            if not valid:
                raise Invalid(f"Unsafe interrupted action in {pending}")
    else:
        changes = []
        if migration:
            saved = state / "backups" / uuid.uuid4().hex
            for name in MIGRATION_SOURCES:
                source = migration / name
                if exists(source):
                    if source.is_symlink() or not source.is_dir():
                        raise Invalid(f"Legacy entry must be a real directory: {source}")
                    changes.append(Change("backup", source, saved / name))
            legacy_config = migration / "pstack/codex-config.json"
            if legacy_config.exists():
                changes.insert(0, Change("preserve-config", legacy_config, collection.root / "providers/codex/config.local.json"))
        if not (dest.is_symlink() and dest.resolve() == collection.root / "skills"):
            changes.append(Change("link", collection.root / "skills", dest))
        changes = tuple(changes)
    excluded = {dest}
    for change in changes:
        if change.kind == "backup":
            original, saved = change.source, change.destination
            if exists(original) and exists(saved):
                raise Invalid(f"Both original and backup exist: {original}, {saved}. Review {pending}")
            actual = original if exists(original) else saved
            if not actual.exists():
                raise Invalid(f"Original and backup are missing: {original}, {saved}")
            verify_legacy(collection, actual, original.name)
            excluded.add(original)
        elif change.kind == "preserve-config":
            source = config_source(change, changes)
            config(source)
            if exists(change.destination) and (change.destination.is_symlink() or change.destination.read_bytes() != source.read_bytes()):
                raise Invalid(f"A differing local configuration exists: {change.destination}. Preserve and reconcile it before migration.")
    check_collisions(collection, target, excluded, migration)
    return changes


def write_json(path: Path, value):
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        with temporary.open("x") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def installation_lock(target: Path):
    state = state_dir(target)
    state.mkdir(parents=True, exist_ok=True)
    path = state / "lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise Invalid(f"Installation lock exists: {path}. Verify its recorded process has exited before removing this lock.") from error
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(str(os.getpid()) + "\n")
        yield
    finally:
        path.unlink()


def config_source(change: Change, changes: tuple[Change, ...]) -> Path:
    if change.source.exists():
        return change.source
    backups = [c for c in changes if c.kind == "backup" and c.source == change.source.parent]
    return backups[0].destination / change.source.name if backups else change.source


def preserve_config(source: Path, destination: Path):
    contents = source.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(".preserve-config-" + uuid.uuid4().hex)
    try:
        with temporary.open("xb") as stream:
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError as error:
            if destination.is_symlink() or destination.read_bytes() != contents:
                raise Invalid(f"A differing local configuration appeared during installation: {destination}") from error
    finally:
        temporary.unlink(missing_ok=True)


def apply_install(collection: Collection, target: Path, migration: Path | None, changes: tuple[Change, ...]):
    state = state_dir(target)
    pending = state / "pending.json"
    if not pending.exists():
        write_json(pending, dict(root=str(collection.root), target=str(target), migration=str(migration) if migration else None, changes=[c.record() for c in changes]))
    try:
        for change in changes:
            if change.kind == "preserve-config":
                preserve_config(config_source(change, changes), change.destination)
            elif change.kind == "backup":
                if exists(change.source):
                    if exists(change.destination):
                        raise Invalid(f"Backup destination appeared during installation: {change.destination}")
                    verify_legacy(collection, change.source, change.source.name)
                    change.destination.parent.mkdir(parents=True, exist_ok=True)
                    change.source.rename(change.destination)
                elif not exists(change.destination):
                    raise Invalid(f"Original disappeared without its planned backup: {change.source}. Review {pending}")
            elif change.kind == "link":
                target.mkdir(parents=True, exist_ok=True)
                temporary = target / (".agent-skills-link-" + uuid.uuid4().hex)
                try:
                    temporary.symlink_to(change.source, target_is_directory=True)
                    os.replace(temporary, change.destination)
                finally:
                    temporary.unlink(missing_ok=True)
        if any(c.kind == "preserve-config" and c.destination == collection.root / "codex-config.local.json" for c in changes):
            migrate_config(collection.root, False)
        write_json(state / "install.json", dict(source=str(collection.root / "skills"), target=str(target / BUNDLE)))
        if any(c.kind == "backup" for c in changes):
            pending.rename(state / ("migration-" + uuid.uuid4().hex + ".json"))
        else:
            pending.unlink()
    except BaseException:
        print(f"Installation interrupted. Recovery plan: {pending}", file=sys.stderr)
        raise


def plan_uninstall(collection: Collection, target: Path):
    dest = target / BUNDLE
    if not exists(dest):
        return ()
    if not dest.is_symlink() or dest.resolve() != collection.root / "skills":
        raise Invalid(f"Refusing to remove another installation: {dest}")
    return (Change("unlink", dest, collection.root / "skills"),)



def adapter_config(root: Path, provider: str):
    path = root / "providers" / provider / "adapter.json"
    adapter = read_json(path)
    required = {"discovery_directory", "additional_discovery_directories", "environment_discovery_directories"}
    if not isinstance(adapter, dict) or not required <= set(adapter) or set(adapter) - required - {"entry_points"} or not isinstance(adapter["additional_discovery_directories"], list):
        raise Invalid(f"Invalid provider adapter: {path}")
    if "entry_points" in adapter:
        entries = adapter["entry_points"]
        if not isinstance(entries, list) or not entries or any(not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) for name in entries) or len(set(entries)) != len(entries):
            raise Invalid(f"Invalid entry_points in {path}")
    environments = adapter["environment_discovery_directories"]
    if not isinstance(environments, dict) or any(not re.fullmatch(r"[A-Z_][A-Z_0-9]*", key) for key in environments):
        raise Invalid(f"Invalid provider environment directories: {path}")
    directories = [adapter["discovery_directory"], *adapter["additional_discovery_directories"], *environments.values()]
    for value in directories:
        if not isinstance(value, str) or not value or Path(value).is_absolute() or ".." in Path(value).parts:
            raise Invalid(f"Invalid discovery directory in {path}")
    return adapter


def provider_target(provider: str) -> Path:
    return Path.home() / adapter_config(ROOT, provider)["discovery_directory"]


def migrate_config(root: Path, dry_run: bool):
    source = root / "codex-config.local.json"
    destination = root / "providers/codex/config.local.json"
    if not exists(source):
        return
    if source.is_symlink():
        raise Invalid(f"Refusing to migrate a symlinked configuration: {source}")
    config(source)
    if exists(destination) and (destination.is_symlink() or destination.read_bytes() != source.read_bytes()):
        raise Invalid(f"Differing provider configuration exists: {destination}. Reconcile it before migration.")
    print(f"migrate-config: {source} -> {destination}")
    if not dry_run:
        preserve_config(source, destination)
        source.unlink()


def install_provider(collection: Collection, provider: str, target: Path, command: str, dry_run: bool):
    if target.is_symlink():
        raise Invalid(f"Discovery directory must not be a symlink: {target}")
    adapter = adapter_config(collection.root, provider)
    roots = {target, absolute(Path.home() / adapter["discovery_directory"])}
    roots.update(absolute(Path.home() / value) for value in adapter["additional_discovery_directories"])
    roots.update(absolute(Path(os.environ[key]) / value) for key, value in adapter["environment_discovery_directories"].items() if os.environ.get(key))
    state = state_dir(target)
    record = state / "provider-install.json"
    if any(state.resolve() == directory.resolve() or directory.resolve() in state.resolve().parents for directory in roots):
        raise Invalid("Installer state must be outside the discovery directory")
    print(f"Provider: {provider}\nDiscovery directory: {target}")

    def run():
        previous = read_json(record) if record.exists() else None
        if previous and (previous.get("provider") != provider or previous.get("target") != str(target)):
            raise Invalid(f"Another provider owns this installation: {record}")
        if previous and "prior_links" in previous and previous.get("root") != str(collection.root):
            raise Invalid(f"Resume the interrupted provider installation from its original checkout: {record}")
        owned = previous.get("links", {}) if previous else {}
        if not isinstance(owned, dict) or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or not isinstance(source, str) for name, source in owned.items()):
            raise Invalid(f"Invalid installation record: {record}")
        entries = set(adapter.get("entry_points", [skill.name for skill in collection.skills]))
        desired = {skill.name: str(skill.source) for skill in collection.skills if skill.name in entries} if command == "install" else {}
        if command == "install":
            validate(collection)
        elif previous and previous.get("root") != str(collection.root):
            raise Invalid(f"Refusing to uninstall another checkout: {record}")
        prior_links = previous.get("prior_links", {}) if previous else {}
        if not isinstance(prior_links, dict) or not set(prior_links) <= set(owned) or any(not isinstance(source, str) for source in prior_links.values()):
            raise Invalid(f"Invalid recovery links: {record}")
        for name, source in owned.items():
            destination = target / name
            allowed = {source, prior_links.get(name, source)}
            if exists(destination) and (not destination.is_symlink() or str(destination.resolve()) not in allowed):
                raise Invalid(f"Managed link changed; preserve and review it: {destination}")
        for name, source in desired.items():
            destination = target / name
            if exists(destination) and name not in owned:
                raise Invalid(f"Refusing to replace unmanaged entry {destination}")
        excluded = {target / name for name in owned}
        wanted = set(desired)
        for directory in roots:
            for skill in discovery_skills(directory, excluded):
                if skill.name in wanted:
                    raise Invalid(f"Skill name collision: {skill.name} at {skill.source}")
        changes = [Change("unlink", target / name, Path(source)) for name, source in owned.items() if name not in desired]
        changes.extend(Change("link", Path(source), target / name) for name, source in desired.items() if not (target / name).is_symlink() or (target / name).resolve() != Path(source))
        for change in changes:
            print(f"{change.kind}: {change.source} -> {change.destination}")
        if dry_run:
            return
        # Persist ownership before links so an interrupted installation can resume.
        if command == "install":
            write_json(record, dict(provider=provider, root=str(collection.root), target=str(target), links={**owned, **desired}, prior_links={**owned, **prior_links}))
        target.mkdir(parents=True, exist_ok=True)
        for change in changes:
            if change.kind == "unlink":
                change.source.unlink(missing_ok=True)
            else:
                temporary = target / (".agent-skills-link-" + uuid.uuid4().hex)
                try:
                    temporary.symlink_to(change.source, target_is_directory=True)
                    os.replace(temporary, change.destination)
                finally:
                    temporary.unlink(missing_ok=True)
        if command == "install":
            write_json(record, dict(provider=provider, root=str(collection.root), target=str(target), links=desired))
        else:
            record.unlink(missing_ok=True)
    if dry_run:
        run()
    else:
        with installation_lock(target):
            run()
    return 0

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "install", "uninstall", "migrate-config"))
    parser.add_argument("--provider", choices=(*PROVIDERS, "all"))
    parser.add_argument("--target-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--migrate-from", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.migrate_from and args.command != "install":
            raise Invalid("--migrate-from is only valid with install")
        if args.command == "migrate-config":
            if args.provider or args.target_dir:
                raise Invalid("migrate-config operates on this checkout, without provider or target options")
            migrate_config(ROOT, args.dry_run)
            return 0
        if args.provider == "all" and (args.command not in {"install", "uninstall"} or args.target_dir or args.migrate_from):
            raise Invalid("--provider all supports global install or uninstall without --target-dir or --migrate-from")
        collection = Collection(ROOT, ()) if args.command == "uninstall" else load_collection(ROOT)
        if args.command == "validate":
            validate(collection)
            print(f"Validated {len(collection.skills)} skills in {collection.root}")
            return 0
        if args.provider == "all":
            targets = [(provider, absolute(provider_target(provider))) for provider in PROVIDERS]
            for provider, target in targets:
                install_provider(collection, provider, target, args.command, True)
            if not args.dry_run:
                for provider, target in targets:
                    install_provider(collection, provider, target, args.command, False)
            return 0
        if args.provider:
            if args.migrate_from:
                raise Invalid("Use the legacy bundle installer for --migrate-from, then install provider links.")
            target = absolute(args.target_dir or provider_target(args.provider))
            return install_provider(collection, args.provider, target, args.command, args.dry_run)
        target = absolute(args.target_dir or Path.home() / ".agents/skills")
        migration = absolute(args.migrate_from) if args.migrate_from else None
        if migration and (migration == target or migration in target.parents or target in migration.parents):
            raise Invalid("Migration and target discovery directories must be separate")
        print(f"Collection: {collection.root}\nDiscovery directory: {target}")
        def run():
            if args.command == "install":
                validate(collection)
                changes = plan_install(collection, target, migration)
            else:
                if (state_dir(target) / "pending.json").exists():
                    raise Invalid(f"Resume the interrupted install before uninstalling: {state_dir(target) / 'pending.json'}")
                changes = plan_uninstall(collection, target)
            for change in changes:
                print(f"{change.kind}: {change.source} -> {change.destination}")
            if not changes:
                print("Already in the requested state.")
            if not args.dry_run:
                if args.command == "install":
                    apply_install(collection, target, migration, changes)
                else:
                    for change in changes:
                        change.source.unlink()
                    (state_dir(target) / "install.json").unlink(missing_ok=True)
        if args.dry_run:
            run()
        else:
            with installation_lock(target):
                run()
        return 0
    except (Invalid, OSError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
