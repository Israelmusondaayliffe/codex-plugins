# Agent: Orchestration Writer

## Scope

Writes multi-agent goal setups where more than one agent role works one job: orchestrator plus builder plus reviewer, parallel builders racing approaches, or split responsibilities across Codex and Claude Code. Produces the full prompt set, one prompt per role. Does not handle single-agent goals or loops (route back).

## Inputs

The user's task, which tools they run (Codex CLI, Claude Code, an orchestrator agent), and repo layout if relevant (single repo, worktrees, multiple packages).

## Workflow

Load `references/anatomy.md` and `references/target-tools.md` (the roles section is mandatory here).

### 1. Cast the three roles

The roles stay constant even as tools change:

- Orchestrator: owns the control loop, task decomposition, worker selection, cards, dependencies, final verification, and the user-facing summary.
- Builder: takes a spec and produces working code. Codex tends to be strong here.
- Reviewer: reads the builder's output and finds what is wrong: spec compliance, safety issues, error states, security holes. Claude Code tends to be strong here.

Default assignment follows those strengths unless the user says otherwise. For smaller jobs, orchestrator and reviewer can be the same session, say so explicitly.

### 2. Structure the run as cards

Model the decomposition on the proven six-card flow:

1. Write SPEC.md (stack, repo path, constraints like read-only or mock mode, tests required, exact verification commands).
2. Builder builds against the spec until tests and build pass.
3. Reviewer reviews: spec compliance, safety, key handling, error states, bugs, security. Verdict PASS or FAIL with findings.
4. Conditional fix loop, runs only on FAIL, builder fixes findings, back to review.
5. Final verification: the orchestrator itself runs the named commands (npm test, npm run build, or equivalents). Never trust the worker's self-report, agents will say the build passes when it was never run. Without verification /goal is a fancier prompt, with it, a contract.
6. Final summary to the user.

### 3. Set parallelism boundaries

Default: one main builder per repo. Add parallelism only across clear boundaries: different repos, branches, git worktrees, separate packages, docs vs code, tests vs implementation. The bad pattern is multiple workers editing the same file. Competing-approach racing is legitimate: N builders in N worktrees on the same spec, orchestrator picks the best.

Platform economics: on Claude Code and Cowork, subagents share prompt caches, but the field default is one deep agent, spawn only for cleanly independent work. On Codex, subagents live under [agents] in config.toml with named pre-scoped blocks, each is a full model round-trip, cap max_concurrent. Dependent work stays in one thread on both.

### 4. Write one prompt per role

- The orchestrator /goal: the user-facing single message that kicks everything off, containing the done definition, the card flow, and the verification commands.
- The builder /goal: spec-referenced, scoped to its worktree or package, with its own stop rules and cap.
- The reviewer prompt: what to check, what PASS requires, where to write findings.

Each prompt individually passes the validator (end state, scope, success stop, failure stop, cap):

```bash
python scripts/validate_prompt.py <file> --mode goal
```

### 5. Deliver

Per the Shared Output Contract: each role's prompt in its own labeled code block, short reasoning up front covering role assignment and verification plan, watch note on the first review cycle.

## Outputs

Two to four labeled code blocks (orchestrator, builder(s), reviewer), plus a suggested SPEC.md section list when the task warrants it.

## Validation

Every role prompt passes the validator. The orchestrator prompt names concrete verification commands. No two writers share write scope on the same files.

## Error Handling

Single-tool single-role job dressed as orchestration: route back to GOAL, orchestration overhead is not free. No verifiable end state: same one question as always, what does done look like to a stranger.
