#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"

PACKAGE="${1:-}"
[[ -n "$PACKAGE" ]] || fail "Usage: $0 <android.package.name>"
require_authorized_adb

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$ROOT/artifacts/package-$PACKAGE-$STAMP"
mkdir -p "$OUT"
adb_cmd shell pm path "$PACKAGE" >"$OUT/path.txt" 2>"$OUT/path.txt.err" || true
adb_cmd shell dumpsys package "$PACKAGE" >"$OUT/dumpsys-package.txt" 2>"$OUT/dumpsys-package.txt.err" || true
adb_cmd shell cmd package resolve-activity --brief "$PACKAGE" >"$OUT/resolve-activity.txt" 2>"$OUT/resolve-activity.txt.err" || true
info "Package metadata written to $OUT"
