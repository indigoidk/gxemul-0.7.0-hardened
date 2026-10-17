#!/bin/bash
#  assemble_v4.sh -- the v4 pass packets for the tools/cxlaunch.sh landing: ONE token per seat, the v3 -> v4 diffs (the
#  launcher's comments, the controls, the mutant list), the census, the receipts' result lines, the kill table, the records
#  previews and the CHANGELOG draft.  Writes packet_cxland_v4_<SEAT>.md here; refuses an empty section or a missing sentinel.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
for f in "$H/v4_head.md" "$H/v4_tail.md" "$H/launcher_v3_to_v4.udiff" "$H/controls_v3_to_v4.udiff" "$H/mutants_v3_to_v4.udiff" \
         "$A/CENSUS_v4.txt" "$A/RECEIPT_v4.txt" "$A/KILLTABLE_v4.txt" "$A/f3/records_preview_OB.diff" \
         "$A/f3/records_preview_ledger.txt" "$A/f3/records_preview_rulingsC.diff" "$A/f3/changelog_block_draft.md"; do need "$f"; done
tail -1 "$A/RECEIPT_v4.txt" | grep -q CXLAND_CONTROLS_DONE || { echo "ASSEMBLY FAIL: RECEIPT_v4.txt has no sentinel"; exit 9; }
tail -1 "$A/KILLTABLE_v4.txt" | grep -q CXLAND_MUTANTS_DONE || { echo "ASSEMBLY FAIL: KILLTABLE_v4.txt has no sentinel"; exit 9; }
tail -1 "$A/CENSUS_v4.txt" | grep -q CENSUS_V4_DONE || { echo "ASSEMBLY FAIL: CENSUS_v4.txt has no sentinel"; exit 9; }
body() {
    echo
    echo "## 3. The repair, v3 -> v4"
    echo
    echo "### 3a. tools/cxlaunch.sh -- comments only ($(grep -c '^[-+][^-+]' "$H/launcher_v3_to_v4.udiff") changed lines)"
    echo
    echo '```diff'; cat "$H/launcher_v3_to_v4.udiff"; echo '```'
    echo
    echo "### 3b. the controls, \`run_controls_v3.sh\` -> \`run_controls_v4.sh\` (the CONTRACT is in the header)"
    echo
    echo '```diff'; cat "$H/controls_v3_to_v4.udiff"; echo '```'
    echo
    echo "### 3c. the mutant list, \`mut_launcher_v3.py\` -> \`mut_launcher_v4.py\`"
    echo
    echo '```diff'; cat "$H/mutants_v3_to_v4.udiff"; echo '```'
    echo
    echo "### 3d. \`CENSUS_v4.txt\` (\`census_v4.py\`)"
    echo
    echo '```'; cat "$A/CENSUS_v4.txt"; echo '```'
    echo
    echo "## 4. The receipts"
    echo
    echo "### 4a. \`RECEIPT_v4.txt\` -- its result lines (the indented per-run launcher output is omitted; it is in the file)"
    echo
    echo '```'; grep -v '^      ' "$A/RECEIPT_v4.txt"; echo '```'
    echo
    echo "### 4b. \`KILLTABLE_v4.txt\`, whole"
    echo
    echo '```'; grep -v -e 'SyntaxWarning' -e '^  ' "$A/KILLTABLE_v4.txt"; echo '```'
    echo
    echo "## 5. The records this landing writes AT COMMIT (previews against HEAD 8bf8b5a1)"
    echo
    echo "### 5a. OUTSTANDING_BUGS.md"
    echo
    echo '```diff'; cat "$A/f3/records_preview_OB.diff"; echo '```'
    echo
    echo "### 5b. the ledger rows"
    echo
    echo '```'; cat "$A/f3/records_preview_ledger.txt"; echo '```'
    echo
    echo "### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md (V12)"
    echo
    echo '```diff'; cat "$A/f3/records_preview_rulingsC.diff"; echo '```'
    echo
    echo "### 5d. the CHANGELOG block (a DRAFT: its v4-pass sentence is written from this pass's answers)"
    echo
    cat "$A/f3/changelog_block_draft.md"
    echo
}
body > "$H/body.md"
grep -q '^+' "$H/body.md" || { echo "ASSEMBLY FAIL: no diff lines in the body"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
    tok="${seat}_CXLANDV4_20261017"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    { sed "s|<TOKEN_LINE>|$line|" "$H/v4_head.md"; cat "$H/body.md" "$H/v4_tail.md"; } > "$H/packet_cxland_v4_$seat.md"
    echo "packet_cxland_v4_$seat.md  $(wc -c < "$H/packet_cxland_v4_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_cxland_v4_$seat.md")"
done
