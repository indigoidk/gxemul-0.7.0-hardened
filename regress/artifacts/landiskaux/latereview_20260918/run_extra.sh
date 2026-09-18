#!/bin/bash
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918
cp "$D/lax_cd_probe.py" /tmp/lax_cd_probe.frozen.py; cp "$D/lax_probe.py" /tmp/lax_probe.py
cp "$D/boot_cd.py" /tmp/boot_cd.frozen.py; cp "$D/boot_cmp.py" /tmp/boot_cmp.frozen2.py
echo "CD_PROBE md5 $(md5sum < /tmp/lax_cd_probe.frozen.py | cut -c1-12)  BOOT_CD md5 $(md5sum < /tmp/boot_cd.frozen.py | cut -c1-12)  BOOT_CMP md5 $(md5sum < /tmp/boot_cmp.frozen2.py | cut -c1-12)"
for T in base fix; do
  echo "=== CD PROBE $T"; python3 -u /tmp/lax_cd_probe.frozen.py /tmp/gxopus_lax_$T/gxemul
done
for T in base fix; do
  echo "=== CD BOOT $T"; python3 -u /tmp/boot_cd.frozen.py $T /tmp/lax_bootcd_$T.log
done
echo "=== BASE QUIET BOOT, 2nd run (console-variance control)"
python3 -u /tmp/boot_cmp.frozen2.py base 0 /tmp/lax_boot_base_v0_run2.log | grep -E 'PROMPT|NONEX_2C|WD0'
python3 "$D/cmp_console.py" /tmp/lax_boot_base_v0.log /tmp/lax_boot_base_v0_run2.log
echo "=== WINM1 QUIET BOOT"; python3 -u /tmp/boot_cmp.frozen2.py winm1 0 /tmp/lax_boot_winm1_v0.log
echo "=== WINM1 VERBOSE BOOT"; python3 -u /tmp/boot_cmp.frozen2.py winm1 1 /tmp/lax_boot_winm1_v1.log
echo RUN_EXTRA_DONE
