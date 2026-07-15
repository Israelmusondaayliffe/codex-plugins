# Agent: MULTI-OUTPUT

Multi-page system briefs. One visual DNA. Multiple distinct deliverable types generated as a coherent set.

**Inheritance**: Extended from EDITORIAL's brand system capability and SERIES' consistency enforcement. MULTI-OUTPUT is the mode when the request is not "7 variations of one thing" (SERIES) and not "one layout" (EDITORIAL), but "7 different page types that must feel like one system."

---

## Scope

MULTI-OUTPUT is for briefs where:
- The user wants multiple DISTINCT deliverable types (identity sheet, color page, manifesto poster, campaign keyvisual, social assets, guidelines, not 7 versions of one poster)
- All outputs must share a visual DNA backbone
- The subject is a brand, product, event, IP, character, or world with an established or referenced aesthetic

**Do not use MULTI-OUTPUT for:**
- 7 variations of the same poster or image (route to SERIES)
- One layout with multiple design tradition options (route to EDITORIAL)
- A storyboard or sequential panels (route to NARRATIVE)
- A structured diagram or chart set (route to INFOGRAPHIC)

**Common MULTI-OUTPUT requests:**
- Brand kit / brand system
- Style guide pages
- Product family system
- Pitch deck pages (each slide as a distinct image)
- Event identity package (poster, ticket, social, signage)
- Character or IP design bible
- Editorial magazine issue (cover, spread, table of contents)

---

## Format escalation

**Default for MULTI-OUTPUT: system prompt operating contract.** The visual DNA backbone is exactly what one batch prompt encodes. One submission returns the entire page set under one shared constraint regime.

The previous workaround (restate visual DNA in every PLAN of every NL prompt) was a workaround for not having a single batch prompt. With a system prompt batch, the visual DNA lives in `<visual_dna>` once at the top, applies to every per-image spec inside `<images>`, and the model returns the entire page set from one submission.

Auto-detection rules:

- **System prompt format (default)**: any MULTI-OUTPUT request with a defined visual DNA and 4+ page inventory. Produces 1 batch prompt that returns the entire page set from a single submission, with each page specified inline in `<images>`.
- **JSON envelope format**: when the user wants individual self-contained prompts that each carry the full visual DNA, useful when pages will be generated in separate runs.
- **NL format (fallback)**: exploratory MULTI-OUTPUT requests, "give me 7 different page concepts for a brand," casual tone with no commitment to system architecture.

State the format chosen in the preamble. Read `references/system-prompt-template.md` Variant C for MULTI-OUTPUT-specific framing.

---

## Template

This is the reusable structure. Extract values from the user's request and fill every block before generating any prompts.

```
MULTI-OUTPUT SYSTEM BRIEF

[SUBJECT & CONTEXT]
Subject: [Name and type: brand, product, event, IP, character]
Description: [What it is, what it does, what it stands for. 1-3 sentences.]
Key text: [Exact name, tagline, or line that must appear verbatim in relevant pages]

[VISUAL DNA]
Reference: [Attached images described / or stated visual world if no uploads]
Palette: [Primary color, accent color, secondary tones, name each]
Treatments: [Textures, grain, glitch, compositional devices, be specific]
Subject matter: [What imagery lives in this world: botanical, architectural, portrait, product, etc.]
Mood: [2-4 descriptors]

[PAGE INVENTORY]
Deliver each of the following as a separate image:
1. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
2. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
3. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
4. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
5. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
6. [Page type]: [specific content: exact text in quotes, key elements, layout intent]
7. [Page type]: [specific content: exact text in quotes, key elements, layout intent]

[CONSISTENCY BACKBONE]
Visual DNA held across all pages: [which elements must appear in every image]
Color rules: [which colors are permitted and their roles]
Background default: [base surface across all pages]
Treatment rule: [which texture or effect is mandatory on every page]

[VERIFY]
Verify all text is correctly spelled before output.
Verify [key name or text] appears correctly in every page that includes it.
Verify visual DNA is consistent across all pages before output.
```

---

## Common Page Inventories

Use these as starting inventories. Customize per the subject's needs. The user does not need to specify all 7. If the request is open-ended, propose from the relevant inventory and confirm.

### Brand Kit (default)
1. Brand identity system sheet (wordmark, symbol mark, palette swatches, application mockup)
2. Brand manifesto or cover poster (typographic, key tagline)
3. Color palette editorial page (colors shown in context with imagery)
4. Typography specimen sheet (display and body at multiple sizes)
5. Campaign keyvisual (hero image with wordmark)
6. Social media asset system (profile, cover, story format mockup sheet)
7. Brand guidelines overview (mark usage, voice, color rules, correct application)

### Event Identity Package
1. Main event poster
2. Ticket or wristband design
3. Social media announcement card
4. Event program cover
5. Venue signage keyvisual
6. Sponsor block / credits page
7. Post-event recap cover

### Product Family
1. Product hero shot (primary product, full bleed)
2. Color family sheet (product shown in all available colors)
3. Product detail callout page (key features labeled)
4. Lifestyle context image (product in use)
5. Packaging flat lay
6. Comparison or size guide sheet
7. Campaign keyvisual with product + headline

### Character or IP Design Bible
1. Character portrait sheet (front, 3/4, profile)
2. Expression sheet (6-8 core emotions)
3. Costume or outfit variations
4. Scale reference sheet (character vs environment)
5. Color and material palette for the character
6. Action or pose study sheet
7. World / environment keyvisual

### Editorial Issue Package
1. Magazine cover
2. Feature spread opening page
3. Photo essay full-bleed image
4. Pull quote / typographic spread
5. Secondary article layout
6. Table of contents page
7. Back cover

---

## Workflow

### Step 0: Run deconstruction first when starting from a reference image

If the user uploads a reference image and wants the vibe extracted and applied to a brand, run the deconstruction pattern from `references/reference-deconstruction.md` before this workflow. It produces a 4:3 brand board capturing seven systems (core idea and tension, color and material language, typography direction, image and composition logic, signature visual device, layout and grid, multi-format applications). The brand board then feeds the visual DNA backbone for this multi-page system.

Skip Step 0 when the user has already supplied a written brand spec or visual DNA in any form.

### Step 1: Parse the request

Identify the subject, any uploaded references, and whether the user specified page types or left them open. If the user gave a subject but no page inventory, propose from the common inventories above, confirm before generating.

### Step 2: Fill the template

Extract all values. Every block must be filled before any prompt is written. The VISUAL DNA block is the most important. If references are uploaded, describe what is visible (palette, texture, mood, subject matter) before proceeding.

### Step 3: Detect variation axis

In MULTI-OUTPUT, the axis is page type. It does not vary. What varies across the 7 prompts is the deliverable. What stays frozen is the visual DNA (palette, treatment, mood, subject vocabulary).

### Step 4: Map PSGV for MULTI-OUTPUT

**PLAN**: State the page type and its specific deliverables first. Reference the visual DNA backbone. Define the layout logic for this specific page type (identity sheet needs different compositional reasoning than a manifesto poster).

**SEARCH**: SKIP for most multi-output work. Active only when a page must contain current verified data (current pricing, live event schedule, current stats for a pitch deck slide).

**GENERATE**: The creative brief for this specific page. All exact text in quotes. Visual DNA applied. Layout approach named. Aspect ratio specified. Reference how this page connects to the system as a whole.

**VERIFY**: Exact text present and spelled correctly. Visual DNA consistent with the system (not just internally coherent, consistent with the other pages in the set). Aspect ratio matches brief.

### Step 5: Write 7 prompts, one per page

Each prompt is one page from the inventory. Each must reference the shared visual DNA backbone so the model reasons about system coherence before rendering.

---

## PSGV Template per Prompt (system prompt format, default)

The default delivery is one batch prompt that contains the shared visual DNA at the top and per-page specifications inline. The user submits it once and the model returns up to 8 coordinated pages from that single submission.

### System prompt (single batch submission)

```
Generate [N up to 8] separate images as a coordinated multi-page system for [SUBJECT NAME, type]. All [N] share one visual DNA backbone. Each image is a distinct page type. Visual DNA, palette, treatment, mood hold across the set.

<visual_dna>
Subject: [name and type: brand, event, product, character, IP].
Description: [what it is, what it stands for. 1 to 3 sentences.]
Key text: [exact name, tagline, or line that must appear verbatim in relevant pages].
Palette: [primary color, accent color, secondary tones, named].
Treatments: [textures, grain, glitch, compositional devices].
Subject matter: [imagery vocabulary that lives in this world].
Mood: [2 to 4 descriptors].
Aspect ratio defaults: [per page type, listed by page].
</visual_dna>

<global_forbidden>
- palette drift across pages
- treatment loss between pages
- text spelling errors on key text
- page-type bleed (one page looking like another)
- system incoherence (pages that read like different brands)
- generic stock-image substitutes for brand-specific imagery
- legible text in placeholder language not requested
- [SUBJECT NAME] misspelled
</global_forbidden>

<images>
<image_1 subject="[page type 1, e.g. brand identity sheet]">
[Page type, layout logic, exact text in quotes, aspect ratio for this page type, specific visual elements.]
</image_1>
<image_2 subject="[page type 2, e.g. campaign keyvisual]">
[Spec for page 2.]
</image_2>
<image_3 subject="[page type 3]">
[Spec for page 3.]
</image_3>
<image_4 subject="[page type 4]">
[Spec for page 4.]
</image_4>
<image_5 subject="[page type 5]">
[Spec for page 5.]
</image_5>
<image_6 subject="[page type 6]">
[Spec for page 6.]
</image_6>
<image_7 subject="[page type 7]">
[Spec for page 7.]
</image_7>
</images>

<verify>
Before showing output, confirm for ALL [N] pages:
- Visual DNA palette and treatment present on every page
- Exact text rendered verbatim on each page where it appears
- Each page is a distinct deliverable type with no duplicates
- Aspect ratio matches the page type defaults stated in the visual DNA
- The set reads as one coherent system, not seven different brands
- [SUBJECT NAME] spelled correctly throughout
</verify>
```

This is a structural shift from any earlier NL-only approach. The visual DNA lives at the top of one batch prompt. The per-page specs sit inside `<images>`. The whole prompt is submitted once and the model returns the full page set in a single coordinated batch.

---

## PSGV Template per Prompt (NL fallback, when system prompt is overkill)

When the user wants standalone NL prompts (each carrying the full visual DNA in itself, useful when pages will be generated separately), use this format. Each prompt is one page, restating the visual DNA backbone.

```
PLAN: [Page type] for [subject name]. Visual DNA backbone: [palette names], [treatment names], [mood]. Specific deliverables for this page: [elements]. Layout logic: [compositional approach]. Aspect ratio: [ratio].
SEARCH: SKIP. [Or: Search the web, today is [date]: [specific data needed].]
GENERATE: [The full creative brief for this page. Exact text in quotes. Visual DNA applied. Layout described. All key elements named. Connection to the broader system noted where relevant.]
VERIFY: Before showing output, verify [exact text] is spelled correctly. Verify [treatment] is present as specified. Verify this page shares palette and texture with the system DNA. Verify aspect ratio is [ratio].
```

---

## Preamble format

```
Mode: MULTI-OUTPUT.
Subject: [name and type].
Page inventory: [list the 7 page types, numbered].
Axis varied: page type (each prompt is a different deliverable).
Axes frozen: visual DNA (palette, treatments, mood, subject vocabulary, held across all 7 pages).
Format: [System prompt operating contract / NL fallback].
SEARCH active: [yes + which pages] OR [no].
```

---

## Output contract

Identical to the base skill output contract:

1. Preamble (mode, subject, page inventory, axis, frozen axes, search status).
2. Exactly 7 prompts.
3. Every prompt in its own triple-backtick code block.
4. Natural language, not keyword stacks.
5. No em-dashes. Periods or commas.
6. Every prompt structured: PLAN, SEARCH (or SKIP), GENERATE, VERIFY.
7. Each prompt is a distinct page type from the inventory.

---

## Consistency enforcement

The most common failure in MULTI-OUTPUT: pages that look like they came from different brands.

**With system prompt format (default)**: visual DNA lives in the `<visual_dna>` block at the top of the batch prompt. Every per-image spec inside `<images>` inherits that DNA. The model holds the system across all N outputs from one submission. No restating per page needed.

**With NL fallback format**: visual DNA must be restated in the PLAN of every prompt. Short restatement, not full re-description. Example:

```
PLAN: Typography specimen page for "BRAND NAME". Visual DNA backbone: slate navy background, hot coral red accent, halftone grain overlay, analog-digital editorial mood. Specific deliverables: ...
```

The system prompt format is structurally better at this. The NL format works when system prompt overhead is wrong for the request.

---

## Aspect ratio defaults by page type

| Page type | Default ratio |
|---|---|
| Identity system sheet | 3:4 |
| Manifesto / cover poster | 2:3 |
| Color palette page | 3:4 |
| Typography specimen | 3:4 |
| Campaign keyvisual | 2:3 |
| Social asset system mockup sheet | 16:9 |
| Guidelines overview | 3:4 |
| Event poster | 2:3 |
| Magazine cover | 3:4 |
| Magazine spread | 3:2 landscape |
| Product hero | 1:1 or 4:5 |
| Character sheet | 3:4 |

---

## Flag: logo mark fidelity

GPT Image 2 generates wordmarks and symbol marks, but exact letter-perfect fidelity across multiple generations is not guaranteed. Flag this when the brief requires strict mark consistency. Recommend: run identity system sheet first, approve the mark, then reference it explicitly in subsequent page prompts. For production delivery, final typography should be set manually using the rendered layout as a base.

---

## Self-validation before output

- [ ] Template fully filled before any prompt was written
- [ ] Preamble states mode, subject, all 7 page types, axis, frozen axes, format chosen, search status
- [ ] Format chosen matches request signals (system prompt for visual DNA backbone, NL fallback when overkill)
- [ ] If system prompt format: 1 batch prompt with shared visual_dna and N per-image specs in `<images>`
- [ ] If NL fallback format: 7 standalone prompts each restating visual DNA in PLAN
- [ ] Each prompt in its own code block
- [ ] Each prompt is a distinct page type
- [ ] Each prompt encodes PSGV per format (XML blocks for system prompt, labels for NL)
- [ ] All exact text is in quotes throughout
- [ ] Aspect ratio specified in every prompt
- [ ] Verification step checks text spelling, visual DNA consistency, and aspect ratio
- [ ] No em-dashes anywhere
