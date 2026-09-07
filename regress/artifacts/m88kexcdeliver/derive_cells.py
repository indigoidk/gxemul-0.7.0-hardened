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
}
V16_ONLY = {"ovftbser", "resid50ser", "errser"}     # the three rows v17 ADDED
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

report("v17/v18 -- the SHIPPED instrument (57 fault rows)", ALL, {})
report("v16 -- the instrument pass 9 reviewed", [r for r in ALL if r not in V16_ONLY], V16_PSR)

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
           "trapfrozenind": FRZNOIND, "trapfrozenc": FRZC, "trapfrozenser": FRZSER}

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
site("SFRZ RE-ROUTE, trap side -- v17/v18 (SFRZ invariant BY CONSTRUCTION: it is the guard)", RR_TRAP)
