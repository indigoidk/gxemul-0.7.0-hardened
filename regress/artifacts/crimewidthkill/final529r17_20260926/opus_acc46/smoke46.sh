#!/bin/bash
#  smoke46.sh -- ONE short replay before the lanes: entry 32 latch CLEAR (sw +0x38), S38/S52 from the capture.
#  Predicted: {c t4w gap} red, one re-run session (S62) with one hit.  Runs from a frozen copy of the driver.
cd /tmp
cp /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/replay46.py /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/replay46.smoke.py
md5sum /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/replay46.smoke.py > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/smoke.md5
REPLAY_FROMCACHE=38,52 python3 -u /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/replay46.smoke.py replay /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/r17.2fe7123b.py /tmp/gxopus_acc46_bins/envmut /tmp/gxopus_acc46_cache.pkl smoke '4:W:38:*:*:C' > /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/smoke_k32C.raw 2>&1
echo RC=$?
grep -E '^CRIMEP_|^FAILING|^REPLAY46' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/smoke_k32C.raw
grep -c 'ACC46HIT' /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_acc46/runs/smoke_k32C.raw
