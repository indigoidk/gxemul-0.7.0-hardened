#!/bin/bash
# disc_all.sh -- every discriminator of disc_r15p2.py against every binary this seat built, four binaries at a time.
A=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/opus_r15p2_20260926
B=/tmp/gxopus_r15p2_bins
mkdir -p "$A/disc"
cp "$A/disc_r15p2.py" /tmp/disc_r15p2.frozen.py
run() { for m in "$@"; do python3 -u /tmp/disc_r15p2.frozen.py "$B/$m" > "$A/disc/disc_$m.out" 2>&1; done; }
run restored P_ist1r_set P_imk1r_set &
run C_istW_clr C_imk2_clr C_ist2_clr &
run C_imkW_clr P_ctl2wrc_set P_istprev_set &
run P_ist_set P_imk_set census &
wait
echo "DISC_ALL_DONE $(date '+%T')"
