---
name: brand-consistency-verifier
description: Checks a logo system, identity board, campaign series, or image set against an approved brand brief and reference assets. Use when a visual series needs a release or expansion decision. Records artifact-level findings for composition, color, typography, logo treatment, imagery, and forbidden drift, then validates a pass, fail, or blocked result.
---

# Brand Consistency Verifier

## Overview

Verify the series against the approved visual authority. Similar-looking images are not enough if the rules, logo treatment, or message drift.

## Workflow

1. Load the approved brand brief, source references, and all artifacts in the review set.
2. Check each artifact against references/workflow.md.
3. Record artifact identifiers, checks, findings, and evidence with assets/output-template.json.
4. Run scripts/validate_output.py.
5. Return pass only when every required check is tested and no material finding remains.
6. Name exact revisions by artifact and rule when the result is fail.

## Error Handling

- If the approved brief or reference set is missing, return blocked instead of inventing a visual authority.
- If an artifact cannot be inspected, keep its checks untested and do not pass the series.
- Separate deliberate variation from uncontrolled drift by citing the governing principle.

## Reliability Notes

The model performs visual judgment. The validator enforces unique artifact and check identifiers, required evidence fields, and an allowed overall result.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
