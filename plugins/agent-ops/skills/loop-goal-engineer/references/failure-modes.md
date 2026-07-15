# Failure Modes and Judgment Calls

Load in every mode. Mandatory in DIAGNOSE.

## The five mistakes that waste time and tokens

1. No failure stop. A real loop ran 40+ minutes on a problem that needed human input. Fix: always add "if this fails after 3 attempts, stop and tell me what went wrong."
2. Scope too wide. A real loop created 11 files across 4 unexpected directories and overwrote manual notes. Fix: explicit read scope and write scope, "do not create files outside [dir]."
3. Vague goal. "Research competitors and write a summary" produced unusable generic output. Fix: specify which competitors, what criteria, what counts as complete.
4. Not watching the first cycle. One loop misunderstood the intent in iteration one and built on a wrong foundation for 12 more. Fix: watch cycle one, or add an approval gate after the plan step.
5. Using loops for simple tasks. Goal-checking overhead makes single-prompt tasks slower. Fix: recognize which tasks are loop-shaped and leave the rest as prompts.

## Where loops do not work

Quick questions. Creative work needing the user's judgment at every step. Tasks where done is subjective ("make this better" is not verifiable). Anything requiring real-time decisions the user has not made yet.

The honest field assessment: after three weeks of daily use, loops handled 30 to 40 percent of usage, the rest stayed regular prompting, and that is fine. The value is recognizing which tasks are loop-shaped. This skill should say "not loop-shaped" without apology when that is the truth.

## Pro tips to bake into recommendations

- Start with /goal before /loop. Same behavior, easier to reason about. Recommend this to anyone running their first loop.
- Spend most of the design time on the deliverable definition, not the mechanics.
- Default reasoning effort to high. Reserve xHigh, Max, and Ultracode for complex builds.
- Deploy subagents inside loops, each starts with a fresh context window.
- Always cap with a hard iteration limit and a dollar budget.
- Run /compact manually before long sessions.
- Loops work far beyond code: writing, research, and unconventional non-coding tasks.
- Never trust the worker's self-report. The orchestrator or the user runs the verification commands. Agents are confident, they will report a passing build that was never run.
- Every loop starts life as a skill run by hand. Prove it, then put it on a timer. A wrong loop repeats the same mistake faster.
- Token economics: CLAUDE.md and rules files are paid for on every beat of the loop. Keep them to constraints only.

## The approval gate principle

Put a stop-and-wait step wherever a wrong call would poison everything after it: plan sign-off before build, spec sign-off before parallel builders launch, first-section review before a long research run. Gates are cheap, wrong foundations are not.
