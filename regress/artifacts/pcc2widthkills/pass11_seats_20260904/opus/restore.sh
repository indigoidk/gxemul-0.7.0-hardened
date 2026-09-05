#!/bin/sh
set -x
D=/tmp/gxopus_p11
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cp $SEC/src/devices/dev_pcc2.c $D/src/devices/dev_pcc2.c
cd $D || exit 9
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > /tmp/gxopus_p11_restore_build.log 2>&1
echo "MAKE_RC=$?"
cmp $D/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c && echo "RESTORE_CMP_CLEAN" || echo "RESTORE_CMP_DIRTY"
if [ $D/gxemul -nt $D/src/devices/dev_pcc2.c ]; then echo "FRESH_OK"; else echo "STALE_BINARY"; fi
rm -f $D/.MUTANT
ls -la $D/.MUTANT 2>&1
