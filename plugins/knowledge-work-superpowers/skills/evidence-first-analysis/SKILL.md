---
name: evidence-first-analysis
description: Use when important claims, comparisons, conclusions, or recommendations must be tested against evidence before drafting.
---

# Evidence-First Analysis

## Purpose

Test the claims that will carry the deliverable before writing polished prose. A convincing sentence is not evidence.

## Core Rule

Do not mark a claim as supported until the cited evidence directly supports it. If the reasoning extends beyond the source, mark it as inference.

## Claim Cycle

### 1. State The Claim

Write one specific, falsifiable claim at a time. Avoid combining several claims in one row.

Weak: "Curiosity programs improve culture and performance."

Stronger: "In the cited study population, the program was associated with a measured increase in the named engagement score during the reported period."

### 2. Define The Support Test

Ask what evidence would make the claim acceptable:

- Direct statement or measurement.
- Matching population and context.
- Matching time range.
- Appropriate comparison or baseline.
- Current enough for the decision.

### 3. Attach Evidence

Link the claim to source IDs from the source ledger. Read the relevant source passage or data, not only a summary or snippet.

### 4. Seek Disconfirmation

Look for evidence that weakens, narrows, or contradicts the claim. Record it in the notes rather than hiding it from the draft.

### 5. Assign Status

Use `../../assets/claim-ledger-template.md` and one of these statuses:

- `supported`: evidence directly supports the claim.
- `inferred`: evidence supports the premises, but the conclusion is analytical.
- `disputed`: credible evidence conflicts.
- `unresolved`: support is missing or too weak.

### 6. Assign Confidence

Use high, medium, or low confidence based on source quality, independence, directness, consistency, and freshness. Explain the reason. Do not convert subjective confidence into a fabricated percentage.

### 7. Decide What The Draft May Say

- Supported claims may be stated as facts with citations.
- Inferred claims must be labeled as analysis or interpretation.
- Disputed claims must show the disagreement.
- Unresolved claims must be removed, narrowed, or presented as open questions.

## Recommendation Test

For each recommendation, record:

- The decision it serves.
- The evidence it depends on.
- The assumptions connecting evidence to action.
- Plausible alternatives.
- Conditions that would change the recommendation.
- Known costs, risks, or missing information.

Recommendations are judgments. Cite their factual premises and state the judgment plainly.

## Common Failures

- Citation laundering: citing a secondary page that merely repeats an unsupported claim.
- Source stretching: turning a narrow finding into a universal statement.
- Correlation inflation: writing causal language for correlational evidence.
- Date collapse: combining evidence from different periods as if it were simultaneous.
- Definition drift: treating similar terms as identical.
- Confidence theater: using precise numbers for subjective certainty.

## Verification

Before drafting, check:

- Every key claim has a status.
- Every supported, inferred, or disputed claim links to known source IDs.
- Counterevidence is recorded.
- Unresolved claims are not presented as settled.
- Recommendations identify their assumptions.

For file-based bundles, run `python3 ../../scripts/verify_research_bundle.py /path/to/bundle --profile research` from this skill directory or use the absolute plugin script path.

After the ledger passes, load `knowledge-work-superpowers:drafting-from-evidence`.
