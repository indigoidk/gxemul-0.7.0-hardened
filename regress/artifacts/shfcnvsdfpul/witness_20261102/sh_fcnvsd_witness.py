#!/usr/bin/env python3
"""shfcnvsdfpul -- RUNG-3 WITNESS: does the SuperH FCNVSD handler leave FPUL alone?

The SH-4 programming manual (section 9.29, _scratchpad/sh4_programming.txt:10866-10871) defines FCNVSD FPUL,DRn as
"(double) FPUL -> DRn": it READS FPUL and writes the register pair DRn.  X(fcnvsd_fpul_drn) in
src/cpus/cpu_sh_instr.c additionally stores `(int32_t) op1.f' into FPUL -- the truncated integer value of the
single-precision number -- so any guest that uses FPUL after an FCNVSD sees the wrong value.  The sibling
FCNVDS DRm,FPUL (9.28) is the instruction that DOES write FPUL, and it is the control here.

Shape: the cold debugger seeds fpscr (PR set), fpul and the DRn pair, writes real guest instructions at CODE,
single-steps them, and the guest itself moves the register under test into a sentinel word in RAM (`sts fpul,r2'
+ `mov.l r2,@r1', or `fmov.s frN,@r1'), read back with `dump'.  Machine: UNMODIFIED in-tree `-E landisk' with the
rig's kernel loaded so the machine constructs (never executed) -- the same shape as regress/sh_rounding_probe.py,
whose run() this file copies.  Little-endian: the dump word is reversed.

Rows:
  fpul 1.5      FCNVSD, then read FPUL        want 0x3fc00000 (unchanged)   HEAD predicted 0x00000001
  fpul -1.5     FCNVSD, then read FPUL        want 0xbfc00000               HEAD predicted 0xffffffff
  fpul 0.1      FCNVSD, then read FPUL        want 0x3dcccccd               HEAD predicted 0x00000000
  dr hi 1.5     FCNVSD, then read FR2 (hi)    want 0x3ff80000  LIVENESS: the conversion landed (both builds)
  dr lo 0.1     FCNVSD, then read FR3 (lo)    want 0xa0000000  LIVENESS: low half written, nonzero (both builds)
  fcnvds ctl    FCNVDS DR2,FPUL, read FPUL    want 0x3fc00000  CONTROL: the FPUL write channel is live where the
                                                               manual says write (both builds)
A row that fails with got == the HEAD-predicted truncation prints FAILED-FOR-THE-REASON-UNDER-TEST; any other
failure prints FAILED-FOR-SOME-OTHER-REASON and must not be claimed as the defect.

usage: sh_fcnvsd_witness.py <gxemul> <landisk kernel>
Sentinel: SH_FCNVSD_WITNESS_DONE
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
KERNEL = sys.argv[2]
CODE = 0x8c010000
DEST = 0x8c010100
DN = 0x00040000
PR = 0x00080000
RN = 0x0
SENT = 0xdeadbeef

#  16-bit SH-4 encodings (sh4_programming.txt:10866 FCNVSD 1111nnn010101101; :10754 FCNVDS 1111mmm010111101;
#  sts fpul,r2 = 0000 0010 0101 1010 = 0x025a; mov.l r2,@r1 = 0010 0001 0010 0010 = 0x2122; nop = 0x0009;
#  fmov.s FRm,@Rn = 1111 nnnn mmmm 1010 -> fmov.s fr2,@r1 = 0xf12a, fmov.s fr3,@r1 = 0xf13a)
FCNVSD_DR2 = 0xf2ad
FCNVDS_DR2 = 0xf2bd
STS_FPUL_R2 = 0x025a
MOVL_R2_AT_R1 = 0x2122
NOP = 0x0009
FMOVS_FR2 = 0xf12a
FMOVS_FR3 = 0xf13a


def pack(lo, hi):
    """two 16-bit instructions in one little-endian 32-bit word: `lo' executes first"""
    return (hi << 16) | lo


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

    def wait(timeout=40, mark=0, echo=None):
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

    def send(s):
        b = (s + "\n").encode("latin1")
        _mark = len(buf)
        n = 0
        while n < len(b):
            n += os.write(fd, b[n:])
        return wait(mark=_mark, echo=s if s else None)

    if not wait(90):
        try:
            os.kill(pid, 9); os.waitpid(pid, 0)
        except Exception:
            pass
        return None, buf
    cmds = ["fpscr=0x%08x" % fpscr]
    cmds += ["%s=0x%08x" % (k, v) for k, v in seed.items()]
    cmds += ["r1=0x%08x" % DEST, "put w 0x%08x, 0x%08x" % (DEST, SENT)]
    cmds += ["put w 0x%08x, 0x%08x" % (CODE, word)]
    if word2 is not None:
        cmds += ["put w 0x%08x, 0x%08x" % (CODE + 4, word2)]
    cmds += ["pc=0x%08x" % CODE, "step %d" % (3 if word2 is not None else 2)]
    for c in cmds:
        send(c)
    mark = len(buf)
    send("dump 0x%08x 0x%08x" % (DEST, DEST + 4))
    tail = buf[mark:]
    try:
        os.write(fd, b"quit\n"); time.sleep(0.4); os.kill(pid, 9); os.waitpid(pid, 0)
    except Exception:
        pass
    m = re.search(r"0x0*%x\s+([0-9a-f]{8})" % DEST, tail)
    if not m:
        return None, buf
    return int.from_bytes(bytes.fromhex(m.group(1)), "little"), buf


#  (name, seeds, first word, second word, want, HEAD-predicted wrong value or None, role)
FP_RD = pack(FCNVSD_DR2, STS_FPUL_R2)          # fcnvsd fpul,dr2 ; sts fpul,r2
STORE = pack(MOVL_R2_AT_R1, NOP)               # mov.l r2,@r1 ; nop
ROWS = [
    ("fpul 1.5",   {"fpul": 0x3fc00000, "fr2": SENT, "fr3": SENT}, FP_RD, STORE, 0x3fc00000, 0x00000001, "DEFECT"),
    ("fpul -1.5",  {"fpul": 0xbfc00000, "fr2": SENT, "fr3": SENT}, FP_RD, STORE, 0xbfc00000, 0xffffffff, "DEFECT"),
    ("fpul 0.1",   {"fpul": 0x3dcccccd, "fr2": SENT, "fr3": SENT}, FP_RD, STORE, 0x3dcccccd, 0x00000000, "DEFECT"),
    ("dr hi 1.5",  {"fpul": 0x3fc00000, "fr2": SENT, "fr3": SENT}, pack(FCNVSD_DR2, FMOVS_FR2), None, 0x3ff80000, None, "LIVENESS"),
    ("dr lo 0.1",  {"fpul": 0x3dcccccd, "fr2": SENT, "fr3": SENT}, pack(FCNVSD_DR2, FMOVS_FR3), None, 0xa0000000, None, "LIVENESS"),
    ("fcnvds ctl", {"fpul": SENT, "fr2": 0x3ff80000, "fr3": 0x00000000}, pack(FCNVDS_DR2, STS_FPUL_R2), STORE, 0x3fc00000, None, "CONTROL"),
]

print("shfcnvsdfpul RUNG-3 WITNESS -- binary=%s" % BIN)
print("machine: -E landisk -M 64 (UNMODIFIED in-tree), kernel loaded for construction only; fpscr = DN|PR|RN")
print("%-12s %-10s %-10s %-9s %s" % ("row", "got", "want", "role", "verdict"))
ok = 0
for name, seed, w1, w2, want, headpred, role in ROWS:
    got, transcript = run(DN | PR | RN, seed, w1, w2)
    if got is None:
        print("%-12s %-10s 0x%08x %-9s FAILED-FOR-SOME-OTHER-REASON (no readback; transcript tail: %r)"
              % (name, "None", want, role, transcript[-160:]))
        continue
    if got == want:
        ok += 1; verdict = "ok"
    elif headpred is not None and got == headpred:
        verdict = "FAILED-FOR-THE-REASON-UNDER-TEST (FPUL holds the truncated integer the handler stores)"
    elif got == SENT:
        verdict = "FAILED-FOR-SOME-OTHER-REASON (sentinel untouched: the guest store never ran)"
    else:
        verdict = "FAILED-FOR-SOME-OTHER-REASON (unexpected value)"
    print("%-12s 0x%08x 0x%08x %-9s %s" % (name, got, want, role, verdict))
print("RESULT=%d/%d" % (ok, len(ROWS)))
print("SH_FCNVSD_WITNESS_DONE")
