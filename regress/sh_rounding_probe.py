#!/usr/bin/env python3
"""Gate 10's measuring instrument: SuperH floating-point rounding, on real guest code.

Prints one line per vector:  <name> <mode> <got> <want> ok|FAIL
and a final SH_ROUND_RESULT=<passed>/<total>. gate_sh_rounding.sh does the asserting.

Why it is built this way
------------------------
Nothing here trusts a debugger convenience. `reg` does not print floating-point registers
on this core, and `dump`/`examine` reads do not route through device handlers -- so every
vector has the GUEST execute the instruction and store the result to memory with its own
fmov.s, and the value is recovered from a memory dump. Dump output is in memory order and
landisk is little-endian, so the four bytes are byte-swapped back.

No media, no console, no boot. The SuperH serial port drops host->guest writes
non-deterministically (the defect behind #293), so anything typed at a guest shell would be
intermittent; the debugger prompt does not go through it. A real kernel is named on the
command line only because the SH loader rejects hand-made ELFs and `-E landisk` with no
file at all never constructs the machine -- it is never executed.

Every vector must DISCRIMINATE: its two modes must want different answers, or it must be
explicitly marked a pin. Otherwise reverting #296 would leave the gate green.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]

CODE = 0x8c010000
DEST = 0x8c010100

DN = 0x00040000            # FPSCR.DN, set at reset
PR = 0x00080000            # double precision
NODN = 0x80000000          # #303 row marker, NOT an FPSCR bit: the harness strips
                           # DN for rows whose operands are denormal (see the #303
                           # rows for why a DN=1 numeric expectation would be wrong)
RN = 0x0                   # round to nearest
RZ = 0x1                   # round to zero

#  fmov.s FRm,@Rn  = 1111 nnnn mmmm 1010.  Rn = r1 throughout.
ST = {n: (0xf10a | (n << 4)) for n in range(16)}


def instr(op, store_reg):
    """Pack the operation and the store into one 32-bit little-endian write."""
    return (ST[store_reg] << 16) | op


#  name, fpscr extra bits, register seed, packed instruction word, {mode: expected}
#  A vector may carry an OPTIONAL sixth element: a second 32-bit instruction word placed
#  at CODE+4 (stepped as 3 instructions instead of 2). ftrc needs it: the result lands in
#  FPUL, so the guest runs `ftrc ; sts fpul,r2` then `mov.l r2,@r1`.
VECTORS = [
    # ---- the reported defect: FDIV, cpu_sh_instr.c fdiv single arm -------------------
    ("fdiv 1.0/3.0", 0,
     {"fr0": 0x3f800000, "fr1": 0x40400000},
     instr(0xf013, 0),                       # fdiv fr1,fr0
     {RN: 0x3eaaaaab, RZ: 0x3eaaaaaa}),

    # ---- FLOAT: int32 -> single, the one case where the SOURCE is the wide one -------
    #  16777219 = 2^24 + 3, exactly between 16777218 and 16777220.
    ("float 2^24+3", 0,
     {"fpul": 0x01000003},
     instr(0xf02d, 0),                       # float fpul,fr0
     {RN: 0x4b800002, RZ: 0x4b800001}),

    # ---- FADD: 1.0 + 1.5*2^-24, three quarters of the way up one ulp ----------------
    ("fadd 1.0+1.5*2^-24", 0,
     {"fr0": 0x3f800000, "fr1": 0x33c00000},
     instr(0xf010, 0),                       # fadd fr1,fr0
     {RN: 0x3f800001, RZ: 0x3f800000}),

    # ---- FMAC: 1.5*(1+2^-23) + 0, an exact midpoint. Manual s6.4: FMAC rounds ONCE. -
    ("fmac 1.5*(1+2^-23)", 0,
     {"fr0": 0x3fc00000, "fr1": 0x3f800001, "fr2": 0x00000000},
     instr(0xf21e, 2),                       # fmac fr0,fr1,fr2
     {RN: 0x3fc00002, RZ: 0x3fc00001}),

    # ---- FIPR: reduced-precision INTERMEDIATE, but the final round is under RM -------
    #  Manual s6.4 names FIPR and FTRV explicitly. Left truncating in the first draft of
    #  #296; a panel seat refuted that and the measurement agreed.
    ("fipr midpoint", 0,
     {"fr0": 0x3fc00000, "fr1": 0, "fr2": 0, "fr3": 0,
      "fr4": 0x3f800001, "fr5": 0, "fr6": 0, "fr7": 0},
     instr(0xf4ed, 7),                       # fipr fv0,fv4  -> fr7
     {RN: 0x3fc00002, RZ: 0x3fc00001}),

    # ---- FTRV: same class, separate site (four stores) ------------------------------
    ("ftrv midpoint", 0,
     dict([("fr0", 0x3f800001), ("fr1", 0), ("fr2", 0), ("fr3", 0),
           ("xf0", 0x3fc00000)] + [("xf%d" % i, 0) for i in range(1, 16)]),
     instr(0xf1fd, 0),                       # ftrv xmtrx,fv0 -> fr0
     {RN: 0x3fc00002, RZ: 0x3fc00001}),

    # ---- the overflow rider: leaving IEEE_RM_LEGACY changed this too ----------------
    #  Manual s6.5: RZ overflow yields the maximum normalized number, RN yields infinity.
    ("fmul 1e30*1e30 overflow", 0,
     {"fr0": 0x7149f2ca, "fr1": 0x7149f2ca},
     instr(0xf012, 0),                       # fmul fr1,fr0
     {RN: 0x7f800000, RZ: 0x7f7fffff}),

    # ---- D-format directed rounding, FIXED by #300 and now discriminating -----------
    #  This row was a PIN from #296 to #299: the D store is a pure re-encode, so wiring
    #  the STORE could never fix it, and both modes measured the host-nearest 9a. #300
    #  corrects the ARITHMETIC instead -- one fma residual recovers which neighbour the
    #  host's nearest result landed on -- so toward-zero now yields the true 99. The pin
    #  flipped exactly as its own comment required, by the only mechanism that could.
    ("Ddiv 1.0/10.0 low", PR,
     {"fr0": 0x3ff00000, "fr1": 0x00000000,
      "fr2": 0x40240000, "fr3": 0x00000000},
     instr(0xf023, 1),                       # fdiv dr2,dr0 ; store fr1 = low half
     {RN: 0x9999999a, RZ: 0x99999999}),

    # ---- the double-rounding band, FIXED by #299 and now discriminating -------------
    #  This row was a PIN from #296 to #298: the sum collapsed in host double before the
    #  store could round it, so both modes measured 0x3f800000. #299 routes the sum
    #  through round-to-odd (Knuth 2Sum + odd-force in float_emul.c), so toward-zero now
    #  yields the true 0x3f7fffff. The pin flipped exactly as its own comment required.
    ("fsub band 1.0-2^-60", 0,
     {"fr0": 0x3f800000, "fr1": 0x21800000},
     instr(0xf011, 0),                       # fsub fr1,fr0
     {RN: 0x3f800000, RZ: 0x3f7fffff}),

    # ---- #299's organic default-mode witness: the fmac tie band ---------------------
    #  (0x3fc00003 * 0x33fffffc) + 1.0 lands just below the midpoint between
    #  0x3f800001 and 0x3f800002. The manual says fmac rounds ONCE; the old
    #  two-rounding path collapsed onto the midpoint in double and ties-to-even then
    #  picked 0x3f800002. Correct under BOTH modes is 0x3f800001, so this row is
    #  mode-independent by value -- but the pre-#299 build fails its RN arm, which is
    #  what makes it a revert tripwire. Constructed and verified exactly offline.
    ("fmactie (a*b)+1.0", 0,
     {"fr0": 0x3fc00003, "fr1": 0x33fffffc, "fr2": 0x3f800000},
     instr(0xf21e, 2),                       # fmac fr0,fr1,fr2
     {RN: 0x3f800001, RZ: 0x3f800001}),

    # ---- #299 panel: Inf must pass through the round-to-odd helper UNTOUCHED --------
    #  Three seats independently refuted the first helper's NaN guard (NaN != 0.0 is
    #  TRUE in C), under which +Inf + 1.0 came back as FLT_MAX under toward-zero and
    #  -Inf - 1.0 as a NaN. The offline gate watched both corruptions happen before the
    #  isfinite() guard existed; this row keeps the rig honest about the same contract.
    ("faddinf +Inf+1.0", 0,
     {"fr0": 0x7f800000, "fr1": 0x3f800000},
     instr(0xf010, 0),                       # fadd fr1,fr0
     {RN: 0x7f800000, RZ: 0x7f800000}),

    # ---- #297: ftrc's value ladder. DELIBERATELY mode-independent -- the manual says
    #  "the rounding mode is always truncation", so these rows run under both modes and
    #  must agree; if someone ever wires ftrc to RM, the discriminating-count check
    #  catches the drift. Before #297 the conversion was a raw C cast (UB on the
    #  specials): +Inf and +2^40 measured 0x80000000 on x86 where the manual owes +MAX.
    #  sequence: ftrc fr0,fpul (0xf03d) ; sts fpul,r2 (0x025a) ; mov.l r2,@r1 (0x2122)
    ("ftrcS-inf +Inf",   0, {"fr0": 0x7f800000},
     (0x025a << 16) | 0xf03d, {RN: 0x7fffffff, RZ: 0x7fffffff},
     (0x0009 << 16) | 0x2122),
    ("ftrcS-ovf +2^40",  0, {"fr0": 0x53800000},
     (0x025a << 16) | 0xf03d, {RN: 0x7fffffff, RZ: 0x7fffffff},
     (0x0009 << 16) | 0x2122),
    #  A positive NaN also exceeds the positive range bound; the manual routes it to
    #  -MAX. This row is what catches a ladder with the checks in the wrong order.
    ("ftrcS-nan qNaN+",  0, {"fr0": 0x7fc00000},
     (0x025a << 16) | 0xf03d, {RN: 0x80000000, RZ: 0x80000000},
     (0x0009 << 16) | 0x2122),
    #  The S bound is STRICT: 0x4effffff itself is NORM and truncates to 2147483520.
    ("ftrcS-edge 4effffff", 0, {"fr0": 0x4effffff},
     (0x025a << 16) | 0xf03d, {RN: 0x7fffff80, RZ: 0x7fffff80},
     (0x0009 << 16) | 0x2122),
    #  The D bound is >=: exactly 2^31 is already Invalid -> +MAX.
    ("ftrcD-2p31 exact", PR, {"fr0": 0x41e00000, "fr1": 0x00000000},
     (0x025a << 16) | 0xf03d, {RN: 0x7fffffff, RZ: 0x7fffffff},
     (0x0009 << 16) | 0x2122),
    #  The NEGATIVE D bound is -(2^31+1): -2147483648.5 is still NORM and truncates to
    #  -2^31 -- a defined cast, not the invalid arm (same stored bits, different route).
    ("ftrcD-neghalf -2^31-0.5", PR, {"fr0": 0xc1e00000, "fr1": 0x00100000},
     (0x025a << 16) | 0xf03d, {RN: 0x80000000, RZ: 0x80000000},
     (0x0009 << 16) | 0x2122),

    # ---- #303: subnormal OPERANDS decode to their true IEEE value -------------------
    #  Every other row in this table runs under DN=1 (the reset default this probe
    #  ORs in), which is honest for them -- none has a denormal operand. These two DO,
    #  and a numeric true-IEEE expectation under DN=1 would bless a value real
    #  silicon flushes to zero, so they carry NODN: the harness STRIPS the DN bit and
    #  the architectural claim is DN=0-with-kernel-completion (which computes exactly
    #  this decode; the FPU-error trap itself stays unmodelled -- the #296/#297
    #  precedent). RM is pinned by the row's single mode key; SH-4 resets to RZ, so
    #  an unpinned mode would make the fdiv byte ambiguous (panel pass-2).
    #  Committed-build bytes, measured live before the fix: 0x32000001, 0x3f800001.
    #  The results here are NORMAL, so the #287/#292 store flush is never involved.
    ("subn fmul S-min*2^100", NODN, {"fr0": 0x00000001, "fr1": 0x71800000},
     instr(0xf012, 0),                       # fmul fr1,fr0
     {RN: 0x27000000}),
    #  quotient of garbles was ~1.0 (0x3f800001 under RN); true quotient is exactly 2.
    ("subn fdiv 2ulp/1ulp", NODN, {"fr0": 0x00000002, "fr1": 0x00000001},
     instr(0xf013, 0),                       # fdiv fr1,fr0
     {RN: 0x40000000}),
]


def run(fpscr, seed, word, word2=None):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-E", "landisk", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""

    def rd(t=0.4):
        nonlocal buf
        r, _, _ = select.select([fd], [], [], t)
        if fd not in r:
            return True
        try:
            d = os.read(fd, 65536)
        except OSError:
            return False
        if not d:
            return False
        buf += d.decode("latin1", "replace")
        return True

    def wait(timeout=40):
        t = time.time()
        while time.time() - t < timeout:
            if not rd():
                return False
            if buf.rstrip().endswith(">"):
                return True
        return False

    def send(s):
        b = (s + "\n").encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait()

    if not wait(90):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    cmds = ["fpscr=0x%08x" % fpscr]
    cmds += ["%s=0x%08x" % (k, v) for k, v in seed.items()]
    cmds += ["r1=0x%08x" % DEST,
             "put w 0x%08x, 0x%08x" % (DEST, 0xdeadbeef)]   # sentinel
    cmds += ["put w 0x%08x, 0x%08x" % (CODE, word)]
    if word2 is not None:
        cmds += ["put w 0x%08x, 0x%08x" % (CODE + 4, word2)]
    cmds += ["pc=0x%08x" % CODE,
             "step %d" % (3 if word2 is not None else 2)]
    for c in cmds:
        send(c)
    mark = len(buf)
    send("dump 0x%08x 0x%08x" % (DEST, DEST + 4))
    tail = buf[mark:]
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.4)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass

    m = re.search(r"0x0*%x\s+([0-9a-f]{8})" % DEST, tail)
    if not m:
        return None
    # dump renders bytes in memory order; landisk is little-endian.
    return int.from_bytes(bytes.fromhex(m.group(1)), "little")


passed = total = 0
for vec in VECTORS:
    name, extra, seed, word, want = vec[:5]
    word2 = vec[5] if len(vec) > 5 else None
    for mode, expect in sorted(want.items()):
        total += 1
        fps = DN | (extra & ~NODN) | mode
        if extra & NODN:
            fps &= ~DN          # #303 rows: denormal operands, DN must be clear
        got = run(fps, seed, word, word2)
        label = "nearest" if mode == RN else "toward-zero"
        if got is None:
            print("%-28s %-12s %-10s %-10s FAIL(no-readback)"
                  % (name, label, "None", "0x%08x" % expect))
            continue
        ok = (got == expect)
        passed += ok
        print("%-28s %-12s 0x%08x 0x%08x %s"
              % (name, label, got, expect, "ok" if ok else "FAIL"))

# A vector whose two modes want the SAME answer cannot detect a reverted fix. Report the
# count of genuinely discriminating vectors so the gate can assert on it rather than
# trusting that the table was written correctly. The ftrc rows are REQUIRED to be
# mode-independent (truncation by architecture), so this count doubles as the tripwire
# for anyone accidentally wiring ftrc to FPSCR.RM.
discriminating = sum(1 for v in VECTORS if len(set(v[4].values())) > 1)
print("SH_ROUND_DISCRIMINATING=%d" % discriminating)
print("SH_ROUND_RESULT=%d/%d" % (passed, total))
