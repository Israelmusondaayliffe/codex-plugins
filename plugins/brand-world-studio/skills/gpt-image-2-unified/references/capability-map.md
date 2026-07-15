# Capability Map

Official and community-confirmed capabilities of ChatGPT Images 2.0 and the underlying GPT Image 2 model. Tagged by mode. High-confidence claims anchor each row. Unconfirmed items are in the bottom section.

Launch date: April 21, 2026. Model ID for API: `gpt-image-2`.

## Core capabilities by mode

| Capability | Description | Instant | Thinking |
|---|---|---|---|
| Text-to-image | Image generation from a text brief | Yes | Yes |
| Image-to-image | Modification of uploaded image | Yes | Yes |
| Multi-reference composition | Blend multiple uploaded references | Yes (simple cases) | Yes (full fidelity) |
| Aspect ratio range | 3:1 to 1:3 | Yes | Yes |
| Max resolution | 2K native (2560x1440); 4K experimental in API beta | Yes | Yes |
| Latency | Seconds per image (5 to 10s typical) | Yes | No (20 to 60s typical) |
| Web search during generation | Retrieves current facts, weather, news | No | Yes |
| Multi-output count | Single image or small batches per call | 1 to 4 | Up to 8 with consistency |
| Self-verification | Internal reasoning checks factual and compositional coherence | No | Yes |
| Conversational editing | Iterative refinement without manual masking | Yes | Yes |
| Typography accuracy | Dense, legible text; roughly 99% accuracy (Handy AI estimate) | High | Highest |
| Multilingual scripts | Japanese, Korean, Chinese, Hindi, Bengali, Latin | High | Highest |
| Character consistency | Maintains visual DNA across outputs | Limited | Up to 8 outputs |
| Visual reasoning | Puzzles, math, logic diagrams | Limited | Yes |
| Photoreal texture | Skin pores, fabric weaves, atmospheric lighting | Yes | Yes |
| Anti-slop aesthetic | Amateur/candid authenticity (iPhone feel, motion blur) | Yes | Yes |
| C2PA provenance | Output carries provenance metadata | Yes | Yes |
| Imperceptible watermark | Embedded in all outputs | Yes | Yes |

## Capability families the skill routes on

- **Generation**: text-to-image, image-to-image, multi-reference (CREATE, EDIT, COMPOSE modes)
- **Reasoning**: search-grounded, consistency-verified (SEARCH, SERIES modes)
- **Design deliverables**: typography, infographics, editorial layouts, sequential art (TYPOGRAPHY, INFOGRAPHIC, EDITORIAL, NARRATIVE modes)

## Instant vs Thinking: capability split (summary)

Instant has every baseline capability. Thinking adds three things Instant cannot do:

1. **Web search during generation**. Required for current-data prompts.
2. **Up to 8 consistent outputs per prompt**. Required for multi-frame series.
3. **Self-verification loop**. Required for factual, anatomical, cartographic, or logical accuracy.

Everything else (typography, aspect ratios, editing, aesthetic quality) is available in both modes, with Thinking typically producing higher-fidelity results at the cost of latency.

## Knowledge cutoff

December 2025. Thinking mode bridges this gap via web search. Instant mode cannot bridge it; prompts that depend on post-cutoff facts should route through SEARCH.

## Provenance and safety

All outputs carry C2PA metadata and an imperceptible watermark. Note: screenshots and re-uploads strip C2PA metadata, so provenance guarantees are limited in the real world. Safety stack combines prompt and output classifiers plus a safety reasoning monitor.

Adversarial evaluation (from OpenAI system card):
- Instant mode: 22.0% violative rate pre-safety, 99.1% safe outputs post-safety
- Thinking mode: 6.7% violative rate pre-safety, 99.2% safe outputs post-safety

Thinking mode produces fewer bad outputs at the source because "Safe Completions" training rewrites unsafe requests rather than executing them. Side effect: Thinking mode occasionally over-blocks benign creative requests involving public figures.

## Unconfirmed or low-confidence

Flagged, not asserted. Revisit in 2 to 4 weeks.

- **Sora image-to-animation pipeline**: hinted at but not functional in API as of launch day
- **Long-term Memories integration with image styles**: unclear how persistent style preferences work across sessions
- **Thinking chain-of-thought access**: not currently exposed via API
- **Batch zip export from the 8-output set**: only in pre-release demos for Codex users at launch
- **Exact Thinking-token pricing mechanics**: rates documented but billing edge cases still emerging from community testing
- **Actual max reference-image count for COMPOSE**: less precisely documented than Nano Banana Pro's 14; skill defaults to 4 for reliability
