# Benny

Benny provides Slack report triage and verified reproduction instructions for Codex. Triage emits one verdict in the original thread. Reproduction may prepare a small draft fix after real before-and-after evidence.

The pack is dormant. Start with [FOR_AGENTS.md](./FOR_AGENTS.md) and name the target repository. Setup copies it to `.codex/benny-pack/`, preserving local changes. Keep user configuration and maps separately under `.codex/benny/` or another explicit location. Never commit secrets.

Run a selected report directly, or explicitly request a Codex polling schedule. Codex scheduling does not provide Slack event triggers. An immediate event-driven workflow requires a separately configured service. Setup checks integrations and thread safety before enabling writes or normal traffic.

Shared pstack skills must be readable in the execution environment. Installing the pack does not create a schedule or authorize external messages, repository changes, merges, or deployment.
