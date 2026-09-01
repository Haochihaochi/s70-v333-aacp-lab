#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"
require_authorized_adb

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${PROFILE_OUT:-$ROOT/artifacts/device-profile-$STAMP}"
mkdir -p "$OUT"

capture() {
  local name="$1"
  shift
  if ! adb_cmd "$@" >"$OUT/$name" 2>"$OUT/$name.err"; then
    printf 'Command failed or was denied; see %s.err\n' "$name" >>"$OUT/collection-warnings.txt"
  fi
  tr -d '\r' <"$OUT/$name" >"$OUT/$name.tmp" || true
  mv "$OUT/$name.tmp" "$OUT/$name"
}

info "Collecting allow-listed Android properties"
PROPS=(
  ro.build.display.id
  ro.build.fingerprint
  ro.build.version.release
  ro.build.version.sdk
  ro.build.version.security_patch
  ro.build.type
  ro.build.tags
  ro.product.manufacturer
  ro.product.brand
  ro.product.model
  ro.product.device
  ro.product.board
  ro.product.cpu.abi
  ro.product.cpu.abilist
  ro.hardware
  ro.board.platform
  ro.boot.hardware
  ro.boot.verifiedbootstate
  ro.boot.vbmeta.device_state
  ro.boot.flash.locked
  ro.secure
  ro.debuggable
  service.adb.root
)
: >"$OUT/properties.txt"
for prop in "${PROPS[@]}"; do
  value="$(adb_cmd shell getprop "$prop" 2>/dev/null | tr -d '\r' || true)"
  printf '%s=%s\n' "$prop" "$value" >>"$OUT/properties.txt"
done

info "Collecting display, feature, USB, audio and package metadata"
{
  adb_cmd shell wm size || true
  adb_cmd shell wm density || true
} >"$OUT/wm.txt" 2>"$OUT/wm.txt.err"

capture features.txt shell pm list features
capture packages.txt shell pm list packages -f
capture usb.txt shell dumpsys usb
capture display.txt shell dumpsys display
capture window-displays.txt shell dumpsys window displays
capture audio.txt shell dumpsys audio
capture audio-flinger.txt shell dumpsys media.audio_flinger
capture media-session.txt shell dumpsys media_session
capture input.txt shell dumpsys input
capture input-devices.txt shell cat /proc/bus/input/devices
capture power.txt shell dumpsys power
capture connectivity.txt shell dumpsys connectivity
capture wifi.txt shell dumpsys wifi
capture partitions.txt shell cat /proc/partitions
capture mounts.txt shell mount
capture storage.txt shell df -h
capture selinux.txt shell getenforce
capture id.txt shell id

# CPU info can contain a hardware serial on some systems. Redact that line.
if adb_cmd shell cat /proc/cpuinfo 2>"$OUT/cpuinfo.txt.err" | tr -d '\r' | sed -E 's/^[Ss]erial[[:space:]]*:.*/Serial: [REDACTED]/' >"$OUT/cpuinfo.txt"; then
  :
else
  printf 'Unable to collect CPU information\n' >>"$OUT/collection-warnings.txt"
fi

KNOWN_PACKAGES=(
  com.android.settings
  com.android.packageinstaller
  com.google.android.packageinstaller
  com.google.android.projection.gearhead
  com.andrerinas.headunitrevived
)
: >"$OUT/packages-known.txt"
for package_name in "${KNOWN_PACKAGES[@]}"; do
  if adb_cmd shell pm path "$package_name" >/dev/null 2>&1; then
    printf '%s=true\n' "$package_name" >>"$OUT/packages-known.txt"
  else
    printf '%s=false\n' "$package_name" >>"$OUT/packages-known.txt"
  fi
done

cat >"$OUT/README.txt" <<EOF
This profile was collected using read-only ADB commands.
No firmware, application APK, private key, certificate, VIN, serial number or MAC address should be added to this directory.
Run: python3 tools/profile_report.py "$OUT" --strict-v333
EOF

python3 "$ROOT/tools/profile_report.py" "$OUT" || true
info "Profile written to $OUT"
