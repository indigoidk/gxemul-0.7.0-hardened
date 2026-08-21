#!/usr/bin/env python3
"""`fbpending`: a RUNG-3 cold-debugger witness that the emulated footbridge clock
STOPS for 42.9 s in every 85.9 s, on an UNMODIFIED in-tree `-E cats`.

THE DEFECT.  dev_footbridge.c:73 declares `int pending_timer_interrupts[4]`; the four
callbacks at :86-92 do `->pending_timer_interrupts[N] ++` with no bound; and
DEVICE_TICK(footbridge) at :259-277 delivers a tick ONLY under `if (... [i] > 0)`.
Nothing decrements the counter except a guest write to TIMER_x_CLEAR, so a guest that
programs a fast timer and does not acknowledge drives the counter to INT_MAX, where `++`
is signed overflow (UB) and, in practice, wraps to INT_MIN.  For the next 2^31
increments the `> 0` test is FALSE: no INTERRUPT_ASSERT, and timer_value stops being
re-randomised.

THE RATE, arithmetic this probe measures rather than assumes.  The increments happen in
the SIGALRM handler (core/timer.c:254-290), at up to TIMER_MAX_CATCHUP (1048576) per
timer per signal, TIMER_BASE_FREQUENCY (65.0 Hz) signals per second -- a ceiling of
68,157,440 increments per WALL-CLOCK second.  The footbridge timer's own rate is
machine->emulated_hz / effective_cycles, and cats sets emulated_hz = 50,000,000
(machine_cats.c:56-57), so TIMER_1_LOAD = 1 asks for 50e6 Hz, under the ceiling and
therefore delivered in full.  2^31 / 50e6 = 42.95 s to the wrap and 2^32 / 50e6 =
85.90 s to the return, giving the 42.9-in-85.9 duty cycle this probe plots.

THE GUEST-VISIBLE DISCRIMINATOR, and why it needs no interrupt plumbing.  TIMER_1_VALUE
(dev_footbridge.c:557-562) is READ/WRITE: a read returns d->timer_value[0], a write
stores `idata & TIMER_MAX_VAL`.  DEVICE_TICK overwrites that same field with
`random() % footbridge_effective_cycles(load, control, 0)` -- and with load == 1 that
modulus is 1, so EVERY delivered tick writes exactly 0.  So the guest:

    writes 0x00AB0000 into TIMER_1_VALUE, then polls it.
    It reads back 0x00AB0000 ... until a tick lands, and then reads 0.

Each 0 is one delivered tick, counted by the guest into RAM.  Pre-wrap that count climbs
at the device-tick rate; post-wrap it FREEZES and the sentinel the guest wrote survives
indefinitely.  No interrupt controller, no IRQ enable (which would hit an unrelated
fatal()+exit(1) at dev_footbridge.c:486-499), no guest OS, no disk image.

*** WHY A FROZEN COUNTER IS NOT MERELY "THE EMULATOR STOPPED", which is the whole
    difficulty of a negative measurement.  Three quantities run CONCURRENTLY in the same
    guest loop and are published to separate RAM words every iteration: ***

      0x9024  iteration count   -- climbs whether or not the device does anything.  If
                                   this freezes, the EMULATOR stopped and the whole
                                   measurement is void.  It is a liveness control.
      0x902c  VENDOR_ID re-read -- a fresh guest ldr from footbridge+0x00 on EVERY
                                   iteration.  0x1011 here during the frozen window
                                   proves the device is still MAPPED and still
                                   DISPATCHING; what stopped is the TICK, not the
                                   device.  RAM cannot produce 0x1011.
      0x9020  delivered ticks   -- the thing under test.

    A freeze in 0x9020 while 0x9024 climbs and 0x902c still reads 0x1011 is a statement
    about dev_footbridge.c and about nothing else.

THE MMU TRAP (documented by footbridge_sites_probe.py, whose arm T this reuses).
machine_cats.c calls arm_setup_initial_translation_table(), which maps only the low
256 MB and IGNORES the top VA nibble.  The footbridge is at PA 0x42000000, outside that
window, so under the boot MMU every device read returns 0 with a RAM liveness row still
green.  Hence arm T: the same program with the three MMU-disable words replaced by nops
MUST NOT produce the device's answers.

ARMS
  A  the witness.  MMU off, TIMER_1_LOAD=1, TIMER_1_CONTROL=TIMER_ENABLE, then
     free-running in wall-clock slices with the counters sampled out of RAM between
     them.  Default 23 x 5 s = 115 s of free-run, which brackets BOTH the wrap at
     42.95 s and the return at 85.90 s.
  E  encodings.  Byte-identical to A except ONE immediate: the sentinel is 0 instead of
     0x00AB0000, which makes the poll compare equal on the first pass and therefore
     walks EVERY instruction of both loop bodies under `step 1`.  That is what lets the
     hand-assembled words of the loop -- the words actually under test -- be checked
     against the disassembly the emulator prints as it EXECUTES them, rather than
     against a separate `unassemble` of words that might never run.
  T  negative control.  MMU left on.  Must not return 0x1011 or 0x00345678.
  K  failability control.  Arm A's prologue plus ONE instruction, a guest read of
     IRQ_ENABLE_SET (footbridge+0x188), which dev_footbridge.c:486-499 answers with
     fatal() then exit(1).  A probe in which nothing can die proves nothing by
     surviving; K must kill the host and A must not.

CONTROLS ARE NOT OPTIONAL AND ABSENT DATA MUST FAIL.  Every RAM word is poisoned with
0xDEADBEEF before the run, every verdict row first requires the values it consults to be
PRESENT, and an arm that did not reach SURVIVED voids every row that reads it.  This
project has shipped a row that reported ok by comparing two -1 defaults.

PRE-FIX / POST-FIX POLARITY.  There is no fix at the time of writing, so what this file
can show is the FIRST clause of witness validity only: the symptom on the committed
build.  It is written so the SAME file is the post-fix detector -- FBPENDING_VERDICT=PASS
means the controls held AND the run was LONG ENOUGH to see the window AND the clock never
stopped.

*** A RUN THAT WAS TOO SHORT MUST NOT CERTIFY A FIX, which is "absent data must fail"
    applied to the TIME axis and is a trap this probe walked into while being written.
    At 11 x 5 s the wrap is reached at 43.1 s and only 10 s of dead window fits inside
    the run, which is under the freeze threshold -- so the probe printed SYMPTOM=ABSENT,
    VERDICT=PASS, exit 0, on a build with the defect fully present.  A shorter run than
    that would not have reached the wrap at all and would have looked even cleaner.
    Hence FBPENDING_COVERAGE: absence is only reportable once the free-run total has
    passed the predicted RETURN at 85.90 s, and otherwise the symptom is UNDETERMINED
    rather than ABSENT. ***

KNOWN BLIND SPOT, stated rather than discovered later.  This measures the guest-visible
SYMPTOM, not the undefined behaviour.  A "fix" that merely made the counter unsigned
would remove the freeze and pass every row here while leaving a wrap in place; only a
sanitizer build (regress/build_asan.sh does pass -fsanitize=address,undefined) or a row
that inspects the counter's own bound can speak to that.

usage: fbpending_witness.py <gxemul-binary> <four-byte-raw-stub>
                            [--slices N] [--slice-seconds S] [--learn]
"""
import os, pty, re, select, signal, struct, sys, time

BIN   = sys.argv[1]
STUB  = sys.argv[2]
LEARN = "--learn" in sys.argv


def _opt(name, default, cast):
    if name in sys.argv:
        return cast(sys.argv[sys.argv.index(name) + 1])
    return default


SLICES  = _opt("--slices", 23, int)
SLICE_S = _opt("--slice-seconds", 5.0, float)

CODE = 0x00008000
DATA = 0x00009000
NOP  = 0xE1A00000
NOPTXT = "mov r0,r0"          # the EMULATOR's spelling of 0xe1a00000

#  RAM the guest publishes into.  Poisoned before the run so "never written" is
#  distinguishable from "written zero".
LIVE   = DATA + 0x00          # 0x11223344, the C1 liveness constant
SRC    = DATA + 0x04          # 0x12345678, the A2 source value
CLOB   = DATA + 0x20          # delivered device ticks   <- the thing under test
ITER   = DATA + 0x24          # guest loop iterations    <- emulator liveness
LASTV  = DATA + 0x28          # last TIMER_1_VALUE read
LASTID = DATA + 0x2c          # last VENDOR_ID read      <- device still dispatching
POISON = 0xDEADBEEF

SENTINEL = 0x00AB0000         # survives `idata & TIMER_MAX_VAL` (0x00FFFFFF)
VENDOR   = 0x1011             # dev_footbridge.c:423
LOADBACK = 0x00345678         # 0x12345678 & TIMER_MAX_VAL, dev_footbridge.c:548

EMU_HZ      = 50000000.0
PREDICT_OFF = 2147483648.0 / EMU_HZ      # 42.95 s: the wrap
PREDICT_ON  = 4294967296.0 / EMU_HZ      # 85.90 s: the return

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


def prologue(sentinel_word, sentinel_txt):
    return [
    (0x0c, 0xEE113F10, "mrc 15,0,r3,cr1,cr0,0", "C2: read CP15 c1 BACK -- measures MMU state"),
    (0x10, 0xE3A00442, "mov r0,#0x42000000",    "footbridge base (machine_cats.c:63-64)"),
    (0x14, 0xE3A04A09, "mov r4,#0x9000",        "scratch RAM"),
    (0x18, 0xE5945000, "ldr r5,[r4]",           "C1 liveness: plain RAM, expect 0x11223344"),
    (0x1c, 0xE5906000, "ldr r6,[r0]",           "A1: VENDOR_ID, expect 0x1011 (RAM/absent: 0)"),
    (0x20, 0xE5942004, "ldr r2,[r4,#4]",        "0x12345678 out of RAM"),
    (0x24, 0xE5802300, "str r2,[r0,#768]",      "TIMER_1_LOAD <- 0x12345678"),
    (0x28, 0xE5907300, "ldr r7,[r0,#768]",      "A2: expect 0x00345678 -- the handler's own mask"),
    (0x2c, 0xE3A01080, "mov r1,#0x80",          "TIMER_ENABLE (dc21285reg.h:367)"),
    (0x30, 0xE5801308, "str r1,[r0,#776]",      "TIMER_1_CONTROL <- TIMER_ENABLE"),
    (0x34, 0xE3A01001, "mov r1,#1",             ""),
    (0x38, 0xE5801300, "str r1,[r0,#768]",      "TIMER_1_LOAD <- 1  => 50 MHz, modulus 1"),
    (0x3c, sentinel_word, sentinel_txt,         "the sentinel"),
    (0x40, 0xE3A0A000, "mov sl,#0",             "r10: delivered-tick count"),
    (0x44, 0xE3A0B000, "mov fp,#0",             "r11: guest iteration count"),
    ]


#  The free-running loop.  Every word is planted; NONE of it is stepped in arm A.
LOOP = [
    (0x48, 0xE5808304, "str r8,[r0,#772]",  "outer: TIMER_1_VALUE <- sentinel"),
    (0x4c, 0xE28BB001, "add fp,fp,#1",      "inner: iterations++"),
    (0x50, 0xE584B024, "str fp,[r4,#36]",   "publish iterations   -> 0x9024"),
    (0x54, 0xE5901000, "ldr r1,[r0]",       "VENDOR_ID, EVERY iteration"),
    (0x58, 0xE584102C, "str r1,[r4,#44]",   "publish VENDOR_ID    -> 0x902c"),
    (0x5c, 0xE5909304, "ldr r9,[r0,#772]",  "read TIMER_1_VALUE"),
    (0x60, 0xE5849028, "str r9,[r4,#40]",   "publish it           -> 0x9028"),
    (0x64, 0xE3590000, "cmps r9,#0",        "0 == a tick was delivered"),
    (0x68, 0x1AFFFFF7, "bne 0x804c",        "sentinel intact -> keep polling"),
    (0x6c, 0xE28AA001, "add sl,sl,#1",      "a tick was delivered: count it"),
    (0x70, 0xE584A020, "str sl,[r4,#32]",   "publish tick count   -> 0x9020"),
    (0x74, 0xEAFFFFF3, "b 0x8048",          "re-arm the sentinel"),
]
LANDING = (0x78, NOP, NOPTXT, "landing pad -- planted, never reached")
KILL    = (0x48, 0xE5907188, "ldr r7,[r0,#392]",
           "arm K: read IRQ_ENABLE_SET -> fatal()+exit(1) at dev_footbridge.c:492-497")

SENT_A = (0xE3A088AB, "mov r8,#0xab0000")     # 0x00AB0000
SENT_E = (0xE3A08000, "mov r8,#0")            # arm E: the ONE immediate that differs

PROLOGUE_N = 18          # instructions from 0x00 to 0x44 inclusive
TIMERMSG   = "asked for more ticks than a host period can deliver"


class Session:
    """One emulator process on a cold debugger."""

    def __init__(self):
        self.buf = ""
        self.dead = False
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            #  EXPLICIT PATH.  os.execvp on a bare name searches PATH; every arm then
            #  reports dead, which looks exactly like a wedged session rather than a
            #  bad invocation.
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
        _mark = len(self.buf)
        n = 0
        try:
            while n < len(b):
                n += os.write(self.fd, b[n:])
        except OSError:
            self.dead = True
            return False
        return self.wait(mark=_mark, echo=x if x else None, timeout=timeout)

    def free_run(self, seconds):
        """`continue`, drain for `seconds`, then SIGINT back to the prompt.

        Returns (ok, measured_free_run_seconds).  The pty is DRAINED throughout: a full
        pty buffer blocks the emulator, which would look like a device that stopped
        ticking -- the exact conclusion this probe is trying to reach, so it must not be
        manufacturable by the harness."""
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
        """Read n consecutive words out of RAM.  `dump` prints the raw little-endian
        bytes, so a guest word 0x11223344 comes back as `44332211` and MUST be swapped."""
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
                raw = int(w, 16)
                out[base + 4 * i] = struct.unpack("<I", struct.pack(">I", raw))[0]
        vals = [out.get(addr + 4 * i) for i in range(n)]
        return None if any(v is None for v in vals) else vals

    def regs(self, which=(0, 1, 3, 5, 6, 7, 8, 9)):
        mark = len(self.buf)
        if not self.send("reg", timeout=30) or self.dead:
            return {}
        seg = self.buf[mark:]
        names = {10: "sl", 11: "fp", 12: "ip", 13: "sp", 14: "lr"}
        got = {}
        for k in which:
            nm = names.get(k, "r%d" % k)
            m = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)" % nm, seg)
            if m:
                got[k] = int(m.group(1), 16)
        return got

    def close(self):
        try:
            os.write(self.fd, b"quit\n")
            time.sleep(0.3)
        except OSError:
            pass
        try:
            os.close(self.fd)
        except OSError:
            pass
        try:
            os.waitpid(self.pid, 0)
        except Exception:
            pass


def plant(s, prog):
    s.send("put w 0x%08x, 0x%08x" % (LIVE, 0x11223344))
    s.send("put w 0x%08x, 0x%08x" % (SRC, 0x12345678))
    for a in (CLOB, ITER, LASTV, LASTID):
        s.send("put w 0x%08x, 0x%08x" % (a, POISON))
    for off, word, _t, _c in prog:
        s.send("put w 0x%08x, 0x%08x" % (CODE + off, word))
    s.send("pc=0x%08x" % CODE)


def step_and_check(s, prog, n):
    """`step 1` n times; check every EXECUTED word against what was planted at that
    address AND its disassembly against the emulator's own spelling.  Returns
    (mismatches, covered_addresses, executed)."""
    planted = {CODE + off: (word, text) for off, word, text, _ in prog}
    bad, covered, executed = [], set(), []
    for _ in range(n):
        mark = len(s.buf)
        if not s.send("step 1", timeout=30) or s.dead:
            bad.append("host died or no prompt during step %d" % (len(executed) + 1))
            break
        seg = s.buf[mark:]
        m = re.search(r"([0-9a-f]{8}):\s+([0-9a-f]{8})\s+([^\r\n<]+)", seg)
        if not m:
            bad.append("no step line at step %d" % (len(executed) + 1))
            break
        addr, word = int(m.group(1), 16), int(m.group(2), 16)
        got = re.sub(r"\s+", " ", m.group(3)).strip()
        executed.append((addr, word, got))
        if addr not in planted:
            bad.append("stepped 0x%08x, which was never planted" % addr)
            continue
        pw, pt = planted[addr]
        covered.add(addr)
        if word != pw:
            bad.append("0x%08x read back 0x%08x, planted 0x%08x" % (addr, word, pw))
        if pt is not None and got != pt:
            bad.append("0x%08x 0x%08x -> %r, expected %r" % (addr, word, got, pt))
    return bad, covered, executed


def run_witness(head, sentinel, slices, slice_s, label):
    prog = head + prologue(sentinel[0], sentinel[1]) + LOOP + [LANDING]
    s = Session()
    if not s.wait(timeout=120):
        s.close()
        return dict(status="NO-PROMPT", label=label, samples=[], regs={}, badis=[], catchup=0)
    plant(s, prog)
    bad, _, _ = step_and_check(s, prog, PROLOGUE_N)
    r = s.regs()
    samples, t_cum, lost = [], 0.0, False
    for _ in range(slices):
        ok, dt = s.free_run(slice_s)
        t_cum += dt
        if not ok or s.dead:
            lost = True
            break
        w = s.read_words(CLOB, 4)
        if w is None:
            lost = True
            break
        samples.append(dict(t=t_cum, clob=w[0], iters=w[1], lastv=w[2], lastid=w[3]))
    if s.dead:
        status = "HOST-DIED"
    elif lost:
        status = "INTERRUPT-LOST"
    else:
        status = "SURVIVED"
    catchup = s.buf.count(TIMERMSG)
    s.close()
    return dict(status=status, label=label, regs=r, badis=bad,
                samples=samples, catchup=catchup)


def run_kill():
    prog = MMU_OFF + prologue(*SENT_A) + [KILL, (0x4c, NOP, NOPTXT, "")]
    s = Session()
    if not s.wait(timeout=120):
        s.close()
        return dict(status="NO-PROMPT", saw_fatal=False, badis=[], nsteps=0)
    plant(s, prog)
    bad, _, ex = step_and_check(s, prog, PROLOGUE_N + 1)
    died = s.dead
    if not died:
        #  The exit may land between the write and our read; one more poke settles it.
        s.send("reg", timeout=10)
        died = s.dead
    seen = "ENABLE SET" in s.buf
    s.close()
    return dict(status="HOST-DIED" if died else "SURVIVED", saw_fatal=seen,
                badis=bad, nsteps=len(ex))


def run_encodings():
    """Arm E: sentinel 0 makes the poll compare EQUAL, so `step 1` walks BOTH loop
    bodies and every planted word is checked as it EXECUTES."""
    prog = MMU_OFF + prologue(*SENT_E) + LOOP + [LANDING]
    s = Session()
    if not s.wait(timeout=120):
        s.close()
        return dict(status="NO-PROMPT", regs={}, badis=[], covered=set(), want=set(),
                    nsteps=0, executed=[])
    plant(s, prog)
    bad, covered, ex = step_and_check(s, prog, PROLOGUE_N + 2 * len(LOOP))
    r = s.regs()
    want = {CODE + off for off, *_ in prog if off != LANDING[0]}
    status = "HOST-DIED" if s.dead else "SURVIVED"
    s.close()
    return dict(status=status, regs=r, badis=bad, covered=covered, want=want,
                nsteps=len(ex), executed=ex)


def main():
    t_probe = time.time()
    print("=" * 78)
    print("fbpending witness -- %s" % BIN)
    print("  cats emulated_hz=%.0f  =>  wrap predicted at %.2f s, return at %.2f s"
          % (EMU_HZ, PREDICT_OFF, PREDICT_ON))
    print("  arm A: %d slices x %.1f s = %.0f s of FREE-RUNNING guest execution"
          % (SLICES, SLICE_S, SLICES * SLICE_S))
    print("=" * 78)

    E = run_encodings()
    K = run_kill()
    T = run_witness(MMU_NOP, SENT_A, 1, SLICE_S, "T (MMU LEFT ON)")
    A = run_witness(MMU_OFF, SENT_A, SLICES, SLICE_S, "A (the witness)")

    print("\n--- arm E : encodings, every planted word stepped as it EXECUTES ---")
    print("    status %s, %d steps, %d/%d planted offsets covered"
          % (E["status"], E["nsteps"], len(E["covered"]), len(E["want"])))
    if E["badis"]:
        print("    *** DISASSEMBLY / READBACK MISMATCH (hand-assembled-encoding trap) ***")
        for b in E["badis"]:
            print("        " + b)
    if LEARN:
        for a, w, t in E["executed"]:
            print("      0x%08x  %08x  %s" % (a, w, t))
    missing = sorted(E["want"] - E["covered"])
    if missing:
        print("    NEVER STEPPED: " + " ".join("0x%08x" % a for a in missing))
    print("    regs " + ", ".join("r%d=0x%x" % (n, v) for n, v in sorted(E["regs"].items())))

    print("\n--- arm K : failability, arm A's prologue plus ONE instruction ---")
    print("    status %s, saw the device's own complaint: %s"
          % (K["status"], K["saw_fatal"]))

    print("\n--- arm T : MMU LEFT ON, negative control ---")
    print("    status %s" % T["status"])
    print("    regs " + ", ".join("r%d=0x%x" % (n, v) for n, v in sorted(T["regs"].items())))
    for smp in T["samples"]:
        print("      t=%5.1fs  ticks=%-10d iters=%-12d lastv=0x%08x lastid=0x%08x"
              % (smp["t"], smp["clob"], smp["iters"], smp["lastv"], smp["lastid"]))

    print("\n--- arm A : THE WITNESS ---")
    print("    status %s   catch-up-bound messages: %d" % (A["status"], A["catchup"]))
    print("    regs " + ", ".join("r%d=0x%x" % (n, v) for n, v in sorted(A["regs"].items())))
    if A["badis"]:
        print("    *** prologue disassembly mismatch ***")
        for b in A["badis"]:
            print("        " + b)
    print("    %-8s %-12s %-10s %-14s %-11s %s"
          % ("t(s)", "ticks", "d(ticks)", "iters", "d(iters)", "lastv / lastid"))
    prev = None
    for smp in A["samples"]:
        dc = smp["clob"] - prev["clob"] if prev else smp["clob"]
        di = smp["iters"] - prev["iters"] if prev else smp["iters"]
        flag = "   <-- CLOCK STOPPED" if (prev and dc == 0) else ""
        print("    %-8.2f %-12d %-10d %-14d %-11d 0x%08x / 0x%08x%s"
              % (smp["t"], smp["clob"], dc, smp["iters"], di,
                 smp["lastv"], smp["lastid"], flag))
        prev = smp

    # ------------------------------------------------------------------ analysis
    S = A["samples"]
    #  (index of the LATER sample, t_start, t_end, d_ticks, d_iters)
    deltas = [(i, S[i - 1]["t"], S[i]["t"],
               S[i]["clob"] - S[i - 1]["clob"], S[i]["iters"] - S[i - 1]["iters"])
              for i in range(1, len(S))]
    frozen = [d for d in deltas if d[3] == 0]
    frozen_span = sum(d[2] - d[1] for d in frozen)
    live_pre = [d for d in deltas if d[3] > 0 and d[2] <= PREDICT_OFF]
    live_rate = (sum(d[3] for d in live_pre) / sum(d[2] - d[1] for d in live_pre)) \
        if live_pre else 0.0
    plateau = max((s["clob"] for s in S), default=0)
    first_frozen_t = frozen[0][1] if frozen else None
    last_frozen_t = frozen[-1][2] if frozen else None
    #  Ticks are linear in free-run time before the wrap, so the plateau height divided
    #  by the measured pre-wrap rate IS the wrap time, to finer resolution than a slice.
    plateau_clob = S[frozen[0][0] - 1]["clob"] if frozen else None
    interp = (plateau_clob / live_rate) if (frozen and live_rate > 0) else None
    resumed = bool(frozen) and any(d[3] > 0 and d[1] >= last_frozen_t for d in deltas)

    print("\n" + "=" * 78)
    print("CONTROLS  (if any is RED, every row below it is meaningless)")
    print("=" * 78)
    ok = True

    def row(tag, good, detail):
        nonlocal ok
        ok &= bool(good)
        print("  %-4s %-47s %s" % ("ok" if good else "FAIL", tag, detail))

    rA, rE, rT = A["regs"], E["regs"], T["regs"]
    ranA = A["status"] == "SURVIVED" and len(S) == SLICES
    ranE = E["status"] == "SURVIVED"
    ranT = T["status"] == "SURVIVED" and len(T["samples"]) == 1

    row("R0 every arm produced data", ranA and ranE and ranT and K["status"] != "NO-PROMPT",
        "A=%s(%d/%d samples) E=%s T=%s K=%s"
        % (A["status"], len(S), SLICES, E["status"], T["status"], K["status"]))
    row("C1 liveness: RAM through the same decode",
        rA.get(5) == 0x11223344 and rE.get(5) == 0x11223344,
        "A r5=0x%x  E r5=0x%x" % (rA.get(5, -1), rE.get(5, -1)))
    row("C2 the MMU is OFF in the device arms",
        (rA.get(3, 1) & 1) == 0 and (rE.get(3, 1) & 1) == 0,
        "CP15 c1: A=0x%x E=0x%x (bit 0 must be clear)"
        % (rA.get(3, -1), rE.get(3, -1)))
    row("A1 device signature VENDOR_ID",
        rA.get(6) == VENDOR and rE.get(6) == VENDOR,
        "A r6=0x%x E r6=0x%x (expect 0x%x; RAM and absent both give 0)"
        % (rA.get(6, -1), rE.get(6, -1), VENDOR))
    row("A2 device signature: the handler's own 24-bit mask",
        rA.get(7) == LOADBACK and rE.get(7) == LOADBACK,
        "wrote 0x12345678, read A=0x%08x E=0x%08x (RAM would return 0x12345678)"
        % (rA.get(7, -1), rE.get(7, -1)))
    row("E  encodings: every planted word, as EXECUTED",
        ranE and not E["badis"] and not (E["want"] - E["covered"]),
        "%d mismatches, %d/%d offsets stepped"
        % (len(E["badis"]), len(E["covered"]), len(E["want"])))
    row("K  failability: the kill instruction really kills",
        K["status"] == "HOST-DIED" and A["status"] == "SURVIVED",
        "K=%s (device complaint seen: %s), A=%s"
        % (K["status"], K["saw_fatal"], A["status"]))
    row("T  the MMU-ON control cannot see the device",
        ranT and rT.get(6) != VENDOR and rT.get(7) != LOADBACK,
        "T r6=0x%x r7=0x%x" % (rT.get(6, -1), rT.get(7, -1)))
    ratio = (S[0]["iters"] / S[0]["clob"]) if (S and S[0]["clob"]) else 0
    row("D1 the ticks come from the DEVICE, not an absent read",
        bool(S) and S[0]["clob"] > 0 and ratio >= 100,
        "iters/ticks in slice 1 = %.0f (an unmapped read gives ~1)" % ratio)
    row("L1 the guest never stopped running",
        bool(deltas) and all(d[4] > 0 for d in deltas),
        "min d(iters) over %d slices = %s"
        % (len(deltas), min((d[4] for d in deltas), default="n/a")))
    row("L2 the device stayed MAPPED and DISPATCHING throughout",
        bool(S) and all(s["lastid"] == VENDOR for s in S),
        "live VENDOR_ID re-read == 0x1011 in %d/%d samples"
        % (sum(1 for s in S if s["lastid"] == VENDOR), len(S)))
    row("L3 TIMER_1_VALUE still answers reads throughout",
        bool(S) and all(s["lastv"] in (0, SENTINEL) for s in S),
        "every sample's last read is 0 or the sentinel 0x%08x" % SENTINEL)

    print("\n" + "=" * 78)
    print("MEASURED")
    print("=" * 78)
    print("  pre-wrap delivered-tick rate       %.1f ticks/s" % live_rate)
    print("  highest tick count reached         %d" % plateau)
    print("  slices delivering ZERO ticks       %d of %d  (%.1f s of free-run)"
          % (len(frozen), len(deltas), frozen_span))
    if frozen:
        print("  dead window (slice-bracketed)      %.2f s .. %.2f s"
              % (first_frozen_t, last_frozen_t))
    if interp:
        print("  wrap time, interpolated            %.2f s   (predicted %.2f s)"
              % (interp, PREDICT_OFF))
    print("  clock RESUMED after the freeze     %s   (predicted return at %.2f s)"
          % ("yes" if resumed else "no", PREDICT_ON))
    print("  timer catch-up-bound messages      %d" % A["catchup"])

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    #  COVERAGE IS A SEPARATE TOKEN FROM CONTROL on purpose: "the probe is broken" and
    #  "the probe was not run long enough to answer" are different failures and were
    #  conflated in the first draft, which reported PASS on a defective build.
    total_free = S[-1]["t"] if S else 0.0
    covered = total_free >= PREDICT_ON + SLICE_S
    print("FBPENDING_CONTROL=%s" % ("OK" if ok else "FAILED"))
    print("FBPENDING_COVERAGE=%s  (%.1f s of free-run; %.1f s needed to see the return)"
          % ("OK" if covered else "SHORT", total_free, PREDICT_ON + SLICE_S))
    if ok and frozen and frozen_span >= 15.0:
        symptom = "PRESENT"
    elif ok and covered:
        symptom = "ABSENT"
    else:
        symptom = "UNDETERMINED"
    print("FBPENDING_SYMPTOM=%s" % symptom)
    if symptom == "PRESENT":
        print("  The emulated footbridge clock delivered NOTHING for %.1f s of continuous"
              % frozen_span)
        print("  free-running guest execution, while the guest kept running and the device")
        print("  kept answering reads.  That is dev_footbridge.c:86-92 against :265.")
    good = ok and covered and symptom == "ABSENT"
    print("FBPENDING_VERDICT=%s" % ("PASS" if good else "FAIL"))
    print("PROBE_WALL=%.1fs" % (time.time() - t_probe))
    sys.exit(0 if good else 1)


main()
