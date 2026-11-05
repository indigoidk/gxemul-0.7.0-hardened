#!/bin/bash
# simulates gate_pvr_block.new's checks against a finished probe log (no probe is run: the python3 line is skipped)
LOG="$1"; BLOCK="$2"
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
P=0; F=0
check() { if [ "$2" = "$3" ]; then P=$((P+1)); else F=$((F+1)); echo "FAIL $1 got=$2 want=$3"; fi; }
LOGDIR=$(mktemp -d); PMAX=/nonexistent
cp "$LOG" "$LOGDIR/pvr_zwrite.log"
src=$(sed -e '/^python3 -u pvr_zwrite_probe.py/d' "$BLOCK")
eval "$src"
echo "SIM: $P passed, $F failed"
