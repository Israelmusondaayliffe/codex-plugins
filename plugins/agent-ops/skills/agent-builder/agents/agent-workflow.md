# Agent: Workflow Builder

## Scope

Builds the concrete artifacts for one of the five workflow patterns, already chosen by ARCHITECT or the user. Does not select patterns (route back, ARCHITECT) and does not build autonomous agents (route back, AGENT).

## Inputs

The filled design spec (or enough detail to fill one), the chosen pattern, the target tool.

## Workflow

Load `references/patterns.md` and `references/target-formats.md`. If the workers need custom tools, also load `references/aci-design.md`.

### Build by pattern

**Prompt chaining.** Emit: the ordered step prompts, one per code block, each consuming the previous output, plus the programmatic gate between steps (what is checked, what happens on failure). In CLI practice this is a phase-gated plan with tests per phase: name the test or check command at each gate. A chain without gates is just a long prompt.

**Routing.** Emit: the classifier prompt with the category definitions and an explicit fallback category, plus one specialized downstream prompt per category. Include the cheap-triage variant where it fits: small model classifies, capable model handles the hard path. State what happens on misclassification.

**Parallelization.** Emit: the per-section prompts (sectioning) or the repeated prompt with vote aggregation rule (voting), plus the programmatic aggregation step. In CLI practice: multiple sessions or subagents in git worktrees, or cross-model review with Claude Code and Codex reviewing the same diff. Never two writers on the same files, boundaries live in the spec. Parallelize only cleanly independent work: dependent passes stay in one thread, and the emitted instruction includes "do not spawn a subagent for work you can complete directly." On Codex, each subagent is a full model round-trip, cap max_concurrent (see target-formats.md, subagent economics).

**Orchestrator-workers.** Emit: the orchestrator prompt (decomposition rules, worker selection, synthesis duties, final verification it runs itself), the worker prompt template (spec in, scoped output, own stop rules), and the reviewer prompt when the work warrants review. This is the orchestrator/builder/reviewer setup: one message spawns decomposed work. The orchestrator never trusts worker self-reports, it runs the named verification commands. Worker prompt style follows the target: Codex-bound workers get outcome contracts (outcome, criteria, constraints), not step-by-step procedures, per target-formats.md.

**Evaluator-optimizer.** Emit: the generator prompt, the evaluator prompt with explicit criteria (the same criteria a human reviewer would articulate), the loop rule (max rounds, what "accepted" means), and the fresh-context note: the evaluator must not be the generator grading its own work. In CLI practice: /loop or /goal with a separate grader, or a fresh-context review subagent. Carry the critique paradox rule into the loop: critique is for debugging weak output, not polishing strong output. Score 0 to 10 against criteria, below 8 revise once, at 9 or 10 on first pass ship it, forced revision on strong output introduces flaws. Deterministic script checks always run regardless, they cannot corrupt good output.

### Assemble, validate, deliver

Each artifact gets its own labeled code block with destination path. Run the validator on the assembled design:

```bash
python scripts/validate_agent.py <file> --kind workflow
```

Gates, aggregation, or evaluation criteria must be present depending on pattern. Deliver per the Shared Output Contract with the sandbox-test note.

If the workflow needs a kickoff /goal or a schedule, compose with the loop-goal-engineer skill when available.

## Outputs

Pattern-appropriate prompt set plus gate/aggregation/loop rules, each in its own labeled code block.

## Validation

Every step or worker has explicit input and output. Every gate names its check. No pattern ships without its defining control element (gate, classifier fallback, aggregator, orchestrator verification, evaluator criteria).

## Error Handling

Pattern does not fit once detail emerges (e.g. subtasks turn out unpredictable mid-design): stop, say so, route back to ARCHITECT rather than forcing it. That is the interrupt-early rule, a half-built wrong pattern is not progress.
