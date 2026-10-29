---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
---

# Interrogate

Spawn independent reviewers to adversarially review code changes. Configured model diversity can expose different blind spots; same-model reviewers remain independent reviewers, not a diverse-model panel. The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, determine the actual base branch and run `git diff <base>...HEAD` for the full changeset.
- If the user's message references recent work, gather the relevant files.

When the user targets an existing PR for review, attach it to this chat using `attach_artifact`. Do not attach background references or dependencies.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the code. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Resolve `interrogate reviewers` in the effective configuration. A configured list sets the reviewer count. Otherwise use `panel_size` (default two), each inheriting the parent. Label seats Reviewer A, B, and so on.

Resolve this skill directory through symlinks. Read `../../codex-config.local.json` if it exists, otherwise `../../codex-config.json`. The local file replaces the defaults. Reject an invalid local file rather than falling back. Resolve the named role from `roles`, falling back to `default_model`, then `inherit-parent`. `auto` and `inherit-parent` mean omit model and reasoning overrides. An explicit role is an object with `model` and optional `reasoning_effort`. Validate it against the current spawn tool and use the context-inheritance mode that permits overrides. If unavailable, report the mismatch and inherit the parent unless the user requires that exact model. Never substitute another model family. Report the actual models used and distinguish independent same-model reviews from model diversity.

Use the available Codex collaboration tools to spawn, inspect, message, and wait for subagents. Respect current concurrency limits and queue excess work. Spawns run asynchronously. Give each brief its scope, absolute skill/reference paths, and expected evidence. Read-only is an instruction in the brief, not a tool permission flag. Give writers exclusive files or an isolated worktree, tell them they share the codebase, and forbid reverting others' work. Do not create user-visible chats as substitutes for subagents. If delegation is unavailable, report that limitation and perform the scoped work directly without claiming independent review. Every reviewer is read-only.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the stated intent, the diff or file contents, the rubric from `references/rubric.md`, and the code-quality lens from `references/code-quality-review.md`. Use only supported model and reasoning overrides from the role configuration.

## Step 4, Synthesize

As results come back, build a unified picture. Parse every reviewer's findings. Merge findings that describe the same issue differently, and note which models raised each one. Findings two or more models raised independently are the highest signal. Read a lone model's finding, but weight it accordingly. Note disagreements. If one model flags something and another explicitly says the opposite, that is context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Put every finding in one of four buckets, with the model(s) that raised it and a one-line rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. They would block a real PR.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output Format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On
[Each: description, which models raised it, why it matters.]

### Consider
[Each: description, which models raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where models agreed and diverged, and what that pattern tells us.]
