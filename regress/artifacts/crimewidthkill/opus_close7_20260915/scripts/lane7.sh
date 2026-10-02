#!/bin/bash
# lane7.sh LANE name ...  -- runs the FROZEN shipped probe against /tmp/gxopuscrimec7_bins/<name>; never builds.
set -u
LANE="$1"; shift
BINS=/tmp/gxopuscrimec7_bins
WD=/tmp/gxopuscrimec7_work
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
P="$WD/probe.frozen.py"
LOG="$OUT/logs/lane_$LANE.out"
for name in "$@"; do
    log="$OUT/logs/probe_$name.raw"
    [ -f "$BINS/$name" ] || { echo "$name: NO BINARY" >>"$LOG"; continue; }
    echo "$(date +%T) START $name" >>"$LOG"
    python3 -u "$P" "$BINS/$name" "$name" > "$log" 2>&1
    res=$(grep -oE 'CRIMEP_RESULT=[0-9]+/[0-9]+' "$log" | tail -1)
    ctl=$(grep -oE 'CRIMEP_CONTROL=(OK|FAIL)' "$log" | tail -1)
    fail=$(grep -E '^FAILING:' "$log" | tail -1)
    echo "$(date +%T) $name: $res $ctl last=[$(tail -1 "$log")] $fail" >>"$LOG"
done
echo "LANE_${LANE}_DONE" >>"$LOG"
