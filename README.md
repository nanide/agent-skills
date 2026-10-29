# Agent skills

Codex skills for investigating, implementing, reviewing, and verifying engineering work. Use `$nanide-mode` to route a task through the collection's playbooks, or invoke a helper directly. The source checkout is the editable installation. A detached checkout or extracted Git archive is a stable installation.

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

The installer checks for conflicting skill names and unmanaged destination paths. See [installation and recovery](docs/installation.md) for collision rules, migration, and recovery.

## Use the skills

Invoke [`$nanide-mode`](skills/nanide-mode/SKILL.md) with a task and a check that can pass or fail:

```text
$nanide-mode investigate why retries create duplicate records. reproduce, fix, and verify.
```

`$nanide-mode` resolves helpers from its real sibling directory and reads this checkout's model configuration. If another collection exposes the same helper name, select a direct helper by its source path. Duplicate catalog selectors establish no override precedence.

The [skill catalog](docs/catalog.md) and [workflow guide](docs/guide/README.md) describe the available skills and playbooks.

## Configure model roles

Model roles default to `inherit-parent`, with two independent reviewers per panel. Invoke [`$setup-nanide-skills`](skills/setup-nanide-skills/SKILL.md) to save your choices in ignored `codex-config.local.json`. That complete document replaces [the portable defaults](codex-config.json). Copy it explicitly to a different checkout when switching versions.

## Improve skills while using them

Create a branch in this checkout with `git switch -c improve-skill-name`. Edit its linked source while you work in another project. Return here to review `git diff`, run validation, and commit the change. The [release guide](docs/releases.md) covers version bumps and immutable tags.

A project installation does not override a global installation. The installer refuses duplicate names outside its recorded collision exception. Use a separate test environment or uninstall the global bundle before trying another project target.

## Install a stable version or roll back

Choose an exact commit or an existing release tag, then follow [release and rollback instructions](docs/releases.md). Installation from another checkout switches the managed link after collision checks. Uninstall with the currently installed checkout:

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

The validator parses YAML, checks metadata and local Markdown links, and checks configuration and installation records. See [the authoring playbook](skills/nanide-mode/playbooks/authoring-a-skill.md) for instruction changes.

Distributed copies must include the [MIT license](LICENSE) and its attribution.
