#!/bin/bash
#  Unit controls for fix/killscore.sh's ks_score, both directions, on synthetic logs.  Expectations are
#  written beside each case BEFORE it runs; the script exits 0 only if every case matches.
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
KS=${1:-$W/fix/killscore.sh}
. "$KS" || { echo "cannot source $KS"; exit 9; }
D=$W/controls/ks_unit; rm -rf "$D"; mkdir -p "$D"
SEN='^WDC_IDENTIFY_(PASS|FAIL)$'; CNT='^  FAIL'
printf '  ok   a\n  FAIL b\n  FAIL c\n\n3 rows, 2 failures\nWDC_IDENTIFY_FAIL\n'     > "$D/kill.log"
printf '  ok   a\n  ok   b\n\n2 rows, 0 failures\nWDC_IDENTIFY_PASS\n'                > "$D/surv.log"
printf '  ok   a\n  FAIL b\n\n2 rows, 1 failures\nWDC_IDENTIFY_FAIL\n\n\n'           > "$D/blanktail.log"
printf '  ok   a\n  FAIL b\n'                                                       > "$D/trunc.log"
: > "$D/empty.log"
printf '  ok   a\nWDC_IDENTIFY_PASS\nfatal: something after the sentinel\n'          > "$D/after.log"
printf '  ok   a\nWDC_IDENTIFY_PASSED\n'                                            > "$D/nearmiss.log"
n=0 bad=0
t () {   # label want  -- args to ks_score
	local lab=$1 want=$2 got rc; shift 2
	got=$(ks_score "$@"); rc=$?
	n=$((n + 1))
	if [ "$got" = "$want" ]; then printf 'PASS %-34s got=%-16s (return %s)\n' "$lab" "$got" "$rc"
	else printf 'FAIL %-34s got=%-16s want=%s\n' "$lab" "$got" "$want"; bad=$((bad + 1)); fi
}
t "genuine kill: 2 red"            "2"             "$D/kill.log" 1 "$SEN" "$CNT"
t "genuine survivor: 0 red"        "0"             "$D/surv.log" 0 "$SEN" "$CNT"
t "sentinel then blank lines"      "1"             "$D/blanktail.log" 1 "$SEN" "$CNT"
t "truncated by SIGFPE"            "NOLOG rc=136"  "$D/trunc.log" 136 "$SEN" "$CNT"
t "empty log"                      "NOLOG rc=136"  "$D/empty.log" 136 "$SEN" "$CNT"
t "absent log"                     "NOLOG rc=127"  "$D/nosuch.log" 127 "$SEN" "$CNT"
t "content AFTER the sentinel"     "NOLOG rc=1"    "$D/after.log" 1 "$SEN" "$CNT"
t "near-miss sentinel spelling"    "NOLOG rc=0"    "$D/nearmiss.log" 0 "$SEN" "$CNT"
t "count nothing (-)"              "0"             "$D/kill.log" 1 "$SEN" "-"
t "wrong argument count"           "NOLOG rc=usage" "$D/kill.log" 1 "$SEN"
echo "KS_UNIT: $((n - bad)) of $n as expected"
echo KS_UNIT_DONE
[ "$bad" = 0 ]
