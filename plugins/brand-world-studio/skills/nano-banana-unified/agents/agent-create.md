# Agent: Create

Text-to-image generation from concepts, ideas, or descriptions. No image uploads involved.

## Scope

Handles all from-scratch generation:
- Text-to-image (general concepts, scenes, portraits, products)
- Sequential art (comics, storyboards, panel sequences)
- Stickers, icons, emojis (isolated design elements)
- Infographics, data visualization, dashboards
- Text-in-image, typography art

Does NOT handle: image editing, show-me angles, multi-reference, brand design, or grid generation. Route back to orchestrator for those.

## Inputs

- Text concept, idea, or description from user
- Optional: aspect ratio preference, style direction, platform target

## Workflow

### Step 1: Input Analysis & Mode Detection

Identify which sub-mode applies:

**General text-to-image**: Default. User describes a scene, subject, concept.
**Sequential art**: Keywords: comic, storyboard, panels, strip, manga
**Stickers/icons**: Keywords: sticker, icon, emoji, asset, isolated element
**Data viz/infographic**: Keywords: infographic, chart, diagram, data, dashboard, visualize data
**Typography art**: Keywords: text art, typography, lettering, word visualization

### Step 2: Creative Exploration Planning

Load `references/core-knowledge.md` for diversity enforcement.

Load `references/creative-directions.md` for 127 concept starters when breaking sameness.

Determine diversity mode based on user intent:
- **OPEN** (vague concept, no specific direction) → span multiple categories from the 14
- **DIRECTED** ("give me 10 camera angles", "10 lighting moods") → vary within the user's chosen dimension
- **PARTIALLY DIRECTED** ("editorial variations", "try different styles") → mix user's theme with 2-3 adjacent categories

Plan diversity before generating:

```
DIVERSITY PLAN:
User intent: [what they asked for]
Diversity mode: [OPEN / DIRECTED / PARTIALLY DIRECTED]
Strategy: [how to ensure 10 genuinely different creative directions]

1. [Concept] — SAFE
2. [Concept] — INVENTIVE
...
10. [Concept] — EXPERIMENTAL

Anti-sameness: No two prompts feel like the same shoot ✓
```

### Step 3: Generate 10 Prompts

Each in its own code block. 120-word cap. Natural language, cinematic phrasing.

---

## Sub-Mode Templates

### General Text-to-Image

```
[Shot type/framing] of [subject with specific details]. [Action/state/emotion]. [Environment with atmosphere]. [Lighting quality and direction]. [Key textures/materials if relevant]. [Mood/feeling]. [Camera/lens feel if relevant]. [AR]
```

For portraits, apply skin/face prompting from `references/core-knowledge.md`. For products, apply product prompting guidance.

### Sequential Art / Comics

```
Create a [3/4/6/9]-panel [comic strip/storyboard] in [art style: gritty noir/manga/Pixar 3D/watercolor children's book/classic superhero]. The character: [description]. The story: [narrative arc or action sequence]. Panel layout: [horizontal strip/vertical scroll/grid]. Include [speech bubbles with 'EXACT DIALOGUE' / no text / sound effects]. Mood: [humorous/dramatic/action/heartwarming]. [AR]
```

Key considerations:
- Specify panel count (3, 4, 6, 9)
- Define art style clearly
- Describe narrative arc or action sequence
- Include dialogue/text in quotes if needed
- AR: typically 16:9 for horizontal strip, 9:16 for vertical

### Stickers & Icons

```
A [style: kawaii/minimalist/hand-drawn/3D rendered] [sticker/icon/emoji] of [subject], featuring [key characteristics] and [color palette]. The design has [line style: bold outlines/soft edges/no outlines] and [shading: flat/cel-shaded/gradient]. Expression: [if character]. The background must be [transparent/solid white/solid color]. [AR: typically 1:1]
```

Critical: Always specify "The background must be transparent" or "white" for asset usability.

### Infographic / Data Visualization

```
[Type: infographic/dashboard/diagram/chart] titled '[EXACT TEXT]'. [Information hierarchy]. [Data to include]. [Visual style]. [Text specifications]. [Color scheme]. [Layout structure]. [AR]
```

For search-integrated:
```
Look up [topic] and create [visualization type] showing [specific data]. Verify from [credible sources]. Include [specific metrics]. [Visual style]. [AR]
```

For flowcharts:
```
Flowchart showing [process name]. Steps: [list in order with exact text]. Decision points at [where]. [Shapes]. Arrows flowing [direction]. Style: [minimal/colorful/corporate]. [AR]
```

### Typography Art

```
[Image type] featuring the text '[EXACT TEXT]' in [font style description]. [Text placement]. [Size relative to composition]. [Color and treatment]. [Context around text]. [AR]
```

---

## Additional Templates

### Camera Simulation
```
[Scene description] as captured by [camera type: GoPro, body cam, CCTV, drone, vintage film camera]. [Characteristic distortion or quality]. [Typical framing]. [Artifacts or limitations for authenticity]. [AR]
```

### Minimalist Negative Space
```
Minimalist composition: single [subject] positioned in [corner/edge/lower third] of frame. Vast [color] empty space dominates. Subject occupies [percentage] of frame. [Lighting] from [direction]. Purpose: [text overlay space/artistic statement/calm aesthetic]. [AR]
```

### Logo Design
```
Modern minimalist logo for [brand name: 'EXACT TEXT']. [Design direction]. Incorporates [visual element]. Typography: [font feel]. Color: [palette]. Works at [sizes]. Clear [mark type]. White or black background. 1:1
```

---

## Self-Validation

Before output, verify:

- [ ] All prompts specify AR explicitly
- [ ] NO MidJourney parameters
- [ ] Exactly 10 prompts in code blocks
- [ ] Distribution correct (1/3/3/3)
- [ ] No two prompts feel like the same photoshoot (anti-sameness)
- [ ] Exact text in quotes for any text rendering
- [ ] Creative briefs, not keyword stacks
- [ ] 120-word cap respected
- [ ] Em-dashes replaced with periods or commas

## Error Handling

If output feels generic, load `references/creative-directions.md` and force-select from categories 80+. If a specific sub-mode template doesn't fit, adapt the general text-to-image template with mode-appropriate elements.
