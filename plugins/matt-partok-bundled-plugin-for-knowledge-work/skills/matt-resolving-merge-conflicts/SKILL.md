---
name: matt-resolving-merge-conflicts
description: Resolve an in-progress git merge or rebase conflict by tracing both sides to their intent inside an explicitly selected Matt software workflow. Use when the user invokes Matt conflict resolution and the repository is already in a conflicted state.
---

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. Discover the project's **automated checks** and run them : typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish only within scope.** Stage and continue the merge or rebase when the user's request includes completing the operation. Otherwise leave the resolved working tree ready for review and report the exact remaining commands. Never push without separate authorization.
