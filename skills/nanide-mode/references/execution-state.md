# Execution state in Codex

Use the current tool schemas as the authority. Discover available tools before calling them. If a capability is unavailable, report the limitation and preserve a recoverable local checkpoint. This reference belongs to Nanide skills and requires no other skill bundle.

## Plans and checkpoints

A plan tool, when exposed, can track a working checklist. Do not assume it saves a durable plan or invent a save/load-plan API. For long, multi-phase, or resumable work, save a Markdown plan and task-state checkpoint at an explicit durable path agreed by the task or chosen within its workspace. Use an existing plan location when present. Keep personal notes outside tracked project files unless repository delivery needs them. Report the path. A temporary directory is suitable only for disposable work; disclose that it may disappear.

Record the objective, scope and authorization, completion predicate, milestones, verified results with the revision and artifact paths, pending work, decisions, blockers, worktree and branch, owned processes, and the next concrete action. Link the bundled show-me-your-work decision trail instead of duplicating it. Update after meaningful milestones and before context compaction or handoff. Compaction is a checkpoint-and-continue event. It does not authorize pausing a Goal, cancelling agents, or stopping work.

A native Goal tracks execution status and budget. It does not replace the plan, evidence, per-PR revision ledger, or orchestrator state. `open_in_codex` can display a saved plan or review diff when useful; opening a panel is not persistence.

## Goals

Only call `create_goal` when the user or system/developer instructions explicitly request creating or starting a Goal. A long task, nanide invocation, autonomy grant, or request to keep going is not enough. Do not activate a Goal while merely researching or preparing a handoff.

On an explicit Goal request, inspect `get_goal` first. Reconcile an unfinished Goal with the requested objective rather than replacing it. Ask for direction if the objectives conflict. Create only when no unfinished Goal prevents it. Set `token_budget` only when explicitly requested; never infer it from a timebox or estimate. Use the actual completion predicate in the objective.

Read `get_goal` when picking up Goal work and at meaningful checkpoints. Reconcile its status and remaining budget with the plan. Honor runtime limits. Do not create another Goal to evade them. `update_goal` cannot resume a Goal, edit its objective, adjust its budget, or set usage-limit states; those changes belong to the user or system.

- Set `complete` only when the objective is achieved and no required work remains. Budget exhaustion or ending a turn is not completion. For a budgeted completed Goal, report the final token usage returned by the tool.
- Set `paused` only on the user's explicit request to pause the Goal. Report the returned status and stop Goal work. Budget limits take precedence. A later user resume revokes that pause request, but does not authorize a fabricated resume API call.
- Set `blocked` only after the same blocking condition has recurred for at least three consecutive Goal turns, including the original turn and automatic continuations, and no meaningful independent progress remains without user input or external change. Difficulty, uncertainty, or a useful clarification is insufficient. Track the condition and consecutive turns in the checkpoint. Once the threshold is met, mark blocked instead of repeating an active blocked report. Resumption after blocked starts a fresh three-turn audit.

Goals do not authorize schedules. Use a Codex automation only for an explicit future continuation, reminder, or recurring monitoring request. Prefer a thread heartbeat for follow-ups, preserve notification intent, and stay quiet on unchanged, non-actionable state. Do not promise execution while the required host is unavailable.

## Worktrees

Inspect `list_artifacts` and reuse a suitable attached checkout before creating one. This lists this chat's attachments, not all repository worktrees. Keep the bundled read-only worktree audit for repository-wide Git evidence.

When isolation is needed, use `create_worktree` with `allowAsync: true`. Its default base is the remote default branch, not the current checkout, and it does not copy uncommitted changes. Resolve the intended base and supply a verified `ref` when needed. Use the returned workspace path for all work.

If creation returns an operation ID, check `get_worktree_creation_status` with spaced, bounded checks, backing off when unchanged. Continue independent work between checks. If registration fails after creation, retry attachment with `attach_worktree` and the returned workspace path. Restore an archived attachment with `restore_worktree`; its saved state returns as a snapshot commit on detached HEAD, not staged or unstaged edits. Inspect that state before continuing.

Archive managed worktrees with `archive_worktree` when no longer needed. Preserve needed ignored files separately and never remove another worker's checkout. Follow current tool eligibility constraints and repository branch rules.

## Processes and PRs

For a long-running shell command, record command, cwd, owner, `session_id`, log paths, and stop condition. Poll a running `exec_command` session with `write_stdin` using bounded waits and progress updates. A running functions execution cell instead returns a cell ID and is resumed with `functions.wait`; these IDs are not interchangeable.

Check actual process exit before starting a replacement watcher or transferring ownership. Interrupting a subagent does not establish that its child processes stopped. Stop only owned processes, preserve required shared services, and record uncertain ownership as unresolved. Keep the bundled forge watcher for merge-readiness semantics; a shell session alone says nothing about PR readiness.

Use `attach_artifact` for every created PR and an existing PR the user asks to review, update, or continue. Do not attach PRs used only as background examples, dependencies, or comparisons. Show saved artifacts or review panels with `open_in_codex` when useful. Use inline code comments for focused review findings when appropriate, not as a substitute for verified evidence.
