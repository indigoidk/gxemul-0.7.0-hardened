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
RN = 0x0                   # round to nearest
RZ = 0x1                   # round to zero

#  fmov.s FRm,@Rn  = 1111 nnnn mmmm 1010.  Rn = r1 throughout.
ST = {n: (0xf10a | (n << 4)) for n in range(16)}


def instr(op, store_reg):
    """Pack the operation and the store into one 32-bit little-endian write."""
    return (ST[store_reg] << 16) | op


#  name, fpscr extra bits, register seed, packed instruction word, {mode: expected}
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

    # ---- PIN: double precision is mode-INDEPENDENT and must stay that way -----------
    #  The D format IS a host double, so the store is a pure re-encode with no narrowing
    #  for a mode to control; the rounding already happened in host arithmetic. This pin
    #  fails if someone "fixes" D by wiring the store, which would be a no-op, or breaks
    #  it by routing D through a rounding path it must not enter.
    #  1.0/10.0 low word: nearest 0x9999999a, and toward-zero WOULD be 0x99999999.
    ("PIN double 1.0/10.0 low", PR,
     {"fr0": 0x3ff00000, "fr1": 0x00000000,
      "fr2": 0x40240000, "fr3": 0x00000000},
     instr(0xf023, 1),                       # fdiv dr2,dr0 ; store fr1 = low half
     {RN: 0x9999999a, RZ: 0x9999999a}),

    # ---- PIN: the double-rounding limitation, recorded so it cannot drift silently --
    #  Every core evaluates in host double then narrows, so 1.0 - 2^-60 collapses to
    #  exactly 1.0 before the store. Real silicon rounds the exact difference and yields
    #  0x3f7fffff under toward-zero. Pre-existing, shared by all cores, NOT fixed by
    #  #296 -- pinned so that if it ever does get fixed, the gate says so out loud.
    ("PIN fsub 1.0-2^-60 dblround", 0,
     {"fr0": 0x3f800000, "fr1": 0x21800000},
     instr(0xf011, 0),                       # fsub fr1,fr0
     {RN: 0x3f800000, RZ: 0x3f800000}),
]


def run(fpscr, seed, word):
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
             "put w 0x%08x, 0x%08x" % (DEST, 0xdeadbeef),   # sentinel
             "put w 0x%08x, 0x%08x" % (CODE, word),
             "pc=0x%08x" % CODE,
             "step 2"]
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
for name, extra, seed, word, want in VECTORS:
    for mode, expect in sorted(want.items()):
        total += 1
        got = run(DN | extra | mode, seed, word)
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
# trusting that the table was written correctly.
discriminating = sum(1 for _, _, _, _, w in VECTORS if len(set(w.values())) > 1)
print("SH_ROUND_DISCRIMINATING=%d" % discriminating)
print("SH_ROUND_RESULT=%d/%d" % (passed, total))
