#!/bin/bash
#  lcabadval RUNG-3 WITNESS driver -- HEAD 74daefd, 2026-09-09.
#
#  READ-ONLY against build/gxemul.  Builds nothing, mutates nothing, and writes only into this
#  artifacts directory.  The probe it runs is the FROZEN copy beside it (`.asrun.py'), so the
#  shipped regress/lca_badval_probe.py is free to be edited while this runs -- the carrier's
#  frozen-copy rule, which exists because bash and python read a script at different times and
#  a comparison run owes ONE instrument.
#
#  The two-part clearance is re-run HERE and recorded in the log, rather than asserted from an
#  earlier terminal: "run it, do not assert it".
set -u
ROOT=/mnt/c/DocumentNoSnc/CC/GXEMUL
SEC=$ROOT/GXEMUL-SEC
ART=$SEC/regress/artifacts/lcabadval/witness_20260909
BIN=$ROOT/build/gxemul

echo "=== lcabadval RUNG-3 WITNESS -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD: $(cd $SEC && git rev-parse --short HEAD 2>/dev/null || echo '?')"
echo ""
echo "=== TWO-PART CLEARANCE (build/ is a BUILD tree; dev_lca.c is a SHARED file, not in"
echo "=== tools/est_divergence.txt, so cmp against SEC is the correct comparison) ==="
if cmp $ROOT/build/src/devices/dev_lca.c $SEC/src/devices/dev_lca.c; then
	echo "PART 1 PASS: build/src/devices/dev_lca.c == GXEMUL-SEC/src/devices/dev_lca.c"
else
	echo "PART 1 FAIL -- STOPPING"; exit 9
fi
if [ $BIN -nt $ROOT/build/src/devices/dev_lca.c ]; then
	echo "PART 2 PASS: build/gxemul is NEWER than its dev_lca.c"
else
	echo "PART 2 FAIL -- STOPPING"; exit 9
fi
ls -la --time-style=full-iso $BIN $ROOT/build/src/devices/dev_lca.c
echo "MUTANT sentinel: $(ls $ROOT/build/.MUTANT 2>/dev/null || echo 'absent (good)')"
echo ""
echo "=== FROZEN INSTRUMENT ==="
cmp $ART/lca_badval_probe.asrun.py $SEC/regress/lca_badval_probe.py \
	&& echo "asrun copy == shipped probe (byte-identical)" \
	|| echo "*** asrun copy DIFFERS from shipped probe ***"
md5sum $ART/lca_badval_probe.asrun.py $SEC/regress/lca_badval_probe.py
echo ""
echo "=== PROBE ==="
cd $ART
python3 -u $ART/lca_badval_probe.asrun.py $BIN HEAD_74daefd
echo "PROBE_EXIT=$?"
