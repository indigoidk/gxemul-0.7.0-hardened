#!/bin/bash
# assemble the pass-14 packet from its parts; refuses if the diff carries zero hunks (the git-show-head trap)
set -u
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
D=$R/regress/artifacts/m88kexcdeliver/repair13_20261016
P=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/m88kv20
OUT=$D/pass14/packet_m88k_p14.md
git -C $R diff -- regress/m88k_exc_probe.py regress/gate_m88k_rounding.sh > $D/pass14/repair13_probe_gate.diff
h=$(grep -c '^@@' $D/pass14/repair13_probe_gate.diff)
[ "$h" -gt 0 ] || { echo "REFUSING: 0 diff hunks"; exit 9; }
{
  cat $D/pass14/packet_head.md
  echo
  echo "## 3. The repair -- \`git diff\` of the probe and the gate against HEAD 7b23b785 ($h hunks)"
  echo
  echo "The records-only deriver change (\`regress/artifacts/m88kexcdeliver/derive_cells.py\`, +48/-4) is NOT inlined; its new"
  echo "delay-slot output is in section 4.  File-reading seats: \`git diff -- regress/artifacts/m88kexcdeliver/derive_cells.py\`."
  echo
  echo '```diff'
  cat $D/pass14/repair13_probe_gate.diff
  echo '```'
  echo
  echo "## 4. Tables 16 and 16b (measured; logs t16_*.out / t16b_*.out in repair13_20261016/)"
  echo
  echo "Table 16 ran the v20 probe as frozen BEFORE the records edits (\`m88k_exc_probe_v20.FROZEN.py\`); table 16b ran the"
  echo "committed form (\`m88k_exc_probe_v20final.FROZEN.py\`: the same plus two asserts and comments).  \"true red set\" lists"
  echo "the rows whose RESULT differs from what the probe expects (eight rows expect HALT by design)."
  echo
  echo '```'
  cat $D/ANALYSIS.out
  echo
  sed -n '/DELAY-SLOT axis -- v20/,/^closed/p' $R/regress/artifacts/m88kexcdeliver/CELLCENSUS.out | tr -d '\r'
  echo '```'
  echo
  echo "## 5. The enclosing function -- \`m88k_exception()\`, \`src/cpus/cpu_m88k.c\` at HEAD (lines 689-981, unchanged by this repair)"
  echo
  echo '```c'
  cat $P/m88k_exception_HEAD.txt
  echo '```'
  echo
  cat $D/pass14/packet_tail.md
} > $OUT
wc -c $OUT; grep -c '^@@' $OUT
