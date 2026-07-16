# Model Change Policy

Treat model-specific compensations as provisional.

When the user requests the latest or current model, check current official documentation before selecting a model or rewriting prompts. Preserve an explicitly named target unless the user asks to change it.

After a major model change:

1. Re-run representative harness tasks.
2. Compare the current prompt with a shorter version.
3. Remove reminders that the new model follows without them.
4. Recheck approval behavior, tool routing, response length, and stop conditions.
5. Keep stable user policy separate from temporary model corrections.

Do not invent model names, parameters, prices, or availability.
