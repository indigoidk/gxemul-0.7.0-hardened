#!/bin/bash
#  assemble_v6.sh -- the v6 pass packets for `dashokclass`: ONE token per seat, the staged checker WHOLE, the renderer's diff
#  against HEAD and the Q2 block (no staged file changed in v6), the controls' v5 -> v6 diff AND the v6 controls WHOLE (their
#  docstring is the CONTRACT), the receipt, the kill table with the v6 mutants, the census, the records previews and the
#  CHANGELOG draft.  Writes packet_dashok_v6_<SEAT>.md here; refuses a section that came out empty or an artifact without its
#  completion sentinel.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
for f in "$H/v6_head.md" "$H/v6_tail.md" "$A/staged_v5/tools/pipeline/check_entry_domain.py" \
         "$A/staged_v5/tools/pipeline/gen_dashboard.py" "$A/gen_dashboard_before.py" "$A/staged_v5/tools/precommit_check.sh" \
         "$A/run_controls_v5.py" "$A/run_controls_v6.py" "$A/run_mutants_v6.py" "$A/RECEIPT_v6_on_staged_v5.txt" \
         "$A/KILLTABLE_v6_staged.txt" "$A/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt" "$A/f3/records_preview_OB.diff" \
         "$A/f3/records_preview_ledger.txt" "$A/f3/records_preview_rulingsC.diff" "$A/f3/changelog_block_draft.md"; do need "$f"; done
grep -q 'DASHOKCLASS_CONTROLS_DONE' "$A/RECEIPT_v6_on_staged_v5.txt" || { echo "ASSEMBLY FAIL: no sentinel in the v6 receipt"; exit 9; }
grep -q 'DASHOKCLASS_MUTANTS_DONE' "$A/KILLTABLE_v6_staged.txt" || { echo "ASSEMBLY FAIL: no sentinel in the kill table"; exit 9; }
grep -q 'DASHMISSINGD_CENSUS_DONE' "$A/DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt" || { echo "ASSEMBLY FAIL: no sentinel in the census"; exit 9; }
grep -q '<GROK_ROWS>\|<GROK_VERDICT>' "$H/v6_head.md" && { echo "ASSEMBLY FAIL: the head still carries a Grok placeholder"; exit 9; }
#  the receipt and the table must be of the CURRENT controls and driver: each run is launched with a first line
#  "# controls md5 <md5>" (and the table "# driver md5 <md5>"), so an edit after the run -- even a docstring -- is caught here
want=$(md5sum < "$A/run_controls_v6.py" | cut -c1-32); wantm=$(md5sum < "$A/run_mutants_v6.py" | cut -c1-32)
for f in RECEIPT_v6_on_staged_v5.txt KILLTABLE_v6_staged.txt; do
    grep -q "^# controls md5 $want" "$A/$f" || { echo "ASSEMBLY FAIL: $f is not of the current run_controls_v6.py ($want)"; exit 9; }
done
grep -q "^# driver md5 $wantm" "$A/KILLTABLE_v6_staged.txt" || { echo "ASSEMBLY FAIL: the kill table is not of the current run_mutants_v6.py"; exit 9; }
diff -u --label gen_dashboard.py@HEAD --label gen_dashboard.py@staged_v5 "$A/gen_dashboard_before.py" "$A/staged_v5/tools/pipeline/gen_dashboard.py" > "$H/render_head_to_staged.udiff"
diff -u --label run_controls_v5.py --label run_controls_v6.py "$A/run_controls_v5.py" "$A/run_controls_v6.py" > "$H/controls_v5_to_v6.udiff"
need "$H/render_head_to_staged.udiff"; need "$H/controls_v5_to_v6.udiff"
body() {
    echo
    echo "## 3. The files under test (UNCHANGED since v5: md5s in the receipt header)"
    echo
    echo "### 3a. the staged checker, \`staged_v5/tools/pipeline/check_entry_domain.py\`, WHOLE"
    echo
    echo '```python'; cat -n "$A/staged_v5/tools/pipeline/check_entry_domain.py"; echo '```'
    echo
    echo "### 3b. the renderer change, \`gen_dashboard.py\` HEAD -> staged ($(grep -c '^[-+][^-+]' "$H/render_head_to_staged.udiff") changed lines)"
    echo
    echo '```diff'; cat "$H/render_head_to_staged.udiff"; echo '```'
    echo
    echo "### 3c. precommit section Q2, as staged"
    echo
    echo '```bash'; sed -n '/^#  ---- Q2 ---/,/^#  ---- R ---/p' "$A/staged_v5/tools/precommit_check.sh"; echo '```'
    echo
    echo "## 4. The repair: the controls, v5 -> v6"
    echo
    echo "### 4a. \`run_controls_v5.py\` -> \`run_controls_v6.py\` ($(grep -c '^[-+][^-+]' "$H/controls_v5_to_v6.udiff") changed lines)"
    echo
    echo '```diff'; cat "$H/controls_v5_to_v6.udiff"; echo '```'
    echo
    echo "### 4b. \`run_controls_v6.py\`, WHOLE (its docstring is the CONTRACT and the row list)"
    echo
    echo '```python'; cat -n "$A/run_controls_v6.py"; echo '```'
    echo
    echo "### 4c. \`RECEIPT_v6_on_staged_v5.txt\`, whole"
    echo
    echo '```'; cat "$A/RECEIPT_v6_on_staged_v5.txt"; echo '```'
    echo
    echo "### 4d. \`KILLTABLE_v6_staged.txt\` (the mutants are \`run_mutants_v6.py\`'s MUTANTS; the v6 additions follow)"
    echo
    echo '```'; grep -v '^#   ' "$A/KILLTABLE_v6_staged.txt"; echo '```'
    echo
    echo '```python'; sed -n "/#  v6 -- the v5 pass's survivors/,/^]\$/p" "$A/run_mutants_v6.py"; echo '```'
    echo
    echo "### 4e. \`DASHMISSINGD_CENSUS_HEAD_8bf8b5a1.txt\` (\`dashmissingd_census.py\` on HEAD's ledger)"
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
    echo "### 5d. the CHANGELOG block (a DRAFT: its v6-pass sentence is written from this pass's answers)"
    echo
    cat "$A/f3/changelog_block_draft.md"
    echo
}
body > "$H/body.md"
grep -q '^+' "$H/body.md" || { echo "ASSEMBLY FAIL: no diff lines in the body"; exit 9; }
#  the PACKET-FED seat (GLM) gets a narrower body: the CONTRACT (the docstring), the renderer FIXTURE (the EXPECT table and the
#  FX rows -- K20 was not checkable without it, GLM 5.3, v5 pass) and C27's walk (new logic in v6), instead of the controls
#  whole and their diff, and no records previews -- the three file-reading seats review those
sed -n '/^"""Controls/,/^"""$/p' "$A/run_controls_v6.py" > "$H/doc.txt"
sed -n '/^SEATS = \[s\["id"\]/,/^fx_path = wjson/p' "$A/run_controls_v6.py" > "$H/fixture.txt"
sed -n '/^def walk_name/,/^say("C27 /p' "$A/run_controls_v6.py" > "$H/c27.txt"
need "$H/doc.txt"; need "$H/fixture.txt"; need "$H/c27.txt"
awk '/^## 4\. The repair/ { skip = 1
                            print "## 4. The repair: the controls, v5 -> v6 (the whole file and its diff are in the tree; this seat gets the parts below)"
                            print ""; print "### 4a. the CONTRACT and the 115 rows -- the docstring of `run_controls_v6.py`"; print ""; print "```"
                            while ((getline l < DOC) > 0) print l
                            print "```"; print ""; print "### 4b. the renderer FIXTURE -- the EXPECT table and the FX rows, verbatim"; print ""; print "```python"
                            while ((getline l < FIX) > 0) print l
                            print "```"; print ""; print "### 4b2. C27 -- the ast walk and its use whitelists, verbatim (new in v6)"; print ""; print "```python"
                            while ((getline l < C27) > 0) print l
                            print "```"; print ""; next }
     /^### 4c\./ { skip = 0 }
     /^## 5\./ { print "## 5. The records previews are OMITTED for this seat (the file-reading seats review them); answer question 4 with N/A."; exit }
     !skip' DOC="$H/doc.txt" FIX="$H/fixture.txt" C27="$H/c27.txt" "$H/body.md" > "$H/body_glm.md"
grep -q '^### 4c\.' "$H/body_glm.md" && grep -q 'OMITTED for this seat' "$H/body_glm.md" && grep -q '^def walk_name' "$H/body_glm.md" \
    && grep -q '^EXPECT = ' "$H/body_glm.md" || { echo "ASSEMBLY FAIL: the GLM body"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
    tok="${seat}_DASHOKV6_20261017"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    b="$H/body.md"; [ "$seat" = GLM ] && b="$H/body_glm.md"
    { sed "s|<TOKEN_LINE>|$line|" "$H/v6_head.md"; cat "$b" "$H/v6_tail.md"; } > "$H/packet_dashok_v6_$seat.md"
    echo "packet_dashok_v6_$seat.md  $(wc -c < "$H/packet_dashok_v6_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_dashok_v6_$seat.md")"
done
