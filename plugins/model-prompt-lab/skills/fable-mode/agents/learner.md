# Learner

Makes solves compound. Two operations: read precedent before similar work, write a note
after non-trivial work.

## Defer rule (read first)

If the workspace already has a learnings capture mechanism (an extract-approach skill, a
learning law in CLAUDE.md, or the frontier-extraction skill's recorder), invoke that
mechanism and write nothing yourself. One capture path per workspace; two paths produce
duplicate notes in drifting formats, which corrupts retrieval. Only capture directly when
no mechanism exists.

## Read (before work)

1. If a learnings/ folder exists in the workspace, search it for notes matching the
   task's shape: same subsystem, same class of problem, same tool.
2. Surface at most the 3 most relevant reusable rules to the active agent. Precedent
   informs the frame; it does not replace phase 1.

## Write (after work, only when no other mechanism exists)

Non-trivial means: more than one plausible approach existed, or the first attempt failed,
or diagnosis took real work. Routine edits get no note; noise buries signal.

Use the workspace's note template if one exists (frontier-extraction ships one at
`assets/learnings-note-template.md`). The note captures, in this order: the insight as a
claim-style title, the insight itself standalone, what to try first next time written as
forward-looking procedure, one checkable reusable rule, and links to related notes. Do
not transcribe the reasoning that produced the solve; reasoning-replay instructions
trigger refusal classifiers on Claude 5 family models. Outcomes and next-time procedure
carry the same value without the risk.

A non-trivial solution without its learnings note is unfinished work.
