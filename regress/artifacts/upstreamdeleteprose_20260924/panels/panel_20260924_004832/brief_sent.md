# PANEL BRIEF -- `#547` upstreamdeleteprose (a one-word comment change that turns gate 8 green at HEAD), and the owed nine-seat review of `#546`'s attribution rider

Project root: C:\DocumentNoSnc\cc\GXEMUL.  2026-09-24.  Two independent questions in one packet: **U** (a proposed
commit) and **R** (a committed rider owed a review).  Answer both.

**FIRST LINE OF YOUR ANSWER, exactly this shape:**
`VERDICT: U=<SHIP | SHIP WITH NOTES | DO NOT SHIP>; R=<SHIP | SHIP WITH NOTES | DO NOT SHIP>`
then numbered findings tagged `U-n` / `R-n`.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (`src/`, `test/`, `tools/pipeline/`).  There are
THREE pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count — ENUMERATE it
rather than reasoning about it.**  **And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**

**VERDICT LINE FIRST**, so your answer survives truncation.

**Reading scope, for the seats that read files:** `GXEMUL-SEC/src/`, `GXEMUL-SEC/test/`,
`GXEMUL-SEC/regress/gate_upstream.sh` and `GXEMUL-SEC/tools/pipeline/check_commit_attribution.py`.  Please do not
read `GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json` -- what they would tell you is inlined.

## 0. HAS EITHER ALREADY SHIPPED?  (run at brief-writing time)

    git log -1 -- src/devices/dev_sgi_re.c    ->  fd150657 2026-09-12 #519 (sgirandomcolour) ...
    grep -c upstreamdeleteprose CHANGELOG.md   ->  0

U is NOT committed.  R IS committed: 3e33201d (#546, 2026-09-24), so this is its review AFTER the fact -- a finding
against R is disposed of as a wrong record (corrected in place), a measured false pass (fixed in a follow-up
commit), or a filing.

## 1. SETTLED PREMISES, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM

Settled by measurement today (durable copies in `GXEMUL-SEC/regress/artifacts/upstreamdeleteprose_20260924/`):

* **Gate 8 is `regress/gate_upstream.sh`**, which runs upstream's `test/check_delete_calls.sh` from the repository root
  and wants exit status 0.  The script, whole:

```
#!/bin/sh

rm -f tmp_delete.out
LC_ALL=C grep -R "delete " src|grep -v \\.svn|cut -d \: -f 1|sort|uniq |grep -v "inary file" > tmp_delete.out 2> /dev/null

ANYERRORS=0

for a in `cat tmp_delete.out`; do
	# Is $a a known exception?
	if grep -q $a test/check_delete_calls.exceptions; then
		:
	else
		printf "\nError: $a is not in check_delete_calls.exceptions!"
		ANYERRORS=1
	fi
done

rm -f tmp_delete.out

if [ z$ANYERRORS = z1 ]; then
	printf "\n\n"
	false
fi

```

  and `test/check_delete_calls.exceptions`, whole:

```
./HISTORY
./src/debugger/debugger.cc
./src/debugger/debugger_cmds.cc
./src/include/refcount_ptr.h
./src/include/thirdparty/debug_new.h
./src/include/thirdparty/fast_mutex.h
./src/include/thirdparty/static_assert.h
./src/main/debug_new.cc
./src/main/ComponentFactory.cc
```

* **On a pure `git archive` export of HEAD (3e33201d) the script exits 1** with
  `Error: src/devices/dev_sgi_re.c is not in check_delete_calls.exceptions!`.  **On the working tree with U applied
  it exits 0.**
* **The 2026-09-20 weekly battery failed gate 8** (it ran on a dirty tree):

```
  FAIL upstream check_delete_calls.sh                       got=1 want=0
       grep: src/debugger/debugger.o: binary file matches
       Error: src/devices/dev_sgi_re.c is not in check_delete_calls.exceptions!
       Error: src/devices/dev_sh4.c is not in check_delete_calls.exceptions!
```

  The `dev_sh4.c` instance lived only in another unit's UNCOMMITTED text: `delete ` occurs 0 times in HEAD's
  `dev_sh4.c` and 0 times in today's working copy.
* **The flagged text is a comment** added by `#513` (e302c98c, 2026-09-08).  Gate 8 runs only in the weekly battery;
  `tools/precommit_check.sh` does not mention `check_delete_calls` at all.  The battery's verdict directory holds no
  verdict between 2026-08-30 and 2026-09-20, so 09-20 was the first battery that could have seen it.
* **U changes no compiled code, measured:** HEAD's and the working `dev_sgi_re.c` differ in exactly one line; each was
  preprocessed at the SAME path with identical flags (`gcc -E -P`, 3049 lines each) and the outputs are byte-identical;
  compiled (`gcc -c -O0`) the two objects are byte-identical (32752 bytes each).

## 2. THE DIFF U  (`git diff --numstat`: `1  1  src/devices/dev_sgi_re.c` -- INLINED; the only file)

```
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 8e9727d5..2eff3075 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -502,17 +502,17 @@ DEVICE_ACCESS(sgi_re)
 				debug("d->re_tlb_a[%i] = 0x%04x\n", tlbi, d->re_tlb_a[tlbi]);
 				tlbi++;
 			}
 		} else {
 			/*
 			 *  #513: ACCEPT.  A guest read of a len == 8 TLB slot ended
 			 *  the host.  The write arm directly above already computes
 			 *  and stores the value, so the disposition is member 4 of
-			 *  the option set -- delete the kill and RETURN THE VALUE --
+			 *  the option set -- remove the kill and RETURN THE VALUE --
 			 *  rather than a decline: nothing is unimplemented here.
 			 *  This loop is the exact inverse of the write loop, cell for
 			 *  cell and shift for shift.
 			 *
 			 *  *** IT MUST WRITE odata, NOT data[]. ***  The function's
 			 *  common tail is
 			 *      if (writeflag == MEM_READ)
 			 *              memory_writemax64(cpu, data, len, odata);
```

## 3. QUESTIONS ON U

**U1 (premise audit).**  I believe the check matches the seven characters `delete` followed by a space ANYWHERE in
any file under `src/` -- comments, strings, identifiers alike -- and discards grep's `Binary file ... matches` lines.
Check that.  And check whether any OTHER file at HEAD fails the script once this one is fixed.

**U2 (option set).**  (a) reword the comment -- chosen; (b) add `src/devices/dev_sgi_re.c` to the exceptions list;
(c) change upstream's check (e.g. ignore comments); (d) a member I did not name?  The exceptions test is
`grep -q $a` of each flagged path against the list -- a SUBSTRING match.  What would (b) stop the check seeing?
Grep the fork for how other comments phrase the same idea without the flagged word.

**U3 (recurrence).**  This sat red at HEAD for sixteen days because gate 8 runs only weekly.  Is a structural landing
spot owed -- for instance precommit running `test/check_delete_calls.sh` -- and is that this round's work or a filing?
Say whether it is cheap and sound; a design is not needed.

**U4 (records).**  The ledger row closes with witness `none -- comment-only ...`.  The vocabulary: `none` =
"documented-only; no code shipped, or explicitly filed"; `harness:` = "the round's subject IS the test apparatus, so
there is no guest path to witness".  Here the subject is a comment in emulator source that the test apparatus flags,
and the compiled code is measured identical.  Which term is honest?

## 4. THE RIDER R -- committed in 3e33201d (#546); its owed nine-seat review

**The defect (measured).**  `tools/pipeline/check_commit_attribution.py` (precommit section L) reads the last 60
commit subjects, finds ledger row ids in them, and grades each match: a CLOSED row must name the commit in its
`commits` field (whitespace-separated shas, validated elsewhere as 7-40 lowercase hex, or a "no commit" /
"outside the repo" / "ops" note); a subject saying "closed" against a non-closed row is HARD unless the row's
free-text `reopened` field names the commit.  It compared git's `%h` by exact membership (`h in commits`) and by
substring (`h in reopened`).  The rows carry the 7-character form git printed when each closed; after `4264ee20`
git's automatic abbreviation became 8 characters (`git log --abbrev=7` still prints 7 for all 794 commits -- no
collision; git's own minimum grew), so six correctly attributed rows hard-failed and the gate was red for every
commit.  The mirror case failed too: a row written at 8 characters did not match a 7-character `%h`.

**The fix as committed** (`git show --format= 3e33201d -- tools/pipeline/check_commit_attribution.py`, 23+/6-,
INLINED):

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

**Controls** (predictions sealed before each run; every output asserted by a verifier, 18/18, whose own negative
control -- three injected breaks in a copy -- gave 14/18 and exit 1):

| case | input | result |
|---|---|---|
| pre P0 | 8-char abbreviation, depth 60 | 6 HARD (the six) |
| pre P1 | abbreviation 7 | 1 HARD: `4264ee2 fbdeclinefive` (the ledger holds `4264ee20`) -- a MISSED prediction, recorded before the edit |
| pre P2 | 8-char, depth 130 | 11 HARD, incl. `b78bb0f6 pcc2widthkills`, whose `reopened` names `b78bb0f` |
| post Q0 / Q1 | 8 / 7 chars | 0 HARD; the two outputs identical modulo hash width |
| post Q2 | depth 130 | REOPENED `b78bb0f6`, 0 HARD |
| post Q3 | a closed row's commits = a different real sha | HARD |
| post Q4 | commits = `cdbe7d76` (agrees with `cdbe7d75...` in 7 chars; not a prefix) | HARD |
| post Q5 | commits = the full 40-char hash | no HARD |
| post Q6 | the index ledger | 0 HARD |
| post Q7 | `pcc2widthkills.reopened = "b78bb0 -- ..."` (6 chars), depth 130 | HARD |
| variant Q8 | extractor `{7,40}` -> `{6,40}` (applied in memory), Q7's input | REOPENED, PASS -- Q7 separates it |
| variant Q9 | the same variant, Q0's input | byte-identical to Q0 (Q0-Q6 could not see it) |

**Two seats reviewed R before commit -- codex (GPT-6 Astra, max) and grok 4.7 (xhigh), both SHIP WITH NOTES,
agreeing on every note.  Their notes, and my dispositions:**

1. Prefix matching presumes the prefix is unique -- true of every current token.  RECORDED.
2. The extractor is shared with the FREE-TEXT `reopened` field, where constructed inputs defeat it: a 7+ letter
   hex-only English word ("effaced") that prefixes a scanned commit's hash reads as a name (the old substring test had
   the same exposure at 7 characters); a sha glued to letters, or followed by an uppercase hex digit, becomes
   invisible (the old test saw it); `_` and non-ASCII letters count as boundaries.  None occurs in the ledger -- two
   rows carry `reopened`, both opening with their sha.  RECORDED, NOT CHANGED: the suggested remedy (parse only the
   leading token, with a stated case policy) changes the field's meaning and is its own round if wanted.
3. My comment said `%h` was only printed, but `records_only(h)` passes it to `git show` -- a lookup of the
   abbreviation git just printed, not a comparison.  COMMENT CORRECTED; the output re-ran byte-identical.
4. The `{7,40}` -> `{6,40}` variant survived Q0-Q6.  Q7 ADDED; it separates the variant.
5. The first driver only printed, so a wrong verdict could not fail it.  VERIFIER ADDED.
   Also noted: Q6 adds no matcher coverage (section L reads the WORKTREE ledger, not the index); Q4's gloss "a shared
   prefix is not a name" was loose -- `cdbe7d76` is NOT a prefix -- corrected in the results file.

## 5. QUESTIONS ON R

**R1.**  Which of the dispositions above is WRONG?  I accepted or recorded every note from two seats -- agreement is
not evidence -- and "recorded, not changed" on note 2 is the one I am least sure of.
**R2.**  Does an edit to the committed code exist that keeps EVERY control above green yet changes a verdict on the
CURRENT ledger or history?  Say whether one exists; name it if you can.
**R3.**  What did both earlier seats miss?

If, while verifying a claim, you found something ELSE — say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
