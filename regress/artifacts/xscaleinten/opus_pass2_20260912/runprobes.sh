#!/bin/bash
# usage: runprobes.sh LABEL OUTDIR_X OUTDIR_P
LABEL="$1"; OX="$2"; OP="$3"
SD=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opus_p2
CL=/tmp/gxopus_p2
STUB=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/xscaleinten/base_20260912/xscale_stub.bin
cd /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress

echo "### XSCALE $LABEL"
python3 -u "$SD/xscale_inten_probe.frozen.py" "$CL/gxemul" "$LABEL" "$STUB" > "$OX/xscale_${LABEL}.log" 2>&1
grep -E 'XSCALE_RESULT|XSCALE_CONTROL|XSCALE_PROBE_DONE|^FAILING' "$OX/xscale_${LABEL}.log" | tr '\n' ' '; echo

echo "### RLWIMI $LABEL"
python3 -u "$SD/ppc_rlwimi_probe.frozen.py" "$CL/gxemul" "$LABEL" > "$OP/rlwimi_${LABEL}.log" 2>&1
grep -E 'PPC_RLWIMI_RESULT|PPC_RLWIMI_CONTROL|PPC_RLWIMI_PROBE_DONE|^FAILING' "$OP/rlwimi_${LABEL}.log" | tr '\n' ' '; echo

echo "### RLDIMI $LABEL"
python3 -u "$SD/ppc_rldimi_probe.frozen.py" "$CL/gxemul" "$LABEL" > "$OP/rldimi_${LABEL}.log" 2>&1
grep -E 'PPC_RLDIMI_RESULT|PPC_RLDIMI_CONTROL|PPC_RLDIMI_PROBE_DONE|^FAILING' "$OP/rldimi_${LABEL}.log" | tr '\n' ' '; echo
echo "RUNPROBES_DONE $LABEL"
