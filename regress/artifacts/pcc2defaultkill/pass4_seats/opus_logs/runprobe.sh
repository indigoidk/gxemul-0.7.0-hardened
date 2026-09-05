#!/bin/bash
cd /tmp/gxinst501p4 || exit 9
python3 -u /tmp/gxinst501p4/pcc2_default_probe.py /tmp/gxopus501p4/gxemul "$1" > "/tmp/gxopus501p4_$1.out" 2>&1
echo "PROBE_RC=$?"
grep -E "PCC2D_RESULT|PCC2D_RED|PCC2D_PROBE_DONE" "/tmp/gxopus501p4_$1.out"
