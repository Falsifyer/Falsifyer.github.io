#!/usr/bin/env python3
"""Render a product's assessment table from its claim registry.

The registry is the source; the table is a view. Rendering it here — rather than in a
Jekyll plugin, which GitHub Pages does not run — keeps the site static and still makes the
two unable to drift: `--check` fails when the file on disk differs from what the registry
would produce.

The opening marker must not be left as a standalone HTML block: kramdown stops
parsing a GFM table after one, and the table is published as text. Keep it at the end of
the preceding text block, with a blank line before the table; the CI job checks the built
page for a literal pipe header.

The block to replace is delimited by ``<!-- claims:begin -->`` and ``<!-- claims:end -->``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BEGIN = "<!-- claims:begin -->"
END = "<!-- claims:end -->"

CONFIDENCE = {"high": "High", "moderate": "Moderate", "low": "Low"}
PROBABILITY = {
    "nearly_certain": "nearly certain",
    "very_likely": "very likely",
    "likely": "likely",
    "roughly_even": "roughly even chance",
    "unlikely": "unlikely",
    "very_unlikely": "very unlikely",
    None: "n/a",
}


def _refs(document: dict, ids: list[str]) -> str:
    refs = {source["id"]: source.get("ref", source["id"]) for source in document.get("sources", [])}
    return "".join(f"[{refs.get(item, item)}]" for item in ids)


def table(document: dict) -> str:
    lines = ["| Assessment | Confidence | Probability | Basis |", "|---|---|---|---|"]
    if document.get("hypotheses"):
        for judge in document.get("judgements") or []:
            basis = _refs(document, [str(item) for item in judge.get("sources") or []])
            note = f" · {judge['note']}" if judge.get("note") else ""
            lines.append(
                f"| {judge['claim']} | {CONFIDENCE.get(judge['confidence'], judge['confidence'])} "
                f"| {PROBABILITY.get(judge.get('probability'), judge.get('probability'))} | {basis}{note} |"
            )
    else:
        for claim in document.get("claims") or []:
            basis = _refs(document, [str(item.get("id")) for item in claim.get("sources") or []])
            note = f" · {claim['note']}" if claim.get("note") else ""
            lines.append(
                f"| {claim['claim']} | {CONFIDENCE.get(claim['confidence'], claim['confidence'])} "
                f"| {PROBABILITY.get(claim.get('probability'), claim.get('probability'))} | {basis}{note} |"
            )
    return "\n".join(lines)


def render(text: str, document: dict) -> str:
    if BEGIN not in text or END not in text:
        return text
    # kramdown opens an HTML block on a standalone comment and then refuses to parse
    # the GFM table that follows, so the opening marker must sit at the end of the
    # preceding paragraph, with a blank line before the table.
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n\n{table(document)}\n\n{END}{tail}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--posts", type=Path, default=None)
    parser.add_argument("--claims", type=Path, default=None)
    parser.add_argument("--check", action="store_true", help="fail if a file is out of date")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    posts = args.posts or root / "_posts"
    claims_dir = args.claims or root / "_data" / "claims"

    changed: list[str] = []
    rendered = 0
    for post in sorted(posts.glob("*.md")):
        registry = claims_dir / f"{post.stem}.json"
        if not registry.is_file():
            continue
        document = json.loads(registry.read_text(encoding="utf-8"))
        before = post.read_text(encoding="utf-8")
        after = render(before, document)
        if after == before:
            continue
        rendered += 1
        changed.append(post.name)
        if not args.check:
            post.write_text(after, encoding="utf-8")

    if args.check:
        for name in changed:
            print(f"out of date: {name}", file=sys.stderr)
        print(f"render: {len(changed)} file(s) differ from their registry")
        return 1 if changed else 0

    print(f"render: {rendered} table(s) regenerated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
