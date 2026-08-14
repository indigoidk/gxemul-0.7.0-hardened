#!/bin/bash
# GATE 4 -- the two primary MIPS rigs boot OpenBSD 2.2 to a root shell.
#
# These rigs are the reason the fork's priorities are what they are: pmax (DECstation
# 3MAX, R3000) and arc (Acer PICA, R4000) are the OSes the corrections are aligned to, so
# a break here outranks anything else in the harness.
#
# Runs the rigs SEQUENTIALLY, never concurrently -- concurrent rigs have produced a
# contaminated reading before.
#
# Two console quirks, both of which have silently produced false readings:
#
#  * pmax sets the 8th bit on every console character, so the log must be de-garbled
#    before grepping or the guest tokens are invisible.
#  * arc's VGA console repaints DIFFERENTIALLY. A raw grep of the pty stream misses
#    tokens that were printed underneath a similar token, so guest output must be read
#    from a RECONSTRUCTED screen. Emulator diagnostics are the opposite case: fatal() and
#    debugmsg() go straight to stdout and are garbled BY the screen rebuild, so those are
#    counted from the raw log. Gate 6 does that half.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/lib.sh"

S=$ROOT/_scratchpad
PMAX_RIG=$ROOT/gxemul_pmax_rig
ARC_RIG=$ROOT/gxemul_arc_rig

gate_begin "mips-rigs"
need_file "$PMAX_RIG/boot_login.sh" "$ARC_RIG/boot_login_arc_r23.sh" "$S/r49_screen.py"
need_exec "$ROOT/build/gxemul" "$ARC_RIG/gxsec-gxemul"

echo "  binaries under test:"
ls -la "$ROOT/build/gxemul" "$ARC_RIG/gxsec-gxemul" | awk '{print "       ",$5,$6,$7,$8,$9}'
echo

# Delete the pty logs BEFORE the rigs run. They live in /tmp and survive until reboot, so
# a rig that fails to start would otherwise leave the previous run's logs in place and
# gate 6 would grade those -- output from a binary that no longer exists.
rm -f /tmp/pD.log /tmp/aD.log

# ---- pmax ----------------------------------------------------------------
note "pmax (DECstation 3MAX, R3000) -- OpenBSD 2.2"
( cd "$PMAX_RIG" && sh ./boot_login.sh ) > "$LOGDIR/pmax.out" 2>&1
PSTEP=$(grep -oE 'completed [0-9]+/[0-9]+ steps' "$LOGDIR/pmax.out" | tail -1)
check "pmax: harness steps" "${PSTEP:-none}" "completed 15/15 steps"

tr '\200-\377' '\000-\177' < /tmp/pD.log > "$LOGDIR/pmax.degarbled"
check "pmax: reached uid=0(root)" \
      "$(grep -qa 'uid=0(root)'  "$LOGDIR/pmax.degarbled" && echo yes || echo no)" "yes"
check "pmax: rig token present" \
      "$(grep -qa 'RIG_TOKEN_END' "$LOGDIR/pmax.degarbled" && echo yes || echo no)" "yes"
grep -a -m1 'OpenBSD'     "$LOGDIR/pmax.degarbled" | sed 's/^/       /'
grep -a -m1 'uid=0(root)' "$LOGDIR/pmax.degarbled" | sed 's/^/       /'
echo

# ---- arc -----------------------------------------------------------------
note "arc (Acer PICA, R4000) -- OpenBSD 2.2"
( cd "$ARC_RIG" && sh ./boot_login_arc_r23.sh ) > "$LOGDIR/arc.out" 2>&1
ASTEP=$(grep -oE 'completed [0-9]+/[0-9]+ steps' "$LOGDIR/arc.out" | tail -1)
check "arc: harness steps" "${ASTEP:-none}" "completed 13/13 steps"

python3 "$S/r49_screen.py" /tmp/aD.log > "$LOGDIR/arc.screen" 2>/dev/null
check "arc: reached uid=0(root)" \
      "$(grep -qa 'uid=0(root)'   "$LOGDIR/arc.screen" && echo yes || echo no)" "yes"
check "arc: rig token present" \
      "$(grep -qa 'ARC_TOKEN_END' "$LOGDIR/arc.screen" && echo yes || echo no)" "yes"
grep -a -m1 'OpenBSD'     "$LOGDIR/arc.screen" | sed 's/^/       /'
grep -a -m1 'uid=0(root)' "$LOGDIR/arc.screen" | sed 's/^/       /'
if grep -qa 'uid=0(root)' /tmp/aD.log; then
    note "(raw pty log also had it this run)"
else
    note "(raw pty log MISSED it -- differential repaint, exactly as expected)"
fi

# Publish the raw pty logs for gate 6. It reads THESE copies rather than /tmp, so that a
# run in which this gate skipped or died cannot leave gate 6 grading stale output from a
# binary that no longer exists.
cp -f /tmp/pD.log "$LOGDIR/pmax.ptylog" 2>/dev/null
cp -f /tmp/aD.log "$LOGDIR/arc.ptylog"  2>/dev/null

gate_end
exit $?
