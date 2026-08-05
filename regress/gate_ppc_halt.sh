#!/bin/bash
# GATE 15 -- legal PowerPC floating-point encodings must not stop the emulator.
#
# What this protects
# -----------------
# Both floating-point blocks in the PowerPC translator end with `default: goto bad;`,
# and `bad:` is the shared label in cpu_dyntrans.c that prints "UNIMPLEMENTED instruction"
# and sets `cpu->running = 0`. That is not a program exception the guest can handle -- it
# stops the whole machine. #326 measured 24 legal encodings doing exactly that and decoded
# twelve of them; this gate holds the line and records the rest.
#
# The one that mattered most was not an exotic instruction. `if (rc) goto bad;` sat at the
# entry of BOTH the opcode-59 and opcode-63 blocks, so every RECORD FORM halted -- `fadd.`,
# `frsp.`, `fmr.`, `fadds.` -- including the record forms of instructions that worked
# perfectly with Rc=0. A compiler emits those whenever a floating-point result feeds a
# condition test.
#
# Why the control rows are load-bearing
# ------------------------------------
# Four rows drive instructions the decoder already handled. If one of those reads HALTED
# the rig is broken -- wrong machine, FP not enabled, bad code address -- and NO other row
# may be believed. This is not hypothetical: round 76 shipped an m88k probe whose second
# instruction was a placeholder, and every condition mask "halted", including the nine that
# actually worked. The control failing is what catches that.
#
# A halt is read off the dyntrans message, never off a memory marker. Round 80 learned
# that the hard way: a marker-only classifier cannot separate "the emulator stopped" from
# "the instruction ran and simply did not reach the store", and after a fix lands it
# reports every repaired row as still broken.
#
# The PEND rows
# -------------
# Twelve encodings still halt, on purpose, and the gate asserts that they DO -- so the
# count cannot quietly drift and the queue cannot quietly lie. Three groups, with
# different reasons, spelled out in the probe: fctid/fctidz/fcfid and fsqrt/fsqrts are
# 64-bit-only or outside the G4's instruction groups, so on this machine real silicon
# takes a program interrupt and the honest fix is the missing exception model, not an
# implementation; fres/frsqrte are estimates; and fcmpo/fnmadd/fnmsub/fmadds/fmsubs have
# no technical blocker at all and were left out for round size alone. That last group is
# recorded as such deliberately -- a queue entry that invents a blocker costs a future
# round the time to disprove it.
set -u
cd "$(dirname "$0")"
. ./lib.sh

gate_begin "gate 15: PowerPC FP encodings must not halt (#326)"

PMAX=${PMAX:-$ROOT/build/gxemul}
LOG=$LOGDIR/gate_ppc_halt.log

need_exec "$PMAX"
need_file "$IMAGES/netbsd401-macppc-GENERIC"
command -v python3 >/dev/null || gate_skip "python3 not available"

note "binary : $PMAX"
note "machine: macppc/G4, NetBSD kernel loaded so the machine constructs; never executed"
note "each row steps ONE instruction and classifies alive / HALTED / DEAD"

python3 ppc_halt_probe.py "$PMAX" "$IMAGES" > "$LOG" 2>&1 || true

if ! grep -q "PPC_HALT_RESULT=" "$LOG"; then
    note "probe produced no result line; last lines follow"
    tail -5 "$LOG" | sed 's/^/       /'
    gate_skip "probe did not complete"
fi

grep -E " ok$| FAIL$" "$LOG" | sed 's/^/       /'

ctrl=$(grep -o "PPC_HALT_CONTROL=[A-Z]*" "$LOG" | tail -1 | cut -d= -f2)
check "control rows prove the probe measures" "${ctrl:-missing}" "OK"

res=$(grep -o "PPC_HALT_RESULT=[0-9]*/[0-9]*" "$LOG" | tail -1 | cut -d= -f2)
got=${res%/*}; want=${res#*/}
check "rows run"     "$want" 28
check "rows correct" "$got"  "$want"

# Class counts, asserted rather than trusted: a gate whose rows are all PEND proves
# nothing was fixed, and one with no CTRL cannot tell a fix from a dead rig.
ctrls=$(grep -c " CTRL " "$LOG")
fixed=$(grep -c " FIXED " "$LOG")
pend=$(grep -c " PEND " "$LOG")
check "control rows present" "$ctrls" 4
check "rows fixed by #326+#344" "$fixed" 14
check "rows still pending"   "$pend"  10

# Named rows, so one site reverting cannot hide behind a total. The pattern demands TWO
# spaces after the name because the probe pads to a fixed column -- a name that is a
# prefix of another would otherwise match both rows and count 2 where it wants 1.
for v in "ctrl fadd" "ctrl fmr" "ctrl fctiwz" "ctrl mtfsf" \
         "fadd. (Rc=1)" "frsp. (Rc=1)" "fctiwz. (Rc=1)" "fmr. (Rc=1)" \
         "fadds. (Rc=1)" "mcrfs" "mtfsb0" "mtfsb1" "mtfsfi" "fctiw" \
         "fnabs" "fsel"; do
    n=$(count "$LOG" "^$v  .*ok$")
    check "  row: $v" "$n" 1
done

gate_end
