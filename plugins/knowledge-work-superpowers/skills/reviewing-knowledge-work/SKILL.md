---
name: reviewing-knowledge-work
description: Use when a report, brief, memo, analysis, recommendation, or research package needs requirements and evidence review before delivery.
---

# Reviewing Knowledge Work

## Purpose

Review the deliverable against what it was supposed to do and whether its evidence and reasoning earn the conclusions.

## Review Inputs

Use the smallest complete review package:

- Work brief or requirements.
- Deliverable.
- Source ledger.
- Claim ledger.
- Named constraints or template.
- Relevant verification results.

Review the artifacts, not the creator's explanation of what they intended.

## Two-Stage Review

### Stage 1: Brief Compliance

Check each requirement separately:

- Required question answered.
- Intended audience served.
- Scope respected.
- Required sources used.
- Requested format and length followed.
- Success criteria met.
- No unapproved expansion.

Mark each item as pass, fail, or cannot verify. Missing requirements block approval even when the prose is strong.

### Stage 2: Evidence And Quality

Review these areas:

#### Sources

- Are important sources primary or authoritative where available?
- Are current claims current enough?
- Are discovery sources being used as final evidence?
- Are quoted or paraphrased passages represented accurately?

#### Claims

- Does each citation support the nearby claim?
- Is any claim broader or more causal than the evidence?
- Are inference, dispute, and uncertainty labeled?
- Are unresolved claims presented as settled?

#### Reasoning

- Are assumptions visible?
- Were credible alternatives considered?
- Is counterevidence addressed?
- Do recommendations follow from the decision and evidence?
- What evidence would change the conclusion?

#### Communication

- Does the answer lead with the outcome?
- Is the structure useful to the reader?
- Is the language plain and precise?
- Are limits placed where they affect the answer?

## Finding Levels

- Critical: the deliverable could materially mislead, violate the brief, expose sensitive information, or support a harmful decision.
- Important: a required element, key source, claim, or reasoning step is missing or weak enough to affect the conclusion.
- Minor: clarity, structure, consistency, or presentation issue that does not change the conclusion.

## Output

Use `../../assets/review-template.md` for file-based reviews.

For each finding, include:

- Location.
- Problem.
- Why it matters.
- Evidence.
- Smallest useful correction.

End with one verdict:

- Approved.
- Approved with noted limits.
- Revision required.

Do not approve while Critical or Important findings remain open.

## Handoff

When feedback is ready for revision, load `knowledge-work-superpowers:receiving-work-review`. After revisions, re-review affected areas and then load `knowledge-work-superpowers:verification-before-delivery`.
