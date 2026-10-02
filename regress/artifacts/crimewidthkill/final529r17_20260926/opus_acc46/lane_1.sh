#!/bin/bash
cd /tmp
P=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/r17.2fe7123b.py
R=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/replay46.frozen.py
B=/tmp/gxopus_acc46_bins/envmut
K=/tmp/gxopus_acc46_cache.pkl
python3 -u $R replay $P $B $K k14S '8:W:8:*:201:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k14S.raw 2>&1
echo "k14S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k14S.raw)"
python3 -u $R replay $P $B $K k40S '4:W:4:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k40S.raw 2>&1
echo "k40S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k40S.raw)"
python3 -u $R replay $P $B $K k13S '4:W:8:*:200:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k13S.raw 2>&1
echo "k13S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k13S.raw)"
python3 -u $R replay $P $B $K k01S '8:W:0:0:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k01S.raw 2>&1
echo "k01S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k01S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k31C '8:R:38:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k31C.raw 2>&1
echo "k31C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k31C.raw)"
python3 -u $R replay $P $B $K k14C '8:W:8:*:201:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k14C.raw 2>&1
echo "k14C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k14C.raw)"
python3 -u $R replay $P $B $K k43C '4:W:8:*:100:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k43C.raw 2>&1
echo "k43C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k43C.raw)"
python3 -u $R replay $P $B $K k03C '4:W:0:0:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k03C.raw 2>&1
echo "k03C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k03C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k35S '8:R:40:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k35S.raw 2>&1
echo "k35S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k35S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k34S '8:W:40:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k34S.raw 2>&1
echo "k34S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k34S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k26C '8:W:30:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k26C.raw 2>&1
echo "k26C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k26C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k19S '8:R:10:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k19S.raw 2>&1
echo "k19S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k19S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k39S '4:R:34:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k39S.raw 2>&1
echo "k39S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k39S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k26S '8:W:30:*:*:S' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k26S.raw 2>&1
echo "k26S rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k26S.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k35C '8:R:40:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k35C.raw 2>&1
echo "k35C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k35C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k23C '8:R:18:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k23C.raw 2>&1
echo "k23C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k23C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k46C '8:R:278:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k46C.raw 2>&1
echo "k46C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k46C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k39C '4:R:34:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k39C.raw 2>&1
echo "k39C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k39C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k27C '8:R:30:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k27C.raw 2>&1
echo "k27C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k27C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k18C '8:W:10:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k18C.raw 2>&1
echo "k18C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k18C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k41C '4:R:4:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k41C.raw 2>&1
echo "k41C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k41C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k06C '4:W:0:1:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k06C.raw 2>&1
echo "k06C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k06C.raw)"
REPLAY_FROMCACHE=38,52 python3 -u $R replay $P $B $K k05C '4:R:0:1:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k05C.raw 2>&1
echo "k05C rc=$? $(date '+%T') $(grep -h '^CRIMEP_RESULT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/k05C.raw)"
echo LANE_1_DONE
