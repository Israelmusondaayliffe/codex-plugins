# Failure Modes

Documented limitations of GPT Image 2 as of launch (April 21, 2026). Each failure mode includes attribution. Flag relevant ones in the preamble of prompts that touch them. Do not attempt silent workarounds.

## Geographic and cartographic hallucination

**Failure**: GPT Image 2 invents fake countries ("Ciger," "Mharee") and misplaces real capitals (Nairobi placed in Saudi Arabia in a launch-day demo map).

**Attribution**: OpenAI launch-day world map demo, confirmed by Gizmodo coverage (Ece Yildirim: "smarter, more precise slop").

**When it bites**: any map prompt, especially multi-region world maps, historical atlases, or educational cartography.

**Mitigation in prompts**:
- Specify the source explicitly ("according to current Wikipedia")
- Name the specific region of interest rather than "world map"
- Ask the model to verify country names and capital cities before rendering
- For high-stakes maps, recommend user verification against an authoritative source

**Affected modes**: INFOGRAPHIC (maps), SEARCH (geographic).

## Brand logo and mark fidelity

**Failure**: GPT Image 2 struggles to reproduce specific brand logos exactly. David Gewirtz at ZDNET reported the model producing a drooping "Z" in the ZDNET logo and, on another attempt, a pre-2022 version of the logo that no longer appears on the site.

**Attribution**: ZDNET hands-on coverage by David Gewirtz.

**When it bites**: any prompt requiring a real brand's current official logo reproduced at fidelity.

**Mitigation in prompts**:
- Flag the fidelity risk in the preamble
- Offer iterative refinement as the workflow
- Suggest uploading a reference of the current logo for EDIT-mode work
- For brand campaigns, frame as "in the spirit of [brand]" when exact reproduction is not required

**Affected modes**: EDITORIAL (brand systems, campaigns), TYPOGRAPHY (wordmarks), EDIT (logo touch-ups).

## Anatomical accuracy

**Failure**: Dense anatomy diagrams may omit structurally necessary features (e.g., muscle attachments missing the bones they attach to, like sternocleidomastoid without clavicle).

**Attribution**: Launch-day community testing on anatomical posters.

**When it bites**: medical education diagrams, scientific anatomy plates, detailed biological illustrations.

**Mitigation in prompts**:
- List the specific anatomical features that must appear as labeled elements
- Recommend Thinking mode for higher logical coherence
- For medical or academic use, flag that outputs should be verified against authoritative references before publication

**Affected modes**: INFOGRAPHIC (anatomy), EDITORIAL (educational posters).

## Consistency drift beyond the 8-output ceiling

**Failure**: Character features, accessories, or environmental details may drift when the user extends a series beyond 8 outputs or across multiple conversational turns.

**Attribution**: OpenAI official ceiling (up to 8 outputs per Thinking-mode prompt). Community reports on drift across sessions.

**When it bites**: any multi-output workflow pushed beyond 8.

**Mitigation in prompts**:
- Hard-cap at 8 outputs per single prompt
- For longer series, specify strict visual DNA anchors in each new prompt
- Recommend single-prompt completion over multi-turn extension when possible

**Affected modes**: SERIES, NARRATIVE (multi-page comics).

## Outdated search defaults

**Failure**: Thinking mode's web search may fetch stale data when the query is not date-specific. A Reddit user (u/PumpkinNarrow6339) reported "today's IPL match" returning a 2024 lineup instead of current.

**Attribution**: r/ChatGPT "ChatGPT Images 2.0 claims real-time data…" thread.

**When it bites**: any current-events prompt without explicit date anchoring.

**Mitigation in prompts**:
- Anchor the date in the prompt ("today, April 22, 2026" or "as of [specific date]")
- Name the specific event or entity with current-year context
- For sports, name the current season or tournament cycle
- For news, name the specific outlet and publication date

**Affected modes**: SEARCH, INFOGRAPHIC (when search-integrated).

## Dense small-text illegibility

**Failure**: Very small text in overcrowded layouts may still be illegible or garbled despite GPT Image 2's typography improvements.

**Attribution**: Launch-day community testing on dense posters and editorial layouts.

**When it bites**: magazine spreads with extensive body copy, dashboards with many small labels, maps with dense toponym labels.

**Mitigation in prompts**:
- Prioritize hierarchy: specify which text must be legible
- Leave breathing room: describe generous spacing
- Break extreme density across multiple outputs via SERIES
- For critical text, place it in a larger scale than decorative text

**Affected modes**: TYPOGRAPHY, EDITORIAL, INFOGRAPHIC.

## Safety filter over-correction

**Failure**: The safety stack occasionally refuses benign prompts involving named public figures even in harmless contexts (community example: "Sam Altman, Donald Trump, and Elon Musk working behind the counter of a busy movie theater" got through, but similar requests are often blocked).

**Attribution**: OpenAI system card (acknowledges safety-filter trade-offs). Community examples from launch-day X threads.

**When it bites**: any prompt naming a real public figure, politically sensitive topic, or religious content.

**Mitigation in prompts**:
- Warn the user that the prompt may be blocked
- Suggest framing that focuses on role ("a software CEO" rather than a named person) if exact identity is not required
- If exact identity is required, mention that reframing may be needed if the first attempt is blocked

**Affected modes**: all modes that name real figures, especially CREATE, EDITORIAL, NARRATIVE.

## Physical reasoning limitations

**Failure**: GPT Image 2 struggles with precise physical reasoning (objects held behind the back, unusual poses, mechanical linkages, architectural load paths). Community side-by-side tests favored Nano Banana Pro on physics-heavy prompts.

**Attribution**: OpenAI official acknowledgment plus community comparison tests on launch day.

**When it bites**: complex action poses, mechanical diagrams requiring accurate linkages, physics-dependent compositions.

**Mitigation in prompts**:
- Simplify the physics where possible
- Recommend Thinking mode for better spatial reasoning
- For critical physical accuracy, suggest Nano Banana Pro as an alternative tool

**Affected modes**: CREATE, INFOGRAPHIC (mechanical), NARRATIVE (action poses).

## Cost variance surprises

**Failure**: Thinking tokens are billed regardless of whether `includeThoughts` is set to true or false. Users pay for the reasoning effort even if they don't see the trace. Some community reports suggest pricing is 60% higher than GPT Image 1.5 for high-quality 1K output ($0.211 vs ~$0.132).

**Attribution**: OpenAI API docs and Developer community threads.

**When it bites**: budget-sensitive workflows, high-volume batch generation.

**Mitigation**: not a prompting issue but a recommendation issue. The skill can suggest Instant mode when latency and cost matter more than reasoning depth. Full pricing table in `api-surface.md`.

## Diagram label incoherence

**Failure**: Some technical schematics produce visually polished but logically incoherent labels (duplicate numbers, contradictory legends).

**Attribution**: Community consensus on technical schematics (less formally documented than other failures).

**When it bites**: technical schematics, circuit diagrams, complex process flowcharts.

**Mitigation in prompts**:
- Specify labels explicitly in quotes
- Limit information density per diagram
- Recommend Thinking mode for logical coherence
- Suggest iterative refinement rather than single-shot generation

**Affected modes**: INFOGRAPHIC (technical diagrams).

## Character face drift in long sequences

**Failure**: In 8-panel pages or multi-page NARRATIVE work, secondary character faces may drift slightly between panels even when protagonist is stable.

**Attribution**: Launch-day manga testing.

**When it bites**: manga or comic pages with multiple named characters.

**Mitigation in prompts**:
- Describe each character's identity markers in detail
- Limit named recurring characters to 3 or fewer for highest fidelity
- Recommend Thinking mode

**Affected modes**: NARRATIVE, SERIES (when series is character-heavy).

---

## Format-specific failure modes

The format ladder introduces its own failure modes, distinct from the model's content failures. Document and mitigate.

## JSON envelope: over-constraint freeze

**Failure**: forbidden array runs too long (50+ items), model produces a flat or generic output to avoid violating any rule. The model's creative reasoning collapses under the weight of refusals.

**When it bites**: portrait work where the prompt author over-specifies. SHOW-ME with too many axis-preservation rules. Editorial work where every imaginable drift is forbidden.

**Mitigation**:
- Cap forbidden array at 25-35 items for photoreal preservation, 8-12 for surgical edits, 12-14 for axis-lock work.
- Group items into category clusters; one category-level item replaces 5 keyword-level items.
- If output flattens, halve the forbidden array and re-run.

**Affected modes**: any mode using JSON envelope, but most acute in CREATE photoreal, EDIT surgical, SHOW-ME style-lock.

## JSON envelope: ControlNet field literalism

**Failure**: prompt author writes `controlnet` block with `recommended_weight: 0.95` and assumes the model has the OpenPose pipeline. It does not. The model role-plays adherence based on the structured field language.

**When it bites**: when the prompt author treats the field as a literal pipeline directive and is surprised by drift.

**Mitigation**:
- Frame `controlnet` blocks as instructional cues in skill documentation.
- Use only when pose, depth, or composition lock matters and NL has failed.
- Do not assert the model runs ControlNet in user-facing context.

**Affected modes**: any JSON envelope with `controlnet` blocks, mainly CREATE portrait and EDIT surgical.

## JSON envelope: verify drift

**Failure**: model claims it verified (filling the `verify` array confirmations) but the output violates a forbidden item. Verification is generated as text, not enforced as a runtime gate.

**When it bites**: any high-stakes JSON run where the user trusts the verification statement as guarantee.

**Mitigation**:
- Treat `verify` as the model's stated intent, not its runtime guarantee.
- Independent post-generation review against the forbidden array still required for high-stakes work.
- Flag this in failure notes when relevant.

**Affected modes**: all JSON envelope use.

## JSON envelope: forbidden under-signal

**Failure**: forbidden item too vague ("bad", "ugly", "wrong"). Model cannot unpack to a category and ignores or interprets unpredictably.

**When it bites**: novice prompt construction copying tag-style negative prompts from non-reasoning models.

**Mitigation**:
- Rewrite each forbidden item as a class of refusals at the category level.
- "bad anatomy" becomes "anatomy normalization, body proportion averaging, dataset-average anatomy, aesthetic proportion correction".
- One vague item is worse than zero. Cut, don't keep.

**Affected modes**: all JSON envelope use.

## System prompt: over-constrained DNA flattens the batch

**Failure**: `<visual_dna>` and `<global_forbidden>` over-specify across the batch. Per-image specs cannot achieve creative variance because every image is filtered through too many shared constraints. Output flattens into repetition with cosmetic surface differences.

**When it bites**: SERIES with very long forbidden lists. MULTI-OUTPUT where the visual DNA includes details that should actually vary per page. NARRATIVE where the character bible includes excessive forbidden patterns that fight the per-panel action.

**Mitigation**:
- Keep `<visual_dna>` to elements that genuinely apply to every image in the batch.
- Cap `<global_forbidden>` at 25-35 category-level items.
- Move per-image variation specifics into the per-image specs inside `<images>`, not into the shared DNA.
- If output flattens, halve the forbidden list and remove the most aggressive DNA constraints, then re-run.

**Affected modes**: SERIES, MULTI-OUTPUT, NARRATIVE, COMPOSE batch.

## System prompt: drift past 8 outputs

**Failure**: even with one batch prompt enforcing visual DNA, the model's hard ceiling is 8 outputs per submission. Requests for 10 or 12 outputs in one prompt return fewer than requested or degrade in consistency.

**When it bites**: long brand campaigns, character bibles with many panels, multi-page systems beyond 8 pages.

**Mitigation**:
- Hard-cap at 8 outputs per single batch prompt.
- For batches larger than 8, submit a fresh prompt with the same `<visual_dna>` and `<global_forbidden>` blocks, and a new `<images>` set for outputs 9 through 16.
- Reference earlier outputs by description in the second batch ("matching the palette from the first batch").
- Accept that consistency across separate submissions is probabilistic, not deterministic.

**Affected modes**: SERIES (high panel count), NARRATIVE (long pages), MULTI-OUTPUT (large page sets).

## System prompt: brittleness from one bad rule

**Failure**: one poorly-written constraint or forbidden item in the shared blocks poisons every output in the batch. Discovered only after the model returns the full set and every image shares the same defect.

**When it bites**: rushed batch prompts shipped without a sanity check on the DNA and forbidden blocks.

**Mitigation**:
- Sanity-check protocol: read every item in `<visual_dna>` and `<global_forbidden>` against the actual drift risks of this specific batch. Cut anything that does not earn its place.
- For high-stakes batches, run a smaller test (3 images instead of 8) with the same DNA blocks, validate, then scale up.
- Read `<verify>` against the planned variation. If verify cannot detect the failure mode you care about, strengthen verify before submitting.

**Affected modes**: all system prompt use.

## System prompt: image inventory length mismatch

**Failure**: the top-line declaration says "Generate 8 separate images" but `<images>` contains only 6 numbered children, or vice versa. The model returns whichever count it chooses, often the smaller, and the user is missing outputs.

**When it bites**: batches edited iteratively where the top-line was set first and image children were added or trimmed without updating the count.

**Mitigation**:
- Count `<image_N>` children before submission. Match the top-line N exactly.
- Treat the top-line declaration and the count of children as two restatements that must agree.

**Affected modes**: all system prompt use.

## System prompt: DNA scope creep into per-image specs

**Failure**: items that should vary per image accidentally appear inside `<visual_dna>`. The model treats them as locked across the batch and the output set flattens. Or items that should hold across the batch appear only in one per-image spec, and the model lets them drift in the others.

**When it bites**: complex DNA blocks where the boundary between "shared across batch" and "varies per image" is fuzzy.

**Mitigation**:
- Test for each DNA item: would I want this exact value on every image in the batch? If no, move it into per-image specs.
- Test for each per-image spec item: should this hold identically across the batch? If yes, lift it into `<visual_dna>`.
- The boundary is the model's contract; place each item on the correct side.

**Affected modes**: all system prompt use.

## Format mismatch: NL where JSON was needed

**Failure**: user requested anti-correction or surgical work, agent shipped NL prompts, model normalized or drifted as predicted.

**When it bites**: agents missing the auto-detection signal in the user's request.

**Mitigation**:
- Re-read `references/format-ladder.md` escalation triggers.
- Train agents to flag preservation language explicitly.
- When in doubt and the request mentions preservation, default to JSON.

**Affected modes**: all modes, most acute in EDIT, SHOW-ME, CREATE photoreal.

## Format mismatch: JSON where NL was wanted

**Failure**: user wanted exploratory creative work, agent shipped rigid JSON envelopes, output came back stiff and over-controlled.

**When it bites**: agents over-applying the JSON default in modes where NL is canonical.

**Mitigation**:
- NL is the default for CREATE, EDITORIAL, exploratory NARRATIVE, casual EDIT.
- JSON is the escalation, not the default for creative-divergent work.
- When the user uses words like "explore," "casual," "give me ideas," stay on NL.

**Affected modes**: CREATE, EDITORIAL, exploratory work in any mode.
