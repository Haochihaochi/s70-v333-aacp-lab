#!/usr/bin/env python3
"""Compare two profile summaries without requiring proprietary firmware images."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from profile_report import analyze_profile


def load_profile(path: Path) -> dict[str, Any]:
    if path.is_dir():
        summary = path / "summary.json"
        if summary.exists():
            return json.loads(summary.read_text(encoding="utf-8"))
        return analyze_profile(path)
    return json.loads(path.read_text(encoding="utf-8"))


def mapping_diff(left: dict[str, Any], right: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(set(left) | set(right)):
        if left.get(key) != right.get(key):
            rows.append({"key": key, "left": left.get(key), "right": right.get(key)})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--json", dest="json_out", type=Path)
    args = parser.parse_args()

    left = load_profile(args.left)
    right = load_profile(args.right)
    result = {
        "properties": mapping_diff(left.get("properties", {}), right.get("properties", {})),
        "packages": mapping_diff(left.get("packages", {}), right.get("packages", {})),
        "features_added": sorted(set(right.get("features", [])) - set(left.get("features", []))),
        "features_removed": sorted(set(left.get("features", [])) - set(right.get("features", []))),
    }

    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.json_out:
        args.json_out.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
