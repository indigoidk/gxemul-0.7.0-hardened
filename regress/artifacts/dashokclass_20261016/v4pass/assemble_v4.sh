#!/bin/bash
#  assemble_v4.sh -- the v4 pass packets for `dashokclass`: ONE token per seat, the staged v3 -> v4 diff, the v4 controls'
#  CONTRACT (their docstring), the receipts, the kill table, the records previews and the CHANGELOG draft.  Writes
#  packet_dashok_v4_<SEAT>.md here; refuses a section that came out empty or a receipt without its completion sentinel.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
for f in "$H/v4_head.md" "$H/v4_tail.md" "$H/staged_v3_to_v4.udiff" "$A/run_controls_v4.py" "$A/run_mutants_v4.py" \
         "$A/RECEIPT_v4_on_staged_v4.txt" "$A/RECEIPT_v4_on_staged_v3.txt" "$A/KILLTABLE_v4_staged.txt" \
         "$A/f3/records_preview_OB.diff" "$A/f3/records_preview_ledger.txt" "$A/f3/records_preview_rulingsC.diff" \
         "$A/f3/changelog_block_draft.md"; do need "$f"; done
grep -q 'DASHOKCLASS_CONTROLS_DONE' "$A/RECEIPT_v4_on_staged_v4.txt" || { echo "ASSEMBLY FAIL: no sentinel in the v4 receipt"; exit 9; }
grep -q 'DASHOKCLASS_MUTANTS_DONE' "$A/KILLTABLE_v4_staged.txt" || { echo "ASSEMBLY FAIL: no sentinel in the kill table"; exit 9; }
body() {
    echo
    echo "## 3. The repair, staged v3 -> v4 ($(grep -c '^[-+][^-+]' "$H/staged_v3_to_v4.udiff") changed lines; the checker's shape check is the only code change)"
    echo
    echo '```diff'; cat "$H/staged_v3_to_v4.udiff"; echo '```'
    echo
    echo "## 4. The controls and their receipts"
    echo
    echo "### 4a. the CONTRACT and the 72 controls -- the docstring of \`run_controls_v4.py\`"
    echo
    echo '```'; sed -n '/^"""Controls/,/^"""$/p' "$A/run_controls_v4.py"; echo '```'
    echo
    echo "### 4b. \`RECEIPT_v4_on_staged_v4.txt\`, whole"
    echo
    echo '```'; cat "$A/RECEIPT_v4_on_staged_v4.txt"; echo '```'
    echo
    echo "### 4c. \`RECEIPT_v4_on_staged_v3.txt\` (the v3 files, the pre-repair column) -- the tally and the red rows"
    echo
    echo '```'; head -1 "$A/RECEIPT_v4_on_staged_v3.txt"; grep -E '  NO  ' "$A/RECEIPT_v4_on_staged_v3.txt" | cut -c1-140; tail -2 "$A/RECEIPT_v4_on_staged_v3.txt"; echo '```'
    echo
    echo "### 4d. \`KILLTABLE_v4_staged.txt\` (the mutant list is \`run_mutants_v4.py\`'s MUTANTS)"
    echo
    echo '```'; grep -v '^#   ' "$A/KILLTABLE_v4_staged.txt"; echo '```'
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
    echo "### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md"
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
    tok="${seat}_DASHOKV4_20261017"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    { sed "s|<TOKEN_LINE>|$line|" "$H/v4_head.md"; cat "$H/body.md" "$H/v4_tail.md"; } > "$H/packet_dashok_v4_$seat.md"
    echo "packet_dashok_v4_$seat.md  $(wc -c < "$H/packet_dashok_v4_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_dashok_v4_$seat.md")"
done
