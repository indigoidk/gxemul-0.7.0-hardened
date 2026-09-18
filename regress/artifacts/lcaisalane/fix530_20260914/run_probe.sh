#!/bin/sh
#  #530 lcaisalane: run the shipped probe (from a FROZEN copy) against a named binary.
#  usage: run_probe.sh <label> <binary> [probe]   -> $W/<label>.out, meta in $W/<label>.meta
#  READ-ONLY against every build tree.  The .out ends in the probe's own LCAISALANE_DONE sentinel;
#  the clearance and exit status go to the .meta, never after the sentinel.
set -u
W=/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/lcaisalane/fix530_20260914
L=$1; BIN=$2
SRC=${3:-/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/lca_isalane_probe.py}
P=$W/lca_isalane_probe.$L.asrun.py
cp "$SRC" "$P"
cp /mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/alpha_dummy.bin "$W/alpha_dummy.bin" 2>/dev/null || true
{
  echo "label=$L binary=$BIN probe=$SRC (frozen $P)"
  ls -la --time-style=full-iso "$BIN"
  md5sum "$P" "$SRC"
  date
} > "$W/$L.meta" 2>&1
cd "$W"
LCAISALANE_RAW= python3 -u "$P" "$BIN" "$L" > "$W/$L.out" 2>&1
echo "EXIT=$?" >> "$W/$L.meta"
date >> "$W/$L.meta"
