#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
ROOT="$(repo_root)"
cd "$ROOT"

OWNER="${OWNER:-haochihaochi}"
REPO="${REPO:-s70-v333-aacp-lab}"
VISIBILITY="${VISIBILITY:-private}"

require_command git
require_command gh

gh auth status >/dev/null 2>&1 || fail "GitHub CLI is not authenticated. Run: gh auth login"

case "$VISIBILITY" in
  private|public|internal) ;;
  *) fail "VISIBILITY must be private, public or internal" ;;
esac

python3 tools/repo_guard.py
python3 -m unittest discover -s tests -v

if git remote get-url origin >/dev/null 2>&1; then
  ORIGIN_URL="$(git remote get-url origin)"
  case "$ORIGIN_URL" in
    *.bundle|/*)
      info "Renaming local bundle origin to bundle-source"
      git remote rename origin bundle-source
      ;;
    *)
      fail "A non-local origin remote already exists: $ORIGIN_URL"
      ;;
  esac
fi

info "Creating $OWNER/$REPO as $VISIBILITY and pushing main plus tags"
gh repo create "$OWNER/$REPO" "--$VISIBILITY" --source=. --remote=origin --description "Safety-first Proton S70 v333 no-dongle Android Auto research foundation"
git push -u origin main --follow-tags
gh repo edit "$OWNER/$REPO" --add-topic proton-s70 --add-topic android-auto --add-topic atlas-os --add-topic android-9 --add-topic headunit --add-topic reverse-engineering
info "Published: https://github.com/$OWNER/$REPO"
