#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"
require_authorized_adb

PACKAGE=com.andrerinas.headunitrevived
if ! adb_cmd shell pm path "$PACKAGE" >/dev/null 2>&1; then
  fail "$PACKAGE is not installed"
fi

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$ROOT/artifacts/smoke-test-$STAMP"
mkdir -p "$OUT"

adb_cmd logcat -c || true
adb_cmd shell monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1 >"$OUT/launch.txt" 2>&1 || true
sleep 5
adb_cmd shell dumpsys package "$PACKAGE" >"$OUT/package.txt" 2>"$OUT/package.txt.err" || true
adb_cmd shell dumpsys activity activities >"$OUT/activities.txt" 2>"$OUT/activities.txt.err" || true
adb_cmd logcat -d >"$OUT/logcat-raw.txt" 2>"$OUT/logcat-raw.txt.err" || true
python3 "$ROOT/tools/redact_text.py" "$OUT/logcat-raw.txt" "$OUT/logcat-redacted.txt"
rm -f "$OUT/logcat-raw.txt"

info "Smoke-test evidence written to $OUT"
