---
layout: post
title: "Scattered Spider: an actor profile built from open sources"
date: 2026-10-06
categories: threat-intelligence
summary: "An actor profile assembled from open reporting, with the vendor divergences left visible instead of flattened into a single confident story."
description: "A graded actor profile: identity-first intrusion, RMM abuse, hypervisor operations and ransomware, with the vendor divergences left visible."
kind: "Actor profile"
---

| | |
|---|---|
| **Product** | Actor profile |
| **Handling** | TLP:CLEAR — open sources only |
| **Version** | 2.2 (2026-10-28) |
| **Review trigger** | New government advisory, MITRE ATT&CK update, vendor re-assessment, or law-enforcement action |
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

Scattered Spider is a native-English-speaking, financially motivated intrusion set active since at
least 2022 whose primary attack surface is **people and identity, not software**. Its signature is
impersonating IT and help-desk staff to reset passwords and move MFA tokens, then abusing legitimate
remote-monitoring tools and cloud identity to hold an enterprise from the inside. Since 2024 it has
added hypervisor-level (VMware vSphere/ESXi) operations and ransomware to a data-extortion playbook,
and in 2025 a self-branded coalition — "Scattered Lapsus$ Hunters" — ran a large voice-phishing and
OAuth-theft campaign against SaaS (Salesforce) tenants. Law-enforcement arrests in 2025 slowed the
activity without stopping it.

## 1. Identity and naming

The same activity is tracked under several designations:

| Designation | Attributed to |
|---|---|
| Scattered Spider (early phase: Roasted 0ktapus) | CrowdStrike |
| UNC3944 | Mandiant / Google Threat Intelligence |
| Octo Tempest, Storm-0875 | Microsoft |
| Muddled Libra | Palo Alto Networks Unit 42 |
| 0ktapus | Group-IB |
| Scatter Swine | Okta |
| G1015 | MITRE ATT&CK |

CISA lists "UNC3944, Scatter Swine, Oktapus, Octo Tempest, Storm-0875, and Muddled Libra" as aliases
of Scattered Spider [1]; MITRE records them as **Associated Groups** [2], which is explicitly weaker
than "same actor".

**Caveat — low confidence.** These designations are not universally treated as co-referential. Public
analysis notes that the shared 0ktapus phishing kit was reused by multiple actors, and some vendor
assessments go as far as treating Muddled Libra as a distinct cluster despite overlapping tradecraft.
Read the aliases as an **overlapping cluster, not a verified single identity** [2][9].

## 2. Assessment ledger<!-- claims:begin -->

| Assessment | Confidence | Probability | Basis |
|---|---|---|---|
| Native-English-speaking, active since at least 2022 | Moderate | n/a | [2] |
| Initial access via help-desk vishing and MFA bypass (push bombing, SIM swap) | Moderate | n/a | [1][2] |
| Abuse of legitimate RMM tools (AnyDesk, TeamViewer, ScreenConnect, Splashtop, Tailscale, Teleport.sh) | Moderate | n/a | [1] |
| Registers its own MFA tokens and historically adds a federated IdP to the SSO tenant | Moderate | n/a | [1] |
| Hypervisor (vCenter/ESXi) operations | High | n/a | [2][3] |
| Ransomware: BlackCat, and DragonForce from 2025 | Moderate | n/a | [1][2] |
| Sector wave targeting (retail, insurance, airlines) | Moderate | likely | [3][4] |
| 2025 arrests slowed the group | Moderate | likely | [5] |
| Scattered Lapsus$ Hunters is Scattered Spider plus Lapsus$ plus ShinyHunters | Low | roughly even chance | [6][7][8] |
| The ~1 billion-record Salesforce claim | Low | unlikely | [6][7] |

<!-- claims:end -->

## 3. Tradecraft

**Initial access — the help desk is the perimeter.** Voice phishing (vishing) impersonating IT or
help-desk staff — or employees impersonating staff — to get passwords reset and MFA tokens
transferred, frequently across several calls ("layered social engineering"); MFA push bombing (MFA
fatigue); SIM swap to intercept one-time codes; and purchased credentials from criminal marketplaces,
including abuse of contracted third-party IT help desks. Lookalike domains mirror the target
(`<target>-helpdesk.com`, `<target>-okta.com`, `<target>-servicedesk.com`) [1][2].

**Identity persistence and privilege.** The actor registers its own MFA tokens and, historically, adds
a federated identity provider to the SSO tenant and enables automatic account linking — allowing
sign-in even after a password reset. It also modifies conditional-access policies and creates new
identities to survive response [1][2].

**Cloud and hypervisor.** It enumerates and abuses Okta, AWS, and Microsoft Entra ID, uses AWS Systems
Manager Inventory for discovery, and creates cloud instances for lateral movement and staging [1][2].
The 2025 pivot is notable: compromise of vSphere (vCenter Server), reboot into single-user mode,
deployment of Teleport for covert access, mounting domain-controller disks via "orphaned" VMs,
disabling backups, and running ransomware **from the ESXi shell** — which renders in-guest security
tooling ineffective [3].

**Discovery, collection, exfiltration.** It searches SharePoint, code repositories, credential-storage
documents, VPN/MFA enrollment guides and new-hire guides; reads Slack, Teams and Exchange for
conversations about the intrusion and the response; and — reported repeatedly — joins incident-response
calls to learn how defenders are hunting it [1][2]. Exfiltration targets include MEGA, AWS S3, and
Snowflake for mass extraction [1].

**Impact.** Dual extortion: data theft with the threat to leak it, plus encryption (BlackCat
historically; DragonForce in 2025, encrypting ESXi servers) [1][2].

## 4. Targeting

Initially CRM providers, business-process outsourcing, telecom and technology; from 2023 gaming,
hospitality, retail, MSP, manufacturing and financial [2]. In 2025, a concentrated wave against UK
retail and — per Google — US retail, airline and insurance [3][4].

## 5. The "Scattered Lapsus$ Hunters" branding (2025) — low confidence

A group self-branded **Scattered Lapsus$ Hunters** (also "Trinity of Chaos"), claiming to combine
Scattered Spider, Lapsus$ and ShinyHunters, ran a large campaign against Salesforce customers using
voice phishing and malicious OAuth applications — including abuse of Salesloft Drift tokens — with
claims reaching approximately one billion records across dozens of named organisations. Google tracks
related activity as UNC6040/UNC6395 and the FBI issued an advisory. Attribution rests largely on
**actor self-claims plus TTP overlap**; analysts caution the relationship may be a shared criminal
community rather than a single merged entity, and Salesforce disputes that its platform was
compromised. Treat this as context on a brand, not a confirmed organisational structure [6][7][8].

## 6. Disruption and current status

Arrests and guilty pleas in 2024–2026 prompted reporting in mid-2025 that UNC3944 activity had "gone
quiet", followed by continued or rebranded activity. Assessment: **degraded, not dismantled** [5].

## 7. What this means for defenders

Adapted from CISA's mitigations [1], ordered by how directly they attack this actor's playbook:

1. **Phishing-resistant MFA (FIDO2/WebAuthn).** This single control removes push bombing and SIM swap
   from the board.
2. **Help-desk verification.** Out-of-band identity checks for password resets, no MFA-token transfer
   over the phone, and alerting on reset-then-reenrolment bursts.
3. **Control remote access tools.** Allowlist execution and alert on portable RMM binaries.
4. **Harden the hypervisor.** No direct ESXi shell access, isolated/immutable backups, and monitoring
   of vCenter SSO and new admin roles.
5. **Watch the identity control plane.** New federated IdPs, new trusted locations, and new MFA device
   registrations are high-signal events here.
6. **Offline, tested backups.** The last line, and the one this actor specifically targets.

## 8. Detection opportunities

What to look for, not a validated ruleset (consistent with the rule-provenance policy I use elsewhere):

- A help-desk password reset followed within a short window by MFA re-registration for the same identity.
- A new federated identity provider or trusted location added to the IdP tenant.
- Portable RMM binaries running from user-writable paths, and their network beaconing.
- On vSphere: changes to the `ESX Admins` group, vCenter single-user-mode reboots, and Teleport
  service units.

## 9. Intelligence gaps and what I could not verify

- The exact structure and membership of "Scattered Lapsus$ Hunters" — one entity, or a brand over a
  community.
- Victim counts (actor claims, disputed by at least one platform vendor).
- The precise boundary between Scattered Spider, UNC3944 and Muddled Libra remains contested.
- Nothing here is validated against private telemetry, and I did not analyse malware samples for this
  profile. This is an open-source assessment, and it is bounded by that.

## 10. Outlook — what would change this judgement

The confidence above is a snapshot; these events would move it:

- A **new or revised advisory** (CISA AA23-320A, or MITRE ATT&CK group G1015) that merges the alias
  cluster or splits it — the single strongest lever on the naming judgement.
- Vendor reporting that **resolves Muddled Libra** as the same actor or as a distinct cluster.
- Attribution of **"Scattered Lapsus$ Hunters"** beyond actor self-claims and TTP overlap.
- Evidence the **ESXi/ransomware playbook** has changed (a new encryptor, or new hypervisor tradecraft).

## Sources

1. CISA, FBI, RCMP, ASD/ACSC, AFP, CCCS, NCSC-UK — **Cybersecurity Advisory AA23-320A: Scattered
   Spider** (last revised 29 Jul 2025). https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a
2. MITRE ATT&CK — **Group G1015: Scattered Spider** (v3.0, last modified 31 Jul 2026).
   <https://attack.mitre.org/groups/G1015>
3. Google Threat Intelligence Group — **Defending vSphere from UNC3944** (summarised by Infosecurity
   Magazine, 28 Jul 2025). https://cloud.google.com/blog/topics/threat-intelligence/defending-vsphere-from-unc3944
4. Google/GTIG via Computer Weekly — *Scattered Spider retail attacks spreading to US* (14 May 2025).
   <https://www.computerweekly.com/news/366623999/Scattered-Spider-retail-attacks-spreading-to-US-says-Google>
5. Infosecurity Magazine — *Cybercriminals 'Spooked' After Scattered Spider Arrests* (31 Jul 2025).
   <https://www.infosecurity-magazine.com/news/cybercriminals-spooked-scattered>
6. BleepingComputer — *ShinyHunters launches Salesforce data leak site to extort 39 victims* (3 Oct
   2025). https://www.bleepingcomputer.com/news/security/shinyhunters-starts-leaking-data-stolen-in-salesforce-attacks
7. SC Media — *New Scattered Lapsus$ Hunters escalates Salesforce extortion* (6 Oct 2025).
   <https://www.scworld.com/brief/new-scattered-lapsus-hunters-escalates-salesforce-extortion>
8. Computer Weekly — *ShinyHunters Salesforce cyber attacks explained* (11 Aug 2025).
   <https://www.computerweekly.com/feature/ShinyHunters-Salesforce-cyber-attacks-explained-What-you-need-to-know>
9. Vendor tracking names and the non-equivalence caveat, as reported in public actor-profile
   aggregations (secondary source; treated as low confidence).

---

*All analysis is open-source. Views are my own.*

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-06 | First release. |
| 2.0 | 2026-10-09 | Split confidence and probability into two axes; added the product header, the outlook and this history. No assessed fact changed. |
| 2.1 | 2026-10-28 | Handling corrected from the retired TLP 1.0 label to `TLP:CLEAR` (TLP 2.0), now checked in CI. No assessed fact changed. |
| 2.2 | 2026-10-28 | Grades now computed from the claim registry. Five `High` became `Moderate`: MITRE G1015 derives from the CISA-led advisory, and several rows rested on one source. The facts are unchanged; the confidence was overstated. |
