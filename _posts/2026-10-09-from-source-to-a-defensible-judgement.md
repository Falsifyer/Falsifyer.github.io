---
layout: post
title: "From source to a defensible judgement: the method behind the tooling"
date: 2026-10-09
categories: threat-intelligence
summary: "How a judgement earns its confidence, what would overturn it, and the tooling that makes the hard part impossible to skip."
description: "How a source becomes a defensible judgement: two-axis grading, ACH, a computed ceiling and a corrections loop that leaves a trace."
kind: "Method note"
---

| | |
|---|---|
| **Product** | Method note |
| **Handling** | TLP:CLEAR — open sources only |
| **Version** | 1.1 (2026-10-28) |
| **Review trigger** | A change to the method, or a case that breaks it |
| **Next review** | 2027-04-30 |
| **Author** | Martín Eliseo |

## Bottom line

A judgement is defensible when a reader can see **why** it was reached and **what would
overturn it**. This note describes the method I use to get there — and the tooling that
encodes it so the hard part cannot be skipped.

## The problem: the names drift

Ask five vendors who an actor is and you may get five names. *Volt Typhoon*, *VOLTZITE*,
*Insidious Taurus*, *BRONZE SILHOUETTE*, *UNC3236*. Platforms then store those names as a
**flat list of aliases**, which quietly turns a hypothesis into a fact: if two names sit
together, they "are" the same actor. The reasoning is lost, the confidence is unstated,
and a decision — an incident response, a procurement choice, a threat hunt — is made on
ground that no longer shows why it holds.

I worked through one instance of this by hand in
[Is VOLTZITE the same actor as Volt Typhoon?](/ach-voltzite-volt-typhoon/). This note is
the step from doing it once to doing it repeatably.

## The method

Four rules do the work.

**1. A merge is a hypothesis, not a fact.** Two names are compared, never collapsed. The
link between them is a graded edge that carries its evidence and can be split again by
lowering a threshold — the reasoning is never deleted.

**2. Evidence is typed by diagnostic strength.** Infrastructure, code and operator
artefacts can bear on identity; shared tradecraft cannot. This is the trap: two actors can
share tooling, binaries and C2 paths without being one organisation, so TTP overlap must
not, on its own, sustain an identity claim.

**3. Two axes, per claim.** *Confidence* — how good the sourcing and reasoning are — is
kept separate from *probability* — how likely the outcome is. A claim can be very likely
at low confidence (a single source) or roughly even at high confidence (strong data,
genuine uncertainty). Conflating the two is the most common tradecraft error.

**4. Truth is external, and disagreement is a result.** A binary judgement is admitted
only if independent sources actually assert it; a single source is not corroboration, and
a disagreement between sources is recorded as *contested*, not decided. An alias list is
weaker than an identity claim, and the method says so.

## From method to tooling

Prose does not stop you skipping the hard part on a busy Tuesday; a program does. So each
rule above is encoded. The tools are small on purpose — the interesting thing is the rule,
not the line count. What they share is that they refuse to let a claim pass without its
evidence, its confidence, and a statement of what would change it. The
[engineering page](/engineering/) walks through each one.

## What this does not prove

- The checks are heuristics where the truth is not a schema; they are stated as such.
- External truth for a *specific* alias pair is scarce; a corpus that is mostly contested
  is a finding, not a failure.
- The method is single-author. It is a standard, not a peer review.

## The numbers

The suite is public and MIT-licensed, and it runs in CI:
[github.com/Falsifyer/Defensible-CTI](https://github.com/Falsifyer/Defensible-CTI). I don't copy test counts into
prose — a number in a blog post goes stale, and the whole point of the tooling is that the claim can
be checked at source. What the CI checks:

- the reconciliation engine against an adjudicated corpus with a committed coverage baseline, with
  STIX output validated against the reference library;
- the handling gate against FIRST TLP 2.0 and STIX 2.1, where the ground truth is a schema and not
  an opinion;
- the hunting planner and the assessment ledger, whose *refusals* are the behaviour under test.

---

*A judgement is finished only when it changes a decision — and when someone can see why.*

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-09 | First release. |
| 1.1 | 2026-10-28 | Handling corrected from the retired TLP 1.0 label to `TLP:CLEAR`; test counts replaced by the CI they come from. No assessed fact changed. |
