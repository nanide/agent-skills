---
name: goal
description: "Run a long-running task through Nanide skills with the collection’s durable execution state and native goal tracking when available. Use when the user invokes goal to start or continue task execution."
---

# Nanide Goal

Use Nanide skills to own a long-running task in the current chat. A direct request such as `goal <task>` requests starting that task with durable goal tracking and the host’s native goal lifecycle when available. A request to explain, edit, or prepare this skill does not request Goal activation. Automatic skill selection alone is not authorization to create a Goal. Honor explicit research-only or planning-only scope.

## Start

Read [mode](../mode/SKILL.md) and [Execution state](../mode/references/execution-state.md). These own routing, durable state, Goal lifecycle, and process ownership. Use their procedures rather than defining another framework.

Ground the requested outcome and completion check in the user's request and repository evidence. Ask for a task if none is available. Resolve material ambiguity before dependent implementation without inventing acceptance thresholds.

For execution requests, follow Execution state's Goal procedure. Prepare and display the canonical plan below before creating or continuing a Goal. If native Goals are unavailable, use the canonical plan and checkpoint as the goal record. Continue authorized work in the active session without claiming native lifecycle transitions or automatic continuation.

Let mode select and run the appropriate playbook and supporting skills. Its authorization boundaries and repository guidance apply throughout. Record applicable guidance paths and required checks in the canonical plan, revisit them when scope changes, and include them in mode's delegate briefs. No separate preparation chat or manual chain of invocations is required.

Use Execution state for checkpoint contents and storage. Keep the canonical state paths discoverable from the Goal objective or existing checkpoint. On pickup, follow [Session pickup](../mode/playbooks/session-pickup.md) to reconcile saved context with current artifacts and resume the selected playbook.

## Keep the plan visible

Save the plan at one canonical path under Execution state's conventions. Reuse an existing plan in place. Near the top, name the current step, blockers, and next action. List the chunks in execution order as Markdown task items (`- [ ]`). Give each an outcome and a completion check. Together they must cover the requested deliverables, constraints, and acceptance checks. Keep the original task text below the checklist.

Display the saved plan using the active [provider adapter](../../providers/README.md) when available. Confirm success before reporting a panel as open. Immediately before creating the Goal, send one or two sentences in chat saying which Goal is about to start, with a clickable link to the saved plan. With local tracking, introduce the local plan instead. A missing panel does not block execution. If the save fails, report the path and error and resolve the failure before starting the Goal.

After each chunk passes its completion check, mark its existing row `- [x]`, record the evidence beside it, and advance the current step. Leave partial or blocked rows unchecked. Before starting another chunk, even within the same turn, send one or two sentences in chat summarizing what finished and linking the same updated plan. The final report can carry the last chunk's update. Reconcile every required row before completion.

At every goal reevaluation, read the native goal when available and the canonical checkpoint, reconcile actual progress and evidence, then update the same plan document before continuing work. This includes each continuation turn, milestone assessment, scope change, pickup after compaction, and completion or other lifecycle assessment. Refresh the status summary and checkpoint contents defined by Execution state. Record the assessment time even when the plan is unchanged. Preserve useful history and link detailed evidence.

Edit the canonical file in place. Do not create a new plan per turn or repeatedly open duplicate panels. On pickup, reuse and reconcile the existing document, then open it beside the chat if needed. After a native goal lifecycle transition, record the returned status in that same document. Without native tracking, record the local task status and label it as local. If a later save fails, report that the visible plan is stale and retry at the next checkpoint without misrepresenting its freshness.

## Amend an active plan

When a user instruction or authorized handoff changes the work, read the last saved plan and apply outstanding clarifications in arrival order before the next affected action. Use the current objective and checklist as the starting point. Keep the original request verbatim. A status question or detour alone leaves the objective intact.

Trace each change to the affected outcome, steps, dependencies, and completion checks. Edit those rows in place. Insert new steps in execution order using the existing checklist format. Preserve unaffected wording, headings, order, checkbox states, and evidence links. Remove superseded work from the pending queue and briefly record what retired it. Keep completed work with the evidence it earned. Give newly required proof its own unchecked step. Reassess in-flight assignments before using their results or dispatching more work.

For a material change, record its source and effect beside the affected work or in the existing decision trail. Refresh the effective objective, completion check, and next action wherever they have changed. Compare the saved plan with its previous version: every changed requirement must be accounted for, and every removed obligation must follow from the clarification. Correct unrelated rewrites. Repeated steering should leave one set of steps. If the amendment cannot be saved, recover it before continuing dependent work.

After compaction, reconcile the saved amendments with any newer user instructions and the actual evidence. Resume at the first authorized, actionable step of the amended checklist. If the native objective predates an amendment, record the difference and follow the provider's lifecycle rules. An incompatible replacement requires resolving the native conflict before claiming completion.

## Return after side work

When the user asks for side work and then continuation, record the first unfinished Goal step before switching. A detour alone does not request a pause. After the detour, reread the same plan and native status when available. For an active Goal, execute the next authorized step in the same turn. Do the same for a local plan.

For a paused Goal, an explicit request to continue authorizes returning to the work in this turn. If the host still reports paused, say so, identify the provider's resume control for automatic continuation, and do the next authorized step. Report native resumption only after observing active status. Honor a pause that the user has not lifted, unresolved blockers, and host limits. Preserve the existing Goal.

## Finish

At Finish, a request to complete the Goal includes its read-only review and verification assignments within the host’s permissions. Apply these checks to small diffs too. If the operator restricts the review method, give reviewers that same restriction. If required independence is unavailable, leave the review open.

Use the selected playbook's completion checks. Before declaring completion or making a final commit or push, open [interrogate](../interrogate/SKILL.md) and follow it to review the complete task diff and resulting artifacts. Include the applicable skills and guidelines from the plan in its review context so the independent audit covers compliance as well as correctness. Let interrogate own reviewer selection, read-only review, synthesis, and lead judgment.

Open [swarm](../swarm/SKILL.md) and follow it to delegate required verification checks, using the repository's existing test and verification skills for the commands and real-surface checks. Let swarm own worker briefs, revision evidence, coverage, and reporting. Assign verification without source edits. Respect each verification skill's resource ownership and approval rules, including any requirement that the coordinator drive a shared app. Reuse review and verification already performed by the selected playbook when their scope and evidence cover the current work. Do not launch a duplicate pass merely because the Goal is ending.

Resolve actionable findings within the authorized task through the selected playbook. Corrections may belong in code, tests, documentation, configuration, or the applicable skills. Use [Authoring a skill](../mode/playbooks/authoring-a-skill.md) for skill corrections. Do not weaken guidance to make the implementation pass. Record out-of-scope findings as follow-ups. Rerun affected verification and review corrected requirements before completion.

Use [show-me-your-work](../show-me-your-work/SKILL.md) for the decision trail and its independent evidence review. In the canonical plan, link the independent review verdict and verification results for the revision they cover. Leave each missing result unchecked and record the failed read or capability, when applicable. Mark the Goal complete only when required acceptance evidence and audits support it. Missing required proof prevents completion. Follow Execution state and current runtime rules for lifecycle transitions and blocked work.

After completing and pushing changes, check for an existing PR for each changed branch before workspace cleanup. Refresh its description using [PR description instructions](../mode/references/pr-descriptions.md). When a stack is available, inspect related PRs and refresh descriptions whose scope, dependencies, validation claims, or stack context changed because of the work. Leave descriptions that remain accurate unchanged. This step does not authorize creating a PR.

Only edit descriptions of PRs personally owned by the user. Verify the PR author against the user's confirmed hosting-service identity before each update. Repository ownership, collaborator access, and write permission do not establish personal ownership. Skip PRs authored by others or with uncertain ownership, and report any affected descriptions left unchanged. Record updated PR links and any verification or publication gaps in the checkpoint.

Before the final handback, clean up temporary branches and workspaces created for the task. Use the [worktree cleanup playbook](../mode/playbooks/worktree-cleanup.md) for task-owned workspaces, including its ownership checks, preservation, hold conditions, and cleanup report. Preserve the canonical checkpoint and needed evidence outside workspaces being removed.

After an authorized push, fetch the relevant remote refs and reset the task's original local branches to their verified origin heads. Check each branch's checkout for uncommitted work and active users before resetting it. Verify that local-only work is included in the pushed result or preserved before replacing a ref. Do not reset unrelated branches or delete remote branches. Delete temporary local branches only after their work is preserved and no checkout needs them.

Retain branches needed for unresolved work, active processes, or uncertain ownership. Record retained branch refs and workspace paths, reasons, and cleanup conditions in the checkpoint. Verify final branch refs and record resets alongside the worktree cleanup report. A queued archive request is pending, not completed cleanup. Resolve required cleanup outcomes and report failures before marking the Goal complete.

Use mode and Execution state for authorization and scheduling rules. This skill adds no authorization for external actions and requires no external preparation or handoff workflow.
