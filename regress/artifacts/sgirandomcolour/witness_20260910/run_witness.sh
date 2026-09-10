#!/bin/bash
#  sgirandomcolour RUNG-3 WITNESS driver -- agy measuring seat, 2026-09-10.
#
#  READ-ONLY against build/gxemul. Builds nothing, mutates nothing, and writes only into this
#  artifacts directory. The probe it runs is the FROZEN copy beside it (`.asrun.py`).
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
ART=$SEC/regress/artifacts/sgirandomcolour/witness_20260910
BIN=$ROOT/build/gxemul

echo "=== sgirandomcolour RUNG-3 WITNESS -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD: $(cd $SEC && git rev-parse --short HEAD 2>/dev/null || echo '?')"
echo ""
echo "=== BINARY CLEARANCE ==="
ls -la --time-style=full-iso $BIN
echo "MUTANT sentinel: $(ls $ROOT/build/.MUTANT 2>/dev/null || echo 'absent (good)')"
echo ""
echo "=== FROZEN INSTRUMENT ==="
cmp $ART/sgi_re_colourdefault_probe.asrun.py $SEC/regress/sgi_re_colourdefault_probe.py \
	&& echo "asrun copy == shipped probe (byte-identical)" \
	|| echo "*** asrun copy DIFFERS from shipped probe ***"
md5sum $ART/sgi_re_colourdefault_probe.asrun.py $SEC/regress/sgi_re_colourdefault_probe.py
echo ""
echo "=== PROBE RUN 1 ==="
cd $ART
python3 -u $ART/sgi_re_colourdefault_probe.asrun.py $BIN HEAD_run1 > $ART/HEAD_run1.out 2>&1 || true
cat $ART/HEAD_run1.out
echo ""
echo "=== PROBE RUN 2 ==="
python3 -u $ART/sgi_re_colourdefault_probe.asrun.py $BIN HEAD_run2 > $ART/HEAD_run2.out 2>&1 || true
cat $ART/HEAD_run2.out
echo ""
echo "=== SENTINEL VERIFICATION ==="
tail -n 1 $ART/HEAD_run1.out
tail -n 1 $ART/HEAD_run2.out
