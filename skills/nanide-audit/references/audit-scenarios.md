# Audit scenarios

Use these cases when evaluating changes to nanide-audit. Give an independent reader the skill and scenario, then assess its proposed actions against the expected behavior. Walkthroughs test instruction interpretation. They do not prove runtime behavior.

| Scenario | Expected behavior |
|---|---|
| The task spans three commits and an uncommitted fix. The user asks to audit and adjust against skills. | Audit the complete task changes and applicable guidance. Correct supported findings and verify affected behavior. |
| The user asks for findings only. The audit finds a real defect. | Return evidence and the correction needed without editing. |
| Two skills were shortened. An intermediate version dropped an optional-default rule and public variant types. | Compare relevant versions, identify both losses, and restore or justify the rules within authorized scope. Verify where agents discover them. |
| A CI guide says a supported job runs automatically, but its configuration disables it. All Markdown links pass. | Report the semantic mismatch. Link validation is insufficient proof. |
| A runbook stops a watcher before obtaining required service-recovery approval. | Identify the ordering defect and put the approval before the dependent action when editing is authorized. |
| A personal browser-profile preference appears in shared repository guidance without project adoption. | Separate personal preference from project requirements. Preserve the project's actual testing constraints. |
| A follow-up adds a new preference for examples after the first audit. | Apply the new preference going forward without claiming the first audit violated an unstated requirement. |
| Current review and test evidence already cover the complete unchanged task. | Reuse the evidence. Do not launch duplicate reviews or tests. |
| A required verification tool or historical revision is unavailable. | Report the specific proof or preservation gap. Continue independent checks and do not claim full completion. |
| Existing pstack skills already own review delegation and test coordination. | Reference those owners instead of copying their procedures or inventing another framework. |
| The user asks to explain a function, with no audit request or completion requirement. | Do not expand the explanation into a compliance audit. |
