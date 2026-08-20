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
SHAPE = re.compile(r"^(boot:\S|probe:\S|construction:\S|harness:\S|none\b)")


def main(argv):
    listing = "--list" in argv
    ledger = json.load(io.open(LEDGER, encoding="utf-8"))

    missing, malformed, ok, grandfathered = [], [], 0, 0
    for row in ledger["rows"]:
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
    if not missing and not malformed:
        print("WITNESS_PASS  every row that closed with commits since the rule names its witness")
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
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
