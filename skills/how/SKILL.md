---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Resolve this skill directory through symlinks. Read `../../codex-config.local.json` if it exists, otherwise `../../codex-config.json`. The local file replaces the defaults. Reject an invalid local file rather than falling back. Resolve the named role from `roles`, falling back to `default_model`, then `inherit-parent`. `auto` and `inherit-parent` mean omit model and reasoning overrides. An explicit role is an object with `model` and optional `reasoning_effort`. Validate it against the current spawn tool and use the context-inheritance mode that permits overrides. If unavailable, report the mismatch and inherit the parent unless the user requires that exact model. Never substitute another model family. Report the actual models used and distinguish independent same-model reviews from model diversity.

Use `how explorer` for explorers and `how explainer` for explainers.

Use the available Codex collaboration tools to spawn, inspect, message, and wait for subagents. Respect current concurrency limits and queue excess work. Spawns run asynchronously. Give each brief its scope, absolute skill/reference paths, and expected evidence. Read-only is an instruction in the brief, not a tool permission flag. Give writers exclusive files or an isolated worktree, tell them they share the codebase, and forbid reverting others' work. Do not create user-visible chats as substitutes for subagents. If delegation is unavailable, report that limitation and perform the scoped work directly without claiming independent review. All delegates are read-only.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Launch explorers within the available slots, each with `references/explorer-prompt.md` and its angle filled in.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Own the final answer. Check the explainer’s evidence and summarize it for the user without changing supported findings or dropping relevant uncertainty.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
