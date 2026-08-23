#!/usr/bin/env python3
"""#455: an interrupt asserted at priority 0 ended the host process.

Prints one line per row:  <name> <got> <want> ok|FAIL
then SH_INTPRIO_CONTROL=OK|DEAD and SH_INTPRIO_RESULT=<passed>/<total>.
gate_sh_rounding.sh does the asserting.

What this protects
------------------
`sh_cpu_interrupt_assert()` (cpu_sh.c) ended the host process when the asserted
line's priority nibble was zero, under the comment "Interrupt not implemented?
Hm."  Nothing is unimplemented.  Priority 0 is a documented, guest-selectable,
RESET-DEFAULT state -- SH7750 Hardware Manual Rev.7.00 19.2 (:39887): "When level
0 is set, the interrupt is masked and interrupt requests are ignored", and 19.3.1
(:40193): "IPRA to IPRC are initialized to H'0000 ... by a reset".

*** WHAT THIS FILE COVERS CHANGED IN #456, AND THE OLD TEXT IS KEPT BECAUSE THE
CHANGE WAS SILENT. ***

WHEN #455 SHIPPED, this paragraph read: machine_test.c wires the entire
test-machine interrupt tree to SH4_INTEVT_IRQ15 (0x3e0, array index 31);
sh_update_interrupt_priorities()'s IRQ loop is bounded `i <= SH4_INTEVT_IRQ14`, so
index 31 is NEVER assigned; therefore ONE guest store to the mp device's IPI
register reached the priority-0 kill synchronously.  Measured then, one
`mov.l r0,@r1`:

    80010000:  2102        mov.l   r0,@r1  ; r1 = 0xb10000a0
    [ SH interrupt 0x3e0, prio 0 (?), aborting ]

#456 MOVED THAT LINE TO IRQ14, priority 1 -- because a machine whose whole
interrupt tree sits on a permanently-masked line cannot deliver anything, and
#455 had just turned that from a loud exit(1) into silence.  So a store here no
longer reaches the priority-0 arm at all, and the two rows that used to pin it
would have gone on passing FOR THE WRONG REASON.  Measured, not predicted: a build
carrying IRQ14 AND a verbatim reinstatement of the priority-0 kill scores 5/7 with
both old rows GREEN, while the same kill on an IRQ15 build scores 3/7 with both
RED.  One identifier apart.

The rows were therefore repurposed rather than deleted -- see the block above them
-- and #455's priority-0 coverage now rests on the landisk TMU rows, which still
redden on that same reinstatement.  The old text stays because a future reader
who finds "the testsh route reaches the priority-0 kill" in a git log needs to see
where it stopped being true.

*** WHY NOT THE TIMER ROUTE, WHICH IS THE OBVIOUS ONE. ***  A TMU underflow also
reaches the kill, but it is produced by a HOST timer -- timer_add/SIGALRM ->
sh4_timer_tick() -> timer_interrupts_pending++ -> DEVICE_TICK asserts.  And
debugger.c:800 calls timer_stop() "while interacting with the user", with the
step command returning at :835-836 BEFORE timer_start() at :840.  So host timers
are stopped for the whole `step N`: the tick loop still runs (machine.c:726-728
decrements by 1 under single_step) but finds nothing pending, and NOTHING
ASSERTS.  A step-based timer row would score a correct pre-fix build ALIVE and
fail vacuity floor clause (a) in silence.  A review seat caught that in the
design, after two earlier drafts of the project's own step-visibility rule had
already been written down and one witness designed on them.

    The discriminator, kept here because it is easy to get wrong twice:
    a step probe sees a SYNCHRONOUS assert -- a device handler reached inside the
    guest's own load or store.  It does not see one fed by a host-timer callback.
    Ask what produces the thing the tick consumes.

testsh is handed the landisk kernel purely so the machine constructs; it is never
executed.  The SH5 corpus file cannot be used -- it constructs the machine and
then dies in the loader with "SH64: 32-bit instruction encoding: TODO".
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]

#  dev_mp.c: DEV_MP_ADDRESS 0x11000000 + DEV_MP_IPI_ONE 0x00a0.  Reached through P2
#  (0xa0000000..0xbfffffff), which memory_sh.c maps as `vaddr & 0x1fffffff` with no
#  UTLB involvement, so the row does not depend on MMU state.
IPI = 0xb10000a0
MPMEM = 0xb1000090            # DEV_MP_MEMORY -- returns ram_mb * 1048576
CODE = 0x80010000
#  *** testsh RAM IS AT PHYSICAL 0, NOT AT LANDISK'S 0x0c000000. ***  The first
#  draft of this probe reused landisk's 0x8c010200 and its LIVENESS control read
#  back 0x00000000 -- a control failing for a reason that had nothing to do with
#  the defect.  This project has now made that exact mistake twice on testsh, the
#  earlier one in a pclock witness.  P1 at 0x80010200 is physical 0x00010200.
SCRATCH = 0x80010200
LIVE = 0x12345678         # ASYMMETRIC on purpose -- see dumped()
MPWANT = 64 * 1048576         # -M 64

MOV_L_R0_AT_R1 = 0x2102
MOV_L_AT_R1_R0 = 0x6012       # mov.l @r1,r0
#  *** MATCH THE SHAPE, NOT THE SPELLING. ***  An earlier draft matched
#  "SH interrupt 0x..., prio 0" literally, and a review seat produced the obvious
#  escape: a maintainer who removes the crash but keeps a warning --
#  `fatal("[ SH masked interrupt 0x%x ignored ]\n", irq_nr); return;` -- passes
#  every row, because the reworded line does not match.  The diagnostic is still
#  un-silenceable (fatal() has no quiet_mode early-out), so the row must reject the
#  CLASS.  Every gxemul diagnostic of this kind is bracketed, so that is the shape
#  to reject: any `[ ... ]` line appearing after the triggering command.
ABORT_RE = re.compile(r"^\[", re.M)
#  *** AND IT IS SEARCHED ONLY IN THE DELTA AFTER THE TRIGGERING COMMAND, WHICH IS
#  NOT A REFINEMENT BUT THE POINT. ***  Broadening a pattern false-positives as
#  easily as narrowing one misses, and this one did: applied to the whole
#  transcript it matched the TMU row's own ORDINARY SETUP CHATTER --
#  `[ sh4 timer 0 clock set to 8333333.250000 Hz ]` and
#  `[ sh4 timer: starting timer 0 ]`, both emitted by the legal register writes the
#  row makes on purpose -- and reddened a correct build.  Measured, not guessed: a
#  clean startup prints ZERO bracketed lines and the fixed build's post-trigger
#  delta prints ZERO, while the pre-fix delta carries the abort.  Scoped this way
#  the row rejects the CLASS of assert-path diagnostic without caring how it is
#  worded, which is what kills the "remove the crash but keep a warning" mutant.


def session(cmds, settle=8.0, machine="testsh", spin=1.2, verify=True):
    """Return (transcript, host_died).  The host dying IS the observable here.

    `spin` is how long to wait after each command.  The default is fine for `step`;
    a `continue` needs long enough to outlast at least one host-timer callback, and
    that number was MEASURED against a build known to contain the defect rather than
    guessed -- a drive that leaves a defective build alive is a broken driver, not
    evidence about the route.
    """
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-E", machine, "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
            except OSError:
                return False
            if not d:
                return False
            buf += d.decode("latin-1", "replace")
        return True

    alive = rd(settle)
    last_mark = len(buf)
    #  *** THE LONG SPIN BELONGS TO THE LAST COMMAND ONLY. ***  An earlier draft
    #  passed `spin` to every command; with 17 setup commands ahead of `continue`
    #  that made one TMU session wait roughly 510 seconds instead of 30.  A review
    #  seat caught it by reading what the parameter actually reaches.
    for i, c in enumerate(cmds):
        if i == len(cmds) - 1:
            last_mark = len(buf)
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 1.2):
            alive = False
            break
    #  Ask one more question, so "did not die" is a POSITIVE reading rather than
    #  the absence of a crash we might simply have missed.
    #
    #  *** AND CHECK THE ANSWER, NOT JUST THE PIPE. ***  An earlier draft only
    #  tested that the pty stayed open, so a HUNG emulator -- alive but no longer
    #  answering -- would have been scored the same as a healthy one.  A review seat
    #  named that; the probe now requires the value back.
    #
    #  *** BUT ONLY FOR A SESSION THAT ENDS AT A PROMPT. ***  A FREE-RUNNING session
    #  is executing the guest -- here a `bra .` self-loop -- and has no debugger to
    #  answer, by construction.  MEASURED: after `continue` the pty stays open and
    #  `print 0x1234` returns nothing at all.  Requiring the answer there turned two
    #  GREEN rows red on the fixed build -- a regression this very repair introduced
    #  while fixing something else, caught only because the rows were re-measured
    #  rather than assumed.  For those rows the liveness signal is the process
    #  surviving, and the DISCRIMINATION comes from the pre-fix control, where it
    #  does not survive.
    if alive and verify:
        mark = len(buf)
        try:
            os.write(fd, b"print 0x1234\n")
            rd(1.5)
            alive = "0x1234" in buf[mark:] or "4660" in buf[mark:]
        except OSError:
            alive = False
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.2)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return buf, not alive, buf[last_mark:]


def ipi_store():
    return ["r0=0x00000000", "r1=0x%x" % IPI,
            "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),
            "pc=0x%x" % CODE, "step 1"]


def dumped(transcript, died):
    """Pull one word out of a `dump` and convert it LITTLE-ENDIAN.

    *** THE RAW HEX IS NOT THE VALUE. ***  `dump` prints bytes in memory order and
    this CPU is little-endian, so the digits must be swapped -- the idiom is
    sh_halt_probe.py's `int.from_bytes(..., "little")`.  An earlier draft of this
    probe compared the raw string, and its LIVENESS row still passed, because
    0x5a5a5a5a is a PALINDROME under byte swap.  The device-signature row is what
    exposed it: 0x04000000 came back as 0x00000004.
    A control value must be ASYMMETRIC or it cannot see this class at all -- the
    same lesson the hand-assembled encoding trap already records for register
    fields, in a different disguise.
    """
    if died:
        return "died"
    m = re.search(r"0x0*[0-9a-f]+\s+([0-9a-f]{8})", transcript.split("dump")[-1])
    if not m:
        return "nodump"
    return "0x%08x" % int.from_bytes(bytes.fromhex(m.group(1)), "little")


rows = []


def row(name, got, want, tag="#455"):
    """Each row names the round that OWNS it.  This file now carries two: #455's
    priority-0 masking rows and #456's delivery rows, which replaced the two #455
    rows that #456 made vacuous.  A single hardcoded tag would have said #455 on
    rows #455 never had."""
    ok = (got == want)
    rows.append(ok)
    print("%-14s %-24s %-24s %-10s %s"
          % (name, got, want, tag, "ok" if ok else "FAIL"))


#  ---- control: the session comes up and answers at all ------------------------
ctl, ctl_died, _ = session([])
print("SH_INTPRIO_CONTROL=%s" % ("DEAD" if ctl_died else "OK"))
if ctl_died:
    print("SH_INTPRIO_RESULT=0/0")
    sys.exit(0)

#  ---- R1: the witness ---------------------------------------------------------
#  TWO assertions on purpose.  "alive" alone is satisfied by a mutant that drops
#  the exit() and leaves the fatal() -- and fatal() has no quiet_mode early-out
#  (debugmsg.c:384-390), so it would print forever, un-silenceable, while the row
#  went green.  A review seat named that mutant; this is what kills it.
#  *** THESE TWO ROWS USED TO PIN #455 AND NO LONGER CAN.  #456 TOOK THAT AWAY,
#  AND IT DID SO SILENTLY. ***
#
#  #455's rows worked here BECAUSE the test machine's whole interrupt tree hung off
#  a line whose priority was permanently 0.  #456 moved it to IRQ14, priority 1, so a
#  store here no longer reaches the priority-0 arm at all.  MEASURED, not predicted:
#  a build carrying IRQ14 AND a verbatim reinstatement of the priority-0 kill scores
#  5/7 with both old rows GREEN, while the same kill on an IRQ15 build scores 3/7
#  with both RED.  One identifier apart, and the fix itself stays 7/7 -- so nothing
#  would have forced anyone to notice.
#
#  RETARGETING THEM TO SOME OTHER PRIORITY-0 SOURCE IS NOT AVAILABLE, and that was
#  measured rather than assumed.  SCIF asserts synchronously inside a guest store but
#  sits at priority 3 (`intc_intpri08` is initialised to 0x33333333) and the register
#  that would lower it is unmapped -- `non-existant paddr=0xfe080008`.  The TMU on
#  testsh dies on EVERY build with "pclock must be set for this machine", a different
#  host death entirely.  **After #456 the test machine has no guest-reachable
#  priority-0 interrupt source at all.**
#
#  So the SESSION machinery is kept and the rows' PURPOSE changes: they now pin that
#  a legal priority-1 interrupt IS DELIVERED, which is #456's own claim.  #455's
#  priority-0 coverage survives on the landisk TMU rows below, which still redden on
#  that same reinstatement -- confirmed, so the vacuity floor still holds.
TESTSH_VBR = 0x80020000
TESTSH_HANDLER = TESTSH_VBR + 0x600


def testsh_deliver(imask):
    """Free-run one IPI store with SR.IMASK set, and see whether the vector is reached.

    `imask` is what brackets the priority.  Delivery needs `IMASK < int_level`
    (cpu_dyntrans.c), so a line at level 1 is admitted at IMASK 0 and refused at
    IMASK 1.  Running BOTH pins the level to exactly 1 -- which is the whole point,
    because a witness that only asks "did something deliver" is passed by any of
    IRQ0..IRQ13.  That mutant was built and measured escaping before these rows
    existed.
    """
    return ["put h 0x%x, 0x0009" % TESTSH_HANDLER,          # nop, so the fetch works
            "put h 0x%x, 0xaffe" % (TESTSH_HANDLER + 2),    # bra .
            "put h 0x%x, 0x0009" % (TESTSH_HANDLER + 4),    # nop (delay slot)
            "r0=0x00000000", "r1=0x%x" % IPI,
            "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),  # mov.l r0,@r1  (the IPI)
            "put h 0x%x, 0xaffe" % (CODE + 2),              # bra .  -- park here if
            "put h 0x%x, 0x0009" % (CODE + 4),              # nothing is delivered
            "pc=0x%x" % CODE,
            "sr=0x%08x" % (0x40000000 | (imask << 4)),      # MD=1, BL=0, IMASK=imask
            "vbr=0x%x" % TESTSH_VBR,
            "breakpoint add 0x%x" % TESTSH_HANDLER]


t, died, tail = session(testsh_deliver(0) + ["continue"], spin=6.0, verify=True)
row("irq14 deliv", "nodeliver" if died else "delivered", "delivered", "#456")
#  verify=True on BOTH, and it is load-bearing on this one.  A refused interrupt
#  leaves the guest spinning in `bra .` with the process perfectly alive, so "did the
#  process survive" cannot tell refused from delivered.  Requiring the DEBUGGER to
#  answer can: only a breakpoint hit returns to a prompt.
t6, died6, _ = session(testsh_deliver(1) + ["continue"], spin=6.0, verify=True)
row("irq14 imask", "delivered" if not died6 else "refused", "refused", "#456")

#  ---- R2: LIVENESS control ----------------------------------------------------
#  A known value through the same decode, in the same machine, so a dead or
#  mis-built session cannot be read as "the defect is fixed".
t2, died2, _ = session(
    ["r0=0x%08x" % LIVE, "r1=0x%x" % SCRATCH,
     "put w 0x%x, 0xdeadbeef" % SCRATCH,
     "put h 0x%x, 0x%04x" % (CODE, MOV_L_R0_AT_R1),
     "pc=0x%x" % CODE, "step 1",
     "dump 0x%x 0x%x" % (SCRATCH, SCRATCH + 4)])
row("prio0 live", dumped(t2, died2), "0x%08x" % LIVE)

#  ---- R3: DEVICE-SIGNATURE control -------------------------------------------
#  One control is NOT enough: the footbridge probe's first draft returned 0x0
#  everywhere WITH its RAM control green.  So this reads DEV_MP_MEMORY through a
#  real guest load on the SAME device the witness pokes -- it answers
#  ram_mb * 1048576, a value RAM at that address could not produce and which only
#  dev_mp can compute.  An earlier draft asserted on the ABORT STRING instead,
#  which is no control at all: it is present exactly when the defect is present,
#  so post-fix it would have been reading its own absence.
t3, died3, _ = session(
    ["r1=0x%x" % MPMEM, "r2=0x%x" % SCRATCH,
     "put w 0x%x, 0xdeadbeef" % SCRATCH,
     "put h 0x%x, 0x%04x" % (CODE, MOV_L_AT_R1_R0),
     "put h 0x%x, 0x%04x" % (CODE + 2, 0x2202),      # mov.l r0,@r2
     "pc=0x%x" % CODE, "step 2",
     "dump 0x%x 0x%x" % (SCRATCH, SCRATCH + 4)])
row("prio0 devsig", dumped(t3, died3), "0x%08x" % MPWANT)


#  ---- the SECOND route, and it is the reason this probe is not one-route --------
#  *** A PARTIAL FIX PASSES EVERY testsh ROW. ***  Measured: a mutant reading
#  `if (prio == 0) { if (index == 31) return; fatal(...); exit(1); }` -- i.e. one
#  that repairs ONLY the route the witness drives -- scores 4/4 above while leaving
#  every other route ending the host.  A review seat named that shape; building it
#  confirmed it.
#
#  This is the FIFTH consecutive round in which a detector covered one instance of a
#  multi-instance thing (#451 two SCI sites, #452 two TLB devices, #453 eight DMA
#  channels, #454 two store queues and an unwritten QACR pair, now two interrupt
#  routes).  Treat a second instance as owed by default rather than as a discovery.
#
#  The TMU route is on landisk, index 32, and it MUST free-run: the underflow is
#  produced by a host timer, and debugger.c stops those for the duration of a step.
#  Controlled in both directions before being trusted -- on a pre-fix build this
#  drive kills the host, and on the fixed build it does not.
LANDISK_CODE = 0x8c010000
TMU_SPIN = 30.0


def landisk_tmu():
    """Arm TMU0's underflow interrupt with IPRA untouched, then free-run.

    TCR0 = TCR_UNIE, which PASSES #447's guard (TCR_UNIMPLEMENTED is 0x02DC and
    UNIE is 0x0020, not in that mask), so this is a legal write that a driver makes.
    TCOR0/TCNT0 are tiny so the first host callback underflows.  `bra .` parks the
    guest in a self-loop so the run is bounded by wall clock rather than by
    instructions.
    """
    c = ["r1=0xffd80010", "r2=0x00000020",          # TCR0  = UNIE
         "r3=0xffd80008", "r4=0x00000002",          # TCOR0 = 2
         "r5=0xffd8000c", "r6=0x00000002",          # TCNT0 = 2
         "r7=0xffd80004", "r8=0x00000001",          # TSTR  = start
         "put h 0x%x, 0x2122" % LANDISK_CODE,       # mov.l r2,@r1
         "put h 0x%x, 0x2342" % (LANDISK_CODE + 2),  # mov.l r4,@r3
         "put h 0x%x, 0x2562" % (LANDISK_CODE + 4),  # mov.l r6,@r5
         "put h 0x%x, 0x2782" % (LANDISK_CODE + 6),  # mov.l r8,@r7
         "put h 0x%x, 0xaffe" % (LANDISK_CODE + 8),  # bra .
         "put h 0x%x, 0x0009" % (LANDISK_CODE + 10),  # nop (delay slot)
         "pc=0x%x" % LANDISK_CODE, "step 4"]
    return c


t4, died4, tail4 = session(landisk_tmu() + ["continue"], settle=8.0,
                    machine="landisk", spin=TMU_SPIN, verify=False)
row("prio0 tmu", "died" if died4 else "alive", "alive")
row("prio0 tmuq", "abort" if ABORT_RE.search(tail4) else "silent", "silent")


#  ---- the ACCEPT row: a LEGAL interrupt must still be delivered ----------------
#  *** THIS IS PART OF THE FIX'S COST, NOT FUTURE STRENGTHENING. ***  The
#  de-escalation clause: a fatal->survive fix DELETES the accidental tripwire that
#  made guard growth self-announcing.  Before #455, widening the predicate to
#  `prio <= 1` meant exit(1) on the first legal priority-1 interrupt -- unmissable.
#  After it, the same edit SILENTLY SWALLOWS every priority-1 interrupt on every SH
#  machine, and nothing anywhere notices.  `prio == 0` is the only predicate that
#  gated death, so exactly one accept row is owed.
#
#  FAILABILITY, per the accept-row rule -- the row must redden under the smallest
#  realistic growth mutant, and the pinning value must reach the predicate's
#  OPERAND.  Read the store arm: dev_sh4.c's `case SH4_IPRA:` stores `intc_ipra`
#  UNMASKED, and cpu_sh.c loads `(intc_ipra >> 12) & 0xf` straight into `prio`, so
#  a guest can place any value 0..15 there and guard-only growth is non-equivalent.
#  There is no latch operand here at all -- the fix is a bare `return` -- so the
#  JOINT form does not exist and guard-only IS the least-observable non-equivalent
#  form.  The row pins prio 1, which `prio <= 1` swallows.
#
#  Two seats independently named `if (prio <= 1) return;` as passing all six rows
#  above, because every interrupt-bearing row uses a prio-0 line.  This is its kill.
#
#  The observable is DELIVERY, so it free-runs -- and the discriminator is the
#  breakpoint.  Delivered: the vector at VBR+0x600 is reached, the breakpoint stops
#  the guest, the debugger answers.  Not delivered: the guest spins in `bra .`
#  forever and never returns to a prompt.  So `verify=True` is exactly right here,
#  unlike the two rows above -- a delivered interrupt is precisely the case that
#  DOES end at a prompt.
VBR = 0x8c020000
HANDLER = VBR + 0x600
SH4_IPRA = 0xffd00004          # 16-bit; TMU0 priority is bits [15:12]


def landisk_accept():
    c = ["put h 0x%x, 0x0009" % HANDLER,           # nop, so the fetch succeeds
         "put h 0x%x, 0xaffe" % (HANDLER + 2),     # bra .
         "put h 0x%x, 0x0009" % (HANDLER + 4),     # nop (delay slot)
         "r9=0x%x" % SH4_IPRA, "r10=0x00001000",   # IPRA: TMU0 -> priority 1
         "r1=0xffd80010", "r2=0x00000020",
         "r3=0xffd80008", "r4=0x00000002",
         "r5=0xffd8000c", "r6=0x00000002",
         "r7=0xffd80004", "r8=0x00000001",
         "put h 0x%x, 0x29a1" % LANDISK_CODE,          # mov.w r10,@r9  (IPRA)
         "put h 0x%x, 0x2122" % (LANDISK_CODE + 2),    # mov.l r2,@r1
         "put h 0x%x, 0x2342" % (LANDISK_CODE + 4),    # mov.l r4,@r3
         "put h 0x%x, 0x2562" % (LANDISK_CODE + 6),    # mov.l r6,@r5
         "put h 0x%x, 0x2782" % (LANDISK_CODE + 8),    # mov.l r8,@r7
         "put h 0x%x, 0xaffe" % (LANDISK_CODE + 10),   # bra .
         "put h 0x%x, 0x0009" % (LANDISK_CODE + 12),   # nop (delay slot)
         "pc=0x%x" % LANDISK_CODE, "step 5",
         #  SR last: MD=1 (privileged), IMASK=0 so level 1 is admitted, BL=0 so
         #  exceptions are not blocked.  Reset leaves IMASK at 15, which would
         #  refuse a priority-1 interrupt and make this row vacuous.
         "sr=0x40000000", "vbr=0x%x" % VBR,
         "breakpoint add 0x%x" % HANDLER]
    return c


t5, died5, _ = session(landisk_accept() + ["continue"], settle=8.0,
                       machine="landisk", spin=TMU_SPIN, verify=True)
row("prio0 accept", "nodeliver" if died5 else "delivered", "delivered")

print("SH_INTPRIO_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)))
