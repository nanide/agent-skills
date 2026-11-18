### Multi-phase or multi-PR plan

Write a plan when work has independently verifiable phases or PRs. Stop at the plan unless the operator also requested implementation.

1. Establish the outcome, base revision and authorized scope. Settle factual questions with existing evidence or a focused [prototype](prototype.md). Record remaining uncertainty. Save the plan according to [Execution state](../references/execution-state.md).
2. State who benefits and what they will see. Name the execution playbook and who owns landing. Use [Autopilot-full](autopilot-full.md) for independent PRs with landing authority, [Autopilot-stack](autopilot-stack.md) for an operator-landed stack, or [Orchestrate](orchestrate.md) for a standing program.
3. Write one section per change in dependency order. Give it a short, unique ID in the heading. Name every direct dependency by ID, or write `None`. List the files the owner can change and the result a caller can observe.
4. Choose evidence for each change. Name the unit check and exercise the real entry point. Give an input, expected result and receipt. A CLI can use stdout and exit status. An interaction change needs an operator review of the changed interaction and evidence the operator can inspect. A performance claim needs a metric, a repeatable probe, a comparable baseline and a numerical failure threshold. When performance or interaction review does not apply, give the reason.
5. Run the [installed checker](../scripts/check-plan.mjs) with `node <collection-root>/skills/mode/scripts/check-plan.mjs <plan.md>`. Resolve its diagnostics, then read the plan for details the checker cannot establish, including the scope of a file glob, whether two benchmark workloads are comparable and whether a proposed receipt proves the result.

Use the following Markdown for each change. Keep the field labels so the checker can find them. Use normal prose for the content. Include the plan title and summary before the first section. Additional reading and risks may follow in appendix sections.

```markdown
## LIST. Show the names of installed skills

- [ ] **Depends on.** None
- [ ] **Files.** `src/list.ts`, `tests/list.test.ts`
- [ ] **Build.** Sort installed skills by their public name.
- [ ] **Result.** With beta installed before alpha, the first line of stdout is alpha.
- [ ] **Unit.** Run the list-ordering test with both installation orders.
- [ ] **Live.** Run the installed list command in a temporary installation with both skills. Save stdout and exit status. Expect alpha then beta and exit zero.
- [ ] **Performance.** N/A. This change makes no timing or resource-use claim.
- [ ] **Review.** N/A. The command changes text order and has no interactive controls.
```

For a measured change, put four bullets under **Performance.** Label them `Metric.`, `Probe.`, `Baseline.` and `Limit.`. Put a number and the failure condition under `Limit.`. For an interaction change, describe what the operator reviews under **Review.** and add an `Evidence.` bullet naming the recording, screenshot, or interaction transcript. Existing full-format plans with a program checklist and PR sections remain supported.

**Reply.** Link the saved plan. Name the change IDs, dependencies and review gates. Give the checker result and any unproven assumptions.
