#!/usr/bin/env python3
"""jazz_vector_probe.py <gxemul-binary> [kernel] -- #578 `jazzvecdeassert` (OB-22): the Jazz/R4030 interrupt-source register and
the CPU's IRQ3 line, 26 rows, cold debugger, self-contained (no import outside the standard library).

THE DEFECT (GXEMUL-SEC/src/devices/dev_jazz.c, DEVICE_ACCESS(jazz_jazzio), HEAD 3cb8bdc1 :696-697): EVERY access to the pica_jazzio
register (physical 0xf0000000, 4 bytes; offset 0 is the local-bus interrupt-source vector, offset 2 the local-bus interrupt-enable word
PICA_SYS_LB_IE that the model stores as jazz_timer_value) ended with an unconditional INTERRUPT_DEASSERT(d->mips_irq_3) ("This is
needed by Windows NT during startup").  With a second JAZZ line still pending, a guest's vector read for the first dropped the CPU's
IRQ3 while a level interrupt was outstanding, until some line was asserted anew or the EXT_IMASK enable TRANSITIONED (a same-value
rewrite heals nothing).  #578 DELETES the tail's deassert: the CPU line is kept by jazz_interrupt_assert()/_deassert() and the EXT_IMASK
write arm, which keep it EQUAL to "(int_asserted & 0x7fff) && (int_enable_mask & R4030_EXT_IP3)" -- the assert handler raises it on
EVERY call made while that predicate holds (level, not edge: a tick re-asserting a still-pending line heals a drop), the deassert handler
lowers it on every call made while the predicate is false, and the mask arm acts on the predicate's TRANSITIONS (a same-value rewrite
moves nothing); those three are the only writers of the line (the census at pass 1, re-run at pass 2:
dev_jazz.c :144, :154, :467/:469 at HEAD 37b04798; the MIPS mtc0 Cause arm writes IP0/IP1 only), so a conditional deassert at the tail
could never fire with an effect; measured equivalent (M_del 13 of 13 on the 13-row witness; M_cond 22 of 22 on table 2).

VEHICLE: the UNMODIFIED in-tree arc/pica machine (`-V -e pica`, the rig kernel loaded for construction only).  Every device access is a
genuine guest instruction through XKPHYS (one-instruction stubs sb/sh/lbu/sw/lw placed in KSEG0 scratch RAM and run with `step`), never
a debugger `put`; the CPU-side observable is COP0 Cause's IP3 bit, masked (`cause & 0x800`; mips_irq_3 is `1 << (STATUS_IM_SHIFT + 3)`,
cpu_mips.c), read with `print cause`.  No interrupt is ever DELIVERED (Status.IE is clear on the cold CPU and the debugger does not
dispatch exceptions while stepping); Cause.IP reflects the asserted lines regardless.  Two JAZZ lines are driven from the two ns16550
UARTs machine_arc.c wires for pica (0x80006000 = jazz.8, 0x80007000 = jazz.9): a UART asserts its line SYNCHRONOUSLY inside the guest's
IER store (dev_ns16550.c: the IER write sets IIR_TXRDY and calls dev_ns16550_tick, which asserts when MCR.IENABLE is set), so the whole
probe runs under single-step.  STEP BUDGET: DEVICE_TICK(ns16550) re-asserts a pending UART line on every tick (TICK_SHIFT 14 = every
16384 single-steps), so the pre-fix red rows are deterministic only while a run stays far inside one tick period; this probe issues
well under a hundred steps.  Nothing here free-runs and no oracle is wall-clock (a pty timeout yields None and therefore FAIL, never a
false pass).  The driver records any timed-out or failed command (JAZZVEC_DRIVER=bad at the end, checked by the gate): a store the
debugger never executed would otherwise look exactly like a fixed build on every IP3 row that follows it.

ROWS (want on the FIXED build; HEAD's reading in brackets where it differs):
  jz imask       EXT_IMASK reads back 0x2 after the guest store            device signature of the R4030 register; enables IP3
  jz com0 mcr    com0 MCR reads back 0x8 (IENABLE/OUT2 set explicitly)      the UART may drive its line; checked, not assumed
  jz com0 ier    com0 IER reads back 0x2                                     device signature of the UART
  jz ip one      Cause.IP3 set after com0's IER write                        LIVENESS of the interrupt path to the CPU
  jz ip both     Cause.IP3 set after com1's IER write too
  jz vec         vector reads 0x24 = (8 + 1) << 2                            device signature of jazzio: RAM cannot answer this
  jz ip after    Cause.IP3 STILL set after that vector read   [HEAD: 0 -- THE DEFECT, two lines pending]
  jz vec again   a second vector read still 0x24                             the read clears no line (pins against a clear-on-read remedy)
  jz vec byte    a BYTE read of the vector returns 0x24                      the guest's own access width: OpenBSD's pica_iointr reads
                                                                             the vector with inb(PVIS) (picabus.c)
  jz ip vecb     IP3 STILL set after that byte read         [HEAD: 0]        THE DEFECT at the guest's own width: label (0, read), len 1
  jz ip vecw     IP3 set after a guest STORE to offset 0      [HEAD: 0]      the tail is reached from every access: label (0, write)
  jz ip lbie     IP3 set after a byte read at offset 2        [HEAD: 0]      label (2, read)   -- LB_IE in the guest's own header
  jz ip lbiew    IP3 set after a HALFWORD store of 0x0f at offset 2 [HEAD: 0]  label (2, write); the only 16-bit access and the only
                                                                             nonzero LB_IE value: pins `len == 2`, `idata != 0` and
                                                                             `jazz_timer_value != 0` (nonzero from here on; the
                                                                             "Linux?" tick arm it arms is inert under step: its
                                                                             count comes from a host timer the debugger stops)
  jz lbie rb     a byte read at offset 2 returns 0x0f                        the store landed (device signature of LB_IE)
  jz ip dflt     IP3 set after a byte read at offset 1        [HEAD: 0]      the default: arm (one unlatched fatal() print)
  jz ip dfltw    IP3 set after a byte store of 0x5a at offset 3 [HEAD: 0]    label (default, write) -- the sixth label cell, at the
                                                                             page's other default offset; one more unlatched fatal()
  jz vec com1    com0's IER cleared: the vector names line 9, 0x28
  jz ip com1     IP3 set with com1 alone pending              [HEAD: 0]      stacked on the earlier drop; does not localise by itself
  jz ip onevec   com1 re-raised alone, then one vector read   [HEAD: 0]      the clean one-line-pending cell
  jz ip reheal   re-enabling com0's IER re-asserts IP3                       the self-healing mechanism, as a control
  jz ip maskoff  EXT_IMASK cleared with lines pending: IP3 clear             the mask arm; green on both builds (no-regression row)
  jz vec masked  the vector still names line 8 with IP3 masked               the vector ignores the enable mask (pinned as current behaviour)
  jz ip maskon   EXT_IMASK restored: IP3 set again                           the mask arm's re-assert
  jz ip none     both IERs cleared: IP3 clear                                the deassert handler with nothing pending
  jz vec none    vector reads 0 with nothing pending
  jz ip nt       IP3 clear after a vector read with nothing pending          NO-REGRESSION row: IP3 is already clear here on every build,
                                                                             so no mutant of the tail can red it; it pins the case the
                                                                             old "Windows NT" comment named
CONTRACT (clause (e)): the rows drive lines 8 and 9 only and the mask values 0x2 and 0 only; a re-introduction of the removed deassert
keyed to lines this table does not drive, directly (`if (int_asserted & 0x7cff)`) or as the complement of the driven pair
(`if (!(int_asserted & 0x0300))`), to the timer line, or to a mask value other than those two, is disclosed, not rowed.  Every
access-label cell of the enclosing function's own tests -- {0, 2, default} x {read, write}, six cells -- is rowed with lines pending
(vec/vecb/after/onevec/com1, vecw, lbie, lbiew, dflt, dfltw), so a re-introduction keyed to ONE of those two inputs, or to one of the six
cell keys, reds (measured: table 3); the default cell is driven at offset 1 (read) and offset 3 (written) only, so a refinement of that
cell by an offset the body does not distinguish (`relative_addr == 1 && writeflag == MEM_WRITE`, `relative_addr == 3 && writeflag ==
MEM_READ`) is clause-(e) debt, disclosed.  The function's other inputs are each driven at two or more values with a pending-lines row on
each side -- `len` 1 (vec byte, lbie, dflt, dfltw), 2 (lbiew), 4 (vec, vecw); `idata` 0 (vecw) and nonzero (lbiew 0x0f, dfltw 0x5a);
`jazz_timer_value` 0 until lbiew's store and 0x0f from lbiew on (lbiew's own IP3 row sees the new value) -- so a re-introduction keyed to
any ONE of them AT THE VALUES THE ROWS DRIVE reds -- zero against nonzero, one width against another (measured: table 3) -- while a
predicate that separates values INSIDE a driven side (`idata & 0xff00`: every stored value is below 0x100) or that names a value no row
drives (`idata == 0x5b`, `len == 8`, `jazz_timer_value == 0x10`) is clause-(e) debt, disclosed (SAMPLED, not EXHAUSTED: the body tests
none of these inputs as a case).  OpenBSD/arc makes THREE access shapes to this register (Grok, F2, from the guest's source):
inb(PVIS) -- offset 0 read as a byte (`relative_addr == 0 && len == 1`), rowed by `jz ip vecb`; out16(PICA_SYS_LB_IE, 0) at initcpu --
a ZERO halfword store at offset 2, NOT rowed (lbiew stores 0x0f); and out16(PICA_SYS_LB_IE, local_int_mask) at intr_establish, whose
COM enable bits are 0x0100 and 0x0200 -- NOT rowed (lbiew's 0x0f has neither bit), so `if (writeflag == MEM_WRITE && relative_addr == 2 &&
(idata & 0x0100))` is predicted to keep every row green and is guest-visible.  Both stores are clause-(e) debt, DISCLOSED and FILED (`jazzvecrowsowed`: a zero
halfword store row and lbiew at 0x0300 close them).  Any other conjunction of two or more inputs that selects no rowed cell (`len == 2 &&
relative_addr == 0`, `relative_addr == 2 && len == 4`, `len == 2 && writeflag == MEM_READ` -- whether a guest reads LB_IE at 16 bits was
not checked here, `idata != 0 && relative_addr == 2 && len == 1`) is clause-(e) debt, disclosed.  `jz lbie rb`'s own read is a blind
access (its IP3 is not checked before the next reheal), so a form aimed only at it stays green.  Names
stay at 13 characters or fewer (`%-14s`; the gate anchors `^name  .*ok$` with two spaces).  Ends with JAZZVEC_RESULT=n/N,
JAZZVEC_DRIVER=ok|bad and JAZZVEC_DONE.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2] if len(sys.argv) > 2 else "/mnt/c/DocumentNoSnc/CC/GXEMUL/gxemul_arc_rig/bsd"

XK = 0x9000000000000000
JAZZ = XK | 0x80000000
EXT_IMASK = JAZZ + 0xe8          # R4030_SYS_EXT_IMASK (pica.h: R4030 + 0x00e8)
COM0 = XK | 0x80006000           # ns16550 at jazz.8
COM1 = XK | 0x80007000           # ns16550 at jazz.9
VEC = XK | 0xf0000000            # pica_jazzio: offset 0 the vector, offset 2 LB_IE
IER, MCR = 1, 4                  # ns16550 register offsets (addrmult 1)
IP3 = 0x800                      # mips_irq_3 in COP0 Cause
R4030_EXT_IP3 = 0x02
SCRATCH = 0xffffffff80010000     # KSEG0 RAM: safe to overwrite and execute
STUBS = {"sb": 0xa0220000, "sh": 0xa4220000, "lbu": 0x90220000, "sw": 0xac220000, "lw": 0x8c220000}   # <op> v0,0(at)

rows = []


def row(name, got, want):
    ok = (got == want)
    rows.append(ok)
    g = "None" if got is None else "0x%x" % got
    print("%-14s %-24s %-24s %s" % (name, g, "0x%x" % want, "ok" if ok else "FAIL"), flush=True)


class Emu(object):
    """One GXemul -V session on a pty, driven by prompt detection (never by fixed waits)."""

    def __init__(self, argv, log):
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            try:
                os.execvp(argv[0], argv)
            finally:
                os._exit(127)
        self.buf = ""
        self.dead = False
        self.bad = False          # set by any command that died or timed out; reported as JAZZVEC_DRIVER=bad
        self.log = log
        self.wait(timeout=30)

    def rd(self, t=0.2):
        r, _, _ = select.select([self.fd], [], [], t)
        if self.fd not in r:
            return True
        try:
            d = os.read(self.fd, 65536)
        except OSError:
            self.dead = True
            return False
        if not d:
            self.dead = True
            return False
        self.buf += d.decode("latin1", "replace")
        return True

    def wait(self, mark=0, timeout=20):
        t = time.time()
        while time.time() - t < timeout:
            if not self.rd():
                return False
            if len(self.buf) > mark and self.buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False

    def send(self, cmd, timeout=20):
        if self.dead:
            self.bad = True
            return None
        mark = len(self.buf)
        data = (cmd + chr(10)).encode("latin1")
        while data:
            try:
                n = os.write(self.fd, data)
            except OSError:
                self.dead = True
                self.bad = True
                return None
            data = data[n:]
            if data:
                self.rd(0.05)
        if not self.wait(mark, timeout):
            self.bad = True
            return None
        return self.buf[mark:]

    def put_word(self, addr, word):
        return self.send("put w 0x%x, 0x%08x" % (addr, word & 0xffffffff))

    def set_reg(self, name, value):
        return self.send("%s=0x%x" % (name, value & 0xffffffffffffffff))

    def read_reg(self, name):
        out = self.send("print %s" % name)
        if out is None:
            return None
        m = re.search(re.escape(name) + r"\s*=\s*0x([0-9a-fA-F]+)", out)
        if m:
            return int(m.group(1), 16)
        idx = out.find(name)
        tail = out[idx + len(name):] if idx >= 0 else out
        m = re.search(r"0x([0-9a-fA-F]+)", tail)
        return int(m.group(1), 16) if m else None

    def exec_stub(self, op, addr, value=0):
        """One genuine guest instruction: <op> v0,0(at) with at = addr, v0 = value; returns v0 afterwards."""
        a = self.set_reg("v0", value)
        b = self.set_reg("at", addr)
        c = self.set_reg("pc", self.stub[op])
        d = self.send("step")
        if None in (a, b, c, d):
            self.bad = True       # the instruction may never have executed: a skipped store must not read as a fixed build
            return None
        return self.read_reg("v0")

    def close(self):
        bad = self.bad            # `quit` ends the session without a prompt: not a driver failure
        try:
            self.send("quit", timeout=5)
        except Exception:
            pass
        self.bad = bad
        try:
            os.waitpid(self.pid, 0)
        except Exception:
            pass
        if self.log:
            with open(self.log, "w", encoding="utf-8", newline=chr(10)) as f:
                f.write(self.buf)


log = os.environ.get("JAZZVEC_LOG") or ("/tmp/jazzvec_%d.log" % os.getpid())
emu = Emu([BIN, "-V", "-e", "pica", KERNEL], log)
emu.stub = {}
for i, (name, word) in enumerate(sorted(STUBS.items())):
    emu.stub[name] = SCRATCH + 4 * i
    emu.put_word(emu.stub[name], word)
print("JAZZVEC binary=%s log=%s" % (BIN, log), flush=True)


def st8(a, v):
    emu.exec_stub("sb", a, v)


def st16(a, v):
    emu.exec_stub("sh", a, v)


def st32(a, v):
    emu.exec_stub("sw", a, v)


def ld8(a):
    v = emu.exec_stub("lbu", a)
    return None if v is None else v & 0xff


def ld32(a):
    v = emu.exec_stub("lw", a)
    return None if v is None else v & 0xffffffff


def ip3():
    c = emu.read_reg("cause")
    return None if c is None else c & IP3


def reheal():
    """A fresh com0 assert (IER 0 then 2) re-raises IRQ3 on every build."""
    st8(COM0 + IER, 0x00)
    st8(COM0 + IER, 0x02)


st32(EXT_IMASK, R4030_EXT_IP3)
row("jz imask", ld32(EXT_IMASK), R4030_EXT_IP3)
st8(COM0 + MCR, 0x08)
row("jz com0 mcr", ld8(COM0 + MCR), 0x08)
st8(COM0 + IER, 0x02)
row("jz com0 ier", ld8(COM0 + IER), 0x02)
row("jz ip one", ip3(), IP3)
st8(COM1 + MCR, 0x08)
st8(COM1 + IER, 0x02)
row("jz ip both", ip3(), IP3)
row("jz vec", ld32(VEC), (8 + 1) << 2)
row("jz ip after", ip3(), IP3)
row("jz vec again", ld32(VEC), (8 + 1) << 2)
reheal()
row("jz vec byte", ld8(VEC), (8 + 1) << 2)
row("jz ip vecb", ip3(), IP3)
reheal(); st32(VEC, 0)
row("jz ip vecw", ip3(), IP3)
reheal(); ld8(VEC + 2)
row("jz ip lbie", ip3(), IP3)
reheal(); st16(VEC + 2, 0x0f)
row("jz ip lbiew", ip3(), IP3)
row("jz lbie rb", ld8(VEC + 2), 0x0f)
reheal(); ld8(VEC + 1)
row("jz ip dflt", ip3(), IP3)
reheal(); st8(VEC + 3, 0x5a)
row("jz ip dfltw", ip3(), IP3)
st8(COM0 + IER, 0x00)
row("jz vec com1", ld32(VEC), (9 + 1) << 2)
row("jz ip com1", ip3(), IP3)
st8(COM1 + IER, 0x00); st8(COM1 + IER, 0x02); ld32(VEC)
row("jz ip onevec", ip3(), IP3)
st8(COM0 + IER, 0x02)
row("jz ip reheal", ip3(), IP3)
st32(EXT_IMASK, 0)
row("jz ip maskoff", ip3(), 0)
row("jz vec masked", ld32(VEC), (8 + 1) << 2)
st32(EXT_IMASK, R4030_EXT_IP3)
row("jz ip maskon", ip3(), IP3)
st8(COM0 + IER, 0x00); st8(COM1 + IER, 0x00)
row("jz ip none", ip3(), 0)
row("jz vec none", ld32(VEC), 0)
row("jz ip nt", ip3(), 0)

emu.close()
print("JAZZVEC_RESULT=%d/%d" % (sum(1 for r in rows if r), len(rows)), flush=True)
print("JAZZVEC_DRIVER=%s" % ("bad" if emu.bad else "ok"), flush=True)
print("JAZZVEC_DONE", flush=True)
