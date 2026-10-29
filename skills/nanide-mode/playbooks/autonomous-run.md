### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.**

1. Read [Execution state in Codex](../references/execution-state.md) for durable plans, native Goals, and process ownership. This playbook alone does not authorize Goal creation. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N PRs merged, pixel-diff zero).
2. Continue in the active turn. Use a watcher process or subagent for CI, merge, or ref events, with bounded waits and progress updates. Only an explicit request for future continuation or recurring monitoring authorizes the Codex automation tool. Save a clear predicate and checkpoint for that continuation; invocation of this playbook alone creates no schedule.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help. Belt-and-suspenders that "might help" gets reverted, not left to ride.
   Sequence the work via the **nanide-principle-sequence-verifiable-units** principle skill, verifying each unit before the next instead of batching checks at the end.
4. Mid-run discoveries are yours. Fix blockers within the authorized scope. Record unrelated discoveries as follow-ups instead of expanding the task. Do not park reversible work for the human or use a user-input question. Surface only irreversible actions, genuine product or preference calls no experiment can settle, or a real dead end. Keep the predicate as the main drive, and return to it after each side fix.
5. Checkpoint every iteration via the **nanide-show-me-your-work** skill, a row for what changed and whether the predicate moved.
6. Honor explicit stops and native Goal/runtime limits. Update an active Goal under the linked completion, pause, and three-turn blocker rules. Stop when the predicate is met. A plateau is not a stop, so keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state.
