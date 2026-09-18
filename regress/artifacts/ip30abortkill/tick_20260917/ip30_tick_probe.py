#!/usr/bin/env python3
"""ip30 TICK-ROW BUILDABILITY MEASUREMENT.

QUESTION: is the FOURTH abort() -- dev_sgi_ip30.c:74-78, inside DEVICE_TICK -- reachable
from a STEPPING probe, i.e. without free-run?

    DEVICE_TICK(sgi_ip30) { d->reg_0x20000 += 1000;
        if (d->imask0 & ((int64_t)1<<50)) { fatal(...); abort(); } }

Two panel seats disagreed and their answers COMBINE:
  agy   -- reachable by `step 70000': tickshift 16 => a tick every 65536 cycles, no free-run.
  codex -- stepping alone is insufficient; the guarded BRANCH must be exercised, i.e.
           imask0 bit 50 must be SET first.

*** THE THING NEITHER SEAT SAID, read out of machine.c before this probe was written: ***
`machine_add_tickfunction' sets `ticks_till_next[n] = 0' (machine.c:354) while
`ticks_reset_value[n] = 1 << tickshift' (:355).  machine_run() then does
`ticks_till_next[te] -= single_step ? 1 : N_SAFE_DYNTRANS_LIMIT' and fires while <= 0
(:726-738).  So the FIRST machine_run() of a session drives it to -1 and FIRES EVERY TICK
FUNCTION IMMEDIATELY.  Prediction under test: `step 1' suffices, not `step 70000'.

*** BIT 50 CANNOT BE SET BY `sw'. ***  imask0 is uint64_t and `case 0x10000' assigns the
whole of it from memory_readmax64(cpu, data, len).  A 4-byte store gives idata < 2^32, so
bit 50 stays clear whatever the guest writes.  The store must be `sd' (8 bytes).  That is
why the `sd rt' row exists: without it a negative tick row would be ambiguous between
"the tick is unreachable" and "my store never set the bit".

POLARITY: WANT = POST-FIX CORRECT, the house convention.  A kill row wants `alive'; its
FAIL is the reproduction.

Controls, per witness-ladder clause (ii) -- rung 3 owes BOTH, one is not enough:
    live    LIVENESS    a known value planted in RAM returns through a guest load
    devsig  DEVICE-SIG  case 0x20 answers 0x80010000, which RAM cannot produce

AND the discriminating negative control the question actually needs:
    tick49 s70k   bit 49 set instead of 50, stepped just as far.  If THAT dies too, the
                  death is not attributable to bit 50 and no tick row is buildable.
    tick0  s70k   nothing stored at all, stepped just as far.
"""
import os
import pty
import re
import select
import signal
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul"
HERE = os.path.dirname(os.path.abspath(__file__))
DUMMY = os.path.join(HERE, "ip30_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

CODE = 0x80001000
SENTINEL = 0x5A5A5A5A
RAMPLANT = 0x11223344

BASE = 0xFFFFFFFFAFF00000
A_BANKCFG = BASE + 0x00020
A_IMASK0 = BASE + 0x10000
A_RAM = 0xFFFFFFFF80002000

OP_LW_V0_AT = 0x8C220000       # lw   $v0, 0($at)     op 0x23
OP_LD_V0_AT = 0xDC220000       # ld   $v0, 0($at)     op 0x37  rs=at(1) rt=v0(2)
OP_SD_T0_A3 = 0xFCE80000       # sd   $t0, 0($a3)     op 0x3f  rs=a3(7) rt=t0(8)
OP_B_SELF = 0x1000FFFF
OP_NOP = 0x00000000

BIT50 = 1 << 50
BIT49 = 1 << 49

rows = []


def row(name, got, want, note=""):
    rows.append((name, str(got), str(want), note))


def session(cmds, settle=2.0, spin=2.5, cmd_wait=0.35, last_wait=None):
    """One fresh process per scored row.  Returns (transcript, alive).

    The waitpid form is COPIED from regress/artifacts/ip30abortkill/ip30_abort_probe.py,
    not reinvented: rd() returns immediately on EOF, so `spin' is SKIPPED exactly when the
    child dies, and a single waitpid(WNOHANG) then lands ~0 s after EOF while the kernel is
    still writing the core -- reporting "still running" and turning a live host death GREEN.
    """
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip30", "-M", "64",
                       "0x%x:" % CODE + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t, until_prompt=False):
        """Read for t seconds.  With until_prompt, ALSO return as soon as the debugger
        prompt comes back -- so a long `step N' that SURVIVES does not burn the whole
        timeout, while one that DIES still returns instantly on EOF."""
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            if until_prompt and buf.rstrip(" ").endswith("GXemul>"):
                return
            try:
                r, _, _ = select.select([fd], [], [], 0.1)
            except OSError:
                return
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return
            if not d:
                return
            buf += d.decode("utf-8", "replace")

    rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode())
        except OSError:
            break
        if last_wait is not None and i == len(cmds) - 1:
            rd(last_wait, until_prompt=True)
        else:
            rd(cmd_wait)
    rd(spin)

    alive = True
    deadline = time.time() + 12.0
    while time.time() < deadline:
        try:
            wpid, status = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            alive = False
            status = None
            break
        if wpid == pid:
            alive = False
            break
        time.sleep(0.05)
    sig = None
    if not alive and status is not None:
        if os.WIFSIGNALED(status):
            sig = "SIG%d" % os.WTERMSIG(status)
        elif os.WIFEXITED(status):
            sig = "exit%d" % os.WEXITSTATUS(status)
    if alive:
        try:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
        except OSError:
            pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf, alive, sig


def plant(ops, at=CODE):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at]


def guest_load(addr, op=OP_LW_V0_AT):
    return (["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + plant([op])
            + ["step 1", "print v0"])


def guest_store64(addr, val, nsteps=1):
    """sd $t0,0($a3) then keep stepping in a b-self loop for nsteps-1 more machine_run()s."""
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + plant([OP_SD_T0_A3]) + ["step %d" % nsteps]


def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-fA-F]+)" % reg, t)
    return m.group(1) if m else "ABSENT"


def as_int(s):
    try:
        return int(s, 16)
    except Exception:
        return None


# ------------------------------------------------------------------ CONTROL set
t, alive, _ = session(["put w 0x%x, 0x%08x" % (A_RAM & 0xFFFFFFFF, RAMPLANT)]
                      + guest_load(A_RAM))
row("live", (printed(t, "v0") if alive else "died"), "0x%x" % RAMPLANT,
    "LIVENESS: a planted RAM value returns through a real guest load.")

t, alive, _ = session(guest_load(A_BANKCFG))
row("devsig", (printed(t, "v0") if alive else "died"), "0xffffffff80010000",
    "DEVICE-SIGNATURE: case 0x20 answers 0x80010000, sign-extended by lw. RAM cannot "
    "produce it. One control is not enough.")

# ------------------------------------------------------------------ does `sd' reach imask0?
#  Uses bit 49, deliberately NOT bit 50, so this row cannot arm the death it is qualifying.
t, alive, _ = session(["a3=0x%x" % A_IMASK0, "t0=0x%x" % BIT49] + plant([OP_SD_T0_A3])
                      + ["step 1", "at=0x%x" % A_IMASK0, "v0=0x%x" % SENTINEL]
                      + plant([OP_LD_V0_AT]) + ["step 1", "print v0"])
sd_got = printed(t, "v0") if alive else "died"
row("sd rt", ("0x%x" % as_int(sd_got)) if as_int(sd_got) is not None else sd_got,
    "0x%x" % BIT49,
    "QUALIFIER: an 8-byte guest store must reach imask0 with its HIGH bits intact. `sw' "
    "cannot -- memory_readmax64(len=4) caps idata below 2^32, so bit 50 is unsettable by a "
    "word store. Without this row a negative tick row is ambiguous.")

# ------------------------------------------------------------------ THE TICK ROWS
#  Prediction from machine.c:354 -- ticks_till_next starts at 0, so machine_run #1 fires
#  every tick function.  step 1 should be enough.
LADDER = [("s1", 1), ("s2", 2), ("s70k", 70000)]
for tag, n in LADDER:
    lw = 90.0 if n > 1000 else 0.35
    t, alive, sig = session(guest_store64(A_IMASK0, BIT50, n), last_wait=lw)
    txt = "yes" if "IP30 legacy interrupt rewrite" in t else "no"
    row("tick50 " + tag, ("alive" if alive else "DEAD(%s)" % (sig or "?")), "alive",
        "sd 1<<50 to imask0 (case 0x10000 ACCEPTS it), then step %d. The tick's guard is "
        "then TRUE. WANT=alive is post-fix-correct; a FAIL here IS the reproduction." % n)
    row("tick50 " + tag + " txt", txt, "yes",
        "DIAGNOSIS ONLY, never half the trigger.")

# ------------------------------------------------------------------ PERIODICITY
#  `step 1' works because ticks_till_next STARTS at 0 (machine.c:354), so machine_run #1
#  fires every tick function.  That could be dismissed as a startup artifact, so these two
#  rows measure the SECOND tick: burn 10 machine_run()s on NOPs first (consuming tick #1),
#  THEN arm bit 50.  Arithmetic: after run #1 the counter is 65535 and run #k leaves
#  65537-k, so tick #2 lands at run #65537 -- i.e. 65527 steps after a 10-step warmup.
LATE_WARM = ["at=0x0", "v0=0x0"] + plant([OP_NOP]) + ["step 10"]
ARM = ["a3=0x%x" % A_IMASK0, "t0=0x%x" % BIT50] + plant([OP_SD_T0_A3])

t, alive, sig = session(LATE_WARM + ARM + ["step 1"])
row("late s1", ("alive" if alive else "DEAD(%s)" % (sig or "?")), "alive",
    "PERIODICITY (a): tick #1 already consumed by a 10-step warmup, THEN bit 50 armed, "
    "then ONE step. The guard is true but the tick is not due, so this must survive. If it "
    "dies, `step 1' above was not measuring the tick at all.")

t, alive, sig = session(LATE_WARM + ARM + ["step 70000"], last_wait=90.0)
row("late s70k", ("alive" if alive else "DEAD(%s)" % (sig or "?")), "alive",
    "PERIODICITY (b): same warmup and arming, 70000 steps. Reaches tick #2 at run #65537, "
    "so a guest arming bit 50 at ANY time dies within 65536 cycles -- not a startup artifact.")

# ------------------------------------------------------------------ DISCRIMINATING NEGATIVES
t, alive, sig = session(guest_store64(A_IMASK0, BIT49, 70000), last_wait=90.0)
row("tick49 s70k", ("alive" if alive else "DEAD(%s)" % (sig or "?")), "alive",
    "*** THE DISCRIMINATOR. *** Same store, same step count, BIT 49 instead of 50. If this "
    "also dies, the death is not attributable to the guard and no tick row is buildable.")

t, alive, sig = session(plant([OP_NOP]) + ["step 70000"], last_wait=90.0)
row("tick0 s70k", ("alive" if alive else "DEAD(%s)" % (sig or "?")), "alive",
    "No store at all, stepped just as far. Pins that 70000 steps on this machine is itself "
    "survivable -- so a death above is the GUARD, not the stepping.")

# ------------------------------------------------------------------ report
CONTROL = "OK"
for nm, got, want, _ in rows:
    if nm in ("live", "devsig", "sd rt") and got != want:
        CONTROL = "DEAD"

print("ip30_tick_probe -- binary=%s machine=sgi/ip30" % BIN)
print("IP30TICK_CONTROL=%s" % CONTROL)
n_ok = 0
for nm, got, want, note in rows:
    ok = (got == want)
    n_ok += 1 if ok else 0
    print("  %-16s got=%-14s want=%-14s %s  %s" % (nm, got, want, "ok" if ok else "FAIL", note[:66]))
print("IP30TICK_RESULT=%d/%d" % (n_ok, len(rows)))
if CONTROL == "DEAD":
    print("  *** SETUP FAILED -- the vehicle is not the vehicle. NOT 'no defect'. ***")
print("IP30TICK_DONE")
