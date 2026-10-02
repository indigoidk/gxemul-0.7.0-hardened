#!/bin/bash
# pc_ctlrst.sh -- pc_ctlrst.py (the probe's own `ctlrst sw' session: AFTER's pc, v1) and replay_ctl.py's texts, on base
# and on T_halttwin, one lane.
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair16_f2_20260926/opus_f2
cp "$A/replay_ctl.py" /tmp/replay_ctl.frozen.py
cp "$A/sessions_5f770991.json" /tmp/sessions_5f770991.frozen.json
cp "$A/pc_ctlrst.py" /tmp/pc_ctlrst.frozen.py
for m in restored T_halttwin; do
    echo "== $m"
    python3 -u /tmp/pc_ctlrst.frozen.py "/tmp/gxopus_r15p2_bins/$m" /tmp/sessions_5f770991.frozen.json
    python3 -u /tmp/replay_ctl.frozen.py "/tmp/gxopus_r15p2_bins/$m" /tmp/sessions_5f770991.frozen.json "ctlrst sw msg"
done
echo "PC_CTLRST_DONE $(date '+%T')"
