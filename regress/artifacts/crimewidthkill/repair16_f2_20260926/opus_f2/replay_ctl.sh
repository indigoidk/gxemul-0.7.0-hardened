#!/bin/bash
# replay_ctl.sh -- replay_ctl.py on the four short CONTROL-text sessions (ctldog sw/sd, ctlrst sw/sd) of probe 5f770991,
# on base, table 16's H_noresetclear / D_nodogclear / E_noendianclear, and this seat's D_dogbit0.  ONE lane, sequential.
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair16_f2_20260926/opus_f2
cp "$A/replay_ctl.py" /tmp/replay_ctl.frozen.py
cp "$A/sessions_5f770991.json" /tmp/sessions_5f770991.frozen.json
for bin in /tmp/gxopus_r15p2_bins/restored /tmp/gxopus_r14_bins16/H_noresetclear /tmp/gxopus_r14_bins16/D_nodogclear \
           /tmp/gxopus_r14_bins16/E_noendianclear /tmp/gxopus_r15p2_bins/D_dogbit0; do
    python3 -u /tmp/replay_ctl.frozen.py "$bin" /tmp/sessions_5f770991.frozen.json \
        "ctldog sw msg" "ctldog sd msg" "ctlrst sw msg" "ctlrst sd msg"
done
echo "REPLAY_CTL_ALL_DONE $(date '+%T')"
