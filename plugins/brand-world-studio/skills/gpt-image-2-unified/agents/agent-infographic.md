# Agent: INFOGRAPHIC

Diagrams, charts, maps, educational visuals, data visualization. Structured information rendered as imagery.

**Inheritance**: ADAPT from `nano-banana-unified/agents/agent-create.md` (Infographic sub-mode). Structural scaffolding (titled infographic, information hierarchy, exact-text labeling) is model-agnostic. Adapted: added web-search grounding pattern for Thinking mode. Research confirmed via Gewirtz (ZDNET San Francisco weather activities infographic), Cantor's diagonalization proof, Barreleye fish anatomy poster, and VentureBeat Aztec/Maya/Inca empire map with legible legend.

## Scope

INFOGRAPHIC is for imagery where structure and information are the primary content:

- Flowcharts and process diagrams
- Data visualization (bar, line, pie, scatter, Sankey, treemap)
- Maps with accurate geography and legible legends
- Educational diagrams (anatomy, cycles, hierarchies, taxonomies)
- Dashboards and stat boards
- Explainer graphics (how something works)
- Timeline visualizations

For adjacent workflows, route back:
- Heavy text with decorative image → TYPOGRAPHY
- Poster layout with image focus → EDITORIAL
- Requires current live data → SEARCH (or SEARCH-integrated INFOGRAPHIC; see below)
- Multi-page educational comic → NARRATIVE

## Known strengths

- Legible legends at magazine scale (VentureBeat map demo)
- Logical flowchart and process diagrams (Cantor's proof, chili pork cooking flowchart per @Kurt_Rousey466)
- Scientific anatomy diagrams with labeled structures
- Mixed-script infographics (Korean water cycle, Hindi educational posters)

## Known weaknesses (flag)

- Geographic hallucination: invented countries ("Ciger", "Mharee"), misplaced capitals (Nairobi in Saudi Arabia per launch demo). Always specify source and verify.
- Anatomical accuracy: muscles may lack bone attachments (sternocleidomastoid + clavicle example). Flag for high-stakes medical use.
- Very dense small text in cluttered layouts may still degrade.
- Diagrams with duplicate numbers or incoherent labels reported occasionally.

## Format escalation

**Default for INFOGRAPHIC: JSON envelope.** The forbidden array refuses hallucinated data, fabricated labels, wrong axes, and invented place names at the category level. NL alone cannot stop the model from helpfully filling in plausible but wrong content.

Auto-detection rules:

- **JSON envelope format (default)**: any INFOGRAPHIC with specific named labels, data, geographic content, or anatomical accuracy requirements. Forbidden array enforces label fidelity.
- **System prompt format**: when the user runs an information series across the same data set in one session (e.g., 7 chart styles for the same dataset, or 7 educational posters from one curriculum).
- **NL format (fallback)**: stylized graphics with no critical data, decorative diagram work, "make me a pretty flowchart of X" where label accuracy is loose.

State the format chosen in the preamble.

## Workflow

### Step 1: Declare the information content

```
INFORMATION SPECIFICATION:
Type: [flowchart, map, anatomy diagram, bar chart, process diagram, dashboard]
Subject: [what the infographic is about]
Key data points or labels: [list, with exact text in quotes]
Title: "[EXACT TITLE]"
Source (if factual accuracy matters): [e.g., Wikipedia, official statistics, user-provided data]
```

### Step 2: Decide if web search is needed

If the information depends on current facts (today's weather, current statistics, live sports), route through SEARCH patterns inside Thinking mode. Otherwise, Instant mode is often sufficient for structural diagrams.

### Step 3: Detect the variation axis

Common INFOGRAPHIC axes:

- Visual style (editorial, scientific, corporate, textbook, hand-drawn)
- Layout approach (vertical poster, horizontal dashboard, circular, radial, grid)
- Complexity level (executive summary vs detailed reference)
- Color palette (muted editorial, bold modern, monochrome, high-contrast)
- Chart type (for data: bar vs line vs treemap vs sankey)
- Audience register (children's educational vs academic vs professional)

### Step 3: Map PSGV for INFOGRAPHIC

**PLAN**: Information hierarchy first. Title, key labels, logical relationships, and information density defined before the brief. The model needs to reason about label consistency before rendering. For maps, specify the exact region and source to reduce geographic hallucination.

**SEARCH**: Active when information depends on current facts: today's data, live statistics, current event data. Include explicit search trigger and date anchor. For historical or static content, SKIP.

**GENERATE**: The diagram brief. Title and all labels in quotes, structure, style, density, aspect ratio.

**VERIFY**: Before showing output, verify all labels are present, correctly spelled, and logically consistent. Verify no duplicate numbers or contradictory legend items. For maps, verify country names and capitals against the stated source.

### Step 5: Generate 7 prompts

## Preamble format

```
Infographic type: [flowchart, map, chart, diagram, poster].
Information content: [one-line summary].
Title: "[EXACT TITLE]"
Axis varied: [e.g., visual style, from editorial to textbook to hand-drawn to corporate to mid-century to modern minimalist to Japanese vernacular].
Axes frozen: information content, title, data points.
Format: [JSON envelope / Natural language fallback].
SEARCH active: [yes + topic + date anchor] OR [no].
Known risks: [geographic hallucination, anatomical gaps, small-text illegibility if dense].
```

## Prompt templates: JSON envelope format (default)

### Titled infographic (JSON)

```json
{
  "plan": "Information hierarchy: title \"[EXACT TITLE]\" dominant. Supporting labels [list]. Layout and density defined. Label fidelity is the primary risk.",
  "search": null,
  "subject": "[Type] titled \"[EXACT TITLE]\". Information hierarchy: primary message at top, supporting data below. Data and labels: [\"label 1\", \"label 2\", \"label 3\"].",
  "pose": "Static infographic composition.",
  "environment": "[Background field appropriate to style.]",
  "camera": "[Layout framing: vertical poster / horizontal dashboard / radial.]",
  "lighting": "[Even lighting for legibility.]",
  "mood": "[Mood register tied to subject.]",
  "style": "[Editorial / textbook / hand-drawn / corporate / mid-century / minimalist.]",
  "palette": "[Specified palette.]",
  "quality": "All labels legible. No duplicate values. No invented data.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "title spelled correctly",
    "every supporting label present and spelled correctly",
    "no label appears twice with different values",
    "no fabricated data points",
    "visual hierarchy reads as specified"
  ],
  "negative_prompt": {
    "forbidden": [
      "fabricated data points",
      "invented labels not in the brief",
      "duplicate labels with conflicting values",
      "title misspelling",
      "label corruption",
      "decorative ornament obscuring data",
      "axis values that don't match data",
      "legend items not present in the chart",
      "filler placeholder text where real labels were specified"
    ]
  }
}
```

### Map with legend (JSON)

```json
{
  "plan": "Specific region. Source stated. Geographic accuracy is the primary risk. Forbidden array refuses invented place names and capital misplacement.",
  "search": "[Search the web, today is [date]: current borders of [region]. Source: Wikipedia.] OR null for historical maps",
  "subject": "Map of [specific region] at [specific period or date]. Source: [stated, e.g. Wikipedia].",
  "pose": "Static cartographic composition.",
  "environment": "Map field with legible legend area.",
  "camera": "[Map projection and framing.]",
  "lighting": "Even, no atmospheric drama.",
  "mood": "Authoritative, factual.",
  "style": "[Cartographic style: editorial, textbook, vintage, modern minimalist.]",
  "palette": "[Cartographic palette appropriate to style.]",
  "quality": "All country names verified against source. Capitals correctly placed. Legend legible.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "all country names match the stated source",
    "capitals placed in correct countries",
    "legend items match map content",
    "no invented place names",
    "borders historically accurate to stated period"
  ],
  "negative_prompt": {
    "forbidden": [
      "invented country names",
      "invented city names",
      "capital cities misplaced (e.g., Nairobi in Saudi Arabia)",
      "borders inconsistent with stated period",
      "legend items not present on the map",
      "decorative cartouche substituting for legible legend",
      "country shape distortion that obscures identity",
      "anachronistic borders",
      "missing major landmarks specified in the brief"
    ]
  }
}
```

### Anatomy or scientific diagram (JSON)

```json
{
  "plan": "Anatomical structure. Label inventory. Structural relationships. Anatomical accuracy is the primary risk. Forbidden array refuses missing attachments and invented structures.",
  "search": null,
  "subject": "[Scientific illustration / anatomy plate / encyclopedia poster] of [subject]. Labels: [\"label 1\", \"label 2\", \"label 3\"]. Accurate anatomical relationships.",
  "pose": "Static diagrammatic composition.",
  "environment": "[Background field appropriate to scientific style.]",
  "camera": "[View: lateral, anterior, cross-section, exploded.]",
  "lighting": "Even, diagrammatic.",
  "mood": "Authoritative, scientific.",
  "style": "[Encyclopedia engraving / modern medical illustration / textbook line art / colorized educational.]",
  "palette": "[Style-appropriate palette.]",
  "quality": "All structures correctly attached. All labels present. No invented features.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "every listed label present",
    "structural attachments correct (muscles to bones, vessels to organs)",
    "scientific names spelled correctly",
    "no invented anatomical structures",
    "view consistent throughout"
  ],
  "negative_prompt": {
    "forbidden": [
      "muscles without bone attachments",
      "invented anatomical features",
      "missing labels from the inventory",
      "label spelling errors",
      "structural impossibilities",
      "decorative ornament obscuring anatomy",
      "view inconsistency (mixing lateral and anterior elements)",
      "stylized illustration where scientific accuracy was specified"
    ]
  }
}
```

### Data visualization (JSON)

```json
{
  "plan": "Chart type. Axes labeled exactly. Data points or source. Axis fidelity and label accuracy primary risks.",
  "search": "[Search the web, today is [date]: [data source].] OR null",
  "subject": "[Chart type: bar, line, pie, scatter, treemap] showing [data subject]. Axes labeled: \"[X-AXIS LABEL]\", \"[Y-AXIS LABEL]\". Data points: [specify or describe source].",
  "pose": "Static chart composition.",
  "environment": "Chart field with legible axis area.",
  "camera": "[Chart layout framing.]",
  "lighting": "Even, dataviz-clean.",
  "mood": "Analytical, factual.",
  "style": "[Editorial / corporate / minimalist / FT-style / NYT-style.]",
  "palette": "[Dataviz palette: sequential, diverging, categorical, monochrome.]",
  "quality": "Axis labels exact. Data values match source. Legend complete.",
  "aspect_ratio": "[W:H]",
  "verify": [
    "X-axis label spelled exactly",
    "Y-axis label spelled exactly",
    "data points labeled correctly",
    "chart type matches data structure",
    "legend items match plotted series"
  ],
  "negative_prompt": {
    "forbidden": [
      "fabricated data values",
      "axis label corruption",
      "wrong chart type for data structure",
      "legend mismatch with plotted series",
      "scale errors that misrepresent data",
      "decorative chart junk obscuring values",
      "extra series not in the brief",
      "missing series specified in the brief"
    ]
  }
}
```

## Prompt templates: NL fallback (stylized graphics, decorative diagrams)

### Titled infographic

```
PLAN: Information hierarchy: title "[EXACT TITLE]" dominant, [key data point labels] supporting. Layout and density defined: [vertical poster, horizontal dashboard, radial].
SEARCH: SKIP. (Active if data requires current verification.)
GENERATE: [Type] titled "[EXACT TITLE]". [Information hierarchy: primary message at top, supporting data below]. [Data and labels: "label 1", "label 2", "label 3"]. [Visual style]. [Color palette]. [Layout]. [Aspect ratio].
VERIFY: Before showing output, verify title and all labels are present and correctly spelled. Verify no label appears twice with different values.
```

### Flowchart or process diagram

```
PLAN: Process steps defined in order: [step 1, step 2, step 3...]. Decision points identified. Arrow direction established.
SEARCH: SKIP.
GENERATE: Flowchart showing [process name]. Steps in order: [step 1: "EXACT TEXT", step 2: "EXACT TEXT", ...]. Decision points at: [specify]. Shapes: rounded rectangles, diamonds for decisions. Arrows flow [direction]. [Style: minimal, colorful, corporate, hand-drawn]. [Aspect ratio].
VERIFY: Before showing output, verify all step labels are present and spelled correctly. Verify decision points have at least two exit paths labeled. Verify logical sequence is intact.
```

### Map with legend

```
PLAN: Specific region defined: [not "world map"]. Source stated. Geographic elements required listed.
SEARCH: SKIP for historical maps. (Active for current political borders: "Search the web, today is [date]: current borders of [region]. Source: Wikipedia.")
GENERATE: Map of [specific region] at [specific period or date]. Include: [geographic elements]. Legend with legible labels and a key. Source: [stated]. [Style]. [Aspect ratio].
VERIFY: Before showing output, verify all country names and capitals match the stated source. Flag any invented place names before rendering.
```

### Anatomy or scientific diagram

```
PLAN: Anatomical features required listed explicitly. Label inventory: [label 1, label 2, label 3...]. Structural relationships stated.
SEARCH: SKIP. (Active if current taxonomy or nomenclature verification required.)
GENERATE: [Scientific illustration, anatomy plate, encyclopedia poster] of [subject]. Labels: ["label 1", "label 2", "label 3"]. Accurate [anatomical relationships, scientific names, structural hierarchy]. [Style]. [Aspect ratio]. For medical accuracy, outputs should be verified against authoritative references.
VERIFY: Before showing output, verify all listed labels are present and structurally coherent. Verify no muscle is depicted without its bone attachment.
```

### Data visualization

```
PLAN: Chart type, axes, data points, and source defined. Axes labeled exactly.
SEARCH: SKIP. (Active if data is current: "Search the web, today is [date]: [data source].")
GENERATE: [Chart type: bar, line, pie, scatter, treemap] showing [data subject]. Data points: [specify or describe source]. Axes labeled: "[X-AXIS LABEL]", "[Y-AXIS LABEL]". [Color palette]. [Visual style]. Legible labels. [Aspect ratio].
VERIFY: Before showing output, verify axis labels are present and legible. Verify data points are labeled correctly. Verify chart type matches the data structure.
```

### Search-integrated infographic

```
PLAN: Infographic container defined: title, layout, metrics inventory. All visual decisions made before search populates the content.
SEARCH: Search the web, today is [date]: [specific current data]. Verify from [credible source].
GENERATE: Create an infographic titled "[EXACT TITLE]" incorporating the retrieved data. [Visual style]. [Aspect ratio]. Include source attribution in the design.
VERIFY: Before showing output, verify all data points are search-retrieved and not from training memory. Verify source attribution is visible in the design.
```

### Educational poster

```
PLAN: Audience register defined. Key concepts listed. Label inventory established before brief.
SEARCH: SKIP.
GENERATE: Educational poster titled "[EXACT TITLE]" explaining [topic]. Key concepts illustrated: ["concept 1", "concept 2", "concept 3"]. [Style: friendly illustrated, textbook clean, mid-century children's book]. [Palette appropriate for audience]. Legible labels. [Aspect ratio].
VERIFY: Before showing output, verify title and all concept labels are present and correctly spelled. Verify visual complexity is appropriate for the stated audience.
```

### Dashboard or stat board

```
PLAN: Metric categories defined. Each metric: number, label, brief context. Layout type established.
SEARCH: SKIP. (Active if metrics require current data.)
GENERATE: Dashboard titled "[EXACT TITLE]" showing [categories of metrics]. Each metric presented with: number, label, brief context. [Layout: grid, modular, newspaper-style]. [Visual style: corporate clean, fintech, sports scoreboard, newsroom]. [Aspect ratio].
VERIFY: Before showing output, verify all metric labels are present and logically consistent. Verify no metric contradicts another in the same dashboard.
```

## Verbatim exemplars from the research

Gewirtz ZDNET test:

```
Generate an infographic about activities I should do with tomorrow's weather in San Francisco in mind.
```

Pattern: search-integrated infographic. Model retrieves weather, reasons about activities, designs layout.

From the research (cooking flowchart, @Kurt_Rousey466):

```
Chili Pork Cooking Flowchart.
```

Pattern: minimal prompt with the model filling in process steps. Works for well-known processes. For custom processes, specify steps explicitly.

From OpenAI blog (mathematical proof):

```
Infographic showing Cantor's diagonalization proof on a blackboard.
```

Pattern: mathematical content rendered with correct logical structure in a specific visual context (blackboard).

From VentureBeat hands-on:

```
Map of the Aztec, Maya, and Inca empires at their heights, complete with a fully legible legend.
```

Pattern: multi-empire historical map with explicit legend requirement. GPT Image 2 renders this correctly; specifying the legend as a requirement is key.

From @itnavi2022 (Barreleye fish):

```
Science Encyclopedia Vertical Poster about the anatomy of a Barreleye Fish.
```

Pattern: specific species + format (vertical poster) + style tradition (science encyclopedia). Produces labeled anatomy at high fidelity.

## Self-validation before output

- [ ] Title specified exactly in quotes
- [ ] Key labels specified in quotes
- [ ] Preamble names axis, frozen axes, format chosen, SEARCH status, and known risks
- [ ] Format chosen matches request (JSON for accuracy-critical, NL for stylized graphics)
- [ ] Exactly 7 prompts
- [ ] Each prompt in its own code block (JSON in ` ```json `, NL in plain ` ``` `)
- [ ] Each prompt encodes PSGV per format
- [ ] Each prompt's verification step checks label consistency and logical coherence
- [ ] If JSON: forbidden array refuses fabricated data, invented place names, missing structures
- [ ] For map prompts: source named, geographic hallucination risk flagged
- [ ] Prompts vary along the stated axis only
- [ ] No em-dashes

## Error handling

For geographic content, always include a source reference to reduce hallucination. Flag "Ciger"-type failures as a known risk.

For medical or scientific accuracy, recommend the user verify outputs against authoritative references before publication.

If the user's data is ambiguous, ask with `ask_user_input_v0` whether to use placeholder data, generate sample data, or search for real current data.
