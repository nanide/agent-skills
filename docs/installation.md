# Install and manage the collection

Run `scripts/skills.py` with the Python environment prepared in the [README](../README.md). Keep the source checkout at its installed path. Moving or deleting it breaks the discovery link.

## Preview an installation

```sh
.venv/bin/python scripts/skills.py install --provider <provider> --dry-run
```

Replace `<provider>` with a provider ID from the [adapter index](../providers/README.md). Review the printed source, discovery directory, and actions. A dry run writes nothing. Use the same `--target-dir` for installation, switching versions, and uninstalling.

The installer checks the selected target and the selected provider's personal discovery roots for conflicting skill names before replacing managed links. Use the selected adapter for discovery paths. Check additional custom discovery roots and other projects separately.

## Install alongside other collections

Run the normal install command without a migration option to leave other collections in place. Each collection keeps its own model configuration. Save this collection's model choices in ignored `providers/<provider>/config.local.json`.

Each live public skill ID uses `nanide-`, except `$setup-nanide-skills`. For example, use `$nanide-how`, `$nanide-interrogate`, and `$nanide-audit` instead of the old generic Nanide selectors. Use [`$nanide-mode`](../skills/nanide-mode/SKILL.md#work-on-a-pr) for PR work. The former `nanide-pr` and `nanide-pr-description` selectors are removed without aliases. Their writing instructions live in mode references. Other existing `$nanide-*` selectors keep their names. The [registry](../skill-names.json) records the source-to-public mappings for live skills and creates no runtime aliases. The old `how` selector belongs to other installed collections.

An unmanaged entry with the same public ID stops installation. Managed provider installations can point to the same canonical source. Other collections may update their generic helpers without changing Nanide installation. Model configuration stays in each collection's own checkout.

Explicit provider installations use one link per public skill ID and a receipt outside discovery. The older command without `--provider` retains the single `agent-skills` bundle link for compatibility. Uninstall that legacy bundle before installing flat links into the same discovery directory. Use the same provider and target for later operations.

## Choose a collection for the task

Explicitly invoke a Nanide skill or ask to use Nanide to select it for the current task. Keep that collection through the task's continuations unless you explicitly switch. A repository default applies only when you have not explicitly chosen a collection. Installing Nanide or asking for a generic audit or PR task alone does not select it. Reading or editing a skill is not a choice to use its workflow.

For an optional project default, add this to the project's `AGENTS.md`:

```text
When no collection has been explicitly selected for the current task, use Nanide for completion audits and PR work. Use $nanide-audit and $nanide-mode. Keep an explicit collection choice through the current task unless the user switches.
```

Selecting Nanide chooses the workflow, not permission for every PR action. A draft stays a draft, a status check stays within its requested mode, and merging follows an explicit shipping request and its gates. Editing PR guidance itself does not select its workflow.

The [selection guidance](../skills/nanide-mode/SKILL.md#select-a-collection-for-the-task) governs Nanide's helpers. Other installed collections retain their own descriptions and routing rules. This guidance does not promise deterministic host selection or suppress third-party skills. The installer stores no collection-selection state. Review [selection scenarios](collection-selection-scenarios.md) when changing these instructions.

## Migrate an installation

The legacy bundle migration is separate from provider installation. Preview it first and preserve its recovery records. See the [legacy migration instructions](../providers/codex/legacy-migration.md). It moves only recognized sources whose hashes match the import receipt. It leaves unrelated collections installed.

After migration, uninstall the managed legacy bundle before installing provider links into the same target. Uninstall retains source backups and local configuration.

## Recover an interrupted provider installation

Rerun the same provider install command from the same checkout with the same target. The `provider-install.json` receipt records both intended and prior link targets until installation completes. Repeated interruption retains those accepted targets. Finish recovery before switching to another checkout. If a managed link was changed by another actor, preserve it and resolve the conflict before retrying.

## Recover an interrupted migration

Keep the printed `pending.json` path and backup paths. Rerun the same command from the same checkout with the same target and migration directory. The installer verifies sources or saved backups and resumes remaining moves. It refuses conflicting changes or missing sources and backups.

A pending plan that includes a backup action for `prepare-goal` or `research-to-goal` is invalid. Use the manual restoration procedure below for every saved source, including those helpers. Keep the journal as a recovery record outside the active `pending.json` path before retrying.

A lock records the installer process ID. If a lock remains after a crash, verify that process has exited before removing the lock file printed in the error. Then rerun the same command.

To restore manually, uninstall the bundle link from its source checkout. Move each saved source back to its printed source path only when that path is absent. Leave unrelated skill entries in place. Keep the migration receipt until you have checked discovery in a fresh chat.

## Switch checkouts and uninstall

Copy `providers/<provider>/config.local.json` into the destination checkout if you want the same model choices. Run that checkout's installer with the same target. Switching requires the current symlink to match the install receipt, so an arbitrary symlink cannot become managed through replacement.

Run uninstall with the same provider and target from the currently installed checkout. It refuses changed managed links or another checkout's installation. It removes managed links and the current receipt while retaining migration receipts, backups, and local configuration. For the legacy bundle, omit `--provider`.
