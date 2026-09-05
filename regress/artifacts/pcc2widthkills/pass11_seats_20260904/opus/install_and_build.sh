#!/bin/sh
set -x
D=/tmp/gxopus_p11
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
echo "M_ICLR TxICR guard conjunct" > $D/.MUTANT
cp /tmp/mut_scratch.c $D/src/devices/dev_pcc2.c
cd $D || exit 9
rm -f src/devices/dev_pcc2.o gxemul
make -j4 > /tmp/gxopus_p11_miclr_build.log 2>&1
echo "MAKE_RC=$?"
ls -la $D/gxemul $D/src/devices/dev_pcc2.c
if [ $D/gxemul -nt $D/src/devices/dev_pcc2.c ]; then echo "FRESH_OK"; else echo "STALE_BINARY"; fi
tail -2 /tmp/gxopus_p11_miclr_build.log
