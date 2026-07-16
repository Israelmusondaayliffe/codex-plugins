# Verification Standard

Completion requires fresh evidence from the installed environment.

## Structural checks

- Required files exist at the approved paths.
- JSON, TOML, YAML, and Markdown parse or validate where a validator exists.
- The `AGENTS.md` chain resolves in the intended order.
- Plugin and skill manifests contain no placeholders.
- Generated files contain no secrets or user-specific sample data.

## Behavioral checks

- A new task discovers installed skills and plugin front doors.
- Command policy allows safe examples and blocks forbidden examples.
- Hooks run only after review and trust.
- Connectors return an authenticated profile or a precise setup requirement.
- Browser and Computer Use are tested only when the harness depends on them.

## Completion receipt

List every required check once. Include the command or inspection, fresh result, evidence path, and pass or fail status. A missing or stale check is a failure, not a clean no-op.
