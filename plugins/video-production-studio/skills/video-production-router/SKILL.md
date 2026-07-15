---
name: video-production-router
description: Routes video requests to concept, script, prompt, footage, captions, overlays, motion graphics, music visualization, slideshow, product launch, PR, website capture, or runtime implementation. Use when a video brief spans multiple production skills or the correct production path is unclear. Produces a validated route and explicit runtime choice before asset generation or rendering begins.
---

# Video Production Router

## Overview

Turn a video brief into one primary production path and a short sequence of supporting skills. Choose the runtime only after the output format and evidence needs are clear.

## Workflow

1. Extract objective, audience, duration, aspect ratio, platform, source assets, and delivery format.
2. Choose one primary route using references/routing.md.
3. Record the decision in assets/route-template.json and run scripts/validate_route.py.
4. Load only the skills needed for the selected sequence.
5. Use HyperFrames as the default runtime for generated motion work. Use Remotion only when the user requests it or the source project already depends on it.
6. End every rendered delivery with video-delivery-qc.

## Error Handling

- If required source media is missing, stop before inventing substitutes that change the brief.
- If platform dimensions are unknown, state the assumed target and keep the layout adaptable.
- If runtime ownership is unclear, choose a route before writing implementation code.

## Reliability Notes

The model selects and sequences creative skills. The validator enforces an allowed primary route, delivery dimensions, and runtime. Rendering quality is checked separately.

## Resources

- scripts/validate_route.py validates production routes.
- references/routing.md maps briefs to skills.
- assets/route-template.json records the decision.
