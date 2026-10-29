---
name: nanide-swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for $nanide-swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
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
3. Pick the `swarm workers` role. Resolve this skill directory through symlinks. Read `../../codex-config.local.json` if it exists, otherwise `../../codex-config.json`. The local file replaces the defaults. Reject an invalid local file rather than falling back. Resolve the named role from `roles`, falling back to `default_model`, then `inherit-parent`. `auto` and `inherit-parent` mean omit model and reasoning overrides. An explicit role is an object with `model` and optional `reasoning_effort`. Validate it against the current spawn tool and use the context-inheritance mode that permits overrides. If unavailable, report the mismatch and inherit the parent unless the user requires that exact model. Never substitute another model family. Report the actual models used and distinguish independent same-model reviews from model diversity. For a model race, name the actual model of each arm before spawning.

4. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Use the available Codex collaboration tools to spawn, inspect, message, and wait for subagents. Respect current concurrency limits and queue excess work. Spawns run asynchronously. Give each brief its scope, absolute skill/reference paths, and expected evidence. Read-only is an instruction in the brief, not a tool permission flag. Give writers exclusive files or an isolated worktree, tell them they share the codebase, and forbid reverting others' work. Do not create user-visible chats as substitutes for subagents. If delegation is unavailable, report that limitation and perform the scoped work directly without claiming independent review.

When a worker needs a specific branch, prepare a separate worktree at the verified ref and give its absolute directory and base SHA in the brief. Do not reset the shared checkout.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
