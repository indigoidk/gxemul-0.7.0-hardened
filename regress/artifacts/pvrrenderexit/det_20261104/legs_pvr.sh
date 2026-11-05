#!/bin/bash
# legs_pvr.sh -- pvrrenderexit detector legs in a WSL scratch clone (/tmp/gxpvr_det, a cp -a of build/; nothing under the project is
# mutated).  Baseline = the round's working-set fix (dev_pvr.c.fix, cmp-checked against GXEMUL-SEC first), rebuilt IN THE CLONE before
# anything is measured; then the HEAD leg (dev_pvr.c.HEAD), then three null media.  Clone-local sentinel; restore verified by cmp.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/pvrrenderexit/det_20261104
SEC=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC; C=/tmp/gxpvr_det; P=$A/probe51_draft_frozen.py; OUT=$A/legs51; mkdir -p $OUT
log(){ echo "$(date '+%H:%M:%S') $*" | tee -a $OUT/LEGS.log; }
cmp -s $A/dev_pvr.c.fix $SEC/src/devices/dev_pvr.c || { log "ABORT: dev_pvr.c.fix differs from SEC"; exit 2; }
rm -rf $C; cp -a /mnt/c/DocumentNoSnc/cc/GXEMUL/build $C || { log "ABORT: clone failed"; exit 2; }
cmp -s $C/src/devices/dev_pvr.c $A/dev_pvr.c.fix || { log "ABORT: clone dev_pvr.c is not the fix"; exit 2; }
build(){ rm -f $C/src/devices/dev_pvr.o; ( cd $C && make -j4 > $OUT/build_$1.log 2>&1 ); local rc=$?
         [ $C/gxemul -nt $C/src/devices/dev_pvr.c ] && [ -f $C/src/devices/dev_pvr.o ] && log "build $1 rc=$rc FRESH $(md5sum < $C/gxemul | cut -c1-12)" && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
leg(){ python3 -u $P "$2" "$1" $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
       log "leg $1: $(grep -h 'PVR_ZWRITE_RESULT\|PVR_ZWRITE_CONTROL\|PVR_ZWRITE_SYMPTOM\|PVR_ZWRITE_RED\|PVR_ZWRITE_PROBE_DONE' $OUT/probe_$1.out | tr '\n' ' ')"; }
md5sum $P $A/dev_pvr.c.fix $A/dev_pvr.c.HEAD > $OUT/MD5.txt
build base || exit 3; leg base $C/gxemul
echo "$(date) dev_pvr.c HEAD" > $C/.MUTANT; cp $A/dev_pvr.c.HEAD $C/src/devices/dev_pvr.c
build head || exit 3; leg head $C/gxemul; cp $C/gxemul $C/gxemul.head
cp $A/dev_pvr.c.fix $C/src/devices/dev_pvr.c; build restored || exit 3
cmp -s $C/src/devices/dev_pvr.c $SEC/src/devices/dev_pvr.c && [ $C/gxemul -nt $C/src/devices/dev_pvr.c ] && rm -f $C/.MUTANT && log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
leg null_true /bin/true; leg null_absent /nonexistent/gxemul; leg null_false /bin/false
log LEGS_DONE
