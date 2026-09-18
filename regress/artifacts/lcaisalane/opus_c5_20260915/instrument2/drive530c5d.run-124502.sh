#!/bin/bash
# drive530c5d.sh -- #530 closing pass 5, Opus seat (2nd instance), THIRD batch: the FOUR unbuilt cells of the
# eight-cell forward-count space (the coordinator's derivation, corrected).  WAITS for batch C's PITDRIVE_DONE first,
# so only TWO probe lanes ever run.  Launch from a FROZEN COPY.  NO `set -e'.
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
MUT=$I/mut530c5d.frozen.py
PROBE=$D/instrument/lca_isalane_probe.c5.frozen.py
NEW="WXR RXW Wdrop Rdrop"

echo "DRIVER D START $(date '+%F %T')"
echo "waiting for batch C (PITDRIVE_DONE) -- never more than two probe lanes"
until grep -q '^PITDRIVE_DONE' "$L/driverC.out"; do sleep 15; done
echo "batch C done $(date '+%T')"

cp "$I/mut530c5d.py" "$MUT"
md5sum "$ROWS" "$MUT" "$PROBE" "$SEC/$F1" "$SEC/$F2" "$SEC/$F3" | tee "$L/INSTRUMENT_D.md5"
cmp -s "$PROBE" "$SEC/regress/lca_isalane_probe.py" && echo "PROBE frozen == shipped (still)" || { echo "PROBE mismatch"; exit 1; }
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && cmp -s "$F3" "$SEC/$F3"; then
    echo "BASELINE_CMP CLEAN (clone, all THREE files)"
else echo "clone differs from SEC -- abort"; exit 1; fi
echo "$F1 $F2 $F3 -- #530 c5 (opus, 2nd) batch D: Wdrop/WXR/RXW/Rdrop; restore all three from GXEMUL-SEC, rebuild, cmp + [ gxemul -nt ]" > .MUTANT

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
    build restoredD || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
    if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && cmp -s "$F3" "$SEC/$F3" \
       && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ] && [ gxemul -nt "$F3" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean(all three) binary-nt-source=yes(all three)"
    else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1; fi
}
OK=""
for m in $NEW; do
    python3 "$MUT" "$m" "$SEC" "$C" || { echo "APPLY FAILED $m"; continue; }
    { diff -u "$SEC/$F1" "$F1"; diff -u "$SEC/$F2" "$F2"; diff -u "$SEC/$F3" "$F3"; } > "$L/$m.diff"
    if build "$m"; then OK="$OK $m"; else echo "NOTE $m DID NOT BUILD -- recorded as a RESULT, not retried"; fi
done
restore || exit 1
cmp -s "$B/base" "$B/restoredD" && echo "restoredD == base (byte-identical)" || echo "NOTE restoredD differs from base"
for m in $OK; do cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base -- EQUIVALENT MUTANT"; done
echo "BUILDS D DONE ($OK) $(date '+%F %T')"

probeleg() {
    for m in "$@"; do
        case " $OK " in *" $m "*) ;; *) echo "PROBE185 $m SKIPPED (no build)"; continue;; esac
        log="$L/probe185_$m.raw"
        ( cd "$D/instrument" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "PROBE185 $m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log") $(date '+%T')"
    done
}
pitleg() {
    for m in "$@"; do
        case " $OK " in *" $m "*) ;; *) echo "$m SKIPPED (no build)"; continue;; esac
        log="$L/pit_$m.out"
        ( cd "$I" && python3 -u pitrows530c5.frozen.py "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^PITROWS_RESULT=' "$log") done=$(grep -c '^PITROWS_DONE' "$log") $(date '+%T')"
    done
}
{ probeleg RXW Rdrop;  pitleg RXW;  } > "$L/laneD0.out" 2>&1 &
{ probeleg WXR Wdrop;  pitleg WXR;  } > "$L/laneD1.out" 2>&1 &
wait
echo "==== BATCH D RESULTS ===="
cat "$L/laneD0.out" "$L/laneD1.out"
echo "DDRIVE_DONE $(date '+%F %T')"
