# Legacy bundle migration

This compatibility path handles the customized source collection recorded in [import-receipt.json](../../import-receipt.json). It is not a way to import arbitrary current upstream versions.

```sh
.venv/bin/python scripts/skills.py install --migrate-from /path/to/discovery-directory --dry-run
.venv/bin/python scripts/skills.py install --migrate-from /path/to/discovery-directory
```

Use a separate `--target-dir` when needed. Migration moves only `pstack` and `poteto-pr-description`, after checking source hashes. It leaves `prepare-goal` and `research-to-goal` in place. The legacy source `pstack/codex-config.json` is preserved as `providers/codex/config.local.json`. A differing local override stops migration.

Backups retain runtime data and dependencies. They live beside the discovery directory under `.agent-skills/<discovery-directory-name>/backups/`, outside discovery. Follow [recovery](../../docs/installation.md#recover-an-interrupted-migration) after interruption. Do not discard pending journals or backups.

To switch an existing bundle to flat provider links, uninstall the legacy bundle using its installed checkout and target, then install with `--provider codex` and the same target. Preview both operations. Uninstall retains source files, configuration, and backups.
