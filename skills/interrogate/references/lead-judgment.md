# Lead Judgment Framework

## Admit evidence before judgment

Use the evidence fields in [reviewer-prompt.md](reviewer-prompt.md). Verification and impact are separate decisions. Agreement is provenance, not proof.

For each behavioral claim, inspect the command and repro artifacts before running them. Reconstruct the recorded source snapshot in a clean lead-owned copy. Transfer only inspected repro files. Do not reuse reviewer-generated binaries or caches. Confirm that the disputed implementation is unchanged and that setup exercises the intended path. Follow repository execution approvals and avoid shared mutable test targets.

Rerun the command and inspect its output and resulting artifacts. Admit the finding only when the failure reproduces and violates the stated intent. Check the actual base or changed path before attributing a preexisting failure to the change. Missing dependencies, permissions, unsafe targets, or unavailable runtime state are verification gaps. A reviewer run without the lead rerun is not lead-verified.

For each structural claim, read the cited definitions and consumers in the snapshot. Confirm the present maintenance cost and that the proposed simpler shape preserves the stated behavior and constraints. A demonstrated ownership or instruction contradiction can survive without a runtime failure. An unrun behavioral claim cannot enter through this route.

Only verified findings enter Act on, Consider, or Noted. Dismiss disproven or irrelevant claims with a reason. Keep unresolved claims and blocked checks in verification gaps. Merge verified findings by root cause and retain their evidence. Check source drift before reporting so the verdict covers only the recorded snapshot.

## Filtering Principles

### Nitpick Gravity

Reviewers, especially adversarial ones, tend to fill their review. If they don't find critical issues, they'll inflate nits to fill the space. If a reviewer's findings are all nits and style preferences, the code is probably fine. Say so.

### Hypothetical vs. Actual

"What if someone passes null here?" is only a finding if the caller can actually pass null. Trace the call site. If the input is validated upstream or the type system prevents it, dismiss the finding. Reviewers working from a diff can't always see the full call chain. You can.

### Premature Abstraction Warnings

Reviewers often suggest extracting functions, adding interfaces, or creating abstractions. Does this code need to change in a second way? If not, the abstraction is premature. Simple inline code that works beats a clean abstraction that's overkill for the current scope.

### "I Would Have Done It Differently"

This is the most common false positive in code review. A finding that amounts to "I prefer a different approach" is not a bug, not a design flaw, and not actionable unless the reviewer shows a concrete problem with the current approach. Dismiss these, and say why.

### Missing Context Signals

Watch for findings that reveal the reviewer didn't understand the context:
- Suggesting changes to code the author didn't write or modify
- Flagging patterns that are consistent with the rest of the codebase (the reviewer just doesn't know that)
- Recommending approaches that conflict with constraints you know about

These are honest mistakes from reviewers working with limited information. Dismiss them gracefully.

## When Reviewers Are Right

Don't dismiss findings just because they're uncomfortable. The whole point of adversarial review is to catch things you'd miss. Signs a finding deserves attention:

- The evidence survives an independent rerun or direct source inspection
- The finding identifies a concrete execution path, not a hypothetical
- The finding reveals a gap in your mental model of the code
- You read the finding and think "...yeah, actually"

Be especially careful about dismissing security findings and correctness bugs. These deserve more scrutiny even when they come from a single model.
