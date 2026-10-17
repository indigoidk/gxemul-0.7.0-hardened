#!/bin/bash
# assemble the cxlaunch landing pass-2 packet; refuses on a zero-hunk diff or a controls receipt without its sentinel
set -u
C=/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/cxland
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
A=$R/regress/artifacts/cxlaunchland_20261016
diff -u $A/cxlaunch_before.sh $R/tools/cxlaunch.sh > $C/production_to_landed.udiff
h=$(grep -c '^@@' $C/production_to_landed.udiff)
[ "$h" -gt 0 ] || { echo "REFUSING: 0 diff hunks"; exit 9; }
tail -1 $A/RECEIPT.txt | grep -q CXLAND_CONTROLS_DONE || { echo "REFUSING: RECEIPT.txt has no completion sentinel"; exit 9; }
OUT=$C/packet_cxland_p2.md
{
  cat $C/packet_head.md
  echo
  echo "## 4. The delta from the production copy the farm ran (\`cxlaunch_before.sh\`, md5 3c51a757) to the landed file -- \`diff -u\`, $h hunks"
  echo
  echo '```diff'
  cat $C/production_to_landed.udiff
  echo '```'
  echo
  echo "## 5. The landed \`tools/cxlaunch.sh\`, whole (the tracked file it replaces ran Astra at \`max\` with the 2026-09-07 classifier)"
  echo
  echo '```bash'
  cat $R/tools/cxlaunch.sh
  echo '```'
  echo
  echo "## 6. The controls -- \`regress/artifacts/cxlaunchland_20261016/run_controls.sh\` against a FAKE codex, RECEIPT.txt verbatim"
  echo
  echo '```'
  cat $A/RECEIPT.txt
  echo '```'
  echo
  cat $C/packet_tail.md
} > $OUT
wc -c $OUT; grep -c '^## ' $OUT
