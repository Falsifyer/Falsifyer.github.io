---
layout: page
title: Falsification
permalink: /falsification/
kicker: Register
description: "Every claim a reader would act on, the condition that would change it, the artefact that would satisfy it, and when it expires."
---

This is the register behind the products. It is not a statement of confidence: it is the list
of things we would have to see to stop believing what we published. It is generated from the
same claim registries that produce each product's assessment ledger, so it cannot drift from
them.

<!-- falsification:begin -->
**19 conditions** across 4 products. 4 carry an expiry; the nearest is **2027-01-31**. None has expired.

| Product | Claim | What would change it | Artefact | Type | Expires |
|---|---|---|---|---|---|
| [Scattered Spider](/scattered-spider-actor-profile/) | 2025 arrests slowed the group | A resumption at the pre-arrest tempo, or a conviction | Law-enforcement statement or incident reporting | behavioural | 2027-01-31 |
| [Scattered Spider](/scattered-spider-actor-profile/) | Hypervisor (vCenter/ESXi) operations | New hypervisor tooling, or a patch that closes the access path | Vendor research or an exploited CVE | technical | 2027-04-30 |
| [Scattered Spider](/scattered-spider-actor-profile/) | Sector wave targeting (retail, insurance, airlines) | A new sector wave, or a pause longer than two quarters | Incident reporting across the named sectors | behavioural | 2027-04-30 |
| [Volt Typhoon](/volt-typhoon-actor-profile/) | Uses compromised SOHO routers (KV Botnet and successors) to proxy C2 and obscure origin | A successor SOHO botnet, or a takedown that survives a reboot | DOJ/FBI announcement or vendor botnet telemetry | technical | 2027-04-30 |
| [Is VOLTZITE the same actor as Volt Typhoon? Two questions, not three hypotheses](/ach-voltzite-volt-typhoon/) | Dragos's VOLTZITE is the same actor as Volt Typhoon | A statement that asserts or denies identity | Joint advisory or ATT&CK change | documentary | — |
| [Is VOLTZITE the same actor as Volt Typhoon? Two questions, not three hypotheses](/ach-voltzite-volt-typhoon/) | SYLVANITE hands established access to VOLTZITE | SYLVANITE serving a second consumer, or the handoff being denied | Vendor report | documentary | — |
| [Is VOLTZITE the same actor as Volt Typhoon? Two questions, not three hypotheses](/ach-voltzite-volt-typhoon/) | The clusters are distinct but related | A vendor states the clusters are separate, or one | Vendor report | documentary | — |
| [Is VOLTZITE the same actor as Volt Typhoon? Two questions, not three hypotheses](/ach-voltzite-volt-typhoon/) | The clusters are unrelated | Shared infrastructure or code linking the designations | Vendor research | documentary | — |
| [Scattered Spider](/scattered-spider-actor-profile/) | Scattered Lapsus$ Hunters is Scattered Spider plus Lapsus$ plus ShinyHunters | A statement from the actors or a vendor separating the brands | Vendor report or actor communication | documentary | — |
| [Scattered Spider](/scattered-spider-actor-profile/) | The ~1 billion-record Salesforce claim | Independent confirmation of the record count | Victim, regulator or court statement | documentary | — |
| [The broker is the actor you can see](/sylvanite-access-layer/) | Dragos states it directly observed SYLVANITE handing established footholds to VOLTZITE, with the interval as short as days | A second consumer cluster, or a denial that the handoff happened | Vendor research or an incident report | documentary | — |
| [The broker is the actor you can see](/sylvanite-access-layer/) | SYLVANITE and UNC5174 are the same actor | Published shared infrastructure or code between SYLVANITE and UNC5174 | Vendor infrastructure research | documentary | — |
| [The broker is the actor you can see](/sylvanite-access-layer/) | The names overlapping SYLVANITE are best read as multiple entities under one direction, not one actor | A vendor states the overlapping clusters are one entity, or several named ones | Vendor report | documentary | — |
| [The broker is the actor you can see](/sylvanite-access-layer/) | UNC3236 is both an ATT&CK alias of Volt Typhoon and a Dragos overlap of SYLVANITE | ATT&CK changes the alias list for G1017 | ATT&CK group update | documentary | — |
| [The broker is the actor you can see](/sylvanite-access-layer/) | UNC5174 (Uteus) is assessed as a PRC access broker that attempted to sell access to edge-device victims | A government attribution of UNC5174 | Government advisory | documentary | — |
| [Volt Typhoon](/volt-typhoon-actor-profile/) | Assessed as pre-positioning for disruptive or destructive attacks against OT | A publicly confirmed disruptive or destructive effect attributed to the actor | A government advisory or a vendor incident report | documentary | — |
| [Volt Typhoon](/volt-typhoon-actor-profile/) | Dragos's VOLTZITE is the same actor as Volt Typhoon | A vendor or government statement that asserts or denies identity | A joint advisory or an ATT&CK group change | documentary | — |
| [Volt Typhoon](/volt-typhoon-actor-profile/) | Initial access increasingly brokered by SYLVANITE and handed to Volt Typhoon/VOLTZITE | A statement on SYLVANITE tasking, or a second consumer cluster | Vendor research or a joint advisory | documentary | — |
| [Volt Typhoon](/volt-typhoon-actor-profile/) | Operated by the PLA Cyberspace Force | A government statement naming the unit | An indictment, an advisory, or an official attribution | documentary | — |
<!-- falsification:end -->

## Why a condition beats a label

A confidence label tells you how much to trust a judgement today. A falsification condition
tells you what would make it wrong tomorrow, and it can be checked by someone who does not
trust the author. The second is harder to write and more useful: it turns a claim into a test.

## Why some of these expire

A documentary condition — a vendor asserting identity, a government naming a unit, ATT&CK
changing an alias — does not decay. If the statement is never made, the question stays open,
and an arbitrary expiry would only manufacture urgency.

A technical or behavioural condition does decay. A successor botnet, a new sector wave, a
resumption after arrests: each has a window in which it would mean something, and after it the
absence of the event is itself information. So those triggers carry a date, and an expired one
fails the build. The review is not a calendar ritual; it is the moment the evidence went stale.

## What happens when one fires

A trigger firing is not a correction by itself. It opens a review: the claim is re-graded
against the new evidence, and if the judgement changes, the product gets a new version and a
row in its revision history — never a silent edit. The gate enforces the shape; the analyst
decides the judgement.

## The limit

A condition is worth what the watching is worth. Nothing in a static repository notices that a
government published an advisory at 2am, which is why one source — the ATT&CK collection — is
checked weekly by a job that opens an issue when it moves. The rest depend on a person
reading, and that is stated rather than implied.
