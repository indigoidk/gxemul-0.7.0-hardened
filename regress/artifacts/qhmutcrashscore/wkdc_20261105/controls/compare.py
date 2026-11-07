#!/usr/bin/env python3
"""compare.py -- the CONTROLS table, read mechanically from the witness logs that run_controls.sh and
run_w1r479.sh wrote.  Every expectation is written HERE, before reading, and each line prints
PASS only when the log says exactly what the expectation says.

  SAME   the FIX line is byte-identical to the HEAD line (a genuine kill / survivor / valid run)
  <re>   the FIX line matches this regex (the refused crash), AND the HEAD line matches its own regex
         (the witness: HEAD scored the crash as a table result)
Writes controls/CONTROLS.txt; exit 0 only if every row PASSes.
"""
import io, os, re, sys

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WI = os.path.join(W, "witness")


def rd(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def section(log, start, stop):
    t = rd(log)
    a = t.find(start)
    b = t.find(stop, a + 1) if a >= 0 else -1
    return t[a:b] if a >= 0 and b > a else None


def line_for(text, label):
    for l in (text or "").splitlines():
        if re.match(r"\s*%s\b" % re.escape(label), l) or re.search(r"\bmutant %s is DETECTED" % re.escape(label), l) \
                or (label.startswith("~") and label[1:] in l):
            return l.rstrip()
    return None


ROWS = []   # (witness, label, head_re, fix_expect)


def W1():
    h = section(os.path.join(WI, "k479", "W1_HEAD.log"), "the driver's own output", "ground truth")
    f = section(os.path.join(WI, "k479", "W1_FIX.log"), "the driver's own output", "ground truth")
    spec = [("~5 rows, 0 failures", None, "SAME"),
            ("Mk_kill", r"KILLED +2 red", "SAME"),
            ("Ms_survive", r"\*ESCAPED\* \(clean sweep", "SAME"),
            ("Mc_early", r"\*ESCAPED\* \(clean sweep", r"NOLOG +rc=136: no WDC_IDENTIFY_ sentinel"),
            ("Mc_late", r"KILLED +1 red", r"NOLOG +rc=136: no WDC_IDENTIFY_ sentinel"),
            ("Mx_exit1", r"KILLED +1 red", r"NOLOG +rc=1: no WDC_IDENTIFY_ sentinel"),
            ("Mcf_nocompile", r"KILLED +does not compile", r"BUILDFAIL does not compile -- not a measurement")]
    return [("W1 kill479.sh, stub detectors", lab, line_for(h, lab), hre, line_for(f, lab), fx) for lab, hre, fx in spec]


def W1R():
    d = os.path.join(WI, "k479real", "r479src")
    h, f = rd(os.path.join(d, "HEAD", "driver.out")), rd(os.path.join(d, "FIX", "driver.out"))
    return [("W1R kill479.sh, REAL #479 detector (80 rows)", "whole driver output", h.strip(), None, f.strip(), "SAME")]


def W2(stub):
    h = section(os.path.join(WI, "g3", "W2_HEAD.%s.log" % stub), "the gate's own output", "ground truth")
    f = section(os.path.join(WI, "g3", "W2_FIX.%s.log" % stub), "the gate's own output", "ground truth")
    rows = []
    if stub in ("allkill", "real"):
        hh = "\n".join(l for l in (h or "").splitlines() if not l.startswith("gate script"))
        ff = "\n".join(l for l in (f or "").splitlines() if not l.startswith("gate script"))
        return [("W2 gate 3, %s" % stub, "whole gate output", hh.strip(), None, ff.strip(), "SAME")]
    want = {"mixed": {"revert287": ("ok", "SAME"), "flushband": ("ok", "SAME"), "tiesaway": ("FAIL.*got=1 want=0", "SAME"),
                      "modeignored": (r"ok .* 0$", r"FAIL .*got=NOLOG rc=136 want=0"),
                      "wlegacyrounds": (r"ok .* 0$", r"FAIL .*got=NOLOG rc=136 want=0"),
                      "revert303": (r"ok .* 0$", r"FAIL .*got=NOLOG rc=1 want=0"),
                      "maskcarry": (r"ok .* 0$", r"FAIL .*got=NOLOG rc=0 want=0")},
            "allcrash": dict((m, (r"ok .* 0$", r"FAIL .*got=NOLOG rc=136 want=0")) for m in
                             ("revert287", "tiesaway", "modeignored", "wlegacyrounds", "revert303", "maskcarry",
                              "flushband"))}[stub]
    rows.append(("W2 gate 3, %s" % stub, "control row", line_for(h, "~unmutated source passes gate 2"), r"ok .* 1$",
                 line_for(f, "~unmutated source passes gate 2"), "SAME"))
    for m, (hre, fx) in want.items():
        rows.append(("W2 gate 3, %s" % stub, m, line_for(h, m), hre, line_for(f, m), fx))
    gh = re.search(r"selftest-float-emul-can-fail: (PASS|FAIL)[^\n]*", h or "")
    gf = re.search(r"selftest-float-emul-can-fail: (PASS|FAIL)[^\n]*", f or "")
    gwant = {"mixed": (r"FAIL \(1 of 15", r"FAIL \(5 of 15"), "allcrash": (r"PASS \(15 checks", r"FAIL \(7 of 15")}[stub]
    rows.append(("W2 gate 3, %s" % stub, "GATE VERDICT", gh.group(0) if gh else None, gwant[0],
                 gf.group(0) if gf else None, gwant[1]))
    return rows


def W3():
    h = section(os.path.join(WI, "r5c", "W3_HEAD.log"), "the scorer's own output", "ground truth")
    f = section(os.path.join(WI, "r5c", "W3_FIX.log"), "the scorer's own output", "ground truth")
    spec = [("BASE", r"6/6/6/11 +ok", "SAME"), ("Ms", r"\*\*\* ESCAPED", "SAME"), ("Mk", r"5/6/5/11 +killed", "SAME"),
            ("Mc ", r"/// +killed", r"NOLOG rc=1 +NOLOG -- the census did not finish; not scored"),
            ("Mc2", r"6/6// +killed", r"NOLOG rc=1 +NOLOG -- the census did not finish; not scored")]
    return [("W3 killrow5c.sh scorer, stub census", lab.strip(), line_for(h, lab.strip()), hre, line_for(f, lab.strip()), fx)
            for lab, hre, fx in spec]


def main():
    rows = W1() + W1R() + W2("mixed") + W2("allcrash") + W2("allkill") + W2("real") + W3()
    out, bad = [], 0
    for wit, lab, hl, hre, fl, fx in rows:
        if hl is None or fl is None:
            ok, why = False, "line not found (HEAD %s, FIX %s)" % (hl is not None, fl is not None)
        elif fx == "SAME":
            ok = hl == fl and (hre is None or re.search(hre, hl) is not None)
            why = "FIX byte-identical to HEAD" if hl == fl else "FIX DIFFERS from HEAD"
            if hl == fl and hre is not None and not re.search(hre, hl):
                why = "identical, but HEAD's line is not the expected genuine result"
        else:
            hok = re.search(hre, hl) is not None if hre else True
            fok = re.search(fx, fl) is not None
            ok = hok and fok
            why = "HEAD scored it as a table result%s; FIX %s" % ("" if hok else " -- NOT AS EXPECTED",
                                                                    "refused it" if fok else "DID NOT refuse it as expected")
        bad += not ok
        out.append("%-4s %-44s %-14s %s" % ("PASS" if ok else "FAIL", wit, lab, why))
        if fx != "SAME" or not ok:
            out.append("        HEAD: %s" % (hl or "-")[:118])
            out.append("        FIX : %s" % (fl or "-")[:118])
    out.append("CONTROLS: %d of %d rows as expected" % (len(rows) - bad, len(rows)))
    out.append("COMPARE_DONE")
    io.open(os.path.join(W, "controls", "CONTROLS.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n".join(out))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
