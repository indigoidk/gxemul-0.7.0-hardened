#!/bin/bash
# drive530c5b.sh -- #530 closing pass 5 (Opus), SECOND batch (the coordinator's panel findings).  Reuses the batch-1
# clone /tmp/gxopus530c5 (restored by drive530c5; its probes run from the COPIED bins, not the clone), with its own
# .MUTANT.  Builds at nice -n 19 make -j2 while batch 1's two probe lanes run.  Then WAITS for DRIVE530C5_DONE, runs the
# frozen 185-row probe on WW6 / RD2post / cdxZL3 (2 lanes), then disc530c5b.py on nine binaries (2 lanes).
# Launch from a FROZEN COPY.  NO `set -e'.
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
MUT=$I/mut530c5b.frozen.py
DISC=$I/disc530c5b.frozen.py
LIST="WW6 RD2post cdxZL3 Wpure"
PLIST="WW6 RD2post cdxZL3"
DLIST="base Wpure WWall WWtail WW6 dNZtail RD2post RD2z cdxZL3"

echo "DRIVER B START $(date '+%F %T')"
cp "$I/mut530c5b.py" "$MUT"; cp "$I/disc530c5b.py" "$DISC"
md5sum "$PROBE" "$MUT" "$DISC" "$SEC/$F1" "$SEC/$F2" | tee "$L/INSTRUMENT_B.md5"
cmp -s "$PROBE" "$SEC/regress/lca_isalane_probe.py" && echo "PROBE frozen == shipped (still)" || { echo "PROBE mismatch"; exit 1; }
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2"; then echo "BASELINE_CMP CLEAN (clone, both files)"
else echo "clone differs from SEC -- abort"; exit 1; fi
echo "$F1 $F2 -- #530 c5 (opus) batch B mutants; restore both from GXEMUL-SEC, rebuild, cmp + [ gxemul -nt ]" > .MUTANT

build() {
    rm -f src/cpus/*.o src/devices/dev_lca.o src/devices/dev_pckbc.o
    nice -n 19 make -j2 > "$L/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ] \
       && [ src/devices/dev_lca.o -nt "$F1" ] && [ src/devices/dev_pckbc.o -nt "$F2" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else echo "BUILD_FAIL $1 rc=$rc"; tail -25 "$L/build_$1.log"; return 1; fi
}
restore() {
    cp "$SEC/$F1" "$F1"; cp "$SEC/$F2" "$F2"
    build restoredB || { echo "RESTORE BUILD FAILED -- sentinel kept"; return 1; }
    if cmp -s "$F1" "$SEC/$F1" && cmp -s "$F2" "$SEC/$F2" && [ gxemul -nt "$F1" ] && [ gxemul -nt "$F2" ]; then
        rm -f .MUTANT; echo "CLONE RESTORED cmp=clean(both) binary-nt-source=yes(both)"
    else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; return 1; fi
}
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC" "$C" || { echo "APPLY FAILED $m"; restore; exit 1; }
    { diff -u "$SEC/$F1" "$F1"; diff -u "$SEC/$F2" "$F2"; } > "$L/$m.diff"
    build "$m" || { restore; exit 1; }
done
restore || exit 1
cmp -s "$B/base" "$B/restoredB" && echo "restoredB == base (byte-identical)" || echo "NOTE restoredB differs from base"
for m in $LIST; do cmp -s "$B/base" "$B/$m" && echo "NOTE $m BINARY IDENTICAL TO base"; done
echo "BUILDS B DONE $(date '+%F %T')"

echo "waiting for batch 1 (DRIVE530C5_DONE)"
until grep -q '^DRIVE530C5_DONE' "$L/driver.out"; do sleep 15; done
echo "batch 1 done $(date '+%T')"

lane() {
    n=$1; shift
    for m in "$@"; do
        log="$L/probe_$m.raw"
        ( cd "$I" && python3 -u "$PROBE" "$B/$m" "$m" > "$log" 2>&1 )
        echo "$m $(grep '^LCAISALANE_RESULT=' "$log") $(grep '^LCAISALANE_RETRIED=' "$log") done=$(grep -c '^LCAISALANE_DONE' "$log") $(date '+%T')"
    done > "$L/laneB$n.out"
}
lane 0 WW6 cdxZL3 &
lane 1 RD2post &
wait
echo "==== PROBE RESULTS (c5 batch B) ===="
for m in $PLIST; do grep -h "^$m " "$L/laneB0.out" "$L/laneB1.out"; done

dlane() {
    for m in "$@"; do
        ( cd "$I" && python3 -u "$DISC" "$B/$m" "$m" > "$L/discB_$m.out" 2>&1 )
        echo "discB $m done=$(grep -c '^DISC530C5B_DONE' "$L/discB_$m.out") $(date '+%T')"
    done
}
dlane base WWall WW6 RD2post cdxZL3 > "$L/dlaneB0.out" &
dlane Wpure WWtail dNZtail RD2z > "$L/dlaneB1.out" &
wait
cat "$L/dlaneB0.out" "$L/dlaneB1.out"
echo "DRIVE530C5B_DONE $(date '+%F %T')"
