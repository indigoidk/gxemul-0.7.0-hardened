#!/bin/bash
#  kt568t2b.sh -- #568 table 2b: build and score the ONE clause-(e) leg M_IDATABIT1 in the clean clone /tmp/gx568g3
#  (git archive of HEAD 86114a90 + fix568b), then restore fix568b.  Clone-local sentinel; the restore is VERIFIED by
#  cmp against the SEC working tree AND by the rebuilt binary matching gxemul.fix, or the sentinel stays.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/vmedefaultkill/killtable2_20261021
O=$A/table2b
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gx568g3
PROBE=$A/vme_default_probe.rev3.frozen.py
PMD5=ddcebfe3257d3370f3c16b0bee79a4be
log() { echo "$(date '+%F %T') $*"; }
[ "$(md5sum < $PROBE | cut -c1-32)" = $PMD5 ] || { log "frozen probe md5 wrong"; exit 9; }
[ -f $O/PRETABLE2B.txt ] || { log "no PRETABLE2B.txt -- prediction not on disk"; exit 9; }
[ -e $C/.MUTANT ] && { log "clone already MUTANT: $(cat $C/.MUTANT)"; exit 9; }
log "PRETABLE2B.txt mtime $(date -r $O/PRETABLE2B.txt '+%F %T')"
python3 -I -B $O/mk_leg_idatabit.py $S/rev3/dev_vme.fix568b.c $O || { log "leg generator refused"; exit 9; }
echo "M_IDATABIT1 src/devices/dev_vme.c" > $C/.MUTANT
cp $O/legs/src/M_IDATABIT1.dev_vme.c $C/src/devices/dev_vme.c
cd $C
rm -f src/devices/dev_vme.o src/machines/machine_mvme88k.o gxemul
make -j4 > $O/build_M_IDATABIT1.log 2>&1; rc=$?
if [ $rc -ne 0 ] || [ ! -x gxemul ] || [ ! gxemul -nt src/devices/dev_vme.c ]; then
    log "BUILD M_IDATABIT1 FAILED rc=$rc -- sentinel KEPT"; exit 8
fi
log "BUILD M_IDATABIT1 rc=0 binary $(md5sum < gxemul | cut -c1-32)"
{ echo "PROBE_MD5=$(md5sum < $PROBE | cut -c1-32) LEG=M_IDATABIT1 BINARY=$(md5sum < gxemul | cut -c1-32)"
  python3 -u $PROBE $C/gxemul t2b 2>&1; } > $O/M_IDATABIT1.raw
log "M_IDATABIT1 $(grep -E '^VME_DEFAULT_(RESULT|CONTROL)=' $O/M_IDATABIT1.raw | tr '\n' ' ')"
grep ' FAIL$' $O/M_IDATABIT1.raw | sed 's/^/    red: /'
log "raw ends: $(tail -1 $O/M_IDATABIT1.raw)"
cp $S/rev3/dev_vme.fix568b.c src/devices/dev_vme.c
if ! cmp -s src/devices/dev_vme.c $R/src/devices/dev_vme.c; then
    log "RESTORE: source differs from SEC WT -- sentinel KEPT"; exit 8
fi
rm -f src/devices/dev_vme.o src/machines/machine_mvme88k.o gxemul
make -j4 > $O/build_restore.log 2>&1
if [ -x gxemul ] && [ gxemul -nt src/devices/dev_vme.c ] && \
   [ "$(md5sum < gxemul | cut -c1-32)" = "$(md5sum < gxemul.fix | cut -c1-32)" ]; then
    rm -f .MUTANT
    log "RESTORE_OK source cmp-clean vs SEC WT; rebuilt binary $(md5sum < gxemul | cut -c1-32) == gxemul.fix"
else
    log "RESTORE: rebuilt binary stale or != gxemul.fix -- sentinel KEPT"; exit 8
fi
echo "KT568T2B_DONE"
