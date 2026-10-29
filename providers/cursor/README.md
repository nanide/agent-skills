# Cursor adapter

Install with `python3 scripts/skills.py install --provider cursor`. Personal discovery uses `~/.cursor/skills`. Use `--target-dir /path/to/project/.cursor/skills` for a project. Start a fresh session and invoke `/nanide-mode` or another public skill ID. See the official [skills documentation](https://cursor.com/docs/skills).

## Tools

Use the current subagent tool when exposed. Inspect its schema before choosing a model, background mode, or agent type. Do not assume upstream pstack's model names or registered agent types exist. Shared agent prompt files are brief templates. Follow the [shared delegation policy](../../skills/nanide-mode/references/delegation.md).

Use a native planning tool for the working checklist and the shared checkpoint for durable state. A to-do list does not establish a persistent execution loop. Use native background or cloud execution only when requested and available. Scheduling needs an explicit request and a real scheduler. Do not assume a local session will keep running after the application closes.

For worktree isolation, inspect current checkouts and use available managed tools or Git with an explicit base. Preserve ownership and dirty work during cleanup. Use only conversation history exposed to this session or supplied by the user.

## Configuration

Follow the [shared configuration precedence](../README.md#configuration). Save personal choices in `providers/cursor/config.local.json`. Keep model identifiers out of shared workflows. Missing native features use the same documented fallbacks as other adapters.
