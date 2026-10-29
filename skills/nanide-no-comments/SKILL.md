---
name: nanide-no-comments
description: "Review comments in the requested diff using repository conventions and preserve durable constraints."
---

# Review comments

Read the repository's comment rules first. Review only the requested files or current diff against the verified base branch. Do not sweep unrelated comments.

Use an independent read-only reviewer when available. Give it the diff, relevant source, and repository comment rules. Ask it to distinguish redundant narration from durable reasons, invariants, compatibility constraints, and required tooling directives. It must cite evidence for proposed changes and identify uncertainty.

For an edit request, remove or shorten only proven redundant or inaccurate comments within scope. Prefer clearer names where that makes the code easier to understand without broadening the task. Preserve license text, suppression directives, and non-obvious constraints unless their removal is independently justified. Uncertainty is not a reason to delete a comment. Do not rewrite application behavior to justify deleting a comment.

For a review-only request, return findings without edits. Report meaningful changes and unresolved constraints concisely. Follow repository validation rules if code or tooling directives change.
