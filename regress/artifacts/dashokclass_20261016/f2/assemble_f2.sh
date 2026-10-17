#!/bin/bash
# assemble the dashokclass adjudication (§F2) packets -- one per seat token, so a packet-fed seat sees ONLY its own token
# (GLM 5.3 answered two earlier packets under the Fable seat's token).  Refuses on a zero-hunk diff or a missing sentinel.
set -u
R=/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC
D=$R/regress/artifacts/dashokclass_20261016
P=$D/f2
cd $R
git diff --no-index -- $D/staged/tools/pipeline/check_entry_domain.py $D/staged_v2/tools/pipeline/check_entry_domain.py > $P/checker_v1v2.diff
git diff --no-index -- $D/staged/tools/pipeline/gen_dashboard.py $D/staged_v2/tools/pipeline/gen_dashboard.py > $P/renderer_v1v2.diff
git diff --no-index -- $D/staged/tools/precommit_check.sh $D/staged_v2/tools/precommit_check.sh > $P/precommit_v1v2.diff
for f in checker_v1v2 renderer_v1v2 precommit_v1v2; do h=$(grep -c '^@@' $P/$f.diff); [ "$h" -gt 0 ] || { echo "REFUSING: 0 hunks in $f"; exit 9; }; done
tail -1 $D/RECEIPT_v2_staged.txt | grep -q DASHOKCLASS_CONTROLS_DONE || { echo "REFUSING: receipt sentinel"; exit 9; }
tail -1 $D/KILLTABLE_staged.txt | grep -q DASHOKCLASS_MUTANTS_DONE || { echo "REFUSING: kill table sentinel"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
  OUT=$P/packet_dashok_f2_$seat.md
  {
    sed "s/<TOKEN_LINE>/Open with your seat token \`${seat}_DASHOKF2_20261016\`, then ONE line: \`VERDICT: SHIP \/ SHIP WITH CHANGES (<n>) \/ DO NOT SHIP (<one line>)\`./" $P/f2_head.md
    echo
    echo "## 4. The repair -- v1 (pass 2) -> v2, \`git diff --no-index\` of the staged files"
    echo
    echo "### 4a. check_entry_domain.py"; echo; echo '```diff'; cat $P/checker_v1v2.diff; echo '```'; echo
    echo "### 4b. gen_dashboard.py"; echo; echo '```diff'; cat $P/renderer_v1v2.diff; echo '```'; echo
    echo "### 4c. precommit_check.sh, section Q2"; echo; echo '```diff'; cat $P/precommit_v1v2.diff; echo '```'; echo
    echo "## 5. The receipts -- run in a staging copy of HEAD 8bf8b5a1 with the v2 files in place"
    echo
    echo "### 5a. RECEIPT_v2_staged.txt (run_controls_v2.py), verbatim"; echo; echo '```'; cat $D/RECEIPT_v2_staged.txt; echo '```'; echo
    echo "### 5b. KILLTABLE_staged.txt (run_mutants.py), verbatim"; echo; echo '```'; cat $D/KILLTABLE_staged.txt; echo '```'; echo
    cat $P/f2_tail.md
  } > $OUT
  printf '%s %s bytes\n' "$seat" "$(wc -c < $OUT)"
done
