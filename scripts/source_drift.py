#!/usr/bin/env python3
"""Detect that the ATT&CK collection moved since the standard was pinned.

A review trigger fires when the world changes, but nothing in a static repository notices
that the world changed. This checks the one source every product depends on: the ATT&CK
enterprise collection.

It does **not** break a build. A build is deterministic over the repository; a source that
moved is a fact about the world, and the response is to open an issue and let a person
re-review, not to fail a commit.

Exit codes follow the suite contract: 0 checked (drift or not), 2 could not check.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

INDEX = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/index.json"
COLLECTION = "Enterprise ATT&CK"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    pinned = json.loads((root / "_data" / "sources.json").read_text(encoding="utf-8"))["attack"]

    try:
        with urllib.request.urlopen(INDEX, timeout=30) as response:
            index = json.load(response)
        collection = next(item for item in index["collections"] if item["name"] == COLLECTION)
        latest = collection["versions"][0]
    except Exception as exc:  # not checked is not clean
        print(f"drift: cannot check: {exc}", file=sys.stderr)
        return 2

    print(f"drift: pinned {pinned['version']} ({pinned['modified']})")
    print(f"drift: remote {latest['version']} ({latest['modified']})")

    moved = (
        latest["version"] != pinned["version"]
        or latest["modified"] != pinned["modified"]
    )
    if not moved:
        print("drift: no change")
        return 0

    detail = (
        f"{COLLECTION} moved from {pinned['version']} ({pinned['modified']}) "
        f"to {latest['version']} ({latest['modified']})"
    )
    print(detail)
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write("drift=true\n")
            handle.write(f"detail={detail}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
