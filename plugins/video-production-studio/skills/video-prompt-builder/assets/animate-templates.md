# Prompt Templates

Structural templates for each mode's prompt output. These are scaffolds, not fill-in-the-blanks. Adapt phrasing to the specific brief. The structure ensures consistency. The language adapts to the concept.

## Image-to-Video Prompt Template

Single reference image animated. Focus on motion, not description.

### Short Clip (single shot, 3-8 seconds)

```
Using the uploaded [explicit description of subject, pose, setting, lighting, and notable details], [describe the primary motion: what moves, in which direction, at what speed]. Camera [camera behavior: push-in, orbit, static, tracking]. [Secondary motion: environmental elements, atmospheric effects, fabric, hair]. [Speed/timing: normal speed, slow-motion percentage, speed ramp]. [Lighting shifts if any]. Maintain [identity anchors: specific features, outfit, expression foundation that must not change]. [Duration]. Do not change aspect ratio.
```

### Multi-Shot Sequence (4+ shots)

Each shot follows this structure:

```
SHOT [N] ([timestamp]). [Shot Name]
EFFECT: [Primary effect] + [secondary effects]
Using the uploaded [explicit description], [what moves in this shot]. Camera [behavior]. [Speed/timing]. [Subject identity anchors repeated]. [Transition to next shot]. Do not change aspect ratio.
```

## Keyframe Interpolation Prompt Template

Two reference images: start state and end state. Prompt describes the transformation between them.

### Variation Format (3-5 variations exploring different interpolation styles)

```
Starting from the uploaded [explicit description of start frame: subject, pose, environment, lighting, mood], transition toward the state shown in the uploaded [explicit description of end frame: what changed, new pose, new environment, new lighting, new mood]. [Transformation style: smooth morph / dramatic shift / physics-based / time-lapse]. [What changes first, what changes last. sequencing the transformation]. [Midpoint description: what the halfway state looks like]. Camera [behavior during transformation]. [Speed/pacing: constant, accelerating, decelerating]. [Duration]. Maintain [persistent elements: what stays constant across both states]. Do not change aspect ratio.
```

### Shot-by-Shot Format (for complex transformations)

```
SHOT 1 ([timestamp]). Anchor Start State
EFFECT: [Subtle motion establishing the start frame is alive]
Starting from the uploaded [explicit start frame description], [minimal motion: breathing, wind, ambient movement]. Camera [static or very subtle]. Maintain [all start-state anchors]. Do not change aspect ratio.

SHOT 2 ([timestamp]). Transformation Begins
EFFECT: [First transformation effect]
[What element begins changing first]. [Direction and speed of change]. Camera [reacts to or reveals the change]. [Start frame anchors still mostly intact]. Do not change aspect ratio.

SHOT N ([timestamp]). Arrive at End State
EFFECT: [Resolution effect]
[Final elements settle into the end state shown in the uploaded end frame description]. Camera [final position]. [All end-state anchors now established]. Do not change aspect ratio.
```

## Multi-Image Shot Prompt Template (Seedance 2.0 Native)

Seedance 2.0 supports a native multi-image multi-shot syntax. One prompt references multiple uploaded images by `@imageN` tags and describes a full sequence (up to ~15 seconds from up to 9 images). This is a streamlined node-based workflow compressed into a single prompt.

### Structure

```
[Style, context, character preamble. One line describing visual style, world, and main subject.]
[Shot 1] [What happens in shot 1, referencing @image1 or another image.]
[Shot 2] [What happens in shot 2, referencing @imageN.]
[Shot 3] [What happens in shot 3, may reference one or more images: @imageN, @imageM.]
[Shot 4] [What happens in shot 4.]
[Shot 5] [What happens in shot 5. Closing shot can reference multiple images.]
[Music, background noise, audio context. One line.]
Do not change aspect ratio.
```

### Reference Example (Seedance 2.0 idiomatic)

```
Cinematic 3D render, warm golden-hour kitchen, a small husky in a white chef hat,
[Shot 1] In a bustling restaurant kitchen, the chef husky stirs a copper pot in @image1.
[Shot 2] The husky in @image2 glances at the camera and barks a single command.
[Shot 3] A waiter in @image3 rushes past carrying a steaming plate from @image4.
[Shot 4] Rapidly fly over the finished dishes on @image5, @image6, @image7.
[Shot 5] The scene ends with @image8 and a title card reading "Chef Husky."
Warm jazz piano, ambient kitchen clatter, soft laughter in the background.
Do not change aspect ratio.
```

### Rules

- One prompt in one code block. Not N prompts.
- `@imageN` numbering follows upload order. @image1 is the first uploaded image, @image2 the second, and so on.
- Each shot is 1-2 sentences. Tight. Action-focused.
- Shots can reference one image or multiple images.
- Preamble is one line. Style + context + character.
- Audio/music outro is one line at the end.
- Always close with "Do not change aspect ratio."
- Do NOT use the "Using the uploaded [description]..." prefix. That convention is for other sub-modes. Seedance native syntax uses @tags instead.

### Image Mapping Block (shown in the response, NOT in the prompt)

Above the prompt code block, present a mapping so the user knows which upload corresponds to which @tag:

```
IMAGE MAPPING:
@image1 = [description of first uploaded image]
@image2 = [description of second uploaded image]
@image3 = [description of third uploaded image]
...
```

This mapping is for the user's reference. It is not part of the Seedance prompt itself.

## Extended Seedance 2.0 Reference Tags

Beyond `@imageN`, Seedance 2.0 community prompts use additional reference tag types:

**`@video1`**: Motion reference. Points to an uploaded video whose movement, pacing, or camera behavior should be inherited. "Camera motion follows @video1."

**`@Audio1`**: Audio reference. Points to an uploaded audio clip for beat sync or ambience matching. "The rhythm of @Audio1 intensifies during Shot 3."

These tags work identically to `@imageN` inside the shot list. Reference them in the IMAGE MAPPING block using the same pattern:

```
IMAGE MAPPING:
@image1 = [first uploaded image description]
@video1 = [uploaded video description, for motion reference]
@Audio1 = [uploaded audio description, for beat sync]
```

## Continue Video Pattern

For sequential generation where the user wants to extend an existing Seedance output:

```
Continue this video. [What happens next in one or two sentences.] [Camera behavior]. [Audio continuation.] Do not change aspect ratio.
```

Example from community: "Continue this video, the phone reforms back into the smart phone and lands onto the ground."

Use when the user references a previous generation and wants a narrative continuation. Keep the prompt tight. The model inherits style and subject from the prior clip.

## JSON-Formatted Seedance Prompt (Optional)

Some community users prefer structured JSON for Seedance 2.0 prompts. Offer this variant only when the user explicitly requests JSON format or API-style structure.

```json
{
  "style": "cinematic 3D render, warm golden hour kitchen",
  "character": "small husky in a white chef hat",
  "shots": [
    {"id": 1, "action": "stirs a copper pot", "reference": "@image1"},
    {"id": 2, "action": "glances at camera and barks a command", "reference": "@image2"},
    {"id": 3, "action": "rushes past with steaming plate", "reference": "@image3, @image4"}
  ],
  "audio": "warm jazz piano, ambient kitchen clatter",
  "duration": "15s",
  "aspect_ratio": "preserve"
}
```

The natural-language template remains the default. JSON is only for users who ask for it.

## Role-Based Multi-Reference Prompt Template (Model-Agnostic)

For Kling, Veo, Sora, and other models that accept role-assigned reference images (subject reference, style reference, environment reference, mood reference).

### Shot Prompt Structure

```
SHOT [N] ([timestamp]). [Shot Name]
EFFECT: [Primary effect] + [secondary effects]
Using the subject from the uploaded [explicit description of subject reference: identity, features, clothing, pose], placed in the environment from the uploaded [explicit description of environment reference: space, architecture, lighting, atmosphere], rendered in the visual style of the uploaded [explicit description of style reference: color palette, grain, contrast, mood, photographic quality]. [What moves in this shot]. Camera [behavior]. [Speed/timing]. [How the references integrate: which dominates, where they blend]. Maintain [identity anchors from subject reference]. [Transition to next shot]. Do not change aspect ratio.
```

If only two references (e.g., subject + style, no separate environment):

```
Using the subject from the uploaded [explicit subject description], rendered in the visual style of the uploaded [explicit style description]. [Environment described in text since no environment reference]. [Motion, camera, effects]. Maintain [identity anchors]. Do not change aspect ratio.
```

## BUILD Shot Prompt Template

Text-only brief, no reference images. Full description of the visual.

```
SHOT [N] ([timestamp]). [Shot Name]
EFFECT: [Primary effect] + [secondary effects if stacked]
[Detailed description of what is visible: subject, environment, lighting, composition]
[Camera behavior: angle, movement, lens, position]
[Speed/timing: percentages, durations, ramp directions]
[Subject appearance details repeated for character consistency]
[Atmospheric and environmental details]
[Transition out: how this shot exits and connects to the next]
```

## Supporting Section Templates

### Effects Inventory Entry

```
[N]. [EFFECT NAME] (used [count]x). Shots [list]. [One-line role description].
```

### Density Map Entry

```
[timestamp range] = [HIGH/MEDIUM/LOW] DENSITY ([brief effect list]. [count] effects in [duration])
```

### Energy Arc Structure

```
Act 1 ([time range]): [ENERGY LEVEL]. [What happens and why].
Act 2 ([time range]): [ENERGY LEVEL]. [What happens and why].
Act 3 ([time range]): [ENERGY LEVEL]. [What happens and why].
```

## Timeline Brackets Template (Seedance 2.0 native structure)

Alternative structured format for multi-shot prompts. Cleaner than "SHOT 1 / SHOT 2" labels. Matches the pattern in highest-engagement Seedance prompts.

```
Style: [STYLE_FAMILY + cinematic markers: 35mm anamorphic, 24fps, film grain]. Duration: [Ns].
[00-05s] Shot 1: [Shot name]. [Subject + action]. Camera: [movement]. Lighting: [description]. [Dialogue cue if any].
[05-10s] Shot 2: [Shot name]. [Subject + action]. Camera: [movement]. Lighting: [description].
[10-15s] Shot 3: [Shot name]. [Subject + action]. Camera: [movement]. Lighting: [description].
Constraints: consistent faces and clothing, no deformation, realistic physics, stable proportions.
Audio: [ambient], [foreground sound], [music or score].
Do not change aspect ratio.
```

Use this when the user requests: precise timing, a single-prompt multi-shot output, Seedance 2.0 native syntax, or a time-coded script. This is an alternative to the BUILD shot-by-shot format, not a replacement.

## Video Continuation Template (@video1 reference)

Seedance 2.0 supports `@video1` as a motion reference for extending a previous generation. Use this when the user wants to continue, extend, or chain a prior video without regenerating from scratch.

```
Continue from @video1. [What happens next: motion, action, transformation]. Camera: [movement]. Style: [maintain @video1 style, any evolution]. Constraints: consistent characters, clothing, and environment from @video1, no deformation. Audio: [diegetic continuation]. Duration: [Ns]. Do not change aspect ratio.
```

Example: "Continue from @video1. The phone reforms back into its shape and lands softly on the ground. Camera: slow push-in following the reformation. Style: maintain @video1 cinematic realism. Constraints: consistent material physics and lighting. Audio: subtle reverse-shatter crystalline tones settling into a gentle impact thud. Duration: 5s. Do not change aspect ratio."

Use this for sequence chaining, extending action beats, reversing transformations, or producing director-continuation cuts. `@video1` references the most recent generation unless the user specifies otherwise.

## Positive Constraints Library

Drop-in consistency clauses for any prompt. Pick the one matching the context.

**Character-driven:**
```
Consistent faces, clothing, and hairstyles throughout without deformation, drift, or artifacts.
```

**Physics-heavy:**
```
Consistent gravity, realistic material response, accurate collision, no floating objects.
```

**Portrait / subtle motion:**
```
Clear undeformed face, normal human body structure, stable proportions, rich skin and fabric detail.
```

**Multi-shot coherence:**
```
Consistent lighting, environment, and character identity across all shots.
```

## Diegetic Audio Library

Standard audio outro lines by context.

- **Action:** "Footsteps, fabric rustle, weapon impact, distant echo."
- **Nature:** "Wind through leaves, flowing water, ambient birdsong."
- **Urban:** "Distant traffic, neon hum, footfalls on wet pavement."
- **Interior / intimate:** "Soft breathing, room tone, faint score."
- **Commercial / product:** "Subtle impact, material chime, ambient hum."
