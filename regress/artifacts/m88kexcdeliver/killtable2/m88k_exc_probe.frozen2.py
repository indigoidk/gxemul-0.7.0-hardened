#!/usr/bin/env python3
"""m88kexcdeliver -- rung-3 witness AND detector: does the m88k exception core DELIVER a trap-like
exception (vector entry reached, shadow registers right, machine still running), or stop the machine?

`cpu_m88k.c`'s exception switch marks only RESET / INTERRUPT / INSTRUCTION_ACCESS / DATA_ACCESS
`implemented`; every other vector below M88K_EXCEPTION_USER_TRAPS_START falls to a fallback that
prints `unimplemented vector=0x%03x` and sets `running = false` on EVERY guest CPU.  The vector-
specific tail switch then has a `default:` that stops THIS cpu with `internal error` -- so a fix
needs BOTH `implemented = true` AND a tail arm (the naive one-site fix was MEASURED to halt, pass 1).
Real hardware delivers VBR + 8*vector (MC88100 UM Table 6-1, mc88100.txt:8524-8538) and the guest OS
turns it into a signal; rte resumes at SNIP (:8983-8985), the destination register is unchanged
(6.6 :9305-9308; 6.8.3 :10300-10305).

Cold-debugger probe on the COMMITTED `testm88k` machine (no machine or device edits).  Per row: a
guest program at 0x10000 planted with `put w` (liveness marker `addu r9,r0,r10` first), registers
seeded with `rN=`, a `br .` (c0000000) planted at every vector entry so a delivered exception spins
rather than executing zeros, `breakpoint add <8*vector>`, `continue`, then `reg` and `reg 0,0`.

  row        program (after the marker at 0x10000)                 raise                     entry
  div0       divu r2,r3,r0            f4436800                    ILLEGAL_INTEGER_DIVIDE 8  0x40
  ovf        add  r2,r3,r4 (7fffffff+1) f4437004                  INTEGER_OVERFLOW 9        0x48
  misalign   ld   r2,r3,0 (r3 odd)    14430000 (major opcode 5)   MISALIGNED_ACCESS 4       0x20
  bounds     tb1  0,r3,7 (r3=1)       f003d807  supervisor trap   BOUNDS_CHECK 7            0x38
  priv       stcr r3,cr1 (r3=0x2: MODE clear) 80038023; ldcr r2,cr1 80404020   PRIVILEGE 6  0x30
  privtb     stcr r3,cr1; tb1 0,r4,8 (f004d808) in user mode      PRIVILEGE 6               0x30
  unimpl     stcr r3,cr1; prom_call f400fc92 in user mode         UNIMPLEMENTED_OPCODE 5    0x28
  error      div0 whose handler at 0x40 is a misaligned ld: the 2nd fault with SFRZ set re-routes
             to ERROR 10                                                                    0x50
  dslot      br.n +8 (c4000002) with divu r2,r3,r0 in its delay slot -> the else-arm of the
             delay-slot branch (SNIP = pc+4, SFIP = delay_target)   ILLEGAL_INTEGER_DIVIDE   0x40
  errortb    tb1  0,r3,10 (r3=1)      f003d80a  supervisor trap naming ERROR (10) directly -- the
             only route to switch 1's ERROR arm (the double-fault route enters at the re-route AFTER
             switch 1, so it cannot see that arm: M_ERRORDROP escaped the error row 9/9, table 1)  0x50
  live       divu r2,r3,r4  (r3=0x60, r4=0x10) -> r2 = 6           none      LIVENESS control
  attrib     divu r2,r3,r4  (r3=0x10, r4=0x10) -> r2 = 1           none      ATTRIBUTION control
  selftest   no program: `reg 0,0` at reset must parse PSR == 0x80000002 (the CR parse works)

RESULT per fault row (the classifier tests the STOP channel before pc, deliberately: the naive fix
sets pc = entry and THEN stops, so pc alone cannot tell it from delivery):
  HALT       `unimplemented vector=` printed and the machine stopped (pre-fix)
  TAILHALT   `internal error` printed and the machine stopped (the naive fix's shape)
  STOP       the machine stopped for another reason (e.g. a wrong vector base landed in zeros)
  BADREGS    the entry breakpoint fired but a shadow-register/PSR/destination assert failed
  DELIVER    entry breakpoint fired, machine running, and every assert holds:
             pc == entry, SXIP == fault_pc|V, SNIP, SFIP, PSR == 0x8000000b (SFRZ|IND|SFD1|MODE),
             EPSR == the pre-fault PSR (0x80000002 supervisor rows; 0x00000002 user-mode rows),
             r2 unchanged (0xdeadbeef)
  NOSTART    the liveness marker never ran
Controls print DONE (r2 == the expected quotient, machine running) or a failure word.

Output: one `M88KEXC_ROW=<name> RESULT=<word> ...` line per row, `M88KEXC_RESULT=<delivered>/<fault rows>`,
`M88KEXC_SELFTEST=OK|FAIL`, `M88KEXC_DONE`.  Set M88KEXC_VERBOSE=1 for transcripts.

CONTRACT (clause e): catches a class returned to the fallback (HALT); a class reaching the tail
default (TAILHALT); a wrong vector base (STOP/BADREGS); a stale SXIP/SNIP/SFIP; a wrong PSR; a
skipped supervisor switch (the user-mode rows: EPSR MODE clear vs PSR MODE set); a wrong return
address; a written destination.  Does NOT catch: the debugmsg level; fcr2/fcr4/fcr5; scoreboard
(SSBR) bits; DMT contents; vectors 11..113 and 116..127 (fallback halts by design); SFU1 (114/115,
row m88kexcsfu1).
"""
import os, pty, re, select, struct, sys, time

BIN = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gxsec-build/gxemul"
CODE = 0x10000
DATA = 0x20000
XIP_V = 0x2
PSR_RESET = 0x80000002          # MODE | IND (cpu_m88k.c: cr[PSR] = M88K_PSR_MODE | M88K_PSR_IND)
PSR_EXC = 0x8000000b            # MODE | SFD1 | IND | SFRZ after the common path
PSR_USER = 0x00000002           # IND only: what the user-mode rows write via stcr

def tri(sub, d, s1, s2):
    return 0xf4000000 | (d << 21) | (s1 << 16) | (sub << 8) | s2

MARK = tri(0x60, 9, 0, 10)                       # addu r9,r0,r10  -> r9 = 0x12345678 (liveness)
SELF = 0xc0000000                                # br . (disp 0)
DIVU_R2_R3_R0 = tri(0x68, 2, 3, 0)               # f4436800
DIVU_R2_R3_R4 = tri(0x68, 2, 3, 4)               # f4436804
ADD_R2_R3_R4 = tri(0x70, 2, 3, 4)                # f4437004
LD_R2_R3_0 = 0x14000000 | (2 << 21) | (3 << 16)  # 14430000 (major opcode 5, ld)
TB1_0_R3_7 = 0xf003d807                          # tb1 0,r3,7   (computed vector 7, supervisor)
TB1_0_R4_8 = 0xf004d808                          # tb1 0,r4,8
TB1_0_R3_10 = 0xf003d80a                         # tb1 0,r3,10  (a supervisor trap naming vector 10 = ERROR directly)
STCR_R3_CR1 = 0x80038023                         # stcr r3,cr1 (PSR)
LDCR_R2_CR1 = 0x80404020                         # ldcr r2,cr1
PROM_CALL = 0xf400fc92                           # M88K_PROM_INSTR
BR_N_PLUS8 = 0xc4000002                          # br.n +2 words

V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR = 4, 5, 6, 7, 8, 9, 10
VECTORS = (V_MISALIGN, V_UNIMPL, V_PRIV, V_BOUNDS, V_DIV0, V_OVF, V_ERROR)

# name, program words after MARK, regs, vector, fault_pc, epsr, handler words at the div0 entry (None = br .)
ROWS = [
    ("div0",     [DIVU_R2_R3_R0],               {"r3": 0x10},                    V_DIV0,     0x10004, PSR_RESET, None),
    ("ovf",      [ADD_R2_R3_R4],                {"r3": 0x7fffffff, "r4": 1},     V_OVF,      0x10004, PSR_RESET, None),
    ("misalign", [LD_R2_R3_0],                  {"r3": DATA + 1},                V_MISALIGN, 0x10004, PSR_RESET, None),
    ("bounds",   [TB1_0_R3_7],                  {"r3": 1},                       V_BOUNDS,   0x10004, PSR_RESET, None),
    ("priv",     [STCR_R3_CR1, LDCR_R2_CR1],    {"r3": PSR_USER},                V_PRIV,     0x10008, PSR_USER,  None),
    ("privtb",   [STCR_R3_CR1, TB1_0_R4_8],     {"r3": PSR_USER, "r4": 1},       V_PRIV,     0x10008, PSR_USER,  None),
    ("unimpl",   [STCR_R3_CR1, PROM_CALL],      {"r3": PSR_USER},                V_UNIMPL,   0x10008, PSR_USER,  None),
    ("error",    [DIVU_R2_R3_R0],               {"r3": 0x10, "r5": DATA + 1},    V_ERROR,    0x10004, PSR_RESET,
                 [0x14000000 | (6 << 21) | (5 << 16)]),       # handler at 0x40: ld r6,r5,0 with r5 odd -> 2nd fault
    ("dslot",    [BR_N_PLUS8, DIVU_R2_R3_R0],   {"r3": 0x10},                    V_DIV0,     0x10008, PSR_RESET, None),
    ("errortb",  [TB1_0_R3_10],                 {"r3": 1},                       V_ERROR,    0x10004, PSR_RESET, None),
    ("live",     [DIVU_R2_R3_R4],               {"r3": 0x60, "r4": 0x10},        None,       None,    None,      None),
    ("attrib",   [DIVU_R2_R3_R4],               {"r3": 0x10, "r4": 0x10},        None,       None,    None,      None),
]
EXPECT_R2 = {"live": 6, "attrib": 1}

class Sess:
    def __init__(self):
        stub = "/tmp/gx_m88k_exc_%d.bin" % os.getpid()
        with open(stub, "wb") as f:
            f.write(struct.pack(">I", 0xf4005800))          # or r0,r0,r0 so the machine constructs
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.execvp(BIN, [BIN, "-V", "-E", "testm88k", "-M", "64", "0x10000:%s" % stub])
            os._exit(127)
        self.buf = ""
    def rd(self, t=0.4):
        r, _, _ = select.select([self.fd], [], [], t)
        if self.fd not in r:
            return True
        try:
            d = os.read(self.fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        self.buf += d.decode("latin1", "replace")
        return True
    def wait_prompt(self, mark, timeout=30):
        t = time.time()
        while time.time() - t < timeout:
            if not self.rd():
                return False
            if len(self.buf) > mark and self.buf[mark:].rstrip().endswith("GXemul>"):
                return True
        return False
    def send(self, sx, timeout=30):
        mark = len(self.buf)
        b = (sx + "\n").encode("latin1"); n = 0
        while n < len(b):
            n += os.write(self.fd, b[n:])
        self.wait_prompt(mark, timeout)
        return mark
    def cr(self, name):
        m = self.send("reg 0,0")
        mm = re.search(r"(?<![A-Z])%s=0x([0-9a-f]{8})" % name, self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def gpr(self, n):
        m = self.send("reg")
        mm = re.search(r"r%-2d\s*=\s*0x([0-9a-f]{8})" % n, self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def pc(self):
        m = self.send("reg")
        mm = re.search(r"pc\s*=\s*0x([0-9a-f]{8})", self.buf[m:])
        return int(mm.group(1), 16) if mm else None
    def close(self):
        try:
            os.write(self.fd, b"quit\n"); time.sleep(0.3); os.kill(self.pid, 9); os.waitpid(self.pid, 0)
        except Exception:
            pass

def fmt(v):
    return ("0x%08x" % v) if isinstance(v, int) else str(v)

def run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler, grace=6.0):
    s = Sess()
    if not s.wait_prompt(0, 60):
        s.close(); return dict(result="NOBOOT")
    words = [MARK] + prog + [SELF]
    for i, w in enumerate(words):
        s.send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    for v in VECTORS:                                   # every entry spins unless a handler is planted
        s.send("put w 0x%x, 0x%08x" % (8 * v, SELF))
    if handler:
        for i, w in enumerate(handler):
            s.send("put w 0x%x, 0x%08x" % (8 * V_DIV0 + 4 * i, w))
        s.send("put w 0x%x, 0x%08x" % (8 * V_DIV0 + 4 * len(handler), SELF))
    s.send("put w 0x%x, 0x%08x" % (DATA, 0x0badf00d))
    for r, v in regs.items():
        s.send("%s=0x%x" % (r, v))
    s.send("r10=0x12345678"); s.send("r2=0xdeadbeef")
    if vector is not None:
        s.send("breakpoint add 0x%x" % (8 * vector))
    s.send("pc=0x%x" % CODE)
    mark = len(s.buf)
    os.write(s.fd, b"continue\n")
    t = time.time()
    while time.time() - t < grace:
        s.rd(0.3)
        if s.buf[mark:].rstrip().endswith("GXemul>"):
            break
    if not s.buf[mark:].rstrip().endswith("GXemul>"):
        os.write(s.fd, b"\x03"); s.wait_prompt(len(s.buf), 15)
    tr = s.buf[mark:]
    halted = ("unimplemented" in tr and "vector=" in tr)
    tailhalt = "internal error" in tr
    stopped = "machines stopped" in tr
    pc = s.pc(); r2 = s.gpr(2); r9 = s.gpr(9)
    sxip, snip, sfip, psr, epsr = s.cr("SXIP"), s.cr("SNIP"), s.cr("SFIP"), s.cr("PSR"), s.cr("EPSR")
    s.close()
    started = (r9 == 0x12345678)
    res = dict(pc=pc, sxip=sxip, snip=snip, sfip=sfip, psr=psr, epsr=epsr, r2=r2, transcript=tr)
    if not started:
        res["result"] = "NOSTART"; return res
    if vector is None:
        ok = (not stopped) and r2 == EXPECT_R2[name]
        res["result"] = "DONE" if ok else ("STOP" if stopped else "BADREGS"); return res
    if halted:
        res["result"] = "HALT"
    elif tailhalt:
        res["result"] = "TAILHALT"
    elif stopped:
        res["result"] = "STOP"
    elif pc != 8 * vector:
        res["result"] = "STOP"          # ran past its grace without the entry breakpoint firing
    else:
        want = dict(sxip=(fault_pc | XIP_V), psr=PSR_EXC, epsr=epsr_exp, r2=0xdeadbeef)
        if name == "error":
            # the re-route runs with SFRZ set: the shadows stay FROZEN at the first fault's values
            want.update(sxip=(0x10004 | XIP_V), snip=(0x10008 | XIP_V), sfip=(0x1000c | XIP_V), epsr=PSR_RESET)
        elif name == "dslot":
            # the else-arm of the delay-slot branch: SNIP = (pc + 4) | V, SFIP = delay_target | V
            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((CODE + 4 + 8) | XIP_V))
        else:
            want.update(snip=((fault_pc + 4) | XIP_V), sfip=((fault_pc + 8) | XIP_V))
        bad = [k for k, v in want.items() if res.get(k) != v]
        res["result"] = "DELIVER" if not bad else "BADREGS"
        res["bad"] = bad
    return res

def selftest():
    s = Sess()
    ok = s.wait_prompt(0, 60)
    psr = s.cr("PSR") if ok else None
    s.close()
    return psr == PSR_RESET, psr

def main():
    ok, psr = selftest()
    print("M88KEXC_SELFTEST=%s psr_at_reset=%s (want 0x80000002)" % ("OK" if ok else "FAIL", fmt(psr)), flush=True)
    delivered = 0; total = 0
    for name, prog, regs, vector, fault_pc, epsr_exp, handler in ROWS:
        res = run_row(name, prog, regs, vector, fault_pc, epsr_exp, handler)
        print("M88KEXC_ROW=%-9s RESULT=%-8s pc=%s sxip=%s snip=%s sfip=%s psr=%s epsr=%s r2=%s%s" % (
            name, res.get("result"), fmt(res.get("pc")), fmt(res.get("sxip")), fmt(res.get("snip")),
            fmt(res.get("sfip")), fmt(res.get("psr")), fmt(res.get("epsr")), fmt(res.get("r2")),
            (" bad=" + ",".join(res["bad"])) if res.get("bad") else ""), flush=True)
        if vector is not None:
            total += 1
            if res.get("result") == "DELIVER":
                delivered += 1
        if os.environ.get("M88KEXC_VERBOSE"):
            print("---- transcript ----"); print(res.get("transcript", "")[-1200:]); print("--------------------")
    print("M88KEXC_RESULT=%d/%d" % (delivered, total), flush=True)
    print("M88KEXC_DONE", flush=True)

if __name__ == "__main__":
    main()
