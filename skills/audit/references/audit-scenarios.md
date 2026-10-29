# Audit scenarios

Use these cases when evaluating changes to audit. Give an independent reader the skill and scenario, then assess its proposed actions against the expected behavior. Walkthroughs test instruction interpretation. They do not prove runtime behavior.

| Scenario | Expected behavior |
|---|---|
| The task spans three commits and an uncommitted fix. The user asks to audit and adjust against skills. | Audit the complete task changes and applicable guidance. Correct supported findings and verify affected behavior. |
| The user asks for findings only. The audit finds a real defect. | Return evidence and the correction needed without editing. |
| A parent delegates an audit within an authorized implementation task without assigning corrections. The delegate finds a defect and an existing checkpoint. | Return the requirement source, artifact location, consequence, evidence, and needed correction. Do not edit the defect or checkpoint. The parent judges and coordinates fixes. |
| A delegate receives files but no approved outcome or complete change range and cannot access the parent's conversation. | Recover observable repository facts, report missing context to the parent, and continue independent checks. Do not invent intent, editing authorization, or a complete-task verdict. |
| A parent explicitly assigns corrections in one file and allowed checks within an authorized implementation task. The delegate also finds a defect in an unassigned file. | Correct and verify only the assigned work, preserve others' changes, and return the other finding to the parent. Do not commit or expand ownership. |
| A delegate finds that independent review and a shared browser verification session are required but neither is assigned. | Report the missing proof to the parent. Do not create another panel, take over the shared session, or claim completion. |
| Two skills were shortened. An intermediate version dropped an optional-default rule and public variant types. | Compare relevant versions, identify both losses, and restore or justify the rules within authorized scope. Verify where agents discover them. |
| A CI guide says a supported job runs automatically, but its configuration disables it. All Markdown links pass. | Report the semantic mismatch. Link validation is insufficient proof. |
| A runbook stops a watcher before obtaining required service-recovery approval. | Identify the ordering defect and put the approval before the dependent action when editing is authorized. |
| A personal browser-profile preference appears in shared repository guidance without project adoption. | Separate personal preference from project requirements. Preserve the project's actual testing constraints. |
| A follow-up adds a new preference for examples after the first audit. | Apply the new preference going forward without claiming the first audit violated an unstated requirement. |
| Current review and test evidence already cover the complete unchanged task. | Reuse the evidence. Do not launch duplicate reviews or tests. |
| A required verification tool or historical revision is unavailable. | Report the specific proof or preservation gap. Continue independent checks and do not claim full completion. |
| Existing pstack skills already own review delegation and test coordination. | Reference those owners instead of copying their procedures or inventing another framework. |
| The user asks to explain a function, with no audit request or completion requirement. | Do not expand the explanation into a compliance audit. |
