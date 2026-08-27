#!/usr/bin/env python3
"""RESEARCH probe for the #465 pass-2 opus seat.  NOT a shipping detector.

Drives the ONE route the shipped 13-row detector does not: the `:429`
sector_count-vs-cnt MISMATCH arm (post-fix numbering; `:415` pre-fix), which is
the arm `m_ret415` mutates.  The route is:

    stage_toc            -> alloc_data(408): data != NULL, data_len = 408,
                            tail sets COND_DATA_AVAIL and leaves cnt = 408
    COND = 0xa0 + 0x30 packet with sector_count = 1
                         -> handle_command: top release, then 1*2048 != 408,
                            so the ":429" arm runs (fatal "Huh?" then break)
    [optional COND = 0xef]
    LOAD GDROM_DATA      -> reaches :624 `cur_data_offset < data_len`

Reports HOW the process ended (sig11 = the NULL deref; exit0 = survived),
the value the load returned, whether the arm actually ran (ARM PROOF), and
whether the common tail ran (cnt readback: the tail zeroes cnt).
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
KERNEL = sys.argv[2] if len(sys.argv) > 2 else \
    "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images/openbsd76-landisk-bsd.rd"

CODE = 0x8c001000
SCRATCH = 0x8c001800
GDROM_DATA = 0xa05f7080
GDROM_CNTLO = 0xa05f7090
GDROM_CNTHI = 0xa05f7094
GDROM_COND = 0xa05f709c
SH4_IPRD = 0xffd00010
IPRD_RESET = 0xda74
LIVE = 0x12345678
BRA_SELF = 0xaffe
NOP = 0x0009

def MOVW_ST(n, m): return 0x2001 | (n << 8) | (m << 4)
def MOVW_LD(n, m): return 0x6001 | (n << 8) | (m << 4)
def MOVL_ST(n, m): return 0x2002 | (n << 8) | (m << 4)
def MOVL_LD(n, m): return 0x6002 | (n << 8) | (m << 4)

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-16s %-12s %-12s %-44s %s" % (name, got, want, note, "ok" if ok else "FAIL"))
    return ok

def session(cmds, settle=8.0, spin=2.0, step=0.30):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "dreamcast", "-M", "64", KERNEL])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.25)
            if not r: continue
            try: d = os.read(fd, 65536)
            except OSError: return False
            if not d: return False
            buf += d.decode("latin-1", "replace")
        return True
    alive = rd(settle)
    if alive:
        for i, c in enumerate(cmds):
            try: os.write(fd, (c + "\n").encode("latin-1"))
            except OSError:
                alive = False; break
            if not rd(spin if i == len(cmds) - 1 else step):
                alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.6)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat): how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat): how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError: pass
    return buf, alive, how

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\r?\n\s*(0x[0-9a-f]+)" % reg, t)
    return m.group(1) if m else "absent"

class Addr(object):
    def __init__(self, base): self.a = base
    def take(self):
        a = self.a; self.a += 0x40; return a

def run(ops, at):
    put = ["put h 0x%x, 0x%04x" % (at + 2 * i, op) for i, op in enumerate(ops)]
    put += ["put h 0x%x, 0x%04x" % (at + 2 * len(ops), BRA_SELF),
            "put h 0x%x, 0x%04x" % (at + 2 * len(ops) + 2, NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def store16(reg, val, A):
    return ["r7=0x%x" % reg, "r8=0x%04x" % val] + run([MOVW_ST(7, 8)], A.take())

def load16(reg, A, dest=2):
    return ["r1=0x%x" % reg, "r%d=0" % dest] + run([MOVW_LD(dest, 1)], A.take()) + \
           ["print r%d" % dest]

def packet(words, A):
    setup = ["r7=0x%x" % GDROM_DATA]
    for i, w in enumerate(words):
        setup.append("r%d=0x%04x" % (8 + i, w))
    return setup + run([MOVW_ST(7, 8 + i) for i in range(len(words))], A.take())

CMD_TOC = [0x0014] * 6
CMD_READ = [0x2030, 0x0000, 0x0000, 0x0000, 0x0000, 0x0001]

def stage_toc(A):
    return (store16(GDROM_CNTLO, 0x98, A) + store16(GDROM_CNTHI, 0x01, A) +
            store16(GDROM_COND, 0xa0, A) + packet(CMD_TOC, A))

def mism(A):
    """The :429 mismatch arm: cnt is 408 from the TOC, sector_count says 2048."""
    return store16(GDROM_COND, 0xa0, A) + packet(CMD_READ, A)

# ------------------------------------------------------------------ controls
A = Addr(CODE)
t, alive, how = session(["r7=0x%x" % SCRATCH, "r8=0x%08x" % LIVE,
                         "r1=0x%x" % SCRATCH, "r2=0"] +
                        run([MOVL_ST(7, 8), MOVL_LD(2, 1)], A.take()) + ["print r2"])
row("live", printed(t, "r2") if alive else "died", "0x%x" % LIVE,
    "LIVENESS: guest store then guest load, through RAM")

A = Addr(CODE)
t, alive, how = session(["r1=0x%x" % SH4_IPRD, "r2=0"] +
                        run([MOVL_LD(2, 1)], A.take()) + ["print r2"])
g = printed(t, "r2") if alive else "died"
row("devsig sh4", ("0x%x" % (int(g, 16) & 0xffff)) if g.startswith("0x") else g,
    "0x%x" % IPRD_RESET, "DEVSIG: SH4 IPRD reset value, RAM reads 0")

#  DEVICE SIGNATURE + the staging half of the route, on its own.
A = Addr(CODE)
t, alive, how = session(stage_toc(A) + ["r1=0x%x" % GDROM_DATA, "r2=0"] +
                        run([MOVW_LD(2, 1)], A.take()) + ["print r2"])
row("devsig toc", printed(t, "r2") if alive else "died", "0x10",
    "DEVSIG: synthesized TOC halfword 0, device-only value")

# ------------------------------------------------------------- the :429 route
#  (a) with the extra 0xef store, matching the shipped probe's idiom
A = Addr(CODE)
t1, a1, h1 = session(stage_toc(A) + mism(A) + store16(GDROM_COND, 0xef, A) +
                     load16(GDROM_DATA, A))
row("mism ef how", h1, "exit0", "TOC then MISMATCHED 0x30, +0xef, then LOAD")
row("mism ef val", printed(t1, "r2") if a1 else "died", "0xffffffff",
    "declined read returns 0xffff, sign-extended")
row("mism ef arm", "yes" if re.search(r"Huh\? GDROM data_len", t1) else "no", "yes",
    "ARM PROOF: the :427 Huh? diagnostic ran")

#  (b) WITHOUT the 0xef store.  If the mutant skips the tail, COND_DATA_AVAIL
#      survives from the TOC and no re-open store is needed at all.
A = Addr(CODE)
t2, a2, h2 = session(stage_toc(A) + mism(A) + load16(GDROM_DATA, A))
row("mism noef how", h2, "exit0", "SAME minus the 0xef re-open store")
row("mism noef val", printed(t2, "r2") if a2 else "died", "0xffffffff",
    "declined read returns 0xffff")

#  (c) TAIL-REACH channel: the tail zeroes cnt when data == NULL.  Reading
#      CNTHI back tells us whether the arm fell into the tail or bypassed it.
A = Addr(CODE)
t3, a3, h3 = session(stage_toc(A) + mism(A) + load16(GDROM_CNTHI, A, dest=3))
row("mism cnt post", printed(t3, "r3") if a3 else "died", "0x0",
    "TAIL-REACH: the tail zeroes cnt; 0x1 means it was bypassed")

n = sum(1 for _, ok in rows if ok)
print("MISM_RESULT=%d/%d" % (n, len(rows)))
print("MISM_VECTOR=" + ",".join(("1" if ok else "0") for _, ok in rows))
