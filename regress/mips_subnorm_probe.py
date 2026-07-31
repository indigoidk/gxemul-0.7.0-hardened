#!/usr/bin/env python3
"""Gate 12's second instrument: #303 subnormal-operand decode on BOTH MIPS rigs.

Prints one line per row plus MIPS_SUBN_RESULT=<passed>/<total>.

Why pmax rows exist at all
--------------------------
#246 gates denormal operands behind fpu_unimpl_trap() -- but that function
returns 0 for EXC3K (the R3010 signals via an external interrupt pin the
emulated machines do not wire), so on pmax/R3000 the gate falls through and the
DECODED value is consumed. Two panel seats refuted the "MIPS is fully masked"
claim and the rig agreed: before #303 the mul.s row measured 0x32000001 (the
garbled decode), cvt.d.s measured 3800000020000000, and the flip row 0x00800001.
pmax is therefore a fourth REAL-victim architecture and these rows are
DISCRIMINATORS. arc/R4000 keeps the trap: its row proves the sentinel survives
(the store never runs) -- the no-change control for #246 itself.

The flip row is a pinned KNOWN-CHANGE and runs on the NEGATIVE operand: the
true sum of two -S-min subnormals is -2^-148, subnormal, so the deliberate
#287/#292 store flush answers MINUS zero (0x80000000) -- the sign survives
because #287 fixed exactly that. A #303 revert trips it (the garble lands
S-normal: the positive twin measured 0x00800001 pre-fix, the negative one is
the same path with the sign applied at the end), and a #287 revert trips it
too (the old store LOST the sign: +0, not -0). A POSITIVE flip row could not
see a #287 revert at all -- +0 is +0 under both stores -- which is why this
row is negative (a diff-review seat's finding). The guest still observes
x != 0 but x + x == 0: the interim half-state the queued store-side round
inherits.

Probe facts (mirrors mips_rounding_probe.py): put w + dump work on RAM; both
rigs are little-endian (dump renders memory order -- bytes reversed on read);
status is a debugger SETTING (CU1 = 0x20000000; R3000 has no FR bit);
FPRs are not debugger-settable, so operands go through guest lwc1; COP1 fd
lives at bits 10:6 (cvt.d.s f4,f0 = 0x46000121; add.s f4,f0,f0 = 0x46000100;
mul.s f4,f0,f2 = 0x46020102). R3000 FR=0 pairs f4:f5 with f4 = LOW word (LE).
"""
import os
import pty
import re
import select
import sys
import time

BIN = sys.argv[1]
PMAX_KERNEL = sys.argv[2]
ARC_KERNEL = sys.argv[3]
CODE = 0xffffffff80020000
SRC = 0xffffffff80021000


def run(machine, kernel, status, src0, words, nread):
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
    send("put w 0x%x, 0x%08x" % (SRC, src0))      # first operand (per row)
    send("put w 0x%x, 0x71800000" % (SRC + 4))    # 2^100
    send("put w 0x%x, 0xdeadbeef" % (SRC + 8))    # sentinel
    send("put w 0x%x, 0xdeadbeef" % (SRC + 12))
    full = [0x3c090000 | ((SRC >> 16) & 0xffff),
            0x35290000 | (SRC & 0xffff)] + words
    for i, w in enumerate(full):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w & 0xffffffff))
    send("pc=0x%x" % CODE)
    send("step %d" % len(full))
    vals = None
    #  Retry the READ, never the row (the value cannot change between dumps).
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (SRC + 8, SRC + 16))
        tail = buf[mark:]
        wordshex = re.findall(
            r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})", tail)
        flat = "".join(wordshex).split()
        if len(flat) >= nread:
            vals = ["%08x" % int.from_bytes(bytes.fromhex(f), "little")
                    for f in flat[:nread]]
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
    return vals



#  #309: an unimplemented REGIMM sub-opcode must raise Reserved Instruction,
#  not stop the machine. The witness is therefore not a register value but
#  WHICH OUTCOME the session reaches: the emulator prints "exception RI" and
#  keeps running, where before it printed "UNIMPLEMENTED instruction" and set
#  cpu->running = 0. Both rigs run the row -- the arm is CPU-independent, and
#  a fix that reached only one dyntrans mode would pass a single-rig gate.
def run_regimm(machine, kernel, status, iword, nstep=1):
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

    def send(x):
        b = (x + chr(10)).encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait()

    if not wait(150):
        try:
            os.kill(pid, 9); os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    send("status=0x%08x" % status)
    send("put w 0x%x, 0x%08x" % (CODE, iword))
    #  A delay slot the branch control needs, and harmless to the RI rows.
    send("put w 0x%x, 0x00000000" % (CODE + 4))
    send("pc=0x%x" % CODE)
    mark = len(buf)
    send("step %d" % nstep)
    tail = buf[mark:]

    #  Read the PC back, so a branch row has a witness beyond "did not fault".
    pc = None
    for _ in range(2):
        mark2 = len(buf)
        send("reg")
        m = re.search(r"\bpc\s*=\s*0x([0-9a-f]+)", buf[mark2:])
        if m:
            pc = int(m.group(1), 16) & 0xffffffff
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit" + bytes([10]))
        time.sleep(0.4)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass

    #  Every outcome is named. The first version returned a catch-all
    #  "ran-no-exception" for anything that was not exactly RI or a halt, so a
    #  timeout, an EOF or a DIFFERENT exception all scored as success -- a
    #  diff-review seat's finding, and the same class of defect this gate
    #  exists to catch in the emulator.
    if "All machines stopped" in tail or "UNIMPLEMENTED instruction" in tail:
        return "halted"
    if "exception RI" in tail:
        return "RI"
    if "exception" in tail:
        return "other-exception"
    if pc is None:
        return "no-pc-readback"
    return "pc=0x%08x" % pc



def run_branch_control(machine, kernel, status):
    """Prove BGEZ actually BRANCHES, through the dump channel both rigs share.

    The first version of this control asserted "did not fault", which a nop
    would have satisfied, and then a PC readback, which parses reliably on arc
    but not on pmax. So the guest writes its own witness instead: two stores
    to the same address, one on the fall-through path and one at the branch
    target. Taken -> 0x22222222; not taken -> 0x11111111; nothing ran -> the
    sentinel survives. Three outcomes, all distinguishable, no PC parsing.

      lui/ori r9  = the witness address
      lui/ori r8  = 0x11111111   (fall-through marker)
      lui/ori r10 = 0x22222222   (target marker)
      bgez r0,+2  -- r0 >= 0 always, target = branch + 4 + 8
      nop         -- the delay slot, which executes either way
      sw r8,0(r9) -- skipped when the branch is taken
      sw r10,0(r9)-- the branch target
    """
    addr = SRC + 16
    words = [0x3c090000 | ((addr >> 16) & 0xffff),
             0x35290000 | (addr & 0xffff),
             0x3c081111, 0x35081111,
             0x3c0a2222, 0x354a2222,
             0x04010002,          # bgez r0, +2
             0x00000000,          # delay slot
             0xad280000,          # sw r8,0(r9)   -- fall-through
             0xad2a0000]          # sw r10,0(r9)  -- branch target
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

    def send(x):
        b = (x + chr(10)).encode("latin1")
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        wait()

    if not wait(150):
        try:
            os.kill(pid, 9); os.waitpid(pid, 0)
        except Exception:
            pass
        return None

    send("status=0x%08x" % status)
    send("put w 0x%x, 0xdeadbeef" % addr)
    for i, w in enumerate(words):
        send("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    send("pc=0x%x" % CODE)
    send("step %d" % len(words))
    val = None
    for _ in range(3):
        mark = len(buf)
        send("dump 0x%x 0x%x" % (addr, addr + 4))
        hits = re.findall(r"0x0*[0-9a-f]+\s+((?:[0-9a-f]{8}\s+){1,4})",
                          buf[mark:])
        flat = "".join(hits).split()
        if flat:
            val = "%08x" % int.from_bytes(bytes.fromhex(flat[0]), "little")
            break
        time.sleep(1.0)
        rd(1.0)
    try:
        os.write(fd, b"quit" + bytes([10]))
        time.sleep(0.4)
        os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    if val is None:
        return "no-readback"
    if val == "22222222":
        return "branched"
    if val == "11111111":
        return "fell-through"
    return "marker=" + val


#  name, machine, status, instruction word, expected outcome
#  REGIMM is opcode 0x01; rt selects the sub-opcode. 0x15 is in the
#  unimplemented range (4-7, 0xd, 0xf, 0x14-0x17, 0x1a-0x1e); 0x01 is BGEZ,
#  the control that must still execute as a branch rather than fault.
REGIMM_ROWS = [
    ("pmax regimm rt=0x15", "3max", 0x20000000, 0x04150000, 1, "RI"),
    ("arc regimm rt=0x15",  "pica", 0x24000000, 0x04150000, 1, "RI"),
    ("pmax regimm rt=0x1e", "3max", 0x20000000, 0x041e0000, 1, "RI"),
]

#  The branch controls, which prove an IMPLEMENTED REGIMM sub-opcode still
#  works -- and prove it by branching, not merely by not faulting.
BRANCH_ROWS = [
    ("pmax BGEZ control", "3max", 0x20000000, "branched"),
    ("arc BGEZ control",  "pica", 0x24000000, "branched"),
]


#  name, machine, status, first-operand word, guest words (after the lui/ori
#  prelude), reads, want
ROWS = [
    #  pmax discriminators: pre-#303 measured 32000001 / 20000000:38000000.
    ("pmax mul.s subn",  "3max", 0x20000000, 0x00000001,
     [0xc5200000, 0xc5220004, 0x46020102, 0xe5240008], 1, ["27000000"]),
    ("pmax cvt.d.s subn", "3max", 0x20000000, 0x00000001,
     [0xc5200000, 0x46000121, 0xe5240008, 0xe525000c], 2,
     ["00000000", "36a00000"]),
    #  the pinned KNOWN-CHANGE flip row, NEGATIVE operand (see above): -S-min +
    #  -S-min -> true -2^-148 -> store flush KEEPS the sign -> -0. Positive twin
    #  measured 00800001 pre-#303.
    ("pmax add.s flip",  "3max", 0x20000000, 0x80000001,
     [0xc5200000, 0x46000100, 0xe5240008], 1, ["80000000"]),
    #  arc control: sw r9,12(r9) (0xad29000c, an INTEGER store) executes FIRST
    #  and writes r9's low word -- the execution witness -- then the #246 trap
    #  fires on mul.s, the pc leaves, swc1 never runs, the sentinel at +8
    #  survives. want = [sentinel, marker]: a dead session shows [deadbeef,
    #  deadbeef] and FAILS on the marker.
    ("arc mul.s trap",   "pica", 0x24000000, 0x00000001,
     [0xc5200000, 0xc5220004, 0xad29000c, 0x46020102, 0xe5240008], 2,
     ["deadbeef", "80021000"]),
]

passed = 0
for name, machine, status, src0, words, nread, want in ROWS:
    kernel = PMAX_KERNEL if machine == "3max" else ARC_KERNEL
    got = run(machine, kernel, status, src0, words, nread)
    ok = got == want
    passed += ok
    print("%-19s got %s want %s %s" %
          (name, got, want, "ok" if ok else "FAIL"))
for name, machine, status, iword, nstep, want in REGIMM_ROWS:
    kernel = PMAX_KERNEL if machine == "3max" else ARC_KERNEL
    got = run_regimm(machine, kernel, status, iword, nstep)
    ok = got == want
    passed += ok
    print("%-19s got %-18s want %-18s %s" %
          (name, got, want, "ok" if ok else "FAIL"))

for name, machine, status, want in BRANCH_ROWS:
    kernel = PMAX_KERNEL if machine == "3max" else ARC_KERNEL
    got = run_branch_control(machine, kernel, status)
    ok = got == want
    passed += ok
    print("%-19s got %-18s want %-18s %s" %
          (name, got, want, "ok" if ok else "FAIL"))
print("MIPS_SUBN_RESULT=%d/%d" %
      (passed, len(ROWS) + len(REGIMM_ROWS) + len(BRANCH_ROWS)))
