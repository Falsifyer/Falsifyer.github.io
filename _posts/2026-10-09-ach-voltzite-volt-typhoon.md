---
layout: post
title: "Is VOLTZITE the same actor as Volt Typhoon? Two questions, not three hypotheses"
date: 2026-10-09
categories: threat-intelligence
summary: "An analysis of competing hypotheses that splits one overloaded question into two — identity and mechanism — and grades the answer to each separately."
---

| | |
|---|---|
| **Product** | Assessment (structured technique: ACH, two questions) |
| **Handling** | TLP:CLEAR — open sources only |
| **Version** | 2.0 (2026-10-28) |
| **Review trigger** | A vendor or government statement that explicitly asserts or denies identity; published infrastructure or code reuse; detail on SYLVANITE tasking |
| **Next review** | 2027-04-30 |
| **Author** | Martín Eliseo |

*Every claim below carries a source and is graded on two independent axes. The grades are computed
from a registry (`_data/claims/`), not typed into the table.*

## Bottom line

1. **The identity question is undecided, and saying so is the finding.** “Same unit” and “distinct
   but related” both sit at **roughly even**, at **low confidence**. What the open evidence supports
   is that *some* relationship exists rather than none — “unrelated” is **very unlikely**.
2. **The mechanism is better evidenced than the identity.** A separate cluster establishing access
   and handing it to VOLTZITE is **likely**, at **moderate confidence**: that is a direct observation,
   not an inference from shared tradecraft.
3. **This version changes the identity judgement.** v1.3 said “unlikely (20–45%)”. That conclusion
   rested on counting one observation three times; counted once, the estimate returns to the band it
   started from.

## What changed from v1.3, and why

| v1.3 | v2.0 | Why |
|---|---|---|
| One matrix: H1 same, H2 related, H3 brokered | Two matrices: **identity** and **mechanism** | H3 was compatible with H2, so the matrix could never refute it. A hypothesis that cannot lose is not being tested. |
| E1, E4 and E9 counted as three inconsistencies against H1 | One item (A-i), with its independence stated | All three say the same thing: no vendor asserts identity. Three rows for one fact inflate the case. |
| H2 defined broadly enough to absorb anything | A2 has a refutation condition | A hypothesis that explains every observation wins by construction. |
| H1 `unlikely` (20–45%) | A1 `roughly even` (45–55%) | The triple count was what pushed it below the band. Grouped, it returns to the prior. |
| H2 graded `moderate confidence` | A2 graded `low` | Nothing in the public evidence is diagnostic for identity: no infrastructure, no code, no operator artefact. Under the site's ceiling, no diagnostic item means no more than low. |

## Question A — are they one organisational unit?

- **A1 — Same unit.** VOLTZITE and Volt Typhoon are one entity under two vendor names.
- **A2 — Distinct, related.** Separate teams or units that share tooling, infrastructure, targeting or
  tasking. *Refuted if* a vendor or government explicitly asserts identity, or published
  infrastructure or code establishes a single operator.
- **A3 — Distinct, unrelated.** The overlap is what any ICS-focused intrusion set looks like from
  outside. *Refuted by* the same evidence that would confirm A1, or by a shared artefact.

### Evidence

| # | Evidence | Bears on | Independence | Diagnostic weight |
|---|---|---|---|---|
| A-i | No vendor asserts identity: Dragos says “technical overlaps”, MITRE records Associated Groups, CISA lists an alias [3][7][12] | Naming convention | One observation across three publishers; two of them draw on vendor reporting | **Weak**: evidence about how names are assigned |
| A-ii | CISA lists Voltzite among Volt Typhoon’s aliases [1] | Equivalence at campaign level | Government, but an alias list is not an identity finding | **Moderate** |
| A-iii | Same sectors, same living-off-the-land tradecraft, same SOHO proxying [1][10] | Targeting and capability | Several, independent | **None**: consistent with A1, A2 and A3 |
| A-iv | No public shared infrastructure, no shared code, no operator artefact | Identity | — | **Absence of evidence**, not evidence of difference |

### Matrix

`C` consistent · `I` inconsistent · `0` neutral

| Evidence | A1 same | A2 related | A3 unrelated |
|---|---|---|---|
| A-i naming language | 0 | C | C |
| A-ii CISA alias list | C | 0 | 0 |
| A-iii shared tradecraft | C | C | C |
| A-iv no linkage published | 0 | C | C |

### Judgement A

Only one item discriminates, and it points both ways: the government lists the names together, the
vendors decline to. That is not enough to separate A1 from A2, and it is not enough to exclude A3 on
open sources either.

### Assessment ledger

<!-- claims:begin -->
| Assessment | Confidence | Probability | Basis |
|---|---|---|---|
| Dragos's VOLTZITE is the same actor as Volt Typhoon | Low | roughly even chance | [1][3][7][12] |
| The clusters are distinct but related | Low | roughly even chance | [1][3][7][12] |
| The clusters are unrelated | Low | very unlikely | [1][10] |
<!-- claims:end -->

Both leading hypotheses are `low` because **nothing diagnostic exists in public**: the ceiling is set
by the evidence, and no amount of vendor language raises it. v1.3 graded “distinct but related” at
moderate confidence; that grade was not supported, and the registry refused it.

## Question B — is the overlap produced by brokered access?

- **B1 — Brokered.** A separate cluster establishes footholds and hands them to VOLTZITE.
- **B2 — Direct.** VOLTZITE does its own initial access; the overlap is capability, not supply.
- **B3 — Shared tradecraft, no broker.** Clusters exchange tooling or buy the same commodity access
  without a standing handoff.

### Evidence

| # | Evidence | B1 | B2 | B3 |
|---|---|---|---|---|
| B-i | Dragos observed SYLVANITE weaponising edge-device vulnerabilities and handing established footholds to VOLTZITE, during incident response at U.S. electric and water utilities [12] | C | I | 0 |
| B-ii | SYLVANITE is tracked as a separate group with its own overlaps — UNC5221, UNC5174, UNC5291, UNC3236 and others [12] | C | 0 | C |
| B-iii | VOLTZITE has also exploited edge devices itself, e.g. Versa Director CVE-2024-39717 [9] | 0 | C | C |
| B-iv | No public evidence of a sale, a price or a market transaction [12] | 0 | 0 | 0 |

### Judgement B

**B1 is likely, at moderate confidence.** It is the only judgement here carried by direct observation
rather than by naming: Dragos states it watched the handoff. B2 is not excluded for other intrusions —
B-iii shows the actor still does its own initial access where it can — and B3 cannot be separated from
B1 on public evidence, because a one-directional handoff and a shared-access arrangement look the same
from outside.

The distinction matters for defenders: under B1, edge-device exploitation by *any* cluster in the
ecosystem is a precursor to this actor, not a separate problem to triage away.

## Sensitivity — how much of this is the prior?

The identity judgement is not robust, and it should say so.

**The prior.** Before the evidence, the odds that two vendor cryptonyms for the same activity are one
organisational unit are close to even: renames are common, splits are common, and nothing here
establishes which this is.

**The discriminant.** A-i is the only item that moves A1, and it is not about the actor: it is about
what vendors are willing to say. Counted once, it is weak. If the prior were 30% rather than even, no
combination of the current evidence would lift A1 out of “unlikely”. An explicit assertion of identity,
or published infrastructure or code establishing a shared operator, would move it across 50% on its
own.

Question B is different. B-i is a direct observation, so its judgement depends on whether Dragos is
right, not on a prior — which is why it carries moderate confidence with a single source and A1 does
not.

## What would break the tie

- A vendor or government statement that **explicitly asserts or denies identity** — the alias list is
  the weak form of this evidence, and it is already counted.
- Published **infrastructure or code reuse** establishing a shared operator rather than shared tooling.
- Detail on **SYLVANITE tasking**: whether it serves one consumer cluster or several.
- A joint advisory naming VOLTZITE and Volt Typhoon together as one actor or as distinct.

## Intelligence gaps

- Vendor taxonomy is internal and seldom explained; “overlap” is not a standardised term.
- The Dragos 2026 report is load-bearing for A-i and B-i and represents a single vendor.
- No public infrastructure or code links the two designations; this is the gap that keeps both leading
  hypotheses at low confidence.
- No telemetry, no samples, no shared-infrastructure analysis: this is an open-source assessment and is
  bounded by that.

## Sources

The numbering follows the [Volt Typhoon profile](/volt-typhoon-actor-profile/), which holds the full
list; only the entries cited here are repeated. Entries 2, 4, 5, 6, 8 and 11 are in the profile and
are not cited in this product.

1. CISA, NSA, FBI and international partners — **Joint Cybersecurity Advisory AA24-038A** (7 Feb 2024).
   https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a
3. MITRE ATT&CK — **Group G1017: Volt Typhoon** (v2.0, last modified 31 Jul 2026).
   https://attack.mitre.org/groups/G1017
7. Dragos — **OT/ICS Cybersecurity Report 2026: Year in Review** (17 Feb 2026).
   https://www.dragos.com/resources/press-release/dragos-2026-year-in-review-new-ot-threats-ransomware
9. MITRE ATT&CK — **Campaign C0039: Versa Director Zero Day Exploitation** (June–August 2024).
   https://attack.mitre.org/campaigns/C0039
10. Palo Alto Networks Unit 42 — **Threat Brief: Attacks on Critical Infrastructure Attributed to
    Insidious Taurus (Volt Typhoon)** (Feb 2024).
    https://unit42.paloaltonetworks.com/volt-typhoon-threat-brief/
12. Dragos — **SYLVANITE** threat group page (accessed 28 Oct 2026).
    https://www.dragos.com/threat/sylvanite/

---

*All analysis is open-source. Views are my own.*

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-09 | First release. |
| 1.1 | 2026-10-28 | Handling corrected from the retired TLP 1.0 label to `TLP:CLEAR`, now checked in CI. The Volt Typhoon profile's identity row was aligned to this product's judgement. The matrix, the hypotheses and the judgement are unchanged. |
| 1.2 | 2026-10-28 | Citation corrected: the SYLVANITE handoff (E7) is a Dragos observation, not an ATT&CK record. The matrix, the hypotheses and the judgement are unchanged. |
| 1.3 | 2026-10-28 | Added a sensitivity paragraph: H1 rests on a prior near even and one weak observation repeated three times; one documentary event would move it across 50%. The matrix and the judgement are unchanged. |
| 2.0 | 2026-10-28 | Split identity from mechanism; grouped the naming observation; gave A2 a refutation condition; moved A1 from `unlikely` to `roughly even` and A2 from `moderate` to `low`; registered the judgements so the ceiling is computed. The identity judgement changed. |
