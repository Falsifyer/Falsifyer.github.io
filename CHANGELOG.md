---
layout: page
title: "Changelog"
sitemap: false
---

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased — 2026-10-28

### Added

- `scripts/sitegate.py` and its workflow: handling (through `sharegate`), versioning, freshness,
  grading vocabulary and cross-product consistency, with two negative fixtures that must fail.
- Claim registries (`_data/claims/<slug>.json`) graded by the suite's ceiling, with a self-test
  for the three rejection cases.
- "The broker is the actor you can see": an access-layer assessment with a validated hunt plan in
  `hunts/sylvanite-handoff.json`.

### Changed

- All four existing products: handling moved to TLP 2.0 (`TLP:CLEAR`) and a next-review date added.
- Volt Typhoon profile v2.2: the SYLVANITE attribution corrected — MITRE records campaign C0029, not
  a group — and the eight-name overlap list added, including the UNC3236 trap.
- Method: *independent* defined as separately collected; the probability lexicon anchored to ICD
  203/208.
- Engineering: hand-copied test counts replaced by CI; `huntplan` described in terms of detection
  strategies, not the retired data sources.

### Fixed

- Engineering: the paragraph introducing the suite was published twice.
- Changelog: no longer listed in the sitemap as a product page, and it renders a single `h1`
  instead of two.

## 1.0.0 — 2026-10-22

First version published as a release. The repository has existed since 2026-10-06.

- Jekyll site with the intelligence products: actor profiles, ACH assessments and the method behind them.
- Prose licensed CC BY 4.0 since 2026-10-22.
