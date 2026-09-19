#!/bin/bash
#  Farm: seven read-only codex jobs (gpt-6-astra, max) in parallel, one cxlaunch.sh each; the parent waits so no
#  child is torn down with the invoking shell.  Owner directive 2026-09-18: "send as much to Codex 6 astra".
D=/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/cxfarm_20260918
date '+FARM_START %F %T' > "$D/FARM_TIMES.txt"
for j in j1_scexempt j2_fbnobuild j3_checkertrio j4_exemptcliff j5_fbdecline j6_ptydeath j7_smallrows; do
    bash /c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/tools/cxlaunch.sh "$D/$j.md" "$D/out" "$j" > "$D/out/launch_$j.log" 2>&1 &
done
wait
date '+FARM_DONE %F %T' >> "$D/FARM_TIMES.txt"
for j in j1_scexempt j2_fbnobuild j3_checkertrio j4_exemptcliff j5_fbdecline j6_ptydeath j7_smallrows; do
    printf '%-16s %8s b   %s\n' "$j" "$(wc -c < "$D/out/codex_$j.txt")" "$(grep -m1 -E 'codex rc=|refus|VERDICT' "$D/out/launch_$j.log" | cut -c1-80)" >> "$D/FARM_TIMES.txt"
done
echo FARM_ALL_DONE >> "$D/FARM_TIMES.txt"
