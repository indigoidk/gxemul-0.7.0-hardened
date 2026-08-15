#!/usr/bin/env python3
"""Mutation census for drive_guest.split_stream(), graded by selftest_absorb.py.

WHY A COMMITTED CENSUS, and not a number in a commit message.  A detector's worth is what it
KILLS, and that is measurable -- but only if the measurement can be re-run by someone who was
not there.  The figure that made this necessary was "10/10 parser mutants killed", written
over a census in which five of twenty-two mutants survived: the denominator had been quietly
narrowed to the ones that died.

*** THE DENOMINATOR RULE, enforced by this file rather than remembered. ***
  * the header prints the identity  attempted = killed + survived + faults, and this program
    EXITS NONZERO if that identity does not hold -- a census that cannot count itself is not
    evidence.  HONESTLY: with today's dispatch every mutant lands in exactly one list, so the
    identity cannot currently fail; a review seat named that plainly.  It is a guard against a
    future edit that adds a verdict and forgets a list, not a live check, and it is documented
    as such rather than counted as one;
  * every survivor is NAMED, with a disposition from a closed vocabulary: EQUIVALENT (with the
    argument) or FILED (with a queue id).  "Survivors: none" prints even when there are none,
    because absence must be stated rather than inferred from silence;
  * A CRASH IS A FAULT, NEVER A DETECTION.  A mutant that makes the selftest explode has not
    been caught by a row; counting it as a kill inflates the detector;
  * a substitution that does not apply EXACTLY ONCE is a FAULT, not a survivor -- otherwise a
    renamed variable silently turns the whole census green.
  * FORBIDDEN in any report built from this: a ratio whose denominator is not `attempted`, and
    any subset ("parser mutants", "the ones that matter") unless the excluded complement is
    listed by name with its reason.  EXCLUSION IS A DISPOSITION, NOT A DISAPPEARANCE.

NOTHING IN THE REPOSITORY IS MUTATED.  Each mutant is applied to a COPY of drive_guest.py in a
private directory, with selftest_absorb.py copied beside it; the copied selftest imports the
copied parser through its own sys.path.insert.  The .MUTANT history in this project is what
that provision is for: an interrupted in-place run leaves the tree mutant and poisons every
later measurement.

Usage:  absorb_census.py [workdir]      (default: $LOGDIR/absorb_census, else /tmp/absorb_census)

*** THE WORKDIR IS NEVER DELETED, ONLY THE PER-MUTANT SUBDIRECTORIES THIS PROGRAM CREATES. ***
An earlier version removed the whole directory it was given.  Measured by a review seat:
`absorb_census.py $LOGDIR` destroyed /tmp/gxregress -- the pty logs gate 6 grades -- and the
usage line above was the thing that invited it.  A census that can delete the evidence of
other gates is worse than no census.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

#  (name, exact old text, exact new text, what it breaks).  Each must apply EXACTLY ONCE to
#  drive_guest.py.  The axes are the parser's decisions: the three hold clauses, which string
#  the hold is taken from, the bound, the record regex, the strip loop, and the return.
MUTANTS = [
    ("m01-drop-newline-clause",
     '''if i != -1 and "\\n" not in rest[i:] and len(rest) - i < HOLD_MAX:''',
     '''if i != -1 and len(rest) - i < HOLD_MAX:''',
     "holds a completed line for ever; the boot marker never reaches the body"),
    ("m02-drop-bracket-guard",
     '''if i != -1 and "\\n" not in rest[i:] and len(rest) - i < HOLD_MAX:''',
     '''if "\\n" not in rest[i:] and len(rest) - i < HOLD_MAX:''',
     "a read with no '[' holds its last character for ever"),
    ("m03-drop-bound",
     '''if i != -1 and "\\n" not in rest[i:] and len(rest) - i < HOLD_MAX:''',
     '''if i != -1 and "\\n" not in rest[i:]:''',
     "an unterminated '[' stalls the buffer without limit"),
    ("m04-bound-off-by-one",
     '''len(rest) - i < HOLD_MAX:''',
     '''len(rest) - i <= HOLD_MAX:''',
     "holds one character past the documented bound"),
    ("m05-hold-from-tail",
     '''i = rest.rfind("[")''',
     '''i = tail.rfind("[")''',
     "the hold is taken from the unparsed text, leaking a stripped record back"),
    ("m06-first-bracket",
     '''i = rest.rfind("[")''',
     '''i = rest.find("[")''',
     "an earlier resolved '[' suppresses the hold and a real record leaks"),
    ("m07-rec-drop-instrs",
     '''REC = re.compile(r"\\[ *(\\d+) instrs[^\\]]*\\]\\r?\\n")''',
     '''REC = re.compile(r"\\[ *(\\d+) [^\\]]*\\]\\r?\\n")''',
     "guest text that merely looks bracketed is eaten and a count invented"),
    ("m08-rec-greedy-body",
     '''REC = re.compile(r"\\[ *(\\d+) instrs[^\\]]*\\]\\r?\\n")''',
     '''REC = re.compile(r"\\[ *(\\d+) instrs.*\\]\\r?\\n")''',
     "a record body runs to the line's last ']', swallowing text between records"),
    ("m09-rec-optional-terminator",
     '''REC = re.compile(r"\\[ *(\\d+) instrs[^\\]]*\\]\\r?\\n")''',
     '''REC = re.compile(r"\\[ *(\\d+) instrs[^\\]]*\\]\\r?\\n?")''',
     "the shipped defect: an unterminated record is consumed instead of held"),
    ("m10-rec-drop-cr",
     '''REC = re.compile(r"\\[ *(\\d+) instrs[^\\]]*\\]\\r?\\n")''',
     '''REC = re.compile(r"\\[ *(\\d+) instrs[^\\]]*\\]\\n")''',
     "a CRLF record is never matched"),
    ("m11-strip-keeps-newline",
     '''pos = m.end()''',
     '''pos = m.end() - 1''',
     "the record's own newline is left behind, splitting the guest's line"),
    ("m12-first-count-wins",
     '''n = int(m.group(1))''',
     '''n = n if n is not None else int(m.group(1))''',
     "the FIRST count in a read is reported instead of the last"),
    ("m13-drop-preceding-text",
     '''out.append(tail[pos:m.start()])''',
     '''out.append("")''',
     "guest text before a record is discarded"),
    ("m14-rest-is-whole-tail",
     '''rest = tail[pos:]''',
     '''rest = tail''',
     "already-stripped records are re-emitted as console text"),
    ("m15-hold-slice-drops-head",
     '''out.append(rest[:i])''',
     '''out.append("")''',
     "text before the held '[' never reaches the console"),
    ("m16-hold-keeps-everything",
     '''tail = rest[i:]''',
     '''tail = rest''',
     "the held tail duplicates text already emitted"),
    ("m17-else-drops-rest",
     '''        out.append(rest)
        tail = ""''',
     '''        out.append("")
        tail = ""''',
     "the unheld remainder is dropped entirely"),
    ("m18-never-clears-tail",
     '''        out.append(rest)
        tail = ""''',
     '''        out.append(rest)
        tail = rest''',
     "the tail is never cleared, so text repeats for ever"),
    ("m19-return-empty-tail",
     '''    return "".join(out), tail, n''',
     '''    return "".join(out), "", n''',
     "a held record is silently dropped at the return"),
    ("m20-return-no-count",
     '''    return "".join(out), tail, n''',
     '''    return "".join(out), tail, None''',
     "no count is ever reported, so progress cannot be measured"),
    ("m21-hold-max-huge",
     '''HOLD_MAX = 256''',
     '''HOLD_MAX = 1000000000''',
     "the bound is nominal: any '[' stalls the buffer"),
    ("m22-hold-max-tiny",
     '''HOLD_MAX = 256''',
     '''HOLD_MAX = 1''',
     "no record is ever held, so every split record corrupts a line"),
]


def run_one(work, name, old, new):
    """Apply one mutant to a COPY and grade it. Returns (verdict, detail)."""
    #  Per-mutant subdirectory ONLY.  Never the caller's directory (see the header).
    d = os.path.join(work, "m", name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    src = open(os.path.join(HERE, "drive_guest.py"), encoding="utf-8").read()
    if src.count(old) != 1:
        return "FAULT", "substitution applies %d times, not once" % src.count(old)
    open(os.path.join(d, "drive_guest.py"), "w", encoding="utf-8",
         newline="\n").write(src.replace(old, new))
    shutil.copyfile(os.path.join(HERE, "selftest_absorb.py"),
                    os.path.join(d, "selftest_absorb.py"))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run([sys.executable, os.path.join(d, "selftest_absorb.py")],
                           capture_output=True, text=True, timeout=120, env=env)
    except subprocess.TimeoutExpired:
        return "FAULT", "selftest did not terminate"
    out = p.stdout
    if "SELFTEST_ABSORB_FAIL" in out:
        m = re.search(r"^  FAIL  (\S.*?)\s*$", out, re.M)
        return "KILLED", (m.group(1).strip() if m else "(row name not parsed)")
    if "SELFTEST_ABSORB_PASS" in out:
        return "SURVIVED", "every row stayed green"
    return "FAULT", "no verdict token (rc=%d)" % p.returncode


def main():
    work = (sys.argv[1] if len(sys.argv) > 1
            else os.path.join(os.environ.get("LOGDIR") or "/tmp", "absorb_census"))
    os.makedirs(work, exist_ok=True)
    killed, survived, faults = [], [], []
    try:
        for name, old, new, breaks in MUTANTS:
            verdict, detail = run_one(work, name, old, new)
            print("  %-9s %-28s %s" % (verdict, name, detail))
            {"KILLED": killed, "SURVIVED": survived,
             "FAULT": faults}[verdict].append((name, breaks))
    finally:
        #  A `finally`, because an INTERRUPTED run used to leave its copies behind -- measured
        #  by killing one mid-census.  Residue from a measurement is how this project's shared
        #  log directory got polluted twice.
        try:
            shutil.rmtree(os.path.join(work, "m"))
        except OSError as e:
            print("  NOTE  could not remove %s/m: %s" % (work, e))

    a, k, s, f = len(MUTANTS), len(killed), len(survived), len(faults)
    print("\nABSORB_CENSUS attempted=%d killed=%d survived=%d faults=%d" % (a, k, s, f))
    #  EXCLUSION IS A DISPOSITION, NOT A DISAPPEARANCE.  This census covers REC, not
    #  REC_EOF (drive_guest.py:155, used once at the end-of-run flush).  A review seat
    #  measured that replacing REC_EOF with a pattern that matches nothing SURVIVES every
    #  row, so the gap is real and named rather than implied by its absence.
    print("  EXCLUDED  REC_EOF (end-of-run flush)      FILED (b1w-2): no row reaches it")
    if survived:
        for name, breaks in survived:
            #  A survivor entry names a disposition or it is not an entry.  Until one is
            #  written here by hand, it is FILED against this row -- never silently dropped.
            print("  SURVIVOR %-28s FILED (b1w): %s" % (name, breaks))
    else:
        print("  Survivors: none")
    if a != k + s + f:
        print("ABSORB_CENSUS_FAIL identity attempted=killed+survived+faults does not hold")
        return 2
    print("ABSORB_CENSUS_%s" % ("PASS" if not survived and not faults else "INCOMPLETE"))
    return 0 if (not survived and not faults) else 1


if __name__ == "__main__":
    sys.exit(main())
