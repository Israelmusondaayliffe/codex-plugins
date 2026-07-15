# Knowledge Work Superpowers

Knowledge Work Superpowers is a composable workflow system for substantial non-coding work. It covers research, analysis, planning, drafting, review, verification, and handoff.

The plugin is inspired by the process design of Superpowers. It replaces coding-specific mechanics with evidence-first knowledge-work methods.

## Default Workflow

1. Frame the work.
2. Write the plan.
3. Research systematically.
4. Test claims against evidence.
5. Draft from the evidence record.
6. Review requirements and quality separately.
7. Verify the finished result with fresh checks.
8. Package and hand off the deliverable.

Parallel research and feedback reception are conditional branches, not mandatory steps.

## Skills

- `using-knowledge-work-superpowers`: route substantial knowledge work through relevant skills.
- `framing-knowledge-work`: define purpose, audience, scope, sources, constraints, and success criteria.
- `planning-knowledge-work`: turn an approved brief into a concrete plan.
- `systematic-research`: conduct multi-pass research with source hierarchy and contradiction checks.
- `evidence-first-analysis`: test important claims before accepting them.
- `drafting-from-evidence`: write from a source and claim ledger.
- `executing-knowledge-work-plans`: execute plans in checked stages.
- `dispatching-parallel-research`: split independent research strands safely.
- `reviewing-knowledge-work`: review brief compliance, evidence, reasoning, and communication.
- `receiving-work-review`: assess feedback before revising.
- `verification-before-delivery`: run fresh claim, citation, link, and format checks.
- `finishing-a-deliverable`: version, package, record limitations, and hand off.

## Shared Assets

Templates under `assets/` support work briefs, plans, source ledgers, claim ledgers, reviews, and delivery notes. They are defaults, not mandatory formats when the user provides another template.

## File-Based Verification

For a file-based research bundle, run:

```bash
python3 scripts/verify_research_bundle.py /path/to/bundle --profile deliverable
```

Expected filenames are documented by the templates. Chat-only tasks can use the same checks manually.

## Scope

Use this plugin for substantial research, reports, memos, comparisons, recommendations, decision support, and other evidence-backed deliverables.

Do not use it to answer a simple factual question that needs only one direct lookup. Do not treat it as a substitute for domain-specific legal, medical, financial, or compliance review.
