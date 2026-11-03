#!/bin/bash
# run_probe_leg.sh <binary> <label> -- one leg of the #576 table: the extended probe against one scratch binary.
# Output: /mnt/c/.../w576/killtable_20261102/<label>.raw (full probe output + a header naming the binary and its freshness).
set -u
BIN=$1; LABEL=$2
OUT=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w576/killtable_20261102/$LABEL.raw
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd
PROBE=/mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w576/sh_rounding_probe.NEW.py
SRC=$(dirname "$BIN")/src/cpus/cpu_sh_instr.c
{ echo "LEG $LABEL binary=$BIN $(ls -la --time-style=+%F_%T "$BIN" | awk '{print $5, $6}') md5=$(md5sum "$BIN" | cut -c1-12)";
  echo "binary newer than cpu_sh_instr.c: $( [ "$BIN" -nt "$SRC" ] && echo yes || echo NO-STALE )";
  echo "sentinel: $(cat "$(dirname "$BIN")/.MUTANT" 2>/dev/null || echo none)"; } > "$OUT"
cd /tmp && python3 -u "$PROBE" "$BIN" "$KERNEL" >> "$OUT" 2>&1
echo "LEG_DONE $LABEL $(grep -E '^SH_ROUND_RESULT=' "$OUT")" | tee -a "$OUT"
