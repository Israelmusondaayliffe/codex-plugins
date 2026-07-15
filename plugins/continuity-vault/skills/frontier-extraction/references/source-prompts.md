# Source Prompts (adapted)

From Machina, "Do this on your last day with Fable". Em-dashes removed, wording adapted
for reuse beyond the original Fable deadline. Load only the prompt for the move being run.

## Move 1: workspace

```
Read this entire project and how I work in it. Then rewrite my CLAUDE.md as the operating
manual a less capable model would need to work here at your level: the conventions I
follow and the ones you would add; the mistakes a weaker model will make in this codebase,
named, with the rule that prevents each; the quality bar per deliverable, written as
checkable criteria, not adjectives; what to do when uncertain, the exact escalation rules.
Then propose the 3 skills that would save me the most hours, and write them in full.
```

## Move 2: consultant audit

```
Act as the consultant I cannot afford. Audit everything: projects, offers, workflows,
pricing, where my time goes. Deliver a roadmap I can execute with a less capable model:
ranked moves, highest expected return first; per move: why, the exact steps, what done
looks like, what a weaker model needs to be told to execute it; the three things I should
stop doing, with the reasoning written out in full.
```

## Move 3: second brain

The source article gives no paste-ready prompt for Move 3; it links out to a separate
walkthrough. The method lives in `agents/vault-miner.md`.

## Move 4: goal example

```
/goal every module in this repo has a test file, the full test suite passes with the
complete green run pasted in this chat, and a migration-notes.md documents every change.
Or stop after 25 turns and paste the failures.
```

## Move 5: learning law (CLAUDE.md wiring)

```
## learning law
After every non-trivial solved problem, run the extract-approach skill before moving on.
A solution without its learnings note is unfinished work.
```

## The gate, verbatim logic

One question sorts everything: can a cheaper model redo this tomorrow? If yes, skip it.
What passes: a standard written down, a roadmap already reasoned through, a knowledge
vault already distilled, a skill that fires on its own.
