#!/usr/bin/env python3
"""fbpending DRAIN PROBE -- a RUNG-3 detector that MEASURES the pending-interrupt
backlog of footbridge timer 1 in ~10 s, instead of waiting 43 s for it to overflow.

WHY THIS EXISTS.  The rung-3 witness (fbpending_witness.py) proves the defect by
running until the counter wraps, which takes 42.95 s at cats' emulated_hz and cannot
be made faster than 31.51 s on ANY machine (the delivery ceiling is
TIMER_MAX_CATCHUP x TIMER_BASE_FREQUENCY = 68,157,440 increments per wall second, and
timer_tick0 is called from nowhere else).  A gate row cannot spend that.

THE TRICK: MEASURE THE COUNTER, DO NOT WAIT FOR IT TO OVERFLOW.

  1. The guest arms timer 1 at a KNOWN SLOW rate.  cats' emulated_hz is 50,000,000 and
     reload_timer_value() asks for emulated_hz / effective_cycles(load, ctrl, 1).  With
     TIMER_FCLK_256 and load 256 that is 50e6 / (256*256) = 762.94 Hz.
  2. It free-runs for T seconds.  Nothing acks, so the backlog is rate*T -- UNLESS the
     device bounds it.
  3. It then FREEZES the timer by writing TIMER_1_LOAD = 0x00FFFFFF while keeping
     TIMER_FCLK_256: the rate falls to 50e6/(0xFFFFFF*256) = 0.0116 Hz, one tick per
     86 s.  *** A LOAD WRITE DOES NOT CLEAR pending_timer_interrupts *** (only a
     TIMER_x_CONTROL write WITHOUT TIMER_ENABLE does, dev_footbridge.c:583), so the
     backlog survives the freeze.  That turns a moving quantity into a static one.
  4. It then DRAINS AND COUNTS.  DEVICE_TICK writes timer_value = random() %
     effective_cycles(load, ctrl, 0) whenever the backlog is > 0, and with load
     0x00FFFFFF that modulus is 0xFFFFFF, so the produced value is in [0, 0xFFFFFE].
     The guest writes the sentinel 0x00FFFFFF -- which the modulo CANNOT produce and
     which survives TIMER_x_VALUE's own `idata & TIMER_MAX_VAL` mask -- and spins.  A
     changed read means one tick was delivered; the guest then writes TIMER_1_CLEAR
     (one decrement) and repeats.  When the spin budget expires with the sentinel
     intact, the backlog is 0 and the number of decrements IS the backlog.

  The measured number is the whole verdict: pre-fix it is rate*T; post-fix it is the
  cap.  No wrap, no 43 s, and the row reports a NUMBER rather than a boolean, so a cap
  that is too high or too low is visible rather than merely "not the bug".

ARM X -- THE PLACEMENT DISCRIMINATOR, and the reason it is not merely a second run.
  dev_footbridge.c never calls timer_remove() and never lowers the core frequency when
  the guest DISABLES a timer: TIMER_x_CONTROL without TIMER_ENABLE zeroes the counter
  once (:583) and leaves the struct timer running.  So timer_tickN keeps incrementing a
  counter that DEVICE_TICK will never look at.  Arm X arms the timer, immediately
  disables it, free-runs, re-enables (which does NOT clear the counter) and then
  measures.  A non-zero result proves the counter accrues while the device is disabled
  -- which is exactly the state in which a bound placed in DEVICE_TICK cannot run.

ARMS
  D  enabled throughout.  Backlog after T seconds.
  X  disabled during the accrual.  Backlog after T seconds.  Q1's discriminator.
  T  negative control: MMU left on, so the footbridge is not mapped.  Must not return
     the device's answers.  (machine_cats.c's boot page tables map only the low 256 MB;
     the footbridge is at PA 0x42000000.)
  K  failability control: arm D's prologue plus ONE instruction, a read of
     IRQ_ENABLE_SET, which dev_footbridge.c answers with fatal() then exit(1).  A probe
     in which nothing can die proves nothing by surviving.

Every RAM output word is poisoned with 0xDEADBEEF first and every verdict row requires
the values it consults to be PRESENT.  Every planted instruction is checked, as it
EXECUTES, against the emulator's own disassembly (the hand-assembled-encoding trap).

usage: fbpending_drain.py <gxemul-binary> <four-byte-raw-stub>
                          [--accrue S] [--expect-cap N] [--learn]
"""
import os, pty, re, select, signal, struct, sys, time

BIN = sys.argv[1]
STUB = sys.argv[2]
LEARN = "--learn" in sys.argv


def _opt(name, default, cast):
    if name in sys.argv:
        return cast(sys.argv[sys.argv.index(name) + 1])
    return default


ACCRUE_S = _opt("--accrue", 4.0, float)
EXPECT_CAP = _opt("--expect-cap", -1, int)   # -1 = report only
#  WHICH of the four timers.  dev_footbridge.c derives timer_nr as
#  (relative_addr >> 5) & 3, so timer N's registers sit at 0x300 + N*0x20 and
#  TIMER_1_* is INDEX 0.  A fix applied to only one of the four callbacks passes a
#  row that exercises only timer 1, which is why this is a parameter and not a
#  constant.
TIMER_NR = _opt("--timer", 0, int)
TBASE = 0x300 + 0x20 * TIMER_NR
T_LOAD, T_VALUE, T_CTRL, T_CLEAR = TBASE, TBASE + 4, TBASE + 8, TBASE + 12

CODE = 0x00008000
DATA = 0x00009000
FB = 0x42000000

EMU_HZ = 50000000.0
#  --fast drives the counter at the machine's FULL emulated_hz (load 1, no
#  prescaler = 50 MHz on cats), which is the only setting that reaches the 2^31
#  wrap inside a run: 2^31 / 50e6 = 42.95 s.  The default 762.94 Hz would need
#  32 days.  The freeze/drain machinery below is independent of the accrual rate.
FAST = "--fast" in sys.argv
LOAD_RUN = 0x001 if FAST else 0x100   # with FCLK_256 -> 50e6/65536 = 762.94 Hz
LOAD_FREEZE = 0x00FFFFFF              # with FCLK_256 -> 0.0116 Hz
CTRL_ON = 0x80 if FAST else 0x88      # TIMER_ENABLE [| TIMER_FCLK_256]
CTRL_OFF = 0x00
SENTINEL = 0x00FFFFFF                 # random() % 0xFFFFFF can never produce it
SPIN = 0x00010000                     # 65536 iterations ~ 20 device-tick periods
LIMIT = 200000
RATE = EMU_HZ / (LOAD_RUN * (1.0 if FAST else 256.0))
ONLY = _opt("--only", "", str)        # run a single arm, e.g. --only X

VENDOR = 0x1011
LOADBACK = 0x00345678
POISON = 0xDEADBEEF

# ---- RAM map (offsets from DATA) -----------------------------------------
K_LIVE, K_SRC, K_L, K_FRZ, K_CON, K_SEN, K_SPIN, K_COFF = (
    0x00, 0x04, 0x08, 0x0c, 0x10, 0x14, 0x18, 0x1c)
O_DRAIN, O_ITER, O_LASTV, O_VEND, O_PHASE, K_LIM = (
    0x20, 0x24, 0x28, 0x2c, 0x30, 0x34)

CONSTS = {K_LIVE: 0x11223344, K_SRC: 0x12345678, K_L: LOAD_RUN,
          K_FRZ: LOAD_FREEZE, K_CON: CTRL_ON, K_SEN: SENTINEL,
          K_SPIN: SPIN, K_COFF: CTRL_OFF, K_LIM: LIMIT}
OUTS = (O_DRAIN, O_ITER, O_LASTV, O_VEND, O_PHASE)

R = dict(r0=0, r1=1, r2=2, r3=3, r4=4, r5=5, r6=6, r7=7, r8=8, r9=9,
         sl=10, fp=11, ip=12, sp=13, lr=14, pc=15)


# ---------------------------------------------------------------- assembler
#  Encodings are GENERATED, not typed.  Every generated word is still checked
#  against the emulator's own disassembly as it executes (arm E of the witness
#  found this class of error four times in this project).
def _imm12(v):
    for rot in range(16):
        c = ((v << (2 * rot)) | (v >> (32 - 2 * rot))) & 0xFFFFFFFF
        if c < 256:
            return (rot << 8) | c
    raise ValueError("0x%x is not an ARM immediate" % v)


def mov(rd, imm):
    return 0xE3A00000 | (R[rd] << 12) | _imm12(imm), "mov %s,#0x%x" % (rd, imm)


def movr(rd, rm):
    return 0xE1A00000 | (R[rd] << 12) | R[rm], "mov %s,%s" % (rd, rm)


def ldr(rd, rn, off):
    return 0xE5900000 | (R[rn] << 16) | (R[rd] << 12) | off, \
        "ldr %s,[%s,#%d]" % (rd, rn, off)


def st(rd, rn, off):
    return 0xE5800000 | (R[rn] << 16) | (R[rd] << 12) | off, \
        "str %s,[%s,#%d]" % (rd, rn, off)


def cmpr(rn, rm):
    return 0xE1500000 | (R[rn] << 16) | R[rm], "cmps %s,%s" % (rn, rm)


def subs1(rd):
    return 0xE2500001 | (R[rd] << 16) | (R[rd] << 12), "subs %s,%s,#1" % (rd, rd)


def add1(rd):
    return 0xE2800001 | (R[rd] << 16) | (R[rd] << 12), "add %s,%s,#1" % (rd, rd)


def br(cond, target, here):
    off = ((target - here - 8) >> 2) & 0xFFFFFF
    return (cond << 28) | 0x0A000000 | off, None


NOP = (0xE1A00000, "mov r0,r0")


def build(mmu_on=False, disable_during_accrual=False, kill=False):
    """Returns [(offset, word, expected_disassembly_or_None, comment)]."""
    p = []

    def emit(off, wt, comment=""):
        p.append((off, wt[0], wt[1], comment))

    if mmu_on:
        for o in (0x00, 0x04, 0x08):
            emit(o, NOP, "arm T: MMU LEFT ON -- the negative control")
    else:
        p.append((0x00, 0xEE110F10, "mrc 15,0,r0,cr1,cr0,0", "read CP15 c1"))
        p.append((0x04, 0xE3C00001, "bic r0,r0,#1", "clear MMU enable"))
        p.append((0x08, 0xEE010F10, "mcr 15,0,r0,cr1,cr0,0", "MMU OFF -> VA == PA"))
    p.append((0x0c, 0xEE113F10, "mrc 15,0,r3,cr1,cr0,0", "C2: CP15 c1 read BACK"))
    emit(0x10, mov("r0", FB), "footbridge base")
    emit(0x14, mov("r4", DATA), "scratch RAM")
    emit(0x18, ldr("r5", "r4", K_LIVE), "C1 liveness, expect 0x11223344")
    emit(0x1c, ldr("r6", "r0", 0), "A1 VENDOR_ID, expect 0x1011")
    emit(0x20, ldr("r2", "r4", K_SRC), "0x12345678 out of RAM")
    emit(0x24, st("r2", "r0", T_LOAD), "TIMER_x_LOAD <- 0x12345678")
    emit(0x28, ldr("r7", "r0", T_LOAD), "A2 expect 0x00345678 (the handler's mask)")
    emit(0x2c, ldr("r2", "r4", K_CON), "CTRL = TIMER_ENABLE|TIMER_FCLK_256")
    emit(0x30, st("r2", "r0", T_CTRL), "TIMER_1_CONTROL <- 0x88")
    emit(0x34, ldr("r2", "r4", K_L), "load 256")
    emit(0x38, st("r2", "r0", T_LOAD), "TIMER_1_LOAD <- 256 => 762.94 Hz")
    emit(0x3c, ldr("r8", "r4", K_SEN), "sentinel 0x00FFFFFF")
    emit(0x40, ldr("ip", "r4", K_SPIN), "spin budget")
    emit(0x44, mov("sl", 0), "drained count")
    emit(0x48, mov("lr", 0), "accrual iterations")
    emit(0x4c, mov("r1", 0), "")
    emit(0x50, st("r1", "r4", O_PHASE), "PHASE = 0")
    if disable_during_accrual:
        emit(0x54, ldr("r2", "r4", K_COFF), "arm X: CTRL = 0")
        emit(0x58, st("r2", "r0", T_CTRL),
             "arm X: DISABLE.  Zeroes the counter ONCE and leaves the core timer running.")
    else:
        emit(0x54, NOP, "")
        emit(0x58, NOP, "")
    if kill:
        p.append((0x5c, 0xE5907188, "ldr r7,[r0,#392]",
                  "arm K: IRQ_ENABLE_SET -> fatal()+exit(1)"))
        emit(0x60, NOP, "")
        return p
    #  accrual loop -- publishes liveness and a fresh VENDOR_ID every iteration
    emit(0x5c, add1("lr"), "ACCRUE: iterations++")
    emit(0x60, st("lr", "r4", O_ITER), "publish iterations")
    emit(0x64, ldr("r1", "r0", 0), "fresh VENDOR_ID read, every iteration")
    emit(0x68, st("r1", "r4", O_VEND), "publish it")
    p.append((0x6c, br(0xE, CODE + 0x5c, CODE + 0x6c)[0], None, "b ACCRUE"))
    #  ---- DRAIN entry.  The harness sets pc here after the accrual free-run. ----
    if disable_during_accrual:
        emit(0x70, ldr("r2", "r4", K_CON), "arm X: re-enable")
        emit(0x74, st("r2", "r0", T_CTRL),
             "arm X: CONTROL <- 0x88.  reload_timer_value() does NOT clear the counter.")
    else:
        emit(0x70, NOP, "")
        emit(0x74, NOP, "")
    emit(0x78, ldr("r2", "r4", K_FRZ), "0x00FFFFFF")
    emit(0x7c, st("r2", "r0", T_LOAD), "FREEZE: LOAD <- 0x00FFFFFF => 0.0116 Hz")
    emit(0x80, mov("r1", 1), "")
    emit(0x84, st("r1", "r4", O_PHASE), "PHASE = 1")
    emit(0x88, ldr("sp", "r4", K_LIM), "drain limit")
    emit(0x8c, st("r8", "r0", T_VALUE), "DLOOP: TIMER_1_VALUE <- sentinel")
    emit(0x90, movr("fp", "ip"), "reset spin budget")
    emit(0x94, ldr("r9", "r0", T_VALUE), "SPIN: read TIMER_1_VALUE")
    emit(0x98, cmpr("r9", "r8"), "")
    p.append((0x9c, br(0x1, CODE + 0xac, CODE + 0x9c)[0], None, "bne TICKSEEN"))
    emit(0xa0, subs1("fp"), "")
    p.append((0xa4, br(0x1, CODE + 0x94, CODE + 0xa4)[0], None, "bne SPIN"))
    p.append((0xa8, br(0xE, CODE + 0xc8, CODE + 0xa8)[0], None,
              "budget expired, sentinel intact -> backlog is 0"))
    emit(0xac, st("r9", "r4", O_LASTV), "TICKSEEN: publish the value the tick wrote")
    emit(0xb0, st("r1", "r0", T_CLEAR), "TIMER_1_CLEAR -- one decrement")
    emit(0xb4, add1("sl"), "")
    emit(0xb8, st("sl", "r4", O_DRAIN), "publish the drained count")
    emit(0xbc, cmpr("sl", "sp"), "")
    p.append((0xc0, br(0xA, CODE + 0xdc, CODE + 0xc0)[0], None, "bge OVER"))
    p.append((0xc4, br(0xE, CODE + 0x8c, CODE + 0xc4)[0], None, "b DLOOP"))
    emit(0xc8, mov("r1", 3), "DONE:")
    emit(0xcc, st("r1", "r4", O_PHASE), "PHASE = 3")
    emit(0xd0, ldr("r1", "r0", 0), "final VENDOR_ID")
    emit(0xd4, st("r1", "r4", O_VEND), "")
    p.append((0xd8, br(0xE, CODE + 0xd8, CODE + 0xd8)[0], None, "HALT"))
    emit(0xdc, mov("r1", 4), "OVER:")
    emit(0xe0, st("r1", "r4", O_PHASE), "PHASE = 4 -- drain limit hit")
    p.append((0xe4, br(0xE, CODE + 0xd8, CODE + 0xe4)[0], None, "b HALT"))
    return p


DRAIN_ENTRY = CODE + 0x70
PROLOGUE_N = 21          # 0x00 .. 0x50 inclusive


# ------------------------------------------------------------------ session
class Session:
    def __init__(self):
        self.buf, self.dead = "", False
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", "32",
                            "0x%x:%s" % (CODE, STUB)])
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
        #  `_mark`, not `mark`: gate 6's fresh-mark census keys on that exact spelling.
        #  Every other pty probe in the tree writes it that way, so a probe spelling it
        #  `mark` has the guard PRESENT and UNCOUNTED -- two of the three counts move and
        #  the third does not, a signature that reads like a defect and is not one.
        _mark, n = len(self.buf), 0
        try:
            while n < len(b):
                n += os.write(self.fd, b[n:])
        except OSError:
            self.dead = True
            return False
        return self.wait(mark=_mark, echo=x if x else None, timeout=timeout)

    def free_run(self, seconds):
        mark = len(self.buf)
        b, n = b"continue\n", 0
        try:
            while n < len(b):
                n += os.write(self.fd, b[n:])
        except OSError:
            self.dead = True
            return False, 0.0
        t0 = time.time()
        while time.time() - t0 < seconds:
            if not self.rd(0.25):
                return False, time.time() - t0
        try:
            os.kill(self.pid, signal.SIGINT)
        except OSError:
            self.dead = True
            return False, time.time() - t0
        ok = self.wait(mark=mark, timeout=20)
        t1 = time.time()
        if not ok and not self.dead:
            try:
                os.kill(self.pid, signal.SIGINT)
            except OSError:
                pass
            ok = self.wait(mark=mark, timeout=20)
            t1 = time.time()
        return ok, t1 - t0

    def read_words(self, addr, n):
        mark = len(self.buf)
        if not self.send("dump 0x%08x 0x%08x" % (addr, addr + 4 * n)):
            return None
        out = {}
        for line in self.buf[mark:].splitlines():
            m = re.match(r"\s*0x([0-9a-f]{8})\s+((?:[0-9a-f]{8}\s+){1,4})", line)
            if not m:
                continue
            base = int(m.group(1), 16)
            for i, w in enumerate(m.group(2).split()):
                out[base + 4 * i] = struct.unpack("<I", struct.pack(">I", int(w, 16)))[0]
        vals = [out.get(addr + 4 * i) for i in range(n)]
        return None if any(v is None for v in vals) else vals

    def regs(self, which=(3, 5, 6, 7)):
        mark = len(self.buf)
        if not self.send("reg", timeout=30) or self.dead:
            return {}
        seg, got = self.buf[mark:], {}
        for k in which:
            m = re.search(r"\br%d\s*=\s*0x([0-9a-fA-F]+)" % k, seg)
            if m:
                got[k] = int(m.group(1), 16)
        return got

    def close(self):
        for f in (lambda: os.write(self.fd, b"quit\n"), lambda: time.sleep(0.3),
                  lambda: os.close(self.fd), lambda: os.waitpid(self.pid, 0)):
            try:
                f()
            except Exception:
                pass


def plant(s, prog):
    for off, v in CONSTS.items():
        s.send("put w 0x%08x, 0x%08x" % (DATA + off, v))
    for off in OUTS:
        s.send("put w 0x%08x, 0x%08x" % (DATA + off, POISON))
    for off, word, _t, _c in prog:
        s.send("put w 0x%08x, 0x%08x" % (CODE + off, word))
    s.send("pc=0x%08x" % CODE)


def spell_ok(expected, got):
    """The emulator's own spelling differs cosmetically from the generator's:
    it prints `ldr r5,[r4]` for a zero offset and `#0` rather than `#0x0`.  Those
    are FORMAT differences, not encoding differences -- the WORD is compared
    separately and exactly.  Normalise both sides so the check keeps its teeth
    (a wrong register or a wrong offset still fails) without red rows for
    punctuation."""
    def norm(t):
        t = re.sub(r"\s+", "", t.lower())
        t = re.sub(r",#0\]", "]", t)                      # [r4,#0]  -> [r4]
        t = re.sub(r"#0x([0-9a-f]+)",
                   lambda m: "#" + str(int(m.group(1), 16)), t)   # #0x100 -> #256
        return t
    return norm(expected) == norm(got)


def step_and_check(s, prog, n):
    planted = {CODE + off: (w, t) for off, w, t, _ in prog}
    bad, covered, ex = [], set(), []
    for _ in range(n):
        mark = len(s.buf)
        if not s.send("step 1", timeout=30) or s.dead:
            bad.append("host died / no prompt at step %d" % (len(ex) + 1))
            break
        m = re.search(r"([0-9a-f]{8}):\s+([0-9a-f]{8})\s+([^\r\n<]+)", s.buf[mark:])
        if not m:
            bad.append("no step line at step %d" % (len(ex) + 1))
            break
        addr, word = int(m.group(1), 16), int(m.group(2), 16)
        got = re.sub(r"\s+", " ", m.group(3)).strip()
        ex.append((addr, word, got))
        if addr not in planted:
            bad.append("stepped 0x%08x, never planted" % addr)
            continue
        pw, pt = planted[addr]
        covered.add(addr)
        if word != pw:
            bad.append("0x%08x read back 0x%08x, planted 0x%08x" % (addr, word, pw))
        if pt is not None and not spell_ok(pt, got):
            bad.append("0x%08x %08x -> %r, expected %r" % (addr, word, got, pt))
    return bad, covered, ex


def run_arm(label, mmu_on=False, disable=False, accrue=None, max_drain_s=30.0):
    accrue = ACCRUE_S if accrue is None else accrue
    prog = build(mmu_on=mmu_on, disable_during_accrual=disable)
    s = Session()
    if not s.wait(timeout=120):
        s.close()
        return dict(label=label, status="NO-PROMPT")
    plant(s, prog)
    bad, cov, ex = step_and_check(s, prog, PROLOGUE_N)
    #  ACCRUAL.  The SIGALRM timer is stopped at the debugger prompt
    #  (debugger.c:800) and restarted on `continue` (:840), so only free-run
    #  seconds accrue -- which is what makes rate*T predictable at all.
    ok, dt = s.free_run(accrue)
    accrued = dt
    mid = s.read_words(DATA + O_DRAIN, 5) if ok and not s.dead else None
    #  PHASE CHANGE: the harness, not a guest clock, decides when accrual ends.
    if ok and not s.dead:
        s.send("pc=0x%08x" % DRAIN_ENTRY)
    #  DRAIN, in slices, until PHASE says done.
    t0, phase, out = time.time(), None, None
    while ok and not s.dead and time.time() - t0 < max_drain_s:
        ok, _ = s.free_run(0.5)
        if not ok or s.dead:
            break
        out = s.read_words(DATA + O_DRAIN, 5)
        if out is None:
            break
        phase = out[4]
        if phase in (3, 4):
            break
    r = s.regs()
    status = "HOST-DIED" if s.dead else ("SURVIVED" if ok else "INTERRUPT-LOST")
    s.close()
    return dict(label=label, status=status, regs=r, badis=bad, executed=ex,
                covered=cov, want={CODE + o for o, *_ in prog},
                accrued=accrued, mid=mid, out=out, phase=phase,
                drain_s=time.time() - t0)


#  Arm E walks the drain body in SEGMENTS, each entered by setting pc directly.
#
#  WHY SEGMENTS AND NOT ONE WALK, stated because the first draft did the obvious
#  thing and got 7 offsets of silent non-coverage: under `step 1` the emulated CPU
#  advances ONE cycle per command, and DEVICE_TICK is driven by the dyntrans cycle
#  counter at one call per 1 << DEV_FOOTBRIDGE_TICK_SHIFT == 16384 cycles.  So a
#  single-stepped SPIN loop can never see a delivered tick inside a few dozen steps
#  and the TICKSEEN arm is unreachable by stepping, however large the backlog is.
#
#  This check is about DECODE, not about control flow: it asks whether the emulator
#  reads back each planted word as the instruction the assembler above meant.  That
#  question is answered wherever the word executes, so entering a segment at its head
#  is legitimate here -- and it is NOT a substitute for the behavioural evidence,
#  which is separate: reaching phase 3 with a non-zero drained count is only possible
#  if 0xac..0xc4 and 0xc8..0xd4 executed for real, in order, during arms D and X.
E_SEGMENTS = ((0x70, 12),        # re-enable NOPs, freeze, PHASE=1, DLOOP, SPIN head
              (0xa0, 2),         # subs fp / bne SPIN
              (0xa8, 1),         # b DONE -- the budget-expiry arm
              (0xac, 7),         # TICKSEEN .. b DLOOP
              (0xc8, 5),         # DONE .. HALT
              (0xdc, 2),         # OVER
              (0xe4, 1))         # b HALT


def run_drainenc():
    """Arm E: every word of the drain body stepped as it EXECUTES."""
    prog = build()
    s = Session()
    if not s.wait(timeout=120):
        s.close()
        return dict(status="NO-PROMPT", badis=[], covered=set(), nsteps=0, executed=[])
    plant(s, prog)
    bad, cov, ex = step_and_check(s, prog, PROLOGUE_N)
    for head, n in E_SEGMENTS:
        if s.dead:
            break
        s.send("pc=0x%08x" % (CODE + head))
        b2, c2, e2 = step_and_check(s, prog, n)
        bad += b2
        cov |= c2
        ex += e2
    status = "HOST-DIED" if s.dead else "SURVIVED"
    s.close()
    return dict(status=status, badis=bad, covered=cov, nsteps=len(ex), executed=ex)


def run_kill():
    prog = build(kill=True)
    s = Session()
    if not s.wait(timeout=120):
        s.close()
        return dict(status="NO-PROMPT", saw=False)
    plant(s, prog)
    step_and_check(s, prog, PROLOGUE_N + 3)
    died = s.dead
    if not died:
        s.send("reg", timeout=10)
        died = s.dead
    saw = "ENABLE SET" in s.buf
    s.close()
    return dict(status="HOST-DIED" if died else "SURVIVED", saw=saw)


def main():
    t0 = time.time()
    print("=" * 78)
    print("fbpending DRAIN PROBE -- %s" % BIN)
    print("  TIMER %d (index %d, base 0x%x): FCLK_256, load %d -> %.2f Hz.  accrual %.1f s"
          % (TIMER_NR + 1, TIMER_NR, TBASE, LOAD_RUN, RATE, ACCRUE_S))
    print("  UNCAPPED prediction: backlog = %.0f" % (RATE * ACCRUE_S))
    print("=" * 78)

    skip = dict(label="(not run)", status="SKIPPED", regs={}, badis=[],
                covered=set(), executed=[], out=None, mid=None, phase=None)
    K = run_kill() if not ONLY else dict(status="SKIPPED", saw=False)
    E = run_drainenc() if not ONLY else dict(status="SKIPPED", badis=[],
                                             covered=set(), nsteps=0, executed=[])
    T = (run_arm("T (MMU ON, negative control)", mmu_on=True, accrue=1.0,
                 max_drain_s=4.0) if not ONLY else dict(skip, label="T"))
    D = (run_arm("D (enabled throughout)") if ONLY != "X" else dict(skip, label="D"))
    X = (run_arm("X (DISABLED during accrual)", disable=True)
         if ONLY != "D" else dict(skip, label="X"))

    for A in (D, X, T):
        print("\n--- arm %s ---" % A["label"])
        print("    status %s  accrued %.2f s  drain wall %.1f s  phase %s"
              % (A["status"], A.get("accrued", 0), A.get("drain_s", 0),
                 A.get("phase")))
        if A.get("badis"):
            print("    *** ENCODING / READBACK MISMATCH ***")
            for b in A["badis"]:
                print("        " + b)
        if LEARN:
            for a, w, t in A.get("executed", []):
                print("      0x%08x  %08x  %s" % (a, w, t))
        rr = A.get("regs", {})
        print("    regs " + ", ".join("r%d=0x%x" % (k, v) for k, v in sorted(rr.items())))
        mid, out = A.get("mid"), A.get("out")
        if mid:
            print("    at end of accrual : drained=%-10s iters=%-12s lastv=0x%08x "
                  "vendor=0x%08x phase=%s"
                  % (mid[0], mid[1], mid[2], mid[3], mid[4]))
        if out:
            print("    after the drain   : drained=%-10s iters=%-12s lastv=0x%08x "
                  "vendor=0x%08x phase=%s"
                  % (out[0], out[1], out[2], out[3], out[4]))

    print("\n--- arm E (drain body, stepped as it EXECUTES) ---")
    print("    status %s, %d steps, %d distinct offsets covered"
          % (E["status"], E["nsteps"], len(E["covered"])))
    for b in E["badis"]:
        print("        " + b)
    if LEARN:
        for a, w, t in E["executed"]:
            print("      0x%08x  %08x  %s" % (a, w, t))

    print("\n--- arm K (failability) ---")
    print("    status %s, saw the device's own complaint: %s" % (K["status"], K["saw"]))

    print("\n" + "=" * 78)
    print("CONTROLS")
    print("=" * 78)
    ok = True

    def row(tag, good, detail):
        nonlocal ok
        ok &= bool(good)
        print("  %-4s %-46s %s" % ("ok" if good else "FAIL", tag, detail))

    rD, rX, rT = D.get("regs", {}), X.get("regs", {}), T.get("regs", {})
    ranD = D["status"] == "SURVIVED" and D.get("out") is not None
    ranX = X["status"] == "SURVIVED" and X.get("out") is not None
    row("R0 every arm produced data",
        ranD and ranX and T["status"] != "NO-PROMPT" and K["status"] != "NO-PROMPT",
        "D=%s X=%s T=%s K=%s" % (D["status"], X["status"], T["status"], K["status"]))
    row("C1 liveness: RAM through the same decode",
        rD.get(5) == 0x11223344 and rX.get(5) == 0x11223344,
        "D r5=0x%x  X r5=0x%x" % (rD.get(5, -1), rX.get(5, -1)))
    row("C2 the MMU is OFF in the device arms",
        (rD.get(3, 1) & 1) == 0 and (rX.get(3, 1) & 1) == 0,
        "CP15 c1: D=0x%x X=0x%x" % (rD.get(3, -1), rX.get(3, -1)))
    row("A1 device signature VENDOR_ID",
        rD.get(6) == VENDOR and rX.get(6) == VENDOR,
        "D r6=0x%x X r6=0x%x (expect 0x%x)" % (rD.get(6, -1), rX.get(6, -1), VENDOR))
    row("A2 device signature: the handler's own 24-bit mask",
        rD.get(7) == LOADBACK and rX.get(7) == LOADBACK,
        "wrote 0x12345678, read D=0x%08x X=0x%08x" % (rD.get(7, -1), rX.get(7, -1)))
    drain_words = {CODE + o for o in range(0x70, 0xe8, 4)}
    row("E  encodings: prologue AND drain body, as EXECUTED",
        not D.get("badis") and not X.get("badis") and not E["badis"]
        and not (drain_words - E["covered"]),
        "%d mismatches; drain offsets not stepped: %s"
        % (len(D.get("badis", [])) + len(X.get("badis", [])) + len(E["badis"]),
           " ".join("0x%x" % a for a in sorted(drain_words - E["covered"])) or "none"))
    row("K  failability: the kill instruction really kills",
        K["status"] == "HOST-DIED" and D["status"] == "SURVIVED",
        "K=%s (complaint seen: %s)" % (K["status"], K["saw"]))
    row("T  the MMU-ON control cannot see the device",
        rT.get(6) != VENDOR and rT.get(7) != LOADBACK,
        "T r6=0x%x r7=0x%x" % (rT.get(6, -1), rT.get(7, -1)))
    row("L1 the guest ran during the accrual",
        ranD and D["out"][1] not in (None, POISON) and D["out"][1] > 1000,
        "arm D accrual iterations = %s" % (D["out"][1] if ranD else "n/a"))
    row("L2 the device answered a fresh read after the drain",
        ranD and D["out"][3] == VENDOR,
        "arm D final VENDOR_ID = 0x%08x" % (D["out"][3] if ranD else -1))
    row("P  the drain terminated normally (phase 3, not the limit)",
        ranD and D["phase"] == 3 and ranX and X["phase"] == 3,
        "D phase=%s X phase=%s (4 == drain limit %d hit)"
        % (D.get("phase"), X.get("phase"), LIMIT))

    print("\n" + "=" * 78)
    print("MEASURED")
    print("=" * 78)
    predicted = RATE * D.get("accrued", 0)

    #  *** A POISONED DRAINED-COUNT IS NOT A HUGE BACKLOG, IT IS A DEAD CLOCK, and
    #  the first draft of this file reported it as 3,735,928,559 pending interrupts.
    #  0xDEADBEEF in that word means the guest never executed the publish store,
    #  i.e. the very first poll found the sentinel intact: DEVICE_TICK delivered
    #  NOTHING.  That is the OPPOSITE failure from an unbounded backlog and it is the
    #  one this whole round is about, so conflating them would have shipped a wrong
    #  record about the exact symptom under test.  Both still FAIL; they just have to
    #  fail by their own names.  A live fix can never land here: the reset leaves the
    #  counter at 1, so at least one tick is always owed.  ***
    def backlog(A, ran):
        if not ran:
            return None, False
        v = A["out"][0]
        return (0, True) if v == POISON else (v, False)

    bD, deadD = backlog(D, ranD)
    bX, deadX = backlog(X, ranX)
    print("  arm D backlog after %.2f s enabled     %s%s   (uncapped prediction %.0f)"
          % (D.get("accrued", 0), bD,
             "  <-- CLOCK DEAD: zero ticks delivered" if deadD else "", predicted))
    print("  arm X backlog after %.2f s DISABLED    %s%s   (uncapped prediction %.0f)"
          % (X.get("accrued", 0), bX,
             "  <-- CLOCK DEAD: zero ticks delivered" if deadX else "",
             RATE * X.get("accrued", 0)))
    if bD and not deadD:
        print("  arm D measured accrual rate           %.1f Hz  (asked for %.2f Hz)"
              % (bD / D["accrued"], RATE))

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("FBDRAIN_CONTROL=%s" % ("OK" if ok else "FAILED"))
    print("FBDRAIN_BACKLOG_D=%s" % bD)
    print("FBDRAIN_BACKLOG_X=%s" % bX)
    print("FBDRAIN_CLOCK_DEAD=%s" % ("D " if deadD else "") + ("X" if deadX else ""))
    if EXPECT_CAP >= 0 and ok and bD is not None and bX is not None:
        good = (bD <= EXPECT_CAP and bX <= EXPECT_CAP
                and not deadD and not deadX)
        print("FBDRAIN_BOUNDED=%s  (cap asserted: %d)"
              % ("YES" if good else "NO", EXPECT_CAP))
        print("FBDRAIN_VERDICT=%s" % ("PASS" if good else "FAIL"))
        sys.exit(0 if good else 1)
    print("FBDRAIN_VERDICT=REPORT-ONLY")
    print("PROBE_WALL=%.1fs" % (time.time() - t0))
    sys.exit(0 if ok else 1)


main()
