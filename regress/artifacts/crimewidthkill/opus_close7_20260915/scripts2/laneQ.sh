#!/bin/bash
#  laneQ.sh LANE BIN...  -- run the FROZEN post7b prototype (the TIME-row repair) against each named binary.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
W=/tmp/gxopuscrimec7_work
B=/tmp/gxopuscrimec7_bins
LANE="$1"; shift
OUT="$A/logs2"
mkdir -p "$OUT"
if [ "$LANE" = "Q" ]; then
    cp "$A/scripts2/post7b.py" "$W/post7b.frozen.py"
    md5sum "$W/post7b.frozen.py" "$A/scripts2/post7b.py" >> "$OUT/freeze.out"
fi
for m in "$@"; do
    echo "$(date +%H:%M:%S) START $m" >> "$OUT/laneQ_$LANE.out"
    python3 -u "$W/post7b.frozen.py" "$B/$m" "$m" > "$OUT/post7b_$m.out" 2>&1
    res=$(grep -o 'POST7B_RESULT=[0-9]*/[0-9]*' "$OUT/post7b_$m.out" | tail -1)
    fail=$(grep '^FAILING: ' "$OUT/post7b_$m.out" | tail -1)
    last=$(tail -1 "$OUT/post7b_$m.out")
    echo "$(date +%H:%M:%S) $m: $res last=[$last] $fail" >> "$OUT/laneQ_$LANE.out"
done
echo "LANEQ_${LANE}_DONE" >> "$OUT/laneQ_$LANE.out"
