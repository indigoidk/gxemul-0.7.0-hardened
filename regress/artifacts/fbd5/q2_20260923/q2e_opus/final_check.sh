#!/bin/bash
# Final restore check (q2e): every scratch tree's device == the FROZEN copy and no sentinel; the differential dirs'
# base copies == frozen; a fresh baseline rebuild reproduces baseline.log; the GXEMUL-SEC files keep their start md5s.
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/frozen/dev_footbridge.c
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
for t in /tmp/opusq2e /tmp/opusq2e_w0 /tmp/opusq2e_w1 /tmp/opusq2e_w2 /tmp/opusq2e_w3 /tmp/opusq2e_ext; do
	s=$([ -e "$t/.MUTANT" ] && echo SENTINEL-PRESENT || echo no-sentinel)
	c=$(cmp -s "$t/src/devices/dev_footbridge.c" "$F" && echo device==frozen || echo DEVICE-DIFFERS)
	echo "$t $s $c"
done
for w in /tmp/opusq2e_wit0 /tmp/opusq2e_wit1 /tmp/opusq2e_wit2 /tmp/opusq2e_wit3 /tmp/opusq2e_witr; do
	cmp -s "$w/base/dev_footbridge.c" "$F" && echo "$w base==frozen" || echo "$w BASE DIFFERS"
done
cd /tmp/opusq2e/regress || exit 9
rm -f dfinal
gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I/tmp/opusq2e/src -I/tmp/opusq2e/src/include -I/tmp/opusq2e/src/include/thirdparty -o dfinal diff_footbridge.c -lm
[ dfinal -nt ../src/devices/dev_footbridge.c ] && echo "fresh baseline binary newer than its source"
./dfinal > /tmp/opusq2e/final_baseline.log 2>&1; echo "run rc=$?"
tail -2 /tmp/opusq2e/final_baseline.log
cmp /tmp/opusq2e/final_baseline.log "$P/_scratchpad/fbd5/q2e/opus/baseline.log" && echo "final baseline output == setup baseline output"
md5sum "$P/GXEMUL-SEC/src/devices/dev_footbridge.c" "$P/GXEMUL-SEC/regress/diff_footbridge.c" "$P/GXEMUL-SEC/regress/gate_offline.sh"
echo FINAL_CHECK_DONE
