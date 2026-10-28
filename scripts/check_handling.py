#!/usr/bin/env python3
"""Gate this site's products with the same handling check the site describes.

The site argues that a marking should be checked rather than asserted, and its own
`sharegate` already implements the FIRST TLP 2.0 rules. This script applies that gate to
`_posts/`, so the claim on the Engineering page is true of the products themselves.

It is deliberately stricter than `sharegate check` in one respect: `sharegate` refuses a
bundle only on a high finding, while this repository also refuses a *missing* or
*retired* marking. A retired `TLP:WHITE` is a low finding to the gate and a publishing
error here.

Exit codes follow the suite contract: 0 clean, 1 a finding, 2 it could not check.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADER_FIELDS = ("Product", "Handling", "Version", "Review trigger")
HANDLING_ROW = re.compile(r"^[ \t]*\|\s*\*\*Handling\*\*\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)

#: Findings that stop a product from travelling. `tlp-sensitive-permissive` is a medium
#: heuristic and is reported as advisory: open-source CTI at TLP:CLEAR says "victim" and
#: "compromised" in its narrative, and the marking is still right.
BLOCKING = {"tlp-missing", "tlp-conflict", "tlp-deprecated"}


def add_suite_to_path(suite: Path) -> None:
    """Make the suite importable from a source checkout, without installing it."""
    for package in ("cti-method", "sharegate"):
        source = suite / "packages" / package / "src"
        if source.is_dir():
            sys.path.insert(0, str(source))


def check_product(path: Path, check_tlp) -> tuple[list[str], list[str]]:
    """Return (blocking, advisory) messages for one product."""
    text = path.read_text(encoding="utf-8")
    blocking: list[str] = []
    advisory: list[str] = []

    for field in HEADER_FIELDS:
        if not re.search(rf"^[ \t]*\|\s*\*\*{field}\*\*\s*\|", text, re.MULTILINE):
            blocking.append(f"header: no **{field}** row")

    row = HANDLING_ROW.search(text)
    if row is None:
        blocking.append("header: no handling marking in the **Handling** row")
    else:
        result = check_tlp(text)
        for finding in result["findings"]:
            message = f"{finding['code']}: {finding['message']}"
            if finding["code"] in BLOCKING or finding["severity"] == "high":
                blocking.append(message)
            else:
                advisory.append(message)
        if not result["markings"]:
            blocking.append("header: the handling row carries no TLP marking")

    return blocking, advisory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--suite",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "_suite",
        help="path to a cti-suite checkout (default: ./_suite)",
    )
    parser.add_argument("--posts", type=Path, default=None, help="directory of products")
    args = parser.parse_args(argv)

    add_suite_to_path(args.suite)
    try:
        from sharegate.core import check_tlp
    except ImportError as exc:  # not checked is not clean
        print(f"handling: cannot check: sharegate not importable ({exc})", file=sys.stderr)
        return 2

    posts = args.posts or Path(__file__).resolve().parent.parent / "_posts"
    products = sorted(posts.glob("*.md"))
    if not products:
        print(f"handling: cannot check: no products in {posts}", file=sys.stderr)
        return 2

    failed = 0
    for product in products:
        blocking, advisory = check_product(product, check_tlp)
        status = "FAIL" if blocking else "ok"
        print(f"{status:4}  {product.name}")
        for message in blocking:
            print(f"        - {message}")
        for message in advisory:
            print(f"        ~ {message} (advisory)")
        failed += bool(blocking)

    print(f"\nhandling: {len(products) - failed}/{len(products)} products pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
