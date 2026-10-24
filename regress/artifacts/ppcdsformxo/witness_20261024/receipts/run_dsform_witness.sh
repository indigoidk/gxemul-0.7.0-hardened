#!/bin/bash
#  T2 (#571) rung-3 witness run: ppc_dsform_probe.py once against the baseline binary.
#  Foreground, no background jobs.  Writes only into the witness artifacts directory.
set -u
D=/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/ppcdsformxo/witness_20261024
BIN=/tmp/gxt2/base/gxemul
cd "$D" || { echo "NO_ARTIFACTS_DIR"; exit 9; }
echo "=== $(date '+%F %T') binary"
ls -la --time-style=full-iso "$BIN" /tmp/gxt2/base/src/cpus/cpu_ppc_instr.c
md5sum "$BIN" /tmp/gxt2/base/src/cpus/cpu_ppc_instr.c
[ "$BIN" -nt /tmp/gxt2/base/src/cpus/cpu_ppc_instr.c ] && echo "FRESH: gxemul -nt cpu_ppc_instr.c" || echo "STALE_OR_MISSING"
[ -e /tmp/gxt2/base/.MUTANT ] && echo "MUTANT_SENTINEL_PRESENT" || echo "no .MUTANT sentinel in /tmp/gxt2/base"
echo "=== $(date '+%F %T') run (foreground)"
python3 -u "$D/ppc_dsform_probe.py" "$BIN" headbin "$D" > "$D/WITNESS_headbin.out" 2>&1
RC=$?
echo "PROBE_RC=$RC"
echo "=== $(date '+%F %T') output tail"
tail -n 7 "$D/WITNESS_headbin.out"
echo "=== files"
ls -la "$D"
echo "RUN_DONE"
