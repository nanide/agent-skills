---
name: nanide-pr
description: "For tasks that selected Nanide, handle PR descriptions, titles, creation, review, metadata, status, CI, and shipping through their canonical workflows. Use only for explicit invocation, an established current Nanide workflow, or an applicable repository default absent an explicit choice of another collection. Generic requests and installation alone do not select Nanide."
---

# Work on a PR

Apply this skill only when Nanide is selected for the current task under [collection selection](../nanide-mode/SKILL.md#select-a-collection-for-the-task). An explicit choice of another collection takes precedence over a repository default. Installation, a generic request, or reading and editing this skill does not select Nanide.

Establish the requested result and target PR or branch. Read applicable repository instructions and the current PR state before acting. Invoking this skill authorizes only the requested work, not every PR lifecycle action. Preserve existing authorization and collection context through follow-ups.

## Route the requested work

Read the owner for each requested action. A generic "review this PR" requests code review, not a body rewrite. For "make this PR ready", recover whether the user means mark ready or fix blockers before mutating anything. Read status first if it helps establish intent. Ask only when the available context does not settle the action.

| Requested result | Owner |
|---|---|
| Draft, rewrite, or review the body | [Write a PR description](references/descriptions.md). Return a draft or save only as authorized. |
| Draft or change only the title | [Write a PR title](references/titles.md). |
| Open a PR | [Opening a PR](../nanide-mode/playbooks/opening-a-pr.md). |
| Review the code or diff | [Interrogate](../nanide-interrogate/SKILL.md). |
| Audit instruction compliance | [Audit](../nanide-audit/SKILL.md). |
| Check status, watch, diagnose CI, fix blockers, or respond to review threads | [Babysit](../nanide-mode/playbooks/babysit.md). That playbook owns mode selection, polling, repair, and reply authorization. |
| Merge, land, ship, or merge when ready | [Shipping](../nanide-mode/playbooks/shipping.md). Preserve its independent verification and merge gates. |

For combined requests, follow each owner within the user's scope. Creating or editing a PR does not start monitoring. Repair does not authorize merging. Do not duplicate Babysit's mode logic or bypass Shipping because checks are green.

## Handle narrow metadata changes

For an authorized label, assignee, milestone, draft-state, or similar metadata change, read the affected fields, change only those fields, and read them back. Preserve the body, title, base, code, and all unrelated metadata. A mark-ready request still follows repository readiness requirements and [Opening a PR](../nanide-mode/playbooks/opening-a-pr.md).

Route a stack-base change to the stack owner and applicable repository runbook. Do not bypass Babysit's frozen topology or Shipping's rules for a landing stack. Do not infer permission to rebase, force-push, merge, or reopen from a metadata request.

## Use available tools and report the result

Follow [Opening a PR's forge, tool, and attachment rules](../nanide-mode/playbooks/opening-a-pr.md) for PR operations. Prefer a sufficient connected tool, otherwise use the resolved forge CLI. If a required tool or helper is unavailable, report the gap and continue independent authorized work. Return a labeled draft when useful. Do not claim that unsaved text, an unverified state, or a requested merge has taken effect.

Report what changed or what you found, the evidence checked, and material gaps. Link an accessed or created PR. For writing, apply [technical writing](../nanide-technical-writing/SKILL.md) and [Unslop](../nanide-unslop/SKILL.md).
