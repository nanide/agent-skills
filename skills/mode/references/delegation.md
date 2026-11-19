# Delegation

Read the [provider adapter](../../../providers/README.md) for the current host only. It owns configuration paths, native tool mappings, and model override syntax. Resolve this collection through symlinks before reading its configuration. A local configuration replaces the defaults. Reject invalid local configuration rather than silently falling back.

Resolve a named role from `roles`, then `default_model`, then `inherit-parent`. Missing configuration, `inherit-parent`, and `auto` mean inherit without an override. A configured panel list sets the reviewer count. Otherwise use `panel_size`, default two. Validate explicit model and reasoning choices against the live tool schema. Report an unavailable choice and inherit unless the user requires that exact model. Never invent model IDs or substitute families. Report actual models when the host exposes them, and distinguish independent same-model review from model diversity.

Use supported delegation tools within the host's concurrency and depth limits. Give each brief the task, absolute skill and reference paths, bounded evidence, ownership, and acceptance criteria. Declare read-only source and external-state scope in review briefs. A review workflow may grant explicit ownership of isolated temporary repro files and generated outputs. Name those paths and keep implementation edits outside that grant. Give writers exclusive files or isolated worktrees and tell them they share the codebase and must preserve others' changes. Do not create user-visible chats as substitutes for subagents.

When delegating part of an assignment, carry the same resolved mode path, operator constraints, allowed actions, and applicable acceptance checks into the child's brief. Narrow ownership to the assigned slice. Route decisions outside that authority back through the parent. An explicit request for a draft still applies at every level.

Judge the result against the assignment and required repository checks. Add a diagnostic when it helps establish a result. A new sign-off requires an applicable instruction. Before attributing a failing check to the change, run the same check on the base under comparable conditions. Report a reproduced baseline failure separately, including its effect on the requested proof. If comparison or required evidence is unavailable, report the gap to the parent.

## Choose whether to resume a delegate

Guard the delegate's context window as well as the coordinator's. Use the deliverable to decide which history the delegate needs.

- For a correction, retry, or follow-up on the same deliverable, resume its agent when the prior investigation still helps. Send the correction and the relevant evidence.
- Queue only independent work. Start a fresh agent for each independent item, even when an idle agent has the same role or both items serve one parent goal.
- For an independent judgment, start a fresh reviewer with the criteria and primary evidence. Withhold earlier verdicts until the reviewer records its assessment.

Start fresh agents without inherited conversation history when the host supports it. Supply the objective, scope, applicable constraints, evidence paths, and completion check in the brief. If the host includes history or leaves inheritance unclear, report what the host exposes. If an earlier verdict may be visible, keep the independent assessment pending until a reviewer can receive it blind.

On pickup, inspect the agent and its process without restarting either. Keep a running process or unfinished write with its owner through completion or a confirmed handoff. Before transferring work, confirm the previous writer has stopped writing. Give the successor a consolidated brief with corrections, verified progress, remaining work, and the owner and identifier of each active process or writable path.

If delegation is unavailable, report the limitation and perform authorized work directly. Do not claim independent review or model diversity. When independent review is a required acceptance gate, keep that gate unmet and report it. The parent reviews the actual artifacts and owns the final result.
