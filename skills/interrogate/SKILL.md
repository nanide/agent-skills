---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Independent reviewers prove behavioral defects and ground structural findings in the actual source."
---

# Interrogate

Challenge the requested change or design with independent reviewers. Verify their evidence before assigning a verdict. Preserve concrete structural review. Do not apply fixes or post external comments.

## 1. Frame the subject

Use the scope the user names. For a branch review, determine the actual base and merge base. Review the diff from that merge base through the working tree unless the request explicitly excludes local changes. Include relevant staged, unstaged, and nonignored untracked files. Exclude unrelated work and secrets.

Record the intent, base, HEAD, scoped paths, and snapshot inputs. Capture tracked changes from HEAD as a binary-capable patch and explicitly list included untracked files. Check that the source did not change while capturing it. A commit hash alone does not identify uncommitted work.

For a design or named-file review, record the exact files and versions instead of inventing a branch comparison. State the intended behavior from the request and available commits or PR description. Ask only when the intent remains unclear after inspecting that evidence.

When reviewing a requested PR, link it in this chat and use the active provider's attachment capability when available. Do not attach background references or dependencies.

## 2. Prepare independent reviewers

Resolve `interrogate reviewers` in the effective configuration. A configured list sets the reviewer count. Otherwise use `panel_size`, default two, inheriting the parent. Report actual models. Same-model independence is not model diversity.

Follow [Delegation](../mode/references/delegation.md) and [Execution state](../mode/references/execution-state.md) for supported tools and checkout lifecycle. The author checkout and external state stay read-only. When a reproduction can write files, give each reviewer an owned disposable checkout or copy plus explicit repro and build-output paths. Reconstruct the recorded source snapshot, including deletions, binary changes, file modes, and selected untracked files. Verify its contents before running checks. Worktree creation alone does not copy local changes.

Reviewers may create temporary tests or repro scripts only in their assigned paths. They may not change implementation behavior, dependency declarations, or another reviewer's artifacts. Commands follow repository target and service-recovery rules. An isolated checkout does not authorize shared-service or external-state changes.

If isolation is unavailable, continue source inspection and genuinely read-only checks. Report blocked runtime checks instead of running writing commands in the author checkout. If delegation is unavailable, follow the provider fallback and report missing independence. A required independent-review gate remains unmet.

## 3. Collect evidence

Fill [reviewer-prompt.md](references/reviewer-prompt.md) for every reviewer with the same intent, source snapshot, [rubric](references/rubric.md), and [code-quality lens](references/code-quality-review.md). Supply each reviewer's owned paths and execution constraints. The template owns the evidence fields.

Behavioral findings require a run against the actual disputed code. Structural findings require a concrete source trace, present maintenance cost, and feasible simpler shape. Do not turn an unrun behavioral or security claim into a structural finding to avoid reproduction. Unavailable or unsafe checks remain verification gaps.

## 4. Verify before judging

Read each finding and its artifacts. Follow the evidence admission rules in [lead-judgment.md](references/lead-judgment.md). Inspect commands before executing them. Rerun behavioral evidence in a clean lead-owned copy of the same snapshot with only inspected repro artifacts. Do not reuse reviewer-generated binaries or caches. Stop conflicting writers before verification and preserve repository execution approvals.

Inspect structural evidence directly in the cited definitions and consumers. Do not require a fake failing test for an instruction contradiction or a material ownership problem. A structural finding can block approval when its current cost is demonstrated.

Merge verified findings by root cause. Preserve evidence from each reviewer. Agreement records provenance and can guide investigation, but it never replaces proof. Investigate a lone security or correctness finding on its merits.

Assign the existing judgment buckets only after evidence verification. Use **Act on** for material issues that block the requested change, **Consider** for supported tradeoffs, **Noted** for supported context, and **Dismissed** for rejected claims with reasons. Missing proof belongs under verification gaps, not a verified bucket or silent dismissal.

Before reporting, check whether the source changed since the snapshot. Name the snapshot actually reviewed and exclude newer edits from the verdict. Retain referenced repro artifacts and logs before cleaning up only owned checkouts and processes.

## Output

Report the following:

- **Intent and scope.** State the goal, base or named files, reviewed snapshot, included local changes, and any drift.
- **Reviewers.** Name each reviewer and actual model. Report missing independence or coverage.
- **Act on, Consider, and Noted.** Give each finding's evidence kind, locations, concrete impact, lead verification, and contributing reviewers. Include commands, expected and observed output, and artifact paths for behavioral findings.
- **Dismissed.** Give each rejected claim and the concrete reason.
- **Verification gaps.** Name each blocked or unverified claim, attempted check, missing prerequisite, and next safe check.
- **Agreement map.** Note independent agreement and disagreements without treating votes as proof.

No findings is a valid result. If checks remain blocked, say that no findings were verified and list the gaps. Do not call that a clean review.
