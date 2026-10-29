# Diff cleanup

Review the complete task diff before committing. Remove redundant logic, narrating comments, unsupported defensive checks, dead compatibility paths, and accidental unrelated edits. Preserve behavior and constraints that the code or repository evidence establishes. Do not remove a guard merely because it looks defensive.

Use the bundled [nanide-no-comments](../../nanide-no-comments/SKILL.md) review for comments and [nanide-unslop](../../nanide-unslop/SKILL.md) for prose. Keep cleanup within the authorized change. Run checks affected by any behavioral correction and report remaining gaps. No separate cleanup skill is required.
