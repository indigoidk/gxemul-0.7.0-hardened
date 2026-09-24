#!/usr/bin/env python3
"""DOES THE LEDGER KNOW ABOUT THE WORK THAT SHIPPED?

Usage:
    check_commit_attribution.py [--list]

    (This line also advertised `[--all]` from the file's first commit, and nothing ever read it;
    removed 2026-09-24 as a wrong record, found by the codex seat.)

The ledger is this project's single source of truth and `gen_dashboard.py` renders the board
from it.  So a row whose work has SHIPPED but whose `commits` field is empty makes the board
under-report finished work and over-report the open queue -- and every decision taken off that
board is then taken off a stale picture.

MEASURED 2026-08-19, which is why this exists.  Of the 40 most recent commits, 33 were named
by NO ledger row.  Most of those are legitimate (a receipt, a records fix, harness work that
closes nothing).  The sharp subset is not:

    commit 6014b7e   subject "selfmutant6 CLOSED: the fifth control, ..."
                     ledger row `selfmutant6`   state=held   commits=(empty)

A commit that announces a row CLOSED, against a row the board still shows as open, is a wrong
record in the direction that matters: it is invisible work.  Thirteen rows were in some form
of this state when the check was written.

------------------------------------------------------------------------------------------
WHAT IT CHECKS, and the three grades are deliberately different failures:

  HARD   a commit subject names row R with a CLOSURE word, and R.state != "closed".
         EXCEPT when R.reopened names that commit: a closure a later pass of the same round
         superseded, with the board saying so (2026-09-05, pcc2widthkills at b78bb0f).
         The commit says the work is done; the board says it is not.  One of the two is
         wrong and neither can be believed until someone looks.

  HARD   R.state == "closed" and a commit subject names R, but R.commits does not list it.
         A closed row that does not name what closed it cannot be attributed -- the same
         defect `nightly_check.sh` fixes for the battery verdict.

  SOFT   a commit subject names an OPEN row that does not list the commit, and either the
         commit is RECORDS-ONLY, or it shipped code and the row's non-empty `commits` names
         other commits ("open row, commits=...").  Progress on an open row is ordinary, so it
         is listed rather than failed and the drift stays visible.  THE GRADES ARE TAKEN IN
         ORDER, and the order decides them: a closure word in the subject grades a non-closed
         row HARD (or REOPENED) before anything else is asked; a row that lists the commit is
         attributed next; only then do records-only and the rest apply -- and a code commit
         against an open row whose `commits` is EMPTY is HARD (main() says why).  (This
         paragraph named only the records-only case, and called the empty-`commits` code case
         SOFT too, until the 2026-09-24 review.)

  SOFT   a commit subject names a CLOSED row whose `commits` is EMPTY.  That is a
         DOCUMENTED-ONLY closure -- a duplicate credited elsewhere, or a row closed with no
         code -- and `check_witness.py` already treats the same shape as legitimate ("nothing
         shipped"), so hard-failing it here would put the two checks in contradiction.  Found
         by this check's FIRST REAL USE, not by a control: rtcdet closed as a duplicate of
         rtcgate with empty commits on purpose, while the commit subjects said "rtcdet", and
         the check demanded the row name a commit it had deliberately declined to claim.

         It stays SOFT rather than silent because the shape is also how someone would DODGE
         the check -- close a row that really did ship with empty commits and the hard rule
         evaporates.  Only the closure note distinguishes the two, and only a reader can
         judge it, so the check names the row and declines to grade it.

------------------------------------------------------------------------------------------
*** THE BLINDNESS IS REPORTED, NOT HIDDEN, AND THAT IS THE POINT OF THE LAST SECTION. ***

Row ids shorter than MIN_ID characters (`n2`, `d1`, `a4`, `b1w`, ...) are NOT matched, because
a two-character token matches English text and would fire on unrelated subjects.  A check that
silently skips a third of its subjects while printing a green line is this project's own named
vacuity class -- "a check whose blindness is reported as a green line".  So the skipped ids are
PRINTED EVERY RUN, with their count, whether or not anything failed.  If you want them covered,
the fix is to give them longer ids, not to lower MIN_ID.

*** THE SECOND BLINDNESS: THIS CHECK IS SUBJECT-DRIVEN, so a row is covered only if some
commit happens to NAME it. ***  Found by a negative control that injected three breaks into
`rtcgate` and saw none of them: two commits shipped that row's work and neither subject says
"rtcgate".  Every injection was invisible, and read at first like three detector failures.
A row can therefore have wrong attribution forever and this check will never look at it.
That set is PRINTED EVERY RUN alongside the short-id set, for the same reason: a check that
silently covers a third of its subjects while printing a green line is the vacuity class this
project named.  Widening it (matching commit BODIES, or a `rows:` trailer) is a real option
and is deliberately not taken here -- bodies quote other rows constantly, which would trade
this silent gap for loud false positives.

Matching is on the SUBJECT LINE only, at word boundaries.  The body is excluded deliberately:
commit bodies here quote other rows constantly ("filed separately as n2/n4/tfreq"), and a
mention is not a claim of authorship.

*** RECORDS-ONLY COMMITS ARE NOT AUTHORSHIP EITHER, AND THE FIRST VERSION OF THIS CHECK GOT
THAT WRONG. ***  It reported three commits -- ef01e28, 716934d, 8631dc0, all named "m8820x:
..." -- as a closed row failing to name what closed it.  Verifying instead of believing showed
all three touch ONLY OUTSTANDING_BUGS.md: they are the round's reproduction and research
records, and the row correctly names its five CODE commits.  A row is authored by what shipped,
not by what was written about it.  So a commit whose every path ends in .md is not a hard
failure on that ground; it is listed as soft when the row is open, and ignored when the row is
closed.  (This said "never a hard failure" until 2026-09-24 -- but a closure word in the subject
grades a non-closed row HARD before the records test is reached.)

That distinction is the check's own version of the rule it exists to serve, and getting it
wrong would have made the gate fire on every research commit this project makes -- the fastest
possible way to have a gate switched off.
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.normpath(os.path.join(HERE, "..", ".."))
LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")

#  How far back to read.  Not "all history": the ledger's `commits` convention is recent, and
#  older rows were closed under different bookkeeping.  Overridable for an audit.
DEPTH = int(os.environ.get("GXATTR_DEPTH", "60"))

#  Below this length a row id is a word, not an identifier.  See the blindness note above.
MIN_ID = 4

#  *** A ROW ID THAT IS ORDINARY PROJECT VOCABULARY FALSE-POSITIVES ON PROSE. ***
#  Measured 2026-08-26: commit 2e1e662's subject reads "...and two more carrier
#  claims measured false", where "carrier" means the auto-loaded instruction file.
#  It collided with the CLOSED row `carrier`, the commit carried real code, and this
#  check hard-failed a commit that has nothing to do with that row.
#
#  THE HEADER ABOVE PREDICTS THIS FAILURE FOR THE OTHER FIELD: it declines to match
#  commit BODIES because "bodies quote other rows constantly, which would trade this
#  silent gap for loud false positives."  The unstated assumption was that SUBJECTS
#  do not quote row names as prose.  In a project whose subjects are written in its
#  own vocabulary, they do.
#
#  MIN_ID does not help -- it guards SHORT ids against general English, and this one
#  is seven characters.  The problem is not length but that the token is a common
#  word HERE.
#
#  So for these ids ONLY, a match requires the token to look like an IDENTIFIER --
#  backticked or quoted -- never bare prose.  NOT a blanket exemption: a subject that
#  names `carrier` in backticks still matches and is still graded.  The set is printed
#  every run, because a check that silently skips subjects while printing a green line
#  is the vacuity class this file's own header names.
SUBJECT_STOPWORDS = {"carrier", "census"}   #  "census" added 2026-09-07: same measured
                                            #  class as "carrier" -- a row id that is also
                                            #  an ordinary English word, so a subject using
                                            #  it as PROSE ("my sibling census had a
                                            #  backwards filter") hard-failed against the
                                            #  CLOSED row `census'.  Controlled both ways
                                            #  on the day: the prose subject stops matching,
                                            #  and a backticked `census' STILL matches.

#  A commit subject claiming the work is finished.  Deliberately narrow -- "gate", "record"
#  and "file" are progress verbs here, not closure verbs, and including them would turn every
#  ordinary round into a hard failure.
CLOSURE = re.compile(r"\b(closed|closes|closing)\b", re.I)

#  *** A LEDGER SHA NAMES A COMMIT WHEN IT IS A PREFIX OF THE FULL HASH -- AND THE FIRST FORM
#  COMPARED ABBREVIATIONS, WHICH GIT LENGTHENS AS ITS PACKED-OBJECT COUNT GROWS. ***  Measured
#  2026-09-24: the rows carry the 7-character form git printed when each closed; a repack at
#  about 2026-09-23 23:54 -- most likely `git gc --auto`, detached by #545's own commit (4264ee20,
#  23:50, the only commit in that window; pack-366ba631 created 23:54:45, packed-refs rewritten
#  23:54:32; 24,350 objects packed) -- made git's own %h 8 characters: the automatic length follows
#  git's approximate packed-object count, and the commit's part was to trigger the repack.  So
#  `h in commits` stopped matching, and
#  six HARD lines on five correctly attributed rows (stagetokens twice) failed at HEAD -- a red
#  gate on every commit, raised by nothing in the ledger.  The mirror case failed too, in the
#  `commits` check, which compared WHOLE TOKENS: a row written at 8 characters did not match a
#  7-character %h.  Section F's receipt check matches by prefix for a related reason (its first
#  version compared a short receipt with a full hash exactly and never matched); so does this,
#  on %H -- keeping the ledger's own 7-40 floor, which section F does not have.  The floor also
#  binds a whole token inside a non-repository note, which bad_commits() does not validate:
#  under core.abbrev=6 a 6-character token there was credited before this fix and is not now
#  -- a deliberate narrowing, pinned by Q22 (at git's automatic minimum, 7, it cannot arise).
#  (regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/; this block said "after
#  4264ee20" and "six ... rows" until the nine-seat review of 2026-09-24 corrected both.)
SHA = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])")


def names(field, full):
    """True when some 7-40 character hex token in a FREE-TEXT field is a prefix of the full hash.

    For `reopened` only.  `commits` is a LIST and is read by lists() below."""
    return any(full.startswith(t) for t in SHA.findall(field or ""))


#  *** `commits` IS A WHITESPACE-SEPARATED HASH LIST, AND THE PREFIX FIX FIRST READ IT AS PROSE. ***
#  Measured 2026-09-24 by the codex seat's adjudication pass: bad_commits() accepts a
#  non-repository NOTE in this field ("outside the repo (ops) ..."), and names() extracts a hex
#  token from anywhere -- so a note that merely MENTIONS a sha, "(cdbe7d75)", credited that
#  commit as authorship where the whole-token test before it graded HARD.  A `commits` token
#  names a commit only when the WHOLE token is 7-40 lowercase hex and prefixes the full hash.
TOKEN = re.compile(r"[0-9a-f]{7,40}")


def lists(field, full):
    """True when a whole whitespace token of a `commits` list is a 7-40 hex prefix of the full hash."""
    return any(TOKEN.fullmatch(t) and full.startswith(t) for t in (field or "").split())


def git(*args):
    r = subprocess.run(["git", "-C", SEC] + list(args), capture_output=True, text=True)
    #  *** FAIL CLOSED.  This returned stdout and dropped the status, so a git that could not
    #  read the repository gave an empty log and "scanned 0 commits deep ... ATTRIBUTION_PASS"
    #  -- a gate passing on nothing (measured 2026-09-24 with GIT_DIR=/nonexistent by three
    #  seats).  The first line is shaped like a HARD row because section L prints only those.
    if r.returncode != 0:
        print("  HARD   --        (git)          --       git %s exited %d: %s"
              % (args[0], r.returncode, " ".join(r.stderr.split())[:160]))
        print()
        print("ATTRIBUTION_FAIL  git could not read the repository")
        sys.exit(2)
    return r.stdout


def records_only(h):
    """True when every path this commit touched is documentation.

    Cheap, and NOT cached -- this said "cached by the caller" until 2026-09-24: it runs once per
    matched (commit, row) pair that reaches it, which is a handful per run rather than the whole
    log."""
    paths = [p for p in git("show", "--name-only", "--format=", h).splitlines() if p.strip()]
    #  *** THE LEDGER IS A RECORD, AND THE FIRST VERSION OF THIS DID NOT KNOW THAT. ***  It
    #  recognised only .md/.txt, so a commit touching ONLY tools/pipeline/ledger.json and
    #  fable_queue.md -- a pure bookkeeping commit that closes a row and queues its held
    #  stage -- was scored as AUTHORSHIP and hard-failed.  Caught on this check's own first
    #  week, by its own output, on a commit written to satisfy a sibling gate.
    #
    #  tools/pipeline/ is the ledger, the queue, the dashboard renderings and the checkers'
    #  own manifests: writing there is recording, never shipping.  Anything outside it -- and
    #  outside regress/artifacts/, below -- that is not .md/.txt is still authorship.
    #
    #  *** THIS COMMENT ALSO SAID "so a fix that edits a checker's LOGIC still counts", AND
    #  FOR THE CHECKERS THAT LIVE HERE IT IS FALSE. ***  tools/pipeline/ holds the checkers'
    #  own sources, .py and .sh, so a commit editing ONLY a checker's logic here is graded as a
    #  record: measured 2026-09-24 on bbfc942e, which changed this file's SUBJECT_STOPWORDS.
    #  At 3e33201d, 28 of the 60 scanned commits touch pipeline code and 3 of those are graded
    #  records-only BECAUSE of this exemption; dropping it for .py/.sh changes no verdict at
    #  depth 60 and gives 8 HARD at full depth -- whether each is hidden drift or a
    #  mis-attribution is a READING: 7 change checker logic, 748c9daf only adds a MANIFEST entry,
    #  and bbfc942e and 86ea7c0e are harness edits inside commits whose subjects name other rows.  FILED
    #  (attrcheckgaps), not changed here: it changes grading and owes its own controls.
    #
    #  *** AND regress/artifacts/ IS A RECORD TOO -- WIDENED 2026-08-31, THE SECOND TIME THIS
    #  PREDICATE HAS BEEN TOO NARROW FOR THE SAME REASON. ***  It fired HARD on 3d30a20, a
    #  records commit whose only non-exempt path was
    #  regress/artifacts/sgideprimop/killtable_20260831/PRETABLE.out -- a pre-table block,
    #  which is evidence written ABOUT a round before its table runs.
    #
    #  That directory holds preserved measurement logs, frozen copies of the tooling a table
    #  ran, session transcripts and pre-table blocks.  `check_probe_wiring.py` already
    #  classifies its python as CLASS_RESEARCH -- in its own words, "evidence, not detectors
    #  the battery owes a run" -- so the two checkers now agree about what that tree is.
    #
    #  The boundary is unchanged and is what keeps this from becoming a hole: a SHIPPED
    #  detector lives in regress/ ITSELF (regress/sgi_re_unmapped_probe.py), not under
    #  artifacts/, and is still authorship.  Only the evidence directory is exempt.
    return bool(paths) and all(
        p.lower().endswith((".md", ".txt"))
        or p.startswith("tools/pipeline/")
        or p.startswith("regress/artifacts/")
        for p in paths)


#  A `commits` value that is neither a hash list nor a DELIBERATE non-repo note.  Two rows
#  legitimately say "outside the repo (ops)" for work that has no commit at all, so demanding
#  hashes would be wrong -- what must be caught is the PLACEHOLDER: a value written to be
#  replaced later, which nobody replaced.
#
#  MEASURED 2026-08-20: two CLOSED rows carried the literal string "PENDING" and section K
#  accepted them, because check_witness.py skips only an EMPTY commits field.  A field nothing
#  validates is a field that drifts, and this one drifted the same day it was written.
PLACEHOLDER = re.compile(r"^(pending|tbd|todo|xxx|\?+|-+)$", re.I)
NONREPO = re.compile(r"outside the repo|\bops\b|no commit", re.I)


def bad_commits(rows):
    """Rows whose `commits` is a placeholder rather than hashes or a stated non-repo note."""
    out = []
    for rid, row in sorted(rows.items()):
        c = (row.get("commits") or "").strip()
        if not c or NONREPO.search(c):
            continue
        for tok in c.split():
            if PLACEHOLDER.match(tok) or not re.fullmatch(r"[0-9a-f]{7,40}", tok):
                out.append((rid, row.get("state", "?"), c))
                break
    return out


def main(argv):
    listing = "--list" in argv
    ledger = json.load(io.open(LEDGER, encoding="utf-8"))
    rows = {r["id"]: r for r in ledger["rows"]}

    short = sorted(i for i in rows if len(i) < MIN_ID)
    matchable = {i: r for i, r in rows.items() if len(i) >= MIN_ID}
    #  A stopword id must appear as an IDENTIFIER (backticked or quoted); every other
    #  id keeps the word-boundary form.  See SUBJECT_STOPWORDS above for the measured
    #  false positive that motivated this.
    pats = {i: re.compile(
                (r"[`\"']%s[`\"']" % re.escape(i)) if i in SUBJECT_STOPWORDS
                else (r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(i)))
            for i in matchable}

    #  %H to MATCH (names() and lists() above) and to LOOK UP (records_only()); %h to PRINT.  The
    #  lookup took %h until 2026-09-24, and this comment called that "a lookup, never a
    #  comparison" -- but `git show <abbrev>` resolves a same-named REF first: a tag `030e961`
    #  misgraded a records commit as code (measured by the Opus seat in a scratch clone).
    log = [l.split("\t", 2) for l in
           git("log", "--format=%H\t%h\t%s", "-%d" % DEPTH).splitlines() if l.count("\t") >= 2]

    hard, soft, ok = [], [], 0
    for full, h, subj in log:
        for rid, pat in pats.items():
            if not pat.search(subj):
                continue
            row = matchable[rid]
            commits = (row.get("commits") or "").split()
            state = row.get("state", "")
            #  *** THE CLOSURE CONTRADICTION IS TESTED FIRST, AND THE ORDER IS LOAD-BEARING.
            #  ***  It sat below the `h in commits` early-out until a negative control caught
            #  it: a row can NAME the commit and still contradict it -- state "in work" under
            #  a commit whose subject says CLOSED -- and the early-out scored that as
            #  attributed.  The injected break went undetected and the run stayed green.
            #  Being listed is not the same as agreeing.
            if CLOSURE.search(subj) and state != "closed":
                #  *** A THIRD CASE, MEASURED 2026-09-05: BOTH WERE RIGHT AT THEIR TIMES. ***  b78bb0f
                #  closed `pcc2widthkills`; its own pass 2 reopened it the same day and thirteen
                #  detector passes followed with the fix unchanged.  The board must SAY SO: a row
                #  whose `reopened` field names the commit is a known reopening and is reported,
                #  not graded.  Any other closure/state contradiction stays HARD.  `reopened` may
                #  name several commits as 7-40 lowercase-hex tokens bounded by the field's edges or
                #  by characters outside ASCII [0-9A-Za-z]; the contradiction is HARD when none of
                #  them prefixes the scanned commit (wording from the codex seat, 2026-09-24).
                if names(row.get("reopened"), full):
                    print("  REOPENED %s %-14s %-8s row names this commit as the closure its later passes superseded" % (h, rid, state))
                    ok += 1
                else:
                    hard.append((h, rid, state, "commit says CLOSED; row is %r" % state, subj))
            elif lists(row.get("commits"), full):
                ok += 1
            elif records_only(full):
                #  Writing ABOUT a row is not authoring it.  Silent for a closed row (the
                #  research records of a finished round are not drift); soft for an open one,
                #  where it is still useful to see the row is being worked.
                if state != "closed":
                    soft.append((h, rid, state, "records-only commit (.md/.txt)", subj))
            elif state == "closed" and not commits:
                #  Documented-only closure: see the header.  Named, never graded.
                soft.append((h, rid, state,
                             "closed documented-only (empty commits) -- read the closure note",
                             subj))
            elif state == "closed":
                hard.append((h, rid, state, "closed row does not name this code commit", subj))
            elif not commits:
                #  *** HARD, NOT SOFT -- AND THIS BRANCH USED TO BE SOFT, WHICH IS HOW THE
                #  CHECK MISSED ITS OWN MOTIVATING CASE. ***  A ninth-seat review measured
                #  optrow, smdatefmt and constblind all sitting here at once, every one of
                #  them genuinely shipped, and this tool reported ATTRIBUTION_PASS over the
                #  top of them.  That is the newest vacuity class -- blindness reported as a
                #  green line -- inside the check written against exactly that class.  It is
                #  also the mechanism that produced a 5-0 mis-vote: five seats read a stale
                #  sentence in a row whose record had not caught up with its code.
                #
                #  It is safe to be hard because `commits` is NOT closure-only: twelve OPEN
                #  rows carry it.  So an open row with a CODE commit naming it and an EMPTY
                #  field has no legitimate reading -- it is drift, whatever the state says.
                #  (Records-only and documented-only commits are already filtered above, so
                #  this fires on shipped CODE alone.)
                hard.append((h, rid, state,
                             "work shipped and the row does not name it (commits EMPTY)",
                             subj))
            else:
                soft.append((h, rid, state,
                             "open row, commits=%s" % " ".join(commits), subj))

    for label, items in (("HARD", hard), ("SOFT", soft)):
        for h, rid, state, why, subj in items:
            print("  %-6s %-9s %-14s %-8s %s" % (label, h, rid, state, why))
            if listing:
                print("         %s" % subj[:88])
    print()
    print("  scanned %d commits deep; %d subject/row matches already attributed" % (len(log), ok))
    #  ALWAYS printed, pass or fail -- the blindness is part of the result, not a footnote.
    print("  NOT MATCHABLE (id shorter than %d chars, would match English): %d -- %s"
          % (MIN_ID, len(short), " ".join(short) if short else "none"))
    print("  Rows with these ids are INVISIBLE to this check. Lengthen the id to cover one.")
    #  ALWAYS printed too -- same doctrine as the line above.
    _sw = sorted(i for i in matchable if i in SUBJECT_STOPWORDS)
    print("  STOPWORD IDS (ordinary project vocabulary; matched only when written as\n        an identifier, e.g. backticked): %d -- %s"
          % (len(_sw), " ".join(_sw) if _sw else "none"))

    #  The second blindness -- see the header.  A row that SHIPPED but that no commit subject
    #  ever names is never examined, so its attribution could be wrong indefinitely.  Only
    #  rows with commits are worth listing: an open row nobody has committed against yet is
    #  simply not started.
    subjects = " \n".join(sub for _full, _h, sub in log)
    unnamed = sorted(rid for rid, row in matchable.items()
                     if (row.get("commits") or "").strip() and not pats[rid].search(subjects))
    print("  NEVER NAMED in any scanned subject, yet carry commits: %d -- %s"
          % (len(unnamed), " ".join(unnamed) if unnamed else "none"))
    print("  Those rows shipped work this check cannot see. It reads SUBJECTS, not diffs.")

    ph = bad_commits(rows)
    if ph:
        print()
        for rid, st, c in ph:
            print("  HARD   %-9s %-14s %-8s commits is not a hash: %r"
                  % ("--", rid, st, c))
        print("  A `commits` value that is neither hashes nor a stated non-repo note is a")
        print("  PLACEHOLDER nobody came back to.  Section K accepts it -- it skips only an")
        print("  EMPTY field -- so this is the only check that sees it.")

    if hard or ph:
        print()
        print("ATTRIBUTION_FAIL  %d hard, %d soft, %d placeholder"
              % (len(hard), len(soft), len(ph)))
        return 1
    print("ATTRIBUTION_PASS  0 hard, %d soft" % len(soft))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
