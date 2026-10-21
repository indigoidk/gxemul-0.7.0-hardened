#!/bin/bash
# run_probe.sh -- run the UNMODIFIED 2026-10-09 probe against the fresh HEAD binary.
set -u
OUT=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/witness_20261020
BIN=/tmp/gxvme_head_20261020/gxemul
echo "probe md5: $(md5sum "$OUT/vme_sites_probe.py" | cut -d' ' -f1)"
echo "binary: $BIN md5: $(md5sum "$BIN" | cut -d' ' -f1)"
date '+PROBE_START %F %T'
cd "$OUT" || exit 3
python3 -u "$OUT/vme_sites_probe.py" "$BIN" HEAD_5dbc000e
echo "PROBE_RC=$?"
date '+PROBE_END %F %T'
