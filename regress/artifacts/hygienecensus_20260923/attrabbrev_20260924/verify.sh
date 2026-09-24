#!/bin/bash
# attrabbrev: ASSERT every saved control output against its prediction (codex's finding 5: the drivers only printed).
# Exits nonzero on any mismatch.  usage: verify.sh   (reads the .out files beside it)
set -u
A=$(cd "$(dirname "$0")" && pwd)
fails=0; n=0
hard() { grep -E '^  HARD ' "$A/$1" | awk '{print $2, $3}' | sed -E 's/^([0-9a-f]{7})[0-9a-f]? /\1 /' | sort | tr '\n' ';'; }
want() {   # want <file> <verdict-prefix> <expected HARD set: "sha7 row;..." sorted, or "">
	n=$((n+1))
	local f=$1 v=$2 h=$3 got_v got_h
	got_v=$(tail -1 "$A/$f" | awk '{print $1}')
	got_h=$(hard "$f")
	if [ "$got_v" = "$v" ] && [ "$got_h" = "$h" ]; then echo "ok    $f  $got_v  [$got_h]"
	else echo "FAIL  $f  got $got_v [$got_h]  want $v [$h]"; fails=$((fails+1)); fi
}
six="09ded75 stagetokens;686d179 stagetokens;8bd97e4 lcaisalane;bb8efbf pcc2c040mienannounce;cdbe7d7 fbsmlane;e16a8b7 landiskaux;"
old4="2bb9cb4 pcc2defaultkill;257f56f sgirandompixel;b78bb0f pcc2widthkills;c7d7414 lcashiftub;ecc4d3b pcc2defaultkill;"
p2=$(printf '%s' "$six$old4" | tr ';' '\n' | grep . | sort | tr '\n' ';')
want pre_P0.out ATTRIBUTION_FAIL "$six"
want pre_P1.out ATTRIBUTION_FAIL "4264ee2 fbdeclinefive;"
want pre_P2.out ATTRIBUTION_FAIL "$p2"
want pre_P3.out ATTRIBUTION_FAIL "4264ee2 fbdeclinefive;"
want post_Q0.out ATTRIBUTION_PASS ""
want post_Q1.out ATTRIBUTION_PASS ""
want post_Q2.out ATTRIBUTION_PASS ""
want post_Q3.out ATTRIBUTION_FAIL "cdbe7d7 fbsmlane;"
want post_Q4.out ATTRIBUTION_FAIL "cdbe7d7 fbsmlane;"
want post_Q5.out ATTRIBUTION_PASS ""
want post_Q6.out ATTRIBUTION_PASS ""
want post_Q7.out ATTRIBUTION_FAIL "b78bb0f pcc2widthkills;"
want mut_Q8.out ATTRIBUTION_PASS ""
want mut_Q9.out ATTRIBUTION_PASS ""
# the REOPENED path, and the mutant's identity with Q0 on Q0's input
for f in pre_P3.out post_Q2.out mut_Q8.out; do
	n=$((n+1))
	if grep -qE '^  REOPENED b78bb0f[0-9a-f]? pcc2widthkills' "$A/$f"; then echo "ok    $f  REOPENED b78bb0f"
	else echo "FAIL  $f  no REOPENED line for b78bb0f"; fails=$((fails+1)); fi
done
n=$((n+1))
if cmp -s "$A/post_Q0.out" "$A/mut_Q9.out"; then echo "ok    mut_Q9.out == post_Q0.out (the mutant escapes Q0)"
else echo "FAIL  mut_Q9.out differs from post_Q0.out"; fails=$((fails+1)); fi
echo "VERIFY: $((n-fails))/$n"
[ "$fails" -eq 0 ] && echo VERIFY_PASS || { echo VERIFY_FAIL; exit 1; }
