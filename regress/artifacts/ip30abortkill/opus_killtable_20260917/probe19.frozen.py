#!/usr/bin/env python3
"""ip30abortkill -- RUNG-3 REPRODUCTION ATTEMPT on unmodified `-E sgi -e ip30'.

TEST-FIRST: this exists BEFORE any edit, and it is run against the COMMITTED build.  It is a
WITNESS attempt, not a shipped detector -- if it reproduces, it becomes the witness; if it
cannot, the round proceeds documented-only WITH THE ATTEMPT RECORDED, which is a different
state from "did not think to ask" and must not render the same.

THE CLAIM UNDER TEST, from reading dev_sgi_ip30.c at HEAD:

    :127  case 0x10020  Set ISR    d->isr = idata;  fatal(...); abort();
    :135  case 0x10028  Clear ISR  d->isr &= ~idata; fatal(...); abort();
    :145  case 0x10030  ISR write arm             fatal(...); abort();
    :78   DEVICE_TICK              if (d->imask0 & (1<<50)) { fatal(...); abort(); }

`abort()` contains no `exit(', which is why three `exit(' sweeps of this queue walked past all
four.  *** AND `case 0x10020' HAS NO `writeflag' TEST AND RUNS `d->isr = idata' FIRST, with
idata initialised 0 and assigned only on writes -- so a guest LOAD is predicted to ZERO THE ISR
and THEN abort. ***  That asymmetry is why `kill 20 rd' and `kill 30 rd' are separate rows:
0x10030 IS writeflag-tested and its READ is predicted to be SERVICED.

WITNESS-LADDER CLAUSE (ii) -- rung 3 owes BOTH controls, because one is not enough (the
footbridge probe's first draft returned 0x0 everywhere WITH ITS RAM CONTROL GREEN):

    live    LIVENESS   -- a known value planted in RAM returns through a guest load
    devsig  DEVICE-SIG -- case 0x20 returns 0x80010000, a value RAM CANNOT produce
                          (dev_sgi_ip30.c `case 0x20:  odata = 0x80010000ULL;')

Clause (iii): the machine description and dispatch are COMMITTED AND UNMODIFIED.  No device_add
is introduced to reach the site -- `machine_sgi.c:417' already adds `sgi_ip30 addr=0x0ff00000'
and `:744' advertises the subtype.

POLARITY: **WANT IS POST-FIX CORRECT**, the house convention -- so a kill row wants `alive' and
its PRE-FIX FAIL *IS* the reproduction.  Written want=DEAD first, which scored a tidy 9/9 on the
defect and would have gone RED after a correct fix, reading as though the fix broke something.

*** ORACLE POLARITY -- EOF ALONE IS THE KILL. ***  The text is DIAGNOSIS, not half the trigger.
A build that still abort()s with a REWORDED message gives EOF and no matching text; an
EOF-AND-text oracle would never fire and would certify a live defect GREEN.  That lesson was
bought on the ARM MSR spec this same day and is applied here rather than re-learned.
"""
import os
import pty
import re
import select
import signal
import sys
import time

BIN = sys.argv[1] if len(sys.argv) > 1 else "../../../build/gxemul"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"

#  The stub is a GENERATED artefact, never committed (top-level regress/*.bin is NEVER STAGE).
#  All 11 top-level probes that reference such a stub create it if absent; this does the same,
#  so the probe runs on a fresh clone.
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ip30_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

CODE = 0x80001000
SENTINEL = 0x5a5a5a5a
RAMPLANT = 0x11223344

#  KSEG1 (uncached), sign-extended the way the file's own :113 comment prints it:
#  "Address: 0xffffffffaff10018".  base 0x0ff00000 -> 0xffffffffaff00000.
BASE = 0xFFFFFFFFAFF00000
A_BANKCFG = BASE + 0x00020     # case 0x20    -> 0x80010000, the DEVICE SIGNATURE
A_IMASK0 = BASE + 0x10000      # case 0x10000 -> implemented r/w
A_R10018 = BASE + 0x10018      # case 0x10018 -> implemented r/w
A_SETISR = BASE + 0x10020      # case 0x10020 -> PREDICTED KILL, and no writeflag test
A_CLRISR = BASE + 0x10028      # case 0x10028 -> PREDICTED KILL, and no writeflag test
A_ISR = BASE + 0x10030         # case 0x10030 -> writeflag-TESTED; READ predicted SERVICED
A_C20000 = BASE + 0x20000    # case 0x20000 -> implemented r/w counter
A_C30000 = BASE + 0x30000    # case 0x30000 -> implemented r/w
A_RAM = 0xFFFFFFFF80002000     # KSEG0 RAM, for the liveness control

OP_LW_V0_AT = 0x8C220000       # lw   $v0, 0($at)
OP_SW_T0_A3 = 0xACE80000       # sw   $t0, 0($a3)
#  *** 64-BIT FORMS ARE NOT OPTIONAL FOR imask0.  `case 0x10000' does
#  `d->imask0 = idata' with `idata = memory_readmax64(cpu, data, len)', so a 4-BYTE
#  `sw' CAPS idata BELOW 2^32 AND BIT 50 CAN NEVER BE SET.  Measured: sw 0xffffffff
#  + 70000 steps -> ALIVE.  A tick row built with OP_SW_T0_A3 would arm NOTHING,
#  stay alive, and score GREEN ON A LIVE HOST DEATH. ***
OP_SD_T0_A3 = 0xFCE80000       # sd   $t0, 0($a3)   -- REQUIRED to reach bit 50
OP_LD_V0_AT = 0xDC220000       # ld   $v0, 0($at)   -- its readback
OP_B_SELF = 0x1000FFFF         # b    .
OP_NOP = 0x00000000

rows = []


def row(name, got, want, note=""):
    rows.append((name, str(got), str(want), note))


def session(cmds, settle=2.0, spin=2.5):
    """One fresh process per scored row.  Returns (transcript, alive)."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip30", "-M", "64",
                       "0x%x:" % CODE + DUMMY])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
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
    for c in cmds:
        try:
            os.write(fd, (c + "\n").encode())
        except OSError:
            break
        rd(0.35)
    rd(spin)

    #  *** POLL, NEVER SAMPLE ONCE.  MEASURED 2026-09-17, and the first run of this probe
    #  reported `alive' for a process that SIGABRT'd 0.6 s later. ***
    #  `rd()' RETURNS IMMEDIATELY ON EOF rather than waiting out its timeout, so `spin' --
    #  which exists precisely to give a dying child time to die -- is SKIPPED EXACTLY WHEN THE
    #  CHILD DIES.  A single waitpid(WNOHANG) then lands ~0 s after EOF while the kernel is
    #  still writing a 6 MB core, reports "still running", and THE KILL ROW GOES GREEN ON A
    #  LIVE HOST DEATH.  That is the false-green this probe exists to refuse.
    alive = True
    deadline = time.time() + 12.0
    while time.time() < deadline:
        try:
            wpid, status = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            alive = False
            break
        if wpid == pid:
            alive = False
            break
        time.sleep(0.05)
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
    return buf, alive


def run_ops(ops, at=CODE):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]


def guest_load(addr):
    """A REAL guest instruction through real decode and real memory_rw -- rung 3.
    NOT `dump': all four ip30 registrations are DM_DEFAULT, so dump BYPASSES the handler
    and would prove nothing about the device at all."""
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT]) + ["print v0"]


def guest_store(addr, val):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([OP_SW_T0_A3])


def guest_store64(addr, val):
    """A 64-BIT store.  The ONLY way to reach imask0 bit 50 -- see OP_SD_T0_A3."""
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([OP_SD_T0_A3])


def guest_load64(addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LD_V0_AT]) + ["print v0"]


def printed_last(t, reg):
    """*** THE LAST `print <reg>', NOT THE FIRST. ***  L1 repair 2026-09-17.

    `printed()' uses `re.search', which returns the FIRST match.  A row that issues
    MORE THAN ONE guest_load therefore reads the WRONG load's value, silently -- and
    `isr keep' does three commands ending in the read-back it actually wants.

    PRE-FIX THE BUG WAS INVISIBLE because the row's seeding write aborted and the row
    read `died'; the construction defect only surfaced once the fix let the session
    survive.  A row that cannot pass even on a correct fix is vacuous, so this is L1
    construction, repaired in-round rather than filed."""
    m = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return m[-1] if m else "ABSENT"


def printed(t, reg):
    """`print <reg>' emits a BARE 0x... -- `reg' is the command that carries the `r0 = ' prefix.
    Copied from regress/lca_isalane_probe.py rather than invented."""
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "ABSENT"


# ------------------------------------------------------------------ CONTROL=DEAD set
#  If any of these reds the vehicle is not the vehicle, and NO kill row may be scored.
t, alive = session(["put w 0x%x, 0x%08x" % (A_RAM & 0xFFFFFFFF, RAMPLANT)]
                   + guest_load(A_RAM))
live_got = printed(t, "v0") if alive else "died"
row("live", live_got, "0x%x" % RAMPLANT,
    "LIVENESS: a known value planted in RAM returns through a guest load. If this reds, plant "
    "or step or print never executed and nothing below is evidence.")

t, alive = session(guest_load(A_BANKCFG))
devsig_got = printed(t, "v0") if alive else "died"
row("devsig", devsig_got, "0xffffffff80010000",
    "DEVICE-SIGNATURE: case 0x20 answers 0x80010000 and `lw' SIGN-EXTENDS it to "
    "0xffffffff80010000 on this 64-bit R10000 -- a value RAM cannot produce. One control is "
    "NOT enough: the footbridge probe's first draft returned 0x0 everywhere with its RAM "
    "control green.")

# ------------------------------------------------------------------ accept side
t, alive = session(guest_store(A_R10018, 0xDEADBEEF) + guest_load(A_R10018))
row("acc 18", (printed(t, "v0") if alive else "died"), "0xffffffffdeadbeef",
    "case 0x10018 is IMPLEMENTED r/w (the PROM complains without it). An accept control, and "
    "the de-escalation clause's accept row for this arm.  *** THE WANT IS SIGN-EXTENDED: `lw' sign-extends on this 64-bit R10000, so 0xdeadbeef comes back as 0xffffffffdeadbeef.  My first oracle wanted the truncated form and reddened a CORRECT device -- the apparatus was wrong, not the model. ***")

t, alive = session(guest_load(A_ISR))
row("acc 30 rd", ("alive" if alive else "died"), "alive",
    "case 0x10030 IS writeflag-tested, so its READ returns d->isr and must NOT die. This is "
    "the row that proves the three arms are NOT uniform.")

#  ---------------------------------------------------------------- de-escalation accept rows
#  A fatal->survive fix DELETES the accidental tripwire that made guard growth self-announcing,
#  so the detector shipping WITH the fix owes the ACCEPT SIDE of every predicate that used to
#  gate death.  These are owed under EVERY candidate member, which is why they are written
#  before the disposition is settled -- they cannot be wasted work.
#  *** THIS ROW EXPECTED A COUNTER NOT TO COUNT, SO IT WAS RED ON A CORRECT BUILD.  L1
#  construction repair, 2026-09-17, found by running the pre-fix baseline. ***
#
#  Measured: stored 0x1234, read back 0x161c -- and 0x161c - 0x1234 = 0x3e8 = 1000 EXACTLY,
#  which is `d->reg_0x20000 += 1000' in DEVICE_TICK.  The DEVICE was right and the ROW was
#  wrong: as written it manufactured a phantom failure on a correct build, so it could never
#  signal the defect this probe exists for.  (The file's own `/*  A counter  */' comment on
#  case 0x20000 says so; the access arm alone reads like a plain r/w register.)
#
#  THE REPAIRED ORACLE IS STRICTLY STRONGER THAN THE ONE IT REPLACES.  The counter is always
#  a multiple of 1000 (it starts at 0 and only ever += 1000), and 0x1234 = 4660 is NOT a
#  multiple of 1000 -- so:
#      store LANDED    -> readback - 0x1234 == N*1000, an exact multiple
#      store LOST      -> readback is some M*1000, and M*1000 - 4660 is NEVER a multiple
#  The row therefore pins THAT THE STORE REACHED reg_0x20000, which the old literal compare
#  only did by accident on a tickless run, while tolerating any number of ticks.
t, alive = session(guest_store(A_C20000, 0x1234) + guest_load(A_C20000))
_v20000 = printed(t, "v0")
_got20000 = "ABSENT"
if alive and _v20000 != "ABSENT":
    _d20000 = int(_v20000, 16) - 0x1234
    _got20000 = ("stored+N*1000" if (_d20000 >= 0 and _d20000 % 1000 == 0)
                 else _v20000)
row("acc 20000", (_got20000 if alive else "died"), "stored+N*1000",
    "case 0x20000 is writeflag-tested r/w AND is incremented 1000 per DEVICE_TICK, so the "
    "oracle pins that the STORE LANDED (the residue is an exact multiple of the tick stride) "
    "rather than that a counter stood still.  A neighbour that must keep working.")

t, alive = session(guest_store(A_C30000, 0x5678) + guest_load(A_C30000))
row("acc 30000", (printed(t, "v0") if alive else "died"), "0x5678",
    "case 0x30000, writeflag-tested r/w. Second neighbour.")

#  *** THIS IS **THE** ACCEPT ROW FOR THE TICK, not merely a neighbour: the write to imask0 is
#  precisely what used to ARM the host death at :78, so it is the predicate that gated death. ***
#  *** THE SENTENCE THAT STOOD HERE WAS MEASURED FALSE THE SAME DAY.  It read: "Safe under
#  `step' ONLY: tickshift is 16, so the tick fires every 65536 cycles and a handful of steps
#  cannot reach it."  A HANDFUL OF STEPS REACHES IT ON THE FIRST ONE. ***
#  `machine_add_tickfunction' sets `ticks_till_next[n] = 0' (machine.c:354) while
#  `ticks_reset_value[n] = 1 << tickshift' (:355), and `machine_run()' decrements then fires
#  while <= 0 -- so THE FIRST machine_run OF ANY SESSION FIRES EVERY TICK FUNCTION.
#  THIS ROW IS STILL SAFE -- BUT ONLY ONE OF THE TWO REASONS BELOW IS LOAD-BEARING, AND
#  SAYING OTHERWISE INVERTS A HAZARD INTO A SAFETY PROPERTY (Fable adjudication, same day):
#  *** REASON (2) MISDIRECTS.  This row's value is 1<<18 = 0x40000, which has NO high bits
#  at ANY store width -- so width is irrelevant to THIS row, and reason (1) alone carries
#  it.  Written as a pair, `sw cannot set bit 50' reads as a general safety invariant for
#  imask0, AND IT IS NOT ONE: THE DEATH IS REACHABLE, BY `sd 1<<50'. ***
#  Keep both facts, but know which is which: (1) is why this row is safe; (2) is why a
#  COPY of it would be inert as a kill row.  They are a safety reason and a HAZARD.
#    (1) it writes bit 18, not bit 50, so the guarded branch is never armed; and
#    (2) *** IT USES `sw', AND A 4-BYTE STORE CANNOT SET BIT 50 AT ALL. ***  `case 0x10000'
#        does `d->imask0 = idata' with `idata = memory_readmax64(cpu, data, len)', so a
#        word store caps idata below 2^32.  ARMING THE TICK REQUIRES `sd' (0xFCE80000).
#  *** AND THAT IS A FALSE-GREEN TRAP FOR THE NEXT PERSON: `OP_SW_T0_A3' IS THE ONLY STORE
#  HELPER IN THIS FILE, so a tick row copy-pasted from here would arm NOTHING, stay ALIVE,
#  and score GREEN ON A LIVE HOST DEATH. ***  Measured: sw 0xffffffff + 70000 steps -> alive.
#  The tick witness lives in tick_20260917/ip30_tick_probe.py, which uses `sd'.
t, alive = session(guest_store(A_IMASK0, 1 << 18) + guest_load(A_IMASK0))
row("acc imask", (printed(t, "v0") if alive else "died"), "0x40000",
    "case 0x10000 (imask0) accepts and reads back. THE accept row for the tick predicate -- "
    "bit 18 is used, NOT bit 50, so the row does not arm the death it is pinning.")

# ------------------------------------------------------------------ the kill rows
#  EOF ALONE => RED.  The text is diagnosis.
for nm, addr, note in (
    ("kill 20 rd", A_SETISR,
     "*** A GUEST **LOAD** AT 0x0ff10020. case 0x10020 has NO writeflag test and runs "
     "`d->isr = idata' FIRST with idata==0, so this is predicted to ZERO THE ISR and THEN "
     "abort() -- corruption AND host death in one arm. ***"),
    ("kill 28 rd", A_CLRISR,
     "case 0x10028, same missing writeflag test; `d->isr &= ~idata' is a no-op at idata==0, "
     "then abort()."),
):
    t, alive = session(guest_load(addr))
    row(nm, ("alive" if alive else "DEAD"), "alive", note)
    #  *** RE-PINNED 2026-09-17 ONTO THE SHIPPED #531 TEXT.  The old literal was the
    #  PRE-FIX message `IP30 legacy interrupt rewrite: TODO', which #531 replaces with a
    #  latched announce -- so this row pinned a string the fix legitimately renames.
    #  ORDER DISCRIMINATOR (the oracle-correction rule): the re-pin is shown RED on a
    #  PRE-FIX binary before being trusted -- see artifacts/ip30abortkill/REPIN_*.out.
    row(nm + " txt", ("yes" if "sgi_ip30: interrupt-status rewrite not implemented" in t else "no"), "yes",
        "DIAGNOSIS ONLY, never half the trigger: a reworded-message mutant still abort()s, "
        "gives EOF with no text, and an EOF-AND-text oracle would certify it GREEN.")

t, alive = session(guest_store(A_ISR, 0x1))
row("kill 30 wr", ("alive" if alive else "DEAD"), "alive",
    "case 0x10030's WRITE arm aborts while its read is serviced -- the asymmetry, measured.")

#  ------------------------------------------------- rows the PROBE ATTACK proved missing
#  Every one of these closes a mutant that scored 12/12 against the probe without it.  They
#  are L1 CONSTRUCTION -- found while this is still a draft, which is the whole reason the
#  detector was attacked BEFORE the fix shipped.

#  *** THE TICK ROW.  Closes M_tick_abort (which is ALSO clause (b) at site 4 -- a VERBATIM
#  REINSTATEMENT the probe could not see) and M_tick_bit49. ***  It uses `sd' because `sw'
#  cannot set bit 50 at all, and `step 1' suffices because machine_add_tickfunction sets
#  ticks_till_next[n] = 0 (machine.c:354), so the FIRST machine_run fires every tick function.
#  *** THE CHANNEL, AND WHY SURVIVAL ALONE IS NOT ONE POST-FIX.  ***  The pass-2 codex seat
#  measured that after de-fatalisation `tick 50' and `tick 49' BOTH read `alive', so the pair
#  that discriminated pre-fix (ALIVE against DEAD) stops discriminating on the shipped build --
#  the CHANNEL check's "a row whose named channel cannot vary under its named mutant is vacuous
#  by construction", arriving because the fix removed the channel the rows were built on.
#  The channel that DOES vary post-fix is the ANNOUNCE, so the pair is re-aimed onto it.
TICKMSG = "sgi_ip30: timer interrupt delivery not implemented"

t, alive = session(guest_store64(A_IMASK0, 1 << 50) + ["step 1"])
row("tick 50", ("alive" if alive else "DEAD"), "alive",
    "*** ARM imask0 BIT 50 WITH `sd', THEN ONE STEP. ***  Pre-fix the DEVICE_TICK abort fires "
    "and the host dies; post-fix it must survive with a latched announce.  `sw' here would arm "
    "nothing and score GREEN on a live death -- that is the trap this row exists to avoid.")
#  Pre-fix this reads `no': HEAD prints `IP30 legacy interrupt rewrite: TODO' and aborts, so the
#  row is RED on the committed build and green only once the fix renames and latches it.
row("tick 50 txt", ("yes" if TICKMSG in t else "no"), "yes",
    "*** THE POST-FIX HALF OF THE DISCRIMINATOR. ***  `tick 50' pins that the host LIVES; this "
    "pins that the arm still ANNOUNCES.  Without it a mutant deleting the tick fatal() leaves "
    "both tick rows green, and so does one moving the guard to bit 49.")
#  The DISCRIMINATOR: same store, same step, bit 49 instead of 50.  Without it, `tick 50' could
#  be passing for any reason at all and M_tick_bit49 walks free.
t, alive = session(guest_store64(A_IMASK0, 1 << 49) + ["step 1"])
row("tick 49", (("yes" if TICKMSG in t else "no") if alive else "died"), "no",
    "DISCRIMINATOR for `tick 50': bit 49 is NOT the guarded bit, so the arm must stay SILENT on "
    "BOTH builds.  Survival is still pinned -- a dead host reads `died', not `no'.  Re-aimed "
    "from a bare survival oracle, which post-fix could not vary: see the CHANNEL note above.  "
    "A mutant moving the guard to 1<<49 makes this announce and reds the row.")

#  *** THE WRITE ARMS.  The probe only ever LOADED at 0x10020/0x10028, so M_wf20_abort_wr and
#  M_wf28_abort_wr -- abort() kept INSIDE the write arm -- were invisible. ***
for nm, addr in (("kill 20 wr", A_SETISR), ("kill 28 wr", A_CLRISR)):
    t, alive = session(guest_store(addr, 0x1))
    row(nm, ("alive" if alive else "DEAD"), "alive",
        "A guest WRITE at this offset.  Pre-fix it reaches the same abort(); post-fix it must "
        "survive.  Without this row a fix that adds the writeflag test and leaves abort() in "
        "the WRITE arm scores a clean sweep.")

#  *** THE asicindexcase ROW.  Closes M_wf20_store_out -- the writeflag wrapping only the
#  ANNOUNCE while `d->isr = idata' still runs on a LOAD.  That mutant leaves the host ALIVE and
#  the guest's read still zeroes the ISR, which is WORSE than the defect being fixed. ***
#  PRE-FIX THIS ROW READS `dead': the seeding write at 0x10020 itself aborts.  That is correct
#  and is part of the reproduction, not an apparatus failure.
t, alive = session(guest_store(A_SETISR, 0x5a5a)      # seed ISR through the Set arm
                   + guest_load(A_SETISR)             # the LOAD that must not clobber it
                   + guest_load(A_ISR))               # read it back through the read-only ISR
row("isr keep", (printed_last(t, "v0") if alive else "died"), "0x5a5a",
    "*** ISR UNCHANGED ACROSS A LOAD AT 0x10020. ***  Seed via the Set arm, load at 0x10020, "
    "read back at 0x10030 (heart.h: isr is the read-only status register).  If a fix declines "
    "the ANNOUNCE but still runs the store on a read, this row reds while every survival row "
    "stays green.  Pre-fix it reads `died' because the seeding write aborts -- that is the "
    "reproduction, not a broken row.")

#  Closes M_latch_silent_30: deleting the 0x10030 write-arm fatal() while keeping survival.
row("kill 30 txt", ("yes" if "sgi_ip30: interrupt-status rewrite not implemented" in t else "no"), "yes",
    "DIAGNOSIS sibling for the 0x10030 WRITE arm.  `kill 20/28 rd txt' never visit that arm, so "
    "without this a mutant can delete its announce silently.  Never half a trigger.")

# ------------------------------------------------------------------ report
CONTROL = "OK"
for nm, got, want, _ in rows:
    if nm in ("live", "devsig") and got != want:
        CONTROL = "DEAD"

print("ip30_abort_probe -- binary=%s label=%s machine=sgi/ip30" % (BIN, LABEL))
print("IP30ABORT_CONTROL=%s" % CONTROL)
if CONTROL == "DEAD":
    print("IP30ABORT_RESULT=0/0")
    print("  *** SETUP FAILED -- the vehicle is not the vehicle. NOT 'no defect'. ***")
    for nm, got, want, note in rows:
        print("  %-12s got=%-12s want=%-12s %s" % (nm, got, want, note[:60]))
    print("IP30ABORT_DONE")
    raise SystemExit(0)

n = 0
for nm, got, want, note in rows:
    ok = (got == want)
    n += 1 if ok else 0
    print("  %-12s got=%-12s want=%-12s %s  %s" % (nm, got, want, "ok" if ok else "FAIL", note[:70]))
print("IP30ABORT_RESULT=%d/%d" % (n, len(rows)))
print("IP30ABORT_DONE")
