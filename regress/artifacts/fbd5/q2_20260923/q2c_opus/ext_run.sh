#!/bin/bash
# SCRATCH CLOSURE EXPERIMENT: /tmp/opusq2c_ext = a copy of /tmp/opusq2c with the 707 rows + 28 Z rows; re-score every
# variant green on the 707 rows (both tables) from a FROZEN copy of the driver.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2c/frozen
rm -rf /tmp/opusq2c_ext
cp -a /tmp/opusq2c /tmp/opusq2c_ext
rm -f /tmp/opusq2c_ext/regress/d /tmp/opusq2c_ext/regress/g
cmp /tmp/opusq2c_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || exit 9
python3 "$O/mkext.py" "$F/diff_footbridge.c" /tmp/opusq2c_ext/regress/diff_ext.c || exit 9
cp /tmp/opusq2c_ext/regress/diff_ext.c "$O/diff_ext.c"
md5sum "$O/diff_ext.c"
RUN=/tmp/opusq2c_extrun_$(date +%H%M%S); mkdir -p "$RUN"
cp "$O/ext_driver.py" "$O/gen_variants.py" "$RUN/"
python3 -u "$RUN/ext_driver.py" GREENS
cp "$RUN/../opusq2c_ext/regress/diff_ext.c" /dev/null 2>&1
[ -e /tmp/opusq2c_ext/.MUTANT ] && echo "SENTINEL PRESENT" || echo "no sentinel"
cmp /tmp/opusq2c_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "ext device == frozen"
echo EXT_RUN_DONE
