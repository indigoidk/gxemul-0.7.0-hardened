#!/bin/bash
set -x
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
rm -rf /tmp/gxopus_p7
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build /tmp/gxopus_p7
cp $SEC/src/devices/dev_pcc2.c /tmp/gxopus_p7/src/devices/dev_pcc2.c
cmp /tmp/gxopus_p7/src/devices/dev_pcc2.c $SEC/src/devices/dev_pcc2.c && echo "CMP_CLEAN_BASELINE"
mkdir -p /tmp/p7logs
cp $SEC/regress/pcc2_width_probe.py /tmp/p7logs/frozen_probe.py
md5sum /tmp/p7logs/frozen_probe.py /tmp/gxopus_p7/src/devices/dev_pcc2.c
cd /tmp/gxopus_p7
rm -f src/devices/dev_pcc2.o gxemul
make > /tmp/p7logs/build_base.log 2>&1
echo "MAKE_RC=$?"
ls -la /tmp/gxopus_p7/gxemul || echo NO_BINARY
if [ /tmp/gxopus_p7/gxemul -nt /tmp/gxopus_p7/src/devices/dev_pcc2.c ]; then echo "FRESH_BINARY"; else echo "STALE_OR_MISSING"; fi
echo SETUP_DONE
