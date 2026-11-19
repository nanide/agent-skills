# Claude Code adapter

For plugin installation, follow the [plugin guide](../../docs/plugins.md).

For a source checkout, install with `python3 scripts/skills.py install --provider claude`. Personal discovery uses `~/.claude/skills`. Use `--target-dir /path/to/project/.claude/skills` for a project. Start a fresh session and invoke `/nanide-mode` or another installed entry point. See the official [skills documentation](https://code.claude.com/docs/en/skills). Source installs use `/nanide-mode`. Plugin installs use `/nanide:mode`. Other Claude products are not covered by this adapter.

See [autocomplete entry points](../README.md#autocomplete-entry-points) for the installed list and helper access.

## Tools

Use the available subagent tool and its current schema. Shared prompt templates do not register custom agents. Pass the selected skill's real path and required context explicitly. Use only supported model and effort settings. See the official [subagent documentation](https://code.claude.com/docs/en/sub-agents) and the [shared delegation policy](../../skills/mode/references/delegation.md).

For a fresh assignment, select a non-fork subagent. A fork inherits the parent conversation. For a continuation, use the existing agent ID when the active tool supports it. Report any inherited history or uncertainty about what the agent received.

Use native task lists when available and a durable checkpoint for resumable work. A task list is not a native Goal or scheduler. If persistent execution is unavailable, continue within the active session and leave the next action in the checkpoint. Future runs need an explicit request and an available scheduling facility.

Use native worktree isolation when exposed, otherwise Git with an explicit base and ownership record. Preserve dirty work and required processes before cleanup. Read only history supplied by the user or exposed through authorized tools. Do not infer complete transcripts from summaries.

## Configuration

Follow the [shared configuration precedence](../README.md#configuration). Save personal choices in `providers/claude/config.local.json`. Unsupported overrides follow the shared fallback policy. Independent review requires a separate reviewer, even when its model matches the parent.
