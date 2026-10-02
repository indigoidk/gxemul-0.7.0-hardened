#!/bin/bash
# replay_all.sh -- replay_accepts.py (the probe's own `rearm' and `latch x5' sessions) on base, table 14's D_nodogclear
# and this seat's D_doglatch / D_doglen8, one lane each.  Measures the channel of the unnamed entries-13/17 member.
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_r15p2_20260926
B=/tmp/gxopus_r15p2_bins
cp "$A/replay_accepts.py" /tmp/replay_accepts.frozen.py
cp "$A/sessions_f5e915f6.json" /tmp/sessions_f5e915f6.frozen.json
mkdir -p "$A/replay"
for m in restored /tmp/gxopus_r14_bins14/D_nodogclear D_doglatch D_doglen8; do
    case "$m" in /*) bin=$m; nm=T14_$(basename "$m");; *) bin=$B/$m; nm=$m;; esac
    python3 -u /tmp/replay_accepts.frozen.py "$bin" /tmp/sessions_f5e915f6.frozen.json > "$A/replay/replay_$nm.out" 2>&1 &
done
wait
echo "REPLAY_ALL_DONE $(date '+%T')"
