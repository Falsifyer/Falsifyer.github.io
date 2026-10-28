#!/usr/bin/env python3
"""Self-test the claim registry: each fixture must fail for the right reason.

A gate nobody has watched reject anything is a decoration. These fixtures are the
smallest cases that prove the ceiling is computed by the suite and not asserted in prose:

* a grade above the ceiling (two sources declared high, one direct source);
* a derived source counted twice;
* a derivation cycle.

Run: ``python3 scripts/selftest.py --suite _suite``
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

POST = """| | |
|---|---|
| **Product** | Fixture |
| **Handling** | TLP:CLEAR |
| **Version** | 1.0 (2026-01-01) |
| **Review trigger** | none |
| **Next review** | 2099-01-01 |

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-01-01 | First release. |
"""


def registry(sources: list[dict], confidence: str = "high") -> dict:
    return {
        "schema_version": "1.0",
        "product": "2026-01-01-demo",
        "sources": sources,
        "claims": [
            {
                "id": "C1",
                "key": "demo.one",
                "claim": "A documented fact",
                "class": "documented",
                "type": "factual",
                "confidence": confidence,
                "probability": None,
                "sources": [{"id": source["id"], "direct": True} for source in sources],
            }
        ],
    }


SCENARIOS = [
    (
        "grade above the ceiling",
        registry([{"id": "S1", "publisher": "CISA"}]),
        "exceeds what the evidence supports",
    ),
    (
        "derived source is not a second voice",
        registry(
            [
                {"id": "S1", "publisher": "CISA"},
                {"id": "S2", "publisher": "DOJ", "derived_from": ["S1"]},
            ]
        ),
        "exceeds what the evidence supports",
    ),
    (
        "derivation cycle",
        registry(
            [
                {"id": "S1", "publisher": "CISA", "derived_from": ["S2"]},
                {"id": "S2", "publisher": "DOJ", "derived_from": ["S1"]},
            ],
            confidence="low",
        ),
        "derivation cycle",
    ),
]


def run(suite: Path, scenario: tuple[str, dict, str]) -> bool:
    name, document, expected = scenario
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "posts").mkdir()
        (root / "claims").mkdir()
        (root / "posts" / "2026-01-01-demo.md").write_text(POST, encoding="utf-8")
        (root / "claims" / "2026-01-01-demo.json").write_text(json.dumps(document), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("sitegate.py")),
                "--suite",
                str(suite),
                "--posts",
                str(root / "posts"),
                "--claims",
                str(root / "claims"),
            ],
            capture_output=True,
            text=True,
        )
    if result.returncode == 0:
        print(f"FAIL  {name}: the gate accepted it")
        print(result.stdout)
        return False
    if expected not in result.stdout:
        print(f"FAIL  {name}: wrong reason")
        print(result.stdout)
        return False
    print(f"ok    {name}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parent.parent / "_suite")
    args = parser.parse_args()
    results = [run(args.suite, scenario) for scenario in SCENARIOS]
    print(f"\nselftest: {sum(results)}/{len(results)} scenarios refused for the right reason")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
