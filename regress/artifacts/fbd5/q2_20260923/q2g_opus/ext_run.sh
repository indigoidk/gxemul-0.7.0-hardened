#!/bin/bash
# SCRATCH CLOSURE EXPERIMENT: /tmp/opusr3d_ext = a copy of /tmp/opusr3d with the 864 rows + W1-W8; re-score ALL 37
# of this pass's variants from a FROZEN copy of the driver.  Foreground.
set -u
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/opus
F=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2g/frozen
rm -rf /tmp/opusr3d_ext
cp -a /tmp/opusr3d /tmp/opusr3d_ext
rm -f /tmp/opusr3d_ext/regress/d
cmp /tmp/opusr3d_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" || exit 9
[ -e /tmp/opusr3d_ext/.MUTANT ] && { echo "sentinel at start"; exit 9; }
python3 "$O/mkext_q2g.py" "$F/diff_footbridge.c" /tmp/opusr3d_ext/regress/diff_ext.c || exit 9
cp /tmp/opusr3d_ext/regress/diff_ext.c "$O/diff_ext.c"
md5sum "$O/diff_ext.c"
diff "$F/diff_footbridge.c" "$O/diff_ext.c" | grep -c '^>' | sed 's/^/lines added: /'
diff "$F/diff_footbridge.c" "$O/diff_ext.c" | grep -c '^<' | sed 's/^/lines removed: /'
RUN=/tmp/opusr3d_extrun_$(date +%H%M%S); mkdir -p "$RUN"
cp "$O/ext_driver_q2g.py" "$O/gen_r3d_opus.py" "$RUN/"
python3 -u "$RUN/ext_driver_q2g.py" ALL
[ -e /tmp/opusr3d_ext/.MUTANT ] && echo "SENTINEL PRESENT" || echo "no sentinel"
cmp /tmp/opusr3d_ext/src/devices/dev_footbridge.c "$F/dev_footbridge.c" && echo "ext device == frozen"
echo EXT_RUN_DONE
