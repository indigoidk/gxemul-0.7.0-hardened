#!/bin/bash
D=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/panel_501p4_agents/opus
mkdir -p "$D/logs"
for f in /tmp/gxopus501p4_*.out; do
  t=$(tail -1 "$f")
  if [ "$t" = "PCC2D_PROBE_DONE" ]; then cp "$f" "$D/logs/"; echo "copied $(basename $f)  ($(grep -c ' ok$' $f) ok)"; else echo "SKIP $(basename $f) -- no completion sentinel, tail=[$t]"; fi
done
