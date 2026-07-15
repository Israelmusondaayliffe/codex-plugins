# Goal Template

Fill every bracket. Delete optional lines only when genuinely inapplicable, not to save effort.

```
/goal [Deliverable: concrete artifact at a concrete path, or a named passing state].

[Done definition: the sections, fields, or checks the output must contain.
Written so a stranger could confirm completion without asking questions.]

[Scope: Only create/modify files in <dir>. Only read from <dir>.
Do not change existing files unless specified.]

[Checker: verify <specific condition, e.g. every claim has a source URL,
tests pass via <exact command>>. Flag anything that fails verification.]

Stop when [success condition, complete and verified].
If [failure condition] after [N] attempts, [skip and note why / stop and report what went wrong].
Maximum [N] iterations.
[Optional: budget cap.]
[Optional, for long goals: keep a memory file at <path>, read at start, update at end.]
```

Checklist before delivery: stranger test passes, scope named, checker names a condition or command, three stops present with numbers, no em-dashes.
