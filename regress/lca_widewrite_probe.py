#!/usr/bin/env python3
"""lca_widewrite_probe.py -- the width row #530 owed (lcalenzerodrop).  MEASURED 2026-09-18.

WHAT IT PINS.  `#530`'s instruction-driven detector, lca_isalane_probe.py, cannot express a store wider
than 8 bytes -- the widest Alpha store, STQ, is 8 bytes (its own header, :148-151).  So a guard that
declines only len > 8 swept all 352 of its rows: `#530`'s KILLLEN8 leg (`len == 0 || len > 8') and the
`&& len <= 8' write-arm conjunct both scored 352/352.  CLOSE6_VERDICT.md pre-committed the disposition:
*escapes AND len > 8 is guest-reachable -> L2, add a len > 8 row in-round.*  This is that row.

THE PATH -- the NON-INSTRUCTION one, because no instruction can reach it:
    CALL_PAL 0x3fffffe      the word machine_alpha.c:189 stores at PROM_ENTRY_PADDR;
                            cpu_alpha_palcode.c:519-520 dispatches it to alpha_prom_call
      a0 = 0x22             PROM_R_GETENV          (thirdparty/alpha_prom.h:69)
      a1 = 0x8              PROM_E_BOOTED_OSFLAGS  (:85) -> s = boot_string_argument, set by -o
      a2 = k0(SP(0x2ff))    the ns16550 SCR, 64-bit K0SEG, loaded via put d + LDQ
      a3 = 16               len = min(a3, strlen(s)+1) = min(16, 17) = 16   (palcode.c:141-143)
      ra = the next insn    alpha_prom_call RETURNS THROUGH ra (palcode.c:153) -- see RUN 1 below
    -> store_buf(cpu, a2, s, 16) -> ONE memory_rw(a2, 16): 0x5fe0 fails 1024/256/64 alignment and
       passes 16 (memory.c:839-852) -> lca_isa: port 0x2ff, ofs = (0x2ff & 3) % 16 = 3 -> s[3] = 'D'

MEASURED (regress/artifacts/lcalenzerodrop/widewrite_20260918/logs/TABLE.out; every value predicted
in PRETABLE.out at 14:59:49, BEFORE any run, and every value matched):
    base        3/3   wide getenv = 0x44 ('D')
    M2_len8     2/3   wide getenv = 0x5a (the PRESET: the store fell into the READ arm)
    KILLLEN8    2/3   wide getenv = 0x5a (the PRESET: `return 0' -> MEMORY_ACCESS_FAILED, and there
                                          is no Alpha exception branch in memory_rw.c:603-624)

RUN 1 WAS AN L1 CONSTRUCTION FAILURE and is preserved, not hidden (logs/run1_L1_no_return_address/):
the CALL_PAL was executed inline WITHOUT loading ra, so the PROM call "returned" to address 0, phase 4
never ran, and every binary read 0 alike.  The PRETABLE had pre-committed that a base leg short of 3/3
means the ROW is broken, not the fix -- which is how it was read.

CONTRACT (clause e).  DESIGNED TO CATCH: any guard that declines a len > 8 WRITE to lca_isa, in either
the guard form or the write-arm-conjunct form.  DISCLOSED, NOT CAUGHT: (i) which of the 16 bytes
reaches the port -- only s[3] does, and the other 15 are dropped; that is `lcawidefold', whose reopen
condition ("a guest found issuing GETENV into the ISA window") THIS ROW MEETS; (ii) the READ side --
store_buf only writes, and no wide-read producer was found, so a read twin would drive a path no guest
reaches; (iii) widths 64/256/1024 -- 16 was measured; the others share the same `len > 8' predicate.

WITNESS vs DETECTOR.  This is a DETECTOR (green once the defect is gone).  #530's rung-3 WITNESS is
lca_isalane_probe.py's 13/16 on the committed build.
"""
import os, pty, re, select, sys, time

BIN     = sys.argv[1]
LABEL   = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH    = "alphabook1"
BOOTSTR = "ABCDEFGHIJKLMNOP"          # strlen 16, so len = min(a3=16, 17) = 16
DUMMY   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")   # as the parent

# ---- encoder, copied from lca_isalane_probe.py so the encodings are identical
ZERO, T0, T1, T2, T3, T4 = 31, 1, 2, 3, 4, 5
A0, A1, A2, A3 = 16, 17, 18, 19       # Alpha ABI a0..a3 = r16..r19.  NOT defined in the parent probe,
                                      # which deliberately names only T0..T6 -- defined here, on purpose.
def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDBU(ra, disp, rb):      return mem(0x0a, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
CALL_PAL_PROM = (0x00 << 26) | 0x3fffffe      # == 0x03fffffe, the word machine_alpha.c:189 stores

def load_const(reg, val):                     # 32-bit only, exactly as the parent
    lo = val & 0xffff
    hi = (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

SENT = 0x0bad1d8a                             # the parent's pre-seed: a faulting load leaves it
def sent(reg): return load_const(reg, SENT)

K0SEG       = 0xfffffc0000000000
def k0(p):  return K0SEG | p
LCA_PCI_SIO = 0x1c0000000
def SP(port): return LCA_PCI_SIO + (port << 5)
SCRATCH, CODE = 0x01020000, 0x01040000

# ---- harness: the parent's session(), with ONE change -- `-o BOOTSTR' -- in a separate function so
#      the parent's 352 rows cannot be affected by it
def session(cmds, settle, spin):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "-o", BOOTSTR, "0x20000000:" + DUMMY])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.45):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.5)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def build(consts, phases):                    # copied verbatim in behaviour
    prog = load_const(T0, SCRATCH)
    lens = [len(prog)]
    for ops, _ in phases:
        prog += ops
        lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, pr), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        if pr is not None:
            cmds.append("print %s" % pr)
    return cmds

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return None if not m else int(m.group(1), 16)

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-24s %-24s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

# ---- the session
SCR, PRESET = 0x2ff, 0x5a
WANT = ord(BOOTSTR[(SCR & 3) % 16])          # s[3] == 'D' == 0x44 -- derived, not typed in
#  *** RUN 1 WAS AN L1 CONSTRUCTION FAILURE AND THIS IS ITS FIX. ***  alpha_prom_call ENDS WITH
#  `cpu->pc = cpu->cd.alpha.r[ALPHA_RA]' (cpu_alpha_palcode.c:153) -- the real PROM entry is reached
#  by `jsr', which loads ra.  Run 1 executed the CALL_PAL inline WITHOUT setting ra, so the call
#  "returned" to address 0, phase 4 never ran, and t4 kept its initial 0 on every binary alike
#  (logs/run1_L1_no_return_address/).  ra is now loaded with the address of the instruction AFTER the
#  CALL_PAL -- COMPUTED FROM THE LAYOUT, not typed in, so an edit to any phase cannot silently strand it.
RA = 26                                       # Alpha ra = r26
p1 = [LDQ(T2, 0, T0)] + load_const(T1, PRESET) + [STB(T1, 0, T2)]           # preset the SCR
p2 = [LDQ(T2, 0, T0)] + sent(T3) + [LDBU(T3, 0, T2)]                         # CONTROL: reads back
p3 = (load_const(A0, 0x22) + load_const(A1, 0x8) + [LDQ(A2, 0, T0)]
      + load_const(A3, 16) + [LDQ(RA, 8, T0), CALL_PAL_PROM])               # GETENV, 16-byte store
p4 = [LDQ(T2, 0, T0)] + sent(T4) + [LDBU(T4, 0, T2)]                         # the SCR afterwards
RET = k0(CODE) + 4 * (len(load_const(T0, SCRATCH)) + len(p1) + len(p2) + len(p3))
consts = [k0(SP(SCR)), RET]                   # slot 0: the SCR; slot 8: where the PROM call returns
phases = [(p1, None), (p2, "t3"), (p3, None), (p4, "t4")]

print("lca_widewrite -- binary=%s label=%s machine=%s -o %s" % (BIN, LABEL, MACH, BOOTSTR))
cmds = build(consts, phases)
txt, alive = session(cmds, 3.0, 4.0)
#  MIRRORS THE PARENT'S run(): a session whose prints did not all arrive TIMED OUT rather than
#  measured, and is retried ONCE with tripled patience -- "the machine may be loaded".  Without this,
#  a slow run under contention reads as a FAILED ROW: a phantom red that the row did not earn.
retried = False
if printed(txt, "t3") is None or printed(txt, "t4") is None:
    retried = True
    txt, alive = session(cmds, 3.0 * 3, 4.0 * 3)
print("WIDEWRITE_RETRIED=%s" % ("yes" if retried else "none"))
if os.environ.get("WIDEWRITE_RAW"):
    open(os.environ["WIDEWRITE_RAW"], "w", encoding="utf-8").write(txt)

t3, t4 = printed(txt, "t3"), printed(txt, "t4")
row("wide alive", "alive" if alive else "died", "alive",
    "the guest survives an inline CALL_PAL 0x3fffffe")
row("wide live", t3, PRESET,
    "LIVENESS + DEVICE SIGNATURE: a 1-byte store round-trips through the SCR")
row("wide getenv", t4, WANT,
    "a 16-byte store_buf write lands s[3] on the SCR; M2 (`&& len <= 8') leaves the PRESET")
ok = sum(1 for _, o in rows if o)
print("WIDEWRITE_RESULT=%d/%d" % (ok, len(rows)))
print("WIDEWRITE_DONE")
