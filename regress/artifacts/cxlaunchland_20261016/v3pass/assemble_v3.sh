#!/bin/bash
#  assemble_v3.sh -- the v3 pass packets for the tools/cxlaunch.sh landing: ONE token per seat (the adjudication pass's single
#  packet listed all four tokens and GLM 5.3 answered under the Fable seat's), the v2 -> v3 diffs, the receipts' result
#  lines, the records preview and the questions.  Writes packet_cxland_v3_<SEAT>.md here; refuses a section that came out empty.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
R=$(cd "$A/../../.." && pwd)
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
for f in "$H/v3_head.md" "$H/v3_tail.md" "$A/f3/v2_to_v3.udiff" "$A/run_controls_v2.sh" "$A/run_controls_v3.sh" \
         "$A/mut_launcher_v3.py" "$A/RECEIPT_v3.txt" "$A/KILLTABLE_v3.txt" "$A/f3/records_preview_OB.diff" \
         "$A/f3/records_preview_ledger.txt" "$A/f3/records_preview_rulingsC.diff"; do need "$f"; done
tail -1 "$A/RECEIPT_v3.txt" | grep -q CXLAND_CONTROLS_DONE || { echo "ASSEMBLY FAIL: RECEIPT_v3.txt has no completion sentinel"; exit 9; }
tail -1 "$A/KILLTABLE_v3.txt" | grep -q CXLAND_MUTANTS_DONE || { echo "ASSEMBLY FAIL: KILLTABLE_v3.txt has no completion sentinel"; exit 9; }
body() {
    echo
    echo "## 3. The repair, v2 -> v3"
    echo
    echo "### 3a. tools/cxlaunch.sh (\`cxlaunch_landed_v2.sh\` -> the working tree; $(grep -c '^[-+][^-+]' "$A/f3/v2_to_v3.udiff") changed lines)"
    echo
    echo '```diff'; cat "$A/f3/v2_to_v3.udiff"; echo '```'
    echo
    echo "### 3b. the controls (\`run_controls_v2.sh\` -> \`run_controls_v3.sh\`)"
    echo
    echo '```diff'; diff -u "$A/run_controls_v2.sh" "$A/run_controls_v3.sh" | sed '1,2s/\t.*//'; echo '```'
    echo
    echo "### 3c. the mutant generator, whole (\`mut_launcher_v3.py\`)"
    echo
    echo '```python'; cat "$A/mut_launcher_v3.py"; echo '```'
    echo
    echo "## 4. The receipts"
    echo
    echo "### 4a. \`RECEIPT_v3.txt\` -- its result lines (the indented per-run launcher output is omitted here; it is in the file)"
    echo
    echo '```'; grep -v '^      ' "$A/RECEIPT_v3.txt"; echo '```'
    echo
    echo "### 4b. \`KILLTABLE_v3.txt\`, whole"
    echo
    echo '```'; grep -v -e 'SyntaxWarning' -e '^  ' "$A/KILLTABLE_v3.txt"; echo '```'
    echo
    echo "## 5. The records this landing writes AT COMMIT (previews against HEAD)"
    echo
    echo "### 5a. OUTSTANDING_BUGS.md"
    echo
    echo '```diff'; cat "$A/f3/records_preview_OB.diff"; echo '```'
    echo
    echo "### 5b. the ledger rows"
    echo
    echo '```'; cat "$A/f3/records_preview_ledger.txt"; echo '```'
    echo
    echo "### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md (G9)"
    echo
    echo '```diff'; cat "$A/f3/records_preview_rulingsC.diff"; echo '```'
    echo
}
body > "$H/body.md"
grep -q '^+' "$H/body.md" || { echo "ASSEMBLY FAIL: no diff lines in the body"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
    tok="${seat}_CXLANDV3_20261016"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    { sed "s|<TOKEN_LINE>|$line|" "$H/v3_head.md"; cat "$H/body.md" "$H/v3_tail.md"; } > "$H/packet_cxland_v3_$seat.md"
    echo "packet_cxland_v3_$seat.md  $(wc -c < "$H/packet_cxland_v3_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_cxland_v3_$seat.md")"
done
