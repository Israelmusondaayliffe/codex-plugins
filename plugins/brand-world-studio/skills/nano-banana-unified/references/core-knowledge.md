# Core Knowledge — Shared Fundamentals

Shared across all agents. Contains Gemini capabilities, anti-paste mandate, diversity enforcement, prompting guides, aspect ratio intelligence, Google templates, quality benchmarks, and limitations.

---

## Gemini 3 Pro Capabilities

- **Reasoning-first generation** — Plans before painting
- **Thinking mode** — Generates interim "thought images" to refine composition
- **Text rendering** — Zero spelling errors, complex layouts, multilingual
- **Multi-reference** — Up to 14 input images (max 6 objects for high-fidelity, max 5 humans for character consistency)
- **4K native** — True high-resolution (1K, 2K, 4K output)
- **Search integration** — Real-time web data for factual infographics
- **Annotation-driven editing** — Draw on images to indicate edits
- **Financial parsing** — Reads PDFs, extracts data, generates dashboards
- **SynthID watermarking** — Invisible authentication in all outputs

---

## Anti-Paste Mandate

**Critical rule for image editing prompts**: Every transformation MUST also change the subject's angle, pose, or spatial relationship. Style transfers, medium changes, and era shifts applied to a static, unchanged pose look like filters pasted on top.

### The Rule

For EVERY editing prompt (except pure technical edits):
- **Primary transformation** + **Secondary spatial/pose change**

### Anti-Paste Modifiers (add ONE per style/medium/era transformation)

| Category | Modifiers |
|----------|-----------|
| Angle shifts | "Recompose as side profile" / "Now viewed from 3/4 angle" / "Shift to low angle looking up" / "From slightly above" |
| Pose changes | "Mid-turn, catching them in motion" / "Leaning forward with intent" / "Relaxed backward lean" / "Arms repositioned to..." |
| Gaze redirects | "Gaze now directed off-frame" / "Eyes closed in contemplation" / "Looking down at hands" / "Direct eye contact with viewer" |
| Body language | "Shoulders turned 30 degrees" / "Weight shifted to one leg" / "Hands now visible in frame" |
| Spatial reframe | "Pull back to reveal more environment" / "Tighter crop on face and shoulders" / "Reframe to include gesture" |

### When Anti-Paste DOES Apply

- Style transfers (oil painting, watercolor, pencil sketch)
- Medium changes (photograph → illustration → 3D render)
- Era/period shifts (modern → Victorian → cyberpunk)
- Character style transforms (realistic → Pixar → anime)
- Material transformations (flesh → marble → bronze)

### When Anti-Paste Does NOT Apply

- Pure background swaps, color grading, lighting changes
- Object addition/removal, text overlays, technical corrections
- Macro/ECU shots where reframing would lose the subject
- Animation keyframes requiring pose consistency
- Product flat-lays where angle is fixed by convention
- Character sheets where consistency across panels is the goal

### Escape Hatch

If user explicitly requests preserving exact pose ("keep the same pose", "don't change position", "match the original framing"), respect that. Anti-paste is a default, not an override of user intent.

---

## Diversity Enforcement

The goal: 10 prompts that feel like they came from 10 different creative directors. How diversity is applied depends on what the user asked for.

### Context-Aware Diversity

**OPEN requests** (vague concept, "surprise me", no specific direction):
Apply full cross-category diversity. Each prompt should explore a fundamentally different creative territory. Pull from multiple categories below.

**DIRECTED requests** (user specifies a dimension like "camera angles", "style transfers", "era shifts"):
Respect the user's direction. Apply diversity WITHIN that dimension. "10 camera angles" means 10 genuinely different angles (worm's eye, bird's eye, OTS, Dutch, POV, drone, profile, 3/4, straight-on, from below). Do NOT force style changes or era shifts when the user asked for angles.

**PARTIALLY DIRECTED requests** (user gives a theme but leaves room, like "editorial variations" or "try different approaches"):
Mix the user's theme with 2-3 adjacent categories for variety. If the user says "editorial variations," vary across composition, lighting, environment, and narrative moment, but don't randomly inject Pixar transformations or marble sculptures.

### The 14 Exploration Categories (Toolkit, Not Checklist)

Use these as a diversity toolkit. For open requests, span as many as possible. For directed requests, stay within relevant categories.

1. **ANGLE/PERSPECTIVE** — Camera position (side profile, bird's eye, worm's eye, OTS, POV, drone, low angle)
2. **MEDIUM/STYLE** — Art form (oil painting, watercolor, charcoal, 3D render, clay, stained glass)
3. **CHARACTER STYLE** — Animation/render style (Pixar, anime, graphic novel, Tim Burton, Wes Anderson)
4. **TIME OF DAY** — Lighting scenario (blue hour, harsh midday, candlelit night, overcast morning)
5. **SEASON/WEATHER** — Environmental condition (autumn, winter, spring rain, summer heat haze)
6. **ERA/PERIOD** — Time period (Victorian, 1920s, 1980s neon, cyberpunk, Renaissance)
7. **AGE SHIFT** — Life stage (as a child, elderly, younger, older)
8. **POSE/ACTION** — Body state (dancing, running, sleeping, laughing, mid-leap)
9. **ENVIRONMENT** — Setting (underwater, in space, mountaintop, library, nightclub)
10. **EMOTIONAL STATE** — Mood/expression (fierce, vulnerable, joyful, melancholic, mischievous)
11. **SCALE SHIFT** — Framing (extreme macro, tiny figure in landscape, medium action)
12. **SURREAL/CONCEPTUAL** — Breaking reality (melting, fragmenting, impossible physics)
13. **NARRATIVE MOMENT** — Story beat (just before, moment of realization, caught mid-secret)
14. **MATERIAL TRANSFORMATION** — Substance shift (marble, bronze, ice, gold)

### Planning Block

Before generating, plan diversity explicitly:

```
DIVERSITY PLAN:
User intent: [what they asked for]
Diversity mode: [OPEN / DIRECTED / PARTIALLY DIRECTED]
Strategy: [which categories to span, or how to vary within the directed dimension]

1. [Concept] — SAFE
2. [Concept] — INVENTIVE
3. [Concept] — INVENTIVE
4. [Concept] — INVENTIVE
5. [Concept] — BOLD
6. [Concept] — BOLD
7. [Concept] — BOLD
8. [Concept] — EXPERIMENTAL
9. [Concept] — EXPERIMENTAL
10. [Concept] — EXPERIMENTAL

Anti-sameness check: No two prompts feel like the same shoot ✓
Anti-paste check (if editing): Style transforms include pose/angle shift (or are exempt) ✓
```

### The Core Anti-Sameness Test

Regardless of diversity mode, no two prompts should produce images that feel like they came from the same photoshoot. If you can swap them and nobody notices, they're too similar. Vary at least 2 of these per prompt: composition, lighting, environment, subject state, or conceptual approach.

---

## Creative Diversity Framework

For each query, explore these dimensions to ensure NO sameness:

### Compositional Axes
- **Scale**: Macro detail → Extreme wide establishing
- **Angle**: Worm's eye → Bird's eye → Dutch → POV → OTS
- **Framing**: Negative space → Layered depth → Frame-within-frame
- **Subject placement**: Rule of thirds → Centered → Edge → Barely visible

### Lighting Axes
- **Direction**: Front → Side → Back → Under → Overhead → Mixed
- **Quality**: Harsh → Soft → Diffused → Dramatic → Practical → Natural
- **Temperature**: Warm golden → Cool blue → Neutral → Mixed color
- **Mood**: Bright optimistic → Moody dramatic → Ethereal soft → Noir hard

### Temporal/Environmental Axes
- **Time of day**: Golden hour → Blue hour → Midday → Night → Overcast
- **Season/weather**: Spring bloom → Summer heat → Autumn gold → Winter frost → Rain → Fog
- **Era**: Period-appropriate → Anachronistic → Timeless → Futuristic

### Conceptual Axes
- **Narrative**: Single moment → Implied story → Before/after → Cause/effect
- **Emotion**: Joy → Melancholy → Tension → Serenity → Power → Vulnerability
- **Style**: Photorealistic → Stylized → Abstract → Surreal → Documentary

### Technical Axes
- **Lens feel**: Wide distortion → Normal → Telephoto compression → Macro → Fisheye
- **Motion**: Frozen → Motion blur → Implied movement → Transition moment
- **Focus**: Deep → Shallow → Tilt-shift → Selective → Soft focus

---

## Photorealistic Skin & Face Prompting

When generating close-up portraits, add texture tokens ONLY for macro/extreme close-ups where pore-level detail matters.

### Token Usage by Shot Distance

| Shot Type | Tokens |
|-----------|--------|
| Extreme Close-Up (ECU) | 3-5 tokens |
| Close-Up (CU) | 2-3 tokens |
| Medium Close-Up (MCU) | 1-2 tokens |
| Medium Shot (MS) and wider | 0-1 tokens |

### Primary tokens
`visible pores`, `natural skin sheen`, `fine peach fuzz`, `constellation of freckles`, `fine lines`, `natural redness`

### Eye Description Requirements

For any portrait, ALWAYS describe eyes with:
- Color (specific: sea-green, amber, storm-gray, not just "blue")
- Expression (steady, searching, distant, intense, soft)
- Gaze direction (direct contact, off-frame, downcast)

Full texture token library in `references/texture-library.md`.

---

## Product & Commercial Prompting

**Subject**: Material, finish, color accuracy, scale indicators
**Environment**: Surface, setting, props
**Lighting**: Setup type, purpose, reflections/highlights
**Camera**: Angle, focus, lens feel

---

## Aspect Ratio Intelligence

Never hardcode. Reason about use case:

| Context | AR |
|---------|----|
| Instagram feed | 4:5 or 1:1 |
| Stories/Reels/TikTok | 9:16 |
| YouTube thumbnails | 16:9 |
| Pinterest | 2:3 |
| Print ads | 4:5 or 8:10 |
| Digital campaigns | 16:9 or 3:2 |
| Infographics | 9:16 (vertical) or 16:9 (presentation) |
| High-end campaigns | 3:4 (reference standard) |

**Default**: If unclear, 16:9 (most versatile). If social, 9:16. If print, 4:5.

---

## Official Google Prompt Templates

Proven structures from Google's documentation. Use as foundations for SAFE prompts.

### Photorealistic Scenes
```
A photorealistic [shot type] of [subject], [action or expression], set in [environment]. The scene is illuminated by [lighting description], creating a [mood] atmosphere. Captured with a [camera/lens details], emphasizing [key textures and details]. The image should be in a [aspect ratio] format.
```

### Stylized Illustrations & Stickers
```
A [style] sticker of a [subject], featuring [key characteristics] and a [color palette]. The design should have [line style] and [shading style]. The background must be [transparent/white].
```

### Text in Images
```
Create a [image type] for [brand/concept] with the text "[EXACT TEXT TO RENDER]" in a [font style]. The design should be [style description], with a [color scheme].
```

### Product Mockups
```
A high-resolution, studio-lit product photograph of a [product description] on a [background surface/description]. The lighting is a [lighting setup] to [purpose]. The camera angle is a [angle type] to showcase [specific feature]. Ultra-realistic, with sharp focus on [key detail]. [AR].
```

### Minimalist & Negative Space
```
A minimalist composition featuring a single [subject] positioned in the [position] of the frame. The background is a vast, empty [color] canvas, creating significant negative space. Soft, subtle lighting. [AR].
```

### Sequential Art / Comic Panels
```
Make a [number] panel comic in a [art style]. Put the character in a [type of scene].
```

### Adding/Removing Elements
```
Using the provided image of [subject], please [add/remove/modify] [element] to/from the scene. Ensure the change is [integration description].
```

### Inpainting / Semantic Masking
```
Using the provided image, change only the [specific element] to [new element/description]. Keep everything else exactly the same, preserving original style, lighting, and composition.
```

### Style Transfer
```
Transform the provided photograph of [subject] into the artistic style of [artist/art style]. [ANTI-PASTE: recompose with new angle/pose]. Preserve the original composition but render it with [stylistic elements].
```

### Multi-Image Composition
```
Create a new image by combining elements from the provided images. Take the [element from image 1] and place it with/on the [element from image 2]. The final image should be a [scene description].
```

### Search-Grounded Generation
```
[Request for visualization] based on [real-time data topic]. Include [specific data points to look up].
```

### When to Use Google Templates vs. Creative Briefs

**Google Templates**: Straightforward, predictable results. Commercial/professional output. Specific format requirements. The SAFE prompt.
**Creative Briefs**: Artistic/experimental. INVENTIVE, BOLD, EXPERIMENTAL prompts. Narrative/emotional content.

Start with Google template for prompt 1 (SAFE), then progressively deviate toward creative briefs for prompts 8-10 (EXPERIMENTAL).

---

## Quality Benchmarks

- **Text accuracy**: 99% headlines, 95% body, 85% small (12pt+)
- **Consistency**: 90% single subject, 85% (2-3 subjects), 75% (4-5 subjects)
- **Style adherence**: 95% named styles, 85% reference transfers
- **Data accuracy**: 95% charts, 90% financial PDFs, 85% web-sourced
- **Grid visual DNA consistency**: 85%+ across grid
- **Creative boldness**: 90%+ prompts break conventional photography

---

## Known Limitations & Workarounds

| Limitation | Workaround |
|-----------|------------|
| Small text (<12pt): ~40% accuracy | Generate at large scale, composite into scenes |
| Analog clock times: ~25% accuracy | Use digital clocks or simple times (12:00, 3:00) |
| Large groups (8+ people): random selection | Limit to 5 people for reliable consistency |
| AR drift: model may change AR | Always specify "Do not change aspect ratio" for editing |
| Prompt reproducibility: ~50% match | Be maximally specific, don't rely on implied context |
| Grid may generate 7-8 instead of 9 | Acceptable. Emphasize count in prompt if needed |
| Subject centering despite instructions | Use "occupies <20% of frame" or specify distance |

---

## Failure Recovery

- **Generic output**: Return to creative exploration, find the weird angle
- **Anti-sameness fails**: Identify duplicates, revise with fresh approach
- **Pasted-on look**: Add angle/pose shift to transformation (unless exempt)
- **Exact pose requested**: Respect escape hatch, skip anti-paste
- **Shallow pattern scanning**: Force-include 2 patterns from numbers 20+ (non-obvious)
- **User wants ≠10 prompts**: Explain 10-prompt mandate for systematic diversity
- **Unclear image**: State assumptions, generate based on best interpretation
- **Limitation hit**: Note in thinking, apply workaround, set expectations
