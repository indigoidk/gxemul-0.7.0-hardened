#!/bin/bash
#  frozen-copy rule: the probe is copied ONCE and every run uses the copy.
T=/tmp/gxopus_p5
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
LBL="$1"
if [ ! -f /tmp/gxopus_p5_probe.py ]; then
    cp "$SEC/regress/pcc2_width_probe.py" /tmp/gxopus_p5_probe.py
fi
echo "PROBE md5: $(md5sum /tmp/gxopus_p5_probe.py)"
echo "BIN mtime: $(stat -c '%y' $T/gxemul)   SRC mtime: $(stat -c '%y' $T/src/devices/dev_pcc2.c)"
if [ "$T/gxemul" -nt "$T/src/devices/dev_pcc2.c" ]; then echo "FRESH"; else echo "*** STALE -- DO NOT TRUST ***"; fi
cd "$T" || exit 9
timeout 1500 python3 -u /tmp/gxopus_p5_probe.py "$T/gxemul" "$LBL" > "$T/probe_$LBL.out" 2>&1
echo "PROBE_RC=$?"
grep -c ' ok$'   "$T/probe_$LBL.out" | sed 's/^/GREEN /'
grep -c ' FAIL$' "$T/probe_$LBL.out" | sed 's/^/RED   /'
echo "--- reds ---"
grep ' FAIL$' "$T/probe_$LBL.out"
echo "--- tail ---"
tail -2 "$T/probe_$LBL.out"
