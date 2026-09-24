#!/bin/bash
# Final restore check: every scratch tree's device == the FROZEN copy and no sentinel; the differential dirs' base
# copies == frozen (their var/ holds a variant copy by design); the three GXEMUL-SEC files keep their start md5s.
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/frozen/dev_footbridge.c
P=/mnt/c/DocumentNoSnc/cc/GXEMUL
for t in /tmp/opusq2c /tmp/opusq2c_w0 /tmp/opusq2c_w1 /tmp/opusq2c_w2 /tmp/opusq2c_w3 /tmp/opusq2c_ext; do
	s=$([ -e "$t/.MUTANT" ] && echo SENTINEL-PRESENT || echo no-sentinel)
	c=$(cmp -s "$t/src/devices/dev_footbridge.c" "$F" && echo device==frozen || echo DEVICE-DIFFERS)
	echo "$t $s $c"
done
for w in /tmp/opusq2c_wit0 /tmp/opusq2c_wit1 /tmp/opusq2c_wit2 /tmp/opusq2c_wit3 /tmp/opusq2c_witn /tmp/opusq2c_witr /tmp/opusq2c_wit; do
	cmp -s "$w/base/dev_footbridge.c" "$F" && echo "$w base==frozen" || echo "$w BASE DIFFERS"
done
cd /tmp/opusq2c/regress || exit 9
rm -f dfinal
gcc -O2 -std=c99 -Wall -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE -ffunction-sections -fdata-sections -Wl,--gc-sections -I/tmp/opusq2c/src -I/tmp/opusq2c/src/include -I/tmp/opusq2c/src/include/thirdparty -o dfinal diff_footbridge.c -lm
[ dfinal -nt ../src/devices/dev_footbridge.c ] && echo "fresh baseline binary newer than its source"
./dfinal > /tmp/opusq2c/final_baseline.log 2>&1; echo "run rc=$?"
tail -2 /tmp/opusq2c/final_baseline.log
cmp /tmp/opusq2c/final_baseline.log "$P/_scratchpad/fbd5/q2c/opus/baseline.log" && echo "final baseline output == setup baseline output"
md5sum "$P/GXEMUL-SEC/src/devices/dev_footbridge.c" "$P/GXEMUL-SEC/regress/diff_footbridge.c" "$P/GXEMUL-SEC/regress/gate_offline.sh"
echo FINAL_CHECK_DONE
