# ADJUDICATION PASS (SF2) -- `#547` upstreamdeleteprose (U) and `#546`'s attribution rider (R): the whole panel's findings, shared

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree under review is `GXEMUL-SEC/`.  2026-09-24.  **This is the THIRD
pass on this packet, not another review.**  Pass 2 went to nine seats (codex, agy, grok, the kimi seat through
kimi-k3:cloud -- its CLI was on its weekly limit --, glm, deepseek, minimax, the Opus measuring seat, and a dedicated
second codex job).  Every finding they made is consolidated below with MY disposition.  Your job is to adjudicate it --
including where I sided with you, which is the ruling you are least likely to test.

**FIRST LINE, exactly:** `VERDICT: U=<SHIP | SHIP WITH NOTES | DO NOT SHIP>; R=<SHIP | SHIP WITH NOTES | DO NOT SHIP>`
then answer the three questions at the end.  Please do not simply ratify.  If you cannot read files that is expected:
everything a question depends on is inlined.  Seats that read files: stay within `GXEMUL-SEC/src/`, `GXEMUL-SEC/test/`,
`GXEMUL-SEC/regress/gate_upstream.sh` and `GXEMUL-SEC/tools/pipeline/check_commit_attribution.py`; please do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json` -- what they hold is inlined.

## 1. THE MATERIAL

**U** -- uncommitted, a one-word comment change (numstat `1 1 src/devices/dev_sgi_re.c`; HEAD 3e33201d):

```
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 8e9727d5..2eff3075 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -507,7 +507,7 @@ DEVICE_ACCESS(sgi_re)
 			 *  #513: ACCEPT.  A guest read of a len == 8 TLB slot ended
 			 *  the host.  The write arm directly above already computes
 			 *  and stores the value, so the disposition is member 4 of
-			 *  the option set -- delete the kill and RETURN THE VALUE --
+			 *  the option set -- remove the kill and RETURN THE VALUE --
 			 *  rather than a decline: nothing is unimplemented here.
 			 *  This loop is the exact inverse of the write loop, cell for
 			 *  cell and shift for shift.
```

Measured before pass 2: upstream's `test/check_delete_calls.sh` exits 1 on a `git archive` export of HEAD
(`Error: src/devices/dev_sgi_re.c is not in check_delete_calls.exceptions!`) and 0 with U applied; the two
`dev_sgi_re.c` versions preprocess to byte-identical text and compile to byte-identical objects.

**R** -- committed in 3e33201d; `tools/pipeline/check_commit_attribution.py` (precommit section L) matched ledger shas
against git's `%h` by exact comparison and now matches a 7-40 hex token as a PREFIX of `%H`:

```
diff --git a/tools/pipeline/check_commit_attribution.py b/tools/pipeline/check_commit_attribution.py
index b73e598f..90296a9e 100644
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
@@ -224,11 +239,13 @@ def main(argv):
                 else (r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(i)))
             for i in matchable}
 
-    log = [l.split("\t", 1) for l in
-           git("log", "--format=%h\t%s", "-%d" % DEPTH).splitlines() if "\t" in l]
+    #  %H to MATCH (see names() above); %h to print, and for records_only()'s own `git show`, where
+    #  git resolves the abbreviation it has just printed -- a lookup, never a comparison.
+    log = [l.split("\t", 2) for l in
+           git("log", "--format=%H\t%h\t%s", "-%d" % DEPTH).splitlines() if l.count("\t") >= 2]
 
     hard, soft, ok = [], [], 0
-    for h, subj in log:
+    for full, h, subj in log:
         for rid, pat in pats.items():
             if not pat.search(subj):
                 continue
@@ -247,12 +264,12 @@ def main(argv):
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
@@ -309,7 +326,7 @@ def main(argv):
     #  ever names is never examined, so its attribution could be wrong indefinitely.  Only
     #  rows with commits are worth listing: an open row nobody has committed against yet is
     #  simply not started.
-    subjects = " \n".join(sub for _h, sub in log)
+    subjects = " \n".join(sub for _full, _h, sub in log)
     unnamed = sorted(rid for rid, row in matchable.items()
                      if (row.get("commits") or "").strip() and not pats[rid].search(subjects))
     print("  NEVER NAMED in any scanned subject, yet carry commits: %d -- %s"
```

**R-CORRECTIONS** -- uncommitted, proposed for `#547`: comment-only corrections to that file, arising from this review
(the checker's output is byte-identical after them and its Python AST is unchanged):

```
diff --git a/tools/pipeline/check_commit_attribution.py b/tools/pipeline/check_commit_attribution.py
index 90296a9e..49e9639d 100644
--- a/tools/pipeline/check_commit_attribution.py
+++ b/tools/pipeline/check_commit_attribution.py
@@ -142,11 +142,14 @@ CLOSURE = re.compile(r"\b(closed|closes|closing)\b", re.I)
 
 #  *** A LEDGER SHA NAMES A COMMIT WHEN IT IS A PREFIX OF THE FULL HASH -- AND THE FIRST FORM
-#  COMPARED ABBREVIATIONS, WHICH GIT LENGTHENS AS THE REPOSITORY GROWS. ***  Measured
-#  2026-09-24: the rows carry the 7-character form git printed when each closed; after 4264ee20
-#  git's own %h became 8 characters, `h in commits` stopped matching, and six correctly
-#  attributed rows hard-failed at HEAD -- a red gate on every commit, raised by nothing in the
-#  ledger.  The mirror case failed too: a row written at 8 characters did not match a
-#  7-character %h.  Section F's receipt check met this on its first version and matches by
-#  prefix; so does this, on %H.  (regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/)
+#  COMPARED ABBREVIATIONS, WHICH GIT LENGTHENS AS ITS OBJECT COUNT GROWS. ***  Measured
+#  2026-09-24: the rows carry the 7-character form git printed when each closed; a repack at
+#  2026-09-23 23:57 (24,350 packed objects) made git's own %h 8 characters -- the automatic
+#  length follows the object count, not any commit -- so `h in commits` stopped matching, and
+#  six HARD lines on five correctly attributed rows (stagetokens twice) failed at HEAD -- a red
+#  gate on every commit, raised by nothing in the ledger.  The mirror case failed too: a row
+#  written at 8 characters did not match a 7-character %h.  Section F's receipt check met this
+#  on its first version and matches by prefix; so does this, on %H.
+#  (regress/artifacts/hygienecensus_20260923/attrabbrev_20260924/; this sentence said "after
+#  4264ee20" and "six ... rows" until the nine-seat review of 2026-09-24 corrected both.)
 SHA = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])")
 
@@ -176,5 +179,13 @@ def records_only(h):
     #  tools/pipeline/ is the ledger, the queue, the dashboard renderings and the checkers'
     #  own manifests: writing there is recording, never shipping.  Anything OUTSIDE it that
-    #  is not .md/.txt is still authorship, so a fix that edits a checker's LOGIC still counts.
+    #  is not .md/.txt is still authorship.
+    #
+    #  *** THIS COMMENT ALSO SAID "so a fix that edits a checker's LOGIC still counts", AND
+    #  FOR THE CHECKERS THAT LIVE HERE IT IS FALSE. ***  tools/pipeline/ holds check_*.py
+    #  themselves, so a commit editing ONLY a checker's logic here is graded as a record:
+    #  measured 2026-09-24 on bbfc942e, which changed this file's SUBJECT_STOPWORDS.  At
+    #  3e33201d, 3 of the 60 scanned commits edit pipeline code, and dropping the exemption for
+    #  .py/.sh changes no verdict today.  FILED (attrcheckgaps), not changed here: it changes
+    #  grading and owes its own controls.
     #
     #  *** AND regress/artifacts/ IS A RECORD TOO -- WIDENED 2026-08-31, THE SECOND TIME THIS
```

**NEW CONTROLS, all measured after pass 2** (predictions sealed before each run; each variant applied in memory from
the real path, so no tree file was edited; every figure asserted by a verifier whose own negative control reds its
injected breaks).  Q0 here is the committed code, working ledger, depth 60, at 3e33201d: `0 hard, 10 soft`.

| control | input | committed code | the construction it separates |
|---|---|---|---|
| Q10a / Q10b | abbreviation 12 / 40 | identical to Q0 modulo hash width | `elif len(h) <= 8 and names(...)` (codex): 8 HARD at 12 |
| Q11 | fbsmlane.commits = `dbe7d757` (a SUBSTRING of `cdbe7d75...`, not a prefix) | HARD fbsmlane | `t in full` (grok): PASS |
| Q0 itself | -- | 0 HARD | first-token-only `names()` (deepseek): HARD `09ded75c stagetokens`, whose commits field is `686d179 09ded75` -- the real ledger already carried the case |
| Q12 | fbsmlane.commits = `4264ee2 cdbe7d7` (target second) | PASS | first-token-only: HARD fbsmlane |
| Q13 | depth 800 (all 795 commits), abbreviation 7 vs 8 | 0 HARD, identical modulo width | `SHA.findall(...)[:2]` (Opus): 5 HARD; `SHA.findall((field or "")[:40])` (Opus): 2 HARD -- both byte-identical to Q0 at depth 60 |
| Q14 | `records_only()` without the `tools/pipeline/` exemption for .py/.sh | byte-identical to Q0 | measures that the exemption hides no verdict in today's window |
| Q15 | fbdeclinefive.state = "in work" (4264ee20's subject says "closed"; the row names it) | HARD "commit says CLOSED; row is 'in work'" | `names(row.get("reopened") or row.get("commits"), full)` (Opus): REOPENED, PASS; `SHA.findall(field or full)` (Opus): REOPENED, PASS |

## 2. FINDINGS AND MY DISPOSITIONS

**On U**

* **F1** [codex, grok, agy, glm, kimi, minimax, Opus] The exceptions test is `grep -q $a` with `$a` unquoted: an
  UNANCHORED BASIC REGEX of the flagged path against the list, not the literal substring match my brief said -- dots are
  wildcards.  `debugger.c` and `debugger_cmds.c` pass only through stale C++-era `.cc` entries; 8 of the 9 entries name
  files that do not exist.  **ACCEPTED**; the records say so.  Option (b) stays rejected: it would excuse the whole file,
  permanently, by the fork's first edit to upstream's test.
* **F2** [codex, grok, agy, glm, kimi, Opus] "the script discards grep's `Binary file ... matches` lines" is
  grep-version-dependent: WSL's grep 3.12 prints the notice on STDERR, which the filter never sees (it leaked into the
  09-20 battery log); git-bash's grep 3.0 prints it on stdout and the filter removes it.  **ACCEPTED**; records corrected.
* **F3** [glm, Opus] "the seven characters `delete` followed by a space" miscounts: `delete ` is seven characters
  counting its space.  **ACCEPTED** (wording).
* **F4** [codex] "turns gate 8 green" overclaims: only gate 8's `check_delete_calls.sh` row was measured.
  **ACCEPTED**; the records name the row, and the whole gate is left to the weekly battery (it needs gate 7's baselines).
* **F5** [codex, glm, Opus] "red for sixteen days BECAUSE gate 8 runs only weekly" is wrong.  The batteries of 09-06 and
  09-13 left no verdict (the scheduled task's last run is 09-20, next 09-27), so cadence alone would have shown it on
  09-13; and I measured that NOTHING runs `tools/nightly_check.sh`, the dead-man switch whose whole job is reporting a
  battery that never ran -- it is in neither precommit nor the session hooks.  **ACCEPTED**; records corrected; **to FILE
  `batterymissedruns` (MED)** with `#547`: the dead-man switch is never run.
* **F6** [all seats] A precommit landing spot is owed and is a FILING.  It must check the INDEX or HEAD, never the
  worktree: Opus measured that right now the worktree exits 0 while the index and HEAD exit 1 -- so gate 8 itself, which
  runs in the worktree, would report GREEN over a failing HEAD -- and glm that the script's fixed `tmp_delete.out` lets a
  concurrent run empty the loop into a silent pass.  `git grep --cached` costs 0.05 s.  **to FILE `deletecheckhead` (MED)** with `#547`:
  the tripwire and gate 8's domain together.
* **F7** [all] witness `none -- comment-only`, naming the evidence.  **ACCEPTED.**
* **F8** [codex, grok, Opus] the house idiom is "drop the exit(1)" (seven times, `dev_sh4.c`); "remove" is accurate and
  nothing pins the wording.  **ACCEPTED; "remove" kept.**
* **F9** [Opus] pristine upstream passes its own check by the same accident, and the fork's de1398e1 added two `delete `
  help strings that the check never saw.  **RECORDED** in `deletecheckhead`.

**On R**

* **F10** [codex (both jobs), Opus] `records_only()` (a) exempts `tools/pipeline/*.py` -- checker CODE -- so its comment's
  claim that a checker-logic fix still counts is false (measured on bbfc942e; 3 of 60 window commits; Q14: nothing hidden
  today); (b) passes `%h` to `git show`, which a same-named ref shadows (Opus, a tag `030e961` in a scratch clone) --
  `records_only(full)` is equivalent on all current data.  **Comment CORRECTED** (R-CORRECTIONS); **logic to FILE
  `attrcheckgaps` (MED)** with `#547`.
* **F11** [codex, grok, Opus] `git()` discards failures: `GIT_DIR=/nonexistent` gives `scanned 0 commits deep ...
  ATTRIBUTION_PASS`, and section L greps only for the PASS token (the sibling `check_checkpoint.py` refuses this case).
  **To FILE in `attrcheckgaps`.**
* **F12-F16** [codex, grok, deepseek, Opus, kimi] the constructions in the table.  **Q10-Q15 ADDED**; each measured.
* **F17** [grok, minimax] the hex-word hole reaches `commits` too (`bad_commits` accepts any 7-40 hex token, e.g.
  "effaced").  **RECORDED**, extending note 2.
* **F18** [agy] `not commits` tests whitespace tokens while `names()` extracts hex -- identical before and after R.
  **RECORDED.**
* **F19** [agy, glm, minimax, grok, kimi] Q6 is vacuous as matcher coverage: section L reads the WORKTREE ledger.
  **ACCEPTED**: Q6 is kept only as the committed ledger's result on a fresh clone; no claim rests on it.
* **F20** [kimi] the verifier's negative control: 3 breaks gave 4 failures because one appended line broke both Q9's
  verdict and Q9 == Q0.  **EXPLAINED.**
* **F21** [glm] "the inlined diff is one added line short in hunk 1" -- **REFUTED** by count: hunk 1 carries all 15
  added lines, +23/-6 in total, which kimi's recount also found.
* **F22** [glm] REOPENED lines print git's current `%h`.  **ACCEPTED** (display only).
* **F23** [kimi, Opus] "after 4264ee20 git's abbreviation became 8" is wrong: a REPACK at 2026-09-23 23:57 (24,350 packed
  objects) did it -- Opus reproduced 7 vs 8 characters on one history by packing -- so the pre-fix verdict depended on
  local gc state.  **CORRECTED** (R-CORRECTIONS; CHANGELOG in place).
* **F24** [Opus] "six correctly attributed rows" is SIX HARD LINES ON FIVE ROWS -- stagetokens twice.  **CORRECTED**
  (R-CORRECTIONS; CHANGELOG in place).
* **F25** [Opus] ledger row `lcaisalane`'s `reopened` text carries two U+0008 characters where `\b(closing)\b` was
  meant (a JSON escape, committed in e0be9b2a).  **CORRECTED in place**, that field only.
* **F26** [Opus] the carrier and the brief template still say three pristine-upstream copies sit under the project
  root; they moved on 2026-09-13 to `C:\DocumentNoSnc\cc\GXEMUL_upstream_2021` (confirmed: `./src` is gone); the
  MOVED.txt notes carry a literal CR and BEL where `\r` and `\a` were meant; and a directory named `GXEMUL-SEC` plus a
  carriage return sits at the project root.  **to FILE `carrierstalecopies` (LOW)** with `#547`, for the owner: those files are not
  this session's to edit, and deleting the stray directory is the owner's call.
* **F27** [kimi] no control exercises `records_only()`'s own lookup, and note 1 (prefix uniqueness) has no tripwire.
  **RECORDED.**

## 3. DISAGREEMENTS -- each side in its own words, then my ruling

* **D1 -- note 2, "recorded, not changed" (constructed `reopened` inputs).**  glm: *"Its stated reason is contradicted by
  its own recorded facts ... the exposure that recurs is the false NEGATIVE from innocent drift ... codify 'reopened
  begins with the sha token' as the field's written convention."*  kimi: *"on constructed input the new code fails LOUD
  ... where the old substring code failed SILENT ... the right direction for a gate."*  agy: *"leading-token-only would
  break rows recording multiple reopening commits."*  Opus: *"right, but not for the brief's reason ... the branch is
  entered once in 795 commits ... applied inside the SHARED names(), leading-token-only turns Q0 red; if ever, at the
  reopened call site only."*  **RULING: UPHOLD not-changed, on kimi's and Opus's reasons; ADOPT glm's codification as ONE
  comment sentence at the reopened test**, proposed text: *"`reopened` names its commit(s) as their own tokens; names()
  is boundary-anchored, so a sha glued to letters is invisible and the row HARDs."*
* **D2 -- note 1 (prefix uniqueness).**  glm: *"`full.startswith(t)` is an exact test ... uniqueness is load-bearing only
  where an abbreviation is resolved."*  codex and grok: prefix matching does not by itself establish that a token names
  ONE commit.  **RULING: glm's objection REJECTED** -- an ambiguous token passes `startswith` for EVERY commit it
  prefixes, so the row is credited with each; the comparison is exact, the naming is not.  Moot today: Opus resolved all
  184 unique ledger tokens unambiguously, and no 7-character prefix collides in 795 commits.
* **D3 -- Q7.**  agy: *"cosmetic mutation coverage ... git can abbreviate below 7 chars down to 4 via --abbrev=4."*
  codex, grok, minimax, Opus: Q7 is what separates the `{6,40}` construction.  **RULING: Q7 stands** -- `bad_commits()`
  fixes the field contract at 7-40, and Q7 keeps `names()` from reading `reopened` under a looser contract than the one
  that validates `commits`.
* **D4 -- the numstat.**  glm: one added line short; kimi: +23/-6 checks out.  **Settled by count: F21.**

## 4. WHAT IS STILL OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* I have ACCEPTED or RECORDED twenty-seven findings and REJECTED or REFUTED two.  That ratio is itself suspicious.
* SEVEN of those dispositions are "RECORDED" or "FILED" on one 350-line checker (F10, F11, F17, F18, F27, and the two
  halves of D1).  Is `attrcheckgaps` the right sink, or is the checker owed a round now?
* R is committed, so a breach found now is a follow-up commit, never an amendment.  None has been measured on current
  data: every construction found so far is separated by a control that now exists.
* The whole of gate 8 on HEAD+U is NOT measured -- only its delete row.

## 5. QUESTIONS

1. Adjudicate **F1-F27** and **D1-D4**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.  Skip
   the ones you have nothing to add to, but say which you skipped.
2. **WHICH OF MY ACCEPTED OR RECORDED DISPOSITIONS IS WRONG?**  Twenty-seven accepted in a row is not evidence.  If you
   raised a finding, be HARDER on my handling of it than on anyone else's -- and check that the FIX is right, not only
   that the finding was.
3. **WHAT DID ALL NINE OF US MISS?**  You now have the whole panel's output.

If, while verifying a claim, you found something ELSE -- say so.
