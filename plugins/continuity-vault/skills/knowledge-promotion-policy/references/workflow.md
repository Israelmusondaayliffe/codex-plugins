# Knowledge Promotion Workflow

Choose the least duplicative destination that will remain discoverable.

| Destination | Suitable content | Constraint |
| --- | --- | --- |
| `durable-file` | Reusable procedure, decision record, or evidence package | Version it and preserve source links |
| `project-reference` | Stable context specific to one workstream | Follow the project contract and write boundary |
| `graph` | Source-backed entities and relationships | Nodes and edges must retain provenance |
| `memory-candidate` | Helpful recall cue for future retrieval | Must be reverified before load-bearing use |
| `none` | Duplicate, transient, unsupported, or sensitive material | Preserve the source and record why no promotion occurred |

An instruction-chain edit (CLAUDE.md on Claude Code / Cowork, AGENTS.md on Codex) is not a normal promotion destination. It requires an explicit request, a recent backup, and evidence that the rule belongs at that layer. On Claude Code / Cowork the layers are the global `~/.claude/CLAUDE.md`, the workspace `CLAUDE.md`, and the project `CLAUDE.md`; on Codex they are the global, workspace, and project `AGENTS.md` files.
