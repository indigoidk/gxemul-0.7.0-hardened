#!/bin/bash
# table3_pvr.sh -- pvrrenderexit test-variant TABLE 3 (repair 3: the class closure completed, with the Z-off twins; the 128-row probe).  PREPARED, NOT RUN by
# repair 3.  Adapted from r2_20261105/table2_pvr.sh.  Run a frozen copy: `cp table3_pvr.sh table3_pvr.run.sh`, then
#   MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/pvrrenderexit/r3_20261105/table3_pvr.run.sh
# from a run_in_background call (~128 builds; each probe run ~2 s now that no session passes the STDIN CAP).
# Refuses to start without PRETABLE_3.out and the frozen instrument table3/probe128_frozen.py, or if the instrument's md5 is not the
# one PRETABLE_3.out records.  Mutates ONLY the WSL scratch clone /tmp/gxpvr4 (a cp -a of build/) under a clone-local .MUTANT written
# before anything else.  Legs: base (dev_pvr.c.fix3), HEAD (det_20261104/dev_pvr.c.HEAD), three null media, then the 128 variants of
# pvr_variants_3.py (variants/*.c).  Restore = the fix copied from GXEMUL-SEC, cmp-checked, rebuilt and freshness-checked before the
# sentinel is cleared.  Ends with `pvr_variants_3.py check`, which scores every leg against PRETABLE_3's predictions (CHECK.txt).
set -u
G=/mnt/c/DocumentNoSnc/cc/GXEMUL
SEC=$G/GXEMUL-SEC
A=$SEC/regress/artifacts/pvrrenderexit/r3_20261105
DET=$SEC/regress/artifacts/pvrrenderexit/det_20261104
C=/tmp/gxpvr4
OUT=$A/table3
P=$OUT/probe128_frozen.py
S=src/devices/dev_pvr.c
mkdir -p $OUT
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $OUT/TABLE.log; }
[ -f $A/PRETABLE_3.out ] || { log "ABORT: no PRETABLE_3.out"; exit 2; }
[ -f $P ] || { log "ABORT: no frozen probe $P"; exit 2; }
want=$(sed -n 's/^INSTRUMENT_MD5 \([0-9a-f]*\) .*/\1/p' $A/PRETABLE_3.out)
got=$(md5sum $P | cut -d' ' -f1)
[ -n "$want" ] && [ "$want" = "$got" ] || { log "ABORT: frozen probe md5 $got is not PRETABLE_3's $want"; exit 2; }
cmp -s $P $SEC/regress/pvr_zwrite_probe.py || log "NOTE: the in-tree probe has changed since PRETABLE_3; the table measures the frozen instrument"
[ -e $C ] && { log "ABORT: $C exists (remove it if its .MUTANT is gone, or restore it first)"; exit 3; }
cp -a $G/build $C || { log "ABORT: clone failed"; exit 3; }
cd $C || exit 3
echo "$S: pvrrenderexit table 3; baseline $A/dev_pvr.c.fix3" > .MUTANT
cmp -s $S $A/dev_pvr.c.fix3 && cmp -s $S $SEC/$S || { log "ABORT: clone baseline is not the fix"; exit 4; }
md5sum $P $A/dev_pvr.c.fix3 $DET/dev_pvr.c.HEAD $A/variants/*.c $A/PRETABLE_3.out > $OUT/MD5.txt; : > $OUT/SCORES.txt
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
if cmp -s $S $SEC/$S && cmp -s $S $A/dev_pvr.c.fix3 && [ gxemul -nt $S ]; then rm -f .MUTANT; log "restored: cmp clean vs SEC, binary fresh, sentinel cleared"
else log "RESTORE NOT VERIFIED -- sentinel kept"; fi
python3 $A/pvr_variants_3.py check $OUT/SCORES.txt $A/base128/probe_base128.out > $OUT/CHECK.txt 2>&1 || log "check failed: see CHECK.txt"
log "$(tail -1 $OUT/CHECK.txt)"
log TABLE3_PVR_DONE
