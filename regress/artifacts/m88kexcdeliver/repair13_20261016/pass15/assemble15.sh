#!/bin/bash
# assemble the pass-15 packet; refuses on a zero-hunk diff (the git-show-head trap) or a missing table analysis
set -u
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
D=$R/regress/artifacts/m88kexcdeliver/repair13_20261016
P=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kv20
OUT=$D/pass15/packet_m88k_p15.md
git -C $R diff --no-index -- $P/snap_v22/m88k_exc_probe.py $R/regress/m88k_exc_probe.py > $D/pass15/v22_to_v23_probe.diff
git -C $R diff --no-index -- $P/snap_v22/gate_m88k_rounding.sh $R/regress/gate_m88k_rounding.sh > $D/pass15/v22_to_v23_gate.diff
h=$(cat $D/pass15/v22_to_v23_probe.diff $D/pass15/v22_to_v23_gate.diff | grep -c '^@@')
[ "$h" -gt 0 ] || { echo "REFUSING: 0 diff hunks"; exit 9; }
[ -s $D/ANALYSIS_19.out ] || { echo "REFUSING: no ANALYSIS_19.out"; exit 9; }
{
  cat $D/pass15/packet_head.md
  echo
  echo "## 4. Tables 19 and 19b (measured; PRETABLE_19.out / PRETABLE_19b.out written first, each in its own file)"
  echo
  echo "\"red\" lists the rows whose RESULT differs from what the probe expects (eight rows -- nine in v23 -- expect HALT by design)."
  echo
  echo '```'
  cat $D/ANALYSIS_19.out
  echo '```'
  echo
  echo "The delay-slot grid, printed by \`regress/artifacts/m88kexcdeliver/derive_cells.py\` from the row definitions"
  echo "(\`CELLCENSUS.out\`; a cell shows its first row alphabetically, +N more):"
  echo
  echo '```'
  sed -n '/DELAY-SLOT GRID -- v23/,$p' $R/regress/artifacts/m88kexcdeliver/CELLCENSUS.out | tr -d '\r'
  echo '```'
  echo
  echo "## 5. The repair -- v22 -> v23 ($h hunks: the probe, then gate 11)"
  echo
  echo "v22 (repair 13: the four \`dslot*\` rows, the asserts, the records) was reviewed by pass 14 and is NOT re-inlined.  The"
  echo "whole uncommitted change against HEAD, for file-reading seats:"
  echo "\`git -C C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC diff -- regress/m88k_exc_probe.py regress/gate_m88k_rounding.sh\`."
  echo
  echo '```diff'
  cat $D/pass15/v22_to_v23_probe.diff $D/pass15/v22_to_v23_gate.diff
  echo '```'
  echo
  echo "## 6. The enclosing function -- \`m88k_exception()\`, \`src/cpus/cpu_m88k.c\` at HEAD (lines 689-981, unchanged)"
  echo
  echo '```c'
  cat $P/m88k_exception_HEAD.txt
  echo '```'
  echo
  cat $D/pass15/packet_tail.md
} > $OUT
wc -c $OUT; grep -c '^## ' $OUT
