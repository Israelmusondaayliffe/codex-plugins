# Model selection workflow

## Evidence order

1. Confirm run completeness and comparability.
2. Apply safety and hard-threshold rules first.
3. Compare preregistered primary metrics.
4. Use secondary metrics and human rubrics only as declared tie-breakers.
5. State measured findings before interpretation.
6. Name operational tradeoffs, limitations, and rollback conditions.

## Recommendation states

- `select-baseline`: evidence does not justify a change.
- `select-candidate`: a named candidate satisfies the decision rule.
- `no-decision`: evidence is incomplete, incomparable, unsafe, or tied under the rule.

Do not convert `no-decision` into a preference. State what additional run would resolve it.
