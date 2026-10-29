# Install and manage the collection

Run `scripts/skills.py` with the Python environment prepared in the [README](../README.md). Keep the source checkout at its installed path. Moving or deleting it breaks the discovery link.

## Preview an installation

```sh
.venv/bin/python scripts/skills.py install --dry-run
```

Review the printed source, discovery directory, and actions. A dry run writes nothing. Use the same `--target-dir` for installation, switching versions, and uninstalling.

The installer checks the target directory, `~/.agents/skills`, `${CODEX_HOME:-$HOME/.codex}/skills`, and the explicit migration directory for conflicting skill names. Check any additional discovery roots separately.

## Install alongside other collections

Run the normal install command without a migration option to leave other collections in place. Each collection keeps its own model configuration. Save this collection's model choices in ignored `codex-config.local.json`.

Each live public skill ID uses `nanide-`, except `$setup-nanide-skills`. For example, use `$nanide-how`, `$nanide-interrogate`, and `$nanide-audit` instead of the old generic Nanide selectors. Use [`$nanide-mode`](../skills/nanide-mode/SKILL.md#work-on-a-pr) for PR work. The former `nanide-pr` and `nanide-pr-description` selectors are removed without aliases. Their writing instructions live in mode references. Other existing `$nanide-*` selectors keep their names. The [registry](../skill-names.json) records the source-to-public mappings for live skills and creates no runtime aliases. The old `how` selector belongs to other installed collections.

Any external skill with the same public ID stops installation, even when its bytes match this collection or it is reached through a symlink. Other collections may update their generic helpers without changing Nanide installation. Model configuration stays in each collection's own checkout.

The discovery link is named `agent-skills`. The installer uses that identity when switching checkouts.

## Choose a collection for the task

Explicitly invoke a Nanide skill or ask to use Nanide to select it for the current task. Keep that collection through the task's continuations unless you explicitly switch. A repository default applies only when you have not explicitly chosen a collection. Installing Nanide or asking for a generic audit or PR task alone does not select it. Reading or editing a skill is not a choice to use its workflow.

For an optional project default, add this to the project's `AGENTS.md`:

```text
When no collection has been explicitly selected for the current task, use Nanide for completion audits and PR work. Use $nanide-audit and $nanide-mode. Keep an explicit collection choice through the current task unless the user switches.
```

Selecting Nanide chooses the workflow, not permission for every PR action. A draft stays a draft, a status check stays within its requested mode, and merging follows an explicit shipping request and its gates. Editing PR guidance itself does not select its workflow.

The [selection guidance](../skills/nanide-mode/SKILL.md#select-a-collection-for-the-task) governs Nanide's helpers. Other installed collections retain their own descriptions and routing rules. This guidance does not promise deterministic host selection or suppress third-party skills. The installer stores no collection-selection state. Review [selection scenarios](collection-selection-scenarios.md) when changing these instructions.

## Migrate an installation

Use `--migrate-from /path/to/discovery-directory` only to move the supported source directories out of discovery. Omit this option to keep those sources installed. Preview the migration before applying it:

```sh
.venv/bin/python scripts/skills.py install --migrate-from /path/to/discovery-directory --dry-run
.venv/bin/python scripts/skills.py install --migrate-from /path/to/discovery-directory
```

Migration moves only the `pstack` and `poteto-pr-description` directories. It leaves `prepare-goal` and `research-to-goal` in discovery. The installer checks the moved sources against [the import receipt](../import-receipt.json) before moving anything. A source change stops migration. It copies `pstack/codex-config.json` to ignored `codex-config.local.json`. A differing personal override stops migration.

Backups include runtime data and dependencies. They live beside the discovery directory under `.agent-skills/<discovery-directory-name>/backups/`, outside skill discovery. The installer retains those backups and unrelated siblings.

## Recover an interrupted migration

Keep the printed `pending.json` path and backup paths. Rerun the same command from the same checkout with the same target and migration directory. The installer verifies sources or saved backups and resumes remaining moves. It refuses conflicting changes or missing sources and backups.

A pending plan that includes a backup action for `prepare-goal` or `research-to-goal` is invalid. Use the manual restoration procedure below for every saved source, including those helpers. Keep the journal as a recovery record outside the active `pending.json` path before retrying.

A lock records the installer process ID. If a lock remains after a crash, verify that process has exited before removing the lock file printed in the error. Then rerun the same command.

To restore manually, uninstall the bundle link from its source checkout. Move each saved source back to its printed source path only when that path is absent. Leave unrelated skill entries in place. Keep the migration receipt until you have checked discovery in a fresh chat.

## Switch checkouts and uninstall

Copy `codex-config.local.json` into the destination checkout if you want the same model choices. Run that checkout's installer with the same target. Switching requires the current symlink to match the install receipt, so an arbitrary symlink cannot become managed through replacement.

Run uninstall from the checkout currently named by the bundle link. Uninstall refuses a link belonging to another checkout. It removes only the bundle link and current install receipt, and leaves migration receipts and backups for recovery.
