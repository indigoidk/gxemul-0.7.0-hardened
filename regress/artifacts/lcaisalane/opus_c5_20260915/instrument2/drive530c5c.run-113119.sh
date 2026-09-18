#!/bin/bash
# drive530c5c.sh -- #530 closing pass 5, Opus seat (2nd instance).  Builds the TWO mutants the walled seat predicted
# and never built (noff, RWall), restores the clone, then runs (a) the FROZEN prototype 8253 row session on 13
# binaries and (b) the SHIPPED 185-row probe on RWall -- the fourth cell of the class's 2x2 at the DIRECT widths,
# which no table has ever measured.  TWO lanes.  Launch from a FROZEN COPY.  NO `set -e'.
set -u
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane/opus_c5_20260915
I=$D/instrument2
L=$D/logs2
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopus530c5
B=/tmp/gxopus530c5_bins
F1=src/devices/dev_lca.c
F2=src/devices/dev_pckbc.c
F3=src/devices/dev_8253.c
ROWS=$I/pitrows530c5.frozen.py
MUT=$I/mut530c5c.frozen.py
PROBE=$D/instrument/lca_isalane_probe.c5.frozen.py
NEW="RWall noff"
LEGS="base nox cdxZL3 noff WWall Wpure WWtail WW6 dNZtail RD2post RD2z RWall RWtail"

echo "DRIVER C START $(date '+%F %T')"
cp "$I/pitrows530c5.py" "$ROWS"; cp "$I/mut530c5c.py" "$MUT"
md5sum "$ROWS" "$MUT" "$PROBE" "$SEC/$F1" "$SEC/$F2" "$SEC/$F3" | tee "$L/INSTRUMENT_C.md5"
cmp -s "$PROBE" "$SEC/regress/lca_isalane_probe.py" && echo "PROBE frozen == shipped (still)" || { echo "PROBE mismatch"; exit 1; }
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && cmp -s "$F3" "$SEC/$F3"; then
    echo "BASELINE_CMP CLEAN (clone, all THREE files)"
else echo "clone differs from SEC -- abort"; exit 1; fi
echo "$F1 $F2 $F3 -- #530 c5 (opus, 2nd) mutants noff/RWall; restore all three from GXEMUL-SEC, rebuild, cmp + [ gxemul -nt ]" > .MUTANT

build() {
    rm -f src/cpus/*.o src/devices/dev_lca.o src/devices/dev_pckbc.o src/devices/dev_8253.o
    nice -n 19 make -j2 > "$L/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ] && [ gxemul -nt "$F3" ] \
       && [ src/devices/dev_lca.o -nt "$F1" ] && [ src/devices/dev_pckbc.o -nt "$F2" ] \
       && [ src/devices/dev_8253.o -nt "$F3" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$L/build_$1.log"; return 1; fi
}
restore() {
    cp "$SEC/$F1" "$F1"; cp "$SEC/$F2" "$F2"; cp "$SEC/$F3" "$F3"
    build restoredC || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
    if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && cmp -s "$F3" "$SEC/$F3" \
       && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ] && [ gxemul -nt "$F3" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean(all three) binary-nt-source=yes(all three)"
    else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1; fi
}
for m in $NEW; do
    python3 "$MUT" "$m" "$SEC" "$C" || { echo "APPLY FAILED $m"; restore; exit 1; }
    { diff -u "$SEC/$F1" "$F1"; diff -u "$SEC/$F2" "$F2"; diff -u "$SEC/$F3" "$F3"; } > "$L/$m.diff"
    build "$m" || { restore; exit 1; }
done
restore || exit 1
cmp -s "$B/base" "$B/restoredC" && echo "restoredC == base (byte-identical)" || echo "NOTE restoredC differs from base"
for m in $NEW; do cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base -- EQUIVALENT MUTANT"; done
echo "BUILDS C DONE $(date '+%F %T')"

pitleg() {
    for m in "$@"; do
        log="$L/pit_$m.out"
        ( cd "$I" && python3 -u pitrows530c5.frozen.py "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^PITROWS_RESULT=' "$log") done=$(grep -c '^PITROWS_DONE' "$log") $(date '+%T')"
    done
}
probeleg() {
    for m in "$@"; do
        log="$L/probe185_$m.raw"
        ( cd "$D/instrument" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "PROBE185 $m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log") $(date '+%T')"
    done
}
{ probeleg RWall; pitleg base noff WWall WWtail dNZtail RD2z; } > "$L/laneC0.out" &
{ pitleg nox cdxZL3 Wpure WW6 RD2post RWall RWtail; }        > "$L/laneC1.out" &
wait
echo "==== RESULTS ===="
cat "$L/laneC0.out" "$L/laneC1.out"
echo "PITDRIVE_DONE $(date '+%F %T')"
