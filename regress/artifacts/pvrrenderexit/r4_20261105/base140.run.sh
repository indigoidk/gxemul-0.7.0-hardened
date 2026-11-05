#!/bin/bash
# base140.sh -- pvrrenderexit repair 4, step 2: the 140-row probe (a cmp-identical copy, $1/probe140_run.py) on build/gxemul, the
# way r3_20261105/base128 ran: WSL python3, session transcripts in $1/sessions.  Read-only use of build/.  Before the run it records
# the two-part clearance for the one source the fix edits (src/devices/dev_pvr.c, a SHARED file, not in tools/est_divergence.txt):
# build/'s copy cmp-clean against GXEMUL-SEC, and build/gxemul newer than it; and that build/ carries no .MUTANT sentinel.
# usage: base140.sh <outdir under r4_20261105>
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/pvrrenderexit/r4_20261105
OUT=$A/$1
S=src/devices/dev_pvr.c
mkdir -p $OUT/sessions
P=$OUT/probe140_run.py
cp $SEC/regress/pvr_zwrite_probe.py $P
{
  echo "base140.sh $(date '+%Y-%m-%d %H:%M:%S %Z')"
  grep -vE '^\s*(#|$)' $SEC/tools/est_divergence.txt | grep -qx "$S" && echo "DIVERGENCE PATH: $S -- the clearance below does not apply" || echo "shared file: $S (not in tools/est_divergence.txt)"
  cmp -s $G/build/$S $SEC/$S && echo "part 1: cmp build/$S GXEMUL-SEC/$S: CLEAN" || echo "part 1: cmp build/$S GXEMUL-SEC/$S: DIFFERENT"
  [ $G/build/gxemul -nt $G/build/$S ] && echo "part 2: build/gxemul -nt build/$S: YES" || echo "part 2: build/gxemul -nt build/$S: NO"
  [ -e $G/build/.MUTANT ] && echo "build/.MUTANT: PRESENT ($(cat $G/build/.MUTANT))" || echo "build/.MUTANT: absent"
  ls -l --time-style=full-iso $G/build/gxemul $G/build/$S | awk '{print "  " $6, $7, $9}'
  cmp -s $P $SEC/regress/pvr_zwrite_probe.py && echo "instrument: $1/probe140_run.py cmp-identical to regress/pvr_zwrite_probe.py" || echo "instrument: COPY DIFFERS"
  md5sum $P $SEC/$S $G/build/gxemul | sed 's#/mnt/c/DocumentNoSnc/cc/GXEMUL/##'
} > $OUT/CLEARANCE.txt
t0=$(date +%s.%N)
python3 -u $P $G/build/gxemul $1 $OUT/sessions > $OUT/probe_$1.out 2>&1
rc=$?
t1=$(date +%s.%N)
echo "rc=$rc wall=$(awk -v a=$t0 -v b=$t1 'BEGIN{printf "%.1f", b - a}')s" >> $OUT/probe_$1.out
tail -6 $OUT/probe_$1.out
echo BASE140_DONE
