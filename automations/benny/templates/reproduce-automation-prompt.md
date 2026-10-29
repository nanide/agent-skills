# Reproduce automation prompt

> Prompt source for a direct report run or explicitly requested Codex schedule. Verify every referenced file in the actual execution environment. Scheduling does not provide a Slack event trigger.

Read and follow `.codex/benny-pack/skills/reproduce-and-fix-issues/SKILL.md` for this run.

Configuration source. Include this repository-relative path only when it is committed in the same target repository. Otherwise paraphrase the configured values. Never use a plugin source or cache path:

```text
{{BENNY_CONFIG_PATH}}
```

Report coordinates, supplied by the user or discovered through configured Slack reads:

```json
{
	"source_channel_id": "{{SLACK_CHANNEL_ID}}",
	"ts": "{{SLACK_MESSAGE_TS}}",
	"thread_ts": "{{SLACK_THREAD_TS_OR_EMPTY}}"
}
```

For polling, discover new top-level reports in the configured channel and deduplicate them using the configured state file and existing verdicts. Do not expect an event payload from the scheduler. It should include the configured repository, default branch, issue tracker, control adapter, feature map, and draft pull request capability.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting.

Wait for a configured triage marker from the configured triage identity in this exact thread. Proceed only for `[benny:bug]` or `[benny:performance]`.

Read the configured control runbook and verify its tools before attempting a repro. Reproduce the exact discriminating symptom twice through the real UI. Verify existing pull requests or commits without authoring over them. Attempt a bounded fix only after a confirmed repro and the operational file's fix gate.

The coordinator is the only Slack poster. Every child prompt must forbid all Slack write tools and API calls. Children return findings only.

Never post a root message in the source channel.
