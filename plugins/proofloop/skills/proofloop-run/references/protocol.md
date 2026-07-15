# Run Protocol Reference

Fix the contract before execution. Use `all_required` aggregation and caps of three drafts, two executions, two verifier runs, twenty tool calls, thirty minutes, two local record writes, one candidate, and zero promotions. A capped draft executes only with explicit best-effort authorization and a passing deterministic safety gate.

Keep retrieval off by default. Display exact record content and digest, then bind affirmative current-turn consent to task ID, record ID, digest, and `retrieve`.

Use terminal outcomes `completed_verified`, `completed_unverified`, `blocked`, `budget_exhausted`, `ineligible_learning_disabled`, `policy_denied`, `capability_missing`, or `security_quarantine`.
