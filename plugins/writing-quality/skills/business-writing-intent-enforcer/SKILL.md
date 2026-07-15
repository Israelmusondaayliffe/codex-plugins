---
name: business-writing-intent-enforcer
description: Use for memos, specs, PRDs, operating docs, executive summaries, proposals, project plans, and structured business deliverables where reader intent, decisions, actionability, and evidence matter.
---

# Business Writing Intent Enforcer

Tier: 2 structured writing skill.

Use this skill when the output needs to help a reader decide, act, align, approve, review, or execute.

## Router Logic

- New business document: load `agents/agent-intent-architect.md`.
- Existing draft cleanup: load `agents/agent-editor.md`.
- Local file validation: optionally run `scripts/check_business_doc.py <file>`.

## Required References

- `references/document-intent-patterns.md`: common business document jobs and structures.

## Required Assets

- `assets/business-doc-checklist.md`: final review checklist.

## Workflow

1. Identify the reader and what they need to do after reading.
2. State the document's job in one sentence.
3. Organize around decisions, risks, next actions, and evidence.
4. Remove throat-clearing, generic context, and decorative framing.
5. Make every section earn its place.
6. End with the concrete next step or decision point.
