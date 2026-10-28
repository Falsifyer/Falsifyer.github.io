---
layout: page
title: Engineering
permalink: /engineering/
---

I don't only consume platforms — I encode the intelligence method into tooling, so the
discipline is enforced by construction rather than remembered. Each tool below is a working
program with tests, a continuous-integration job and a security boundary, not a script.

They are now one suite of six commands in one workspace, running as a single chain:
requirement (`pir`) → judgement (`cryptonym`) → ledger (`assessment`) → hunt plan
(`huntplan`) → STIX product (`stixforge`) → gate (`sharegate`). One command runs the six in
order on fictional data, which is also the regression test.

They are now one suite of six commands in one workspace, running as a single chain:
requirement (`pir`) → judgement (`cryptonym`) → ledger (`assessment`) → hunt plan
(`huntplan`) → STIX product (`stixforge`) → gate (`sharegate`). One command runs the six
in order on fictional data, which is also the regression test.

The suite is public and MIT-licensed: [github.com/Falsifyer/Defensible-CTI](https://github.com/Falsifyer/Defensible-CTI),
with its tests and CI runs. The corpus it is evaluated against stays private; the code that
applies the method does not.

## pir — a requirement tied to a decision

**Problem.** Collection starts from interest, not from a decision: a topic list dressed up
as intelligence requirements.

**Method.** A PIR must name the decision it informs, the consumer and the graded indicator
that would close it. The validator rejects the register when any of the three is missing,
so "we should watch X" cannot pass as a requirement.

**Evidence.** The broken cases are fixtures — no decision, no consumer, an indicator
without an Admiralty grade — and each one fails the run.

## cryptonym — deciding whether two vendor names are the same actor

**Problem.** Vendors disagree on names — *Volt Typhoon*, *VOLTZITE*, *Insidious Taurus* —
and platforms store aliases as a flat list of assertions. Identity becomes an accident of
data entry.

**Method.** Treat a merge as a hypothesis. Evidence is typed by diagnostic strength:
infrastructure, code and operator artefacts can bear on identity; shared tradecraft
cannot. Competing explanations are tested with Analysis of Competing Hypotheses, and every
claim carries two axes — confidence and probability — kept separate. An external-truth
filter admits a binary truth only when *independent* sources assert it; genuine
disagreement is recorded as contested, not resolved by fiat.

**Evidence.** An adjudicated corpus with a committed coverage baseline; STIX 2.1 output
validated against the reference library in CI. The test count is reported by CI rather than
copied here, because a number in prose goes stale: see the
[workflow runs](https://github.com/Falsifyer/Defensible-CTI/actions).

## assessment — a ledger of graded judgements

**Problem.** Judgements live in prose: never re-derivable, comparable or diffable.

**Method.** Any claim gets the same discipline — evidence, competing hypotheses, two axes,
and an external truth that must be earned — and a persistent ledger.

**Evidence.** Tested in CI, including the case that matters: a declared confidence above
what the evidence supports is refused, not warned about. It consumes the shared core
(`cti-method`), so the method is inherited, not reimplemented.

## huntplan — turning a question into a falsifiable hunt

**Problem.** "Hunting" that is really browsing: no hypothesis, no way to close.

**Method.** Force a falsifiable *If … then …*, name the ATT&CK detection strategies that would
satisfy it — ATT&CK v18 retired data sources in favour of detection strategies — and require a
closure criterion. Maturity is scored against the Hunting Maturity Model.

**Evidence.** Tested in CI; the hypothesis checks are stated as heuristics, not guarantees.

## stixforge — a product that says who says it

**Problem.** Sharing starts at the export dialog. The bundle leaves without a marking, or
with a marking nobody can defend.

**Method.** Build the bundle from the product — marking, identity, observables, indicators
and a report referencing them — with deterministic identifiers. The identifier travels as
`<id>@<sha256:12>`, so an edited assessment no longer keeps the same identity silently, and
a retired TLP 1.0 marking is refused rather than emitted.

**Evidence.** The factory refuses to emit a product carrying the retired TLP 1.0 label, and
the factory and the gate call one STIX validator — a test asserts both report identical
findings.

## sharegate — a handling check before a product leaves the building

**Problem.** Most leaks are mundane: a missing TLP marking, a conflicting one, a
`TLP:CLEAR` on sensitive content, or malformed STIX.

**Method.** Two objective gates judged against published specifications — FIRST TLP 2.0
and STIX 2.1 — including a permissive-mark-on-sensitive-content check.

**Evidence.** Tested in CI. Because the ground truth is a schema, the checks are not
opinions. The same gate runs on this site's own products: see `scripts/sitegate.py`.

---

## The gate on itself

`scripts/sitegate.py` runs on every push against this site's products, and it checks the
things a reader would otherwise check by hand:

- **handling** — the TLP rules, delegated to `sharegate`;
- **versioning** — a version in the header must exist in the revision history;
- **freshness** — a product past its **next review** date fails the build;
- **vocabulary** — confidence and probability come from the declared lexicons;
- **cross-product consistency** — the same claim, stated in two products, must carry the same
  grade; wording is normalised, so a contradiction is found rather than declared.

The last one is not hypothetical: it is the check that would have caught two products grading the
same identity claim differently two days apart. A contradiction between products is now a build
failure, not a reader's discovery.

---

The code is public and the runs are public; the corpus it is evaluated against is not. The
method and the evidence are here — and I am glad to walk through any of them.

*Every tool encodes a rule that stops you skipping the hard part: grade the claim, earn
the truth, state what would change your mind.*
