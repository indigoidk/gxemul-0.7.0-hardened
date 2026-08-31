#!/usr/bin/env python3
#  score500.py -- lines 66-197 of regress/sgi_re_width_probe.py VERBATIM
#  (imports, constants, session(), printed(), Addr, run_ops, store, load),
#  then the two oracles under test appended.  Extraction, not transcription:
#  the fidelity of the reproduction is checkable by diff, not by trust.
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
DUMMY = "/tmp/dummy497.bin"
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 16)

CODE        = 0x80001000
SCRATCH_RAM = 0xa0001800
LIVE_VAL    = 0x12345678
DE_STATUS   = 0xb5004000
DE_STAT_VAL = "0x1e000000"
OUTSIDE     = 0xb5001800          # past LINEAR_B -> the final else (straggler)
ACC_VAL     = "0x1122334455667788"

#            name        base          symbol               accept-probe text
SITES = [
 ("tlb_a",    0xb5001000, "CRIME_RE_TLB_A",    "d->re_tlb_a[4] = 0x1122"),
 ("tlb_b",    0xb5001200, "CRIME_RE_TLB_B",    "d->re_tlb_b[4] = 0x1122"),
 ("tlb_c",    0xb5001400, "CRIME_RE_TLB_C",    "d->re_tlb_c[4] = 0x1122"),
 ("tex",      0xb5001600, "CRIME_RE_TEX",      "d->re_tex[1] = 0x1122"),
 ("linear_a", 0xb5001700, "CRIME_RE_LINEAR_A",
              "d->re_linear_a[2] = 0x11223344, [3] = 0x55667788"),
 ("linear_b", 0xb5001780, "CRIME_RE_LINEAR_B",
              "d->re_linear_b[2] = 0x11223344, [3] = 0x55667788"),
]

def decl(sym):
    """The literal a WIDTH decline emits.  Deliberately includes ' -- declined.'
    so it cannot also match the read kill's 'TODO: read from <sym>'."""
    return "for " + sym + " -- declined."

OP_NOP      = 0x00000000
OP_B_SELF   = 0x1000ffff
OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
OP_LD_V0_AT = 0xdc220000          # ld   $v0, 0($at)

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-18s %-12s %-12s %-46s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

def session(cmds, settle=1.5, spin=1.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64",
                       "0x80001000:" + DUMMY])
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
            alive = False
            break
        if not rd(spin if i == len(cmds) - 1 else 0.25):
            alive = False
            break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    how = "nostatus"
    try:
        _, stat = os.waitpid(pid, 0)
        if os.WIFSIGNALED(stat):
            how = "sig%d" % os.WTERMSIG(stat)
        elif os.WIFEXITED(stat):
            how = "exit%d" % os.WEXITSTATUS(stat)
    except OSError:
        pass
    return buf.replace("\r", ""), alive, how

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    if not m:
        return "absent"
    #  Normalise width: a 64-bit register may print sign/zero-extended, and a
    #  row comparing raw strings would then fail on formatting rather than on
    #  behaviour.
    return "0x%x" % int(m.group(1), 16)

class Addr(object):
    def __init__(self, base): self.a = base
    def take(self, n):
        got = self.a; self.a += 4 * (n + 2) + 0x20; return got

def run_ops(ops, at):
    put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
    put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
            "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
    return put + ["pc=0x%x" % at, "step %d" % len(ops)]

def store(A, addr, op=OP_SW_T0_A3, val="0x12345678"):
    return ["a3=0x%x" % addr, "t0=%s" % val] + run_ops([op], A.take(1))

#  THE DESTINATION REGISTER IS PRESET TO A SENTINEL, NOT TO 0.
#  Preset to 0 the row cannot tell "the common tail ran and wrote odata (0)"
#  from "the load never completed at all" -- both leave v0 == 0.  With a
#  sentinel the two separate: a declined read that reaches the tail yields 0,
#  and a read that faulted or never landed yields the sentinel.
SENTINEL = 0xdeadbeef

def load(A, addr, op=OP_LW_V0_AT):
    return ["at=0x%x" % addr, "v0=0x%x" % SENTINEL] + run_ops([op], A.take(1))

# =====================  APPENDED: THE ORACLES UNDER TEST  =====================
print("SCORE500 binary=%s label=%s" % (BIN, LABEL))
print("")

# ---- ORACLE P: exactly as proposed in REPIN_REQUIRED.md / repin.py ----------
A = Addr(CODE)
tP, aliveP, howP = session(store(A, OUTSIDE))
okP = ("unimplemented write to address" in tP) and ("-- declined." in tP)
gotP = howP + ("+txt" if okP else "-txt")
print("  P  proposed      got=%-24s want=%-24s %s"
      % (gotP, "exit0+txt", "ok" if gotP == "exit0+txt" else "FAIL"))
print("       components: how=%s  txt=%s   alive=%s  <-- DISCARDED by this oracle"
      % (howP, okP, aliveP))

# ---- ORACLE N: the replacement -------------------------------------------
#  ONE contiguous literal including the address and the data field.  Two
#  independent `in t' tests are a weaker claim: "-- declined." is emitted by the
#  six #497 width declines and by #498's sgi_de decline as well.
DECL_W = ("unimplemented write to address 0x1800, "
          "data=0x0000000012345678 -- declined.  (once) ]")
A = Addr(CODE)
tN, aliveN, howN = session(store(A, OUTSIDE) + load(A, DE_STATUS) + ["print v0"])
nlit = tN.count(DECL_W)
valN = printed(tN, "v0") if aliveN else "died"
gotN = "%s/%s/%s" % (howN, "txt" if nlit == 1 else "notxt", valN)
wantN = "exit0/txt/" + DE_STAT_VAL
print("  N  replacement   got=%-24s want=%-24s %s"
      % (gotN, wantN, "ok" if gotN == wantN else "FAIL"))
print("       components: how=%s  contiguous-literal-count=%d  alive=%s  v0=%s"
      % (howN, nlit, aliveN, valN))

#  DENOMINATOR.  A literal that matches nothing produces a confident RED that
#  looks exactly like a caught mutant.  Print what the transcript actually held.
cand = [l for l in tN.split("\n") if "unimplemented write to address" in l]
print("       transcript lines containing 'unimplemented write to address': %d"
      % len(cand))
for l in cand:
    print("         | " + l.strip())

# ---- ORACLE N3: the one-token minimum (alive folded in), for comparison -----
gotN3 = gotP + ("+alive" if aliveP else "+dead")
print("  N3 alive-only    got=%-24s want=%-24s %s"
      % (gotN3, "exit0+txt+alive", "ok" if gotN3 == "exit0+txt+alive" else "FAIL"))
print("")
print("SCORE500_DONE")
