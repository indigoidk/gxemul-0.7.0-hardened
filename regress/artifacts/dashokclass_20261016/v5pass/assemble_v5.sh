#!/bin/bash
#  assemble_v5.sh -- the v5 pass packets for `dashokclass`: ONE token per seat, the staged v4 -> v5 diff (two title lines), the
#  staged checker WHOLE, the renderer's diff against HEAD and the Q2 block, the v5 controls WHOLE (their docstring is the
#  CONTRACT), the receipt, the kill table, the census, the records previews and the CHANGELOG draft.  Writes
#  packet_dashok_v5_<SEAT>.md here; refuses a section that came out empty or an artifact without its completion sentinel.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
for f in "$H/v5_head.md" "$H/v5_tail.md" "$H/staged_v4_to_v5.udiff" "$A/staged_v5/tools/pipeline/check_entry_domain.py" \
         "$A/staged_v5/tools/pipeline/gen_dashboard.py" "$A/gen_dashboard_before.py" "$A/staged_v5/tools/precommit_check.sh" \
         "$A/run_controls_v5.py" "$A/run_mutants_v5.py" "$A/RECEIPT_v5_on_staged_v5.txt" "$A/KILLTABLE_v5_staged.txt" \
         "$A/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt" "$A/f3/records_preview_OB.diff" "$A/f3/records_preview_ledger.txt" \
         "$A/f3/records_preview_rulingsC.diff" "$A/f3/changelog_block_draft.md"; do need "$f"; done
grep -q 'DASHOKCLASS_CONTROLS_DONE' "$A/RECEIPT_v5_on_staged_v5.txt" || { echo "ASSEMBLY FAIL: no sentinel in the v5 receipt"; exit 9; }
grep -q 'DASHOKCLASS_MUTANTS_DONE' "$A/KILLTABLE_v5_staged.txt" || { echo "ASSEMBLY FAIL: no sentinel in the kill table"; exit 9; }
grep -q 'DASHMISSINGD_CENSUS_DONE' "$A/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt" || { echo "ASSEMBLY FAIL: no sentinel in the census"; exit 9; }
diff -u --label gen_dashboard.py@HEAD --label gen_dashboard.py@staged_v5 "$A/gen_dashboard_before.py" "$A/staged_v5/tools/pipeline/gen_dashboard.py" > "$H/render_head_to_v5.udiff"
need "$H/render_head_to_v5.udiff"
body() {
    echo
    echo "## 3. The repair, staged v4 -> v5 ($(grep -c '^[-+][^-+]' "$H/staged_v4_to_v5.udiff") changed lines: two title lines; no code)"
    echo
    echo '```diff'; cat "$H/staged_v4_to_v5.udiff"; echo '```'
    echo
    echo "### 3a. the staged checker, \`staged_v5/tools/pipeline/check_entry_domain.py\`, WHOLE"
    echo
    echo '```python'; cat -n "$A/staged_v5/tools/pipeline/check_entry_domain.py"; echo '```'
    echo
    echo "### 3b. the renderer change, \`gen_dashboard.py\` HEAD -> staged v5 ($(grep -c '^[-+][^-+]' "$H/render_head_to_v5.udiff") changed lines)"
    echo
    echo '```diff'; cat "$H/render_head_to_v5.udiff"; echo '```'
    echo
    echo "### 3c. precommit section Q2, as staged"
    echo
    echo '```bash'; sed -n '/^#  ---- Q2 ---/,/^#  ---- R ---/p' "$A/staged_v5/tools/precommit_check.sh"; echo '```'
    echo
    echo "## 4. The controls and their receipts"
    echo
    echo "### 4a. \`run_controls_v5.py\`, WHOLE (its docstring is the CONTRACT and the row list)"
    echo
    echo '```python'; cat -n "$A/run_controls_v5.py"; echo '```'
    echo
    echo "### 4b. \`RECEIPT_v5_on_staged_v5.txt\`, whole"
    echo
    echo '```'; cat "$A/RECEIPT_v5_on_staged_v5.txt"; echo '```'
    echo
    echo "### 4c. \`KILLTABLE_v5_staged.txt\` (the mutants are \`run_mutants_v5.py\`'s MUTANTS; the v5 additions follow)"
    echo
    echo '```'; grep -v '^#   ' "$A/KILLTABLE_v5_staged.txt"; echo '```'
    echo
    echo '```python'; sed -n '/#  v5 -- the v4 pass/,/^]$/p' "$A/run_mutants_v5.py"; echo '```'
    echo
    echo "### 4d. \`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt\` (\`dashmissingd_census.py\` on HEAD's ledger; v5 adds the NOT-FIRED screen)"
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
    echo "### 5c. regress/artifacts/adj_20261016/RULINGS_C_records.md"
    echo
    echo '```diff'; cat "$A/f3/records_preview_rulingsC.diff"; echo '```'
    echo
    echo "### 5d. the CHANGELOG block (a DRAFT: its v5-pass sentence is written from this pass's answers)"
    echo
    cat "$A/f3/changelog_block_draft.md"
    echo
}
body > "$H/body.md"
grep -q '^+' "$H/body.md" || { echo "ASSEMBLY FAIL: no diff lines in the body"; exit 9; }
#  the PACKET-FED seat (GLM) gets a narrower body: the controls' docstring (the CONTRACT and the row list) instead of their
#  whole code, and no records previews -- the three file-reading seats review those (a 160 KB packet risks a thinking burn)
sed -n '/^"""Controls/,/^"""$/p' "$A/run_controls_v5.py" > "$H/doc.txt"
need "$H/doc.txt"
awk '/^### 4a\./ { skip = 1; print "### 4a. the CONTRACT and the 96 rows -- the docstring of `run_controls_v5.py` (the whole file is in the tree)"; print ""; print "```"; while ((getline l < DOC) > 0) print l; print "```"; print ""; next }
     /^### 4b\./ { skip = 0 }
     /^## 5\./ { print "## 5. The records previews are OMITTED for this seat (the file-reading seats review them); answer question 4 with N/A."; exit }
     !skip' DOC="$H/doc.txt" "$H/body.md" > "$H/body_glm.md"
grep -q '^### 4b\.' "$H/body_glm.md" && grep -q 'OMITTED for this seat' "$H/body_glm.md" || { echo "ASSEMBLY FAIL: the GLM body"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
    tok="${seat}_DASHOKV5_20261017"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    b="$H/body.md"; [ "$seat" = GLM ] && b="$H/body_glm.md"
    { sed "s|<TOKEN_LINE>|$line|" "$H/v5_head.md"; cat "$b" "$H/v5_tail.md"; } > "$H/packet_dashok_v5_$seat.md"
    echo "packet_dashok_v5_$seat.md  $(wc -c < "$H/packet_dashok_v5_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_dashok_v5_$seat.md")"
done
