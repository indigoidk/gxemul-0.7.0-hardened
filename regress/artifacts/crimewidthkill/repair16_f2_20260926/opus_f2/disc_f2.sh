#!/bin/bash
# disc_f2.sh -- disc_f2.py (free-running vs stepped CONTROL residue text) against base and M_ctldebug.
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/repair16_f2_20260926/opus_f2
cp "$A/disc_f2.py" /tmp/disc_f2.frozen.py
for m in restored M_ctldebug; do
    python3 -u /tmp/disc_f2.frozen.py "/tmp/gxopus_r15p2_bins/$m"
done
