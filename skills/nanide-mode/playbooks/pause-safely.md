### Pause safely

**You own a clean stop. Leave a checkpoint a cold-start agent can resume from.** This is explicit only. On "keep going", "going to bed, keep going", or "don't stop", do not pause.

1. Stop at a safe boundary. Finish the current atomic step or back out of it. Start nothing new, and stop owned nested subagents. Confirm their owned child processes have stopped; an interrupted agent alone is not proof. Preserve unrelated shared services.
2. Take no irreversible action to pause. No PR and no push unless you already had one out.
3. Make the work durable. Preserve all edits. If local commits are authorized and the branch permits them, commit only this task’s edits as a clear `wip:` commit; never sweep in unrelated changes. If the tree is broken, say so in the commit body in one line.
4. Write the resume note off-context. Capture intent, what you were doing, progress and what's verified, current state, next steps, key files, and gotchas. Use a durable plan/checkpoint path per [Execution state in Codex](../references/execution-state.md). Compaction alone checkpoints and continues, without entering this pause playbook. If a show-me-your-work trail exists, point at it instead of duplicating it.
5. If the user explicitly requested pausing an active Goal, use `update_goal` with `paused`, report the returned status, and stop Goal work. Follow the native lifecycle rules in the linked reference.

**Reply:** where you are in the loop, what's on disk versus still in your head (paths, no diff dumps), the commits you made and whether the tree is clean, and the first action on resume. This is a pause, not a final report.
