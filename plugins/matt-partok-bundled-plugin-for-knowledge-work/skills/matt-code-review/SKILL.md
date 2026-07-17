---
name: matt-code-review
description: Review a software diff from a fixed point on two independent axes, Code Standards and Spec Fidelity. Use when the user explicitly invokes Matt Code Review, reviews a Matt implementation slice, or asks to check a branch or PR against its originating spec.
---

# Matt Code Review

Keep the two axes separate. Code can follow every convention while implementing the wrong behavior, or match the spec while damaging the codebase.

## 1. Pin the review surface

Resolve the user-supplied commit, branch, tag, or merge base. If none is supplied, infer only when the repository makes the intended base unambiguous; otherwise ask one focused question. Verify the diff is non-empty.

## 2. Find sources

- Spec Fidelity: locate the originating spec, issue, or ticket.
- Code Standards: locate the closest `AGENTS.md`, coding standards, contribution guide, architecture decisions, and test conventions.

If a source is absent, say so and lower confidence. Do not fabricate a spec or standard.

## 3. Run independent axes

Use parallel review agents when current instructions permit delegation. Otherwise review sequentially while keeping separate notes.

Code Standards checks documented rules, test quality, naming, duplication, scattered change, unnecessary abstraction, shallow wrappers, and error behavior. Treat general code-smell guidance as judgment, while documented project rules can be hard requirements.

Spec Fidelity checks missing or partial requirements, scope added without authorization, incorrect behavior, and acceptance criteria without proof. Cite the exact spec section for each finding.

## 4. Report and repair

Report each axis with severity, file or hunk, evidence, and the smallest corrective action. Give each axis its own verdict: pass, pass with fixes, or fail.

If the user authorized implementation changes, fix the highest-risk findings, rerun relevant checks, and repeat both axes. Do not commit or post review comments unless the task authorizes it.
