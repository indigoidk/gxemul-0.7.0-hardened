#!/bin/bash
#  assemble_v7.sh -- the v7 pass packets for the tools/cxlaunch.sh landing: ONE token per seat, the launcher whole and its
#  v6 -> v7 diff (comments only, checked), the v7 controls whole and their v6 -> v7 diff (the CONTRACT is their header), the
#  mutant list whole, the censuses and the v6-pass measurements, the receipt's result lines, the kill table, the records
#  previews and the CHANGELOG draft.  Writes packet_cxland_v7_<SEAT>.md here; refuses an empty section, a missing sentinel, or a receipt or table that
#  is not of the current controls and driver.
set -u
H=$(cd "$(dirname "$0")" && pwd)
A=$(cd "$H/.." && pwd)
R=$(cd "$A/../../.." && pwd)
need() { [ -s "$1" ] || { echo "ASSEMBLY FAIL: missing or empty $1"; exit 9; }; }
M6="$A/v6pass/main_meas"
for f in "$H/v7_head.md" "$H/v7_tail.md" "$R/tools/cxlaunch.sh" "$A/cxlaunch_landed_v6.sh" "$A/run_controls_v6.sh" \
         "$A/run_controls_v7.sh" "$A/mut_launcher_v7.py" "$A/run_mutants_v7.sh" "$A/CENSUS_v5.txt" "$A/RECEIPT_v7.txt" \
         "$A/KILLTABLE_v7.txt" "$A/v5pass/RULELEN_CENSUS.txt" "$A/v5pass/SEMISGR_WHERE.txt" "$M6/ESC_WHERE.txt" \
         "$M6/NUL_HDR.txt" "$M6/NUL_BLOCKS.txt" "$M6/TAGCASE.txt" \
         "$A/f3/records_preview_OB.diff" "$A/f3/records_preview_ledger.txt" "$A/f3/changelog_block_draft.md"; do need "$f"; done
tail -1 "$A/RECEIPT_v7.txt" | grep -q CXLAND_CONTROLS_DONE || { echo "ASSEMBLY FAIL: RECEIPT_v7.txt has no sentinel"; exit 9; }
grep -q '^CXLAND_MUTANTS_DONE' "$A/KILLTABLE_v7.txt" || { echo "ASSEMBLY FAIL: KILLTABLE_v7.txt has no sentinel"; exit 9; }
grep -q '^SUMMARY: ' "$M6/ESC_WHERE.txt" && grep -q '^SUMMARY: ' "$M6/NUL_BLOCKS.txt" || { echo "ASSEMBLY FAIL: a v6-pass measurement has no SUMMARY"; exit 9; }
tail -1 "$A/CENSUS_v5.txt" | grep -q CENSUS_V5_DONE || { echo "ASSEMBLY FAIL: CENSUS_v5.txt has no sentinel"; exit 9; }
want=$(md5sum < "$A/run_controls_v7.sh" | cut -c1-32); wantm=$(md5sum < "$A/run_mutants_v7.sh" | cut -c1-32)
wantl=$(md5sum < "$A/mut_launcher_v7.py" | cut -c1-32); lm=$(md5sum < "$R/tools/cxlaunch.sh" | cut -c1-32)
for f in RECEIPT_v7.txt KILLTABLE_v7.txt; do
    grep -q "^# controls md5 $want" "$A/$f" || { echo "ASSEMBLY FAIL: $f is not of the current run_controls_v7.sh ($want)"; exit 9; }
done
grep -q "^# driver md5 $wantm" "$A/KILLTABLE_v7.txt" || { echo "ASSEMBLY FAIL: the kill table is not of the current run_mutants_v7.sh"; exit 9; }
grep -q "^# mutant list md5 $wantl" "$A/KILLTABLE_v7.txt" || { echo "ASSEMBLY FAIL: the kill table is not of the current mut_launcher_v7.py"; exit 9; }
grep -q "^# after:   $lm" "$A/RECEIPT_v7.txt" || { echo "ASSEMBLY FAIL: the receipt is not of the current launcher"; exit 9; }
grep -q "^# kill table for .*($lm)" "$A/KILLTABLE_v7.txt" || { echo "ASSEMBLY FAIL: the kill table is not of the current launcher"; exit 9; }
diff -u "$A/cxlaunch_landed_v6.sh" "$R/tools/cxlaunch.sh" > "$H/launcher_v6_to_v7.udiff"
diff -u "$A/run_controls_v6.sh" "$A/run_controls_v7.sh" > "$H/controls_v6_to_v7.udiff"
need "$H/launcher_v6_to_v7.udiff"; need "$H/controls_v6_to_v7.udiff"
diff <(grep -v '^ *#' "$A/cxlaunch_landed_v6.sh") <(grep -v '^ *#' "$R/tools/cxlaunch.sh") > /dev/null || { echo "ASSEMBLY FAIL: an executable launcher line moved"; exit 9; }
body() {
    echo
    echo "## 3. The repair, v6 -> v7"
    echo
    echo "### 3a. \`tools/cxlaunch.sh\` -- WHOLE, as it ships (md5 $(md5sum < "$R/tools/cxlaunch.sh" | cut -c1-32))"
    echo
    echo '```bash'; cat -n "$R/tools/cxlaunch.sh"; echo '```'
    echo
    echo "### 3a'. its v6 -> v7 diff ($(grep -c '^[-+][^-+]' "$H/launcher_v6_to_v7.udiff") changed lines; COMMENTS ONLY -- every executable line is v6's)"
    echo
    echo '```diff'; cat "$H/launcher_v6_to_v7.udiff"; echo '```'
    echo
    echo "### 3b. the controls, \`run_controls_v7.sh\`, WHOLE (the CONTRACT is its header)"
    echo
    echo '```bash'; cat -n "$A/run_controls_v7.sh"; echo '```'
    echo
    echo "### 3b'. their v6 -> v7 diff ($(grep -c '^[-+][^-+]' "$H/controls_v6_to_v7.udiff") changed lines)"
    echo
    echo '```diff'; cat "$H/controls_v6_to_v7.udiff"; echo '```'
    echo
    echo "### 3c. the mutant list, \`mut_launcher_v7.py\`, WHOLE (each mutant's exact edit and the controls named to kill it)"
    echo
    echo '```python'; cat -n "$A/mut_launcher_v7.py"; echo '```'
    echo
    echo "### 3d. the censuses: \`CENSUS_v5.txt\`, \`v5pass/RULELEN_CENSUS.txt\`, \`v5pass/SEMISGR_WHERE.txt\`"
    echo
    echo '```'; cat "$A/CENSUS_v5.txt"; echo; cat "$A/v5pass/RULELEN_CENSUS.txt"; echo; cat "$A/v5pass/SEMISGR_WHERE.txt"; echo '```'
    echo
    echo "### 3e. \`v6pass/main_meas/\` -- the main loop's measurements of the v6 pass's claims (the escape shapes, a NUL"
    echo "in a header, the NUL census, the tag case), each with its script in that directory"
    echo
    echo '```'; for m in ESC_WHERE NUL_HDR NUL_BLOCKS TAGCASE; do echo "== $m.txt"; cat "$M6/$m.txt"; echo; done; echo '```'
    echo
    echo "## 4. The receipts"
    echo
    echo "### 4a. \`RECEIPT_v7.txt\` -- the AFTER rows and every content check (the tracked and before rows, which record the old"
    echo "files, and the indented per-run output are in the file; the new rows' tracked and before values were recorded by"
    echo "\`RECEIPT_v7_calibration.txt\`, every after expectation written first)"
    echo
    echo '```'; grep -v '^      ' "$A/RECEIPT_v7.txt" | grep -vE '^[A-Z][0-9A-Z]* +(tracked|before) +exit='; echo '```'
    echo
    echo "### 4b. \`KILLTABLE_v7.txt\`, whole (\`run_mutants_v7.sh\`: each mutant through the after column; the base run is all three)"
    echo
    echo '```'; cat "$A/KILLTABLE_v7.txt"; echo '```'
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
    echo "### 5c. the CHANGELOG block (a DRAFT: its v7-pass sentence is written from this pass's answers)"
    echo
    cat "$A/f3/changelog_block_draft.md"
    echo
}
body > "$H/body.md"
grep -q '^+' "$H/body.md" || { echo "ASSEMBLY FAIL: no diff lines in the body"; exit 9; }
#  the PACKET-FED seat (GLM) gets the body without the controls' v6 -> v7 diff (the whole file is in 3b) and without the
#  records previews -- the three file-reading seats review those
awk '/^### 3b'"'"'\./ { skip = 1; next } /^### 3c\./ { skip = 0 }
     /^## 5\./ { print "## 5. The records previews are OMITTED for this seat (the file-reading seats review them); answer question 4 with N/A."; exit }
     !skip { print }' "$H/body.md" > "$H/body_glm.md"
grep -q 'OMITTED for this seat' "$H/body_glm.md" && grep -q '^### 3c\.' "$H/body_glm.md" || { echo "ASSEMBLY FAIL: the GLM body"; exit 9; }
for seat in FABLE ASTRA GROK GLM; do
    tok="${seat}_CXLANDV7_20261017"
    case $seat in
        FABLE) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then the FIRST LINE of \`C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/CHECKPOINT.md\` quoted verbatim, then your verdict line." ;;
        *) line="**Liveness:** open your answer with the token \`$tok\` on its own line, then your verdict line." ;;
    esac
    b="$H/body.md"; [ "$seat" = GLM ] && b="$H/body_glm.md"
    { sed "s|<TOKEN_LINE>|$line|" "$H/v7_head.md"; cat "$b" "$H/v7_tail.md"; } > "$H/packet_cxland_v7_$seat.md"
    echo "packet_cxland_v7_$seat.md  $(wc -c < "$H/packet_cxland_v7_$seat.md") bytes  token $tok  diff lines $(grep -c '^[-+][^-+]' "$H/packet_cxland_v7_$seat.md")"
done
