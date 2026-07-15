# Seedance 2.0 Technical Patterns

Production patterns extracted from viral Seedance 2.0 prompts. Use these to harden BUILD and ANIMATE output.

## Timeline Brackets

Native multi-shot syntax. More structured than plain Shot 1 / Shot 2 labels.

```
[00-05s] Shot 1: [description]
[05-10s] Shot 2: [description]
[10-15s] Shot 3: [description]
```

Use this inside the Seedance native multi-image prompt OR inside BUILD shot blocks when the user wants precise timing. Works for 5s, 10s, 15s durations.

## Reference Tags

- `@image1`, `@image2`... `@image9`. static image references, numbered by upload order
- `@video1`. PREVIOUS video reference for motion continuation. Use when the user wants to extend or continue a prior generation. Example: "Continue from @video1, the phone reforms back into its shape and lands on the ground."
- `@audio1`. audio reference for beat sync. Example: "The rhythm of @audio1 intensifies. fast spins enter."

`@video1` is new capability. Unlocks sequence chaining without regenerating from scratch.

## Positive Constraints Clause

Standard closing clause for photorealistic or character-driven prompts. Drop into any shot or at the end of the prompt:

```
Consistent faces and clothing, no deformation, realistic physics, stable proportions, no artifacts.
```

Variants by context:
- Character: "consistent faces, clothing, hairstyles throughout without deformation, drift, or artifacts"
- Physics-heavy: "consistent gravity, realistic material response, accurate collision"
- Portrait: "clear undeformed face, normal human body structure, rich details"

## Diegetic Audio Cues

Seedance 2.0 has native audio sync. Every Seedance prompt should close with an audio line.

Format: `[ambient sound], [foreground sound], [music or score], [dialogue cue if any].`

Examples:
- "Rustling leaves, blade ring, distant birds."
- "Warm jazz piano, ambient kitchen clatter, soft laughter."
- "Diegetic wind, subtle orchestral swell."

## Lens and Format Specs

Filmic markers that materially improve output quality:
- **24fps**. cinematic default
- **35mm anamorphic**. widescreen filmic grain
- **2.35:1**. cinematic widescreen ratio
- **8K sharp** or **4K resolution**. detail target
- **Shallow DOF / creamy bokeh**. subject isolation
- **Warm film grain**. analog texture

Drop 2-3 of these into the Style line of any prompt.

## Subject-Action-Environment-Camera-Style Order

Harvested prompts consistently follow this clause order within a shot:

1. **Subject** (who/what, with identity anchors)
2. **Action** (what happens)
3. **Environment** (where)
4. **Camera** (movement, angle, lens)
5. **Style** (aesthetic, film format, grade)
6. **Constraints** (consistency clause)
7. **Audio** (diegetic cues)

This order is not mandatory but matches the pattern in the highest-engagement prompts.

## Word Count Sweet Spot

60-150 words per prompt for single-shot. 200-400 words for full multi-shot Seedance native. Below 60 words loses detail. Above 400 introduces contradictions.
