#!/usr/bin/env python3
"""mm_parse_control.py -- measure (not read) the claim that _scratchpad/pipe/mutmeasure.py already refuses a run
without its completion sentinel.  Calls mutmeasure.parse() and report-side helpers on SYNTHETIC rundirs written
under wkdc/controls/mm_rundir/; imports mutmeasure with bytecode writing OFF so nothing lands in _scratchpad/pipe/.
Run: python -B mm_parse_control.py
"""
import io, os, sys

sys.dont_write_bytecode = True
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPE = os.path.join(os.path.dirname(W), "pipe")
sys.path.insert(0, PIPE)
import mutmeasure as mm  # noqa: E402

R = os.path.join(W, "controls", "mm_rundir")
os.makedirs(os.path.join(R, "logs"), exist_ok=True)
JOB = {"probe": {"result_re": r"^STUB_RESULT=(\d+)/(\d+)$", "row_re": r"^  (\S+)\s+(ok|FAIL)$",
                 "sentinel": r"^STUB_DONE$"}}
CASES = {   # label: (.st, .out, expected kind, expected red)
    "base":     ("build=ok rc=0 reaped=0 base=base", "  r1 ok\n  r2 ok\nSTUB_RESULT=2/2\nSTUB_DONE\n", "OK", []),
    "Mk_kill":  ("build=ok rc=1 reaped=0 base=base", "  r1 ok\n  r2 FAIL\nSTUB_RESULT=1/2\nSTUB_DONE\n", "OK", ["r2"]),
    "Ms_surv":  ("build=ok rc=0 reaped=0 base=base", "  r1 ok\n  r2 ok\nSTUB_RESULT=2/2\nSTUB_DONE\n", "OK", []),
    "Mc_trunc": ("build=ok rc=136 reaped=0 base=base", "  r1 ok\n  r2 FAIL\n", "NOLOG", None),
    "Mc_late":  ("build=ok rc=136 reaped=0 base=base", "  r1 ok\n  r2 FAIL\nSTUB_RESULT=1/2\n", "NOLOG", None),
    "Mc_empty": ("build=ok rc=136 reaped=0 base=base", "", "NOLOG", None),
    "Mb_fail":  ("build=fail rc=- reaped=0 base=base", "", "BUILDFAIL", None),
}


def main():
    bad = 0
    for lab, (st, out, kind, red) in CASES.items():
        io.open(os.path.join(R, "logs", lab + ".st"), "w", encoding="latin-1", newline="").write(st + "\n")
        io.open(os.path.join(R, "logs", lab + ".out"), "w", encoding="latin-1", newline="").write(out)
    for lab, (st, out, kind, red) in CASES.items():
        r = mm.parse(JOB, R, lab)
        ok = r is not None and r["kind"] == kind and (red is None or r.get("red") == red)
        bad += not ok
        print("%-4s %-9s want %-9s got %-9s red=%s  %s" % ("PASS" if ok else "FAIL", lab, kind, r and r["kind"],
                                                          r and r.get("red"), (r or {}).get("why", "")))
    print("MM_PARSE_CONTROL: %d of %d as expected" % (len(CASES) - bad, len(CASES)))
    print("MM_PARSE_CONTROL_DONE")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
