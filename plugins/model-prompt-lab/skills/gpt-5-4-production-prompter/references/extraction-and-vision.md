# Extraction, Vision, and Computer Use Patterns for GPT-5.4

GPT-5.4 shows improvements in document understanding, image perception, and multimodal tasks. It is the first mainline model with built-in computer-use capabilities.

## Structured Extraction

### Core Extraction Spec

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

### Structured Output Contract

For SQL, JSON, or other parse-sensitive outputs:

```xml
<structured_output_contract>
- Output only the requested format.
- Do not add prose or markdown fences unless they were requested.
- Validate that parentheses and brackets are balanced.
- Do not invent tables or fields.
- If required schema information is missing, ask for it or return an explicit error object.
</structured_output_contract>
```

### Null Policy

```xml
<null_policy>
- If a field is not present in source, set to null
- Do NOT guess or infer values not explicitly stated
- Do NOT fill fields with "N/A" or placeholder text
</null_policy>
```

### Self-Verification

```xml
<verification>
Before returning:
1. Re-scan source document for missed fields
2. Verify all values are accurately extracted
3. Correct any omissions
</verification>
```

### Multi-Table Extraction

```xml
<multi_table_handling>
- Identify all tables in the document
- Extract each table separately
- Maintain table identifiers in output
- Cross-reference between tables when relationships exist
</multi_table_handling>
```

### Contract Extraction Pattern

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

### Invoice Extraction Pattern

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

## Vision and Image Detail

If your workflow depends on visual precision, specify the image detail level explicitly instead of relying on auto:

| Level | Use Case |
|-------|----------|
| high | Standard high-fidelity image understanding |
| original | Large, dense, or spatially sensitive images. Computer use, localization, OCR, click-accuracy tasks |
| low | Speed and cost matter more than fine detail |

## Document Localization and OCR

### Bbox Extraction Spec

For bbox tasks, be explicit about coordinate conventions and add drift tests:

```xml
<bbox_extraction_spec>
- Use the specified coordinate format exactly, such as [x1,y1,x2,y2] normalized to 0..1.
- For each bbox, include: page, label, text snippet, confidence.
- Add a vertical-drift sanity check:
  - ensure bboxes align with the line of text (not shifted up or down).
- If dense layout, process page by page and do a second pass for missed items.
</bbox_extraction_spec>
```

## Computer Use

GPT-5.4 is the first mainline model with built-in computer-use capabilities. Enables agents to interact directly with software.

**Good for:**
- Browser or desktop workflows where a person could complete the task through the UI
- Navigating sites, filling out forms, validating that a change worked
- Build-run-verify-fix loops

**Rules:**
- Use in an isolated browser or VM
- Keep a human in the loop for high-impact actions
- Supports the built-in Responses API loop, custom harness patterns, and code-execution-based setups

## Uncertainty Handling for Extraction

```xml
<uncertainty_and_ambiguity>
- If the source is ambiguous about a field value, note the ambiguity in the output.
- Never fabricate exact figures, dates, or references when uncertain.
- Prefer language like "Based on the document..." instead of absolute claims.
- If multiple interpretations exist, choose the most conservative (least assuming) interpretation.
</uncertainty_and_ambiguity>
```

## Error Handling

```xml
<extraction_errors>
If extraction fails:
- Specify which fields could not be extracted
- Note the reason (illegible, missing, ambiguous)
- Return partial extraction with nulls for failed fields
- Do NOT fabricate data to fill gaps
</extraction_errors>
```
