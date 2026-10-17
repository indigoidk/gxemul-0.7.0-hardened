#!/bin/bash
# assemble the dashokclass pass-2 packet; refuses on a zero-hunk diff or a receipt without its completion sentinel
set -u
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
D=$R/regress/artifacts/dashokclass_20261016
P=$D/pass2
cd $R
git diff --no-index -- tools/pipeline/gen_dashboard.py $D/staged/tools/pipeline/gen_dashboard.py > $P/renderer.diff
git diff --no-index -- tools/precommit_check.sh $D/staged/tools/precommit_check.sh > $P/precommit.diff
for f in renderer precommit; do h=$(grep -c '^@@' $P/$f.diff); [ "$h" -gt 0 ] || { echo "REFUSING: 0 hunks in $f.diff"; exit 9; }; done
tail -1 $D/RECEIPT_staged.txt | grep -q DASHOKCLASS_CONTROLS_DONE || { echo "REFUSING: RECEIPT_staged.txt has no completion sentinel"; exit 9; }
OUT=$P/packet_dashok_p2.md
{
  cat $P/packet_head.md
  echo
  echo "## 4. The renderer -- \`git diff\` of \`tools/pipeline/gen_dashboard.py\` (HEAD) against the staged copy ($(grep -c '^@@' $P/renderer.diff) hunks)"
  echo
  echo '```diff'; cat $P/renderer.diff; echo '```'
  echo
  echo "## 5. The checker -- \`tools/pipeline/check_entry_domain.py\` (new), whole"
  echo
  echo '```python'; cat $D/staged/tools/pipeline/check_entry_domain.py; echo '```'
  echo
  echo "## 6. The precommit wiring -- \`git diff\` of \`tools/precommit_check.sh\` (HEAD) against the staged copy"
  echo
  echo '```diff'; cat $P/precommit.diff; echo '```'
  echo
  echo "## 7. The controls -- \`regress/artifacts/dashokclass_20261016/run_controls.py\`, run in a staging copy of the tree (RECEIPT_staged.txt verbatim)"
  echo
  echo "The baseline writer is \`write_baseline.py\` beside it (one-time; the checker never runs it); the first lines of the baseline:"
  echo
  echo '```'; head -4 $D/staged/tools/pipeline/entry_domain_baseline.json; echo "... ($(wc -l < $D/staged/tools/pipeline/entry_domain_baseline.json) lines)"; echo '```'
  echo
  echo '```'; cat $D/RECEIPT_staged.txt; echo '```'
  echo
  cat $P/packet_tail.md
} > $OUT
wc -c $OUT; grep -c '^## ' $OUT
