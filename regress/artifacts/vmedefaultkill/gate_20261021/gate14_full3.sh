#!/bin/bash
#  gate14_full3.sh -- the FULL gate 14 (regress/gate_arm.sh with #568's rev-3 block), ALONE, on the CLEAN clone's
#  HEAD + fix568b binary (/tmp/gx568g3/gxemul.fix via PMAX) -- build/gxemul carries another session's uncommitted
#  dev_pcc2.c / mvme_pcctworeg.h / dev_lca.c / dev_sh4.c / cpu_alpha_palcode.c, and gate 14 has pcc2 blocks.
set -u
R=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress
O=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/vme/gate3
L=/tmp/gx568gate3
B=/tmp/gx568g3/gxemul.fix
[ -x "$B" ] || { echo "no binary $B"; echo "GATE14_FULL3_DONE rc=9"; exit 9; }
[ -e /tmp/gx568g3/.MUTANT ] && { echo "clone is MUTANT: $(cat /tmp/gx568g3/.MUTANT)"; echo "GATE14_FULL3_DONE rc=9"; exit 9; }
rm -rf "$L"; mkdir -p "$L"
echo "start $(date '+%F %T') PMAX $B $(md5sum < $B | cut -c1-32) gate_arm.sh $(md5sum < $R/gate_arm.sh | cut -c1-32) probe $(md5sum < $R/vme_default_probe.py | cut -c1-32)"
cd "$R" && PMAX=$B LOGDIR=$L bash gate_arm.sh
rc=$?
echo "end $(date '+%F %T') rc=$rc"
cp "$L/vme_default.log" "$O/gate14_full3_vme_default.log" 2>/dev/null
echo "GATE14_FULL3_DONE rc=$rc"
