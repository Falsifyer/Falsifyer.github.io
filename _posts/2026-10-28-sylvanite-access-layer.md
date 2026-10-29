---
layout: post
title: "The broker is the actor you can see: SYLVANITE and the alias problem at the access layer"
date: 2026-10-28
categories: threat-intelligence
summary: "Dragos observed SYLVANITE handing footholds to VOLTZITE. What a defender should merge, and what must stay separate, when three vendors track one access layer as three different things."
description: "The access layer as an actor: SYLVANITE, the alias problem, and what a broker looks like when the buyer is the story."
kind: "Assessment"
---

| | |
|---|---|
| **Product** | Assessment (access layer, with a hunt plan) |
| **Handling** | TLP:CLEAR — open sources only |
| **Version** | 1.1 (2026-10-28) |
| **Review trigger** | A vendor or government statement linking the access clusters; a new edge-device campaign; a public incident that shows the handoff |
| **Next review** | 2027-04-30 |
| **Author** | Martín Eliseo |

*Every claim below carries a source and is graded on two independent axes. Where vendors disagree, I say so.*

## Bottom line

Three judgements, in the order a defender needs them:

1. **The access layer is tracked at three levels that are not interchangeable** — a MITRE *campaign*
   (C0029, Cutting Edge), a Dragos *group* (SYLVANITE) and Mandiant *clusters* (UNC5221, UNC5174,
   UNC5291). Flattening them into an alias list deletes the broker, which is the only part a defender
   can see before the OT intrusion starts.
2. **The handoff is a direct observation, not an inference from shared tradecraft.** Dragos states it
   observed SYLVANITE transferring access to VOLTZITE, with the interval as short as days [1]. That is
   a different class of evidence from the vendor language around identity, and it is enough to support
   a hunt.
3. **The broker is still not one entity.** Dragos assesses the names it lists as overlapping SYLVANITE
   as *multiple entities under the same overarching direction* [1]. The honest unit of analysis is an
   **access ecosystem**, not a broker — and the hunt below is written for the ecosystem.

## The decision this answers

[PIR-1](/requirements/) asks which actors pose a credible disruptive intent against OT; PIR-3 asks
where vendor designations diverge and how much confidence the evidence supports. This assessment sits
where they meet, because the access layer is where a divergence has an operational cost: if a
SYLVANITE compromise is the leading edge of a VOLTZITE intrusion, then an edge-device incident is an
OT-scope event, and the response clock starts at the appliance, not at the engineering workstation.

## Three levels, and why they are not the same object

| Level | What it is | Who records it | What it is *not* |
|---|---|---|---|
| **Campaign C0029** | Ivanti Connect Secure zero-day exploitation, Dec 2023 – Feb 2024, attributed variously to UNC5221/UTA0178 and UNC5325 [3] | MITRE ATT&CK | Not a group, and not a name for one |
| **SYLVANITE** | A Dragos-tracked initial-access group, active since 2023, that weaponises edge-device proofs of concept and hands footholds to Stage 2 actors [1] | Dragos | Not an assertion that its member clusters are one organisation |
| **UNC5221 / UNC5174 / UNC5291** | Mandiant cluster designations, some with a persona attached (UNC5174 = "Uteus") [2] | Mandiant / Google | Not campaign names, and not evidence of a single operator |

A campaign is an *event with a window*. A group is a *tracking construct*. A cluster is a *set of
activity with a shared toolset*. Citing one for another is how this layer acquired a false clarity:
the published Volt Typhoon profile did exactly that, and it was corrected on 2026-10-28 (profile v2.2).

## What was actually observed

**By Dragos.** SYLVANITE monitors vulnerability research and weaponises newly disclosed exploits,
in several cases compromising targets before the vendor had issued a patch. Its toolset includes
memory-resident web shells (Godzilla, LIGHTWIRE, WIREFIRE), Cobalt Strike, Sliver and SUPERSHELL, and
FRP for tunnelling; it harvests credentials from backend systems, including LDAP data and Office 365
tokens. Dragos states that it directly observed the group transferring access to VOLTZITE, and that
the handoff can occur within days of initial access [1].

**By Mandiant.** UNC5174, using the persona "Uteus", exploited F5 BIG-IP CVE-2023-46747 and
ConnectWise ScreenConnect CVE-2024-1709, and was observed *attempting to sell* access to U.S. defense
contractor and UK government victims. Mandiant assesses with moderate confidence that UNC5174 is a
PRC access broker with a claimed MSS affiliation [2]. One behaviour is worth keeping: after taking
access, UNC5174 ran the vendor's own mitigation script and removed an unrelated actor's account —
closing the door behind itself. Access was being treated as an asset, which is what a broker does.

**By MITRE.** C0029 records the campaign, its techniques (T1190, T1505.003, T1078.002, T1003.003,
T1572 among them) and its software (WIREFIRE, LIGHTWIRE, GLASSTOKEN) [3]. It does not record a group
called SYLVANITE — ATT&CK v20 carries 193 enterprise groups and none is SYLVANITE [4].

## The name graph, read flatly

```
MITRE (who is named)              Dragos (what is tracked)         Mandiant (what was seen)
─────────────────────             ────────────────────────         ────────────────────────
Volt Typhoon ──alias── UNC3236
        │                              ⋮ overlap
        │                         SYLVANITE ──overlap── UNC5221 / UTA0178 ──► campaign C0029
        │                              │                                  UNC5325
        │                              ├──overlap── UNC5174 ("Uteus")
        │                              ├──overlap── UNC5291
        │                              └──overlap── HOUKEN / Red Dev 61 / CL-STA-0048
        └───────────── handoff observed ──────────────┘
```

The trap is one edge. Dragos lists **UNC3236** among the names overlapping SYLVANITE [1]. ATT&CK
lists UNC3236 as an alias of Volt Typhoon [4]. Read with the flat alias convention most platforms
use — two names in one field are two names for one thing — UNC3236 is Volt Typhoon, UNC3236 overlaps
SYLVANITE, therefore SYLVANITE *is* Volt Typhoon, and the broker disappears from the graph.

No vendor asserts that. The record says "overlaps", which is a statement about shared activity, not
about shared organisation. This is the same error the [ACH](/ach-voltzite-volt-typhoon/) was written
to avoid, one layer down.

## Assessment ledger<!-- claims:begin -->

| Assessment | Confidence | Probability | Basis |
|---|---|---|---|
| SYLVANITE is a Dragos-tracked initial-access group active since 2023 that weaponises edge-device proofs of concept | Moderate | n/a | [1] |
| Dragos states it directly observed SYLVANITE handing established footholds to VOLTZITE, with the interval as short as days | Moderate | n/a | [1] |
| The names overlapping SYLVANITE are best read as multiple entities under one direction, not one actor | Moderate | likely | [1] |
| UNC5174 (Uteus) is assessed as a PRC access broker that attempted to sell access to edge-device victims | Moderate | likely | [2] |
| ATT&CK records C0029 as a campaign covering Ivanti exploitation, not a group named SYLVANITE | Moderate | n/a | [3][4] |
| UNC3236 is both an ATT&CK alias of Volt Typhoon and a Dragos overlap of SYLVANITE | High | n/a | [1][4] |
| SYLVANITE and UNC5174 are the same actor | Low | unlikely | [1][2] |

<!-- claims:end -->

The last two rows are the ones to hold carefully. Row 7 is *not* "unlikely" because the clusters look
different; it is "unlikely" because the only thing joining them is commodity tooling — SUPERSHELL is
used by the administrators of the framework as much as by any one customer — and because the tracking
vendor that knows the cluster best says the names are several entities. Row 8 is a judgement about
consequence, not about identity: it survives even if every cluster in the list turns out to be
separate.

## Hunt plan

The plan is written to be refuted. It is stored at
[`hunts/sylvanite-handoff.json`](/hunts/sylvanite-handoff.json) and validated with `huntplan` 0.2.0
(`ready: true`, no findings).

**Hypothesis.** If SYLVANITE handed access to VOLTZITE, then edge-appliance audit logs will show a
newly created local administrator account followed within 14 days by domain-account logons and
credential dumping on the same estate.

**Anchors** — the plan is only threat-informed if it names techniques: T1078 (valid accounts),
T1021 (remote services), T1003 (OS credential dumping), T1059 (command and scripting interpreter).

**What a hit looks like**, using the detection strategies the suite maps for those techniques:

- a local account created on a VPN/SD-WAN appliance or firewall, and the same identity authenticating
  to the domain (T1078; logon-session and account-metadata components);
- remote service use from that identity — RDP, SMB, SSH, WinRM (T1021; logon-session creation plus
  process creation on the destination);
- credential dumping on a host reached that way (T1003; process access, file access, LSASS/NTDS
  analytics);
- shell or scripting execution that does not match the administrative baseline on those hosts (T1059;
  process creation, command execution).

**Closure.** Confirmed if at least two incidents show the three stages in order within 14 days.
Refuted if, across three public incident reports or 90 days of telemetry, broker-stage artefacts are
absent in the majority, or the OT-facing stage systematically precedes them. A negative result closes
the hunt for that window; it does not establish that the actor is absent.

**One honest limit.** `huntplan` 0.2.0 ships a curated detection-strategy subset of 12 techniques and
does not include T1190, so the plan anchors the post-access stages it can map. The edge stage is
covered by the appliance's own audit log, which is where the hypothesis starts anyway.

## What would change this judgement

- A vendor or government statement that the clusters are one organisation, or that the handoff is a
  sale rather than a tasking relationship.
- Published infrastructure or code shared *between* the access clusters, as opposed to tooling
  shared across the ecosystem.
- Evidence that SYLVANITE serves more than one consumer cluster, which would confirm the broker model
  and weaken any single-actor reading.
- A disruptive effect attributed to this chain: that would move the whole assessment from access to
  consequence.

## Intelligence gaps

- The handoff is a single-vendor observation. No government advisory names SYLVANITE.
- "Access ecosystem" is a construct I am imposing to avoid a worse one; no source uses the term.
- Mandiant's UNC5174 assessment is from March 2024; the persona may have moved, been absorbed, or
  changed customers since.
- No telemetry, no infrastructure analysis, no malware samples: this is an open-source assessment and
  is bounded by that.
- Whether the same handoff pattern holds outside U.S. electric and water utilities is unknown.

## Sources

1. Dragos — **SYLVANITE** threat group page (accessed 28 Oct 2026).
   <https://www.dragos.com/threat/sylvanite/>
2. Mandiant — **Bringing Access Back — Initial Access Brokers Exploit F5 BIG-IP (CVE-2023-46747) and
   ScreenConnect** (21 Mar 2024).
   <https://cloud.google.com/blog/topics/threat-intelligence/initial-access-brokers-exploit-f5-screenconnect>
3. MITRE ATT&CK — **Campaign C0029: Cutting Edge** (last modified 31 Jul 2026).
   <https://attack.mitre.org/campaigns/C0029>
4. MITRE ATT&CK — **Group G1017: Volt Typhoon** (v2.0, last modified 31 Jul 2026).
   <https://attack.mitre.org/groups/G1017>
5. CISA, NSA, FBI and international partners — **Joint Cybersecurity Advisory AA24-038A** (7 Feb 2024).
   <https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a>

---

*All analysis is open-source. Views are my own.*

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-28 | First release. |
| 1.1 | 2026-10-28 | The operational recommendation left the ledger: a recommendation is not a claim, and the ledger now holds only what evidence can grade. It remains in the bottom line and in the defender section. Grades are computed from the claim registry. |
