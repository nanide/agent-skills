# Nanide

Nanide adds engineering workflows to Cursor, Codex, and Claude Code. Use it to trace unfamiliar code, investigate a bug, or review a change. Nanide is an independently maintained fork of [pstack](https://github.com/cursor/plugins/tree/main/pstack).

## Install as a plugin

Choose your client. The plugin manager handles the download. While this repository is private, you need repository access or a plugin distributed by your team.

### Cursor

A team admin opens **Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace → Import from Repo**, enters `https://github.com/nanide/agent-skills`, and connects GitHub if prompted. The admin adds Nanide with **Add to Marketplace**, sets **Marketplace Access** under **Marketplace Settings**, and saves. Teammates can then open **Customize**, find **Nanide**, and select **Install**.

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

Open a fresh agent session in your project and ask:

> Use Nanide to explain how this project starts and where its tests live.

Look for an answer that points to files in your project. See the [plugin guide](docs/plugins.md) for team distribution, upgrades, and alternative installation commands.

## Use the skills

Start with **Nanide mode**. Tell it what you want to learn or change. Mode chooses the matching helper, so you can start a plan, ask why the code works a certain way, or investigate a bug from the same chat.

The examples below use `nanide-mode` and `nanide-goal` as shorthand for the two skills. In Codex, select `$nanide:mode` or `$nanide:goal`. In Claude Code, use `/nanide:mode` or `/nanide:goal`. In Cursor, select the installed Nanide skill or ask for “Nanide mode” or “Nanide goal” by name.

Pick a starting question for your project:

```text
nanide-mode create a plan to make invoice retries safe. Include a test that retries the same invoice twice.
nanide-mode why does the invoice worker acknowledge a job before saving its result?
nanide-mode investigate why retrying a failed invoice sometimes creates a second charge. Trace one retry and draft a fix plan.
```

Once you have a plan, choose how to run it:

- `nanide-mode implement the plan` works through the agreed change and verifies the result in the current chat.
- `nanide-goal implement the plan` starts a longer-running task. Goal saves the plan and checkpoints each verified step. If the conversation context is compacted one or more times, the agent can pick up from the saved checkpoint. Hosts with native Goal tracking also show the task's lifecycle status.

You can change a plan while it runs. In the same chat, ask:

```text
nanide-mode update the plan to cover retries after a worker restart. Add that test before changing the worker, then continue.
```

Goal updates the existing plan, keeps the evidence for completed steps, and continues with the revised work. See the [skill catalog](docs/catalog.md) for other helpers and the [workflow guide](docs/guide/README.md) for more examples.

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

For source installations, Codex exposes `$mode` and `$goal`. Cursor and Claude Code expose `/nanide-mode` and `/nanide-goal`. See the [provider entry points](providers/README.md#autocomplete-entry-points) for the full list.

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
