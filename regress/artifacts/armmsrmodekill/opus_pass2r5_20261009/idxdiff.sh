S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/msr/opus5
T=/tmp/gxopus562r5/LANE1/tree
diff $S/headexport/src/devices/.index $T/src/devices/.index | head -20
diff $S/headexport/src/machines/.index $T/src/machines/.index | head -20
wc -l $S/headexport/src/devices/.index $T/src/devices/.index $S/headexport/src/machines/.index $T/src/machines/.index
