---
name: agent-system-audit
description: Audits an agent, Goal, loop, or autonomous workflow for authority, stop conditions, evidence, tool contracts, cost controls, recovery, and durable state. Use for read-only reviews before launch, after failures, or before increasing autonomy. Produces a validated finding ledger with severity and evidence, without executing or repairing the system unless separately authorized.
---

# Agent System Audit

## Overview

Assess whether an agent system can operate safely and finish reliably. Keep audit authority read-only.

## Workflow

1. Collect the agent instructions, workflow, tools, state model, and verification contract.
2. Review every control in references/audit-controls.md.
3. Record findings with assets/audit-template.json.
4. Run scripts/validate_audit.py.
5. Report blockers first, then high, medium, and low findings with evidence and a concrete remedy.
6. Do not implement fixes during an audit-only request.

## Error Handling

- Mark a control unknown when evidence is absent. Do not infer that it passes.
- Treat missing stop conditions, unbounded external authority, and unverifiable completion as blockers.
- If runtime behavior differs from written instructions, report both and privilege observed evidence.

## Reliability Notes

The model evaluates the system against named controls. The validator checks finding IDs, severity, evidence, and remedies. It does not prove runtime safety without scenario tests.

## Resources

- scripts/validate_audit.py validates the finding ledger.
- references/audit-controls.md defines the audit.
- assets/audit-template.json provides the schema.
