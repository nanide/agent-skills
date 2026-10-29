# Install the personal collection alongside pstack

Run `scripts/skills.py` with the Python environment prepared in the [README](../README.md). Keep the source checkout at its installed path. Moving or deleting it breaks the discovery link.

## Preview an installation

```sh
.venv/bin/python scripts/skills.py install --dry-run
```

Review the printed source, discovery directory, and actions. A dry run writes nothing. Use the same `--target-dir` for installation, switching versions, and uninstalling.

The installer checks the target directory, `~/.agents/skills`, `${CODEX_HOME:-$HOME/.codex}/skills`, and the explicit migration directory for conflicting skill names. It does not infer other clients' search paths. Check those paths separately if you configured additional discovery roots.

## Keep the original baseline installed

Run the normal install command without a migration option. Only five `poteto-*` skill IDs become `nanide-*`. The 55 generic pstack helper names stay unchanged. Installation and uninstall leave the original `pstack`, `poteto-pr-description`, `prepare-goal`, and `research-to-goal` directories in place. Each collection keeps its own model configuration. Personal choices live in this checkout's ignored `codex-config.local.json`.

The collision exception covers only unchanged helper IDs at their exact original `SKILL.md` locations under `${CODEX_HOME:-$HOME/.codex}/skills`, recorded in [the import receipt](../import-receipt.json). Their file hashes must match the receipt, and the paths cannot contain symlinks below that discovery root. Modified baseline helpers and duplicates at other paths stop installation.

Use the unique `$nanide-mode` or `$poteto-mode` entrypoint. Each resolves its own sibling helpers. Shared helpers such as `$how` and `$setup-pstack` appear twice in discovery. The standalone `$prepare-goal` and `$research-to-goal` helpers remain available only from their original directories. Select a direct helper by source path. This installation establishes no override precedence.

The installed bundle remains named `agent-skills`. Its discovery link and installer state keep the same identity when you upgrade this checkout.

## Legacy migration recovery

The explicit `--migrate-from` option remains for the former workflow that moved the customized global sources into this repository. It is not needed for side-by-side installation. Do not use it against a baseline you want to keep installed.

Migration moves only the original `pstack` and `poteto-pr-description` directories. It leaves the standalone `prepare-goal` and `research-to-goal` directories in discovery because this collection omits them. It verifies the sources it moves against [the historical import receipt](../import-receipt.json) before moving anything. The receipt still records all four original sources. A source change stops migration. It copies `pstack/codex-config.json` to ignored `codex-config.local.json`. A differing personal override stops migration.

Legacy backups include runtime data and dependencies. They live beside the discovery directory under `.agent-skills/<discovery-directory-name>/backups/`, outside skill discovery. The installer retains those backups and unrelated siblings.

## Recover an interrupted migration

Keep the printed `pending.json` path and backup paths. Rerun the same command from the same checkout with the same target and migration directory. The installer verifies originals or saved backups and resumes remaining moves. It refuses conflicting changes or missing originals and backups.

If an older pending plan includes a backup action for `prepare-goal` or `research-to-goal`, this version rejects the entire plan before making changes. Use the original installer version to resume that plan, or restore manually as described below. Restore any saved standalone goal helpers to their original discovery paths. Keep the old journal as a recovery record outside the active `pending.json` path before retrying with this version.

A lock records the installer process ID. If a lock remains after a crash, verify that process has exited before removing the lock file printed in the error. Then rerun the original command.

To restore manually, uninstall the bundle link from its source checkout. Move each saved original back to its printed source path only when that path is absent. Leave unrelated skill entries in place. Keep the migration receipt until you have checked discovery in a fresh chat.

## Switch checkouts and uninstall

Copy `codex-config.local.json` into the destination checkout if you want the same personal choices. Run that checkout's installer with the same target. Switching requires the current symlink to match the install receipt, so an arbitrary symlink cannot become managed through replacement.

Run uninstall from the checkout currently named by the bundle link. Uninstall refuses a link belonging to another checkout. It removes only the bundle link and current install receipt, and leaves migration receipts and backups for recovery.
