#!/bin/bash
# disclaneR.sh -- second discriminator lane, REVERSE order, own output names (disc2_<m>.out).  Waits until driver B's
# probe lanes are done (it prints "==== DISCRIMINATORS"), then works from the end of the list and stops at the first
# binary driver B has already started (disc_<m>.out exists).  At most two lanes of mine run at once.
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus530c4
B=/tmp/gxopus530c4_bins
DISC=$D/disc530c4.frozen.py
until grep -q "==== DISCRIMINATORS" "$D/logs/driverB.out"; do sleep 15; done
for m in RD2L0 R2w2 R2w WTsplit WT6 L3gate L1gate dataB dataA Wpure base; do
    [ -e "$D/logs/disc_$m.out" ] && { echo "STOP at $m (driver B has it)"; break; }
    ( cd "$D" && python3 -u "$DISC" "$B/$m" "$m" > "$D/logs/disc2_$m.out" 2>&1 )
    echo "--- $m"; grep -E "^  |DONE" "$D/logs/disc2_$m.out"
done
echo DISCLANER_DONE
