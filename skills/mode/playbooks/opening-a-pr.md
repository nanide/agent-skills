### Opening a PR

Use when opening a PR is within the requested task. Investigations and local-only tasks do not open PRs.

**Worktree.** Inspect the current branch, status, and intended PR base. Preserve existing changes. Reuse a suitable checkout or create an isolated worktree when needed. Never hard-reset a shared or dirty checkout. Follow the repository branch and PR runbooks and the [native worktree lifecycle](../references/execution-state.md#worktrees).

**Commits.** Commit each completed, reviewed, validated phase before starting the next. Preserve those phase commits unless the user requests history rewriting. Commit bodies don't restate the subject.

**PRs.** Apply the bundled [diff cleanup](../references/diff-cleanup.md) before commit and `no-comments` before review. Write every PR title, description, and commit body with `technical-writing` (every layer except Diátaxis, and apply the STE vocabulary rules: one word per action, keep articles, a plain verb over `-ing` where one works), then apply `unslop`.

**Titles and descriptions.** Use the shared [title instructions](../references/pr-titles.md) and [description instructions](../references/pr-descriptions.md) directly. Repository templates and required sections take precedence over the default body structure. The body is a one-minute briefing, not a lab notebook. Where the body becomes the squash commit body, keep it under about 40 lines when the required content permits.

Attach videos or screenshots when they prove a claim. Full SHAs, swarm or arena lane recitals, lever-correction essays, file-by-file checklists, and "CLEAN" verdicts go in a linked artifact, not the body.

**Forge.** Resolve the forge before the first PR operation and keep that choice for create, edit, view, watch, and merge. GitHub CLI (`gh`) is the default. If `command -v origin` succeeds and Origin can resolve the repository, prefer `origin pr ...`. If Origin is absent or cannot resolve the repository, stay on `gh` and record the fallback. Do not require Graphite (`gt`).

**PR tools.** Prefer connected GitHub tools when sufficient; otherwise use the repository’s forge CLI. Link every created PR in the current chat. Use the active provider’s attachment capability when available, including for an existing PR the user asks to review, update, or continue. Exclude background references and dependencies. If a required tool or helper is unavailable, report the gap and continue independent authorized work. Return a labeled draft when useful. Do not claim that unsaved text, an unverified state, or a requested merge has taken effect.

**Size and stacks.** Prefer five narrow PRs to one large PR. A stack is a base-branch chain. The root PR targets trunk. Each child branch rebases onto its parent's exact tip and its PR targets the parent branch. As a parent merges, move its child onto trunk per `playbooks/shipping.md` step 4. Without a built-in PR tool, per the resolved forge, create a child with `origin pr create --status open --base <parent-branch>` or `gh pr create --base <parent-branch>`, and retarget one with `origin pr edit <pr> --base <parent-branch>` or `gh pr edit <pr> --base <parent-branch>`. Branch from trunk only for independent work. Rebase on trunk before substantial stack work.

**Readiness.** Follow the user’s requested draft status and repository runbook. Do not mark a PR ready while required validation remains blocked. Attach created PRs to the current chat when the attachment tool is available.

**Babysit.** Opening a PR does not start a babysit. Post the URL and keep building. Finish the phase or stack first. Run a separate babysit pass only when the user asks for one after the whole stack exists. A babysit for each new PR stalls the build and spends checks on commits later waves restart. Push back when feedback drifts from intent.

A subagent that opens a PR runs `interrogate`, the focused diff cleanup above, and `no-comments`, and posts the URL. It returns to the parent without babysitting, unless it is an Autopilot-full or Autopilot-stack owner. That owner's brief assigns the babysit loop and is the ask `playbooks/babysit.md` waits for. The owner starts the loop after its code-ready report, reports merge-ready or STACK-READY per its playbook, and is exempt from the rules here and in `playbooks/babysit.md` that hold babysitting until a whole stack is built.
