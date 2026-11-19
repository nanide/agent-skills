### Bug fix

**You own this task. Plan, review, verify.** Investigate and fix narrow defects directly. Delegate independent hypotheses or disjoint fixes when useful, following [Delegation](../references/delegation.md).

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself on the matching surface following [Mode’s verification instructions](../SKILL.md#non-negotiables), even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Use [how](../../how/SKILL.md) for unfamiliar behavior and [why](../../why/SKILL.md) when regression history can distinguish the hypotheses. Reuse current evidence. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Continue a long hunt in the active turn with bounded tool waits and progress updates. Use the host scheduling tool only if the user explicitly requests future continuation. Confirm the surviving *mechanism* with runtime evidence before selecting the fix.
3. Plan the fix. Use [architect](../../architect/SKILL.md) for consequential design choices with viable alternatives. Request a design-only handoff and use the chosen sketch in the fix. Choose one owner for each fix. Delegate a separable scope using the configured bug-fix role when useful.
4. Before editing production code, use [tdd](../../tdd/SKILL.md) when the user requests a failing test, regression test, or TDD, or the bug has a cheap local test target. The fix owner follows its failing-test, fix, and passing-test sequence and returns the before-and-after output. If a focused test is impractical, record why and make the smallest fix justified by the reproduction. When committing a regression test, place its failing revision before the fix.
5. Rerun the original reproduction on the same surface after the fix. Report missing or inconclusive proof. Obtain independent review for substantial changes or a contested fix.
6. Run **Opening a PR** when PR creation is authorized.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
