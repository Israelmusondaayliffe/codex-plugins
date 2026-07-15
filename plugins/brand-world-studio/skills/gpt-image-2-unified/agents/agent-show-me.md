# Agent: SHOW-ME

Angle, perspective, framing, or viewpoint variations of an uploaded subject. Style holds. Angle varies.

**Inheritance**: INHERIT from `nano-banana-unified/agents/agent-edit.md` (Show-Me sub-mode). Axis locking for angle variations is fully model-agnostic. Ported pattern; surface phrasing adjusted for GPT Image 2 reasoning style. The core discipline (do not introduce style changes when the user asked for angles) is the entire point of smart diversity and survives verbatim.

**Update (June 8 2026)**: Angle library reorganized into a shot-distance ladder plus coverage angles. Added extreme close-up, full body, extreme wide, and aerial/drone still framings. Added the "camera movements are not still angles" boundary, which maps dolly/orbit/crane/tracking to still analogues and hands the actual motion off to video-prompt-builder. Sourced from the "20 camera angles for AI creators" reference; the 5 movement entries were correctly excluded as video work.

## Scope

The user uploaded an image and wants the same subject rendered from different camera angles, distances, framings, or viewpoints. The identity of the subject, the style of the image, the lighting, and the mood should all hold across all 7 outputs. Only the camera moves.

If the user asks for any other kind of variation (style, era, mood, environment), route back to EDIT instead.

## Why this mode exists as its own agent

The most common failure when a user says "show me this from different angles" is that the model returns different styles or moods of the subject. This skill exists in part to prevent that. SHOW-ME freezes every non-angle axis and enforces angle-only variation.

## Format escalation

**Default for SHOW-ME: JSON envelope.** The forbidden array is what NL alone cannot enforce. "wardrobe variation," "style reinterpretation," "lighting change," "mood register shift" as forbidden tokens lock the freeze set at the category level. This is the agent's biggest weakness fixed.

Auto-detection rules:

- **JSON envelope format (default)**: any SHOW-ME request with explicit angle variation language and a clearly described subject. Forbidden array enforces the freeze set.
- **System prompt format**: when the user wants to run a multi-angle shoot across multiple subjects in one session (e.g., 8 product shots each from 4 angles, or a character sheet across multiple characters). System prompt holds the angle library and freeze rules.
- **NL format (fallback)**: exploratory requests, "show me a few angles," casual tone with no commitment to surgical precision.

State the format chosen in the preamble. Read `references/json-envelope-template.md` Exemplar 3 for SHOW-ME-specific framing.

## Workflow

### Step 1: Describe the upload

```
UPLOADED SUBJECT: [identity, wardrobe, pose, style of the original image, lighting logic, color palette, mood, distinctive features]
```

The style description is critical here. It becomes the anchor that every SHOW-ME prompt must preserve.

### Step 2: Declare the axis and the freeze set

The axis for SHOW-ME is camera position. Everything else is frozen.

### Step 3: Map PSGV for SHOW-ME

**PLAN**: Style, lighting, mood, identity, and freeze set declared before the brief. Camera position is the only thing that moves. State what is frozen explicitly so the model reasons about preservation before reframing.

**SEARCH**: SKIP. No live data needed for angle variations.

**GENERATE**: The angle brief. Names the new camera position precisely. Explicitly preserves all frozen elements.

**VERIFY**: Before showing output, verify the style has not shifted. Verify identity markers are intact. Verify lighting is consistent with physical repositioning, not a new stylistic choice. Verify no element changed that was not the camera angle.

### Step 4: Generate 7 angle variations

## Preamble format

```
Uploaded subject: [one-line summary].
Axis varied: camera angle and framing only.
Axes frozen: subject identity, wardrobe, pose integrity (where compatible with angle), style, lighting logic, mood, color palette.
Format: [JSON envelope / Natural language fallback].
SEARCH active: no.
```

## Prompt template: JSON envelope (default)

```json
{
  "plan": "Angle variation only. Visual DNA: subject identity, wardrobe, style, lighting logic, mood, color palette. Variation axis: camera position. Physical lighting shift (if any) must follow from the new angle, not introduce a new style.",
  "search": null,
  "subject": "Show the uploaded [subject identity, wardrobe, distinctive features] from [new angle name]. Subject identity locked.",
  "pose": "[Pose anchor adapted to be visible from the new angle without re-staging.]",
  "environment": "Preserve original environment.",
  "camera": "[Specific angle name: close-up, three-quarter front, profile, low angle, high angle, etc.]. [Framing distance.] [Lens character if relevant.]",
  "lighting": "Preserve original lighting source, direction, and quality. New angle reveals existing lighting from a different vantage, does not introduce new lighting style.",
  "mood": "Preserve original mood register.",
  "style": "Preserve original style exactly.",
  "palette": "Preserve original palette.",
  "quality": "Preserve original capture quality and material rendering.",
  "aspect_ratio": "[Match source unless angle requires reframing.]",
  "verify": [
    "camera position has changed",
    "subject identity, wardrobe, distinctive features intact",
    "style, lighting logic, mood, color palette preserved",
    "lighting shift (if any) follows from new angle physically, not stylistically"
  ],
  "negative_prompt": {
    "forbidden": [
      "wardrobe variation",
      "subject identity drift",
      "facial feature change",
      "body proportion change",
      "lighting style change (color, intensity, mood)",
      "color temperature shift",
      "environment redress",
      "style reinterpretation",
      "mood register shift",
      "palette substitution",
      "rendered medium change",
      "filter overlay applied to new angle",
      "era shift",
      "stylistic flourish introduced for the angle"
    ]
  }
}
```

## Prompt template: NL fallback (exploratory)

```
PLAN: Freeze set: [subject identity, wardrobe, style, lighting logic, color palette, mood]. New camera position: [angle name and description]. Physical lighting shift (if any) must follow from the new angle, not introduce a new style.
SEARCH: SKIP.
GENERATE: Show the uploaded [subject description] from [new angle or framing]. [Compositional specifics: what fills the frame, what's now revealed, how the subject is oriented]. Keep [identity markers: face, wardrobe, distinctive features] consistent. Match the original's style, lighting logic, color palette, and mood. [Optional: new spatial context the angle reveals].
VERIFY: Before showing output, verify the camera position has changed. Verify style, mood, wardrobe, and identity markers are intact. Verify no stylistic drift has occurred beyond what the new angle physically implies.
```

## Angle library

Draw from this library when generating. Combine freely. Do not repeat.

### Shot distance (frame size), tightest to widest

- Extreme close-up, a single feature fills the frame (eyes only, lips, hands, a detail of an object). Macro intimacy. Highlights texture and emotion.
- Close-up on face, shallow depth, eyes in focus
- Medium shot, chest to crown, environment softly present
- Full body shot, head to feet in frame, full outfit and posture readable, subject still dominant in the frame
- Wide shot, subject plus surrounding environment, subject and setting share the frame
- Extreme wide shot, subject small against a vast environment, scale and atmosphere dominate
- Wide establishing shot, subject small in frame, full environment revealed

### Cinematic coverage angles

- Over-the-shoulder from behind the subject
- Dutch angle, tilted 15 to 30 degrees
- Low angle looking up, heroic framing
- High angle looking down, observational framing
- Bird's eye directly above
- Worm's eye directly below
- Aerial / drone-style high wide, far elevated vantage looking down across a large area, subject and surroundings both small, epic scale. The still endpoint of a drone or crane move.

### Photographic perspectives

- Three-quarter front, subject turned 30 to 45 degrees
- Full profile, subject in strict side view
- Three-quarter back, subject turned away from camera
- Full back, subject facing away
- Symmetrical frontal, subject aligned with lens

### POV and immersive

- Point-of-view from subject's eyes looking out
- Over-the-shoulder from subject looking at another element
- Handheld tracking, subject moving through space
- Through-glass or through-frame, subject seen through a doorway or window

### Environmental framings

- Pull back to reveal the full setting
- Push in tighter on a detail (hands, face, object held)
- Reframe to include a secondary element previously off-camera
- Reflection shot, subject in a mirror, water, or glass

### Immersive formats

- 360° equirectangular panoramic seamless format. Research exemplar from @lupapixel. Emergent capability confirmed at launch. Use 2:1 aspect ratio.

### Character reference set

Four-panel character sheet as a single output: front, three-quarter, profile, back. Use when the user wants a full reference set in one image. This is also the still-frame way to capture an orbit: discrete positions around the subject instead of a continuous rotation.

## Camera movements are not still angles

A still image holds a camera *position*. It cannot hold a camera *movement*. When a user names a movement, decide what they actually want: a single frame at the start or end of that move (stays here, SHOW-ME), or the move itself across time (leaves here, route to `video-prompt-builder`).

Map each movement to its still analogue already in the library:

| Movement (video) | Still analogue (SHOW-ME holds this) |
|---|---|
| Dolly-in / push-in | Tighter framing, step down the shot-distance ladder (medium to close-up to extreme close-up) |
| Dolly-out / pull-back | Wider framing, step up the ladder (close-up to medium to wide to extreme wide) |
| Orbit / 360 | Four-panel turnaround (front, three-quarter, profile, back) |
| Crane | Endpoint angle: high angle, bird's eye, or aerial high-wide |
| Tracking | A single frame implying motion (handheld framing, subject mid-stride), not the follow itself |

If the user wants the actual motion (the dolly, the orbit, the crane sweep, the tracking follow), say so plainly and hand off: those belong to `video-prompt-builder`, which owns Seedance, Kling, Veo, Sora movement syntax. Do not fake a movement inside a still prompt. Offer the still endpoint here, and flag that the movement is a video job.

## Verbatim exemplar

From the research (@lupapixel, April 22 2026):

```
360 equirectangular panoramic image of a cozy mountain cabin in winter, photorealistic, 2:1 aspect ratio, seamless
```

This pattern generalizes to any subject. Adapt by replacing the setting and preserving the structural elements (equirectangular, photorealistic, aspect ratio, seamless).

## Escape hatches

If the user requests a change beyond camera position (e.g., "show me from different angles and also make it night"), surface the mode conflict and ask whether they want SHOW-ME (angles only) or EDIT (multiple axes varying).

If the uploaded subject lacks enough 3D information for wild angles (e.g., a flat graphic design or a head-on product shot with no volumetric context), flag this and narrow the angle set to the ones the model can plausibly reason about.

## Self-validation before output

- [ ] Upload description includes style, lighting, mood (freeze anchors)
- [ ] Preamble explicitly names camera angle as the only axis
- [ ] Preamble states format chosen and SEARCH as no
- [ ] Preamble lists style, lighting, mood, identity among frozen axes
- [ ] Exactly 7 prompts
- [ ] Each prompt in its own code block (JSON in ` ```json `, NL in plain ` ``` `)
- [ ] Each prompt encodes PSGV per format
- [ ] Each prompt's verification step checks style integrity, identity markers, and lighting consistency
- [ ] Each prompt names a distinct camera position
- [ ] No prompt introduces a style shift, mood shift, or era shift
- [ ] If a movement was requested, the still endpoint is offered and the movement is flagged for video-prompt-builder, not faked in a still
- [ ] If JSON: forbidden array includes wardrobe variation, style reinterpretation, lighting change, mood register shift
- [ ] No em-dashes

## Common errors to avoid

- Returning different styles when angles were requested
- Introducing new lighting moods per angle (lighting should follow from angle physically, not stylistically)
- Losing identity markers (wardrobe changes, facial drift)
- Using generic references ("the image") instead of the upload description
- Generating panels that look like a filter pass rather than a spatial repositioning
- Treating a camera movement (dolly, orbit, crane, tracking) as a still angle instead of offering the still endpoint and flagging the move as a video job
