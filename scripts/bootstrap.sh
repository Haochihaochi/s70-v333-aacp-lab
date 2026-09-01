#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"

require_command git
require_command python3

info "Initializing pinned Open Headunit submodule"
git submodule update --init --recursive

info "Installing repository-local Git hooks"
git config core.hooksPath .githooks

info "Running foundation tests"
python3 -m unittest discover -s tests -v
python3 tools/repo_guard.py

info "Bootstrap complete"
