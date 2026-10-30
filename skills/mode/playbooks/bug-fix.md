### Bug fix

**You own this task. Plan, review, verify.** Investigate and fix narrow defects directly. Delegate independent hypotheses or disjoint fixes when useful, following [Delegation](../references/delegation.md).

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Reproduce it yourself on the matching surface via the available surface tools (Non-negotiables), even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Use `how` for unfamiliar behavior and **why** when regression history can distinguish the hypotheses. Reuse current evidence. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Continue a long hunt in the active turn with bounded tool waits and progress updates. Use the host scheduling tool only if the user explicitly requests future continuation. Confirm the surviving *mechanism* with runtime evidence before selecting the fix.
3. Plan the fix. Use `architect` for consequential design choices with viable alternatives. Implement a narrow fix directly, or delegate a separable scope using the configured bug-fix role. Obtain independent review for substantial changes or a contested fix.
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Stage the commits so the failing repro lands before the fix in git history. See the **tdd** skill for the failing-test-first cadence when the bug has a cheap local test path. Skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical **principle-sequence-verifiable-units** principle skill, the failing test first and the fix on top.
6. Run **Opening a PR** when PR creation is authorized.

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
