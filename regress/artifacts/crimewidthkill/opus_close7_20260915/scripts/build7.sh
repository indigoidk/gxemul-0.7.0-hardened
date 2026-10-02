#!/bin/bash
# build7.sh -- clone build/ into /tmp/gxopuscrimec7 (cp -a), baseline = GXEMUL-SEC's working-tree dev_sgi_ip32.c, build
# the base and every mutant into /tmp/gxopuscrimec7_bins, then restore + rebuild + two-part clearance.  Clone-local
# .MUTANT sentinel while any mutant is applied.  Writes nothing outside the clone, the bins dir, the work dir and this
# seat's artifacts dir.
set -u
CLONE=/tmp/gxopuscrimec7
BINS=/tmp/gxopuscrimec7_bins
WD=/tmp/gxopuscrimec7_work
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=$SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
MUT="$OUT/scripts/mutate7.py"
F=src/devices/dev_sgi_ip32.c
rm -rf "$CLONE" "$BINS" "$WD"; mkdir -p "$BINS" "$WD"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$CLONE" || { echo CLONE FAILED; exit 1; }
[ -e "$CLONE/.MUTANT" ] && { echo "build/ carried a .MUTANT -- abort"; cat "$CLONE/.MUTANT"; exit 1; }
cp "$SEC/$F" "$CLONE/$F"
cp "$SEC/$F" "$WD/dev_sgi_ip32.c.orig"
cmp -s "$CLONE/$F" "$SEC/$F" && echo "BASELINE cmp CLEAN vs SEC" || { echo "BASELINE cmp DIFFERS"; exit 1; }
md5sum "$SEC/$F"
cp "$SEC/regress/crime_width_probe.py" "$WD/probe.frozen.py"
cp "$SEC/regress/crime_width_probe.py" "$OUT/scripts/crime_width_probe.frozen7.py"
cmp -s "$WD/probe.frozen.py" "$SEC/regress/crime_width_probe.py" && echo "PROBE frozen cmp CLEAN" || { echo PROBE DIFFERS; exit 1; }
md5sum "$WD/probe.frozen.py"
cd "$CLONE" || exit 1
rm -f src/cpus/*.o src/devices/dev_sgi_ip32.o gxemul
echo "BUILDING BASE $(date +%T)"
make -j2 >"$WD/build_base.log" 2>&1; echo "MAKE_RC=$?"
if [ -f gxemul ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then echo "BASE BINARY FRESH"; else echo "BASE STALE/MISSING"; tail -8 "$WD/build_base.log"; exit 1; fi
cp gxemul "$BINS/base"
for name in $(python3 "$MUT" list); do
    [ "$name" = base ] && continue
    python3 "$MUT" "$name" "$WD/dev_sgi_ip32.c.orig" "$WD/mut_$name.c" || { echo "  $name MUTATE FAILED"; continue; }
    echo "$F: mutant $name applied by opus close-7 build7.sh -- restore from GXEMUL-SEC" > "$CLONE/.MUTANT"
    cp "$WD/mut_$name.c" "$F"
    diff -u "$WD/dev_sgi_ip32.c.orig" "$F" > "$OUT/mutants/$name.diff"
    rm -f src/devices/dev_sgi_ip32.o gxemul
    make >"$WD/build_$name.log" 2>&1
    if [ -f gxemul ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$BINS/$name"; echo "  $name BUILT $(grep -c '^[-+][^-+]' "$OUT/mutants/$name.diff") changed lines"
        cmp -s "$BINS/$name" "$BINS/base" && echo "  NOTE $name BINARY IDENTICAL TO base"
    else
        echo "  $name BUILD FAILED/STALE"; tail -6 "$WD/build_$name.log"
    fi
    cp "$WD/dev_sgi_ip32.c.orig" "$F"
done
# restore: source from SEC (never the script's own copy), rebuild, two-part clearance
cp "$SEC/$F" "$F"
rm -f src/devices/dev_sgi_ip32.o gxemul
make >"$WD/build_restore.log" 2>&1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then
    rm -f "$CLONE/.MUTANT"; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
    cmp -s gxemul "$BINS/base" && echo "restored binary == base (byte-identical)" || echo "restored binary differs from base"
else
    echo "CLONE RESTORE FAILED -- sentinel kept"
fi
ls -la "$BINS"
echo "BUILD7_DONE"
