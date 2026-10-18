#!/bin/bash
# run_final.sh -- #565 after the pass-2 repair: the probe once against build/gxemul (as gate_ppc.sh runs it), then the
# null-medium legs, both with the FINAL probe.  Read-only on every tree but the round's artifacts dir.
cd /mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress || exit 9
A=artifacts/ppcrldiclzero/gatewire_20261018
B=/mnt/c/DocumentNoSnc/cc/GXEMUL/build/gxemul
echo "binary $(ls -la --time-style=full-iso "$B" | awk '{print $6, $7}')  probe md5 $(md5sum ppc_rldicl_probe.py | cut -c1-32)"
timeout 120 python3 -u ppc_rldicl_probe.py "$B" gate > $A/rldicl_final_build_20261018.log 2>&1; echo "probe rc=$?"
tail -3 $A/rldicl_final_build_20261018.log
bash /mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/ppcw/nullmedium.sh
