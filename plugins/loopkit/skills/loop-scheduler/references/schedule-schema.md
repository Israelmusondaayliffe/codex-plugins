# Schedule record

```json
{
  "cadence": "User-approved cadence and timezone",
  "task_prompt": "Self-contained task prompt with workspace and run directory",
  "manual_tested_at": "UTC timestamp of successful manual test",
  "stop_condition": "When the schedule must pause or be removed",
  "no_op_behavior": "What to return when nothing meaningful changed",
  "evidence_return": "What proof each meaningful run returns",
  "ui_dependencies": [],
  "codex_schedule_id": null
}
```

The scheduling skill adds `schema_version` and `updated_at`. Populate `codex_schedule_id` only after the Codex surface returns a real identifier.
