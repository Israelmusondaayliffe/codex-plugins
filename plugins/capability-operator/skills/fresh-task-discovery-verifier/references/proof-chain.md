# Discovery proof chain

For each plugin confirm:

1. source manifest and skill directories exist.
2. plugin manager reports installed and enabled.
3. installed cache matches the source version.
4. a clean codex debug prompt-input includes every expected namespaced skill.

If step four fails, do not erase or rebuild sources until steps one through three are compared.
