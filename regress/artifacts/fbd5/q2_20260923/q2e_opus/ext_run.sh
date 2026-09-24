#!/bin/bash
# SCRATCH CLOSURE EXPERIMENT: /tmp/opusq2e_ext = a copy of /tmp/opusq2e with the 862 rows + 19 Y rows; re-score ALL 54
# of this pass's variants from a FROZEN copy of the driver.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2e/frozen
rm -rf /tmp/opusq2e_ext
cp -a /tmp/opusq2e /tmp/opusq2e_ext
rm -f /tmp/opusq2e_ext/regress/d
cmp /tmp/opusq2e_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || exit 9
python3 "$O/mkext_q2e.py" "$F/diff_footbridge.c" /tmp/opusq2e_ext/regress/diff_ext.c || exit 9
cp /tmp/opusq2e_ext/regress/diff_ext.c "$O/diff_ext.c"
md5sum "$O/diff_ext.c"
RUN=/tmp/opusq2e_extrun_$(date +%H%M%S); mkdir -p "$RUN"
cp "$O/ext_driver_q2e.py" "$O/gen_q2e.py" "$RUN/"
python3 -u "$RUN/ext_driver_q2e.py" ALL
[ -e /tmp/opusq2e_ext/.MUTANT ] && echo "SENTINEL PRESENT" || echo "no sentinel"
cmp /tmp/opusq2e_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "ext device == frozen"
echo EXT_RUN_DONE
