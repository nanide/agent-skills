# Prepare a Nanide plugin release

Build one ZIP for Codex submission and local provider testing. The same source repository supplies the Cursor and Claude marketplaces. Publishing, workspace import, and changing repository visibility are separate actions.

## Build the package

Use the Python environment from the [source installation instructions](../README.md#install-a-source-checkout).

1. Update `plugin.json` and `.claude-plugin/plugin.json` to the same new version.
2. Stage the intended package files. The builder includes tracked working-tree files, including staged additions, and excludes untracked files.
3. Run the checks and build command.

```sh
.venv/bin/python scripts/skills.py validate
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/package_plugin.py --output-dir dist
```

The output is `dist/agent-skills-<version>.zip` and its SHA-256 sidecar. The archive has `plugin.json` at its root. Internal file symlinks become regular files. Dependencies and relative paths stay together.

The build rejects tracked private configuration and generated state. A directory allowlist limits archive contents. Git-based marketplaces install the repository directly, so the tracked-file check also protects that route. This check does not inspect Git history or detect secrets inside otherwise permitted source files.

The validation workflow builds and uploads the ZIP as a CI artifact. It does not create a GitHub release or publish to a plugin directory.

## Verify the extracted package

Extract the ZIP into a new temporary directory outside the source checkout. Run collection validation against that directory using the source checkout's Python environment.

```sh
/path/to/source/.venv/bin/python /path/to/extracted/scripts/skills.py validate
claude plugin validate /path/to/extracted/.claude-plugin/plugin.json
claude plugin validate /path/to/extracted/.claude-plugin/marketplace.json
```

Use a temporary Codex home to register the extracted marketplace and install `agent-skills@nanide`. Check the installed cache for `skills/nanide-mode/SKILL.md`, a sibling helper, `providers/README.md`, and `agent-config.json`. Keep this test separate from your normal installed collection.

For Cursor, copy the extracted package into an isolated local plugin test directory supported by your environment. Cursor's documented location is `~/.cursor/plugins/local/<plugin-name>`. Reload the application and inspect **Customize**. Local imports may be disabled by an administrator. See [Cursor local plugin testing](https://cursor.com/docs/plugins).

In each target application, start a fresh session and ask Nanide to explain a small fixture project. Confirm that the agent reads the packaged mode, a sibling helper, and the provider adapter. Static validation does not prove this workflow or UI discovery. Record the application version and any missing proof before publication.

## Publish for Codex

Upload the ZIP using the [OpenAI plugin submission flow](https://developers.openai.com/plugins/deploy/submission). The package includes its display metadata and SVG icon. It contains skills only, with no MCP server or lifecycle hooks.

Resolve portal findings and complete any required publisher information. After approval, explicitly publish the listing. For a workspace trial, an administrator can use [workspace plugin publishing](https://developers.openai.com/plugins/build/plugins). The repo marketplace is also available through the commands in the [installation guide](plugins.md).

## Share with other providers

Push the reviewed files to a repository revision teammates can access. Use the [Cursor and Claude installation instructions](plugins.md). Cursor public listing requires its own review. Claude teammates can use the repository marketplace without a public directory listing.

Preserve the license and upstream attribution. Keep existing release tags immutable. For rollback, retain the previous version and follow the provider's version selection or reinstall flow.
