# Writing route rules

## intent-architecture

Use when the user needs a new draft, message strategy, audience adaptation, or structural rethink. Load business-writing-intent-enforcer first.

## rewrite

Use when the user authorizes changes to supplied prose. Preserve meaning and claims. Load business-writing-intent-enforcer, then writing-enforcer.

## detect-only

Use for audits, critique, issue spotting, and requests that prohibit rewriting. Report findings with locations and proposed remedies. Do not return replacement prose unless requested.

## validation

Use when the draft already exists and the user wants a pass or fail against named requirements. Report failed checks before optional refinements.

## Claim boundary

Invoke claim-boundary-checker when a material statement is unsupported by supplied sources, depends on current facts, or crosses from editing into factual invention.
