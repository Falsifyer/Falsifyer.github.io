#!/usr/bin/env python3
"""Validate a product's claim registry against the suite's ceiling.

The registry is the machine-readable form of a product's assessment ledger. It exists so
that a grade is **computed**, not typed: the ceiling comes from
``cti_method.grading.ceiling(..., mode="claim")`` — the suite owns the rule — and the
registry only supplies the evidence and the declaration.

A claim is a statement with one or more sources. Each source says whether it bears
**directly** on the claim; independence is structural, through the source registry and
``derived_from``. The class is metadata for the reader: the ceiling uses `direct`, and an
author who marks an inference as direct is making a judgement the gate cannot check.

Schema (``schema_version`` 1.0)::

    {
      "schema_version": "1.0",
      "product": "2026-10-28-sylvanite-access-layer",
      "sources": [{"id": "S1", "publisher": "Dragos", "derived_from": []}],
      "claims": [
        {"id": "SYL-01", "key": "sylvanite.exists", "claim": "…",
         "class": "documented", "type": "factual",
         "confidence": "moderate", "probability": null,
         "sources": [{"id": "S1", "direct": true}]}
      ]
    }
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

from cti_method.evidence import Evidence, EvidenceType
from cti_method.grading import check_declared, derived_grade

SCHEMA_VERSION = "1.0"


def suite_supports_claim_mode() -> bool:
    """True when the checked-out suite has the claim mode (cti-method >= 0.2.0)."""
    return "mode" in inspect.signature(derived_grade).parameters
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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _evidence(claim: dict[str, Any], sources: dict[str, dict[str, Any]]) -> list[Evidence]:
    items: list[Evidence] = []
    for index, source in enumerate(claim.get("sources") or [], start=1):
        entry = sources.get(source.get("id", ""), {})
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


def check(document: dict[str, Any], slug: str) -> tuple[list[str], list[str], dict[str, tuple[str, str, str]]]:
    """Return (blocking, advisory, claims-by-key) for one registry."""
    blocking: list[str] = []
    advisory: list[str] = []
    claims: dict[str, tuple[str, str, str]] = {}

    if document.get("schema_version") != SCHEMA_VERSION:
        blocking.append(f"schema_version must be {SCHEMA_VERSION}")
    if document.get("product") != slug:
        blocking.append(f"registry names product '{document.get('product')}', expected '{slug}'")

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

    seen_ids: set[str] = set()
    for claim in document.get("claims") or []:
        cid = str(claim.get("id") or "")
        if not cid:
            blocking.append("claim without an id")
            continue
        if cid in seen_ids:
            blocking.append(f"duplicate claim id {cid}")
        seen_ids.add(cid)

        if claim.get("class") not in CLASSES:
            blocking.append(f"{cid}: unknown class '{claim.get('class')}'")
        if claim.get("type") not in TYPES:
            blocking.append(f"{cid}: unknown type '{claim.get('type')}'")
        if claim.get("confidence") not in CONFIDENCE:
            blocking.append(f"{cid}: unknown confidence '{claim.get('confidence')}'")
        if claim.get("probability") is not None and claim.get("probability") not in PROBABILITY:
            blocking.append(f"{cid}: unknown probability '{claim.get('probability')}'")

        refs = claim.get("sources") or []
        if not refs:
            blocking.append(f"{cid}: no sources")
            continue
        for ref in refs:
            if str(ref.get("id")) not in sources:
                blocking.append(f"{cid}: cites unknown source {ref.get('id')}")

        items = _evidence(claim, sources)
        derived = derived_grade(items, list(sources.values()), mode="claim")
        for finding in check_declared(claim.get("confidence"), items, list(sources.values()), mode="claim"):
            if finding["severity"] == "high":
                blocking.append(f"{cid}: {finding['message']}")
        if derived["ceiling"] == "high" and claim.get("confidence") != "high":
            advisory.append(f"{cid}: the evidence would support high; the claim declares {claim.get('confidence')}")

        key = str(claim.get("key") or cid)
        claims[key] = (str(claim.get("confidence")), str(claim.get("probability")), str(claim.get("claim")))

    return blocking, advisory, claims


def load_for(slug: str, directory: Path) -> tuple[dict[str, Any] | None, Path]:
    path = directory / f"{slug}.json"
    if not path.is_file():
        return None, path
    return load(path), path
