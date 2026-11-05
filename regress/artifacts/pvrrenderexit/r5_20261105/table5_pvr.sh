#!/bin/bash
# table5_pvr.sh -- pvrrenderexit test-variant TABLE 5 (repair 5: the swap body's statement-deletion closure, the right end from above,
# a negative span start; the 148-row probe).  Adapted from ../r4_20261105/table4_pvr.sh.  Run a frozen copy: `cp table5_pvr.sh
# table5_pvr.run.sh`, then from a run_in_background call
#   MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/pvrrenderexit/r5_20261105/table5_pvr.run.sh
# Refuses to start without PRETABLE_5.out and the frozen instrument table5/probe148_frozen.py, or if the instrument's md5 is not the
# one PRETABLE_5.out records.  Mutates ONLY the WSL scratch clone /tmp/gxpvr8 (a cp -a of build/) under a clone-local .MUTANT written
# before anything else.  Legs: base (dev_pvr.c.fix5), HEAD (det_20261104/dev_pvr.c.HEAD), three null media, then the 190 variants of
# pvr_table5.py (variants/*.c).  Restore = the fix copied from GXEMUL-SEC, cmp-checked, rebuilt and freshness-checked before the
# sentinel is cleared.  Ends with `pvr_table5.py check`, which scores every leg against PRETABLE_5's predictions (CHECK.txt).
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/pvrrenderexit/r5_20261105
DET=$SEC/regress/artifacts/pvrrenderexit/det_20261104
C=/tmp/gxpvr8
OUT=$A/table5
P=$OUT/probe148_frozen.py
S=src/devices/dev_pvr.c
mkdir -p $OUT
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/TABLE.log; }
[ -f $A/PRETABLE_5.out ] || { log "ABORT: no PRETABLE_5.out"; exit 2; }
[ -f $P ] || { log "ABORT: no frozen probe $P"; exit 2; }
want=$(sed -n 's/^INSTRUMENT_MD5 \([0-9a-f]*\) .*/\1/p' $A/PRETABLE_5.out)
got=$(md5sum $P | cut -d' ' -f1)
[ -n "$want" ] && [ "$want" = "$got" ] || { log "ABORT: frozen probe md5 $got is not PRETABLE_5's $want"; exit 2; }
cmp -s $P $SEC/regress/pvr_zwrite_probe.py || log "NOTE: the in-tree probe has changed since PRETABLE_5; the table measures the frozen instrument"
[ -e $C ] && { log "ABORT: $C exists (remove it if its .MUTANT is gone, or restore it first)"; exit 3; }
cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S: pvrrenderexit table 5; baseline $A/dev_pvr.c.fix5" > .MUTANT
cmp -s $S $A/dev_pvr.c.fix5 && cmp -s $S $SEC/$S || { log "ABORT: clone baseline is not the fix"; exit 4; }
md5sum $P $A/dev_pvr.c.fix5 $DET/dev_pvr.c.HEAD $A/variants/*.c $A/PRETABLE_5.out > $OUT/MD5.txt; : > $OUT/SCORES.txt
build(){ rm -f src/devices/dev_pvr.o; make -j4 > $OUT/build_$1.log 2>&1; local rc=$?
         [ $rc = 0 ] && [ -f src/devices/dev_pvr.o ] && [ src/devices/dev_pvr.o -nt $S ] && [ gxemul -nt $S ] && [ gxemul -nt src/devices/dev_pvr.o ] && return 0
         log "build $1 rc=$rc NOT FRESH"; return 1; }
run(){ python3 -u $P "$2" "$1" $OUT/sessions_$1 > $OUT/probe_$1.out 2>&1
       local r=$(grep -h "PVR_ZWRITE_RESULT=" $OUT/probe_$1.out | cut -d= -f2) c=$(grep -h "PVR_ZWRITE_CONTROL=" $OUT/probe_$1.out | cut -d= -f2)
       local s=$(grep -h "PVR_ZWRITE_SYMPTOM=" $OUT/probe_$1.out | cut -d= -f2) d=$(grep -c PVR_ZWRITE_PROBE_DONE $OUT/probe_$1.out)
       local red=$(grep -h "PVR_ZWRITE_RED=" $OUT/probe_$1.out | cut -d= -f2)
       local to=$(grep -l 'transcript (TIMEOUT)' $OUT/sessions_$1/*.txt 2>/dev/null | xargs -r -n1 basename | sed 's/\.txt$//' | paste -sd, -)
       echo "$1 ${r:-none} CONTROL=${c:-none} SYMPTOM=${s:-none} DONE=$d RED=${red:-none} TIMEOUT_SESSIONS=${to:-none}" >> $OUT/SCORES.txt
       log "$1 ${r:-none} RED=${red:-none} TIMEOUT_SESSIONS=${to:-none}"; }
build base && run base $C/gxemul
cp $DET/dev_pvr.c.HEAD $S; build HEAD && run HEAD $C/gxemul
run null_true /bin/true; run null_absent /nonexistent/gxemul; run null_false /bin/false
for v in $A/variants/*.c; do n=$(basename $v .c)
  cp $v $S
  if build $n; then run $n $C/gxemul; else echo "$n BUILD-FAILED" >> $OUT/SCORES.txt; fi
done
cp $SEC/$S $S; build restored && run restored $C/gxemul
if cmp -s $S $SEC/$S && cmp -s $S $A/dev_pvr.c.fix5 && [ gxemul -nt $S ]; then rm -f .MUTANT; log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
python3 $A/pvr_table5.py check $OUT/SCORES.txt $A/base148f/probe_base148f.out > $OUT/CHECK.txt 2>&1 || log "check failed: see CHECK.txt"
log "$(tail -1 $OUT/CHECK.txt)"
log TABLE5_PVR_DONE
