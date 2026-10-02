#!/bin/bash
#  laneP.sh LANE BIN...  -- #529 closing pass 7 (Opus finishing seat): run the FROZEN post7 prototype against each
#  named binary of /tmp/gxopuscrimec7_bins.  The prototype is frozen ONCE by mk (below) so every leg of the
#  comparison runs the same instrument.  No tree is mutated: these binaries were built by the previous seat and
#  the clone is left cmp-clean.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
W=/tmp/gxopuscrimec7_work
B=/tmp/gxopuscrimec7_bins
LANE="$1"; shift
OUT="$A/logs2"
mkdir -p "$OUT"
for m in "$@"; do
    echo "$(date +%H:%M:%S) START $m" >> "$OUT/laneP_$LANE.out"
    python3 -u "$W/post7.frozen.py" "$B/$m" "$m" > "$OUT/post7_$m.out" 2>&1
    res=$(grep -o 'POST7_RESULT=[0-9]*/[0-9]*' "$OUT/post7_$m.out" | tail -1)
    fail=$(grep '^FAILING: ' "$OUT/post7_$m.out" | tail -1)
    last=$(tail -1 "$OUT/post7_$m.out")
    echo "$(date +%H:%M:%S) $m: $res last=[$last] $fail" >> "$OUT/laneP_$LANE.out"
done
echo "LANEP_${LANE}_DONE" >> "$OUT/laneP_$LANE.out"
