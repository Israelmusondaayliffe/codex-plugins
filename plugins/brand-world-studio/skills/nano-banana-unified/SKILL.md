---
name: nano-banana-unified
description: "Unified prompt architect for Gemini 3 Pro Image (Nano Banana). Generates 10 production-ready prompts per query across four modes. CREATE: text-to-image, comics, stickers, icons, infographics, data viz. EDIT: image editing, style transfer, inpainting, show-me angles, multi-reference composition, character transformation. BRAND: brand design, identity systems, logo treatments, mockups, apparel, typography, capsule collections, 35+ brand use cases with DNA extraction. GRID: 6-9 image campaign grids, moodboards, visual systems using Gizem methodology. Backed by 43+ use case patterns, 127 creative directions, texture library, and official Google templates. Triggers: nano banana, gemini image, generate image, create image, image prompt, edit this image, show me angles, brand design, brand identity, brand mockup, logo treatment, brand visualization, capsule collection, grid, campaign grid, moodboard, comic, sticker, infographic, diagram, product concept, or any Gemini image generation request."
---

# Nano Banana Unified — Prompt Architect

Generate 10 production-ready prompts for Gemini 3 Pro Image. One skill covering all modes: creation, editing, brand design, and campaign grids.

## Core Understanding

Gemini 3 Pro Image uses extended thinking to plan composition, logic, and layout BEFORE generating pixels. Write creative briefs, not tag stacks. Describe the WHY, not just the WHAT. Be granular where it matters (skin texture for macro, material properties for products, spatial relationships for scenes). Trust the model's intelligence with context, metaphor, and storytelling.

Load `references/core-knowledge.md` for full shared fundamentals (anti-paste, diversity enforcement, skin/product prompting, AR intelligence, Google templates, quality benchmarks, limitations).

---

## Shared Format Rules

### Output Mandate

**Exactly 10 prompts** per query, each in its own code block.

**Distribution** (default):
- 1 SAFE (commercially viable, predictable)
- 3 INVENTIVE (creative but grounded)
- 3 BOLD (pushes boundaries, unexpected)
- 3 EXPERIMENTAL (avant-garde, high-risk/high-reward)

User can override distribution.

### When User Uploads Image(s)

1. FIRST: Write explicit description of what's in each image.
2. EVERY editing prompt MUST start: "Using the uploaded [explicit description]..."
3. EVERY editing prompt MUST end: "Do not change aspect ratio."
4. NEVER use: "the image", "this photo", "Image 1", generic references.

### When No Images Uploaded

1. Specify AR explicitly as last element: "16:9" or "1:1" etc.
2. Natural language descriptions only.
3. NO MidJourney parameters (no --ar, --exp, --q, --style, --v, --sref).

### Universal Quality Rules

- Natural language, cinematic/poetic phrasing. No tag stacking.
- 120-word cap per prompt (except brand design, which has no word cap).
- Each prompt in its own triple-backtick code block.
- Replace every em-dash with a period (new sentence) or comma (continue thought).
- No AI cliches: delve, leverage, unlock, journey, game-changer, paradigm shift, deep dive, synergy, scalable, robust, disruptive, bandwidth, revolutionary, groundbreaking.
- No emojis.

---

## Router Logic

Assess the user's request and route to the appropriate agent.

### CREATE mode → Load `agents/agent-create.md`

**Triggers**: Text-only request with no image uploads. User wants images generated from a concept, idea, or description.

Also routes here for specialized creation:
- Sequential art / comics / storyboards
- Stickers / icons / emojis
- Infographics / data visualization / dashboards
- Text-in-image / typography art

### EDIT mode → Load `agents/agent-edit.md`

**Triggers**: User uploads image(s) AND wants changes, transformations, or explorations.

Sub-modes detected by the agent:
- **Image Editing**: Upload + modification request (add, remove, style transfer, relight)
- **Show-Me**: Upload + angle/perspective request
- **Multi-Reference**: Multiple uploads + composition request
- **Image-Only**: Upload with no specific direction (explore possibilities)

### BRAND mode → Load `agents/agent-brand.md`

**Triggers**: Request involves a brand name with design intent. Keywords: brand, branded, logo, identity, mockup, capsule, reinterpretation, brand DNA, brand kit, brand design, brand visualization, product concept, logo treatment, brand mockup, capsule collection.

Examples: "Nike boxing gloves", "Tesla branded souvenirs", "Chanel fire extinguisher", "surprise me with Patagonia"

### GRID mode → Load `agents/agent-grid.md`

**Triggers**: User wants multi-image grids, campaign grids, Instagram feed grids, product photography series, brand moodboards, cohesive visual systems, or multi-image content series. Keywords: grid, campaign grid, Instagram grid, moodboard, visual system, content series, 3x3, 2x3.

### Ambiguous Requests

If the request could fit multiple modes, use this priority:
1. If brand name + design intent present → BRAND
2. If "grid" or multi-image series requested → GRID
3. If image(s) uploaded → EDIT
4. Otherwise → CREATE

If still unclear, ask the user which mode they need.

---

## Shared Resources

All agents reference:
- `references/core-knowledge.md` — Anti-paste, diversity enforcement, skin/product prompting, AR intelligence, Google templates, quality benchmarks, limitations
- `references/creative-directions.md` — 127 concept starters for breaking sameness
- `references/texture-library.md` — Skin, material, environmental texture tokens

CREATE and EDIT agents also reference:
- `references/use-case-patterns.md` — 43 specialized workflows with examples

BRAND agent also references:
- `references/brand-design-catalog.md` — 35+ brand design use cases with templates
- `references/brand-dna-extraction.md` — Brand DNA framework + 20 example extractions
- `references/creative-directions-brand.md` — Brand-specific creative starters (7 axes)
- `references/shared-patterns.md` — Cross-cutting visual specs, UI conventions

---

## Philosophy

Every prompt is a creative brief to a reasoning model that THINKS before it creates. The model explores the description, plans the composition, and generates something matching the INTENT. Write for that model. Describe the feeling, the story, the moment.

The goal is not 10 variations. The goal is 10 DIFFERENT outputs that could have come from 10 different shoots, photographers, or creative directors. Unified only by the core subject and user intent.
