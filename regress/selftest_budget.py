#!/usr/bin/env python3
"""Offline check: is the budget the driver PRINTS the budget it ENFORCES?

WHY THIS EXISTS.  Gate 5 range-checks the constants the driver reports, and until #425 the
driver read them TWICE -- once for the call that enforces them, once for the record block the
gate grades.  MEASURED: mutating only the enforcing read (`budget * 1000` in argument
position) left every printed key identical and every gate row GREEN, while the run went from
stopping at REASON=BUDGET to running past the ceiling to REASON=STALLED.  #425 makes the
driver print what the callee received, which closes the two-reads hole -- but nothing in a
PRINT can prove what a COMPARISON does, so this file proves it behaviourally instead.

THE STRADDLE.  Run the driver three times against a stub in place of the emulator:
  1. a probe leg, only to read `BUDGET=N` FROM THE DRIVER'S OWN OUTPUT -- never a literal.  Passing literals is
     exactly the precedent (gate_ab.sh) that left this hole open: a test that supplies its own
     constants cannot notice that the code under test is using different ones;
  2. a leg whose record reports N-1 instructions MUST NOT stop for the budget;
  3. a leg whose record reports N+1 instructions MUST stop for the budget.
Together those bind the printed number to the enforced threshold FROM BOTH SIDES.  A mutation
at the comparison (`ninstrs > budget * 1000`) or a deleted stop survives every printing scheme
and dies here.

NO EMULATOR, NO RIG, NO BOOT: the stub is a shell one-liner that prints one record and then
sleeps, so the driver's parser and its stopping logic run against the shipped code.  It does
need the image DIRECTORY to exist, because the shipped drive() chdirs there before it opens
anything -- a review seat caught the first version of this file claiming otherwise while gate
2, the OFFLINE gate, would have gone red on a machine without it.  When the directory is
absent this prints a distinguishable SKIP rather than a failure that blames the driver.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import drive_guest                                        # the SHIPPED module

FAILS = 0
ROWS = 0

#  The budget this selftest declares.  It is deliberately SMALL and its own -- the point is
#  the relationship between print and enforcement, not luna88k's calibrated ceiling, and a
#  fixture that borrowed the real constant would move with it and pin nothing.
BUDGET = 1000
STALL = 4
BACKSTOP = 12

#  A WRAPPER, because the rig is injected into THIS process: running drive_guest.py directly
#  would start a fresh interpreter whose RIGS has no such rig, and its usage guard would
#  reject the name.  The wrapper imports the SHIPPED module, injects, and calls the SHIPPED
#  drive() -- the same shape selftest_logdir.py uses.
WRAPPER = '''\
import sys
sys.path.insert(0, %r)
import drive_guest
drive_guest.RIGS["selftest_budget"] = %r
drive_guest.drive("selftest_budget", %r)
'''


def check(name, got, want):
    global FAILS, ROWS
    ROWS += 1
    if got == want:
        print("  ok    %-58s" % name)
    else:
        FAILS += 1
        print("  FAIL  %-58s\n          got  %r\n          want %r" % (name, got, want))


#  The shipped drive() chdirs here before opening anything; this check needs no image
#  CONTENTS, only the directory.  Same guard, same reason, as selftest_logdir.py.
IMAGES = getattr(drive_guest, "IMAGES", "")


def run_leg(tmp, instrs):
    """Drive the shipped driver against a stub that reports `instrs` and then waits."""
    stub = os.path.join(tmp, "stub_%s.sh" % instrs)
    with open(stub, "w") as f:
        #  One record in the -N shape the parser accepts, then stay alive: an emulator that
        #  exits gives REASON=EXITED, which would answer a different question.
        f.write("#!/bin/sh\nprintf '[ %d instrs; i/s=1 avg=1; pc=0x0 <x+0x0>]\\n'\n"
                "sleep 30\n" % instrs)
    os.chmod(stub, 0o755)
    drive_guest.RIGS["selftest_budget"] = {
        "args": [], "boot_wait": BACKSTOP, "boot_pat": r"NEVER_MATCHES_selftest_budget",
        "budget": BUDGET, "stall": STALL, "tries": 1, "steps": [], "markers": [],
    }
    #  A WRAPPER, because the rig is injected into THIS process: running drive_guest.py
    #  directly would hit a fresh interpreter whose RIGS has no such rig, and its usage
    #  guard would reject the name.  The wrapper imports the SHIPPED module, injects, and
    #  calls the shipped drive() -- the same shape selftest_logdir.py uses.
    wrapper = os.path.join(tmp, "wrap_%s.py" % instrs)
    with open(wrapper, "w") as f:
        f.write(WRAPPER % (HERE, drive_guest.RIGS["selftest_budget"], stub))
    out = os.path.join(tmp, "out_%s.txt" % instrs)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LOGDIR=tmp)
    with open(out, "w") as fh:
        subprocess.run([sys.executable, wrapper], stdout=fh, stderr=subprocess.STDOUT,
                       env=env, timeout=120)
    text = open(out, encoding="utf-8", errors="replace").read()
    def key(k):
        m = re.search(r"^%s=(.*)$" % k, text, re.M)
        return m.group(1).strip() if m else None
    return key("REASON"), key("NINSTRS"), key("BUDGET")


def main():
    if not os.path.isdir(IMAGES):
        print("SELFTEST_BUDGET images_dir_absent=yes")
        print("SELFTEST_BUDGET_SKIP")
        return 0
    tmp = tempfile.mkdtemp(prefix="selftest_budget.")
    try:
        #  THREE LEGS, and the first exists only to LEARN THE NUMBER.  The straddle's two
        #  legs are then built from what the driver PRINTED, never from this file's own
        #  constant -- the first version used BUDGET + 1 for the over-leg, which is exactly
        #  the literal-passing the docstring forbids, and a review seat caught the file
        #  breaking its own rule.
        _, _, printed = run_leg(tmp, 1)
        check("the driver reports a budget at all", printed is not None, True)
        if printed is None:
            print("\n%d rows, %d failures" % (ROWS, FAILS))
            print("SELFTEST_BUDGET_FAIL")
            return 1
        n = int(printed)
        check("the printed budget is the one this rig declared", n, BUDGET)

        reason, ninstrs, printed_over = run_leg(tmp, n + 1)
        check("a run PAST the printed budget stops for the budget", reason, "BUDGET")
        check("...and reports the count that crossed it", ninstrs, str(n + 1))

        reason2, _, printed2 = run_leg(tmp, n - 1)
        check("a run UNDER the printed budget does not stop for the budget",
              reason2 != "BUDGET", True)
        check("...and it stopped for a stated reason", reason2 in ("STALLED", "BACKSTOP"), True)
        check("the printed budget is stable across legs", (printed_over, printed2),
              (printed, printed))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n%d rows, %d failures" % (ROWS, FAILS))
    print("SELFTEST_BUDGET_%s" % ("PASS" if FAILS == 0 else "FAIL"))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
