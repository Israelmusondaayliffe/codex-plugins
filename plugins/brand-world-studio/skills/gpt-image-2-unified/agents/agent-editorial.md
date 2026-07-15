# Agent: EDITORIAL

Posters, magazine spreads, campaign layouts, slide decks, brand systems. Layouts where image and typography share the canvas with intentional design.

**Inheritance**: ADAPT from `nano-banana-unified/agents/agent-brand.md` and the CREATE posters/campaign sub-template. Brand-system generation from a single name (research exemplar from @SRKDAN's stamp-and-badge prompt) is a confirmed GPT Image 2 emergent capability. Adapted: absorbed Nano Banana's BRAND mode into EDITORIAL to keep the mode surface focused on layout as the unifying concept.

## Scope

EDITORIAL is for image-text layouts where the design composition is the deliverable:

- Movie posters, theater posters, concert posters
- Magazine covers and spreads
- Campaign keyvisuals and ad layouts
- Slide deck pages (single slide as an image asset)
- Album or book covers
- Editorial portrait layouts (fashion, lifestyle, culinary)
- Brand identity systems (logo + wordmark + supporting marks)
- Social media keyvisuals and carousel covers
- Event flyers and broadsides

For adjacent workflows, route back:
- Dense structured information → INFOGRAPHIC
- Text is the primary subject → TYPOGRAPHY
- Sequential story panels → NARRATIVE
- Multi-output consistency → SERIES
- Based on current facts → SEARCH

## Known strengths

- Stylistic sophistication across design traditions (Bauhaus, French New Wave, Swiss, Art Deco, Memphis, vernacular)
- Typography placement that respects compositional logic (title center-stage, hierarchy, breathing room)
- Mixed-language campaign work (Korean luxury, Japanese editorial, Bengali social)
- Brand-from-name system generation (visual DNA extracted from a word)
- UI mockups and app screen layouts

## Known weaknesses (flag)

- Brand logo mark reproduction drift
- Very small text at high density may degrade
- Safety filters may over-correct for political, religious, or named-public-figure campaign work

## Format escalation

**Default for EDITORIAL: natural-language brief.** Editorial work benefits from atmospheric, mood-driven prose that NL captures better than rigid JSON keys. Design tradition, typography hierarchy, and palette logic flow naturally as paragraph briefs.

**Escalate to JSON envelope** when:
- The hero shot is a single high-stakes campaign keyvisual where exact text fidelity is mission-critical and safety against drift outweighs prose flexibility.
- The user wants a brand wordmark or logo treatment where letterform consistency must be explicitly refused against drift.
- Multi-reference editorial (subject reference + style reference for a poster) where role separation matters.

**Escalate to system prompt** when:
- The user runs an editorial campaign series across the same brand voice (cover + spread + social + outdoor in one session).

State the format chosen in the preamble. NL is the default unless one of these signals fires.

## Workflow

### Step 0: Run deconstruction first when starting from a reference image

If the user uploads a reference image and wants the look extracted and applied to a different brand, product, or campaign, run the deconstruction pattern from `references/reference-deconstruction.md` before this workflow. The pattern returns a 4:3 brand board that becomes the written visual DNA for the editorial layout. Skip when the user already supplied a brand spec or named the design tradition explicitly.

### Step 1: Declare the design brief

```
DESIGN BRIEF:
Format: [poster, magazine cover, slide, ad, brand system, book cover]
Subject or product: [what the design is for]
Exact text: [headline, subhead, date, secondary copy, all in quotes]
Design tradition or reference: [Bauhaus, French New Wave, Korean luxury, brutalist, vernacular]
Palette direction: [specified or open]
Aspect ratio or format: [letter, tabloid, billboard, 1:1, 2:3]
```

### Step 2: Detect the variation axis

Common EDITORIAL axes:

- Design tradition (7 design schools applied to the same brief)
- Layout (7 compositional arrangements of the same elements)
- Palette (7 color schemes on identical layout)
- Typographic treatment (7 typeface voices)
- Era (7 decades of design style)
- Format (vertical, square, horizontal, extreme ratios)
- Brand tone (luxury vs vernacular vs utilitarian vs playful)

If ambiguous, ask.

### Step 3: Map PSGV for EDITORIAL

**PLAN**: Design brief declared first. Format, exact copy in quotes, design tradition, palette direction. The model reasons about compositional logic before placing a single element. Define what aesthetic coherence means for this specific brief.

**SEARCH**: SKIP for most editorial work. Active when the layout must include current real-world information (current stats, live pricing, current event data for a data-driven editorial piece).

**GENERATE**: The layout brief. Every piece of exact text in quotes, design tradition, compositional approach, palette, aspect ratio.

**VERIFY**: Before showing output, verify all exact text is present and correctly spelled. Verify aesthetic is cohesive across all elements (typography, image, color). Verify the format and aspect ratio match the brief.

### Step 4: Generate 7 prompts

## Preamble format

```
Format: [poster, spread, slide, brand system].
Exact text: [key text in quotes].
Axis varied: [e.g., design tradition, from Bauhaus to Swiss International to Memphis to French New Wave to Art Deco to vernacular hand-painted to Y2K techno].
Axes frozen: text content, subject, aspect ratio, message.
Format chosen: [Natural language (default) / JSON envelope (hero shot escalation) / System prompt (campaign series)].
SEARCH active: [yes + topic] OR [no].
```

## Prompt templates

### Film or concert poster

```
PLAN: Format: [film, theater, concert] poster, [aspect ratio: 2:3]. Key text: title "[EXACT TITLE]", tagline "[EXACT TEXT]". Hero image direction and typographic voice defined.
SEARCH: SKIP.
GENERATE: [Film, theater, concert] poster for "[EXACT TITLE]". [Tagline: "EXACT TEXT"]. [Hero image direction: protagonist portrait, symbolic object, atmospheric scene]. [Typographic voice: elegant serif, brutalist sans, hand-lettered, French New Wave vernacular]. [Palette]. [Layout: centered, asymmetric, split, full-bleed image with text band]. [Mood]. [Aspect ratio: 2:3].
VERIFY: Before showing output, verify title and tagline are spelled correctly and visually dominant. Verify typographic voice matches the stated tradition.
```

### Magazine cover

```
PLAN: Cover hierarchy: masthead dominant, cover line secondary, image as backdrop. All exact text defined before brief.
SEARCH: SKIP.
GENERATE: Magazine cover for [title or concept magazine]. Masthead: "[EXACT TITLE]". Cover line: "[EXACT HEADLINE]". Secondary lines: [list in quotes]. [Cover image direction]. [Typographic system: serif luxury, modernist sans, editorial elegance]. [Palette]. [Aspect ratio: 3:4 or similar].
VERIFY: Before showing output, verify masthead and cover line are correctly spelled and in correct hierarchy. Verify the cover image does not obscure masthead.
```

### Campaign keyvisual

```
PLAN: Campaign intent: [brand, product, tone]. Headline and supporting copy exact. Compositional approach defined.
SEARCH: SKIP. (Active if campaign must reference current stats or live data.)
GENERATE: Campaign keyvisual for [brand or product]. Hero element: [image direction]. Headline: "[EXACT TEXT]". Supporting copy: "[EXACT TEXT]". [Brand tone: luxury, everyday, aspirational, utilitarian]. [Compositional approach: symmetrical, diagonal, rule-of-thirds, full-bleed]. [Palette]. [Aspect ratio].
VERIFY: Before showing output, verify headline and copy are present and correctly spelled. Verify brand tone is consistent across image and typography.
```

### Brand identity system (from a name)

```
PLAN: Brand name to render. Personality keywords: [bold/angular/industrial, OR soft/organic, OR editorial]. Deliverable set: wordmark, symbol mark, palette swatches, typography sample, one application mockup.
SEARCH: SKIP.
GENERATE: Full brand identity system for "[EXACT BRAND NAME]". Include: primary wordmark, symbol mark, palette swatches, supporting typography sample, one application mockup. [Brand personality]. [Aspect ratio appropriate for identity sheet].
VERIFY: Before showing output, verify brand name is spelled correctly in the wordmark. Verify aesthetic is consistent across all system components.
```

### Slide deck page

```
PLAN: Slide headline and content exact text defined. Visual anchor type determined. Design system stated.
SEARCH: SKIP. (Active if slide must contain current data or verified statistics.)
GENERATE: Single slide titled "[EXACT HEADLINE]". Content: [bullet points or message as exact text]. [Visual anchor: chart, photo, diagram, illustration]. [Design system: corporate modern, editorial, startup bold, consulting conservative]. [Palette: two or three colors]. [Aspect ratio: 16:9].
VERIFY: Before showing output, verify headline is spelled correctly. Verify all content text is legible at slide scale.
```

### UI mockup

```
PLAN: UI type and product category. All UI element labels exact. Design tradition and color palette defined.
SEARCH: SKIP.
GENERATE: [Mobile app or web] screen mockup for [product type]. Layout includes: [specify UI elements: search bar at top, featured cards, bottom navigation with labeled icons: "Home", "Explore", "Bookings", "Profile"]. [Design tradition: Material, Apple HIG, neobrutalist, glassy, skeuomorphic]. [Color palette]. [Typography]. [Aspect ratio: 9:19.5 for mobile, 16:10 for web].
VERIFY: Before showing output, verify all UI labels are spelled correctly and semantically consistent. Verify the layout reads as a functional UI, not decorative.
```

### Book or album cover

```
PLAN: Title and creator exact text. Genre or category determines visual direction and typographic voice.
SEARCH: SKIP.
GENERATE: [Book, album] cover for "[EXACT TITLE]" by "[EXACT CREATOR]". [Genre or category]. [Visual direction: single strong image, typographic-first, abstract composition, illustrated]. [Typographic voice]. [Palette]. [Aspect ratio: 2:3 for books, 1:1 for albums].
VERIFY: Before showing output, verify title and creator name are spelled correctly. Verify genre conventions are present in the visual treatment.
```

### Event flyer

```
PLAN: Event details exact: name, date, location. Design voice appropriate to event type.
SEARCH: SKIP.
GENERATE: [Event type] flyer. Event: "[EXACT NAME]". Date: "[EXACT DATE]". Location: "[EXACT LOCATION]". [Design voice: hand-painted vernacular, punk cut-and-paste, modernist grid, luxury minimal]. [Color palette]. [Supporting imagery or texture]. [Aspect ratio: 2:3 or 1:1].
VERIFY: Before showing output, verify event name, date, and location are spelled correctly. Verify all critical information is legible.
```

## Verbatim exemplars from the research

OpenAI launch:

```
French New Wave–inspired poster for a film titled "L'Amour à Paris".
```

Pattern: design tradition + exact title. Model designs the poster around the typography in the style's visual vocabulary.

```
Luxury fashion book spread, premium hospitality campaign using Korean typography.
```

Pattern: layout type + category + cultural typography anchor. Generalizes to any cultural campaign brief.

From @austinit:

```
Generate a clean and modern mobile app UI design for a travel booking platform. The layout should include a search bar at the top, featured destination cards with high-quality imagery, a bottom navigation bar with icons for 'Home', 'Explore', 'Bookings', and 'Profile', and a minimalist typography style. Use a color palette of soft blues, whites, and light grays.
```

Pattern: UI mockup with explicit element list, icon labels in quotes, style specification, palette. GPT Image 2 treats UI elements as semantic objects rather than shapes, which is why this works.

From @SRKDAN:

```
Generate a full stamp-and-badge identity system from one product name. Bold, angular, industrial.
```

Pattern: brand-from-name system generation. Three-word personality cue unlocks a full identity suite.

From @yammamon (Momotaro explainer slide): specific narrative subject + slide format generates structured explanatory slides.

## Self-validation before output

- [ ] Exact text specified in quotes throughout
- [ ] Format and aspect ratio specified
- [ ] Preamble names axis, frozen axes, format chosen, and SEARCH status
- [ ] Format chosen matches request (NL default, JSON for hero shots and brand mark fidelity, system prompt for campaign series)
- [ ] Exactly 7 prompts
- [ ] Each prompt in its own code block (NL in plain ` ```, JSON in ` ```json `, system prompts in plain ` ``` `)
- [ ] Each prompt encodes PSGV per format
- [ ] Each prompt's verification step checks text spelling, aesthetic coherence, and format
- [ ] Prompts vary along the stated axis only
- [ ] No em-dashes

## Error handling

For brand-logo work, flag fidelity risks and offer iterative refinement.

For campaigns involving real public figures, warn about safety filters and suggest framings that keep the figure as a stylistic reference rather than a literal portrait.

If the user has not provided exact copy, ask with `ask_user_input_v0` (options: give exact copy, use placeholder, generate sample copy).
