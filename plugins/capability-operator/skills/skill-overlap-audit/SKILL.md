---
name: skill-overlap-audit
description: Finds duplicate, drifted, mirrored, and collision-prone skills across loose roots and plugin bundles. Use before bundling skills, retiring loose copies, resolving conflicting triggers, or auditing why multiple similarly named skills appear. Consumes a capability inventory and reports exact fingerprints without mutating any source.
---

# Skill Overlap Audit

## Overview

Separate safe mirrors from harmful overlap. Matching names are a signal to inspect, not automatic permission to delete.

## Workflow

1. Generate a current inventory with capability-inventory.
2. Run scripts/find_overlaps.py against the inventory.
3. Classify each group with references/classification.md.
4. Review semantic trigger overlap for different names manually.
5. Produce a disposition using assets/overlap-report-template.md.
6. Require explicit authorization and a backup before any consolidation.

## Error Handling

- If fingerprints are missing, classify the group as unresolved.
- If two skills share intent but not names, record a semantic overlap with cited trigger text.
- If canonical ownership is unknown, recommend an ownership decision rather than deletion.

## Reliability Notes

The script detects exact name and fingerprint relationships. Semantic overlap and retirement decisions require judgment and source review.

## Resources

- scripts/find_overlaps.py creates exact overlap groups.
- references/classification.md defines overlap states.
- assets/overlap-report-template.md structures the audit.
