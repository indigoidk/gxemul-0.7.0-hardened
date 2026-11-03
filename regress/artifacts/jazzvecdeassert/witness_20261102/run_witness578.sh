#!/bin/bash
# run_witness578.sh <binary> <label> -- one witness leg for OB-22 (WSL); writes witness_<label>.out beside this script's dir.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w578; OUT=$W/witness_20261102/witness_$2.out
{ echo "LEG $2 binary=$1 $(ls -la --time-style=+%F_%T "$1" | awk '{print $5, $6}') md5=$(md5sum "$1" | cut -c1-12)";
  echo "binary newer than dev_jazz.c: $( [ "$1" -nt "$(dirname "$1")/src/devices/dev_jazz.c" ] && echo yes || echo NO-STALE )";
  echo "sentinel: $(cat "$(dirname "$1")/.MUTANT" 2>/dev/null || echo none)"; } > "$OUT"
cd /tmp && JAZZVEC_LOG=$W/witness_20261102/transcript_$2.log timeout 600 python3 -u "$W/jazz_vector_witness.py" "$1" >> "$OUT" 2>&1
echo "WITNESS_LEG_DONE $2 $(grep -E '^JAZZVEC_RESULT=' "$OUT")" | tee -a "$OUT"
