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
import hashlib
import io
import os
import re
import shutil
import signal
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


#  *** TIMEOUTS, AND THEY ARE NOT SHARED.  A HANG PRODUCED NO TOKEN AT ALL. ***
#  Neither subprocess call had a timeout, so a mutant that loops forever emitted NOTHING --
#  not OK, not FAIL, not SETUP -- and gate 2 wedged with nothing to grade.  Reproduced: an
#  outer `timeout 45` had to fire from outside; the helper never returned.
#
#  The two phases get SEPARATE budgets because they mean different things.  A two-minute
#  compile means the HOST is sick; a spinning run is an EXPECTED mutant outcome and the whole
#  reason this control exists.  Sharing one number would also make the SETUP message unable
#  to name the phase.  Measured on an idle machine across all 12 lanes: slowest build 1.37 s
#  (diskimage_io / diskimage_geom), slowest run 0.31 s (m8820x).  The margins below are ~88x
#  and ~190x, deliberately enormous: `gate_ab` uses 3x and that MEASURABLY false-FAILed a
#  45-minute battery under subagent load.  A too-tight timeout turns a busy host into a red
#  gate, which is the fastest way to get a gate switched off.
BUILD_TIMEOUT = float(os.environ.get("SELFMUTANT_BUILD_TIMEOUT", "120"))
RUN_TIMEOUT = float(os.environ.get("SELFMUTANT_RUN_TIMEOUT", "60"))


def run_bounded(argv, timeout):
    """Run argv, killing the whole PROCESS GROUP on expiry.  Returns (proc_or_None, why)."""
    #  *** start_new_session IS THE LOAD-BEARING PART, AND killpg WITHOUT IT WOULD KILL THE
    #  GATE. ***  A bare subprocess.run(timeout=) kills only the DIRECT child.  Measured: with
    #  a genuine grandchild (the gcc -> cc1 shape) run() raised TimeoutExpired promptly and
    #  left TWO orphans spinning; the same shape under start_new_session + killpg left ZERO.
    #  The orphan is the real hazard, not a wedge -- an abandoned compiler loading the host is
    #  exactly the background load that false-FAILed a battery through a wall-clock oracle.
    #
    #  (A reviewing seat predicted instead that run()'s post-kill DRAIN would block forever on
    #  the grandchild's pipe.  MEASURED FALSE on POSIX: CPython calls process.wait() there,
    #  not communicate(), so nothing drains and nothing blocks.  The conclusion survived the
    #  refutation of its mechanism, which is why the measurement is recorded and not just the
    #  design.)
    #
    #  Without start_new_session the child shares the GATE's process group -- a command
    #  substitution creates no new group in non-interactive bash -- so killpg would be gate
    #  suicide.  Measured: the child's pgid was 32 against the gate's 11.
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)
    try:
        o, e = p.communicate(timeout=timeout)
        return p, (o, e)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            p.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            pass
        return None, "exceeded %gs and was killed" % timeout


def build_and_run(tree, harness, binp):
    cmd = "cd %s/regress && %s %s -o %s %s -lm" % (tree, CC, EXTRA_FLAGS, binp, harness)
    p, res = run_bounded(["bash", "-c", cmd], BUILD_TIMEOUT)
    if p is None:
        return None, "build phase " + res
    if p.returncode != 0:
        return None, (res[1].strip().splitlines() or ["?"])[0]
    r, res = run_bounded([binp], RUN_TIMEOUT)
    if r is None:
        return None, "run phase " + res
    #  F5: A SIGNAL DEATH IS SETUP, NEVER A VERDICT.  The first version discarded
    #  returncode, so a mutant that died by SIGFPE before printing its verdict was scored
    #  "the detector did NOT report a failure" -- right colour, wrong diagnosis, and the
    #  same class as gate 3's filed #55.  A negative returncode is a signal on POSIX.
    if r.returncode < 0:
        return None, "killed by signal %d before printing a verdict" % (-r.returncode)
    return res[0], None


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

    #  *** (3b) THE FRAGMENTS MUST ACTUALLY DIFFER.  THIS IS THE SMALLEST APPARATUS FAILURE
    #  THERE IS -- `cp x.old x.new`, ZERO characters of difference. ***  Constructed and
    #  MEASURED by a seat asked for the smallest escape: the anchor is unique, the write
    #  lands, both arms are byte-identical, the detector correctly does not fail, and the
    #  helper printed "mutant applied but the detector did NOT report a failure" -- the exact
    #  false sentence this round exists to remove, from a two-file copy.
    if old == new:
        out("SETUP", "the .old and .new fragments are identical -- there is no mutant")
        print("SELFMUTANT_SETUP")
        return 1

    tmp = tempfile.mkdtemp(prefix="selfmutant_")
    try:
        #  *** BOTH ARMS BUILD AT THE SAME PATH, AND THAT IS A MEASURED REQUIREMENT, NOT
        #  TIDINESS. ***  The old shape built each arm in its own directory.  Harmless today,
        #  but it makes the binary-identity check below SILENTLY VACUOUS the moment anyone
        #  adds `-g`: MEASURED, with -g and -g3 the PRISTINE arm's binary DIFFERS FROM ITSELF
        #  across two tree paths (debug info records the compilation directory), so "the two
        #  arms differ" becomes true unconditionally and the check stops catching anything
        #  without ever going red.  At one path, with -g3, pristine-vs-pristine is IDENTICAL
        #  and mutant-vs-pristine still differs.  It also saves an entire link_tree.
        tree = os.path.join(tmp, "arm")
        os.makedirs(tree)
        #  real_file goes to BOTH mirrors.  It used to reach only the src one, so a subject
        #  anywhere else -- regress/, tools/ -- was symlinked pristine into both arms and the
        #  mutant text landed NOWHERE.  Each call ignores a real_file that is not under it,
        #  so passing both is safe and makes an out-of-src subject WORK rather than merely be
        #  refused.  Nothing uses one today; refusing would not have been simpler.
        link_tree(os.path.join(SEC, "regress"), os.path.join(tree, "regress"),
                  real_file=src_subject, real_text=body)
        link_tree(os.path.join(SEC, "src"), os.path.join(tree, "src"),
                  real_file=src_subject, real_text=body)

        tree_subject = os.path.join(tree, subject)
        binp = os.path.join(tree, "d")
        digest = {}

        for arm, text in (("pristine", body), ("mutant", body.replace(old, new, 1))):
            #  Rewrite the ONE real file in place, then prove what is there.
            if os.path.islink(tree_subject):
                out("SETUP", "%s is a SYMLINK in the tree -- the mutant would not land"
                    % subject)
                print("SELFMUTANT_SETUP")
                return 1
            io_write(tree_subject, text)

            #  *** (3c) THE MUTATION MUST HAVE LANDED, AND THE TEST IS EXACT TEXT, NOT A
            #  FRAGMENT COUNT. ***  The obvious form -- "the file contains `new` exactly
            #  once" -- is wrong in BOTH directions and was caught before it shipped.  It is
            #  blind to the escapes below, AND it FALSE-ALARMS on a currently-green lane:
            #  MEASURED, diskimage_io's `new` is a suffix-substring of its `old` and that text
            #  occurs FIVE times in src/disk/diskimage.c, so the lane would have gone SETUP
            #  the day the check landed.  Three seats found this independently.
            #
            #  The helper already computed exactly what each arm should contain, so compare
            #  against that.  Immune to substring games and recurrence; it also subsumes
            #  "is the pristine arm really pristine" for free, and catches a truncated write,
            #  newline mangling, or a write misdirected by case-folding.  Read back with
            #  newline="" so universal-newline translation cannot mask a corrupted write.
            got = io.open(tree_subject, encoding="utf-8", newline="").read()
            if got != text:
                out("SETUP", "the %s arm's %s is not the text this helper wrote "
                    "(%d bytes on disk, %d expected)" % (arm, subject, len(got), len(text)))
                print("SELFMUTANT_SETUP")
                return 1

            if os.path.exists(binp):
                os.unlink(binp)
            stdout, err = build_and_run(tree, harness, binp)
            if stdout is None:
                out("SETUP", "%s arm did not build or run: %s" % (arm, err))
                print("SELFMUTANT_SETUP")
                return 1
            digest[arm] = hashlib.sha256(io.open(binp, "rb").read()).hexdigest()
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
                #  *** (7) DID THE MUTANT REACH THE COMPILER AT ALL?  COMPARE WHAT THE
                #  COMPILER PRODUCED, NOT WHAT THIS HELPER WROTE. ***  Every check above is
                #  about the TREE; none of them proves the compiler consumed it.  Three
                #  escapes were CONSTRUCTED AND MEASURED that pass a tree-file postcondition
                #  and still print the false "the detector did NOT report a failure":
                #
                #    * `new` = `old` plus a trailing comment -- lands, compiles, inert;
                #    * SELFMUTANT_EXTRA_FLAGS naming the subject by an ABSOLUTE path, so the
                #      REPO copy is compiled while the tree copy sits there mutated.  That is
                #      the case gate_offline.sh:955-963 already calls "the dangerous one of
                #      the three", and it is why the filing's claim that a tree postcondition
                #      "unifies the three extra-flags hazards" is FALSE -- measured, not
                #      argued;
                #    * a mutation inside a section that -Wl,--gc-sections discards.
                #
                #  Identical binaries mean the mutant is SEMANTICALLY INERT, so "the detector
                #  did not detect it" is not a fact about the detector.  That is sound rather
                #  than heuristic.  Measured across all 12 shipped lanes: mutant differs from
                #  pristine 12/12, and the same source at the same path builds byte-identical
                #  to itself.  Cost 0.048 ms of sha256 against a 1370 ms build.
                #
                #  HONEST LIMIT: sufficient, not necessary.  A mutant CAN change the binary
                #  and still be inert (pure reordering), so this catches a subset -- soundly,
                #  and with zero false alarms on the 12 shipped rows.
                if digest["mutant"] == digest["pristine"]:
                    out("SETUP", "both arms produced a byte-identical binary -- the mutant "
                                 "never reached the compiler, or is inert")
                    print("SELFMUTANT_SETUP")
                    return 1

                #  (1) FAIL PRESENT, not PASS ABSENT.
                #  *** AND A RUN WITH NO TOKEN AT ALL IS SETUP, NOT FAIL. ***  The old form
                #  asked only "is there a FAIL token", so a detector that printed NEITHER
                #  token was scored as a detector failure.  gate_offline.sh:913-925 records
                #  that measured: diskimage_geom's mutant arm reported "the detector did NOT
                #  report a failure" while its named row was in fact RED, because the file had
                #  no verdict token at all.  It was fixed by adding tokens to two detectors,
                #  not in the helper -- so differential #14 would have walked into it again.
                if not failtok and not passtok:
                    out("SETUP", "the mutant arm printed NO verdict token at all -- "
                                 "this says nothing about the detector")
                    print("SELFMUTANT_SETUP")
                    return 1
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
    #  *** AN UNCAUGHT EXCEPTION PRINTED A TRACEBACK AND NO TOKEN -- the smhang symptom
    #  without the hang. ***  MEASURED on the shipped helper: a subject path typo, a missing
    #  fragment file, and a wrong argument count each produced NO SELFMUTANT_* token, and gate
    #  2 grades by `grep -c 'SELFMUTANT_OK' == 1` under the row name "the detector still
    #  detects, via its named row" -- so an apparatus failure was reported as a DETECTION
    #  failure at the gate, which is the whole class this round removes.  The timeout closes
    #  one member; this closes the rest.
    #
    #  The traceback still goes to stderr, because a token without a diagnosis would trade one
    #  silent failure for another.
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except BaseException:
        import traceback
        traceback.print_exc()
        out("SETUP", "the helper itself raised -- this says nothing about the detector")
        print("SELFMUTANT_SETUP")
        sys.exit(1)
