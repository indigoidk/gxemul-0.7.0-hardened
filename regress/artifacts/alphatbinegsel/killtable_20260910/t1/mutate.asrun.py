#!/usr/bin/env python3
"""mutate.py -- #520 alphatbinegsel kill-table mutator.

    usage:  mutate.py <mutant-name> <target-file> <baseline-file> [head-file]

Copies BASELINE over TARGET, then applies the named mutation in place.

TWO RULES THIS ENFORCES, both paid for by earlier rounds:

  1. MUTANT-TEXT-NOT-FOUND IS A HARD FAIL (exit 9), never a silent no-op.
     That turns every mutant into a PRESENCE PIN on the fix's own text: if the
     guard is ever reworded, the table refuses to run rather than quietly
     measuring an unmutated binary and reporting it as a kill.

  2. THE BASELINE IS THE REPO, NEVER THE SCRIPT'S OWN BACKUP.  The caller
     passes GXEMUL-SEC's copy directly.  A crashed run once left a tree mutant,
     so the next run's "orig" backup captured the mutant and its restore
     restored it.

Every mutation is a SINGLE SMALLEST EDIT to the guard, except HEAD, which is a
whole-file replacement with the committed pre-fix source (the null medium).
"""
import sys, os, shutil

GUARD = "(int64_t)a0 >= 1 && (int64_t)a0 <= 3"

# name -> (old, new).  None means "no edit" (BASE) or handled specially (HEAD).
MUTANTS = {
    "BASE": None,
    "M_A":  (GUARD, "(int64_t)a0 >= 2 && (int64_t)a0 <= 3"),
    "M_B":  (GUARD, "(int64_t)a0 >= 1 && (int64_t)a0 <= 2"),
    "M_C":  (GUARD, "(int64_t)a0 >= 1 && (int64_t)a0 <= 4"),
    "M_D":  (GUARD, "(int64_t)a0 >= 0 && (int64_t)a0 <= 3"),
    "M_E":  (GUARD, GUARD + " && a1 != 0"),
    "HEAD": "whole-file",
}

def main():
    if len(sys.argv) < 4:
        sys.stderr.write(__doc__)
        return 2
    name, target, baseline = sys.argv[1], sys.argv[2], sys.argv[3]
    head = sys.argv[4] if len(sys.argv) > 4 else None

    if name not in MUTANTS:
        sys.stderr.write("MUTATE: unknown mutant %s\n" % name)
        return 2

    spec = MUTANTS[name]

    if spec == "whole-file":
        if not head or not os.path.exists(head):
            sys.stderr.write("MUTATE: HEAD needs a head-file argument\n")
            return 9
        shutil.copyfile(head, target)
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            body = f.read()
        # Presence pin in the other direction: the null medium must NOT contain
        # the fix, and MUST contain the pre-fix guard.
        if GUARD in body:
            sys.stderr.write("MUTATE: HEAD file still contains the FIX guard\n")
            return 9
        if "if (a0 >= 1)" not in body:
            sys.stderr.write("MUTATE: HEAD file lacks the pre-fix guard\n")
            return 9
        print("MUTATE %s: whole-file null medium installed" % name)
        return 0

    shutil.copyfile(baseline, target)
    if spec is None:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            body = f.read()
        if GUARD not in body:
            sys.stderr.write("MUTATE: BASE lacks the fix guard -- wrong baseline\n")
            return 9
        print("MUTATE %s: baseline installed unmutated" % name)
        return 0

    old, new = spec
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        body = f.read()
    n = body.count(old)
    if n != 1:
        sys.stderr.write("MUTATE %s: MUTANT TEXT NOT FOUND UNIQUELY "
                         "(%d occurrences of %r)\n" % (name, n, old))
        return 9
    body = body.replace(old, new)
    with open(target, "w", encoding="utf-8", newline="") as f:
        f.write(body)
    print("MUTATE %s: %r -> %r" % (name, old, new))
    return 0

if __name__ == "__main__":
    sys.exit(main())
