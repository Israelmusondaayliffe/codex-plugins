# Completion Doctrine

The rules that make "done" mean something. Load in every mode.

## The stranger test

A goal is verifiable when a stranger with only the contract and the artifact could confirm completion without asking the author anything. Every contract passes this test before execution begins. Tasks that cannot pass it after one reshaping attempt are not run, "make it better" is not a goal.

## The machine/judgment split

Push every criterion as far down the reliability ladder as it goes: deterministic script first, template second, instruction last. A script either passes or fails, no interpretation, and it cannot corrupt good output. Judgment criteria are the residue that genuinely requires reading, keep them few (three to six) and write each with what an 8-or-above looks like. The compounding math enforces this: at 95 percent per-step reliability a 15-step workflow succeeds end to end roughly 46 percent of the time. Few, coarse iterations with deterministic gates beat many fine ones with felt judgment.

## The four stops

1. Success: all machine checks pass, all judgment criteria at 8 or above.
2. Failure: a named condition persisting after N attempts, reported with what went wrong.
3. Blocked: no defensible path remains under current limits, reported with what would clear the block. Distinct from failure: blocked means the run needs something from outside (input, access, a decision), not another attempt.
4. Cap: a hard iteration maximum (default 5 in-session) and a budget where relevant. Reaching the cap is not completing the objective, it is a stop that reports honestly.

## Iteration policy

The contract states how attempt N+1 differs after each failure type: which knob turns, what evidence triggers which change. Retries without a policy repeat the same guess with fresh confidence. The progress file is the policy's memory, a loop that cannot see its own attempts cannot improve.

## The truthful-progress rule

Before any progress claim is reported or logged: audit it against a tool result from this session. Work you cannot point to evidence for is reported as unverified. Failing tests are reported as failing, with output. Skipped steps are reported as skipped. This instruction nearly eliminated fabricated status reports in Anthropic's long-run testing, it carries more completion assurance per line than anything else in this skill.

## Fresh-context verification

Self-critique is the builder grading its own work: the working narrative ("I did X so X is done") contaminates the verdict. The verifier receives only the contract and the artifact. That independence is why separate fresh-context verifiers outperform self-critique in long-run harnesses, and why the native Claude Code /goal design uses a separate model as its grader. A verifier that edits, inherits the builder's context, or reads the builder's reasoning is not a verifier.

## The critique paradox

Critique is for debugging weak output, not polishing strong output. Score 0 to 10 per criterion. Below 8: revise once against the named gaps, re-verify. At 8: one revision pass is allowed if specific gaps are named, otherwise ship. At 9 or 10 on the first pass: ship immediately, forced revision on already-strong output tends to introduce flaws rather than remove them. Deterministic checks are exempt, they always run and cannot damage anything.

## Turn-ending discipline

A turn does not end on a plan, a promise, a question the files can answer, or a list of next steps. If the last paragraph describes undone work, the work happens now. Mid-run pauses are reserved for destructive or irreversible actions, real scope changes, and input only the user can provide. Everything else proceeds under the approved contract, the contract is the permission.

## State lives in files

Context is lossy (compaction, session ends). The contract and progress files are the run's production state: durable, addressable, resumable. Anything load-bearing that exists only in context is one compaction away from gone.
