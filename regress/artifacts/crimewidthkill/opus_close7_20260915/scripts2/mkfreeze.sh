#!/bin/bash
#  freeze the prototype ONCE, so every leg of the comparison runs one instrument (the carrier's frozen-copy rule),
#  and record the state of the clone before any measurement.
set -u
A=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_close7_20260915
SEC=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC
W=/tmp/gxopuscrimec7_work
mkdir -p "$W" "$A/logs2"
cp "$A/scripts2/post7.py" "$W/post7.frozen.py"
chmod +x "$W/post7.frozen.py"
{
  echo "FROZEN $(date +%Y-%m-%d\ %H:%M:%S)"
  md5sum "$W/post7.frozen.py" "$A/scripts2/post7.py"
  echo "--- clone state (no mutant applied by this seat) ---"
  ls -la /tmp/gxopuscrimec7/.MUTANT 2>&1 | head -2
  cmp -s /tmp/gxopuscrimec7/src/devices/dev_sgi_ip32.c "$SEC/src/devices/dev_sgi_ip32.c" \
     && echo "clone dev_sgi_ip32.c CLEAN vs SEC" || echo "clone dev_sgi_ip32.c DIVERGENT"
  echo "--- binaries ---"
  md5sum /tmp/gxopuscrimec7_bins/* | sort
  echo "--- shipped probe md5 (not edited) ---"
  md5sum "$SEC/regress/crime_width_probe.py"
  echo "FREEZE_DONE"
} > "$A/logs2/freeze.out" 2>&1
cat "$A/logs2/freeze.out"
