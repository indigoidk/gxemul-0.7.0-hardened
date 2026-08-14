#!/bin/bash
# GATE 6 -- no distress markers in the boot logs.
#
# Cheap, and it has caught real regressions: round 40 found that #265's own diagnostic
# flooded the log on a healthy boot, and that #261 was listing a subsystem it had not
# actually armed. Neither changed a pass/fail count -- both showed up only as marker counts.
#
# READS THE RAW PTY LOGS ON PURPOSE. fatal() and debugmsg() output is not guest console
# output; it goes straight to stdout and interleaves into the pty stream, and the arc
# screen reconstruction that gate 4 needs for GUEST tokens actively garbles it. Measured:
# '{ asc: data in' reads 0 from the arc screen rebuild and 5 from the raw log.
#
# TWO WAYS THIS GATE USED TO PASS WITHOUT PROVING ANYTHING, both now closed:
#
#  * EMPTY LOGS. It checked only that the files existed. `: > /tmp/pD.log` made 20 checks
#    go green -- two empty files certifying a clean boot. There is now a POSITIVE CONTROL:
#    each log must be substantial AND contain the guest's own uid=0(root), so absence of
#    distress is only counted when presence of a real boot is proved.
#  * STALE LOGS. Everything lives in /tmp and survives until reboot, so running this gate
#    alone -- or after gate 4 skipped -- graded yesterday's logs, produced by a binary that
#    no longer exists. Gate 4 now deletes them first and copies them into $LOGDIR when it
#    finishes; this gate reads THOSE copies, which only exist if gate 4 actually ran.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

gate_begin "log-hygiene"

# ---- static wiring: the readiness-predicate ratchet ---------------------
#
#  DELIBERATELY BEFORE the log check below, so a missing log can never SKIP
#  it.  This gate had no source assertions at all until now -- it graded logs
#  and nothing else -- which is why the defect it guards could spread unseen.
#
#  THE DEFECT IT FREEZES: a readiness predicate matching a BARE ">" is
#  satisfied by the guest's own register dump, whose FIRST line is the
#  symbol line "  <...>" -- and that line ends in ">".  Line-buffered on a
#  pty, each line is its own flush, so a reader waking between line 1 and
#  line 2 returns SATISFIED WITH THE REGISTERS UNREAD.  Healthy host,
#  microseconds wide, and armed on every CPU family whose dump starts that
#  way (MIPS, PPC, SH, m88k all do).
#
#  THE CONVERSION HAS LANDED (#392), so EXPECT_BARE is now 0 and this is a
#  RATCHET AGAINST REGRESSION rather than against spread.  All 14 sites now take
#  a fresh mark before the write, require the FULL prompt in that slice, and
#  require the command's own echo first.
#
#  The converted predicate deliberately keeps the LITERAL endswith("GXemul>")
#  spelling, which is the idiom the ARM probes already use (arm_idle_probe.py:194).
#  A reviewer proposed a shared helper holding the prompt in a constant or a
#  regex; either would have broken this gate, though -- as a pass-2 seat pointed
#  out -- NOT by the same route, and the first draft of this comment conflated
#  them:
#      endswith(PROMPT)  -> counted, unrecognised -> fails the `unknown` check;
#      re.search(...)    -> not an endswith at all, so `unknown` never moves --
#                           it fails the anchored-site COUNT below instead.
#  Matching the house idiom kept the ratchet working with no redesign, which is
#  worth remembering the next time a "cleaner" abstraction is proposed for
#  something a static check is watching.
#
#  Exact equality, not a ceiling, and on purpose: a "<=" check would let the
#  number fall silently, and a silent fall is how you lose track of whether
#  the conversion actually happened.  Any movement in either direction must
#  be a deliberate edit here.
#  COUNTING IT PROPERLY, after a review pass named three ways to walk around a
#  naive grep: the single-quoted spelling, a variable or helper holding the
#  prompt, and probes living in a subdirectory the flat glob never visits.
#  A ratchet you can step around is worse than no ratchet, because it reads as
#  protection.  So:
#    - find RECURSIVELY, not "$HERE"/*.py;
#    - accept either quote style;
#    - and make the check CLOSED-WORLD: every .endswith() in the tree must use
#      one of the two KNOWN literals.  A third spelling -- including
#      endswith(PROMPT) or any indirection through a helper -- is unknown, and
#      unknown fails.  That converts "I grepped for the bad thing" into "I
#      enumerated everything and recognised all of it", which is the only form
#      that cannot be evaded by inventing a new way to write it.
EXPECT_BARE=0
EXPECT_UNKNOWN=0
#  CODE ONLY.  The first version of this check counted a line of PROSE -- a
#  comment in arm_flags_probe.py that discusses endswith() -- and reported an
#  unrecognised spelling that does not exist.  A check that fires on its own
#  documentation trains the reader to ignore it, so full-line comments are
#  stripped before anything is counted.  (Known limit, stated rather than
#  hidden: an endswith() sitting after code on the same line as a trailing
#  comment is still counted as code, which is the safe direction.)
#  readiness_predicate_test.py is EXCLUDED here and pinned separately below.
#  It is the offline truth table for #392, so it necessarily CONTAINS the two
#  broken spellings -- demonstrating them is its whole job. Counting them with
#  the live sites would make the ratchet permanently red.
#
#  This is a FAIL-CLOSED exception, not a hole: the file is named exactly, and
#  its own contents are asserted below, so it cannot quietly stop testing what it
#  claims to test. A loose `grep -v test` would have been the wrong shape -- it
#  would silently exempt any future file with "test" in its name.
py_code() { find "$HERE" -name '*.py' -type f \
                 ! -name 'readiness_predicate_test.py' -print0 2>/dev/null | \
            xargs -0 grep -h "endswith(" 2>/dev/null | grep -v '^[[:space:]]*#'; }
#  -o, so these count OCCURRENCES and not LINES.  With -c a single line holding
#  two different spellings counts once in each of the three totals and drives
#  `unknown` NEGATIVE -- a subtraction is only meaningful if all three terms
#  count the same kind of thing.
bare=$(py_code | grep -o "endswith([\"']>[\"'])" | wc -l)
#  Every endswith( in code, minus the two we recognise: the bare prompt above
#  and the correct full prompt.  Anything left is a spelling nobody reviewed --
#  including endswith(PROMPT) or any indirection through a helper.
allends=$(py_code | grep -o "endswith(" | wc -l)
full=$(py_code | grep -o "endswith([\"']GXemul>[\"'])" | wc -l)
unknown=$((allends - bare - full))
check "readiness: bare-prompt sites frozen (#37)" "$bare" "$EXPECT_BARE"
check "readiness: no unrecognised endswith spelling" "$unknown" "$EXPECT_UNKNOWN"

#  THE POSITIVE HALF OF THE #392 CHECK, and it is the half that binds the offline
#  truth table in gate_offline.sh to the code that actually ships.  Counting only
#  the ABSENCE of the bad spelling is not enough: a site could be deleted, or
#  reverted to something that is neither the old form nor the new one, and the two
#  checks above would both stay green.  So count the three constructs the
#  conversion introduced and require all fourteen of each.
#
#  Exact equality again, and for the same reason as EXPECT_BARE: a ">=" would let
#  a site quietly disappear.  If a probe legitimately gains or loses a wait site,
#  this number is edited deliberately, in the same commit, by someone who looked.
EXPECT_CONVERTED=14
#  One helper for all three, so they agree on WHAT they look at.  The first draft
#  used py_code() for the anchored count and a raw grep for the other two, which
#  meant a comment mentioning the echo guard would have inflated one count and not
#  the others -- a spurious mismatch with no defect behind it.  A seat caught it
#  while it was still latent.
probe_code() { find "$HERE" -name '*.py' -type f \
                    ! -name 'readiness_predicate_test.py' -print0 2>/dev/null | \
               xargs -0 grep -h "$1" 2>/dev/null | grep -v '^[[:space:]]*#'; }
conv_anchor=$(probe_code 'resp.rstrip().endswith("GXemul>")' | grep -c .)
conv_echo=$(probe_code 'echo is not None and echo not in resp' | grep -c .)
#  ANCHOR THROUGH THE ECHO ARGUMENT.  The first version stopped at
#  'return wait(mark=_mark' -- a PREFIX -- so deleting ", echo=s if s else None"
#  from all fourteen sites left this count at 14 and every other counter
#  unchanged. A pass-2 seat MEASURED that mutant passing gate_hygiene,
#  gate_offline, gate_mips_rounding and gate_sh_rounding simultaneously: a
#  shipped fix with no detector, which is this project's worst vacuity class.
#  The comma is what makes the assertion an assertion.
#  ANCHOR THROUGH THE WHOLE EXPRESSION, not just as far as "echo=". A pass-2b
#  seat pointed out that the previous form still admitted
#      return wait(mark=_mark, echo=None)
#  which passes the argument and disables the guard in ONE WORD. This is the
#  THIRD tightening of this same count -- first it stopped at "_mark", then at
#  "echo=", now at the full conditional. Each time the surviving prefix was a
#  real substring of both the fixed and the broken code, which is exactly the
#  property a detector must not have.
conv_mark=$(probe_code 'return wait(mark=_mark, echo=[a-z][a-z]* if [a-z][a-z]* else None)' | grep -c .)

#  THE HOLE A PASS-2 SEAT FOUND, and it is the sharpest finding of the review:
#  the checks above catch a REVERT but not an ADDITION of the OTHER broken form.
#  A brand-new site spelled
#        if buf.rstrip().endswith("GXemul>"):
#  passes everything -- bare is still 0, the spelling is RECOGNISED so `unknown`
#  stays 0, and it is not the anchored form so conv_anchor stays 14.  Yet #392
#  MEASURED that exact configuration (full prompt, whole buffer) failing just as
#  completely as the bare one: arm B scored 0/80, byte-identical to arm A.
#
#  So count it explicitly.  The two that exist are arm_flags_probe.py:144 and
#  :645 -- known, filed, and deliberately out of #392's scope.  Pinning the count
#  at 2 turns that scope decision into a FAIL-CLOSED ALLOWLIST: those two are
#  tolerated, a third is not, and when they are finally converted this number
#  goes to 0 in the same commit.
EXPECT_WHOLE_FULL=2
whole_full=$(probe_code 'buf.rstrip().endswith("GXemul>")' | grep -c .)
check "readiness: whole-buffer full-prompt sites (allowlist)" "$whole_full" "$EXPECT_WHOLE_FULL"
check "readiness: anchored full-prompt sites (#392)" "$conv_anchor" "$EXPECT_CONVERTED"
check "readiness: echo guard present (#392)"         "$conv_echo"   "$EXPECT_CONVERTED"
check "readiness: send takes a fresh mark (#392)"    "$conv_mark"   "$EXPECT_CONVERTED"

#  PIN THE EXEMPTED FILE'S OWN CONTENTS.  readiness_predicate_test.py is excluded
#  from the census above because it deliberately contains the broken spellings;
#  that exemption is only safe while the file still HOLDS them.  If its two
#  negative arms were deleted the offline truth table would go green by testing
#  nothing, and the exclusion above would hide it.  So the exemption and this
#  assertion travel together -- an allowlist entry that checks what it exempts.
#  -o again, not -c: OCCURRENCES, not lines.  Same reason as above, and the
#  expected numbers are asymmetric for a real reason -- 2 bad arms, but 3 good
#  occurrences, because besides the two `full-*` arms the test also prints the
#  LEFTOVER demonstration line, which re-matches the prompt on purpose to show
#  that rstrip() erases the trailing space.  The first draft of this check
#  expected 2 and failed; the file was right and the expectation was wrong.
#  CODE ONLY here too.  The first version grepped the file RAW, so a seat
#  gutted both negative arms, dropped the two spellings into a single COMMENT
#  line, and the pin still read 2 and 3. The filter that this file already
#  applies sixty lines above was missing from the one check whose whole job is
#  to keep an exemption honest.
rpt="$HERE/readiness_predicate_test.py"
rpt_code() { [ -f "$rpt" ] && grep -v '^[[:space:]]*#' "$rpt"; }
check "readiness: truth table keeps its 2 bad arms" \
      "$( [ -f "$rpt" ] && rpt_code | grep -o 'endswith(">")' | wc -l || echo missing)" "2"
#  FIVE, not three: the two original full-* arms, the two late-prompt arms that
#  give the ECHO conjunct its behavioural coverage, and the leftover demo.
check "readiness: truth table keeps its good arms + leftover demo" \
      "$( [ -f "$rpt" ] && rpt_code | grep -o 'endswith("GXemul>")' | wc -l || echo missing)" "5"

PLOG=$LOGDIR/pmax.ptylog
ALOG=$LOGDIR/arc.ptylog
[ -f "$PLOG" ] && [ -f "$ALOG" ] || \
    gate_skip "no logs from this run -- gate 4 must run first (it publishes them here)"

# ---- positive control --------------------------------------------------
# Without this the gate cannot tell "nothing went wrong" from "nothing happened".
# The floor is MEASURED, not guessed. A healthy run produces about 4,600 bytes on pmax
# (a plain serial console) and about 1,195,000 on arc (a VGA text console that repaints
# differentially, so it re-emits the screen constantly). An earlier draft used a single
# 20,000-byte floor for both and failed pmax on a perfectly good boot -- a false red, which
# is how gates get switched off. 2,000 is comfortably below the smaller rig and still far
# above the "empty or truncated file" case this control exists to catch.
for pair in "pmax:$PLOG" "arc:$ALOG"; do
    lab=${pair%%:*}; f=${pair##*:}
    check_min "$lab: log is substantial"   "$(wc -c < "$f")" 2000
done
# pmax sets the 8th bit on every console character; arc repaints differentially. Strip the
# high bit for pmax and accept either the raw arc log or gate 4's screen rebuild.
check "pmax: log proves a real boot (uid=0)" \
      "$(tr '\200-\377' '\000-\177' < "$PLOG" | grep -qa 'uid=0(root)' && echo yes || echo no)" "yes"
check "arc: log proves a real boot (uid=0)" \
      "$( { grep -qa 'uid=0(root)' "$ALOG" || grep -qa 'uid=0(root)' "$LOGDIR/arc.screen" 2>/dev/null; } && echo yes || echo no)" "yes"
echo

# ---- markers that must be ZERO -----------------------------------------
# Every pattern below was verified to exist as an emittable string in src/. Three did NOT
# survive that check and were removed rather than left in place looking like coverage:
#   'FIFO underrun'        -- 0 sites. The real string is 'FIFO overrun' (4 sites).
#   'INSTR: unimplemented' -- 0 sites. The token 'INSTR:' is in no format string at all;
#                             the real dyntrans marker is 'could not find physical'.
#   '{ asc: data in'       -- exists, but is NOT distress. See the bounded list below.
PATTERNS='panic
FATAL
zero-length
FIFO overrun
short DATA_IN DMA
short DATA_OUT DMA
unimplemented format
could not find physical'

printf "  %-28s %8s %8s\n" "marker" "pmax" "arc"
while IFS= read -r pat; do
    [ -n "$pat" ] || continue
    p=$(count "$PLOG" "$pat")
    a=$(count "$ALOG" "$pat")
    printf "  %-28s %8s %8s\n" "$pat" "$p" "$a"
    check "pmax clean: $pat" "$p" "0"
    check "arc  clean: $pat" "$a" "0"
done <<EOF
$PATTERNS
EOF
echo

# ---- the OTHER rigs' logs ----------------------------------------------
# This gate used to read only the two MIPS pty logs, so a panic in the m88k or SuperH
# guest left it green while the README claimed "any boot log". Gate 5's logs are scanned
# here too when they exist -- they are the newer, less-exercised rigs, which is exactly
# where a distress marker is most likely to be informative.
for rig in luna88k landisk; do
    rlog=$LOGDIR/drive_$rig.log
    [ -f "$rlog" ] || { note "$rig: no log from this run (gate 5 did not run it)"; continue; }
    while IFS= read -r pat; do
        [ -n "$pat" ] || continue
        c=$(count "$rlog" "$pat")
        [ "$c" != 0 ] && printf "  %-20s %-28s %s\n" "$rig" "$pat" "$c"
        check "$rig clean: $pat" "$c" "0"
    done <<EOF
$PATTERNS
EOF
done
echo

# ---- markers with a KNOWN NON-ZERO baseline ----------------------------
# '{ asc: data in, lenIn=.. lenIn2=.. }' (dev_asc.c:417) fires whenever a SCSI target has
# fewer bytes ready than the guest asked for. That is an ordinary occurrence -- measured
# at 1 on pmax and 5 on arc across a healthy OpenBSD 2.2 boot -- so demanding zero was
# simply wrong, and this gate failed on it the first time it ran.
#
# It is still worth watching, because the failure mode that matters is a FLOOD: round 40
# found #265's own diagnostic firing on every healthy boot, and that showed up only as a
# marker count. So the assertion is a CEILING rather than an equality -- generous enough
# that ordinary boot-to-boot variation cannot trip it, tight enough that a per-transfer
# flood will.
printf "  %-28s %8s %8s   %s\n" "bounded marker" "pmax" "arc" "ceiling"
BOUNDED_CEILING=50
for pat in '{ asc: data in'; do
    p=$(count "$PLOG" "$pat")
    a=$(count "$ALOG" "$pat")
    printf "  %-28s %8s %8s   %s\n" "$pat" "$p" "$a" "$BOUNDED_CEILING"
    check "pmax not flooding: $pat" "$([ "$p" -le "$BOUNDED_CEILING" ] && echo ok || echo FLOOD)" "ok"
    check "arc  not flooding: $pat" "$([ "$a" -le "$BOUNDED_CEILING" ] && echo ok || echo FLOOD)" "ok"
done

gate_end
exit $?
