#!/bin/bash
# opus5 late seat: score the THREE PROPOSED rows (propose_rows.py) -- a patched SCRATCH
# copy of HEAD's regress/diff_wdc_identify.c -- against HEAD and every mutant already
# built in /tmp/gxopuswdc.  The baseline must stay green; the escapes must die.
set -u
S=/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/opuswdc
T=/tmp/gxopuswdc
OUT=$S/proposed_opus
mkdir -p "$OUT"
P=$OUT/diff_wdc_identify.PROPOSED.c
cp "$T/t_HEAD/regress/diff_wdc_identify.c" "$P"
python3 "$S/propose_rows.py" "$P" > "$OUT/patch.log" 2>&1 || { cat "$OUT/patch.log"; exit 3; }
diff -u "$T/t_HEAD/regress/diff_wdc_identify.c" "$P" > "$OUT/PROPOSED.diff"
: > "$OUT/TABLE.txt"
for tree in t_HEAD m_HEAD_Md_frozenj m_HEAD_Md_revwalk m_HEAD_Md_halfj m_HEAD_Md_armfrozen \
            m_HEAD_Md_wrongoff m_HEAD_Md_order m_HEAD_no495; do
  D=$T/$tree
  cp "$P" "$D/regress/diff_wdc_identify.PROPOSED.c"
  ( cd "$D/regress" && gcc -O2 -std=c99 -I../src/include -I../src/include/thirdparty \
      -ffunction-sections -fdata-sections -Wl,--gc-sections \
      -o prop diff_wdc_identify.PROPOSED.c ) > "$OUT/$tree.build" 2>&1
  if [ ! "$D/regress/prop" -nt "$D/regress/diff_wdc_identify.PROPOSED.c" ]; then
    echo "$tree BUILD FAILED" | tee -a "$OUT/TABLE.txt"; head -20 "$OUT/$tree.build"; continue
  fi
  ( cd "$D/regress" && ./prop ) > "$OUT/$tree.out" 2>&1
  printf '%-22s %s %s | %s\n' "$tree" "$(grep -E '^[0-9]+ rows' "$OUT/$tree.out")" \
     "$(grep -cE 'WDC_IDENTIFY_PASS' "$OUT/$tree.out")pass" \
     "$(grep -E '^  FAIL' "$OUT/$tree.out" | grep -v SELFCHECK | sed -E 's/^  FAIL //' | cut -c1-38 | tr '\n' ';')" \
     | tee -a "$OUT/TABLE.txt"
done
echo "--- proposed rows as printed on HEAD:" | tee -a "$OUT/TABLE.txt"
grep -E 'WHOLE chunk|chunk BODY|write route' "$OUT/t_HEAD.out" | tee -a "$OUT/TABLE.txt"
echo PROPOSED_DONE | tee -a "$OUT/TABLE.txt"
