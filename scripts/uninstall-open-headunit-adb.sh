#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

ACK=0
[[ "${1:-}" == "--acknowledge-parked" ]] && ACK=1
[[ "$ACK" == "1" ]] || fail "Usage: $0 --acknowledge-parked"
require_authorized_adb

adb_cmd uninstall com.andrerinas.headunitrevived
info "Open Headunit package removed"
