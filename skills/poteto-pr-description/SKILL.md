---
name: poteto-pr-description
description: Write or update PR descriptions with the main change first, evidence-backed details about behavior and output, and focused guidance for reviewers. Use when drafting, rewriting, or refreshing a pull request body. Does not cover title-only edits or PR status monitoring.
---

# PR descriptions

Write a briefing for a reviewer who has not seen the conversation. Lead with what the PR changes and why that matters. Explain the consequential details, effects on consumers and maintainers, and what deserves review. Adapt the length and sections to the change rather than filling a fixed template.

## Establish the current scope

Read the existing description, actual PR base and head, and complete diff against that base. Read repository PR instructions. For stacked PRs, describe what this PR adds over its parent, not the cumulative change against the default branch. Confirm that local files match the PR head before using them as evidence.

Use the existing body as context, not proof. Remove claims that belong to earlier revisions or other PRs. Preserve useful issue links, stack context, and repository-required sections. Keep stack history below the main explanation unless the repository requires otherwise. In the stack section, bold the current PR’s linked number, title, and “(this PR)” marker as one entry. Identify it by the PR being described, and leave the other entries unbolded so exactly one PR stands out.

Check the current merge status of each PR in the stack through an available connector or CLI. Wrap each confirmed merged entry, including its linked number and title, in Markdown strikethrough (`~~...~~`). Preserve stack order and links. If the current PR is merged, apply strikethrough around its bold entry. Do not strike through open PRs or PRs closed without merging. If merge status cannot be verified, leave that entry's formatting unchanged and report the verification gap.

Inspect the implementation and relevant callers, build configuration, or tests to establish important claims. Distinguish an intended guarantee, a guarantee enforced by code, and a result demonstrated by a test or run. If evidence is missing, qualify or omit the claim and identify a consequential verification gap.

## Put the main point first

Write the Summary as two short paragraphs. The first says what changes. The second states the main benefits for users or maintainers, such as a failure avoided, a workflow made easier, or a capability enabled. Keep each to one or two sentences. Do not lead with a file inventory, stack bookkeeping, or a generic claim about improvements.

The benefits paragraph must add the practical value of the change rather than paraphrase its implementation. Ground benefits in the diff and available evidence; distinguish intended benefits from demonstrated results, and do not invent performance gains or guarantees. Put implementation mechanics, compatibility boundaries, and review-sensitive details in a separate section such as Important details. Reserve those facts for that section instead of previewing them in the Summary.

In the details section, give just enough context to understand how the affected area works. Describe the most important changes in order of consequence and connect each implementation detail to its effect. Include symbol names and paths only when they help the reviewer locate or understand that effect.

## Explain consequences and compatibility

Choose the relevant dimensions of impact. These may include generated code and artifacts, runtime behavior, API responses, stored data, configuration, dependencies, developer commands, CI, deployment, or supported environments. Do not force every dimension into every PR.

For build or tooling changes, distinguish changes to the build process from changes to what ships or runs. For other work, make the equivalent distinction between internal mechanics and observable behavior.

Mention preserved contracts when a reviewer could reasonably worry that the change affects them. Verify their preservation through the diff and surrounding code. For example, preserving an output format does not establish identical bytes, ordering, performance, or runtime behavior. Avoid blanket claims that nothing changes and generic lists of untouched areas.

Describe compatibility breaks and required actions concretely. Include architectural choices or tradeoffs only when they explain the final design. Do not invent rejected alternatives or retell abandoned implementation attempts.

## Identify review areas

Call out the interactions, boundaries, or failure modes most likely to need careful review. Explain the consequence to check, not just the component's name. Prefer specific guidance such as checking that shared styles load before an entry script over asking reviewers to check edge cases.

When describing a policy check or validation gate, trace where it runs and what makes it fail. State relevant exceptions, flags, and environment conditions. A helper's existence does not prove that the build or CI invokes it. A configured check does not prove that the current head passed it. Do not describe a narrow rule set as comprehensive policy compliance.

## State validation accurately

After the two Summary paragraphs, add a one-sentence testing summary. Name the applicable coverage or completed checks, such as unit tests, manual Storybook checks, automated Storybook tests, or E2E tests. Distinguish existing coverage from tests actually run, and briefly note when validation is missing. Leave commands, individual cases, and detailed results for the later Test plan.

Separate completed validation from the remaining test plan. Record only observed results or explicitly attributed prior evidence. Identify results from an earlier revision when they do not establish the current head's status. Distinguish building an artifact from exercising it, and mocked integration coverage from a real external integration run.

For description-only work, inspect available evidence without launching unrelated test suites, deployments, or monitoring. Follow repository rules for any verification that the task does require. Keep pending checks unchecked and report material limits without presenting them as failures.

## Shape and deliver the description

Use Summary followed by a clearly separate details section when there are details worth highlighting. Add Review areas, Compatibility, or Test plan only where they serve a distinct purpose or the repository requires them. A small fix may need only a summary and a validation note.

Give each fact one home. Do not repeat a change in the summary, expand it in details, then restate it as a review bullet. Keep a consequence and its review concern together when they concern the same fact. Validation should add evidence or a remaining check, not repeat the implementation description. Before saving, read across sections and remove repeated claims, including paraphrases; retain a repeated reference only when it adds a distinct constraint, result, or action.

Use plain language, concrete verbs, and short paragraphs. Reuse the codebase's names. Avoid promotional language, invented jargon, long dashes, and bold labels that merely repeat the sentence. Keep the opening readable in under a minute. Add detail only when it changes a reviewer's understanding or next action.

If the user asks for a draft, return a draft. If the user authorizes updating the PR body, save it with an available connector or CLI and read it back to verify the saved text. Preserve the title, base, state, and other metadata. Do not create comments, change code, merge, or start monitoring as part of a description update.

If the PR cannot be accessed, use available evidence to produce a clearly labeled draft and state what could not be verified or saved. Do not claim publication. Before saving, check whether the head or body changed during the work and reconcile any relevant changes without overwriting new user content.
