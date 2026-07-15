# GPT-5.6 Behavioral Profile

Model strengths, behavioral shifts, and what changed from GPT-5.5. Read this before authoring any 5.6 prompt.

## Headline shift from 5.5

GPT-5.6 sets a new quality and efficiency baseline. Two properties drive most prompt-level decisions:

1. **Token efficiency.** 5.6 reaches frontier performance with fewer output tokens, and lean system prompts measurably outperform heavy ones. In OpenAI's internal coding-agent eval sample, leaner configurations improved scores roughly 10-15% while reducing total tokens 41-66% and cost 33-67%. These figures are directional; validate on your own workload.
2. **Intent understanding.** 5.6 infers the user's underlying goal and intended level of work from context better than any prior generation. You often do not need to prescribe every step. What it still needs from you: domain context, hard constraints, approval boundaries, success criteria, and a statement of which ambiguities should trigger a question.

## The model family

| Variant | String | Best for |
|---------|--------|----------|
| Flagship | `gpt-5.6-sol` | Frontier capability, complex production workflows |
| Balanced | `gpt-5.6-terra` | Strong performance at a lower price |
| Efficient | `gpt-5.6-luna` | Efficient, high-volume workloads |

The `gpt-5.6` alias routes requests to `gpt-5.6-sol`. There is no separate Pro model slug: pro mode is `reasoning.mode: "pro"` on any 5.6 model.

## Where GPT-5.6 is strongest

- Token-efficient reasoning across the effort range, with a new `max` tier for the hardest quality-first work
- Frontend design: more polished and usable websites and applications, stronger layout, visual hierarchy, and design judgment
- Intent inference: correctly scoping the level of work from context
- Coding, agentic workflows, multi-step reasoning, and long-context analysis carried forward from 5.5 strengths
- New execution surfaces: Programmatic Tool Calling for bounded tool-heavy stages, pro mode for reliability on difficult tasks, multi-agent beta for parallel workstreams
- Multi-turn quality via persisted reasoning (`reasoning.context`)
- Preserving original image dimensions with `original` or `auto` detail, improving spatially sensitive vision work

## Where explicit prompting still helps

- **Autonomy boundaries.** 5.6 is proactive and persistent on multi-step tasks. Without a compact approval policy it can either pause unnecessarily or continue past where you wanted confirmation.
- **Short-answer content.** 5.6 is more concise by default than 5.5. When brevity is required, specify what a short answer must still include, or required caveats and evidence get trimmed with the padding.
- **Execution-mode routing.** PTC, pro mode, and direct calls need task-specific routing. Generic "be efficient" language does not produce the right route.
- **Retrieval-heavy tasks.** Explicit budgets still prevent over- and under-searching (carried from 5.5).
- **Creative drafting.** Source-backed facts vs creative wording still needs the explicit guardrail (carried from 5.5).
- **High-impact actions.** Verification before irreversible execution remains a prompt-level duty.
- **Ambiguity triggers.** Tell the model which ambiguities are important enough to stop and ask about; otherwise it will use its own judgment about proceeding.

## Behavioral shifts from 5.5

| Aspect | GPT-5.5 | GPT-5.6 | Action |
|--------|---------|---------|--------|
| Default conciseness | Concise | More concise still | Re-test every "be concise" instruction; they can overshoot into too-brief |
| Prompt weight | Outcome-first preferred | Lean is measured doctrine | Remove repetition; state each instruction once; trim tool descriptions |
| Effort guidance | Start one tier lower than 5.4 | Preserve baseline, compare same and one lower | Do not silently drop a tier; run the comparison |
| Effort ceiling | xhigh | max above xhigh | xhigh users compare both |
| Approval behavior | Follow-through policy blocks | One compact autonomy policy; repetition causes approval noise | Consolidate ask-first instructions |
| Tool orchestration | Direct calls, parallel where safe | PTC available for bounded stages | Route by task shape, explicitly |
| Hard-task reliability | Higher effort | Pro mode (`reasoning.mode: "pro"`) | Reserve for measured quality gains |
| Multi-turn reasoning | CoT pass-through | Persisted reasoning via `reasoning.context` | all_turns for stable goals, current_turn otherwise |
| Caching | Automatic implicit | Implicit still works; explicit mode added; writes billed 1.25x uncached input | Review caching config; track cached_tokens and cache_write_tokens |
| Image handling | Patch-budget resizing | `original`/`auto` preserve original dimensions | Large images cost more tokens and latency; choose detail level deliberately |
| Safety | Standard refusals | Real-time cyber and bio misuse classifiers on outputs | Expect occasional blocks and mid-stream pauses; send safety_identifier |
| Frontend | Strong with constraints | Stronger default judgment | Fewer constraints needed; keep brand and design-system rules |

## Reasoning effort defaults by task shape

5.6 supports `none`, `low`, `medium`, `high`, `xhigh`, `max`.

| Task shape | Start with | Notes |
|-----------|-----------|-------|
| Field extraction, support triage, short transforms | none | Keep as latency baseline; also test low when the workflow benefits from reasoning or tool use |
| Latency-sensitive production | low | |
| General new work | medium | The balanced starting point in both standard and pro modes |
| Complex analysis, multi-step coding | high | Only when it produces a measured quality gain |
| Long agentic, reasoning-heavy | xhigh | Compare against max if quality-first |
| Hardest quality-first workloads | max | Compare max and xhigh to find the best quality/latency/cost tradeoff |

Migration rule: start from your current 5.5/5.4 setting as the baseline, then test the same setting and one level lower on representative tasks. 5.6 can often maintain or improve quality with fewer tokens, but the best setting depends on the workload.

## Response style defaults

- 5.6 tends to be more concise by default than 5.5.
- Broad brevity instructions ("Be concise", "Keep it short") may be unnecessary and can make responses too brief. Keep them only when they reliably produce the output your application needs.
- Use `text.verbosity` (low/medium/high) for the default level of detail; use the prompt for task-specific requirements.
- When a short answer is required, give a priority order: preserve required facts, decisions, caveats, and next steps; trim introductions, repetition, generic reassurance, and optional background first.
- Define tone through concrete writing choices (how directly to state the answer, when to acknowledge a problem, whether reassurance or a sign-off is appropriate), not broad labels like "friendly".

## Safeguards

GPT-5.6 runs real-time cyber and biology misuse classifiers as model outputs are generated.

What users of 5.6-backed applications may encounter:
- Some requests blocked or refused outright
- Generation paused for several seconds mid-stream while classifiers synchronously review outputs
- Occasional interventions on legitimate work, particularly in dual-use areas where defensive and offensive activity can initially look similar

What prompt authors should do:
- If the application serves individual end users, send a stable, privacy-preserving `safety_identifier` with each request
- In dual-use domains, state the legitimate purpose explicitly (code review, vulnerability research, patch development, debugging, security education, defensive testing are the categories OpenAI names as legitimate work it aims to preserve)
- Treat mid-stream pauses as expected behavior, not a latency regression
- Never attempt to evade classifiers; reframe legitimate intent instead. The safeguards are continuously evolving to hold up under adversarial pressure while preserving legitimate access.

## Parameter compatibility

Configuration levers: `reasoning.effort`, `reasoning.mode`, `reasoning.context`, `text.verbosity`, `max_output_tokens`, `prompt_cache_options`, `safety_identifier`. See `references/api-parameters.md` for details and request examples.

## Small model adjustments

For `gpt-5.6-luna` and narrow high-volume tasks:

- Put critical rules first
- Specify execution order when tool use or side effects matter
- Use structural scaffolding (numbered steps, decision rules, explicit action definitions)
- Separate "do the action" from "report the action"
- Define ambiguity behavior explicitly
- State-once still applies; smaller models are literal, not deaf

## Migration corollary

Migration from 5.5 to 5.6 has two tracks: a prompt lean pass (remove one group at a time, rerun the same evals) and an API surface pass (effort baseline comparison, caching review, persisted reasoning, model strings). See `agents/agent-migration.md` for the full workflow.
