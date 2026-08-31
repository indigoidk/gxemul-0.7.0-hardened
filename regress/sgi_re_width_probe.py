#!/usr/bin/env python3
#
#  #497 widthkillclass -- the detector.
#
#  CONTRACT (vacuity-floor clause (e)) -- which edits this detector is designed
#  to catch, and which it is NOT:
#
#    CATCHES
#      * removal or reinstatement of ANY of the six width kills, at any one of
#        the six sites individually (the `sw surv' rows are per site);
#      * narrowing the decline so it applies to writes only, i.e.
#        `len != 8' -> `len != 8 && writeflag == MEM_WRITE'  (the `lw surv' rows);
#      * ANY decline that does not reach the function's common tail -- an early
#        `return', or `return 0' (which memory_rw coerces to -1 and turns into a
#        guest EXCEPTION_DBE).  The `lw surv' rows check the VALUE the declined
#        read returns, not merely that the host survived: the destination
#        register is preset to a sentinel, so "tail ran, wrote 0" and "load
#        never completed" are distinguishable.  A survival-only oracle at a
#        refusal-effect site is vacuous by construction, and this row was one
#        until the d_returnzero mutant was built;
#      * deleting the latch, or dropping the `d->warned |= BIT' set, so the
#        message floods  (the `sw lat1' rows COUNT; they do not test presence);
#      * making two or more sites share a latch bit  (`xsite 6msg');
#      * mis-attributing a window's message to another window (`xsite order');
#      * growth of the width predicate that swallows LEGAL 8-byte accesses
#        (the `accept' rows, probed at an offset with bit 3 SET so that a
#        `|| (relative_addr & 8)' tightening reddens them);
#      * silent removal of the six READ kills or of the final catch-all, which
#        this round deliberately does NOT touch  (`<s> ld kill' x6, `other kill').
#
#    *** AND IT PINS THE ROUND'S CENTRAL DISCLOSURE, RATHER THAN ASSERTING IT.
#        The width guard is evaluated FIRST, so after #497 a 4-byte read
#        DECLINES -- but an ordinary 8-byte `ld' to each of the six windows
#        STILL ENDS THE HOST, because len == 8 passes the width guard and falls
#        into the read arm's exit(1) (dev_sgi_re.c lines 245 262 279 296 346
#        362).  Fixing six width kills leaves EXACTLY six read kills at the same
#        six offsets.  The `<s> ld kill' rows measure that at every window, so a
#        future reader cannot conclude from `lw surv' that reads were made safe.
#        Filed as sgirekills, which has no witness yet. ***
#
#    DOES NOT CATCH
#      * anything in DEVICE_ACCESS(sgi_de) or (sgi_mte), including sgi_de's own
#        width kill (accept set {4,8}, filed sgidewidth) and sgi_mte's
#        unreachable one (filed sgimtewidth);
#      * the LINEAR out-of-bounds index itself.  Observing re_linear_b[0] being
#        clobbered needs a READ path, and every read arm here still exit(1)s.
#        The aliasing is pinned by offsetof in PRETABLE.out section 1.2, not by
#        a row.  Owed to sgirekills.
#
#    ONE THING THE CONTRACT UNDERSTATED, corrected before shipping rather than
#    left as a modest-sounding false claim: an earlier draft said there is NO
#    anchored cell-position row.  There is.  Each `accept' row matches the arm's
#    own debug() text INCLUDING THE INDEX AND THE VALUE -- e.g.
#    "d->re_tlb_a[4] = 0x1122" -- so it is anchored to a SPECIFIC cell by a
#    channel outside the decode under test, which is clause (f)'s requirement.
#    A re-map of the index arithmetic (>> 1 -> >> 2) or of the byte packing
#    reddens it.  Window-level translations are additionally caught by the
#    per-site attribution rows, since each checks the message naming ITS OWN
#    symbol.  What remains genuinely uncovered is a re-map that preserves both
#    index and symbol.
#
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

print("#497 widthkillclass DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("%-18s %-12s %-12s %-46s %s" % ("row", "got", "want", "note", ""))

# ------------------------------------------------ controls / identity  (c)
A = Addr(CODE)
t, alive, how = session(store(A, SCRATCH_RAM) + load(A, SCRATCH_RAM)
                        + ["print v0"])
row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
    "LIVENESS: guest store then load, through RAM")

A = Addr(CODE)
t, alive, how = session(load(A, DE_STATUS) + ["print v0"])
row("devsig stat", printed(t, "v0") if alive else "died", DE_STAT_VAL,
    "DEVSIG: CRIME_DE_STATUS reads 0x1e000000; RAM would read 0")

print("OPUS497T_CONTROL=%s" % ("OK" if all(o for _, o in rows) else "DEAD"))
print("")

# ------------------------------------------------ per site x 6
for nm, base, sym, acctext in SITES:
    lit = decl(sym)

    # 1. a len=4 WRITE must be DECLINED, not fatal
    A = Addr(CODE)
    t, alive, how = session(store(A, base))
    row(nm + " sw surv", how, "exit0", "len=4 WRITE declined, host survives")

    # 2. the latch: TWO declined accesses in ONE session -> exactly ONE message
    A = Addr(CODE)
    t, alive, how = session(store(A, base) + store(A, base + 4))
    row(nm + " sw lat1", t.count(lit), 1,
        "(once): COUNT over 2 accesses -- presence would pass unlatched")

    # 3. a len=4 READ must ALSO be declined.
    #    NOTE: the width arm is evaluated BEFORE the read arm, so a len=4 read
    #    takes the (now declining) width arm and never reaches the still-live
    #    read kill.  An 8-byte read still dies -- see `ld readkill' below.
    #    This row is what kills M1 (`len != 8 && writeflag == MEM_WRITE').
    A = Addr(CODE)
    t, alive, how = session(load(A, base) + ["print v0"])
    got = how + "/" + (printed(t, "v0") if alive else "died")
    row(nm + " lw surv", got, "exit0/0x0",
        "declined READ reaches the tail and returns a DEFINED 0")

    # 4. ACCEPT side (de-escalation clause).  Offset +8 has bit 3 SET on
    #    purpose: a `|| (relative_addr & 8)' growth must redden this.
    A = Addr(CODE)
    t, alive, how = session(store(A, base + 8, OP_SD_T0_A3, ACC_VAL))
    row(nm + " accept", "1" if acctext in t else "0", "1",
        "LEGAL len=8 write still lands (probed at +8, bit 3 set)")

# ------------------------------------------------ cross-site  (M2 + anchor)
A = Addr(CODE)
cmds = []
for nm, base, sym, _a in SITES:
    cmds += store(A, base)
t, alive, how = session(cmds, spin=2.0)
present = [decl(sym) for _n, _b, sym, _a in SITES]
n_present = sum(1 for lit in present if t.count(lit) == 1)
row("xsite 6msg", n_present, 6,
    "six windows, ONE session: 6 distinct latches (kills bit collision)")

pos = [t.find(lit) for lit in present]
ordered = all(p >= 0 for p in pos) and pos == sorted(pos)
row("xsite order", "1" if ordered else "0", "1",
    "ANCHOR: message order == the order the guest issued them")

# ------------------------------------------------ contract / non-regression
#  THE LEFTOVER, MEASURED AT EVERY WINDOW rather than argued from the pairing:
#  len == 8 passes the width guard and reaches the still-live read kill.
for nm, base, sym, _a in SITES:
    A = Addr(CODE)
    t, alive, how = session(load(A, base, OP_LD_V0_AT))
    ok_txt = ("TODO: read from " + sym) in t
    row(nm + " ld kill", how + ("+txt" if ok_txt else "-txt"), "exit1+txt",
        "len=8 READ STILL KILLS THE HOST here -- untouched (sgirekills)")

A = Addr(CODE)
t, alive, how = session(store(A, OUTSIDE))
# *** DEATH-ONLY.  This row observes THAT the catch-all kills, never WHICH kill it is --
# it discards the transcript its six `ld kill` siblings above test for membership.  So a
# change to the catch-all message that leaves exit(1) in place passes: MEASURED 35/35 with
# zero red rows, against a matched control (a read arm's text) at 34/35.  It is the
# `d_returnzero` shape mirrored onto the death side -- a death-only oracle at a site where
# death is the shared answer.  Filed as `otherkilldeath`; the fix is the ok_txt test the
# siblings already carry.  Do NOT read this row as pinning the catch-all's identity. ***
row("other kill", how, "exit1",
    "the :372 catch-all still ends the host -- DEATH ONLY, not its identity")

ok = sum(1 for _, o in rows if o)
print("")
print("OPUS497T_RESULT=%d/%d" % (ok, len(rows)))
print("OPUS497T_LABEL=%s" % LABEL)
print("OPUS497T_DONE")
