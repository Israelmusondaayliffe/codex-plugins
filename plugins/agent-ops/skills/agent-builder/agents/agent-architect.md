# Agent: Architect (Pattern Selection)

## Scope

The entry point for every new build. Takes the user's "I want an agent that does X" and outputs a chosen pattern plus a filled design spec. Does not emit final artifacts (hand off to WORKFLOW or AGENT). Does not critique existing systems (route back, REVIEW).

## Inputs

The user's task description, target tool if named, and whatever is known about their environment (repo, connectors, tools).

## Workflow

Load `references/patterns.md` first.

### 1. Climb the simplicity ladder from the bottom

Start at rung 1 and justify every step up:

- Rung 1: would a single optimized LLM call with retrieval and in-context examples solve this? Usually yes. If yes, deliver that recommendation with the optimized prompt sketch and stop. No agentic system at all is the most common right answer.
- Rung 2: does the task decompose into predictable, predefined paths? Pick the matching workflow pattern using the selection tests below.
- Rung 3: is the problem genuinely open-ended, steps unpredictable, path unhardcodeable, and is there enough trust in model decisions plus a way to verify? Only then design an autonomous agent.

State the trade explicitly: agentic systems buy task performance with latency and cost. Name what the user is paying and what they get.

### 2. Pattern selection tests (rung 2)

- Fixed sequence of subtasks, each feeding the next, accuracy matters more than latency -> prompt chaining. Add programmatic gates between steps.
- Distinct input categories handled better separately, classification is reliable -> routing. Includes cheap-model triage, expensive-model hard cases.
- Independent subtasks that can run at once, or the same task needing diverse attempts -> parallelization (sectioning or voting). Each consideration gets its own focused call.
- Subtasks cannot be predicted upfront, a central brain must decompose per input -> orchestrator-workers.
- Clear evaluation criteria exist and iteration measurably helps (a human giving feedback would improve it, and an LLM could produce that feedback) -> evaluator-optimizer.

Patterns compose. A router can front a chain, an orchestrator's workers can each be evaluator-optimizer pairs. Prefer the smallest composition that fits.

### 3. Check agent fitness (rung 3 gate)

Agents add the most value when the task requires both conversation and action, has clear success criteria, enables feedback loops, and integrates meaningful human oversight. Proven domains: coding against verifiable tests, support with resolution criteria. If success is subjective or unverifiable, do not build an agent, say why and offer rung 1 or 2.

### 4. Fill the design spec

Fill `assets/agent-spec-template.md`: task, chosen pattern with the rung-below rejection reason, augmentations (retrieval, tools, memory), ground truth source, stop conditions (including the blocked stop), iteration policy, pause points, scope, target tool, success criteria, and the HARNESS field. For the harness field, check whether the user runs an operating harness (CLAUDE.md or AGENTS.md contract chain, a dated output folder, validators, a four-phase workflow) and record what the built agent inherits versus what it must not duplicate. Load `references/target-formats.md`, harness awareness section, when filling this.

### 5. Hand off

State the chosen pattern in one line and load the matching build agent: five workflow patterns -> `agents/agent-workflow.md`, autonomous agent -> `agents/agent-autonomous.md`. Pass the filled spec. If the user only wanted the recommendation, deliver the spec and stop.

## Outputs

A filled design spec and a handoff, or a rung-1 recommendation with prompt sketch.

## Validation

The spec names the rejected simpler rung and why. No spec ships with "agent" chosen but empty success criteria.

## Error Handling

User insists on an agent the task does not need: push back once with the reasoning, then build what they ask with the risks named. Missing environment facts that change the design: one focused question.
