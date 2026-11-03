#!/bin/bash
# run_witness577.sh <binary> <out> -- the shblreset rung-3 witness against one scratch binary (WSL).  Writes only <out>.
set -u
BIN=$1; OUT=$2
KERNEL=/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd
SRC=$(dirname "$BIN")/src/cpus/cpu_sh.c
{ echo "binary: $BIN $(ls -la --time-style=+%F_%T "$BIN" | awk '{print $5, $6}') md5=$(md5sum "$BIN" | cut -c1-12) HEADREV $(cat "$(dirname "$BIN")/HEADREV" 2>/dev/null)";
  echo "binary newer than cpu_sh.c: $( [ "$BIN" -nt "$SRC" ] && echo yes || echo NO-STALE )";
  echo "sentinel: $(cat "$(dirname "$BIN")/.MUTANT" 2>/dev/null || echo none)"; } > "$OUT"
cd /tmp && python3 -u /mnt/c/DocumentNoSnc/CC/GXEMUL/_scratchpad/w577/sh_blreset_witness.py "$BIN" "$KERNEL" >> "$OUT" 2>&1
tail -3 "$OUT"
