---
layout: post
title: "Volt Typhoon: an actor profile built from open sources"
date: 2026-10-07
categories: threat-intelligence
summary: "A living-off-the-land intrusion tracked from open sources, graded claim by claim, with the attribution kept to what the evidence carries and no further."
kind: "Actor profile"
---

| | |
|---|---|
| **Product** | Actor profile |
| **Handling** | TLP:CLEAR — open sources only |
| **Version** | 2.4 (2026-10-28) |
| **Review trigger** | MITRE ATT&CK or government update, a confirmed disruptive effect, or new edge-device exploitation |
| **Next review** | 2027-04-30 |
| **Author** | Martín Eliseo |

*Every claim below carries a source and is graded on two independent axes. Where vendors disagree, I
say so.*

## How to read this

Two axes are graded separately, per claim — not per section:

- **Confidence** — how good the sourcing and the reasoning are: **High** (corroborated by two or more
  independent authoritative sources), **Moderate** (one credible source, or corroboration with gaps),
  **Low** (single-source, self-claimed, or heavily inferential).
- **Probability** — how likely the assessed outcome is, stated only where the claim is estimative:
  *nearly certain*, *very likely*, *likely*, *roughly even chance*, *unlikely*, *very unlikely*.

They are not the same thing. A claim can be *very likely* at *low confidence* (a single source) or
*roughly even* at *high confidence* (strong data, genuine uncertainty). Purely factual claims are
graded for confidence only and carry *n/a* for probability. **Unverified** means it could not be
substantiated, and is recorded so it is not repeated as fact.

## Bottom line

Volt Typhoon is a People's Republic of China (PRC) state-sponsored intrusion set, active since at
least 2021, that targets critical infrastructure — above all **communications, energy, transportation
and water/wastewater** — in the continental United States, its territories (including Guam) and
Western-aligned countries. Its defining trait is not a tool but the absence of one: it prefers stolen
credentials, living-off-the-land (LOTL) binaries, hands-on-keyboard activity and web shells over
custom malware, and it hides behind chains of compromised SOHO routers and edge devices. U.S.
agencies assess the activity as **pre-positioning** for disruptive or destructive operations against
operational technology (OT) in the event of a crisis or conflict, not as espionage alone. Since 2025
the emphasis has moved from access to preparation: OT-focused reporting places a closely overlapping
cluster inside engineering workstations and cellular gateways — Stage 2 of the ICS Cyber Kill Chain —
with initial access increasingly brokered by a separate access cluster, SYLVANITE.

## 1. Identity and naming

The same activity is tracked under several designations:

| Designation | Attributed to |
|---|---|
| Volt Typhoon | Microsoft |
| BRONZE SILHOUETTE | Secureworks |
| Vanguard Panda | CrowdStrike |
| DEV-0391, Storm-0391 | Microsoft (initial designations) |
| UNC3236 | Mandiant / Google |
| Voltzite | Dragos |
| Insidious Taurus | Palo Alto Networks Unit 42 |
| Redfly | Symantec / Gen Digital |
| DazedToad | MITRE ATT&CK |
| G1017 | MITRE ATT&CK |

MITRE records these as **Associated Groups** [3], which is explicitly weaker than "same actor".
CISA lists Vanguard Panda, BRONZE SILHOUETTE, Dev-0391, UNC3236, Voltzite and Insidious Taurus as
aliases in its advisory [1].

**Caveat — low confidence.** Not every tracking name is asserted to be the same actor. Dragos's
VOLTZITE is described as sharing "extensive technical overlaps" with Volt Typhoon rather than being
declared identical [7], and it is Dragos's analyst designation for the OT-facing activity. Read the
OT reporting as an **overlapping cluster**, not a single verified entity [3][7]. The same caution
applies one layer down: the access cluster that feeds this actor is itself a set of names, not a
name (§3).

## 2. Assessment ledger

<!-- claims:begin -->
| Assessment | Confidence | Probability | Basis |
|---|---|---|---|
| PRC state-sponsored, active since at least 2021 | Moderate | n/a | [1][3] |
| Targets communications, energy, transportation and water/wastewater in the US and its territories, including Guam | Moderate | n/a | [1] |
| Assessed as pre-positioning for disruptive or destructive attacks against OT | Moderate | likely | [1][3] |
| Living-off-the-land tradecraft: stolen credentials, `wmic`/`ntdsutil`/`netsh`/PowerShell, minimal custom malware | Moderate | n/a | [1][3] |
| Uses compromised SOHO routers (KV Botnet and successors) to proxy C2 and obscure origin | High | n/a | [1][6][8] |
| Exploited the Versa Director zero-day CVE-2024-39717 with the VersaMem web shell | Moderate | n/a | [3][9] |
| Deployed the SockDetour backdoor in at least one intrusion | Moderate | n/a | [10] |
| Initial access increasingly brokered by SYLVANITE and handed to Volt Typhoon/VOLTZITE | Moderate | likely | [7][12] |
| Reached Stage 2 of the ICS Cyber Kill Chain in 2025 (engineering workstations, cellular gateways) | Moderate | n/a | [7] |
| Operated by the PLA Cyberspace Force | Low | n/a | [11] |
| Dragos's VOLTZITE is the same actor as Volt Typhoon | Low | roughly even chance | [3][7] · [ACH](/ach-voltzite-volt-typhoon/) |
<!-- claims:end -->

## 3. Tradecraft

**Living off the land, by design.** The actor's signature is doing almost everything with tools that
are already on the host: `wmic`, `ntdsutil`, `netsh` and PowerShell, plus built-in remote-access
features, all under valid — usually stolen — accounts. The effect is that its traffic and its
process tree look like an administrator's. CISA's advisory documents the command lines and publishes
detection signatures precisely because there is no malware to fingerprint [1][3].

**Infrastructure obfuscation and proxying.** Rather than host its own command-and-control, it
builds chains of compromised small office/home office (SOHO) routers, mostly end-of-life Cisco and
Netgear devices, and proxies through them so that its traffic originates from U.S. IP addresses. The
FBI named the best-known instance the **KV Botnet** [6]; vendors and OT reporting have observed
successor botnets such as the JDY botnet after the takedown [7][8].

**Initial access through edge devices.** Volt Typhoon reaches victims by exploiting internet-facing
edge infrastructure — VPN gateways, firewalls and SD-WAN management — rather than user inboxes. In
mid-2024 it exploited a zero-day in Versa Director, CVE-2024-39717, tracked by MITRE as campaign
C0039, dropping a custom web shell (VersaMem) whose purpose was credential capture from managed
service providers and ISPs, to pivot into their downstream customers [3][9].

**The access layer is tracked separately, and by one vendor.** **SYLVANITE** is Dragos's designation
for an initial-access group active since 2023 that weaponises edge-device proofs of concept, harvests
credentials and hands established footholds to Stage 2 actors. Dragos states that it has directly
observed SYLVANITE transferring access to VOLTZITE, with the handoff possible within days [12]. Two
cautions belong here.

First, **MITRE does not record SYLVANITE as a group.** ATT&CK v20 — the version current when this
was checked — carries 193 enterprise groups and none is SYLVANITE, and G1017 does not mention it. What
MITRE records is *campaign* C0029, Cutting Edge — Ivanti Connect Secure zero-day exploitation from
December 2023 to February 2024, attributed variously to UNC5221/UTA0178 and UNC5325 [13]. A campaign
and a group are different objects, and citing one for the other is how a broker acquires a name it was
never given.

Second, **SYLVANITE is not a single name either.** Dragos lists it as overlapping UNC5221, UNC5174,
UNC5291, UNC3236, HOUKEN, Red Dev 61, CL-STA-0048 and UTA0178, and assesses those as *multiple
entities under the same overarching direction* [12]. Note what that list contains: UNC3236 is, in
ATT&CK, an alias of Volt Typhoon [3]. Read flatly — the convention most platforms use — UNC3236 is
Volt Typhoon, and UNC3236 overlaps SYLVANITE, so SYLVANITE *is* Volt Typhoon, and the broker
disappears from the graph. No vendor asserts that. Overlap is not identity, and shared tooling is not
a shared operator: the honest unit here is an **access ecosystem**, not a broker.

**Persistence and credential theft.** Persistence leans on web shells and valid accounts, with at
least one documented use of **SockDetour**, a custom backdoor designed to survive the removal of a
primary access method [10]. The collection priority is credentials and the material needed to
understand and reach the target's operational environment.

## 4. Targeting

CISA's advisory is explicit about sectors — **Communications, Energy, Transportation Systems, and
Water and Wastewater Systems** — across the continental and non-continental United States, including
Guam [1]. Microsoft's tracking adds manufacturing, utilities, construction, maritime, government,
information technology, education, defense and media [4]. OT-focused reporting adds the operational
data itself: geographic information system (GIS) data, OT network diagrams and OT operating
instructions exfiltrated from ICS organisations [7][8]. In 2025, Dragos reported activity reaching
U.S. midstream pipeline operations through compromised Sierra Wireless AirLink cellular gateways,
and electric and oil-and-gas environments [7].

## 5. From access to pre-positioning (2025–2026)

This is the assessment that makes Volt Typhoon different from a data-theft crew, and it is the one
to hold carefully. The U.S. government's stated view is that the PRC is positioning itself to
launch destructive attacks that would threaten physical safety and impede military readiness in a
crisis or conflict [1] — an assessment about **intent and preparation**, not a report of observed
destruction.

What changed in 2025 is that OT reporting moved the activity further along that path. Dragos placed
VOLTZITE at **Stage 2 of the ICS Cyber Kill Chain**: manipulating engineering workstation software
to extract configuration files and alarm data, and specifically investigating what operational
conditions would trigger process shutdowns — reconnaissance of *how to disrupt*, not disruption
itself [7]. Initial access is increasingly brokered: SYLVANITE weaponises edge-device vulnerabilities
and hands footholds over for the deeper OT intrusion [7][12]. No publicly confirmed disruptive effect
has been observed. What is **corroborated** here is only that the actor has the access and is
collecting the data; the disruptive end state remains an assessed intent [1][7].

## 6. Disruption and current status

- **KV Botnet disrupted.** Following a December 2023 court-authorised operation, the FBI announced on
  31 January 2024 that it had remotely removed the KV Botnet malware from hundreds of U.S.-based
  SOHO routers and severed their command-and-control [6].
- **Temporary, and replaced.** The FBI noted the remediation was temporary — a router reboot could
  reverse it — and that the devices remained vulnerable [6]. Dragos observed the botnet being
  rebuilt and successor infrastructure in use afterwards [7][8].
- **Not deterred.** Activity continued through 2025 and, by OT reporting, deepened [7].
- Assessment: **infrastructure degraded, intent unchanged**. Takedowns cost the actor proxies, not
  access to its objectives [6][7].

## 7. What this means for defenders

Ordered by how directly they attack this actor's playbook:

1. **Inventory and patch the edge.** VPN gateways, firewalls and SD-WAN managers are the front door.
   Known-exploited CVEs here, and end-of-life devices, are the single highest-value fix [9].
2. **Assume stolen credentials are in play.** Phishing-resistant MFA, credential hygiene and
   privilege tiering — the actor's whole method depends on valid accounts that look legitimate [1].
3. **Log the identity and remote-access planes.** Authentication, VPN and RDP events, plus process
   telemetry (EDR/Sysmon), because the malicious activity is native behaviour [1].
4. **Hunt the LOTL command lines.** `ntdsutil` credential extraction, `wmic`/`netsh` used by
   unexpected parents, and PowerShell that does not match administrative baselines [1][3].
5. **Watch egress to SOHO and edge ranges.** Encrypted sessions to compromised consumer routers, and
   the non-standard TCP-then-HTTPS pattern MITRE documents for C0039, are high-signal [3][9].
6. **Segment and monitor OT.** Engineering-workstation configuration and alarm data, and cellular
   gateways, are the current collection targets — monitor reads, not just writes [7].
7. **Treat "no alerts" as "no evidence".** For an actor whose method is native tools and valid
   accounts, absence of detections is not absence of the actor [1][3].

## 8. Detection opportunities

What to look for, not a validated ruleset (consistent with the rule-provenance policy I use elsewhere):

- `ntdsutil` invoking `ac i ntds` to create an IFM (Install From Media) copy — credential dumping that
  needs no external tool.
- `wmic`, `netsh` or PowerShell spawned by service, web-server or backup processes rather than an
  interactive admin session.
- A new web shell or unexpected file on an SD-WAN manager, VPN appliance or firewall.
- Long-lived encrypted sessions from a host to consumer/SOHO router address space, and the
  non-standard TCP handshake followed by HTTPS command-and-control from campaign C0039 [3][9].
- On OT networks: reads of GIS data, OT network diagrams, alarm configuration or engineering
  workstation configuration files by accounts outside the engineering baseline [7].

## 9. Intelligence gaps and what I could not verify

- Whether VOLTZITE (Dragos) and Volt Typhoon (Microsoft and the U.S. government) are one actor or an
  overlapping ecosystem; the naming is explicitly "technical overlap", not identity [3][7].
- Whether the eight names Dragos lists as overlapping SYLVANITE are one entity. Dragos assesses
  multiple entities under one overarching direction, which is not the same as a single broker, and no
  public source resolves it [12].
- Unit-level attribution — the claim that the group is run by the PLA Cyberspace Force is public
  reporting, not a government confirmation, and is treated as low confidence [11].
- Whether the pre-positioning has translated into any confirmed disruptive or destructive effect.
  None is public; the disruptive end state is an assessed intent [1][7].
- Victim enumeration is inherently incomplete — CISA's own framing is that what has been found is
  likely "the tip of the iceberg" [1].
- Nothing here is validated against private telemetry, and I did not analyse malware samples for this
  profile. This is an open-source assessment, and it is bounded by that.

## 10. Outlook — what would change this judgement

- A **MITRE ATT&CK or government update** that merges or separates VOLTZITE and Volt Typhoon, or
  reassigns the group/campaign IDs.
- Any **publicly confirmed disruptive or destructive effect**; that would move the pre-positioning
  judgement from assessed intent to observed action.
- New **edge-device exploitation** (a fresh known-exploited CVE) or a new access-broker cluster.
- A change in the **SOHO botnet** layer — successor infrastructure, or a takedown that holds.

## Sources

1. CISA, NSA, FBI and international partners — **Joint Cybersecurity Advisory AA24-038A: PRC
   State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure**
   (7 Feb 2024). https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a
2. CISA, NSA, FBI and partners — **Joint Cybersecurity Advisory AA23-144A: PRC State-Sponsored
   Cyber Actor Living off the Land to Evade Detection** (24 May 2023).
   https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-144a
3. MITRE ATT&CK — **Group G1017: Volt Typhoon** (v2.0, last modified 31 Jul 2026).
   https://attack.mitre.org/groups/G1017
4. Microsoft Threat Intelligence — **Volt Typhoon (VANGUARD PANDA)**.
   https://www.microsoft.com/en-us/security/security-insider/threat-landscape/volt-typhoon
5. CISA, NSA and partners — **Identifying and Mitigating Living Off the Land Techniques** (joint
   guidance, Feb 2024). https://www.cisa.gov/resources-tools/resources/identifying-and-mitigating-living-land-techniques
6. U.S. Department of Justice — **U.S. Government Disrupts Botnet PRC Used to Conceal Hacking of
   Critical Infrastructure** (31 Jan 2024).
   https://www.justice.gov/opa/pr/us-government-disrupts-botnet-peoples-republic-china-used-conceal-hacking-critical
7. Dragos — **OT/ICS Cybersecurity Report 2026: Year in Review** (17 Feb 2026).
   https://www.dragos.com/resources/press-release/dragos-2026-year-in-review-new-ot-threats-ransomware
8. Dragos — **OT/ICS Cybersecurity Report 2025: Year in Review** (25 Feb 2025).
   https://www.dragos.com/resources/press-release/dragos-reports-ot-ics-cyber-threats-escalate-amid-geopolitical-conflicts-and-increasing-ransomware-attacks
9. MITRE ATT&CK — **Campaign C0039: Versa Director Zero Day Exploitation** (June–August 2024), and
   Lumen Black Lotus Labs' exploitation report.
   https://attack.mitre.org/campaigns/C0039
10. Palo Alto Networks Unit 42 — **Threat Brief: Attacks on Critical Infrastructure Attributed to
    Insidious Taurus (Volt Typhoon)** (Feb 2024). https://unit42.paloaltonetworks.com/volt-typhoon-threat-brief/
11. Public reporting on unit-level attribution of the group (secondary source; treated as low
    confidence).
12. Dragos — **SYLVANITE** threat group page (accessed 28 Oct 2026). Records the group since 2023,
    the observed handoff to VOLTZITE, and the overlap list.
    https://www.dragos.com/threat/sylvanite/
13. MITRE ATT&CK — **Campaign C0029: Cutting Edge** (Ivanti Connect Secure exploitation,
    December 2023 – February 2024; last modified 31 Jul 2026).
    https://attack.mitre.org/campaigns/C0029

---

*All analysis is open-source. Views are my own.*

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-07 | First release. |
| 2.0 | 2026-10-09 | Split confidence and probability into two axes; added the product header, the outlook and this history. No assessed fact changed. |
| 2.1 | 2026-10-28 | The VOLTZITE identity row now carries the ACH's judgement (`unlikely`, ~20–45%) instead of `roughly even chance`, and points to the product that tests it. Handling corrected from the retired TLP 1.0 label to `TLP:CLEAR`, now checked in CI. No other assessed fact changed. |
| 2.2 | 2026-10-28 | Corrected the SYLVANITE attribution: MITRE records campaign C0029, not a group, and G1017 does not mention SYLVANITE. Added the overlap list — eight names, assessed by Dragos as multiple entities under one direction — including UNC3236, an ATT&CK alias of Volt Typhoon, and the reason overlap must not be read as identity. Ledger basis for the broker row moved from [3][7] to [7][12]. |
| 2.3 | 2026-10-28 | The identity row follows ACH v2.0: `roughly even chance` instead of `unlikely`, because v2 counts the naming observation once instead of three times. The probability changed; the confidence did not. |
| 2.4 | 2026-10-28 | Grades now computed from the claim registry. Five `High` became `Moderate`: MITRE G1017 derives from the CISA advisory, so it is not a second voice, and two ATT&CK objects are one publisher. The facts are unchanged; the confidence was overstated. |
