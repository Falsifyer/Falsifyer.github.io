#!/usr/bin/env python3
"""Render the falsification register from the claim registries.

Every claim a reader would act on carries at least one review trigger. This page is the
list of those conditions: what would change the judgement, the artefact that would satisfy
it, and — for technical and behavioural triggers — when the window closes.

The page is generated so it cannot drift from the registries, and the counts in the lede
are computed for the same reason: a number typed into prose is a number that goes stale.

Block: ``<!-- falsification:begin -->`` … ``<!-- falsification:end -->``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

BEGIN = "<!-- falsification:begin -->"
END = "<!-- falsification:end -->"
TITLE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)


def _title(post: Path) -> str:
    match = TITLE.search(post.read_text(encoding="utf-8"))
    if not match:
        return post.stem
    return match.group(1).strip().strip('"')


def collect(root: Path) -> list[dict]:
    rows: list[dict] = []
    posts = {post.stem: post for post in (root / "_posts").glob("*.md")}
    for registry in sorted((root / "_data" / "claims").glob("*.json")):
        document = json.loads(registry.read_text(encoding="utf-8"))
        slug = registry.stem
        url = f"/{re.sub(r'^\d{4}-\d{2}-\d{2}-', '', slug)}/"
        product = _title(posts[slug]).split(":")[0] if slug in posts else slug
        items = list(document.get("claims") or []) + list(document.get("judgements") or [])
        for item in items:
            for trigger in item.get("triggers") or []:
                rows.append(
                    {
                        "product": product,
                        "url": url,
                        "claim": str(item.get("claim") or item.get("hypothesis") or ""),
                        "condition": str(trigger.get("condition") or ""),
                        "artifact": str(trigger.get("artifact") or ""),
                        "type": str(trigger.get("type") or ""),
                        "expires": trigger.get("expires"),
                    }
                )
    rows.sort(key=lambda row: (row["expires"] is None, row["expires"] or "", row["product"], row["claim"]))
    return rows


def _cell(text: str) -> str:
    return text.replace("|", "\\|").strip()


def block(rows: list[dict], today: date) -> str:
    total = len(rows)
    dated = [row for row in rows if row["expires"]]
    expired = [row for row in dated if date.fromisoformat(row["expires"]) < today]
    nearest = min((row["expires"] for row in dated), default=None)

    products = len({row["product"] for row in rows})
    lede = f"**{total} conditions** across {products} products. {len(dated)} carry an expiry"
    if nearest:
        lede += f"; the nearest is **{nearest}**"
    lede += ". None has expired." if not expired else f". **{len(expired)} have expired.**"

    lines = [
        lede,
        "",
        "| Product | Claim | What would change it | Artefact | Type | Expires |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| [{_cell(row['product'])}]({row['url']}) | {_cell(row['claim'])} "
            f"| {_cell(row['condition'])} | {_cell(row['artifact'])} "
            f"| {_cell(row['type'])} | {row['expires'] or '—'} |"
        )
    return "\n".join(lines)


def render(text: str, content: str) -> str:
    if BEGIN not in text or END not in text:
        return text
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    # kramdown stops parsing GFM tables after a standalone HTML comment, so the
    # opening marker rides at the end of the previous paragraph instead.
    return f"{head.rstrip()} {BEGIN}\n\n{content}\n\n{END}{tail}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--page", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    page = args.page or root / "_posts" / "2026-10-28-falsification-register.md"
    if not page.is_file():
        print(f"falsification: cannot check: no page at {page}", file=sys.stderr)
        return 2

    rows = collect(root)
    if not rows:
        print("falsification: cannot check: no triggers in the registries", file=sys.stderr)
        return 2

    before = page.read_text(encoding="utf-8")
    after = render(before, block(rows, date.today()))
    if after == before:
        print(f"falsification: {len(rows)} condition(s), page up to date")
        return 0

    if args.check:
        print("falsification: page is out of date with the registries", file=sys.stderr)
        return 1

    page.write_text(after, encoding="utf-8")
    print(f"falsification: {len(rows)} condition(s) written to {page.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
