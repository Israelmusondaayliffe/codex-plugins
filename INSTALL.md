# Install and update

## Add the marketplace

Run this once:

    codex plugin marketplace add Israelmusondaayliffe/codex-plugins --ref main

The marketplace name is israel-codex-plugins.

## Install a plugin

Use the plugin folder name shown in the catalog:

    codex plugin add <plugin-name>@israel-codex-plugins

For example:

    codex plugin add model-prompt-lab@israel-codex-plugins

Start a new Codex task after installation. An already open task may keep the
capability inventory it loaded before the plugin was installed.

## Update

Refresh the marketplace source:

    codex plugin marketplace upgrade israel-codex-plugins

Install the desired plugin again:

    codex plugin add <plugin-name>@israel-codex-plugins

Start a new task to verify that the updated skills are visible.

## Troubleshooting

List installed marketplaces and plugins:

    codex plugin marketplace list
    codex plugin list

If a plugin is present on disk but absent from a task, close that task and open
a completely new one. Task inventories can remain stale after installation.

Some skills call optional tools or external services. Read that skill's
instructions for required CLIs, environment variables, accounts, or connectors.
No secrets are included in this repository.
