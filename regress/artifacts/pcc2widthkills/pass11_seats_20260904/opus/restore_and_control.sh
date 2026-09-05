#!/bin/sh
set -x
D=/tmp/gxopus_p11
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p11_opus
cp $SEC/src/devices/dev_pcc2.c $D/src/devices/dev_pcc2.c
cd $D || exit 9
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > /tmp/gxopus_p11_restore_build.log 2>&1
echo "MAKE_RC=$?"
cmp $D/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c && echo "RESTORE_CMP_CLEAN" || echo "RESTORE_CMP_DIRTY"
if [ $D/gxemul -nt $D/src/devices/dev_pcc2.c ]; then echo "FRESH_OK"; else echo "STALE_BINARY"; fi
echo "RESTORED_BINARY_MD5=$(md5sum $D/gxemul | cut -c1-12)"
#  the SAME positive control, now on the restored baseline: it must DECLINE
cd $SEC/regress || exit 9
python3 -u $P/control_iclr.py $D/gxemul RESTORED 2>&1 | tail -5
rm -f $D/.MUTANT
ls -la $D/.MUTANT 2>&1
