#!/bin/sh
D=/tmp/gxopus_p11
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
echo "SENTINEL: $(cat $D/.MUTANT)"
sed -n '511,512p' $D/src/devices/dev_pcc2.c
echo "--- changed lines vs SEC ---"
diff $SEC/src/devices/dev_pcc2.c $D/src/devices/dev_pcc2.c | grep -c '^[<>]'
ls -la --time-style=+%H:%M:%S $D/src/devices/dev_pcc2.o $D/src/devices/dev_pcc2.c $D/gxemul
echo "MUTANT_BINARY_MD5=$(md5sum $D/gxemul | cut -c1-12)"
