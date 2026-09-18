#!/bin/bash
# drive530c4b.sh -- #530 closing pass 4 (opus), table 2: the panel's cells + lane questions, then discriminators.
# Builds in /tmp/gxopus530c4 (own .MUTANT) while driver 1's probes run (niced); starts its probe lanes only after
# driver 1 prints DRIVE530C4_DONE, so at most two probe lanes of mine run at any time.
set -u
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus530c4
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530c4
B=/tmp/gxopus530c4_bins
F=src/devices/dev_lca.c
PROBE=$D/lca_isalane_probe.c4.frozen.py
MUT=$D/mut530c4b.frozen.py
DISC=$D/disc530c4.frozen.py
LIST="L3gate WT6 WTsplit R2w R2w2 RD2L0"
DLIST="base Wpure dataA dataB L1gate L3gate WT6 WTsplit R2w R2w2 RD2L0"
cp "$D/mut530c4.py" "$MUT"; cp "$D/disc530c4.py" "$DISC"
cmp -s "$PROBE" "$SEC/regress/lca_isalane_probe.py" && echo "PROBE frozen == shipped" || { echo "PROBE mismatch"; exit 1; }
md5sum "$PROBE" "$MUT" "$DISC" "$SEC/$F" | tee "$D/logs/INSTRUMENT2.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN (clone)" || { echo "clone differs from SEC -- abort"; exit 1; }
echo "$F #530 c4 table 2 (opus) -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_lca.o src/cpus/*.o
    nice -n 19 make -j3 > "$D/logs/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_lca.o -nt "$F" ]; then cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$D/logs/build_$1.log"; return 1; fi
}
restore_and_exit() {
    cp "$SEC/$F" "$F"; build restored2
    cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && rm -f .MUTANT && echo "CLONE RESTORED after failure"
    exit 1
}
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }
    diff -u "$SEC/$F" "$F" > "$D/logs/$m.diff"
    build "$m" || restore_and_exit
done
cp "$SEC/$F" "$F"
build restored2 || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored2" && echo "restored2 == base (byte-identical)" || echo "restored2 differs from base"
for m in $LIST; do cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; done
echo "WAITING for driver 1 (DRIVE530C4_DONE)"
until grep -q DRIVE530C4_DONE "$D/logs/driver.out"; do sleep 20; done
echo "driver 1 done; starting table-2 probe lanes"
lane() {
    n=$1; shift
    for m in "$@"; do
        log="$D/logs/probe_$m.raw"
        ( cd "$D" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log")"
    done > "$D/logs/lane$n.out"
}
L0=(); L1=(); i=0
for m in $LIST; do case $((i % 2)) in 0) L0+=("$m");; 1) L1+=("$m");; esac; i=$((i + 1)); done
lane 2 "${L0[@]}" &
lane 3 "${L1[@]}" &
wait
echo "==== RESULTS (table 2) ===="
for m in $LIST; do grep -h "^$m " "$D/logs/lane2.out" "$D/logs/lane3.out"; done
echo "==== DISCRIMINATORS (one lane) ===="
for m in $DLIST; do ( cd "$D" && python3 -u "$DISC" "$B/$m" "$m" > "$D/logs/disc_$m.out" 2>&1 ); echo "--- $m"; grep -E "^  |DONE" "$D/logs/disc_$m.out"; done
echo DRIVE530C4B_DONE
