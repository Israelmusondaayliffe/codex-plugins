# Capability Operator

Capability Operator is the routing, maintenance, and governance plugin for personal capabilities on Claude Code, Claude Cowork, and Codex.

## Owned skills

- capability-router
- capability-inventory
- skill-overlap-audit
- fresh-task-discovery-verifier
- plugin-portfolio-manager
- harness-meta-audit
- skill-creator-pro

## Companion capabilities

- system plugin-creator and skill-creator for canonical scaffolding
- Plugin Eval for analysis and benchmarks
- ProofLoop for bounded verification
- Claude Mem for recall only, never as a source of truth

## Host surfaces

- Claude Code and Claude Cowork: `~/.claude/` is the config home. Installed plugins are recorded in `enabledPlugins` inside `~/.claude/settings.json`, `~/.claude/plugins/installed_plugins.json`, and the cached marketplaces under `~/.claude/plugins/marketplaces/`. Loose skills live in `~/.claude/skills/` and agents in `~/.claude/agents/`. Live listing comes from `claude plugin list` or the `/plugin` command. Fresh-task discovery evidence is the skill inventory of a fresh `claude -p` session.
- Codex: `~/.codex/` (or `CODEX_HOME`) is the config home, holding `config.toml` and `~/.codex/skills/`. Live listing comes from `codex plugin list`. Fresh-task discovery evidence is a clean-task prompt from `codex debug prompt-input`.

## Boundaries

- One request gets one primary route. Companions load only at documented handoffs.
- Explicit user selections win, and focused actions route to the narrow owned skill.
- Inventory and audit operations are read-only by default.
- Global writes require explicit task authority and a recent backup.
- Filesystem presence is not accepted as installation or discovery proof.

## Verification

Run `scripts/verify_bundle.py`, the 38 routing cases, the plugin validator, and the skill validators. Regenerate the human routing reference from the registry. After installation, compare source with the installed cache and run `fresh-task-discovery-verifier`.
