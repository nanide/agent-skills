---
name: help
description: "Explain the installed Nanide skills and help choose a workflow."
---


# Nanide skills help

Follow [Delegation](../mode/references/delegation.md) for the active provider’s role configuration.

For help, explain rather than starting the work. For an action request, read the appropriate sibling skill and execute within scope.

The normal entrypoint is mode followed by a goal and a check that can pass or fail. It selects a playbook and reads supporting skills. Read ../mode/SKILL.md for the current playbook catalog. Read the active [provider adapter](../../providers/README.md) before recommending an invocation. If a helper is outside its discovery entry points, tell the user to ask mode to use that helper by name. Resolve helper files from this skill’s real sibling directory even when they have no discovery link.

Use `how` for a code walkthrough, `why` for historical motivation, `interrogate` for independent review, `blast-radius` for downstream risks, `arena` for competing approaches, `swarm` for partitioned checks, and `benchmark-checklist` for performance evidence. Read the named skill before describing its workflow in detail.

Use [mode](../mode/SKILL.md#work-on-a-pr) for PR bodies, titles, creation, review, metadata, status, CI, and shipping. It routes each request to its owner and preserves the authorized scope. Generic PR review means code review. Opening or editing a PR does not start monitoring or authorize merging.

Use setup to change role models. The installed default inherits the current chat model; panels use two independent reviewers unless configured otherwise. Check the effective configuration before explaining this user's settings. Same-model review is not multi-provider review.

Use `statechart` to check TLA+ models and draw Mermaid charts with paths to broken rules. Run the bundled `scripts/statechart` launcher with a spec and optional view module. Model checking needs Java and TLC through `TLA2TOOLS` or mise. Render SVGs with Pele using the skill's rendering reference.

Use `recall` for relevant prior chat context, `reflect` for lessons from a run, and `automate-me` for a personal working-style skill. Use available chat tools within the requested project, topic, and time window. Chat summaries are not full execution transcripts.

Invoke the skill for each new task. Use the host scheduling tool for explicitly requested future work. Ordinary chat execution does not promise background continuation. Event-triggered webhooks require separately configured infrastructure.

Give at most one relevant example prompt and link the actual installed file. For update questions, read ../../README.md and ../../docs/releases.md. Preserve local configuration when switching installations.
