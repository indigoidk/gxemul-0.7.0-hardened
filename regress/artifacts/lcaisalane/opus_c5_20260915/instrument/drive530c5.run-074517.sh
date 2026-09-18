#!/bin/bash
# drive530c5.sh -- #530 closing pass 5 (Opus measuring seat).  Scratch clone /tmp/gxopus530c5 (cp -a of build/),
# its own .MUTANT.  Baseline = GXEMUL-SEC working-tree src/devices/dev_lca.c + dev_pckbc.c.  Builds base + 7 mutants,
# restores, runs the shipped 185-row probe (frozen) in 2 lanes, then the discriminator on 5 binaries.
# Launch from a FROZEN COPY (drive530c5.run-<stamp>.sh).  NO `set -e': a comparison must not end the script.
set -u
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane/opus_c5_20260915
I=$D/instrument
L=$D/logs
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530c5
B=/tmp/gxopus530c5_bins
F1=src/devices/dev_lca.c
F2=src/devices/dev_pckbc.c
PROBE=$I/lca_isalane_probe.c5.frozen.py
MUT=$I/mut530c5.frozen.py
DISC=$I/disc530c5.frozen.py
LIST="RD2z WWtail WWall dNZtail W23 RWtail nox"
ALL="base RD2z WWtail WWall dNZtail W23 RWtail nox"
DLIST="base RD2z WWtail dNZtail WWall"

echo "DRIVER START $(date '+%F %T')"
[ -e "$C" ] && { echo "clone $C exists -- abort"; exit 1; }
cp "$SEC/regress/lca_isalane_probe.py" "$PROBE"
cp "$I/mut530c5.py" "$MUT"
cp "$I/disc530c5.py" "$DISC"
cmp -s "$PROBE" "$SEC/regress/lca_isalane_probe.py" && echo "PROBE frozen == shipped" || { echo "PROBE mismatch"; exit 1; }
md5sum "$PROBE" "$MUT" "$DISC" "$SEC/$F1" "$SEC/$F2" | tee "$L/INSTRUMENT.md5"

cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$C" || { echo "clone copy failed"; exit 1; }
mkdir -p "$B"
cd "$C" || exit 1
rm -f .MUTANT
cp "$SEC/$F1" "$F1"; cp "$SEC/$F2" "$F2"
if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2"; then echo "BASELINE_CMP CLEAN ($F1, $F2 == GXEMUL-SEC working tree)"
else echo "BASELINE_CMP DIFFERS -- abort"; exit 1; fi
echo "$F1 $F2 -- #530 c5 (opus) mutants; restore both from GXEMUL-SEC, rebuild, cmp + [ gxemul -nt ]" > .MUTANT

build() {
    rm -f src/cpus/*.o src/devices/dev_lca.o src/devices/dev_pckbc.o
    make -j6 > "$L/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ] \
       && [ src/devices/dev_lca.o -nt "$F1" ] && [ src/devices/dev_pckbc.o -nt "$F2" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$L/build_$1.log"; return 1; fi
}
restore() {
    cp "$SEC/$F1" "$F1"; cp "$SEC/$F2" "$F2"
    build restored || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
    if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean(both) binary-nt-source=yes(both)"
    else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1; fi
}

build base || { restore; exit 1; }
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC" "$C" || { echo "APPLY FAILED $m"; restore; exit 1; }
    { diff -u "$SEC/$F1" "$F1"; diff -u "$SEC/$F2" "$F2"; } > "$L/$m.diff"
    build "$m" || { restore; exit 1; }
done
restore || exit 1
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "NOTE restored differs from base"
for m in $LIST; do cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; done
echo "BUILDS DONE $(date '+%F %T')"

lane() {
    n=$1; shift
    for m in "$@"; do
        log="$L/probe_$m.raw"
        ( cd "$I" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log") $(date '+%T')"
    done > "$L/lane$n.out"
}
L0=(); L1=(); i=0
for m in $ALL; do case $((i % 2)) in 0) L0+=("$m");; 1) L1+=("$m");; esac; i=$((i + 1)); done
lane 0 "${L0[@]}" &
lane 1 "${L1[@]}" &
wait
echo "==== PROBE RESULTS (c5) ===="
for m in $ALL; do grep -h "^$m " "$L/lane0.out" "$L/lane1.out"; done

echo "==== DISCRIMINATOR ===="
for m in $DLIST; do
    ( cd "$I" && python3 -u "$DISC" "$B/$m" "$m" > "$L/disc_$m.out" 2>&1 )
    echo "disc $m done=$(grep -c '^DISC530C5_DONE' "$L/disc_$m.out")"
done
echo "DRIVE530C5_DONE $(date '+%F %T')"
