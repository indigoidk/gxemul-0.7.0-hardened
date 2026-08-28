#!/usr/bin/env python3
"""wdcnoirq (#485) -- RUNG-3 WITNESS.

Real guest instructions, through real address decode and real memory_rw, on an
UNMODIFIED in-tree machine description (`-E landisk`).  Nothing is added to the
machine; a disk image is attached, which is ordinary operation.

  usage:  python3 wdcnoirq_rung3_probe.py <gxemul> <kernel> <disk> [tag]

Prints one line per row, then

  WDCNOIRQ_CONTROL=OK|DEAD          the machine came up and answers at all
  WDCNOIRQ_RESULT=<passed>/<total>

=========================================================================================
WHY THIS EXISTS
=========================================================================================
#485 added `d->int_assert = 1;` to the two arms of wdc_command() that terminate a
command with WDCE_ABRT and never raised the completion interrupt -- the six
WDCC_SEC_* opcodes and `default:`.  A seat built and measured a rung-3 witness for
that round and ITS SCRIPT WAS NOT PRESERVED, so the round shipped `detector:` with the
scores standing as a seat's report that nothing could re-run.  This is the rebuild.
The scores it prints are its own, and its transcripts are written beside it.

=========================================================================================
WHY IT MUST FREE-RUN
=========================================================================================
cpu_dyntrans.c gates the whole interrupt-delivery block on `if (!single_step)` --
"Do not cause interrupts while single-stepping.  It is so horribly annoying."  A
STEPPED probe therefore reads "not delivered" on a correct build and on a defective one
alike, which is the vacuous shape in its purest form.  Every delivery row here
breakpoints and `continue`s.

The ASSERT, by contrast, is synchronous: dev_wdc_access() tail-calls dev_wdc_tick(),
which does INTERRUPT_ASSERT(d->irq) whenever d->int_assert is set -- so the request
reaches the CPU inside the guest's own store instruction, and DELIVERY happens on the
next pass of the run loop.  That is why the stepped control rows below are legitimate:
they observe the ABORT BIT, not the interrupt.

=========================================================================================
THE MACHINE, AND EVERY ADDRESS DERIVED RATHER THAN GUESSED
=========================================================================================
machine_landisk.c's MACHINE_SETUP registers

    wdc irq=<machine>.cpu[0].irq[SH4_INTEVT_IRQ10] addr_mult=2 addr=0x14000000

and dev_wdc_access() divides relative_addr by addr_mult, so register N sits at
0x14000000 + 2N.  P2 (0xa0000000..0xbfffffff) maps to `paddr = vaddr & 0x1fffffff`
with no MMU involvement, and is the uncached window a device access must use.

    wd_error   = 1  (wdcreg.h)  ->  0xb4000002
    wd_command = 7  (wdcreg.h)  ->  0xb400000e

RAM is at physical 0x0c000000 (machine_landisk.c), so 0x8c... is its P1 alias.

SH4_INTEVT_IRQ10 is 0x340 (sh4_exception.h).  sh_update_interrupt_priorities() gives
the hardwired IRQ lines `15 - ((intevt - SH4_INTEVT_IRQ0) / 0x20)`, so IRQ10 is
LEVEL 5.  cpu_dyntrans.c delivers when `int_to_assert > 0 && !(sr & SH_SR_BL) &&
IMASK < int_level`, so `sr = 0x40000000` -- MD=1, BL=0, IMASK=0 -- admits it.  Reset
leaves IMASK at 15, which would refuse IRQ10 and make every delivery row vacuous.
cpu_sh.c's sh_exception() sets `cpu->pc = vbr + 0x600` for an interrupt.

=========================================================================================
THE ORACLE FOR "DELIVERED", AND WHY IT IS NOT "THE DEBUGGER ANSWERED"
=========================================================================================
cpu_dyntrans.c prints `BREAKPOINT: pc = 0x...` through fatal(), which has no
quiet_mode early-out (debugmsg.c), so a breakpoint hit is un-silenceable and it NAMES
THE ADDRESS.  The rows therefore report the address the breakpoint names and compare it
against the interrupt vector, rather than the weaker "the process came back to a
prompt" -- which is also true of a hundred other ways of stopping.

Not delivered: the guest sits in the `bra .` self-loop at CODE+2 forever and nothing is
printed.  The two readings are POSITIVE-vs-ABSENT on a named address, in the same
script, on two builds.

=========================================================================================
"SILENT" IS MADE INTO A POSITIVE READING, IN THE SAME SESSION
=========================================================================================
An absence proves nothing until you know the stimulus arrived.  Each delivery leg is
therefore broken back into the debugger with SIGINT after its spin -- emul.c installs
debugger_activate as the SIGINT handler for exactly this -- and the ERROR register is
then read BY A GUEST LOAD at a second code address.

    0xF5 / 0xAA  ->  ERROR == 0x04 (WDCE_ABRT) on BOTH builds
    power-on         ERROR == 0x01 (DEVINIT's `d->error = 1`)

So on the PRE-FIX build the leg says, in one session: the free-running store reached
wdc_command(), the arm ran and set the abort bit, AND no interrupt was delivered.
Without that read, "silent" would be indistinguishable from a store that never landed.

The 0xAA leg carries a second, independent proof on a different channel: the
un-silenceable `[ wdc: WARNING! Unimplemented command 0xaa ... ]` fatal() appears in the
FREE-RUNNING transcript.  Two channels, one fact -- which is the device-signature
discipline applied to the stimulus instead of to the observable.

=========================================================================================
A DISK IMAGE IS REQUIRED, AND WITHOUT IT EVERY ROW IS VACUOUS
=========================================================================================
wdc_command() opens with

    if (!diskimage_exist(cpu->machine, d->drive + d->base_drive, DISKIMAGE_IDE)) {
            ...  d->error |= WDCE_ABRT;  d->int_assert = 1;  return;  }

*** THAT EARLY RETURN ALREADY ASSERTS ON BOTH BUILDS. ***  Run without `-d`, and 0xF5
and 0xAA deliver an interrupt on the PRE-FIX binary too -- every row green, nothing
measured, and the probe would report the fix as unnecessary.  `-d iR:<img>` attaches the
image as IDE unit 0 (diskimage.c's 'i' prefix); d->base_drive is 0 for addr 0x14000000
and d->drive is 0 until the guest writes SDH, so diskimage_exist() is true and the
switch is reached.

The `iR:` spelling is exact: ALL prefix chars come before a SINGLE colon, and `R`
discards guest writes into a pid-unique overlay so repeated runs cannot inherit state.

*** AND THAT IS MEASURED, NOT ARGUED.  Set WDCNOIRQ_NODISK=1 and the probe drops the
`-d` and runs the identical rows. ***  On the PRE-FIX binary the two defect rows then
go GREEN -- the no-disk early return asserts for every opcode -- so a witness built
without a disk would have reported the unfixed build as fixed on exactly the two rows
the round is about.  The `unimpl aa warn` row is what names the reason: it reads 0,
because wdc_command() returned before the switch and the arm never ran.

=========================================================================================
THE ROWS
=========================================================================================
  sec f5 irq        *** DEFECT ***    0xF5 WDCC_SEC_FREEZE_LOCK -> interrupt delivered
  sec f5 landed     STIMULUS PROOF    ERROR after that free-running store == 0x04
  unimpl aa irq     *** DEFECT ***    0xAA (no case in the switch) -> interrupt delivered
  unimpl aa warn    STIMULUS PROOF    the free run printed the unimplemented-command
                                      fatal() exactly once
  unimpl aa landed  STIMULUS PROOF    ERROR after that free-running store == 0x04
  live ec irq       LIVENESS          0xEC WDCC_IDENTIFY already asserted before #485,
                                      so it must deliver on BOTH builds.  A row green on
                                      the pre-fix build is what separates "the fix works"
                                      from "this script cannot deliver anything"
  attrib noram      ATTRIBUTION       the SAME instruction, the same sr/vbr/breakpoint
                                      and the same free-run, with the store aimed at RAM
                                      instead of at the command register -- so a delivery
                                      seen above cannot be the RTC, the SCIF or a timer.
                                      It carries its own execution proof: the store is
                                      stepped and dumped BEFORE the free-run, so "silent"
                                      cannot mean "the guest never ran"
  devsig err        DEVICE SIGNATURE  the ERROR register by a guest load, before and
                                      after a 0xF5 store: 0x01 -> 0x04.  RAM answers 0x00
                                      both times and cannot CHANGE as a result of a
                                      command, so the responder is the device
  ram live          ENCODING CONTROL  the identical mov.b store/load pair against plain
                                      RAM.  Without it, a device row reading 0x00 could
                                      be blamed on a bad hand-assembled encoding

*** THE DEVICE-SIGNATURE ROW IS DELIBERATELY NOT READ INSIDE THE HANDLER. ***  Reading
it only when the interrupt lands makes it unmeasurable on the build where the interrupt
does NOT land, so the row would fail for two reasons at once and could not tell them
apart.  It runs unconditionally, in its own stepped session, on both builds.
"""
import os
import pty
import re
import select
import signal
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]
DISK = sys.argv[3]
TAG = sys.argv[4] if len(sys.argv) > 4 else "run"

#  ---- addresses, all derived above ------------------------------------------------
WDC = 0xb4000000
WD_ERROR = WDC + 2                 # reg 1 * addr_mult 2
WD_CMD = WDC + 14                  # reg 7 * addr_mult 2

CODE = 0x8c010000                  # the free-running stimulus
SCRATCH = 0x8c011000               # RAM target for the attribution / encoding rows
READBACK = 0x8c012000              # the post-SIGINT ERROR read, kept clear of CODE
VBR = 0x8c020000
HANDLER = VBR + 0x600

#  ---- opcodes ---------------------------------------------------------------------
#  mov.b Rm,@Rn  = 0010 nnnn mmmm 0000 ;  mov.b @Rm,Rn = 0110 nnnn mmmm 0000
NOP = 0x0009
BRA_SELF = 0xaffe
MOVB_R8_AT_R7 = 0x2780             # mov.b r8,@r7
MOVB_R8_AT_R3 = 0x2380             # mov.b r8,@r3
MOVB_AT_R1_R2 = 0x6210             # mov.b @r1,r2
MOVB_AT_R1_R4 = 0x6410             # mov.b @r1,r4

SPIN = 5.0                         # after `continue`; the assert is synchronous
SETTLE = 8.0

BP_ANY = re.compile(r"BREAKPOINT: pc = (0x[0-9a-f]+)")
P_UNIMPL = re.compile(r"wdc: WARNING! Unimplemented command")

#  The negative control for the paragraph above: run the identical rows with no disk
#  attached and watch the two defect rows go green on the pre-fix build.
NODISK = os.environ.get("WDCNOIRQ_NODISK") == "1"

LOGS = []


def session(cmds, label, settle=SETTLE, spin=SPIN, post=None, disk=True):
    """Drive one emulator.  Returns the whole transcript.

    `post` is a command list run AFTER a SIGINT that follows the spin.  A leg that
    does not deliver is still free-running the guest, so there is no prompt to type
    at; SIGINT is what makes the not-delivered case measurable rather than merely
    empty.  The session is ALWAYS killed with SIGKILL at the end, because a polite
    `quit` would hang on exactly the rows the defect owns.
    """
    argv = [BIN, "-V", "-E", "landisk", "-M", "64"]
    if disk and not NODISK:
        argv += ["-d", "iR:" + DISK]
    argv.append(KERNEL)
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, argv)
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

    def send(c, t):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            return False
        return rd(t)

    rd(settle)
    for i, c in enumerate(cmds):
        if not send(c, spin if i == len(cmds) - 1 else 0.4):
            break
    if post:
        try:
            os.kill(pid, signal.SIGINT)
        except OSError:
            pass
        rd(1.5)
        #  debugger_activate() injects a ctrl-C into the input queue when the
        #  debugger is ALREADY at a prompt (the delivered case), which aborts the
        #  current line.  One bare newline flushes that before the real commands.
        send("", 0.4)
        for c in post:
            if not send(c, 0.6):
                break
    try:
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    LOGS.append((label, " ".join(argv), cmds, post or [], buf))
    return buf


def put(at, ops):
    return ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]


def delivered(t):
    """The address the breakpoint named, or "silent".

    Reported as an ADDRESS rather than as a boolean, so a breakpoint hit somewhere
    unexpected reads as itself instead of as a pass.
    """
    m = BP_ANY.search(t)
    return ("0x%08x" % int(m.group(1), 16)) if m else "silent"


def deliver(cmd_reg, opcode):
    """Free-run ONE guest byte store to the command register, then park in a
    self-loop.  The handler is three real instructions so the fetch after the vector
    succeeds; the breakpoint stops the guest at its first one."""
    return (put(HANDLER, [NOP, BRA_SELF, NOP])
            + put(CODE, [MOVB_R8_AT_R7, BRA_SELF, NOP])
            + ["r7=0x%x" % cmd_reg, "r8=0x%08x" % opcode,
               "pc=0x%x" % CODE,
               "sr=0x40000000", "vbr=0x%x" % VBR,
               "breakpoint add 0x%x" % HANDLER,
               "continue"])


def read_error():
    """Post-SIGINT: read the wdc ERROR register with a real guest load."""
    return (put(READBACK, [MOVB_AT_R1_R2, BRA_SELF, NOP])
            + ["r1=0x%x" % WD_ERROR, "r2=0x0",
               "pc=0x%x" % READBACK, "step 1", "print r2"])


rows = []


def row(name, got, want, note):
    ok = (got == want)
    rows.append((name, ok))
    print("%-17s %-24s %-24s %-40s %s"
          % (name, got, want, note, "ok" if ok else "FAIL"))


def printed(t, reg):
    m = re.findall(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return "0x%02x" % (int(m[-1], 16) & 0xff) if m else "absent"


def dumped(t):
    """One word out of the LAST `dump`, byte-swapped.

    `dump` prints bytes in memory order and this CPU is little-endian, so the digits
    must be swapped -- a raw string compare passes on palindromes and fails on
    everything else for the wrong reason.
    """
    m = re.search(r"0x0*[0-9a-f]+\s+([0-9a-f]{8})", t.split("dump")[-1])
    return "0x%08x" % int.from_bytes(bytes.fromhex(m.group(1)), "little") if m else "nodump"


#  ---- CONTROL: does this machine come up and answer at all? -------------------------
ctl = session(["print 0x1234"], "control", spin=1.5)
alive = ("0x1234" in ctl) or ("4660" in ctl)
print("WDCNOIRQ_DISK=%s" % ("NONE (negative control)" if NODISK else DISK))
print("WDCNOIRQ_CONTROL=%s" % ("OK" if alive else "DEAD"))
if not alive:
    print("WDCNOIRQ_RESULT=0/0")
    sys.exit(0)

VEC = "0x%08x" % HANDLER

#  ---- R1 / R2: the WDCC_SEC_* arm ---------------------------------------------------
t = session(deliver(WD_CMD, 0xf5), "sec_f5", post=read_error())
row("sec f5 irq", delivered(t), VEC, "0xF5 WDCC_SEC_FREEZE_LOCK")
row("sec f5 landed", printed(t, "r2"), "0x04", "WDCE_ABRT: the arm ran, free-running")

#  ---- R3 / R4 / R5: the default: arm ------------------------------------------------
t = session(deliver(WD_CMD, 0xaa), "unimpl_aa", post=read_error())
row("unimpl aa irq", delivered(t), VEC, "0xAA -> the default: arm")
row("unimpl aa warn", str(len(P_UNIMPL.findall(t))), "1",
    "un-silenceable fatal() during the free run")
row("unimpl aa landed", printed(t, "r2"), "0x04", "WDCE_ABRT: the arm ran, free-running")

#  ---- R6: LIVENESS -- a command that asserted BEFORE the fix ------------------------
t = session(deliver(WD_CMD, 0xec), "live_ec")
row("live ec irq", delivered(t), VEC, "0xEC IDENTIFY: green on BOTH builds")

#  ---- R7: ATTRIBUTION -- same everything, store aimed at RAM ------------------------
#  The store is stepped and dumped first so the row cannot pass by the guest simply
#  never running; then the pc is rewound and the SAME instruction is free-run.
t = session(put(HANDLER, [NOP, BRA_SELF, NOP])
            + put(CODE, [MOVB_R8_AT_R7, BRA_SELF, NOP])
            + ["put w 0x%x, 0x00000000" % SCRATCH,
               "r7=0x%x" % SCRATCH, "r8=0x000000f5",
               "pc=0x%x" % CODE, "step 1",
               "dump 0x%x 0x%x" % (SCRATCH, SCRATCH + 4),
               "pc=0x%x" % CODE,
               "sr=0x40000000", "vbr=0x%x" % VBR,
               "breakpoint add 0x%x" % HANDLER,
               "continue"], "attrib")
row("attrib noram", "%s/%s" % (dumped(t), delivered(t)), "0x000000f5/silent",
    "same store, RAM target: nothing fires")

#  ---- R8: DEVICE SIGNATURE -- the ERROR register across a 0xF5 store -----------------
#  Stepped on purpose: the ABORT BIT is observable on BOTH builds whether or not the
#  interrupt is delivered, so this row is never confounded with delivery.
t = session(put(CODE, [MOVB_AT_R1_R2, MOVB_R8_AT_R3, MOVB_AT_R1_R4, BRA_SELF, NOP])
            + ["r1=0x%x" % WD_ERROR, "r3=0x%x" % WD_CMD, "r8=0x000000f5",
               "r2=0x0", "r4=0x0",
               "pc=0x%x" % CODE, "step 3",
               "print r2", "print r4"], "devsig", spin=1.5)
row("devsig err", "%s->%s" % (printed(t, "r2"), printed(t, "r4")), "0x01->0x04",
    "power-on d->error, then WDCE_ABRT")

#  ---- R9: ENCODING CONTROL -- the same shapes against plain RAM ----------------------
t = session(put(CODE, [MOVB_R8_AT_R3, MOVB_AT_R1_R2, BRA_SELF, NOP])
            + ["put w 0x%x, 0x00000000" % SCRATCH,
               "r1=0x%x" % SCRATCH, "r3=0x%x" % SCRATCH, "r8=0x0000005a",
               "r2=0x0",
               "pc=0x%x" % CODE, "step 2",
               "print r2"], "ramlive", spin=1.5)
row("ram live", printed(t, "r2"), "0x5a", "mov.b store/load pair works")

print("WDCNOIRQ_RESULT=%d/%d" % (sum(1 for _, ok in rows if ok), len(rows)))

#  ---- transcripts, because a score with no log is a claim ---------------------------
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "transcript_%s.log" % TAG)
with open(out, "w", encoding="utf-8") as f:
    f.write("binary : %s\nkernel : %s\ndisk   : %s\n\n" % (BIN, KERNEL, DISK))
    for label, argv, cmds, post, buf in LOGS:
        f.write("=" * 88 + "\nLEG %s\n  %s\n" % (label, argv))
        for c in cmds:
            f.write("    > %s\n" % c)
        if post:
            f.write("    -- SIGINT --\n")
            for c in post:
                f.write("    > %s\n" % c)
        f.write("-" * 88 + "\n" + buf + "\n")
print("transcript: %s" % out)
