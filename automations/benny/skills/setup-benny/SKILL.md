---
name: setup-benny
description: Configure Benny's Slack triage and reproduction workflows for Codex, including required integrations and explicitly requested schedules.
---

# Set up Benny

Benny is a dormant pack of instructions. Installation does not create schedules, connect accounts, or grant write permissions. Read `../../FOR_AGENTS.md` for intent. The operational files are read directly and are not registered agent roles.

## 1. Install the pack and resolve dependencies

Resolve the requested target repository from context. Ask only when it is unclear. Copy the pack containing `FOR_AGENTS.md` to `<repository>/.codex/benny-pack/`. This is a data directory, not Codex's personal scheduler directory. Preserve destination-only files and merge differing source-managed files without discarding local changes. Keep user configuration outside the copied pack.

Verify the setup, operational files, references, and templates exist. Resolve the installed personal pstack skill root, normally `~/.codex/skills/pstack/skills`, and record it in the external configuration. Verify how, why, tdd, unslop, and every principle used by the operational files are readable in the actual execution environment. Do not create plugin settings or assume the current session's loaded skills will be present in another host.

Use stable repository paths for the copied pack. A local heartbeat may use local files. A standalone checkout must have every needed repository file committed on the selected branch. Verify the files under the actual execution identity. Follow the user's authorization and repository workflow for commits.

## 2. Adapt the configuration

Open these copied examples:

- `../../templates/configuration.example.yaml`
- `../reproduce-and-fix-issues/references/feature-map.example.md`

Create user-owned copies outside `.codex/benny-pack/`. These are configuration files, not pack files. Example locations:

- Project config, such as `.codex/benny/configuration.yaml`
- Project feature map, such as `.codex/benny/feature-map.md`
- Project routing map, such as `.codex/benny/routing.md`
- User config, such as `~/.config/benny/configuration.yaml`
- User feature map, such as `~/.config/benny/feature-map.md`

Fill one feature-map section for every user-facing feature the automation may reproduce. Keep it at the user point of view. Do not freeze implementation details or current code paths in the map.

Do not edit the copied examples. Pack refreshes may update source-managed files after conflict review, but they must never touch the user-owned copies.

Prefer committed, secret-free files in the target repository when a fresh automation checkout must read them. Otherwise paraphrase the required values into the live prompt. Verify each referenced path is readable in the actual execution environment. A fresh checkout requires committed files on its selected branch.

Use stable repository-relative paths for committed pack and configuration files. Never reference the plugin source directory or a plugin cache path from a live automation.

## 3. Fill the required choices

Ask for or confirm:

- Source Slack channel ID
- Optional operations or status channel ID
- Repository URL and default branch
- Triage identity or Slack user ID
- Issue tracker type, team, project, labels, and intake status
- Tracker runbook path with the available MCP actions or CLI commands
- Optional routing map path
- Required control runbook path
- Required user-facing feature-map path
- Status emoji strings
- Pull request URL format
- Polling and effort budgets
- Model slug for triage, repro, code work, and media review

Default delegated roles to inherit-parent. Validate explicit model and reasoning choices against the current tool schema. Read pstack's codex-config.json for delegation defaults. Scheduled job model fields follow automation_update's schema separately.

The source channel, triage identity, repository, tracker adapter, control runbook, and feature map must be explicit. Fail setup if any required value stays ambiguous.

Use pstack's `unslop` skill on the final automation names, descriptions, and prompt shims before saving them.

When updating an existing configuration, replace `control.skill_name` with `control.runbook_path` and `tracker.adapter_skill_name` with `tracker.runbook_path`. Write the actual required commands and tool actions into those runbooks after inspecting the existing configuration and repository. Do not merely rename a skill identifier into a path. Resolve relative runbook and feature-map paths against the configured repository checkout. Verify the runbooks and their capabilities before enabling execution.

## 4. Check integration capabilities

The triage automation needs:

- Read access to the configured source Slack channel and its threads
- Thread-reply access in that channel
- Attachment metadata and file download access when reports include media
- Search, read, create, and update access through the configured issue-tracker adapter

The repro automation needs:

- Read access to the source thread
- Thread-reply access in the source channel
- Optional post and edit access in the configured operations channel
- Repository read and history access
- A pull request action that can open a draft pull request
- The configured control runbook and its required tools

Prefer connected Slack tools for reads and posts. The optional `BENNY_SLACK_BOT_TOKEN` may fill a narrow gap such as editing one operations status message or downloading an attachment. Store the value in a secret manager or environment, not in YAML.

Do not use undocumented integration endpoints.

## 5. Prepare the routing map

If the user wants reroutes or owner pings:

1. Copy `../triage-issue-reports/references/routing.example.md` outside `.codex/benny-pack/`.
2. Replace every placeholder with public or organization-local values.
3. Keep owner pings off by default.
4. Allow a ping only for a configured feature owner or a confirmed likely regression author.

If no routing map is configured, triage may classify a report but must not guess a destination or owner.

## 6. Verify the control adapter

Read `../reproduce-and-fix-issues/references/control-adapter.md` and the user's completed feature map.

Confirm that the named skill can:

- Bring up the target app
- Navigate every mapped feature through the real UI
- Exercise mapped states through declared adapter actions
- Inspect state without forcing the result
- Capture screenshots
- Start and stop a recording
- Clean up its processes and temporary data

If any capability is missing, leave the repro automation disabled. It must fail closed rather than claim a reproduction it did not perform.

## 7. Choose the supported execution path

Codex's automation tool provides scheduled runs. It does not expose a Slack event trigger or webhook receiver. Do not create fictional trigger fields or promise event delivery.

Choose the path that matches the user's request:

- Run one explicitly selected Slack report in this chat using connected Slack tools.
- For requested periodic monitoring, use a scheduled heartbeat to discover new top-level reports in the configured channel. Persist processed source coordinates in the configured state file, deduplicate against existing verdicts, and avoid overlapping writes. Process each report with immutable coordinates. Triage and repro can run sequentially in one heartbeat so a separate repro watcher does not race triage.
- A standalone project job requires an explicit request. Resolve its project ID with `list_projects` and use the actual `automation_update` schema. Do not substitute a standalone job for a thread heartbeat without authorization.
- An exact event-driven requirement needs a separately configured, documented event delivery service. Report this dependency if unavailable. Scheduling is not equivalent to immediate event delivery.

Read `$CODEX_HOME/automations/*/automation.toml` to find matching existing schedules before creating one. Inspect only the relevant configuration. Use `automation_update` to view, create, or update the resolved schedule. Preserve existing fields and notification policy unless the user changes them. Never manually write scheduler directives.

The prompt must identify the target repository, operational file paths, external configuration, report discovery and deduplication state, scope of permitted Slack and tracker writes, and bounded fix permissions. A schedule alone does not grant permission to send messages or change repositories. This setup skill authorizes configured thread-only messages only when the user explicitly invokes it to configure that workflow. Obtain missing scope before enabling writes.

Stay quiet while monitored state is unchanged or non-actionable. Notify on meaningful changes, completion, failure, or required user action. Keep notification settings in the tool fields. A polling schedule must be accepted by the current tool; do not promise the short polling interval from an in-run wait budget as a supported schedule frequency.

Create or update only when the user requests it. If required integrations or proof are missing, keep the schedule paused and state the blocker. Do not claim installation enabled a working integration.

## 8. Test thread safety

Use an authorized test channel or harmless report. First confirm that configuration and operational files are available to the run, required integrations resolve, and the control capability check passes.

Verify all of the following:

1. Triage stores the root thread timestamp and posts exactly one verdict as a reply.
2. The verdict contains exactly one configured marker.
3. Repro accepts the marker only from the configured identity.
4. Source coordinates remain immutable.
5. No source-channel root message appears.
6. Workers receive no Slack credentials or writes. If the harness cannot enforce isolation, keep work in the coordinator.
7. Missing coordinates, a deleted parent, or failed preflight produces no post or tracker issue.
8. Reprocessing the same report creates no duplicate verdict, ticket, or fix.

Enable normal traffic only after these checks pass. Report which checks actually ran and which remain blocked. Do not infer success from configuration validation alone.
