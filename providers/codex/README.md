# Codex adapter

Install with `python3 scripts/skills.py install --provider codex`. Personal discovery uses `~/.agents/skills`. Use `--target-dir /path/to/project/.agents/skills` for a project. Refresh discovery in a new session. Invoke `$nanide-mode` or another public skill ID. See the official [skills documentation](https://developers.openai.com/codex/skills/).

Provider-specific UI and invocation metadata lives under `skills/` in this folder. Conventional `agents/openai.yaml` entries in the shared skills link to it. Preserve these policies when editing instructions.

## Tools

Use the exposed collaboration tools for spawning, messaging, inspection, and waiting. Check the current schema for model overrides and inheritance restrictions. Omit model and effort overrides for inherited roles. Shared agent prompt files are brief templates, not registered agent types.

Read [execution state](execution-state.md) when native Goals, scheduling, managed worktrees, command sessions, or artifact attachments are involved. These tools vary across hosts. Their absence does not prevent ordinary local work or durable checkpoints.

Use scoped conversation tools only when available and authorized. A summary is not a complete transcript. Do not scan unrelated private history to compensate for a missing tool.

## Configuration and migration

Follow the [shared configuration precedence](../README.md#configuration). Personal choices belong in `providers/codex/config.local.json`. Run `python3 scripts/skills.py migrate-config --dry-run`, then omit `--dry-run`, to move an existing root `codex-config.local.json` there. The command preserves bytes, refuses a conflicting destination, and removes the old file only after a successful copy. Legacy import receipts remain provenance, not active instructions.
