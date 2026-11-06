#!/bin/bash
# table1_fbs.sh -- fbsdrampair test-variant TABLE 1.  Refuses to start without PRETABLE_1.out and the frozen probe
# (PRETABLE's mtime must precede runs/, TABLE.log and SCORES.txt).  Mutates ONLY the WSL scratch clone /tmp/gxfbs2,
# a cp -a of build/, under a clone-local .MUTANT written before anything is built.  Baseline (named) = fix1, the
# GXEMUL-SEC working copy at HEAD edb3213f + the fbsdrampair fix: cmp'd against the working copy and against the
# clone's source before mutant 1, then REBUILT in the clone with [ gxemul -nt source ] required.  Legs: base, HEAD
# (impl_20261105/dev_footbridge.c.pre_fbs, built in the clone), three null media; then the 40 variants of
# fbs_variants_1.py; then restored.  Restore = cp from GXEMUL-SEC, cmp, rebuild, [ gxemul -nt source ]; only then is
# the sentinel cleared and the clone removed.  Run a frozen copy (table1_fbs.run.sh) in the background, never under
# `timeout`.  Every output is written straight into table1_20261105/ (durable); TABLE1_DONE is the completion line.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
T=$SEC/regress/artifacts/fbsdrampair/table1_20261105
IMPL=$SEC/regress/artifacts/fbsdrampair/impl_20261105
C=/tmp/gxfbs2
S=src/devices/dev_footbridge.c
P=$T/probe56_frozen.py
V=$T/fbs_variants_1.py
STUB=$IMPL/arm_stub.bin
OUT=$T/runs
log(){ echo "$(date '+%F %T') $*" | tee -a $T/TABLE.log; }
[ -f $T/PRETABLE_1.out ] || { echo "ABORT: no PRETABLE_1.out"; exit 2; }
[ -f $P ] || { echo "ABORT: no frozen probe"; exit 2; }
[ -e $T/SCORES.txt ] && { echo "ABORT: SCORES.txt already exists -- preserve that table before re-running"; exit 2; }
mkdir -p $OUT
log "table 1 start; PRETABLE_1.out mtime $(stat -c %y $T/PRETABLE_1.out)"
cmp -s $T/dev_footbridge.c.fix1 $SEC/$S || { log "ABORT: fix1 is not the GXEMUL-SEC working copy"; exit 4; }
[ -e $C ] && { log "ABORT: $C already exists"; exit 3; }
cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S: fbsdrampair table 1 in progress (variants of $T/dev_footbridge.c.fix1)" > .MUTANT
log "clone $C made; sentinel: $(cat .MUTANT)"
cmp -s $S $T/dev_footbridge.c.fix1 || { log "ABORT: the clone's $S is not the baseline -- sentinel kept"; exit 4; }
log "baseline cmp: clone $S == fix1 == GXEMUL-SEC working copy (md5 $(md5sum < $S | cut -d' ' -f1))"
md5sum $P $T/dev_footbridge.c.fix1 $IMPL/dev_footbridge.c.pre_fbs $V $T/PRETABLE_1.out $STUB > $T/MD5.txt
: > $T/SCORES.txt
build(){ rm -f src/devices/dev_footbridge.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
  if [ $rc = 0 ] && [ -f src/devices/dev_footbridge.o ] && [ src/devices/dev_footbridge.o -nt $S ] \
     && [ gxemul -nt $S ] && [ gxemul -nt src/devices/dev_footbridge.o ]; then return 0; fi
  log "build $1: rc=$rc, binary NOT fresh"; return 1; }
run(){ python3 -u $P "$2" $STUB > $OUT/probe_$1.out 2>&1
  local o=$OUT/probe_$1.out
  local rows=$(sed -n 's/^ROWS=\([0-9]*\) of \([0-9]*\)$/\1\/\2/p' $o)
  local c=$(sed -n 's/^FOOTBRIDGE_SITES_CONTROL=//p' $o)
  local d=$(grep -c '^PROBE_WALL=' $o)
  local red=$(grep -E '^[A-Z][A-Za-z0-9]{1,3} .* FAIL$' $o | cut -d' ' -f1 | paste -sd, -)
  local n=$(grep -cE '^[A-Z][A-Za-z0-9]{1,3} .* FAIL$' $o)
  [ "$c" = OK ] || c=FAIL
  echo "$1 ${rows:-none} CONTROL=$c DONE=$d NRED=$n RED=${red:-none}" >> $T/SCORES.txt
  log "$1 ${rows:-none} CONTROL=$c RED=${red:-none}"; }
if build base; then log "baseline rebuilt in the clone: [ gxemul -nt $S ] holds"; run base $C/gxemul
else log "ABORT: the baseline did not build fresh -- sentinel kept, clone left"; exit 5; fi
cp $IMPL/dev_footbridge.c.pre_fbs $S
if build HEAD; then run HEAD $C/gxemul; else echo "HEAD BUILD-FAILED" >> $T/SCORES.txt; fi
run null_absent /nonexistent/gxemul
run null_true /bin/true
run null_false /bin/false
for n in $(python3 $V list); do
  if ! python3 $V apply $n $T/dev_footbridge.c.fix1 $S > /dev/null; then echo "$n APPLY-FAILED" >> $T/SCORES.txt; continue; fi
  echo "$n $(md5sum < $S | cut -d' ' -f1)" >> $T/VARIANT_MD5.txt
  if build $n; then run $n $C/gxemul; else echo "$n BUILD-FAILED" >> $T/SCORES.txt; fi
done
cp $SEC/$S $S
if cmp -s $S $SEC/$S && build restored && cmp -s $S $SEC/$S && [ gxemul -nt $S ]; then
  run restored $C/gxemul
  rm -f .MUTANT && log "restored: $S cmp's clean against GXEMUL-SEC, rebuilt, binary newer; sentinel cleared"
  cd / && rm -rf $C && [ ! -e $C ] && log "clone $C removed"
else
  log "RESTORE NOT VERIFIED -- sentinel KEPT, clone left at $C"
fi
log "SCORES.txt: $(wc -l < $T/SCORES.txt) lines"
log TABLE1_DONE
