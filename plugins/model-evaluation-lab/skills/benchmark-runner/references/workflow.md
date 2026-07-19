# Benchmark execution workflow

## Backend routing

- Local harness: use when the model endpoint and dataset can be invoked reproducibly in the current environment.
- Hugging Face Jobs: use when remote compute, dataset access, or tracked community evaluation is needed and the companion is installed.
- External authorized runner: use when credentials or production infrastructure must remain outside the host platform. Export the frozen plan and require the stable raw result contract on return.

## Raw result contract

Each case record must include a unique identifier, candidate configuration, pass state, numeric score, latency in milliseconds, and marginal request cost. Record failures explicitly. Do not encode a failed execution as a score of zero unless the frozen metric defines that treatment.

## Handoff gate

The normalized run is comparable only when candidate coverage, plan hash, dataset, environment, and stopping-rule treatment match. A partial run can be preserved but cannot support model selection.
