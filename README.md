# Nanide

Nanide adds engineering workflows to Cursor, Codex, and Claude Code. Use it to trace unfamiliar code, investigate a bug, or review a change. Nanide is an independently maintained fork of [pstack](https://github.com/cursor/plugins/tree/main/pstack).

## Install as a plugin

Choose your client below. All three installation paths use this public GitHub repository.

### Cursor

1. Open **Customize** in Cursor and choose **From GitHub Repository**.
2. Paste `https://github.com/nanide/agent-skills` and import the repository.
3. Select **Nanide → Install** and choose **User** to make the skills available across your projects.

If you prefer the Cursor CLI, register the marketplace from your terminal:

```sh
agent plugin marketplace add https://github.com/nanide/agent-skills
```

Then open **Customize** and install **Nanide** with **User** scope. If GitHub import is unavailable, follow the [manual ZIP installation](docs/plugins.md#install-from-a-zip).

### Codex

Run in your terminal:

```sh
codex plugin marketplace add nanide/agent-skills
codex plugin add nanide@nanide
```

### Claude Code

Run in your terminal:

```sh
claude plugin install nanide --marketplace nanide/agent-skills
```

### Try it in your project

Open a fresh agent chat in your project. Try the line for your client:

| Client | First message |
| --- | --- |
| Cursor | Type `/mode`, select the **mode** skill from Nanide in the picker, then type `explain how this project starts and where its tests live`. |
| Codex | `$nanide:mode explain how this project starts and where its tests live` |
| Claude Code | `/nanide:mode explain how this project starts and where its tests live` |

Look for an answer that points to files in your project. See the [plugin guide](docs/plugins.md) for team distribution, upgrades, and alternative installation commands.

## Use the skills

Start with **mode**. Tell it what you want to learn or change, and it picks the matching helper. Type the selector in your agent chat, followed by a space and your request. For the plugin installs above, use these selectors:

| Skill | Cursor (choose the Nanide match) | Codex | Claude Code |
| --- | --- | --- | --- |
| Mode | `/mode` | `$nanide:mode` | `/nanide:mode` |
| Goal | `/goal` | `$nanide:goal` | `/nanide:goal` |
| Audit | `/audit` | `$nanide:audit` | `/nanide:audit` |
| Help | `/help` | `$nanide:help` | `/nanide:help` |
| Setup | `/setup` | `$nanide:setup` | `/nanide:setup` |

In Cursor, typing `/` opens the skill picker. Search for the name and select the Nanide skill if another command has the same name. [Cursor skill invocation](https://cursor.com/docs/skills)

Here are three ways to start. Each example uses one client's spelling. To use it in another client, change only the selector.

| Task | Example message |
| --- | --- |
| Plan in Cursor | `/mode create a plan to make invoice retries safe. Include a test that retries the same invoice twice.` |
| Ask why in Codex | `$nanide:mode why does the invoice worker acknowledge a job before saving its result?` |
| Investigate in Claude Code | `/nanide:mode investigate why retrying a failed invoice sometimes creates a second charge. Trace one retry and draft a fix plan.` |

Once you have a plan, choose how to run it. These examples use Codex.

- `$nanide:mode implement the plan` works through the agreed change and verifies the result in the current chat.
- `$nanide:goal implement the plan` starts a longer-running task. Goal saves the plan and checkpoints each verified step. If the conversation context is compacted one or more times, the agent can pick up from the saved checkpoint. Hosts with native Goal tracking also show the task's lifecycle status.

You can change a plan while it runs. In the same chat, ask:

```text
$nanide:mode update the plan to cover retries after a worker restart. Add that test before changing the worker, then continue.
```

Goal updates the existing plan, keeps the evidence for completed steps, and continues with the revised work.

### Audit the branch before review

```text
$nanide:audit check changes in this branch
```

Audit compares the changes since the branch split from its base, including relevant uncommitted work, with the task requirements and repository instructions. For the invoice example, it would check whether the restart test actually exercises the retry path and whether its assertions catch a second charge. It reports confirmed defects, the evidence for each finding, and gaps that still need verification. A standalone audit is read-only. During an authorized implementation task, it can also correct findings within that scope.

See the [skill catalog](docs/catalog.md) for other helpers and the [workflow guide](docs/guide/README.md) for more examples.

## Install a source checkout

Use Python 3.9 or newer and Git. Keep one checkout at a permanent path. New users can start with:

```sh
git clone https://github.com/nanide/agent-skills.git "$HOME/.local/share/agent-skills/source"
cd "$HOME/.local/share/agent-skills/source"
```

If you already have a checkout, use it instead. From that checkout, run:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/skills.py validate
.venv/bin/python scripts/skills.py install --provider all --dry-run
.venv/bin/python scripts/skills.py install --provider all
```

`--provider all` installs globally for the current user across every supported provider, including ones you may install later. It creates discovery links for Codex, Cursor, and Claude Code. It does not install those applications or copy the skills. All links use this checkout, so one source update reaches all three.

The command checks every target before writing. Rerun it after adding skills or switching checkouts. Keep the checkout at its installed path. Start a fresh agent session to refresh discovery.

For just one provider, replace `all` with `codex`, `cursor`, or `claude`. Use a single provider with `--target-dir` for a project installation. The [provider adapters](providers/README.md) contain discovery paths, invocation syntax, and native tool behavior.

The installer checks for conflicting skill names and unmanaged destination paths. See [installation and recovery](docs/installation.md) for collision rules, migration, and recovery.

The source installer exposes five chat selectors:

| Client | Mode | Goal | Audit | Help | Setup |
| --- | --- | --- | --- | --- | --- |
| Cursor and Claude Code | `/nanide-mode` | `/nanide-goal` | `/nanide-audit` | `/nanide-help` | `/nanide-setup` |
| Codex | `$mode` | `$goal` | `$audit` | `$help` | `$setup` |

For example, after a Cursor source install, type `/nanide-mode create a plan to make invoice retries safe`. See the [provider entry points](providers/README.md#autocomplete-entry-points) for discovery details.

## Configure model roles

Model roles default to `inherit-parent`, with two independent reviewers per panel. Select Nanide [`setup`](skills/setup/SKILL.md) to save your choices in an ignored provider-local configuration. That complete document replaces [the portable defaults](agent-config.json). Read [configuration precedence](providers/README.md#configuration). Copy it explicitly to a different checkout when switching versions.

## Improve skills while using them

Create a branch in this checkout with `git switch -c improve-skill-name`. Edit the canonical file under `skills/` while you work in another project. After changing skill metadata, run `python scripts/skills.py generate-source-adapters` to refresh Cursor and Claude entry points. Return here to review `git diff`, run validation, and commit the change. The [release guide](docs/releases.md) covers version bumps and immutable tags.

The installer rejects conflicting public skill names in checked discovery roots. Provider installations can link the same canonical sources. Use a separate test environment when validating a different checkout.

## Install a stable version or roll back

Choose an exact commit or an existing release tag, then follow [release and rollback instructions](docs/releases.md). Installation from another checkout switches the managed links after collision checks. Uninstall with the currently installed checkout:

```sh
.venv/bin/python scripts/skills.py uninstall --provider all --dry-run
.venv/bin/python scripts/skills.py uninstall --provider all
```

Uninstall removes the managed discovery links. It retains source files, personal configuration, and migration backups.

## Validate changes

```sh
.venv/bin/python scripts/skills.py validate
.venv/bin/python -m unittest discover -s tests -v
```

The validator parses YAML, checks metadata and local Markdown links, and checks configuration and installation records. See [the authoring playbook](skills/mode/playbooks/authoring-a-skill.md) for instruction changes.

Distributed copies must include the [MIT license](LICENSE) and its attribution.

## Shared workflows and provider support

Shared skills contain workflow decisions. [Provider adapters](providers/README.md) contain host-specific behavior and metadata. The [review notes](docs/provider-neutral-review.md) explain the changes and validation limits.

## Upstream attribution

This collection derives from [pstack in cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack). Its skills, engineering principles, playbooks, and supporting tools provided the foundation for Nanide. Thank you to Lauren Tan and the upstream contributors for that work.

Nanide adds its own skill namespace, provider-neutral workflows, provider adapters, a shared global installer, and changes to delegation and verification. Borys maintains this fork independently of upstream.

[upstream.json](upstream.json) records the imported upstream revision and version. [import-receipt.json](import-receipt.json) records hashes of the customized sources used for the import. These records describe provenance, not a claim that this checkout is identical to upstream.

The [MIT license](LICENSE) retains Lauren Tan's copyright notice for the upstream material and adds Borys's notice for Nanide modifications. Upstream attribution does not imply endorsement of this fork. Include the license and copyright notices when redistributing copies or substantial portions of the derived material. README credit supplements these notices; it does not replace them.
