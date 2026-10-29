# Skill catalog

`$nanide-mode` resolves its own sibling helpers. Every helper uses its namespaced public selector. See [collection selection](installation.md#choose-a-collection-for-the-task) for explicit choices and optional repository defaults.

## skills

[`$nanide-mode`](../skills/nanide-mode/SKILL.md) runs most of these for you when a step needs them (`nanide-how`, `nanide-why`, `nanide-architect`, `nanide-arena`, `nanide-swarm`, `nanide-interrogate`, `nanide-unslop`, `nanide-no-comments`, `nanide-technical-writing`, `nanide-tdd`, and the principles). the table below is for when you want one directly:

```
$nanide-how do we cancel runs? do we have an n+1 when we look up every run to cancel?
```

```
$nanide-interrogate review this pr.
```

<details>
<summary>all skills</summary>

| skill | use it when |
|---|---|
| [`$nanide-mode`](../skills/nanide-mode/SKILL.md) | default entry point for any non-trivial task. |
| [`$nanide-help`](../skills/nanide-help/SKILL.md) | you're new to the collection, or unsure which skill, playbook, or principle fits. finds out what you're trying to do, answers that part, and hands you a prompt to type. runs only when you type `$nanide-help`. |
| [`$nanide-in-your-own-words`](../skills/nanide-in-your-own-words/SKILL.md) | you want the agent to play back your goal and the problem before it starts. runs only when you type `$nanide-in-your-own-words`. |
| [`$nanide-sharpen`](../skills/nanide-sharpen/SKILL.md) | you want a prompt made deeper, not bigger, before you send it: what a top professional would do that you didn't ask for, the raw material they'd start from, their methods and tools, and an outside check that the result is right. hands back the rewritten prompt and leaves your choices open. doesn't do the task. runs only when you type `$nanide-sharpen`. |
| [`$nanide-how`](../skills/nanide-how/SKILL.md) | you want a walkthrough of how a subsystem works. |
| [`$nanide-why`](../skills/nanide-why/SKILL.md) | you want to know why something was built this way. discovers available MCPs at run time and queries each evidence category in parallel (source control, issue tracker, long-form docs, real-time chat, infra observability, error tracking, analytics warehouse). |
| [`$nanide-recall`](../skills/nanide-recall/SKILL.md) | you're starting or resuming work and want your recent context on a topic rebuilt from your own chat history and the shared record, handed back as a tight current-state brief. |
| [`$nanide-ketchup`](../skills/nanide-ketchup/SKILL.md) | you want what changed in this chat since your last message, in plain words and small visuals, with every item waiting on you listed and decidable from the reply alone, even when that makes the reply long. |
| [`$nanide-blast-radius`](../skills/nanide-blast-radius/SKILL.md) | you have a small-looking change and want to know what else it could break, with the one fact it's safe because of proven by running code, not asserted. |
| [`$nanide-architect`](../skills/nanide-architect/SKILL.md) | you're about to write code that crosses a function boundary and want the caller's usage, types, and module shape settled first. |
| [`$nanide-arena`](../skills/nanide-arena/SKILL.md) | you want N parallel attempts at the same thing, then to grab the best parts of each. |
| [`$nanide-swarm`](../skills/nanide-swarm/SKILL.md) | you want N parallel workers across different slices or races, then one aggregated report. |
| [`$nanide-audit`](../skills/nanide-audit/SKILL.md) | you want completed task changes checked against applicable skills and instructions, with corrections within the existing task authorization. |
| [`$nanide-interrogate`](../skills/nanide-interrogate/SKILL.md) | you have a diff and want independent reviewers to try to break it, including a strict code-quality lens. |
| [`$nanide-automate-me`](../skills/nanide-automate-me/SKILL.md) | you want your own `-mode` skill, drafted from how you've actually worked. |
| [`$nanide-make-bot-ui`](../skills/nanide-make-bot-ui/SKILL.md) | you want a dashboard for a supported, authorized automation endpoint. |
| [`$setup-nanide-skills`](../skills/setup-nanide-skills/SKILL.md) | you want to pick which models the collection uses per role. checks supported models and updates the ignored local configuration. |
| [`$nanide-reflect`](../skills/nanide-reflect/SKILL.md) | a long task landed and you want the recipe captured as a skill edit. |
| [`$nanide-correct`](../skills/nanide-correct/SKILL.md) | you keep correcting agents for the same mistakes. mines history for mistake classes, fixes each at the highest level that works (architecture, then types, lint, and ci, then tests, with docs last), and keeps a table pairing each rule with what enforces it. |
| [`$nanide-teach`](../skills/nanide-teach/SKILL.md) | you want to actually understand a change or subsystem, not just have it summarized. runs `$nanide-how` and `$nanide-why` and weaves one plain explanation, built up diagram by diagram. |
| [`$nanide-tdd`](../skills/nanide-tdd/SKILL.md) | you're fixing a bug and there's a cheap local test path. write the failing test first, then the fix. |
| [`$nanide-benchmark-checklist`](../skills/nanide-benchmark-checklist/SKILL.md) | you ran a benchmark or measured a speedup or regression. vets the number (limiter, tuning, errors, repeat runs, end-to-end relevance) before you report or act on it. |
| [`$nanide-no-comments`](../skills/nanide-no-comments/SKILL.md) | strip comments before review; spawns Comment Sicko, fixes accepted findings, offers encodings for claimed constraints. |
| [`$nanide-typescript-best-practices`](../skills/nanide-typescript-best-practices/SKILL.md) | you're reading or editing typescript. grounds the type-system-discipline principle in syntax. |
| [`$nanide-figure-it-out`](../skills/nanide-figure-it-out/SKILL.md) | no bundled playbook fits. designs a rigorous, auditable playbook for the task. |
| [`$nanide-show-me-your-work`](../skills/nanide-show-me-your-work/SKILL.md) | you want a reviewable decision trail. logs decisions to a tsv you can commit. |
| [`$nanide-create-verification-skill`](../skills/nanide-create-verification-skill/SKILL.md) | your project has no scripted way to prove app behavior. generates a project-local verify skill with a feature map, for any language or platform. |
| [`$nanide-maintain-verification-skill`](../skills/nanide-maintain-verification-skill/SKILL.md) | your verify skill's feature map has drifted from the app. source wave + one live pass, at most one PR of proven corrections. |
| [`$nanide-create-formal-verification-skill`](../skills/nanide-create-formal-verification-skill/SKILL.md) | tests can't reach the case that breaks a race, retry, state machine, parser, or unsafe code. verifies one property with the tool that fits and generates a project-local skill to recheck it on every change. |
| [`$nanide-maintain-formal-verification-skill`](../skills/nanide-maintain-formal-verification-skill/SKILL.md) | code your formal verification covers has changed since it was last checked. updates the model, harness, or properties to match the code, reruns, and says whether each failure is drift in the verification or a bug in the code. |
| [`$nanide-statechart`](../skills/nanide-statechart/SKILL.md) | someone who owns the behavior needs to see it, not read a spec. draws what the user sees as a mermaid statechart generated from a tla+ model, marks each state works, still wrong, or fixed by your open pr, and draws each bug tlc finds as a numbered path. also turns an agreed chart into a tla+ skeleton, or audits the code against an existing spec. |
| [`$nanide-unslop`](../skills/nanide-unslop/SKILL.md) | you're cleaning up writing. removes AI tells. |
| [`$nanide-bro`](../skills/nanide-bro/SKILL.md) | you want the last message restated in plain human language, no jargon. |
| [`$nanide-technical-writing`](../skills/nanide-technical-writing/SKILL.md) | layered doc standard (Diátaxis + Google developer style + STE + Global English) for docs, RFCs, readmes, PR descriptions, commit messages. |

</details>



### examples

mostly i type [`$nanide-mode`](../skills/nanide-mode/SKILL.md) at the start of a task and let it route to a playbook. the other skills fire as the steps need them. a few i reach for directly.


<details>
<summary>all the examples</summary>

```
bug fix:           $nanide-mode this pr has a subtle bug where the scroll drifts every 750ms even
                   when idle. repro first, then fix and verify.
perf:              $nanide-mode a big list takes a second or two to load even though we virtualize.
                   run a cpu trace and tell me why.
feature:           $nanide-mode build a small feature behind a feature flag. verify it really works.
prototype:         $nanide-mode build two prototypes of the markdown renderer so we can compare.
                   spawn an agent for each.
multi-phase:       $nanide-mode open source these skills as a plugin. nothing internal leaks, work
                   in a temp dir, show me the dependency graph first.
overnight run:     $nanide-mode i'm going to bed. land the stack only after required checks pass. i want
                   everything merged by morning.
babysit:           $nanide-mode check on pr 123. anything outstanding?
visual parity:     $nanide-mode the row spacing is too tall when this flag is on. the second image
                   is correct. repro and fix until it matches.
figure it out:     $nanide-mode i'm stepping away. migrate every caller from the synchronous store
                   to the new async one, keeping behavior identical. i want to trust it was done
                   right when i'm back.
how:               $nanide-how do we cancel runs? do we have an n+1 when we look up every run to cancel?
why:               $nanide-why is this feature flag not on yet?
architect:         design this instrumentation to be high signal with no false positives. $nanide-architect
                   this first.
arena:             $nanide-arena take my prompt to the arena verbatim. i want to compare their proposals
                   with yours.
swarm:             $nanide-swarm check every package under packages/ against its check.sh. one worker per
                   package. one report.
interrogate:       $nanide-interrogate review this pr.
tdd:               $nanide-tdd implement
unslop:            can we unslop and tighten the new changes?
reflect:           $nanide-reflect that took too long. capture what we learned so the next run doesn't
                   repeat it.
correct:           $nanide-correct
show-me-your-work: $nanide-show-me-your-work keep a decision trail i can review when i'm back.
automate-me:       $nanide-automate-me
help:              $nanide-help which skill should i use to review this branch?
```

</details>

## Delegate with Codex subagents

The parent owns the playbook and reviews delegated work. [nanide-agent](../agents/nanide-agent.md) and [Comment Sicko](../agents/comment-sicko.md) are prompt templates, not registered agent types. Use an available Codex role and include the relevant absolute skill paths in its brief.

Assign file ownership. Use separate worktrees for competing implementations. Respect the concurrency limit and queue required coverage. Independent reviewers inherit the parent model unless the role configuration provides a supported override. Reports name the models that actually ran.

## principles

twenty-four short skills, one principle each. `nanide-mode` indexes them inline and reads that index at task start. the standalone files are there so other skills can reference a principle by name, and so the index can point at the full rule for each.

<details>
<summary>all twenty-four principles</summary>

| principle | group | rule |
|---|---|---|
| [laziness-protocol](../skills/nanide-principle-laziness-protocol/SKILL.md) | core | Bias toward deletion and the smallest change that solves the problem. |
| [foundational-thinking](../skills/nanide-principle-foundational-thinking/SKILL.md) | core | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. |
| [redesign-from-first-principles](../skills/nanide-principle-redesign-from-first-principles/SKILL.md) | core | Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on. |
| [attack-the-premise](../skills/nanide-principle-attack-the-premise/SKILL.md) | core | Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it. |
| [subtract-before-you-add](../skills/nanide-principle-subtract-before-you-add/SKILL.md) | core | Remove dead weight, redundant validators, and stub references first, then build on the simpler base. |
| [minimize-reader-load](../skills/nanide-principle-minimize-reader-load/SKILL.md) | core | Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. |
| [outcome-oriented-execution](../skills/nanide-principle-outcome-oriented-execution/SKILL.md) | core | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. |
| [experience-first](../skills/nanide-principle-experience-first/SKILL.md) | core | Choose user delight over implementation convenience; ship fewer polished features over more rough ones. |
| [exhaust-the-design-space](../skills/nanide-principle-exhaust-the-design-space/SKILL.md) | core | Build 2-3 competing prototypes and compare side by side before committing. |
| [build-the-lever](../skills/nanide-principle-build-the-lever/SKILL.md) | core | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun. |
| [model-the-domain](../skills/nanide-principle-model-the-domain/SKILL.md) | architecture | Encode the domain in a structure instead of scattered conditionals. |
| [boundary-discipline](../skills/nanide-principle-boundary-discipline/SKILL.md) | architecture | Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. |
| [type-system-discipline](../skills/nanide-principle-type-system-discipline/SKILL.md) | architecture | Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas. |
| [make-operations-idempotent](../skills/nanide-principle-make-operations-idempotent/SKILL.md) | architecture | Converge to the same end state regardless of partial prior runs. |
| [migrate-callers-then-delete-legacy-apis](../skills/nanide-principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | architecture | Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. |
| [separate-before-serializing-shared-state](../skills/nanide-principle-separate-before-serializing-shared-state/SKILL.md) | architecture | Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. |
| [prove-it-works](../skills/nanide-principle-prove-it-works/SKILL.md) | verification | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'. |
| [fix-root-causes](../skills/nanide-principle-fix-root-causes/SKILL.md) | verification | Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. |
| [sequence-verifiable-units](../skills/nanide-principle-sequence-verifiable-units/SKILL.md) | verification | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer. |
| [test-behavior-not-implementation](../skills/nanide-principle-test-behavior-not-implementation/SKILL.md) | verification | Apply when you write, change, or keep a test. Assert what the code's users can observe, so the test fails when that behavior breaks and keeps passing when only the internals change. |
| [explain-the-number](../skills/nanide-principle-explain-the-number/SKILL.md) | verification | Apply before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think. |
| [guard-the-context-window](../skills/nanide-principle-guard-the-context-window/SKILL.md) | delegation | Route bulk to subagents; keep summaries in the main thread, not raw payloads. |
| [never-block-on-the-human](../skills/nanide-principle-never-block-on-the-human/SKILL.md) | delegation | Proceed, present the result, let the human course-correct after the fact; reserve confirmation for irreversible actions. |
| [encode-lessons-in-structure](../skills/nanide-principle-encode-lessons-in-structure/SKILL.md) | meta | Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. |

</details>

## Host capabilities

Use the bundled [authoring playbook](../skills/nanide-mode/playbooks/authoring-a-skill.md) for skill authoring and [diff cleanup](../skills/nanide-mode/references/diff-cleanup.md) before committing. Browser and terminal checks use the available tools and repository runbooks. A build alone does not prove UI behavior.

Conversation recall uses scoped Codex chat tools and supplied evidence. Summaries are not complete transcripts. Scheduled follow-ups use the available Codex automation tool only when requested. An ordinary chat does not promise later execution.

## Update the collection

Review skill changes in this checkout and run the [validation commands](../README.md#validate-changes). Preserve the license, model configuration, invocation policies, and repository-specific validation rules.
