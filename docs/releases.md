# Prepare and install a stable version

## Prepare a source release

From a development branch, update `plugin.json` to the next version and add its changes to `CHANGELOG.md`. Run the [validation commands](../README.md#validate-changes) and review the diff. Commit the intended source files. Git's tracked tree defines the archive contents. Personal overrides, dependency directories, and caches stay untracked.

After review, tag the exact committed revision and create an archive. The commands below prepare version 0.2.0. Use a new version and tag for later changes. Keep existing release tags unchanged.

```sh
git tag -a v0.2.0 -m 'agent-skills v0.2.0' <reviewed-commit>
git archive --format=tar.gz --prefix=agent-skills-0.2.0/ v0.2.0 > /tmp/agent-skills-0.2.0.tar.gz
mkdir -p /tmp/agent-skills-release-check
tar -xzf /tmp/agent-skills-0.2.0.tar.gz -C /tmp/agent-skills-release-check
cd /tmp/agent-skills-release-check/agent-skills-0.2.0
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/skills.py validate
.venv/bin/python -m unittest discover -s tests -v
```

Inspect the archive with `tar -tzf /tmp/agent-skills-0.2.0.tar.gz`. Confirm it contains no `node_modules`, caches, credentials, or `codex-config.local.json`. Tagging creates a local tag. Publishing a tag or hosted release is a separate action.

## Install a pinned checkout

Choose an existing tag or exact commit. Keep the clone at a permanent path. Replace `<exact-commit-or-existing-tag>` below with that revision.

```sh
git clone https://github.com/nanide/agent-skills.git "$HOME/.local/share/agent-skills/stable"
git -C "$HOME/.local/share/agent-skills/stable" checkout --detach <exact-commit-or-existing-tag>
cd "$HOME/.local/share/agent-skills/stable"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/skills.py validate
.venv/bin/python scripts/skills.py install --dry-run
.venv/bin/python scripts/skills.py install
```

An extracted archive works with the same environment and install commands. Neither method downloads updates during installation. Save personal choices in that checkout's ignored `codex-config.local.json`.

## Roll back to a previous checkout

Retain the previous checkout and its local configuration. Run its installer against the same target directory to switch the managed link back. Refresh Codex discovery in a fresh chat. Do not move or remove either checkout while its link is active.

Version `v0.1.0` retains the five original `poteto-*` names and rejects shared helper collisions. It cannot coexist with the original global baseline. Keep a version with the five renamed entrypoints and the recorded baseline exception when the baseline is installed. Test `v0.1.0` in a separate discovery environment if you need that version. Existing release tags remain unchanged.
