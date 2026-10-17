#!/bin/bash
# assemble the pass-16 packet; refuses on a zero-hunk diff (the git-show-head trap) or a missing table analysis
set -u
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
D=$R/regress/artifacts/m88kexcdeliver/repair13_20261016
P=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kv20
OUT=$D/pass16/packet_m88k_p16.md
git -C $R diff -- regress/m88k_exc_probe.py regress/gate_m88k_rounding.sh > $D/pass16/v23_to_v24.diff
h=$(grep -c '^@@' $D/pass16/v23_to_v24.diff)
[ "$h" -gt 0 ] || { echo "REFUSING: 0 diff hunks"; exit 9; }
[ -s $D/ANALYSIS_20.out ] && [ -s $D/ANALYSIS_20b.out ] || { echo "REFUSING: no ANALYSIS_20/20b"; exit 9; }
{
  cat $D/pass16/packet_head.md
  echo
  echo "## 3. Table 20 (measured; PRETABLE_20.out written first, in its own file)"
  echo
  echo "\"red\" lists the rows whose RESULT differs from what the probe expects (ten v24 rows expect HALT by design)."
  echo
  echo '```'
  cat $D/ANALYSIS_20.out
  echo '```'
  echo
  echo "Table 20b, the corrected v24 (trapfrozen9dslot at br.n +16), the mutants that touch that row (PRETABLE_20b.out):"
  echo
  echo '```'
  cat $D/ANALYSIS_20b.out
  echo '```'
  echo
  echo "## 4. The grid, printed by \`regress/artifacts/m88kexcdeliver/derive_cells.py\` from its (hand-transcribed) row table"
  echo
  echo '```'
  sed -n '/x is_trap GRID -- v24/,$p' $R/regress/artifacts/m88kexcdeliver/CELLCENSUS.out | tr -d '\r'
  echo '```'
  echo
  echo "## 5. The repair -- \`git diff\` of the probe and gate 11 against HEAD c64445fa (v23) ($h hunks)"
  echo
  echo '```diff'
  cat $D/pass16/v23_to_v24.diff
  echo '```'
  echo
  echo "## 6. The enclosing function -- \`m88k_exception()\`, \`src/cpus/cpu_m88k.c\` at HEAD (lines 689-981, unchanged)"
  echo
  echo '```c'
  cat $P/m88k_exception_HEAD.txt
  echo '```'
  echo
  cat $D/pass16/packet_tail.md
} > $OUT
wc -c $OUT; grep -c '^## ' $OUT
