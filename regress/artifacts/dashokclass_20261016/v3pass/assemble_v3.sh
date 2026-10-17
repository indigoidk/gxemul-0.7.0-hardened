#!/bin/bash
#  assemble_v3.sh -- the v3 pass packets for `dashokclass`: ONE token per seat, the staged v2 -> v3 diff, the v3 controls'
#  docstring, the receipts, the kill table, the records previews and the CHANGELOG draft.  Writes packet_dashok_v3_<SEAT>.md
#  here; refuses a section that came out empty or a receipt without its completion sentinel.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
for f in "$H/v3_head.md" "$H/v3_tail.md" "$H/staged_v2_to_v3.udiff" "$A/run_controls_v3.py" "$A/run_mutants_v3.py" \
         "$A/RECEIPT_v3_on_staged_v3.txt" "$A/RECEIPT_v3_on_staged_v2.txt" "$A/KILLTABLE_v3_staged.txt" \
         "$A/f3/records_preview_OB.diff" "$A/f3/records_preview_ledger.txt" "$A/f3/records_preview_rulingsC.diff" \
         "$A/f3/changelog_block_draft.md" "$A/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt"; do need "$f"; done
grep -q 'DASHOKCLASS_CONTROLS_DONE' "$A/RECEIPT_v3_on_staged_v3.txt" || { echo "ASSEMBLY FAIL: no sentinel in the v3 receipt"; exit 9; }
grep -q 'DASHOKCLASS_MUTANTS_DONE' "$A/KILLTABLE_v3_staged.txt" || { echo "ASSEMBLY FAIL: no sentinel in the kill table"; exit 9; }
body() {
    echo
    echo "## 3. The repair, staged v2 -> v3 ($(grep -c '^[-+][^-+]' "$H/staged_v2_to_v3.udiff") changed lines across the checker, the renderer and precommit Q2)"
    echo
    echo '```diff'; cat "$H/staged_v2_to_v3.udiff"; echo '```'
    echo
    echo "## 4. The controls and their receipts"
    echo
    echo "### 4a. what each of the 46 controls asserts (the docstring of \`run_controls_v3.py\`)"
    echo
    echo '```'; sed -n '/^"""Controls/,/^"""$/p' "$A/run_controls_v3.py"; echo '```'
    echo
    echo "### 4b. \`RECEIPT_v3_on_staged_v3.txt\` (the v3 files), whole"
    echo
    echo '```'; cat "$A/RECEIPT_v3_on_staged_v3.txt"; echo '```'
    echo
    echo "### 4c. \`RECEIPT_v3_on_staged_v2.txt\` (the v2 files, the pre-repair column) -- the tally and the red rows"
    echo
    echo '```'; head -1 "$A/RECEIPT_v3_on_staged_v2.txt"; grep -E '  NO  ' "$A/RECEIPT_v3_on_staged_v2.txt" | cut -c1-140; tail -2 "$A/RECEIPT_v3_on_staged_v2.txt"; echo '```'
    echo
    echo "### 4d. the kill table: the mutants (\`run_mutants_v3.py\`'s list) and \`KILLTABLE_v3_staged.txt\`"
    echo
    echo '```python'; sed -n '/^MUTANTS = \[/,/^\]$/p' "$A/run_mutants_v3.py"; echo '```'
    echo
    echo '```'; grep -v '^#   ' "$A/KILLTABLE_v3_staged.txt"; echo '```'
    echo
    echo "### 4e. \`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt\` (H14)"
    echo
    echo '```'; cat "$A/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt"; echo '```'
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
    echo "### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md (H12)"
    echo
    echo '```diff'; cat "$A/f3/records_preview_rulingsC.diff"; echo '```'
    echo
    echo "### 5d. the CHANGELOG block (a DRAFT: its v3-pass sentence is written from this pass's answers)"
    echo
    cat "$A/f3/changelog_block_draft.md"
    echo
}
body > "$H/body.md"
grep -q '^+' "$H/body.md" || { echo "ASSEMBLY FAIL: no diff lines in the body"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
    tok="${seat}_DASHOKV3_20261017"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    { sed "s|<TOKEN_LINE>|$line|" "$H/v3_head.md"; cat "$H/body.md" "$H/v3_tail.md"; } > "$H/packet_dashok_v3_$seat.md"
    echo "packet_dashok_v3_$seat.md  $(wc -c < "$H/packet_dashok_v3_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_dashok_v3_$seat.md")"
done
