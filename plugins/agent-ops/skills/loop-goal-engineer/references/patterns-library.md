# Patterns Library

Proven, field-tested templates. Adapt these instead of writing from scratch when the task matches. Sourced from a field-tested loop and goal engineering collection.

## Contents

- Three steal-worthy templates: research brief goal, content audit goal, weekly report loop
- The full research loop with quality gate and CLAUDE.md
- A first /goal for beginners
- The eight loop skeletons: ingest (3), build (2), improve (3)

## Template: the research brief (/goal)

For understanding a new tool or topic well enough to write about it.

```
/goal Research [TOPIC] and produce a comprehensive brief saved to /research/[topic]-brief.md.

The brief must include:
- A 3-sentence plain-English summary
- Key capabilities (with specific examples, not vague claims)
- Pricing or access details
- 3 practical use cases for non-technical users
- Limitations or drawbacks (be honest, no marketing language)
- Sources for every major claim

Only create files in /research/.
Stop when all 6 sections are complete and every claim has a source.
If you can't verify a claim after 3 attempts, flag it as unverified.
Maximum 20 iterations.
```

## Template: the content audit (/goal)

Replaces a manual spreadsheet task.

```
/goal Audit all markdown files in /content/drafts/.

For each file, extract:
- Title
- Main topic
- Target audience (beginner / intermediate / advanced)
- Whether it includes a practical example (yes/no)
- Whether it includes a copy-paste prompt or template (yes/no)

Save the audit as a table in /content/audit-results.md.

After the table, add a "Gaps" section listing:
- Topics with no beginner-level content
- Posts that have no practical example
- Any topic covered more than twice

Only read from /content/drafts/. Only write to /content/audit-results.md.
Stop when every file has been processed and the gaps section is complete.
```

## Template: the weekly report (/loop, scheduled)

```
/loop Every Monday at 9 AM,
read all files updated in the past 7 days in /notes/,
produce a weekly summary saved to /reports/weekly-[date].md with:
- What got done (list of completed items with dates)
- What's still open (items mentioned but not marked complete)
- Decisions made (any file containing "decided" or "decision")
- Top 3 priorities for this week (based on frequency of mention)

Keep the report under 500 words.
Only read from /notes/. Only write to /reports/.
Stop after producing the report.
```

## The full research loop, three set-once pieces plus the loop

CLAUDE.md, set once: research style comprehensive, cited, no fluff; output format markdown with clear headers; never create files outside /research; preferred sources primary and reputable; max budget per session 3 dollars.

Quality-gate skill, set once:

```
/skill verify-research: before marking any section complete, confirm every major claim has a source, every section has at least 3 supporting data points, and there are no obvious gaps. Never hand back thin research.
```

The loop:

```
/loop every 30 minutes,
only touching /research/brief.md,
stop after 10 iterations or if the same search query appears 3 times in a row without new information surfacing,
use the verify-research skill after each section is drafted,
use a verifier agent to check source quality and coverage completeness at the halfway point and before final submission,
and keep a memory file at /research/progress.md that logs what sections are done, what sources have been used, and what angles still need coverage, read it at the start of every run and update it at the end.
Topic: [your topic here]
```

## A first /goal, for users new to the primitive

```
/goal Research the top 5 open-source AI tools released in the past 30 days. For each tool, find: name, what it does in one sentence, GitHub star count, and one specific use case.
Save the results to /research/ai-tools-june.md as a clean table.
Stop when all 5 entries are complete with sources.
If you can't find reliable information for a tool after 3 attempts, skip it and note why.
```

The lesson it teaches: you did not tell the agent how to research, you told it what done looks like.

## The eight loop skeletons

Rule that holds for all eight: every loop starts life as a skill built and run by hand first. Build the skill, prove it, then automate. Never put something on a timer that has not been watched running at least once.

### Group 1: loops that feed the system (the data is the moat)

1. Data ingestion loop. Reads the last 24 hours across connected sources, discards noise, stores only what changes a decision:

```
Build me a skill called /data-ingestion-loop.
Sources: Slack, Gmail, call transcripts.

On each run, read the last 24 hours from each source.
Strip the fluff. Keep only what changes a decision:
numbers, commitments, new facts.

Write the clean result to my notes folder, one dated file per run.
Skip anything you have already stored.
```

Connect sources once via connectors, run by hand a few days, then schedule every morning.

2. External alpha farming loop. Alpha is the non-obvious input that makes output different from the default everyone else gets:

```
Build me a skill called /alpha-farming-loop.
Alpha I'm farming: [what makes my output different].
Sources: [YouTube creators / newsletters / forums I trust].

On each run, pull those sources and keep only the level-2 insight:
the non-obvious take most people skip,
not the basics every model already has.

File each one with a citation.
Store run history so we don't re-pull the same source.
```

Point it at a scraping MCP (like Firecrawl) for clean web reads. The level-two filter is the whole game.

3. Internal alpha farming loop. Hunts inside the user's own system for patterns and gaps, outputs actions, not a report:

```
Build me a skill called /internal-alpha-loop.
Read everything already in my system from the last two weeks.

Surface the patterns I keep missing:
what keeps coming up, where the gaps are.

Output an action list, not a report.
Every item is one concrete thing I can do next.
Run each proposed plan through /plan-verification before you show me.
```

/plan-verification is a small utility skill worth building once: it interviews the user about tools they use and will not touch, then checks every plan against that.

### Group 2: loops that build faster

4. Optimization loop, for goals that are a number. The feedback window does not have to be instant, a day-long cycle is still a loop. Candidates: load time, cost per run, test coverage, cold-sequence reply rate:

```
Build me a loop called /optimize-loop.
Goal: [one objective metric and its target, e.g. homepage loads in under 2 seconds].

On each run: measure the metric, propose one change,
apply it, measure again.

Keep going until the number hits the target
or you have tried five changes.
Log every attempt and its result so the next run picks up where this one stopped.
```

5. Code build loop, for shipping a product, plan before touching anything:

```
Build me a loop called /code-build-loop for [what I want to build].

1. Pull in the goal, by interview or from a doc I give you.
2. Plan the delivery in plan mode.
3. Stop and wait for me to sign off on the plan.
4. Build it.
5. Review the code with /code-review-fix.
6. Verify the result matches the goal with /verify.
```

Two transferable ideas: the approval gate (step 3 stops on purpose where a wrong turn poisons everything after, put a gate wherever a wrong call would ruin the rest of the run), and letting the loop pick the documented agent-splitting pattern rather than designing it by hand.

### Group 3: loops that improve the system itself (where the compounding lives)

6. Improve-system loop, twice a week:

```
Build me a loop called /improve-system-loop. Run it twice a week.
Read my recent sessions. Find what slowed me down or repeated.

Propose changes, sorted into three buckets:

- Auto-approve: low-risk fixes. Apply them and log to changelog.md.
- Needs sign-off: skill edits, new skills, structural changes.
  Write these to a review file as a checklist I approve or reject.
- More context needed: anything you can't decide alone.
  Add it to the same review file.
```

Auto-approve is the self-improving part, needs-sign-off keeps the user as taste-maker. The changelog matters: a loop with no memory of what it changed cannot improve.

7. Ecosystem monitoring loop, the loop that watches the other loops:

```
Build me a loop called /ecosystem-monitoring-loop that manages my other loops.

On each run:
1. Discover: scan .claude/skills/ for every *-loop,
   read its frontmatter, build a live registry.
   New loops register themselves.
2. Health check: read each loop's run-log,
   see what ran and what failed.
   Fix failures first, escalate only what needs me.
3. Composability: find logic repeated across two or more loops
   and pull it into one skill they can all call.

Run weekly.
```

The composability step is quietly the most valuable: as loops multiply, two end up doing the same thing, and this refactors the repeat into one shared skill. Discovery by naming convention means new loops join the monitor automatically.

8. North star loop, the compass:

```
Build me a loop called /north-star-loop.
My goals: [the real ones, e.g. ship two paid products, land 12 clients].

On each run: read my session history and loop results,
and map where I'm actually heading.

Tell me where I land in six months if nothing changes.
If I've drifted, name what's pulling me off
and the one change that corrects it.
```
