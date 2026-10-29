# Install Nanide as a plugin

Install the complete Nanide collection through your application's plugin tools. You do not need to clone the source or run the Python installer. Some workflows run tools such as Git, Node.js, or Java. Those workflows retain their runtime requirements.

These instructions require the marketplace catalogs to be available in the repository revision you install. A private repository also requires access. Preparing the repository does not publish a listing in any provider's public directory.

## Install in Codex

For a published listing, open the Plugins directory, find **Nanide**, and install it. A workspace administrator can distribute the plugin to selected workspace roles without a public listing. See [OpenAI plugin distribution](https://developers.openai.com/plugins/build/plugins).

Before a listing exists, use the Codex CLI marketplace commands. These commands fetch and manage the plugin for you.

```sh
codex plugin marketplace add nanide/agent-skills
codex plugin add agent-skills@nanide
```

Start a fresh session. Ask Codex to use Nanide to explain your project. Use the installed skill selector for `nanide-mode` when available.

## Install in Cursor

A team administrator can import this repository once for the team.

1. Open **Dashboard > Plugins & MCPs > Team Marketplaces**.
2. Select **Add Marketplace**, then **Import from Repo**.
3. Enter `https://github.com/nanide/agent-skills` and grant repository access when prompted.
4. Review the plugin and set the marketplace's access policy.

Teammates open **Customize**, find the plugin, and select **Install**. Cursor accepts the portable root `plugin.json`. Team marketplaces require a supported Teams or Enterprise plan. See [Cursor plugin installation](https://cursor.com/docs/plugins).

For public discovery, the maintainer must submit the repository through [Cursor's publishing portal](https://cursor.com/marketplace/publish). A catalog in Git does not create that listing.

## Install in Claude Code

Run these commands inside Claude Code.

```text
/plugin marketplace add nanide/agent-skills
/plugin install agent-skills@nanide
```

Start a fresh session and invoke the namespaced skill.

```text
/agent-skills:nanide-mode explain how this project works.
```

The equivalent shell commands are `claude plugin marketplace add nanide/agent-skills` and `claude plugin install agent-skills@nanide`. See [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

## Switch from a source installation

If Nanide is already installed through `scripts/skills.py`, uninstall its discovery links from that checkout before enabling the plugin. Follow [uninstall instructions](installation.md#switch-checkouts-and-uninstall). Keep the checkout and personal configuration until you have verified the plugin.

Plugin discovery can expose all helpers in `skills/`. The source installer exposes five main entry points. Start with `nanide-mode` or `nanide-help` in either installation. Host-specific invocation syntax and available tools still differ.

## Configure and update

Nanide works with its bundled defaults. Model setup is optional. Ask the installed `setup-nanide-skills` skill to configure role choices only when you want different models.

Configuration saved inside a plugin cache can be replaced during an update or uninstall. Keep a separate copy of `providers/<provider>/config.local.json` if you customize it. Restore it only after checking that the new package supports those choices.

Use the provider's plugin manager to update or remove the plugin. Start a fresh session after updating. Do not edit a cached plugin as your development checkout.

## Report a problem

Include the provider and application version, the installed plugin version from `plugin.json`, your prompt, and the error. For a missing helper, include the path the agent tried to read. Report issues through the repository's GitHub issue tracker.
