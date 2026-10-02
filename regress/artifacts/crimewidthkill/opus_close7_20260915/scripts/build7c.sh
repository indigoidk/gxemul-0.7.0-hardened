#!/bin/bash
# build7b.sh -- the F* mutants (added mid-pass) in the SAME clone, from the same baseline; restore + two-part clearance.
set -u
CLONE=/tmp/gxopuscrimec7
BINS=/tmp/gxopuscrimec7_bins
WD=/tmp/gxopuscrimec7_work
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
OUT=$SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
MUT="$OUT/scripts/mutate7.py"
F=src/devices/dev_sgi_ip32.c
cd "$CLONE" || exit 1
[ -e .MUTANT ] && { echo "SENTINEL PRESENT at start -- abort"; cat .MUTANT; exit 1; }
cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ] && echo "CLONE CLEAN at start (cmp + binary-nt-source)" || { echo "CLONE NOT CLEAN"; exit 1; }
cmp -s "$WD/dev_sgi_ip32.c.orig" "$SEC/$F" && echo "orig == SEC" || { echo "orig differs from SEC"; exit 1; }
for name in E3b_byp_revout_acc; do
    python3 "$MUT" "$name" "$WD/dev_sgi_ip32.c.orig" "$WD/mut_$name.c" || { echo "  $name MUTATE FAILED"; continue; }
    echo "$F: mutant $name applied by opus close-7 build7b.sh -- restore from GXEMUL-SEC" > .MUTANT
    cp "$WD/mut_$name.c" "$F"
    diff -u "$WD/dev_sgi_ip32.c.orig" "$F" > "$OUT/mutants/$name.diff"
    rm -f src/devices/dev_sgi_ip32.o gxemul
    make >"$WD/build_$name.log" 2>&1
    if [ -f gxemul ] && [ gxemul -nt "$F" ] && [ src/devices/dev_sgi_ip32.o -nt "$F" ]; then
        cp gxemul "$BINS/$name"; echo "  $name BUILT"
        cmp -s "$BINS/$name" "$BINS/base" && echo "  NOTE $name BINARY IDENTICAL TO base"
    else
        echo "  $name BUILD FAILED/STALE"; tail -6 "$WD/build_$name.log"
    fi
    cp "$WD/dev_sgi_ip32.c.orig" "$F"
done
cp "$SEC/$F" "$F"
rm -f src/devices/dev_sgi_ip32.o gxemul
make >"$WD/build_restore3.log" 2>&1
if cmp -s "$F" "$SEC/$F" && [ gxemul -nt "$F" ]; then
    rm -f .MUTANT; echo "CLONE RESTORED cmp=clean binary-nt-source=yes"
    cmp -s gxemul "$BINS/base" && echo "restored binary == base (byte-identical)" || echo "restored binary differs from base"
else
    echo "CLONE RESTORE FAILED -- sentinel kept"
fi
echo BUILD7C_DONE
