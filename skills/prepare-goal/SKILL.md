---
name: prepare-goal
description: Research a proposed task with poteto-mode, then automatically use research-to-goal to deliver a handoff and a paste-ready Codex Goal prompt for execution in a new chat. Use when the user wants investigation and preparation in one request, before implementation.
---

# Prepare Goal

Own the sequence from a task idea to a research-backed launch prompt for a fresh chat. Run the investigation and package its results in this chat. Leave implementation and Goal activation to the new chat.

## Resolve the two skills

Read the installed `poteto-mode` and `research-to-goal` skills. Use their catalog paths when available. Otherwise resolve this skill directory through symlinks and read `../poteto-mode/SKILL.md` and `../research-to-goal/SKILL.md`. Record the resolved paths for the handoff.

If a dependency is missing, report which one and complete independent preparation where useful. Do not claim its workflow ran or silently replace it. Do not install dependencies without a request to do so.

## Research with poteto-mode

Pass poteto-mode this task brief, populated from the user's request:

> Investigate the proposed task and prepare the evidence needed for a future implementation Goal. Establish the current behavior, relevant architecture, constraints, plausible approaches and tradeoffs, verification strategy, unknowns, and recommended first implementation step. This phase is research-only. Its deliverable feeds research-to-goal automatically in this chat. Do not implement, activate a Goal, open a PR, or switch into execution when the investigation finishes.

Let poteto-mode route the research and select its supporting skills. Keep the research-only boundary even when the eventual task is large or involves a bug, migration, or performance work. Reuse research already present in the conversation. Delegate only as permitted by the active harness and applicable skill instructions; pass the same research-only scope to delegates.

Resolve factual questions from evidence. Ask about product choices or constraints only when the answer materially changes the task, while continuing independent research. Do not invent measurable targets when the user has supplied only a direction. Recommend a target with its basis or make baseline measurement and target selection an explicit prerequisite.

Read-only diagnostics and authorized checks may support the investigation. Preserve repository requirements for test targets, services, browser profiles, and production access. Write research notes and handoff artifacts outside tracked project files unless the user requests a project destination. Do not change application code to obtain a speculative answer.

Research is sufficient when the evidence supports a bounded recommendation, identifies the affected areas, provides a credible validation strategy, and distinguishes remaining implementation discovery from decisions that block starting. Do not exhaust every possible avenue. If missing evidence prevents a reliable recommendation, package the partial findings with an explicit blocker and make resolving it the first step.

## Automatically package the findings

Immediately apply the installed research-to-goal skill to the research and conversation. Do not end with an offer to package it or require the user to invoke another skill. Do not copy that skill's artifact templates here; it owns their format, checkpoint behavior, and validation.

Pass along:

- Original request, subsequent corrections, findings and source evidence.
- Recommended approach, alternatives rejected with reasons, and unresolved decisions.
- Scope, acceptance criteria, verification commands and baseline evidence.
- Execution context and authorizations, including any ongoing restrictions.
- Requested destination and token budget, if explicitly provided.

Distinguish this wrapper's research-only phase from a user's continuing prohibition on implementation. The generated new-chat prompt may authorize execution of the defined task when the user submits it, but must not claim the research chat already authorized extra external actions or lift an explicit review gate. If a decision remains blocking, make resolving it a prerequisite in the launch prompt rather than presenting the task as ready to implement.

## Deliver the new-chat instructions

Finish in the same turn with:

1. A concise research conclusion and any prerequisite that prevents starting implementation.
2. Links to HANDOFF.md, TASK_STATE.md, and START_PROMPT.md produced by research-to-goal.
3. The repository/worktree the user should open and the complete, populated contents of START_PROMPT.md in a copyable code block.
4. A brief note that submitting that prompt in the new chat starts the Goal workflow. Local artifacts must be accessible there; copy or attach them for a different machine. Disclose temporary storage when used.

Check that the prompt can stand alone without this conversation and that all three artifacts exist. State what was actually researched and checked. Never claim the future Goal has already been activated, that implementation has begun, or that checkpoints guarantee lossless compaction.
