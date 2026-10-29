# Review collection selection

Use these cases to review selection decisions against [Nanide's selection guidance](../skills/nanide-mode/SKILL.md#select-a-collection-for-the-task). They are review scenarios, not automated proof of model behavior. Both collections can remain installed. The installer does not record the task's choice or change third-party skill descriptions.

| Current task and request | Expected decision |
|---|---|
| No collection selected. The user invokes `$nanide-audit` for completed changes. | Use Nanide's audit within the task's existing authorization. |
| No collection selected. The user invokes `$nanide-mode` for a PR body draft. | Use Nanide's description reference and return a draft without saving it. |
| The user selected Nanide earlier in this task, then asks for an audit or PR work. | Keep Nanide for the continuation. |
| The user selected pstack earlier in this task, then asks for an audit or PR work. | Keep pstack. The generic follow-up does not switch collections. |
| Both collections are installed. No task choice or repository default exists. The user asks for an audit or PR work. | Do not infer a Nanide choice from installation or the generic request. Follow applicable host and repository guidance. |
| The repository defaults to Nanide. The user explicitly chooses pstack for this task. | Follow the explicit pstack choice through the task, including generic follow-ups. |
| The repository defaults to Nanide. The user has made no explicit collection choice and asks for a completion audit. | Apply the repository default and use Nanide. |
| The current task uses pstack. The user explicitly switches to Nanide for the PR description. | Use Nanide for the requested work and retain the new choice for the task's continuation. |
| The user asks to edit or compare Nanide's audit or PR instructions. | Treat the skill as the artifact under review. Mentioning or reading it does not select its workflow. |
| A Nanide task requires a sibling helper. The discovery entry is a symlink. | Resolve the supplied entrypoint to its real directory, load the namespaced sibling, and preserve that absolute identity in delegate briefs. |
| A selected Nanide workflow requires a helper or tool that is unavailable. | Report the missing dependency and continue independent authorized work. Do not silently substitute a helper from another collection. |
| A new task begins after a previous Nanide task. | Establish selection from the new task and its applicable repository default. The previous task's choice does not create a persistent default. |

See [PR workflow scenarios](pr-workflow-scenarios.md) for action boundaries after selection.

For substantial instruction changes, review the applicable cases independently. Record the actual decisions, evidence, and gaps with the task's review artifacts. A passing structural validator establishes valid names and references, not these model decisions.
