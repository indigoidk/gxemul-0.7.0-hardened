#!/usr/bin/env python3
"""fbd5 pass-1 measuring seat: the five undefined-direction footbridge sites,
driven by REAL GUEST INSTRUCTIONS on a cold -E cats debugger (rung 3).

Same shape as regress/footbridge_sites_probe.py: MMU-off prologue, words planted
with `put w`, stepped ONE AT A TIME, every stepped word compared against the
disassembly the emulator itself prints.  Runs unchanged on a pre-fix and a
post-fix binary, so one script scores both colours.

usage: opus_w.py <gxemul> <stub> <arm-set>   arm-set in {witness,accept,decline}
"""
import os, pty, re, select, signal, sys, time

BIN, STUB = sys.argv[1], sys.argv[2]
SET = sys.argv[3] if len(sys.argv) > 3 else "witness"
CODE, DATA, NOP = 0x00008000, 0x00009000, 0xE1A00000
NOPTXT = "mov r0,r0"
ALIAS = {10: "sl", 11: "fp", 12: "ip", 13: "sp", 14: "lr"}
CONSTS = {0x00: 0x11223344,   # C1 liveness
          0x04: 0x00000030,   # IRQ enable mask
          0x08: 0x00000010,   # IRQ write value (inside 0x30)
          0x0c: 0x000000c0,   # FIQ enable mask
          0x10: 0x00000040,   # FIQ write value (inside 0xc0)
          0x14: 0x00000000,   # an all-zero word
          0x18: 0x00000001,   # TIMER_1_LOAD value
          0x1c: 0x000000c0,   # TIMER_ENABLE | TIMER_MODE_PERIODIC
          0x20: 0x00000034}   # IRQ enable incl. IRQ_TIMER_1 (bit 2)

PRO = [
    (0x00, 0xEE110F10, "mrc 15,0,r0,cr1,cr0,0", "read CP15 c1"),
    (0x04, 0xE3C00001, "bic r0,r0,#1",          "clear the MMU enable bit"),
    (0x08, 0xEE010F10, "mcr 15,0,r0,cr1,cr0,0", "MMU OFF -> VA == PA"),
    (0x0c, 0xEE113F10, "mrc 15,0,r3,cr1,cr0,0", "C2: read CP15 c1 BACK -> r3"),
    (0x10, 0xE3A00442, "mov r0,#0x42000000",    "footbridge base"),
    (0x14, 0xE3A04A09, "mov r4,#0x9000",        "scratch RAM"),
    (0x18, 0xE5945000, "ldr r5,[r4]",           "C1 liveness -> 0x11223344"),
    (0x1c, 0xE5906000, "ldr r6,[r0]",           "A1 device signature -> 0x1011"),
]
REGSTOP = "REGSTOP"


def P(*words):
    out, off = list(PRO), 0x20
    for w in words:
        if w == REGSTOP:
            out.append((None, REGSTOP, "", "read registers here"))
            continue
        out.append((off, w[0], w[1], w[2]))
        off += 4
    out.append((off, NOP, NOPTXT, "landing pad -- planted, never stepped"))
    return out


#  building blocks
E30   = (0xE5942004, "ldr r2,[r4,#4]",   "r2 = 0x30 (IRQ enable mask)")
SETE  = (0xE5802188, "str r2,[r0,#392]", "+0x188 IRQEnableSet <- r2")
V10   = (0xE5948008, "ldr r8,[r4,#8]",   "r8 = 0x10 (write value, inside 0x30)")
FC0   = (0xE594A00C, "ldr sl,[r4,#12]",  "sl = 0xc0 (FIQ enable mask)")
SETF  = (0xE580A288, "str sl,[r0,#648]", "+0x288 FIQEnableSet <- sl")
V40   = (0xE5948010, "ldr r8,[r4,#16]",  "r8 = 0x40 (write value, inside 0xc0)")
ZERO  = (0xE5942014, "ldr r2,[r4,#20]",  "r2 = 0")

W180  = (0xE5808180, "str r8,[r0,#384]", "SITE +0x180 IRQ_STATUS    <- r8 (WRITE: undefined direction)")
W184  = (0xE5808184, "str r8,[r0,#388]", "SITE +0x184 IRQ_RAW_STAT  <- r8 (WRITE: undefined direction)")
W280  = (0xE5808280, "str r8,[r0,#640]", "SITE +0x280 FIQ_STATUS    <- r8 (WRITE: undefined direction)")
W284  = (0xE5808284, "str r8,[r0,#644]", "SITE +0x284 FIQ_RAW_STAT  <- r8 (WRITE: undefined direction)")
R18C1 = (0xE590118C, "ldr r1,[r0,#396]", "SITE +0x18c IRQ_ENABLE_CLEAR -> r1 (READ: undefined direction)")
R18C7 = (0xE590718C, "ldr r7,[r0,#396]", "SITE +0x18c IRQ_ENABLE_CLEAR -> r7 (READ: 2nd access)")

RB180_1 = (0xE5901180, "ldr r1,[r0,#384]", "read back +0x180 -> r1")
RB184_7 = (0xE5907184, "ldr r7,[r0,#388]", "read back +0x184 -> r7")
RB188_9 = (0xE5909188, "ldr r9,[r0,#392]", "read back +0x188 -> r9 (IRQEnable)")
RB280_1 = (0xE5901280, "ldr r1,[r0,#640]", "read back +0x280 -> r1")
RB284_7 = (0xE5907284, "ldr r7,[r0,#644]", "read back +0x284 -> r7")
RB288_9 = (0xE5909288, "ldr r9,[r0,#648]", "read back +0x288 -> r9 (FIQEnable)")
CLR10   = (0xE580818C, "str r8,[r0,#396]", "+0x18c IRQEnableClear <- 0x10 (LEGAL write)")
CLR0    = (0xE580218C, "str r2,[r0,#396]", "+0x18c IRQEnableClear <- 0 (LEGAL, no-op)")
RB188_B = (0xE590B188, "ldr fp,[r0,#392]", "read back +0x188 -> fp")
CLRF40  = (0xE580828C, "str r8,[r0,#652]", "+0x28c FIQEnableClear <- 0x40 (LEGAL write)")
RB288_C = (0xE590C288, "ldr ip,[r0,#648]", "read back +0x288 -> ip")

E34    = (0xE5942020, "ldr r2,[r4,#32]",  "r2 = 0x34 (enable, incl. IRQ_TIMER_1 bit 2)")
TLOAD  = (0xE5948018, "ldr r8,[r4,#24]",  "r8 = 1 (timer load)")
TL_ST  = (0xE5808300, "str r8,[r0,#768]", "+0x300 TIMER_1_LOAD <- 1")
TCTL   = (0xE594801C, "ldr r8,[r4,#28]",  "r8 = 0xc0 (ENABLE|PERIODIC)")
TC_ST  = (0xE5808308, "str r8,[r0,#776]", "+0x308 TIMER_1_CONTROL <- 0xc0")
SPIN   = (NOP, NOPTXT, "spin a step while the tick runs")
R18C2  = (0xE590218C, "ldr r2,[r0,#396]", "SITE +0x18c read (5th site, same process)")
RB280_B = (0xE590B280, "ldr fp,[r0,#640]", "read back +0x280 -> fp")
RB284_C = (0xE590C284, "ldr ip,[r0,#644]", "read back +0x284 -> ip")

R190_1 = (0xE5901190, "ldr r1,[r0,#400]", "SIBLING +0x190 IRQSoft READ (write-only reg)")
R28C_7 = (0xE590728C, "ldr r7,[r0,#652]", "SIBLING +0x28c FIQEnableClear READ (write-only reg)")
R290_9 = (0xE5909290, "ldr r9,[r0,#656]", "SIBLING +0x290 FIQSoft READ (write-only reg)")
W190   = (0xE5808190, "str r8,[r0,#400]", "SIBLING +0x190 IRQSoft WRITE (the LEGAL direction)")

ARMS = {}
#  ---- 1. THE WITNESS: one guest access per site, registers read FIRST ----
ARMS["witness"] = [
    ("W1 write +0x180", P(V10, REGSTOP, W180)),
    ("W2 write +0x184", P(V10, REGSTOP, W184)),
    ("W3 write +0x280", P(V10, REGSTOP, W280)),
    ("W4 write +0x284", P(V10, REGSTOP, W284)),
    ("W5 read  +0x18c", P(REGSTOP, R18C1)),
]
#  ---- 2. THE ACCEPT SIDE: only legal directions; must already work at HEAD ----
ARMS["accept"] = [
    ("A-IRQ legal directions",
     P(E30, SETE, RB180_1, RB184_7, V10, CLR10, RB188_9, ZERO, CLR0, RB188_B, REGSTOP)),
    ("A-FIQ legal directions",
     P(FC0, SETF, RB280_1, RB284_7, RB288_9, V40, CLRF40, RB288_C, REGSTOP)),
]
#  ---- 3. POST-FIX: two accesses per site, then the state read back ----
ARMS["decline"] = [
    ("D1 two writes +0x180",
     P(E30, SETE, V10, W180, W180, RB180_1, RB184_7, RB188_9, REGSTOP)),
    ("D2 two writes +0x184",
     P(E30, SETE, V10, W184, W184, RB180_1, RB184_7, RB188_9, REGSTOP)),
    ("D3 two reads  +0x18c",
     P(E30, SETE, R18C1, R18C7, RB188_9, REGSTOP)),
    ("D4 two writes +0x280",
     P(FC0, SETF, V40, W280, W280, RB280_1, RB284_7, RB288_9, REGSTOP)),
    ("D5 two writes +0x284",
     P(FC0, SETF, V40, W284, W284, RB280_1, RB284_7, RB288_9, REGSTOP)),
]
#  ---- 4. X: two DIFFERENT sites in ONE process (the shared-latch question) ----
ARMS["cross"] = [
    ("X1 +0x180 then +0x184, one process",
     P(E30, SETE, V10, W180, W184, RB180_1, RB184_7, RB188_9, REGSTOP)),
    ("X2 +0x280 then +0x284, one process",
     P(FC0, SETF, V40, W280, W284, RB280_1, RB284_7, RB288_9, REGSTOP)),
]
#  ---- 6. ALL FIVE sites in ONE process: one arm, five announcements ----
ARMS["all5"] = [
    ("Z1 all five sites, one process",
     P(E30, SETE, V10, W180, W184, FC0, SETF, V40, W280, W284, R18C2,
       RB180_1, RB184_7, RB188_9, RB280_B, RB284_C, REGSTOP)),
]
#  ---- 7. SIBLING PARITY: the other write-only interrupt-controller registers ----
ARMS["sibling"] = [
    ("Y1 reads of 190h / 28ch / 290h, twice each",
     P(R190_1, R190_1, R28C_7, R28C_7, R290_9, R290_9, REGSTOP)),
    ("Y2 the LEGAL write to 190h (IRQSoft), twice",
     P(V10, W190, W190, RB180_1, RB184_7, REGSTOP)),
]
#  ---- 5. S: can a guest make irq_status NONZERO under single-stepping? ----
ARMS["seed"] = [
    ("S1 arm timer 1, spin, read raw status",
     P(E34, SETE, TLOAD, TL_ST, TCTL, TC_ST,
       *([SPIN] * 24 + [RB180_1, RB184_7, RB188_9, REGSTOP]))),
]


def hx(v):
    return "-" if v is None else "0x%08x" % v


def run(label, prog):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", "32",
                        "0x%x:%s" % (CODE, STUB)])
        os._exit(127)
    buf = ""
    dead = [False]

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
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
        return wait(mark=_mark, echo=x if x else None)

    def grabregs():
        mark = len(buf)
        got = {}
        if send("reg", timeout=30) and not dead[0]:
            for n in range(16):
                nm = ALIAS.get(n, "r%d" % n)
                mm = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)" % nm, buf[mark:])
                if mm:
                    got[n] = int(mm.group(1), 16)
        return got

    print("")
    print("==== arm %s" % label)
    status, regs, pre = "SURVIVED", {}, {}
    if not wait(timeout=120):
        print("  NO-PROMPT")
        status = "NO-PROMPT"
    else:
        for o in sorted(CONSTS):
            send("put w 0x%08x, 0x%08x" % (DATA + o, CONSTS[o]))
        for off, word, _t, _c in prog:
            if word == REGSTOP:
                continue
            send("put w 0x%08x, 0x%08x" % (CODE + off, word))
        send("pc=0x%08x" % CODE)
        n_last = len(prog) - 1
        for i, (off, word, text, c) in enumerate(prog):
            if word == REGSTOP:
                pre = grabregs()
                print("  --- REG checkpoint: r3=%s r5=%s r6=%s r8=%s"
                      % (hx(pre.get(3)), hx(pre.get(5)), hx(pre.get(6)), hx(pre.get(8))))
                continue
            if i == n_last:
                break               # landing pad: planted, never stepped
            mark = len(buf)
            if not send("step 1", timeout=30) or dead[0]:
                status = "HOST-DIED"
                print("  0x%02x 0x%08x  *** PROCESS ENDED HERE ***  | %s" % (off, word, c))
                break
            seg = buf[mark:]
            m = re.search(r"%08x:\s+%08x\s+([^\r\n<]+)" % (CODE + off, word), seg)
            got = re.sub(r"\s+", " ", m.group(1)).strip() if m else "(NO STEP LINE)"
            flag = "" if got == text else "   *** DISASSEMBLY MISMATCH, expected %r" % text
            print("  0x%02x 0x%08x  %-24s | %s%s" % (off, word, got, c, flag))
        if status == "SURVIVED":
            regs = grabregs()
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    t1, eof = time.time(), False
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
            gone = True
            break
        if rpid == 0:
            time.sleep(0.05)
    hk = False
    if rpid == 0 and not gone:
        hk = True
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
    if hk and sig == signal.SIGKILL:
        sig = "HARNESS-KILL(%s)" % sig
    elif not eof and sig is not None:
        sig = "HARNESS-CLOSE(%s)" % sig
    print("  STATUS=%s exit=%s signal=%s eof=%s" % (status, code, sig, eof))
    print("  COMPLAINTS (%d): %s" % (len(fatals), fatals if fatals else "NONE"))
    src = regs if regs else pre
    if src:
        print("  regs r1=%s r2=%s r5=%s r6=%s r7=%s r8=%s r9=%s sl=%s fp=%s ip=%s"
              % tuple(hx(src.get(n)) for n in (1, 2, 5, 6, 7, 8, 9, 10, 11, 12)))
    return {"label": label, "status": status, "exit": code, "signal": sig,
            "fatals": fatals, "regs": regs, "pre": pre}


print("OPUS_W BINARY=%s SET=%s" % (BIN, SET))
t0 = time.time()
res = [run(l, p) for l, p in ARMS[SET]]
print("")
print("==== SUMMARY (%s) ====" % SET)
for r in res:
    print("%-24s status=%-10s exit=%-5s complaints=%d  %s"
          % (r["label"], r["status"], r["exit"], len(r["fatals"]),
             r["fatals"][0] if r["fatals"] else ""))

#  ---------------- scored rows, post-fix expectations ----------------
ROWS = []


def rowv(tag, arm, reg, want, note):
    got = res[arm]["regs"].get(reg)
    ok = got == want
    ROWS.append((tag, ok))
    print("%-6s %-46s got=%-12s want=%-12s %s"
          % (tag, note, hx(got), hx(want), "ok" if ok else "RED"))


def rowc(tag, arm, n, text, note):
    f = res[arm]["fatals"]
    ok = (len(f) == n and res[arm]["exit"] == 0
          and res[arm]["status"] == "SURVIVED"
          and all(text in x for x in f))
    ROWS.append((tag, ok))
    print("%-6s %-46s n=%-2d exit=%-4s %-9s %s"
          % (tag, note, len(f), res[arm]["exit"], res[arm]["status"],
             "ok" if ok else "RED"))
    if f and not all(text in x for x in f):
        print("       text got %r, wanted it to contain %r" % (f[0], text))


print("")
print("---- scored rows ----")
if SET == "accept":
    rowv("A1", 0, 1, 0x00000000, "+0x180 read, enable 0x30 (status & enable)")
    rowv("A2", 0, 7, 0x00000000, "+0x184 read (raw status)")
    rowv("A3", 0, 9, 0x00000020, "+0x18c write 0x10 -> enable 0x20")
    rowv("A3b", 0, 11, 0x00000020, "+0x18c write 0 preserves 0x20")
    rowv("A4", 1, 1, 0x00000000, "+0x280 read, fiq_enable 0xc0")
    rowv("A5", 1, 7, 0x00000000, "+0x284 read")
    rowv("A6", 1, 9, 0x00000000, "+0x288 read (fiqenableread: 0 today)")
    rowc("AQ1", 0, 0, "", "A-IRQ arm: silent, exit 0")
    rowc("AQ2", 1, 0, "", "A-FIQ arm: silent, exit 0")
elif SET == "decline":
    for i, (tag, r1, r7, r9, txt) in enumerate([
            ("D1", 0, 0, 0x30, "write to irq status? (once)"),
            ("D2", 0, 0, 0x30, "write to irq_raw_status (once)"),
            ("D3", 0, 0, 0x30, "read from ENABLE CLEAR? (once)"),
            ("D4", 0, 0, 0x00, "write to fiq status? (once)"),
            ("D5", 0, 0, 0x00, "write to fiq_raw_status (once)")]):
        rowv(tag + "s", i, 1, r1, tag + ": first state readback unchanged")
        rowv(tag + "r", i, 7, r7, tag + ": second state readback unchanged")
        rowv(tag + "e", i, 9, r9, tag + ": enable register unchanged")
        rowc(tag + "n", i, 1, txt, tag + ": announced ONCE over two accesses")
elif SET == "cross":
    rowc("X1n", 0, 2, "footbridge", "+0x180 and +0x184 each announce (2 in one run)")
    rowc("X2n", 1, 2, "footbridge", "+0x280 and +0x284 each announce (2 in one run)")
    rowv("X1e", 0, 9, 0x00000030, "X1: enable register unchanged")
elif SET == "all5":
    rowc("Z1n", 0, 5, "footbridge", "all five sites announce in ONE process")
    rowv("Z1a", 0, 1, 0x00000000, "Z1: +0x180 unchanged")
    rowv("Z1b", 0, 7, 0x00000000, "Z1: +0x184 unchanged")
    rowv("Z1c", 0, 9, 0x00000030, "Z1: +0x188 enable unchanged")
    rowv("Z1d", 0, 11, 0x00000000, "Z1: +0x280 unchanged")
    rowv("Z1e", 0, 12, 0x00000000, "Z1: +0x284 unchanged")
elif SET == "sibling":
    rowv("Y1a", 0, 1, 0x00000000, "+0x190 read returns 0")
    rowv("Y1b", 0, 7, 0x00000000, "+0x28c read returns 0")
    rowv("Y1c", 0, 9, 0x00000000, "+0x290 read returns 0")
    print("Y1n    announcements over SIX sibling reads: %d" % len(res[0]["fatals"]))
    for f in res[0]["fatals"]:
        print("         %s" % f)
    print("Y2n    announcements over TWO legal 190h writes: %d" % len(res[1]["fatals"]))
    for f in res[1]["fatals"]:
        print("         %s" % f)
elif SET == "seed":
    rowv("S1a", 0, 1, 0x00000000, "+0x180 after arming timer 1 and spinning")
    rowv("S1b", 0, 7, 0x00000000, "+0x184 after arming timer 1 and spinning")
    rowv("S1c", 0, 9, 0x00000034, "+0x188 enable still 0x34")
elif SET == "witness":
    for i, (tag, txt) in enumerate([
            ("W1", "write to irq status?"), ("W2", "write to irq_raw_status"),
            ("W3", "write to fiq status?"), ("W4", "write to fiq_raw_status"),
            ("W5", "read from ENABLE CLEAR?")]):
        ok = res[i]["status"] == "SURVIVED" and res[i]["exit"] == 0
        ROWS.append((tag, ok))
        print("%-6s %-46s status=%-10s exit=%-4s %s"
              % (tag, "survives its single undefined-direction access",
                 res[i]["status"], res[i]["exit"], "ok" if ok else "RED"))

if ROWS:
    bad = [t for t, o in ROWS if not o]
    print("")
    print("OPUS_W_ROWS=%d of %d" % (sum(1 for _, o in ROWS if o), len(ROWS)))
    print("OPUS_W_RED=%s" % (",".join(bad) if bad else "NONE"))
print("OPUS_W_WALL=%.1fs" % (time.time() - t0))
print("OPUS_W_DONE")
