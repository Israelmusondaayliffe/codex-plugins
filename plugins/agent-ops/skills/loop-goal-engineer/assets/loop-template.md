# Loop Template

Fill every bracket. All six parts are required, a loop missing one is an agent guessing in a circle.

```
/loop [Trigger: every <interval> / Every <day> at <time> / verifiable end state for self-paced],
only touching [write scope], only reading from [read scope if different],
stop after [N] iterations or [failure/no-progress condition, with numbers],
use [named skill] at [named checkpoint],
use a verifier agent to [what it checks] at [halfway point / before final submission],
and keep a memory file at [path] that logs [what is done, what was used, what remains],
read it at the start of every run and update it at the end.
[Task specifics: topic, metric and target, sources, output path and format.]
```

Set-once companions, each in its own code block when the loop needs them:

Quality-gate skill:

```
/skill [name]: before marking any [unit] complete, confirm [specific quality bars].
Never hand back [the thin version of this work].
```

CLAUDE.md lines (constraints only, every line is paid for on every beat of the loop):

```
[style constraint]
[output format constraint]
[scope constraint]
[source preference]
[budget cap per session]
```

Checklist before delivery: all six parts present, trigger explicit or deliberately self-paced, both stops plus cap with numbers, memory read-and-update phrasing included, no em-dashes, watch note recommends observing the first cycle.
