# Agent skills

Provider-neutral skills for investigating, implementing, reviewing, and verifying engineering work. Use `$nanide-mode` to route a task through the collection's playbooks, or invoke a helper directly. The source checkout is the editable installation. A detached checkout or extracted Git archive is a stable installation.

## Install a development checkout

Use Python 3.9 or newer and Git. From this repository, run:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/skills.py validate
.venv/bin/python scripts/skills.py install --provider <provider> --dry-run
.venv/bin/python scripts/skills.py install --provider <provider>
```

Replace `<provider>` with `codex`, `cursor`, or `claude`. The installer links each skill into that application's discovery directory. All three use the same source files. Refresh discovery in a fresh session. Use `--target-dir` for a project installation. The [provider adapters](providers/README.md) contain discovery paths, invocation syntax, and native tool behavior.

The installer checks for conflicting skill names and unmanaged destination paths. See [installation and recovery](docs/installation.md) for collision rules, migration, and recovery.

## Use the skills

Invoke [`$nanide-mode`](skills/nanide-mode/SKILL.md) with a task and a check that can pass or fail:

```text
$nanide-mode investigate why retries create duplicate records. reproduce, fix, and verify.
```

`$nanide-mode` resolves helpers from its real sibling directory and reads this checkout's model configuration. All helper selectors use `nanide-`, such as `$nanide-how` and `$nanide-audit`. `$setup-nanide-skills` keeps its existing name. Old generic selectors have no Nanide aliases. See [collection selection](docs/installation.md#choose-a-collection-for-the-task) for task choices and optional repository defaults.

Use [`$nanide-mode`](skills/nanide-mode/SKILL.md#work-on-a-pr) for PR writing, creation, review, metadata, status, CI, or shipping within the requested scope. The former `nanide-pr` and `nanide-pr-description` selectors are removed without aliases. Their writing instructions live in mode references.

The [skill catalog](docs/catalog.md) and [workflow guide](docs/guide/README.md) describe the available skills and playbooks.

## Configure model roles

Model roles default to `inherit-parent`, with two independent reviewers per panel. Invoke [`$setup-nanide-skills`](skills/setup-nanide-skills/SKILL.md) to save your choices in an ignored provider-local configuration. That complete document replaces [the portable defaults](agent-config.json). Read [configuration precedence](providers/README.md#configuration). Copy it explicitly to a different checkout when switching versions.

## Improve skills while using them

Create a branch in this checkout with `git switch -c improve-skill-name`. Edit its linked source while you work in another project. Return here to review `git diff`, run validation, and commit the change. The [release guide](docs/releases.md) covers version bumps and immutable tags.

The installer rejects conflicting public skill names in checked discovery roots. Provider installations can link the same canonical sources. Use a separate test environment when validating a different checkout.

## Install a stable version or roll back

Choose an exact commit or an existing release tag, then follow [release and rollback instructions](docs/releases.md). Installation from another checkout switches the managed links after collision checks. Uninstall with the currently installed checkout:

```sh
.venv/bin/python scripts/skills.py uninstall --provider <provider> --dry-run
.venv/bin/python scripts/skills.py uninstall --provider <provider>
```

Uninstall removes the managed discovery links. It retains source files, personal configuration, and migration backups.

## Validate changes

```sh
.venv/bin/python scripts/skills.py validate
.venv/bin/python -m unittest discover -s tests -v
```

The validator parses YAML, checks metadata and local Markdown links, and checks configuration and installation records. See [the authoring playbook](skills/nanide-mode/playbooks/authoring-a-skill.md) for instruction changes.

Distributed copies must include the [MIT license](LICENSE) and its attribution.

## Shared workflows and provider support

The original [pstack](https://github.com/cursor/plugins/tree/main/pstack) informs the skill, playbook, reference, and script structure. Shared skills contain workflow decisions. [Provider adapters](providers/README.md) contain host-specific behavior and metadata. The [review notes](docs/provider-neutral-review.md) explain the changes and validation limits.
