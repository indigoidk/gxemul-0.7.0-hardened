"""#536 edit to check_probe_wiring.py, applied identically to the HEAD-based staged blob and to the
working tree (which also carries #529's uncommitted MANIFEST hunk, not ours to ship).

  1. drop the EXEMPT entries of the two probes #536 wires into gate_arm.sh;
  2. re-date every remaining 2026-09-20 entry to 2026-09-27 (owner ruling 2026-09-18: wire 2,
     re-date 11);
  3. derive the selftest's M5a/M5b dates from the table instead of the literals 2026-09-19 and
     2026-09-21 -- which bracketed the old block and would turn M5b GREEN (and the selftest red)
     the moment the block moved.

Usage: python apply536_exempt.py <path-to-check_probe_wiring.py>.  Refuses unless it finds exactly
what it expects, and is NOT idempotent on purpose: a second run fails on step 1."""
import io, re, sys

p = sys.argv[1]
s = io.open(p, encoding="utf-8", newline="").read()

# ---- 1 + 2: the EXEMPT table -------------------------------------------------------------
i = s.index("EXEMPT = {"); j = s.index("\n}", i)
blk = s[i:j]
for name in ("mk48_nvram_probe.py", "hpcmips_ctor_probe.py"):
    m = re.search(r'\n    "%s":\s*\("2026-09-20",\n(?:\s+"[^\n]*\n)*?\s+"[^\n]*"\),' % re.escape(name), blk)
    if not m:
        m = re.search(r'\n    "%s":\s*\("2026-09-20",[^\n]*\),' % re.escape(name), blk)
    assert m, "entry not found: " + name
    blk = blk.replace(m.group(0), "", 1)
n = blk.count('("2026-09-20"')
assert n == 11, "expected 11 remaining 2026-09-20 entries, found %d" % n
blk = blk.replace('("2026-09-20"', '("2026-09-27"')
s = s[:i] + blk + s[j:]

# ---- 3: the selftest's M5a/M5b dates -----------------------------------------------------
OLD = (
    '    rg, chk = fresh()\n'
    '    case("M5a a live exemption is GREEN the day before", 0, "PROBEWIRING_PASS", chk, rg,\n'
    '         extra=("--today", "2026-09-19"))\n'
    '    case("M5b the same tree is RED the day after", 1, "EXPIRED EXEMPTION", chk, rg,\n'
    '         extra=("--today", "2026-09-21"))\n'
)
NEW = (
    '    #  #536: THE TWO DAYS ARE DERIVED FROM THE TABLE, NEVER LITERALS.  They were 2026-09-19 and\n'
    '    #  2026-09-21, the days either side of the block every dated exemption then shared -- so\n'
    '    #  the day that block was re-dated, M5b would have run on a tree with nothing expired, gone\n'
    '    #  GREEN, and failed the selftest.  The frozen-claim-about-a-table-designed-to-change that\n'
    '    #  _pick_exempt_detector() refuses for M1-M3, earlier in this selftest.  The\n'
    '    #  comparison is `d < today`, so an exemption is valid ON its stamped date: the earliest\n'
    '    #  DETECTOR date ITSELF is green and the day after is red.  M5a runs ON the date, not the\n'
    '    #  day before, because that is the one day on which `<` and `<=` differ: with `d <= today`\n'
    '    #  both day-before and day-after cases passed (codex, #536 pass 2, executed; Opus measured\n'
    '    #  22/22 -> 21/22 once M5a moved).  The day-before case\'s only UNIQUE kill was `!=` (M5b\n'
    '    #  still reds `>` and `>=`), and `!=` expires every exemption on every day except its\n'
    '    #  stamped date, so it cannot stay quiet in production -- and M0 and M2b, which read the\n'
    '    #  real clock, still catch it on any other day.  No dated detector exemption left is two\n'
    '    #  FAILS, never a skip -- the denominator must not shrink.\n'
    '    _m5 = sorted(EXEMPT[_n][0] for _n in EXEMPT\n'
    '                 if MANIFEST.get(_n, (None,))[0] == CLASS_DETECTOR\n'
    '                 and DATE_RE.match(EXEMPT[_n][0] or ""))\n'
    '    if not _m5:\n'
    '        results.extend([False, False])\n'
    '        print("  FAIL  M5a/M5b -- no well-formed dated DETECTOR exemption to derive the days from.")\n'
    '    else:\n'
    '        import datetime as _dt5\n'
    '        _d5 = _dt5.date.fromisoformat(_m5[0])\n'
    '        rg, chk = fresh()\n'
    '        case("M5a a live exemption is GREEN ON its stamped date", 0, "PROBEWIRING_PASS", chk, rg,\n'
    '             extra=("--today", _d5.isoformat()))\n'
    '        case("M5b the same tree is RED the day after", 1, "EXPIRED EXEMPTION", chk, rg,\n'
    '             extra=("--today", (_d5 + _dt5.timedelta(days=1)).isoformat()))\n'
)
k = s.count(OLD)
assert k == 1, "M5a/M5b block found %d times (want 1)" % k
s = s.replace(OLD, NEW)

# ---- 4: the two comments the edit would otherwise leave false ------------------------------
A_OLD = "#  chose is a deadline nobody owns.\n#\n"
A_NEW = (
    "#  chose is a deadline nobody owns.\n"
    "#\n"
    "#  *** #536/#537, 2026-09-18: ONE HALF OF THAT PAIRING IS GONE. ***  #537 discharged\n"
    "#  fbpending_bound's SM_EXEMPT line -- its self-mutant lane runs now.  The other half,\n"
    "#  fbpending_drain_probe.py below, is still exempt: #536 wired mk48_nvram_probe.py and\n"
    "#  hpcmips_ctor_probe.py into gate_arm.sh and moved the eleven left at 2026-09-20 to 2026-09-27\n"
    "#  BY OWNER RULING, so those eleven again fall due as ONE block: the cliff `exemptcliff` names\n"
    "#  is re-created a week out, deliberately and dated, not by copying.\n"
    "#\n"
)
k = s.count(A_OLD)
assert k == 1, "pairing-comment anchor found %d times (want 1)" % k
s = s.replace(A_OLD, A_NEW)

B_OLD = "    #  STALE EXEMPTION.  Six exemptions remain.\n"
B_NEW = (
    "    #  STALE EXEMPTION.  Six exemptions remain.\n"
    "    #  mk48_nvram_probe.py's and hpcmips_ctor_probe.py's exemptions are DISCHARGED, 2026-09-18\n"
    "    #  (#536) -- both wired into gate_arm.sh, mk48 on the mvme187 machine that file already\n"
    "    #  drives for the PCC2 probes, hpcmips as a construction check with no rig image.  Deleted\n"
    "    #  in the SAME edit as the wiring, for the same reason.\n"
)
k = s.count(B_OLD)
assert k == 1, "discharge-note anchor found %d times (want 1)" % k
s = s.replace(B_OLD, B_NEW)

# ---- 5: the MANIFEST comment that said mk48 is EXEMPT and has no home (Opus seat, #536 pass 2) ----------
C_OLD = """    #  CLASS_DETECTOR, and EXEMPT below rather than wired.  It is a fast (0.4 s) single-leg
    #  instrument that runs green on the fix today, so unlike a witness it COULD be gated --
    #  what it lacks is a home: gate_m88k_rounding.sh is the only gate on this CPU family and
    #  it drives luna88k, not mvme88k/mvme187.  Giving it an mvme187 leg is a gate change
    #  owing its own negative controls, i.e. a harness round, not a rider on a device fix.
    #  Filed to `wiringcliff'.
"""
C_NEW = """    #  CLASS_DETECTOR, WIRED by #536 (2026-09-18) into gate_arm.sh.  It stood EXEMPT on the
    #  reason "gate_m88k_rounding.sh is the only gate on this CPU family and it drives luna88k,
    #  not mvme88k/mvme187" -- true of that gate, false of the tree: gate_arm.sh already drives
    #  mvme187 for the PCC2 probes, so the home already existed and wiring it was the whole job.
"""
k = s.count(C_OLD)
assert k == 1, "mk48 MANIFEST comment x%d" % k
s = s.replace(C_OLD, C_NEW)

# ---- 6: the EXEMPT-block paragraph describing mk48's entry, which step 1 deleted ---------------------------
D_OLD = """    #  #521's detector.  Single-leg, fast, green on the fix -- it lacks a HOME, not a design:
    #  the only gate on this CPU family drives luna88k, not mvme88k/mvme187.  Dated to fall
    #  due with the others so the cliff stays one date rather than a rolling excuse.
"""
k = s.count(D_OLD)
assert k == 1, "mk48 EXEMPT paragraph x%d" % k
s = s.replace(D_OLD, "")

# ---- 7: the pairing premise above the "ONE HALF" note, still in the present tense (grok, #536 F2 pass) ----
E_OLD = """#  2026-09-20 matches the fbpending_bound:2026-09-20 deadline already standing in
#  gate_offline.sh's SM_EXEMPT, so #442's two debts fall due together.  IT IS A PROPOSAL: the
"""
E_NEW = """#  2026-09-20 MATCHED the fbpending_bound:2026-09-20 deadline then standing in
#  gate_offline.sh's SM_EXEMPT, so #442's two debts fell due together.  IT WAS A PROPOSAL: the
"""
k = s.count(E_OLD)
assert k == 1, "pairing premise x%d" % k
s = s.replace(E_OLD, E_NEW)

# ---- 8: M5f's "exhaustively", false before M5a moved and not true after (grok, #536 F2 pass) -----------
F_OLD = """    #  pass `--today` EXPLICITLY, so between them they test the COMPARISON exhaustively
    #  and the CLOCK IT READS not at all."""
F_NEW = """    #  pass `--today` EXPLICITLY, so between them they test the COMPARISON -- at its boundary
    #  since #536 (M5a ON the stamped date, M5b the day after), never exhaustively -- and the
    #  CLOCK IT READS not at all."""
k = s.count(F_OLD)
assert k == 1, "M5f exhaustively x%d" % k
s = s.replace(F_OLD, F_NEW)

io.open(p, "w", encoding="utf-8", newline="").write(s)
print("removed 2 wired entries; re-dated %d entries to 2026-09-27; M5a/M5b dates derived; mk48 prose corrected" % n)
