#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"
require_command git

OUT="${1:-$ROOT/../s70-v333-aacp-lab.bundle}"
git status --porcelain | grep -q . && fail "Working tree is not clean; commit or discard changes before creating a bundle"
git bundle create "$OUT" --all
info "Git bundle created: $OUT"
