#!/bin/bash
# kill529.sh -- #529 crimewidthkill kill table, scratch clone /tmp/gxopuscrime, baseline = the #529 working set.
# Launch from a FROZEN COPY (cp kill529.sh kill529.run-<stamp>.sh).  Clone-local sentinel; restore = SEC source +
# rebuild + two-part clearance, sentinel kept if either part fails.
set -u
K=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable_20260913
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
C=/tmp/gxopuscrime
B=/tmp/gxcrime529_bins
F=src/devices/dev_sgi_ip32.c
PROBE=/tmp/crime_width_probe.table1.py
MUT=/tmp/mutants529.table1.py
mkdir -p "$B" "$K/logs"
cp "$SEC/regress/crime_width_probe.py" "$PROBE"
cp "$K/mutants529.py" "$MUT"
md5sum "$PROBE" "$MUT" "$SEC/$F" | tee "$K/logs/INSTRUMENT.md5"
cd "$C" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
echo "$F #529 kill table (main loop) -- restore from GXEMUL-SEC" > .MUTANT
build() {
    rm -f src/devices/dev_sgi_ip32.o
    make -j4 > "$B/build_$1.log" 2>&1
    rc=$?
    if [ "$rc" = 0 ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$B/$1"; echo "BUILD_OK $1"
    else
        echo "BUILD_FAIL $1 rc=$rc"; tail -20 "$B/build_$1.log"; return 1
    fi
}
LIST=$(python3 "$MUT" list x x)
for m in $LIST; do
    python3 "$MUT" "$m" "$SEC/$F" "$F" || { echo "APPLY FAILED $m"; exit 1; }
    diff -u "$SEC/$F" "$F" > "$K/logs/$m.diff"
    if [ "$m" = base ]; then cmp -s "$F" "$SEC/$F" && echo "BASELINE_CMP CLEAN" || { echo "BASELINE_CMP DIFFERS"; exit 1; }; fi
    build "$m" || exit 1
done
for m in $LIST; do
    [ "$m" = base ] || { cmp -s "$B/base" "$B/$m" && echo "WARNING $m BINARY IDENTICAL TO base"; }
done
for m in $LIST; do
    python3 -u "$PROBE" "$B/$m" "$m" > "$K/logs/probe_$m.raw" 2>&1
    echo "$m $(grep '^CRIMEP_RESULT=' "$K/logs/probe_$m.raw") $(grep '^CRIMEP_CONTROL=' "$K/logs/probe_$m.raw") $(grep -c '^CRIMEP_DONE' "$K/logs/probe_$m.raw")"
done
cp "$SEC/$F" "$F"
build restored || exit 1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"; else echo "CLONE RESTORE INCOMPLETE -- sentinel kept"; fi
cmp -s "$B/base" "$B/restored" && echo "restored == base (byte-identical)" || echo "restored differs from base"
echo KILL529_DONE
