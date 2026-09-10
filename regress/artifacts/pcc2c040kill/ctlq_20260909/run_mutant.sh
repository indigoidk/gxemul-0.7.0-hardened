#!/bin/sh
#  run_mutant.sh <MUTANT> <probe-file> <out-basename>
#  Restores from SEC, applies the mutant, rebuilds, checks freshness, runs the FROZEN probe.
M="$1"; PROBE="$2"; OUT="$3"
SPW=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/ctlq
ART=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/pcc2c040kill/ctlq_20260909
CL=/tmp/gxopusctlq
echo "=== MUTANT=$M  PROBE=$(basename $PROBE)  OUT=$OUT ==="
python3 "$SPW/mutate.py" "$M" || exit 9
echo "--- the edit ---"
diff -u /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c "$CL/src/devices/dev_pcc2.c"
cd "$CL" || exit 9
rm -f src/devices/dev_pcc2.o
make -j4 > /tmp/ctlq_build.log 2>&1
RC=$?
echo "MAKE_RC=$RC"
[ $RC -eq 0 ] || { tail -20 /tmp/ctlq_build.log; exit 9; }
if [ "$CL/gxemul" -nt "$CL/src/devices/dev_pcc2.c" ]; then echo "FRESHNESS=OK"; else echo "FRESHNESS=STALE"; exit 9; fi
echo "PROBE_MD5=$(md5sum $PROBE | cut -d' ' -f1)"
python3 -u "$PROBE" "$CL/gxemul" "$OUT" 2>&1 | tee "$ART/$OUT.raw"
