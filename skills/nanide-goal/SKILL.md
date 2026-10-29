---
name: nanide-goal
description: "Run a long-running task through Nanide skills with a native Codex Goal and the collection's durable execution state. Use when the user invokes nanide-goal to start or continue task execution."
---

# Nanide Goal

Use Nanide skills to own a long-running task in the current chat. A direct request such as `$nanide-goal <task>` requests starting that task as a native Codex Goal. A request to explain, edit, or prepare this skill does not request Goal activation. Automatic skill selection alone is not authorization to create a Goal. Honor explicit research-only or planning-only scope.

## Start

Read [nanide-mode](../nanide-mode/SKILL.md) and [Execution state in Codex](../nanide-mode/references/execution-state.md). These own routing, durable state, Goal lifecycle, and process ownership. Use their procedures rather than defining another framework.

Ground the requested outcome and completion check in the user's request and repository evidence. Ask for a task if none is available. Resolve material ambiguity before dependent implementation without inventing acceptance thresholds.

For execution requests, follow Execution state's Goal procedure. Prepare and display the canonical plan below before creating or continuing a Goal. If native Goals are unavailable, report the limitation and continue authorized work without claiming automatic continuation.

Let nanide-mode select and run the appropriate playbook and supporting skills. Its authorization boundaries and repository guidance apply throughout. Record applicable guidance paths and required checks in the canonical plan, revisit them when scope changes, and include them in nanide-mode's delegate briefs. No separate preparation chat or manual chain of invocations is required.

Use Execution state for checkpoint contents and storage. Keep the canonical state paths discoverable from the Goal objective or existing checkpoint. On pickup, follow [Session pickup](../nanide-mode/playbooks/session-pickup.md) to reconcile saved context with current artifacts and resume the selected playbook.

## Keep the plan visible

Before creating a native Goal, save the plan at one canonical path under Execution state's conventions. Reuse the existing plan or checkpoint when it already holds the plan. Put a concise summary of completed work, current work, blockers, and the next action near the top.

Open the saved plan beside the current chat with `open_in_codex`, using its absolute file path and right placement. Omit `threadId` to target the current chat. Confirm that the tool succeeded before reporting the plan as open. This displays a file panel; do not claim native Plan mode creation or sidebar pinning. If the display tool is unavailable or fails, link the saved file and report the limitation, then continue authorized execution. If the plan cannot be saved, report the failure and resolve it before creating a new Goal.

At every Goal reevaluation, read the Goal and reconcile actual progress and evidence, then update the same plan document before continuing work. This includes each continuation turn, milestone assessment, scope change, pickup after compaction, and completion or other lifecycle assessment. Refresh the status summary and checkpoint contents defined by Execution state. Record the assessment time even when the plan is unchanged. Preserve useful history and link detailed evidence.

Edit the canonical file in place. Do not create a new plan per turn or repeatedly open duplicate panels. On pickup, reuse and reconcile the existing document, then open it beside the chat if needed. After a Goal lifecycle transition, record the returned status in that same document. If a later save fails, report that the visible plan is stale and retry at the next checkpoint without misrepresenting its freshness.

## Finish

Use the selected playbook's completion checks. Before declaring completion or making a final commit or push, route the complete task diff and resulting artifacts through [nanide-interrogate](../nanide-interrogate/SKILL.md). Include the applicable skills and guidelines from the plan in its review context so the independent audit covers compliance as well as correctness. Let interrogate own reviewer selection, read-only review, synthesis, and lead judgment.

Delegate required verification checks through [nanide-swarm](../nanide-swarm/SKILL.md), using the repository's existing test and verification skills for the commands and real-surface checks. Let swarm own worker briefs, revision evidence, coverage, and reporting. Assign verification without source edits. Respect each verification skill's resource ownership and approval rules, including any requirement that the coordinator drive a shared app. Reuse review and verification already performed by the selected playbook when their scope and evidence cover the current work. Do not launch a duplicate pass merely because the Goal is ending.

Resolve actionable findings within the authorized task through the selected playbook. Corrections may belong in code, tests, documentation, configuration, or the applicable skills. Use [Authoring a skill](../nanide-mode/playbooks/authoring-a-skill.md) for skill corrections. Do not weaken guidance to make the implementation pass. Record out-of-scope findings as follow-ups. Rerun affected verification and review corrected requirements before completion.

Use [nanide-show-me-your-work](../nanide-show-me-your-work/SKILL.md) for the decision trail and its independent evidence review. Link the review verdicts, verification evidence, and remaining gaps from the canonical plan. Mark the Goal complete only when required acceptance evidence and audits support it. Missing required proof prevents completion. Follow Execution state and current runtime rules for lifecycle transitions and blocked work.

After completing and pushing changes, check for an existing PR for each changed branch before workspace cleanup. Refresh its description using [PR description instructions](../nanide-mode/references/pr-descriptions.md). When a stack is available, inspect related PRs and refresh descriptions whose scope, dependencies, validation claims, or stack context changed because of the work. Leave descriptions that remain accurate unchanged. This step does not authorize creating a PR.

Only edit descriptions of PRs personally owned by the user. Verify the PR author against the user's confirmed hosting-service identity before each update. Repository ownership, collaborator access, and write permission do not establish personal ownership. Skip PRs authored by others or with uncertain ownership, and report any affected descriptions left unchanged. Record updated PR links and any verification or publication gaps in the checkpoint.

Before the final handback, clean up temporary branches and workspaces created for the task. Use the [worktree cleanup playbook](../nanide-mode/playbooks/worktree-cleanup.md) for task-owned workspaces, including its ownership checks, preservation, hold conditions, and cleanup report. Preserve the canonical checkpoint and needed evidence outside workspaces being removed.

After an authorized push, fetch the relevant remote refs and reset the task's original local branches to their verified origin heads. Check each branch's checkout for uncommitted work and active users before resetting it. Verify that local-only work is included in the pushed result or preserved before replacing a ref. Do not reset unrelated branches or delete remote branches. Delete temporary local branches only after their work is preserved and no checkout needs them.

Retain branches needed for unresolved work, active processes, or uncertain ownership. Record retained branch refs and workspace paths, reasons, and cleanup conditions in the checkpoint. Verify final branch refs and record resets alongside the worktree cleanup report. A queued archive request is pending, not completed cleanup. Resolve required cleanup outcomes and report failures before marking the Goal complete.

Use nanide-mode and Execution state for authorization and scheduling rules. This skill adds no authorization for external actions and requires no external preparation or handoff workflow.
