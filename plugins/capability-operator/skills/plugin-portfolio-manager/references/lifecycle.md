# Plugin lifecycle

- planned: value, scope, and ownership are defined.
- built: source bundle and manifest pass validators.
- installed: plugin manager reports the intended version enabled.
- verified: source and cache match, clean-task discovery passes, and scenario checks pass.
- deprecated: replacement and migration path are documented.
- retired: dependents are migrated and the removal was explicitly authorized.

Never advance a state based only on file presence.
