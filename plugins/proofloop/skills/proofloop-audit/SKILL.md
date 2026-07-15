---
name: proofloop-audit
description: Perform a read-only audit of ProofLoop outcomes, advisory retrieval effects, verifier calibration, memory quality, drift, security denials, cost, and portability. Use only when the user explicitly invokes $proofloop-audit or asks to audit ProofLoop learning or determine whether ProofLoop is helping.
---

# ProofLoop Audit

Measure behavior without changing it. Separate verified improvement, neutral effect, harmful retrieval, and insufficient evidence.

## Read-only invariant

Do not write or mutate records, statuses, exclusions, policy, skills, scripts, schemas, host configuration, connectors, or external systems. If an audit needs a write to continue, stop and provide the exact read-only evidence still available.

## Audit workflow

1. Fix scope, time window, task families, eligible records, comparison method, and privacy constraints before inspecting outcomes.
2. Validate sampled contracts and records. Treat invalid or missing provenance as a finding, not evidence.
3. Compare paired runs with and without retrieval only when contracts, environments, budgets, and verifiers are comparable.
4. Count helpful, neutral, harmful, and indeterminate retrievals. Never collapse indeterminate cases into improvement.
5. Measure evidence levels, revisions, attempts, verifier failures, overrides, stale or conflicting records, exclusions, tool errors, latency, and cost when available.
6. Test verifier calibration against deterministic or direct-human outcomes. Flag correlated judges and shared dependencies.
7. Run trigger, protocol, security, and portability fixtures through `python3 scripts/run-regressions` when Python 3.11 is available.
8. Report unauthorized activation, protected-data disclosure, cross-scope retrieval, and unauthorized consequential writes separately. Release requires zero in the maintained critical suite.
9. Recommend narrowing, expiry, exclusion, verifier repair, or adapter changes as proposals only. Do not apply them.

## Claim discipline

- Call fewer than twenty paired cases per claimed task family exploratory.
- Do not infer causality from one successful run.
- Do not call E0 or E1 evidence verified improvement.
- Do not call results independent when they share a generation, verifier implementation and configuration, test data, source, or connector trust path.
- State missing data and compatibility mismatches explicitly.

## Read when needed

- Read `references/audit-policy.md` for metrics, paired evaluation, and release gates.
- Read `references/security-model.md` for the critical abuse suite.
- Use bundled scripts only for deterministic read-only validation and summaries.
