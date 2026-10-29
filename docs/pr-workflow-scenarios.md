# Review PR workflow decisions

Use these cases to review [Nanide mode](../skills/nanide-mode/SKILL.md#work-on-a-pr) and its linked owners. They are instruction-review scenarios, not automated proof of model behavior. Unless a row says otherwise, Nanide is selected for the current task.

| Request and evidence | Expected decision |
|---|---|
| "Draft a body for PR 42." The PR is accessible. | Read its base, head, diff, and repository rules. Return a draft without saving, changing metadata, or starting monitoring. |
| "Change only the title." The diff includes a rename and a behavior change. | Use the title reference and summarize the whole PR. Save and read back only the title. Preserve the body and other fields. |
| "Open this PR." The branch is validated. | Use Opening a PR, shared title and body references, and the requested draft state. Follow worktree, commit, forge, attachment, and readiness rules. Return the URL without starting Babysit unless separately assigned. |
| "Set the label and assignee on PR 42." | Read the target and affected fields, change only those authorized fields, and read them back. Preserve all other fields and code. |
| "Mark PR 42 ready." Required validation is blocked. | Follow repository readiness rules and leave it draft. Do not infer permission to repair, merge, or reopen. |
| An Autopilot-full or Autopilot-stack owner opens its assigned PR. | Follow Opening a PR's assigned-owner exception. Start the already assigned Babysit loop after its code-ready report. Other opening requests do not start monitoring. |
| "Review PR 42." | Use Interrogate for code review. Do not rewrite the body from this request. |
| "Check on PR 42." | Use Babysit's single-pass status mode. Do not start a watcher or fix code from the status request. |
| "Watch PR 42, but do not change anything." | Use Babysit's read-only watch mode with its stop conditions. Do not push, reply, retry checks, or merge. |
| "Get PR 42 green." CI and review findings need fixes. | Use Babysit's repair mode. Keep stack topology frozen and respect reply authorization. Stop at merge-ready without merging. |
| "Merge PR 42 when ready." Checks are green. | Use Shipping and its independent verification gates. Green checks alone do not permit landing. Read the merge result back. |
| "Make PR 42 ready." The context does not distinguish marking ready from fixing blockers. | Read status if useful, then recover the intended action before a mutation. Do not infer either action or permission to merge. |
| "Update the body." The repository requires a specific PR template. | Preserve the template and required sections. Use the two-paragraph Summary and testing note only where compatible. A tiny PR may use a concise summary and validation note. |
| "Refresh the stack body." PR 41 is confirmed merged, PR 42 is current, and PR 43 is open. | Preserve stack order and links. Strike through PR 41. Bold PR 42's linked number, title, and "(this PR)" together, with exactly one current entry. Leave PR 43 unbolded and unstruck. If PR 42 is merged, strike through its whole bold entry. |
| The body claims a stack entry merged, but the forge cannot verify it. | Treat the body as context. Leave that entry's formatting unchanged and report the verification gap. Do not infer merge status. |
| A body update is ready to save, but the head or body changed since inspection. | Re-read both, refresh affected evidence, and reconcile new user content before saving. Read the saved body back against the reconciled head. |
| "Draft the body." The local checkout differs from the PR head. | Use the verified PR diff or inspect the correct head. Do not cite unmatched local files as evidence. Label any remaining evidence gap. |
| "Update the body." No connector or CLI can access the PR. | Return a labeled draft from available evidence and name what could not be verified or saved. Do not claim publication or silently switch collections. |
| "Change the base of this stacked PR." A Babysit run owns a frozen stack. | Route to the stack owner and repository runbook. Do not retarget, rebase, or force-push through a metadata shortcut. |
| The task explicitly uses pstack, then the user asks for a generic PR update. | Keep pstack despite an installed Nanide skill or repository default. An explicit switch to Nanide changes the current task's selection. |
| The user asks to edit Nanide mode or its PR references. | Treat the instructions as the artifact. Follow skill authoring without invoking PR lifecycle work from the edit alone. |
| A Goal completes and pushes changes with existing related PRs. | Use the Goal's description-refresh step only for verified personally owned PRs whose descriptions became inaccurate. Leave accurate bodies untouched, skip other or uncertain authors, record gaps, and create no PR from this step. |

For substantial changes, record actual route decisions, allowed actions, prohibited actions, and gaps in the task's review artifacts. Structural validation checks names and links. It does not establish these behavioral decisions.
