---
name: nanide-help
description: "Explain the installed Codex version of Nanide skills and help choose a workflow."
---


# Nanide skills help for Codex

Resolve this skill directory through symlinks. Read `../../codex-config.local.json` if it exists, otherwise `../../codex-config.json`. The local file replaces the defaults. Reject an invalid local file rather than falling back.

For help, explain rather than starting the work. For an action request, read the appropriate sibling skill and execute within scope.

The normal entrypoint is $nanide-mode followed by a goal and a check that can pass or fail. It selects a playbook and reads supporting skills. Read ../nanide-mode/SKILL.md for the current playbook catalog. Skills are explicitly invoked and may call sibling skills by reading their files.

Use $how for a code walkthrough, $why for historical motivation, $interrogate for independent review, $blast-radius for downstream risks, $arena for competing approaches, $swarm for partitioned checks, and $benchmark-checklist for performance evidence. Read the named skill before describing its workflow in detail.

Use $setup-nanide-skills to change role models. The installed default inherits the current chat model; panels use two independent reviewers unless configured otherwise. Check the effective configuration before explaining this user's settings. Same-model review is not multi-provider review.

Use $statechart to generate user-facing Mermaid statecharts from TLA+ models or turn agreed charts into model skeletons. Full model checking needs Java and a configured TLA2TOOLS JAR; PNG rendering needs Mermaid CLI.

Use $recall for relevant prior chat context, $reflect for lessons from a run, and $automate-me for a personal working-style skill. Use available Codex chat tools within the requested project, topic, and time window. Chat summaries are not full execution transcripts.

Invoke the skill for each new task. Use the Codex automation tool for explicitly requested future work. Ordinary chat execution does not promise background continuation. Event-triggered webhooks require separately configured infrastructure.

Give at most one relevant example prompt and link the actual installed file. For update questions, read ../../README.md and ../../docs/releases.md. Preserve local configuration when switching installations.
