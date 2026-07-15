# Model evaluation routing workflow

Route every new or multi-stage request through this sequence:

1. No frozen plan, or the user asks what to compare: `model-evaluation-plan`.
2. Frozen plan present and cases need execution: `benchmark-runner` in execute mode.
3. Raw case results present but no checked aggregates: `benchmark-runner` in normalize mode.
4. Comparable normalized results present: `model-selection-memo`.
5. Decision memo present: report decision-ready state or route a requested re-evaluation back to planning.

## Stop rules

- Stop at planning when candidates, cases, metrics, or decision rules are not fixed.
- Stop at execution when candidate coverage or environment conditions diverge.
- Stop before the decision memo when results are partial, incomparable, or unsafe.

The router selects the next stage. Each stage owns its domain work and returns a validated artifact to the router.
