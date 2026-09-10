#!/usr/bin/env python3
#
#  lcabadval -- RUNG-3 WITNESS: SIX value-guarded write arms in `dev_lca.c' end the host process
#  on values the 21066/21066A hardware manual makes LEGAL, one of which the manual REQUIRES SROM
#  to write.
#
#  THE DEFECT.  `DEVICE_ACCESS(lca_ioc)' has six write arms of this shape:
#
#      case LCA_IOC_W_MASK0:
#              ...
#              d->window_mask_0 = idata;          <-- STORED FIRST, unconditionally
#              if (idata != 0x700000ULL) {
#                      fatal("TODO: LCA_IOC_W_MASK0 value differs (0x%" PRIx64") from the only"
#                            " implemented value\n", (uint64_t)idata);
#                      exit(1);                   <-- then the process ends
#              }
#
#  The accepted sets, as enumerated from the predicates themselves (NOT from a table):
#
#      arm         offset   predicate                              accepted set
#      IOC_CONF    +0x020   idata & ~1                             {0, 1}
#      IOC_TB_ENA  +0x0a0   idata & ~IOC_TB_ENA_TEN   (~0x80)      {0, 0x80}
#      W_BASE0     +0x100   idata != 0 && idata != 0x300800000     {0, 0x300800000}
#      W_MASK0     +0x140   idata != 0x700000                      {0x700000}
#      W_BASE1     +0x120   idata != 0x240000000                   {0x240000000}
#      W_MASK1     +0x160   idata != 0x3ff00000                    {0x3ff00000}
#
#  *** THE GUARDS ARE WRONG, NOT MERELY HARSH, AND THE MANUAL IS WHAT SAYS SO. ***  Every `legal'
#  row below drives a value the 21066/21066A HRM documents as legal for that register, and each
#  one cites its own line in `_scratchpad/21066_66a_hrm.txt'.  The sharpest is W_BASE1: S6.4.14
#  item 3 (:10791-10792) says SROM "Prevents the IOC from responding to itself by writing zero to
#  the IOC_W_BASE1 and IOC_W_BASE0 registers".  ZERO IS THE VALUE THE INITIALISATION SEQUENCE IS
#  REQUIRED TO WRITE, and at W_BASE1 it ends the emulator.  It is also the value the model's own
#  register reads back before anyone writes it, so writing back what you just read is fatal.
#
#  THE MANUAL VALUES USED, each verified by reading the cited lines rather than taken from a seat:
#
#    CONF    -> 2      Table 6-10 (:10246-10254): bits <1:0> are the CFG AD<1:0> FIELD, so all
#                      four encodings are legal.  S6.2.9 (:9217) says the same from the other end.
#                      The guard accepts HALF of a documented two-bit field.
#    TB_ENA  -> 0x81   Table 6-13 (:10443, :10453): bits 63:8 and 6:0 are RES of type X, and the
#                      manual's own type legend (:985-988) defines X as "return UNPREDICTABLE
#                      results when read and are IGNORED ON WRITE OPERATIONS".  0x81 differs from
#                      the accepted 0x80 in exactly one bit the hardware is documented to IGNORE.
#    W_BASE0 -> 0x280000000    Figure 6-9 (:10556-10560) and Table 6-16 (:10562-10583): WEN is
#                      bit 33, SG bit 32, W_BASE<31:20> bits 31:20.  So this is WEN set, direct
#                      mapping (SG clear), window base 0x80000000 -- naturally aligned to any
#                      window size up to 2 GB, as :10538-10539 requires, and not overlapping the
#                      base the fork accepts at the sibling register (:10540-10541).  Zero cannot
#                      be used here: W_BASE0's guard is the one arm of the six that accepts it.
#    W_MASK0 -> 0x100000       Table 6-6 (:9587), encoding `0000 0000 0001' = 2 MB window.
#    W_BASE1 -> 0              S6.4.14 item 3 (:10791-10792), the SROM-required value.
#    W_MASK1 -> 0xfff00000     Table 6-6 (:9598), encoding `1111 1111 1111' = 4 GB window.
#
#  Table 6-6 lists THIRTEEN legal W_MASK encodings (:9586-9598).  W_MASK0 accepts one of them and
#  W_MASK1 accepts a different one, so TWELVE OF THIRTEEN are fatal at each register and neither
#  register accepts the other's value.  DERIVE IT, do not trust this sentence:
#      awk 'NR>=9586 && NR<=9598' _scratchpad/21066_66a_hrm.txt | wc -l      -> 13
#  and each arm's predicate is a single `!=' against one constant, so the accepted set has size 1.
#  (Note 1 MB is the encoding `0000 0000 0000' = 0x0, so writing ZERO to either mask register is a
#  legal window size and is also fatal.)
#
#  *** THE FIGURE/TABLE STAGGER WAS CHECKED, NOT ASSUMED. ***  `pdftotext -layout' staggers
#  Table 6-16's descriptions against its bit rows (:10566-10583 reads WEN's description beside
#  SG's row), which is the extraction artefact the carrier warns about.  It is NOT relied on: the
#  UNSTAGGERED Figure 6-9 (:10556-10560) gives the layout directly, and this tree's own
#  `alpha_lcareg.h' independently pins IOC_W_BASE_WEN = bit 33, IOC_W_BASE_SG = bit 32,
#  IOC_W_BASE_W_BASE = bits 31:20.  Three sources agree, so no single calibration point is
#  load-bearing here.
#
#  ---------------------------------------------------------------------------------------------
#  *** WHAT THIS IS AND IS NOT.  IT IS A WITNESS, NOT A DETECTOR. ***
#
#  It establishes: on unmodified `alphabook1', ONE ordinary guest `stq' of a manual-legal value to
#  a documented LCA IOC register ends the host process, with that arm's own diagnostic as
#  evidence, after the SAME register at the SAME width through the SAME path has just been proven
#  live in the SAME process.  It does NOT establish that any shipped guest writes these values,
#  and it is NOT a detector of the repair: `alive' greens equally for a silent accept, for a
#  latched announce, for a decline that discards the value, and for a full implementation.  A fix
#  round owes rows that discriminate those -- at minimum a readback row per arm proving what the
#  repair did with the value, and a latch-count row if the disposition is a bounded announce.
#
#  THE STORE-BEFORE-CHECK IS VISIBLE IN THE SOURCE AND IS DELIBERATELY NOT ROWED HERE.  Every arm
#  assigns `d->field = idata' before testing it, so on HEAD the rejected value is already in the
#  struct when exit(1) runs -- but the process ends, so no guest can observe it and no row can
#  either.  It becomes observable only once the kill goes, which makes it a FIX-round row (does
#  the repair leave the register holding the refused value?), not a witness row.  Recorded so the
#  fix round does not have to rediscover it.
#
#  ---------------------------------------------------------------------------------------------
#  SHAPE: ONE PROCESS PER ARM, CONTROL FIRST, and every element of it was paid for by a sibling
#  probe in this tree.
#
#    1.  ONE PROCESS, NOT TWO.  [A] pre-read, [B] accepted store, [C] read-back and [D] the
#        killing store all happen in the SAME emulator run, so between the store that LIVES and
#        the store that DIES only the VALUE differs -- not the address, not the width, not the
#        path, not the process.  Two sessions would leave a residual that something else differed.
#    2.  THE PAIR IS THE ORACLE.  A bare "the register read back 0x700000" row would be weak;
#        UNMAPPED space and a missed device both read 0 (`memory_rw.c''s #95 pre-zero), and a
#        bare zero proves nothing.  `<arm> live' asserts the TRANSITION 0x0 -> <accepted value>
#        from the same address in the same process, which nothing but the device can produce.
#        All six accepted values are NONZERO, so every `live' row carries a device signature.
#    3.  STAY ON `step'.  #516 de-fatalised the two ISA interrupt stubs, so they are no longer
#        confounders -- but `continue' would still let a host-timer tick reach code this probe is
#        not testing, and the witness costs nothing by stepping.
#    4.  EVERY ACCESS IS A GUEST INSTRUCTION.  Debugger `dump' skips DM_DEFAULT handlers and
#        `lca_ioc' is registered DM_DEFAULT, so `dump' would read the pre-zero and make the
#        window look unmapped.  A debugger `put d' of a killing value IS a host kill but is NOT a
#        guest access and witnesses nothing.  Every `put d' below targets SCRATCH, which is RAM.
#    5.  ATTRIBUTION IS BY THE ARM'S OWN TEXT, NEVER BY EXIT STATUS.  A wrong offset would fall
#        into `default:' and die with "[ lca_ioc: unimplemented write to offset ... ]" -- a death
#        for a DIFFERENT reason, which is a FAILED reproduction.  Each `<arm> attrib' row is green
#        in both directions by construction and reds only if the host died WITHOUT that arm's
#        diagnostic.  All six literals were verified unique in `src/' (one hit each).
#
#  THE NEGATIVE CONTROL IS `W_T_BASE0' (+0x180), and the VALUE is chosen to make it work hard:
#  it is written 0x100000 -- the very value that kills at W_MASK0 two rows up.  W_T_BASE0 is an
#  implemented case in the same switch, in the same handler, with no value guard, so the pair
#  attributes the deaths to THE ARM'S PREDICATE rather than to the value, to the width, to K0SEG,
#  or to writing into the IOC window at all.  (0x100000 is also a legal page-table base for that
#  register: IOC_W_T_BASE is bits 31:10, so a 1 MB-aligned value is well-formed.)
#
#  Usage:  lca_badval_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"          #  device_add(machine, "lca") is ST_ALPHABOOK1 ONLY

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-24s %-24s %-52s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder (memory format only)
ZERO, T0, T1, T2, T3, T4, T5 = 31, 1, 2, 3, 4, 5, 6
#  T5 is the highest used.  A probe reaching for an undefined register name dies with a NameError
#  rather than emitting a bad encoding, which is the safe direction (#516 found this the hard way).

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
#  QUADWORD ONLY, and that is architectural rather than a preference: HRM S6.4 says the IOC
#  registers are accessed with quadword operations, so LDL/STL are excluded by the manual.

def load_const(reg, val):
    #  32-bit only, and deliberately so: this builds the SCRATCH pointer, never a 64-bit operand.
    #  Every operand this probe drives is 64-bit-capable and arrives via `put d' + LDQ.
    lo = val & 0xffff
    hi = (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

# ---------------------------------------------------------------- addresses (ALL RAM < 64 MB)
K0SEG        = 0xfffffc0000000000
def k0(p):   return K0SEG | p

LCA_IOC_BASE  = 0x180000000              # alpha_lcareg.h; DEVINIT maps 0x20000000 bytes here
IOC_CONF      = LCA_IOC_BASE + 0x020
IOC_TB_ENA    = LCA_IOC_BASE + 0x0a0
IOC_W_BASE0   = LCA_IOC_BASE + 0x100
IOC_W_BASE1   = LCA_IOC_BASE + 0x120
IOC_W_MASK0   = LCA_IOC_BASE + 0x140
IOC_W_MASK1   = LCA_IOC_BASE + 0x160
IOC_W_T_BASE0 = LCA_IOC_BASE + 0x180     # the negative control: implemented, NO value guard

SCRATCH      = 0x01020000
CODE         = 0x01040000

assert max(SCRATCH, CODE) < 64 * 1024 * 1024, "scratch/code must be inside RAM"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- session
def session(cmds, settle=1.6, spin=2.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
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
        if not rd(spin if i == len(cmds) - 1 else 0.35):
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

# ---------------------------------------------------------------- the per-arm driver
#  Register discipline, copied from lca_confbus_probe.py: T0 holds the SCRATCH base and is read
#  for the LAST time by the third LDQ, so every operand is in a register before anything else
#  happens.  The four accesses are labelled [A]..[D] here and in the report.
def arm(addr, accepted, legal, settle=1.6, spin=2.2):
    setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(addr)),
             "put d 0x%x, 0x%x" % (SCRATCH + 8,  accepted),
             "put d 0x%x, 0x%x" % (SCRATCH + 16, legal)]
    prologue = load_const(T0, SCRATCH) + [
        LDQ(T1, 0,  T0),    # t1 = k0(register)
        LDQ(T4, 8,  T0),    # t4 = the ACCEPTED value
        LDQ(T5, 16, T0),    # t5 = the manual-LEGAL value  (T0 is dead after this)
        LDQ(T2, 0,  T1),    # [A] PRE-read       -- must be 0 (the model memsets its state)
        STQ(T4, 0,  T1),    # [B] ACCEPTED store -- must survive
        LDQ(T3, 0,  T1)]    # [C] READ-BACK      -- must echo the accepted value
    armed = [STQ(T5, 0, T1)]  # [D] the manual-LEGAL store -- ends the host on HEAD
    cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op)
                    for i, op in enumerate(prologue + armed)]
    cmds += ["pc=0x%x" % k0(CODE),
             "step %d" % len(prologue),   # up to and including the read-back
             "print t2",                  # [A], while the host is certainly still alive
             "print t3",                  # [C], likewise
             "step %d" % len(armed)]      # [D]
    txt, alive = session(cmds, settle, spin)
    return txt, alive, printed(txt, "t2"), printed(txt, "t3")

def evidence(txt):
    #  *** ECHO THE EVIDENCE INTO THIS LOG. ***  lca_confbus_probe.py shipped an attribution row
    #  whose only evidence was a pty buffer nobody preserved -- a green row a later reader cannot
    #  check.  Every diagnostic this handler can emit is printed here instead.
    for _l in txt.split(chr(10)):
        if "TODO:" in _l or "lca_ioc:" in _l or "[ lca:" in _l:
            print("  EVIDENCE: %s" % _l.strip())

print("lca_badval_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-24s %-24s %-52s %s" % ("row", "got", "want", "note", ""))

# ---------------------------------------------------------------- the six arms
#  (label, address, accepted value, manual-legal value, this arm's UNIQUE fatal() literal,
#   the note that says what the `legal' row proves)
ARMS = [
    ("conf",   IOC_CONF,    0x1,          0x2,
     "Write to unimplemented bit of",
     "CFG AD<1:0> is a 2-bit FIELD (T6-10 :10250); 2 of 4 encodings kill"),
    ("tbena",  IOC_TB_ENA,  0x80,         0x81,
     "LCA_IOC_TB_ENA value",
     "bit 0 is RES type X = IGNORED ON WRITE (legend :985, T6-13 :10453)"),
    ("wbase0", IOC_W_BASE0, 0x300800000,  0x280000000,
     "LCA_IOC_W_BASE0 value differs",
     "WEN + base 0x80000000, aligned (F6-9 :10556; :10538-10539)"),
    ("wmask0", IOC_W_MASK0, 0x700000,     0x100000,
     "LCA_IOC_W_MASK0 value differs",
     "2 MB window, Table 6-6 :9587 -- 12 of 13 legal encodings kill"),
    ("wbase1", IOC_W_BASE1, 0x240000000,  0x0,
     "LCA_IOC_W_BASE1 value differs",
     "*** THE SROM-REQUIRED VALUE, S6.4.14 item 3 :10791-10792 ***"),
    ("wmask1", IOC_W_MASK1, 0x3ff00000,   0xfff00000,
     "LCA_IOC_W_MASK1 value differs",
     "4 GB window, Table 6-6 :9598 -- MASK0's own value kills here too"),
]

for label, addr, accepted, legal, sig, why in ARMS:
    txt, alive, pre, post = arm(addr, accepted, legal)

    #  ---- LIVENESS + DEVICE SIGNATURE, in one row -------------------------------------------
    #  The PAIR is the oracle: unmapped space and a missed device both read 0 forever, so only a
    #  live device can turn 0x0 into a nonzero value it was just handed.  This also proves the
    #  ACCEPTED store did not kill -- which is what makes the death two rows down attributable to
    #  the VALUE and to nothing else about the access.
    row("%s live" % label, "%s->%s" % (pre, post), "0x0->0x%x" % accepted,
        "LIVENESS+DEVSIG: same addr/width/process; only a device echoes this")

    #  ---- THE DEFECT ROW ---------------------------------------------------------------------
    #  ORACLE POLARITY: the witness ladder requires the symptom on the PRE-FIX build and green
    #  post-fix with the SAME script, so this asserts the CORRECT behaviour.
    #  PRE-FIX -> "dead" -> RED.   POST-FIX -> "alive" -> GREEN.
    row("%s legal" % label, "alive" if alive else "dead", "alive", why)

    #  ---- ATTRIBUTION: if it died, it died HERE ----------------------------------------------
    #  Green in BOTH directions by construction; RED only if the host died WITHOUT this arm's
    #  diagnostic -- i.e. "did it fail for the reason under test?"  A wrong offset lands in
    #  `default:' and reds this row instead of quietly passing as a reproduction.
    hit = (sig in txt)
    row("%s attrib" % label, "yes" if (alive or hit) else "died-elsewhere", "yes",
        "ATTRIBUTION: a death here must carry THIS arm's unique diagnostic")
    evidence(txt)

# ---------------------------------------------------------------- the negative control
#  W_T_BASE0 is an implemented case in the SAME switch with NO value guard, and it is handed the
#  value that kills at W_MASK0.  If this died too, the deaths above would be about the window or
#  the width rather than about the predicates, and the whole witness would be void.
CTLVAL = 0x100000
txtc, alivec, prec, postc = arm(IOC_W_T_BASE0, CTLVAL, CTLVAL)

row("ctl noguard", "alive" if alivec else "dead", "alive",
    "CONTROL: same window, same width, an arm with NO value guard")
row("ctl echo", "%s->%s" % (prec, postc), "0x0->0x%x" % CTLVAL,
    "CONTROL: the value that KILLS at W_MASK0 is stored and echoed here")
evidence(txtc)

# ================================================================ #518 DETECTOR ROWS
#  The rows above are the WITNESS (RED on HEAD 74daefd at 14/20, GREEN on the fix with the same
#  script).  The rows below DEFEND the fix -- they are what a kill table is scored against -- and
#  each names the mutant it kills and the observable that differs (the CHANNEL line).
#
#  CONTRACT (clause (e)).  Designed to catch, per arm: (b) the verbatim kill reinstated (the
#  `stored' rows die); (d) the STORE MASK narrowed (CONF `& 0x3' -> `& 0x1' loses bit 1; TB_ENA
#  storing the raw value keeps 0x81; W_BASE dropping WEN/SG or truncating to 32 bits; W_MASK
#  `& 0xfff00000' widened or narrowed); (d) the W_MASK FIELD RULE weakened (`f != 0' accepts
#  0x500000; `f == 1' declines 0xfff00000) or the old STORE-BEFORE-CHECK order reinstated (the
#  declined value is kept instead of the previous one); (d) the latch bits COLLAPSED (the second
#  register's, or the second direction's, announce never prints) or the latch REMOVED (a second
#  identical write announces twice); (d) the default arm declining reads to nonzero or writing
#  state.  NOT rowed, disclosed: the SG bit's effect (nothing consumes it), the W_T_BASE arms
#  (unchanged, and the negative control already pins one), the reserved bits ABOVE bit 33 of
#  W_BASE (dropped by the same mask as the ones below it -- one row per mask, not per bit), and
#  the `ofs > len' exit in lca_isa, which belongs to lcaisalane.  Every value here is QUADWORD.
#
#  WHAT THE READ-BACKS ARE, stated so nobody reads them as architecture (grok, pass 2): the HRM
#  types these registers WO, readback UNPREDICTABLE (:980-988).  The model has always echoed the
#  stored value; every `stored'/`widen'/`declined' row tests THAT ECHO POLICY, which is what the
#  fix wrote into and what a mutant would change -- it is not a claim about hardware readback.
#
#  Session shape: T0 = SCRATCH base (live throughout), T1 = address, T2 = value, T3 = read-back;
#  each phase reloads T1/T2 from a `put d' slot, so eight registers are never a constraint.  A
#  phase is stepped as a block and its read-back printed while the host is certainly alive.

def seq(consts, phases, settle=1.6, spin=2.2):
    """consts: list of 64-bit values -> SCRATCH slots 0,8,16,...  phases: list of lists of
    (op, addr_slot, val_slot) with op in {'st', 'ld'}; each phase ends with `print t3'.
    Returns (txt, alive, [read-backs in phase order as strings])."""
    setup = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    prog = load_const(T0, SCRATCH)
    lens = [len(prog)]
    for ph in phases:
        ops = []
        for op, a, v in ph:
            ops.append(LDQ(T1, 8 * a, T0))
            if op == "st":
                ops.append(LDQ(T2, 8 * v, T0))
                ops.append(STQ(T2, 0, T1))
            else:
                ops.append(LDQ(T3, 0, T1))
        prog += ops
        lens.append(len(ops))
    cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for n in lens[1:]:
        cmds += ["step %d" % n, "print t3"]
    txt, alive = session(cmds, settle, spin)
    vals = ["0x%x" % int(m, 16) for m in
            re.findall(r"print\s+t3\s*\n\s*(0x[0-9a-f]+)", txt)]
    return txt, alive, vals

def nth(vals, i):
    return vals[i] if i < len(vals) else "absent"

def announces(txt, needle):
    return txt.count(needle)

#  ---- D1: the STORED value per arm -- accepted, then manual-legal, then read back -------------
#  KILLS: (b) reinstated kill (dies); (d) mask narrowed / raw store / declined-not-stored (reads
#  the accepted value or the raw one).  The want is the NORMALIZED legal value: for TB_ENA 0x81
#  reads back 0x80, which is the reserved-bit rule in one row.
NORMAL = {"conf": 0x2, "tbena": 0x80, "wbase0": 0x280000000, "wmask0": 0x100000,
          "wbase1": 0x0, "wmask1": 0xfff00000}
for label, addr, accepted, legal, sig, why in ARMS:
    txt, alive, vals = seq([k0(addr), accepted, legal],
                           [[("st", 0, 1)], [("st", 0, 2), ("ld", 0, 0)]])
    row("%s stored" % label, nth(vals, 1) if alive else "dead", "0x%x" % NORMAL[label],
        "accepted then legal: reads back the NORMALIZED legal value (fields kept, RES dropped)")
    evidence(txt)

#  ---- D2: unsupported W_MASK encodings are DECLINED, the previous value KEPT, once per register --
#  KILLS: field rule weakened to `f != 0' (0x500000 stored); store-before-check reinstated (reads
#  0x500000); latch removed (two announces); MASK0/MASK1 latch bits collapsed (MASK1 never
#  announces after MASK0 did, in the SAME session).
DECL0, DECL1 = "IOC_W_MASK0 encoding declined", "IOC_W_MASK1 encoding declined"
txt, alive, vals = seq([k0(IOC_W_MASK0), 0x100000, 0x500000, 0x900000,
                        k0(IOC_W_MASK1), 0xfff00000, 0x200000],
                       [[("st", 0, 1), ("st", 0, 2), ("ld", 0, 0)],      # phase 0: legal, bad, read
                        [("st", 0, 3), ("ld", 0, 0)],                     # phase 1: second bad, read
                        [("st", 4, 5), ("st", 4, 2), ("st", 4, 3), ("ld", 4, 4)],   # phase 2: MASK1 legal, bad, bad, read
                        [("st", 0, 6), ("ld", 0, 0)]])                            # phase 3 (codex): f = 2 at MASK0
row("wmask0 declined", nth(vals, 0) if alive else "dead", "0x100000",
    "0x500000 (field 101b) declined: previous legal value KEPT, host alive")
row("wmask0 once", announces(txt, DECL0) if alive else "dead", 1,
    "TWO unsupported writes announce EXACTLY ONCE -- the (once) latch")
row("wmask0 kept2", nth(vals, 1) if alive else "dead", "0x100000",
    "the second unsupported write also leaves the previous value")
row("wmask1 declined", nth(vals, 2) if alive else "dead", "0xfff00000",
    "MASK1: 0x500000 declined after 0xfff00000 stored")
row("wmask1 indep", announces(txt, DECL1) if alive else "dead", 1,
    "MASK1 still announces after MASK0 did -- independent latch bits")
row("wmask0 f2", nth(vals, 3) if alive else "dead", "0x100000",
    "PASS 2 (codex): field 0b10 is NOT a Table 6-6 encoding; a rule weakened to admit it (== 0 -> <= 2) stores 0x200000")
row("wmask1 once", announces(txt, DECL1) if alive else "dead", 1,
    "PASS 2 (glm): TWO unsupported MASK1 writes announce ONCE -- pins MASK1 latch REMOVED, not only shared")
evidence(txt)

#  ---- D3: IOC_CONF reserved bits dropped, bit 1 kept and announced once ----------------------
#  KILLS: mask narrowed to bit 0 (reads 0x0 or 0x1); raw store (reads 0x100000002); latch removed.
CFG1 = "IOC_CONF<1> set"
txt, alive, vals = seq([k0(IOC_CONF), 0x1, 0x100000002, 0x2],
                       [[("st", 0, 1), ("st", 0, 2), ("ld", 0, 0)],
                        [("st", 0, 3), ("ld", 0, 0)]])
row("conf reserved", nth(vals, 0) if alive else "dead", "0x2",
    "0x100000002: reserved bit 32 DROPPED, CFG<1> kept")
row("conf once", announces(txt, CFG1) if alive else "dead", 1,
    "two writes with CFG<1> set announce EXACTLY ONCE")
evidence(txt)

#  ---- D4: enabling a window announces ONCE across both registers; BASE0 accepts SROM's zero ---
#  KILLS: WEN latch removed (two announces); per-register WEN latches (also two); BASE0 zero
#  refused.  0x240000000 has bit 33 (WEN) set, so the accepted W_BASE1 value enables a window.
WEN = "a DMA window was enabled"
txt, alive, vals = seq([k0(IOC_W_BASE0), 0x280000000, k0(IOC_W_BASE1), 0x240000000, 0x0],
                       [[("st", 0, 1), ("st", 2, 3), ("ld", 2, 2)],
                        [("st", 0, 4), ("ld", 0, 0)]])
row("wen once", announces(txt, WEN) if alive else "dead", 1,
    "BASE0 then BASE1 both with WEN: the not-modelled announce prints ONCE")
row("wbase1 wen", nth(vals, 0) if alive else "dead", "0x240000000",
    "BASE1's accepted value round-trips with WEN (bit 33) intact")
row("wbase0 zero", nth(vals, 1) if alive else "dead", "0x0",
    "SROM's required zero lands at BASE0 too (S6.4.14 item 3)")
evidence(txt)

#  ---- D5: the default arm -- write declined, read answers zero, each direction latched -------
#  KILLS: reinstated kill; a default arm that stores or returns nonzero; the two direction
#  latches collapsed (the read never announces after the write did); latch removed (two writes
#  announce twice).  +0x1e0 is inside DEVINIT's window and names no register in alpha_lcareg.h.
UNL = LCA_IOC_BASE + 0x1e0
DEFW, DEFR = "unimplemented write to offset 0x1e0", "unimplemented read to offset 0x1e0"
txt, alive, vals = seq([k0(UNL), 0x5a5a5a5a5a5a],
                       [[("st", 0, 1), ("st", 0, 1)],
                        [("ld", 0, 0), ("ld", 0, 0)]])   # PASS 2: TWO reads, so the read latch REMOVED is pinned too
row("def alive", "alive" if alive else "dead", "alive",
    "two writes to an unlisted IOC offset survive")
row("def w once", announces(txt, DEFW) if alive else "dead", 1,
    "the declined write announces EXACTLY ONCE for two writes")
#  PASS 2 (kimi substitute): this read nth(vals, 0) -- the print after the STORE-ONLY phase 0, a
#  STALE t3 -- so M20_def_echo passed it.  The load is in phase 1; index 1 is the read-back.
row("def width", "yes" if ("0x5a5a5a5a5a5a" in txt) else "no", "yes",
    "PASS 2 (codex): the declined-write announce prints the FULL 64-bit value; a (int) narrowing prints 0x5a5a5a5a")
row("def read0", nth(vals, 1) if alive else "dead", "0x0",
    "a read of the unlisted offset answers ZERO, not the written value")
row("def r once", announces(txt, DEFR) if alive else "dead", 1,
    "two reads announce ONCE on the read direction OWN latch bit, after the write did")
evidence(txt)


#  ---- D6 (PASS 2 additions, 2026-09-10): the mask cells the first block did not drive -----------
#  Named by four packet-fed seats against my own enumeration.  KILLS: SG dropped from the W_BASE
#  mask (deepseek/kimi/minimax: no row drove bit 32); masks WIDENED (minimax: CONF `& 0x3' -> `& 0x7';
#  W_BASE keeping bit 34; W_MASK `& 0xfff00000' -> `& 0xfffff000'); the field taken from idata
#  instead of v (glm: `f = idata >> 20' declines a legal value that carries bit 32); a TB_ENA
#  no-store (kimi: the accepted 0x80 equals the normalized legal value, so `tbena stored' cannot see
#  a skipped store -- this row writes 0x80 then the reserved-only 0x01 and wants TEN CLEAR).
txt, alive, vals = seq([k0(IOC_CONF), 0x6, k0(IOC_TB_ENA), 0x80, 0x01,
                        k0(IOC_W_BASE0), 0x380000000, 0x680000000,
                        k0(IOC_W_MASK0), 0x1f0000, 0x100100000],
                       [[("st", 0, 1), ("ld", 0, 0)],                 # conf 0x6 -> 0x2
                        [("st", 2, 3), ("st", 2, 4), ("ld", 2, 2)],   # tbena 0x80 then 0x01 -> 0x0
                        [("st", 5, 6), ("ld", 5, 5)],                 # wbase0 SG|WEN|base -> same
                        [("st", 5, 7), ("ld", 5, 5)],                 # wbase0 bit 34 set -> dropped
                        [("st", 8, 9), ("ld", 8, 8)],                 # wmask0 low bits -> dropped
                        [("st", 8, 10), ("ld", 8, 8)]])               # wmask0 bit 32 -> dropped, field legal
row("conf widen", nth(vals, 0) if alive else "dead", "0x2",
    "0x6 reads 0x2: a mask WIDENED to bit 2 stores it (minimax)")
row("tbena clear", nth(vals, 1) if alive else "dead", "0x0",
    "0x80 then 0x01 reads 0x0: TEN cleared by a reserved-only write; a NO-STORE reads 0x80 (kimi)")
row("wbase0 sg", nth(vals, 2) if alive else "dead", "0x380000000",
    "SG|WEN|base round-trips: the SG bit (32) is stored (deepseek)")
row("wbase0 widen", nth(vals, 3) if alive else "dead", "0x280000000",
    "bit 34 set reads dropped: reserved bits ABOVE 33 are not stored (deepseek Q6, minimax)")
row("wmask0 widen", nth(vals, 4) if alive else "dead", "0x100000",
    "0x1f0000 reads 0x100000: bits 19:16 below the mask are not stored (minimax); first draft wrote 0x100f0000 = bit 28, declined")
row("wmask0 hif", nth(vals, 5) if alive else "dead", "0x100000",
    "0x100100000 reads 0x100000: bit 32 is masked BEFORE the field test (glm: f = idata >> 20 declines it)")
row("wen base0", announces(txt, WEN) if alive else "dead", 1,
    "BASE0 ALONE enables (twice) in this session: the announce prints once -- pins BASE0's own announce (grok)")
evidence(txt)

#  ---- D7 (PASS 2): all six announces in ONE process -- any two latch bits shared reds the later --
#  kimi Q4.5: D2/D5 armed only a SIBLING's bit before the firing write; a cross-arm collision
#  (conf<->wen, mask<->def, ...) was unrowed.  One session fires every announce; each needle once.
txt, alive, vals = seq([k0(IOC_CONF), 0x2, k0(IOC_W_BASE0), 0x280000000,
                        k0(IOC_W_MASK0), 0x500000, k0(IOC_W_MASK1), 0x500000, k0(UNL), 0x5a5a],
                       [[("st", 0, 1), ("st", 2, 3), ("st", 4, 5), ("st", 6, 7), ("st", 8, 9), ("ld", 8, 8),
                         ("st", 0, 1), ("st", 4, 5)]])   # codex: REPEAT conf and mask0 after the others
for _n, _needle in (("all conf", CFG1), ("all wen", WEN), ("all m0", DECL0), ("all m1", DECL1),
                    ("all defw", DEFW), ("all defr", DEFR)):
    row(_n, announces(txt, _needle) if alive else "dead", 1,
        "six announces in one process, then conf and mask0 REPEATED: prints once (bits neither shared nor erased by `=')")
evidence(txt)


#  ---- D8 (PASS 2, grok): BASE1 ALONE enables a window -- the per-label WEN announce ------------
#  D4 enables BASE0 first, so deleting BASE1's announce (or BASE0's) still gives `wen once' = 1.
#  The shared latch bit is the JOIN the 7g-1 discriminator warns about, reached through a shared
#  bit rather than a fall-through label.  Together with `wen base0' (D6) each label's announce is
#  pinned on its own.
txt, alive, vals = seq([k0(IOC_W_BASE1), 0x240000000],
                       [[("st", 0, 1), ("ld", 0, 0)]])
row("wen base1", announces(txt, WEN) if alive else "dead", 1,
    "BASE1 ALONE enables: the announce prints once -- pins BASE1's own announce (grok)")
row("wbase1 alone", nth(vals, 0) if alive else "dead", "0x240000000",
    "and the value round-trips in a session that never touched BASE0")
evidence(txt)

# ---------------------------------------------------------------- summary
#  Computed adjacent to the print on purpose: #516 shipped a probe whose numerator was counted
#  over an older row set while the denominator was evaluated at print time, and every row said
#  `ok' beside a summary that did not.
ok = sum(1 for _, o in rows if o)
print("")
print("LCABADVAL_ARMS=%d" % len(ARMS))
print("LCABADVAL_RESULT=%d/%d" % (ok, len(rows)))
print("LCABADVAL_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("LCABADVAL_DONE")
sys.exit(0 if ok == len(rows) else 1)
