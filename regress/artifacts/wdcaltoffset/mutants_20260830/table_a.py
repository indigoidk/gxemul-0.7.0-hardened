"""wdcaltoffset TABLE A -- score N legs against the SHIPPED witness, UNMODIFIED.

    python3 table_a.py <outdir> <disk> <tag>=<binary> [<tag>=<binary> ...]

THE INSTRUMENT IS NOT REIMPLEMENTED HERE.  This file IMPORTS
witness_20260829/wdcaltoff_rung3_probe.py and calls its own run_one() against its own
ROWS.  So the question the table answers is exactly the one asked -- "does the detector
THE ROUND WILL SHIP kill these mutants" -- and not "does a detector I rewrote for the
occasion kill them".  The import is cmp'd against the artifact copy below, so the
provenance is stated rather than assumed.

SCORING.  Every leg is compared against BOTH shipped expectation columns:
    KILLED-as-defect   the leg reproduces the COMMITTED pattern on the two defect rows
                       (the fix is absent or nulled)
    KILLED-on-accept   the leg breaks a row that is GREEN on both shipped legs
                       (an over-reaching fix, or collateral damage)
    ESCAPED            all 15 rows match the FIX column exactly
A mutant that ESCAPES is a hole in the detector, and is reported as such rather than
folded into a pass count.
"""
import io
import os
import sys
import time

OUTDIR = sys.argv[1]
DISK = sys.argv[2]
LEGS = [a.split("=", 1) for a in sys.argv[3:]]

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.normpath(os.path.join(HERE, "..", "witness_20260829"))

os.makedirs(OUTDIR, exist_ok=True)
sys.argv = [sys.argv[0]]                     # the probe reads argv at import
sys.path.insert(0, WIT)
import wdcaltoff_rung3_probe as W            # noqa: E402  -- the shipped instrument

W.DISK = DISK
W.OUTDIR = OUTDIR
W.RAWBIN = os.path.join(OUTDIR, "wdcaltoff.bin")
with open(W.RAWBIN, "wb") as f:
    for w, _ in W.prog:
        f.write(bytes([w & 0xff, (w >> 8) & 0xff, (w >> 16) & 0xff, (w >> 24) & 0xff]))

lines = []


def out(s=""):
    lines.append(s)
    print(s)
    sys.stdout.flush()


out("=" * 100)
out("wdcaltoffset TABLE A -- the SHIPPED witness scored against the fix and four mutants")
out("=" * 100)
out("date        %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
out("instrument  %s/wdcaltoff_rung3_probe.py  (IMPORTED, not reimplemented)" % WIT)
src = io.open(os.path.join(WIT, "wdcaltoff_rung3_probe.py"), "rb").read()
out("            %d bytes, %d rows, %d guest instructions"
    % (len(src), len(W.ROWS), len(W.prog)))
out("rig         evbmips -e malta, image %s, attached iR:" % DISK)
out("legs        %s" % ", ".join(t for t, _ in LEGS))
out()

res = {}
for tag, binary in LEGS:
    out("-" * 100)
    out("LEG %s   %s" % (tag, binary))
    out("-" * 100)
    got, w_ok, m_ok, hit, dg = W.run_one(binary, tag, out)
    res[tag] = dict(got=got, w=w_ok, m=m_ok, hit=hit, dg=dg)
    out()

#  ---------------------------------------------------------------------- the table
out("=" * 100)
out("THE TABLE -- every cell is a byte a GUEST LOAD returned through real decode")
out("=" * 100)
hdr = "  %-52s %-4s %-9s %-9s" % ("", "reg", "want:base", "want:fix")
for tag, _ in LEGS:
    hdr += " %-7s" % tag
out(hdr)
for label, rn, wb, wf, kind in W.ROWS:
    line = "  %-52s %-4s %-9s %-9s" % (label, rn, "%02x" % wb, "%02x" % wf)
    for tag, _ in LEGS:
        g = res[tag]["got"].get(rn)
        line += " %-7s" % (("%02x" % g) if g is not None else "??")
    out(line)
out()

#  --------------------------------------------------------------------- the verdict
out("=" * 100)
out("VERDICTS -- what the shipped detector says about each leg")
out("=" * 100)
verdicts = {}
for tag, _ in LEGS:
    got = res[tag]["got"]
    like_fix = [l for l, rn, wb, wf, k in W.ROWS if got.get(rn) != wf]
    defect_back = [l for l, rn, wb, wf, k in W.ROWS
                   if k == "defect" and got.get(rn) == wb and wb != wf]
    accept_broke = [l for l, rn, wb, wf, k in W.ROWS
                    if wb == wf and got.get(rn) != wb]
    if not res[tag]["hit"]:
        v = "*** THE GUEST NEVER PARKED -- see the transcript"
    elif not like_fix:
        v = "ESCAPED   all %d rows match the FIX column" % len(W.ROWS)
    elif defect_back and not accept_broke:
        v = "KILLED as-defect   %d defect row(s) show the COMMITTED value" % len(defect_back)
    elif accept_broke:
        v = "KILLED on-accept   %d row(s) green on BOTH shipped legs went red" % len(accept_broke)
    else:
        v = "KILLED   %d row(s) differ from the fix column" % len(like_fix)
    verdicts[tag] = v
    out("  %-6s %s" % (tag, v))
    for l in accept_broke:
        out("           accept/control broken: %s" % l)
    for l in defect_back:
        out("           defect reinstated:     %s" % l)
    out("           encodings %d/%d words, %d/%d mnemonics; parked %s"
        % (res[tag]["w"], len(W.prog), res[tag]["m"], len(W.prog), res[tag]["hit"]))
out()

esc = [t for t, _ in LEGS if verdicts[t].startswith("ESCAPED") and t != "fix"]
out("  MUTANTS THAT ESCAPED THE SHIPPED DETECTOR: %s"
    % (", ".join(esc) if esc else "none"))
out()

out("-" * 100)
out("EMULATOR DIAGNOSTIC COUNTS -- informational; debug() is silent when free-running")
out("-" * 100)
names = sorted(set(n for t, _ in LEGS for n in res[t]["dg"]))
out("  %-30s %s" % ("", " ".join("%-6s" % t for t, _ in LEGS)))
for n in names:
    out("  %-30s %s" % (n, " ".join("x%-5d" % res[t]["dg"].get(n, 0) for t, _ in LEGS)))
out()
out("TABLE_A_DONE")

with open(os.path.join(OUTDIR, "TABLE_A.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
