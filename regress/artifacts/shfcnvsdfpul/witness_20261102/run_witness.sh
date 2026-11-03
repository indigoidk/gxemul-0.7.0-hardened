#!/bin/bash
# run_witness.sh -- the shfcnvsdfpul rung-3 witness against the HEAD clone binary (/tmp/gxdivw/gxemul, 987cb596).
# Output goes to the artifacts dir named on the command line (a /mnt/c path); nothing in a project tree is written.
set -u
BIN=/tmp/gxdivw/gxemul
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd
OUT=${1:-/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w576/witness_head.out}
echo "binary: $BIN  $(ls -la --time-style=+%F_%T "$BIN" | awk '{print $5, $6}')  HEADREV $(cat /tmp/gxdivw/HEADREV)" | tee "$OUT"
echo "source newer than binary? $( [ /tmp/gxdivw/src/cpus/cpu_sh_instr.c -nt "$BIN" ] && echo YES-STALE || echo no-binary-is-fresh )" | tee -a "$OUT"
cd /tmp
python3 -u /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w576/sh_fcnvsd_witness.py "$BIN" "$KERNEL" 2>&1 | tee -a "$OUT"
