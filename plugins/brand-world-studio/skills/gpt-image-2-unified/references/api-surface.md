# API Surface

GPT Image 2 API endpoint, parameters, pricing, rate limits. Based on OpenAI official documentation and community confirmation as of April 21, 2026.

Confidence levels flagged inline. Revisit in 2 to 4 weeks as the docs firm up.

## Endpoints

- `POST /v1/images/generations`: legacy image-generation endpoint with updated support for `gpt-image-2`
- `POST /v1/responses`: new Responses API with integrated tool calling (including Thinking mode and web search)

Model ID: `gpt-image-2`

Integrated in Codex without a separate API key.

## Core parameters

| Parameter | Type | Values | Notes |
|---|---|---|---|
| `model` | string | `gpt-image-2` | Required |
| `prompt` | string | text | Required |
| `size` | string or object | `square_hd` (1024x1024), `portrait`, `landscape`, or custom `{width, height}` | Custom sizes: max edge under 3840 px, multiple of 16, ratio within 3:1 to 1:3, total pixels 655K to 8.29M |
| `quality` | enum | `low`, `medium`, `high` | Token consumption scales with quality |
| `n` | integer | 1 to 8 | 1 to 4 for Instant, up to 8 for Thinking |
| `thinking_level` | enum | `minimal`, `high`, `dynamic` (beta) | Controls reasoning depth in Thinking mode |
| `response_format` | string | image URL or base64 | Standard |
| `response_modalities` | array | `["image"]` or `["text", "image"]` | Image-only saves ~0.5% (negligible; Thinking tokens always generated) |

## Aspect ratio handling

Range: 3:1 to 1:3.

Common sizes and pricing indicators (confidence: medium, based on launch estimates):

| Resolution | Quality | Approx. thinking tokens | Approx. total cost |
|---|---|---|---|
| 512x512 | low | ~200 | $0.018 |
| 1024x1024 | low | - | $0.006 |
| 1024x1024 | medium | - | $0.053 |
| 1024x1024 | high | ~500 | $0.211 |
| 1024x1536 | high | ~800 | $0.165 |
| 2560x1440 (2K) | high | ~1200 | $0.230 |
| 3840x2160 (4K) | high | ~2000 | $0.410 |

Note: vertical 1024x1536 high is actually cheaper than square 1024x1024 high. GPT Image 2 optimizes its generation grid differently for portrait outputs.

## Token-based pricing

OpenAI moved to a tokenized output pricing model.

| Token type | Rate per 1M tokens |
|---|---|
| Image output tokens | $30.00 |
| Image input tokens | $8.00 |
| Text output tokens | $10.00 |
| Text input tokens | $5.00 |
| Cached input | reduced (varies) |

Thinking tokens are billed regardless of whether `includeThoughts` is true. The model's reasoning effort is always paid-for.

## Rate limits

- Standard platform limits apply initially (Tier 1)
- Thinking mode requests subject to a separate "Reasoning Rate Limit" to prevent GPU cluster exhaustion
- Organizations must complete "API Organization Verification" before accessing the full capability of GPT Image 2

Specific RPM / TPM values are tier-dependent and not consistently documented at launch; check the OpenAI dashboard for current limits.

## Authentication

Standard OpenAI API key.

Codex integration: no separate key required (inherits the session).

## Provenance and watermarking

All outputs carry:
- C2PA provenance metadata (strippable via screenshots or re-upload)
- Imperceptible watermark (embedded in pixel data)

No parameter to disable either.

## Response structure

Standard response:
- `created` timestamp
- `data` array with `url` or `b64_json` per image
- `usage` object with token consumption breakdown (image, text, thinking)

## Legacy model status

- `gpt-image-1.5`: remains in API for legacy support; no longer default
- `dall-e-2`, `dall-e-3`: retiring May 12, 2026
- Sora (image side): shut down March 24, 2026

## Failure responses

Common failure patterns flagged by community reports:

- Safety refusal: returns a refusal message without generated image; retry with reframed prompt
- Resolution out of range: validator error; adjust size
- Aspect ratio outside 3:1 to 1:3: validator error; adjust size
- Pixel count outside 655K to 8.29M: validator error; adjust size
- Rate limit: standard 429 response with retry-after

## Knowledge gaps (revisit in 2 to 4 weeks)

- Exact per-minute and per-day Thinking-mode rate limits by tier
- Actual pricing edge cases for partial Thinking token generation
- Batch-export tooling for the 8-output sets (pre-release Codex demo only at launch)
- Official max reference-image count for COMPOSE workflows
- Full parameter schema for `thinking_level: dynamic` (beta)
