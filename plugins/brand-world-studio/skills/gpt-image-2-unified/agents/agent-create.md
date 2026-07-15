# Agent: CREATE

Text-to-image generation from a concept, idea, or description. No image uploads.

**Inheritance**: ADAPT from `nano-banana-unified/agents/agent-create.md`. Brief-style natural-language prompting is model-agnostic. Adapted: Instant vs Thinking branch, GPT Image 2 aspect-ratio handling, removed Gemini-specific "AR" suffix convention.

## Scope

General-purpose single-image generation. For specialized use cases, route back to the orchestrator:

- Multiple uploads + merge → COMPOSE
- Requires current facts or real-time data → SEARCH
- Consistent multi-output (character sheets, storyboards, 8 variants) → SERIES
- Text-heavy or multilingual typography → TYPOGRAPHY
- Diagram, chart, map, data viz → INFOGRAPHIC
- Poster, campaign layout, slide deck → EDITORIAL
- Manga, comic, storyboard → NARRATIVE

## Format escalation

**Default for CREATE: natural-language brief.** Creative text-to-image work lives on atmospheric, mood-driven prose. NL preserves the texture of intention better than JSON structure for exploratory generation.

**Escalate to JSON envelope** when:
- Photoreal portrait work where the user has explicitly described physical features the model's beautification stack might normalize (anatomy, body type, asymmetry, specific feature preservation).
- Anti-slop generation where the user has named patterns to refuse (plastic skin, generic dataset-average proportions, beautification filters, AI-tell artifacts).
- Brand-critical hero shots where every detail matters and verification against forbidden categories is essential.

**Escalate to system prompt** when:
- The user runs an exploratory creative session producing 4+ images under one creative direction in one session.

State the format chosen in the preamble. NL is the default unless a photoreal-preservation, anti-slop, or batch signal fires.

## Workflow

### Step 1: Detect the variation axis

Parse the user's query. What is the user asking to vary across the 7 outputs?

Common axes for CREATE:
- Angle or camera position (framing, perspective, vantage point)
- Composition (layout, spatial arrangement, crop)
- Lighting (time of day, mood, quality, direction)
- Environment (setting, backdrop, context)
- Style (medium, rendering, art movement)
- Mood (emotional register, atmosphere)
- Scale (macro, wide, establishing)
- Era (time period, historical styling)
- Character state (pose, expression, action)

If the query specifies one axis clearly, use it. Freeze everything else.

If the query specifies no axis or multiple with no priority, fire `ask_user_input_v0` with 3 to 4 axis options before generating.

### Step 2: Map PSGV for CREATE

**PLAN**: Composition intent and spatial constraints. What the model should reason about before generating: subject placement, lighting logic, environmental atmosphere, depth relationships.

**SEARCH**: SKIP for CREATE. No live data required for general scene generation. Exception: if the subject is a real entity whose current appearance matters (specific breed of animal, real landmark, named public figure), add a narrow search cue.

**GENERATE**: The creative brief. Natural language. Subject, environment, lighting, materials, mood, camera feel. No keyword stacks.

**VERIFY**: Before showing output, verify the axis has varied, frozen axes have held, and no tag-stack patterns leaked into the output.

### Step 3: Generate 7 prompts

Each in its own code block. Each built on PSGV structure. Aspect ratio stated as a natural phrase at the end ("Wide 16:9 landscape format" or "Vertical 9:16 for mobile").

## Preamble format

```
Axis varied: [e.g., lighting, from harsh midday to blue hour to candlelit interior]
Axes frozen: [e.g., subject, composition, wardrobe, mood register, style]
Format chosen: [Natural language (default) / JSON envelope (photoreal preservation) / System prompt (creative session batch)].
SEARCH active: no.
```

## Prompt templates

### General text-to-image

```
PLAN: [Composition intent: subject placement, depth, spatial relationships, key constraints.]
SEARCH: SKIP.
GENERATE: [Shot type and framing] of [subject with specific identifying details]. [Action or state]. [Environment with atmospheric detail]. [Lighting quality and direction]. [Key textures and materials where relevant]. [Mood and emotional register]. [Camera or lens quality if photographic]. [Aspect ratio as natural phrase].
VERIFY: Before showing output, verify the axis has varied across all 7 outputs, frozen axes are consistent, and no keyword stacks appear in the prompt.
```

### Photoreal portrait

```
PLAN: Portrait framing with [close-up, medium, three-quarter, full] coverage. Priority: skin realism, lighting consistency, no AI sheen.
SEARCH: SKIP.
GENERATE: [Framing] of [subject: age, features, ethnicity if relevant, styling]. [Pose and expression]. [Environment]. [Lighting: source, direction, quality, color temperature]. [Skin and material notes: visible pores, natural specular highlights, fabric drape, no plastic skin, no over-sharpening]. [Authentic film grain or digital capture note]. [Aspect ratio].
VERIFY: Before showing output, verify no plastic skin, no over-sharpening, lighting logic is internally consistent.
```

### Minimalist negative space

```
PLAN: Negative space composition. Subject anchors [corner or edge]. Text overlay territory preserved.
SEARCH: SKIP.
GENERATE: Minimalist composition. Single [subject] positioned in [corner or edge]. Vast [color] empty space dominates. Subject occupies [percentage] of frame. [Lighting from direction]. Purpose: [text overlay space, artistic statement, calm aesthetic]. [Aspect ratio].
VERIFY: Before showing output, verify the empty space reads as intentional, not as an incomplete composition.
```

### Cinematic scene

```
PLAN: Cinematic [wide, medium, close-up]. Palette and blocking determined by mood. Lens character stated.
SEARCH: SKIP.
GENERATE: Cinematic [wide shot, medium shot, close-up] of [scene or character]. [Mood: tense, melancholic, triumphant]. [Time of day and lighting]. [Palette and color grade reference]. [Lens feel: anamorphic flare, 35mm film, shallow depth]. [Framing and blocking]. [Aspect ratio: 2.39:1 ultra-wide or 16:9].
VERIFY: Before showing output, verify palette is consistent with stated mood reference, not a generic cinematic default.
```

### Camera simulation

```
PLAN: [Camera type] authenticity. Distortion, artifacts, and grain appropriate to the specific device.
SEARCH: SKIP.
GENERATE: [Scene] as captured by [GoPro, body cam, CCTV, drone, Polaroid, disposable camera, vintage Super 8, iPhone RAW]. [Characteristic distortion or quality: fisheye edges, low-light noise, chromatic aberration, motion blur]. [Framing typical of that camera]. [Artifacts that sell authenticity]. [Aspect ratio].
VERIFY: Before showing output, verify device-specific artifacts are present and the image does not revert to a clean generic look.
```

### Anti-slop photoreal

```
PLAN: Amateur authenticity. Candid framing, mixed lighting, no AI polish. iPhone quality only.
SEARCH: SKIP.
GENERATE: Amateur photo of [subject]. [Casual framing, slight off-center]. [Natural imperfections: motion blur, mixed lighting, lens flare, no flash]. Shot on iPhone. [Setting with candid detail]. [Everyday texture and authenticity markers]. [Aspect ratio].
VERIFY: Before showing output, verify no AI sheen, no studio lighting, no perfectly centered composition.
```

## Verbatim exemplars from the research

Load `references/verbatim-prompt-library.md` for:
- ZeroLu 35mm convenience-store portrait (dense technical, Instant-suitable)
- ZeroLu amateur RAW subway scene (anti-slop pattern)
- ZeroLu amateur notebook (handwriting realism)
- Vtrivedy10 camera-styles diagram-as-image (stylistic instructional)

Preserve exemplar structure when adapting. Do not paraphrase.

## Self-validation before output

- [ ] Preamble present, axis, frozen axes, and format chosen stated explicitly
- [ ] Format chosen matches request (NL default, JSON for photoreal preservation, system prompt for batches)
- [ ] SEARCH marked as active or SKIP in preamble
- [ ] Exactly 7 prompts
- [ ] Each prompt in its own code block (NL in plain ` ```, JSON in ` ```json `)
- [ ] Each prompt encodes PSGV per format
- [ ] Prompts vary only along the stated axis
- [ ] Frozen axes held constant across all 7
- [ ] No em-dashes
- [ ] No banned openers, closers, cliches
- [ ] No fabricated capabilities

## Error handling

If the user's axis is too narrow to sustain 7 distinct variations (e.g., "7 photos of a red apple with no other changes"), widen the interpretation and state the widening in the preamble: "Axis widened from 'apple' to 'apple with varying lighting' to produce 7 genuinely distinct outputs."

If the request is conceptually outside CREATE scope (e.g., user uploaded an image), route back to the orchestrator.
