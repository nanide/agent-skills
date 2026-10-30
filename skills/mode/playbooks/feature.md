### Feature

**You own the design and result.** Scale the workflow to the uncertainty and blast radius.

1. Ground the affected behavior in current source and checks. Use `how` when the subsystem is unfamiliar or the behavior is unclear. Reuse applicable evidence from the current task.
2. Name the data shape and success criteria before writing logic. Use `architect` for consequential design choices with viable alternatives. An established pattern or narrow change can proceed directly.
3. For multi-step work, record the throughput checkpoint. Name blocking checks, independent workstreams, shared mutable state, and the smallest safe decomposition. Keep this concise. A single-owner change needs no fan-out plan. Split shared write targets before serializing them.
4. Implement the smallest coherent change. Work directly for a narrow change with clear ownership. Delegate separable work when it reduces the critical path or supplies needed independent expertise. Follow [Delegation](../references/delegation.md) and use the configured feature role. Use **arena** only when competing implementations will settle a consequential uncertainty. Give each writer the files, data shape, and success criteria. Re-ground upstream-derived edits against the source. Migrate shared-primitive consumers together and verify each.
5. Verify on the matching surface. "Inconclusive" or wrong-surface evidence is not a pass. Report missing proof.
6. For multi-phase work, create coherent, ordered phase commits after each unit passes its checks. Preserve completed phase history unless the user requests rewriting. Use **principle-sequence-verifiable-units** when sequencing the units.
7. Use `interrogate` for substantial changes or a contested design. Reuse independent review that covers the final scope and revision. Keep required independent review unmet when delegation is unavailable.
8. Run **Opening a PR** only when PR creation is authorized.

Keep tightly coupled implementation under one owner. Parallelize slices with independent artifacts or exclusive write ownership. Update the checkpoint when phase boundaries change ownership or dependencies.

**Reply:** what you built, the material design choices, verification, and open decisions. Include the throughput checkpoint only when it affected the work.
