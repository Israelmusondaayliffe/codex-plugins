---
name: video-prompt-builder
description: "Build cinematic, shot-by-shot video prompts with full effects breakdowns. Four modes. BUILD: creative brief to shot-by-shot prompts with effects timeline, inventory, density map, energy arc. ANIMATE: image-to-video, keyframe interpolation (start+end frame), Seedance 2.0 native multi-image multi-shot prompts (@imageN syntax for up to 9 images in one prompt), and role-based multi-reference composition (subject/style/environment). DECONSTRUCT: reverse-engineer a described video into structured effects format. REMIX: transplant effects architecture onto a new subject or brand. Each shot prompt output in its own code block. Optimized for Seedance 2.0, Kling 3, Veo 3, Sora 2. Triggers on video prompt, shot list, effects breakdown, brand film, ad prompt, animate this, image to video, keyframe, multi-image seedance, @image prompt, deconstruct video, remix video, or any visual concept needing generation-ready video prompts."
---

# Video Prompt Builder

Build cinematic, shot-by-shot video prompts from creative briefs, uploaded reference images, deconstructed references, or remixed architectures. Every output follows a structured effects breakdown format designed to give AI video generators maximum detail on camera work, effects, transitions, pacing, and energy arc.

Model-agnostic. Optimized for Seedance 2.0, Kling 3, Veo 3, Sora 2.

## Output Mandate

**Every shot prompt always in its own triple-backtick code block.** Non-negotiable.

Supporting sections (effects inventory, density map, energy arc) are presented as structured text outside code blocks. They frame the full picture. The code-blocked shot prompts are the deliverable.

## Tone

Direct, technical. Director's shot notes, not a marketing brief. No hype language, no "stunning" or "breathtaking." Describe what happens and let the visuals speak.

Replace every em-dash with a period (new sentence) or comma (continue thought).

---

## Router Logic

Assess the user's request and route to the appropriate agent.

### BUILD mode → Load `agents/agent-build.md`

**Triggers**: User provides a creative brief, concept, idea, or description and wants video prompts generated from it. No uploaded images, no existing breakdown to work from. Pure text-to-video.

Examples:
- "Write me a video prompt for a trail running shoe ad"
- "I need a 15-second brand film concept for a coffee brand"
- "Shot list for a dramatic product reveal"
- "Seedance prompt for a dancer in an empty warehouse"
- "Plan a video sequence for this concept"

### ANIMATE mode → Load `agents/agent-animate.md`

**Triggers**: User uploads one or more images alongside a video generation request. Four sub-modes detected by the agent based on input type.

**Image-to-Video**: One image uploaded + motion intent.
**Keyframe**: Two images uploaded as start and end states.
**Multi-Image Shot Prompt (Seedance 2.0 native)**: 3-9 images uploaded. Each image becomes a moment or element in a single multi-shot prompt using `@imageN` syntax. This is Seedance 2.0's native workflow. One prompt, full 15-second sequence.
**Role-Based Multi-Reference (model-agnostic)**: 2+ images with assigned roles (subject, style, environment). For Kling, Veo, Sora.
**Video Continuation (@video1)**: No new upload. User wants to extend or chain a previous Seedance generation using the `@video1` reference tag.

Examples:
- "Animate this image" (single upload)
- "Make this move" (single upload)
- "Transition from this to this" (two uploads, keyframe)
- "Seedance prompt from these 6 images" (multi-upload, native syntax)
- "Use these as shots for one video" (multi-upload, native syntax)
- "Use this as the subject and this as the style reference" (role-based)
- "Bring this to life with a slow push-in"

The agent loads prompt templates from `assets/animate-templates.md`.

### DECONSTRUCT mode → Load `agents/agent-deconstruct.md`

**Triggers**: User wants to analyze, reverse-engineer, or break down an existing video into the effects breakdown format. The input is a description of something that already exists, not a brief for something new.

Examples:
- "Deconstruct the Apple Watch ad"
- "Break down this video into shots and effects"
- "Analyze the effects in this Nike commercial"
- "What's the shot structure of this reference?"
- "Reverse-engineer this video's editing style"

### REMIX mode → Load `agents/agent-remix.md`

**Triggers**: User has (or wants to use) an existing effects breakdown and wants to apply that structure to a new subject, brand, or concept. Requires both a source structure and a new context.

Examples:
- "Take the Hoka breakdown and apply it to a skateboarding brand"
- "Use that effects structure but for a perfume ad"
- "Remix the deconstruction we just did for a tech product"
- "Same energy arc but for a completely different subject"

### Ambiguous Requests

If the request could fit multiple modes, use this priority:
1. If user uploads image(s) with video intent → ANIMATE
2. If user references an existing video to analyze → DECONSTRUCT
3. If user has an existing breakdown AND a new context → REMIX
4. If user provides a concept, brief, or idea with no images → BUILD
5. If unclear, ask: "Are you building from a concept, animating reference images, deconstructing a reference, or remixing an existing structure?"

---

## Shared Resources

All agents reference:
- `references/effects-breakdown-reference.md`. The Hoka athletic brand film example. Gold standard for detail level and structure.
- `references/effects-vocabulary.md`. Named effects catalog with precise descriptions.
- `references/creative-principles.md`. Five creative principles, duration calibration, anti-patterns.
- `references/ai-video-failure-modes.md`. What AI video generators struggle with and how to write around it.
- `references/style-families.md`. Six style families (cinematic narrative, action/VFX, product/commercial, character portrait, environment/landscape, UGC/meme) with signature language patterns.
- `references/consistency-constraints.md`. Character, physics, anatomy, and quality constraint language for reliable output.

BUILD agent also references:
- `assets/build-templates.md`. Five text-to-video template scaffolds (T1 Cinematic Narrative, T2 Product, T3 Portrait, T4 Landscape, T5 Action/VFX).

ANIMATE agent also references:
- `assets/animate-templates.md`. Image-to-video, keyframe, Seedance 2.0 native multi-image (@imageN), @video1 motion reference, @Audio1 beat sync, continue-video extension pattern, optional JSON variant, and role-based multi-reference templates.

---

## Phase Handoff Protocol

Modes can chain. Typical multi-turn flows:

**Analysis → Production:** DECONSTRUCT a reference → REMIX that deconstruction for a new brand → refine with BUILD.

**Image → Sequence:** ANIMATE a single reference image (short clip) → BUILD a full multi-shot sequence around the same concept.

**Full pipeline:** DECONSTRUCT reference → REMIX for new context → ANIMATE with reference images for key shots.

Between modes, verify:
- Previous mode output exists in the conversation
- User has confirmed or approved the previous output (or explicitly moved on)
- Required inputs for the next mode are available

If a user jumps modes without completing the previous one, note what is missing and ask if they want to continue the previous mode or proceed with incomplete inputs.

---

## Failure Recovery

**User uploads images with unclear intent**: If the user uploads images alongside a video request, route to ANIMATE. If they upload images but seem to want image prompts (not video), route to the appropriate image skill instead.

**User asks for a single monolithic prompt instead of shot-by-shot**: Explain that shot-by-shot prompts give the generator more control and produce better results. Offer to consolidate the shot list into a single narrative prompt as a secondary output if they insist, but recommend the shot-by-shot approach.

**User provides an extremely long or complex brief**: Break it into segments. Build one segment at a time. Confirm each before proceeding.

**User expects Claude to watch a video**: Claude cannot process video input. Route to DECONSTRUCT and ask the user to describe the video in text. The more specific their description (shot count, effects, timing), the better the deconstruction.
