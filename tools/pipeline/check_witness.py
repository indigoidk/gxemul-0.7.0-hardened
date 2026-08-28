#!/usr/bin/env python3
"""A ROW THAT CLOSES WITH COMMITS MUST NAME THE ARTEFACT THAT WITNESSED THE DEFECT.

Adopted 2026-08-19 as part of the WITNESS LADDER, and specified by the flagship seat that
adjudicated it: *"Enforcement: one check in precommit_check.sh -- any ledger row entering a
closed state with a non-empty `commits` must carry a `witness` field."*

**WHY IT IS NEEDED, and this is measured rather than argued.** Asked whether the tightened
reproducibility rule would retroactively invalidate any shipped round, a measure seat found the
answer was no -- but that answering it AT ALL required reading round PROSE, because the ledger
schema is id/title/state/commits/entries/hold and nothing names the witnessing artefact. That
is the "a check a human has to remember" class this project keeps paying for: the rule cannot
be audited backwards or enforced forwards without a field to hold the answer.

**FORWARD-ONLY, and deliberately.** The 15 rows that closed before this rule existed are
grandfathered exactly as pre-2026-08-16 stages were, for the same reason: a directive cannot
judge work that predates it. Demanding a backfill would either produce 14 guesses or 14 blanks,
and a guessed witness is worse than an absent one -- it reads as evidence.

**WHAT COUNTS**, per the ladder's four rungs:
    boot:<rig/gate>          a real driver reached the path unaided                (rung 4)
    probe:<path>             a real guest instruction through real address decode  (rung 3)
    construction:<gate>      ONLY where construction is itself the defective path  (rung 2)
    harness:<what proved it> the round's subject IS the test apparatus, so there is
                             no guest path to witness -- see below
    detector:<path>          a fix whose evidence is an offline differential plus a
                             measured kill table -- see the BOUND below
    none                     documented-only; no code shipped, or explicitly filed

**`harness:` IS A GAP IN THE LADDER, FOUND BY THIS CHECK ON ITS FIRST RUN.** The ladder's four
rungs all assume the closed row is an EMULATOR defect with a guest-reachable path. A round whose
subject is the test apparatus -- `gate3scope`, which built the self-mutant helper and its
controls -- ships real commits and has no guest path at all. `none` would be false (code
shipped); `probe:` would be laundering (there is no guest instruction to run). So the vocabulary
needed a fifth term rather than a forced fit, and what it names is the thing that actually proved
the work: for a harness round that is the mutation run itself -- the control going RED without
the fix and GREEN with it.

An `#include`/direct-call harness is NEVER a witness -- it is a DETECTOR, and naming one here
is the laundering this field exists to make visible. The check enforces the SHAPE, not the
truth: it cannot tell whether `probe:foo.py` really preserves routing. That judgement stays
with the panel, which is the honest division -- a script that claimed to validate a witness
would be exactly the false comfort the ladder was written against.

Exit 0 clean, 1 on a violation.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")

#  The rule's start date. Rows whose newest entry predates it are grandfathered.
CUTOFF = "2026-08-19"
#  *** `detector:` ADOPTED 2026-08-27 BY OWNER DECISION, WITH A BOUND. ***
#
#  THE GAP IT FILLS.  Three rounds -- b115 (#472), wdcringambig/wdcrearmzero (#473) and
#  fbclearread (#474) -- each shipped a REAL FIX to emulator code whose only evidence is an
#  offline differential plus a measured kill table.  None of the five existing terms fits:
#  boot:/construction: are false; `probe:` is ACTIVELY DANGEROUS because the shape regex
#  scores it rung-3, which this file's own header calls laundering; `harness:` is admitted
#  only when the round's SUBJECT is the test apparatus, and those three fix emulator code;
#  and `none` means DOCUMENTED-ONLY, so on a round that shipped a fix it asserts that no
#  code changed.  Each round parked at `held` carrying a prose note -- THE NOTE DOING WORK A
#  SCHEMA VALUE SHOULD DO.  Survivable once; at three it is a pattern, and a fourth would
#  have copied whichever note it found.
#
#  *** THE BOUND, AND IT IS NOT OPTIONAL: `detector:` IS NOT A RUNG. ***  It records that a
#  fix shipped with a MEASURED DETECTOR and no guest-path witness.  It ranks BELOW every
#  access witness and it does NOT satisfy the reproduce-before-you-edit step -- a round using
#  it still owes the rung-3 ATTEMPT the 2026-08-27 lifecycle ruling requires, and must record
#  that the attempt was made and what it found.  The one thing it may never mean is 'we did
#  not think to ask'.
#
#  It exists so that `check_witness.py` can tell FIXED-WITH-A-DETECTOR from DOCUMENTED-ONLY,
#  which it could not do before: both had to be written `none`, and that conflation is what
#  made three honest rounds look like three rounds that shipped nothing.
#
#  WHY NOT A PER-ROUND EXEMPTION, which was the other option put to the owner: an exemption
#  is a note, and a note is what already failed here three times.  The cost the owner
#  accepted is real and is written down rather than glossed -- adding a term changes what
#  EVERY future round may claim, which is why the bound above is part of the adoption and
#  not a footnote to it.
SHAPE = re.compile(r"^(boot:\S|probe:\S|construction:\S|harness:\S|detector:\S|none\b)")

#  *** AND THE SHAPE IS NOT THE CLAIM.  A witness field that names a file THAT DOES NOT
#  EXIST passes every check above and is worse than a missing one, because it reads as
#  evidence. ***
#
#  THE ESCALATION TRIGGER FIRED 2026-08-27.  The carrier's pre-specified rule is that the
#  first MEASURED DECISION consumed by a bad citation converts the prose rule into a check.
#  One was: `gdromexitsix` was carried as 'fully panelled and rung-3 witnessed', a round was
#  designed on that basis, and its `probe:` field named two scratchpad scripts that a `find`
#  over the entire project cannot locate.  A sibling grep then found `regress/diff_fb_clear.c`
#  -- cited by TWO more rows, and never a real file.
#
#  MEASURED POPULATION rather than guessed: 73 file citations, THREE resolving to nothing.
#  All three corrected before this landed, so the check is GREEN on arrival -- deliberately,
#  because a rule that retro-fails the archive gets switched off and a switched-off rule
#  protects nothing.
#
#  WHAT IT CANNOT DO, said plainly so a green line is not read as more than it is: it tests
#  EXISTENCE, never whether the named artifact is any good or whether it measures what the
#  row claims.  Those are readings; this is a filesystem test.  It resolves by BASENAME
#  anywhere under the project root rather than by exact path, because artifacts legitimately
#  move between regress/ and regress/artifacts/<row>/ -- a stricter test would fail on honest
#  relocation, which is how a check earns the reputation that gets it disabled.
#
#  `harness:` and `none` are SKIPPED: harness routinely names a FACT rather than a file
#  ('read', 'measured 2026-08-26'), and none names nothing by definition.
CITED = re.compile(r"[A-Za-z0-9_./-]+[.](?:py|c|sh)")


def _project_basenames():
    """Every .py/.c/.sh basename under the project root (two levels up from here)."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
    seen = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [x for x in dirnames if x not in (".git", "__pycache__")]
        for fn in filenames:
            if fn.endswith((".py", ".c", ".sh")):
                seen.add(fn)
    return seen




def main(argv):
    listing = "--list" in argv
    ledger = json.load(io.open(LEDGER, encoding="utf-8"))

    missing, malformed, ok, grandfathered = [], [], 0, 0
    ghosts = []
    names = _project_basenames()
    #  *** THE EXISTENCE CHECK RUNS OVER **EVERY** ROW WITH A WITNESS FIELD, NOT ONLY
    #  CLOSED ONES -- and that scope is the whole point.  MEASURED: scoped to closed rows
    #  it did NOT fire on an injected ghost citation, because all three real defects sat on
    #  rows that are `open` or `held`.  A check that cannot fail on the case that motivated
    #  it is worse than no check, and this one nearly shipped that way. ***
    for row in ledger["rows"]:
        #  *** SCAN ONLY THE OPERATIVE CLAUSE, NOT THE CORRECTION PROSE AFTER IT. ***
        #  This project's corrections QUOTE the text they refute, and a naive scan cannot
        #  tell an assertion from a quotation of one -- the carrier records that exact trap
        #  ('a grep built to find STALE CLAIMS reported a defect that was really an honest
        #  correction quoting the text it refutes').  MEASURED here: correcting two rows to
        #  name their real detector left the check RED, because the correction note quotes
        #  the dead filename.  Corrections in this tree are introduced by `***`, so the
        #  operative citation is everything before the first one.
        #
        #  The cost is honest and bounded: a ghost introduced AFTER a `***` in the same
        #  field is missed.  That is the right trade -- the alternative reds every corrected
        #  row forever, and a check that punishes correction is a check that gets switched
        #  off, which this project has watched happen.
        w0 = (row.get("witness") or "").strip().split("***")[0]
        if w0 and not w0.startswith(("harness:", "none")):
            for m in CITED.findall(w0):
                if m.split("/")[-1] not in names:
                    ghosts.append((row["id"], m))
        if row.get("state") != "closed":
            continue
        if not (row.get("commits") or "").strip():
            continue                      # documented-only closure; nothing shipped
        newest = max([e.get("date", "") for e in row.get("entries", [])] or [""])
        w = (row.get("witness") or "").strip()
        if newest < CUTOFF:
            grandfathered += 1
            if listing and w:
                print("  --    %-14s grandfathered, but names one anyway: %s" % (row["id"], w))
            continue
        if not w:
            missing.append((row["id"], row.get("commits", "")[:16]))
        elif not SHAPE.match(w):
            malformed.append((row["id"], w[:44]))
        else:
            ok += 1
            if listing:
                print("  ok    %-14s %s" % (row["id"], w[:60]))

    print("check_witness: %d closed-with-commits rows named a witness, %d grandfathered "
          "(pre-%s), %d missing, %d malformed"
          % (ok, grandfathered, CUTOFF, len(missing), len(malformed)))
    if ghosts:
        print("    %d witness citation(s) name a file that exists NOWHERE:" % len(ghosts))
        for rid, m in ghosts:
            print("      %-14s cites %s" % (rid, m))
    if not missing and not malformed and not ghosts:
        print("WITNESS_PASS  every row that closed with commits since the rule names its "
              "witness, and every cited artifact exists")
        return 0

    print("WITNESS_FAIL")
    for rid, commits in missing:
        print("    %-14s closed at %s with NO witness field" % (rid, commits))
    for rid, w in malformed:
        print("    %-14s witness %r does not name a rung" % (rid, w))
    print()
    print("  Add one of: boot:<rig/gate>  probe:<path>  construction:<gate>")
    print("              harness:<what proved it>  none")
    print("  An #include/direct-call harness is a DETECTOR, never a witness -- naming one")
    print("  here is precisely the laundering this field exists to make visible.")
    if ghosts:
        print()
        print("  A citation naming a file that does not exist is WORSE than a missing one,")
        print("  because it reads as evidence.  Either restore the artifact, or correct the")
        print("  field to say plainly that the measurement was not preserved.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
