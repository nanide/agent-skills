---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

# Swarm

## Start

Use the available plan tool, or keep a concise checklist in chat, with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Pick the `swarm workers` role. Follow [Delegation](../mode/references/delegation.md) for role configuration, model selection, and tool availability. For a model race, name the actual model of each arm before spawning.

4. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Follow [Delegation](../mode/references/delegation.md) for scoped briefs, ownership, concurrency, and missing-tool handling.

When a worker needs a specific branch, prepare a separate worktree at the verified ref and give its absolute directory and base SHA in the brief. Do not reset the shared checkout.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. If a receipt omits a required SHA or measurement method, give the original worker one chance to supply it from the run records while its investigation is still available. If a replacement is needed, use [Delegation](../mode/references/delegation.md#choose-whether-to-resume-a-delegate) for the handoff within the same retry limit. Accept the receipt only when the evidence supports the required details. Otherwise record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
