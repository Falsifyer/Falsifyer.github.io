---
layout: post
title: "Is VOLTZITE the same actor as Volt Typhoon? An Analysis of Competing Hypotheses"
date: 2026-10-09
categories: threat-intelligence
---

| | |
|---|---|
| **Product** | Assessment (structured technique: ACH) |
| **Handling** | TLP:CLEAR — open sources only |
| **Version** | 1.3 (2026-10-28) |
| **Review trigger** | A vendor or government statement that asserts or denies identity; a new joint advisory |
| **Next review** | 2027-04-30 |
| **Author** | Martín Eliseo |

## Bottom line

We assess with **moderate confidence** that "VOLTZITE" (Dragos) and "Volt Typhoon" (Microsoft and the
U.S. government) are best treated as an **overlapping ecosystem, not a verified single actor**. The
probability that they are literally the same organisational unit is **unlikely** (~20–45%). The
overlap is consistent with a **brokered-access mechanism** — a separate cluster establishing footholds
and passing them on — at **low confidence**.

The discriminating evidence is not the shared tradecraft (which is common and non-diagnostic) but the
vendors' own language: Dragos's "extensive technical overlaps", MITRE's weaker *Associated Groups*
recording, and the documented SYLVANITE access broker.

## The question

This assessment answers a standing requirement: *"Where vendor designations diverge, how much
confidence does the evidence support for treating them as the same actor?"* (see
[Requirements](/requirements/)). It matters because a naming judgement changes decisions — an incident
responder, a hunting team or a procurement choice should not treat two designations as one actor
without a stated confidence.

## Why a structured technique

Unstructured comparison drifts toward the most recent or most authoritative-sounding source. **ACH
(Heuer)** forces the alternatives to be written down and tests the evidence against all of them at
once. It favours the hypothesis with the **least inconsistent** evidence, not the one with the most
supporting data — which is the trap when every hypothesis shares the same visible TTPs.

## Hypotheses

- **H1 — Same actor.** VOLTZITE and Volt Typhoon are one organisational entity under different vendor
  names.
- **H2 — Distinct but overlapping.** Separate teams or units that share tooling, infrastructure,
  targeting or tasking, tracked separately by different vendors.
- **H3 — Brokered / shared access.** The overlap is produced by an access broker or shared operational
  support that hands footholds to more than one consumer cluster, without a single actor.

H3 is a mechanism that can coexist with H2; it is tested on its own because it makes a different
prediction about *where* the overlap comes from.

## Evidence

| # | Evidence | Source |
|---|---|---|
| E1 | Dragos describes VOLTZITE as sharing "extensive technical overlaps" with Volt Typhoon rather than being declared identical | [7] |
| E2 | Dragos's VOLTZITE is its analyst designation for the OT-facing activity, not an identity claim | [7] |
| E3 | CISA lists Voltzite among the aliases in its Volt Typhoon advisory | [1] |
| E4 | MITRE records the tracking names as Associated Groups — explicitly weaker than "same actor" | [3] |
| E5 | Same targeting: critical infrastructure and OT (communications, energy, transport, water) | [1][7] |
| E6 | Same tradecraft: living-off-the-land, valid accounts, SOHO proxying | [1][3] |
| E7 | SYLVANITE establishes footholds on edge devices and hands them to Volt Typhoon / VOLTZITE | [7][12] |
| E8 | Stage 2 ICS Cyber Kill Chain activity attributed to VOLTZITE | [7] |
| E9 | No public statement by any vendor asserting identity; the language used is overlap | [3][7][10] |
| E10 | Government advisories list Voltzite as an alias, implying sameness at the campaign level | [1] |

## Consistency matrix

`C` = consistent · `I` = inconsistent · `0` = neutral or ambiguous.

| Evidence | H1 (same) | H2 (overlap) | H3 (brokered) |
|---|---|---|---|
| E1 | I | C | C |
| E2 | 0 | C | 0 |
| E3 | C | 0 | 0 |
| E4 | I | C | 0 |
| E5 | C | C | C |
| E6 | C | C | C |
| E7 | I | C | C |
| E8 | 0 | C | C |
| E9 | I | C | C |
| E10 | C | 0 | 0 |

## What the matrix shows

- **H1 carries four inconsistencies** (E1, E4, E7, E9) and is the least supported. ACH favours the
  hypothesis with the least inconsistent evidence, not the one with the most supporters.
- **H2 has no inconsistencies** and explains every observation, including the vendors' own careful
  language.
- **H3 has no inconsistencies** and is the most parsimonious explanation for E7 (a broker that hands
  footholds onward) and for part of E5–E6.
- The **discriminating** evidence is E1, E4, E7 and E9 — all linguistic or structural. Shared
  tradecraft (E5, E6) is **non-diagnostic**: consistent with every hypothesis, which is exactly why
  actor identification should not rest on TTP overlap alone.

## Judgement

1. Best treated as **separate but overlapping** (H2) — **moderate confidence**.
2. That they are the **same organisational unit** (H1) — **unlikely** (~20–45%).
3. That the overlap is at least partly **brokered** (H3) — **roughly even chance**, **low confidence**.

## Sensitivity — how much of this is the prior?

Two numbers decide H1, and neither is measured.

**The prior.** Before the evidence, the odds that two vendor cryptonyms for the same activity are one
organisational unit are close to even: renames are common, splits are common, and nothing here
establishes which this is.

**The discriminant.** The evidence that moves H1 is not about the actor. E1, E4 and E9 are one
observation — no vendor asserts identity — repeated three times, and it is evidence about what
vendors are willing to say. Counted once, it is weak. Counted three times, the matrix overweights it.

That is why the band is wide. The strongest documentary evidence that exists today is an alias list —
CISA records VOLTZITE among Volt Typhoon's aliases (E3, E10) — which is the weakest form of an
identity claim, and the matrix already counts it. An explicit statement that they are one unit, or
published infrastructure or code establishing a shared operator, would move H1 across 50% on its own.
If the prior were 30% rather than even, no combination of the current evidence would lift H1 out of
"unlikely". A reader who disagrees with the prior should disagree with the band — the matrix is the
same either way, and that is the honest state of the question.

## What would break the tie

- A government or vendor statement that explicitly **asserts or denies identity**.
- Published **infrastructure or code reuse** establishing a shared operator rather than shared tooling.
- Details of **SYLVANITE tasking** — whether it serves one consumer or several.
- A **joint advisory** naming VOLTZITE and Volt Typhoon together as one actor or as distinct.

## Intelligence gaps

- Vendor taxonomy is internal and seldom explained; "overlap" is not a standardised term.
- Dragos's 2026 report is the load-bearing source (E1, E2, E7, E8) and represents a single vendor.
- No access to private telemetry or shared-infrastructure analysis; this is an open-source assessment
  and is bounded by that.

## Sources

1. CISA, NSA, FBI and international partners — **Joint Cybersecurity Advisory AA24-038A: PRC
   State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure**
   (7 Feb 2024). https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a
3. MITRE ATT&CK — **Group G1017: Volt Typhoon** (v2.0, last modified 31 Jul 2026).
   https://attack.mitre.org/groups/G1017
7. Dragos — **OT/ICS Cybersecurity Report 2026: Year in Review** (17 Feb 2026).
   https://www.dragos.com/resources/press-release/dragos-2026-year-in-review-new-ot-threats-ransomware
9. MITRE ATT&CK — **Campaign C0039: Versa Director Zero Day Exploitation** (June–August 2024).
   https://attack.mitre.org/campaigns/C0039
10. Palo Alto Networks Unit 42 — **Threat Brief: Attacks on Critical Infrastructure Attributed to
    Insidious Taurus (Volt Typhoon)** (Feb 2024). https://unit42.paloaltonetworks.com/volt-typhoon-threat-brief/

The numbering follows the [Volt Typhoon actor profile](/volt-typhoon-actor-profile/), which holds the
full source list and the unreferenced entries.

---

*All analysis is open-source. Views are my own.*

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-09 | First release. |
| 1.1 | 2026-10-28 | Handling corrected from the retired TLP 1.0 label to `TLP:CLEAR`, now checked in CI. The Volt Typhoon profile's identity row was aligned to this product's judgement. The matrix, the hypotheses and the judgement are unchanged. |
| 1.2 | 2026-10-28 | Citation corrected: the SYLVANITE handoff (E7) is a Dragos observation, not an ATT&CK record. The matrix, the hypotheses and the judgement are unchanged. |
| 1.3 | 2026-10-28 | Added a sensitivity paragraph: H1 rests on a prior near even and one weak observation repeated three times; one documentary event would move it across 50%. The matrix and the judgement are unchanged. |
