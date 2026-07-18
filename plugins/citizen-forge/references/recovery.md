# Recovery

State writes use temporary files, flush to disk, and replace atomically. Material state writes snapshot the prior file first. A deterministic lock prevents concurrent writers. Audit history is append-only and hash chained.

If corruption or a stale lock is detected, block changes. Verify the audit chain and recover from the newest valid snapshot before continuing.
