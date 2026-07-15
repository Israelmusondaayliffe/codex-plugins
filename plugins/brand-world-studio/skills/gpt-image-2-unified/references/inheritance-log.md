# Inheritance Log

Every pattern ported from `nano-banana-unified` with classification (INHERIT, ADAPT, REPLACE, NEW) and rationale. Future maintenance depends on this log.

## Classification definitions

- **INHERIT**: pattern is fully model-agnostic. Ported with only surface phrasing adjustments.
- **ADAPT**: pattern applies but required syntactic or parameter changes per GPT Image 2 research.
- **REPLACE**: pattern was Gemini-specific or contradicted by research. Not ported; GPT Image 2 native pattern used instead.
- **NEW**: capability the research reveals that Nano Banana does not have. Built from scratch using research exemplars.

## Mode-level inheritance

| GPT Image 2 mode | Source | Classification | Rationale |
|---|---|---|---|
| CREATE | nano-banana `agent-create.md` | ADAPT | Inherited text-to-image brief-style prompting. Adapted: Instant vs Thinking branch logic; aspect ratio stated as natural phrase rather than Gemini's "AR" suffix; dropped the 120-word cap (research shows dense prompts work in Instant mode, e.g., the BubbleBrain convenience-store exemplar at 300+ words). |
| EDIT | nano-banana `agent-edit.md` | ADAPT | Inherited upload-description discipline and the "Using the uploaded [explicit description]" opener. Adapted: dropped "Do not change aspect ratio" tail (Gemini-specific; GPT Image 2 respects ratios natively). Softened anti-paste mandate from requirement to recommendation (GPT Image 2's conversational edit loop handles pose preservation natively). |
| SHOW-ME | nano-banana `agent-edit.md` (Show-Me sub-mode) | INHERIT | Axis locking for angle-only variation is fully model-agnostic and is the entire point of smart diversity. Ported verbatim in logic. Added 360° equirectangular as a documented option (launch-day emergent capability from @lupapixel). |
| COMPOSE | nano-banana `agent-edit.md` (Multi-Reference sub-mode) | INHERIT with limit adjustment | Multi-reference composition logic ported. Adapted: Nano Banana Pro's documented 14-input, 6-object, 5-human ceiling is not yet confirmed for GPT Image 2. Defaulted to 4 references for reliability; flagged as approximate. |
| SEARCH | No analog | NEW | GPT Image 2 is the first image model with native web search inside the generation pipeline. Built from research exemplars (Gewirtz weather, PumpkinNarrow6339 IPL, Abstruse0788 Leon Kennedy). |
| SERIES | Partial (Nano Banana GRID sub-mode exists but caps at 9-panel single-image grids) | NEW | GPT Image 2's 8-output-with-consistency is a strictly better capability than Nano Banana's grid generation. Built from research exemplars (8 summer outfits, 4-page Spud & Garlic, character reference sheets). |
| TYPOGRAPHY | nano-banana `agent-create.md` (Typography Art sub-template) | NEW with partial ADAPT | Took structural scaffolding for exact-text-in-quotes discipline. Replaced body with GPT Image 2 multilingual exemplars. The non-Latin gain is the headline differentiator of GPT Image 2; Nano Banana's typography sub-template does not anticipate it. |
| INFOGRAPHIC | nano-banana `agent-create.md` (Infographic sub-mode) | ADAPT | Inherited structure (titled infographic, information hierarchy, exact-text labeling). Adapted: added web-search grounding pattern for Thinking mode. Added geographic-hallucination warning based on research failure modes. |
| EDITORIAL | nano-banana `agent-brand.md` + CREATE posters/campaign | ADAPT | Inherited poster and layout logic. Absorbed Nano Banana's standalone BRAND mode into EDITORIAL to keep mode surface focused on layout. Added brand-system-from-name pattern (@SRKDAN exemplar). |
| NARRATIVE | nano-banana `agent-create.md` (Sequential Art / Comics sub-template) | ADAPT | Inherited panel structure and art-style specification. Adapted: leveraged 8-output consistency for multi-page work; recommended routing to SERIES when page count exceeds 1. Added specific manga sub-genre guidance (Seinen, Shonen, Shojo) based on research exemplars. |

## Nano Banana modes not ported

| Nano Banana mode | Decision | Rationale |
|---|---|---|
| BRAND (standalone) | REPLACE (absorbed into EDITORIAL) | Brand-system work fits naturally under layout design. GPT Image 2's brand-from-name emergent capability surfaces cleanly inside EDITORIAL without a separate mode surface. |
| GRID (9-panel single-image grids, Gizem methodology) | REPLACE (absorbed into SERIES) | GPT Image 2's 8-output consistency is the strictly better capability. SERIES handles Instagram grids, moodboards, and campaign grids natively. |

## Cross-cutting patterns

### Anti-paste mandate (Nano Banana)

**Classification**: ADAPT. The anti-paste rule in Nano Banana requires every style transfer to also change angle or pose to prevent a filter-on-top look. GPT Image 2's conversational edit loop handles pose preservation more gracefully, so anti-paste is a recommendation rather than a hard rule. Flagged in EDIT agent.

### "Do not change aspect ratio" tail

**Classification**: REPLACE. This was a Gemini-specific workaround for aspect-ratio drift during edits. GPT Image 2 respects requested aspect ratios natively. Dropped across all modes.

### 120-word cap per prompt (Nano Banana default except brand)

**Classification**: REPLACE. Research shows GPT Image 2 handles dense 300+ word prompts without losing primary subject (the BubbleBrain convenience-store exemplar). Cap lifted; replaced with intent-clarity guidance.

### Fixed 1/3/3/3 distribution (SAFE/INVENTIVE/BOLD/EXPERIMENTAL)

**Classification**: REPLACE with variation-axis detection. This is the single most important replacement. The fixed-matrix approach fails when users ask for a specific axis (angles) and get style variations. Smart diversity via axis detection is the core of every GPT Image 2 sub-agent.

### Diversity enforcement (14 exploration categories)

**Classification**: INHERIT as a toolkit, not a checklist. The 14 categories (angle, medium, character style, time of day, season, era, age, pose, environment, emotion, scale, surreal, narrative, material) are model-agnostic and remain useful for OPEN-axis requests. Each sub-agent may pull from this toolkit when the user's requested axis is itself open-ended.

### AR handling

**Classification**: ADAPT. Nano Banana uses an "AR" suffix at the end of each prompt. GPT Image 2 treats aspect ratio as a natural-language phrase ("Wide 16:9 landscape format") or an API parameter. Prompts drop the suffix convention.

### Upload description discipline ("Using the uploaded [description]")

**Classification**: INHERIT. Ported verbatim. This discipline prevents generic references that drift. Applies to EDIT, SHOW-ME, and COMPOSE.

### 10-prompt output default

**Classification**: REPLACE with 7. The brief specified 7 prompts per query for GPT Image 2. Lower than Nano Banana's 10. Likely reasoning: 7 is under the 8-output Thinking ceiling so each prompt can map cleanly to a single Thinking call; also reduces cognitive load and production cost.

## Preserved exemplar fidelity

Every research exemplar captured in `verbatim-prompt-library.md` is preserved unchanged, with attribution. The sub-agents derive patterns from these exemplars without paraphrasing the originals. This is a direct inheritance of the Nano Banana skill's attribution discipline and the no-fabrication principle.

## Things to revisit in 2 to 4 weeks

As the community builds more muscle with GPT Image 2, revisit:

- **COMPOSE reference-count ceiling**: is it closer to Nano Banana Pro's 14, or does GPT Image 2 degrade sooner?
- **SERIES consistency beyond 8**: are there workarounds (strict visual DNA anchors, reference uploads) that extend the ceiling?
- **TYPOGRAPHY across more scripts**: launch research confirmed 5 non-Latin scripts; how does GPT Image 2 handle Arabic, Hebrew, Thai, Korean Hanja, etc.?
- **Brand logo fidelity workflows**: does uploading a reference logo via EDIT significantly improve fidelity?
- **Thinking-token cost optimization**: can `thinking_level: minimal` produce similar outputs at a fraction of the cost for simpler reasoning tasks?
- **Emergent capabilities**: the 360° equirectangular pattern emerged within 24 hours of launch; what else will surface?

---

## Format ladder upgrade (2026-04 maintenance cycle)

### What changed

The skill originally shipped with one prompt format: natural-language brief with PSGV labels. This worked for ~80% of requests but failed measurably on three categories:

1. Photoreal portraits where the model's beautification stack normalized features the user wanted preserved.
2. Surgical edits where the model "improved" untouched regions.
3. SHOW-ME requests where style drifted alongside the requested angle change.

Investigation revealed that GPT Image 2 is a reasoning model. Structure acts as instruction. Three formats exploit this at three reliability tiers:

- **Tier 3**: NL brief + PSGV labels (default, ~80% of work).
- **Tier 2**: JSON envelope with `forbidden` array + constraint blocks (escalation for anti-drift, anti-normalization, surgical work).
- **Tier 1**: System prompt operating contract (escalation for batch and persistent-role work).

PSGV is encoded in all three formats. The four stages re-encode rather than disappear:
- NL: labeled sections.
- JSON: `plan`, `search`, descriptive keys, `verify`, `forbidden`.
- System prompt: top-line declaration + `<visual_dna>` + `<images>` + `<verify>` blocks. PSGV runs once across the entire batch.

### Files added

- `references/format-ladder.md`: conceptual spine, escalation triggers, when each format wins and loses, ControlNet honesty.
- `references/json-envelope-template.md`: canonical JSON schema, PSGV-to-JSON mapping, forbidden array construction rules, three framework-anonymized exemplars (photoreal preservation, surgical edit, SHOW-ME style lock).
- `references/system-prompt-template.md`: canonical XML-blocked operating contract, PSGV-as-operating-procedure mapping, three variants (SERIES, NARRATIVE, MULTI-OUTPUT), sanity check protocol.

### Agent updates

All 10 active agents updated for format auto-detection:

- **agent-series.md**: system prompt as default. 7 system-prompt templates (wardrobe variations, character reference sheet, product family, emotion set, interior style sheet, storyboard progression, time progression). NL retained as fallback.
- **agent-multi-output.md**: system prompt as default (replaces "restate visual DNA in every PLAN" workaround). One batch prompt holds visual DNA in `<visual_dna>` at the top and per-page specs in `<images>`. NL retained as fallback.
- **agent-narrative.md**: system prompt as default for multi-panel work. 3 system-prompt templates (multi-panel manga, Western comic continuity, storyboard sequence). 7 NL templates retained as fallback.
- **agent-edit.md**: JSON envelope as default. 7 JSON templates (element swap, color variant, background replacement, style transfer, era shift, material transformation, relighting). NL retained for exploratory edits.
- **agent-show-me.md**: JSON envelope as default (fixes the agent's biggest weakness, style drift on angle requests). Forbidden array refuses wardrobe variation, style reinterpretation, lighting change, mood register shift. NL retained as fallback.
- **agent-compose.md**: JSON envelope default for single runs, system prompt for batches. 3 JSON templates (two-subject, subject-in-environment, style-applied-to-subject) plus 1 system prompt template. NL retained as fallback.
- **agent-typography.md**: JSON envelope as default for non-Latin scripts. Forbidden array refuses character corruption, latin substitution, invented glyphs. NL retained as Latin-only fallback.
- **agent-infographic.md**: JSON envelope as default. Forbidden array refuses fabricated data, invented place names, missing structures. NL retained for stylized graphics.
- **agent-editorial.md**: JSON envelope as optional escalation for high-stakes hero shots and brand mark fidelity. NL stays default.
- **agent-create.md**: JSON envelope as optional escalation for portrait, photoreal, and anti-slop subsections. NL stays default.

### Auto-detection logic

Agents read the user's request for escalation signals. If signals are absent, NL default. If signals fire, the agent escalates silently and names the format chosen in the preamble. When two formats are equally viable and the choice meaningfully changes the deliverable, fire `ask_user_input_v0` with format options.

### ControlNet honesty

JSON exemplars in the wild include `controlnet` blocks with `OpenPose`, `ZoeDepth`, `recommended_weight` values. **GPT Image 2 does not run ControlNet.** It reads these fields as instructional cues and role-plays adherence. Documented honestly in skill rather than asserted as literal capability.

### Eval status

Files shipped first per project directive. Evals to follow. Confidence high on conceptual frame and per-mode benefit map. Confidence medium on specific forbidden-array length (25-35 items observed sweet spot, pending eval validation per subject domain).

### Cross-skill inheritance flag for nano-banana-unified

GPT Image 2 and Nano Banana 2 are the same model class (reasoning models that read structure as instruction). The format ladder applies identically to NB2. **Next maintenance cycle for nano-banana-unified should port the same three-format pattern.** The NB2 Collection System (50-prompt collections shipped to Notion hub) would benefit measurably from JSON envelope and system prompt formats for collection-level consistency.

### Things to revisit specifically for the format ladder

- **Forbidden array length sweet spot**: 25-35 items observed. Run evals to confirm per subject domain.
- **System prompt drift past 8 outputs**: confirm whether a fresh batch prompt with identical DNA blocks reliably maintains consistency for outputs 9 through 16.
- **JSON over-constraint freeze threshold**: at what length does the model collapse to flat output?
- **ControlNet field language patterns**: which phrasings of `pose_control` constraints actually produce the strongest reasoning lock?
- **Multi-format compose**: can a single response use NL for some prompts and JSON for others when the variation axis itself crosses the format boundary?

---

## Batch-prompt architectural correction (2026-04 maintenance cycle, follow-up)

### What was wrong

The system prompt operating contract format shipped in the prior maintenance cycle was structurally wrong. It described a sequential workflow:

> "Paste system prompt once at the top of the chat. Then send short per-image briefs sequentially. The model produces one image per brief."

This borrowed chat-system-prompt convention (`<role>`, `<psgv_loop>`, `<constraints>`, `<output_format>`, `<conflict_resolution>`) and treated the system prompt as a session preamble. GPT Image 2's Thinking mode does not work this way. It generates up to 8 outputs per single submission natively.

### What was corrected

Adopted the practitioner-validated batch-prompt structure:

```
Generate [N] separate [aspect ratio] images as a coordinated [task type]. All [N] share one visual DNA. [What varies]. [What holds].

<reference> [optional, for uploaded references] </reference>
<visual_dna> [shared DNA] </visual_dna>
<global_forbidden> [category-level exclusions] </global_forbidden>
<images>
<image_1 subject="..."> [full per-image spec] </image_1>
... through image_N ...
</images>
<verify> [cross-batch consistency checks] </verify>
```

Submit ONE prompt. The model runs PSGV once over the entire batch and returns all N outputs from a single submission.

### Files changed in this cycle

- `references/system-prompt-template.md`: rewritten end to end. Three variants (SERIES, NARRATIVE, MULTI-OUTPUT) restructured. Sanity check protocol updated. Batch-specific failure modes added.
- `agents/agent-series.md`: 7 system-prompt templates restructured (wardrobe variations, character reference sheet, product family, emotion set, interior style sheet, storyboard progression, time progression).
- `agents/agent-multi-output.md`: system prompt template restructured. "Paste once + per-page briefs" framing removed throughout.
- `agents/agent-narrative.md`: 3 system-prompt templates restructured (multi-panel manga, Western comic continuity, storyboard sequence).
- `agents/agent-compose.md`: multi-composition batch template restructured. `<reference>` block added to handle uploaded references explicitly.
- `SKILL.md`: tier 1 description updated, PSGV encoding bullet updated, frontmatter description tightened to reflect batch framing.
- `references/format-ladder.md`: tier 1 row updated, PSGV mapping table updated, "system prompt loses when" reframed.
- `references/failure-modes.md`: removed `constraint cage`, `style bleed across sessions`, `conflict silence`. Replaced with `over-constrained DNA flattens the batch`, updated `drift past 8 outputs` with batch guidance, updated `brittleness from one bad rule`. Added `image inventory length mismatch` and `DNA scope creep into per-image specs`.

### XML blocks removed

The following blocks were borrowed from chat-system-prompt convention and do not apply to image batch prompts:

- `<role>`: image batches do not declare a chat role; the task is named in the top-line declaration.
- `<psgv_loop>`: PSGV is not a per-image loop; it runs once over the batch.
- `<constraints>`: replaced by `<visual_dna>` (positive constraints) and `<global_forbidden>` (negative constraints).
- `<output_format>`: not needed; image count, aspect ratio, and verification are encoded in top-line + `<visual_dna>` + `<verify>`.
- `<conflict_resolution>`: not needed; single-submission batches have no per-image briefs to conflict with the top-level constraints.

### Aspect ratio rule

The canonical pattern is never locked to any specific aspect ratio. In skeleton templates `[aspect ratio]` is a placeholder. In worked examples the ratio is a parameter chosen for that specific use case (4:5 brand campaign, 1:1 social grid, 16:9 storyboard), framed as a choice for the example, never a default for all batch work. Aspect ratio sits inside `<visual_dna>` as one DNA element among others.

### Cross-skill inheritance flag for nano-banana-unified (URGENT)

**`nano-banana-unified` has the same architectural error.** Gemini 3 Pro Image (Nano Banana 2) is the same model class. A reasoning image model that supports multi-output batch generation. The skill's system-prompt format almost certainly inherits the wrong session-style framing.

**Next maintenance cycle for nano-banana-unified must port this batch-prompt correction.** The fix is identical:
- Replace `<role>`, `<psgv_loop>`, `<constraints>`, `<output_format>`, `<conflict_resolution>` blocks.
- Adopt top-line + `<reference>` (optional) + `<visual_dna>` + `<global_forbidden>` + `<images>` + `<verify>` structure.
- Remove all "paste once, send per-image briefs" workflow language.
- Parameterize aspect ratio across all skeletons.

The NB2 Collection System (50-prompt collections shipped to Notion hub) would benefit measurably from the corrected batch pattern for collection-level consistency runs.

### Reference doc

The Notion doc "GPT Image 2: The Reasoning Model That Happens to Make Images" (page ID 34e8f541416681c68bfac83a7cf72740) carries the corrected mental model and a worked brand-campaign example. That doc was corrected in the same cycle as this skill maintenance.
