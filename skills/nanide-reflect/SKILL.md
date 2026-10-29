---
name: nanide-reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "$nanide-reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Gather the current session evidence

Use the current conversation and, when needed, the available list/read chat tools scoped to this chat and project. Pass a bounded evidence digest with real chat IDs, turn references, tool results, and artifact paths. Treat chat summaries as summaries, not complete execution transcripts. If tool-level evidence is unavailable, state that limitation and do not infer which tools or files an agent used. Never guess transcript paths or search unrelated chats.

## 2. Spawn three reviewers in parallel

Follow [Delegation](../nanide-mode/references/delegation.md) for scoped briefs, ownership, concurrency, and missing-tool handling. Reviewers are read-only and may inspect only connected evidence referenced by the session.

| Lens | Configuration role | Default model behavior | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `inherit-parent` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `inherit-parent` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `inherit-parent` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the bounded session evidence where marked. Reviewers return findings in their final response.

## 3. Synthesize

Spawn one independent read-only synthesizer using `reflect judgment, divergent, synthesizer`. It spot-checks citations through the available connected tools. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **nanide-principle-encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output. If the user already authorized skill edits, apply that scope. Otherwise request approval for the concrete Accepted edits. The user may choose a subset or redirect routing.

Keep Backlog items in the report. File them externally only when the user authorized that action.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): follow [Authoring a skill](../nanide-mode/playbooks/authoring-a-skill.md), including its validation checks.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): follow [Authoring a skill](../nanide-mode/playbooks/authoring-a-skill.md) and validate that its description matches the intended requests.
- `new skill: <kebab-name>`: follow [Authoring a skill](../nanide-mode/playbooks/authoring-a-skill.md).

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog retained in the report or filed when authorized: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
