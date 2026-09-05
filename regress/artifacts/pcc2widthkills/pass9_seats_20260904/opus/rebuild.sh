#!/bin/sh
cd /tmp/gxopus_p9 || exit 9
rm -f src/devices/dev_pcc2.o
make >/tmp/gxopus_p9_build.log 2>&1
echo "MAKE_RC=$?"
ls -la gxemul src/devices/dev_pcc2.c src/devices/dev_pcc2.o
if [ gxemul -nt src/devices/dev_pcc2.c ]; then echo FRESH_OK; else echo STALE_BAD; fi
cmp src/devices/dev_pcc2.c /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c && echo SRC_CMP_CLEAN
tail -3 /tmp/gxopus_p9_build.log
