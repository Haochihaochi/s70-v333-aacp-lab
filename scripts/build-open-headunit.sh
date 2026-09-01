#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"

require_command git
require_command java

# shellcheck disable=SC1091
source "$ROOT/config/upstream.env"

if [[ ! -f third_party/open-headunit/gradlew ]]; then
  info "Open Headunit submodule is missing; initializing it"
  git submodule update --init --recursive
fi

ACTUAL_COMMIT="$(git -C third_party/open-headunit rev-parse HEAD)"
if [[ "$ACTUAL_COMMIT" != "$OPEN_HEADUNIT_COMMIT" && "${ALLOW_UPSTREAM_DRIFT:-0}" != "1" ]]; then
  fail "Open Headunit is at $ACTUAL_COMMIT, expected $OPEN_HEADUNIT_COMMIT. Set ALLOW_UPSTREAM_DRIFT=1 only after auditing the change."
fi

info "Building Open Headunit at $ACTUAL_COMMIT"
(
  cd third_party/open-headunit
  chmod +x gradlew
  ./gradlew --no-daemon "$OPEN_HEADUNIT_GRADLE_TASK"
)

APK="$(find third_party/open-headunit/app/build/outputs/apk -type f \
  \( -name '*github*debug*.apk' -o -name '*debug.apk' \) 2>/dev/null | sort | tail -n 1)"
[[ -n "$APK" && -f "$APK" ]] || fail "Build completed but no debug APK was found"

mkdir -p dist
OUT="dist/open-headunit-s70-v333-foundation-debug.apk"
cp "$APK" "$OUT"
sha256_file "$OUT" > "$OUT.sha256"

info "APK: $OUT"
info "Checksum: $OUT.sha256"
