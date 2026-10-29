# Provider adapters

Nanide keeps one canonical workflow in `skills/` and shared role defaults in [agent-config.json](../agent-config.json). Read only the adapter for the active application. Select it from the host identity, not the model family. A model supplied by another vendor does not change the host's tools.

| Application | Adapter | Personal discovery directory |
|---|---|---|
| Codex | [Codex](codex/README.md) | `~/.agents/skills` |
| Cursor | [Cursor](cursor/README.md) | `~/.cursor/skills` |
| Claude Code | [Claude Code](claude/README.md) | `~/.claude/skills` |

Run `python3 scripts/skills.py install --provider all --dry-run` to preview one global installation across all supported providers. Omit `--dry-run` to install. Use `codex`, `cursor`, or `claude` instead of `all` to select a single provider. Each installation links the same shared source. Read [installation](../docs/installation.md) for dependencies, project targets, conflicts, and recovery.

## Autocomplete entry points

The `entry_points` list in each provider’s `adapter.json` limits local discovery to `nanide-mode`, `nanide-goal`, `nanide-help`, `nanide-audit`, and `setup-nanide-skills`. The installer validates these names against the collection. An adapter without this optional list installs every skill.

Run the provider install command again to remove previously managed helper links. The source files remain in the checkout. Main workflows resolve their real source paths and read sibling helpers directly. Helpers no longer have individual autocomplete entries. To request one, ask `nanide-mode` to use the named helper.

This controls filesystem discovery, not a host visibility flag. A separately installed copy can still appear in autocomplete. Legacy bundle installations without `--provider` still expose the full collection. Follow the [legacy bundle conversion](../docs/installation.md#install-alongside-other-collections) before using this entry-point list.

## Configuration

Resolve paths from this repository's real directory, following symlinks. Read `providers/<provider>/config.local.json` when present, otherwise `providers/<provider>/config.json` when present, otherwise [agent-config.json](../agent-config.json). Each file is a complete replacement, not a merge. Reject malformed configuration instead of falling back. Keep personal model IDs in the ignored provider-local file.

The shared [delegation policy](../skills/nanide-mode/references/delegation.md) owns role resolution, panel sizing, ownership, and fallback behavior. Adapters map those choices to available host tools. Do not copy that policy into each provider folder.

## Capability contract

Every adapter supports the same skill sources, role configuration, durable checkpoints, verification requirements, and authorization boundaries. Native delegation, persistent tasks, history, scheduling, managed worktrees, and discovery-policy enforcement depend on the current host. Existing explicit-invocation metadata is retained in its adapter. Do not assume another host interprets that metadata or guarantees identical automatic selection. Use only exposed tools. If a required capability is absent, report the missing proof and continue independent work. Never present sequential self-review as independent review.

Provider-specific tool names, installation paths, metadata, and review integrations belong under the provider's folder. Discovery files may link back here when the host requires a conventional location. Shared skills express desired behavior and link this index rather than naming a service. New providers extend adapters and installation data, not copies of skills.

Support here means filesystem installation and portable workflow behavior. It does not claim hosted marketplace distribution or identical native features across applications. Run a fresh-host discovery and representative workflow check before claiming a particular application version has been tested live.
