# System Prompt Operating Contract Template (Batch Generation)

The highest reliability rung. ONE structured prompt that produces up to 8 coordinated outputs from a single submission. Shared visual DNA at the top. Per-image specifications inline within `<images>`. Cross-batch verify at the bottom.

## When to use this format

Read `format-ladder.md` for full escalation logic. Quick triggers:

- Batch volume of 4+ images sharing one constraint regime.
- SERIES with character continuity, product family, or style sheet.
- NARRATIVE with character bible across panels.
- MULTI-OUTPUT with visual DNA backbone across distinct deliverable types.
- "Across all of these," "every image in this set," "consistent throughout."
- User explicitly requests system-prompt format or operating contract.

## Why XML blocks

GPT Image 2 is a reasoning model. Structured XML blocks read as named instructions. Each block carries a defined role. The model parses and applies them in priority order, running PSGV once across the entire batch and returning all N outputs as a coordinated set.

This is consistent with the pattern in `gpt-5-4-production-prompter`. The two skills speak the same dialect.

## How the model runs this prompt

The user submits ONE prompt. The model reads the entire structure, plans the batch, and returns up to 8 coordinated outputs from that single submission. There is no session, no sequential per-image briefing, no paste-once preamble. One prompt in, the entire batch out.

## Canonical structure

```
Generate [N] separate [aspect ratio] images as a coordinated [task type]. All [N] share one visual DNA. [What varies across the batch]. [What holds across the batch].

<reference>
[OPTIONAL block. Include only when reference images are uploaded with the brief. State what aesthetic cues to pull. State what NOT to pull. Include negative usage constraints when the subject of the reference is NOT the subject of the outputs.]
</reference>

<visual_dna>
[What persists across every output. Style, palette, lighting philosophy, subject anchor, typographic treatment, surface vocabulary. State aspect ratio here as one DNA element among others.]
</visual_dna>

<global_forbidden>
[Category-level exclusions that apply to ALL outputs. Same construction rules as the JSON envelope's forbidden array. Cluster by category.]
</global_forbidden>

<images>
<image_1 subject="[brief subject label]">
[Full spec for image 1: composition, framing, subject specifics, per-image variations from the shared DNA.]
</image_1>
<image_2 subject="[brief subject label]">
[Full spec for image 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
[Cross-image consistency checks. What must hold identically across the batch. What must vary distinctly.]
</verify>
```

## PSGV inside the batch prompt

PSGV runs ONCE across the entire batch, not once per image. The four stages re-encode through the structure, never disappear.

| Stage | Where it lives in the batch prompt |
|---|---|
| PLAN | Top-line declaration + `<visual_dna>` block. The model plans the batch shape before generating any pixels. |
| SEARCH | Optional `<search>` block, positioned before `<visual_dna>` when active. SKIP otherwise. |
| GENERATE | `<visual_dna>` + `<images>` together. Visual DNA filters every per-image spec. The model renders all N outputs as one coordinated act. |
| VERIFY | `<verify>` block + `<global_forbidden>` block. Verify is the positive half (what must hold). Global forbidden is the negative half (what must not appear). Together they enforce the cross-batch coherence check before output. |

The model reads the entire prompt once, plans the batch, and generates all N outputs as a coordinated set.

## What is NOT in this template

The following blocks were removed because they were borrowed from chat-system-prompt convention and do not apply to image batch prompts:

- `<role>`: image batch prompts do not declare a chat role. The task is named in the top-line declaration.
- `<psgv_loop>`: PSGV is not a per-image loop. It runs once over the batch.
- `<constraints>`: replaced by `<visual_dna>` (positive constraints) and `<global_forbidden>` (negative constraints). These two blocks together cover the constraint surface.
- `<output_format>`: not needed. The number of images, the aspect ratio, and the verification statement are all encoded in the top-line + `<visual_dna>` + `<verify>`.
- `<conflict_resolution>`: not needed. Single-submission batches have no per-image briefs to conflict with the top-level constraints. The top-line declaration is the single source of truth.

## Three variants

### Variant A: SERIES (consistent multi-output along one axis)

```
Generate [N] separate [aspect ratio] images as a coordinated wardrobe variation series. All [N] share one visual DNA. Wardrobe varies across the batch. Identity, environment, lighting, framing hold.

<visual_dna>
Subject anchor: [exact character identity: face, hair, body type, skin tone, key physical markers].
Visual world: [environment, palette, treatment, mood register].
Pose anchor: [pose held across the set].
Lighting: [source, direction, quality, color temperature].
Style: [photographic standard or rendered medium].
Aspect ratio: [W:H] for every image.
</visual_dna>

<global_forbidden>
- subject identity drift across images
- facial feature change between images
- body proportion change
- hair color or length variation
- environment redress between images
- lighting source or color temperature shift
- style reinterpretation between images
- mood register shift
- aspect ratio variation
</global_forbidden>

<images>
<image_1 subject="[wardrobe variant 1 label]">
[Subject in [wardrobe 1: top, bottom, footwear, accessories]. Same pose anchor. Same environment. Same lighting.]
</image_1>
<image_2 subject="[wardrobe variant 2 label]">
[Spec for variant 2.]
</image_2>
[continue through image_N within the 8-output ceiling]
</images>

<verify>
Before showing output, confirm for ALL [N] images:
- Subject identity matches across every output
- Pose anchor held across every output
- Environment and lighting identical across every output
- Each image shows a distinct wardrobe with no repeats
- Aspect ratio [W:H] held across every output
</verify>
```

### Variant B: NARRATIVE (character bible across panels)

```
Generate [N] separate [aspect ratio] panels as a coordinated sequential narrative. All [N] share one visual DNA. Story beat varies across the panels. Character identities, art tradition, line work, palette hold.

<visual_dna>
Protagonist: [exact identity: name, age, hair, signature feature, wardrobe].
Supporting characters: [each with locked features].
Art tradition: [Seinen / Shonen / Shojo / specific tradition].
Visual style: [line work treatment, ink contrast, screentone usage, color treatment if any].
Visual world: [setting, era, palette logic, mood register].
Aspect ratio: [W:H] for every panel.
</visual_dna>

<global_forbidden>
- protagonist feature drift between panels
- supporting character feature drift
- art tradition shift between panels
- ink treatment or screentone style change
- color treatment shift
- panel-to-panel quality variance
- story beat repetition across panels
- dialogue paraphrasing
</global_forbidden>

<images>
<image_1 subject="[story beat 1 label]">
[Which characters appear, the action, the panel composition, dialogue in quotes if any.]
</image_1>
[continue through image_N]
</images>

<verify>
Before showing output, confirm for ALL [N] panels:
- Character identities consistent across every panel
- Visual style and ink treatment consistent
- Each panel renders a distinct story beat
- Dialogue spelled correctly where present
- Aspect ratio [W:H] held across every panel
</verify>
```

### Variant C: MULTI-OUTPUT (visual DNA backbone across distinct deliverables)

```
Generate [N] separate images as a coordinated multi-page system. All [N] share one visual DNA backbone. Each image is a distinct page type. Visual DNA, palette, treatment, mood hold.

<visual_dna>
Subject: [name and type: brand, event, product, character, IP].
Description: [what it is, what it stands for. 1 to 3 sentences.]
Key text: [exact name, tagline, or line that must appear verbatim in relevant pages].
Palette: [primary color, accent color, secondary tones, named].
Treatments: [textures, grain, glitch, compositional devices].
Subject matter: [imagery vocabulary that lives in this world].
Mood: [2 to 4 descriptors].
Aspect ratio defaults: [per page type, listed below].
</visual_dna>

<global_forbidden>
- palette drift across pages
- treatment loss between pages
- text spelling errors on key text
- page-type bleed (one page looking like another)
- system incoherence (pages that read like different brands)
- generic stock-image substitutes for brand-specific imagery
</global_forbidden>

<images>
<image_1 subject="[page type 1, e.g. brand identity sheet]">
[Page type, layout logic, exact text in quotes, aspect ratio for this page type, specific visual elements.]
</image_1>
<image_2 subject="[page type 2, e.g. campaign keyvisual]">
[Spec for page 2.]
</image_2>
[continue through image_N for each distinct page type]
</images>

<verify>
Before showing output, confirm for ALL [N] pages:
- Visual DNA palette and treatment present on every page
- Exact text rendered verbatim on each page where it appears
- Each page is a distinct deliverable type with no duplicates
- Aspect ratio matches the page type defaults stated in the visual DNA
- The set reads as one coherent system, not seven different brands
</verify>
```

## Output rules

- The whole batch prompt sits in one triple-backtick code block (plain, no language tag).
- Top-line declaration always present. It states image count, aspect ratio, task type, what varies, what holds.
- `<visual_dna>` always present. Aspect ratio is one of the DNA elements, not a separate structural constant.
- `<global_forbidden>` sized to the batch's drift surface. Same length guidance as the JSON envelope (25-35 items typical, less for tightly scoped batches).
- `<images>` always present with one numbered child per output. Subject attribute on each child gives the per-image label.
- `<verify>` always present. Cross-batch checks, not per-image self-checks.
- `<reference>` only when references are uploaded with the brief.
- `<search>` only when current data is required, positioned before `<visual_dna>`.
- No em-dashes anywhere inside the prompt.

## Aspect ratio handling

Aspect ratio is a parameter chosen for the batch, not a default for all batch work. State it once in the top-line declaration and once inside `<visual_dna>`. Skeleton templates use `[aspect ratio]` as a placeholder. Worked examples pick a specific ratio that matches the example's use case (4:5 for brand campaigns, 1:1 for social grids, 16:9 for storyboards), framed as choices for that example, not a constant.

## Sanity check protocol

Before submitting a batch prompt:

1. **Inventory check**: count of `<image_N>` children matches the N stated in the top line. Mismatch poisons the batch.
2. **DNA scope check**: are the `<visual_dna>` items genuinely shared across every image in `<images>`? If a constraint applies to only some images, move it into the per-image specs, not the DNA block.
3. **Forbidden audit**: are forbidden items category-level, not keyword-level? Length within 25-35? Aligned to the actual drift risks of this batch?
4. **Verify alignment**: does `<verify>` cover both the cross-batch consistency (DNA) and the per-image distinctness (variation axis)?

A bad batch prompt poisons every output. The setup cost matters because the failure cost matters.

## Failure modes specific to batch prompt format

See `failure-modes.md` for the full list. Quick reference:

- **Image inventory length mismatch**: the top-line says 8 but `<images>` contains 6 children, or vice versa. Fix by counting before submission.
- **DNA scope creep**: items that vary per image accidentally placed inside `<visual_dna>`. The model treats them as locked and the batch flattens. Fix by moving variation into the per-image specs.
- **Per-image specs too thin**: each image gets only a one-word label and the model fills in generic content. Fix by giving each image enough specificity to be distinct.
- **Drift past 8 outputs**: the 8-output ceiling is the model's hard limit. For a batch larger than 8, submit a fresh prompt with the same `<visual_dna>` and `<global_forbidden>` blocks, and a new `<images>` set for outputs 9 through 16. Consistency across separate submissions is probabilistic, not deterministic.
- **Aspect ratio drift between top-line and visual_dna**: the model trusts the most local declaration. State the ratio identically in both places. If they differ, fix before submission.
