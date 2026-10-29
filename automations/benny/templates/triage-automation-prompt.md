# Triage automation prompt

> Prompt source for a direct report run or explicitly requested Codex schedule. Verify every referenced file in the actual execution environment. Scheduling does not provide a Slack event trigger.

Read and follow `.codex/benny-pack/skills/triage-issue-reports/SKILL.md` for this run.

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

For polling, discover new top-level reports in the configured channel and deduplicate them using the configured state file and existing verdicts. Do not expect an event payload from the scheduler.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting or writing to the issue tracker.

The committed operational file owns classification, attachment review, cause tracing, routing, dedupe, tracker writes, and the final verdict. Post no progress messages. Never post a root message in the source channel.

The coordinator is the only Slack poster. Any delegated worker must be read-only, return findings only, and receive an explicit ban on every Slack write action.

End the single verdict with exactly one configured marker:

```text
[benny:bug]
[benny:performance]
[benny:other]
```

A bug or performance marker may add `tracker=<URL>`.
