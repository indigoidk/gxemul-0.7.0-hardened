#!/usr/bin/env python3
"""Gate 12 section 3's instrument: #295's forced rounding modes, on real guest code.

#295 made round.w/ceil.w/floor.w force their architectural modes (nearest-even,
+Inf, -Inf) instead of inheriting FCSR.RM. The likeliest wrong edit -- a copy-paste
of cvt.w's FPU_RM_FROM_FCSR -- EQUALS the correct code whenever FCSR.RM is 0 (the
reset default), so a reverting mutant passes any row that leaves FCSR alone. Every
discriminating row here therefore sets a NON-ZERO FCSR.RM via guest ctc1, chosen so
the directed-mode answer differs from the forced-mode answer (a row where they agree
is born vacuous -- two such rows were caught at design time and re-moded).

Prints, per row:   M295_ROW=<rig>:<name> RESULT=PASS|FAIL got=<hex> want=<hex>
then per rig:      M295_CONTROL=<rig>:OK|DEAD
and finally:       M295_RESULT=<passed>/<total>
gate_mips_rounding.sh asserts the fixed strings; selftest_mutation_295.sh asserts
the flip matrix. Fixed-string lines on purpose: the padded-column `^name .*ok$`
pattern has already produced both a double-match and an unsatisfiable row here.

Row classes (the mutation self-test treats them differently):
* must-flip (9): round x5 (incl. the -2147483648.5 boundary row: the fix's RN answer
  -2^31 is IN range -- float_emul.c's W guard is deliberately <= -2147483649.0 --
  while the mutant's floor answer -2^31-1 is out of range and saturates to
  0x7fffffff), ceil x2, floor x2. Each flips under exactly its op's mutant.
* controls (5, must-pass, exempt from flipping -- they CANNOT flip by construction):
  - cvt27rm: cvt.w.d consumes FCSR via FPU_RM_FROM_FCSR (cpu_mips_coproc.c:1794),
    so this row is the witness that the guest ctc1 LANDED: a dead FCSR write reads
    the RN answer 3, not the RM answer 2. The trunc rows cannot witness this --
    trunc is mode-immune in every state (a design-time label said otherwise; five
    review seats corrected it).
  - cfc1: direct FCSR readback ($t0 is clobbered to 0x55 between ctc1 and cfc1, so
    a no-op cfc1 cannot false-pass by leaving the written value in place).
  - trunc x2: trunc-wiring contrast (trunc still forces RZ; kills a hypothetical
    trunc->FROM_FCSR revert, which no other row would).
  - nan: result pin -- R4000 B-49: unenabled Invalid returns 2^31-1. Asserts the
    RESULT word, never FCSR flags (flag bits are a recorded deferred item). The
    operand uses the tree's legacy-MIPS QUIET convention (fraction MSB clear,
    cpu_mips_coproc.c #255 block), not the host 0x7ff8... pattern.

Measurement facts inherited from mips_rounding_probe.py (each cost a failed run):
* FPRs are not debugger-settable; the guest loads its own operand and sets FCSR
  itself with ctc1 (proving the mode arrives as a real guest sends it).
* pmax is MIPS-I: ldc1 raises RI, so the double is loaded as the $f0/$f1 pair with
  two lwc1 (FR=0 layout: low word in $f0). The W result is read back with swc1,
  never sdc1 -- sdc1 is itself MIPS-II and its RI is mistakable for the op under
  test (#273).
* A fresh emulator per row: no state survives between rows, and $f2 is ALSO
  explicitly poisoned from the 0xdeadbeef result-slot seed before the op, so an op
  that faults stores the seed -- "stored nothing" and "op never ran" are the same
  distinguishable token, by construction rather than by reset-value luck.
* The dump parse is BOUND to the requested address (a committed sibling probe
  accepts any dump-shaped line; that is queue item #56, not repeated here).

Encodings: pinned constants below are asserted against the helper-built words at
import time, and were verified through the debugger's own unassemble on both rigs
before commit (a wrong register field yields a value some sentinel row would
accept; four past incidents).
"""
import os
import pty
import re
import select
import struct
import sys
import time

BIN = sys.argv[1]
PMAX_KERNEL = sys.argv[2]
ARC_KERNEL = sys.argv[3]
ONLY = sys.argv[4] if len(sys.argv) > 4 else "both"   # pmax | arc | both

CODE = 0xffffffff80020000
SRC = 0xffffffff80021000
OUT = SRC + 8                       # result slot (seeded 0xdeadbeef)

RN, RZ, RP, RM = 0, 1, 2, 3


def dbits(x):
    return struct.unpack("<Q", struct.pack("<d", x))[0]


def cop1(fmt, ft, fs, fd, func):
    return (0x11 << 26) | (fmt << 21) | (ft << 16) | (fs << 11) | (fd << 6) | func


ROUND_W = cop1(0x11, 0, 0, 2, 0x0c)
TRUNC_W = cop1(0x11, 0, 0, 2, 0x0d)
CEIL_W = cop1(0x11, 0, 0, 2, 0x0e)
FLOOR_W = cop1(0x11, 0, 0, 2, 0x0f)
CVT_W = cop1(0x11, 0, 0, 2, 0x24)
CTC1_T0_F31 = 0x44c8f800            # ctc1 t0, fcr31
CFC1_T0_F31 = (0x11 << 26) | (2 << 21) | (8 << 16) | (31 << 11)
ORI_T0_55 = 0x34080055              # ori t0, zero, 0x55 (clobber between ctc1/cfc1)
SW_T0 = 0xad280008                  # sw   t0, 8(t1)
LWC1_F0 = 0xc5200000                # lwc1 f0, 0(t1)
LWC1_F1 = 0xc5210004                # lwc1 f1, 4(t1)
LWC1_F2 = 0xc5220008                # poison f2 from the seeded result slot
LDC1_F0 = 0xd5200000                # arc only: MIPS II
SWC1_F2 = 0xe5220008                # swc1 f2, 8(t1)

#  Self-assert the helper-built words against the pinned constants: a drifting
#  helper otherwise tests a different instruction silently.
assert ROUND_W == 0x4620008c and TRUNC_W == 0x4620008d
assert CEIL_W == 0x4620008e and FLOOR_W == 0x4620008f
#  0x462000a4, NOT 0x46200024: the func field 0x24 sits in bits 5:0 and fd in
#  bits 10:6 -- the wrong constant disassembles as cvt.w.d r0,r0 (fd=0), which
#  overwrites the operand and never writes $f2. Caught by unassemble showing the
#  REGISTERS, not just the mnemonic, at design time (the fifth encoding incident).
assert CVT_W == 0x462000a4 and CFC1_T0_F31 == 0x4448f800

#  Legacy-MIPS quiet NaN (fraction MSB clear -- see the #255 canonicalization
#  block); the conventional host 0x7ff8... qNaN is a SIGNALING pattern here.
QNAN_BITS = 0x7ff7ffffffffffff

#  name, instr, operand bits, FCSR.RM, expected W bits, class
#  Every FCSR value is RM-only (<= 3): trap-enable bits stay clear on purpose --
#  an enabled Invalid would turn the nan row into a trap instead of a result.
ROWS = [
    ("r25rp",   ROUND_W, dbits(2.5),    RP, 0x00000002, "flip"),  # ties-to-EVEN
    ("r35rm",   ROUND_W, dbits(3.5),    RM, 0x00000004, "flip"),  # (2.5 kills
    ("r27rm",   ROUND_W, dbits(2.7),    RM, 0x00000003, "flip"),  #  ties-away;
    ("rn25rm",  ROUND_W, dbits(-2.5),   RM, 0xfffffffe, "flip"),  #  3.5 kills RZ)
    ("rbnd",    ROUND_W, dbits(-2147483648.5), RM, 0x80000000, "flip"),
    ("c21rm",   CEIL_W,  dbits(2.1),    RM, 0x00000003, "flip"),
    ("cn225rm", CEIL_W,  dbits(-2.25),  RM, 0xfffffffe, "flip"),
    ("f29rp",   FLOOR_W, dbits(2.9),    RP, 0x00000002, "flip"),
    ("fn225rp", FLOOR_W, dbits(-2.25),  RP, 0xfffffffd, "flip"),
    ("cvt27rm", CVT_W,   dbits(2.7),    RM, 0x00000002, "ctrl"),  # ctc1 witness
    ("cfc1",    None,    None,          RM, 0x00000003, "ctrl"),  # FCSR readback
    ("t35rp",   TRUNC_W, dbits(3.5),    RP, 0x00000003, "ctrl"),
    ("tn35rm",  TRUNC_W, dbits(-3.5),   RM, 0xfffffffd, "ctrl"),
    ("nan",     ROUND_W, QNAN_BITS,     RM, 0x7fffffff, "ctrl"),
]

RIGS = [
    #  rig,   -e machine, status (CU1 [| FR]),  kernel,     pair-load doubles
    ("pmax", "3max", 0x20000000, PMAX_KERNEL, True),
    ("arc",  "pica", 0x24000000, ARC_KERNEL, False),
]


def build(instr, fcsr, pair_load):
    """lui/ori t0=mode; ctc1; lui/ori t1=SRC; load f0[/f1]; poison f2; op; swc1."""
    w = [
        0x3c080000,                             # lui t0, 0
        0x35080000 | (fcsr & 0xffff),           # ori t0, t0, fcsr
        CTC1_T0_F31,
        0x3c090000 | ((SRC >> 16) & 0xffff),    # lui t1, hi (sign-extends to kseg0)
        0x35290000 | (SRC & 0xffff),            # ori t1, t1, lo
    ]
    if instr is None:                           # the cfc1 readback row
        return w + [ORI_T0_55, CFC1_T0_F31, SW_T0]
    w += [LWC1_F0, LWC1_F1] if pair_load else [LDC1_F0]
    return w + [LWC1_F2, instr, SWC1_F2]


def run(machine, status, kernel, instr, opbits, fcsr, pair_load):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-e", machine, "-M", "64", kernel])
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

    def wait(timeout=60):
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

    if not wait(150):
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    send("status=0x%08x" % status)
    if opbits is not None:
        u = opbits & 0xffffffffffffffff
        send("put w 0x%x, 0x%08x" % (SRC, u & 0xffffffff))        # LOW word first
        send("put w 0x%x, 0x%08x" % (SRC + 4, (u >> 32) & 0xffffffff))
    send("put w 0x%x, 0xdeadbeef" % OUT)
    words = build(instr, fcsr, pair_load)
    for i, w in enumerate(words):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w & 0xffffffff))
    send("pc=0x%x" % CODE)
    send("step %d" % len(words))

    #  Retry the READ, never the row. The parse is BOUND to the dump line's
    #  address (any dump-shaped line would otherwise do -- see #56). Measured
    #  format on both rigs: the line address is ALIGNED DOWN to 16 bytes and
    #  TRUNCATED to 32 bits (`0x80021000  ...`), and only the words inside the
    #  requested range are printed (out-of-range slots render as blank columns),
    #  so for a dump of exactly [OUT, OUT+8) the FIRST hex word on the bound
    #  line is OUT's value, in MEMORY order.
    addr_tail = "%x" % ((OUT & 0xffffffff) & ~0xf)
    val = None
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (OUT, OUT + 8))
        for line in buf[mark:].splitlines():
            m = re.match(r"\s*0x[0-9a-f]*" + addr_tail +
                         r"\s+((?:[0-9a-f]{8}\s*)+)", line)
            if m:
                raw = bytes.fromhex(m.group(1).split()[0])   # 4 bytes, memory order
                val = int.from_bytes(raw, "little")
                break
        if val is not None:
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit\n")
        time.sleep(0.4)
        os.kill(pid, 9)
        os.waitpid(pid, 0)
    except Exception:
        pass
    return val


passed = total = 0
for rig, machine, status, kernel, pair in RIGS:
    if ONLY != "both" and ONLY != rig:
        continue
    ctrl_ok = True
    for name, instr, opbits, fcsr, want, cls in ROWS:
        total += 1
        got = run(machine, status, kernel, instr, opbits, fcsr, pair)
        ok = (got == want)
        passed += ok
        if cls == "ctrl" and name in ("cvt27rm", "cfc1") and not ok:
            ctrl_ok = False
        print("M295_ROW=%s:%s RESULT=%s got=%s want=%08x" % (
            rig, name, "PASS" if ok else "FAIL",
            ("%08x" % got) if got is not None else "None", want))
    #  DEAD when the ctc1 witness pair fails: if FCSR writes are not landing,
    #  no discriminating row on a GOOD binary proves anything (they are all
    #  FCSR-independent on the fix), so the section must not be believed.
    print("M295_CONTROL=%s:%s" % (rig, "OK" if ctrl_ok else "DEAD"))

print("M295_RESULT=%d/%d" % (passed, total))
