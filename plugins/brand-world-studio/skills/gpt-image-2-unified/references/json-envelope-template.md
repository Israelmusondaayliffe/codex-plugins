# JSON Envelope Template

Structured format for high-stakes singles where drift, normalization, or surgical exclusion is the priority. Reasoning model reads JSON keys as structured instructions, not just description.

## When to use this format

Read `format-ladder.md` for full escalation logic. Quick triggers:

- Anatomy, body, or feature preservation against beautification drift.
- Surgical edits where what to leave alone matters as much as what to change.
- SHOW-ME with style lock against drift.
- Multi-reference COMPOSE with role separation.
- TYPOGRAPHY non-Latin where character corruption is likely.
- INFOGRAPHIC with specific labels where hallucination is likely.
- User explicitly requests JSON format.

## Canonical schema

```json
{
  "plan": "[Composition intent. Spatial relationships. What the model reasons about before generating. State the visual DNA anchor if relevant. State the variation axis frozen vs. varied.]",
  "search": "[Search trigger string with date anchor IF current data needed. Otherwise null.]",
  "subject": "[WHO/WHAT: appearance, clothing, key identifiers, preserved features.]",
  "pose": "[Body position. Hand placement. Crop point. Camera-relative orientation.]",
  "environment": "[Setting. Surfaces. Props. Negative space.]",
  "camera": "[Lens type. Height. Angle. Framing logic. Distortion notes.]",
  "lighting": "[Source. Direction. Quality. Bounce surface. Contrast level. Color temperature.]",
  "mood": "[3 to 5 words. Emotional register.]",
  "style": "[Photographic or rendered style. Realism standard. Reference frame.]",
  "palette": "[5 to 7 color and tone tokens.]",
  "quality": "[Material specifics. Texture standard. Output fidelity. Capture method authenticity.]",
  "aspect_ratio": "[W:H, e.g. 3:4]",
  "verify": [
    "[checklist item 1]",
    "[checklist item 2]",
    "[checklist item 3]"
  ],
  "negative_prompt": {
    "forbidden": [
      "[category-level exclusion 1]",
      "[category-level exclusion 2]"
    ]
  }
}
```

## PSGV mapping in JSON format

| Stage | Where it lives |
|---|---|
| PLAN | `plan` key (top of envelope) |
| SEARCH | `search` key, null if SKIP |
| GENERATE | All descriptive keys taken together: subject, pose, environment, camera, lighting, mood, style, palette, quality, aspect_ratio |
| VERIFY | `verify` array (checklist) plus `negative_prompt.forbidden` array (exclusion list) |

The forbidden array is half of VERIFY. The verify checklist tells the model what to confirm; the forbidden array tells it what to refuse.

## Forbidden array construction rules

This is where the format earns its rung on the reliability ladder. Most prompt libraries skip negative prompting because tag-style negative prompts in non-reasoning models are weak. In a reasoning model, a structured forbidden array signals at the **category** level. The model unpacks each item and refuses the entire class of moves behind it.

### Category-level over keyword-level

Wrong: `"plastic skin"` (keyword)
Right: `"plastic skin", "skin smoothing", "beautification filters", "airbrushed texture"` (category cluster)

The cluster signals: "refuse the entire family of moves that produce synthetic skin." The model reads the pattern, not the literal word.

### Length sweet spot

Observed exemplars sit at 25-35 forbidden items. This is empirical, not proven. Confidence: medium. Pending eval. Rules of thumb:

- Under 15 items: under-constrains. Model has too much room.
- 25-35 items: appears to hit the sweet spot for reasoning to track all categories.
- 50+ items: may flatten priorities. Model loses the relative weight of items.

Run evals to confirm for your subject domain.

### Construction pattern

Group forbidden items into clusters of related refusals. Not strictly required for the model, but easier for you to maintain and audit.

```json
"forbidden": [
  // Anatomy correction cluster
  "anatomy normalization",
  "body proportion averaging",
  "aesthetic proportion correction",
  "dataset-average anatomy",

  // Skin and texture artifacts cluster
  "plastic skin",
  "airbrushed texture",
  "skin smoothing",
  "beautification filters",

  // Lens and framing cluster
  "wide-angle distortion not in reference",
  "lens compression not in reference",
  "cropping that removes intent"

  // Style drift cluster
  "stylized realism",
  "editorial fashion proportions",
  "more realistic reinterpretation"
]
```

### What forbidden arrays do well

- Refuse the model's beautification instinct on photoreal subjects.
- Lock anatomy and feature preservation against safety-stack normalization.
- Prevent style drift on SHOW-ME angle-only requests.
- Prevent character corruption on non-Latin TYPOGRAPHY.
- Prevent data hallucination on INFOGRAPHIC outputs.

### What forbidden arrays do not do

- Override safety policies. The model still refuses prohibited content. Forbidden arrays cannot unlock policy.
- Guarantee anatomical fidelity. They lift the floor; ceiling is still probabilistic.
- Compensate for a vague positive prompt. Garbage in, garbage out.

## ControlNet block: instructional, not literal

Some JSON exemplars include `controlnet` blocks. GPT Image 2 does not run ControlNet. The model reads these fields as instructional cues. Use them for pose lock, depth lock, or composition lock when the wording helps the model reason. Do not assert the model has ControlNet pipelines.

```json
"controlnet": {
  "pose_control": {
    "model_type": "OpenPose",
    "purpose": "Exact skeletal and pose lock",
    "constraints": [
      "preserve shoulder width",
      "preserve hip angle",
      "preserve spine curvature",
      "preserve limb placement"
    ],
    "recommended_weight": 0.95
  },
  "depth_control": {
    "model_type": "ZoeDepth",
    "purpose": "Depth, volume, and camera-to-body spatial lock",
    "constraints": [
      "preserve foreground volume",
      "prevent flat or compressed depth",
      "maintain torso-to-background separation"
    ],
    "recommended_weight": 0.8
  }
}
```

This block functions as a structured constraint statement. The model reads `preserve shoulder width` and reasons about shoulder geometry. The `recommended_weight` value carries no literal weight, but signals priority relative to other constraints.

Use sparingly. Only when pose, depth, or composition lock matters and natural language has failed.

## Framework-anonymized exemplars

Three exemplars from the field. Subject details stripped, structure intact. Study the framework, not the subject.

### Exemplar 1: Photoreal preservation with mirror-selfie authenticity

```json
{
  "plan": "Preserve subject identity and feature specificity against beautification drift. Single high-fidelity output. Visual DNA anchor: amateur smartphone capture authenticity.",
  "search": null,
  "subject": "[WHO: detailed appearance preserving specific features the user wants held against normalization. Clothing described materially, not aesthetically.]",
  "pose": "[Body angle. Hand placement. Crop point. Camera-relative orientation.]",
  "environment": "[Restrained interior with named surfaces and minimal props.]",
  "camera": "Believable mirror selfie perspective. Visible smartphone reflection. Chest-height lens. Realistic amateur framing and accurate proportions.",
  "lighting": "[Soft natural source. Bounce surface named. Low contrast.]",
  "mood": "[3 to 5 words.]",
  "style": "High-fidelity, ultra-realistic amateur mirror selfie photography. Strict adherence to physical reality. Preserving skin pores, micro-details, natural lighting, material realism, unretouched proportions.",
  "palette": "[5 to 7 color and tone tokens.]",
  "quality": "[Material specifics. Capture method realism. Premium amateur smartphone capture without beauty corrections.]",
  "aspect_ratio": "3:4",
  "controlnet": {
    "pose_control": {
      "model_type": "OpenPose",
      "purpose": "Exact skeletal and pose lock",
      "constraints": ["preserve shoulder width", "preserve hip angle", "preserve spine curvature", "preserve limb placement"],
      "recommended_weight": 0.95
    },
    "depth_control": {
      "model_type": "ZoeDepth",
      "purpose": "Depth and volume lock",
      "constraints": ["preserve foreground volume", "prevent depth flattening", "maintain subject-to-background separation"],
      "recommended_weight": 0.8
    }
  },
  "verify": [
    "subject features preserved as described",
    "amateur smartphone authenticity not lost to studio polish",
    "lighting consistent with stated source",
    "no items in forbidden array present"
  ],
  "negative_prompt": {
    "forbidden": [
      "anatomy normalization",
      "body proportion averaging",
      "aesthetic proportion correction",
      "beauty standard enforcement",
      "dataset-average anatomy",
      "camera angles that reduce intended volume",
      "wide-angle distortion not in reference",
      "lens compression not in reference",
      "cropping that removes intent",
      "depth flattening",
      "beautification filters",
      "skin smoothing",
      "plastic skin",
      "airbrushed texture",
      "stylized realism",
      "editorial fashion proportions",
      "more realistic reinterpretation",
      "naturalization of distinct features"
    ]
  }
}
```

### Exemplar 2: Surgical EDIT with preservation

```json
{
  "plan": "Targeted modification of one element. Everything else held against drift.",
  "search": null,
  "subject": "[Subject as visible in source image. Modification target named explicitly: change X to Y.]",
  "pose": "Preserve original pose exactly.",
  "environment": "Preserve original environment, lighting setup, framing, and camera distance.",
  "camera": "Preserve original camera position and lens character.",
  "lighting": "Preserve original lighting source, direction, and quality.",
  "mood": "Preserve original mood register.",
  "style": "Preserve original photographic or rendered style.",
  "palette": "Preserve original palette except where the target modification requires color shift.",
  "quality": "Preserve original capture quality and material rendering. Modification must integrate seamlessly.",
  "aspect_ratio": "[Match source.]",
  "verify": [
    "only the named target element has changed",
    "all preservation clauses held",
    "modification integrates with original lighting and material logic",
    "no items in forbidden array present"
  ],
  "negative_prompt": {
    "forbidden": [
      "changing pose",
      "changing framing",
      "changing camera angle",
      "changing lighting direction",
      "changing background",
      "restyling unaltered subject elements",
      "color grading shift not requested",
      "skin tone adjustment not requested",
      "sharpening or smoothing not requested",
      "regenerating untouched regions"
    ]
  }
}
```

### Exemplar 3: SHOW-ME with style lock

```json
{
  "plan": "Identical subject and style across angle variations. Vary only camera angle and framing distance. Visual DNA: subject identity, wardrobe, lighting, environment, mood.",
  "search": null,
  "subject": "[Subject identity locked. Wardrobe locked. Identifying features preserved.]",
  "pose": "[Pose anchor. Body orientation that allows the requested angle without re-staging.]",
  "environment": "[Environment locked. No re-dressing.]",
  "camera": "[Specific angle for this output. The variation axis. Framing distance named.]",
  "lighting": "[Lighting locked. Same source, direction, quality across all outputs.]",
  "mood": "[Mood locked.]",
  "style": "[Style locked.]",
  "palette": "[Palette locked.]",
  "quality": "[Quality and capture method locked.]",
  "aspect_ratio": "[Locked.]",
  "verify": [
    "only camera angle has varied",
    "subject identity unchanged",
    "wardrobe unchanged",
    "lighting unchanged",
    "environment unchanged",
    "no style drift toward different aesthetic"
  ],
  "negative_prompt": {
    "forbidden": [
      "wardrobe variation",
      "subject identity drift",
      "facial feature change",
      "body proportion change",
      "lighting change",
      "color temperature shift",
      "environment redress",
      "style reinterpretation",
      "mood register shift",
      "palette substitution",
      "rendered medium change",
      "framing intent loss"
    ]
  }
}
```

## Output rules

- Each JSON envelope sits in its own ` ```json ` triple-backtick code block.
- All keys present even when null or "preserve original."
- `forbidden` array sized to the request. Surgical edits run shorter (8-12 items). Photoreal preservation runs longer (20-35 items).
- `verify` array sized 3-6 items. Aligned to the highest-priority risks for that specific request.
- No em-dashes inside any string value. Periods or commas.

## Failure modes specific to JSON format

See `failure-modes.md` for the full list. Quick reference:

- **Over-constraint freeze**: forbidden array too long, model produces a flat or generic output to avoid violating any rule. Reduce array size.
- **Schema literalism**: model treats `controlnet` as if it has the pipeline. State the instructional framing in the user-facing context.
- **Verify drift**: the model claims it verified but the output violates a forbidden item. Surface in failure notes; this is probabilistic, not deterministic.
- **Forbidden under-signal**: forbidden item too vague ("bad"), model cannot unpack to a category. Rewrite as a class of refusals.
