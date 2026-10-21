#!/bin/bash
# run_companion.sh -- run the free-running companion against the fresh HEAD binary.
set -u
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/witness_20261020
BIN=/tmp/gxvme_head_20261020/gxemul
echo "companion md5: $(md5sum "$OUT/vme_freerun_companion.py" | cut -d' ' -f1)"
date '+COMPANION_START %F %T'
cd "$OUT" || exit 3
python3 -u "$OUT/vme_freerun_companion.py" "$BIN" HEAD_5dbc000e
echo "COMPANION_RC=$?"
date '+COMPANION_END %F %T'
