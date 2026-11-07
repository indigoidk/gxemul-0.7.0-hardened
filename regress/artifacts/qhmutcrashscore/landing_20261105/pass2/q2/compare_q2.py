#!/usr/bin/env python3
"""compare_q2.py -- score each Q2 leg (run_q2.sh) against the research's OWN control expectations: the W2 rows of
_scratchpad/wkdc/controls/compare.py (imported read-only, its expectations written before any log was read), with the
leg's log in the FIX role and the research's HEAD log in the HEAD role.  A row that does not come back as compare.py
expects for the fix is a control that REDS on that gate.  The STAGED gate must red none (the committed bytes re-measure
the research's FIX rows); a mutant must red at least one, or it is a clause-(d) floor breach.  Writes q2/Q2_CONTROLS.txt.
"""
import importlib.util
import io
import os
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
Q = os.path.dirname(os.path.abspath(__file__))
WKDC = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/wkdc"
sp = importlib.util.spec_from_file_location("compare_wkdc", WKDC + "/controls/compare.py")
C = importlib.util.module_from_spec(sp)
sp.loader.exec_module(C)


def evaluate(row):
    wit, lab, hl, hre, fl, fx = row
    if hl is None or fl is None:
        return False, "line not found (HEAD %s, gate %s)" % (hl is not None, fl is not None)
    if fx == "SAME":
        ok = hl == fl and (hre is None or re.search(hre, hl) is not None)
        return ok, ("byte-identical to HEAD" if hl == fl else "DIFFERS from HEAD")
    hok = re.search(hre, hl) is not None if hre else True
    fok = re.search(fx, fl) is not None
    return hok and fok, ("refused, as the fix must" if fok else "NOT refused as the fix must be")


out, summary = [], []
for gate in ("STAGED", "M_q2a", "M_q2b"):
    reds, total = [], 0
    for stub in ("allcrash", "mixed", "allkill"):
        tmp = tempfile.mkdtemp(prefix="q2cmp_")
        os.makedirs(os.path.join(tmp, "g3"))
        shutil.copyfile(os.path.join(WKDC, "witness", "g3", "W2_HEAD.%s.log" % stub),
                        os.path.join(tmp, "g3", "W2_HEAD.%s.log" % stub))
        shutil.copyfile(os.path.join(Q, "g3", "W2_%s.%s.log" % (gate, stub)),
                        os.path.join(tmp, "g3", "W2_FIX.%s.log" % stub))
        C.WI = tmp
        for row in C.W2(stub):
            total += 1
            ok, why = evaluate(row)
            out.append("%-4s %-7s %-9s %-14s %s" % ("ok" if ok else "RED", gate, stub, row[1], why))
            if not ok:
                reds.append("%s/%s" % (stub, row[1]))
                out.append("        gate's line: %s" % ((row[4] or "-")[:110]))
        shutil.rmtree(tmp)
    summary.append("%-7s %2d of %d control rows RED%s" % (gate, len(reds), total,
                   (": " + ", ".join(reds)) if reds else ""))
out.append("")
out += summary
staged_clean = summary[0].split()[1] == "0"
mut_caught = all(int(s.split()[1]) > 0 for s in summary[1:])
out.append("Q2_CONTROLS: STAGED %s; mutants %s" % ("clean (0 red)" if staged_clean else "*** NOT CLEAN ***",
                                                    "each caught by at least one control row" if mut_caught else
                                                    "*** A MUTANT REDS NO CONTROL: clause-(d) floor breach ***"))
out.append("Q2_COMPARE_DONE")
io.open(os.path.join(Q, "Q2_CONTROLS.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
sys.exit(0 if staged_clean and mut_caught else 1)
