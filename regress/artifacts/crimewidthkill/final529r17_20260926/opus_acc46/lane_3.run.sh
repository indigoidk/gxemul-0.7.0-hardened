#!/bin/bash
cd /tmp
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/r17.2fe7123b.py
R=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/replay46.frozen.py
B=/tmp/gxopus_acc46_bins/envmut
K=/tmp/gxopus_acc46_cache.pkl
python3 -u $R replay $P $B $K k10S '4:W:8:*:201:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k10S.raw 2>&1
echo "k10S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k10S.raw)"
python3 -u $R replay $P $B $K k43S '4:W:8:*:100:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k43S.raw 2>&1
echo "k43S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k43S.raw)"
python3 -u $R replay $P $B $K k16S '8:W:8:*:0:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k16S.raw 2>&1
echo "k16S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k16S.raw)"
python3 -u $R replay $P $B $K k03S '4:W:0:0:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k03S.raw 2>&1
echo "k03S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k03S.raw)"
python3 -u $R replay $P $B $K k11C '4:W:8:*:1:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k11C.raw 2>&1
echo "k11C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k11C.raw)"
python3 -u $R replay $P $B $K k04C '4:R:0:0:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k04C.raw 2>&1
echo "k04C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k04C.raw)"
python3 -u $R replay $P $B $K k10C '4:W:8:*:201:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k10C.raw 2>&1
echo "k10C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k10C.raw)"
python3 -u $R replay $P $B $K k16C '8:W:8:*:0:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k16C.raw 2>&1
echo "k16C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k16C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k46S '8:R:278:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k46S.raw 2>&1
echo "k46S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k46S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k21S '4:R:10:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k21S.raw 2>&1
echo "k21S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k21S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k45C '8:W:278:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k45C.raw 2>&1
echo "k45C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k45C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k36S '4:W:40:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k36S.raw 2>&1
echo "k36S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k36S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k45S '8:W:278:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k45S.raw 2>&1
echo "k45S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k45S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k29S '4:R:30:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k29S.raw 2>&1
echo "k29S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k29S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k37C '4:R:40:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k37C.raw 2>&1
echo "k37C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k37C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k30C '8:W:38:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k30C.raw 2>&1
echo "k30C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k30C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k19C '8:R:10:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k19C.raw 2>&1
echo "k19C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k19C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k25S '4:R:18:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k25S.raw 2>&1
echo "k25S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k25S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k28C '4:W:30:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k28C.raw 2>&1
echo "k28C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k28C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k20C '4:W:10:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k20C.raw 2>&1
echo "k20C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k20C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k06S '4:W:0:1:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k06S.raw 2>&1
echo "k06S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k06S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k42C '8:R:0:1:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k42C.raw 2>&1
echo "k42C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k42C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k32S '4:W:38:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k32S.raw 2>&1
echo "k32S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k32S.raw)"
echo LANE_3_DONE
