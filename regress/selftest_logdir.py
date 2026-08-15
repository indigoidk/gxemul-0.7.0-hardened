#!/usr/bin/env python3
"""Offline check: does the harness put BOTH pty logs where $LOGDIR says?

WHY THIS EXISTS, and why it is not a gate-5 row.  #422 measured that in the DEFAULT battery
$LOGDIR is exactly the string drive_guest.py used to hardcode, so a row that merely runs the
battery and looks for the logs finds them whether or not the driver honours the variable -- a
check that cannot fail.  A real detector must point LOGDIR somewhere ELSE, and gate 5 cannot
do that without moving the files gate 6 grades.  So the check runs here, offline, with a stub
in place of the emulator: no gxemul, no image contents, no boot, no rig.

*** IT MUST TEST BOTH HALVES, AND THE FIRST VERSION OF THIS FILE DID NOT. ***
#422 is two edits: lib.sh EXPORTS LOGDIR, and the driver READS it.  The first version set
os.environ in-process and called drive() directly -- so deleting the export from lib.sh left
both rows green.  It tested the driver half and certified the other.  That is the same trap
the file's own comment warned about for `env LOGDIR=...`, walked into one level down; a
review seat caught it.  The check now runs the driver the way the battery does: a child
shell makes a BARE ASSIGNMENT (not an export), sources lib.sh, and execs python.  If lib.sh
loses its export, the value never reaches the child and both rows go red.

WHAT IT ASSERTS, and why it is the FILES and not the driver's own LOG= line.  A half-fixed
driver (console log relocated, raw log still hardcoded) was measured to print a LOG= line
pointing into the private directory while the raw log escaped.  Reading the driver's claim
would have called that fixed.  Both files are checked by name.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

#  drive() chdirs to the image directory before it opens anything.  That path is absolute
#  and machine-specific, and this check needs no image CONTENTS -- but it cannot run without
#  the directory existing.  Say so distinguishably rather than failing as if the driver were
#  broken: a named coverage gap beats a red row that blames the wrong thing.
IMAGES = "/mnt/c/DocumentNoSnc/CC/GXEMUL/_images"

WRAPPER = '''\
import sys
sys.path.insert(0, %r)
import drive_guest
drive_guest.RIGS["selftest"] = {
    "args": [], "boot_wait": 5, "boot_pat": r"NEVER_MATCHES_selftest",
    "tries": 1, "steps": [], "markers": [],
}
try:
    drive_guest.drive("selftest", %r)
except Exception as e:
    print("wrapper_caught=%%s" %% type(e).__name__)
'''


def main():
    if not os.path.isdir(IMAGES):
        print("SELFTEST_LOGDIR images_dir_absent=yes")
        print("SELFTEST_LOGDIR_SKIP")
        return 0

    tmp = tempfile.mkdtemp(prefix="selftest_logdir.")
    try:
        private = os.path.join(tmp, "logs")
        stub = os.path.join(tmp, "stub.sh")
        with open(stub, "w") as f:
            f.write("#!/bin/sh\nprintf 'selftest stub\\n'\nexit 0\n")
        os.chmod(stub, 0o755)

        wrapper = os.path.join(tmp, "wrapper.py")
        with open(wrapper, "w") as f:
            f.write(WRAPPER % (HERE, stub))

        #  A BARE ASSIGNMENT, then source lib.sh: exactly what a census script does, and the
        #  shape that fails when lib.sh does not export.  NOT `env LOGDIR=...`, which would
        #  export from outside and pass with the export missing.
        script = ('LOGDIR="$1"; . "$2/lib.sh"; exec python3 "$3"')
        subprocess.run(["bash", "-c", script, "_", private, HERE, wrapper],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        console = os.path.isfile(os.path.join(private, "drive_selftest.log"))
        raw = os.path.isfile(os.path.join(private, "drive_selftest.raw.log"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("SELFTEST_LOGDIR console_log_in_logdir=%s raw_log_in_logdir=%s"
          % ("yes" if console else "no", "yes" if raw else "no"))
    if console and raw:
        print("SELFTEST_LOGDIR_PASS")
        return 0
    print("SELFTEST_LOGDIR_FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
