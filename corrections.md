---
layout: page
title: Corrections
permalink: /corrections/
---

The [method](/method/) promises that a correction is visible and that a change to a judgement is a
new version, not an edit in place. This is the log. It is the cheapest test of that promise, so it is
public rather than implied.

| Date | Product | Version | What changed | Assessed fact changed? |
|---|---|---|---|---|
| 2026-10-28 | All four products | 2.1 / 1.1 | Handling moved from the retired TLP 1.0 label to `TLP:CLEAR`, and the marking is now checked by `sharegate` in CI | No |
| 2026-10-28 | [Volt Typhoon profile](/volt-typhoon-actor-profile/) | 2.2 | Corrected the SYLVANITE attribution — MITRE records campaign C0029, not a group — and added the eight-name overlap list, including UNC3236, an ATT&CK alias of Volt Typhoon | Yes — a sourcing error corrected, a fact added |
| 2026-10-28 | [Volt Typhoon profile](/volt-typhoon-actor-profile/) | 2.1 | The VOLTZITE identity row now carries the [ACH](/ach-voltzite-volt-typhoon/)'s judgement (`unlikely`) instead of `roughly even chance` | Yes — a probability, not a fact |
| 2026-10-28 | [ACH assessment](/ach-voltzite-volt-typhoon/) | 1.2 | Citation corrected: the SYLVANITE handoff is a Dragos observation, not an ATT&CK record | No — the matrix and the judgement are unchanged |
| 2026-10-28 | [Method](/method/) | page | *Independent* now means separately collected, matching what the tooling enforces; the probability lexicon is anchored to ICD 203/208 | No |
| 2026-10-28 | [Method note](/from-source-to-a-defensible-judgement/) | 1.1 | Withdrew the hand-copied test counts; they had drifted from the suite. The claim now points at CI, which cannot drift | No — the claim is now weaker and true |

## Why these are in here

None of them was found by re-reading. All of them were found by checking:

- the retired marking, by running the site's own gate against its own products;
- the contradiction, by comparing two products to each other rather than reading either one;
- the definition of independence, by comparing the public method to the code that enforces it;
- the test counts, by counting the tests;
- the SYLVANITE attribution, by looking for the group in ATT&CK's 193 enterprise groups and not
  finding it.

That is the argument for a gate that compares products rather than proofreading them, and the reason
`scripts/sitegate.py` now runs on every push: a contradiction between two products is a build
failure, not a reader's discovery.
