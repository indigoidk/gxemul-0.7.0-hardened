#!/bin/bash
# run_probe2_578.sh <binary> <label> -- one leg of the 22-row SELF-CONTAINED probe (WSL); witness_20261102/probe2_<label>.out.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w578; OUT=$W/witness_20261102/probe2_$2.out; PROBE=$W/jazz_vector_probe.py
{ echo "LEG $2 binary=$1 $(ls -la --time-style=+%F_%T "$1" | awk '{print $5, $6}') md5=$(md5sum "$1" | cut -c1-12)";
  echo "binary newer than dev_jazz.c: $( [ "$1" -nt "$(dirname "$1")/src/devices/dev_jazz.c" ] && echo yes || echo NO-STALE )";
  echo "sentinel: $(cat "$(dirname "$1")/.MUTANT" 2>/dev/null || echo none)"; echo "instrument: $PROBE md5=$(md5sum "$PROBE" | cut -c1-12)"; } > "$OUT"
cd /tmp && JAZZVEC_LOG=$W/witness_20261102/probe2_transcript_$2.log timeout 600 python3 -u "$PROBE" "$1" >> "$OUT" 2>&1
echo "PROBE2_LEG_DONE $2 $(grep -E '^JAZZVEC_RESULT=' "$OUT" || echo NONE)" | tee -a "$OUT"
