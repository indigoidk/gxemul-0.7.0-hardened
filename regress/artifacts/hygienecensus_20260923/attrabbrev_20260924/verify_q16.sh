#!/bin/bash
# attrabbrev: ASSERT the Q15-Q18 outputs (PREDICTIONS_q15.txt, PREDICTIONS_q16.txt).  Exits nonzero on any mismatch.
set -u
A=${1:-$(cd "$(dirname "$0")" && pwd)}
fails=0; n=0
ok() { n=$((n+1)); if eval "$2"; then echo "ok    $1"; else echo "FAIL  $1"; fails=$((fails+1)); fi; }
hards() { grep -E '^  HARD ' "$A/$1" | awk '{print substr($2,1,7), $3}' | sort | tr '\n' ';'; }
pass() { tail -1 "$A/$1" | grep -q '^ATTRIBUTION_PASS'; }
ok "Q15 in work: HARD fbdeclinefive" '[ "$(hards post_Q15.out)" = "4264ee2 fbdeclinefive;" ]'
ok "C4 and N7 pass Q15 as REOPENED" 'pass var_C4_Q15.out && pass var_N7_Q15.out && grep -q "^  REOPENED 4264ee20 fbdeclinefive" "$A/var_C4_Q15.out"'
ok "N11/N10 at depth 60 are byte-identical to Q0" 'cmp -s "$A/var_N11_d60.out" "$A/post_Q0_at3e33201d.out" && cmp -s "$A/var_N10_d60.out" "$A/post_Q0_at3e33201d.out"'
ok "N11 at depth 800: 5 HARD" '[ "$(grep -c "^  HARD " "$A/var_N11_d800.out")" = 5 ]'
ok "N10 at depth 800: 2 HARD" '[ "$(grep -c "^  HARD " "$A/var_N10_d800.out")" = 2 ]'
ok "Q16 full-hash reopened: REOPENED, PASS" 'pass post_Q16.out && grep -q "^  REOPENED b78bb0f6 pcc2widthkills" "$A/post_Q16.out"'
ok "C1 HARDs Q16 and passes Q2's input" '[ "$(hards var_C1_Q16.out)" = "b78bb0f pcc2widthkills;" ] && pass var_C1_Q2.out'
ok "Q17a held / Q17b open: HARD fbdeclinefive" '[ "$(hards post_Q17a.out)" = "4264ee2 fbdeclinefive;" ] && [ "$(hards post_Q17b.out)" = "4264ee2 fbdeclinefive;" ]'
ok "K4 passes Q17a, still HARDs Q15" 'pass var_K4_Q17a.out && [ "$(hards var_K4_Q15.out)" = "4264ee2 fbdeclinefive;" ]'
ok "Lg5: PASS but NEVER NAMED 135, where Q0 prints 114" \
   'pass var_Lg5_Q0.out && grep -q "carry commits: 135 " "$A/var_Lg5_Q0.out" && grep -q "carry commits: 114 " "$A/post_Q0_at3e33201d.out"'
ok "Q18: exemption dropped at depth 800 -> 8 HARD" '[ "$(grep -c "^  HARD " "$A/var_Q18.out")" = 8 ]'
ok "pipeline census: 60 scanned, 28 touch pipeline code, 3 records-only by the exemption" \
   'grep -q "scanned 60; touch pipeline code 28; graded records-only among them 3" "$A/pipeline_code_census.out"'
echo "VERIFY_Q16: $((n-fails))/$n"
[ "$fails" -eq 0 ] && echo VERIFY_Q16_PASS || { echo VERIFY_Q16_FAIL; exit 1; }
