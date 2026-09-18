#!/usr/bin/env python3
"""check_pred.py -- #530 kill table 6: compare each measured red-row set to PRETABLE.out's prediction, EXACTLY.  The
predictions are transcribed here as Python sets (table 4's checker mis-parsed a nested parenthetical in the PRETABLE
text, so this one does not parse prose)."""
import io, os

K = os.path.dirname(os.path.abspath(__file__))
IIR8 = {"iir stb", "iir stl", "iir stw", "iir stq", "kbcq b dib", "kbcq w dib", "kbcq l dib", "kbcq q dib"}
N = (1, 2, 4, 8)
CMOSW = {"cmos w%d" % n for n in N}
CMOSR = {"cmos r%d" % n for n in N}
TQW = {"tailq w t%d" % t for t in (7, 6, 5, 3)}
TQR = {"tailq r t%d" % t for t in (7, 6, 5, 3)}
RDQ = {"rdq r%d" % n for n in N}
IIRR2 = {"iir lca rd2", "iir lca rd4", "iir lca rd8"}


def stub(lanes, arm, widths=N):
    return {"stub%d %s%d" % (l, arm, n) for l in lanes for n in widths}


ALL = (0, 1, 2, 3)
P = {
    "base": set(),
    "Wpure": IIR8 | CMOSW | stub(ALL, "w") | TQW,
    "dataA": CMOSW | stub(ALL, "w"),
    "dataB": IIR8 | TQW,
    "L1gate": CMOSW | stub((1,), "w"),
    "L3gate": stub((3,), "w"),
    "WT6": {"tailq w t6"},
    "WTsplit": set(TQW),
    "R2w": {"rdq r2", "rdq r4", "rdq r8", "cmos r2", "cmos r4", "cmos r8"} | IIRR2 | stub(ALL, "r", (2, 4, 8)) | TQR,
    "R2w2": {"rdq r2", "cmos r2", "iir lca rd2"} | stub(ALL, "r", (2,)),
    "RD2L0": RDQ | stub((0,), "r") | TQR,
    "RD2L1": CMOSR | stub((1,), "r"),
    "RD2L3": stub((3,), "r"),
    "RD2": RDQ | CMOSR | {"iir lca rd"} | IIRR2 | stub(ALL, "r") | TQR,
}
NROWS = 185
exact = differ = pend = 0
for m, want in P.items():
    log = os.path.join(K, "logs", "probe_%s.raw" % m)
    txt = io.open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
    if "LCAISALANE_DONE" not in txt:
        print("PENDING  %s" % m); pend += 1; continue
    got = set(l[:14].strip() for l in txt.splitlines() if l.rstrip().endswith(" FAIL") and len(l) > 14)
    res = [l for l in txt.splitlines() if l.startswith("LCAISALANE_RESULT=")]
    score = res[-1].split("=")[1] if res else "?"
    if got == want and score == "%d/%d" % (NROWS - len(want), NROWS):
        exact += 1; print("EXACT    %-8s %s" % (m, score))
    else:
        differ += 1
        print("DIFFERS  %-8s %s extra=%s missing=%s" % (m, score, sorted(got - want), sorted(want - got)))
print("CHECKPRED exact=%d differs=%d of %d measured (%d predicted)" % (exact, differ, exact + differ, len(P)))
