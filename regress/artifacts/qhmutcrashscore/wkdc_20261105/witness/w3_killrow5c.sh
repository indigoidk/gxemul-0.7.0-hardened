#!/bin/bash
#  WITNESS 3 (harness:) -- the SCORER of HEAD's regress/artifacts/batteryreds/row5_20260829/killrow5c.sh
#  (its score/want_delta/row functions, lines 26-54, extracted VERBATIM -- md5 printed), fed a STUB census
#  tool whose endings are chosen.  This is the shape that scores from END TOKENS, which the ledger row
#  recommends copying -- and it still scores a crashed run as a kill, because a MISSING token reads as a
#  MISMATCH and a mismatch is "killed".
#  usage: bash w3_killrow5c.sh [DRIVER] [TAG]
set -u
W=/mnt/c/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc
DRV=${1:-$W/headsrc/regress/artifacts/batteryreds/row5_20260829/killrow5c.sh}
TAG=${2:-HEAD}
X=$W/witness/r5c/$TAG
rm -rf "$X"; mkdir -p "$X/in"
exec > "$W/witness/r5c/W3_$TAG.log" 2>&1
a=$(grep -n '^score () {' "$DRV" | cut -d: -f1)
z=$(grep -n '^echo "=== ROW 5 KILL TABLE' "$DRV" | cut -d: -f1)
sed -n "${a},$((z - 1))p" "$DRV" > "$X/scorer.sh"
echo "driver: $DRV  md5 $(md5sum < "$DRV" | cut -c1-32)"
echo "scorer = its lines $a..$((z - 1)), extracted verbatim: md5 $(md5sum < "$X/scorer.sh" | cut -c1-32)"
for f in base surv kill crash crashlate; do echo "/* stub input $f */" > "$X/in/$f.c"; done
CEN=$W/witness/stub_census.py
WANT="6/6/6/11"
. "$X/scorer.sh"
echo "=================== the scorer's own output ==================="
row "BASE  unmodified" "$X/in/base.c" no
row "Ms   a genuine survivor" "$X/in/surv.c" yes
row "Mk   a genuine kill" "$X/in/kill.c" yes
row "Mc   census crashes before any token" "$X/in/crash.c" yes
row "Mc2  census crashes after 2 of 4 tokens" "$X/in/crashlate.c" yes
echo "=================== ground truth ==================="
for f in base surv kill crash crashlate; do
	python3 "$CEN" "$X/in/$f.c" > "$X/$f.out" 2> "$X/$f.err"; rc=$?
	printf '  %-10s census exit %s, %s of 4 end tokens, stderr: %s\n' "$f" "$rc" \
	    "$(grep -cE '^WDC_LATCH_(SET|READ|BALANCED|DECL)=' "$X/$f.out")" "$(tail -n 1 "$X/$f.err" | cut -c1-60)"
done
echo "W3_KILLROW5C_DONE $TAG"
