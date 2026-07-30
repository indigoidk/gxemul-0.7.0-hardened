#!/usr/bin/env python3
"""Gate 12's measuring instrument: MIPS cvt.d.l and cvt.s.l rounding, on real guest code.

Prints one line per row:  <name> <got> <want> ok|FAIL
then MIPS_CVT_RESULT=<passed>/<total>. gate_mips_rounding.sh does the asserting.

Machine and scope
-----------------
arc (Acer PICA, R4400) ONLY: cvt.d.l is MIPS-III+, and the pmax R3000 raises a
Reserved Instruction exception on the ldc1 -- measured, which is why this gate does not
run there and why #301's blast radius is R4000+ machines.

How it measures (each fact below cost a failed run; do not relearn them)
------------------------------------------------------------------------
* MIPS FPRs are NOT debugger-settable. The guest loads its own operand with ldc1 from
  debugger-written memory, and sets FCSR itself with ctc1 -- which also proves the mode
  arrives the way a real guest sends it, not via a debugger side door.
* The arc rig is LITTLE-endian: `put w` takes a value but `dump` renders bytes in
  MEMORY order, so the int64 operand is written LOW word first and the result bytes are
  reversed on read.
* COP1 R-format puts fd at bits 10:6. cvt.d.l $f2,$f0 is 0x46a000a1: 0x46a00021
  (fd field misplaced) is cvt.d.l r0,r0 which overwrites the operand, and 0x46a00081
  (function bit dropped) is sub.l -- both were built and both measured garbage.
* `status=0x24000000` (CU1|FR) is a debugger SETTING; bare `status` is not a command.

The control row is LOAD-BEARING: if the small-integer nearest row is wrong, the probe
measured nothing and no other row may be believed. The first version of this probe
reported REPRODUCED off six sentinel reads while its guest code had never run.
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
KERNEL = sys.argv[2]
CODE = 0xffffffff80020000
SRC = 0xffffffff80021000

RN, RZ, RP, RM = 0, 1, 2, 3

#  name, int64 operand, FCSR mode, expected double bits
ROWS = [
    #  control: exact conversion, mode irrelevant -- must be RIGHT or the probe is dead
    ("control 5 RN",  5,                    RN, "4014000000000000"),
    #  2^53+1: the first integer that needs a rounding decision
    ("2^53+1 RP",     0x0020000000000001,   RP, "4340000000000001"),
    ("2^53+1 RN",     0x0020000000000001,   RN, "4340000000000000"),
    ("2^53+1 RM",     0x0020000000000001,   RM, "4340000000000000"),
    #  2^54+7: a multi-bit tail
    ("2^54+7 RZ",     0x0040000000000007,   RZ, "4350000000000001"),
    ("2^54+7 RP",     0x0040000000000007,   RP, "4350000000000002"),
    #  negative: toward-zero truncates toward zero, not toward -Inf
    ("-(2^54+7) RZ",  -0x0040000000000007,  RZ, "c350000000000001"),
    ("-(2^54+7) RM",  -0x0040000000000007,  RM, "c350000000000002"),
    #  a genuine tie, odd lower neighbour: ties-to-even goes UP
    ("2^54+6 RN tie", 0x0040000000000006,   RN, "4350000000000002"),
    #  cvt.s.l (the L->S half): the double-tie witness. Pre-fix this tied down TWICE
    #  through the host double and read 5a800000; direct rounding owes 5a800001. The
    #  row is single-precision: the probe swaps in cvt.s.l + swc1 for it.
    ("SL dbltie RN",  0x0040000040000002,   RN, "5a800001"),
    #  FR=0: every other row runs with Status.FR set, so the 32-bit-FPU pair-assembly
    #  path that feeds (int64_t)fs_v had no end-to-end measurement -- it rested on
    #  reading the code, and this project's history is precisely about reading versus
    #  measuring (a #301 panel seat's finding). Same witness, FR clear.
    ("FR0 2^53+1 RP", 0x0020000000000001,   RP, "4340000000000001"),
]


def build(fcsr, single=False):
    """lui/ori t0=mode; ctc1; lui/ori t1=SRC; ldc1 f0; cvt f2,f0; store f2.
    single=True swaps in cvt.s.l (0x46a000a0) and swc1 (0xe5220008)."""
    return [
        0x3c080000 | ((fcsr >> 16) & 0xffff),
        0x35080000 | (fcsr & 0xffff),
        0x44c8f800,
        0x3c090000 | ((SRC >> 16) & 0xffff),
        0x35290000 | (SRC & 0xffff),
        0xd5200000,
        0x46a000a0 if single else 0x46a000a1,
        0xe5220008 if single else 0xf5220008,
    ]


def run(intbits, fcsr, single=False, fr=True):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp(BIN, [BIN, "-V", "-e", "pica", "-M", "64", KERNEL])
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

    u = intbits & 0xffffffffffffffff
    #  CU1 always; FR only when the row wants 64-bit FPU register mode.
    send("status=0x%08x" % (0x24000000 if fr else 0x20000000))
    send("put w 0x%x, 0x%08x" % (SRC, u & 0xffffffff))            # LOW word first (LE)
    send("put w 0x%x, 0x%08x" % (SRC + 4, (u >> 32) & 0xffffffff))
    send("put w 0x%x, 0xdeadbeef" % (SRC + 8))
    send("put w 0x%x, 0xdeadbeef" % (SRC + 12))
    for i, w in enumerate(build(fcsr, single)):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w & 0xffffffff))
    send("pc=0x%x" % CODE)
    send("step 8")

    #  Retry the READ, never the row (a dump can straggle past the prompt detector
    #  under host load; the value cannot change between two dumps).
    val = None
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (SRC + 8, SRC + 16))
        tail = buf[mark:]
        words = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", tail)
        flat = "".join(words).split()
        if len(flat) >= (1 if single else 2):
            if single:
                raw = bytes.fromhex(flat[0])            # 4 bytes, memory order
                val = "%08x" % int.from_bytes(raw, "little")
            else:
                raw = bytes.fromhex(flat[0] + flat[1])  # 8 bytes, memory order
                val = "%016x" % int.from_bytes(raw, "little")
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
results = {}
for name, v, mode, want in ROWS:
    total += 1
    got = run(v, mode, single=name.startswith("SL "),
              fr=not name.startswith("FR0 "))
    results[name] = got
    ok = (got == want)
    passed += ok
    print("%-16s %-18s %s %s"
          % (name, got if got is not None else "None", want, "ok" if ok else "FAIL"))

if results.get("control 5 RN") != "4014000000000000":
    print("MIPS_CVT_CONTROL=DEAD")
else:
    print("MIPS_CVT_CONTROL=OK")
print("MIPS_CVT_RESULT=%d/%d" % (passed, total))
