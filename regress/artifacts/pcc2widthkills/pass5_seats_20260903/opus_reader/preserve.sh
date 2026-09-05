#!/bin/bash
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_opus
mkdir -p "$D/artifacts"
for f in /tmp/gxopus_p5/probe_*.out; do cp "$f" "$D/artifacts/"; done
cp /tmp/gxopus_p5_disc.py "$D/artifacts/" 2>/dev/null
echo "--- completion sentinels (a preserved log is verified by its sentinel) ---"
for f in "$D"/artifacts/probe_*.out; do echo "$(tail -1 "$f")   <- $(basename $f)"; done
echo "--- final clone state ---"
ls /tmp/gxopus_p5/.MUTANT 2>/dev/null && echo "*** SENTINEL PRESENT ***" || echo "no sentinel"
cmp -s /tmp/gxopus_p5/src/devices/dev_pcc2.c /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_pcc2.c && echo "clone source CMP CLEAN vs SEC" || echo "clone source DIRTY"
if [ /tmp/gxopus_p5/gxemul -nt /tmp/gxopus_p5/src/devices/dev_pcc2.c ]; then echo "clone binary FRESH"; else echo "clone binary STALE"; fi
