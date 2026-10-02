#!/bin/bash
# disc_dog.sh -- the three DOG discriminators (dog_sw_clr, dog_sd_clr, dog_sw_set) against base, table 14's D_nodogclear
# and this seat's four DOG-partition builds, ONE process, sequential (light: it runs beside probe batch 1).
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_r15p2_20260926
B=/tmp/gxopus_r15p2_bins
cp "$A/disc_r15p2.py" /tmp/disc_r15p2_dog.frozen.py
for m in restored /tmp/gxopus_r14_bins14/D_nodogclear D_doglatch D_dogbit0 D_doglen8 D_dogstopwiden; do
    case "$m" in /*) bin=$m; nm=T14_$(basename "$m");; *) bin=$B/$m; nm=$m;; esac
    python3 -u /tmp/disc_r15p2_dog.frozen.py "$bin" dog_sw_clr dog_sd_clr dog_sw_set > "$A/disc/dog_$nm.out" 2>&1
done
echo "DISC_DOG_DONE $(date '+%T')"
