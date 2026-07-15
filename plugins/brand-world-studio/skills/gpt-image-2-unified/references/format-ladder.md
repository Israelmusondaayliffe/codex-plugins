# Format Ladder

Canonical decision spine for prompt format selection. Every agent reads this when format escalation signals fire. Three formats, one ladder, one rule: escalate only when the request earns it.

## The three formats

GPT Image 2 is a reasoning model. That makes structure act as instruction, not just description. Three formats exploit this at three different reliability tiers:

| Tier | Format | What it controls | Reliability rung |
|---|---|---|---|
| 3 | Natural-language brief + PSGV labels | Intent, texture, atmosphere | High (advisory). Default for ~80% of work. |
| 2 | JSON envelope with `forbidden` array + constraint blocks | Anti-drift, anti-normalization, role separation, surgical exclusion | Higher floor. Wins when the model's own correction instinct is the enemy. |
| 1 | System prompt operating contract (XML-blocked) | Batch generation of up to 8 coordinated outputs from a single submission, multi-image consistency, embedded PSGV across the batch | Highest floor for multi-image runs. One prompt in, the entire batch out. |

Natural-language stays the default. JSON and system-prompt are escalations, not replacements.

## PSGV across all three formats

PSGV does not get abandoned. It re-encodes per format. The same four stages run regardless of which format the agent ships:

| Stage | NL format | JSON format | System prompt format |
|---|---|---|---|
| PLAN | Labeled section "PLAN: ..." | `"plan"` JSON key | Top-line declaration + `<visual_dna>` block |
| SEARCH | Labeled "SEARCH: ..." or SKIP | `"search"` key with trigger or `null` | Optional `<search>` block, positioned before `<visual_dna>` when active |
| GENERATE | Labeled "GENERATE: ..." (the brief) | `"subject"`, `"environment"`, `"camera"`, `"lighting"`, `"mood"`, `"style"`, `"palette"`, `"quality"`, `"aspect_ratio"` keys | `<visual_dna>` + `<images>` together. Visual DNA filters every per-image spec inside `<images>`. |
| VERIFY | Labeled "VERIFY: ..." | `"verify"` key (checklist array) | `<verify>` block (positive checks) + `<global_forbidden>` block (negative checks) |

If you cannot encode all four stages in the chosen format, the format is wrong for the request. Drop down a tier or rebuild.

## Auto-detection: when to escalate

Agents read the user's request for these signals. No need to ask. If the signals are absent, default to NL.

### Escalate to JSON envelope when:

- **Anti-correction signals**: anatomy, body proportions, asymmetry, specific physical features the user wants preserved against beautification drift, "do not normalize," "do not stylize," "preserve as-is," explicit body or feature description that the model's safety stack might soften.
- **Surgical edit signals**: "do not change X," "leave Y untouched," "only modify Z," targeted preservation language.
- **Style-lock-on-angle signals**: SHOW-ME requests where the user explicitly wants angle variation but identical style, lighting, environment. Forbidden array enforces what NL cannot.
- **High-stakes single output**: portrait realism with skin and material specificity, brand-critical hero shot, single editorial poster the user will publish.
- **Multi-reference role separation**: COMPOSE with three or more references where each plays a defined role (subject, style, environment) and cross-bleed is the failure mode.
- **Anti-hallucination signals**: INFOGRAPHIC with specific data labels, TYPOGRAPHY with non-Latin scripts where character corruption is likely.
- **User explicitly names the format**: "give me a JSON prompt," "use the forbidden array pattern," "structured prompt format."

### Escalate to system prompt operating contract when:

- **Batch volume signals**: SERIES count of 4+, MULTI-OUTPUT page sets, NARRATIVE multi-panel work, COMPOSE batches of 3+.
- **Persistence signals**: "across all of these," "every image in this set," "for this entire shoot," "consistent throughout."
- **Visual DNA signals**: brand system, design bible, character bible, style guide, design system, shared aesthetic across distinct deliverables.
- **Character continuity signals**: same character across panels, same product across variants, same protagonist across story beats.
- **User explicitly names the format**: "system prompt for the model," "operating contract," "set the role then generate," "use a meta-prompt."

### Stay on natural-language when:

- Single image, conversational request, no preservation hostility, no batch.
- Exploration mode, fast iteration, no commitment to constraint.
- The user is testing creative ideas, not shipping production output.
- Agent default unless an escalation signal explicitly fires.

## When each format loses

Honesty pass. No format is universally better.

### NL loses when:
- Anatomy or feature preservation matters and the model's correction instinct will override soft positive language.
- Multiple images need consistent constraints; restating per image creates drift through paraphrase.
- The user has a strict exclusion list at the category level; positive prompting cannot encode "do not normalize."

### JSON loses when:
- The request is exploratory or creative-divergent; rigid schema kills the texture that NL captures.
- Forbidden array gets too long (rough sweet spot 25-35 items based on observed exemplars; longer arrays may flatten priorities, shorter may under-constrain). This is testable, not proven. Confidence: medium.
- The brief is poetic, mood-driven, or atmospheric; JSON fields fragment the unified read.

### System prompt loses when:
- The user wants a single image. The batch structure is overhead for one output.
- The constraint regime should genuinely change between images. Batch DNA enforces uniform constraints across the set; if every image needs a different regime, ship separate prompts.
- The brief is exploratory and the user wants free creative direction per generation rather than a coordinated coherent set.

## Format encoding rules

Hard rules across all formats:

1. **Every prompt in its own triple-backtick code block.** JSON in ` ```json `, system prompts in plain ` ``` `, NL in plain ` ``` `.
2. **PSGV always present.** Encoded per format. If a stage doesn't apply (SEARCH SKIP), state it explicitly.
3. **Variation-axis preamble unchanged.** Whatever format the prompts use, the response opens with the axis statement.
4. **7 prompts unless mode-specific override.** SERIES exceptions where one prompt = one consistent multi-output run. MULTI-OUTPUT exceptions where one prompt = one page from a 7-page set.
5. **Aspect ratio stated in every format.** NL phrase ("Vertical 9:16"), JSON `aspect_ratio` key, system prompt `<visual_dna>` block (aspect ratio is one DNA element).

## ControlNet fields: instructional, not literal

Some JSON exemplars in the wild include `controlnet` blocks naming `OpenPose`, `ZoeDepth`, with `recommended_weight` values. **GPT Image 2 does not run ControlNet.** It reads these fields as instructional cues and role-plays adherence. They function as structured constraint statements, not as literal model controls.

Teach this honestly. Use `controlnet` blocks when they help the model reason about pose lock, depth lock, or composition lock, but never assert that GPT Image 2 has ControlNet. The mechanism is reasoning over structure, not pipeline integration.

## Format selection: silent or surfaced?

Default: **silent auto-detection.** The agent reads request signals, picks a format, ships. Preamble names the format chosen ("Format: JSON envelope") so the user can see it without being prompted.

When two formats are equally viable and the choice would meaningfully change the deliverable, fire `ask_user_input_v0` with format options. This is rare. Only when the request is genuinely ambiguous between, say, "8 portraits one constraint set" (system prompt) and "8 portraits explored creatively" (NL with diversity).

## Cross-skill inheritance flag

The same format ladder applies to nano-banana-unified. Same model class (Gemini 3 Pro Image / NB2), same reasoning capability, same structural exploitation. When this skill ports its format ladder, the inheritance log records the move and the next maintenance cycle ports the same patterns to nano-banana-unified.
