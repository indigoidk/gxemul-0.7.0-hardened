#!/bin/sh
set -x
D=/tmp/gxopus_p11
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
rm -rf $D
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build $D || exit 9
ls -la $D/.MUTANT 2>&1
cmp $D/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c && echo "CLONE_CMP_CLEAN" || echo "CLONE_CMP_DIRTY"
cd $D || exit 9
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > /tmp/gxopus_p11_base_build.log 2>&1
echo "MAKE_RC=$?"
ls -la $D/gxemul $D/src/devices/dev_pcc2.c
if [ $D/gxemul -nt $D/src/devices/dev_pcc2.c ]; then echo "FRESH_OK"; else echo "STALE_BINARY"; fi
tail -3 /tmp/gxopus_p11_base_build.log
