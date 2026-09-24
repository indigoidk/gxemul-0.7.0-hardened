REVIEW BRIEF -- a 22-line fix to a commit-attribution checker in this project's pre-commit gate.  Please do not simply
ratify: check the premises, and try to break the fix.  Answer with a VERDICT line first
(VERDICT: SHIP / SHIP WITH NOTES / DO NOT SHIP), then numbered findings.  The tree under review is
C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\ (a git repo); ignore any other copy.  Read-only: do not write anywhere.

THE CHECKER.  GXEMUL-SEC/tools/pipeline/check_commit_attribution.py (precommit section L) reads the last 60 commit
subjects, finds ledger row ids in them (tools/pipeline/ledger.json, rows[].id), and grades each subject/row match: a
CLOSED row must name the commit in its `commits` field (a whitespace-separated list of hex shas, validated elsewhere
as 7-40 lowercase hex tokens, or a "no commit"/"outside the repo"/"ops" note); a subject saying "closed" against a
non-closed row is HARD unless the row's free-text `reopened` field names that commit.

THE DEFECT (measured).  It compared git's `%h` abbreviation with the ledger's shas by exact membership
(`h in commits`) and substring (`h in reopened`).  The ledger's shas are the 7-character form git printed when each
row closed.  After the repository grew, git's automatic abbreviation became 8 characters, so six correctly
attributed rows hard-failed and the gate went red for every commit.  The mirror case also failed: a row written with
an 8-character sha did not match a 7-character %h.

THE FIX (the whole diff):
diff --git a/tools/pipeline/check_commit_attribution.py b/tools/pipeline/check_commit_attribution.py
index b73e598f..7d71afca 100644
--- a/tools/pipeline/check_commit_attribution.py
+++ b/tools/pipeline/check_commit_attribution.py
@@ -140,6 +140,21 @@ SUBJECT_STOPWORDS = {"carrier", "census"}   #  "census" added 2026-09-07: same m
 #  ordinary round into a hard failure.
 CLOSURE = re.compile(r"\b(closed|closes|closing)\b", re.I)
 
+#  *** A LEDGER SHA NAMES A COMMIT WHEN IT IS A PREFIX OF THE FULL HASH -- AND THE FIRST FORM
+#  COMPARED ABBREVIATIONS, WHICH GIT LENGTHENS AS THE REPOSITORY GROWS. ***  Measured
+#  2026-09-24: the rows carry the 7-character form git printed when each closed; after 4264ee20
+#  git's own %h became 8 characters, `h in commits` stopped matching, and six correctly
+#  attributed rows hard-failed at HEAD -- a red gate on every commit, raised by nothing in the
+#  ledger.  The mirror case failed too: a row written at 8 characters did not match a
+#  7-character %h.  Section F's receipt check met this on its first version and matches by
+#  prefix; so does this, on %H.  (regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/)
+SHA = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])")
+
+
+def names(field, full):
+    """True when some 7-40 character hex token in `field` is a prefix of the full hash."""
+    return any(full.startswith(t) for t in SHA.findall(field or ""))
+
 
 def git(*args):
     return subprocess.run(["git", "-C", SEC] + list(args),
@@ -224,11 +239,12 @@ def main(argv):
                 else (r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(i)))
             for i in matchable}
 
-    log = [l.split("\t", 1) for l in
-           git("log", "--format=%h\t%s", "-%d" % DEPTH).splitlines() if "\t" in l]
+    #  %H to MATCH (see names() above), %h to PRINT.
+    log = [l.split("\t", 2) for l in
+           git("log", "--format=%H\t%h\t%s", "-%d" % DEPTH).splitlines() if l.count("\t") >= 2]
 
     hard, soft, ok = [], [], 0
-    for h, subj in log:
+    for full, h, subj in log:
         for rid, pat in pats.items():
             if not pat.search(subj):
                 continue
@@ -247,12 +263,12 @@ def main(argv):
                 #  detector passes followed with the fix unchanged.  The board must SAY SO: a row
                 #  whose `reopened` field names the commit is a known reopening and is reported,
                 #  not graded.  Any other closure/state contradiction stays HARD.
-                if h in (row.get("reopened") or ""):
+                if names(row.get("reopened"), full):
                     print("  REOPENED %s %-14s %-8s row names this commit as the closure its later passes superseded" % (h, rid, state))
                     ok += 1
                 else:
                     hard.append((h, rid, state, "commit says CLOSED; row is %r" % state, subj))
-            elif h in commits:
+            elif names(row.get("commits"), full):
                 ok += 1
             elif records_only(h):
                 #  Writing ABOUT a row is not authoring it.  Silent for a closed row (the
@@ -309,7 +325,7 @@ def main(argv):
     #  ever names is never examined, so its attribution could be wrong indefinitely.  Only
     #  rows with commits are worth listing: an open row nobody has committed against yet is
     #  simply not started.
-    subjects = " \n".join(sub for _h, sub in log)
+    subjects = " \n".join(sub for _full, _h, sub in log)
     unnamed = sorted(rid for rid, row in matchable.items()
                      if (row.get("commits") or "").strip() and not pats[rid].search(subjects))
     print("  NEVER NAMED in any scanned subject, yet carry commits: %d -- %s"

CONTROLS RUN (regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/: PREDICTIONS.txt sealed before any run,
PREDICTIONS_addendum.txt sealed after the pre-fix run and before the edit, RESULT.txt, pre_P*.out, post_Q*.out):
  pre-fix at git's default 8-char abbreviation: 6 HARD (all "closed row does not name this code commit")
  pre-fix at core.abbrev=7: 1 HARD (the mirror case: ledger holds 4264ee20, %h is 4264ee2)
  pre-fix at depth 130: 11 HARD incl. b78bb0f6 whose row's `reopened` text names b78bb0f
  post-fix: 0 HARD at both abbreviations, output identical modulo hash width; REOPENED line for b78bb0f6 at depth 130
  negative controls post-fix: a closed row's commits replaced by a different real sha -> HARD; by cdbe7d76 (shares 7
  chars with cdbe7d75..., not a prefix) -> HARD; by the full 40-char hash -> no HARD.  The ledger being committed -> 0 HARD.
  Also measured: at 8 chars the pre-fix check reported 14 extra SOFT "open row, commits=..." lines -- fake drift.

QUESTIONS
1. Is "a 7-40 char hex token in the field is a PREFIX of the full hash" the right test for BOTH fields -- `commits`
   (a sha list) and `reopened` (free text that starts with a sha)?  Name any input that gives a false HARD or a false
   pass under it that the old exact test did not (uppercase hex? a sha glued to punctuation or to letters? a hex-only
   English word of 7+ letters in `reopened`, e.g. "effaced", that happens to prefix a scanned commit?).
2. Is the abbreviated hash compared anywhere else on this code path (this file, or section L of
   GXEMUL-SEC/tools/precommit_check.sh) that the fix missed?
3. The smallest edit to the FIXED code that still passes every control above but reintroduces a false HARD or a false
   pass.  Which control would have to be added to catch it?
4. Could any of the controls above not have failed?
