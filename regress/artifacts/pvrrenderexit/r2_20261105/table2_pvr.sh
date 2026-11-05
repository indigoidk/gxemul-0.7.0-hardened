#!/bin/bash
# table2_pvr.sh -- pvrrenderexit test-variant TABLE 2 (repair 2: the class closure, 68 rows).  PRETABLE_2.out must exist first (its
# mtime precedes table2/'s files).  Mutates ONLY the WSL scratch clone /tmp/gxpvr2 (a cp -a of build/) under a clone-local .MUTANT
# sentinel.  Legs: base (the fix), HEAD (det_20261104/dev_pvr.c.HEAD), three null media; then the 62 variants of pvr_variants_2.py.
# Restore = the fix, cmp-checked against GXEMUL-SEC, rebuilt and freshness-checked before the sentinel is cleared.
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/pvrrenderexit/r2_20261105
DET=$SEC/regress/artifacts/pvrrenderexit/det_20261104
C=/tmp/gxpvr2
OUT=$A/table2
P=$OUT/probe68_frozen.py
S=src/devices/dev_pvr.c
mkdir -p $OUT
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/TABLE.log; }
[ -f $A/PRETABLE_2.out ] || { log "ABORT: no PRETABLE_2.out"; exit 2; }
[ -f $P ] || { log "ABORT: no frozen probe"; exit 2; }
rm -rf $C && cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S: pvrrenderexit table 2; baseline $DET/dev_pvr.c.fix" > .MUTANT
cmp -s $S $DET/dev_pvr.c.fix && cmp -s $S $SEC/$S || { log "ABORT: clone baseline is not the fix"; exit 4; }
md5sum $P $DET/dev_pvr.c.fix $DET/dev_pvr.c.HEAD $A/variants/*.c $A/PRETABLE_2.out > $OUT/MD5.txt; : > $OUT/SCORES.txt
build(){ rm -f src/devices/dev_pvr.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
         [ $rc = 0 ] && [ -f src/devices/dev_pvr.o ] && [ src/devices/dev_pvr.o -nt $S ] && [ gxemul -nt src/devices/dev_pvr.o ] && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
run(){ python3 -u $P "$2" "$1" $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
       local r=$(grep -h "PVR_ZWRITE_RESULT=" $OUT/probe_$1.out | cut -d= -f2) c=$(grep -h "PVR_ZWRITE_CONTROL=" $OUT/probe_$1.out | cut -d= -f2)
       local s=$(grep -h "PVR_ZWRITE_SYMPTOM=" $OUT/probe_$1.out | cut -d= -f2) d=$(grep -c PVR_ZWRITE_PROBE_DONE $OUT/probe_$1.out)
       local red=$(grep -h "PVR_ZWRITE_RED=" $OUT/probe_$1.out | cut -d= -f2)
       echo "$1 ${r:-none} CONTROL=${c:-none} SYMPTOM=${s:-none} DONE=$d RED=${red:-none}" >> $OUT/SCORES.txt; log "$1 ${r:-none} RED=${red:-none}"; }
build base && run base $C/gxemul
cp $DET/dev_pvr.c.HEAD $S; build HEAD && run HEAD $C/gxemul
run null_true /bin/true; run null_absent /nonexistent/gxemul; run null_false /bin/false
for v in $A/variants/*.c; do n=$(basename $v .c)
  cp $v $S
  if build $n; then run $n $C/gxemul; else echo "$n BUILD-FAILED" >> $OUT/SCORES.txt; fi
done
cp $DET/dev_pvr.c.fix $S; build restored && run restored $C/gxemul
if cmp -s $S $SEC/$S && [ gxemul -nt $S ]; then rm -f .MUTANT; log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
log TABLE2_PVR_DONE
