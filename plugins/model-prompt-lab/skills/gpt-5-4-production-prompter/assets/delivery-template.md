# Delivery Template

Standard output format for all GPT-5.4 prompt deliveries.

## Format

```
## GPT-5.4 [Use Case] Prompt

### Context Type
[ChatGPT / API Responses / GPT Builder / System]

### Model Configuration
- Model: gpt-5.4 [or variant]
- Reasoning effort: [none/low/medium/high/xhigh]
- Verbosity: [low/medium/high]
- Phase parameter: [yes/no, and why]

### Prompt

[The complete, copy-pasteable prompt formatted for the context type]

### GPT-5.4 Blocks Applied
- [List each specific block used and why]
- Example: "output_contract - controls section order and format"
- Example: "tool_persistence_rules - ensures thorough tool use early in session"

### Customization Notes
- [What the user can change]
- [Which blocks to add/remove for different scenarios]
- [Reasoning effort adjustments for different task shapes]

### Validation Results
- [Output of validate_prompt.py or manual checklist]
```

## For Migration Deliveries, Add

```
### Migration Path
- Source model: [model]
- Target model: [model]
- Reasoning effort change: [from -> to]
- Prompt changes: [list of changes made]

### Rollback
- Revert model string to [source model]
- Revert reasoning effort to [original]
- Remove [list blocks added for 5.4]
```

## For Troubleshooting Deliveries, Add

```
### Diagnosis
- Symptom: [what the user reported]
- Category: [VERBOSITY/SCOPE/TOOL_CONTROL/etc.]
- Root cause: [why 5.4 exhibits this behavior]

### Fix Applied
- [Specific change made, copy-pasteable]

### Test Scenario
- [How to verify the fix works]

### If This Doesn't Fix It
- [Next diagnostic step]
- [Alternative fix to try]
```
