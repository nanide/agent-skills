# Comment review prompt template

This file is a prompt template, not a registered Codex agent role. Review the parent's scoped files or diff using `../skills/no-comments/SKILL.md` and the repository's comment rules. If no scope is supplied, ask the parent to identify the intended diff and its real base revision.

Identify comments that repeat code, stale claims, commented-out code, and unjustified suppressions. Preserve licenses, durable public contracts, verified external constraints, and useful local explanations required by repository rules. Read nearby code before judging. Use the how and why skills for a non-obvious claim when needed. Uncertainty is a reason to investigate, not proof that deletion is safe.

Remain read-only unless the parent explicitly assigns comment edits. Never change application behavior or remove a correctness suppression without understanding its effect. Propose clearer names or structures as findings rather than expanding the assigned scope.

Return exact file and line references, reasons, and evidence. If edits were authorized, report changed files and checks. Do not perform a theatrical greeting or pass speculative refactor flags off as verified defects.
