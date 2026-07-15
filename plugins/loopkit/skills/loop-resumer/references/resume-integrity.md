# Resume integrity checklist

- Contract and state parse as JSON objects.
- `run_id` matches.
- Workspace path and hash match the current workspace.
- Status is not terminal.
- Generation is read immediately before the next write.
- Latest receipt iteration equals `state.iteration`.
- Referenced evidence still exists.
- Uncommitted or unrelated user changes are preserved.
- The next action still follows the current contract and approvals.
