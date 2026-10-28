---
layout: page
title: Method
permalink: /method/
---

How the analysis on this site is produced, graded and corrected. It is stated so a reader can judge
the products against a declared standard rather than trust the writing.

## Scope

Open-source cyber threat intelligence: actor profiles, structured assessments and the tradecraft
behind them. Every product states its boundary — what is observed, what is inferred, and what could
not be verified.

## Two-axis grading

Every claim carries a **source** and is graded on two independent axes, per claim, not per section:

- **Confidence** — how good the sourcing and the reasoning are: **High** (corroborated by two or more
  independent sources, where *independent* means separately collected — two reports that trace back to
  one origin are one voice, not two), **Moderate** (one credible source, or corroboration with gaps),
  **Low** (single-source, self-claimed, or heavily inferential).
- **Probability** — how likely the assessed outcome is, where the claim is estimative: *nearly
  certain*, *very likely*, *likely*, *roughly even chance*, *unlikely*, *very unlikely*. The terms and
  their bands follow the ODNI analytic standards (ICD 203 / ICD 208), so a stated range means the same
  thing to every reader.

The two are separate. A claim can be *very likely* at *low confidence* (a single source) or *roughly
even* at *high confidence* (strong data, genuine uncertainty). Conflating them is the most common
tradecraft error; keeping them apart is the point.

## Tradecraft standards

| Standard | Requirement here |
|---|---|
| Sourcing | Every factual claim traceable to an identifiable public source. |
| Confidence | Each judgement carries an explicit confidence, and a probability where it is estimative. |
| Alternatives | The competing explanations and why they were set aside — see the ACH assessment. |
| Assumptions | Stated openly, not smuggled into the conclusion. |
| Gaps | What is not known, and why. |
| Review | Stated below. |
| Correction | Published judgements can be revised, visibly. |

## Review — stated honestly

These products are **single-author**. They are **not** presented as peer-reviewed, because there is no
second qualified analyst signing them. What exists instead is a self-check against the standards
above, and an open invitation to challenge. If an independent review happens, it will be recorded here
rather than implied.

## Versioning and corrections

- Each product carries a **version**, a **date** and a **review trigger** in its header.
- Changes are recorded in the product's **Revision history**; no assessed fact is changed silently.
- A correction that changes a judgement is published as a **new version**, not as an edit in place.
- A product carries a **next review** date, and `scripts/sitegate.py` fails the build once it has
  passed: an assessment that has outlived its review is not a product any more.

## Handling

Products are **TLP:CLEAR** unless marked otherwise — open sources, shareable without
restriction. That is the TLP 2.0 name; the retired TLP 1.0 label *TLP:WHITE* is not used here.
The marking is checked rather than asserted: every product's handling row is run through
`sharegate` in CI, and the build fails on a missing marking, conflicting markings or a
retired one.

## Rule provenance

Detection content on this site is described as *opportunities*, not as validated rules: no rule is
published without a stated provenance and a way to check that it still holds.

## Related

- [Requirements](/requirements/)
- [About](/about/)

---

*All analysis is open-source. Views are my own.*
