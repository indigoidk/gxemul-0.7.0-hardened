#!/bin/bash
# killlen8.sh -- #530 closing pass 6+1.  ONE bounded leg: the mutant CODEX named and FABLE ordered built.
#
#   W_len8:  if (writeflag == MEM_WRITE)  ->  if (writeflag == MEM_WRITE && len <= 8)      dev_lca.c:299
#
#   PREDICTION, written before the run (mutlen8.py's docstring carries it too, and its mtime predates
#   this launch): **352/352, A CLEAN SWEEP.**  It diverges from the fix ONLY at len > 8 and the probe
#   is instruction-driven, so its widest access is STQ = 8.  No row can drive the divergent cell.
#
#   THE REACHABILITY HALF IS ALREADY SETTLED IN SOURCE, so this run decides the DISPOSITION, not the
#   fact: len > 8 IS guest-drivable (PROM GETENV -> store_buf at psize 16/64/256; split granule 1024;
#   lca_isa over 2 MB).  By Fable's branch rule a sweep here is **L2, fixed in-round.**
#
#   *** LAUNCH FROM A FROZEN COPY AND WITH run_in_background. ***  Bash reads a script incrementally.
#   SCRATCH CLONE ONLY.  No project tree is written except this artifacts directory.
set -u
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane
A=$D/table7_20260916
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530c5
B=/tmp/gxlen8_bins
F1=src/devices/dev_lca.c
PROBE=$A/lca_isalane_probe.table7.py
MUT=$A/mutlen8.py

mkdir -p "$B" "$A/len8logs"

if [ ! -d "$C" ]; then echo "CLONE $C ABSENT -- abort"; exit 1; fi
cd "$C" || exit 1
if [ -e .MUTANT ]; then echo "SENTINEL PRESENT AT START -- abort"; cat .MUTANT; exit 1; fi

#  prove the clone starts clean against SEC, so the baseline is the intended one
cmp -s "$C/$F1" "$SEC/$F1" || { echo "CLONE $F1 DIVERGENT FROM SEC AT START -- abort"; exit 1; }
echo "CLONE START: $F1 cmp CLEAN against SEC"
md5sum "$SEC/$F1" "$PROBE" | tee "$A/len8logs/INSTRUMENT.md5"

echo "$F1 -- closing pass 6+1 W_len8; restore from GXEMUL-SEC, rebuild, cmp + [ gxemul -nt ]" > .MUTANT

build () {
    rm -f src/devices/dev_lca.o
    nice -n 19 make -j2 > "$A/builds/build_len8_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F1" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc  (or binary NOT newer than source)"; return 1
    fi
}

for m in base W_len8; do
    echo "---- $m ----"
    cp "$SEC/$F1" "$C/$F1" || exit 1
    if [ "$m" != base ]; then
        python3 "$MUT" "$m" "$SEC/$F1" "$C/$F1" || { echo "APPLY FAILED $m"; continue; }
    fi
    build "$m" || continue
done

#  ---- restore and clear the sentinel ONLY after a verified two-part clearance ----
cp "$SEC/$F1" "$C/$F1"
rm -f src/devices/dev_lca.o
nice -n 19 make -j2 > "$A/builds/build_len8_restore.log" 2>&1
if cmp -s "$C/$F1" "$SEC/$F1" && [ gxemul -nt "$F1" ]; then
    rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
else
    echo "*** RESTORE INCOMPLETE -- SENTINEL LEFT IN PLACE ON PURPOSE ***"
fi

#  ---- the equivalence tell the table 7 driver uses: identical binaries ----
if cmp -s "$B/base" "$B/W_len8"; then
    echo "NOTE W_len8 BINARY IDENTICAL TO base -- EQUIVALENT MUTANT (the compiler folded it)"
else
    echo "NOTE W_len8 binary DIFFERS from base -- the edit is live in the object"
fi

#  ---- run the 352-row composite against each ----
for m in base W_len8; do
    [ -x "$B/$m" ] || { echo "NO BINARY for $m -- skipped"; continue; }
    log="$A/len8logs/probe_$m.raw"
    ( cd "$A" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
    echo "$m $(grep -oE 'LCAISALANE_RESULT=[0-9]+/[0-9]+' "$log" | tail -1) $(tail -1 "$log")"
done

echo "KILLLEN8_DONE $(date '+%Y-%m-%d %H:%M:%S')"
