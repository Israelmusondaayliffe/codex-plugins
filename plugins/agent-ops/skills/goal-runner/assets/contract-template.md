# Goal Contract

Single source of truth for what done means. The verifier anchors on this file and nothing else. Fill every field.

```
GOAL: [outcome in one sentence]
DELIVERABLE: [exact path(s)]
CREATED: [date] | TARGET: [Cowork / Claude Code / chat] | STATUS: [active / complete / stopped]

## MACHINE CHECKS
[One check per line. These are run by scripts/verify_contract.py. Be greedy,
every criterion here is one that cannot be argued with. DSL below.]
- file_exists: <path>
- section: <path> | <exact heading text>
- contains: <path> | <required string>
- forbid: <path> | <forbidden string>
- min_words: <path> | <N>
- max_words: <path> | <N>
- no_dashes: <path>
- command: <shell command, exit 0 = pass>

## JUDGMENT CRITERIA
[Three to six. Each scored 0-10 by a fresh-context verifier. Write what 8+ looks like.]
1. [criterion]. 8+ means: [specific, observable bar]
2. [criterion]. 8+ means: [specific, observable bar]
3. [criterion]. 8+ means: [specific, observable bar]

## SCOPE
Read: [paths]. Write: [paths, harness output folder when one exists]. Never touch: [paths].

## STOPS
- Success: all machine checks pass and all judgment criteria score 8 or above.
- Failure: if [condition] persists after [N] attempts, stop and report what went wrong.
- Blocked: if no defensible path remains, stop and report what would clear the block.
- Cap: maximum [N] iterations (default 5). Budget: [if relevant].

## ITERATION POLICY
[Per failure type, which knob turns. E.g. machine check X fails -> fix directly.
Criterion 2 below 8 -> revise only the flagged sections against the quoted gaps.
Same check fails twice -> change approach, do not re-run the same fix.]
```

## DSL notes for the contract builder

- `section` matches an exact line in the file (use the full heading, e.g. `## Limitations`).
- `contains` / `forbid` are literal substring checks, case-sensitive.
- `command` runs in the shell with a timeout, exit code 0 passes. Use for tests, builds, and harness validators (e.g. `python SKILLS/_validators/detect_cliches.py <path>`).
- `no_dashes` fails on em-dash or en-dash anywhere in the file.
- Multiple deliverables: repeat checks per path.
