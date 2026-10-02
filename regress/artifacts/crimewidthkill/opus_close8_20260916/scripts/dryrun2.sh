#!/bin/bash
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close8_20260916
S=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c
K11=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable11_20260916
rm -rf /tmp/c8dry2; mkdir -p /tmp/c8dry2
for m in base C_ctl4r G_lane_ctl G_glm_tim4clear; do
    python3 "$A/scripts/mutants8b.py" "$m" "$S" "/tmp/c8dry2/$m.c" || echo "FAILED $m"
done
echo "--- C_ctl4r edit vs killtable11's ---"
diff -u "$S" /tmp/c8dry2/C_ctl4r.c | grep '^[+-][^+-]' > /tmp/c8m.h
grep '^[+-][^+-]' "$K11/logs/C_ctl4r.diff" > /tmp/c8t.h
cmp -s /tmp/c8m.h /tmp/c8t.h && echo "IDENTICAL EDIT" || { echo "DIFFERS"; diff -u /tmp/c8t.h /tmp/c8m.h; }
echo "--- the glm mutant diff ---"
diff -u "$S" /tmp/c8dry2/G_glm_tim4clear.c | sed -n '3,16p'
echo "--- G_lane_ctl diff ---"
diff -u "$S" /tmp/c8dry2/G_lane_ctl.c | sed -n '3,14p'
echo "--- syntax ---"
cd /tmp/gxopusc8 || exit 1
for m in C_ctl4r G_lane_ctl G_glm_tim4clear; do
    cp /tmp/c8dry2/$m.c /tmp/c8dry2/try.c
    gcc -fsyntax-only -Isrc/include -I. /tmp/c8dry2/try.c 2>/tmp/c8dry2/$m.err && echo "SYNTAX_OK $m" || { echo "SYNTAX_FAIL $m"; head -5 /tmp/c8dry2/$m.err; }
done
echo DRYRUN2_DONE
