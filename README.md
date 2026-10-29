# Agent skills

Nanide's personal Codex skills, based on poteto's pstack workflows. Five skill names replace `poteto-` with `nanide-`. The 55 generic pstack helpers retain their original names. The source checkout is the editable installation. A detached checkout or extracted Git archive is a stable installation.

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

Install this collection alongside the original global pstack collection with the normal command above. The installer permits unchanged helpers at their recorded baseline locations and refuses unrelated duplicate names or unmanaged destination paths. See [installation and recovery](docs/installation.md).

## Use and customize

Invoke [`$nanide-mode`](skills/nanide-mode/SKILL.md) with a task and a check that can pass or fail:

```text
$nanide-mode investigate why retries create duplicate records. reproduce, fix, and verify.
```

Use `$poteto-mode` for the original baseline and `$nanide-mode` for this personal variant. Each mode resolves helpers from its own real sibling directory and reads its own configuration. Shared helpers have duplicate catalog selectors. Select a direct helper by its source path; there is no override precedence.

| Collection | Entrypoint and helper example | Source |
| --- | --- | --- |
| Original baseline | `$poteto-mode`, `$how`, `$setup-pstack` | `~/.codex/skills/pstack/skills/` |
| Personal variant | `$nanide-mode`, `$how`, `$setup-pstack` | This checkout's `skills/`, discovered through `~/.agents/skills/agent-skills` |

The original standalone skills remain at `~/.codex/skills/poteto-pr-description/`, `~/.codex/skills/prepare-goal/`, and `~/.codex/skills/research-to-goal/`. This collection includes `$nanide-pr-description`. The two standalone goal helpers remain available from their original directories. The original pstack configuration stays at `~/.codex/skills/pstack/codex-config.json`. This checkout reads its own configuration files.

Imported invocation policies remain intact. The [skill catalog](docs/catalog.md) and [workflow guide](docs/guide/README.md) describe the collection.

Model roles default to `inherit-parent`, with two independent reviewers per panel. Invoke [`$setup-pstack`](skills/setup-pstack/SKILL.md) to save personal choices in ignored `codex-config.local.json`. That complete document replaces [the portable defaults](codex-config.json). Copy it explicitly to a different checkout when switching versions.

## Improve skills while using them

Create a branch in this checkout with `git switch -c improve-skill-name`. Edit its linked source while you work in another project. Return here to review `git diff`, run validation, and commit the change. The [release guide](docs/releases.md) covers version bumps and immutable tags.

A project installation does not override a global installation. The installer refuses duplicate names outside the recorded baseline exception. Use a separate test environment or uninstall the global bundle before trying another project target.

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

The validator parses YAML, checks metadata and local Markdown links, and checks configuration and provenance. [The rename map](skill-names.json) records only the five `poteto-*` names and their `nanide-*` counterparts. Validation keeps those mapped skills present and rejects references to the renamed IDs. Generic helper names remain valid. New skills do not need a historical map entry. See [the authoring playbook](skills/nanide-mode/playbooks/authoring-a-skill.md) for instruction changes.

The [upstream record](codex-port.json) retains its pinned revision. The [import receipt](import-receipt.json) retains the historical source hashes, including the two standalone goal helpers omitted from this collection. The original [MIT license](LICENSE) and attribution remain. See [CHANGELOG.md](CHANGELOG.md) for collection changes.
