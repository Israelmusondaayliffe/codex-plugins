---
name: video-delivery-qc
description: Verifies rendered video files against delivery requirements, including readable media metadata, dimensions, duration, audio presence, caption evidence, source-to-output consistency, and visual inspection. Use before handing off any video export. Includes deterministic ffprobe checks and a human inspection checklist, and reports untested requirements rather than claiming a render passed.
---

# Video Delivery QC

## Overview

Treat a playable file as the start of delivery verification, not the end. Check technical metadata and inspect representative frames or playback.

## Workflow

1. Confirm the required container, codec constraints, dimensions, duration, audio, captions, and platform.
2. Run scripts/inspect_delivery.py on the rendered video with the applicable requirement flags. It uses ffprobe when available and the macOS metadata service as a local fallback.
3. Inspect the opening, midpoint, closing, text-heavy, and transition-heavy moments using references/inspection.md.
4. Compare the final asset against the brief, source media, and caption script.
5. Record the result with assets/qc-report-template.md.
6. Fix failures and rerun both technical and visual checks.

## Error Handling

- If neither ffprobe nor the macOS metadata service can read the media, report technical verification as blocked.
- If no caption source exists, do not claim caption accuracy.
- If visual playback is unavailable, mark visual checks untested.
- Keep platform-safe-area assumptions explicit.

## Reliability Notes

The script verifies objective file metadata. A human or visual tool must assess composition, legibility, timing, clipping, and semantic accuracy.

## Resources

- scripts/inspect_delivery.py runs technical checks.
- references/inspection.md defines visual checks.
- assets/qc-report-template.md structures the evidence.
