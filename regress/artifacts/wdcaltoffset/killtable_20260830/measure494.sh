#!/bin/bash
#
#  #494 pass 2 -- run the rung-3 witness against the SHIPPED fix.
#
#      MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash \
#        /mnt/c/.../wdcaltoffset/killtable_20260830/measure494.sh
#
#  WHAT MAKES THIS DIFFERENT FROM #493's RUN: #493 measured a SYNTHETIC fix leg built
#  by mkfixleg.py.  This measures the leg built from the WORKING TREE's own diff, so
#  the claim "the witness covers the shipped code" is a measurement rather than an
#  inference.  (The two were separately shown to have byte-identical CODE lines once
#  comments are stripped -- that check is what caught a `*/` quoted inside the new
#  comment, which would have ended it early and broken the build.)
#
#  THE PROBE IS FROZEN (`cp`) BEFORE THE RUN.  A comparison run owes ONE instrument:
#  python reads the whole file at startup, so the RUNNING invocation is immune, but a
#  multi-run driver re-reads it between runs and an edit lands in the very output
#  being diffed.
#
set -u

SEC=${GXSEC:-/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC}
ART="$SEC/regress/artifacts/wdcaltoffset"
O=${OUT:-/tmp/gx494}
R="$O/run"
LOG="$O/MEASURE.log"

mkdir -p "$R"
: > "$LOG"
say () { echo "$@" | tee -a "$LOG"; }

say "=============================================================================="
say "#494 wdcaltoffset -- the witness against the SHIPPED fix"
say "=============================================================================="
say "date $(date '+%Y-%m-%d %H:%M:%S')"

for leg in base fix; do
	if [ ! -x "$O/$leg/gxemul" ]; then
		say "*** $O/$leg/gxemul missing -- run build494.sh first"
		exit 8
	fi
done

IMG="$O/altoff-scratch.img"
[ -f "$IMG" ] || dd if=/dev/zero of="$IMG" bs=1M count=8 status=none
say "image $IMG  ($(stat -c %s "$IMG") bytes)"

#  Frozen copy -- one instrument for both legs.
cp "$ART/witness_20260829/wdcaltoff_rung3_probe.py" "$R/probe.frozen.py"
say "probe frozen at $R/probe.frozen.py"
say ""

cd "$R" || exit 9
python3 -u "$R/probe.frozen.py" \
    "$O/base/gxemul" "$O/fix/gxemul" "$IMG" "$R" 2>&1 | tee -a "$LOG"

say ""
#  A preserved log is verified by its COMPLETION SENTINEL, not by its existence.
if tail -5 "$LOG" | grep -q ALTOFF_DONE; then
	say "sentinel ALTOFF_DONE present -- the run completed"
	cp "$LOG" "$ART/killtable_20260830/RESULTS_shipped.txt"
	say "preserved: killtable_20260830/RESULTS_shipped.txt"
else
	say "*** NO ALTOFF_DONE -- the run did not finish; NOT preserving a truncation"
	exit 8
fi
say "MEASURE494_DONE"
