#!/bin/bash
#  Capture the pinned counts gate_hygiene derives, so the F2 population edit can
#  be shown a MEASURED NO-OP rather than asserted one.
set -u
cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress || exit 1
LABEL="$1"
echo "=== $LABEL ==="
bash gate_hygiene.sh 2>&1 | grep -E '^  (ok|FAIL) +readiness|^  (ok|FAIL) +class ratchet|log-hygiene:' 
echo "POPCAP_DONE"
