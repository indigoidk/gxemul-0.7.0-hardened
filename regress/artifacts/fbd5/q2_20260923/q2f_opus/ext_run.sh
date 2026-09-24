#!/bin/bash
# SCRATCH CLOSURE EXPERIMENT: /tmp/opusq2f_ext = a copy of /tmp/opusq2f with the 864 rows + 7 W rows; re-score ALL 22
# of this pass's variants from a FROZEN copy of the driver.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2f/frozen
rm -rf /tmp/opusq2f_ext
cp -a /tmp/opusq2f /tmp/opusq2f_ext
rm -f /tmp/opusq2f_ext/regress/d
cmp /tmp/opusq2f_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || exit 9
python3 "$O/mkext_q2f.py" "$F/diff_footbridge.c" /tmp/opusq2f_ext/regress/diff_ext.c || exit 9
cp /tmp/opusq2f_ext/regress/diff_ext.c "$O/diff_ext.c"
md5sum "$O/diff_ext.c"
RUN=/tmp/opusq2f_extrun_$(date +%H%M%S); mkdir -p "$RUN"
cp "$O/ext_driver_q2f.py" "$O/gen_q2f.py" "$RUN/"
python3 -u "$RUN/ext_driver_q2f.py" ALL
[ -e /tmp/opusq2f_ext/.MUTANT ] && echo "SENTINEL PRESENT" || echo "no sentinel"
cmp /tmp/opusq2f_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "ext device == frozen"
echo EXT_RUN_DONE
