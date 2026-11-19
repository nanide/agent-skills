---
name: help
description: "Explain the installed Nanide skills and help choose a workflow."
---


# Nanide skills help

Follow [Delegation](../mode/references/delegation.md) for the active provider’s role configuration.

For help, explain rather than starting the work. For an action request, read the appropriate sibling skill and execute within scope.

For ordinary engineering work, select [mode](../mode/SKILL.md) with the desired result. Read the active [provider adapter](../../providers/README.md) before suggesting a selector. For a hidden helper, select mode and describe the outcome or name the helper. Resolve the linked files relative to this skill’s real directory.

## Choose by outcome

Match the user's requested result. Open the linked owner for that result. In a help-only conversation, explain the choice. An index match grants no additional permissions.

| Requested result | Owner |
|---|---|
| Explain how code works, trace why a decision was made, or teach someone a subsystem | [How](../how/SKILL.md) for mechanics, [Why](../why/SKILL.md) for history, [Teach](../teach/SKILL.md) for a learner's explanation. |
| Summarize changes and pending decisions in this chat, recover context on a topic across chats, or resume one prior run | [Ketchup](../ketchup/SKILL.md) for this chat, [Recall](../recall/SKILL.md) for scoped cross-chat research, [Session pickup](../mode/playbooks/session-pickup.md) to continue a handoff. |
| Restate the last answer plainly, play back the user's intent, or rewrite a prompt for another agent | [Bro](../bro/SKILL.md), [In your own words](../in-your-own-words/SKILL.md), or [Sharpen](../sharpen/SKILL.md), respectively. |
| Show what a change could break downstream or independently challenge a diff | [Blast radius](../blast-radius/SKILL.md) for downstream risk. [Interrogate](../interrogate/SKILL.md) for independent review. For PR operations, use [Mode’s PR routes](../mode/SKILL.md#work-on-a-pr). |
| Settle a consequential design, compare competing implementations, or divide checks among workers | [Architect](../architect/SKILL.md) for design, [Arena](../arena/SKILL.md) for competing candidates, [Swarm](../swarm/SKILL.md) for partitioned work. |
| Establish whether a performance measurement supports a claim | [Benchmark checklist](../benchmark-checklist/SKILL.md). |
| Create a reusable way to drive the app, or update a stale feature map | [Create an app verifier](../create-verification-skill/SKILL.md) or [maintain the existing verifier](../maintain-verification-skill/SKILL.md). For a request to verify one change, use the existing project checks. |
| Prove an invariant and create a repeatable formal check, or reconcile a model with changed code | [Create a formal verifier](../create-formal-verification-skill/SKILL.md) or [maintain the formal verifier](../maintain-formal-verification-skill/SKILL.md). For a diagram or counterexample path from a TLA+ model, use [Statechart](../statechart/SKILL.md). |
| Audit completed work against applicable instructions | [Audit](../audit/SKILL.md) under the task's existing authorization. |
| Prevent a repeated class of agent mistakes, learn from one run, or capture personal working preferences | [Correct](../correct/SKILL.md) for repeated mistakes, [Reflect](../reflect/SKILL.md) for a requested retrospective, [Automate me](../automate-me/SKILL.md) for a personal skill. |
| Build a dashboard for a configured bot service | [Make bot UI](../make-bot-ui/SKILL.md). |
| Start or continue a durable Goal, or change the collection's model roles | Use [Goal](../goal/SKILL.md) for an explicit Goal request. Use [Setup](../setup/SKILL.md) for a role change. To explain current settings, read the effective configuration. |

For other engineering tasks, consult [Mode’s playbooks](../mode/SKILL.md#playbooks). Use the [prompt recipes](references/recipes.md) for examples.

Give at most one relevant example prompt and link the actual installed file. For update questions, read ../../README.md and ../../docs/releases.md. Preserve local configuration when switching installations.
