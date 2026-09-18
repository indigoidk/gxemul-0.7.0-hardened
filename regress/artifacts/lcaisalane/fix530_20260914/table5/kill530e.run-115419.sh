#!/bin/bash
# kill530e.sh -- #530 (lcaisalane) kill table 5 (closing pass 3: the fallthrough class closure).  Scratch clone
# /tmp/gxlca530.  Baseline = GXEMUL-SEC's src/devices/dev_lca.c (fix comment corrected after closing pass 2).
# Instrument: regress/lca_isalane_probe.py (111 rows) frozen as lca_isalane_probe.table5.py.  PRETABLE.out written first.
# Builds serial in the clone; probe runs in TWO lanes (#529 table 9 holds four).  Launch from a frozen copy.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane/fix530_20260914/table5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxlca530
B=/tmp/gxlca530e_bins
F=src/devices/dev_lca.c
PROBE=$K/lca_isalane_probe.table5.py
MUT=/tmp/m530e/mutants530e.py
LIST="${LIST:-base head x_wfallthru W1 W2 W3 W4 RD2 W5}"
mkdir -p "$B" "$K/logs" "$K/builds"
rm -rf /tmp/m530e; mkdir -p /tmp/m530e; cp "$K/mutants530e.py" /tmp/m530e/
cp "$SEC/regress/lca_isalane_probe.py" "$PROBE"
cp "$SEC/regress/alpha_dummy.bin" "$K/alpha_dummy.bin" 2>/dev/null || true
( cd "$SEC" && git show HEAD:$F ) > "$K/dev_lca.HEAD.c"
md5sum "$PROBE" "$MUT" "$SEC/$F" "$K/dev_lca.HEAD.c" | tee "$K/logs/INSTRUMENT.md5"
if [ ! -d "$C" ]; then cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$C" || exit 1; fi
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #530 kill table 5 (main loop) -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_lca.o
    make -j3 > "$K/builds/build_$1.log" 2>&1
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
    if [ "$m" = head ]; then cp "$K/dev_lca.HEAD.c" "$F"
    else python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; restore_and_exit; }; fi
    diff -u "$SEC/$F" "$F" > "$K/logs/$m.diff"
    if [ "$m" = base ]; then cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS"; restore_and_exit; }; fi
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
        log="$K/logs/probe_$m.raw"
        ( cd "$K" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") $(grep -c '^LCAISALANE_DONE' "$log")"
    done > "$K/logs/lane$n.out"
}
L0=(); L1=(); i=0
for m in $LIST; do case $((i % 2)) in 0) L0+=("$m");; 1) L1+=("$m");; esac; i=$((i + 1)); done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
wait
for m in $LIST; do grep -h "^$m " "$K/logs/lane0.out" "$K/logs/lane1.out"; done
echo KILL530E_DONE
