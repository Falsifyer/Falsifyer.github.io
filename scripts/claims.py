#!/usr/bin/env python3
"""Validate a product's claim registry against the suite's ceiling.

The registry is the machine-readable form of a product's assessment: the evidence, the
hypotheses, and the declared grade. It exists so that a grade is **computed**, not typed:
the ceiling comes from ``cti_method.grading`` — the suite owns the rule — and the registry
only supplies the evidence and the declaration.

Two shapes, one file:

* **claim** — a statement with sources that each say whether they bear **directly** on it
  (``claims[]``). Independence is structural, through ``derived_from``.
* **ach** — competing hypotheses with typed evidence and a consistency cell per hypothesis
  (``hypotheses[]`` + ``evidence[]`` + ``judgements[]``). The ceiling is per hypothesis.
  A dossier may carry several independent questions under ``questions[]``; each is graded
  against its own hypotheses, so one question cannot inflate another's ceiling.

A file may carry both arrays. The class is metadata for the reader: the ceiling uses
``direct`` and the evidence type, and an author who marks an inference as direct is making
a judgement the gate cannot check.
"""

from __future__ import annotations

import inspect
import json
from datetime import date
from pathlib import Path
from typing import Any

from cti_method.evidence import Consistency, Evidence, EvidenceType
from cti_method.grading import check_declared, derived_grade

SCHEMA_VERSION = "1.0"
CLASSES = {"documented", "observed", "assessed", "inferential"}
TYPES = {"factual", "estimative"}
CONFIDENCE = {"high", "moderate", "low"}
PROBABILITY = {
    "nearly_certain",
    "very_likely",
    "likely",
    "roughly_even",
    "unlikely",
    "very_unlikely",
}
TRIGGER_TYPES = {"documentary", "technical", "behavioural"}


def load_bearing(item: dict[str, Any]) -> bool:
    """True when a reader would act on this claim, so it must carry a review trigger."""
    return (
        item.get("type") == "estimative"
        or item.get("confidence") == "high"
        or item.get("class") in {"observed", "assessed"}
    )


def check_triggers(
    item: dict[str, Any], today: date, label: str
) -> list[str]:
    """Findings for the review triggers attached to one claim or judgement."""
    blocking: list[str] = []
    triggers = item.get("triggers") or []
    if load_bearing(item) and not triggers:
        blocking.append(f"{label}: no review trigger on a claim a reader would act on")
    for trigger in triggers:
        tid = str(trigger.get("id") or label)
        kind = trigger.get("type")
        if kind not in TRIGGER_TYPES:
            blocking.append(f"{tid}: unknown trigger type '{kind}'")
        if not str(trigger.get("condition") or "").strip():
            blocking.append(f"{tid}: no condition")
        if not str(trigger.get("artifact") or "").strip():
            blocking.append(f"{tid}: no artifact that would satisfy it")
        expires = trigger.get("expires")
        if kind in {"technical", "behavioural"} and not expires:
            blocking.append(f"{tid}: a {kind} trigger needs an expiry date")
        if expires:
            try:
                due = date.fromisoformat(str(expires))
            except ValueError:
                blocking.append(f"{tid}: expiry '{expires}' is not an ISO date")
                continue
            if due < today:
                blocking.append(f"{tid}: expired on {due.isoformat()}: re-review the claim")
    return blocking


def suite_supports_claim_mode() -> bool:
    """True when the checked-out suite has the claim mode (cti-method >= 0.2.0)."""
    return "mode" in inspect.signature(derived_grade).parameters


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_for(slug: str, directory: Path) -> tuple[dict[str, Any] | None, Path]:
    path = directory / f"{slug}.json"
    if not path.is_file():
        return None, path
    return load(path), path


def _cycle(graph: dict[str, list[str]]) -> str | None:
    """Return a source id that takes part in a derivation cycle, if any."""
    state: dict[str, int] = {}

    def visit(node: str) -> str | None:
        if state.get(node) == 1:
            return node
        if state.get(node) == 2:
            return None
        state[node] = 1
        for child in graph.get(node, []):
            found = visit(child)
            if found:
                return found
        state[node] = 2
        return None

    for node in graph:
        found = visit(node)
        if found:
            return found
    return None


def _sources(document: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    blocking: list[str] = []
    sources = {str(item.get("id")): item for item in document.get("sources") or [] if item.get("id")}
    graph = {sid: [str(dep) for dep in item.get("derived_from") or []] for sid, item in sources.items()}
    for sid, deps in graph.items():
        for dep in deps:
            if dep == sid:
                blocking.append(f"source {sid} derives from itself")
            elif dep not in sources:
                blocking.append(f"source {sid} derives from unknown source {dep}")
    cycle = _cycle(graph)
    if cycle:
        blocking.append(f"derivation cycle through source {cycle}")
    return sources, blocking


def _claim_evidence(claim: dict[str, Any], sources: dict[str, dict[str, Any]]) -> list[Evidence]:
    items: list[Evidence] = []
    for index, source in enumerate(claim.get("sources") or [], start=1):
        entry = sources.get(str(source.get("id")), {})
        items.append(
            Evidence(
                id=f"{claim['id']}-E{index}",
                statement=str(claim.get("claim", "")),
                source=str(entry.get("publisher", source.get("id", ""))),
                type=EvidenceType.OPEN_SOURCE,
                source_id=str(source.get("id", "")),
                reliability=str(source.get("reliability", "")),
                direct=bool(source.get("direct", False)),
            )
        )
    return items


def check(
    document: dict[str, Any], slug: str, today: date | None = None
) -> tuple[list[str], list[str], dict[str, tuple[str, str, str]]]:
    """Return (blocking, advisory, claims-by-key) for one registry."""
    today = today or date.today()
    blocking: list[str] = []
    advisory: list[str] = []
    claims: dict[str, tuple[str, str, str]] = {}

    if document.get("schema_version") != SCHEMA_VERSION:
        blocking.append(f"schema_version must be {SCHEMA_VERSION}")
    if document.get("product") != slug:
        blocking.append(f"registry names product '{document.get('product')}', expected '{slug}'")

    sources, source_findings = _sources(document)
    blocking += source_findings

    questions = document.get("questions") or []
    if questions:
        for index, question in enumerate(questions, start=1):
            label = str(question.get("id") or f"question-{index}")
            if not question.get("id"):
                blocking.append(f"question {index}: no id")
            if not str(question.get("label") or "").strip():
                advisory.append(f"{label}: no label")
            found, notes, keys = _ach(question, sources, today)
            blocking += found
            advisory += notes
            claims.update(keys)
    elif document.get("hypotheses"):
        found, notes, keys = _ach(document, sources, today)
        blocking += found
        advisory += notes
        claims.update(keys)
    if document.get("claims"):
        found, notes, keys = _claims(document, sources, today)
        blocking += found
        advisory += notes
        claims.update(keys)
    if not questions and not document.get("hypotheses") and not document.get("claims"):
        blocking.append("registry carries neither questions, hypotheses nor claims")

    return blocking, advisory, claims


def _ach(
    document: dict[str, Any], sources: dict[str, dict[str, Any]], today: date
) -> tuple[list[str], list[str], dict[str, tuple[str, str, str]]]:
    blocking: list[str] = []
    advisory: list[str] = []
    claims: dict[str, tuple[str, str, str]] = {}

    hypotheses = [str(item.get("id")) for item in document.get("hypotheses") or [] if item.get("id")]
    if len(hypotheses) < 2:
        blocking.append("an ACH needs at least two competing hypotheses")
    if len(set(hypotheses)) != len(hypotheses):
        blocking.append("duplicate hypothesis id")

    evidence: list[Evidence] = []
    for item in document.get("evidence") or []:
        eid = str(item.get("id") or "")
        if not eid:
            blocking.append("evidence without an id")
            continue
        try:
            kind = EvidenceType(str(item.get("type")))
        except ValueError:
            blocking.append(f"{eid}: unknown evidence type '{item.get('type')}'")
            continue
        consistency: dict[str, Consistency] = {}
        for key, value in (item.get("consistency") or {}).items():
            if str(key) not in hypotheses:
                blocking.append(f"{eid}: consistency names unknown hypothesis {key}")
            try:
                consistency[str(key)] = Consistency(str(value))
            except ValueError:
                blocking.append(f"{eid}: invalid consistency '{value}'")
        source_id = str(item.get("source_id") or "")
        if source_id and source_id not in sources:
            blocking.append(f"{eid}: cites unknown source {source_id}")
        evidence.append(
            Evidence(
                id=eid,
                statement=str(item.get("statement", "")),
                source=str(sources.get(source_id, {}).get("publisher", source_id)),
                type=kind,
                consistency=consistency,
                source_id=source_id,
                reliability=str(item.get("reliability", "")),
            )
        )

    for judge in document.get("judgements") or []:
        hypothesis = str(judge.get("hypothesis"))
        if hypothesis not in hypotheses:
            blocking.append(f"judgement names unknown hypothesis {hypothesis}")
            continue
        if judge.get("confidence") not in CONFIDENCE:
            blocking.append(f"{hypothesis}: unknown confidence '{judge.get('confidence')}'")
            continue
        if judge.get("probability") is not None and judge.get("probability") not in PROBABILITY:
            blocking.append(f"{hypothesis}: unknown probability '{judge.get('probability')}'")
        blocking += check_triggers(judge, today, hypothesis)
        for finding in check_declared(
            judge.get("confidence"), evidence, list(sources.values()), favoured=hypothesis, mode="ach"
        ):
            if finding["severity"] == "high":
                blocking.append(f"{hypothesis}: {finding['message']}")
        derived = derived_grade(evidence, list(sources.values()), favoured=hypothesis, mode="ach")
        if derived["ceiling"] == "high" and judge.get("confidence") != "high":
            advisory.append(f"{hypothesis}: the evidence would support high")
        key = str(judge.get("key") or hypothesis)
        claims[key] = (
            str(judge.get("confidence")),
            str(judge.get("probability")),
            str(judge.get("claim") or hypothesis),
        )

    return blocking, advisory, claims


def _claims(
    document: dict[str, Any], sources: dict[str, dict[str, Any]], today: date
) -> tuple[list[str], list[str], dict[str, tuple[str, str, str]]]:
    blocking: list[str] = []
    advisory: list[str] = []
    claims: dict[str, tuple[str, str, str]] = {}

    seen: set[str] = set()
    for claim in document.get("claims") or []:
        cid = str(claim.get("id") or "")
        if not cid:
            blocking.append("claim without an id")
            continue
        if cid in seen:
            blocking.append(f"duplicate claim id {cid}")
        seen.add(cid)

        if claim.get("class") not in CLASSES:
            blocking.append(f"{cid}: unknown class '{claim.get('class')}'")
        if claim.get("type") not in TYPES:
            blocking.append(f"{cid}: unknown type '{claim.get('type')}'")
        if claim.get("confidence") not in CONFIDENCE:
            blocking.append(f"{cid}: unknown confidence '{claim.get('confidence')}'")
        if claim.get("probability") is not None and claim.get("probability") not in PROBABILITY:
            blocking.append(f"{cid}: unknown probability '{claim.get('probability')}'")
        blocking += check_triggers(claim, today, cid)

        refs = claim.get("sources") or []
        if not refs:
            blocking.append(f"{cid}: no sources")
            continue
        for ref in refs:
            if str(ref.get("id")) not in sources:
                blocking.append(f"{cid}: cites unknown source {ref.get('id')}")

        items = _claim_evidence(claim, sources)
        derived = derived_grade(items, list(sources.values()), mode="claim")
        for finding in check_declared(claim.get("confidence"), items, list(sources.values()), mode="claim"):
            if finding["severity"] == "high":
                blocking.append(f"{cid}: {finding['message']}")
        if derived["ceiling"] == "high" and claim.get("confidence") != "high":
            advisory.append(f"{cid}: the evidence would support high; the claim declares {claim.get('confidence')}")

        key = str(claim.get("key") or cid)
        claims[key] = (str(claim.get("confidence")), str(claim.get("probability")), str(claim.get("claim")))

    return blocking, advisory, claims
