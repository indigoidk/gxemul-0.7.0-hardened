#!/usr/bin/env python3
"""Offline check: does `wait()` fail on SILENCE, or merely on ELAPSED TIME?

WHY THIS EXISTS.  Every pty probe in this tree waited on an ABSOLUTE deadline --
`t = time.time()` once, then `while time.time() - t < timeout`.  That budget is
spent by the CLOCK, not by the guest, so a boot that normally takes 40 s and takes
90 s on a loaded host FAILS -- while bytes were arriving steadily the whole time.
A run that is merely SLOW was indistinguishable from one that is STUCK, and the
battery could only be trusted on an idle machine.

#467 makes the deadline an INACTIVITY deadline: the clock resets whenever the
buffer grows.  `timeout` then means SILENCE, which is the thing actually worth
failing on.

WHAT A PRINT CANNOT PROVE.  Reading the converted source tells you the assignment
is there; it does not tell you the LOOP honours it.  This file proves the
behaviour instead, against a stub in place of the emulator -- no rig, no build, no
wall-clock oracle of its own, so it is as load-insensitive as the property it
defends.

THE STRADDLE.  Two legs, and BOTH must hold or the conversion is worthless:

  SLOW-BUT-PROGRESSING   a stream that emits steadily and finishes well past the
                         deadline.  The OLD shape FAILS it -- that IS the defect
                         -- and the NEW shape must PASS.
  GENUINELY STUCK        a stream that emits nothing at all.  BOTH shapes must
                         FAIL.  This leg is the one that matters: a conversion
                         that made the timeout unreachable would sail through the
                         first leg and defend nothing.

The two legs are deliberately opposite in sign.  A change that passes only the
first has not fixed the timeout, it has REMOVED it.

NOT COVERED, and deliberately: `free_run(seconds)` is NOT converted anywhere.  It
is not a timeout -- it is an EXPOSURE WINDOW that runs the guest for a set period
and then SIGINTs.  Converting it would change the experiment rather than protect
it, and a naive sweep over `time.time()` sites would have eaten it.
"""
import io
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

#  The probes converted by #467.  A file listed here MUST carry the reset; a file
#  that loses it silently reverts to the absolute deadline, which is exactly the
#  regression this selftest exists to catch.
CONVERTED = ("fbpending_drain_probe.py", "fbpending_witness.py")

FAILS = 0


def check(label, got, want):
    global FAILS
    ok = (got == want)
    if not ok:
        FAILS += 1
    print("  %-46s %-10s %-10s %s" % (label, got, want, "ok" if ok else "FAIL"))


class Stub(object):
    """Stands in for the pty side of a probe.  `chunks` is what arrives per tick;
    a None entry is a tick that produces nothing."""

    def __init__(self, chunks):
        self.buf = ""
        self.chunks = list(chunks)
        self.dead = False

    def rd(self, t=0.01):
        time.sleep(0.004)
        if self.chunks:
            c = self.chunks.pop(0)
            if c:
                self.buf += c
        return True


def wait_absolute(s, timeout):
    """The PRE-#467 shape, kept here as the negative control.  Do not 'fix' it."""
    t = time.time()
    while time.time() - t < timeout:
        if not s.rd():
            return False
        if s.buf.rstrip().endswith("GXemul>"):
            return True
    return False


def wait_inactivity(s, timeout):
    """The #467 shape: the clock resets on progress, so `timeout` means SILENCE."""
    t = time.time()
    seen = len(s.buf)
    while time.time() - t < timeout:
        if not s.rd():
            return False
        if len(s.buf) != seen:
            seen = len(s.buf)
            t = time.time()
        if s.buf.rstrip().endswith("GXemul>"):
            return True
    return False


def main():
    print("selftest_inactivity: does wait() fail on SILENCE or on ELAPSED TIME?")
    print("  %-46s %-10s %-10s %s" % ("row", "got", "want", ""))

    #  LEG 1 -- slow but progressing.  Sixty ticks of steady output against a
    #  deadline far shorter than the total run.  This is the loaded-host case.
    slow = ["x"] * 60 + ["GXemul>"]
    check("slow-but-progressing: OLD absolute shape fails",
          "fails" if not wait_absolute(Stub(slow), 0.12) else "passes", "fails")
    check("slow-but-progressing: NEW inactivity shape passes",
          "passes" if wait_inactivity(Stub(slow), 0.12) else "fails", "passes")

    #  LEG 2 -- genuinely stuck.  No output at all.  BOTH must still fail, or the
    #  conversion removed the timeout instead of repairing it.
    stuck = [None] * 400
    check("genuinely stuck: OLD absolute shape fails",
          "fails" if not wait_absolute(Stub(stuck), 0.12) else "passes", "fails")
    check("genuinely stuck: NEW inactivity shape STILL fails",
          "fails" if not wait_inactivity(Stub(stuck), 0.12) else "passes", "fails")

    #  LEG 3 -- the converted probes still carry the reset.  Source presence only:
    #  behaviour is proven above, this catches a silent revert.
    for f in CONVERTED:
        p = os.path.join(HERE, f)
        try:
            t = io.open(p, encoding="utf-8", errors="replace").read()
        except IOError:
            check("%s readable" % f, "no", "yes")
            continue
        has = bool(re.search(r"seen\s*=\s*len\(self\.buf\)", t)
                   and re.search(r"if len\(self\.buf\) != seen:", t))
        check("%s keeps the #467 reset" % f, "yes" if has else "no", "yes")

    print("SELFTEST_INACTIVITY_%s" % ("PASS" if FAILS == 0 else "FAIL"))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
