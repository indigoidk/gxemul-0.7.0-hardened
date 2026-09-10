#!/bin/sh
#  lcaisalane RUNG-3 WITNESS driver -- 2026-09-10, Opus 5 measuring seat.
#
#  READ-ONLY against build/: it runs the ALREADY-BUILT `build/gxemul' and mutates nothing.
#  No .MUTANT sentinel is owed and none is dropped -- nothing here writes into any build tree.
#
#  The probe is run from a FROZEN COPY (`*.asrun.py') so the shipped file stays editable while the
#  measurement is in flight -- the carrier's frozen-copy rule.  Python reads the whole file at
#  startup, so run 1 and run 2 are guaranteed to be ONE instrument.
#
#  *** THE CLEARANCE AND THE EXIT STATUS GO TO $W/RUNMETA_$1.txt, NEVER TO THE .out. ***  A
#  preserved log is verified by its COMPLETION SENTINEL, so `LCAISALANE_DONE' must be the LAST
#  line of HEAD_run$1.out.  Driver v1 appended `EXIT=' and a timestamp after it, which is a
#  log-shape defect: a truncated run and a finished one would have rendered the same.  Both
#  driver-v1 runs are preserved as HEAD_run*_prelim.out and are row-identical to these.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane/witness_20260910
BIN=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul
P=$W/lca_isalane_probe.asrun.py
M=$W/RUNMETA_$1.txt

{
echo "=== two-part clearance (RUN THE CHECK, DO NOT ASSERT IT) ==="
if cmp -s /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/devices/dev_lca.c \
          /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_lca.c; then
	echo "PART1 cmp build/src/devices/dev_lca.c vs GXEMUL-SEC : CLEAN"
else
	echo "PART1 cmp build/src/devices/dev_lca.c vs GXEMUL-SEC : DIFFER"
fi
if [ "$BIN" -nt /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/devices/dev_lca.c ]; then
	echo "PART2 [ build/gxemul -nt build/src/devices/dev_lca.c ] : YES"
else
	echo "PART2 [ build/gxemul -nt build/src/devices/dev_lca.c ] : NO"
fi
ls -la --time-style=full-iso "$BIN" /mnt/c/DocumentNoSnc/CC/GXEMUL/build/src/devices/dev_lca.c
ls -la /mnt/c/DocumentNoSnc/CC/GXEMUL/build/.MUTANT 2>/dev/null || echo "build/.MUTANT : absent"
echo "run=$1  started=$(date '+%Y-%m-%d %H:%M:%S %z')"
} > "$M"

LCAISALANE_RAW=$W/raw$1 python3 -u "$P" "$BIN" "HEAD_1ce8296_run$1"
rc=$?

{
echo "probe EXIT=$rc   (1 is EXPECTED on HEAD: the witness must be RED pre-fix)"
echo "run=$1  finished=$(date '+%Y-%m-%d %H:%M:%S %z')"
} >> "$M"
exit $rc
