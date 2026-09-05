#!/bin/bash
set -e
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
T=/tmp/gxopus_p3
echo "python3: $(which python3) $(python3 -V 2>&1)"
echo "make:    $(which make)"
rm -rf "$T"
cp -a /mnt/c/DocumentNoSnc/CC/GXEMUL/build "$T"
cp "$SEC/src/devices/dev_pcc2.c" "$T/src/devices/dev_pcc2.c"
cp "$T/src/devices/dev_pcc2.c" /tmp/pcc2_p3_baseline.c
cp "$SEC/regress/pcc2_width_probe.py" /tmp/p3_probe.frozen.py
echo "### BASELINE cmp vs SEC (the round's post-fix working set):"
cmp "$T/src/devices/dev_pcc2.c" "$SEC/src/devices/dev_pcc2.c" && echo "  CLEAN"
echo "### md5:"
md5sum /tmp/pcc2_p3_baseline.c /tmp/p3_probe.frozen.py "$SEC/src/devices/dev_pcc2.c" "$SEC/regress/pcc2_width_probe.py"
echo "### frozen probe row-emitting call sites: $(grep -c '^row(\|^    row(' /tmp/p3_probe.frozen.py)"
echo "SETUP_DONE"
