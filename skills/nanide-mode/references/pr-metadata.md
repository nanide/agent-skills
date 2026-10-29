# Change PR metadata

Use these instructions only when Nanide is selected for the current task under [collection selection](../SKILL.md#select-a-collection-for-the-task). An explicit choice of another collection takes precedence over a repository default. Installation, a generic request, or reading and editing these instructions does not select Nanide.

Establish the requested result and actual target PR. Read applicable repository instructions, the current PR state, and the affected fields before acting. For an authorized label, assignee, milestone, draft-state, or similar metadata change, change only those fields and read them back. Preserve the body, title, base, code, and all unrelated metadata.

For "make this PR ready", recover whether the user means mark ready or fix blockers before mutating anything. Read status first if it helps establish intent. Ask only when the available context does not settle the action. Route fixes to [Babysit](../playbooks/babysit.md). A mark-ready request follows repository readiness requirements and [Opening a PR](../playbooks/opening-a-pr.md). Do not mark a PR ready while required validation remains blocked.

Route a stack-base change to the stack owner and applicable repository runbook. Do not bypass Babysit's frozen topology or [Shipping's rules](../playbooks/shipping.md) for a landing stack. Do not infer permission to rebase, force-push, merge, or reopen from a metadata request.

Follow [Opening a PR's forge, tool, and attachment rules](../playbooks/opening-a-pr.md). Report the changed fields, the readback evidence, and material gaps. Link the accessed PR. Do not claim that an unverified state has taken effect.
