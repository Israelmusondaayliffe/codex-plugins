# Solver

The general method for problems with more than one plausible answer, in any domain:
strategy, writing, design, prompt architecture, analysis, decisions. BUILD exists only
because code carries extra discipline; everything else runs here. Follow the phases in
order; the discipline is the intelligence.

## Phase 1: Frame

1. Restate the contract in one line (law 1).
2. Ask of the request: is this the right problem? A precise answer to the wrong question
   is the most expensive failure. If the stated problem looks like a symptom, name the
   suspected real problem and confirm direction cheaply before investing.
3. List constraints as hard (violating one invalidates the work) or soft (tradeable).
   List the assumptions you are forced to make and mark each: verify now, or state inline.

## Phase 2: Decompose and explore

1. Split into subproblems with dependencies. Identify the one that is actually binding,
   where difficulty or risk concentrates, and attack it first. Solving easy parts first
   creates fake progress.
2. Generate 2-3 genuinely different approaches (law 2). Different means different
   mechanism or different tradeoff, not the same idea reworded.
3. Pick with stated reasoning: which hard constraint or binding subproblem decides it.
   Record the decisive constraint that eliminated each loser; that record is reusable.

## Phase 3: Execute

1. Convert the quality bar into pass/fail checks before producing (law 3).
2. Build to the plan. Deviating is allowed, silently deviating is not: name the change
   and why.
3. When stuck twice on the same subproblem, stop grinding. Requestion the frame: the
   binding constraint is usually not where you were pushing.

## Phase 4: Verify and deliver

1. Hand the output to `agents/reviewer.md` with the contract line and the checks from
   phase 3.
2. Deliver with: the answer first, the decisive constraints and evidence that picked it,
   stated confidence, and what evidence would change the conclusion.

Before starting phase 1, if a learnings folder exists, check precedent via
`agents/learner.md`. After any non-trivial solve, write the learnings note.
