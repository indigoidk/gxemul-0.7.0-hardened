#!/bin/bash
#  assemble_v5.sh -- the v5 pass packets for the tools/cxlaunch.sh landing: ONE token per seat, the launcher whole (and its
#  v4 -> v5 diff, comments only), the v5 controls whole (the CONTRACT is their header), the mutant list whole, the census, the
#  receipt's result lines, the kill table, the records previews and the CHANGELOG draft.  Writes packet_cxland_v5_<SEAT>.md
#  here; refuses an empty section or a missing sentinel.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
R=$(cd "$A/../../.." && pwd)
KT="${CXL_KT:-$A/KILLTABLE_v5.txt}"
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
for f in "$H/v5_head.md" "$H/v5_tail.md" "$R/tools/cxlaunch.sh" "$A/cxlaunch_landed_v4.sh" "$A/run_controls_v5.sh" \
         "$A/mut_launcher_v5.py" "$A/run_mutants_v5.sh" "$A/CENSUS_v5.txt" "$A/RECEIPT_v5.txt" "$KT" \
         "$A/f3/records_preview_OB.diff" "$A/f3/records_preview_ledger.txt" "$A/f3/changelog_block_draft.md"; do need "$f"; done
tail -1 "$A/RECEIPT_v5.txt" | grep -q CXLAND_CONTROLS_DONE || { echo "ASSEMBLY FAIL: RECEIPT_v5.txt has no sentinel"; exit 9; }
tail -1 "$KT" | grep -q CXLAND_MUTANTS_DONE || { echo "ASSEMBLY FAIL: KILLTABLE_v5.txt has no sentinel"; exit 9; }
tail -1 "$A/CENSUS_v5.txt" | grep -q CENSUS_V5_DONE || { echo "ASSEMBLY FAIL: CENSUS_v5.txt has no sentinel"; exit 9; }
diff -u "$A/cxlaunch_landed_v4.sh" "$R/tools/cxlaunch.sh" > "$H/launcher_v4_to_v5.udiff"
need "$H/launcher_v4_to_v5.udiff"
body() {
    echo
    echo "## 3. The repair, v4 -> v5"
    echo
    echo "### 3a. \`tools/cxlaunch.sh\` -- WHOLE, as it ships (md5 $(md5sum < "$R/tools/cxlaunch.sh" | cut -c1-32))"
    echo
    echo '```bash'; cat -n "$R/tools/cxlaunch.sh"; echo '```'
    echo
    echo "### 3a'. its v4 -> v5 diff -- comments only ($(grep -c '^[-+][^-+]' "$H/launcher_v4_to_v5.udiff") changed lines)"
    echo
    echo '```diff'; cat "$H/launcher_v4_to_v5.udiff"; echo '```'
    echo
    echo "### 3b. the controls, \`run_controls_v5.sh\`, WHOLE (the CONTRACT is its header)"
    echo
    echo '```bash'; cat -n "$A/run_controls_v5.sh"; echo '```'
    echo
    echo "### 3c. the mutant list, \`mut_launcher_v5.py\`, WHOLE (each mutant's exact edit and the controls named to kill it)"
    echo
    echo '```python'; cat -n "$A/mut_launcher_v5.py"; echo '```'
    echo
    echo "### 3d. \`CENSUS_v5.txt\` (\`census_v5.py\`)"
    echo
    echo '```'; cat "$A/CENSUS_v5.txt"; echo '```'
    echo
    echo "## 4. The receipts"
    echo
    echo "### 4a. \`RECEIPT_v5.txt\` -- the AFTER rows and every content check (the tracked and before rows, which record the old"
    echo "files, and the indented per-run output are in the file)"
    echo
    echo '```'; grep -v '^      ' "$A/RECEIPT_v5.txt" | grep -vE '^[A-Z][0-9A-Z]* +(tracked|before) +exit='; echo '```'
    echo
    echo "### 4b. \`$(basename "$KT")\`, whole (\`run_mutants_v5.sh\`: each mutant through the after column; the base run is all three)"
    echo
    echo "It ran at 03:00 on launcher md5 236cda5f and controls md5 362c8a93.  Since then the launcher gained the three-line usage"
    echo "comment of U21 and the controls the two disclosures of U21/U22 -- comments only (section 3a' carries the launcher's"
    echo "diff).  The receipt in 4a is of the FINAL files (af18158e); the table's re-run on them is in progress and is the one the"
    echo "record will cite."
    echo
    echo '```'; cat "$KT"; echo '```'
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
    echo "### 5c. the CHANGELOG block (a DRAFT: its v5-pass sentence is written from this pass's answers)"
    echo
    cat "$A/f3/changelog_block_draft.md"
    echo
}
body > "$H/body.md"
grep -q '^+' "$H/body.md" || { echo "ASSEMBLY FAIL: no diff lines in the body"; exit 9; }
#  the PACKET-FED seat (GLM) gets the body without the records previews -- the three file-reading seats review those
awk '/^## 5\./ { print "## 5. The records previews are OMITTED for this seat (the file-reading seats review them); answer question 4 with N/A."; exit } { print }' \
    "$H/body.md" > "$H/body_glm.md"
grep -q 'OMITTED for this seat' "$H/body_glm.md" || { echo "ASSEMBLY FAIL: the GLM body"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
    tok="${seat}_CXLANDV5_20261017"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    b="$H/body.md"; [ "$seat" = GLM ] && b="$H/body_glm.md"
    { sed "s|<TOKEN_LINE>|$line|" "$H/v5_head.md"; cat "$b" "$H/v5_tail.md"; } > "$H/packet_cxland_v5_$seat.md"
    echo "packet_cxland_v5_$seat.md  $(wc -c < "$H/packet_cxland_v5_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_cxland_v5_$seat.md")"
done
