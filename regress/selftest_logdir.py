#!/usr/bin/env python3
"""Offline check: does drive_guest.py put BOTH pty logs where $LOGDIR says?

WHY THIS EXISTS, and why it is not a gate-5 row.  #421-follow-up (d1) measured that in the
DEFAULT battery $LOGDIR is exactly the string the driver used to hardcode, so a row that
merely runs the battery and looks for the logs finds them whether or not the driver honours
the variable -- a check that cannot fail.  A real detector must point LOGDIR somewhere ELSE,
and gate 5 cannot do that without moving the files gate 6 grades.  So the check runs here,
offline, against a stub in place of the emulator: no gxemul, no image, no boot, no rig.

WHAT IT ASSERTS, and why it is the FILES and not the driver's own LOG= line.  A half-fixed
driver (console log relocated, raw log still hardcoded) was measured to print a LOG= line
pointing into the private directory while the raw log escaped to the default one.  Reading
the driver's claim would have called that fixed.  Both files are checked by name.

HOW IT RUNS THE PRODUCER, and why a bare assignment.  lib.sh assigns LOGDIR without export,
so a value set that way never reaches a python child -- that is half of the defect under
test.  A caller that wrote `env LOGDIR=... selftest_logdir.py` would export from OUTSIDE and
pass even with lib.sh's export missing, testing the other half only.  This file therefore
sets os.environ itself and the GATE invokes it plainly; the export in lib.sh is covered by
the battery using the same variable for its own redirections.
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import drive_guest                                     # the SHIPPED module


def main():
    tmp = tempfile.mkdtemp(prefix="selftest_logdir.")
    private = os.path.join(tmp, "logs")
    stub = os.path.join(tmp, "stub.sh")
    with open(stub, "w") as f:
        f.write("#!/bin/sh\nprintf 'selftest stub\\n'\nexit 0\n")
    os.chmod(stub, 0o755)

    #  A rig of our own, named so its log basenames cannot collide with the
    #  drive_<rig>.log files gate 6 grades.  boot_pat never matches: the stub exits, the
    #  driver reports EXITED, and this check is about WHERE the files land, not the boot.
    drive_guest.RIGS["selftest"] = {
        "args": [],
        "boot_wait": 5,
        "boot_pat": r"NEVER_MATCHES_selftest",
        "tries": 1,
        "steps": [],
        "markers": [],
    }

    os.environ["LOGDIR"] = private
    try:
        drive_guest.drive("selftest", stub)             # exit status is not the subject
    except Exception as e:                              # a stub cannot boot; that is fine
        print("SELFTEST_LOGDIR driver_raised=%s" % type(e).__name__)

    console = os.path.isfile(os.path.join(private, "drive_selftest.log"))
    raw = os.path.isfile(os.path.join(private, "drive_selftest.raw.log"))
    print("SELFTEST_LOGDIR console_log_in_logdir=%s raw_log_in_logdir=%s"
          % ("yes" if console else "no", "yes" if raw else "no"))
    shutil.rmtree(tmp, ignore_errors=True)

    if console and raw:
        print("SELFTEST_LOGDIR_PASS")
        return 0
    print("SELFTEST_LOGDIR_FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
