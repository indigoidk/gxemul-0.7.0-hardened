#!/bin/bash
# Full variant table (every family in driver.py), then package logs/diffs into the opus dir.
cd /tmp/opusq2r || exit 9
O=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/fbd5/q2r/opus
rm -rf /tmp/opusq2r/logs /tmp/opusq2r/diffs
python3 -u "$O/driver.py" > "$O/driver_all.out" 2>&1
echo "driver rc=$?" >> "$O/driver_all.out"
tar czf "$O/variant_logs_and_diffs.tar.gz" -C /tmp/opusq2r logs diffs
ls -la /tmp/opusq2r/.MUTANT >> "$O/driver_all.out" 2>&1
md5sum /tmp/opusq2r/src/devices/dev_footbridge.c >> "$O/driver_all.out"
echo RUN_ALL_DONE >> "$O/driver_all.out"
