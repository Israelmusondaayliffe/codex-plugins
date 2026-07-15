# Measurement Notes

## Verified benchmark

On July 10, 2026, plugin-eval ran three isolated Codex CLI scenarios with GPT-5.5:

1. Research notes to a validated outcome brief.
2. An operations brief to validated action slices.
3. A creative brief that preserved the no-send and no-publish boundary.

All three scenarios completed. Each created one intended local artifact. Both brief scenarios passed `validate_outcome_brief.py`. The action plan passed `validate_action_slices.py` with no dependency cycle.

## Usage interpretation

The benchmark recorded these averages:

- Input tokens: 107,128
- Output tokens: 2,884.33
- Total tokens: 110,012.33
- Static active plugin estimate: 4,731 tokens

Do not attribute the difference between the static plugin estimate and observed input tokens to Outcome Engine. The observed input count covers the full Codex execution context, including global instructions, available tools, installed skill metadata, workspace rules, source files, and cached input. The benchmark did not run a matching no-plugin baseline, so it does not isolate the plugin's added token cost.

Use the observed numbers as whole-session measurements. A future marginal-cost test should run the same scenarios with and without the plugin under the same Codex version, model, global rules, tool set, and workspace fixture.

## Static evaluation caveats

Plugin-eval's Python complexity warning counts decision words across an entire file and compares that file-level count with function-level thresholds. The validator suite is the source of truth for behavior. Keep functions short and tests green, but do not split working code solely to reduce this heuristic.
