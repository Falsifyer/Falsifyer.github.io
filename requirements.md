---
layout: page
title: Requirements
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

## Essential elements of information

| PIR | EEI | Collection | Product |
|---|---|---|---|
| PIR-1 | Sector targeting; stage in the ICS Cyber Kill Chain; access mechanism; exploited CVEs | Government advisories (CISA/NSA), MITRE ATT&CK campaigns, OT vendor reporting | [Volt Typhoon profile](/volt-typhoon-actor-profile/) · [ACH assessment](/ach-voltzite-volt-typhoon/) · [Access layer](/sylvanite-access-layer/) |
| PIR-2 | Vishing/MFA tactics; IdP manipulation; help-desk abuse; RMM misuse | CISA advisories, MITRE ATT&CK, vendor CTI | [Scattered Spider profile](/scattered-spider-actor-profile/) |
| PIR-3 | Alias mapping; vendor language; confidence gradations | MITRE ATT&CK groups, vendor reports, advisories | Naming sections in each profile · [ACH assessment](/ach-voltzite-volt-typhoon/) · [Access layer](/sylvanite-access-layer/) |

## Collection and cadence

- **Standing:** government advisories, MITRE ATT&CK, vendor CTI reports.
- **Ad hoc:** a new advisory or an incident triggers a review — see each product's *review trigger*.
- **Open sources only**, and every claim carries a source and a grade (see [Method](/method/)).

## Current gaps in direction

- No requirement yet covers **sector-specific** pre-positioning (for example, water versus energy).
- **Access brokers** are noted but are not tracked as their own requirement.
- No **strategic-level** product line (horizon scanning); current products are actor-focused.

## Review

Requirements are reviewed when a review trigger fires or a gap closes. Last updated 2026-10-09.

---

*All analysis is open-source. Views are my own.*
