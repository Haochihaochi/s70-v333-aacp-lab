#!/usr/bin/env python3
"""Fail if sensitive or proprietary binary artifacts are staged/tracked."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

FORBIDDEN_SUFFIXES = {
    ".apk", ".aab", ".img", ".bin", ".rom", ".dump", ".dmp", ".zip", ".7z", ".rar",
    ".tar", ".gz", ".tgz", ".jks", ".keystore", ".p12", ".pfx", ".pem", ".key",
    ".der", ".crt", ".cer",
}
FORBIDDEN_PREFIXES = ("artifacts/", "dist/")


def tracked_files() -> list[str]:
    proc = subprocess.run(["git", "ls-files", "-z"], check=True, stdout=subprocess.PIPE)
    return [p.decode("utf-8", errors="surrogateescape") for p in proc.stdout.split(b"\0") if p]


def main() -> int:
    violations: list[str] = []
    for name in tracked_files():
        path = Path(name)
        lower = name.lower()
        if lower.startswith(FORBIDDEN_PREFIXES):
            violations.append(f"generated/sensitive path is tracked: {name}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            violations.append(f"forbidden binary/key extension is tracked: {name}")
    if violations:
        print("Repository guard failed:", file=sys.stderr)
        for violation in violations:
            print(f"- {violation}", file=sys.stderr)
        return 1
    print("Repository guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
