#!/bin/bash
# drive530c4.sh -- #530 closing pass 4 (opus).  Clone /tmp/gxopus530c4, own .MUTANT.
# Builds base + 4 mutants of the FIXED handler, runs the shipped 111-row probe, 2 lanes.
set -u
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus530c4
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530c4
B=/tmp/gxopus530c4_bins
F=src/devices/dev_lca.c
PROBE=$D/lca_isalane_probe.c4.frozen.py
MUT=$D/mut530c4.frozen.py
LIST="Wpure dataA dataB L1gate"
ALL="base Wpure dataA dataB L1gate"

cp "$SEC/regress/lca_isalane_probe.py" "$PROBE"
cp "$D/mut530c4.py" "$MUT"
cmp -s "$PROBE" "$SEC/regress/lca_isalane_probe.py" && echo "PROBE frozen == shipped" || { echo "PROBE mismatch"; exit 1; }
md5sum "$PROBE" "$MUT" "$SEC/$F" | tee "$D/logs/INSTRUMENT.md5"

cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN (clone)" || { echo "clone differs from SEC -- abort"; exit 1; }
echo "$F #530 c4 (opus) -- restore from GXEMUL-SEC" > .MUTANT

build() {
    rm -f src/devices/dev_lca.o src/cpus/*.o
    make -j6 > "$D/logs/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_lca.o -nt "$F" ]; then cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$D/logs/build_$1.log"; return 1; fi
}
restore_and_exit() {
    cp "$SEC/$F" "$F"; build restored
    cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && rm -f .MUTANT && echo "CLONE RESTORED after failure"
    exit 1
}

# base is already built by setup.sh, but rebuild it here for a fresh cmp-clean baseline binary in this run.
cp "$SEC/$F" "$F"
build base || restore_and_exit
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }
    diff -u "$SEC/$F" "$F" > "$D/logs/$m.diff"
    build "$m" || restore_and_exit
done
# restore
cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "restored differs from base"
for m in $LIST; do cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; done

# probe, 2 lanes
lane() {
    n=$1; shift
    for m in "$@"; do
        log="$D/logs/probe_$m.raw"
        ( cd "$D" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log")"
    done > "$D/logs/lane$n.out"
}
L0=(); L1=(); i=0
for m in $ALL; do case $((i % 2)) in 0) L0+=("$m");; 1) L1+=("$m");; esac; i=$((i + 1)); done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
wait
echo "==== RESULTS (c4) ===="
for m in $ALL; do grep -h "^$m " "$D/logs/lane0.out" "$D/logs/lane1.out"; done
echo DRIVE530C4_DONE
