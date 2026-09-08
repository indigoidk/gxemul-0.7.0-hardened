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
#    *** THE TWO PARAGRAPHS ABOVE ARE #497's AND #499's AND ARE NO LONGER TRUE OF THIS
#        FILE.  #513 REMOVED ALL SIX READ KILLS -- five arms became ACCEPTs and
#        CRIME_RE_TEX became a latched decline -- so `<s> ld kill' x6 NO LONGER EXIST
#        as row names, and an 8-byte `ld' to those windows no longer ends the host.
#        The contract below is the LIVE one; the text above is kept, with this
#        correction beside it, because a reader arriving from #497's or #499's records
#        needs to see which half moved and when.  Found by the pass-2 panel, which read
#        the contract against the diff and reported it stale. ***
#
#    *** AND IT PINS THE ROUND'S CENTRAL DISCLOSURE, RATHER THAN ASSERTING IT.
#        The width guard is evaluated FIRST, so after #497 a 4-byte read
#        DECLINES -- but an ordinary 8-byte `ld' to each of the six windows
#        STILL ENDS THE HOST, because len == 8 passes the width guard and falls
#        into the read arm's exit(1) (dev_sgi_re.c lines 245 262 279 296 346
#        362).  Fixing six width kills leaves EXACTLY six read kills at the same
#        six offsets.  The `<s> ld kill' rows measure that at every window, so a
#        future reader cannot conclude from `lw surv' that reads were made safe.
#        Filed as sgirekills.  *** ITS WITNESS IS THIS FILE: the six `<site> ld kill`
#        rows below ARE rung-3 symptom demonstrations of that defect, and the ledger's
#        witness field names them.  This comment used to say the row `has no witness
#        yet' -- written before those rows existed and left standing after they shipped,
#        so the file denied being the witness it had become.  Found by the codex seat. ***
#
#    DOES NOT CATCH
#      * anything in DEVICE_ACCESS(sgi_de) or (sgi_mte), including sgi_de's own
#        width kill (accept set {4,8}, filed sgidewidth) and sgi_mte's
#        unreachable one (filed sgimtewidth);
#      * the LINEAR out-of-bounds index itself.  Observing re_linear_b[0] being
#        clobbered needs a READ path, and every read arm here still exit(1)s.
#        *** THAT CLAUSE IS #497's AND IS FALSE SINCE #513: five read arms ACCEPT and
#        CRIME_RE_TEX declines, so a READ PATH NOW EXISTS.  Whether that makes the
#        aliasing rowable is a QUESTION FOR sgilinearoob, not a claim made here.
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
DE_BASE     = 0xb5002000          # DEVICE_ACCESS(sgi_de); a BYTE access fires DE_LEN
#  Drawing-engine registers, to fire the last two latch bits.  Addresses and values COPIED from
#  regress/sgi_re_randompixel_probe.py, which drives this path as a shipped rung-3 witness --
#  not invented here.
DE_MODE_DST = 0xb5002008
DE_DRAWMODE = 0xb5002018
DE_XVERT_0  = 0xb5002070
DE_XVERT_1  = 0xb5002074
DE_PRIM_ST  = 0xb5002860          # CRIME_DE_PRIMITIVE | CRIME_DE_START -- the store fires the draw
MODE_LIN_B  = 0x1620              # LIN_B | BUFDEPTH_32 | TYPE_RGBA -> dst_mode 5, the default arm
DRAWMODE    = 0x002000f8
PRIM_RECT   = 0x03020000          # DE_PRIM_RECTANGLE | DE_PRIM_TB -- an IMPLEMENTED op
PRIM_BAD    = 0x05020000          # an UNIMPLEMENTED op: only LINE and RECTANGLE of 256 exist
DE_STATUS   = 0xb5004000
DE_STAT_VAL = "0x1e000000"
OUTSIDE     = 0xb5001800          # past LINEAR_B -> the final else (straggler)
ACC_VAL     = "0x1122334455667788"

#  *** THE RE-PIN VALUES (sgirekills).  VAL_HI differs from VAL_LO in every
#  halfword lane.
#
#  AN EARLIER WORDING CALLED THAT "the point of having two", claiming a single
#  value, or two sharing any lane, "would let such an edit through".  THAT
#  OVERCLAIMED, and the pass-2 panel caught it: VAL_LO ALONE already has four
#  DISTINCT halfwords (1122 3344 5566 7788), so it by itself reddens under a
#  pure read-side lane permutation or duplication -- M11_lanerev reds the lo
#  row as well as the hi one, which is the measurement that settles it.
#
#  What the SECOND value actually buys is narrower and still worth having: two
#  rows cannot both be satisfied by a mutant returning one fixed constant, and
#  the hi row exercises the window's LAST SLOT -- which is what M4 and M7
#  measured, and neither is a lane property at all. ***
VAL_LO      = 0x1122334455667788
VAL_HI      = 0xa1b2c3d4e5f60718

#  Each ACCEPT window gets TWO rows: one at the window BASE and one at its LAST
#  8-byte slot.  #499 measured on THIS DEVICE that one row per arm cannot do the
#  job -- an accept row written at a base tests the near bound twice and the far
#  bound never, and moving it to the top merely swaps which bound is blind.
#
#         nm          base          array          lo_off  lo_i  hi_off  hi_i  kind
REPIN = [
 ("tlb_a",    0xb5001000, "re_tlb_a",    0x000, 0, 0x1f8, 252, "hw"),
 ("tlb_b",    0xb5001200, "re_tlb_b",    0x000, 0, 0x1f8, 252, "hw"),
 ("tlb_c",    0xb5001400, "re_tlb_c",    0x000, 0, 0x1f8, 252, "hw"),
 ("linear_a", 0xb5001700, "re_linear_a", 0x000, 0, 0x078,  30, "w"),
 ("linear_b", 0xb5001780, "re_linear_b", 0x000, 0, 0x078,  30, "w"),
]

TEX_BASE    = 0xb5001600
TEX_HI_OFF  = 0x0d8               # the last 8-byte slot inside CRIME_RE_TEX + 0xe0
TEX_RD_DECL = "unimplemented read from CRIME_RE_TEX -- declined."

def anchor(arr, idx, val, kind):
    """*** THE ANCHOR CHANNEL, clause (f). ***  The store's OWN debug() names the
    INDEX it wrote, so this literal pins WHICH CELL the address resolved to --
    not merely that some cell round-tripped.  A translation that slides the whole
    window keeps every value distinct and still reddens here.  Nothing is added to
    the READ path to make this work: the channel already exists on the write."""
    if kind == "hw":
        return "d->%s[%i] = 0x%04x" % (arr, idx, (val >> 48) & 0xffff)
    return "[ d->%s[%i] = 0x%08x, [%i] = 0x%08x ]" % (
        arr, idx, (val >> 32) & 0xffffffff, idx + 1, val & 0xffffffff)

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
OP_SB_T0_A3 = 0xa0e80000          # sb   $t0, 0($a3)   -- narrow, fires a _LEN latch
OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
OP_LD_V0_AT = 0xdc220000          # ld   $v0, 0($at)

rows = []

#  *** THE NAME COLUMN HAS ZERO MARGIN LEFT.  MEASURED 2026-09-08, before commit. ***
#
#  Rows print as %-18s, and gate_arm.sh matches each by name with the pattern
#      count "$SGILOG" "^$v  .*ok$"
#  -- caret, the name, TWO SPACES.  So a name may be at most 16 characters.  **The longest name in
#  this probe is exactly 16** (`linear_a sw surv`, `linear_b sw surv`, `linear_a lw surv`,
#  `linear_b lw surv`).  ONE more character and that gate row becomes
#  UNSATISFIABLE and the row SILENTLY STOPS BEING TESTED -- the padded-column class, which this
#  project has already paid for once.
#
#  A new row therefore needs <= 16 characters, or the %-18s here and the pattern in the gate must
#  both widen, in the same commit.  The check that catches it is one command against a real run:
#  compare the gate name list with the names actually emitted, both directions.
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

#  *** THE 64-BIT LIVENESS CONTROL, AND IT IS NOT DECORATION. ***  Every re-pinned
#  ACCEPT row below asserts a 64-bit value read back through `print v0'.  On the
#  COMMITTED build all of those rows DIE at the load, so a pre-fix run cannot tell
#  a correct want-string from a mis-formatted one -- the red is explained by the
#  kill either way.  This row exercises the identical sd/ld/print path through RAM,
#  where nothing kills, so the format is pinned BEFORE the fix rather than after.
A = Addr(CODE)
t, alive, how = session(store(A, SCRATCH_RAM, OP_SD_T0_A3, "0x%016x" % VAL_LO)
                        + load(A, SCRATCH_RAM, OP_LD_V0_AT) + ["print v0"])
row("live64", printed(t, "v0") if alive else "died", "0x%x" % VAL_LO,
    "LIVENESS: 64-bit sd/ld through RAM -- pins the re-pin want format")

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
    #    *** BOTH HALVES FALSE SINCE #513: the 8-byte read is ACCEPTED (or, at TEX,
    #    declined), and `ld readkill' no longer exists -- it is `<arm> ld lo|hi'.
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

# ------------------------------------------------ the read arms  (sgirekills)
#
#  *** RE-PINNED FOR sgirekills.  SIX DEATH-ONLY ROWS BECOME FOURTEEN. ***
#
#  THE OLD ROWS were `row(nm + " ld kill", how + txt, "exit1+txt")' -- they asserted
#  that a len == 8 READ still ends the host at each of the six windows.  That was a
#  true and useful pin while the kills stood.  It cannot survive the fix, which is
#  exactly the situation the oracle-correction rule governs: the rows are re-pinned
#  FIRST and the committed build is measured RED under the new expectations, and only
#  then is the device edited.  Same script, opposite colour.
#
#  *** WHAT REPLACED THEM, AND WHY IT IS NOT THE OBVIOUS SET. ***  My first design was
#  one row per window at the window BASE, plus a #499-style decline row for TEX.  The
#  design panel refused it with two floor-shaped holes and one oracle this file had
#  already measured wrong:
#
#    (1) THE FAR BOUND WAS UNPINNED.  An accept row at a window's base tests the near
#        bound twice and the far bound never -- so a shrink of the window's upper limit
#        is invisible to it.  #499 measured that on this same device.  Hence TWO rows
#        per ACCEPT arm, base and LAST SLOT.
#
#    (2) A LOAD-ONLY TEX DECLINE ROW WOULD HAVE BEEN VACUOUS, and this is the sharp one.
#        Such a row wants `v0 == 0'.  If a later round converts TEX to an ACCEPT, it will
#        read back the ZEROED array and yield 0 as well -- so the row could not redden at
#        the very edit it exists to catch.  The TEX rows therefore STORE a non-zero value
#        first: an ACCEPT would return it, and the row goes red.
#
#    (3) `how == "exit0"' IS THE WRONG ORACLE and #499 measured why -- an exit(0)
#        reinstatement prints its message and then dies, scoring green with the process
#        dead.  NO RE-PINNED READ ROW below reads exit status.  (An earlier wording said
#        "no row below", which is FALSE: the pre-existing `other decl' row DOES read `how'
#        and wants `exit0/txt/0x0'.  That row is #499's and is out of scope here; the claim
#        belongs to the rows this round re-pinned.)  SURVIVAL IS IMPLIED BY THE VALUE:
#        a dead session cannot print one.
#
for nm, base, arr, lo_off, lo_i, hi_off, hi_i, kind in REPIN:
    for tag, off, idx, val in (("lo", lo_off, lo_i, VAL_LO),
                               ("hi", hi_off, hi_i, VAL_HI)):
        A = Addr(CODE)
        addr = base + off
        t, alive, how = session(store(A, addr, OP_SD_T0_A3, "0x%016x" % val)
                                + load(A, addr, OP_LD_V0_AT) + ["print v0"])
        anc = anchor(arr, idx, val, kind)
        got = (printed(t, "v0") if alive else "died") + ("+anc" if anc in t else "-anc")
        row("%s ld %s" % (nm, tag), got, "0x%x+anc" % val,
            "ACCEPT %s[%i]: value round-trips AND the store names the cell" % (arr, idx))

#  *** TEX IS THE ONE ARM THAT IS NOT AN ACCEPT. ***  The other five windows have a
#  write path that already computes and stores the value, so reading it back is the
#  ACCEPT member of the option set.  TEX's read is DECLINED instead, and these four
#  rows pin the decline rather than a value.  *** THE STORE-FIRST SHAPE FROM (2) ABOVE IS
#  ON TWO OF THEM, NOT FOUR: `tex ld lo' and `tex ld hi' store a non-zero value before
#  loading, so a future ACCEPT of TEX reddens THEM WITH ACCEPT-SPECIFIC EVIDENCE -- the stored
#  non-zero comes back, which distinguishes an ACCEPT from a merely DELETED message.
#
#  *** THE SENTENCE THAT USED TO SIT HERE OVERSHOT, AND TWO SEATS CAUGHT IT INDEPENDENTLY
#  (grok and kimi, pass 4).  It said `tex rd lat1' and `tex xbit' "would not redden on an
#  ACCEPT".  FALSE: both oracle the decline-message COUNT (`1' and `1/11'), and an ACCEPT
#  drives that count to 0, so BOTH GO RED.  What they cannot do is tell an ACCEPT from a
#  deleted message -- that is the value pair's job.  The correction understated the
#  detection surface, which is the same wrong-record class this round has been fixing,
#  this time INSIDE a correction.  It does not reopen a collision cell. ***
for tag, off in (("lo", 0x000), ("hi", TEX_HI_OFF)):
    A = Addr(CODE)
    addr = TEX_BASE + off
    val = VAL_LO if tag == "lo" else VAL_HI
    t, alive, how = session(store(A, addr, OP_SD_T0_A3, "0x%016x" % val)
                            + load(A, addr, OP_LD_V0_AT) + ["print v0"])
    got = (printed(t, "v0") if alive else "died")
    got += "+1msg" if t.count(TEX_RD_DECL) == 1 else "+%imsg" % t.count(TEX_RD_DECL)
    row("tex ld " + tag, got, "0x0+1msg",
        "DECLINE: reads 0 after a real store -- an ACCEPT would return the store")

#  THE LATCH: one announce per instance, not one per access.  Two reads at DIFFERENT
#  offsets, so a latch keyed on the address rather than on the arm also reddens.
A = Addr(CODE)
t, alive, how = session(load(A, TEX_BASE, OP_LD_V0_AT)
                        + load(A, TEX_BASE + TEX_HI_OFF, OP_LD_V0_AT))
row("tex rd lat1", "%i" % t.count(TEX_RD_DECL) if alive else "died", "1",
    "LATCH: two TEX reads at two offsets announce exactly once")

#  *** THE CROSS-BIT ROW.  #498 measured a latch shared between two arms scoring 23/25,
#  and #490 measured the same collision in another file, so it is pinned here BEFORE it
#  can bite: fire all SIX width latches -- CRIME_RE_TEX's own included -- with narrow
#  writes, then read TEX.  If the read decline is given an existing bit rather than its
#  own, its message is already suppressed and this row reds. ***
#  *** CLASS CLOSURE ON THE LATCH-COLLISION AXIS -- pass 3. ***
#
#  This row USED TO fire only the six width latches (bits 0-5), and pass 3 showed why that is
#  not enough: the mutation operator is `SGIRE_W_TEX_RD := <an already-used bit>' ON THE EDITED
#  LINE, so bits 6, 7, 9 and 10 were the SAME operator on the SAME line and swept by nothing.
#  Pass 2 found the bit-8 cell; pass 3 found the rest.  TWO CONSECUTIVE PASSES FINDING ONE CLASS
#  is the trigger for closing the whole space in one diff rather than one cell per pass.
#
#      bit  latch              fired here by
#      ---  -----------------  ---------------------------------------------------------
#       0-5 *_LEN x6           a narrow (byte) store to each of the six RE windows
#       6   SGIRE_W_DE_LEN     a BYTE store to the DE window -- its accept set is {4,8}
#       7   SGIRE_W_UNMAP_WR   a store to OUTSIDE
#       8   SGIRE_W_UNMAP_RD   a load  from OUTSIDE
#       9   SGIRE_W_PRIM_OP    an unimplemented drawing op stored to PRIMITIVE|START
#      10   SGIRE_W_BADMODE    an unimplemented DST MODE driven through a real rectangle
#
#  *** THE CLASS IS CLOSED, AND BITS 9 AND 10 WERE MEASURED OPEN BEFORE THEY WERE CLOSED. ***
#  An earlier form of this row fired bits 0-8 and DISCLOSED 9 and 10 as unreachable-in-session,
#  on the ground that a TEX-read session never enters the drawing-engine path.  That disclosure
#  was MEASURED rather than asserted -- `M_bit9' and `M_bit10' both scored 46/46, a clean escape
#  (CLASSVERIFY.txt) -- and two seats had called a measured-open cell on the edited line a breach
#  whatever the contract says.  They were right, and the disclosure was answering the wrong
#  question: not "does a TEX session normally draw?" but "CAN one?"  It can, in six stores.
#  The settling fact I had written down as unknown turned out to be one grep away, in a shipped
#  probe that already drives this path.
A = Addr(CODE)
cmds = []
for _nm, _b, _sym, _a in SITES:
    cmds += store(A, _b, OP_SB_T0_A3, "0x1")          # bits 0-5
cmds += store(A, DE_BASE, OP_SB_T0_A3, "0x1")         # bit 6
cmds += store(A, OUTSIDE, OP_SB_T0_A3, "0x1")         # bit 7
cmds += load(A, OUTSIDE, OP_LW_V0_AT)                 # bit 8
#  *** THE SIX CALLS BELOW ONCE PASSED THEIR VALUE AS THE OPCODE. ***  `store()' is
#  `store(A, addr, op=OP_SW_T0_A3, val="0x12345678")', so `store(A, DE_MODE_DST, MODE_LIN_B)'
#  assembled MODE_LIN_B as an INSTRUCTION and wrote the default value to the register.  All six
#  were wrong the same way, and **the row still scored 46/46**, because its oracle is only the TEX
#  decline count -- which garbage stores do not disturb.  A row that passes while doing nothing it
#  claims is exactly the vacuity the floor exists to prevent; it was caught by a reading seat, not
#  by a measurement.  Pass the value as `val', never positionally as `op'.
#
#  bit 10 SGIRE_W_BADMODE -- an unimplemented DST MODE driven through a REAL rectangle, so
#  horrible_getputpixel is actually entered.  The vertex pair is (0,0)-(0,3): the HEIGHT is what
#  makes the primitive iterate, which sgi_re_randompixel_probe.py measured and documents.
cmds += store(A, DE_MODE_DST, OP_SW_T0_A3, "0x%x" % MODE_LIN_B)
cmds += store(A, DE_DRAWMODE, OP_SW_T0_A3, "0x%x" % DRAWMODE)
cmds += store(A, DE_XVERT_0,  OP_SW_T0_A3, "0x0")
cmds += store(A, DE_XVERT_1,  OP_SW_T0_A3, "0x3")
cmds += store(A, DE_PRIM_ST,  OP_SW_T0_A3, "0x%x" % PRIM_RECT)
#  bit 9 SGIRE_W_PRIM_OP -- an unimplemented drawing OP.  draw_primitive's switch rejects it
#  before any pixel work, so this needs no vertex setup of its own.
cmds += store(A, DE_PRIM_ST,  OP_SW_T0_A3, "0x%x" % PRIM_BAD)
cmds += load(A, TEX_BASE, OP_LD_V0_AT)
t, alive, how = session(cmds, spin=4.0)

#  *** THE ROW PROVES ITS OWN SETUP.  This is the repair for the defect that made it vacuous. ***
#  Counting only the TEX decline cannot distinguish "ten latches fired and TEX still announced"
#  from "the setup did nothing and TEX announced".  Both give 1.  So the row also reports HOW MANY
#  of the other announces it actually saw, and wants ALL of them: a setup that silently fails --
#  a mistyped call, a moved register, a changed message -- now REDS this row instead of passing it.
SETUP_LIT = ([decl(sym) for _n, _b, sym, _a in SITES] +          # bits 0-5, the six *_LEN
             ["[ sgi_de: unimplemented len=",                    # bit 6  DE_LEN
              "unimplemented write to address 0x1800",           # bit 7  UNMAP_WR
              "unimplemented read from address 0x1800",          # bit 8  UNMAP_RD
              "UNIMPLEMENTED drawing op",                        # bit 9  PRIM_OP
              "unimplemented dst_mode"])                         # bit 10 BADMODE
fired = sum(1 for lit in SETUP_LIT if lit in t)
row("tex xbit", "%i/%i" % (t.count(TEX_RD_DECL), fired) if alive else "died",
    "1/%i" % len(SETUP_LIT),
    "CROSSBIT: all 11 other latches PROVEN fired; TEX read still announces once")

A = Addr(CODE)
#  *** RE-PINNED BY #499, WHICH REMOVED THIS KILL.  Three channels replace one, and
#  BOTH of the obvious oracles were measured VACUOUS before this one was chosen. ***
#
#  THE OLD ROW was `row("other kill", how, "exit1")' -- DEATH-ONLY.  It observed THAT
#  the catch-all killed, never WHICH kill it was, so a change to the message that left
#  exit(1) standing passed: MEASURED 35/35 against a matched control at 34/35.  Filed
#  as `otherkilldeath', and its own note prescribed the repair used here.
#
#  THE OBVIOUS RE-PIN, `how == "exit0"', IS WORSE, and this is the part that had to be
#  built rather than argued.  A one-token reinstatement of the death as exit(0) prints
#  the announce and then dies; exit status CANNOT distinguish "declined, then quit"
#  from "died with status 0".  MEASURED, variant `mexit0': the exit0+txt oracle scores
#  GREEN (how=exit0, txt=True) while alive=False.  Filed as `exit0oracle'.
#
#  SO THE ROW PINS THREE THINGS:
#    how    the host survives the declined WRITE;
#    txt    ONE CONTIGUOUS literal, address and data field included.  Two independent
#           substring tests are a weaker claim: "-- declined." is emitted by the six
#           #497 width declines and by #498's sgi_de decline as well, and this probe's
#           own decl() helper exists because a bare substring cross-matches;
#    v0     a declined READ REACHES THE COMMON TAIL and lands a DEFINED 0.  v0 is
#           preset to SENTINEL by load(), so "wrote odata (0)" and "never landed" are
#           distinguishable -- the same reason the `lw surv' rows carry it.  This is
#           what kills `mret0' (return 0 -> memory_rw.c coerces to -1 -> EXCEPTION_DBE)
#           and `mrdexit0' (exit(0) in the READ branch only), neither of which any
#           write-only oracle can see.
#
#  ORDER PROOF: the new oracle was measured RED on the COMMITTED pre-#499 build BEFORE
#  the code changed -- table500b.out, variant `base', got=exit1/notxt/died against
#  want=exit0/txt/0x0.  And it is not fitted to the fix either: it was PRE-REGISTERED
#  by #497 in commit 112867a (2026-08-30 22:41), six hours before #499's baseline
#  3ded1e8, in the very note this comment replaces.
#
#  CONTRACT -- so a later escape is a breach or an exclusion, not an argument.  This
#  row covers the catch-all's WRITE announce and the READ tail-return.  It does NOT
#  pin the LATCH (one access per direction here, so first == only) nor the READ
#  announce text.  Those live in sgi_re_unmapped_probe.py (`wr lat1', `rd lat1',
#  `rd decl'), WHICH MUST BE GATE-WIRED -- unwired, that coverage exists nowhere. ***
DECL_W = ("unimplemented write to address 0x1800, "
          "data=0x0000000012345678 -- declined.  (once) ]")
t, alive, how = session(store(A, OUTSIDE) + load(A, OUTSIDE) + ["print v0"])
got = "%s/%s/%s" % (how, "txt" if t.count(DECL_W) == 1 else "notxt",
                   printed(t, "v0") if alive else "died")
row("other decl", got, "exit0/txt/0x0",
    "#499: declines, announces once, declined read lands a defined 0")

#  *** L2 -- A FLOOR BREACH FOUND BY THE PASS-2 PANEL, REPAIRED IN-ROUND. ***
#
#  Clause (d)'s DEPENDS-ON closure includes `d->warned', and -- AT THE TIME OF PASS 2 --
#  `tex xbit' swept the six *_LEN bits only.  (It now fires bits 0-10; see that row.  The
#  past tense is deliberate: this paragraph records why the repair was needed.)  The panel named the escape and predicted its score: give the TEX
#  read decline an ALREADY-USED NON-LEN bit --
#
#      SGIRE_W_TEX_RD = 1 << 11   ->   1 << 8   (= SGIRE_W_UNMAP_RD)
#
#  -- and the 44-row detector scores a CLEAN SWEEP, because its four TEX-read scenarios
#  and its unmapped-read scenario NEVER SHARE AN EMULATOR INSTANCE.  `tex xbit' sets bits
#  0-5, so bit 8 is clear in every session that reads TEX.  M10 established detection of a
#  WIDTH-bit collision, not of every existing-bit collision.
#
#  The repair is a SAME-INSTANCE sequence in BOTH orderings: whichever announce fires
#  first must not suppress the other.  One ordering alone would leave the mirror open --
#  the `#499' shape, where a repair closes the cell the mutant used and leaves its twin.
DECL_R = "unimplemented read from address 0x1800 -- declined.  (once) ]"

for nm, first, second in (("tex/unmap", TEX_BASE, OUTSIDE),
                          ("unmap/tex", OUTSIDE, TEX_BASE)):
    A = Addr(CODE)
    t, alive, how = session(load(A, first, OP_LD_V0_AT) + load(A, second, OP_LD_V0_AT))
    got = "%i/%i" % (t.count(TEX_RD_DECL), t.count(DECL_R)) if alive else "died"
    row(nm, got, "1/1",
        "LATCH INDEPENDENCE: both announces fire in ONE instance, either order")

ok = sum(1 for _, o in rows if o)
print("")
print("OPUS497T_RESULT=%d/%d" % (ok, len(rows)))
print("OPUS497T_LABEL=%s" % LABEL)
print("OPUS497T_DONE")
