#!/usr/bin/env python3
"""IS THE CHECKPOINT'S HEAD THE ACTUAL HEAD?

`_scratchpad/CHECKPOINT.md` is the file a fresh session reads after `git log` -- it records
what git cannot: uncommitted work, in-flight measurements, and which build trees are dirty.
It carries its OWN staleness rule, in its own text:

    "if this HEAD disagrees with `git -C GXEMUL-SEC log --oneline -1`, re-derive and rewrite
     this file. It has no other authority."

*** THAT RULE WAS ENFORCED BY NOTHING, AND IT DRIFTED TWICE IN ONE SESSION. ***  Once by six
commits, and then again an hour after being rewritten -- caught the second time by a REVIEW
SEAT, which opened the file against the brief's own instruction not to read files and reported
"Checkpoint is stale versus `git log`" before answering the question it was asked.

That is the project's recurring shape: a rule written down, obeyed by hand, and eventually
not. RESUME.md went stale for 26 rounds; the SEAT LEDGER for five days; the queue's held-stage
summary said "nineteen" against a real thirty-four; a gate floor comment read "16 -> 17" while
the code read 18. Each was fixed by hand and each drifted again. The ones that STOPPED
drifting are the ones that got a check.

------------------------------------------------------------------------------------------
SOFT, NOT HARD, and the reason is not timidity.  CHECKPOINT.md is UNTRACKED and lives OUTSIDE
the git root (the repo is `GXEMUL-SEC/`, the checkpoint is at the project root beside it).  A
hard failure would block commits in a fresh clone that has no checkpoint at all, and would
block the legitimate window between making a commit and rewriting the file.  What it must not
do is stay SILENT, because a stale checkpoint is indistinguishable from a current one to the
next session -- which is precisely how it cost 26 rounds once.

Absent file: reported, not failed.  A clone without one is a normal state.
"""
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.normpath(os.path.join(HERE, "..", ".."))
ROOT = os.path.normpath(os.path.join(SEC, ".."))
CKPT = os.environ.get("GXCHECKPOINT") or os.path.join(ROOT, "_scratchpad", "CHECKPOINT.md")

HEADLINE = re.compile(r"^HEAD:\s*`?([0-9a-f]{7,40})`?", re.M)


def main(argv):
    if not os.path.exists(CKPT):
        print("CHECKPOINT_ABSENT  no %s -- normal in a fresh clone, reported not failed"
              % os.path.relpath(CKPT, ROOT))
        return 0

    text = io.open(CKPT, encoding="utf-8", errors="replace", newline="").read()
    m = HEADLINE.search(text)
    if not m:
        print("CHECKPOINT_NO_HEAD  the file names no HEAD, so it cannot be attributed "
              "to any tree state")
        return 1

    claimed = m.group(1)
    actual = subprocess.run(["git", "-C", SEC, "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    if not actual:
        print("CHECKPOINT_NO_GIT  could not read HEAD from %s" % SEC)
        return 1

    if actual.startswith(claimed):
        print("CHECKPOINT_OK  names %s, which is HEAD" % claimed)
        return 0

    behind = subprocess.run(
        ["git", "-C", SEC, "rev-list", "--count", "%s..HEAD" % claimed],
        capture_output=True, text=True).stdout.strip() or "?"
    print("CHECKPOINT_STALE  names %s; HEAD is %s (%s commit(s) later)"
          % (claimed, actual[:7], behind))
    print("                  the file's own rule: re-derive and rewrite it -- "
          "it has no other authority")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
