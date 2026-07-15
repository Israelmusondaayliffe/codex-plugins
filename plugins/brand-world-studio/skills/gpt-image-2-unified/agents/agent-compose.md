# Agent: COMPOSE

Multi-reference composition. User uploaded two or more images and wants them blended, merged, or unified into new outputs.

**Inheritance**: INHERIT from `nano-banana-unified/agents/agent-edit.md` (Multi-Reference sub-mode). Multi-reference composition logic is model-agnostic. Adapted: Nano Banana Pro supports up to 14 inputs with max 6 objects and max 5 humans for high fidelity. GPT Image 2's equivalent limits are less precisely documented at launch; flag as approximate and default to 2 to 4 references for reliable fidelity.

## Scope

The user uploaded 2 or more reference images. The goal is to produce 7 compositions that combine elements from the references into new scenes. Identity of the subjects or objects must hold. The composition, environment, and narrative context vary across the 7 outputs.

Common COMPOSE use cases:
- Two characters in the same scene
- A character in a referenced environment
- A product placed into a referenced lifestyle scene
- A style reference applied to a subject reference
- A wardrobe from one image on a body from another

For adjacent workflows, route back:
- One image with edits → EDIT
- One image with angle variations → SHOW-ME
- Multi-output with narrative progression → SERIES

## Known limits

- Recommended maximum 4 reference images for reliable identity preservation
- Human character count above 5 degrades consistency
- Brand logo fidelity is weak; expect iterative refinement
- Physics relationships (who-holds-what) sometimes drift; flag in prompts

## Format escalation

**Default for COMPOSE: JSON envelope** for single composition runs, **system prompt** for compose batches.

The forbidden array prevents cross-bleed between references (Ref 1's wardrobe ending up on Ref 2's body, Ref 2's lighting style overriding the unified plan, style reference dominating subject identity). Role separation lives in the JSON keys; refusal of cross-bleed lives in the forbidden array.

Auto-detection rules:

- **JSON envelope format (default)**: any COMPOSE request with 2-4 references and a single composition run. Forbidden array enforces role separation.
- **System prompt format**: when the user wants to run multiple compositions across the same reference set in one batch (e.g., "place these two characters in 7 different scenes" with 4+ output count). The reference identities live in `<visual_dna>` and each composition variation sits inline as a per-image spec inside `<images>`.
- **NL format (fallback)**: exploratory composition, "what could I do with these two images," casual blending without strict identity preservation.

State the format chosen in the preamble.

## Workflow

### Step 1: Describe each upload

```
UPLOADED REFERENCES:
Reference 1: [full description: subject, identity markers, style, lighting, pose]
Reference 2: [full description]
Reference 3: [if present]
...
```

Individual descriptions become the anchor for each element. Vague descriptions produce drifted identities.

### Step 2: Detect the composition axis

For COMPOSE, the axis is usually the composition itself. Common axes:

- Spatial arrangement (where each element sits in the frame)
- Narrative context (what situation they're in together)
- Environment (where the scene takes place)
- Emotional register (the mood of the interaction)
- Framing and camera angle (how the composition is shot)
- Interaction type (what the elements are doing together)

If the user specifies which axis to vary (e.g., "7 different environments for this character + this product"), lock the other axes.

If ambiguous, fire `ask_user_input_v0` with 3 to 4 axis options.

### Step 3: Map PSGV for COMPOSE

**PLAN**: Reference map first. Describe each uploaded reference and what it contributes to the composition. State the identity markers that must hold for each. Resolve lighting unification approach before the brief (references captured under different conditions need a stated lighting plan).

**SEARCH**: SKIP for most composition work. Active when composition must place references into a real-world context requiring current factual accuracy (a specific real location, a current event).

**GENERATE**: The composition brief. Opens with the reference map, then describes spatial relationships, interaction, environment, lighting, and identity preservation requirements.

**VERIFY**: Before showing output, verify each reference's identity markers are preserved. Verify spatial relationships are correct (who stands where, who holds what). Verify lighting is unified across all references, not a patchwork from their source conditions.

### Step 4: Generate 7 prompts

Each opens with a reference map. Each specifies the composition along the chosen axis. Each includes PSGV structure.

## Preamble format

```
Uploaded references: [Ref 1 summary, Ref 2 summary, Ref 3 summary, ...].
Axis varied: [e.g., narrative context, from formal boardroom to casual cafe to outdoor hike].
Axes frozen: identity of each reference subject, style anchor, lighting quality, interaction relationship.
Format: [JSON envelope / System prompt operating contract / Natural language fallback].
SEARCH active: [yes + topic] OR [no].
```

## Prompt templates: JSON envelope format (default for single runs)

Each JSON envelope is a complete composition specification. Reference roles separated. Cross-bleed refused.

### Two-subject scene (JSON)

```json
{
  "plan": "Two-subject composition. Ref 1 and Ref 2 identities preserved. Lighting unified across both subjects, not patchworked from source images. Spatial relationship defined.",
  "search": null,
  "subject": "Composition of [Ref 1 identity: face, hair, wardrobe, markers] and [Ref 2 identity: face, hair, wardrobe, markers]. [Spatial relationship: who is where, what they are doing].",
  "pose": "[Pose for each subject in the composition.]",
  "environment": "[Environment for the scene, unified across both subjects.]",
  "camera": "[Camera angle and framing for the composition.]",
  "lighting": "[Unified lighting source, direction, quality, color temperature applied to both subjects.]",
  "mood": "[Mood register for the scene.]",
  "style": "[Photographic or rendered style, applied uniformly.]",
  "palette": "[Unified palette derived from the scene.]",
  "quality": "[Capture quality applied uniformly to both subjects.]",
  "aspect_ratio": "[W:H]",
  "verify": [
    "Ref 1 identity markers intact",
    "Ref 2 identity markers intact",
    "lighting unified across both subjects",
    "spatial relationship correct",
    "no wardrobe or feature cross-bleed between subjects"
  ],
  "negative_prompt": {
    "forbidden": [
      "wardrobe transfer between subjects",
      "facial feature blending between subjects",
      "hair color or style transfer between subjects",
      "patchwork lighting (each subject lit as in source image)",
      "scale mismatch between subjects",
      "perspective inconsistency between subjects",
      "Ref 1 absorbing Ref 2 features or vice versa",
      "generic group-photo composition replacing requested spatial relationship"
    ]
  }
}
```

### Subject in referenced environment (JSON)

```json
{
  "plan": "Subject from Ref 1 placed into environment from Ref 2. Subject identity locked. Environment locked. Lighting unified.",
  "search": null,
  "subject": "[Ref 1 identity: face, hair, wardrobe, markers] placed in [Ref 2 environment].",
  "pose": "[Pose appropriate to the new environment context.]",
  "environment": "[Ref 2 environment described in detail. Preserve its character.]",
  "camera": "[Camera angle that respects both subject and environment.]",
  "lighting": "[Unified lighting derived from environment, applied to subject.]",
  "mood": "[Mood derived from environment.]",
  "style": "[Style unified across subject and environment.]",
  "palette": "[Palette derived from environment, applied to subject.]",
  "quality": "[Capture quality unified.]",
  "aspect_ratio": "[W:H]",
  "verify": [
    "subject identity intact",
    "environment character preserved",
    "lighting on subject consistent with environment lighting",
    "subject scale appropriate for environment"
  ],
  "negative_prompt": {
    "forbidden": [
      "subject identity drift",
      "environment character drift",
      "subject lit as in original source rather than environment",
      "subject scale wrong for environment",
      "environment redress to match subject's original context",
      "halo or compositing artifact at subject edges",
      "perspective mismatch between subject and environment"
    ]
  }
}
```

### Style reference applied to subject (JSON)

```json
{
  "plan": "Subject from Ref 1 reinterpreted in style from Ref 2. Subject identity preserved. Style applied as full reinterpretation, not filter overlay.",
  "search": null,
  "subject": "[Ref 1 identity] rendered in style of [Ref 2 style anchor].",
  "pose": "[Preserve Ref 1 pose.]",
  "environment": "[Environment in Ref 2 style.]",
  "camera": "[Framing.]",
  "lighting": "[Lighting per Ref 2 style logic, applied to subject.]",
  "mood": "[Mood per Ref 2 style.]",
  "style": "[Ref 2 style: brushwork, palette, line quality, texture, rendering medium.]",
  "palette": "[Ref 2 palette applied throughout.]",
  "quality": "[Style-appropriate fidelity.]",
  "aspect_ratio": "[W:H]",
  "verify": [
    "Ref 1 subject identity recognizable",
    "Ref 2 style fully applied (not filter overlay)",
    "composition coherent under the new style"
  ],
  "negative_prompt": {
    "forbidden": [
      "filter-on-top appearance",
      "subject identity loss",
      "Ref 2 subject features bleeding into Ref 1 subject",
      "incomplete style application (some regions in style, others photoreal)",
      "generic stylization not specific to Ref 2"
    ]
  }
}
```

## Prompt templates: system prompt format (for compose batches)

When the user runs multiple compositions across the same reference set, one batch prompt holds the reference identities at the top and the per-composition variations inline.

```
Generate [N up to 8] separate [aspect ratio] images as a coordinated multi-composition batch using the uploaded references. All [N] share one visual DNA. Composition and narrative context vary across the batch. Reference identities, role assignments, lighting unification hold.

<reference>
Reference 1: [full identity description: face, hair, wardrobe, markers, style anchor].
Reference 2: [full identity description].
Reference 3 (if present): [full identity description].
Reference 4 (if present): [full identity description].

Reference roles:
- Subject reference(s): [Ref X, Ref Y].
- Environment reference: [Ref Z, if present].
- Style reference: [Ref W, if present].

Negative usage: do not pull subject features from style reference, do not pull lighting from subject reference's source image, do not swap roles.
</reference>

<visual_dna>
Composition style: [photographic / rendered medium].
Lighting unification: [single source, direction, quality, color temperature applied to all references in every output].
Mood register: [for the batch].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- reference identity drift across the batch
- role swap between references (subject becoming style, style becoming subject)
- wardrobe or feature transfer between subject references
- patchwork lighting (each reference lit as in its source image)
- style reference subject features leaking into subject reference
- environment reference character loss
- composition collapse to generic group photo
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[composition 1 label]">
[Spatial arrangement, interaction, environment, mood for composition 1. Reference identities and roles preserved.]
</image_1>
<image_2 subject="[composition 2 label]">
[Spec for composition 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Each reference identity preserved across every composition
- Reference roles never swap between images
- Lighting unified per composition, not patchworked from source images
- No cross-bleed between subject references
- Each composition is distinct, no duplicates
- Aspect ratio [W:H] held across every output
</verify>
```

## Prompt templates: NL fallback (exploratory composition)

### Two-subject scene

```
PLAN: Ref 1 identity anchor: [face, hair, wardrobe, key markers]. Ref 2 identity anchor: [same]. Spatial relationship: [who is where]. Lighting unification: [source, direction, temperature].
SEARCH: SKIP.
GENERATE: Using the uploaded references of [Ref 1: specific identity details] and [Ref 2: specific identity details], create a scene showing both subjects [in the specified situation]. [Spatial relationship]. [Interaction: what they are doing]. [Environment and unified lighting]. Preserve each subject's identity markers.
VERIFY: Before showing output, verify Ref 1 identity markers are intact. Verify Ref 2 identity markers are intact. Verify lighting is unified across both subjects, not sourced from their separate reference images.
```

### Subject + environment

```
PLAN: Subject identity anchor: [markers]. Environment anchor: [mood, lighting direction, color palette]. Lighting on subject must match environment logic.
SEARCH: SKIP.
GENERATE: Using the uploaded reference of [subject details] and the uploaded reference of [environment details], place the subject into the environment. [Position in frame]. [Lighting on subject matches environment: direction, color temperature, quality]. [Environmental details around the subject]. Preserve the subject's identity and the environment's mood.
VERIFY: Before showing output, verify subject identity is intact. Verify lighting on subject is consistent with the environment's light source direction.
```

### Subject + product

```
PLAN: Subject identity anchor. Product identity anchor: form, color, branding. Interaction type defined. Environment consistent with product category.
SEARCH: SKIP.
GENERATE: Using the uploaded reference of [subject details] and the uploaded reference of [product details], compose a lifestyle scene where the subject [interacts with, uses, holds, wears] the product. [Natural body language]. [Environment consistent with product category]. [Lighting that flatters both]. Preserve product form, color, and branding exactly. Preserve subject identity.
VERIFY: Before showing output, verify product form and branding are exact. Verify subject identity is intact. Verify the interaction looks physically plausible.
```

### Style reference + subject

```
PLAN: Style transfer attributes: [palette, lighting quality, mood, rendering technique]. Subject identity markers that must survive the transfer. Not a filter. A reinterpretation.
SEARCH: SKIP.
GENERATE: Using the uploaded style reference [palette, mood, rendering, composition] applied to the uploaded subject [identity details], generate a new image. Preserve the subject's identity. Transfer only the style reference's [color palette, lighting quality, mood, rendering technique], not its subject or composition. [Optional: shift pose slightly to prevent a filter-on-top look.]
VERIFY: Before showing output, verify subject identity is recognizable. Verify style-specific characteristics are present. Verify the output is not a pixel-level copy of the style reference.
```

### Wardrobe or attribute transfer

```
PLAN: Subject identity anchor. Wardrobe or attribute to transfer: [fit, color, material]. Source reference for wardrobe defined. Pose and framing frozen.
SEARCH: SKIP.
GENERATE: Using the uploaded reference of [subject] and the uploaded reference of [wardrobe or attribute], dress or equip the subject with the referenced wardrobe. [Fit and fall on the body]. Preserve the subject's facial identity, pose, and framing. Match the original subject's lighting and environment unless specified.
VERIFY: Before showing output, verify wardrobe details match the reference. Verify subject facial identity is intact.
```

### Multi-character ensemble

```
PLAN: Each character's identity anchor stated. Ensemble maximum: 4 references for fidelity. Spatial arrangement and unified lighting defined.
SEARCH: SKIP.
GENERATE: Using the uploaded references of [Ref 1 details, Ref 2 details, Ref 3 details, Ref 4 details], create an ensemble scene. [Spatial arrangement]. [Interaction or unified activity]. [Environment]. [Unified lighting]. Preserve each character's identity. Note: limiting to 4 references maintains highest identity fidelity.
VERIFY: Before showing output, verify each character's identity markers are intact. Verify lighting is unified across all four. Verify spatial positions match the stated arrangement.
```

## Verbatim exemplar from research

@ZeroLu demonstrated cross-universe composition with world knowledge:

```
In the game Zelda totk link is in a e531 series train made by him
```

Pattern: the prompt names specific world-knowledge elements (TOTK, E531 series) and trusts GPT Image 2 to reason about their intersection. Generalizes to any multi-reference blend where world knowledge enriches the composition.

## Failure modes to flag

- Identity drift when references exceed 4 humans
- Logo or brand mark reproduction drift (flag and offer iteration)
- Lighting mismatch when references were captured under very different conditions
- Scale errors when combining subjects of different sizes (flag and specify relative scale)

## Self-validation before output

- [ ] All uploaded references are described individually in detail
- [ ] Preamble names composition axis, frozen axes, format chosen, and SEARCH status
- [ ] Format chosen matches request signals (JSON for single runs, system prompt for batches, NL for exploration)
- [ ] Exactly 7 prompts (or 1 batch prompt with shared visual_dna and N per-image specs in `<images>` if system prompt format)
- [ ] Each prompt in its own code block (JSON in ` ```json `, system prompts in plain ` ``` `, NL in plain ` ``` `)
- [ ] Each prompt encodes PSGV per format
- [ ] Each prompt names the reference map and lighting unification approach
- [ ] Each prompt's verification step checks identity preservation, role separation, and lighting consistency
- [ ] If JSON: forbidden array refuses cross-bleed (wardrobe transfer, feature blending, role swap)
- [ ] Compositions vary only along the stated axis
- [ ] No em-dashes

## Error handling

If the user uploads more than 4 references, warn about fidelity degradation and ask whether to proceed at full count or prioritize 4.

If two references have incompatible lighting conditions (e.g., harsh noon and candlelit night), state the unification approach in the preamble.
