#!/bin/bash
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress || exit 1
CR=$(printf '\r')
for f in arm_endian_probe.py luna_absentcpu_probe.py mips_rounding_probe.py arm_bdt_probe.py arm_flags_probe.py crime_width_probe.py gdrom_cond_probe.py drive_guest.py selftest_absorb.py pcc2_width_probe.py; do
  echo "=== $f  ($(wc -l < "$f") lines, md5 $(md5sum "$f" | cut -c1-8), CR lines=$(grep -c "$CR" "$f"))"
  grep -nE 'endswith|pty\.fork|^import|^from|coding|def wait|def send|_mark|re\.search' "$f" | head -14
done
