# Reference Deconstruction

A pre-step pattern. Extract the creative system from a reference image into a portable brand board, then reuse that system for a different subject. The point is to harvest the underlying logic (palette, treatment, compositional grammar, signature device) without copying the reference itself.

This is upstream of MULTI-OUTPUT and EDITORIAL. After deconstruction the resulting brand board becomes the visual DNA backbone for whatever the user actually wants to build.

## When to use

- User uploads a reference image and wants the vibe applied to a different brand, product, or subject.
- User says "I love this look, give me X in this style" or "extract the system from this and apply it to Y."
- The visual DNA is not yet defined and the user is starting from inspiration, not from a written brand spec.
- Anti-copy guardrail needed. The user wants the structure, not the artwork.

If the user already has a defined visual DNA in writing, skip this and route straight to MULTI-OUTPUT or EDITORIAL.

## What gets extracted

Seven targets. The model reasons about each one before generating the brand board.

1. **Core idea and creative tension.** What single concept holds the reference together. What contrast or opposition gives it energy.
2. **Color and material language.** Named palette with roles (primary, accent, secondary, background). Surface materials, paper stock, finish quality if implied.
3. **Typography direction.** Type voice (editorial, brutalist, romantic, technical), hierarchy logic, treatment of display vs body, any signature letterform behavior.
4. **Image and composition logic.** Subject matter vocabulary. How figures, products, or environments are framed. Negative space behavior. Camera grammar if photography is involved.
5. **Signature visual device.** The one element that makes the reference feel like itself. A texture, a recurring crop, a typographic mannerism, a color block, a grain.
6. **Layout and grid system.** Modular structure, alignment rules, column logic, hero zone behavior, margin treatment.
7. **Scalable campaign applications.** What this system can become beyond a single image: posters, social, packaging, signage, motion. Stated as possibilities, not produced yet.

## Output spec

A single 4:3 visual brand board. Polished editorial layout. Modular grid. Strong hero zone. Limited readable labels. Large visual tiles. Minimal micro-copy. No overlapping text on active backgrounds. Clean margins, consistent spacing.

This is a reference document, not a campaign asset. It exists to be handed to the next prompt as visual DNA.

## Anti-copy guardrail

The deconstruction prompt must include an explicit refusal to copy the reference directly. The model should rebuild the system, not reproduce the artwork. Without this guardrail GPT Image 2 sometimes returns a near-replica of the input.

Forbid in the brief or the JSON envelope:
- direct reproduction of the reference subject or scene
- copying any specific figure, product, or location from the reference
- pixel-level mimicry of textures or marks

## PSGV mapping

**PLAN.** Declare intent: deconstruction, not reproduction. Name the 7 extraction targets. Specify 4:3 brand-board output.

**SEARCH.** SKIP for most cases. Active only when the reference contains real-world elements that need verification (a real brand, a real location, a real product line being riffed on).

**GENERATE.** The brief itself. Reads as a Creative Director directive. Names the 7 targets explicitly. States anti-copy rule.

**VERIFY.** All 7 systems extracted into the brand board. No direct copy of the reference. 4:3 ratio. Micro-copy minimal. Layout coherent and readable.

## Template prompt (NL, default)

```
PLAN: Reference deconstruction. Extract the underlying creative system from the uploaded image, do not reproduce it. Output a 4:3 visual brand board capturing seven systems: core idea and creative tension, color and material language, typography direction, image and composition logic, signature visual device, layout and grid system, multi-format campaign applications.

SEARCH: SKIP.

GENERATE: Acting as a senior Creative Director, study the attached reference image and rebuild its underlying creative system as a clean 4:3 visual brand board. Do not copy the reference directly. Extract and present: the core idea and creative tension, color and material palette named with roles, typography direction and hierarchy, image vocabulary and composition logic, the single signature visual device that defines the reference, layout and grid system, and a strip of multi-format campaign applications. Treat the board as a premium editorial agency slide. Modular grid, strong hero zone, large visual tiles, limited labels, minimal micro-copy, clean margins, no overlapping text on active backgrounds. The board should function as a portable system that another designer could pick up and apply to a different brand without ever seeing the original reference.

VERIFY: Before showing output, confirm all seven systems are visibly present on the board. Confirm no direct reproduction of the reference subject, scene, or figures. Confirm 4:3 ratio. Confirm micro-copy is minimal and readable.
```

## Template prompt (JSON envelope, anti-drift)

Use when the reference is iconic enough that GPT Image 2's correction instinct will pull toward replication.

```json
{
  "plan": "Reference deconstruction. Extract the creative system from the attached image into a 4:3 brand board. Do not copy the reference. Seven extraction targets: core idea and tension, color and material language, typography direction, image and composition logic, signature visual device, layout and grid, multi-format applications.",
  "search": "skip",
  "format": "4:3 visual brand board, premium editorial agency layout",
  "extraction_targets": [
    "core idea and creative tension",
    "color and material language with named roles",
    "typography direction and hierarchy logic",
    "image vocabulary and composition logic",
    "signature visual device",
    "layout and grid system",
    "multi-format campaign applications strip"
  ],
  "design_rules": [
    "modular grid",
    "strong hero zone",
    "large visual tiles",
    "limited labels",
    "minimal micro-copy",
    "clean margins, consistent spacing",
    "no text overlap on active backgrounds"
  ],
  "forbidden": [
    "direct reproduction of the reference subject or scene",
    "copying any specific figure, product, or location from the reference",
    "pixel-level mimicry of textures or marks",
    "text overlap on active backgrounds",
    "overcrowding"
  ],
  "verify": [
    "all seven extraction targets present and labeled",
    "no direct copy of the reference",
    "4:3 ratio held",
    "micro-copy minimal and readable",
    "layout reads as a portable system"
  ]
}
```

## Chaining downstream

After deconstruction, the brand board feeds the next prompt in two ways.

**Path A. Hand the rendered brand board image as a reference upload to a MULTI-OUTPUT system prompt.** The `<visual_dna>` block restates the extracted palette, treatments, and mood in writing. The model uses both the image and the written DNA to lock the system across the page set.

**Path B. Translate the brand board into a written `<visual_dna>` block directly.** Skip the visual board entirely if the chain is fast and the user does not need a presentable mid-step. The 7 extraction targets become the lines of the visual DNA block.

Path A is for client-facing chains where the brand board is a deliverable on its own. Path B is for internal speed runs.

## Mode hand-off

After this pattern runs, route to:

- **MULTI-OUTPUT** when the next step is a multi-page system (brand kit, pitch deck, event package, full campaign).
- **EDITORIAL** when the next step is a single hero deliverable (key visual, magazine cover, single poster).
- **SERIES** when the next step is consistent variations of one thing under the new system.

State the routing in the response so the user sees the chain.

## Common failures

- **Replication drift.** Model returns a near-copy of the reference. Fix: escalate to JSON envelope with explicit forbidden array.
- **Generic system extraction.** Brand board reads like a stock template, not the reference. Fix: name the signature visual device explicitly in the prompt and force the model to identify it before generating.
- **Text-heavy board.** Model produces a wall of labels instead of a visual document. Fix: state "minimal micro-copy" and "large visual tiles" upfront in PLAN.
- **Wrong ratio.** Model defaults to 1:1 or 16:9. Fix: state 4:3 in both PLAN and VERIFY.

## Attribution

Pattern derived from Amir Mušić's Image-to-Engine Pipeline (2026). The seven-target extraction list and the 4:3 brand-board output spec are his contribution. Adapted into PSGV format and integrated with the skill's MULTI-OUTPUT and EDITORIAL routing.
