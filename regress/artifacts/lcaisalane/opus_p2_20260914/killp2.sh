#!/bin/bash
# killp2.sh -- #530 (lcaisalane) PASS-2 measuring seat (Opus 5), 2026-09-14.
# Scratch clone /tmp/gxopus530 (cp -a of build/, which holds the #530 working set).  Baseline = GXEMUL-SEC's
# src/devices/dev_lca.c (the uncommitted fix).  Instrument: regress/lca_isalane_probe.py frozen here.
# Launched from a frozen copy.  Builds serial in the clone, probes in three lanes.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane/opus_p2_20260914
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530
B=/tmp/gxopus530_bins
F=src/devices/dev_lca.c
PROBE=$K/lca_isalane_probe.opusp2.py
MUT=/tmp/gxopus530_mutants.frozen.py
LIST="${LIST:-base p_wbit1 p_wnarrow p_wdrop4 p_waddr4 p_lane0decl p_nozero p_rep4 p_q8lane p_port10}"
mkdir -p "$B" "$K/logs" "$K/builds"
cp "$K/mutants_p2.py" "$MUT"
cp "$SEC/regress/lca_isalane_probe.py" "$PROBE"
cp "$SEC/regress/alpha_dummy.bin" "$K/alpha_dummy.bin"
md5sum "$PROBE" "$SEC/regress/lca_isalane_probe.py" "$MUT" "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
if [ ! -d "$C" ]; then cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$C" || exit 1; fi
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN (clone vs SEC before mutant 1)" || { echo "BASELINE_CMP DIFFERS -- abort"; exit 1; }
echo "$F #530 pass-2 opus seat mutation -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_lca.o
    make -j2 > "$K/builds/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_lca.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$K/builds/build_$1.log"; return 1
    fi
}
restore_and_exit() {
    cp "$SEC/$F" "$F"
    build restored && cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && rm -f .MUTANT && echo "CLONE RESTORED after failure"
    exit 1
}
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }
    diff -u "$SEC/$F" "$F" > "$K/logs/$m.diff"
    sleep 1
    build "$m" || restore_and_exit
done
cp "$SEC/$F" "$F"
sleep 1
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "restored differs from base"
for m in $LIST; do [ "$m" = base ] || { cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; }; done
lane() {
    n=$1; shift
    for m in "$@"; do
        log="$K/logs/probe_$m.raw"
        ( cd "$K" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log") red=[$(grep -E ' FAIL$' "$log" | cut -c1-14 | sed 's/ *$//' | tr '\n' ',')]"
    done > "$K/logs/lane$n.out"
}
L0=(); L1=(); L2=(); i=0
for m in $LIST; do case $((i % 3)) in 0) L0+=("$m");; 1) L1+=("$m");; 2) L2+=("$m");; esac; i=$((i + 1)); done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
lane 2 "${L2[@]}" &
wait
for m in $LIST; do grep -h "^$m " "$K/logs/lane0.out" "$K/logs/lane1.out" "$K/logs/lane2.out"; done
echo KILLP2_DONE
