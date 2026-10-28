#!/usr/bin/env python3
"""Gate the site as a product: handling, freshness, versioning and cross-product claims.

The site's argument is that a judgement carries its grade and can be diffed. That only
holds if the products are compared *to each other* — the failure this gate exists for was
a contradiction between two products written two days apart, each internally consistent.

Rules, in the order they are checked:

1. header and handling — delegated to ``check_handling.py``, which delegates to
   ``sharegate`` for the TLP rules.
2. versioning — the version in the header must appear in the revision history.
3. freshness — every product carries a ``Next review`` date, and a product past it fails.
4. grading vocabulary — confidence and probability come from the site's lexicons.
5. cross-product consistency — the same claim, stated in two products, must carry the
   same confidence and probability. Wording is normalised, so the check fires on a
   contradiction without declaring it in advance.

Exit codes follow the suite contract: 0 clean, 1 a finding, 2 it could not check.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

CONFIDENCE = {"High", "Moderate", "Low"}
PROBABILITY = {
    "n/a",
    "nearly certain",
    "very likely",
    "likely",
    "roughly even chance",
    "unlikely",
    "very unlikely",
}

VERSION_ROW = re.compile(r"^\|\s*\*\*Version\*\*\s*\|\s*([0-9][^|\s]*)", re.MULTILINE)
REVIEW_ROW = re.compile(r"^\|\s*\*\*Next review\*\*\s*\|\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", re.MULTILINE)
LEDGER_HEADING = re.compile(r"^##.*ledger", re.IGNORECASE | re.MULTILINE)
TABLE_ROW = re.compile(r"^\|(.+)\|\s*$")
SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


def normalise(claim: str) -> str:
    """A claim's identity for comparison: no markdown, no citations, no case."""
    text = re.sub(r"\[[0-9]+\]", "", claim)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "")
    text = re.sub(r"[^0-9a-zA-Z]+", " ", text.lower())
    return " ".join(text.split())


def ledger_rows(text: str) -> list[tuple[str, str, str]]:
    """Return (claim, confidence, probability) from the product's assessment ledger."""
    heading = LEDGER_HEADING.search(text)
    if heading is None:
        return []
    rows: list[tuple[str, str, str]] = []
    in_table = False
    for line in text[heading.end() :].splitlines():
        stripped = line.strip()
        if not stripped:
            if in_table:
                break
            continue
        if not stripped.startswith("|"):
            if in_table:
                break
            continue
        in_table = True
        if SEPARATOR.match(stripped):
            continue
        cells = [cell.strip() for cell in TABLE_ROW.match(stripped).group(1).split("|")]
        if len(cells) < 3:
            continue
        if cells[0].lower() in {"assessment", "claim"}:
            continue
        rows.append((cells[0], cells[1], cells[2]))
    return rows


def check_product(path: Path, today: date) -> tuple[list[str], dict[str, tuple[str, str, str]]]:
    text = path.read_text(encoding="utf-8")
    blocking: list[str] = []
    claims: dict[str, tuple[str, str, str]] = {}

    version = VERSION_ROW.search(text)
    if version is None:
        blocking.append("no **Version** row")
    elif not re.search(rf"^\|\s*{re.escape(version.group(1))}\s*\|", text, re.MULTILINE):
        blocking.append(f"version {version.group(1)} has no revision-history row")
    elif "Revision history" not in text:
        blocking.append("no Revision history section")

    review = REVIEW_ROW.search(text)
    if review is None:
        blocking.append("no **Next review** row")
    else:
        due = date.fromisoformat(review.group(1))
        if due < today:
            blocking.append(f"review date {due.isoformat()} has passed: re-review or re-date it")

    for claim, confidence, probability in ledger_rows(text):
        if confidence not in CONFIDENCE:
            blocking.append(f"unknown confidence '{confidence}' in: {claim[:60]}")
        if probability not in PROBABILITY:
            blocking.append(f"unknown probability '{probability}' in: {claim[:60]}")
        claims[normalise(claim)] = (confidence, probability, claim)

    return blocking, claims


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--posts", type=Path, default=None)
    parser.add_argument("--suite", type=Path, default=None, help="path to a cti-suite checkout")
    parser.add_argument("--today", type=str, default=None, help="override the date (tests)")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parent.parent
    posts = args.posts or root / "_posts"
    products = sorted(posts.glob("*.md"))
    if not products:
        print(f"sitegate: cannot check: no products in {posts}", file=sys.stderr)
        return 2

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from check_handling import check_product as check_handling
        from check_handling import add_suite_to_path
    except ImportError as exc:
        print(f"sitegate: cannot check: {exc}", file=sys.stderr)
        return 2

    suite = args.suite or root / "_suite"
    add_suite_to_path(suite)
    try:
        from sharegate.core import check_tlp  # noqa: F401
    except ImportError as exc:
        print(f"sitegate: cannot check: sharegate not importable from {suite} ({exc})", file=sys.stderr)
        print(
            "  clone it first: git clone --depth 1 https://github.com/ME0094/cti-suite _suite",
            file=sys.stderr,
        )
        return 2
    print(f"sitegate: gate = {suite}")

    today = date.fromisoformat(args.today) if args.today else date.today()
    failed = 0
    seen: dict[str, tuple[str, str, str, str]] = {}

    for product in products:
        blocking, claims = check_product(product, today)
        handling, advisory = check_handling(product, check_tlp)
        blocking += handling

        for key, (confidence, probability, claim) in claims.items():
            if key in seen:
                other_conf, other_prob, other_claim, other_product = seen[key]
                if (confidence, probability) != (other_conf, other_prob):
                    blocking.append(
                        f"contradicts {other_product.name}: '{claim[:70]}' is "
                        f"{confidence}/{probability} here and "
                        f"{other_conf}/{other_prob} there"
                    )
            else:
                seen[key] = (confidence, probability, claim, product)

        print(f"{'FAIL' if blocking else 'ok  '}  {product.name}")
        for message in blocking:
            print(f"        - {message}")
        for message in advisory:
            print(f"        ~ {message} (advisory)")
        failed += bool(blocking)

    print(f"\nsitegate: {len(products) - failed}/{len(products)} products pass (gate: {suite})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
