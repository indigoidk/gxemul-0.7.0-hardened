# PASS ON R' -- the #547 follow-up repair to `#546`'s attribution rider (the repair chain's own pass)

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree under review is `GXEMUL-SEC/`.  2026-09-24.  The adjudication pass
(SF2) on #547 found that R -- the prefix-matching fix committed in 3e33201d -- introduced one regression and left two
fail-open paths.  R' repairs them.  **A repair made in response to a pass owes its own pass, and this is it**: the chain
closes on the first valid pass that finds no breach.  Review EFFORT is scoped to R'; the FLOOR question -- does any edit
still get past every control -- is asked of the whole checker as it now stands.

**FIRST LINE, exactly:** `VERDICT: R'=<SHIP | SHIP WITH NOTES | DO NOT SHIP>; RECORDS=<SHIP | SHIP WITH NOTES | DO NOT SHIP>`
then numbered findings.  Please do not simply ratify; check the premises.  If you cannot read files that is expected --
what a question needs is inlined.  Seats that read files: stay within `GXEMUL-SEC/tools/pipeline/check_commit_attribution.py`
(the WORKING copy is R'), `GXEMUL-SEC/tools/precommit_check.sh` and `GXEMUL-SEC/CHANGELOG.md`; please do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

## 1. WHAT R' CHANGES

1. **`commits` is a hash LIST again.**  R extracted 7-40 hex tokens from anywhere in the field.  But `bad_commits()`
   accepts a non-repository NOTE there ("outside the repo (ops) ..."), so a note that merely MENTIONED a sha --
   `outside the repo (ops); compared against (cdbe7d75)` -- credited that commit as authorship, where the whole-token test
   before R graded HARD (codex, measured with the real `main()`).  R' reads `commits` with `lists()`: a token names a commit
   only when the WHOLE whitespace token is 7-40 lowercase hex and prefixes `%H`.  `names()` stays, for `reopened` only.
2. **`git()` fails closed.**  It dropped git's exit status, so `GIT_DIR=/nonexistent` gave `scanned 0 commits deep ...
   ATTRIBUTION_PASS` (codex, grok, Opus).  R' prints a HARD-shaped line naming git's error and exits 2.  Section L prints
   only `^  HARD` lines on failure, which is why the line has that shape.
3. **`records_only()` takes `%H`.**  `git show <abbrev>` resolves a same-named REF before the object, so a tag named like a
   commit's abbreviation made a records commit read as code (Opus, in a scratch clone).
4. Comment corrections -- every wrong sentence the review found in this file (the repack time and cause, six HARD lines
   on five rows, the mirror case's scope, section F's floor, the pipeline-code exemption's real counts, the lookup, the
   docstring's SOFT/HARD, and codex's wording for what `reopened` may hold).

**The diff against HEAD (3e33201d), whole** (numstat: this one file):

```
diff --git a/tools/pipeline/check_commit_attribution.py b/tools/pipeline/check_commit_attribution.py
index 90296a9e..8ccc0e40 100644
--- a/tools/pipeline/check_commit_attribution.py
+++ b/tools/pipeline/check_commit_attribution.py
@@ -33,9 +33,11 @@ WHAT IT CHECKS, and the three grades are deliberately different failures:
          A closed row that does not name what closed it cannot be attributed -- the same
          defect `nightly_check.sh` fixes for the battery verdict.
 
-  SOFT   a commit subject names an OPEN row and R.commits is empty.  Progress commits on an
-         open row are ordinary and this is NOT a failure; it is listed so the drift stays
-         visible rather than accumulating silently.
+  SOFT   a commit subject names an OPEN row and the commit is RECORDS-ONLY.  Progress commits
+         on an open row are ordinary and this is NOT a failure; it is listed so the drift stays
+         visible rather than accumulating silently.  (A commit that shipped CODE against an
+         open row with an EMPTY `commits` is HARD -- main() says why.  This paragraph said SOFT
+         for that case too until the 2026-09-24 review.)
 
   SOFT   a commit subject names a CLOSED row whose `commits` is EMPTY.  That is a
          DOCUMENTED-ONLY closure -- a duplicate credited elsewhere, or a row closed with no
@@ -141,24 +143,56 @@ SUBJECT_STOPWORDS = {"carrier", "census"}   #  "census" added 2026-09-07: same m
 CLOSURE = re.compile(r"\b(closed|closes|closing)\b", re.I)
 
 #  *** A LEDGER SHA NAMES A COMMIT WHEN IT IS A PREFIX OF THE FULL HASH -- AND THE FIRST FORM
-#  COMPARED ABBREVIATIONS, WHICH GIT LENGTHENS AS THE REPOSITORY GROWS. ***  Measured
-#  2026-09-24: the rows carry the 7-character form git printed when each closed; after 4264ee20
-#  git's own %h became 8 characters, `h in commits` stopped matching, and six correctly
-#  attributed rows hard-failed at HEAD -- a red gate on every commit, raised by nothing in the
-#  ledger.  The mirror case failed too: a row written at 8 characters did not match a
-#  7-character %h.  Section F's receipt check met this on its first version and matches by
-#  prefix; so does this, on %H.  (regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/)
+#  COMPARED ABBREVIATIONS, WHICH GIT LENGTHENS AS ITS PACKED-OBJECT COUNT GROWS. ***  Measured
+#  2026-09-24: the rows carry the 7-character form git printed when each closed; a `git gc` at
+#  about 2026-09-23 23:54 (pack-366ba631 created 23:54:45, packed-refs rewritten 23:54:32; 24,350
+#  objects packed) made git's own %h 8 characters -- the automatic length follows git's
+#  approximate packed-object count, not any commit -- so `h in commits` stopped matching, and
+#  six HARD lines on five correctly attributed rows (stagetokens twice) failed at HEAD -- a red
+#  gate on every commit, raised by nothing in the ledger.  The mirror case failed too, in the
+#  `commits` check, which compared WHOLE TOKENS: a row written at 8 characters did not match a
+#  7-character %h.  Section F's receipt check matches by prefix for a related reason (its first
+#  version compared a short receipt with a full hash exactly and never matched); so does this,
+#  on %H -- keeping the ledger's own 7-40 floor, which section F does not have.
+#  (regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/; this block said "after
+#  4264ee20" and "six ... rows" until the nine-seat review of 2026-09-24 corrected both.)
 SHA = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])")
 
 
 def names(field, full):
-    """True when some 7-40 character hex token in `field` is a prefix of the full hash."""
+    """True when some 7-40 character hex token in a FREE-TEXT field is a prefix of the full hash.
+
+    For `reopened` only.  `commits` is a LIST and is read by lists() below."""
     return any(full.startswith(t) for t in SHA.findall(field or ""))
 
 
+#  *** `commits` IS A WHITESPACE-SEPARATED HASH LIST, AND THE PREFIX FIX FIRST READ IT AS PROSE. ***
+#  Measured 2026-09-24 by the codex seat's adjudication pass: bad_commits() accepts a
+#  non-repository NOTE in this field ("outside the repo (ops) ..."), and names() extracts a hex
+#  token from anywhere -- so a note that merely MENTIONS a sha, "(cdbe7d75)", credited that
+#  commit as authorship where the whole-token test before it graded HARD.  A `commits` token
+#  names a commit only when the WHOLE token is 7-40 lowercase hex and prefixes the full hash.
+TOKEN = re.compile(r"[0-9a-f]{7,40}")
+
+
+def lists(field, full):
+    """True when a whole whitespace token of a `commits` list is a 7-40 hex prefix of the full hash."""
+    return any(TOKEN.fullmatch(t) and full.startswith(t) for t in (field or "").split())
+
+
 def git(*args):
-    return subprocess.run(["git", "-C", SEC] + list(args),
-                          capture_output=True, text=True).stdout
+    r = subprocess.run(["git", "-C", SEC] + list(args), capture_output=True, text=True)
+    #  *** FAIL CLOSED.  This returned stdout and dropped the status, so a git that could not
+    #  read the repository gave an empty log and "scanned 0 commits deep ... ATTRIBUTION_PASS"
+    #  -- a gate passing on nothing (measured 2026-09-24 with GIT_DIR=/nonexistent by three
+    #  seats).  The first line is shaped like a HARD row because section L prints only those.
+    if r.returncode != 0:
+        print("  HARD   --        (git)          --       git %s exited %d: %s"
+              % (args[0], r.returncode, " ".join(r.stderr.split())[:160]))
+        print()
+        print("ATTRIBUTION_FAIL  git could not read the repository")
+        sys.exit(2)
+    return r.stdout
 
 
 def records_only(h):
@@ -175,7 +209,16 @@ def records_only(h):
     #
     #  tools/pipeline/ is the ledger, the queue, the dashboard renderings and the checkers'
     #  own manifests: writing there is recording, never shipping.  Anything OUTSIDE it that
-    #  is not .md/.txt is still authorship, so a fix that edits a checker's LOGIC still counts.
+    #  is not .md/.txt is still authorship.
+    #
+    #  *** THIS COMMENT ALSO SAID "so a fix that edits a checker's LOGIC still counts", AND
+    #  FOR THE CHECKERS THAT LIVE HERE IT IS FALSE. ***  tools/pipeline/ holds the checkers'
+    #  own sources, .py and .sh, so a commit editing ONLY a checker's logic here is graded as a
+    #  record: measured 2026-09-24 on bbfc942e, which changed this file's SUBJECT_STOPWORDS.
+    #  At 3e33201d, 28 of the 60 scanned commits touch pipeline code and 3 of those are graded
+    #  records-only BECAUSE of this exemption; dropping it for .py/.sh changes no verdict at
+    #  depth 60 and gives 8 HARD at full depth -- attribution drift it has been hiding.  FILED
+    #  (attrcheckgaps), not changed here: it changes grading and owes its own controls.
     #
     #  *** AND regress/artifacts/ IS A RECORD TOO -- WIDENED 2026-08-31, THE SECOND TIME THIS
     #  PREDICATE HAS BEEN TOO NARROW FOR THE SAME REASON. ***  It fired HARD on 3d30a20, a
@@ -239,8 +282,10 @@ def main(argv):
                 else (r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(i)))
             for i in matchable}
 
-    #  %H to MATCH (see names() above); %h to print, and for records_only()'s own `git show`, where
-    #  git resolves the abbreviation it has just printed -- a lookup, never a comparison.
+    #  %H to MATCH (names() and lists() above) and to LOOK UP (records_only()); %h to PRINT.  The
+    #  lookup took %h until 2026-09-24, and this comment called that "a lookup, never a
+    #  comparison" -- but `git show <abbrev>` resolves a same-named REF first: a tag `030e961`
+    #  misgraded a records commit as code (measured by the Opus seat in a scratch clone).
     log = [l.split("\t", 2) for l in
            git("log", "--format=%H\t%h\t%s", "-%d" % DEPTH).splitlines() if l.count("\t") >= 2]
 
@@ -263,15 +308,18 @@ def main(argv):
                 #  closed `pcc2widthkills`; its own pass 2 reopened it the same day and thirteen
                 #  detector passes followed with the fix unchanged.  The board must SAY SO: a row
                 #  whose `reopened` field names the commit is a known reopening and is reported,
-                #  not graded.  Any other closure/state contradiction stays HARD.
+                #  not graded.  Any other closure/state contradiction stays HARD.  `reopened` may
+                #  name several commits as 7-40 lowercase-hex tokens bounded by the field's edges or
+                #  by characters outside ASCII [0-9A-Za-z]; the contradiction is HARD when none of
+                #  them prefixes the scanned commit (wording from the codex seat, 2026-09-24).
                 if names(row.get("reopened"), full):
                     print("  REOPENED %s %-14s %-8s row names this commit as the closure its later passes superseded" % (h, rid, state))
                     ok += 1
                 else:
                     hard.append((h, rid, state, "commit says CLOSED; row is %r" % state, subj))
-            elif names(row.get("commits"), full):
+            elif lists(row.get("commits"), full):
                 ok += 1
-            elif records_only(h):
+            elif records_only(full):
                 #  Writing ABOUT a row is not authoring it.  Silent for a closed row (the
                 #  research records of a finished round are not drift); soft for an open one,
                 #  where it is still useful to see the row is being worked.
```

**The enclosing function, whole, as R' leaves it** (every binding the diff's call sites use):

```
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
```

## 2. MEASURED (predictions sealed before every run; durable at `regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/`)

* **Success path unchanged:** on 19 earlier control inputs -- depth 60 / 130 / 800, abbreviations 7 / 8 / 12 / 40, a
  different real sha, a 7-agreeing non-prefix, the full hash, a 6-character `reopened`, a substring token, two tokens,
  states `in work` / `held` / `open`, a full-hash `reopened`, and two non-repo notes -- R' output is BYTE-IDENTICAL to
  HEAD's, and R' on Q0 equals the golden Q0.
* **Q19a**, `commits` = `outside the repo (ops); compared against (cdbe7d75)`: HEAD PASS (the regression); R' HARD fbsmlane.
  Q19b (the note names `4264ee20`): HARD in both.  Q19c (`cdbe7d7 outside the repo (ops)`, a whole token in a note, which the
  pre-R whole-token test also credited): PASS in both.
* **Q20**, `GIT_DIR=/nonexistent`: HEAD exit 0, `scanned 0 commits deep`, PASS; R' exit 2, `HARD -- (git) -- git log
  exited 128: fatal: not a git repository ...`, FAIL.
* **Q21b**, in a `--shared` scratch clone: tag `7a361f47` (the abbreviation of records commit 7a361f47, which names open row
  `m88kexcdetectorl2`, whose `commits` is empty) pointed at code commit fd150657.  Without the tag HEAD and R' both grade
  it SOFT "records-only".  With it, HEAD grades HARD "work shipped and the row does not name it"; R' stays SOFT.
* Every figure is asserted by a verifier (29/29), whose negative control reds its three injected breaks.

## 3. THE RECORDS, CORRECTED IN PLACE -- `CHANGELOG.md` (#546's block), the whole working diff:

```
diff --git a/CHANGELOG.md b/CHANGELOG.md
index b30b51b0..0a16184f 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -94 +94 @@ ABBREVIATIONS, and git lengthened them.**  The first attempt at this commit was
-rows the ledger attributes correctly.  `tools/pipeline/check_commit_attribution.py` tested `h in commits` (exact)
+lines on five rows the ledger attributes correctly (stagetokens twice).  `tools/pipeline/check_commit_attribution.py` tested `h in commits` (exact)
@@ -96 +96,2 @@ and `h in reopened` (substring) against git's `%h`; the rows carry the 7-charact
-and after #545 (4264ee20) git's automatic abbreviation became 8 characters -- so the gate was red at HEAD for EVERY
+and a `git gc` at about 2026-09-23 23:54, after #545 (4264ee20), made git's automatic abbreviation 8 characters (the
+length follows git's approximate packed-object count, not any commit) -- so the gate was red at HEAD for EVERY
@@ -100 +101 @@ before the edit).  Fixed the way section F's receipt check already was: a 7-40 c
-when it is a PREFIX of `%H`; `%h` is only printed.  Controls, predictions first: pre-fix 6 HARD at 8 characters and 1
+when it is a PREFIX of `%H`; `%h` is printed, and passed only to `records_only()`'s own `git show` lookup.  Controls, predictions first: pre-fix 6 HARD at 8 characters and 1
@@ -104 +105,3 @@ and the full 40-character hash -- as predicted (`regress/artifacts/hygienecensus
-The same defect had reported 14 lines of fake SOFT drift.
+The same defect had reported 14 lines of fake SOFT drift.  *(Corrected in place 2026-09-24 by `#547`, from the rider's
+nine-seat review: this paragraph said six HARD "rows" -- six lines on five rows; it dated the abbreviation change to
+#545 itself -- a repack made it; and it said `%h` is "only printed" -- `records_only()` also passes it to `git show`.)*
```

and three ledger text fields that held two U+0008 characters each where `\b` was meant (lcaisalane.reopened since
3c41f011, fbsmlane.state_note since 18ea5646, citestale.state_note): each now reads a literal backslash-b; no other byte
of the ledger changed, and the checker's output is identical before and after (neither field is read by it).

## 4. TO BE FILED WITH #547 (the checker's remaining gaps, and the others the review found)

* `attrcheckgaps` (MED): the `tools/pipeline/` exemption hides checker-code commits (8 HARD at full depth when dropped);
  no tripwire for an ambiguous ledger token (prefix matching fails silent where the old exact test failed loud); section L
  grades the WORKTREE ledger, not the one the commit records; `reopened` has no validation; `rows: []` and duplicate ids
  pass; a closure word in a subject applies to every row it names; merge commits read as code.
* `deletecheckhead` (MED): the precommit tripwire for upstream's `delete ` check must read the INDEX; gate 8's own domain.
* `batterymissedruns` (MED): no verdict for 2026-09-06 and 09-13, and nothing runs the dead-man switch.
* `svbackspace` (MED): `tools/pipeline/seat_verdicts.py`'s wall patterns hold U+0008 where `\b` was meant (since 1cec2daf), so
  `{"error": ...}` and `Error code: 429` are not recognised as walls; the fix needs a decision about bare numbers.
* `carrierstalecopies` (LOW): the carrier and brief template still place the pristine copies under the project root
  (moved 2026-09-13); MOVED.txt carries a literal CR/BEL; a directory named `GXEMUL-SEC` + CR sits at the root; the
  carrier holds the same U+0008 defect.

## 5. QUESTIONS

1. **Is `lists()` exactly the pre-R grammar where it should be, and nothing more?**  Name any `commits` value on which R'
   and the pre-R whole-token test differ other than by R's intended width-independence.
2. **Does `git()` now fail closed WITHOUT failing anything legitimate?**  Name a normal invocation that exits nonzero.
3. **Does any single edit to R' keep every control above green yet change a verdict on this repository's current ledger
   or history?**  Say whether one exists; name it if you can.
4. **Is every corrected sentence (the comment block, the docstring, the CHANGELOG) now TRUE?**  Four of my earlier
   corrections carried new errors, found by the last pass.  Assume these do too, and look.

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
