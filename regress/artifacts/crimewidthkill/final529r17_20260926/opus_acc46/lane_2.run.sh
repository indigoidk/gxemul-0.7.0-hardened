#!/bin/bash
cd /tmp
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/r17.2fe7123b.py
R=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/replay46.frozen.py
B=/tmp/gxopus_acc46_bins/envmut
K=/tmp/gxopus_acc46_cache.pkl
python3 -u $R replay $P $B $K k11S '4:W:8:*:1:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k11S.raw 2>&1
echo "k11S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k11S.raw)"
python3 -u $R replay $P $B $K k44S '8:W:8:*:100:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k44S.raw 2>&1
echo "k44S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k44S.raw)"
python3 -u $R replay $P $B $K k17S '8:W:8:*:200:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k17S.raw 2>&1
echo "k17S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k17S.raw)"
python3 -u $R replay $P $B $K k04S '4:R:0:0:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k04S.raw 2>&1
echo "k04S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k04S.raw)"
python3 -u $R replay $P $B $K k08C '4:R:8:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k08C.raw 2>&1
echo "k08C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k08C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k23S '8:R:18:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k23S.raw 2>&1
echo "k23S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k23S.raw)"
python3 -u $R replay $P $B $K k44C '8:W:8:*:100:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k44C.raw 2>&1
echo "k44C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k44C.raw)"
python3 -u $R replay $P $B $K k12C '4:W:8:*:0:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k12C.raw 2>&1
echo "k12C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k12C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k22C '8:W:18:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k22C.raw 2>&1
echo "k22C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k22C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k27S '8:R:30:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k27S.raw 2>&1
echo "k27S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k27S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k22S '8:W:18:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k22S.raw 2>&1
echo "k22S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k22S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k24S '4:W:18:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k24S.raw 2>&1
echo "k24S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k24S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k41S '4:R:4:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k41S.raw 2>&1
echo "k41S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k41S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k28S '4:W:30:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k28S.raw 2>&1
echo "k28S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k28S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k36C '4:W:40:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k36C.raw 2>&1
echo "k36C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k36C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k24C '4:W:18:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k24C.raw 2>&1
echo "k24C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k24C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k09C '8:R:8:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k09C.raw 2>&1
echo "k09C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k09C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k38C '4:W:34:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k38C.raw 2>&1
echo "k38C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k38C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k20S '4:W:10:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k20S.raw 2>&1
echo "k20S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k20S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k42S '8:R:0:1:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k42S.raw 2>&1
echo "k42S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k42S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k05S '4:R:0:1:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k05S.raw 2>&1
echo "k05S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k05S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k07C '8:W:0:1:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k07C.raw 2>&1
echo "k07C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k07C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k33C '4:R:38:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k33C.raw 2>&1
echo "k33C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k33C.raw)"
echo LANE_2_DONE
