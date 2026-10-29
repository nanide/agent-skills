# Write a PR title

Read the repository's title rules, applicable title skills, the actual base and head, and the complete diff. Repository conventions and applicable title skills take precedence over these defaults. For a stack, summarize this PR's change against its verified parent. Do not infer topology from branch names or an old body.

Summarize the whole change, including both sides of a rename or retarget when they define the work. Use a short, imperative subject with no trailing period. By default, use Conventional Commits, `type(scope): subject`, with an optional scope. Choose a type such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf`. Use `!` for a public breaking change when the convention calls for it.

Add a stack name or position prefix only when repository instructions, an applicable title skill, or a verified existing convention requires it. Ground the name and position in the actual stack. Never guess dependencies or require an external title skill to use this reference.

Apply [technical writing](../../nanide-technical-writing/SKILL.md) and [Unslop](../../nanide-unslop/SKILL.md). For a draft, return the title without saving it. For an authorized edit, re-read the current title and head before saving. Reconcile concurrent edits and refresh the summary if the head changed. Save only the title, then read it back. Preserve the body, base, state, code, and other metadata. Do not create a PR, start monitoring, or merge from a title-only request.
