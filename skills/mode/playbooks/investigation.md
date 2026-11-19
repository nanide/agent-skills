### Investigation

**You own the answer. Plan, route, write.**

Investigation requests are read-only. They produce a cited explanation or a recommendation, not a code change.

1. Choose the helper for the requested answer. Use [teach](../../teach/SKILL.md) for a lesson paced to the reader, [blast-radius](../../blast-radius/SKILL.md) when asked what a change could break downstream, [why](../../why/SKILL.md) for motivation or history, and [how](../../how/SKILL.md) for mechanics, ownership, or a code walkthrough. Keep downstream checks within the investigation’s read-only scope and report any unverified assumption.
2. Throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only investigation`.
3. Return the selected helper’s answer with its evidence. For a choice between alternatives, give a recommendation with the tradeoffs.
4. Apply the [unslop](../../unslop/SKILL.md) skill to the reply.

No PR, no babysit, no `architect` unless the investigation precedes a code change. If it does, hand back to the user and re-route to Bug fix or Feature.

**Reply:** the investigation output. For "are we sure?" answers, include your real judgment with reasons. Push back if the premise is wrong (see Autonomy).
