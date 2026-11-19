---
name: automate-me
description: "Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill with bundled authoring guidance and unslop, optionally pulling fresh evidence from recent transcripts."
---

# Automate me

A guided flow for turning the user's working conventions into a skill agents will follow. The output is one `-mode` skill tailored to them (e.g. `jay-mode`, `priya-mode`).

This workflow combines the inline mining pass in step 1, [Authoring a skill](../mode/playbooks/authoring-a-skill.md), and the bundled [unslop](../unslop/SKILL.md) skill.

Follow [Delegation](../mode/references/delegation.md) for the active provider’s role configuration.

## Flow

### 0. Check for an existing skill

Look for a matching mode in the active host’s configured personal skill directory and any explicitly supplied repository skill directory. Use the [provider adapter](../../providers/README.md) to locate these. Include existing category directories. If one exists, confirm intent with the available user-input tool or chat (unless they already said "update my skill" or similar):

- Update the existing skill (default for repeat runs)
- Start fresh (rare, ask why before doing it)

Update mode changes the rest of the flow:
- Step 1 uses history since the last edit when that date is known. Use Git history only for tracked skills; otherwise report the available time boundary.
- Step 2 asks what's changed or missing, not what to capture from zero.
- Step 4 edits the existing file in place. Preserve sections the user hasn't contradicted. Revise ones with new evidence. Add new sections only for genuinely new rules.

### 1. Mine their history

Use the current conversation and available list/read chat tools. Limit retrieval to the requested project, topic, and time window. Do not scan unrelated private chats or guess transcript paths. When only summaries are available, label that evidence limit.

For a broad history request, delegate separate time or topic slices to read-only subagents using the current spawn tool. Give each the exact allowed chat IDs or scope. Inherit the parent model unless the effective configuration has a supported explicit role override. Workers return patterns and evidence references without messaging the source chats. Default signals worth hunting:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, specialized workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint/format tools)
- Process conventions (worktrees, commits, PRs, review/merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Cross-check across slices before elevating a signal. Patterns seen in 2+ slices are high-confidence. Lone signals are weak and usually get dropped.

### 2. Ask the user directly

Mining misses intent that hasn't come up yet. Use an available user-input tool when it fits the question, or ask concisely in chat.

Ask one or two focused questions using the tool's actual schema and mode restrictions. Use plain chat when no input tool is available. Do not invent multi-select fields. Skip questions already answered by the request or reliable evidence.

Don't dump 20 questions.

### 3. Cluster findings

Group the combined signals into sections. Common ones (use only what applies):

- **Response style**: length, tone, format.
- **Autonomy**: how much to do without asking, MCP tool use.
- **Understand first**: which skills to reach for when scoping or investigating a change.
- **Subagents**: default, parallelism, model-to-task, specialized workflows.
- **Prose / code discipline**: principles, lint tools, style guides.
- **Review and verify**: repro posture, verification skills, live-testing tools.
- **Process**: git worktrees, commits, PRs, review/merge tooling.
- **Skills**: skill-authoring habits, fix-the-skill-first, proposing new skills.

The [mode](../mode/SKILL.md) skill shows the shape. Read it for granularity. Don't copy its content. The user's rules are not the same as mode's.

### 4. Draft the skill

Follow [Authoring a skill](../mode/playbooks/authoring-a-skill.md) to author the skill. Placement:

- Path: preserve an existing mode skill’s category. For a new personal mode, use the active provider’s personal skill directory. Use a repository location when requested, following its conventions.
- Handle: the user's first name or chosen identifier.
- Frontmatter `description`: trigger on their name + `$<handle>-mode` + "work in their style", not on generic keywords like "write code" or "review PR".
- Frontmatter formatting: follow the bundled authoring playbook. Keep `description` as one YAML scalar. Quote it or use `description: >-` with indented continuation lines when punctuation or wrapping requires it.
- Preserve existing invocation policy. For a new skill, use the host’s normal discovery behavior unless the user requests explicit-only invocation. Keep provider-specific metadata in that provider’s adapter and use its supported format.

### 5. Iterate on prose

Apply the bundled [unslop](../unslop/SKILL.md) skill and authoring playbook to every line.

Show the draft to the user and take feedback. Expect multiple iterations. Cut ruthlessly. A mode skill is not a manual.

### 6. Land it

Validate the saved skill and its local links with the checks in the bundled authoring playbook. Personal skills need no repository or PR. For requested repository delivery, follow its branch and PR runbooks and use the verified base branch. Do not publish unrelated configuration.

## Guardrails

- **Don't overfit to one conversation.** A preference stated once and contradicted another time is noise. Require multiple instances before codifying it.
- **Don't be clever.** Restating other skills' contents, inventing metaphors, or writing "poetic" prose for an agent reader is cost without benefit. Keep it operational.
- **Keep dependencies within Nanide skills.** Link bundled guidance by its verified path. Encode the user's specific conventions directly when no bundled guidance covers them. Do not require another installed skill. Honor applicable repository instructions and runbooks.
- **Keep sections minimal.** Only add a section if the user has a specific, non-default rule there. "Communicate clearly" is not a section. "Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." is.
- **Name conventions generic.** Use "the user" or "the human" in imperatives, not the author's first name.
- **Don't force symmetry.** If a user has no process rules worth writing down, skip the Process section entirely.

## Evaluation

A `-mode` skill has subjective prose choices. Validate its structure and check any operational rules with representative scenarios. A benchmark loop is unnecessary for a tone-only edit. Vibe-check with the user: does it read like them? Did it miss anything? Then ship.

Run a description-optimization loop only if the skill's trigger accuracy turns out to be a problem in practice.

## When not to use

- User wants a task-specific skill (not working conventions): [Authoring a skill](../mode/playbooks/authoring-a-skill.md), no mining required.
- User wants to capture one narrow workflow (e.g. "how I write commit messages"). That's a regular skill, not a mode skill.
