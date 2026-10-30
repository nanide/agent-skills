# Execution state

Read the selected [provider adapter](../../../providers/README.md) only when native execution, worktree, scheduling, or process tools are needed. Current tool schemas and host instructions are authoritative. Missing optional tools do not block independent work.

## Plans and checkpoints

Use a plan tool for a working checklist when available. For long or resumable work, save a durable Markdown checkpoint within the task workspace. Reuse an existing task-state location. A temporary directory is only suitable for disposable notes. Report the chosen path.

Record the objective, authorized scope, completion predicate, milestones, verified revisions and artifacts, pending work, decisions, blockers, branch and worktree, owned processes, and next action. Link the [decision trail](../../show-me-your-work/SKILL.md) instead of duplicating it. Update at meaningful milestones and before compaction or handoff. Compaction requires a checkpoint and continuation, not an automatic pause.

## Managed execution

Create a native persistent task or Goal only when explicitly requested and supported. Inspect existing state before creating another. Reconcile its objective, status, and limits with the durable checkpoint. Do not infer budgets, invent lifecycle APIs, replace unfinished work, or create a new task to evade limits. Follow the selected adapter's lifecycle rules.

Completion means the predicate is satisfied and no required work remains. Pausing requires an explicit pause request. Record blockers and continue independent authorized work. If the host has no persistent execution facility, use the checkpoint and explain that continuation needs an active session. Do not claim a native task exists.

Future runs, reminders, and recurring monitoring require an explicit scheduling request and an available scheduler. A plan, running shell, or autonomy grant does not create a schedule. Keep unchanged monitoring quiet and preserve the requested notification behavior.

## Worktrees

Inspect existing worktrees and host-managed attachments before creating another. Reuse a suitable checkout when safe. When isolation is needed, select an explicit base revision and record ownership. Verify the returned path and repository state. Worktree creation does not implicitly copy uncommitted changes.

Use the host's lifecycle tools for host-managed worktrees. Otherwise use Git according to repository rules. Preserve needed files before cleanup. Never remove another worker's checkout. Unknown ownership remains unresolved.

## Processes and PRs

Record each long-running command's working directory, owner, process or session identifier, logs, and stop condition. Use the tool that owns that identifier to poll with bounded waits. Check actual exit before replacing a watcher or transferring ownership. Interrupting an agent does not prove its child processes stopped.

Stop only owned processes and preserve required shared services. Use the bundled forge watcher for merge-readiness evidence. A running shell does not establish PR readiness. Link requested PRs and saved artifacts in the response. Use native attachment or review tools when available, without treating a displayed panel as durable storage.
