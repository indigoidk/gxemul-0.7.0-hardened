#!/bin/bash
#  Run the main loop's CURRENT working-tree detector (frozen copy; the repo file is only READ)
#  against this seat's builds, including mutants its own table did not build.
D=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/opus_landiskaux_20260918
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
cp "$SEC/regress/landisk_aux_probe.py" /tmp/landisk_aux_probe.opusfrozen.py
echo "THEIR_PROBE md5 $(md5sum < /tmp/landisk_aux_probe.opusfrozen.py | cut -c1-12) (repo file mtime $(stat -c %y "$SEC/regress/landisk_aux_probe.py"))"
for T in base fix winm1 len1 guard lastnobrk; do
  echo "=== $T"
  python3 -u /tmp/landisk_aux_probe.opusfrozen.py /tmp/gxopus_lax_$T/gxemul /mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd | grep -E 'FAIL|RESULT|VECTOR|DONE'
done
echo RUN_THEIRS_DONE
