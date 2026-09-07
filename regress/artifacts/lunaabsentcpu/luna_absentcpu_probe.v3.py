#!/usr/bin/env python3
"""lunaabsentcpu (#503) -- rung-3 WITNESS and DETECTOR for dev_luna88k.c reassert_interrupts().

THE DEFECT.  reassert_interrupts() walked all MAX_CPUS (4) slots and called INTERRUPT_ASSERT(d->cpu_irq[cpu]) --
a direct call through the struct's function pointer -- while DEVINIT connected cpu_irq[1..3] only under
`ncpus >= 2/3/4' and memset()s the device to zero.  The INT_ST_MASK0-3 and SOFT_INT0-3 store arms take their slot
from the ADDRESS (`cpunr = (addr - INT_ST_MASK0) / 4') with no ncpus bound, so on the default ONE-cpu luna-88k a
guest word store of 0xfc000000 to INT_ST_MASK1 (0x65000004) arms slot 1, and a following store of 1 to SOFT_INT1
(0x69000004) sets that slot's pending bit and calls reassert SYNCHRONOUSLY inside the store: a NULL function
pointer is called and the emulator process dies with SIGSEGV (MEASURED 2026-09-05: signal 11, no diagnostic).
Any device line whose bit the armed slot's mask enables kills the same way on a running guest -- the clock is line
6 (bit 31); the SIO TX-interrupt route (line 5, bit 30) is SYNCHRONOUS and guest-drivable while stepping (session A2).

THE FIX (#503, option (a) of the pass-1 set): `d->ncpus' captured at DEVINIT and the walk bounded `cpu < d->ncpus'.
The absent slots' registers stay guest-writable storage with readback (a MODEL question filed as lunaabsentmaskdecl).

ONE cold-debugger session per SESSION below, real m88k guest instructions (st/ld through real address decode and
real memory_rw), COMMITTED UNMODIFIED machine description (`-e luna-88k' + the committed rig image; `-n 2' for the
two-cpu accept rows is a command-line configuration of the same description, not a machine edit).  EVERY PLANTED
WORD IS DISASSEMBLED AND ITS TEXT CHECKED BEFORE IT IS STEPPED.

  session A  (1 cpu, stepped)          row          CHANNEL: the mutant it kills / the observable that differs
    C1  RAM word through the same decode            live         identity (floor c): 0x12345678 back
    C2  MASK0 <- 0xfc000000; ld = 0x00fc0000        devsig       RAM-vs-device: the handler's own >>8
    A1  SOFT_INT0 <- 1 on the CONNECTED slot 0      slot0        attribution: the same two stores survive; readback 1
    A2  MASK1 <- 0xfc000000 ALONE; ld = 0x00fc0000  mask1        option-(b)-shaped edits (a declined store reads 0)
    W1  SOFT_INT1 <- 1: THE WITNESS                 soft1        M_REVERT/M_OFFBY1/M_NULLA/M_LATCH/M_GUARDASSERT: host alive.
                                                                 TWO channels in one row -- the STORE exercises ASSERT, the
                                                                 READBACK (== 1; read clears the pending bit -> the next
                                                                 reassert takes the DEASSERT arm) exercises DEASSERT.
                                                                 Three mutants die on the readback, not the store.
    S1  SIO cmd <- 0x01 then 0x02 (WR1 TX_IE): a    sio5         M_CALLGUARD (bound the reassert CALL in the store arms,
        device line (5, bit 30) asserts and walks                loop untouched: W1 survives, this one still walks slot 1).
        the loop with slot 1 armed; ld MASK1 =                   The measured form of "the next enabled device line kills".
        0xa0fc0000 (level 5 in 31..29, mask in 23..16)
    S2  SIO cmd <- 0x28 (RESET_TX_IP), then WR1 <- 0 sio5clr     the DEASSERT walk with a line pending on slot 1 (an
        ld MASK1 = 0x00fc0000                                    ASSERT-only NULL guard dies here); level back to 0
    M2  MASK2 <- 0x84000100; ld = 0x00840001 (23..0) mask2       es438cells: the third label stores and reads back
    M3  MASK3 <- 0x84000100; ld = 0x00840001         mask3       es438cells: the fourth label
    C3  RAM again                                   live2        the machine still executes after everything above
  session A2 (1 cpu, stepped)  MASK1 armed then S1 FIRST: the SIO route's own pre-fix death, ordered before any SOFT store
    sio-first                                        siofirst     PRE-FIX: HALT at the TX_IE store (line 5 walks slot 1)
  session B  (1 cpu, FREE-RUNNING)  MASK0 <- 0x04000000 (bit 26 ONLY: no device line can raise it), SOFT_INT0 <- 1,
        VBR <- 0x40000 (RAM), PSR <- 0x80000000 (IND CLEAR), `br .' planted at VBR+8, breakpoint there, `continue'
    cpu0 setup / slot0 deliver / slot0 shadow        M_NOASSIGN (ncpus never assigned -> 0: the loop never runs, slot 0
                                                     is never asserted, every SURVIVAL row is green) and M_NOREASSERT2:
                                                     cpu 0 enters its INTERRUPT vector (pc == 0x40008), PSR 0x8000000b,
                                                     EPSR 0x80000000.  Stepping cannot deliver (`if (!single_step)').
  session C  (`-n 2', FREE-RUNNING)  cpu 1: VBR 0x40000, PSR 0x80000000, parked at `br .'; cpu 0 steps MASK1 <-
        0x04000000 and SOFT_INT1 <- 1, parks; breakpoint VBR+8; `continue'
    two cpus / cpu1 setup / mask1 land / survive /   M_HARD1 (`d->ncpus = 1' hardcoded -- the clause-(d) null repair:
    cpu1 deliver / cpu1 shadow / cpu0 parked         a TOTAL ESCAPE of every 1-cpu row; measured 19/20, cpu1 deliver alone red): cpu 1 enters
                                                     its vector (pc == 0x40008), IND set, cpu 0 still parked.
  session D  (`-n 2', control)  the same without the SOFT_INT1 store: NO vector entry within the wait
    nodeliver ctl                                    makes the delivery rows attributable
  session B2 (1 cpu, FREE-RUNNING)  MASK0 <- 0x40000000 (bit 30 = SIO line 5), WR1 TX_IE, `continue'
    sio5 deliver                                     M_MASK30 (the walk ignores line 5) and M_SWONLY (walk only slots with a
                                                     software interrupt pending): a DEVICE line must deliver to a CONNECTED
                                                     slot -- cpu 0 enters VBR+8.  v2 had no such row (deepseek, grok, pass 2)
  session C2 (`-n 2', FREE-RUNNING)  MASK0+MASK1 bit 26, SOFT_INT0+SOFT_INT1: BOTH slots pending at once
    both deliver                                     M_IRQACTIVE0 (the per-slot latch collapsed onto slot 0 drops cpu 1's IPI
                                                     when slot 0 is pending too): both cpus reach VBR+8, in either order
                                                     (the first arrival is parked off the vector, then `continue' again) (kimi)
  session E  (`-n 4', FREE-RUNNING)  cpus 1..3 parked with VBR/PSR set; MASK3 + SOFT_INT3 from cpu 0
    four cpus / cpu3 deliver / others idle           M_AND1 (`cpu_irq[cpu & 1]': slots 2/3 alias onto 0/1) and M_MIN2 (the
                                                     bound clamped to two): the LAST slot delivers to cpu 3 and to nobody
                                                     else -- v2 never ran more than two cpus (glm, grok, pass 2)

RESULT words per row: OK / HALT (the host died: signal / exit) / BADREGS (a value assert failed) / STOP (no vector entry
before the wait ran out) / NOSTART.  Output: `LUNAABS_ROW=<name> RESULT=<word> ...' per row, `LUNAABS_RESULT=<ok>/<rows>',
`LUNA_ABSENTCPU_WITNESS=PASS|PRE_FIX_SYMPTOM|FAIL ...', `LUNAABS_DONE'.  Exit status is non-zero on any row that is not OK
(a gate can rely on it).  On HEAD the witness reads PRE_FIX_SYMPTOM at row soft1 (session A) and at siofirst (session A2).

CONTRACT (clause e): catches the walk bound reverted or off by one, an ASSERT-only NULL guard, a decline-once latch on
either arm, a guard moved inside the branch, the reassert CALL bounded in the store arms instead of the walk (sio5), the
bound never assigned (session B), the bound hardcoded to 1 (session C) or clamped to 2 (session E), slots 2/3 aliased onto 0/1
(session E), a device line masked out of the walk or a walk of software-pending slots only (session B2), the per-slot latch
collapsed onto slot 0 (session C2), a declined store to an absent slot (mask1/mask2/mask3 readbacks), and the third/fourth MASK
labels.  Does NOT catch: a both-sided NULL guard instead of the bound
(EQUIVALENT on every reachable configuration -- measured 22/22 in killtable/; the choice is warrant-based), a deleted reassert
in the SOFT arm alone (the clock's own reassert carries the delivery; disclosed debt), a connected slot's DEASSERT (no row observes a
post-clear deassert free-running: handlers are `br .' with IND set and never rte -- kimi, grok), the `irqActive[cpu] = 0' clear
itself (same reason), the clock/timer route (host-timer
driven, not steppable -- same loop as sio5), MASK1..3 written by a real guest kernel (no luna88k source on disk).

Encodings (cpu_m88k.c, the same source as regress/luna_intmask_probe.py):  ld rD,rS1,IMM16 op26=0x05 ; st rD,rS1,IMM16
op26=0x09 ; br . = c0000000.
usage: luna_absentcpu_probe.py <gxemul-binary> <images-dir>
"""
import os, pty, re, select, sys, time

BIN     = sys.argv[1]
IMAGES  = sys.argv[2]
IMG     = IMAGES + "/liveimage-luna88k-raw-20250518.img"
CODE    = 0x00010000
SCRATCH = 0x00020000
PARK    = 0x00030000        # `br .' for a parked cpu
VBR     = 0x00040000        # a vector table in RAM: `br .' at VBR+8 (INTERRUPT)
MASK0   = 0x65000000        # INT_ST_MASK0 -- the LITERAL, deliberately not the #define
SOFT0   = 0x69000000        # SOFT_INT0
SIOCMD0 = 0x51000004        # OBIO_SIO + 4: SCC command register, channel 0
SELF    = 0xc0000000        # br .


def enc(is_store, d, s1, imm16):
    return ((0x09 if is_store else 0x05) << 26) | (d << 21) | (s1 << 16) | imm16


SLOTS = [(CODE + 0x00, enc(True,  4, 5, 0), "st\tr4,r5,0x0"),
         (CODE + 0x04, enc(False, 4, 5, 0), "ld\tr4,r5,0x0"),
         (CODE + 0x08, enc(True,  4, 6, 0), "st\tr4,r6,0x0"),
         (CODE + 0x0c, enc(False, 4, 6, 0), "ld\tr4,r6,0x0")]
A_WDEV, A_RDEV, A_WRAM, A_RRAM = [s[0] for s in SLOTS]

rows = []
fails = []
t0 = time.time()


def row(name, result, note=""):
    rows.append((name, result))
    if result != "OK":
        fails.append(name)
    print("LUNAABS_ROW=%-14s RESULT=%-8s %s" % (name, result, note), flush=True)


class Sess:
    def __init__(self, ncpus=1):
        self.buf = ""
        self.dead = False
        self.status = None
        argv = [BIN, "-V"] + (["-n", str(ncpus)] if ncpus > 1 else []) + ["-e", "luna-88k", "-d", "R:" + IMG, "boot"]
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.chdir(IMAGES)
            os.execvp(BIN, argv)
            os._exit(127)

    def rd(self, t=0.4):
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

    def wait(self, mark=0, echo=None, timeout=60):
        t = time.time()
        while time.time() - t < timeout:
            if not self.rd():
                return False
            resp = self.buf[mark:]
            if echo is not None and echo not in resp:
                continue
            if len(self.buf) > mark and resp.rstrip().endswith("GXemul>"):
                return True
        return False

    def send(self, x, timeout=60):
        b = (x + "\n").encode("latin1")
        mark = len(self.buf)
        n = 0
        try:
            while n < len(b):
                n += os.write(self.fd, b[n:])
        except OSError:
            self.dead = True
            return False
        return self.wait(mark=mark, echo=x if x else None, timeout=timeout)

    def reg(self, name, cpu=None, cr=False):
        """Read GPR/pc (`reg [cpu]') or a control register (`reg [cpu],c')."""
        mark = len(self.buf)
        cmd = "reg"
        if cpu is not None:
            cmd += " %d" % cpu
        if cr:
            cmd += ",c"
        if not self.send(cmd, timeout=30):
            return None
        m = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)" % re.escape(name), self.buf[mark:])
        return int(m.group(1), 16) if m else None

    def step_at(self, addr):
        if self.dead:
            return False
        if not self.send("pc=0x%08x" % addr):
            return False
        ok = self.send("step 1", timeout=30)
        return ok and not self.dead

    def host_status(self):
        try:
            _, st = os.waitpid(self.pid, os.WNOHANG)
            if os.WIFSIGNALED(st):
                return "signal %d" % os.WTERMSIG(st)
            if os.WIFEXITED(st):
                return "exit %d" % os.WEXITSTATUS(st)
        except Exception as e:
            return "unknown (%s)" % e
        return "still running?"

    def plant(self, words):
        for addr, word in words:
            self.send("put w 0x%08x, 0x%08x" % (addr, word))

    def check_dis(self):
        """Disassemble every planted program slot and compare with the emulator's own spelling."""
        ok = True
        for addr, word, want in SLOTS:
            mark = len(self.buf)
            self.send("unassemble 0x%08x" % addr)
            m = re.search(r"((?:ld|st)[\w.]*\s+r\d+,r\d+,0x[0-9a-f]+)", self.buf[mark:])
            got = m.group(1) if m else "(none)"
            good = re.sub(r"\s+", " ", got) == re.sub(r"\s+", " ", want)
            print("  0x%08x word=0x%08x dis=%-20r %s" % (addr, word, got, "OK" if good else "*** WRONG ENCODING ***"))
            ok = ok and good
        return ok

    def cont_until_breakpoint(self, timeout):
        """`continue' and wait for the BREAKPOINT line; returns True on a hit, False on timeout (after ^C)."""
        mark = len(self.buf)
        try:
            os.write(self.fd, b"continue\n")
        except OSError:
            self.dead = True
            return False
        t = time.time()
        while time.time() - t < timeout:
            if not self.rd(0.3):
                return False
            if "BREAKPOINT" in self.buf[mark:]:
                self.wait(mark=len(self.buf) - 1, timeout=15)
                return True
        try:
            os.write(self.fd, b"\x03")
        except OSError:
            self.dead = True
            return False
        self.wait(mark=len(self.buf), timeout=15)
        return False

    def close(self):
        try:
            os.write(self.fd, b"quit\n")
            time.sleep(0.3)
            os.kill(self.pid, 9)
            os.waitpid(self.pid, 0)
        except Exception:
            pass


def boot(ncpus=1):
    s = Sess(ncpus)
    if not s.wait(timeout=180):
        print("NO-PROMPT")
        return None
    s.plant([(a, w) for a, w, _ in SLOTS] + [(PARK, SELF), (VBR + 8, SELF)])
    if not s.check_dis():
        s.close()
        return None
    s.send("r6=0x%08x" % SCRATCH)
    return s


def value(s, label, got, want, mask=0xffffffff):
    ok = got is not None and (got & mask) == want
    print("  %-62s got=%s want=0x%08x %s" % (label, ("0x%08x" % got) if got is not None else "DEAD/NONE", want,
                                            "OK" if ok else "*** MISMATCH ***"))
    return ok


def store(s, addr, val):
    """Word store of VAL to ADDR through the planted `st r4,r5,0'; False if the host died."""
    s.send("r5=0x%08x" % addr)
    s.send("r4=0x%08x" % val)
    return s.step_at(A_WDEV)


def load(s, addr):
    s.send("r5=0x%08x" % addr)
    s.send("r4=0x00000000")
    if not s.step_at(A_RDEV):
        return None
    return s.reg("r4")


def died(s, name, note):
    st = s.host_status()
    m = re.findall(r"\[[^\r\n]*luna88k[^\r\n]*\]", s.buf)
    row(name, "HALT", "HOST DIED (%s); last device line: %s -- %s" % (st, m[-1] if m else "(none)", note))


# ------------------------------------------------------------------------------------------------- session A
def session_A():
    print("=== SESSION A (1 cpu, stepped): the witness rows, then the SIO line-5 route, then MASK2/MASK3")
    s = boot(1)
    if s is None:
        row("live", "NOSTART", "no prompt / bad encoding"); return
    s.send("r4=0x12345678"); s.step_at(A_WRAM); s.send("r4=0x00000000"); s.step_at(A_RRAM)
    row("live", "OK" if value(s, "C1 RAM readback", s.reg("r4"), 0x12345678) else "BADREGS")
    if not store(s, MASK0, 0xfc000000):
        died(s, "devsig", "died on a LEGAL MASK0 store -- the probe itself is broken"); s.close(); return
    g = load(s, MASK0)
    if g is None:
        died(s, "devsig", "died on a LEGAL MASK0 read"); s.close(); return
    row("devsig", "OK" if value(s, "C2 read INT_ST_MASK0 after write 0xfc000000", g, 0x00fc0000, 0x00ffffff) else "BADREGS")
    # A1: the CONNECTED slot 0 -- assert AND deassert (the readback clears the pending bit)
    if not store(s, SOFT0, 1):
        died(s, "slot0", "host died asserting the CONNECTED cpu 0 -- attribution control FAILED"); s.close(); return
    g = load(s, SOFT0)
    if g is None:
        died(s, "slot0", "host died on the SOFT_INT0 readback (the DEASSERT walk on the connected slot)"); s.close(); return
    row("slot0", "OK" if value(s, "A1 SOFT_INT0 readback (the stored 1; the read clears it)", g, 1) else "BADREGS")
    # A2: arm the ABSENT slot 1; nothing pending yet
    if not store(s, MASK0 + 4, 0xfc000000):
        died(s, "mask1", "host died on the MASK1 store alone -- a machine-wide line was already pending"); s.close(); return
    g = load(s, MASK0 + 4)
    if g is None:
        died(s, "mask1", "host died on the MASK1 readback"); s.close(); return
    row("mask1", "OK" if value(s, "A2 MASK1 readback (stored as-is: 0x00fc0000; a DECLINED store reads 0)", g, 0x00fc0000, 0x00ffffff) else "BADREGS")
    # W1: THE WITNESS -- store, then the readback (the DEASSERT walk)
    if not store(s, SOFT0 + 4, 1):
        died(s, "soft1", "W1: SOFT_INT1 store -> reassert -> INTERRUPT_ASSERT(cpu_irq[1]) through NULL on a one-cpu machine")
        print("SYMPTOM=NULL_CALLBACK_ON_ABSENT_CPU"); print("  the PRE-FIX symptom, on a committed unmodified one-cpu luna-88k, reached by two ordinary word stores.")
        s.close(); return
    g = load(s, SOFT0 + 4)
    if g is None:
        died(s, "soft1", "W1 readback: the DEASSERT walk (read clears the pending bit) reached NULL -- an ASSERT-only guard"); s.close(); return
    row("soft1", "OK" if value(s, "W1 SOFT_INT1 store survived; readback (the stored 1, read clears it)", g, 1) else "BADREGS")
    # S1: the SIO line-5 route -- a DEVICE line asserts with slot 1 armed (mask bit 30) and walks the loop
    if not store(s, SIOCMD0, 0x01):
        died(s, "sio5", "died selecting WR1 (the deassert walk with nothing pending)"); s.close(); return
    if not store(s, SIOCMD0, 0x02):
        died(s, "sio5", "S1: WR1 TX_IE -> sio_tx_pending -> line 5 asserts -> reassert walks slot 1 (mask bit 30) -> NULL"); s.close(); return
    g = load(s, MASK0 + 4)
    if g is None:
        died(s, "sio5", "died on the MASK1 readback after the line-5 assert"); s.close(); return
    row("sio5", "OK" if value(s, "S1 MASK1 readback: level 5 in 31..29 (line 5 pending) + mask in 23..16", g, 0xa0fc0000) else "BADREGS")
    # S2: disarm -- RESET_TX_IP (the deassert walk with a line pending), then WR1 <- 0
    if not store(s, SIOCMD0, 0x28):
        died(s, "sio5clr", "S2: RESET_TX_IP -> line 5 deasserts -> the DEASSERT walk reached NULL"); s.close(); return
    store(s, SIOCMD0, 0x01); store(s, SIOCMD0, 0x00)
    g = load(s, MASK0 + 4)
    if g is None:
        died(s, "sio5clr", "died on the MASK1 readback after the disarm"); s.close(); return
    row("sio5clr", "OK" if value(s, "S2 MASK1 readback: level back to 0, mask still 0x00fc0000", g, 0x00fc0000) else "BADREGS")
    # M2/M3: the third and fourth labels (es438cells)
    for k, nm in ((2, "mask2"), (3, "mask3")):
        if not store(s, MASK0 + 4 * k, 0x84000100):
            died(s, nm, "died on the MASK%d store" % k); s.close(); return
        g = load(s, MASK0 + 4 * k)
        if g is None:
            died(s, nm, "died on the MASK%d readback" % k); s.close(); return
        row(nm, "OK" if value(s, "M%d MASK%d readback as-is (0x00840001 in 23..0)" % (k, k), g, 0x00840001, 0x00ffffff) else "BADREGS")
    s.send("r4=0x0badf00d"); s.step_at(A_WRAM); s.send("r4=0x00000000"); s.step_at(A_RRAM)
    row("live2", "OK" if value(s, "C3 RAM readback", s.reg("r4"), 0x0badf00d) else "BADREGS")
    s.close()


# ------------------------------------------------------------------------------------------------- session A2
def session_A2():
    print("=== SESSION A2 (1 cpu, stepped): MASK1 armed, then the SIO line-5 route FIRST (no SOFT store)")
    s = boot(1)
    if s is None:
        row("siofirst", "NOSTART"); return
    if not store(s, MASK0 + 4, 0xfc000000):
        died(s, "siofirst", "died on the arming store"); s.close(); return
    store(s, SIOCMD0, 0x01)
    if not store(s, SIOCMD0, 0x02):
        died(s, "siofirst", "the TX_IE store: line 5 (bit 30) walked slot 1 with no SOFT store ever made -- the device-line route")
        print("SYMPTOM=NULL_CALLBACK_ON_ABSENT_CPU_VIA_DEVICE_LINE"); s.close(); return
    g = load(s, MASK0 + 4)
    row("siofirst", "OK" if value(s, "A2/S1 MASK1 readback (level 5 + mask)", g, 0xa0fc0000) else "BADREGS")
    store(s, SIOCMD0, 0x28); store(s, SIOCMD0, 0x01); store(s, SIOCMD0, 0x00)
    s.close()


# ------------------------------------------------------------------------------------------------- session B
def session_B():
    print("=== SESSION B (1 cpu, FREE-RUNNING): slot 0 delivery -- MASK0 bit 26 only, SOFT_INT0, VBR in RAM, IND clear")
    s = boot(1)
    if s is None:
        row("cpu0 setup", "NOSTART"); return
    if not store(s, MASK0, 0x04000000) or not store(s, SOFT0, 1):
        died(s, "cpu0 setup", "died arming/asserting the connected slot 0"); s.close(); return
    s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
    vbr = s.reg("VBR", cr=True); psr = s.reg("PSR", cr=True)
    ok = value(s, "B VBR set", vbr, VBR) and value(s, "B PSR: MODE only, IND CLEAR", psr, 0x80000000)
    row("cpu0 setup", "OK" if ok else "BADREGS", "VBR=%s PSR=%s" % (("0x%08x" % vbr) if vbr is not None else "?", ("0x%08x" % psr) if psr is not None else "?"))
    s.send("breakpoint add 0x%08x" % (VBR + 8))
    hit = s.cont_until_breakpoint(15.0)
    if s.dead:
        died(s, "slot0 deliver", "host died while free-running"); s.close(); return
    pc = s.reg("pc")
    if not hit:
        row("slot0 deliver", "STOP", "no vector entry within 15 s (pc=%s) -- the pending IPI was never delivered" % (("0x%08x" % pc) if pc is not None else "?"))
        s.close(); return
    row("slot0 deliver", "OK" if value(s, "B cpu0 pc == VBR+8 (INTERRUPT vector)", pc, VBR + 8) else "BADREGS")
    psr = s.reg("PSR", cr=True); epsr = s.reg("EPSR", cr=True)
    ok = value(s, "B PSR after entry: MODE|SFD1|IND|SFRZ", psr, 0x8000000b) and value(s, "B EPSR: the pre-exception PSR", epsr, 0x80000000)
    row("slot0 shadow", "OK" if ok else "BADREGS")
    s.close()


# ------------------------------------------------------------------------------------------------- session B2
def session_B2():
    print("=== SESSION B2 (1 cpu, FREE-RUNNING): slot 0 delivery through a DEVICE line -- MASK0 bit 30 (SIO line 5), WR1 TX_IE")
    s = boot(1)
    if s is None:
        row("sio5 deliver", "NOSTART"); return
    s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
    if not store(s, MASK0, 0x40000000):
        died(s, "sio5 deliver", "died arming slot 0 for line 5"); s.close(); return
    # arm the SIO transmitter interrupt: WR1 select, then TX_IE -- sio_tx_pending raises line 5 (bit 30) machine-wide
    if not store(s, SIOCMD0, 0x01) or not store(s, SIOCMD0, 0x02):
        died(s, "sio5 deliver", "died on the WR1 TX_IE store with slot 0 armed"); s.close(); return
    s.send("pc=0x%08x" % PARK)
    s.send("breakpoint add 0x%08x" % (VBR + 8))
    hit = s.cont_until_breakpoint(15.0)
    if s.dead:
        died(s, "sio5 deliver", "host died while free-running with line 5 pending on slot 0"); s.close(); return
    pc = s.reg("pc")
    if not hit:
        row("sio5 deliver", "STOP", "no vector entry within 15 s (pc=%s) -- the device line was never delivered to slot 0" % (("0x%08x" % pc) if pc is not None else "?"))
        s.close(); return
    row("sio5 deliver", "OK" if value(s, "B2 cpu0 pc == VBR+8 via SIO line 5 (a device line, not SOFT_INT)", pc, VBR + 8) else "BADREGS")
    s.close()


# ------------------------------------------------------------------------------------------------- session C2 (-n 2, both pending)
def session_C2():
    print("=== SESSION C2 (-n 2, FREE-RUNNING): BOTH slots pending -- MASK0+MASK1 bit 26, SOFT_INT0+SOFT_INT1; both cpus must enter")
    s = boot(2)
    if s is None:
        row("both deliver", "NOSTART"); return
    s.send("focus 1"); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
    s.send("focus 0"); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000")
    s.send("r6=0x%08x" % SCRATCH)
    for a, v, what in ((MASK0, 0x04000000, "MASK0"), (MASK0 + 4, 0x04000000, "MASK1"), (SOFT0, 1, "SOFT_INT0"), (SOFT0 + 4, 1, "SOFT_INT1")):
        if not store(s, a, v):
            died(s, "both deliver", "died on the %s store on 2 cpus" % what); s.close(); return
    s.send("pc=0x%08x" % PARK)
    s.send("breakpoint add 0x%08x" % (VBR + 8))
    entered = set()
    for attempt in (1, 2):
        hit = s.cont_until_breakpoint(15.0)
        if s.dead:
            died(s, "both deliver", "host died while free-running with both slots pending"); s.close(); return
        pcs = {c: s.reg("pc", cpu=c) for c in (0, 1)}
        for c in (0, 1):
            if pcs[c] == VBR + 8 and c not in entered:
                entered.add(c)
                # move the arrived cpu off the vector (its IND is set now, so it will not re-enter) and let the other one run
                s.send("focus %d" % c); s.send("pc=0x%08x" % PARK); s.send("focus 0")
        if len(entered) == 2 or not hit:
            break
    if len(entered) == 2:
        row("both deliver", "OK", "cpu 0 and cpu 1 both entered VBR+8 with both IPIs pending (the per-slot latch is per slot)")
    else:
        row("both deliver", "STOP", "only cpus %s entered the vector within the wait -- an IPI was dropped" % sorted(entered))
    s.close()


# ------------------------------------------------------------------------------------------------- session E (-n 4)
def session_E():
    print("=== SESSION E (-n 4, FREE-RUNNING): the LAST slot -- MASK3 + SOFT_INT3 deliver to cpu 3, cpus 0..2 stay out of the vector")
    s = boot(4)
    if s is None:
        row("four cpus", "NOSTART"); return
    mark = len(s.buf); s.send("machine")
    four = ("cpu3" in s.buf[mark:]) or ("cpu 3" in s.buf[mark:])
    row("four cpus", "OK" if four else "BADREGS", "the `machine' listing names cpu3" if four else "no cpu3 in the machine listing")
    for c in (1, 2, 3):
        s.send("focus %d" % c); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
    s.send("focus 0")
    s.send("r6=0x%08x" % SCRATCH)
    if not store(s, MASK0 + 12, 0x04000000):
        died(s, "cpu3 deliver", "died on the MASK3 store on 4 cpus"); s.close(); return
    if not store(s, SOFT0 + 12, 1):
        died(s, "cpu3 deliver", "died on the SOFT_INT3 store on 4 cpus (slot 3 IS connected here)"); s.close(); return
    s.send("pc=0x%08x" % PARK)
    s.send("breakpoint add 0x%08x" % (VBR + 8))
    hit = s.cont_until_breakpoint(15.0)
    if s.dead:
        died(s, "cpu3 deliver", "host died while free-running on 4 cpus"); s.close(); return
    pcs = [s.reg("pc", cpu=c) for c in (0, 1, 2, 3)]
    if not hit:
        row("cpu3 deliver", "STOP", "no vector entry within 15 s (cpu3 pc=%s)" % (("0x%08x" % pcs[3]) if pcs[3] is not None else "?"))
        s.close(); return
    row("cpu3 deliver", "OK" if value(s, "E cpu3 pc == VBR+8 (INTERRUPT vector on the LAST slot)", pcs[3], VBR + 8) else "BADREGS")
    idle = all(pcs[c] != VBR + 8 for c in (0, 1, 2))
    row("others idle", "OK" if idle else "BADREGS", "cpus 0..2 did not enter the vector" if idle else "another cpu took slot 3's interrupt: pcs=%s" % pcs)
    s.close()


# ------------------------------------------------------------------------------------------------- sessions C / D
def session_n2(deliver):
    name = "C" if deliver else "D"
    print("=== SESSION %s (-n 2, FREE-RUNNING): %s" % (name, "cpu 1 delivery via MASK1 + SOFT_INT1" if deliver else "CONTROL: MASK1 armed, no SOFT store"))
    s = boot(2)
    if s is None:
        row("two cpus" if deliver else "nodeliver ctl", "NOSTART"); return
    mark = len(s.buf); s.send("machine")
    two = ("cpu1" in s.buf[mark:]) or ("cpu 1" in s.buf[mark:])
    if deliver:
        row("two cpus", "OK" if two else "BADREGS", "the `machine' listing names cpu1" if two else "no cpu1 in the machine listing")
    # cpu 1: vector table, IND clear, parked
    s.send("focus 1"); s.send("VBR=0x%08x" % VBR); s.send("PSR=0x80000000"); s.send("pc=0x%08x" % PARK)
    vbr = s.reg("VBR", cpu=1, cr=True); psr = s.reg("PSR", cpu=1, cr=True); pc1 = s.reg("pc", cpu=1)
    s.send("focus 0")
    if deliver:
        ok = value(s, "C cpu1 VBR", vbr, VBR) and value(s, "C cpu1 PSR: IND clear", psr, 0x80000000) and value(s, "C cpu1 parked", pc1, PARK)
        row("cpu1 setup", "OK" if ok else "BADREGS")
    s.send("r6=0x%08x" % SCRATCH)
    if not store(s, MASK0 + 4, 0x04000000):
        died(s, "mask1 land" if deliver else "nodeliver ctl", "died on the MASK1 store on 2 cpus"); s.close(); return
    g = load(s, MASK0 + 4)
    if deliver:
        row("mask1 land", "OK" if value(s, "C MASK1 readback on 2 cpus (0x04000000 >> 8)", g, 0x00040000, 0x00ffffff) else "BADREGS")
        if not store(s, SOFT0 + 4, 1):
            died(s, "survive", "died on the SOFT_INT1 store on 2 cpus (slot 1 IS connected here)"); s.close(); return
        row("survive", "OK", "the two stores do not kill the host on 2 cpus")
    s.send("pc=0x%08x" % PARK)                     # park cpu 0 too
    s.send("breakpoint add 0x%08x" % (VBR + 8))
    hit = s.cont_until_breakpoint(15.0 if deliver else 8.0)
    if s.dead:
        died(s, "cpu1 deliver" if deliver else "nodeliver ctl", "host died while free-running on 2 cpus"); s.close(); return
    pc1 = s.reg("pc", cpu=1); pc0 = s.reg("pc", cpu=0)
    if deliver:
        if not hit:
            row("cpu1 deliver", "STOP", "no vector entry within 15 s (cpu1 pc=%s)" % (("0x%08x" % pc1) if pc1 is not None else "?"))
            s.close(); return
        row("cpu1 deliver", "OK" if value(s, "C cpu1 pc == VBR+8 (INTERRUPT vector on cpu 1)", pc1, VBR + 8) else "BADREGS")
        psr = s.reg("PSR", cpu=1, cr=True); epsr = s.reg("EPSR", cpu=1, cr=True)
        ok = value(s, "C cpu1 PSR after entry", psr, 0x8000000b) and value(s, "C cpu1 EPSR: the pre-exception PSR", epsr, 0x80000000)
        row("cpu1 shadow", "OK" if ok else "BADREGS")
        row("cpu0 parked", "OK" if value(s, "C cpu0 still parked (it was cpu 1 that took the vector)", pc0, PARK) else "BADREGS")
    else:
        row("nodeliver ctl", "OK" if not hit else "BADREGS", "with nothing pending cpu 1 does NOT enter its vector in 8 s" if not hit else "cpu 1 entered its vector with NOTHING pending")
    s.close()


def main():
    print("BINARY=%s" % BIN)
    session_A()
    prefix = any(r == "HALT" for _, r in rows)
    session_A2()
    session_B()
    session_B2()
    session_n2(True)
    session_C2()
    session_n2(False)
    session_E()
    ok = sum(1 for _, r in rows if r == "OK")
    print("LUNAABS_RESULT=%d/%d" % (ok, len(rows)))
    halt_rows = [n for n, r in rows if r == "HALT"]
    if halt_rows:
        print("LUNA_ABSENTCPU_WITNESS=PRE_FIX_SYMPTOM (%s)" % ",".join(halt_rows))
    elif fails:
        print("LUNA_ABSENTCPU_WITNESS=FAIL %s" % ",".join(fails))
    else:
        print("LUNA_ABSENTCPU_WITNESS=PASS")
    print("PROBE_WALL=%.1fs" % (time.time() - t0))
    print("LUNAABS_DONE", flush=True)
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
