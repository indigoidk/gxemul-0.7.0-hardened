#!/usr/bin/env python3
"""CAN THIS DETECTOR STILL FAIL WHEN THE CODE IT WATCHES IS BROKEN?

Usage:
    selfmutant.py <harness.c> <subject-relpath> <old-fragment-file> <new-fragment-file> <row-id>

Prints a small report and one of:
    SELFMUTANT_OK        the mutant was applied, the detector went FAIL, and the named row
                         was among the kills, and the PRISTINE build through the same tree
                         still PASSed
    SELFMUTANT_FAIL      the detector did NOT detect the mutant
    SELFMUTANT_SETUP     something about the apparatus is wrong -- anchor missing or not
                         unique, build failed, no verdict token, the control arm failed.
                         NEVER scored as a detection.

Exit 0 only for SELFMUTANT_OK.

------------------------------------------------------------------------------------------
WHY THIS EXISTS.  A measuring seat reproduced the defect: stub check() so it never compares,
and 118 rows across five detectors print `ok`, keep their row counts and identity rows and
verdict tokens, and detect NOTHING -- with every gate-2 assertion green.  Every one of those
assertions greps the detector's own stdout, and all of that stdout is downstream of the one
comparison the stub removes.  They are ONE EQUIVALENCE CLASS.  Only a check that VARIES THE
INPUT and demands the output track it escapes.

The in-detector SELFCHECK row covers the comparator dying (all rows at once).  THIS covers a
different failure: the fixture no longer reaching the code, so a row is live but blind.
Measured as complementary -- neither substitutes for the other.

------------------------------------------------------------------------------------------
FOUR THINGS THIS GETS RIGHT THAT THE OBVIOUS VERSION GETS WRONG, each measured by a seat:

1.  ASSERT THE FAIL TOKEN IS PRESENT, never "the PASS token is absent".  A build failure
    emits NEITHER token, so the negative form is satisfied by a control that never ran.

2.  PIN THE KILL TO THE NAMED ROW.  A verdict-only assertion is VACUOUS on 4 of 5 harnesses:
    stub only the row this mutant was chosen to certify, and other rows still kill the
    mutant, so the control stays green while the row it vouches for has stopped detecting.

3.  THE ANCHOR MUST BE UNIQUE, not merely present.  gate 3's applier tests membership and
    then replaces the first occurrence, so a future duplication silently mutates the wrong
    site -- and a wrong-site mutant that survives looks exactly like a real survivor.  That
    trap has already cost this project a false result once.  count() != 1 is SETUP, not FAIL.

4.  THE DETECTOR REACHES ITS SUBJECT BY A QUOTED RELATIVE INCLUDE (`#include
    "../src/devices/dev_m8820x.c"`), which resolves against the INCLUDING FILE's directory
    first -- so no -I redirection can substitute a mutant.  The mutant tree must contain the
    detector too.  Layout below: everything symlinked pristine except the one real mutated
    file, so the lane compiles what the battery compiles apart from the single edit.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.normpath(os.path.join(HERE, ".."))

#  The same flags gate 2 uses.  -Wl,--gc-sections is load-bearing for several of these
#  (without it the link needs memory_device_register); -lm is harmless.
CC = ("gcc -O2 -std=c99 -D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE "
      "-I../src -I../src/include -I../src/include/thirdparty "
      "-ffunction-sections -fdata-sections -Wl,--gc-sections")

#  *** PER-HARNESS FLAGS, BECAUSE ONE HARDCODED SET IS A LANE THAT COMPILES SOMETHING
#  ELSE. ***  gate 2 builds diff_memory_rw.c with -fno-optimize-sibling-calls, and its own
#  comment calls that LOAD-BEARING: gcc 15.2.1 eliminated the tail call and the
#  loop-not-recursion row passed under the very defect it exists for.  This helper hardcoded
#  a single CC line without it, so for that harness the self-mutant lane compiled DIFFERENTLY
#  from the battery.
#
#  The pristine control arm cannot catch that: both arms are consistently wrong, so it agrees
#  with itself.  A control that compares two copies of the same mistake is the shape this
#  whole round exists to remove.  A reading seat named it; the flag now comes in as an
#  argument so the caller -- which owns the real compile line -- supplies it.
EXTRA_FLAGS = os.environ.get("SELFMUTANT_EXTRA_FLAGS", "")


def out(tag, *msg):
    print("       %-9s %s" % (tag, " ".join(str(m) for m in msg)))


def link_tree(src, dst, real_file=None, real_text=None):
    """Mirror `src` into `dst` with symlinks, except one file written for real."""
    os.makedirs(dst, exist_ok=True)
    for name in os.listdir(src):
        s, d = os.path.join(src, name), os.path.join(dst, name)
        if real_file and os.path.abspath(s) == os.path.abspath(real_file):
            io_write(d, real_text)
        elif os.path.isdir(s):
            if real_file and os.path.abspath(real_file).startswith(os.path.abspath(s) + os.sep):
                link_tree(s, d, real_file, real_text)
            else:
                os.symlink(s, d)
        else:
            os.symlink(s, d)


def io_write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def build_and_run(tree, harness):
    binp = os.path.join(tree, "d")
    cmd = "cd %s/regress && %s %s -o %s %s -lm" % (tree, CC, EXTRA_FLAGS, binp, harness)
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    if p.returncode != 0:
        return None, (p.stderr.strip().splitlines() or ["?"])[0]
    r = subprocess.run([binp], capture_output=True, text=True)
    #  F5: A SIGNAL DEATH IS SETUP, NEVER A VERDICT.  The first version discarded
    #  returncode, so a mutant that died by SIGFPE before printing its verdict was scored
    #  "the detector did NOT report a failure" -- right colour, wrong diagnosis, and the
    #  same class as gate 3's filed #55.  A negative returncode is a signal on POSIX.
    if r.returncode < 0:
        return None, "killed by signal %d before printing a verdict" % (-r.returncode)
    return r.stdout, None


def main(argv):
    if len(argv) != 5:
        print("usage: selfmutant.py <harness.c> <subject-relpath> <old-file> <new-file> <row-id>")
        return 2
    harness, subject, oldf, newf, rowid = argv

    src_subject = os.path.join(SEC, subject)
    old = open(oldf, encoding="utf-8").read()
    new = open(newf, encoding="utf-8").read()
    body = open(src_subject, encoding="utf-8").read()

    #  (3) UNIQUE, not merely present.
    n = body.count(old)
    if n != 1:
        out("SETUP", "anchor occurs %d times in %s (must be exactly 1)" % (n, subject))
        print("SELFMUTANT_SETUP")
        return 1

    tmp = tempfile.mkdtemp(prefix="selfmutant_")
    try:
        for arm, text in (("pristine", body), ("mutant", body.replace(old, new, 1))):
            tree = os.path.join(tmp, arm)
            os.makedirs(tree)
            link_tree(os.path.join(SEC, "regress"), os.path.join(tree, "regress"))
            link_tree(os.path.join(SEC, "src"), os.path.join(tree, "src"),
                      real_file=src_subject, real_text=text)
            stdout, err = build_and_run(tree, harness)
            if stdout is None:
                out("SETUP", "%s arm did not build: %s" % (arm, err))
                print("SELFMUTANT_SETUP")
                return 1
            base = os.path.splitext(harness)[0].upper().replace("DIFF_", "DIFF_")
            passtok = re.search(r"\b([A-Z0-9_]+_PASS)\b", stdout)
            failtok = re.search(r"\b([A-Z0-9_]+_FAIL)\b", stdout)

            if arm == "pristine":
                #  (2b) THE CONTROL ARM.  If the pristine file does not PASS through this
                #  same tree, the lane is not compiling what the battery compiles and every
                #  result from the mutant arm is meaningless.
                if not passtok:
                    out("SETUP", "pristine arm did not PASS through the mutant tree shape")
                    print("SELFMUTANT_SETUP")
                    return 1

                #  *** (5) THE ROW ID MUST NAME EXACTLY ONE ROW. ***  Same trap as the code
                #  anchor, on the other side of the fence, and a reading seat found TWO of
                #  the five shipped pins wrong: footbridge's "zero" does not appear in A1
                #  ("A1 load 0 becomes the full 24-bit span") at all -- it matches B2 and F1,
                #  so that mutant vouched for rows it was not chosen for -- and memory_rw's
                #  "1 KB" matches FOUR rows (G1, G2, Z1, F3), a family rather than a row.
                #  A pin that names a family is satisfied while the row it names is dead.
                named = [l for l in stdout.splitlines()
                         if (l.strip().startswith("ok") or l.strip().startswith("FAIL"))
                         and rowid in l and "@@SELFCHECK@@" not in l]
                if len(named) != 1:
                    out("SETUP", "row id %r names %d rows in the pristine run (must be 1)"
                        % (rowid, len(named)))
                    for l in named[:5]:
                        out("", "  matches: " + l.strip()[:66])
                    print("SELFMUTANT_SETUP")
                    return 1

                #  *** (6) AND IT MUST NOT ALREADY BE FAILING. ***  The helper only checked
                #  that pristine PASSes overall.  A detector carrying a permanent or stray
                #  FAIL line that matches the row id would satisfy the mutant arm's pin
                #  WITHOUT THE MUTANT CAUSING ANYTHING -- a decoy, and the mirror image of
                #  the sentinel-pollution defect this same round had to fix.  Same seat.
                stray = [l.strip() for l in stdout.splitlines()
                         if l.strip().startswith("FAIL") and rowid in l
                         and "@@SELFCHECK@@" not in l]
                if stray:
                    out("SETUP", "the named row ALREADY fails on pristine code: %s"
                        % stray[0][:60])
                    print("SELFMUTANT_SETUP")
                    return 1
                out("ok", "pristine arm through the same tree: %s, row id unique and green"
                    % passtok.group(1))
            else:
                #  (1) FAIL PRESENT, not PASS ABSENT.
                if not failtok:
                    out("FAIL", "mutant applied but the detector did NOT report a failure")
                    print("SELFMUTANT_FAIL")
                    return 1
                #  (2) THE NAMED ROW must be among the kills.
                #  EXCLUDE THE SENTINEL'S OWN PROBE ROWS.  They are deliberate mismatches,
                #  so they print FAIL on the HEALTHY path -- and a pass-2 seat measured that
                #  a rowid as ordinary as "fail" matched one of them and returned OK for a
                #  mutant nothing had caught.  The two controls this round added INTERFERED,
                #  re-opening a defeat the same commit claimed to close.
                killed = [l.strip() for l in stdout.splitlines()
                          if l.strip().startswith("FAIL") and rowid in l
                          and "@@SELFCHECK@@" not in l]
                if not killed:
                    allfails = [l.strip()[:70] for l in stdout.splitlines()
                                if l.strip().startswith("FAIL")]
                    out("FAIL", "detector failed, but NOT via the named row %r" % rowid)
                    for l in allfails[:4]:
                        out("", "  killed by: " + l)
                    print("SELFMUTANT_FAIL")
                    return 1
                out("ok", "mutant killed by the named row: %s" % killed[0][:64])
        print("SELFMUTANT_OK")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
