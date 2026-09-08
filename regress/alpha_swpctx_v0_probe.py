#!/usr/bin/env python3
"""alpha_swpctx_v0_probe.py -- does PAL_OSF1_swpctx return the old context in v0?

    usage:  alpha_swpctx_v0_probe.py <gxemul-binary> [label]

WHAT THIS PINS.  `cpu_alpha_palcode.c' handles `call_pal 0x30' (PAL_OSF1_swpctx).  Its own
comment says "Return old context in v0."; the line under that comment writes ALPHA_A0.  The
third-party ABI wrapper `alpha_pal_swpctx' (alpha_cpu.h) declares `v0 __asm("$0")' as an
OUTPUT and lists a0 as clobbered -- so a correct guest reads the result from v0 and must not
rely on a0.  The model therefore publishes its result into the register the caller is told to
discard, and leaves untouched the one the caller reads.

THE ORACLE NEEDS THREE DISTINGUISHABLE VALUES, and a row asserting only "v0 changed" would
pass an incorrect repair that returned the NEW context instead of the old one:

    C = 0x01000000   the OLD context, established by a first swpctx call
    N = 0x01010000   the NEW context, passed to the second call
    S = 0x00ab0000   a sentinel seeded into v0 immediately before the second call

    v0 == C  ->  correct                     (what this probe asserts)
    v0 == S  ->  the handler never wrote v0  (the shipped defect)
    v0 == N  ->  an incorrect repair returning the new context instead of the old

ORACLE POLARITY, per the witness ladder: the row asserts the CORRECT behaviour, so it is RED
on the pre-fix build and GREEN post-fix with the SAME script.

THE ATTRIBUTION CONTROL is the row that makes this a witness rather than a value check.
`a0 land' reads a0 after the second call.  On the shipped build a0 holds C -- which proves
THE HANDLER RAN AND WROTE THE WRONG REGISTER, and separates that from "the handler never
executed", which would leave a0 holding N and v0 holding S.  One observation, two hypotheses
distinguished.

WHY THE PROGRAM RELOADS ITS SCRATCH POINTER.  T0 is Alpha t0, which the wrapper's own clobber
list names.  Whether this model clobbers it is not the point: the guest program is written to
be correct under the ABI, not under the model's current behaviour.
"""
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-22s %-22s %-56s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder (memory format only)
ZERO, T0 = 31, 1
A0, V0 = 16, 0

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def CALL_PAL(func):          return (0x00 << 26) | (func & 0x3ffffff)

def load_const(reg, val):
    lo, hi = val & 0xffff, (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

# ---------------------------------------------------------------- addresses (ALL RAM < 64 MB)
K0SEG   = 0xfffffc0000000000
def k0(p): return K0SEG | p

SCRATCH = 0x01020000
CODE    = 0x01040000
CTX_C   = 0x01000000          # the OLD context -- a PCB the first call installs
CTX_N   = 0x01010000          # the NEW context
SENT    = 0x00ab0000          # the sentinel seeded into v0; LDAH(0xab) builds it exactly
PAL_SWPCTX = 0x30

assert max(SCRATCH, CODE, CTX_C, CTX_N) < 64 * 1024 * 1024, "everything must be inside RAM"
assert len({CTX_C, CTX_N, SENT}) == 3, "the three oracle values must be distinguishable"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- session
def session(cmds, settle=1.6, spin=2.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
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
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

print("alpha_swpctx_v0_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-22s %-22s %-56s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- the program
#  first call:  a0 = C  ->  ctx = C          (establishes the OLD context)
#  seed:        v0 = S                       (so "untouched" is distinguishable)
#  second call: a0 = N  ->  v0 should be C
first  = load_const(T0, SCRATCH) + [LDQ(A0, 0, T0), CALL_PAL(PAL_SWPCTX)]
second = load_const(T0, SCRATCH) + [LDAH(V0, SENT >> 16),
                                    LDQ(A0, 8, T0), CALL_PAL(PAL_SWPCTX)]
prog = first + second

setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0, CTX_C),
         "put d 0x%x, 0x%x" % (SCRATCH + 8, CTX_N)]
cmds  = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
cmds += ["pc=0x%x" % k0(CODE),
         "step %d" % len(first),      # up to and including the FIRST swpctx
         "print v0",                  # v0 after call 1 -- the liveness/attribution baseline
         "step %d" % len(second),     # seed the sentinel, then the SECOND swpctx
         "print v0",
         "print a0"]
txt, alive = session(cmds)

v0_after1 = printed(txt, "v0")
allv0 = re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", txt)
v0_final = "0x%x" % int(allv0[-1], 16) if allv0 else "absent"
a0_final = printed(txt, "a0")

#  ---- CONTROL 1: LIVENESS -- the guest ran and the debugger answered ---------------------
row("live", "alive" if alive else "died", "alive",
    "CONTROL: the session survives the whole sequence")
row("v0 read", "yes" if v0_after1 != "absent" else "absent", "yes",
    "CONTROL: v0 is readable at all through `print' after call 1")

#  ---- CONTROL 2: ATTRIBUTION -- the handler RAN, and we can see where it wrote ------------
#  On the shipped build a0 holds C: the handler executed and published to the wrong register.
#  If the handler had never run, a0 would still hold N and this row would read 0x1010000.
row("a0 land", a0_final, "0x%x" % CTX_N,
    "ATTRIBUTION: post-fix a0 keeps the INCOMING context; pre-fix it holds the OLD one")

#  ---- THE DEFECT ROW ---------------------------------------------------------------------
#  Asserts the CORRECT behaviour, so: pre-fix RED, post-fix GREEN, same script.
row("v0 ctx", v0_final, "0x%x" % CTX_C,
    "swpctx must return the OLD context in v0 (S=0xab0000 means it never wrote v0)")

bad = [n for n, ok in rows if not ok]
print("\nSWPCTXV0_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
if bad:
    print("FAILING: " + " ".join(bad))
print("SWPCTXV0_DONE")
