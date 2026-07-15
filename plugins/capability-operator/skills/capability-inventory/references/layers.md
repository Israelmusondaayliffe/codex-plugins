# Capability evidence layers

1. canonical: the intended source of truth for a loose skill or plugin source.
2. installed: the plugin manager reports the plugin as installed and enabled.
3. cached: the installed plugin package exists at the resolved cache version.
4. task-visible: a clean task prompt contains the installed namespaced capability.

Do not collapse these layers into one status. A directory can exist without being installed, and an installed package can remain invisible to an already-open task.
