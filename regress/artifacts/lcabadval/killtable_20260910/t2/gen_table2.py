#!/usr/bin/env python3
#
#  #518 table 2 -- emit the measured table body for TABLE2.out.
#
#  It joins three things that must not be typed by hand: the EDIT (imported from the mutator, so
#  the table can never quote an edit the run did not apply), the MEASURED score and reddened rows
#  (read out of the <mutant>.raw logs, each of which must carry LCABADVAL_DONE), and the
#  PREDICTION (parsed out of PREDICTIONS.txt, whose mtime predates every .raw).  A prediction that
#  missed is flagged, because a refuted prediction is a result too.
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutate518_t2 as MU
import summarize_t2 as SU

D = os.path.dirname(os.path.abspath(__file__))


def edit_of(name):
    spec = MU.M[name]
    if spec[0] == "__ARM__":
        return "(b) the WHOLE %s arm replaced by its verbatim pre-#518 source" % spec[1]
    if spec[0] == "__FILE__":
        return "(c) NULL MEDIUM: the entire pre-#518 dev_lca.c (all seven host kills at once)"
    find, repl, occ = spec
    where = "all sites" if occ == 0 else "site %d" % occ
    return "%r -> %r  [%s]" % (find, repl, where)


def predictions():
    p = {}
    cur = None
    for line in open(os.path.join(D, "PREDICTIONS.txt"), errors="replace"):
        m = re.match(r"^(M\d+_\S+)\s+(\d+/\d+)\s+(.*)$", line.rstrip())
        if m:
            cur = m.group(1)
            p[cur] = [m.group(2), m.group(3).strip()]
        elif cur and line.startswith(" " * 32):
            p[cur][1] += " " + line.strip()
        elif line.strip() == "" or line.startswith("-"):
            cur = None
    return p


def main():
    pred = predictions()
    names = sorted([f[:-4] for f in os.listdir(D) if f.endswith(".raw")],
                   key=lambda n: (0, 0) if n == "BASE" else (1, int(re.match(r"M(\d+)", n).group(1))))
    miss = 0
    for n in names:
        score, fails, done, nrows = SU.read_one(os.path.join(D, n + ".raw"))
        pv = pred.get(n, ["--", ""])[0]
        flag = ""
        if not done:
            flag += "  *** NO LCABADVAL_DONE ***"
        if nrows != 58:
            flag += "  *** %d row lines, not 58 ***" % nrows
        if n != "BASE" and pv != "--" and pv != score:
            flag += "  <<< PREDICTION MISS (predicted %s)" % pv
            miss += 1
        print("")
        print("%s   MEASURED %s%s" % (n, score, flag))
        if n != "BASE":
            print("    edit:      %s" % edit_of(n))
            print("    predicted: %s  -- %s" % (pv, pred.get(n, ["", "(none)"])[1]))
        if nrows != 58:
            print("    reddened:  UNATTRIBUTABLE -- the log does not carry 58 row lines")
        else:
            print("    reddened:  %s" % (", ".join(fails) if fails else "NONE -- *** CLEAN SWEEP ***"))
    print("")
    print("PREDICTION MISSES: %d of %d mutants" % (miss, len(names) - 1))


if __name__ == "__main__":
    main()
