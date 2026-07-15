# Caching and Persisted Reasoning for GPT-5.6

Two mechanics that changed the economics and quality of multi-turn 5.6 work. Neither is a prompt pattern; both belong in every production migration checklist.

## Explicit prompt caching

### What changed

- GPT-5.6 lets you mark exactly which reusable prompt prefixes OpenAI caches, via explicit breakpoints or `prompt_cache_options.mode: "explicit"`.
- Implicit (automatic) caching still works with no code change.
- **Cache writes are billed at 1.25x the uncached input rate.** Cache reads remain discounted.
- `prompt_cache_retention` is replaced by `prompt_cache_options.ttl`.

### Why it matters

Under automatic caching, every cache write used to be a free bet. At 1.25x write billing, caching a prefix that never gets re-read costs more than not caching it. The break-even depends on the read/write ratio: stable, high-reuse prefixes (system prompts, tool definitions, shared context) win clearly; volatile prefixes (per-request context, rotating examples) can now be net-negative.

### What to do

1. **Track the numbers.** Watch `cached_tokens` and `cache_write_tokens` in usage to understand net cost.
2. **Structure prompts cache-first.** Stable content (system prompt, tool definitions) at the front, volatile content (user context, retrieved documents) after the last breakpoint. This was always good practice; 1.25x writes make it a billing decision.
3. **Go explicit where reuse is predictable.** Use explicit breakpoints or `prompt_cache_options.mode: "explicit"` to avoid unnecessary writes on content you know will not be re-read.
4. **Replace deprecated config.** Any `prompt_cache_retention` usage becomes `prompt_cache_options.ttl`.
5. **Keep implicit where it already works.** No code change is required to keep automatic caching; the review is about whether its writes are earning their reads.

### Lean prompting interplay

A leaner prompt is a smaller cache write and a smaller cache read. The 41-66% token reductions from lean configurations (directional internal figures) compound with caching economics: less to write at 1.25x, less to re-read every turn.

## Persisted reasoning (`reasoning.context`)

### What it is

GPT-5.6 can reuse available reasoning items across turns to improve multi-turn quality and cache efficiency. `reasoning.context` selects the behavior.

| Value | Behavior |
|-------|----------|
| auto (or omit) | Model default; check the response's `reasoning.context` field to confirm the effective mode |
| all_turns | Reasoning from earlier responses is available to later turns |
| current_turn | Earlier reasoning is not reused |

### When to use all_turns

Set `reasoning.context: "all_turns"` when the task's goals, assumptions, and priorities stay stable across turns: long agent sessions, iterative document work, multi-step coding on one feature. The model stops re-deriving context every turn, which improves both quality and cache efficiency.

### When to use current_turn

Set `current_turn` when earlier reasoning is no longer relevant: topic switches, fresh tasks in a recycled conversation, evaluation harnesses where turn independence matters.

### Mechanics

**With `previous_response_id` (simplest):** with `all_turns`, continue the conversation with `previous_response_id` to make reasoning from earlier responses available to the model.

**Managing history manually:** preserve and resend previous user inputs and every response output item. Dropping output items silently drops the reasoning they carry.

**Under `store: false` or Zero Data Retention:** add `include: ["reasoning.encrypted_content"]` to the request and replay the returned encrypted reasoning items in subsequent requests. The reasoning stays opaque to you but available to the model.

### Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Multi-turn quality drop after migration | Reasoning not persisted; model re-derives context each turn | `all_turns` + `previous_response_id`, or full output-item replay |
| ZDR sessions lose reasoning continuity | Encrypted reasoning items not requested or not replayed | Add `include: ["reasoning.encrypted_content"]`; replay the items |
| Stale assumptions carried into a new task | `all_turns` across a topic switch | Switch to `current_turn` or start a fresh conversation |
| Unsure which mode is active | `auto` resolves per model default | Read the response's `reasoning.context` field |

## Interplay with compaction and phase

Persisted reasoning, compaction, and the phase parameter solve different problems and compose:

- **Persisted reasoning** keeps the model's own reasoning available across turns.
- **Compaction** compresses long histories that would exceed context (see `references/long-context-and-compaction.md`).
- **Phase** distinguishes intermediate updates from final answers (see `references/api-parameters.md`).

A long-running agent typically wants all three: `all_turns` for reasoning continuity, compaction at milestones, phase on every intermediate update.

## Migration checklist (5.5 to 5.6)

- [ ] `prompt_cache_retention` replaced with `prompt_cache_options.ttl`
- [ ] `cached_tokens` and `cache_write_tokens` monitored post-migration
- [ ] Stable prefixes at the front; explicit breakpoints considered for high-reuse content
- [ ] Volatile content excluded from cached prefixes
- [ ] Multi-turn workloads evaluated with `reasoning.context: "all_turns"`
- [ ] ZDR flows request and replay `reasoning.encrypted_content`
