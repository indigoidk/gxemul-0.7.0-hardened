#!/bin/bash
#  kt568t2c.sh -- #568 table 2c: build and score THREE legs (M_DFLTIDNZ, M_DFLTIDZ, M_DIRODATA) one at a time in the
#  clean clone /tmp/gx568g3 (git archive of HEAD 86114a90 + fix568b), then restore fix568b.  Clone-local sentinel; the
#  restore is VERIFIED by cmp against the SEC working tree AND by the rebuilt binary matching gxemul.fix, or it stays.
set -u
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/vmedefaultkill/killtable2_20261021
O=$A/table2c
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gx568g3
PROBE=$A/vme_default_probe.rev3.frozen.py
PMD5=ddcebfe3257d3370f3c16b0bee79a4be
log() { echo "$(date '+%F %T') $*"; }
[ "$(md5sum < $PROBE | cut -c1-32)" = $PMD5 ] || { log "frozen probe md5 wrong"; exit 9; }
[ -f $O/PRETABLE2C.txt ] || { log "no PRETABLE2C.txt -- predictions not on disk"; exit 9; }
[ -e $C/.MUTANT ] && { log "clone already MUTANT: $(cat $C/.MUTANT)"; exit 9; }
log "PRETABLE2C.txt mtime $(date -r $O/PRETABLE2C.txt '+%F %T')"
python3 -I -B $O/mk_legs_t2c.py $S/rev3/dev_vme.fix568b.c $O || { log "leg generator refused"; exit 9; }
cd $C
for LEG in M_DFLTIDNZ M_DFLTIDZ M_DIRODATA; do
    echo "$LEG src/devices/dev_vme.c" > $C/.MUTANT
    cp $O/legs/src/$LEG.dev_vme.c src/devices/dev_vme.c
    rm -f src/devices/dev_vme.o src/machines/machine_mvme88k.o gxemul
    make -j4 > $O/build_$LEG.log 2>&1; rc=$?
    if [ $rc -ne 0 ] || [ ! -x gxemul ] || [ ! gxemul -nt src/devices/dev_vme.c ]; then
        log "BUILD $LEG FAILED rc=$rc -- sentinel KEPT"; exit 8
    fi
    log "BUILD $LEG rc=0 binary $(md5sum < gxemul | cut -c1-32)"
    { echo "PROBE_MD5=$(md5sum < $PROBE | cut -c1-32) LEG=$LEG BINARY=$(md5sum < gxemul | cut -c1-32)"
      python3 -u $PROBE $C/gxemul t2c 2>&1; } > $O/$LEG.raw
    log "$LEG $(grep -E '^VME_DEFAULT_(RESULT|CONTROL)=' $O/$LEG.raw | tr '\n' ' ')"
    grep ' FAIL$' $O/$LEG.raw | sed 's/^/    red: /'
    log "$LEG raw ends: $(tail -1 $O/$LEG.raw)"
done
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
echo "KT568T2C_DONE"
