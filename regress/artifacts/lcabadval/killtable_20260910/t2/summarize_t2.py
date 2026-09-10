#!/usr/bin/env python3
#
#  #518 table 2 -- turn the <mutant>.raw logs into TABLE2.out.
#
#  ROW NAMES ARE ZIPPED POSITIONALLY, NOT PARSED OUT OF THE LINE.  The probe prints
#  "%-14s %-24s %-24s %-52s %s" and several row names are LONGER than their 14-column field
#  ("wmask0 declined" is 15), so a column-based split silently mis-cuts exactly the rows the
#  padded-column trap warns about.  Every row line ends in " ok" or " FAIL" and the rows are
#  emitted in one fixed order, so the honest reading is: collect the status tokens in order and
#  zip them against the ordered name list below -- and REFUSE (loudly) if the count is not 58,
#  which is the denominator that makes the search checkable.
import os, re, sys

NAMES = []
for a in ("conf", "tbena", "wbase0", "wmask0", "wbase1", "wmask1"):
    NAMES += ["%s live" % a, "%s legal" % a, "%s attrib" % a]
NAMES += ["ctl noguard", "ctl echo"]
NAMES += ["%s stored" % a for a in ("conf", "tbena", "wbase0", "wmask0", "wbase1", "wmask1")]
NAMES += ["wmask0 declined", "wmask0 once", "wmask0 kept2", "wmask1 declined", "wmask1 indep",
          "wmask0 f2", "wmask1 once"]
NAMES += ["conf reserved", "conf once"]
NAMES += ["wen once", "wbase1 wen", "wbase0 zero"]
NAMES += ["def alive", "def w once", "def width", "def read0", "def r once"]
NAMES += ["conf widen", "tbena clear", "wbase0 sg", "wbase0 widen", "wmask0 widen",
          "wmask0 hif", "wen base0"]
NAMES += ["all conf", "all wen", "all m0", "all m1", "all defw", "all defr"]
NAMES += ["wen base1", "wbase1 alone"]
assert len(NAMES) == 58, len(NAMES)

ROW = re.compile(r"^(?P<body>\S.*?)\s+(?P<st>ok|FAIL)$")


def read_one(path):
    """-> (score_str, [failing row names], done_sentinel_ok, n_row_lines)"""
    txt = open(path, errors="replace").read()
    lines = txt.split(chr(10))
    done = any(l.strip() == "LCABADVAL_DONE" for l in lines)
    sts = []
    for l in lines:
        m = ROW.match(l.rstrip())
        if m and not m.group("body").startswith("row "):
            sts.append(m.group("st"))
    score = "?"
    for l in lines:
        if l.startswith("LCABADVAL_RESULT="):
            score = l.split("=", 1)[1].strip()
    fails = []
    if len(sts) == len(NAMES):
        fails = [NAMES[i] for i, s in enumerate(sts) if s == "FAIL"]
    return score, fails, done, len(sts)


def main(d):
    names = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".raw"):
            names.append(f[:-4])

    def key(n):
        if n == "BASE":
            return (0, 0)
        m = re.match(r"M(\d+)", n)
        return (1, int(m.group(1)) if m else 999)
    names.sort(key=key)

    for n in names:
        score, fails, done, nrows = read_one(os.path.join(d, n + ".raw"))
        flag = "" if done else "  *** NO LCABADVAL_DONE SENTINEL ***"
        if nrows != 58:
            flag += "  *** %d row lines, expected 58 -- names NOT attributable ***" % nrows
        print("%-24s %-8s  rows=%d  reds=%d%s" % (n, score, nrows, len(fails), flag))
        if fails:
            print("      reddened: %s" % ", ".join(fails))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
