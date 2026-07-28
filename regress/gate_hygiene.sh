#!/bin/bash
# GATE 5 -- no distress markers in the boot logs.
#
# Cheap, and it has caught real regressions: round 40 found that #265's own diagnostic
# flooded the log on a healthy boot, and that #261 was listing a subsystem it had not
# actually armed. Neither changed a pass/fail count -- both showed up only as marker counts.
#
# READS THE RAW PTY LOGS ON PURPOSE. fatal() and debugmsg() output is not guest console
# output; it goes straight to stdout and interleaves into the pty stream, and the arc
# screen reconstruction that gate 3 needs for GUEST tokens actively garbles it. Measured:
# '{ asc: data in' reads 0 from the arc screen rebuild and 5 from the raw log.
#
# TWO WAYS THIS GATE USED TO PASS WITHOUT PROVING ANYTHING, both now closed:
#
#  * EMPTY LOGS. It checked only that the files existed. `: > /tmp/pD.log` made 20 checks
#    go green -- two empty files certifying a clean boot. There is now a POSITIVE CONTROL:
#    each log must be substantial AND contain the guest's own uid=0(root), so absence of
#    distress is only counted when presence of a real boot is proved.
#  * STALE LOGS. Everything lives in /tmp and survives until reboot, so running this gate
#    alone -- or after gate 3 skipped -- graded yesterday's logs, produced by a binary that
#    no longer exists. Gate 3 now deletes them first and copies them into $LOGDIR when it
#    finishes; this gate reads THOSE copies, which only exist if gate 3 actually ran.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

gate_begin "log-hygiene"

PLOG=$LOGDIR/pmax.ptylog
ALOG=$LOGDIR/arc.ptylog
[ -f "$PLOG" ] && [ -f "$ALOG" ] || \
    gate_skip "no logs from this run -- gate 3 must run first (it publishes them here)"

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
# high bit for pmax and accept either the raw arc log or gate 3's screen rebuild.
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
# guest left it green while the README claimed "any boot log". Gate 4's logs are scanned
# here too when they exist -- they are the newer, less-exercised rigs, which is exactly
# where a distress marker is most likely to be informative.
for rig in luna88k landisk; do
    rlog=$LOGDIR/drive_$rig.log
    [ -f "$rlog" ] || { note "$rig: no log from this run (gate 4 did not run it)"; continue; }
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
