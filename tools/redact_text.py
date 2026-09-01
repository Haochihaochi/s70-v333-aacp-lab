#!/usr/bin/env python3
"""Conservative redaction for logs before sharing."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERNS = [
    (re.compile(r"(?i)(serial(?:no|number)?|imei|meid|vin|device[_ -]?id)\s*[:=]\s*[^\s,;]+"), r"\1=[REDACTED]"),
    (re.compile(r"(?i)(?:[0-9a-f]{2}:){5}[0-9a-f]{2}"), "[REDACTED-MAC]"),
    (re.compile(r"(?i)[A-HJ-NPR-Z0-9]{17}"), "[REDACTED-VIN-LIKE]"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[REDACTED-EMAIL]"),
]


def redact(text: str) -> str:
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(redact(args.input.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
