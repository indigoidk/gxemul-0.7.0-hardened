#!/usr/bin/env python3
"""mk_r16.py -- #529 REPAIR 16 applied to a COPY of repair 15's frozen probe (table14_20260926/
crime_width_probe.table14.py, f5e915f6).  The CONTROL arm's residue-text channel, closed as a class in one diff:

  1. `ctlrst sw/sd msg' + `ctlrst sw/sd halt' -- HARD_RESET's residue with the latch CLEAR (the cell the flagship seat
     graded L2 on repair 15's pass 2; measured uncovered in table15a_20260926/);
  2. `rst 4w/8w msg' -- the same residue with the latch SET, in the existing reset sessions (an accepted 0x0001 twin now
     runs first in each, the text channel's in-session liveness half);
  3. `rearm ctl msg' / `latch ctl msg' -- a CONTROL-text count on the two existing ACCEPTS sessions, which already hold
     all ten accepted CONTROL writes in the latch SET and latch CLEAR states (the Opus seat's option on repair 15's
     pass 2): DOG and ENDIANESS residue in both latch states, no new session;
  4. the contract text: the class closure, and the cells deliberately NOT rowed, disclosed with where they were measured;
  5. the header's {1,2} x {R,W} claim given its latch-state scope, and the tl/rl comment's four-op rationale restated.

No score is written into the probe.  Exact-match edits; a find-text that is not unique is a hard failure."""
import hashlib, io, os, sys

SRC = r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\table14_20260926\crime_width_probe.table14.py"
HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "crime_width_probe.r16.py")
s = io.open(SRC, encoding="utf-8", newline="").read()
md5 = hashlib.md5(s.encode("utf-8")).hexdigest()[:8]
if md5 != "f5e915f6":
    sys.exit("the repair-15 probe is %s, not f5e915f6 -- re-derive the edits" % md5)


def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("TEXT NOT UNIQUE (%d): %r" % (n, old[:80]))
    s = s.replace(old, new)


# 1. the header's claim, given its scope
rep("     observable label carries the whole {1,2} x {R,W} refusal floor (CONTROL's reads and DOG have no body: below).\n",
    "     observable label carries the whole {1,2} x {R,W} refusal floor, each cell in at least ONE latch state (CONTROL's\n"
    "     reads and DOG have no body: below).  [Crossed with the latch state, INTSTAT and INTMASK exercise 4 of their 8\n"
    "     cells each -- see the contract block (#529 repair 16; the Opus seat, repair 15's pass 2).]\n")

# 2. the contract: the class closure and every cell deliberately not rowed
rep("  changes nothing any access can see: EQUIVALENT, disclosed.  The latch x DOG joint is clause (e): the CONTROL\n"
    "  arm reads no latch. ***\n",
    "  changes nothing any access can see: EQUIVALENT, disclosed.\n"
    "  REPAIR 16 (2026-09-26) CLOSES THE CONTROL ARM'S RESIDUE-TEXT CHANNEL AS A CLASS: every clear the arm makes before\n"
    "  its residue test (DOG 0x200, HARD_RESET 0x800, ENDIANESS 0x100) has a residue-count row in BOTH latch states --\n"
    "  DOG: `ctldog sw/sd msg' and `latch ctl msg' (CLEAR), `rearm ctl msg' (SET); HARD_RESET: `ctlrst sw/sd msg'\n"
    "  (CLEAR), `rst 4w/8w msg' (SET); ENDIANESS: `latch ctl msg' (CLEAR), `rearm ctl msg' (SET) -- and each TESTED bit\n"
    "  keeps its side-effect rows (DOG's stop and re-arm shapes: `rearm surv', `latch surv', `rearm once'; HARD_RESET's\n"
    "  stop: `sw08 halts', `rst 4w', `rst 8w', `ctlrst sw/sd halt').  Measured in table15a_20260926/ and\n"
    "  table16_20260926/.  NOT ROWED, disclosed as clause (e), each measured by the Opus seat on repair 15's pass 2\n"
    "  (opus_r15p2_20260926/): the residue VALUE when the count does not move (a DOG clear skipped when bit 0 is set);\n"
    "  a latch-SET 2-byte CONTROL write with HARD_RESET clear (host text only; every latch-SET 2-byte write here carries\n"
    "  0x0800); at INTSTAT and INTMASK, the width x direction x latch-state joints no session reaches (1R with the latch\n"
    "  SET; 1W, 2R, 2W with it CLEAR -- the decline tests neither width within the narrow class nor direction); and a\n"
    "  refusal at INTSTAT/INTMASK while the interrupt line is ALREADY asserted (every row here watches the line rise).\n"
    "  Whether those are floor is a question put to the adjudicators with these measurements. ***\n")

# 3. the tl/rl comment: the four ops are ruling C's strengthening over the {label} x {latch SET} floor
rep("#  pc to ra (the `rev pc' rows' channel).  All four narrow ops at each label, as repair 14's ruling said: the\n"
    "#  decline block tests neither width nor direction, and the four are the width x direction cells a leak keyed on\n"
    "#  either could use.\n",
    "#  pc to ra (the `rev pc' rows' channel).  All four narrow ops at each label because repair 14's ruling C asked for\n"
    "#  them -- a STRENGTHENING over the floor, which is {label} x {latch SET}: the decline block tests neither width\n"
    "#  within the narrow class nor direction.  (INTSTAT and INTMASK do not have all four in both latch states: see the\n"
    "#  contract block.  This said \"the four are the width x direction cells a leak keyed on either could use\" --\n"
    "#  repair 15's pass 2, four seats.)\n")

# 4. the HARD_RESET residue pair with the latch CLEAR, after the ctldog block
rep("# ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----\n",
    "# ---- #529 REPAIR 16: HARD_RESET's residue with the latch CLEAR (repair 15's pass 2) ----\n"
    "#  An accepted `sw'/`sd +0x08 = 0x0800' stops every CPU, and because the branch clears HARD_RESET before the residue\n"
    "#  test it prints nothing.  No row counted the CONTROL text in a session holding an accepted 0x0800 write, so a build\n"
    "#  that skipped that clear passed every row while the CPUs still stopped (table15a_20260926/).  The halt ends the\n"
    "#  guest's work, so the twin comes FIRST: 0x0001 (residue 0x1, one text), then 0x0800 as the session's last store.\n"
    "#  CHANNELS: the text count -- ONE on the fixed build, TWO if the clear is skipped -- and the halt: v1 left at the\n"
    "#  sentinel by the RAM trip that cannot run, which shows the 0x0800 write reached the arm.\n"
    "for op in (\"sw\", \"sd\"):\n"
    "    A = Addr(CODE)\n"
    "    x, _ = st(A, op, CRIME + 0x08, 0x0001)\n"
    "    y, _ = st(A, op, CRIME + 0x08, 0x0800)\n"
    "    t, clean = session(x + y + AFTER + roundtrip(A))\n"
    "    row(\"ctlrst %s msg\" % op, count(t, \"CRIME_CONTROL: unimplemented\", clean), 1,\n"
    "        \"%s 0x0001 then 0x0800 +0x08: ONE CONTROL text, the twin's\" % op)\n"
    "    row(\"ctlrst %s halt\" % op, pr(t, \"v1\"), \"0x%x\" % SENT, \"%s 0x0800 +0x08 after the twin: CPUs stopped\" % op)\n"
    "\n"
    "# ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----\n")

# 5. the ACCEPTS sessions' CONTROL-text counts
rep("row(\"rearm surv\", pr(t, \"v1\"), \"0x%x\" % LIVE_VAL, \"the whole interleave completes (a RAM trip)\")\n",
    "row(\"rearm surv\", pr(t, \"v1\"), \"0x%x\" % LIVE_VAL, \"the whole interleave completes (a RAM trip)\")\n"
    "#  #529 repair 16: ACCEPTS holds ten accepted CONTROL writes -- 0x0201, 0x0001, 0, 0x0200, 0x0100 at both widths -- and\n"
    "#  here every one after the first entry runs with the latch SET.  The fixed build prints for the four with a nonzero\n"
    "#  residue (0x0201 and 0x0001, both widths).  A clear skipped for DOG or ENDIANESS adds texts; a latch-SET accepted\n"
    "#  write wrongly declined removes them.  (The Opus seat's option on repair 15's pass 2, replay-measured 4 on base.)\n"
    "row(\"rearm ctl msg\", count(t, \"CRIME_CONTROL: unimplemented\", clean), 4,\n"
    "    \"ten accepted CONTROL writes, latch SET: four print (0x0201, 0x0001 at both widths)\")\n")
rep("row(\"latch surv\", pr(t, \"v1\"), \"0x%x\" % LIVE_VAL, \"host survives all five\")\n",
    "row(\"latch surv\", pr(t, \"v1\"), \"0x%x\" % LIVE_VAL, \"host survives all five\")\n"
    "#  #529 repair 16: the same ten accepted CONTROL writes, here all BEFORE the first refusal -- latch CLEAR.\n"
    "row(\"latch ctl msg\", count(t, \"CRIME_CONTROL: unimplemented\", clean), 4,\n"
    "    \"ten accepted CONTROL writes, latch CLEAR: four print (0x0201, 0x0001 at both widths)\")\n")

# 6. the reset sessions: a 0x0001 twin first, and the CONTROL-text count returned and rowed
rep("def rst_session(op):\n"
    "    \"\"\"a refused lb sets the latch; then an accepted `op' of 0x800 at CONTROL stops every CPU (or does not)\"\"\"\n"
    "    A = Addr(CODE)\n"
    "    c, _ = ld(A, \"lb\", CRIME + 0x07, \"v0\")\n"
    "    if op is not None:\n"
    "        x, _ = st(A, op, CRIME + 0x08, 0x800)\n"
    "        c += x\n"
    "    c += roundtrip(A)\n"
    "    t, clean = session(c)\n"
    "    return pr(t, \"v1\"), (t.count(\"-- declined.\") if clean else \"unclean\")\n",
    "def rst_session(op):\n"
    "    \"\"\"a refused lb sets the latch; then an accepted `op' of 0x800 at CONTROL stops every CPU (or does not).  #529\n"
    "    repair 16: an accepted `op' of 0x0001 runs FIRST, with the latch CLEAR -- one CONTROL text, the text channel's\n"
    "    in-session liveness half -- and the CONTROL-text count is returned: the 0x800 write's residue, latch SET.\"\"\"\n"
    "    A = Addr(CODE)\n"
    "    c = []\n"
    "    if op is not None:\n"
    "        x, _ = st(A, op, CRIME + 0x08, 0x0001)\n"
    "        c += x\n"
    "    x, _ = ld(A, \"lb\", CRIME + 0x07, \"v0\")\n"
    "    c += x\n"
    "    if op is not None:\n"
    "        x, _ = st(A, op, CRIME + 0x08, 0x800)\n"
    "        c += x\n"
    "    c += roundtrip(A)\n"
    "    t, clean = session(c)\n"
    "    return (pr(t, \"v1\"), (t.count(\"-- declined.\") if clean else \"unclean\"),\n"
    "            count(t, \"CRIME_CONTROL: unimplemented\", clean))\n")
rep("_rv, _rn = rst_session(None)\n", "_rv, _rn, _rm = rst_session(None)\n")
rep("    _rv, _rn = rst_session(_op)\n", "    _rv, _rn, _rm = rst_session(_op)\n")
rep("    row(\"rst %dw once\" % _w, _rn, 1, \"CONTROL: exactly one refusal announced in this session\")\n",
    "    row(\"rst %dw once\" % _w, _rn, 1, \"CONTROL: exactly one refusal announced in this session\")\n"
    "    row(\"rst %dw msg\" % _w, _rm, 1, \"twin 0x0001 then, latch SET, 0x800: ONE CONTROL text, the twin's\")\n")

io.open(DST, "w", encoding="utf-8", newline="").write(s)
print("wrote", DST, hashlib.md5(s.encode("utf-8")).hexdigest()[:8])
