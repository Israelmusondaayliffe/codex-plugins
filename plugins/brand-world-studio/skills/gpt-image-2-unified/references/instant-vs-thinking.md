# Instant vs Thinking

Decision tree for recommending GPT Image 2's Instant or Thinking mode. Grounded in the launch research and official system card.

## Two-line summary

**Instant**: fast, up to 4 outputs, no reasoning, no search. Default for simple subjects and quick iteration.

**Thinking**: slower (20 to 60 seconds), up to 8 consistent outputs, internal reasoning, native web search, self-verification. Default for factual accuracy, multi-output consistency, non-Latin typography, and complex compositions.

## Decision tree

```
Does the prompt require current facts, live data, or web search?
├── YES → Thinking (required; Instant cannot search)
└── NO → continue

Does the prompt require 5 or more consistent related outputs?
├── YES → Thinking (required; Instant caps at 4)
└── NO → continue

Does the prompt involve non-Latin dense typography or mixed scripts?
├── YES → Thinking (recommended for typography fidelity)
└── NO → continue

Does the prompt require factual accuracy (anatomy, cartography, science, real entities)?
├── YES → Thinking (self-verification helps)
└── NO → continue

Does the prompt require complex compositional reasoning (multi-element scenes, logical diagrams, mathematical visualization)?
├── YES → Thinking (reasoning depth pays off)
└── NO → continue

Is latency critical or is the user doing rapid batch ideation?
├── YES → Instant (speed wins)
└── NO → continue

Default: either works. Recommend Instant first, offer Thinking as the higher-fidelity option.
```

## Mode recommendation by skill mode

| Skill mode | Typical recommendation | Rationale |
|---|---|---|
| CREATE | Instant default; Thinking for complex factual scenes | Most CREATE prompts are aesthetic, not factual |
| EDIT | Instant default | Edit loop is conversational; reasoning less important |
| SHOW-ME | Thinking if spatial complexity is high, Instant for simple symmetric subjects | 3D reasoning helps for new angles |
| COMPOSE | Thinking | Multi-reference identity preservation benefits from reasoning |
| SEARCH | Thinking (required) | Instant cannot search |
| SERIES | Thinking (required) | Instant caps at 4 outputs |
| TYPOGRAPHY | Thinking for non-Latin or dense, Instant for short Latin display | Fidelity scales with complexity |
| INFOGRAPHIC | Thinking for factual, Instant for conceptual | Logical coherence benefits from reasoning |
| EDITORIAL | Thinking for dense or multilingual, Instant for display posters | Layout complexity is the tell |
| NARRATIVE | Thinking for multi-panel with dialogue, Instant for single frames | Consistency matters more with panels |

## Cost vs quality trade-off

Thinking mode costs more (reasoning tokens billed regardless of visibility). Order-of-magnitude rule of thumb based on launch pricing:

- Instant 1024x1024 low: roughly $0.006
- Instant 1024x1024 high: roughly $0.132 (GPT Image 1.5 baseline; actual Instant 2.0 pricing pending)
- Thinking 1024x1024 high: roughly $0.211

For budget-conscious workflows, Instant at medium quality often delivers production-acceptable outputs for 25 to 40% of Thinking high-quality cost.

## Latency considerations

| Mode | Typical latency |
|---|---|
| Instant | 5 to 10 seconds |
| Thinking (minimal) | 15 to 20 seconds |
| Thinking (high) | 30 to 45 seconds |
| Thinking (dynamic, beta) | Variable; can exceed 60 seconds for complex reasoning |

Interactive workflows (conversational editing, live demos) favor Instant. Batch workflows or single-shot high-stakes outputs can absorb Thinking latency.

## Examples from the research

### Instant-appropriate (simple, fast)

```
Sam Altman, Donald Trump, and Elon Musk working behind the counter of a busy movie theater
```

Simple subject, recognizable faces, no reasoning needed.

```
Help me generate a screenshot of Prabowo versus Anies in the mid lane in Mobile Legends
```

Game-aesthetic, single frame, Instant is plenty.

### Thinking-required (search or consistency)

```
Generate an infographic about activities I should do with tomorrow's weather in San Francisco in mind.
```

Requires web search for weather. Thinking only.

```
generate an image of today's IPL match with the current playing XI.
```

Requires search for current lineup. Thinking only.

```
Manga-style fantasy comic page, Page 1 of 4, showing the protagonist discovering a hidden temple. Use Seinen style with high contrast ink work.
```

Multi-page narrative with consistency. Thinking required for 4-page continuity.

### Thinking-recommended (quality upgrade)

```
Bauhaus-inspired poster with bold typography that says "GPT IMAGE 2" and "DESIGN THE FUTURE".
```

Instant works. Thinking produces tighter typographic hierarchy and cleaner Bauhaus palette choices.

```
Luxury fashion book spread, premium hospitality campaign using Korean typography.
```

Instant renders; Thinking renders more culturally authentic Korean editorial conventions.

## How the skill surfaces this

Each sub-agent states a mode recommendation in the preamble with a one-line reason. Users can override. The skill does not silently default to Thinking across the board because the cost and latency differences are material.

If the user explicitly states their mode ("I'm using Instant," "Give me Thinking prompts"), the skill honors that and does not second-guess.

If the user asks which mode to use for a specific task, load this file and walk them through the decision tree.
