#!/bin/bash
# attrabbrev: ASSERT the Q10-Q14 outputs (PREDICTIONS_q10.txt).  Exits nonzero on any mismatch.
# The Q0 baseline for these is post_Q0_at3e33201d.out: post_Q0.out was taken at 4264ee20, and the 60-commit window moved
# when 3e33201d entered (the commit that left it names lcairqstubkill, so only the NEVER NAMED line differs).
set -u
A=${1:-$(cd "$(dirname "$0")" && pwd)}
fails=0; n=0
norm() { sed -E 's/\b[0-9a-f]{7,40}\b/HASH/g; s/ +/ /g' "$A/$1"; }
verdict() { tail -1 "$A/$1" | awk '{print $1}'; }
hard() { grep -E '^  HARD ' "$A/$1" | awk '{print substr($2,1,7), $3}' | sort | tr '\n' ';'; }
ok() { n=$((n+1)); if eval "$2"; then echo "ok    $1"; else echo "FAIL  $1"; fails=$((fails+1)); fi; }
ok "Q10a abbrev 12 == Q0 modulo width" 'diff <(norm post_Q0_at3e33201d.out) <(norm post_Q10a.out) >/dev/null'
ok "Q10b abbrev 40 == Q0 modulo width" 'diff <(norm post_Q0_at3e33201d.out) <(norm post_Q10b.out) >/dev/null'
ok "Q10a/b PASS" '[ "$(verdict post_Q10a.out)" = ATTRIBUTION_PASS ] && [ "$(verdict post_Q10b.out)" = ATTRIBUTION_PASS ]'
ok "M10 width guard FAILs at abbrev 12, >= 6 HARD incl. fbsmlane" \
   '[ "$(verdict mut_M10.out)" = ATTRIBUTION_FAIL ] && [ "$(grep -c "^  HARD " "$A/mut_M10.out")" -ge 6 ] && hard mut_M10.out | grep -q "cdbe7d7 fbsmlane"'
ok "Q11 substring-not-prefix token HARDs exactly fbsmlane" '[ "$(hard post_Q11.out)" = "cdbe7d7 fbsmlane;" ]'
ok "M11 substring matcher PASSes Q11's input (Q11 separates it)" '[ "$(verdict mut_M11.out)" = ATTRIBUTION_PASS ] && [ -z "$(hard mut_M11.out)" ]'
ok "M12 first-token matcher HARDs stagetokens on Q0's input (Q0 separates it)" 'hard mut_M12.out | grep -q "09ded75 stagetokens"'
ok "Q12 two-token row, target second: PASS" '[ "$(verdict post_Q12.out)" = ATTRIBUTION_PASS ]'
ok "M12 on Q12's input HARDs fbsmlane" 'hard mut_M12b.out | grep -q "cdbe7d7 fbsmlane"'
ok "Q14 no pipeline-code exemption: byte-identical to Q0" 'cmp -s "$A/post_Q0_at3e33201d.out" "$A/var_Q14.out"'
ok "Q13 depth 800: abbrev 7 == abbrev 8 modulo width, both PASS" \
   'diff <(norm post_Q13_a7.out) <(norm post_Q13_a8.out) >/dev/null && [ "$(verdict post_Q13_a7.out)" = ATTRIBUTION_PASS ] && [ "$(verdict post_Q13_a8.out)" = ATTRIBUTION_PASS ]'
echo "VERIFY_Q10: $((n-fails))/$n"
[ "$fails" -eq 0 ] && echo VERIFY_Q10_PASS || { echo VERIFY_Q10_FAIL; exit 1; }
