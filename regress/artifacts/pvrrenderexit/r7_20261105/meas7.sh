#!/bin/bash
# meas7.sh -- pvrrenderexit REGRESS stage: the fb_base / palette_cfg guard swaps (pvr_variants_7.py) and the control, each run on the
# shipped 148-row probe (probe148_frozen.py == pvr_zwrite_probe.py.pre_reg) and on the CANDIDATE 152-row probe (cand152_probe.py: the
# same rows plus the fbhi / zfbhi pair).  Mutates ONLY the WSL scratch clone /tmp/gxpvr9 (a cp -a of build/), under a clone-local
# .MUTANT written first; the base leg doubles as the freshness proof; restore = cp from GXEMUL-SEC + cmp + rebuild + [ gxemul -nt
# source ] before the sentinel goes.  Refuses to start without PREDICTIONS.txt.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/pvrrenderexit/r7_20261105
OUT=$A/meas7
C=/tmp/gxpvr9
P148=$A/probe148_frozen.py
P152=$A/cand152_probe.py
S=src/devices/dev_pvr.c
mkdir -p $OUT
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/MEAS.log; }
[ -f $A/PREDICTIONS.txt ] || { log "ABORT: no PREDICTIONS.txt"; exit 2; }
cmp -s $P148 $A/pvr_zwrite_probe.py.pre_reg || { log "ABORT: the frozen probe is not the shipped probe (pre_reg)"; exit 2; }
[ -e $C ] && { log "ABORT: $C exists"; exit 3; }
cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S: pvrrenderexit REGRESS stage, fb_base guard swaps; baseline GXEMUL-SEC/$S" > .MUTANT
cmp -s $S $SEC/$S || { log "ABORT: clone dev_pvr.c is not GXEMUL-SEC's"; exit 4; }
log "clone $C made, sentinel written, dev_pvr.c cmp-clean vs SEC"
md5sum $P148 $P152 $SEC/$S $A/variants/*.c > $OUT/MD5.txt; : > $OUT/SCORES.txt
build(){ rm -f src/devices/dev_pvr.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
         [ $rc = 0 ] && [ -f src/devices/dev_pvr.o ] && [ src/devices/dev_pvr.o -nt $S ] && [ gxemul -nt $S ] && [ gxemul -nt src/devices/dev_pvr.o ] && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
run(){ local n=$1 tag=$2 p=$3
       python3 -u $p $C/gxemul $n $OUT/sessions_${n}_$tag > $OUT/probe_${n}_$tag.out 2>&1
       local r=$(grep -h "PVR_ZWRITE_RESULT=" $OUT/probe_${n}_$tag.out | cut -d= -f2) c=$(grep -h "PVR_ZWRITE_CONTROL=" $OUT/probe_${n}_$tag.out | cut -d= -f2)
       local d=$(grep -c PVR_ZWRITE_PROBE_DONE $OUT/probe_${n}_$tag.out) red=$(grep -h "PVR_ZWRITE_RED=" $OUT/probe_${n}_$tag.out | cut -d= -f2)
       local to=$(grep -l 'transcript (TIMEOUT)' $OUT/sessions_${n}_$tag/*.txt 2>/dev/null | xargs -r -n1 basename | sed 's/\.txt$//' | paste -sd, -)
       echo "$n $tag ${r:-none} CONTROL=${c:-none} DONE=$d RED=${red:-none} TIMEOUT_SESSIONS=${to:-none}" >> $OUT/SCORES.txt
       log "$n $tag ${r:-none} RED=${red:-none}"; }
both(){ run $1 p148 $P148; run $1 c152 $P152; }
build base && both base
for v in $A/variants/*.c; do n=$(basename $v .c)
  cp $v $S
  if build $n; then both $n; else echo "$n BUILD-FAILED" >> $OUT/SCORES.txt; fi
done
cp $SEC/$S $S; build restored && both restored
if cmp -s $S $SEC/$S && [ gxemul -nt $S ]; then rm -f .MUTANT; log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
log MEAS7_DONE
