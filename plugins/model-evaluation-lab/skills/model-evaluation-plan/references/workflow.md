# Model evaluation planning workflow

## Freeze before execution

Freeze these fields before candidate results are visible:

1. Deployment decision and baseline.
2. Candidate configuration identifiers.
3. Dataset version, provenance, exclusions, and splits.
4. Success, boundary, and failure cases.
5. Metrics, human rubric, thresholds, and tie-breakers.
6. Runtime conditions, repetitions, random seeds when supported, and tool availability.
7. Budget, cost-accounting method, and stopping rules.

## Case coverage

- `success`: representative core work.
- `boundary`: ambiguous or uncommon inputs that expose tradeoffs.
- `failure`: unsafe, invalid, or dependency-failure conditions that must be handled correctly.

## Decision discipline

Name the minimum evidence needed to replace the baseline. If candidate coverage or execution conditions diverge, return an inconclusive result rather than ranking unlike runs.
