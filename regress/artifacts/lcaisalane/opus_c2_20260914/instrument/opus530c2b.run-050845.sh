#!/bin/bash
# opus530c2.sh -- Opus closing-pass-2 sweep for #530 (lcaisalane).  OWN clone /tmp/gxopus530c2 (cp -a of build/),
# baseline = GXEMUL-SEC's working-tree src/devices/dev_lca.c.  Writes ONLY into the clone, /tmp/gxopus530c2_bins,
# this scratch dir, and GXEMUL-SEC/regress/artifacts/lcaisalane/opus_c2_20260914/logs.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus530c2
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
A=$SEC/regress/artifacts/lcaisalane/opus_c2_20260914
L=$A/logs_panel
C=/tmp/gxopus530c2
B=/tmp/gxopus530c2_bins2
F=src/devices/dev_lca.c
PROBE=$S/lca_isalane_probe.c2.py
DEMO=$S/opus_c2_demo2.py
MUT=$S/mutants_c2b.py
LIST="${LIST:-base G1 G2 K1 C1 K2a K2b}"
mkdir -p "$B" "$L"
md5sum "$PROBE" "$SEC/regress/lca_isalane_probe.py" "$DEMO" "$MUT" "$SEC/$F" | tee "$L/INSTRUMENT.md5"
if [ ! -d "$C" ]; then cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$C" || exit 1; echo "CLONED"; fi
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F opus530c2b panel-mutant sweep -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_lca.o
    make -j3 > "$L/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_lca.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$L/build_$1.log"; return 1
    fi
}
restore_and_exit() {
    cp "$SEC/$F" "$F"
    build restored && cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && rm -f .MUTANT && echo "CLONE RESTORED after failure"
    exit 1
}
first=1
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }
    diff -u "$SEC/$F" "$F" > "$L/$m.diff"
    if [ "$m" = base ]; then cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS"; restore_and_exit; }; fi
    if [ $first = 1 ]; then rm -f src/cpus/*.o; first=0; fi
    build "$m" || restore_and_exit
done
cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "restored differs from base"
for m in $LIST; do [ "$m" = base ] || { cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; }; done
lane() {
    n=$1; shift
    for m in "$@"; do
        log="$L/probe_$m.raw"; dlog="$L/demo_$m.raw"
        ( cd "$S" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        ( cd "$S" && python3 -u "$DEMO" "$B/$m" "$m" > "$dlog" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") $(grep -c '^LCAISALANE_DONE' "$log") | $(grep '^OPUSC2_RESULT=' "$dlog") $(grep '^OPUSC2_RETRIED=' "$dlog") $(grep -c '^OPUSC2_DONE' "$dlog")"
    done > "$L/lane$n.out"
}
L0=(); L1=(); i=0
for m in $LIST; do case $((i % 2)) in 0) L0+=("$m");; 1) L1+=("$m");; esac; i=$((i + 1)); done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
wait
for m in $LIST; do grep -h "^$m " "$L/lane0.out" "$L/lane1.out"; done
echo OPUS530C2B_DONE
