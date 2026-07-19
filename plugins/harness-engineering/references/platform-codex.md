# Platform: Codex

The original target of this plugin. Codex specifics that used to be inline in the skills now live here.

## Instruction chain

`AGENTS.md` files, broadest to most specific: global (in the Codex home), workspace, project, nested. Closer files refine broader ones. Templates for all three scopes ship in `assets/`.

## Config home

- `CODEX_HOME`, defaulting to `~/.codex/`.
- `config.toml` holds configuration; audit records key names only, never values.
- Skills live under `~/.codex/skills/`, system skills under `~/.codex/skills/.system/` (including `skill-creator` with `init_skill.py` and `quick_validate.py`, and `plugin-creator`).

## Capability surfaces

- Goals: bounded autonomous runs; the runner skill maps its loop onto Goal mode.
- Automations: scheduled work.
- Rules and hooks: deterministic enforcement; hooks require explicit trust.
- Browser and Computer Use: optional capability bundles; test only when the harness depends on them.
- Skill metadata: each skill carries `agents/openai.yaml` with display name and a default prompt naming `$skill-name`.

## Plugins

- Manifest historically at `.codex-plugin/plugin.json`; the shared schema also accepts `.claude-plugin/plugin.json`. Check which the installed Codex version expects before packaging.
- Marketplace flow: `codex plugin marketplace add <owner>/<repo> --ref main`, then `codex plugin add <plugin>@<marketplace>`.
- Inventory: `codex plugin list --json`. Cache under `~/.codex/plugins/cache/<marketplace>/<name>/<version>/`.
- Start a new task after install so skills appear in the capability inventory.

## Verification

- Validate each skill with the system skill-creator `quick_validate.py`.
- Prove installed listing, source-cache parity (`scripts/verify_install.py`), and fresh-task discovery.
- Model-specific prompt work checks current OpenAI guidance through the official `openai-docs` skill; never invent model names or parameters.
