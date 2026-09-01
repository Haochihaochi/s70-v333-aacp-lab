#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"

APK=""
ACK=0
FORCE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apk) APK="${2:-}"; shift 2 ;;
    --acknowledge-parked) ACK=1; shift ;;
    --force-unverified) FORCE=1; shift ;;
    -h|--help)
      cat <<'EOF'
Usage: install-open-headunit-adb.sh --apk FILE --acknowledge-parked [--force-unverified]

Uses ordinary adb install on an already-authorized IHU. It does not enable ADB,
root the device, bypass signature checks or flash partitions.
EOF
      exit 0 ;;
    *) fail "Unknown argument: $1" ;;
  esac
done

[[ -n "$APK" && -f "$APK" ]] || fail "Provide an existing APK with --apk"
[[ "$ACK" == "1" ]] || fail "Use --acknowledge-parked after placing the vehicle safely in Park and stopping all driving activity"
require_authorized_adb

DISPLAY_ID="$(adb_cmd shell getprop ro.build.display.id 2>/dev/null | tr -d '\r' || true)"
FINGERPRINT="$(adb_cmd shell getprop ro.build.fingerprint 2>/dev/null | tr -d '\r' || true)"
TARGET_TEXT="$DISPLAY_ID $FINGERPRINT"
if [[ "$TARGET_TEXT" != *"00333"* && "$TARGET_TEXT" != *"v333"* && "$FORCE" != "1" ]]; then
  fail "v333 evidence was not found in the exposed build properties. Refusing installation. Re-run with --force-unverified only after manually confirming About IHU."
fi

info "Installing APK through the existing authorized ADB connection"
adb_cmd install -r "$APK"

info "Launching Open Headunit"
adb_cmd shell monkey -p com.andrerinas.headunitrevived -c android.intent.category.LAUNCHER 1 >/dev/null

info "Install command completed. Validate display, audio, microphone and USB only while parked."
