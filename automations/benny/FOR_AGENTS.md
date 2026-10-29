# benny automation intent

## what i want to automate

i want two Codex workflows that work together in one slack issue channel.

### automation 1: triage issue reports

- input: a new top-level report in my configured source Slack channel. Process the report directly or discover it through an explicitly configured polling schedule, keeping its original thread coordinates.
- behavior: i want it to read the thread and attachments, classify the report as a bug or performance issue, feature request, question or feedback, or reroute, and trace the likely owning layer before routing.
- tracker: i want it to search my configured tracker for duplicates, update a confident duplicate, and create a ticket only for a clear net-new bug.
- tools: i want slack thread read and reply access, my configured tracker integration, and my optional routing map.
- outcome: i want exactly one reply in the source thread with a short verdict and `[benny:bug]`, `[benny:performance]`, or `[benny:other]`. a bug or performance marker may include the tracker url.
- boundary: i never want this automation to post a root message in the source channel.

### automation 2: reproduce and fix confirmed bugs

- input: i want this workflow to use the same new top-level report, or a discovered report from an explicitly requested polling schedule, then wait for the trusted triage marker in the original thread.
- gates: i want it to stop when someone clearly owns the fix. if an existing pull request or merged commit may fix the report, i want verification instead of a competing change.
- behavior: i want it to use my configured control adapter and feature map, reproduce the exact symptom twice through the real ui, and capture screenshots, video, and a read-only state cross-check.
- fix: i want it to verify existing pull requests without authoring over them. after a confirmed repro, it may attempt one bounded root-cause fix, use tdd when the test is cheap, smoke the blast radius, and open a draft pull request only when before-and-after proof passes.
- tools: i want slack thread read and reply access, repository and history access, draft pull request creation, my configured tracker, and my control adapter.
- outcome: i want evidence and a verified result in the source or optional operations threads, plus an optional draft pull request. updates should be concise.
- boundary: i never want this automation to post a root message in the source channel.

### shared rules

- i want the source channel and root thread coordinates to stay immutable for the whole run.
- i treat utility and debug bots as evidence, not delegation or fix ownership.
- i allow subagents to help, but they cannot post to slack or receive slack credentials.
- i want this entire pack committed at `.codex/benny-pack/` in the target repository. its `SKILL.md` files are direct automation instructions, not registered plugin skills.
- i want the installed Codex pstack skill root recorded in configuration and its shared dependencies verified in the actual execution environment.
- i want each live automation prompt to read its committed operational file directly. i do not want plugin cache paths, copied excerpts, or slash-skill discovery.
- i keep user-owned configuration, feature maps, routing maps, and secrets outside `.codex/benny-pack/` so pack refreshes cannot overwrite them.
- i want both automations to fail closed when channel coordinates, tracker access, the control adapter, or the feature map are missing or uncertain.
- i want draft pull requests only. do not merge or deploy.

### my configuration

- source slack channel: `<channel>`
- optional operations channel: `<channel or none>`
- repository and default branch: `<repo>`, `<branch>`
- tracker: `<type, team, project, labels, intake status>`
- routing map: `<path or none>`
- triage identity: `<slack identity>`
- control runbook: `<path describing available tools and repository commands>`
- feature map: `<committed same-repo path outside the copied pack, or behavior to paraphrase>`
- models: `<inherit-parent by default; supported overrides only>`
- status emoji strings: `<seen, reproducing, reproduced, blocked, fixing, failed, pull request opened>`
- budgets: `<polling, verdict wait, follow-up, repro, rejection, fix>`
- optional bot token capability: `<none, file download, or editable operations status>`

start from [`configuration.example.yaml`](./templates/configuration.example.yaml) and [`feature-map.example.md`](./skills/reproduce-and-fix-issues/references/feature-map.example.md). copy and fill them outside this pack, for example under `.codex/benny/`. keep secret values in a secret manager or environment.

## For the agent

Read `skills/setup-benny/SKILL.md` and follow its copy, configuration, integration, execution, and test steps. Resolve the target repository from the request. Preserve local files and user configuration. Do not create plugin settings.

Codex automation tools support schedules, not Slack event triggers. Preserve that distinction when discussing the desired behavior. Do not create or update a schedule unless the user requests it. Existing schedules should be updated rather than duplicated. Required integrations and external write scope must be explicit.

Use the copied operational files and completed templates as prompt sources. Verify every referenced path in the execution environment. A fresh checkout requires committed files; a local heartbeat can read the configured local paths. The current chat loading a dependency is not proof that an automation can load it.

Do not merge or deploy. Keep draft fixes within the configured repository and budget. Report unavailable evidence honestly.
