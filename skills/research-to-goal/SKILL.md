---
name: research-to-goal
description: Turn completed research, including poteto-mode investigations, into a self-contained handoff and a Codex Goal launch prompt for a fresh chat. Use when preparing a large task for later execution; does not start implementation or activate a Goal in the research chat.
---

# Research to Goal

Produce a handoff that a fresh Codex chat can execute without access to this conversation. This skill packages existing research; it does not run the implementation or create an active Goal here.

## Extract the execution contract

Use the current conversation and relevant artifacts to identify:

- Desired outcome and observable completion checks.
- Scope, non-goals, constraints, and unresolved decisions.
- Confirmed findings with evidence, hypotheses, rejected approaches and their reasons.
- Existing changes, completed checks, and the next useful action.
- Repository/worktree, branch, base revision, relevant files, required services and available skills.

Inspect only what is needed to fill material gaps. Do not repeat the investigation. Preserve the difference between a recommendation, a user decision, and permission to act. Label unknowns; never invent test results, source references, thresholds, approvals, or a token budget. Ask only about missing information that would materially change the execution contract. A blocking unanswered question belongs in the handoff and must be resolved before dependent implementation.

## Write portable artifacts

Use a user-selected destination or the repository's existing handoff convention. Otherwise create a task-specific directory under `/private/tmp` on macOS or `/tmp` elsewhere and disclose that it is temporary and local. Do not modify tracked project files merely to store the handoff. Use one canonical copy of each fact, and avoid copying secrets or unrelated conversation material.

Create these files:

### HANDOFF.md — durable research and contract

Include:

1. **Outcome and completion evidence:** a concrete pass/fail finish line, the tests/benchmarks/artifacts that prove it, and any baseline and measurement procedure already established. Distinguish mandatory acceptance criteria from suggestions.
2. **Scope and constraints:** intended changes, non-goals, behavior to preserve, operational boundaries, and authorization already given. Carry forward approval requirements for E2E targets, service recovery, external communications, publishing, and other applicable actions. Do not infer those permissions from a request for autonomous work.
3. **Research and decisions:** concise findings with file/symbol references or source links; evidence versus hypotheses; chosen approach and rationale; rejected approaches worth avoiding; open questions and the next way to resolve them.
4. **Execution context:** repository location, branch/base and revision where known, dirty worktree ownership, existing artifacts, relevant instructions/skills and their resolved paths, commands and environment requirements. Mark paths as local or portable. Identify changes that are uncommitted and unavailable in another checkout.
5. **Milestones:** a short sequence of independently verifiable outcomes with the first actionable step. Leave implementation choices open where the research has not settled them.
6. **Stopping conditions:** completion, user pause, configured budget exhaustion, or a genuine blocker handled under the current runtime's Goal rules. Explain what evidence and next input to report when blocked. Do not weaken acceptance criteria or expand scope to force success.

### TASK_STATE.md — mutable checkpoint

Seed it with the actual state at handoff:

- Current milestone and next action.
- Completed work and changed files, including ownership of pre-existing edits.
- Checks already run, their result, revision/environment, and evidence paths.
- Decisions made since the handoff; failed approaches worth avoiding.
- Blockers, pending questions, and active processes or jobs with their identifiers.

Keep this file short and current. Reuse an existing decision log from poteto-mode/show-me-your-work where practical, linking to it rather than duplicating the history. HANDOFF.md holds the research contract; TASK_STATE.md holds execution progress.

### START_PROMPT.md — paste into a fresh chat

Generate a fully populated prompt, not unresolved template placeholders. Use this structure:

```text
Read <absolute HANDOFF.md path> and <absolute TASK_STATE.md path>, then the applicable repository instructions. Resolve referenced skills from this environment; use poteto-mode at <verified path> to route the remaining work. If an essential artifact or skill is unavailable, report that before dependent work.

Establish a Codex Goal: <desired end state>, verified by <specific evidence>, while preserving <constraints>. Work within <scope and authorization boundaries>. <Include a token budget only if the user explicitly supplied one.>

Begin with <first action or unresolved prerequisite>. Continue through the milestones while the Goal remains active and within its limits. Let poteto-mode select the appropriate playbook; use Codex's native Goal continuation instead of requiring Cursor /loop or inventing an equivalent tool. Adapt unavailable platform mechanisms without dropping required verification or authorization boundaries.

Update TASK_STATE.md after meaningful milestones, failed approaches that affect the plan, and before handoff or compaction when possible. Record decisions and evidence, not a transcript. After compaction or resumption, reread the Goal, HANDOFF.md, and TASK_STATE.md; reconcile them with the current branch, diff, and active jobs. Preserve completed work and rerun checks only when changes, stale evidence, or uncertainty justify it.

Complete only when the acceptance evidence supports the Goal. At a stopping condition, leave an accurate checkpoint and report completed work, validation, remaining work, blockers, and the next useful action. Follow the runtime's Goal lifecycle rules. If native Goals are unavailable, say so rather than claiming automatic continuation is enabled.
```

The budget clause is omitted entirely when none was requested. If poteto-mode is not installed, resolve its location from the user or clearly mark the dependency as unavailable; do not claim compatibility with an unread installation. Do not prescribe a chain of pstack skills in place of its router.

## Check the handoff and deliver

Read all three generated files as if the conversation were unavailable. Check that:

- The launch prompt explicitly requests Goal creation in the new chat and identifies the exact artifacts.
- Critical constraints and known pitfalls are captured; references exist or are explicitly marked unavailable.
- Completion can be assessed from concrete evidence; unknown baselines are measurement tasks, not invented facts.
- Research conclusions are not silently promoted to user approval, and a research-only restriction is not silently lifted.
- A new chat can identify the first step without repeating completed research.

Return links to the files and the paste-ready launch prompt. Explain that local files must be copied or attached when starting on another machine, and temporary files should be moved to durable storage for long-lived work. Goals preserve the objective and continuation state; the handoff and checkpoints provide recoverable task context, without promising lossless compaction.
