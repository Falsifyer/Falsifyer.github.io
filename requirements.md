---
layout: page
title: Requirements
kicker: "Direction"
description: "The standing questions this site is asked to answer, decomposed into essential elements of information, collection and the gaps that remain."
permalink: /requirements/
---

What this site is asked to answer, and why. Direction is part of tradecraft: an assessment that
answers a question nobody asked is not intelligence.

## Standing requirements

| ID | Priority intelligence requirement (PIR) | Why it matters |
|---|---|---|
| PIR-1 | Which actors pose a credible disruptive or destructive intent against critical infrastructure and OT? | Pre-positioning changes the risk calculus for infrastructure defenders. |
| PIR-2 | How do actors obtain and abuse identity as initial access, and which controls break it? | Identity is the current perimeter; it drives the highest-value mitigation. |
| PIR-3 | Where do vendor designations diverge, and how much confidence does the evidence support for each claim? | Naming drives attribution, hunting and procurement decisions. |
| PIR-4 | Which criminal operations target account takeover and payment fraud, and which controls break them? | Fraud is the most common financially motivated outcome, and the controls that stop it are transaction controls, not intrusion controls. |

## Essential elements of information

| PIR | EEI | Collection | Product |
|---|---|---|---|
| PIR-1 | Sector targeting; stage in the ICS Cyber Kill Chain; access mechanism; exploited CVEs | Government advisories (CISA/NSA), MITRE ATT&CK campaigns, OT vendor reporting | [Volt Typhoon profile](/volt-typhoon-actor-profile/) · [ACH assessment](/ach-voltzite-volt-typhoon/) · [Access layer](/sylvanite-access-layer/) |
| PIR-2 | Vishing/MFA tactics; IdP manipulation; help-desk abuse; RMM misuse | CISA advisories, MITRE ATT&CK, vendor CTI | [Scattered Spider profile](/scattered-spider-actor-profile/) |
| PIR-3 | Alias mapping; vendor language; confidence gradations | MITRE ATT&CK groups, vendor reports, advisories | Naming sections in each profile · [ACH assessment](/ach-voltzite-volt-typhoon/) · [Access layer](/sylvanite-access-layer/) |
| PIR-4 | Loader and delivery chain; targeted banks and countries; operator model; transaction controls | Vendor malware research, law-enforcement statements, banking-fraud reporting | [Grandoreiro profile](/grandoreiro-actor-profile/) |

## Collection and cadence

- **Standing:** government advisories, MITRE ATT&CK, vendor CTI reports.
- **Ad hoc:** a new advisory or an incident triggers a review — see each product's *review trigger*.
- **Open sources only**, and every claim carries a source and a grade (see [Method](/method/)).

## Current gaps in direction

- No requirement yet covers **sector-specific** pre-positioning (for example, water versus energy).
- **Access brokers** are noted but are not tracked as their own requirement.
- **Fraud** was added as PIR-4 on 2026-10-29, when the Grandoreiro profile was published; it is the
  only product answering it so far.
- No **strategic-level** product line (horizon scanning); current products are actor-focused.

## Review

Requirements are reviewed when a review trigger fires or a gap closes. Last updated 2026-10-29.

---

*All analysis is open-source. Views are my own.*
