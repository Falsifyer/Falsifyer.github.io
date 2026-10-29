---
layout: post
title: "Grandoreiro: a banking trojan that survived its operators"
date: 2026-10-29
categories: threat-intelligence
summary: "A Brazilian banking trojan run as a service, measured against what the arrests actually changed — and against the question the vendors still answer differently."
description: "A Brazilian banking trojan run as a service, measured against what the arrests changed — and the operator model the vendors still contest."
kind: "Malware profile"
---

| | |
|---|---|
| **Product** | Malware profile |
| **Handling** | TLP:CLEAR — open sources only |
| **Version** | 1.0.1 (2026-10-29) |
| **Review trigger** | A conviction, a new distributor, or a vendor resolving the operator model |
| **Next review** | 2027-04-30 |
| **Author** | Martín Eliseo |

*Every claim below carries a source and is graded on two independent axes. Where vendors
disagree, I say so — and on one question they disagree directly.*

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

Grandoreiro is a Delphi banking trojan of Brazilian origin, active since at least 2016 and
operated as a service with the code held closely. The January 2024 arrests of five administrators did not stop it: campaigns in 2024, 2025 and
2026 are documented by three independent vendors, and the codebase split rather than disappeared.

The interesting question is not whether it survived. It is **who runs it now**. IBM counts at
least three distributors; ESET, looking at the command-and-control backend, argues for one group
or a few groups cooperating closely; Kaspersky describes a service that fragmented after the
arrests. Read the operator model as **contested**, not as settled — that is where this product
departs from the vendor summaries.

## 1. What Grandoreiro is

A Windows banking trojan written in Delphi, Brazilian in origin and part of the family Kaspersky
calls the **Tetrade**, alongside Guildma, Javali and Melcoz [3][6]. MITRE records it as software
S0531, first observed in 2016 and using a malware-as-a-service model [7]. INTERPOL dates the
campaign against Spanish-speaking victims to 2017 [1]; the two are not in conflict — 2016 is the
first sample, 2017 the start of sustained targeting.

Its purpose is account takeover, not mass encryption. It watches the foreground window for a
banking site, overlays it, captures keystrokes and one-time codes, and lets an operator drive the
victim's machine to move money [2][3][4]. It also harvests addresses from the local Outlook
profile and uses the infected mailbox to send further phishing [3][4]. Older builds padded
themselves past 300 MB with bitmap resources to defeat scanning; that technique was dropped in
2023 [2][3].

The service model is unusual: Kaspersky found no underground advertisement for the Grandoreiro
package, and access to the source and builders appears limited to trusted partners [3]. That is
one of the reasons the operator question below is hard: a closed service and a small criminal
group look similar from the outside.

## 2. Assessment ledger<!-- claims:begin -->

| Assessment | Confidence | Probability | Basis |
|---|---|---|---|
| A Delphi banking trojan of Brazilian origin, part of the Tetrade family | High | n/a | [3][6][7] |
| Active since at least 2016, and tracked against Spanish-speaking victims since 2017 | High | n/a | [3][1] |
| Operated as a service, with access to the source and builders limited to trusted partners | Moderate | n/a | [3][4] |
| IBM tracks at least three distributors: Hive0148, Hive0149 and a third in development | Moderate | n/a | [5] |
| After the 2024 arrests the codebase split: a lighter variant focused on Mexico runs alongside the main one | Moderate | n/a | [3][6] |
| Targets more than 1,500 banking applications; the country count differs by vendor (45 in Kaspersky, 60+ in IBM) | High | n/a | [3][4] |
| In January 2024, five programmers and operators were arrested in Brazil, in an operation coordinated by INTERPOL with Spain | Moderate | n/a | [1][2] |
| Operations continued after the arrests: campaigns in 2024, 2025 and 2026 are documented by three independent vendors | High | n/a | [3][5][6] |
| The 2026 campaign used a DLL sideloading chain through Duplicate Files Finder, concentrated in Mexico | Moderate | n/a | [6] |
| At least EUR 3.5 million stolen in Spain, with more than EUR 110 million attempted per CaixaBank | Moderate | n/a | [1] |
| Grandoreiro is run by several distributors sharing a codebase, not one organisation | Moderate | roughly even chance | [5][3] |
| Grandoreiro is run by one group or a few closely cooperating groups | Moderate | roughly even chance | [2] |
| Grandoreiro is a vendor label applied to unrelated malware | Low | very unlikely | [3][6] |

<!-- claims:end -->

## 3. The operator question — three readings

Vendors agree on the malware and disagree on the organisation. Three readings survive long enough
to test:

| Reading | What it predicts | What the record shows |
|---|---|---|
| **One group, or a few groups cooperating closely** | A shared backend, load-balanced command and control, no independent forks | ESET found the backend admits one operator at a time, and 94% of observed victims sat in a single DGA cluster — its explicit conclusion was one group or a few cooperating [2] |
| **Several distributors on a shared codebase** | Divergent loaders, C2 and phishing themes; forks after disruption | IBM tracks at least three distributors (Hive0148, Hive0149, one in development) separated by loader, C2 and theme [5]; Kaspersky found two codebases running in parallel after the arrests [3] |
| **A label over unrelated malware** | No shared code between variants carrying the name | Shared string decryption, DGA design and Portuguese C2 tokens appear across variants [3][4][6] — this reading fails |

Both of the first two are supported by direct observation, and they are not the same claim. ESET's
argument is structural: if the same backend serialises operators and most victims land on one
cluster, several independent distributors are hard to sustain. IBM's is behavioural: three
distinct infection chains, loaders and themes are hard to sustain as one team. The honest grade
is that they are roughly evenly matched on public evidence, with the balance turning on whether
you weight backend architecture or distribution tradecraft.

What would settle it is not another summary but an artefact: shared infrastructure or shared code
between two named distributor clusters. Neither vendor publishes that link.

## 4. Tradecraft

**Delivery.** Phishing that impersonates the tax authority, the electricity utility, a court or a
telecom, in the target's language, with a geofenced redirect so that only victims in the intended
country receive the payload [1][4][5]. The archive carries a loader, often with a decoy PDF and
XML inside [6]. Over the years the first stage has been an MSI, a VBS dropper [5] and, in the
2026 campaign, a DLL sideloading chain [6].

**The 2026 loader.** Acronis documented a campaign in May 2026 that abuses the legitimate
**Duplicate Files Finder** application, renamed at random: the signed executable loads
`dupfdll.dll`, which loads a malicious `mingwm10.dll` from the same directory. The implant hides
the application window, checks system uptime, blacklists 49 analysis tools and looks for VMware
and VirtualBox artefacts before it contacts anything [6].

**Anti-analysis.** Uptime thresholds, a long process blacklist, VM driver and BIOS checks,
desktop-shortcut profiling, country blacklists (Russia, Czechia, the Netherlands in one sample)
and a fake "error opening document" dialog in Spanish when a sandbox is suspected [4][6].

**Command and control.** A domain generation algorithm rather than fixed infrastructure. IBM
counted 14 seeds in one sample, yielding 14 possible C2 domains per day, with seeds separated by
function — which is also how a service would keep its operators' traffic apart [4]. Resolution
goes through Google's DNS-over-HTTPS endpoint, and the port is derived from the resolved IP [4][6].
The C2 protocol speaks Portuguese: `CLIENT_SOLICITA_DDS_MODL`, `INFECTADO`, `AV_COMEU_MODULO` [4][6].

**Post-exploitation.** Screen blocking and overlays to capture OTPs, remote mouse and keyboard
control, keylogging, webcam control, clipboard replacement for crypto wallets, file transfer, and
detection of banking security products such as Trusteer and Topaz OFD [2][3][4]. Persistence is a
registry Run key plus encrypted `.CFG` and `.XML` files [4].

## 5. Targeting

Brazil, Mexico and Spain are the long-standing core. ESET's telemetry put Brazil at roughly 41% of
victims, Mexico at 30% and Spain at 28%, with a clear shift towards Mexico and Argentina in 2023
[2]. INTERPOL describes the operation as a threat across Spanish-speaking countries since 2017,
with money moved through mule networks and laundered back to Brazil [1]. Kaspersky measured the
target list growing from 900 banks in 40 countries in 2023 to 1,700 banks and 276 crypto wallets
in 45 countries in 2024 [3]; IBM, on its own sample set, reports more than 1,500 banking
applications in more than 60 countries [4]. The two counts are not reconcilable from public data,
and the difference is a reminder that these numbers describe a hardcoded list, not observed
victims.

IBM also documented expansion beyond the historical Brazil–Mexico–Spain core after the arrests
— South Africa, Argentina and the Indo-Pacific among the impersonated authorities [4]. Acronis's 2026 telemetry is more
conservative: Mexico accounts for the largest share, Spain and several Latin American countries
follow, and Europe and North America show only limited presence [6].

## 6. Disruption: what the arrests changed

In January 2024, Brazilian authorities arrested five programmers and operators, with searches
across five states, in an operation coordinated by INTERPOL and supported by Spain. Trend Micro,
Kaspersky, Group-IB and Scitum contributed analysis; ESET supplied technical analysis, statistics
and C2 indicators [1][2]. INTERPOL puts the Spanish losses at more than EUR 3.5 million, with
failed attempts that could have exceeded EUR 110 million according to CaixaBank [1].

What changed is visible; what it meant is not. Kaspersky observed a surge of Grandoreiro phishing
days after the arrests, and then two codebases in parallel — the updated one and a legacy build
aimed at about 30 Mexican banks, which it reads as a different developer working from older
source [3]. IBM saw Hive0148 campaigns in February–March 2025 against Mexico and Costa Rica [5].
Acronis saw a renewed campaign in May 2026 [6]. **Degraded and fragmented, not dismantled.**

I found no public record of a conviction of the arrested administrators. That is an absence of
evidence, not evidence that none happened: Brazilian and Spanish proceedings are not fully
visible in English-language open sources, and this product does not claim to have searched court
records.

## 7. What this means for defenders

The target is a customer's Windows endpoint, so the controls that matter are not the ones that
stop an intrusion into a corporate network:

1. **Break the loader chain.** Block executables launched from archive downloads and from
   user-writable paths, and alert on signed applications loading DLLs from their own directory —
   the 2026 chain depends on exactly that.
2. **Watch the two reconnaissance calls.** `ip-api.com` and `dns.google/resolve` in quick
   succession, followed by an outbound connection on an unusual high port, is a high-signal
   sequence for this family [4][6].
3. **Treat Outlook automation as suspicious.** A workstation harvesting addresses and sending
   mail at volume is not normal user behaviour [3][4].
4. **Harden the transaction, not only the login.** Overlay and OTP capture defeat password and
   SMS factors; transaction signing, device binding and out-of-band confirmation of the payee are
   the controls that survive an infected endpoint.
5. **Block known DGA-derived domains, but do not rely on it.** The DGA rotates daily and seeds
   change [4].

## 8. Detection opportunities

What to look for, not a validated ruleset:

- A renamed copy of Duplicate Files Finder loading `mingwm10.dll` from the same directory [6].
- A GUI process that hides its window, then queries `ip-api.com` and the BIOS registry key in
  quick succession [6].
- A DNS-over-HTTPS lookup to `dns.google/resolve?name=` immediately followed by TCP/6432 or
  another non-standard port [4][6].
- The token `CLIENT_SOLICITA_DDS_MODL` in egress traffic or process memory [4][6].
- Registry Run keys pointing at an executable under `C:\ProgramData\`, with encrypted `.CFG` and
  `.XML` files alongside [4].
- Outlook sending mail to many recipients from a single workstation, outside any marketing
  process [3][4].

## 9. Intelligence gaps and what I could not verify

- **The operator model.** The central question is contested and the two camps do not publish the
  artefact that would resolve it.
- **The counts.** 1,500 applications in 60+ countries (IBM) versus 1,700 in 45 (Kaspersky) cannot
  both be right as stated; neither vendor publishes its sample set.
- **Distributor boundaries.** Hive0148 and Hive0149 are IBM's clusters, defined by loader, C2 and
  theme. They are analytic constructs, not observed organisations.
- **The 2026 campaign's owner.** Acronis describes the campaign, not which distributor ran it.
- **Legal outcome.** No public conviction found in English-language sources.
- **Method limit.** This is an open-source profile. I did not analyse samples or use private
  telemetry, and I did not exhaust Portuguese- or Spanish-language court reporting.

## 10. Outlook — what would change this judgement

- A **conviction or indictment** naming operators, which would turn the arrest claim from a
  disruption event into an organisational finding.
- **Shared infrastructure or code** linking two named distributor clusters — the single strongest
  lever on the contested question.
- A **vendor merging or splitting** the distributor clusters, or ESET revising its single-group
  assessment against new backend evidence.
- A **new codebase** that abandons the legacy one, or a third fork, which would date the
  post-arrest split.
- A **new country wave** outside the current footprint, or a sustained pause longer than two
  quarters.

## Sources

1. INTERPOL — **Disrupting a Grandoreiro malware operation** (18 Mar 2024).
   <https://www.interpol.int/en/News-and-Events/News/2024/Disrupting-a-Grandoreiro-malware-operation>
2. ESET Research — **ESET takes part in global operation to disrupt the Grandoreiro banking
   trojan** (30 Jan 2024).
   <https://www.welivesecurity.com/en/eset-research/eset-takes-part-global-operation-disrupt-grandoreiro-banking-trojan/>
3. Kaspersky GReAT — **Grandoreiro, the global trojan with grandiose goals** (22 Oct 2024).
   <https://securelist.com/grandoreiro-banking-trojan/114257/>
4. IBM X-Force — **Grandoreiro banking trojan unleashed: X-Force observing emerging global
   campaigns** (2024).
   <https://www.ibm.com/think/x-force/grandoreiro-banking-trojan-unleashed>
5. IBM X-Force — **Hive0148 observed targeting Mexico and Costa Rica** (2025).
   <https://www.ibm.com/think/x-force/ibm-x-force-threat-analysis-hive0148-observed-targeting-mexico-costa-rica>
6. Acronis TRU — **Grandoreiro goes north: from Brazil to Mexico with a new DLL sideloading
   campaign** (19 Aug 2026).
   <https://www.acronis.com/en/tru/posts/grandoreiro-goes-north-from-brazil-to-mexico-with-a-new-dll-sideloading-campaign/>
7. MITRE ATT&CK — **Software S0531: Grandoreiro** (last modified 11 Apr 2024).
   <https://attack.mitre.org/software/S0531>

---

*All analysis is open-source. Views are my own.*

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-29 | First release. |
| 1.0.1 | 2026-10-29 | Corrected a geographic error: Argentina is in Latin America, so the expansion is beyond the historical core, not outside the region. Also tightened the wording of the arrests. No assessed fact changed. |
