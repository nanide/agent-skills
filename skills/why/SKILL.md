---
name: why
description: "Use for 'why does X work this way', design rationale, regressions, postmortems, or data-backed thresholds. Trace the decision through commits and PR discussions and cite the evidence. Use how for runtime behavior."
---

# Why

Find the decision behind the code. For a question about what runs today, use [How](../how/SKILL.md). Keep the investigation read-only, including searches through connected tools.

1. Identify the decision. Start from the named symbol, file, or change. If the target is implicit, state the interpretation you took from the conversation.
2. Trace the decision in order. Find the introducing commit and its PR discussion, then read the later changes that revised, reverted, or replaced the decision. Read that history and assess its answer before opening a design document, linked ticket, or any other source. Use local git history and the available forge tools. A diff can locate a decision. Attribute the reason to what an author wrote.
3. Stop when the record answers the question. Cite the reason and any later revision that changes its meaning. If the question also asks whether the reason still holds, check the relevant current evidence before answering that part.
4. Follow an unresolved question to the source likely to answer it. For example, open the incident linked by a retry change or the design proposal disputed in review. Use the [source guides](references/source-playbook.md) with an authorized connector or repository-approved CLI. Report a missing source when it limits the answer. Stop when the question is settled or the relevant leads run out.
5. Report what the authors said, what you infer, and what remains unknown. Attribute conflicting accounts to their sources. Distinguish a later reversal from an unresolved disagreement. For thin or disputed evidence, use the [confidence guide](references/epistemics.md). If the user plans to change the code, name the constraints that still apply.

For independent lines of inquiry, follow [Delegation](../mode/references/delegation.md). Give each read-only `why investigators` delegate the [investigator brief](references/investigator-prompt.md), the question, its source, and the commits or PRs already read. For a synthesis across multiple findings, use the [synthesis brief](references/synthesizer-prompt.md) and the `why synthesizer` role. Check the resulting citations before answering.
