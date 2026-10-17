#!/bin/bash
# assemble the launcher's adjudication (§F2) packet; refuses on a zero-hunk diff or a receipt/kill table without its sentinel
set -u
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
A=$R/regress/artifacts/cxlaunchland_20261016
P=$A/f2
diff -u $A/cxlaunch_landed_v1.sh $R/tools/cxlaunch.sh > $P/v1_to_v2.udiff
h=$(grep -c '^@@' $P/v1_to_v2.udiff); [ "$h" -gt 0 ] || { echo "REFUSING: 0 hunks"; exit 9; }
tail -1 $A/RECEIPT_v2.txt | grep -q CXLAND_CONTROLS_DONE || { echo "REFUSING: RECEIPT_v2.txt has no sentinel"; exit 9; }
tail -1 $A/KILLTABLE.txt | grep -q CXLAND_MUTANTS_DONE || { echo "REFUSING: KILLTABLE.txt has no sentinel"; exit 9; }
OUT=$P/packet_cxland_f2.md
{
  cat $P/f2_head.md
  echo
  echo "## 4. The repair -- \`diff -u\` of the pass-2 launcher (v1, md5 47d47097) against the working-tree \`tools/cxlaunch.sh\` (v2, md5 $(md5sum < $R/tools/cxlaunch.sh | cut -c1-8)), $h hunks"
  echo
  echo '```diff'; cat $P/v1_to_v2.udiff; echo '```'
  echo
  echo "### 4a. The v2 controls driver, whole (\`run_controls_v2.sh\`; the tracked column is the PRE-FIX file, run through a scratch \$HOME)"
  echo
  echo '```bash'; cat $A/run_controls_v2.sh; echo '```'
  echo
  echo "### 4b. RECEIPT_v2.txt -- every exit line and every content check (the launchers' own log lines are in the file)"
  echo
  echo '```'; grep -E '^# |^[A-Z][0-9A-Z]? +(tracked|before|after) +exit=|^[A-Z][0-9]? +(after|all) |^CONTROLS:|^CXLAND' $A/RECEIPT_v2.txt; echo '```'
  echo
  echo "### 4c. KILLTABLE.txt -- \`run_mutants.sh\` over \`mut_launcher.py\`'s one-edit mutants of v2"
  echo
  echo '```'; grep -v -e 'SyntaxWarning' -e '^  """' -e '^  (' $A/KILLTABLE.txt; echo '```'
  echo
  cat $P/f2_tail.md
} > $OUT
wc -c $OUT; grep -c '^## \|^### ' $OUT
