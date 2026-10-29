# Provider-neutral workflow review

## Scope and source

Reviewed the original [pstack directory](https://github.com/cursor/plugins/tree/main/pstack), its [mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md), [Feature](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/feature.md), [How](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md), [Orchestrate](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md), and [Eval](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md) on 2026-10-29. This was a design comparison with upstream main, not a wholesale reimport. [upstream.json](../upstream.json) retains the original import pin.

The review covers shared instructions, references, executable helpers, discovery metadata, installation, and user documentation. Provider adapters target Codex, Cursor, and Claude Code. “Cloud” in the request was interpreted as Claude. Cloud-hosted execution depends on the selected application's capabilities.

## Decisions

| Finding | Change | Reason |
|---|---|---|
| Host tool assumptions were embedded in shared workflows | Move host instructions, metadata, and integration logic into provider folders | Keep one shared workflow with explicit capability fallbacks |
| Model configuration and delegation rules repeated across helpers | Use shared defaults and one delegation reference with provider-local overrides | Resolve each policy in one place |
| Small tasks required exploration and synthesis agents | Add a direct path and let the parent synthesize evidence | Avoid delegation with no distinct work product |
| Feature routing always escalated to design exploration | Reserve competing designs for material uncertainty | Keep review proportional to risk |
| Plans copied whole playbooks | Use concise task checkpoints | Avoid storing the same instructions twice |
| One nested discovery bundle assumed host recursion | Add explicit provider installs with flat links | Use the same source at each host's skill entrypoint |
| Review signals named a provider inside shared watcher logic | Extract the integration and retain its tests | Preserve readiness behavior without spreading service rules |

Keep the durable orchestration ledger and existing authorization boundaries. Do not copy upstream's model IDs, unconditional external-action permissions, or provider tool calls. The shared workflow supports absent tools by preserving checkpoints and reporting missing proof.

## Validation contract

Repository validation checks frontmatter, local links, metadata, configuration, and provider boundaries. Installer tests exercise all provider targets, dry runs, repeated installation, conflicts, switching, and removal. Watcher tests and typechecking protect the extracted integration.

A filesystem test is not a live application test. Before claiming live support for a host version, start a fresh session there, confirm discovery, and exercise the scenarios below. Do not infer a speedup from fewer instructions. No latency, cost, or quality improvement has been measured in this review.

| Request | Expected behavior |
|---|---|
| Explain one known utility | Read the utility and answer directly with evidence |
| Make a narrow, known behavior change | Implement and verify without compulsory design competition |
| Make a substantial uncertain design change | Explore distinct alternatives and obtain independent review |
| Inspect model configuration | Read effective settings without writing |
| Use an unavailable configured model | Report the mismatch and inherit unless the exact model is required |
| Resume a long task without native persistent execution | Read the checkpoint, reconcile artifacts, continue within the session |
| Review a PR | Review requested code without implicitly merging or scheduling |
| Schedule later work without a scheduler | Report the unavailable capability without claiming a schedule exists |

See [provider adapters](../providers/README.md) for official sources and installation details. Shared skills must remain usable when optional native features are absent.

## Review evidence

An independent same-model reviewer checked the instructional scenarios above and found stale guide text about mandatory design exploration and copying playbook steps. Those passages were corrected. Repository validation passed for all 59 skills. The watcher suite passed 68 tests and TypeScript checking. All 44 installer and validation tests passed. Independent installer review found a repeated-interruption recovery defect. The fix preserves prior link targets until success and rejects switching checkouts while recovery is pending. Regression tests cover both cases. These results establish repository behavior, not live discovery in each application.
