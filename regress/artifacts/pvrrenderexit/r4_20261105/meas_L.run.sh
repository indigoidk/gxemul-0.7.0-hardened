#!/bin/bash
# meas_L.sh -- pvrrenderexit repair 4: the LEFT clause's compares at the half pixel (pvr_variants_L.py, 4 variants) on the 140-row probe
# (meas_L/probe140_frozen.py, cmp-identical to table 4's instrument, pvr_zwrite_probe.py.table4).  Mutates ONLY the WSL scratch clone
# /tmp/gxpvr5c (a cp -a of build/), under a clone-local .MUTANT written first; restore = cp from GXEMUL-SEC + cmp + rebuild + [ gxemul
# -nt source ] before the sentinel goes.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/pvrrenderexit/r4_20261105
OUT=$A/meas_L
C=/tmp/gxpvr5c
P=$OUT/probe140_frozen.py
S=src/devices/dev_pvr.c
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/MEAS.log; }
[ -f $P ] || { log "ABORT: no frozen probe"; exit 2; }
cmp -s $P $A/pvr_zwrite_probe.py.table4 || { log "ABORT: the frozen probe is not table 4 instrument"; exit 2; }
[ -e $C ] && { log "ABORT: $C exists"; exit 3; }
cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S: pvrrenderexit repair 4: the left clause at the half pixel; baseline GXEMUL-SEC/$S" > .MUTANT
cmp -s $S $SEC/$S || { log "ABORT: clone dev_pvr.c is not GXEMUL-SEC's"; exit 4; }
log "clone $C made, sentinel written, dev_pvr.c cmp-clean vs SEC"
md5sum $P $SEC/$S $OUT/variants/*.c > $OUT/MD5.txt; : > $OUT/SCORES.txt
build(){ rm -f src/devices/dev_pvr.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
         [ $rc = 0 ] && [ -f src/devices/dev_pvr.o ] && [ src/devices/dev_pvr.o -nt $S ] && [ gxemul -nt $S ] && [ gxemul -nt src/devices/dev_pvr.o ] && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
run(){ python3 -u $P "$2" "$1" $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
       local r=$(grep -h "PVR_ZWRITE_RESULT=" $OUT/probe_$1.out | cut -d= -f2) c=$(grep -h "PVR_ZWRITE_CONTROL=" $OUT/probe_$1.out | cut -d= -f2)
       local d=$(grep -c PVR_ZWRITE_PROBE_DONE $OUT/probe_$1.out) red=$(grep -h "PVR_ZWRITE_RED=" $OUT/probe_$1.out | cut -d= -f2)
       local to=$(grep -l 'transcript (TIMEOUT)' $OUT/sessions_$1/*.txt 2>/dev/null | xargs -r -n1 basename | sed 's/\.txt$//' | paste -sd, -)
       echo "$1 ${r:-none} CONTROL=${c:-none} DONE=$d RED=${red:-none} TIMEOUT_SESSIONS=${to:-none}" >> $OUT/SCORES.txt
       log "$1 ${r:-none} RED=${red:-none} TIMEOUT_SESSIONS=${to:-none}"; }
build base && run base $C/gxemul
for v in $OUT/variants/*.c; do n=$(basename $v .c)
  cp $v $S
  if build $n; then run $n $C/gxemul; else echo "$n BUILD-FAILED" >> $OUT/SCORES.txt; fi
done
cp $SEC/$S $S; build restored && run restored $C/gxemul
if cmp -s $S $SEC/$S && [ gxemul -nt $S ]; then rm -f .MUTANT; log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
log MEAS_L_DONE
