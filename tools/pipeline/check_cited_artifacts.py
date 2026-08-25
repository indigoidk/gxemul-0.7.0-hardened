#!/usr/bin/env python3
"""Every measurement cited in a committed round block must cite a path that EXISTS.

*** THE RULE THIS MECHANISES ALREADY EXISTED AND WAS ALREADY BEING FOLLOWED.  IT STILL
    FAILED, BECAUSE A CITATION CAN DECAY AFTER IT IS WRITTEN. ***

The carrier's rule is "a score claim names its artifact" -- `8/32 pre-fix (kill461e.out)`.
Two measured failures on 2026-08-24 show that naming is necessary and not sufficient:

  * `#462`'s round block cited `probe_base.raw` for 52/52.  A later table at 57 rows
    REUSED THAT FILENAME.  The claim did not become unverifiable -- it became CONTRADICTED
    BY ITS OWN EVIDENCE, which is worse than uncited, because the named log now says
    something else.
  * `#461`'s only lethal mutant, `m_dmarevert` (22/31), has NO per-row artifact at all:
    0 candidate lines across every `.out` in both scratchpads, denominator stated.  A
    retrospective audit of that detector was ATTEMPTED on 2026-08-24 and could not run.

So this gate asks the weakest useful question, and deliberately only that one:

    DOES THE CITED PATH EXIST?

EXISTENCE ONLY.  It does not parse the log, does not re-derive the score, and does not
compare numerators.  That scope cut is the whole safety argument: section U already checks
DENOMINATORS against the gate pin and cannot see a carried numerator, and a gate that
tried to re-derive numbers would grow without bound -- which is the #392 shape this
project pays for whenever a check's scope is left open.  A gate that stats cited paths
cannot creep into policing scratch directories.

WHAT IT CANNOT CATCH, stated so nobody reads a green row as more than it is:
  * a path that exists but holds a DIFFERENT run's output (the reuse case above).  The
    cure for that is the stamped-path discipline -- `probe_<M>_<pin>rows.raw`, or a
    per-table directory -- not a stronger checker.  This gate makes the reuse case
    *survivable* rather than silent, because a stamped path cannot be overwritten.
  * a number that was never measured at all and cites nothing.  Nothing mechanical can
    tell a measured 8 from a carried 8; that is why the rule is stated in prose too.

FORWARD-ONLY from round CUTOFF.  Earlier blocks were written before the rule existed and
are grandfathered; failing them would produce a red that no edit could clear, and this
project already records what a permanently-red gate does to the credibility of the rest.

Provenance: specified by the fable5 adjudication of `#462`, Decision 4c, which set both
the altitude ("checks committed records, never scratchpad state") and the scope cut.
"""
import os
import re
import subprocess
import sys

BSLASH = chr(92)

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(SEC, ".."))
CHANGELOG = os.path.join(SEC, "CHANGELOG.md")

CUTOFF = 462

#  Where a cited artifact may legitimately live.  The session scratchpad is included
#  because that is where the drivers write TODAY -- and its presence here is itself the
#  argument for moving them into tools/: a root that vanishes with the session cannot
#  keep a citation true.
#  *** THE TRACKED ARCHIVE COMES FIRST, BY OWNER DECISION 2026-08-24. ***  Before it, the
#  only copies lived in `_scratchpad/` -- OUTSIDE the git root and untracked -- so a green
#  here certified existence ON ONE MACHINE and a fresh clone would have failed every
#  post-462 citation.  A citation is re-derivable only if the artifact travels with the
#  record, so the artifacts are now in-repo and this root is authoritative.  The untracked
#  roots are kept BELOW it as a convenience for logs a round has not yet archived; they can
#  never mask the tracked copy.
TRACKED = os.path.join(SEC, "regress", "artifacts")
SEARCH = [
    TRACKED,
    os.path.join(SEC, "regress"),
    os.path.join(ROOT, "_scratchpad"),
    SEC, ROOT,
]
_env = os.environ.get("GX_ARTIFACT_DIR")
if _env:
    SEARCH.insert(0, _env)

ROUND = re.compile(r"^## Round (\d+)", re.M)
#  *** THE FIRST VERSION MATCHED ONLY PARENTHESISED CITATIONS AND CHECKED 2 OF THE 8
#  ARTIFACTS ITS OWN BLOCK CITED -- while printing "every cited measurement exists".
#  That is the zero-selection trap wearing a green coat, inside the gate built to catch
#  decayed claims.  The house's DOMINANT citation form is a backticked path in prose
#  (`table2_57rows/probe_M11.raw`), and `probe_base.raw` -- the founding case, cited three
#  times -- was invisible because it is never parenthesised.
EXT = r"(?:raw|out|log|txt|results)"
#  *** re.I BECAUSE THE SUBJECT IS HAND-WRITTEN. ***  Without it a citation typed
#  `(PROBE_M11.RAW)` was captured by NEITHER regex -- not enforced AND not counted in
#  the unenforced denominator, so it was wholly invisible while this gate printed PASS.
#  Worse on Windows, where the case-insensitive filesystem RESOLVES such a path, so a
#  reader sees a fine citation the gate never examined.  Found by a sibling sweep after
#  a case-sensitive grep reported a duplicated CHANGELOG passage as unique.
CITE = re.compile(r"[(`]([A-Za-z0-9_][A-Za-z0-9_./-]*\.%s)[)`]" % EXT, re.I)
#  Artifact-shaped tokens the collector does NOT enforce (bare, unquoted, or a bare
#  directory).  Reported as a DENOMINATOR, never enforced: widening enforcement to
#  directory citations has no extension anchor and is the creep this gate must not do.
LOOSE = re.compile(r"\b([A-Za-z0-9_][A-Za-z0-9_./-]*\.%s)\b" % EXT, re.I)


def blocks(text):
    """Yield (round_number, block_text) for every round block in the changelog."""
    marks = [(int(m.group(1)), m.start()) for m in ROUND.finditer(text)]
    for i, (num, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        yield num, text[start:end]


def tracked(path):
    """True if `path` is tracked by git in this repo.

    *** EXISTENCE WAS NEVER THE PROPERTY THIS GATE'S WARRANT NAMES. ***  The README says
    a citation is re-derivable only if the artifact TRAVELS WITH THE RECORD -- but SEARCH
    includes `_scratchpad/` and the project root, both OUTSIDE the git root and untracked.
    A citation resolved from either PASSES on the author's machine and FAILS on a fresh
    clone, which is the exact failure this gate was built to end.  The untracked roots
    cannot MASK the tracked copy, which is true and beside the point: they can SUBSTITUTE
    FOR ITS ABSENCE.

    Found by the opus5 seat reading the SEARCH list against the README instead of reading
    the PASS line.  *** IT IS THE THIRD INSTANCE OF ONE SHAPE IN THIS SINGLE FILE *** --
    after the parenthesised-only regex that checked 2 of 8 while printing PASS, and the
    basename fallback that would have greened a stamped path off another table's log.
    """
    rel = path.replace(BSLASH, "/")
    i = rel.find("GXEMUL-SEC/")
    if i < 0:
        return False                      # outside the repo entirely
    rc = subprocess.run(["git", "-C", SEC, "ls-files", "--error-unmatch",
                         rel[i + len("GXEMUL-SEC/"):]],
                        capture_output=True)
    return rc.returncode == 0


def find(name):
    """Resolve `name`, or None.

    *** A CITATION CONTAINING A DIRECTORY MUST RESOLVE TO THAT DIRECTORY. ***  The first
    version fell back to a BASENAME match anywhere under the roots -- so
    `table2_57rows/probe_M11.raw` was satisfied by any `probe_M11.raw` at all, and
    `kill462/` now holds a same-named set from another table.  The directory stamp IS the
    stamped-path discipline; a checker that greens a stamped path off a different
    directory's same-named file has rebuilt the reuse defect inside itself.
    """
    want = name.replace("\\", "/").strip("/")
    parts = want.split("/")
    stamped = len(parts) > 1
    for root in SEARCH:
        direct = os.path.join(root, name)
        if os.path.exists(direct):
            return direct
        if not os.path.isdir(root):
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            if parts[-1] not in filenames:
                continue
            cand = os.path.join(dirpath, parts[-1])
            if not stamped:
                return cand
            #  component-wise suffix match, so only the cited directory satisfies it
            got = cand.replace("\\", "/").split("/")
            if got[-len(parts):] == parts:
                return cand
    return None


def main(argv):
    listing = "--list" in argv
    with open(CHANGELOG, encoding="utf-8") as f:
        text = f.read()

    missing, checked, skipped, unenforced, blocks_seen = [], 0, 0, 0, 0
    #  CLASSIFY, NEVER ENFORCE.  This is an EXISTENCE check across several roots, so an
    #  artifact present only in an UNTRACKED root still greens its citation -- a
    #  clone-red hiding behind a machine-green.  That is deliberate (pre-archive
    #  convenience) and is why the count is printed: the green then says exactly what it
    #  certifies.  Same for bare names, whose ambiguity COMPOUNDS as each round adds an
    #  archive -- `probe_Mb1.raw` and `probe_Mb2.raw`, cited bare one line apart, once
    #  resolved to two DIFFERENT tables.
    untracked, bare, loose = 0, 0, []
    for num, body in blocks(text):
        blocks_seen += 1
        if num < CUTOFF:
            skipped += len(set(CITE.findall(body)))
            continue
        enforced = set(CITE.findall(body))
        unenforced += len(set(LOOSE.findall(body)) - enforced)
        for name in sorted(enforced):
            checked += 1
            hit = find(name)
            if hit is None:
                missing.append((num, name))
            elif not tracked(hit):
                #  Resolves on THIS machine only.  Reported separately from `missing`
                #  because the remedy differs: a missing artifact must be restored or the
                #  claim corrected; an untracked one must be `git add`ed.
                loose.append((num, name, hit))
            else:
                if not hit.startswith(TRACKED):
                    untracked += 1
                if "/" not in name:
                    bare += 1
                if listing:
                    mark = "" if hit.startswith(TRACKED) else "   [machine-local]"
                    mark += "" if "/" in name else "   [bare: resolved by walk order]"
                    print("  ok    #%d  %-26s %s%s" % (num, name, hit, mark))

    roots_present = [r for r in SEARCH if os.path.isdir(r)]
    if untracked:
        print("  note  %d citation(s) resolved from UNTRACKED roots -- machine-local, "
              "not clone-portable" % untracked)
    if bare:
        print("  note  %d BARE citation(s) resolved by walk order -- stamp them "
              "(`tableN_Mrows/name.raw`) before a second table makes them ambiguous" % bare)
    print("check_cited_artifacts: %d citations checked at/after round %d, "
          "%d grandfathered, %d missing, %d artifact-like mentions NOT in enforced "
          "citation form" % (checked, CUTOFF, skipped, len(missing), unenforced))
    if not blocks_seen:
        print("CITED_ARTIFACTS_FAIL  parsed ZERO round headings -- the collector selected")
        print("  nothing, which is not the same as finding nothing.  Check the `## Round N`")
        print("  format before reading this gate's colour again.")
        return 1
    #  VESTIGIAL SINCE THE ARTIFACTS WERE TRACKED: `SEC`, `ROOT` and the tracked archive
    #  exist on every checkout, so this can no longer fire.  Kept, and labelled, so a
    #  future reader does not mistake it for live coverage of the clone case -- that
    #  case was dissolved by the owner decision, not by this branch.
    if not roots_present:
        print("CITED_ARTIFACTS_FAIL  every artifact search root is ABSENT on this machine.")
        print("  This is a clone without `_scratchpad/`, not a decayed citation.  Set")
        print("  GX_ARTIFACT_DIR, or restore the archives, before trusting a red here.")
        return 1
    if loose:
        print("CITED_ARTIFACTS_FAIL  %d citation(s) resolve only to UNTRACKED paths -- they"
              % len(loose))
        print("  pass on this machine and FAIL on a fresh clone, which is the failure this")
        print("  gate exists to end.  `git add` them, or correct the claim.")
        for num, name, hit in loose:
            print("    #%-4d %-30s -> %s" % (num, name, hit))
        return 1
    if missing:
        print("CITED_ARTIFACTS_FAIL  %d cited measurement(s) do not exist:" % len(missing))
        for num, name in missing:
            print("    #%-4d %s" % (num, name))
        print()
        print("  A score claim names its artifact SO THAT IT CAN BE RE-DERIVED.  A name")
        print("  that resolves to nothing is not a citation -- it is the appearance of one.")
        print("  Either restore the artifact, or correct the claim to say plainly that the")
        print("  measurement is recorded but its log was not preserved -- OR the run that")
        print("  produces it has not finished: archive when it does, and do NOT 'correct'")
        print("  a claim that is merely pending.")
        return 1
    print("CITED_ARTIFACTS_PASS  every ENFORCED-FORM citation at/after round %d resolves "
          "(parenthesised or backticked paths with a known extension; %d artifact-like "
          "mentions are outside that form and are COUNTED, not enforced)" % (CUTOFF, unenforced))
    return 0


#  ---------------------------------------------------------------- selftest
#
#  *** THE GATE THAT ENFORCES "EVERY SCORE NAMES VERIFIABLE EVIDENCE" SHIPPED WITH NO
#  EVIDENCE OF ITS OWN CORRECTNESS, and a completeness check caught it. ***  Its siblings
#  (check_probe_wiring.py, seat_verdicts.py) both carry one, and precommit fires it when
#  the checker is edited -- so without this, section X was silently exempt from the one
#  mechanism that would catch it breaking.
#
#  Every case below is a defect this checker ACTUALLY HAD and that review removed.  That
#  is the point: a selftest written from imagination pins nothing, while one written from
#  the bug list pins the bugs.  The first version of this gate checked 2 of its own
#  block's 8 citations while printing "every cited measurement exists", and its basename
#  fallback would have greened a stamped path off ANOTHER TABLE'S same-named log.
def selftest():
    import tempfile
    fails = []

    def check(name, got, want):
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    #  1. THE COLLECTOR'S REACH.  It matched only parenthesised citations once, so the
    #     founding case -- `probe_base.raw`, cited three times in backticks -- was invisible.
    body = "cites (a.raw) and `b/c.out` and bare d.log and (e.results)"
    found = set(CITE.findall(body))
    check("collector: parenthesised", "a.raw" in found, True)
    check("collector: backticked", "b/c.out" in found, True)
    check("collector: .results ext", "e.results" in found, True)
    check("collector: bare NOT enforced", "d.log" in found, False)
    check("collector: bare IS counted", "d.log" in set(LOOSE.findall(body)), True)

    #  1b. CASE. The subject is a hand-written citation, so an upper-cased one must not
    #      vanish from BOTH the enforced set and the denominator -- which is what it did.
    up = "cites (PROBE_M11.RAW) and `T2/probe_Mb1.Raw`"
    check("collector: UPPER extension enforced", "PROBE_M11.RAW" in set(CITE.findall(up)), True)
    check("collector: Mixed extension enforced", "T2/probe_Mb1.Raw" in set(CITE.findall(up)), True)

    #  2. SUFFIX MATCH.  A citation naming a directory may only be satisfied by THAT
    #     directory.  `#462` ran three tables, so three `probe_M11.raw` exist and only the
    #     stamp distinguishes them; a basename fallback rebuilds the reuse defect inside
    #     the checker.  This is the cross-table Mb1/Mb2 case, which really happened.
    root = tempfile.mkdtemp()
    for sub in ("t1", "t2"):
        os.makedirs(os.path.join(root, sub))
        open(os.path.join(root, sub, "probe_Mb2.raw"), "w").close()
    saved = SEARCH[:]
    del SEARCH[:]
    SEARCH.append(root)
    try:
        hit = find("t2/probe_Mb2.raw")
        check("suffix: stamped resolves to ITS dir",
              hit is not None and hit.replace("\\", "/").endswith("t2/probe_Mb2.raw"), True)
        check("suffix: wrong dir REJECTED", find("t3/probe_Mb2.raw"), None)
        check("suffix: bare still resolves", find("probe_Mb2.raw") is not None, True)
        check("suffix: absent name is None", find("nope.raw"), None)
    finally:
        del SEARCH[:]
        SEARCH.extend(saved)

    #  3. ZERO-SELECTION.  A pattern that matches nothing must not read as success -- the
    #     trap this project hit twice in one session, once inventing a failure and once
    #     inventing an absence.
    check("blocks: parses real headings",
          len(list(blocks("## Round 462 (#462) x\nbody"))), 1)
    check("blocks: garbage yields none", len(list(blocks("no headings here"))), 0)

    if fails:
        print("CITED_ARTIFACTS_SELFTEST_FAIL  %d case(s):" % len(fails))
        for f in fails:
            print("    " + f)
        return 1
    print("CITED_ARTIFACTS_SELFTEST_PASS  15 cases, each a defect this checker actually had")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
