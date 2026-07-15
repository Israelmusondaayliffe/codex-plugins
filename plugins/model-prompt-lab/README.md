# Model Prompt Lab

Model Prompt Lab packages model routing, production prompt architecture, migration audits, and benchmark design for GPT-5.6, GPT-5.4, Fable 5, and related prompt surfaces.

## Owned skills

- model-prompt-router
- prompt-benchmark-designer
- prompt-migration-audit
- gpt-5-6-production-prompter
- gpt-5-4-production-prompter
- fable-5-production-prompter
- fable-mode

## Companion capabilities

- OpenAI Developers for current platform guidance when installed
- Proofloop for extended iterative verification
- Writing Quality for final human-facing prose validation

Run `scripts/check_companions.py` to see which optional companions are installed. Missing optional companions do not block owned workflows.

## Boundaries

- Do not state unstable model behavior as current without a live source check.
- Migration preserves the user job but does not preserve unsupported parameters.
- Benchmark design is deterministic planning. It does not claim a model run occurred.

## Verification

Run `scripts/verify_bundle.py` from any directory. Installation is trusted only after plugin validation, skill validation, source-to-cache parity, live listing, real-artifact validation, and clean-task discovery all pass.
