#!/bin/bash
#  mk_clone.sh -- #568 rev 3: a CLEAN clone of committed HEAD (git archive, no other session's
#  uncommitted edits), built twice: as-is (the pre-fix binary) and with fix568b's dev_vme.c.
#  Mutates nothing outside /tmp/gx568g3.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
C=/tmp/gx568g3
O=$S/gate3
log() { echo "$(date '+%F %T') $*"; }
fail() { log "FAILED: $*"; echo "MK_CLONE_FAILED"; exit 9; }
rm -rf $C; mkdir -p $C
tar -x -C $C -f $O/head.tar || fail "tar"
cd $C
log "clone dev_vme.c $(md5sum < src/devices/dev_vme.c | cut -c1-32) (HEAD's)"
for f in src/devices/dev_pcc2.c src/include/thirdparty/mvme_pcctworeg.h; do
    log "clone $f $(md5sum < $f | cut -c1-8)"
done
./configure > $O/configure.log 2>&1 || fail "configure"
log "configure ok"
make -j4 > $O/make_head.log 2>&1; rc=$?
log "make HEAD rc=$rc"
[ $rc -eq 0 ] && [ -x gxemul ] && [ gxemul -nt src/devices/dev_vme.c ] || fail "HEAD build"
cp -p gxemul gxemul.head
log "gxemul.head $(md5sum < gxemul.head | cut -c1-32)"
cp $S/rev3/dev_vme.fix568b.c src/devices/dev_vme.c
cmp -s src/devices/dev_vme.c $R/src/devices/dev_vme.c || fail "fix568b differs from SEC WT dev_vme.c"
log "dev_vme.c <- fix568b $(md5sum < src/devices/dev_vme.c | cut -c1-32) == SEC WT"
rm -f src/devices/dev_vme.o src/machines/machine_mvme88k.o gxemul
make -j4 > $O/make_fix.log 2>&1; rc=$?
log "make FIX rc=$rc warnings=$(grep -c 'warning:' $O/make_fix.log)"
[ $rc -eq 0 ] && [ -x gxemul ] && [ gxemul -nt src/devices/dev_vme.c ] || fail "FIX build"
cp -p gxemul gxemul.fix
log "gxemul.fix $(md5sum < gxemul.fix | cut -c1-32)"
echo "MK_CLONE_DONE"
