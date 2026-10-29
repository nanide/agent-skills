---
name: nanide-help
description: "Explain the installed Nanide skills and help choose a workflow."
---


# Nanide skills help

Follow [Delegation](../nanide-mode/references/delegation.md) for the active provider’s role configuration.

For help, explain rather than starting the work. For an action request, read the appropriate sibling skill and execute within scope.

The normal entrypoint is $nanide-mode followed by a goal and a check that can pass or fail. It selects a playbook and reads supporting skills. Read ../nanide-mode/SKILL.md for the current playbook catalog. Skills follow the active host’s discovery and invocation rules and may call sibling skills by reading their files.

Use $nanide-how for a code walkthrough, $nanide-why for historical motivation, $nanide-interrogate for independent review, $nanide-blast-radius for downstream risks, $nanide-arena for competing approaches, $nanide-swarm for partitioned checks, and $nanide-benchmark-checklist for performance evidence. Read the named skill before describing its workflow in detail.

Use [nanide-mode](../nanide-mode/SKILL.md#work-on-a-pr) for PR bodies, titles, creation, review, metadata, status, CI, and shipping. It routes each request to its owner and preserves the authorized scope. Generic PR review means code review. Opening or editing a PR does not start monitoring or authorize merging.

Use $setup-nanide-skills to change role models. The installed default inherits the current chat model; panels use two independent reviewers unless configured otherwise. Check the effective configuration before explaining this user's settings. Same-model review is not multi-provider review.

Use $nanide-statechart to generate user-facing Mermaid statecharts from TLA+ models or turn agreed charts into model skeletons. Full model checking needs Java and a configured TLA2TOOLS JAR; PNG rendering needs Mermaid CLI.

Use $nanide-recall for relevant prior chat context, $nanide-reflect for lessons from a run, and $nanide-automate-me for a personal working-style skill. Use available chat tools within the requested project, topic, and time window. Chat summaries are not full execution transcripts.

Invoke the skill for each new task. Use the host scheduling tool for explicitly requested future work. Ordinary chat execution does not promise background continuation. Event-triggered webhooks require separately configured infrastructure.

Give at most one relevant example prompt and link the actual installed file. For update questions, read ../../README.md and ../../docs/releases.md. Preserve local configuration when switching installations.
