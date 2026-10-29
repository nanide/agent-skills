---
name: setup-pstack
description: "Configure pstack model roles for Codex when explicitly requested."
---


# Set up pstack for Codex

Resolve this skill directory through symlinks. Read ../../codex-config.local.json if it exists, otherwise ../../codex-config.json. The local file replaces the defaults. Reject an invalid local file rather than falling back. For a request to show, inspect, or explain the configuration without changes, report the existing values and their effective defaults, then stop without writing. Preserve existing role choices unless the user asks to change them. For a new configuration with no preferences, use inherit-parent for all roles and two independent reviewers per panel. Installation already supplies these defaults; setup is optional.

For a requested model change, inspect the current subagent tool's supported models and reasoning levels. Show only available choices. Ask only for choices the request leaves materially ambiguous. Save the complete configuration with the selected role values to ../../codex-config.local.json, not config.toml or AGENTS.md. This changes pstack delegation only, not the main chat model.

The JSON has default_model (inherit-parent), panel_size (positive integer), and roles (object). A role value is inherit-parent, auto, or an object with model and optional reasoning_effort. A panel role can be a list of those values. Recognized roles include feature, refactoring; bug-fix; perf-issue; hillclimb; judgment and prose; hardest tasks; how explorer; how explainer; why investigators; why synthesizer; reflect tooling; reflect judgment, divergent, synthesizer; arena runners; arena cross-judge pool; architect runners; interrogate reviewers; swarm workers. The combined labels containing commas are single role keys.

Validate JSON syntax and every selected model/effort against the current tool. Explain unavailable choices rather than guessing. A missing role inherits the default. Do not manufacture a multi-provider panel from unavailable models. Report the saved choices and show one $nanide-mode example.
