#!/bin/bash
#  score_selftest.sh <file holding the block> <good 33/33 log> <outdir>
#  #566: scores the ip30_abort gate block's scoring text (everything after the probe invocation, through its `fi',
#  extracted from the file named -- the text that ships) against the real 33/33 log and against doctored copies of it.
#  Every doctored case must red.  count/check/note mirror regress/lib.sh (grep -ac; exact compare; print).
#  Pass 1 (Astra, Grok) added n11-n15: a good log under a non-zero exit status, a duplicated and a malformed CONTROL
#  line, a duplicated DONE, and a REAL invocation of a probe file that does not exist.
set -u
BLK=$1; GOOD=$2; OUT=$3
mkdir -p "$OUT"
W=$(mktemp -d)
awk '/python3 -u artifacts\/ip30abortkill\/ip30_abort_probe.py/{on=1; next} on{print} on && /^fi$/{exit}' "$BLK" > "$W/score.sh"
grep -q '^fi$' "$W/score.sh" || { echo "EXTRACT FAILED"; exit 9; }
echo "scoring text: $(wc -l < "$W/score.sh") lines, md5 $(md5sum < "$W/score.sh" | cut -c1-32)"
count() { [ -f "$1" ] || { echo 0; return; }; local c; c=$(grep -ac -- "$2" "$1" 2>/dev/null); echo "${c:-0}"; }
check() { _checks=$((_checks+1)); [ "$2" = "$3" ] || { _fails=$((_fails+1)); _red="$_red [$1 got=$2]"; }; }
note() { :; }
L=$OUT/logs; mkdir -p "$L"
cp "$GOOD" "$L/good.log"
# n1: one row FAILs (status token flipped)
sed 's/^\(  kill 30 wr   got=alive        want=alive        \)ok  /\1FAIL  /' "$GOOD" > "$L/n1_onefail.log"
# n2: one row line missing
grep -v '^  tick 49 ' "$GOOD" > "$L/n2_rowlost.log"
# n3: one row replaced by a duplicate of another (counts unchanged)
awk '/^  tick 49 /{print "  tick 50      got=alive        want=alive        ok  dup"; next}{print}' "$GOOD" > "$L/n3_rowdup.log"
# n4: DEAD vehicle (as the probe prints it: zero RESULT, rows with no status token)
{ echo "ip30_abort_probe -- binary=/bin/true label=gate machine=sgi/ip30"; echo "IP30ABORT_CONTROL=DEAD"; echo "IP30ABORT_RESULT=0/0";
  echo "  *** SETUP FAILED -- the vehicle is not the vehicle. NOT 'no defect'. ***";
  grep '^  .* got=' "$GOOD" | sed 's/ ok  / /'; echo "IP30ABORT_DONE"; } > "$L/n4_dead.log"
# n5: empty log (an instant crash)
: > "$L/n5_empty.log"
# n6: no DONE (killed run)
grep -v '^IP30ABORT_DONE$' "$GOOD" > "$L/n6_nodone.log"
# n7: a second, contradictory RESULT appended
{ cat "$GOOD"; echo "IP30ABORT_RESULT=0/33"; } > "$L/n7_tworesult.log"
# n8: RESULT says 33/33 but a row line says FAIL (contradiction)
sed 's/^\(  latch tick   got=1            want=1            \)ok  /\1FAIL  /' "$GOOD" > "$L/n8_contra.log"
# n9: a 32-row table with RESULT 32/32 (shrunk table)
grep -v '^  xbit rev2 ' "$GOOD" | sed 's/^IP30ABORT_RESULT=33\/33$/IP30ABORT_RESULT=32\/32/' > "$L/n9_shrunk.log"
# n10: a renamed row (name changed, everything else intact)
sed 's/^  acc imask    got=/  acc imask0   got=/' "$GOOD" > "$L/n10_renamed.log"
# n11: the GOOD log, but the probe exited non-zero after printing it (death after DONE) -- scored with rc 1 below
cp "$GOOD" "$L/n11_goodrc1.log"
# n12: a second CONTROL line
{ cat "$GOOD"; echo "IP30ABORT_CONTROL=OK"; } > "$L/n12_twocontrol.log"
# n13: a malformed CONTROL line (lower case)
sed 's/^IP30ABORT_CONTROL=OK$/IP30ABORT_CONTROL=ok/' "$GOOD" > "$L/n13_badcontrol.log"
# n14: a second DONE line
{ cat "$GOOD"; echo "IP30ABORT_DONE"; } > "$L/n14_twodone.log"
# n15: a REAL invocation of a probe file that does not exist, from regress/, exactly as the block invokes one
REG=$(cd "$(dirname "$BLK")" && pwd)
( cd "$REG" && python3 -u artifacts/ip30abortkill/NO_SUCH_probe.py /bin/true gate > "$L/n15_noprobe.log" 2>&1 ); n15rc=$?
echo "n15: python3 on a missing probe file exited $n15rc; log: $(head -c 120 "$L/n15_noprobe.log" | tr '\n' ' ')"
for f in good n1_onefail n2_rowlost n3_rowdup n4_dead n5_empty n6_nodone n7_tworesult n8_contra n9_shrunk n10_renamed \
         n11_goodrc1 n12_twocontrol n13_badcontrol n14_twodone n15_noprobe; do
    IP30LOG=$L/$f.log; ip30rc=0; _checks=0; _fails=0; _red=""
    [ "$f" = n11_goodrc1 ] && ip30rc=1
    [ "$f" = n15_noprobe ] && ip30rc=$n15rc
    . "$W/score.sh" > /dev/null 2>&1
    v=$([ "$_fails" -gt 0 ] && echo RED || echo GREEN)
    want=$([ "$f" = good ] && echo GREEN || echo RED)
    printf '%-15s rc=%-2s checks=%-3s fails=%-3s %-5s %s\n' "$f" "$ip30rc" "$_checks" "$_fails" "$v" "$([ "$v" = "$want" ] && echo as-expected || echo '*** UNEXPECTED ***')"
    [ "$f" = good ] || echo "      red:$(echo "$_red" | cut -c1-220)"
done
rm -rf "$W"
echo SCORE_SELFTEST_DONE
