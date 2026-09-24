#!/usr/bin/env python3
"""#432: the DC21285 "footbridge" driven by REAL GUEST INSTRUCTIONS, with no rig.

WHY THIS EXISTS ALONGSIDE regress/diff_footbridge.c.  The offline differential calls
footbridge_effective_cycles() and dev_footbridge_access() directly, so it proves BEHAVIOUR
but cannot prove the device is REACHABLE by a guest -- it would stay green under a change
that unmapped it (a memory_device_register length, a DM_ flag, or machine_cats.c's
`addr=0x42000000` line).  Until this probe, R6 was THE ONLY CODE ROUND IN THIS TREE WITH NO
REACHABILITY WITNESS OF ANY KIND: no rig boots a footbridge and there is no m8online analog.
This is that analog.  It goes through the real address decode and the real memory_rw
plumbing, on a COLD DEBUGGER -- no boot, no disk image, no guest OS.

*** THE TRAP THIS PROBE EXISTS TO SURVIVE, and it is the whole reason for arm T. ***
machine_cats.c:131 calls arm_setup_initial_translation_table(), which (cpu_arm.c:239-255)
writes a section descriptor for i in 0..255 at VA (j<<28)+(i<<20) -> PA i<<20 -- i.e. the
TOP NIBBLE OF THE VA IS IGNORED and only the low 256 MB of physical space is mapped
anywhere.  The footbridge sits at PA 0x42000000, outside that window, so under the boot-time
MMU it is UNREACHABLE: VA 0x42000000 aliases to PA 0x02000000 and a load returns 0.

That is not a hypothetical.  The first version of this probe returned 0x0 on every device
row WITH ITS RAM CONTROL STILL GREEN, and 0x0 is exactly what "the device is not there"
looks like -- so a survival-shaped or absence-shaped assertion would have CONFIRMED THE
OPPOSITE CONCLUSION.  A RAM liveness row cannot see it, because VA 0x9000 maps to PA 0x9000
identically with the MMU on or off.

So the guard is not a comment, it is arm T: THE SAME PROGRAM WITH THE THREE MMU-DISABLE
INSTRUCTIONS REPLACED BY NOPS MUST NOT PRODUCE THE DEVICE'S ANSWER.  If arm T ever reads
0x1011, the discriminator is dead and every other row here is meaningless -- and it goes RED
rather than silently green.  Arm L additionally reads CP15 c1 BACK after the mcr and asserts
bit 0 is clear, so the precondition is MEASURED rather than inferred from the store having
been issued.  Three separate statements, deliberately: the guest turned the MMU off, the two
arms really differ in MMU state, and only the MMU-off arm can see the device.

VALUES, NOT SURVIVAL (rounds 79/80, and m8820x_sites_probe.py's header says the same).
A row that only asks "did the host stay up" cannot tell a reachable device from an absent
one -- an unmapped read survives too, it just returns 0.  So the two device rows assert
values that ONLY dev_footbridge.c can produce:
  * A1 reads VENDOR_ID and requires 0x1011 (dev_footbridge.c `case VENDOR_ID`, the
    DC21285_VENDOR_ID assignment).
    Nonzero and specific: the hand-assembled-encoding trap this project has been bitten by
    yields 0 from a wrong register field, and 0 is the one answer this row rejects.
  * A2 writes 0x12345678 to TIMER_1_LOAD and reads back 0x00345678.  THE VANISHING TOP BYTE
    IS THE HANDLER'S OWN SIGNATURE: `case TIMER_1_LOAD`'s write branch (one case serves all four
    timers through the fold) stores `idata & TIMER_MAX_VAL`
    (0x00FFFFFF, dc21285reg.h:371).  RAM, or any decode that merely absorbed the store,
    would return 0x12345678 unchanged.  This row therefore distinguishes "the device
    handled it" from "the write landed somewhere", which A1 alone cannot.

THE HARNESS LEGS (#545), which replaced the kill bridge.  Until #545 this probe's failability
control was arm K: arm L plus ONE guest read of IRQ_ENABLE_CLEAR (+0x18c), which the device
answered with fatal() then exit(1).  #545 declines that read (and the four undefined-direction
writes) instead of dying, so nothing a guest can do to this device ends the process any more
-- except the two SDRAM reads at +0x100/+0x104 (`fbsdrampair`), which no arm here touches.  The
control that "this harness notices a dead child" therefore has to come from the HARNESS, and
it comes from two legs that need no product defect:
  H1 STARTUP REJECTION: launch with an unknown `-E` name.  machine.c prints
     `Sorry, emulation "<name>" is unknown.` and main.c exits 1 before any prompt.  The row
     requires NO prompt AND that diagnostic naming THIS run's input AND `WIFEXITED && == 1`.
     The text clause does all the work: five different startup refusals (bad option, bad -M,
     missing file, ...) ALL exit 1 with no prompt, so "exit != 0" or "exit == 1" alone proves
     nothing (measured, pass 1).
  H2 QUIT AFTER A VERIFIED PROLOGUE: arm L's program, stepped to its end, a FRESH `reg` proving
     r3 bit 0 clear, r5 = 0x11223344, r6 = 0x1011 and r1 = 0x00345678 (the prologue really
     ran), then `quit`, then ONE MORE ordinary `reg`: it must fail and `dead` must be set
     BEFORE teardown, and the reap must be `WIFEXITED && == 0`.  Both non-obvious clauses are
     load-bearing: a child that died BEFORE the prologue finished produces `next send fails`
     and `dead` IDENTICALLY, and is separated only by exit == 0 and the fresh-reg values --
     a K2 without them goes green exactly when a product fix has FAILED (measured, pass 1).
  Negative controls (PRETABLE, not shipped): omit the `quit` -> the next `reg` succeeds and H2
  reds; move the teardown ahead of the observation -> H2 must red (it does not observe anything).

ARM S (#545) -- the five declined sites in ONE PROCESS.  Each site is accessed TWICE in its
undefined direction with a LEGAL read of a sibling register between the two, and every access
must (i) leave the process alive, (ii) leave all five interrupt registers unchanged, and (iii)
announce EXACTLY ONCE across the whole arm, in the site's own text.  ONE process is the whole
point: a latch shared between two sites, or one aggregate latch, is INVISIBLE to any design
that runs one site per process -- measured in pass 1, two total escapes of a per-site design.
  enable 0x30 -> +0x188 (IRQ), 0xc0 -> +0x288 (FIQ); decline writes carry 0x10 (IRQ, inside
  0x30) and 0x40 (FIQ, inside 0xc0), so a store into the status field would show in BOTH the
  raw and the masked read.
  N1 str 0x10 -> +0x180 x2   (legal read between: +0x184 -> r7, row S2)
  N2 str 0x10 -> +0x184 x2   (legal read between: +0x180 -> sl, row S1)
  N3 ldr +0x18c x2 -> r9, r8 (both 0: the IRQEnable value that used to be computed there
                              is 188h's answer; legal read between: +0x188 -> fp, row S3 = 0x30)
  N4 str 0x40 -> +0x280 x2   (legal read between: +0x280 -> r2, row S4)
  N5 str 0x40 -> +0x284 x2   (legal read between: +0x284 -> lr, row S5)
  SF1/SF2 FINAL raw reads +0x184 -> r1, +0x284 -> sp, after every decline (a store landed by
     the LAST write of any pair shows here; r1 is A2's register in arm L and is free here).
  N0 the five distinct `(once)` texts each appear exactly once in the arm's diagnostics
     (5 on the fix; 4 under a two-site shared latch; 1 under one aggregate latch -- measured).
  N1..N5 per-site: the site's own text appears exactly once (ACCESS-LOCAL text, so a misnamed
     register reds its own row, not a total).
  Widths (a byte or halfword decline) are NOT rowed here: a `len == 4` conjunct on the decline
  cannot be seen by a count that another access of the same site already latched.  They are
  rowed OFFLINE in regress/diff_footbridge.c (P-rows), which also pins state PRESERVATION with
  a NONZERO seeded status -- something no stepped guest can reach here (Q2 f).
  S3 (a legal EnableClear write works, a zero write preserves) is E5's row already.

ARM E -- #539's ACCEPT rows, in a FOURTH arm so that arms L/T/K are byte-identical to what
they were.  E carries its own C1/A1 (E0 = 0 is also what an ABSENT device returns, so the
E rows are meaningless unless this arm demonstrably reached the device) and then:
  E0 read IRQEnable before any write            -> 0            (reset value, 7.3.31)
  E1 write P=0x2002 to Set, read               -> P            (readable; catches a bit
                                                                  swap, a constant, a wrong
                                                                  field, a masked value)
  E2 write Q=0x60000000 to Set, read           -> P|Q          (pins |=; bit 30 set so a
                                                                  diagnostic kept for the top
                                                                  bits fires here)
  E3 ldrb  +0x188                              -> 0x02         (low byte: len 1 reaches the
  E6 ldrh  +0x188                              -> 0x2002        same case; the CSR drives
                                                                  D[31:0] and the SA-110 takes
                                                                  the lane, DC21285 3.2.x)
  E5 write P to Clear, read Set                -> Q            (Clear works; = the E2 value
                                                                  with P removed)
  E4 no BRACKETED diagnostic naming footbridge anywhere in arm E -- the `fatals` regex is
     `[ ... footbridge ... ]`, the house diagnostic shape; a kept fatal() with its exit gone
     is caught; a diagnostic rewritten WITHOUT brackets or without the device name is NOT
     (listed under NOT COVERED below)
Execution order is E0,E1,E2,E3,E6,E5: E6 wants 0x2002, which is true only while P is set.
P and Q are loaded from RAM (DATA+8, DATA+12), like 0x12345678: P is not a rotated ARM
immediate (bits 1 and 13); Q is (0x06 ROR 4) and is loaded the same way for uniformity.
Values land in r7,r1,r2,r9,fp,ip; r1/r2 are A2's registers in arm L and are free here
because arm E does not score A2.  TESTED PATTERNS, stated so the contract is checkable:
P = bits 1,13 and Q = bits 29,30 only; bit 31 and every other bit are untested by value.

CONTRACT (what this detector is designed to catch, and what it is not).  On the SET read
branch: the exit reinstated (E0 dies), reinstated only when irq_enable == 0 (E0), a wrong
field/constant/mask/bit-swap (E1, E2), a width guard (E3, E6), a kept diagnostic (E4), a
diagnostic kept for bit 30 (E4; E2 if it exits -- bit 31 is never set here, so a bit-31-only
guard is UNTESTED).  On the CLEAR arms: a broken `&= ~`
(E5).  On the FIVE DECLINED SITES (#545): the exit reinstated at any one site (that N row's
arm dies: N0 and every S row red), the announce unlatched (N-row count 2), a shared or
aggregate latch (N0 count 4 or 1), the +0x18c read leaking irq_enable (N3: 0x30 not 0), a
decline storing into a status field (S1/S2/S4/S5/SF1/SF2), a misnamed register (its N row),
a latch cleared by its own read (N3 count 2).  The harness legs H1/H2 as described above.
NOT COVERED by any GUEST row here: (f) a legal status read narrowed to a CONSTANT 0 -- irq_status
is 0 on every path a stepped guest can reach (the timer assert is host-timer driven and the
host timers are stopped at the prompt; measured with timer 1 armed), so S1/S2/S4/S5/SF1/SF2 pin
the VALUE 0 and catch a widening (`&` -> `|`, `odata = enable`), never a narrowing -- the offline
P-rows in diff_footbridge.c seed a nonzero status and pin that; the FIQ read EXPRESSION is
unpinned everywhere (`fiq_status` has no writer in the tree: `fiqenableread`).  +0x28c
(FIQEnableClear read, the FIQ twin of +0x18c) already declined SILENTLY before #545 and is
deliberately unchanged -- a read of it returns 0 before and after, so there is no witness;
it is `fiqenableread` facet (2), where the Opus seat's dissent (fix it in the same commit)
is recorded verbatim.  190h/290h (IRQSoft/FIQSoft) reach `default:` and announce on every
access: `fbirqsoftunimpl`.  (a) no row observes the
CPU IRQ line -- an edit to the write arm's assert condition (`irq_status | irq_enable`) is
invisible to every row here, because cpu_dyntrans.c suppresses interrupt delivery under
`step` and CPSR I/F stay set; it needs a free-running arm with a positive delivery control,
filed with IRQSoft; (b) +0x189..+0x18b: real hardware selects the same CSR by A[10:2] and
returns lanes 1-3, the model routes them to `default:` and returns 0 -- a device-wide decode
deviation, filed, not rowed; (c) irq_status and fiq_enable are 0 throughout, so a mutant
returning either at +0x188 is caught by E1/E2 only through the value, not distinguished
from a constant 0.  (d) D1 compares the disassembly of every STEPPED word; the landing pad is
planted and never stepped, and a step that ends the process is not compared.  (e) E4 sees only
a BRACKETED diagnostic that names footbridge (the `fatals` regex); a bare-text diagnostic on
the read path escapes it.
TEARDOWN CONVENTION this file's bounded drain rests on: rd() returns True on a select TIMEOUT
and False only on EOF/EIO, so the post-quit drain loop breaks on EOF or its deadline, never on
a quiet interval (the same convention as the two pending probes' Session.rd).

EVERY PLANTED WORD IS CHECKED AGAINST THE DISASSEMBLY THE EMULATOR PRINTS AS IT STEPS IT --
not against a separate `unassemble`, because the step line is the instruction that actually
executed.  This project has a recorded incident where a wrong register field made a gate row
measure the wrong thing for months.

COST, measured: see PROBE_WALL below -- 6 cold-debugger launches (#545: +S, +Q, +H), no boot.  A booting-rig row
was deliberately NOT written: no rig in this tree boots a footbridge machine at all, which is
the gap this probe closes, and adding one would put a load-sensitive wall-clock oracle into a
battery already carrying ~37.

usage: footbridge_sites_probe.py <gxemul-binary> <four-byte-raw-stub>
The stub is the same scaffolding gate_arm.sh writes for testarm: `cats` needs a file
argument to construct, and every word of it is overwritten before anything executes.
"""
import os, pty, re, select, signal, sys, time

BIN = sys.argv[1]
STUB = sys.argv[2]
CODE = 0x00008000
DATA = 0x00009000
NOP = 0xE1A00000
NOPTXT = "mov r0,r0"      #  the EMULATOR's spelling of 0xe1a00000; it does not print "nop"

#  (offset, word, expected disassembly text, comment)
#  Spellings are the EMULATOR's own, not a manual's: "mrc 15,0,r0,cr1,cr0,0" and decimal
#  ldr/str offsets ("[r0,#768]" for 0x300) are what this disassembler prints.
MMU_OFF = [
    (0x00, 0xEE110F10, "mrc 15,0,r0,cr1,cr0,0", "read CP15 c1"),
    (0x04, 0xE3C00001, "bic r0,r0,#1",          "clear the MMU enable bit"),
    (0x08, 0xEE010F10, "mcr 15,0,r0,cr1,cr0,0", "MMU OFF -> VA == PA"),
]
MMU_NOP = [
    (0x00, NOP, NOPTXT, "arm T: MMU LEFT ON -- the negative control"),
    (0x04, NOP, NOPTXT, ""),
    (0x08, NOP, NOPTXT, ""),
]
BODY = [
    (0x0c, 0xEE113F10, "mrc 15,0,r3,cr1,cr0,0", "C2: read CP15 c1 BACK -- measures the state"),
    (0x10, 0xE3A00442, "mov r0,#0x42000000",    "footbridge base (machine_cats.c:64)"),
    (0x14, 0xE3A04A09, "mov r4,#0x9000",        "scratch RAM"),
    (0x18, 0xE5945000, "ldr r5,[r4]",           "C1 liveness: plain RAM, 0x11223344"),
    (0x1c, 0xE5906000, "ldr r6,[r0]",           "A1: VENDOR_ID"),
    (0x20, 0xE5942004, "ldr r2,[r4,#4]",        "load 0x12345678 from RAM"),
    (0x24, 0xE5802300, "str r2,[r0,#768]",      "A2: TIMER_1_LOAD <- 0x12345678"),
    (0x28, 0xE5901300, "ldr r1,[r0,#768]",      "A2: read it back"),
]
KILL_NOP  = (0x2c, NOP,        NOPTXT,             "arm L: no kill site (the +0x18c kill retired by #545)")
TAIL = [(0x30, NOP, NOPTXT, "landing pad -- planted, never stepped")]
REG = dict(r0=0, r1=1, r2=2, r3=3, r4=4, r5=5, r6=6, r7=7, r8=8, r9=9, sl=10, fp=11, ip=12, sp=13, lr=14)
def _mov(rd, imm):                          # imm < 256, rotate 0
    return 0xE3A00000 | (REG[rd] << 12) | imm, "mov %s,#0x%x" % (rd, imm)
def _ldr(rd, off):
    return 0xE5900000 | (REG[rd] << 12) | off, "ldr %s,[r0,#%d]" % (rd, off)
def _str(rd, off):
    return 0xE5800000 | (REG[rd] << 12) | off, "str %s,[r0,#%d]" % (rd, off)
def _w(off, wt, comment):
    return (off, wt[0], wt[1], comment)
#  #545: arm S -- the five declined sites, twice each, one legal sibling read between, one process.
SITES = [
    _w(0x2c, _mov("r8", 0x30),  "IRQ enable <- 0x30 (bits 4,5)"),
    _w(0x30, _str("r8", 0x188), ""),
    _w(0x34, _mov("r9", 0xc0),  "FIQ enable <- 0xc0 (bits 6,7)"),
    _w(0x38, _str("r9", 0x288), ""),
    _w(0x3c, _mov("r2", 0x10),  "the IRQ decline value, inside 0x30"),
    _w(0x40, _str("r2", 0x180), "N1: write IRQ_STATUS (read-only) #1"),
    _w(0x44, _ldr("r7", 0x184), "S2: legal IRQ_RAW_STATUS read between -> 0"),
    _w(0x48, _str("r2", 0x180), "N1: write IRQ_STATUS #2 -- must NOT announce again"),
    _w(0x4c, _str("r2", 0x184), "N2: write IRQ_RAW_STATUS (read-only) #1"),
    _w(0x50, _ldr("sl", 0x180), "S1: legal IRQ_STATUS read between -> 0 (0 & 0x30)"),
    _w(0x54, _str("r2", 0x184), "N2: write IRQ_RAW_STATUS #2"),
    _w(0x58, _ldr("r9", 0x18c), "N3: read IRQ_ENABLE_CLEAR (write-only) #1 -> 0"),
    _w(0x5c, _ldr("fp", 0x188), "S3: legal IRQEnable read between -> 0x30 (intact)"),
    _w(0x60, _ldr("r8", 0x18c), "N3: read IRQ_ENABLE_CLEAR #2 -> 0"),
    _w(0x64, _mov("ip", 0x40),  "the FIQ decline value, inside 0xc0"),
    _w(0x68, _str("ip", 0x280), "N4: write FIQ_STATUS (read-only) #1"),
    _w(0x6c, _ldr("r2", 0x280), "S4: legal FIQ_STATUS read between -> 0 (0 & 0xc0)"),
    _w(0x70, _str("ip", 0x280), "N4: write FIQ_STATUS #2"),
    _w(0x74, _str("ip", 0x284), "N5: write FIQ_RAW_STATUS (read-only) #1"),
    _w(0x78, _ldr("lr", 0x284), "S5: legal FIQ_RAW_STATUS read between -> 0"),
    _w(0x7c, _str("ip", 0x284), "N5: write FIQ_RAW_STATUS #2"),
    _w(0x80, _ldr("r1", 0x184), "SF1: FINAL raw IRQ status after every decline -> 0"),
    _w(0x84, _ldr("sp", 0x284), "SF2: FINAL raw FIQ status after every decline -> 0"),
    (0x88, NOP, NOPTXT, "landing pad -- planted, never stepped"),
]
#  #545: the five announce texts, one per site, in the device's own spelling.  ACCESS-LOCAL: each N row
#  counts ITS text, so a misnamed register reds the row for the site that misnamed it.
TEXTS = {
    "N1": "footbridge write to irq status? (once)",
    "N2": "footbridge write to irq_raw_status (once)",
    "N3": "footbridge read from ENABLE CLEAR? (once)",
    "N4": "footbridge write to fiq status? (once)",
    "N5": "footbridge write to fiq_raw_status (once)",
}
H1_NAME = "no-such-machine-fbd5"      # the unknown -E name for leg H1; the diagnostic must name it
P, Q = 0x00002002, 0x60000000           # #539 arm E values; loaded from DATA+8 / DATA+12
ENABLE = [                              # #539: the ACCEPT rows, order E0,E1,E2,E3,E6,E5
    (0x2c, 0xE5907188, "ldr r7,[r0,#392]",   "E0: read IRQ_ENABLE_SET before any write"),
    (0x30, 0xE5948008, "ldr r8,[r4,#8]",     "r8 = P"),
    (0x34, 0xE5808188, "str r8,[r0,#392]",   "IRQEnableSet <- P"),
    (0x38, 0xE5901188, "ldr r1,[r0,#392]",   "E1: read back -> P"),
    (0x3c, 0xE594900C, "ldr r9,[r4,#12]",    "r9 = Q"),
    (0x40, 0xE5809188, "str r9,[r0,#392]",   "IRQEnableSet <- Q"),
    (0x44, 0xE5902188, "ldr r2,[r0,#392]",   "E2: read back -> P|Q (pins |=)"),
    (0x48, 0xE5D09188, "ldrb r9,[r0,#392]",  "E3: BYTE read -> 0x02"),
    (0x4c, 0xE280AD06, "add sl,r0,#0x180",   "sl = base+0x180 (ldrh offsets cap at 255)"),
    (0x50, 0xE1DAB0B8, "ldrh fp,[sl,#8]",    "E6: HALFWORD read -> 0x2002"),
    (0x54, 0xE580818C, "str r8,[r0,#396]",   "IRQEnableClear <- P"),
    (0x58, 0xE590C188, "ldr ip,[r0,#392]",   "E5: read back -> Q"),
    (0x5c, NOP, NOPTXT, "landing pad -- planted, never stepped"),
]
REGNAME = {10: "sl", 11: "fp", 12: "ip", 13: "sp", 14: "lr"}   # the emulator's spellings (cpu_arm.h ARM_REG_NAMES)


def run_arm(label, prog, emul="cats", quit_leg=False):
    """Plant `prog`, step it one instruction at a time, report registers and liveness.
    #545: `emul` is the -E name (leg H1 passes an unknown one and expects NO prompt); `quit_leg`
    runs leg H2 after the register read -- quit, then one more ordinary interaction, observed
    BEFORE teardown."""
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-T", "-E", emul, "-M", "32",
                        "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""
    dead = [False]

    def rd(t=0.4):
        nonlocal buf
        try:
            r, _, _ = select.select([fd], [], [], t)
        except (OSError, ValueError):
            dead[0] = True
            return False
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            dead[0] = True
            return False
        if not d:
            dead[0] = True
            return False
        buf += d.decode("latin1", "replace")
        return True

    #  Signature order is not free choice: gate_hygiene.sh pins the CANONICAL #392 call form
    #  as a literal `return wait(mark=_mark, echo=<x> if <x> else None)`, tightened three
    #  times because every looser prefix was a substring of the broken form too.  Written any
    #  other way, a probe is simply not covered by that ratchet -- which is worse than failing
    #  it.  So timeout goes last, and send() ends on the pinned form.
    def wait(mark=0, echo=None, timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            resp = buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(x, timeout=60):
        b = (x + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        try:
            while n < len(b):
                n += os.write(fd, b[n:])
        except OSError:
            dead[0] = True
            return False
        return wait(mark=_mark, echo=x if x else None, timeout=timeout)

    status, regs, badis = "?", {}, []
    h2 = {}                        # #545 leg H2 observations, all taken BEFORE teardown
    #  KEYWORD, and this is not style.  A positional wait(120) silently becomes mark=120 under
    #  the pinned parameter order -- a real behaviour change, and the exact mistake the
    #  m8820x probe's conversion had to fix in the same commit.
    if not wait(timeout=120):
        status = "NO-PROMPT"
    else:
        send("put w 0x%08x, 0x%08x" % (DATA, 0x11223344))
        send("put w 0x%08x, 0x%08x" % (DATA + 4, 0x12345678))
        send("put w 0x%08x, 0x%08x" % (DATA + 8, P))
        send("put w 0x%08x, 0x%08x" % (DATA + 12, Q))
        for off, word, _t, _c in prog:
            send("put w 0x%08x, 0x%08x" % (CODE + off, word))
        send("pc=0x%08x" % CODE)
        status = "SURVIVED"
        for off, word, text, _c in prog[:-1]:      # the landing pad is never stepped
            mark = len(buf)
            if not send("step 1", timeout=30) or dead[0]:
                status = "HOST-DIED"
                break
            seg = buf[mark:]
            #  Match the emulator's own step line for THIS address and compare the mnemonic
            #  it printed against what this table says was planted.
            m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + off, word), seg)
            got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no step line)"
            if got != text:
                badis.append("0x%02x planted 0x%08x -> %r, expected %r"
                             % (off, word, got, text))
        if status == "SURVIVED":
            mark = len(buf)
            if send("reg", timeout=30) and not dead[0]:
                for n in (0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
                    mm = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)"
                                   % REGNAME.get(n, "r%d" % n), buf[mark:])
                    if mm:
                        regs[n] = int(mm.group(1), 16)
            else:
                status = "HOST-DIED" if dead[0] else "NO-REG"
        if status == "SURVIVED" and quit_leg:
            #  #545 leg H2.  The prologue is VERIFIED from the fresh `reg` above (values, not the fact
            #  that steps were issued), then `quit`, then ONE MORE ordinary interaction.  `dead` is
            #  read here, before any teardown, and the reap below must say exit 0.  Do not
            #  short-circuit the second send because `dead` is already set: the observation IS that
            #  send() reports the death.
            h2["prologue_ok"] = (len(badis) == 0 and 3 in regs and (regs[3] & 1) == 0
                                 and regs.get(5) == 0x11223344 and regs.get(6) == 0x1011
                                 and regs.get(1) == 0x00345678)
            h2["quit_rc"] = None          # M13q: NO quit either
            try:
                os.close(fd)          # M13: teardown BEFORE the observation
            except OSError:
                pass
            h2["next_rc"] = send("reg", timeout=10)
            h2["dead_before_close"] = dead[0]
    #  #539 (pass 2): the SAME teardown as the two pending probes -- quit, DRAIN to EOF (bounded), close
    #  the master, then a BOUNDED reap (poll 10 s, kill, wait).  The old sleep-0.3-then-close could SIGHUP a
    #  child still shutting down and then block forever in waitpid; and fatals are collected AFTER the
    #  drain so a diagnostic printed during shutdown is not missed.
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    t1 = time.time()
    eof = False
    while time.time() - t1 < 20.0:
        if not rd(0.1):
            eof = True
            break
    fatals = re.findall(r"(\[[^\r\n\]]*footbridge[^\r\n\]]*\])", buf)
    try:
        os.close(fd)
    except OSError:
        pass
    rpid, st, gone = 0, None, False
    t1 = time.time()
    while rpid == 0 and time.time() - t1 < 10.0:
        try:
            rpid, st = os.waitpid(pid, os.WNOHANG)
        except OSError:
            gone = True      # ECHILD: already reaped elsewhere -- its pid may be recycled; never kill it
            break
        if rpid == 0:
            time.sleep(0.05)
    harness_killed = False
    if rpid == 0 and not gone:
        #  F2 (#539): a kill WE fire is labelled (see the pending probes' close()): 20 s drain + 10 s reap.
        harness_killed = True
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass
        try:
            _, st = os.waitpid(pid, 0)
        except OSError:
            st = None
    code = os.WEXITSTATUS(st) if st is not None and os.WIFEXITED(st) else None
    sig = os.WTERMSIG(st) if st is not None and os.WIFSIGNALED(st) else None
    if harness_killed and sig == signal.SIGKILL:
        sig = "HARNESS-KILL(%s)" % sig      # our kill, not a product death (a kill that lands on
                                             # a zombie reaps the product's own status: unlabelled)
    elif not eof and sig is not None:
        sig = "HARNESS-CLOSE(%s)" % sig   # the drain deadline expired; our close HUP'd a live child
    print("  arm %-36s %-9s exit=%-5s signal=%s" % (label, status, code, sig))
    for b in badis:
        print("      DISASSEMBLY MISMATCH: %s" % b)
    #  #545 leg H1: the startup-rejection diagnostic must name THIS run's -E input (machine.c:240).
    reject = ('Sorry, emulation "%s" is unknown' % emul) in buf
    return {"status": status, "regs": regs, "exit": code, "signal": sig,
            "fatals": fatals, "badis": badis, "reject": reject, "h2": h2,
            "prompt": "GXemul>" in buf}


def hexs(v):
    return "-" if v is None else "0x%08x" % v


def row(tag, note, got, want):
    ok = got == want
    print("%-4s %-40s got=%-12s want=%-12s %s"
          % (tag, note, hexs(got), hexs(want), "ok" if ok else "FAIL"))
    return ok


print("BINARY=%s" % BIN)
print("machine: cats/SA110, cold debugger, MMU disabled by the guest, no boot")
t0 = time.time()

L = run_arm("L  live      (MMU off)",      MMU_OFF + BODY + [KILL_NOP] + TAIL)
T = run_arm("T  trap ctrl (MMU LEFT ON)",  MMU_NOP + BODY + [KILL_NOP] + TAIL)
E = run_arm("E  enable    (MMU off,#539)", MMU_OFF + BODY + ENABLE)
S = run_arm("S  declines  (MMU off,#545)", MMU_OFF + BODY + SITES)
QL = run_arm("Q  quit leg  (MMU off,#545)", MMU_OFF + BODY + [KILL_NOP] + TAIL, quit_leg=True)   # not `Q`: that is arm E's constant
H = run_arm("H  startup reject (-E %s)" % H1_NAME, [], emul=H1_NAME)
print()

results = []
#  ---- controls.  A probe whose control row failed has measured NOTHING. ----
c1 = row("C1", "liveness: guest ran, plain RAM readback",
         L["regs"].get(5), 0x11223344)
c2 = row("C2", "MMU really OFF in arm L (CP15 c1 bit 0)",
         (L["regs"][3] & 1) if 3 in L["regs"] else None, 0)
c3 = row("C3", "MMU really ON in arm T (the arms differ)",
         (T["regs"][3] & 1) if 3 in T["regs"] else None, 1)
results += [c1, c2, c3]
#  *** C4 IS THE TRAP GUARD.  Stated as an INEQUALITY on purpose: arm T may read 0, or -T may
#  halt it on the non-existent alias at PA 0x02000000, and both are acceptable outcomes.  What
#  is never acceptable is arm T producing the device's answer, because then arm L's 0x1011 is
#  not evidence of anything.  ***
t_vendor = T["regs"].get(6)
#  #545: the key must be PRESENT -- `None != 0x1011` is True, so a register-parse miss used to green this row.
c4 = 6 in T["regs"] and t_vendor != 0x1011
print("%-4s %-40s got=%-12s want=%-12s %s"
      % ("C4", "MMU-on arm CANNOT see the device", hexs(t_vendor), "!= 0x1011",
         "ok" if c4 else "FAIL"))
if not c4:
    print("      *** THE DISCRIMINATOR IS DEAD: the device answered with the boot-time MMU")
    print("      *** still enabled, so arm L proves nothing about turning it off.  Either the")
    print("      *** cats translation table changed (machine_cats.c:131, cpu_arm.c:239-255)")
    print("      *** or the device moved into the low 256 MB.  Re-derive before believing A1/A2.")
results.append(c4)
#  #545: arm T's exit status was recorded and never required; a control arm that died is not a control.
c5 = T["status"] == "SURVIVED" and T["exit"] == 0
print("%-4s %-40s %-30s %s"
      % ("C5", "MMU-on arm SURVIVES, exit 0", "status=%s exit=%s" % (T["status"], T["exit"]),
         "ok" if c5 else "FAIL"))
results.append(c5)

#  ---- the reachability rows.  VALUES, not survival. ----
a1 = row("A1", "VENDOR_ID through a real guest ldr", L["regs"].get(6), 0x1011)
a2 = row("A2", "TIMER_1_LOAD masked to 24 bits (MAX_VAL)", L["regs"].get(1), 0x00345678)
results.append(a1)
results.append(a2)
#  *** NAME THE RIGHT CAUSE, and this branch is here because the first draft named the WRONG
#  one.  A red A1 has two utterly different causes that look identical -- r6 == 0 -- and the
#  earlier version printed "this is NOT the MMU trap" unconditionally, so on the very run
#  where the MMU trap WAS the cause it pointed the reader at the device.  Measured: the
#  negative-control run (arm L with the three mcr/bic words replaced by nops) printed exactly
#  that misdiagnosis.  A diagnostic that fires on the wrong branch is worse than none.  ***
if not a1:
    if not c2:
        print("      *** THE MMU TRAP, and A1/A2 are NOT evidence about the device: arm L's")
        print("      *** CP15 c1 bit 0 is still SET, so VA 0x42000000 aliased to PA 0x02000000")
        print("      *** (machine_cats.c:131 -> cpu_arm.c:239-255 maps only the low 256 MB) and")
        print("      *** nothing ever addressed the footbridge.  Fix the MMU-off sequence first.")
    elif L["regs"].get(6) == 0:
        print("      NOTE: r6 == 0 with C2 and C4 GREEN is not the MMU trap -- the guest really")
        print("      NOTE: did address PA 0x42000000, so the device is absent or has stopped")
        print("      NOTE: decoding there (memory_device_register / DM_ flags / machine_cats.c:64).")
results.append(row("A2b", "the value the guest actually stored",
                   L["regs"].get(2), 0x12345678))

#  ---- the isolation arm, and the two HARNESS LEGS (#545) that replaced the kill bridge. ----
l_ok = L["status"] == "SURVIVED" and L["exit"] == 0 and not L["fatals"]
print("%-4s %-40s %-30s %s"
      % ("I1", "isolation arm SURVIVES untouched",
         "status=%s exit=%s" % (L["status"], L["exit"]), "ok" if l_ok else "FAIL"))
results.append(l_ok)
#  H1: no prompt AND the diagnostic naming this run's input AND WIFEXITED && == 1 (a signal death has
#  exit None).  Five different startup refusals all exit 1 with no prompt, so the TEXT clause is the one
#  that discriminates (measured, pass 1).
h1_ok = (H["status"] == "NO-PROMPT" and not H["prompt"] and H["reject"]
         and H["exit"] == 1 and H["signal"] is None)
print("%-4s %-40s %-30s %s"
      % ("H1", "startup leg: unknown -E named, exit 1",
         "status=%s exit=%s named=%s" % (H["status"], H["exit"], H["reject"]),
         "ok" if h1_ok else "FAIL"))
print("      startup leg said: %s" % ('Sorry, emulation "%s" is unknown.' % H1_NAME if H["reject"]
                                        else "(the diagnostic did not name the input)"))
results.append(h1_ok)
#  H2: the fresh-reg prologue check AND exit 0 are both load-bearing -- a child dead BEFORE the prologue
#  finished shows `next send fails` and `dead` identically (measured, pass 1).
q2 = QL["h2"]
h2_ok = (QL["status"] == "SURVIVED" and q2.get("prologue_ok") is True and q2.get("next_rc") is False
         and q2.get("dead_before_close") is True and QL["exit"] == 0 and QL["signal"] is None
         and not QL["fatals"])
print("%-4s %-40s %-30s %s"
      % ("H2", "quit leg: verified prologue, dead, exit 0",
         "prologue=%s next=%s dead=%s exit=%s" % (q2.get("prologue_ok"), q2.get("next_rc"),
                                                  q2.get("dead_before_close"), QL["exit"]),
         "ok" if h2_ok else "FAIL"))
results.append(h2_ok)

#  ---- #545: arm S -- the five declined sites, one process. ----
sc1 = row("SC1", "arm S liveness: plain RAM readback", S["regs"].get(5), 0x11223344)
sa1 = row("SA1", "arm S reaches the device: VENDOR_ID", S["regs"].get(6), 0x1011)
results += [sc1, sa1]
results.append(row("S1", "IRQ_STATUS read (0 & 0x30) between declines", S["regs"].get(10), 0))
results.append(row("S2", "IRQ_RAW_STATUS read between declines", S["regs"].get(7), 0))
results.append(row("S3", "IRQEnable intact through the declines", S["regs"].get(11), 0x30))
results.append(row("S4", "FIQ_STATUS read (0 & 0xc0) between declines", S["regs"].get(2), 0))
results.append(row("S5", "FIQ_RAW_STATUS read between declines", S["regs"].get(14), 0))
results.append(row("SF1", "FINAL raw IRQ status after all declines", S["regs"].get(1), 0))
results.append(row("SF2", "FINAL raw FIQ status after all declines", S["regs"].get(13), 0))
n3v_ok = S["regs"].get(9) == 0 and S["regs"].get(8) == 0 and 9 in S["regs"] and 8 in S["regs"]
s_alive = S["status"] == "SURVIVED" and S["exit"] == 0 and S["signal"] is None
n_ok = {}
for tag in ("N1", "N2", "N3", "N4", "N5"):
    cnt = sum(1 for f in S["fatals"] if TEXTS[tag] in f)
    ok = s_alive and cnt == 1 and (n3v_ok if tag == "N3" else True)
    n_ok[tag] = ok
    print("%-4s %-40s %-30s %s"
          % (tag, "%s announced ONCE over two accesses" % TEXTS[tag].split(" (once)")[0][11:],
             "count=%d%s" % (cnt, " r9=%s r8=%s" % (hexs(S["regs"].get(9)), hexs(S["regs"].get(8)))
                                if tag == "N3" else ""),
             "ok" if ok else "FAIL"))
    results.append(ok)
n0_cnt = sum(1 for t in TEXTS.values() if sum(1 for f in S["fatals"] if t in f) == 1)
n0_ok = s_alive and n0_cnt == 5 and len(S["fatals"]) == 5
print("%-4s %-40s %-30s %s"
      % ("N0", "five sites, one process, five distinct once",
         "distinct-once=%d fatals=%d exit=%s" % (n0_cnt, len(S["fatals"]), S["exit"]),
         "ok" if n0_ok else "FAIL"))
results.append(n0_ok)

#  ---- #539: IRQEnable is readable.  Arm E first proves it reached the device (its own C1
#  and A1: E0 == 0 is ALSO what an absent device returns), then the value rows. ----
ec1 = row("EC1", "arm E liveness: plain RAM readback", E["regs"].get(5), 0x11223344)
ea1 = row("EA1", "arm E reaches the device: VENDOR_ID", E["regs"].get(6), 0x1011)
results += [ec1, ea1]
results.append(row("E0", "IRQEnable reads 0 before any write", E["regs"].get(7), 0))
results.append(row("E1", "Set <- P, read back", E["regs"].get(1), P))
results.append(row("E2", "Set <- Q, read back (|=)", E["regs"].get(2), P | Q))
results.append(row("E3", "byte read: low byte", E["regs"].get(9), P & 0xff))
results.append(row("E6", "halfword read: low two bytes", E["regs"].get(11), P & 0xffff))
results.append(row("E5", "Clear <- P, read Set back", E["regs"].get(12), Q))
e_ok = E["status"] == "SURVIVED" and E["exit"] == 0 and not E["fatals"]
print("%-4s %-40s %-30s %s"
      % ("E4", "arm E: no footbridge diagnostic, exit 0",
         "status=%s exit=%s fatals=%d" % (E["status"], E["exit"], len(E["fatals"])),
         "ok" if e_ok else "FAIL"))
results.append(e_ok)

nbad = sum(len(a["badis"]) for a in (L, T, E, S, QL))
print("%-4s %-40s %-30s %s"
      % ("D1", "every planted word disassembled as meant",
         "%d mismatches" % nbad, "ok" if nbad == 0 else "FAIL"))
results.append(nbad == 0)

#  Named, not indexed.  The first version wrote `results[0] and results[1] ...`, which silently
#  re-points at different rows the moment a row is inserted above -- the same class as pinning a
#  row by an id that names a family.
ctrl_ok = c1 and c2 and c3 and c4 and c5 and ec1 and ea1 and sc1 and sa1
print()
print("ROWS=%d of %d" % (sum(1 for r in results if r), len(results)))
print("FOOTBRIDGE_SITES_CONTROL=%s" % ("OK" if ctrl_ok else "BAD"))
print("FOOTBRIDGE_SITES_%s" % ("PASS" if all(results) else "FAIL"))
print("PROBE_WALL=%.1fs for 6 cold-debugger arms" % (time.time() - t0))
