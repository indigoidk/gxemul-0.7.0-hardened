#!/bin/bash
# head140.sh -- pvrrenderexit repair 4, step 2: the 140-row probe (head140/probe140_run.py, cmp-identical to regress/pvr_zwrite_probe.py)
# on the PRE-FIX build, the way r3_20261105/head128 ran (det_20261104/dev_pvr.c.HEAD copied over the clone's dev_pvr.c, rebuilt,
# freshness-checked).  Mutates ONLY the WSL scratch clone /tmp/gxpvr4h (a cp -a of build/), under a clone-local .MUTANT written
# first; restore = cp from GXEMUL-SEC + cmp + rebuild + [ gxemul -nt source ] before the sentinel goes.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/pvrrenderexit/r4_20261105
DET=$SEC/regress/artifacts/pvrrenderexit/det_20261104
OUT=$A/head140
C=/tmp/gxpvr4h
P=$OUT/probe140_run.py
S=src/devices/dev_pvr.c
mkdir -p $OUT && cp $SEC/regress/pvr_zwrite_probe.py $P
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/HEAD.log; }
cmp -s $P $SEC/regress/pvr_zwrite_probe.py || { log "ABORT: the probe copy is not the in-tree probe"; exit 2; }
[ -e $C ] && { log "ABORT: $C exists"; exit 3; }
cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S: pvrrenderexit repair 4 HEAD leg; baseline GXEMUL-SEC/$S" > .MUTANT
cmp -s $S $SEC/$S || { log "ABORT: clone dev_pvr.c is not GXEMUL-SEC's"; exit 4; }
build(){ rm -f src/devices/dev_pvr.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
         [ $rc = 0 ] && [ -f src/devices/dev_pvr.o ] && [ src/devices/dev_pvr.o -nt $S ] && [ gxemul -nt $S ] && [ gxemul -nt src/devices/dev_pvr.o ] && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
md5sum $P $DET/dev_pvr.c.HEAD $SEC/$S > $OUT/MD5.txt
cp $DET/dev_pvr.c.HEAD $S
if build HEAD; then python3 -u $P $C/gxemul HEAD $OUT/sessions_HEAD > $OUT/probe_HEAD.out 2>&1
  log "HEAD $(grep -h PVR_ZWRITE_RESULT= $OUT/probe_HEAD.out) $(grep -h PVR_ZWRITE_SYMPTOM= $OUT/probe_HEAD.out) $(grep -h PVR_ZWRITE_CONTROL= $OUT/probe_HEAD.out)"
  log "HEAD $(grep -h PVR_ZWRITE_RED= $OUT/probe_HEAD.out)"; fi
cp $SEC/$S $S
if build restored && cmp -s $S $SEC/$S && [ gxemul -nt $S ]; then
  python3 -u $P $C/gxemul restored $OUT/sessions_restored > $OUT/probe_restored.out 2>&1
  log "restored $(grep -h PVR_ZWRITE_RESULT= $OUT/probe_restored.out); cmp clean vs SEC, binary fresh"; rm -f .MUTANT; log "sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
log HEAD140_DONE
