# Safety and Approvals

## Read-only actions

The initial audit may inspect relevant files, list installed capabilities, read configuration key names, and run non-mutating validators.

## Approval groups

Keep these approvals separate:

1. Workspace folders and templates.
2. Global instructions and configuration.
3. Project contracts.
4. Rules, hooks, and permission changes.
5. Skills and plugins.
6. Connector authentication.
7. Automations and schedules.
8. External repositories and publication.

Approval for one group does not approve another.

## Never implicit

- Deleting existing user work.
- Replacing an existing file without a reviewed diff and matching hash.
- Reading or recording secret values.
- Trusting a hook.
- Installing third-party code.
- Authenticating an account.
- Sending messages or publishing content.
- Expanding paths or permissions during a running Goal.
