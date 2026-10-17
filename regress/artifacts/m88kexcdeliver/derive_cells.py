# DERIVER for the {switch-1 arm} x {settable PSR bit} cell census of the #502 detector.
#
# WHY THIS EXISTS: my pass-10 packet asserted "the previously-closed 23" with no deriver.  kimi could not
# reconstruct 23 from any artifact and derived 34 of 40 instead.  The carrier's rule is that a count names its
# deriver or carries its method inline; a count I cannot re-derive is exactly the class this round has already
# been bitten by twice today.  So: enumerate the cells mechanically, print the GRID (not the total), and let the
# total fall out of it.  A per-cell breakdown is checkable; a total is not.
#
# THE CELL DEFINITION, and it is the one thing here that is a judgement rather than a transcription:
#   a mutant at arm A conditioning `implemented' on bit B -- in EITHER polarity -- is killed iff two rows enter
#   switch 1 at arm A with DIFFERENT values of B.  So cell (A,B) is CLOSED iff bit B VARIES across the rows that
#   reach arm A.  That is polarity-free, which is why it is the right formulation: v16's comment observes that
#   the open cells "are always (C never set) and (IND never clear)", i.e. the arm's rows AGREE on the bit.
#
# THE ARM A ROW ENTERS IS NOT ITS EXPECTED VECTOR.  Every err*/trapfrozen* row faults TWICE: the first fault
# gets the handler running, the second is the one under test.  The re-route rows then have their vector
# REWRITTEN to ERROR after switch 1, so their expected vector (V_ERROR) names a place they never entered.
# Both faults are recorded below, each with the PSR in force at that moment, sourced from the row's own
# setup/handler in m88k_exc_probe.py.
#
# *** v22 UPDATE, 2026-10-16 (repair 13).  Two seats found this deriver stale in the close adjudication:
# Grok 4.7 -- it stopped at the 57-row instrument and still printed the re-route's trap-side MODE and SFD1 OPEN after
# v19's trapfrozenuser/trapfrozensfd1 closed them (a records defect: its output no longer described the shipped probe);
# Fable 5.1 -- its denominator had NO delay-slot axis, although m88k_exception() TESTS cpu->delay_slot, and that omission
# hid a floor breach (`implemented = !cpu->delay_slot' at MISALIGN/UNIMPL/PRIV/OVF swept v21 59/59 at all four arms,
# artifacts/m88kexcdeliver/delayslot_20261016/).  Both are fixed below; the v16 and v17/v18 reports are kept as history.
MODE, SER, C, SFD1, IND, SFRZ = 0x80000000, 0x20000000, 0x10000000, 0x08, 0x02, 0x01
BITS = [("MODE", MODE), ("SER", SER), ("C", C), ("SFD1", SFD1), ("IND", IND), ("SFRZ", SFRZ)]
ARMS = ["MISALIGN", "UNIMPL", "PRIV", "BOUNDS", "DIV0", "OVF", "ERROR"]

RESET, USER, EXC = 0x80000002, 0x00000002, 0x8000000b
CARRY, INDCLR, SUPCNOIND, SERSUP = 0x90000002, 0x80000000, 0xb0000000, 0xa0000002
FRZSUP, FRZUSER, FRZNOIND, FRZC, FRZSER = 0x80000003, 0x00000003, 0x80000009, 0x9000000b, 0xa000000b

# (row, [(arm, psr_at_that_arm), ...])   -- second entry present only for the two-fault rows
FAULTS = {
 "div0": [("DIV0", RESET)], "ovf": [("OVF", RESET)], "misalign": [("MISALIGN", RESET)],
 "bounds": [("BOUNDS", RESET)], "priv": [("PRIV", USER)], "privtb": [("PRIV", USER)],
 "unimpl": [("UNIMPL", USER)], "dslot": [("DIV0", RESET)], "errortb": [("ERROR", RESET)],
 "misaligntb": [("MISALIGN", RESET)], "unimpltb": [("UNIMPL", RESET)], "div0tb": [("DIV0", RESET)],
 "ovftb": [("OVF", RESET)], "vbrtb": [("BOUNDS", RESET)], "privsuptb": [("PRIV", RESET)],
 "udiv0": [("DIV0", USER)], "ovfc": [("OVF", CARRY)], "indclr": [("OVF", INDCLR)],
 "umisalign": [("MISALIGN", USER)], "uovf": [("OVF", USER)],
 "error":     [("DIV0", RESET), ("MISALIGN", EXC)],
 "errovf":    [("DIV0", RESET), ("OVF", EXC)],
 "errind":    [("DIV0", RESET), ("MISALIGN", FRZNOIND)],
 "errc":      [("DIV0", RESET), ("MISALIGN", FRZC)],
 "errser":    [("DIV0", RESET), ("MISALIGN", FRZSER)],
 "errdiv0":   [("DIV0", RESET), ("DIV0", FRZSUP)],
 "errpriv":   [("DIV0", RESET), ("PRIV", FRZUSER)],
 "errunimpl": [("DIV0", RESET), ("UNIMPL", FRZUSER)],
 "trapfrozen":  [("DIV0", RESET), ("BOUNDS", EXC)],
 "trapfrozen4": [("DIV0", RESET), ("MISALIGN", EXC)],
 "trapfrozen5": [("DIV0", RESET), ("UNIMPL", EXC)],
 "trapfrozen6": [("DIV0", RESET), ("PRIV", EXC)],
 "trapfrozen8": [("OVF", RESET), ("DIV0", EXC)],
 "trapfrozen9": [("DIV0", RESET), ("OVF", EXC)],
 "trapfrozen10":[("DIV0", RESET), ("ERROR", EXC)],
 "trapfrozenind":[("DIV0", RESET), ("BOUNDS", FRZNOIND)],
 "trapfrozenc":  [("DIV0", RESET), ("BOUNDS", FRZC)],
 "trapfrozenser":[("DIV0", RESET), ("BOUNDS", FRZSER)],
 "unimpltbc": [("UNIMPL", SUPCNOIND)], "privtbc": [("PRIV", SUPCNOIND)],
 "boundstbc": [("BOUNDS", SUPCNOIND)], "div0tbc": [("DIV0", SUPCNOIND)],
 "errortbc":  [("ERROR", SUPCNOIND)],  "ovftbser": [("OVF", SUPCNOIND)],
 # rows that reach no switch-1 arm under test: the fallback rows, the user-trap rows, the SFU1 rows.
 # sfu1h and the trapfrozen user-trap rows still fault FIRST at a real arm, so that fault counts.
 "sfu1h": [("DIV0", RESET)], "trapfrozen450": [("DIV0", RESET)], "trapfrozen496": [("DIV0", RESET)],
 "trapfrozen511": [("DIV0", RESET)], "trapfrozen128": [("DIV0", RESET)],
 "resid50": [], "resid127": [], "resid11": [], "resid50ind": [], "resid50c": [], "resid50ser": [],
 "usertb": [], "usfu1": [],
 # v19 (pass 11's L2 repair): the re-route's trap side with MODE clear / SFD1 clear.  trapfrozenuser's SECOND fault is a
 # USER trap (128), which enters no switch-1 arm, so only its first fault counts here; trapfrozensfd1's enters BOUNDS.
 "trapfrozenuser": [("DIV0", RESET)],
 "trapfrozensfd1": [("DIV0", RESET), ("BOUNDS", FRZSUP)],
 # v22 (repair 13): a fault IN A DELAY SLOT at the four other arms an instruction reaches from a slot
 "dslotmisalign": [("MISALIGN", RESET)], "dslotunimpl": [("UNIMPL", USER)],
 "dslotpriv": [("PRIV", USER)], "dslotovf": [("OVF", RESET)],
 # v23 (repair 14): the rest of the delay-slot grid.  The err*/trapfrozen* slot rows fault SECOND, frozen, inside the div0
 # handler; usfu1dslot reaches no switch-1 arm under test (SFU1, the fallback row).
 "dslotbounds": [("BOUNDS", RESET)], "dsloterror": [("ERROR", RESET)],
 "errdslotmisalign": [("DIV0", RESET), ("MISALIGN", EXC)], "errdslotovf": [("DIV0", RESET), ("OVF", EXC)],
 "errdslotdiv0": [("DIV0", RESET), ("DIV0", FRZSUP)], "errdslotpriv": [("DIV0", RESET), ("PRIV", FRZUSER)],
 "errdslotunimpl": [("DIV0", RESET), ("UNIMPL", FRZUSER)],
 "trapfrozen7dslot": [("DIV0", RESET), ("BOUNDS", EXC)], "trapfrozen10dslot": [("DIV0", RESET), ("ERROR", EXC)],
 "usfu1dslot": [],
 # v24 (repair 15): the is_trap axis -- a trap in a slot at the five instruction labels, unfrozen and frozen
 "dslotmisaligntb": [("MISALIGN", RESET)], "dslotunimpltb": [("UNIMPL", RESET)], "dslotprivtb": [("PRIV", RESET)],
 "dslotdiv0tb": [("DIV0", RESET)], "dslotovftb": [("OVF", RESET)],
 "trapfrozen4dslot": [("DIV0", RESET), ("MISALIGN", EXC)], "trapfrozen5dslot": [("DIV0", RESET), ("UNIMPL", EXC)],
 "trapfrozen6dslot": [("DIV0", RESET), ("PRIV", EXC)], "trapfrozen8dslot": [("OVF", RESET), ("DIV0", EXC)],
 "trapfrozen9dslot": [("DIV0", RESET), ("OVF", EXC)],
 "sfu1hdslot": [("DIV0", RESET)],
}
V16_ONLY = {"ovftbser", "resid50ser", "errser"}     # the three rows v17 ADDED
V19_ROWS = {"trapfrozenuser", "trapfrozensfd1"}      # the two rows v19 added
V22_ROWS = {"dslotmisalign", "dslotunimpl", "dslotpriv", "dslotovf"}   # the four rows v22 added
V23_ROWS = {"dslotbounds", "dsloterror", "errdslotmisalign", "errdslotovf", "errdslotdiv0", "errdslotpriv",
            "errdslotunimpl", "trapfrozen7dslot", "trapfrozen10dslot", "usfu1dslot"}   # the ten rows v23 added
V24_ROWS = {"dslotmisaligntb", "dslotunimpltb", "dslotprivtb", "dslotdiv0tb", "dslotovftb", "trapfrozen4dslot",
            "trapfrozen5dslot", "trapfrozen6dslot", "trapfrozen8dslot", "trapfrozen9dslot", "sfu1hdslot"}   # v24, eleven
V16_PSR = {"unimpltbc": 0x90000000, "privtbc": 0x90000000, "boundstbc": 0x90000000,
           "div0tbc": 0x90000000, "errortbc": 0x90000000}   # SUPCNOIND before v17 ORed SER in

def census(rows, psr_override):
    seen = {}                       # arm -> bit -> set of values observed
    for r in rows:
        for (arm, psr) in FAULTS.get(r, []):
            if arm not in ARMS: continue
            psr = psr_override.get(r, psr) if len(FAULTS[r]) == 1 else psr
            for (bn, bv) in BITS:
                seen.setdefault(arm, {}).setdefault(bn, set()).add(1 if (psr & bv) else 0)
    return seen

# NAME-SET CHECK (Fable 5.1, pass 16): the hand table above must name exactly the probe's fault rows.  The unsafe
# direction is a row deleted from the probe and left here, which this census would still print as ROWED.
def _probe_fault_rows():
    import ast, os
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "m88k_exc_probe.py")
    mod = ast.parse(open(src, encoding="utf-8").read())
    for node in mod.body:
        if isinstance(node, ast.Assign) and [getattr(x, "id", None) for x in node.targets] == ["ROWS"]:
            names = [e.elts[0].value for e in node.value.elts]
            return set(names) - {"live", "attrib"}, len(names)
    raise SystemExit("NAME-SET CHECK: no ROWS assignment found in " + src)
_probe, _nrows = _probe_fault_rows()
if _probe != set(FAULTS):
    raise SystemExit("NAME-SET CHECK FAILED: only in the probe %s; only here %s" % (sorted(_probe - set(FAULTS)), sorted(set(FAULTS) - _probe)))
print("NAME-SET CHECK: the hand table names exactly the probe's fault rows (%d = %d; ROWS holds %d with the two controls)" % (len(FAULTS), len(_probe), _nrows))
ALL = [r for r in FAULTS]
def report(title, rows, override):
    s = census(rows, override)
    print("\n=== %s  (%d rows enumerated) ===" % (title, len(rows)))
    print("%-9s %s" % ("arm", "  ".join("%-5s" % b for b, _ in BITS)))
    closed = 0; openc = []
    for a in ARMS:
        cells = []
        for (bn, _) in BITS:
            vals = s.get(a, {}).get(bn, set())
            if len(vals) > 1: cells.append("%-5s" % "CLOSE"); closed += 1
            else:
                v = ("=1" if 1 in vals else "=0") if vals else "--"
                cells.append("%-5s" % ("open" + v)); openc.append((a, bn, v))
        print("%-9s %s" % (a, "  ".join(cells)))
    print("closed %d of %d cells; OPEN: %s" % (closed, len(ARMS) * len(BITS),
          ", ".join("%s x %s%s" % (a, b, v) for a, b, v in openc) or "none"))
    return closed, openc

report("v24 -- the SHIPPED instrument (84 fault rows)", ALL, {})
report("v17/v18 -- history (57 fault rows)", [r for r in ALL if r not in V19_ROWS | V22_ROWS | V23_ROWS | V24_ROWS], {})
report("v16 -- the instrument pass 9 reviewed", [r for r in ALL if r not in V16_ONLY | V19_ROWS | V22_ROWS | V23_ROWS | V24_ROWS], V16_PSR)

# ---- THE OTHER TWO SITES, because a pass-10 seat (minimax) asked the right question about one of them.
# It read `resid50ser''s description -- "the fallback, whose own blurb already claimed every settable bit on
# both sides" -- as a row whose blurb claims an axis while the row tests one cell, i.e. pass 9's defect shape
# reproduced.  That is exactly the challenge this brief asked for, and it is answerable by census rather than
# by argument: the claim is true of the ROW SET, not of any single row, which is grok's "the axis is the set
# of rows, not any one of them".  Printed here so the answer is measured instead of asserted.
FALLBACK = {"resid50": RESET, "resid127": RESET, "resid11": RESET, "resid50ind": INDCLR,
            "resid50c": CARRY, "resid50ser": SERSUP, "usfu1": 0x0000000a, "sfu1h": EXC}
RR_NONTRAP = {"error": EXC, "errovf": EXC, "errind": FRZNOIND, "errc": FRZC, "errser": FRZSER,
              "errdiv0": FRZSUP, "errpriv": FRZUSER, "errunimpl": FRZUSER}
RR_TRAP = {"trapfrozen": EXC, "trapfrozen4": EXC, "trapfrozen5": EXC, "trapfrozen6": EXC, "trapfrozen8": EXC,
           "trapfrozen9": EXC, "trapfrozen10": EXC, "trapfrozen128": EXC, "trapfrozen450": EXC,
           "trapfrozen496": EXC, "trapfrozen511": EXC,
           "trapfrozenind": FRZNOIND, "trapfrozenc": FRZC, "trapfrozenser": FRZSER,
           "trapfrozenuser": FRZUSER, "trapfrozensfd1": FRZSUP}     # v19

def site(title, table, drop=()):
    t = {k: v for k, v in table.items() if k not in drop}
    print("\n=== %s  (%d rows) ===" % (title, len(t)))
    for (bn, bv) in BITS:
        vals = {(1 if (p & bv) else 0): [] for p in t.values()}
        for r, p in sorted(t.items()): vals[1 if (p & bv) else 0].append(r)
        if len(vals) > 1:
            odd = min(vals, key=lambda k: len(vals[k]))
            print("  %-5s CLOSED   %s=%d by %s" % (bn, bn, odd, ", ".join(vals[odd])))
        else:
            print("  %-5s open     every row has %s=%d" % (bn, bn, list(vals)[0]))

site("FALLBACK predicate -- v17/v18", FALLBACK)
site("FALLBACK predicate -- v16 (pass 9's instrument)", FALLBACK, drop=("resid50ser",))
site("SFRZ RE-ROUTE, non-trap side -- v17/v18", RR_NONTRAP)
site("SFRZ RE-ROUTE, non-trap side -- v16", RR_NONTRAP, drop=("errser",))
site("SFRZ RE-ROUTE, trap side -- v19 onward; v22/v23 add no new PSR value here (SFRZ invariant BY CONSTRUCTION: it is the guard)", RR_TRAP)
site("SFRZ RE-ROUTE, trap side -- v17/v18, history", RR_TRAP, drop=tuple(V19_ROWS))

# ---- v22-v24: THE DELAY-SLOT AXIS, as a GRID.  m88k_exception()'s delivery path TESTS four inputs: vector (the labels),
# PSR & SFRZ (:811), cpu->delay_slot (:840, and :865, whose write X(br_n) reads to keep the exception vector over the branch
# target) and is_trap (:816).  So the floor is {7 labels} x {SFRZ} x {delay_slot} x {is_trap}: 56 cells, 8 of them
# UNREACHABLE -- is_trap 0 at BOUNDS and ERROR in every (SFRZ, slot) state, because tcnd/tb0/tb1 are the only is_trap=1 raise
# sites and the only routes into 7 and 10 -- so 48 reachable (Fable 5.1, passes 14 and 15; v22 rowed the SFRZ-clear slot
# slice, v23 the SFRZ axis, v24 the is_trap axis).  A cell (label, sfrz, slot, trap) is ROWED iff some row raises that label
# with those values.  Per row: its faults in order (FAULTS); the second fault of every two-fault row runs FROZEN (SFRZ set);
# INSLOT names the fault that sits in a delay slot; TRAPAT names the fault raised by a trap instruction (is_trap = 1).
INSLOT = {"dslot": 0, "dslotmisalign": 0, "dslotunimpl": 0, "dslotpriv": 0, "dslotovf": 0,           # v22 (and dslot)
          "dslotbounds": 0, "dsloterror": 0,                                                         # v23, unfrozen trap
          "errdslotmisalign": 1, "errdslotovf": 1, "errdslotdiv0": 1, "errdslotpriv": 1,             # v23, frozen
          "errdslotunimpl": 1, "trapfrozen7dslot": 1, "trapfrozen10dslot": 1,
          "dslotmisaligntb": 0, "dslotunimpltb": 0, "dslotprivtb": 0, "dslotdiv0tb": 0, "dslotovftb": 0,   # v24
          "trapfrozen4dslot": 1, "trapfrozen5dslot": 1, "trapfrozen6dslot": 1, "trapfrozen8dslot": 1,
          "trapfrozen9dslot": 1}
TRAPAT = {r: 0 for r in ("bounds", "errortb", "misaligntb", "unimpltb", "div0tb", "ovftb", "vbrtb", "privsuptb",
                         "unimpltbc", "privtbc", "boundstbc", "div0tbc", "errortbc", "ovftbser", "dslotbounds", "dsloterror",
                         "dslotmisaligntb", "dslotunimpltb", "dslotprivtb", "dslotdiv0tb", "dslotovftb")}
TRAPAT.update({r: 1 for r in ("trapfrozen", "trapfrozen4", "trapfrozen5", "trapfrozen6", "trapfrozen8", "trapfrozen9",
                              "trapfrozen10", "trapfrozenind", "trapfrozenc", "trapfrozenser", "trapfrozensfd1",
                              "trapfrozen7dslot", "trapfrozen10dslot", "trapfrozen4dslot", "trapfrozen5dslot",
                              "trapfrozen6dslot", "trapfrozen8dslot", "trapfrozen9dslot")})
#  privtb is NOT here: a user-mode tb1 naming a vector below 128 raises PRIVILEGE with is_trap 0 (X(tb1)'s user filter).
TRAP_ONLY = {"BOUNDS", "ERROR"}


def ds_grid(title, rows):
    cells = {}                      # (label, sfrz, slot, trap) -> rows
    for r in rows:
        for k, (arm, _psr) in enumerate(FAULTS.get(r, [])):
            if arm in ARMS:
                key = (arm, 1 if k == 1 else 0, 1 if INSLOT.get(r) == k else 0, 1 if TRAPAT.get(r) == k else 0)
                cells.setdefault(key, []).append(r)
    print("\n=== %s  (%d rows) ===" % (title, len(rows)))
    cols = [(s, d, t) for s in (0, 1) for d in (0, 1) for t in (0, 1)]
    print("%-9s %s" % ("label", " ".join("%-13s" % ("S%d D%d %s" % (s, d, "trap" if t else "fault")) for s, d, t in cols)))
    rowed = reach = 0
    for a in ARMS:
        out = []
        for (s, d, t) in cols:
            if t == 0 and a in TRAP_ONLY:
                out.append("%-13s" % "unreachable")
                continue
            reach += 1
            got = sorted(cells.get((a, s, d, t), []))
            if got:
                rowed += 1
                out.append("%-13s" % ((got[0] + (" +%d" % (len(got) - 1) if len(got) > 1 else ""))[:13]))
            else:
                out.append("%-13s" % "OPEN")
        print("%-9s %s" % (a, " ".join(out)))
    print("rowed %d of %d reachable cells of {7 labels} x {SFRZ} x {delay_slot} x {is_trap} (%d unreachable: is_trap 0 at "
          "BOUNDS/ERROR)" % (rowed, reach, 4 * len(ARMS) * 2 - reach))


ds_grid("DELAY-SLOT x is_trap GRID -- v24, the SHIPPED instrument", ALL)
ds_grid("DELAY-SLOT x is_trap GRID -- v23, history", [r for r in ALL if r not in V24_ROWS])
ds_grid("DELAY-SLOT x is_trap GRID -- v22, history", [r for r in ALL if r not in V23_ROWS | V24_ROWS])
ds_grid("DELAY-SLOT x is_trap GRID -- v21 (HEAD before 2026-10-16: v19's 59 rows)",
        [r for r in ALL if r not in V22_ROWS | V23_ROWS | V24_ROWS])

# The fallback (:799) halts without testing anything the delivery path tests, so {fallback} x {SFRZ} x {slot} is clause (e)
# by the tests-not-reads criterion; v23/v24 row its slot cells anyway, on their measured escapes.
print("\n=== the FALLBACK x {SFRZ} x {delay slot} -- v24 ===")
for name, what in (("usfu1dslot", "SFRZ clear, in a slot"), ("sfu1hdslot", "SFRZ set, in a slot")):
    print("  %-11s %s" % (name, ("ROWED  (" + what + "): SFU1 must still HALT naming 0x072") if name in FAULTS else "open"))
