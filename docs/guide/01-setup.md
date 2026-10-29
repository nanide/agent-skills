# Set up Nanide skills for Codex

Install the collection from its source checkout using the [installation instructions](../../README.md#install-a-development-checkout). The default discovery entry is `~/.agents/skills/agent-skills`, a symlink to the checkout's `skills/` directory. Use `--target-dir` for a project installation.

## Pick your models

Invoke `$setup-nanide-skills` to inspect the defaults in [codex-config.json](../../codex-config.json) or change the ignored `codex-config.local.json` override. Every unconfigured role inherits the parent chat's model. `auto` and `inherit-parent` both omit model and reasoning overrides.

An explicit role override contains `model` and optionally `reasoning_effort`. Use only values supported by the current Codex subagent tool. A panel role can contain a list of overrides. Its length sets the reviewer count. Otherwise `panel_size` sets the count, with two as the default. Queue reviewers within the available concurrency limit.

Setup preserves existing overrides unless you ask to change them. Remove a role's override to restore inherited execution. Unsupported configured models are reported rather than replaced with a guessed model. Independent reviewers can use the same model. The report says which models actually ran.

## Choose verification for your project

Use the repository's existing verification tools first. If none can prove the changed behavior, `$create-verification-skill` can create a project skill with launch, control, evidence, and cleanup steps. It follows the repository's skill-directory convention. Personal skills belong under `~/.codex/skills`.

Use `$create-formal-verification-skill` when one important property needs a model checker or another verifier. The result states the model, bounds, and limitations. Neither generator changes product code or creates schedules merely because you ran setup.

## Keep cost in check

Use fewer reviewers when independent coverage does not need more. Choose supported role overrides deliberately. Inherited execution avoids a stale model catalog. There is no fixed model-family or reasoning-budget ladder.

## Run your first task

```text
$nanide-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

The mode selects a playbook and tracks its steps in the available plan tool or a concise checklist. Follow-ups retain the current task's scope. Start a fresh chat to check discovery after installing or editing skills. If discovery has not refreshed, attach the installed `SKILL.md` by its absolute path.

The bundled `agents/openai.yaml` files define invocation policies. Invoking the mode can load sibling skills needed for the task. It does not change unrelated chats or install a persistent application mode.

Next: [Route work through `$nanide-mode`](./02-nanide-mode.md).
