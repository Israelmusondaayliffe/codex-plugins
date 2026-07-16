---
name: harness-audit
description: Inspect a current Codex home, workspace, project, or imported agent setup without changing it. Use for harness audits, setup inventories, AGENTS.md chain checks, installed skill or plugin reviews, connector and MCP inventories, rules or hook inspection, drift detection, secret-exposure checks, and gap analysis before a harness plan or upgrade.
---

# Harness Audit

Read current state before proposing changes. Do not record credential values or private connector content.

## Workflow

1. Resolve the Codex home from `CODEX_HOME` or the platform default.
2. Identify the selected workspace and applicable `AGENTS.md` chain.
3. Inventory config key names, rules, hooks, skills, plugins, MCP names, templates, projects, memory surfaces, automations, Browser, and Computer Use availability.
4. Check for conflicts, placeholders, stale paths, duplicated ownership, missing validators, untrusted hooks, unsupported settings, and absent evidence.
5. Classify findings across information, execution, and feedback layers.
6. Separate verified facts, inferred risks, and user decisions.
7. Produce `audit.json` plus a short gap summary. Make no changes.

Run:

```text
python3 ../../scripts/harnessctl.py audit --output AUDIT.json [--codex-home PATH] [--workspace PATH]
```

Use `../../references/verification-standard.md` to distinguish file presence from operational proof.
