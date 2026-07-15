# Goal Progress Log

Read at the start of every iteration, appended at the end. This file is what makes retries non-repeating and runs resumable. Claims here follow the truthful-progress rule: evidence or "unverified."

```
CONTRACT: [contract file path]
RUN STARTED: [date]

---
## Iteration 1 | [date/time]
NEXT ACTION CHOSEN LAST TIME: [none, first iteration]
DID: [actions taken, milestone worked]
EVIDENCE: [tool results backing each claim: command output, file created at path, test result]
MACHINE CHECKS: [pass count / fail list from verify_contract.py]
VERIFIER: [not yet run / scores per criterion with one-line gaps]
NEXT ACTION (per iteration policy): [what changes in the next attempt and why]

---
## Resume | [date/time]            (only when a new session picks the run up)
RE-CHECK RESULTS: [current verify_contract.py output, the world may have changed]
ITERATIONS USED / CAP: [n / N]

---
## Final | [date/time]
VERDICT: [complete / stopped: which stop fired]
EVIDENCE SUMMARY: [checks passed, final scores, iterations used]
DELIVERABLE: [exact path]
[If stopped: what is missing, what would clear the block, exact resume instruction.]
```
