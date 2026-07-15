# Agent: TYPOGRAPHY

Text-heavy prompts, dense typographic layouts, multilingual and non-Latin scripts. Uses GPT Image 2's headline capability: significant gains in Japanese, Korean, Chinese, Hindi, Bengali, and Latin script rendering at any density.

**Inheritance**: NEW with partial ADAPT. Took structural scaffolding from `nano-banana-unified/agents/agent-create.md` (Typography Art sub-template). Replaced the body with GPT Image 2 multilingual exemplars. The research is explicit: GPT Image 2 treats images-with-words as a central workload and renders dense text at roughly 99% accuracy vs 90 to 95% for GPT Image 1.5 (Handy AI estimate, cross-referenced with VentureBeat map demo).

## Scope

TYPOGRAPHY is for requests where the text itself is the primary subject or at least the primary design element:

- Non-Latin or multilingual posters, signage, packaging
- Dense typographic layouts (magazine spreads with real-looking body copy)
- Display typography where the typeface choice is central
- Hand-lettering, calligraphy, graffiti
- Text-as-image (a word rendered as its meaning)
- Brand wordmarks and logotypes (flag fidelity risk)
- Menu and sign rendering (restaurant signs, airport displays, shopfronts)

For adjacent workflows, route back:
- Poster where text is secondary to image → EDITORIAL
- Infographic where text labels data → INFOGRAPHIC
- Sequential art with dialogue → NARRATIVE
- Multilingual diagram → INFOGRAPHIC

## Known strengths (high confidence)

- Japanese, Korean, Chinese, Hindi, Bengali dense text with minimal garbling
- Latin typography at magazine density with legible body copy
- Mixed-script layouts (Latin + non-Latin in the same composition)
- Specific typeface feel (Bauhaus geometric, French New Wave vernacular, Korean editorial)
- Calligraphy and brush-stroke authenticity per script

## Known weaknesses (flag)

- Brand logo mark reproduction drifts; iteration often needed
- Very small text in overcrowded layouts may become illegible
- Invented words or nonsense text may still appear in the densest layouts

## Format escalation

**Default for TYPOGRAPHY: JSON envelope** when non-Latin scripts are involved or when text legibility is mission-critical. The forbidden array refuses character corruption, latin substitution, and invented glyphs at the category level. Latin-only display work can run on NL.

Auto-detection rules:

- **JSON envelope format (default)**: any TYPOGRAPHY request involving non-Latin scripts (Japanese, Korean, Chinese, Hindi, Bengali, Arabic, Cyrillic, Hebrew, Thai), brand wordmark fidelity, dense editorial layouts where misspelling is a failure, multilingual mixed-script work.
- **System prompt format**: when the user runs multiple typographic outputs across the same brand voice in one session (e.g., 8 social posts using one brand typeface system).
- **NL format (fallback)**: Latin-only display typography, casual text-as-image work, exploratory typeface voice exploration.

State the format chosen in the preamble.

## Workflow

### Step 1: Declare the text content exactly

Every TYPOGRAPHY prompt must name the exact text to render, in quotation marks. Guessing or paraphrasing produces garbled output.

```
EXACT TEXT: [word or phrase or copy block, quoted]
SCRIPT(S): [Latin, Japanese, Korean, Chinese, Hindi, Bengali, mixed]
```

### Step 2: Detect the variation axis

Common TYPOGRAPHY axes:

- Typeface or font voice (7 typographic treatments of the same text)
- Layout or hierarchy (7 compositional arrangements)
- Script (7 language versions of the same message; each prompt a different script)
- Scale relationship (text dominates vs text as accent across 7 outputs)
- Color palette (7 palettes on identical typography)
- Medium or context (letterpress, screen print, neon sign, carved stone, embroidery, handwriting)
- Era or style movement (Bauhaus, Swiss International, Memphis, Y2K, vernacular)

If ambiguous, ask.

### Step 3: Map PSGV for TYPOGRAPHY

**PLAN**: Text hierarchy first. What text must be legible vs decorative. Which script conventions govern the layout. State this before the brief so the model reasons about rendering accuracy before generating.

**SEARCH**: SKIP for most typography work. Active when text content must be factually accurate (real menu items, real event names, real legal text, current brand copy that may have changed).

**GENERATE**: The typographic brief. Exact text in quotes, script, style tradition, layout, medium.

**VERIFY**: Before showing output, verify all text strings are spelled correctly in the correct script. Verify the stated typographic convention has been applied (vertical flow for Japanese, correct stroke character for each script). Verify legibility hierarchy: primary text reads first.

### Step 4: Generate 7 prompts

Each in its own code block. Each names the exact text in quotes.

## Preamble format

```
Exact text: "[quoted text]"
Script(s): [list]
Axis varied: [e.g., typographic treatment, from Bauhaus to Memphis to Swiss International to Art Deco to Y2K to Pixel to Handwritten]
Axes frozen: text content, aspect ratio, mood register.
Format: [JSON envelope / Natural language fallback / System prompt for batch].
SEARCH active: [yes + topic] OR [no].
```

## Prompt templates: JSON envelope format (default for non-Latin)

### Non-Latin script focus (JSON)

```json
{
  "plan": "Script-specific rendering. [Japanese: vertical flow, stroke authenticity. Korean: geometric vs brush character. Hindi Devanagari: conjuncts, matras. Arabic: connected forms, baseline character. Chinese: stroke order, radical structure.] Culturally appropriate design heritage.",
  "search": null,
  "subject": "[Poster, packaging, signage] featuring \"[EXACT TEXT]\" rendered in [Japanese calligraphy / Korean Hangul display / Chinese seal script / Hindi Devanagari / Bengali display / Arabic / Hebrew]. Exact text in correct script characters.",
  "pose": "Static typographic composition.",
  "environment": "[Supporting visual elements or clean field.]",
  "camera": "[Layout framing.]",
  "lighting": "[Lighting that supports legibility.]",
  "mood": "[Mood register tied to script's cultural design heritage.]",
  "style": "[Stroke and letterform character: traditional brush / modern geometric / vernacular hand-lettering / official type-set / engraved.]",
  "palette": "[Color palette tied to the language's cultural design heritage.]",
  "quality": "Rendered at full legibility. Authentic stroke character. No invented glyphs.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "[EXACT TEXT] in correct script characters, no garbling",
    "stroke order and letterform conventions appropriate to script",
    "no invented characters or pseudo-script",
    "legibility at intended scale",
    "cultural design heritage respected"
  ],
  "negative_prompt": {
    "forbidden": [
      "character corruption",
      "invented glyphs",
      "pseudo-script (decorative shapes resembling but not being the script)",
      "latin substitution for non-latin characters",
      "wrong script (e.g., Chinese hanzi when Japanese kanji requested)",
      "stroke order errors that produce non-existent characters",
      "latinized typographic conventions applied to non-latin script",
      "missing diacritics, matras, or conjuncts",
      "decorative substitution where literal rendering was requested",
      "hybrid characters mixing scripts",
      "AI-style abstract typography in place of correct script"
    ]
  }
}
```

### Mixed-script layout (JSON)

```json
{
  "plan": "Two-script hierarchy. Each script rendered in its native tradition. Unified palette across both. Neither script degrades to decorative noise.",
  "search": null,
  "subject": "[Layout type] combining \"[EXACT TEXT 1]\" in [script 1] with \"[EXACT TEXT 2]\" in [script 2]. Each script in its native typographic tradition.",
  "pose": "Static composition.",
  "environment": "[Supporting design field.]",
  "camera": "[Layout framing.]",
  "lighting": "[Lighting that supports legibility of both scripts.]",
  "mood": "[Unified mood across both scripts.]",
  "style": "[Editorial / luxury / street / minimalist] with both scripts in their native tradition.",
  "palette": "[Unified palette across both scripts.]",
  "quality": "Both scripts rendered authentically. Hierarchy clear. No script degrades.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "EXACT TEXT 1 spelled correctly in script 1",
    "EXACT TEXT 2 spelled correctly in script 2",
    "neither script becomes decorative",
    "hierarchy and size relationship clear",
    "palette unified"
  ],
  "negative_prompt": {
    "forbidden": [
      "either script corrupted or invented",
      "decorative use of one script as ornament instead of legible text",
      "latinization of non-latin script",
      "palette breaking between scripts",
      "hierarchy inversion",
      "size accident causing one script to dominate when balance was specified"
    ]
  }
}
```

### Brand wordmark (JSON, fidelity-flagged)

```json
{
  "plan": "Wordmark for brand. Design direction defined. Letterform consistency required. Fidelity risk acknowledged.",
  "search": null,
  "subject": "Wordmark design for \"[EXACT BRAND NAME]\". [Design direction: geometric / organic / serif / script / stencil].",
  "pose": "Static logo composition.",
  "environment": "[Clear background: white, black, or specified field.]",
  "camera": "[Centered or specified layout.]",
  "lighting": "[Flat lighting for logo legibility.]",
  "mood": "[Mood implied by design direction.]",
  "style": "[Letterform relationships: tight spacing, generous tracking, ligatures.] Brand wordmark fidelity is a known limitation.",
  "palette": "[Color spec.]",
  "quality": "Letterform consistency required. Iteration may be needed for exact fidelity.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "brand name spelled correctly",
    "letterform consistency across the wordmark",
    "design direction visible in execution",
    "no extra characters or repetition"
  ],
  "negative_prompt": {
    "forbidden": [
      "brand name misspelling",
      "extra letters appended",
      "letter substitution",
      "letterform inconsistency (some letters in one style, others in another)",
      "decorative ornament obscuring the wordmark",
      "spacing chaos",
      "imitation of an existing trademark not requested"
    ]
  }
}
```

## Prompt templates: NL fallback (Latin-only and exploratory)

### Single-word display typography

```
PLAN: Hierarchy: "[EXACT TEXT]" as the sole focal element. Medium and rendering tradition defined. Legibility required at full scale.
SEARCH: SKIP.
GENERATE: Typographic composition featuring the word "[EXACT TEXT]" rendered as [typeface voice: heavy geometric sans, hand-lettered script, Art Deco capitals, pixel bitmap]. [Color palette]. [Layout: centered, asymmetric, overlapping]. [Background and supporting elements]. [Texture or medium: letterpress, neon glow, carved stone, embroidered thread]. [Aspect ratio].
VERIFY: Before showing output, verify "[EXACT TEXT]" is spelled correctly and legible at full scale. Verify the medium-specific texture is present.
```

### Multilingual poster

```
PLAN: Text hierarchy: "[EXACT TEXT 1]" in [script 1] as primary headline, "[EXACT TEXT 2]" in [script 2] as supporting line. Each script rendered in its native typographic tradition.
SEARCH: SKIP. (Active if text content requires factual verification.)
GENERATE: Poster design with "[EXACT TEXT 1]" in [script 1] as primary headline and "[EXACT TEXT 2]" in [script 2] as supporting line. [Typographic hierarchy]. [Visual style: minimalist Japanese editorial, Korean luxury, French New Wave, Bauhaus]. [Palette]. [Optional image or texture backdrop]. [Aspect ratio].
VERIFY: Before showing output, verify both text strings are spelled correctly in their respective scripts. Verify typographic hierarchy is visually clear.
```

### Dense editorial layout

```
PLAN: Article layout defined. Headline and subhead exact text specified. Body copy length and column structure determined before brief.
SEARCH: SKIP. (Active if article content requires factual accuracy.)
GENERATE: Magazine spread featuring a full article layout. Headline: "[EXACT HEADLINE]". Subhead: "[EXACT SUBHEAD]". Body copy: [specify exact paragraphs or describe topic]. Typographic style: [serif elegance, modernist sans, brutalist industrial]. Grid structure: [two-column, three-column, asymmetric]. [Image placement if relevant]. [Palette]. [Aspect ratio].
VERIFY: Before showing output, verify headline and subhead are spelled correctly and visually dominant. Verify body copy density is legible at the stated scale.
```

### Non-Latin script focus

```
PLAN: Script-specific rendering requirements. [Japanese: vertical flow, stroke authenticity]. [Korean: geometric vs brush character]. [Hindi Devanagari: conjuncts, matras]. Culturally appropriate design heritage.
SEARCH: SKIP.
GENERATE: [Poster, packaging, signage] featuring "[EXACT TEXT]" rendered in [Japanese calligraphy, Korean Hangul display, Chinese seal script, Hindi Devanagari, Bengali display]. [Stroke and letterform character: traditional brush, modern geometric, vernacular hand-lettering]. [Color palette tied to the language's cultural design heritage]. [Supporting visual elements]. [Aspect ratio].
VERIFY: Before showing output, verify "[EXACT TEXT]" is in the correct script and characters are not garbled or invented. Verify script-appropriate conventions are applied.
```

### Mixed-script layout

```
PLAN: Two-script hierarchy. Script 1 primary, Script 2 supporting. Each rendered in its native tradition. Unified palette across both.
SEARCH: SKIP.
GENERATE: [Layout type] combining "[EXACT TEXT 1]" in [script 1] with "[EXACT TEXT 2]" in [script 2]. Each script rendered in its native typographic tradition. [Hierarchy and size relationship]. [Unified palette]. [Overall design voice: editorial, luxury, street, minimalist]. [Aspect ratio].
VERIFY: Before showing output, verify both text strings are spelled correctly in their respective scripts. Verify neither script degrades or becomes decorative noise.
```

### Brand wordmark (flag fidelity)

```
PLAN: Brand name to render. Design direction: [geometric, organic, serif, script, stencil]. Fidelity risk acknowledged.
SEARCH: SKIP.
GENERATE: Design a wordmark for "[EXACT BRAND NAME]". [Design direction]. [Letterform relationships: tight spacing, generous tracking, ligatures]. [Color]. [Supporting mark or icon if desired]. Clear on [white or black] background. [Aspect ratio]. Note: brand mark fidelity is a known limitation; iteration may be required.
VERIFY: Before showing output, verify brand name spelling is correct. Flag any letterform drift for iteration.
```

### Sign or environmental typography

```
PLAN: Sign type and material defined. Environmental context stated. Script and fabrication technique determine rendering approach.
SEARCH: SKIP. (Active if sign content must reflect current accurate information.)
GENERATE: [Type of sign or surface: shopfront, restaurant facade, airport departure board, street banner, vintage enamel sign] displaying "[EXACT TEXT]" in [script]. [Material and fabrication: enamel, neon, backlit acrylic, painted plaster, engraved brass]. [Contextual environment: street scene, interior, weathered surface]. [Lighting and time of day]. [Aspect ratio].
VERIFY: Before showing output, verify "[EXACT TEXT]" is legible and correctly spelled. Verify material-specific aging or fabrication artifacts are present.
```

## Verbatim exemplars from the research

From OpenAI's launch materials:

```
Bauhaus-inspired poster with bold typography that says "GPT IMAGE 2" and "DESIGN THE FUTURE".
```

Pattern: style tradition + exact typography content + secondary text. Canonical poster prompt.

From @liyue_ai on X:

```
以眼部特写图片为基础，生成3:4的四屏构图超写实眼部特写，四屏按春夏秋冬上下排序... 画面中央"SPRING"白色艺术字点缀... 下面用书法体写着春.
```

Pattern: mixed-script prompt combining English display typography and Chinese calligraphy in a four-panel seasonal composition. Preserves exact text per script and renders both authentically.

From OpenAI luxury campaign demo:

```
Luxury fashion book spread, premium hospitality campaign using Korean typography.
```

Pattern: cultural typography anchor as the primary design identity. Works because GPT Image 2 reasons about Korean editorial conventions rather than treating Hangul as decoration.

## Self-validation before output

- [ ] Exact text specified in quotes in every prompt
- [ ] Script(s) named explicitly
- [ ] Preamble names axis, frozen axes, format chosen, and SEARCH status
- [ ] Format chosen matches request (JSON for non-Latin, NL for Latin-only display work)
- [ ] Exactly 7 prompts
- [ ] Each prompt in its own code block (JSON in ` ```json `, NL in plain ` ``` `)
- [ ] Each prompt encodes PSGV per format
- [ ] Each prompt's verification step checks spelling accuracy and script convention application
- [ ] If JSON: forbidden array refuses character corruption, latin substitution, invented glyphs
- [ ] Prompts vary along the stated axis only
- [ ] Text content frozen across all 7 unless axis is language
- [ ] No em-dashes

## Error handling

If the user's text contains no quotation marks or is too vague to render exactly, ask for the exact copy with `ask_user_input_v0` (options: give exact text, use placeholder, generate sample copy).

If the user requests a real brand's exact logo, warn about the fidelity risk and offer either a "spirit of the brand" interpretation or an iterative refinement approach.
