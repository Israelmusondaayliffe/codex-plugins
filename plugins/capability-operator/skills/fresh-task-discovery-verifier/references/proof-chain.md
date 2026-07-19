# Discovery proof chain

For each plugin confirm:

1. source manifest and skill directories exist.
2. plugin manager reports installed and enabled (`claude plugin list` or `/plugin` on Claude Code and Claude Cowork; `codex plugin list` on Codex).
3. installed cache matches the source version (`~/.claude/plugins/` on Claude Code and Claude Cowork; the `~/.codex` plugin cache on Codex).
4. a clean fresh-session inventory includes every expected namespaced skill: codex debug prompt-input on Codex, or the skill inventory of a fresh claude -p session on Claude Code and Claude Cowork.

If step four fails, do not erase or rebuild sources until steps one through three are compared.
