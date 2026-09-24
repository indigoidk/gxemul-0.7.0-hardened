#!/bin/bash
# attrabbrev: ASSERT the Q22c-Q25 outputs and exit codes (PREDICTIONS_q23.txt).  Exits nonzero on any mismatch.
set -u
A=${1:-$(cd "$(dirname "$0")" && pwd)}
fails=0; n=0
ok() { n=$((n+1)); if eval "$2"; then echo "ok    $1"; else echo "FAIL  $1"; fails=$((fails+1)); fi; }
rc() { grep -E "^$1 rc=" "$A/q23_rc_table.out" | sed 's/.* rc=//'; }
last() { tail -1 "$A/$1"; }
ok "Q22c: TOKEN {6,40} credits the 6-char note token (PASS, no fbsmlane HARD)" \
   'last q23_Q22c_token6.out | grep -q "^ATTRIBUTION_PASS" && ! grep -q "^  HARD .* fbsmlane " "$A/q23_Q22c_token6.out"'
ok "Q22c: R' HARDs it" 'grep -qE "^  HARD +cdbe7d +fbsmlane " "$A/q23_Q22c_rp.out" && [ "$(rc q23_Q22c_rp.out)" = 1 ]'
ok "Q23: R' fails closed on a nonzero git log that printed a full log (exit 2)" \
   'grep -qE "^  HARD +-- +\(git\) .*git log exited 1" "$A/q23_Q23_rp.out" && [ "$(rc q23_Q23_rp.out)" = 2 ]'
ok "Q23: the (and not r.stdout) guard passes it (exit 0)" 'last q23_Q23_stdout.out | grep -q "^ATTRIBUTION_PASS" && [ "$(rc q23_Q23_stdout.out)" = 0 ]'
ok "Q24: R' with NO environment is byte-identical to the golden Q0" 'cmp -s "$A/q23_Q24_rp_noenv.out" "$A/post_Q0_at3e33201d.out" && [ "$(rc q23_Q24_rp_noenv.out)" = 0 ]'
ok "Q24: DEPTH default 0 differs from the golden (scanned 0)" '! cmp -s "$A/q23_Q24_depth0.out" "$A/post_Q0_at3e33201d.out" && grep -q "scanned 0 commits deep" "$A/q23_Q24_depth0.out"'
ok "Q24: DEPTH default 130 differs from the golden" '! cmp -s "$A/q23_Q24_depth130.out" "$A/post_Q0_at3e33201d.out"'
ok "Q25: R' exits 1 on Q19a, Q15 and Q3's inputs and 0 on Q0's" \
   '[ "$(rc q23_Q25_q19a_rp.out)$(rc q23_Q25_q15_rp.out)$(rc q23_Q25_q3_rp.out)$(rc q23_Q25_q0_rp.out)" = 1110 ]'
ok "Q25: the E1 variant exits 0 while printing its HARD line" 'grep -q "^  HARD " "$A/q23_Q25_q19a_e1.out" && [ "$(rc q23_Q25_q19a_e1.out)" = 0 ]'
echo "VERIFY_Q23: $((n-fails))/$n"
[ "$fails" -eq 0 ] && echo VERIFY_Q23_PASS || { echo VERIFY_Q23_FAIL; exit 1; }
