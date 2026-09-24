#!/bin/bash
# attrabbrev: ASSERT the R' outputs (PREDICTIONS_rp.txt + PREDICTIONS_rp_addendum.txt).  Exits nonzero on any mismatch.
# usage: verify_rp.sh [dir-holding-the-outputs]
set -u
A=${1:-$(cd "$(dirname "$0")" && pwd)}
fails=0; n=0
ok() { n=$((n+1)); if eval "$2"; then echo "ok    $1"; else echo "FAIL  $1"; fails=$((fails+1)); fi; }
line() { grep -E "^  (HARD|SOFT) +$2 +$3 " "$A/$1" | head -1; }
for c in Q0 Q1 Q2 Q3 Q4 Q5 Q7 Q10a Q10b Q11 Q12 Q13a7 Q13a8 Q15 Q16 Q17a Q17b Q19b Q19c; do
	ok "$c: R' byte-identical to HEAD" "cmp -s \"\$A/rp_${c}_head.out\" \"\$A/rp_${c}_rp.out\""
done
ok "Q0: R' equals the golden Q0 (post_Q0_at3e33201d.out)" 'cmp -s "$A/rp_Q0_rp.out" "$A/post_Q0_at3e33201d.out"'
ok "Q19a: HEAD passes the note's mention (the regression)" \
   'tail -1 "$A/rp_Q19a_head.out" | grep -q "^ATTRIBUTION_PASS" && ! grep -q "^  HARD .* fbsmlane " "$A/rp_Q19a_head.out"'
ok "Q19a: R' HARDs fbsmlane" 'grep -qE "^  HARD +cdbe7d75 +fbsmlane .*closed row does not name this code commit" "$A/rp_Q19a_rp.out"'
ok "Q19b: both HARD fbsmlane" 'grep -qE "^  HARD +cdbe7d75 +fbsmlane " "$A/rp_Q19b_head.out" && grep -qE "^  HARD +cdbe7d75 +fbsmlane " "$A/rp_Q19b_rp.out"'
ok "Q19c: both PASS" 'tail -1 "$A/rp_Q19c_head.out" | grep -q "^ATTRIBUTION_PASS" && tail -1 "$A/rp_Q19c_rp.out" | grep -q "^ATTRIBUTION_PASS"'
ok "Q20: HEAD fails OPEN (scanned 0, PASS)" 'grep -q "scanned 0 commits deep" "$A/rp_Q20_head.out" && tail -1 "$A/rp_Q20_head.out" | grep -q "^ATTRIBUTION_PASS"'
ok "Q20: R' fails CLOSED (a (git) HARD line, FAIL)" 'grep -qE "^  HARD +-- +\(git\)" "$A/rp_Q20_rp.out" && tail -1 "$A/rp_Q20_rp.out" | grep -q "^ATTRIBUTION_FAIL  git could not read"'
ok "Q21b: without the tag, HEAD and R' agree (SOFT records-only)" \
   '[ "$(line rp_Q21b_head_notag.out 7a361f47 m88kexcdetectorl2)" = "$(line rp_Q21b_rp_notag.out 7a361f47 m88kexcdetectorl2)" ] && line rp_Q21b_rp_notag.out 7a361f47 m88kexcdetectorl2 | grep -q "SOFT .*records-only"'
ok "Q21b: with the tag, HEAD HARDs (the shadowed lookup)" 'line rp_Q21b_head_tag.out 7a361f47 m88kexcdetectorl2 | grep -q "HARD .*work shipped"'
ok "Q21b: with the tag, R' stays SOFT records-only" 'line rp_Q21b_rp_tag.out 7a361f47 m88kexcdetectorl2 | grep -q "SOFT .*records-only"'
echo "VERIFY_RP: $((n-fails))/$n"
[ "$fails" -eq 0 ] && echo VERIFY_RP_PASS || { echo VERIFY_RP_FAIL; exit 1; }
