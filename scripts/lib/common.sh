#!/usr/bin/env bash
set -euo pipefail

repo_root() {
  cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

info() {
  printf '==> %s\n' "$*"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1"
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1"
  else
    fail "Neither sha256sum nor shasum is available"
  fi
}

setup_adb() {
  ADB="${ADB:-adb}"
  require_command "$ADB"
  ADB_ARGS=()
  if [[ -n "${ADB_SERIAL:-}" ]]; then
    ADB_ARGS=(-s "$ADB_SERIAL")
  fi
}

adb_cmd() {
  "$ADB" "${ADB_ARGS[@]}" "$@"
}

require_authorized_adb() {
  setup_adb
  local state
  state="$(adb_cmd get-state 2>/dev/null || true)"
  [[ "$state" == "device" ]] || fail "No authorized ADB device. Current state: ${state:-none}"
}
