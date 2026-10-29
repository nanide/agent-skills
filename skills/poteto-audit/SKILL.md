---
name: poteto-audit
description: "Audit completed task changes against applicable skills and instructions, including changed skills and documentation. Use for completion audits, requests to align work with skills, or audits of new guidance. Apply corrections within the existing task authorization."
---

# Poteto audit

Audit the complete requested work and its guidance. Produce evidence-backed findings, authorized corrections, and an accurate account of remaining gaps.

Use the user's scope and existing authorization. Audit-only and planning requests stay read-only. An audit within an authorized implementation task includes necessary scoped corrections. Do not ask again for permission already given. This skill adds no authorization for publishing, external messages, branch resets, Goals, or schedules.

## Establish the audit boundary

Recover the approved outcome, later corrections, and acceptance criteria from the current task. Identify the actual base and complete task changes, including earlier commits, uncommitted work, and relevant generated artifacts. Preserve unrelated work.

Read applicable repository instructions, skills, and runbooks. Select them by the changed behavior and artifacts, not only those loaded during implementation. Separate requirements from preferences and unrelated guidance. Resolve conflicts using instruction priority and explicit user intent.

Use relevant prior audit results and follow-ups when available. Compare the original request, the agent's result, the user's correction, and the resulting change. Distinguish a missed requirement, an audit-induced regression, a new preference, added scope, and unresolved uncertainty. Verify reported fixes against artifacts before treating them as proven. Do not search unrelated chat history by default or treat historical messages as new authorization.

## Check implementation and evidence

Map applicable requirements to the changed artifacts and proof. For substantial audits, record a compact table in the existing task checkpoint, or report it directly when no checkpoint exists. Include the requirement source, artifact location, evidence, and disposition. A small audit can report this directly.

Check intent, behavior, architecture, naming, tests, comments, and configuration under their owning guidance. Include integration points and affected callers. Reject tests that merely repeat declarations when the repository requires meaningful behavioral proof.

Inspect actual commands, configuration, and execution order behind documentation claims. Check that prerequisites and required approvals precede dependent actions. Structural validation and reviewer agreement do not prove operational correctness.

Reuse existing review and verification only when their scope and artifact state cover the current work. Use [interrogate](../interrogate/SKILL.md) for required independent review. Include the applicable requirements and preservation concerns in its brief. Use [swarm](../swarm/SKILL.md) for delegated verification when useful or required. Repository verification skills own commands, target approvals, and shared resources. Do not create a second review panel or test run merely because this skill was invoked.

## Audit changed skills and documentation

Read this section when guidance changed or the user explicitly requests its audit. Inspect nearby owners before adding another procedure.

Keep each durable rule in its owning skill or runbook and link to it elsewhere. Keep personal tool and profile preferences in personal guidance unless the project explicitly adopts them. Remove stale claims, duplicated procedures, unnecessary clarification gates, and incidental implementation narration.

Before consolidation or deletion, compare the original and intermediate versions relevant to the task. Account for each durable requirement as retained, moved, intentionally changed, or removed with a reason. Check the final destination and its discovery path. If earlier versions are unavailable, report the preservation limit. Do not claim nothing was lost.

Keep entrypoints focused on task selection and common execution. Load detailed references conditionally. Put concrete examples in a separate examples section or linked reference. Delete unnecessary text rather than moving all of it elsewhere.

For skill edits, use [Authoring a skill](../poteto-mode/playbooks/authoring-a-skill.md) for metadata, links, tool contracts, invocation policy, and representative behavioral checks. Keep this procedure in its existing owner.

## Resolve and finish

For each actionable finding, state the violated requirement, artifact location, consequence, and required correction or proof. Distinguish confirmed defects from suggestions and uncertain claims. The parent judges findings and coordinates fixes within scope. Route skill corrections through the authoring playbook. Never weaken guidance merely to excuse a noncompliant implementation.

Rerun checks affected by corrections and review the corrected requirements. Preserve evidence that remains valid. If a required tool or source is unavailable, continue independent work and report the missing proof. Stop when scoped requirements have adequate evidence or the remaining work requires unavailable access or authorization. Record out-of-scope findings without expanding the task.

Report scope, meaningful corrections, verification tied to the final artifact state, unresolved requirements, and follow-ups. Keep clean results brief. The caller owns commits, publishing, and Goal lifecycle. Missing required proof prevents a completion claim.

## Evaluate changes to this skill

When changing this skill, exercise [audit scenarios](references/audit-scenarios.md). These cases test decisions and preservation, not exact wording.
