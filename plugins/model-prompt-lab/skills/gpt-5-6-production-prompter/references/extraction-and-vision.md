# Extraction, Vision, and Computer Use Patterns for GPT-5.6

Extraction remains the invariant-heavy use case where XML blocks earn their place naturally; the 5.5 patterns carry forward almost unchanged. The 5.6-specific changes are in vision: `original` and `auto` image detail now preserve original image dimensions instead of resizing to a patch budget, improving spatially sensitive work at a token and latency cost on large images.

## Lean extraction pattern (default)

```text
Role: A structured data extractor.

# Goal
Extract the requested fields from the source document into JSON.

# Success criteria
- Output matches the schema exactly. No extra fields.
- Fields not present in the source are set to null, never guessed.
- Values are extracted verbatim or as a faithful paraphrase, never fabricated.
- Output is valid JSON with balanced brackets.

# Schema
{
  "field_a": string,
  "field_b": string | null,
  ...
}

# Constraints
- Do not infer values from context outside the source.
- For ambiguous fields, choose the most conservative interpretation and note the ambiguity.

# Output
- JSON only. No prose, no markdown fences.
- If required schema information cannot be determined from the source, return an explicit error object.
```

Reasoning effort: extraction is execution-heavy; start at `none`, test `low` only if quality demands it. `gpt-5.6-luna` is the natural variant for high-volume extraction.

## Extraction spec (XML form)

```xml
<extraction_spec>
You will extract structured data from documents into JSON.

- Follow schema exactly. Do NOT add fields not in schema.
- If a field is not present in the source, set it to null rather than guessing.
- Do NOT infer or fabricate values not explicitly stated.
- Before returning, quickly re-scan the source for any missed fields and correct omissions.
- Quote relevant text verbatim where it helps justify field values.
</extraction_spec>
```

ALL CAPS is appropriate: "do not invent fields" and "do not fabricate values" are true invariants.

## Structured output contract

```xml
<structured_output_contract>
- Output only the requested format.
- Do not add prose or markdown fences unless they were requested.
- Validate that parentheses and brackets are balanced.
- Do not invent tables or fields.
- If required schema information is missing, ask for it or return an explicit error object.
</structured_output_contract>
```

## Null policy

```xml
<null_policy>
- If a field is not present in source, set to null
- Do NOT guess or infer values not explicitly stated
- Do NOT fill fields with "N/A" or placeholder text
</null_policy>
```

## Self-verification (extraction-specific)

Markdown success-criterion form preferred: "Re-scan complete before returning, no missed fields." XML form when nested in an XML prompt:

```xml
<verification>
Before returning:
1. Re-scan source document for missed fields
2. Verify all values are accurately extracted
3. Correct any omissions
</verification>
```

## Multi-table extraction

```xml
<multi_table_handling>
- Identify all tables in the document
- Extract each table separately
- Maintain table identifiers in output
- Cross-reference between tables when relationships exist
</multi_table_handling>
```

## Contract extraction example

```xml
<extraction_spec>
Extract contract data into JSON. Schema:
{
  "parties": [{"name": string, "role": "buyer"|"seller"|"licensor"|"licensee"|null}],
  "effective_date": string | null,
  "termination_date": string | null,
  "jurisdiction": string | null,
  "governing_law": string | null,
  "key_obligations": [string],
  "termination_clause_summary": string | null,
  "renewal_terms": string | null
}

Rules:
- Follow schema exactly, no extra fields
- Set null for absent fields, never guess
- Re-scan document before returning
- Extract verbatim text where possible
</extraction_spec>
```

## Invoice extraction example

```xml
<extraction_spec>
Extract invoice data into JSON. Schema:
{
  "invoice_number": string,
  "invoice_date": string | null,
  "due_date": string | null,
  "vendor": {"name": string, "address": string | null},
  "line_items": [
    {"description": string, "quantity": number|null, "unit_price": number|null, "total": number|null}
  ],
  "subtotal": number | null,
  "tax": number | null,
  "total": number
}

Rules:
- All currency values as numbers without symbols
- Set null for absent fields
- Verify totals against line items
</extraction_spec>
```

## Vision and image detail (changed in 5.6)

GPT-5.6 preserves the original dimensions of images sent with `original` or `auto` detail instead of resizing them to a patch budget or pixel-dimension limit.

| Level | Use case | 5.6 note |
|-------|----------|----------|
| original / auto | Computer use, localization, OCR, click accuracy, dense documents, spatially sensitive analysis | Original dimensions preserved. Large images can use more input tokens and increase latency; budget deliberately |
| high | Standard high-fidelity understanding | |
| low | Speed and cost over fine detail | |

Practical guidance:
- Dense-document OCR and bbox work benefit directly from original dimensions; expect better spatial fidelity on large pages.
- For high-volume pipelines with large images, measure the token and latency cost of `original`/`auto` before defaulting to it; downscale at the application layer when full resolution is not needed.
- Computer-use screenshots on high-resolution displays are the classic case where the quality gain and the cost both land; test both detail levels.

## Document localization and OCR

```xml
<bbox_extraction_spec>
- Use the specified coordinate format exactly, such as [x1,y1,x2,y2] normalized to 0..1.
- For each bbox, include: page, label, text snippet, confidence.
- Add a vertical-drift sanity check: ensure bboxes align with the line of text (not shifted up or down).
- If dense layout, process page by page and do a second pass for missed items.
</bbox_extraction_spec>
```

With original-dimension images, coordinate normalization still applies; state the convention explicitly so program code and model output agree.

## PTC for batch extraction (new for 5.6)

High-volume extraction across many documents fits PTC's task shape: fetch documents, run per-document extraction via an eligible tool, validate against the schema, aggregate into one result set. Rules:

- The extraction invariants (schema fidelity, null policy) go in the tool's own behavior and the orchestration output schema, not just the top-level prompt.
- Validation is a named PTC strength; have the program check schema conformance and report failures as structured entries rather than silently dropping documents.
- The final message must still report coverage (processed / failed / blocked); test it separately from the program output.

See `references/programmatic-tool-calling.md`.

## Computer use

Carried forward: agents interact with software through screenshots and click coordinates.

**Good for:** browser or desktop workflows a person could complete through the UI; navigating sites, filling forms, validating that a change worked; build-run-verify-fix loops.

**Rules:** use in an isolated browser or VM; keep a human in the loop for high-impact actions; the autonomy policy applies to computer-use actions exactly as it does to tool calls.

## Uncertainty handling for extraction

```xml
<uncertainty_and_ambiguity>
- If the source is ambiguous about a field value, note the ambiguity in the output.
- Never fabricate exact figures, dates, or references when uncertain.
- Prefer language like "Based on the document..." instead of absolute claims.
- If multiple interpretations exist, choose the most conservative (least assuming) interpretation.
</uncertainty_and_ambiguity>
```

## Error handling

```xml
<extraction_errors>
If extraction fails:
- Specify which fields could not be extracted
- Note the reason (illegible, missing, ambiguous)
- Return partial extraction with nulls for failed fields
- Do NOT fabricate data to fill gaps
</extraction_errors>
```

## What changed from 5.5 for extraction and vision

| Aspect | 5.5 default | 5.6 default | Action |
|--------|-------------|-------------|--------|
| Schema enforcement | XML blocks | Same (invariant-heavy) | Keep |
| Null policy | XML block | Same | Keep |
| Reasoning effort | Often none | Often none; luna for volume | Re-baseline, test one lower |
| Image detail | Resized to patch budget | original/auto preserve dimensions | Choose detail level deliberately; budget tokens on large images |
| Batch pipelines | Parallel direct calls | PTC candidate | Benchmark; keep final-message coverage reporting |
| Self-verification | Success criterion | Same | Keep lean form |
