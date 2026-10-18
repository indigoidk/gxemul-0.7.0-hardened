#!/usr/bin/env python3
#
#  sgirekills -- RUNG-3 WITNESS (2026-10-17): five guest-drivable host kills in dev_sgi_re.c's
#  do_mte_transfer(), each reached by REAL GUEST STORES through real address decode and real
#  memory_rw on the unmodified `-E sgi -e ip32' machine.
#
#      :1496  if (mode & MTE_MODE_STIPPLE)          { fatal(...STIPPLE...);    exit(1); }
#      :1504  if (src > MTE_TLB_C)                  { fatal(...SRC...);        exit(1); }
#      :1580  [LIN_A/B] if (mode & MTE_MODE_COPY)   { fatal(...COPY...);       exit(1); }
#      :1585  [LIN_A/B] if (depth != 8)             { fatal(...DEPTH_x...);    exit(1); }
#      :1596  [LIN_A/B] if (bytemask != 0xffffffff) { fatal(...bytemask...);  exit(1); }
#
#  (A sixth `exit(1)' at :1720, the sgi_mte handler's width arm, sits under `if (len == 4) ...
#  else if (len != 4) ... else' -- exact complements, so it is UNREACHABLE and has no row.)
#
#  Every site row expects the POST-FIX behaviour -- the host SURVIVES the transfer and a later
#  guest load returns its live value -- so on the committed HEAD each site row is RED, and the
#  note says whether the death carried THAT site's own fatal text (did it fail for the reason
#  under test?).  The rows assert survival only; they deliberately say nothing about WHAT a fixed
#  build does with the transfer, because the fix design is not yet decided.
#
#  Controls (must be green on HEAD): `live' (a guest store/load round-trip in RAM), `devsig'
#  (CRIME_DE_STATUS reads 0x1e000000 -- RAM would read 0), `mode rt' (an MTE register written and
#  read back through the sgi_mte decode), and `lin fill' -- the LINEAR arm with every guarded
#  parameter legal (depth 8, no COPY, bytemask all ones), which SURVIVES on HEAD: the kills are
#  specific to the guarded values, not to the linear path.
#
#  Session mechanics are copied from regress/sgi_mte_fill_probe.py (#509), which established them
#  on this machine: the MTE fires on any write whose ADDRESS carries CRIME_DE_START (0x800), so
#  DST1 is written last with START.
#
#  Usage:  sgi_mte_exit_witness.py <gxemul-binary> [label]
import os, sys, pty, select, time, re, tempfile

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-12s %-22s %-10s %-58s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
OP_B_SELF   = 0x1000ffff          # b    .
OP_NOP      = 0x00000000

CODE      = 0x80001000
SCRATCH   = 0xa0001800
LIVE_VAL  = 0x5a5a5a5a
SENTINEL  = 0xdeadbeef
DE_STATUS = 0xb5004000
DE_STAT   = "0x1e000000"          # CRIME_DE_STATUS; RAM reads 0 -- the device signature

DUMMY = os.path.join(tempfile.gettempdir(), "sgi_mte_exit_witness_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

#  CRIME RE base 0xb5000000; CRIME_MTE_* offsets from src/include/thirdparty/crmfbreg.h.
MTE_MODE       = 0xb5003000
MTE_BYTEMASK   = 0xb5003008       # CRIME_MTE_BYTEMASK 0x3008
MTE_BG         = 0xb5003018
MTE_DST0       = 0xb5003030
MTE_DST1_START = 0xb5003838       # CRIME_MTE_DST1 0x3038 | CRIME_DE_START 0x0800

#  MTE_MODE fields (crmfbreg.h): DST_BUF 0x1c >> 2, SRC_BUF 0xe0 >> 5, DEPTH 0x300 >> 8,
#  STIPPLE 0x400, COPY 0x800.  MTE_TLB_A..C = 0..2, TEX 3, LIN_A 4, LIN_B 5.
D8, D16, D32  = 0x000, 0x100, 0x200
STIPPLE       = 0x400
COPY          = 0x800
SRC_TEX       = 3 << 5            # src = 3 > MTE_TLB_C
DST_LIN_A     = 4 << 2
BG_VAL        = 0x11223344

def session(cmds, settle=1.5, spin=1.8):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64",
                       "0x%x:" % CODE + DUMMY])
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
        if not rd(spin if i == len(cmds) - 1 else 0.22):
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

class Addr(object):
    def __init__(self, base): self.a = base
    def take(self, n):
        got = self.a; self.a += 4 * (n + 2) + 0x20; return got

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def store(A, addr, val):
    return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([OP_SW_T0_A3], A.take(1))

def load(A, addr):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([OP_LW_V0_AT], A.take(1))

def transfer(A, mode, bytemask=None):
    """Program the MTE with `mode' and fire it -- every store a real guest instruction."""
    c = []
    if bytemask is not None:
        c += store(A, MTE_BYTEMASK, bytemask)
    c += store(A, MTE_MODE, mode)
    c += store(A, MTE_BG, BG_VAL)
    c += store(A, MTE_DST0, 0)
    c += store(A, MTE_DST1_START, 0)               # START fires do_mte_transfer()
    return c

#  Each site's own fatal() text at HEAD -- the attribution channel.
TEXT = {
    "stipple":   "unimplemented MTE_MODE_STIPPLE",
    "src tex":   "unimplemented SRC",
    "lin copy":  "unimplemented MTE_MODE_COPY",
    "lin depth": "unimplemented MTE_DEPTH_x",
    "bytemask":  "unimplemented MTE bytemask",
}

def site(name, mode, bytemask=None):
    """One site, one session: transfer, then a RAM round-trip AFTER it.  'survived' iff the
    session lived and the later load returned its live value."""
    A = Addr(CODE)
    t, alive = session(transfer(A, mode, bytemask) + store(A, SCRATCH, LIVE_VAL) +
                       load(A, SCRATCH) + ["print v0"])
    v = printed(t, "v0") if alive else "died"
    got = "survived" if (alive and v == "0x%x" % LIVE_VAL) else ("died" if not alive else "lost:" + v)
    own = TEXT[name] in t
    others = [k for k in TEXT if k != name and TEXT[k] in t]
    note = "own text %s; other sites' texts %s" % ("PRESENT" if own else "absent",
                                                   ",".join(others) if others else "none")
    row(name, got, "survived", note)
    return got, own, others

print("# sgirekills MTE exit witness, binary %s, label %s, %s" % (BIN, LABEL, time.strftime("%Y-%m-%d %H:%M:%S")))
print("%-12s %-22s %-10s %-58s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- controls (green on HEAD)
A = Addr(CODE)
t, alive = session(store(A, SCRATCH, LIVE_VAL) + load(A, SCRATCH) + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL, "RAM round-trip: the session and the CPU run")

A = Addr(CODE)
t, alive = session(load(A, DE_STATUS) + ["print v0"])
row("devsig", printed(t, "v0") if alive else "died", DE_STAT, "CRIME_DE_STATUS: only the device answers this")

A = Addr(CODE)
t, alive = session(store(A, MTE_MODE, STIPPLE | D32) + load(A, MTE_MODE) + ["print v0"])
row("mode rt", printed(t, "v0") if alive else "died", "0x%x" % (STIPPLE | D32),
    "an MTE register through the sgi_mte decode; no START")

A = Addr(CODE)
t, alive = session(transfer(A, DST_LIN_A | D8, bytemask=0xffffffff) + store(A, SCRATCH, LIVE_VAL) +
                   load(A, SCRATCH) + ["print v0"])
v = printed(t, "v0") if alive else "died"
row("lin fill", "survived" if (alive and v == "0x%x" % LIVE_VAL) else "died", "survived",
    "LINEAR arm, every guarded value legal: the path itself lives")

# ---------------------------------------------------------------- the five sites (red on HEAD)
res = {}
res["stipple"]   = site("stipple",   D32 | STIPPLE)
res["src tex"]   = site("src tex",   D32 | SRC_TEX)
res["lin copy"]  = site("lin copy",  DST_LIN_A | D8 | COPY, bytemask=0xffffffff)
res["lin depth"] = site("lin depth", DST_LIN_A | D16, bytemask=0xffffffff)
res["bytemask"]  = site("bytemask",  DST_LIN_A | D8, bytemask=0x0000ffff)

ok = sum(1 for _, k in rows if k)
print("MTEEXIT_RESULT=%d/%d" % (ok, len(rows)))
attributed = sum(1 for g, own, oth in res.values() if g == "died" and own and not oth)
print("MTEEXIT_ATTRIBUTED_DEATHS=%d/5 (died with ONLY that site's own fatal text)" % attributed)
print("MTEEXIT_DONE")
