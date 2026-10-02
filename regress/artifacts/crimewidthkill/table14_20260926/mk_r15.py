#!/usr/bin/env python3
"""mk_r15.py -- #529 REPAIR 15 applied to a COPY of regress/crime_width_probe.py (a0af7c92):

  1. the latch-SET carriers for the decline-suppression floor at TIME and REV, all four narrow ops each (the flagship
     first-hand re-ruling, rerule_20260925/fable5_rerule_529_20260925.md; repair 14's ruling C: "replay time
     lb/sb/lh/sh AFTER a prior refusal", and the REV-window pc redirect likewise);
  2. the entries-13/17 pair (FABLE_RULING_20260917.md B: CONTROL's DOG-only writes at both widths, each paired
     in-session with its 0x0201 twin) -- the ruling's conditional, taken because the CHANNEL check found no row able
     to see the one mutant that moves the cell (D_nodogclear); table 14 measures that escape and the pair's kill;
  3. the four new TIME control rows in the CRIMEP_CONTROL set;
  4. the contract paragraph that said the carriers were owed.

Exact-match edits; a find-text that is not unique is a hard failure.  Written as a FILE -- the Bash -> heredoc path
consumed a backslash level twice in one night.  No score is written into the probe: scores live in table 14's logs."""
import hashlib, io, os, sys

SRC = r"C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\crime_width_probe.py"
HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "crime_width_probe.r15.py")
s = io.open(SRC, encoding="utf-8", newline="").read()
md5 = hashlib.md5(s.encode("utf-8")).hexdigest()[:8]
if md5 != "a0af7c92":
    sys.exit("the working probe is %s, not a0af7c92 -- re-derive the edits" % md5)


def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("TEXT NOT UNIQUE (%d): %r" % (n, old[:80]))
    s = s.replace(old, new)


# 1. the contract: the owed carriers are now rowed; where each label-swap is measured is NAMED, never scored here
rep("  *** OF THE FIVE GUEST-OBSERVABLE LABELS ON THAT FACE, THREE HAVE BEEN SWEPT (INTSTAT killed, TIME and REV\n"
    "  escaping) AND **INTMASK AND CONTROL-WRITE ARE COVERED ONLY BY READING, NEVER MEASURED**.  Deriving them\n"
    "  covered is the same move that M5_revlatch was built to punish: REV was DERIVED open and then MEASURED\n"
    "  open. ***  Carriers for TIME and REV, and label-swap mutants for INTMASK and CONTROL-write, are OWED and\n"
    "  are not in this file yet.\n",
    "  *** REPAIR 15 (2026-09-26) ROWS THE OPEN CELLS.  The floor, by the flagship's first-hand re-ruling\n"
    "  (artifacts/crimewidthkill/rerule_20260925/fable5_rerule_529_20260925.md), is {observable skipped label} x\n"
    "  {latch SET}.  M3/M5 escaped because no refusal at TIME or REV with the latch already SET had a channel: the\n"
    "  `time' and `rev' sessions refuse there FIRST, and the `latch x5' session's later refusals at +0x00 and +0x38\n"
    "  run from CODE (REV's redirect needs the PROM window) with no TIME sample after them.  The `tl' and `rl' rows\n"
    "  refuse at +0x07 FIRST, then at the label.  The five guest-observable labels, the label-swap built for each,\n"
    "  and the table that measures it (scores are in those tables' logs, never here):\n"
    "      INTSTAT  M6_istlatch      istat sb/lh/sh                  repair14_20260916/ (table 12)\n"
    "      INTMASK  M7_intmasklatch  imask sb/lh/sh                  table13a_20260925/\n"
    "      CONTROL  M8_ctllatch      sb08 msg, sh08b run, gate run   table13a_20260925/\n"
    "      TIME     M3_timelatch     tl lb/sb/lh/sh                  table14_20260926/\n"
    "      REV      M5_revlatch      rl lb/lh/sb/sh pc               table14_20260926/\n"
    "  DOG (a bare `break;') and default (host log only -- and `mid nodflt' already reads it after a latch-\n"
    "  setting refusal: M1_gotolatch reddened it in table 12) have no guest-observable arm: clause (e).\n"
    "  ENTRIES 13/17 of ACCEPTS (`sw'/`sd +0x08 = 0x0200', CONTROL's DOG mask): the arm clears DOG and nothing\n"
    "  prints, and the prelude re-forces the register at every access, so the CONTROL text COUNT is the cell's one\n"
    "  observable -- and no row read it in a session holding that write.  `ctldog sw msg'/`ctldog sd msg' are the pair\n"
    "  (D_nodogclear, the DOG branch's clear deleted; table14_20260926/).  A SILENT decline of the DOG-only write\n"
    "  changes nothing any access can see: EQUIVALENT, disclosed.  The latch x DOG joint is clause (e): the CONTROL\n"
    "  arm reads no latch. ***\n")

# 2. the carriers, after the unlatched TIME loop (mag and nth are defined above it)
rep("# ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----\n",
    "# ---- #529 REPAIR 15: THE DECLINE HOLDS WITH THE LATCH ALREADY SET, at the two labels whose leak no row saw ----\n"
    "#  The `time' and `rev' sessions above refuse at TIME/REV FIRST, so the width latch is still CLEAR there -- and a\n"
    "#  `goto' conditioned on the SET latch plus the label (M3_timelatch, M5_revlatch; repair14_20260916/, table 12)\n"
    "#  never leaks in them.  (The `latch x5' session below refuses at +0x00 and +0x38 with the latch SET, but from CODE\n"
    "#  -- REV's redirect needs the PROM window -- and with no TIME sample after, so neither leak had a channel there.)\n"
    "#  Here the FIRST refusal is at +0x07 (the default arm; it sets the latch), and only THEN the refusal at the label.\n"
    "#  CHANNELS: TIME -- crime_update_crime_time() at the refused access moves the next sample by the wall-clock since\n"
    "#  the last update (large vs SMALL: the `time' rows' channel, and their disclosed tick assumption; the extra +0x07\n"
    "#  access adds debugger steps, never a TIME update, on a fix build); REV -- the arm's PROM-window hack redirects the\n"
    "#  pc to ra (the `rev pc' rows' channel).  All four narrow ops at each label, as repair 14's ruling said: the\n"
    "#  decline block tests neither width nor direction, and the four are the width x direction cells a leak keyed on\n"
    "#  either could use.\n"
    "for op in (\"lb\", \"sb\", \"lh\", \"sh\"):\n"
    "    A = Addr(CODE)\n"
    "    c = []\n"
    "    x, _ = ld(A, \"ld\", CRIME + 0x38, \"s0\"); c += x\n"
    "    x, _ = ld(A, \"lb\", CRIME + 0x07, \"v1\"); c += x          # the FIRST refusal: sets the latch\n"
    "    if op in (\"lb\", \"lh\"):\n"
    "        x, _ = ld(A, op, CRIME + 0x38, \"v0\"); c += x\n"
    "    else:\n"
    "        x, _ = st(A, op, CRIME + 0x38, 0xff if op == \"sb\" else 0xffff); c += x\n"
    "    x, _ = ld(A, \"ld\", CRIME + 0x38, \"s1\"); c += x\n"
    "    x, _ = ld(A, \"ld\", CRIME + 0x38, \"s2\"); c += x\n"
    "    t, clean = session(c + [\"print s1\", \"print s2\"])\n"
    "    s1, s2 = nth(t, \"s1\", 0), nth(t, \"s2\", 0)\n"
    "    row(\"tl %s\" % op, mag(s1), \"small\", \"latch SET, refused %s +0x38: no clock step (raw %s)\" % (op, s1))\n"
    "    row(\"tl %s ctl\" % op, mag(s2), \"large\", \"CONTROL: accepted ld moved TIME (raw %s)\" % s2)\n"
    "\n"
    "for op in (\"lb\", \"lh\", \"sb\", \"sh\"):\n"
    "    A = Addr(CODE)\n"
    "    y, _ = ld(A, \"lb\", CRIME + 0x07, \"v1\")                 # the FIRST refusal, from CODE: sets the latch\n"
    "    if op in (\"lb\", \"lh\"):\n"
    "        x, _ = ld(A, op, CRIME + 0, \"v0\", at=PROBE_PC)\n"
    "    else:\n"
    "        x, _ = st(A, op, CRIME + 0, 0xa5 if op == \"sb\" else 0xa5a5, at=PROBE_PC)\n"
    "    t, clean = session([\"ra=0x%x\" % RA] + y + x + AFTER)\n"
    "    row(\"rl %s pc\" % op, pr(t, \"pc\"), \"0x%x\" % (PROBE_PC + 4),\n"
    "        \"latch SET, refused %s at CRIME_REV from 0xbfc05180: pc NOT ra\" % op)\n"
    "\n"
    "# ---- #529 REPAIR 15: ACCEPTS entries 13/17, CONTROL's DOG-only writes (FABLE_RULING_20260917.md B) ----\n"
    "#  `sw'/`sd +0x08 = 0x0200': the arm clears DOG, the residue is 0 and nothing prints, and the prelude re-forces\n"
    "#  CONTROL at every access -- so the CONTROL text COUNT is the cell's one observable, and no session holding a\n"
    "#  0x0200 write read it (the ACCEPTS sessions count `-- declined.'; `p acc ctl msg' writes 0x01, 0x0001 and\n"
    "#  0x0201).  MUTANT: D_nodogclear, the DOG branch's `idata &= ~CRIME_CONTROL_DOG_ENABLE;' deleted -- the arm's own\n"
    "#  tested bit with its repair nulled -- prints for 0x0200.  Each width is one session: the 0x0200 write, then its\n"
    "#  0x0201 twin, the in-session LIVENESS half of the pair (a bare count of 0 is green under a dead channel or a\n"
    "#  declined write).  CHANNEL: fix ONE text, the twin's; D_nodogclear TWO.  A silent decline of the 0x0200 write\n"
    "#  still reads ONE -- EQUIVALENT, since no access can see the cell (disclosed in the contract).\n"
    "for op in (\"sw\", \"sd\"):\n"
    "    A = Addr(CODE)\n"
    "    x, _ = st(A, op, CRIME + 0x08, 0x0200)\n"
    "    y, _ = st(A, op, CRIME + 0x08, 0x0201)\n"
    "    t, clean = session(x + y)\n"
    "    row(\"ctldog %s msg\" % op, count(t, \"CRIME_CONTROL: unimplemented\", clean), 1,\n"
    "        \"%s 0x0200 then 0x0201 +0x08: ONE CONTROL text, the twin's\" % op)\n"
    "\n"
    "# ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----\n")

# 3. the four new control rows join the control set
rep('                                          "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl"))\n',
    '                                          "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl",\n'
    '                                          "tl lb ctl", "tl sb ctl", "tl lh ctl", "tl sh ctl"))\n')

io.open(DST, "w", encoding="utf-8", newline="").write(s)
print("wrote", DST, hashlib.md5(s.encode("utf-8")).hexdigest()[:8])
