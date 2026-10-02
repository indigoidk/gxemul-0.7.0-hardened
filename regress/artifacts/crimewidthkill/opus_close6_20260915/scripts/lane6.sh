#!/bin/bash
# lane6.sh LANE kind:name ...   kind = ship (frozen shipped 141-row probe) | aug (probe.aug6.py)
# Runs each probe against /tmp/gxopuscrimec6_bins/<name>; never builds, never touches a tree.
set -u
LANE="$1"; shift
BINS=/tmp/gxopuscrimec6_bins
WD=/tmp/gxopuscrimec6_work
mkdir -p "$WD/logs"
OUT="$WD/lane_$LANE.out"
for kn in "$@"; do
    kind="${kn%%:*}"; name="${kn#*:}"
    case "$kind" in ship) P="$WD/probe.frozen.py";; aug) P="$WD/probe.aug6.py";; *) echo "bad kind $kind" >>"$OUT"; continue;; esac
    log="$WD/logs/${kind}_$name.raw"
    [ -f "$BINS/$name" ] || { echo "$kind $name: NO BINARY" >>"$OUT"; continue; }
    echo "$(date +%T) START $kind $name" >>"$OUT"
    python3 -u "$P" "$BINS/$name" "${kind}_$name" > "$log" 2>&1
    res=$(grep -oE 'CRIMEP_RESULT=[0-9]+/[0-9]+' "$log" | tail -1)
    ctl=$(grep -oE 'CRIMEP_CONTROL=(OK|FAIL)' "$log" | tail -1)
    fail=$(grep -E '^FAILING:' "$log" | tail -1)
    echo "$(date +%T) $kind $name: $res $ctl last=[$(tail -1 "$log")] $fail" >>"$OUT"
done
echo "LANE_${LANE}_DONE" >>"$OUT"
