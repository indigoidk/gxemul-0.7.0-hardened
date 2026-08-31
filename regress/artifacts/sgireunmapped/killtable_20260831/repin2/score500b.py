#!/usr/bin/env python3
#  score500b.py -- FOUR candidate oracles for sgi_re_width_probe.py's
#  re-pinned catch-all row.  Lines 66-197 of the shipped probe are copied
#  in VERBATIM by extraction, so session()/printed()/Addr/store/load are
#  the shipped ones by construction and the fidelity is diff-checkable.
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

# =====================  FOUR CANDIDATE ORACLES  =====================
print("SCORE500B binary=%s label=%s" % (BIN, LABEL))
print("")

DECL_W = ("unimplemented write to address 0x1800, "
          "data=0x0000000012345678 -- declined.  (once) ]")

def verdict(tag, got, want, extra):
    print("  %-4s got=%-26s want=%-26s %s" % (tag, got, want,
                                             "ok" if got == want else "FAIL"))
    print("       %s" % extra)

# ---- P : as proposed in REPIN_REQUIRED.md.  Write-only session, two loose
#          substring tests, `alive' discarded.
A = Addr(CODE)
tP, aliveP, howP = session(store(A, OUTSIDE))
okP = ("unimplemented write to address" in tP) and ("-- declined." in tP)
gotP = howP + ("+txt" if okP else "-txt")
verdict("P", gotP, "exit0+txt",
        "how=%s loose_txt=%s alive=%s(discarded)" % (howP, okP, aliveP))

# ---- N3: P plus the `alive' the shipped session() already returns.
verdict("N3", gotP + ("+alive" if aliveP else "+dead"), "exit0+txt+alive",
        "one token over P; still the loose two-substring text test")

# ---- N1: contiguous literal + a DEVICE-SIGNATURE read of CRIME_DE_STATUS.
#          Survival proved by a value that only the device can answer.
A = Addr(CODE)
t1, alive1, how1 = session(store(A, OUTSIDE) + load(A, DE_STATUS) + ["print v0"])
n1 = t1.count(DECL_W)
v1 = printed(t1, "v0") if alive1 else "died"
verdict("N1", "%s/%s/%s" % (how1, "txt" if n1 == 1 else "notxt", v1),
        "exit0/txt/" + DE_STAT_VAL,
        "how=%s contiguous=%d alive=%s v0=%s  (devsig channel, other device)"
        % (how1, n1, alive1, v1))

# ---- N2: contiguous literal + a declined READ OF THE SAME UNMAPPED ADDRESS,
#          with the destination register preset to SENTINEL.  This is the probe's
#          own `lw surv' idiom (its comment at the SENTINEL definition explains
#          why 0 and "never landed" must be distinguishable).  It exercises the
#          catch-all's READ branch as well as its write branch.
A = Addr(CODE)
t2, alive2, how2 = session(store(A, OUTSIDE) + load(A, OUTSIDE) + ["print v0"])
n2 = t2.count(DECL_W)
v2 = printed(t2, "v0") if alive2 else "died"
verdict("N2", "%s/%s/%s" % (how2, "txt" if n2 == 1 else "notxt", v2),
        "exit0/txt/0x0",
        "how=%s contiguous=%d alive=%s v0=%s  (sentinel preset 0xdeadbeef)"
        % (how2, n2, alive2, v2))

# ---- DENOMINATORS.  A literal that matches nothing gives a confident RED that
#      looks exactly like a caught mutant.  Show what the transcripts held.
print("")
for nm, t in (("N1", t1), ("N2", t2)):
    ws = [l.strip() for l in t.split("\n") if "unimplemented write to address" in l]
    rs = [l.strip() for l in t.split("\n") if "unimplemented read from address" in l]
    print("  %s transcript: %d write-catchall line(s), %d read-catchall line(s)"
          % (nm, len(ws), len(rs)))
    for l in ws + rs:
        print("       | " + l)
    dbe = [l.strip() for l in t.split("\n")
           if ("exception" in l.lower() or "DBE" in l)]
    print("       exception/DBE lines: %d%s"
          % (len(dbe), ("  | " + dbe[0]) if dbe else ""))
print("")
print("SCORE500B_DONE")
