# Agent skills

A customized collection of Codex skills, based on poteto's pstack workflows. The source checkout is the editable installation. A detached checkout or extracted Git archive is a stable installation.

## Install a development checkout

Use Python 3.9 or newer and Git. From this repository, run:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/skills.py validate
.venv/bin/python scripts/skills.py install --dry-run
.venv/bin/python scripts/skills.py install
```

The installer creates `~/.agents/skills/agent-skills` as one symlink to this checkout's `skills/` directory. Edits take effect from the same source files. Refresh discovery in a fresh Codex chat after installation. Use `--target-dir /path/to/project/.agents/skills` for a project installation.

If you have the former global pstack installation, follow [migration and recovery](docs/installation.md) before installing. A duplicate skill name stops installation. The installer preserves unrelated skills and refuses to overwrite unmanaged paths.

## Use and customize

Invoke [`$poteto-mode`](skills/poteto-mode/SKILL.md) with a task and a check that can pass or fail:

```text
$poteto-mode investigate why retries create duplicate records. reproduce, fix, and verify.
```

Imported invocation policies remain intact. The [skill catalog](docs/catalog.md) and [workflow guide](docs/guide/README.md) describe the collection. The Benny automation skills remain outside discovery under `automations/`.

Model roles default to `inherit-parent`, with two independent reviewers per panel. Invoke [`$setup-pstack`](skills/setup-pstack/SKILL.md) to save personal choices in ignored `codex-config.local.json`. That complete document replaces [the portable defaults](codex-config.json). Copy it explicitly to a different checkout when switching versions.

## Improve skills while using them

Create a branch in this checkout with `git switch -c improve-skill-name`. Edit its linked source while you work in another project. Return here to review `git diff`, run validation, and commit the change. The [release guide](docs/releases.md) covers version bumps and immutable tags.

A project installation does not override a global installation. If both expose the same names, the installer refuses the collision. Use a separate test environment or uninstall the global bundle before trying a project target.

## Install a stable version or roll back

Choose an exact commit or a release tag that exists, then follow [release and rollback instructions](docs/releases.md). This repository does not claim that a hosted release exists. Installation from another checkout switches the managed link after collision checks. Uninstall with the currently installed checkout:

```sh
.venv/bin/python scripts/skills.py uninstall --dry-run
.venv/bin/python scripts/skills.py uninstall
```

Uninstall removes the bundle link. It retains source files, personal configuration, and migration backups.

## Validate changes

```sh
.venv/bin/python scripts/skills.py validate
.venv/bin/python -m unittest discover -s tests -v
```

The validator parses YAML, checks metadata and local Markdown links, and checks configuration and provenance. See [the authoring playbook](skills/poteto-mode/playbooks/authoring-a-skill.md) for instruction changes.

The [upstream record](codex-port.json) retains its pinned revision. The [import receipt](import-receipt.json) records the customized source hashes used for migration. The original [MIT license](LICENSE) and attribution remain. See [CHANGELOG.md](CHANGELOG.md) for collection changes.
