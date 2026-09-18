# `#532` stagetokens -- PASS 2 on the committed diff (686d179).  OWED: the round shipped without one.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise stated wrongly. **Check the premises.** The tree is
`GXEMUL-SEC/`; the files are harness checkers in `tools/pipeline/`, not emulator code. If you cannot read files
that is expected -- the diff is inlined. **VERDICT LINE FIRST.**

## 1. SETTLED PREMISES (measured 2026-09-18, re-derive any you doubt)
* HEAD before 686d179 carried ZERO stage violations; the working tree carried NINETEEN, every one created by
  RECORDING 23 unread seat answers onto the rows they discussed (a recorded remark promotes a stage from ABSENT
  or a one-seat FILING into a 2..8-seat "short panel", which sections H and I redden on).
* The sorting rule used: open each cited panel dir's `brief_sent.md` and ask WAS THIS PANEL CONVENED ON THIS
  ROW.  It overturned a seat-COUNT sort three times; the flagship seat then ruled one stage MISDIRECTED (the
  brief named the row and inlined the wrong material).
* Neither existing token was true: RE_READ says SINGLE-SEAT; ANNOTATION asserts a pre-2026-08-16 vintage.
* Negative controls, run before the token touched real data: a synthetic 3-seat post-cutoff stage reds BOTH
  gates without the token and passes both with it, and the token entry is not counted as a seat.
* gen_dashboard.py matched cells on seat+phase alone; annotations are conventionally written `seat: fable5`,
  so they rendered as FABLE cells.  Pre-fix generator emitted 25,154 more characters than post-fix.
* SINCE the commit, the token was used again and one misuse happened: a main-loop verification was first
  recorded as `seat: opus5`, promoting landiskaux's assess stage to 2/9 -- corrected with the token.

## 2. THE DIFF
```diff
diff --git a/tools/pipeline/check_fable_queue.py b/tools/pipeline/check_fable_queue.py
index 52ddbb8..890a02f 100644
--- a/tools/pipeline/check_fable_queue.py
+++ b/tools/pipeline/check_fable_queue.py
@@ -44,6 +44,16 @@ FLAGSHIP = "fable5"
 HELD = "[HELD AWAITING SEAT:"
 ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"
 
+#  *** THESE TWO WERE KNOWN TO check_stage_panels.py AND NOT TO THIS FILE, SO A STAGE COULD PASS
+#  SECTION H AND STILL RED SECTION I ON THE SAME LEDGER ENTRY.  Found 2026-09-18 while adding
+#  NOPANEL, by asking what the OTHER checker does with the same tokens. ***  The two gates are
+#  deliberately non-redundant -- H asks whether the seat was FIRED, I asks whether owed flagship
+#  work is WRITTEN DOWN -- but "this stage is not a panel stage at all" is a fact about the
+#  LEDGER ENTRY, not about either question, so both must honour it or they disagree about what
+#  the entry means.  RE_READ has been in the other file since 2026-08-21 and was never mirrored.
+RE_READ = "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]"
+NOPANEL = "[NOT A PANEL STAGE: NO PANEL CONVENED]"
+
 #  Directive dates.  Work that predates a directive cannot be judged by it.
 CUTOFF_FULL_PANEL = "2026-08-16"   # full panel on every stage
 CUTOFF_REGRESS_FABLE = "2026-08-15"  # regress becomes flagship-only
@@ -102,7 +112,7 @@ def main(argv):
             note = ent.get("note", "")
             d = stages.setdefault(ph, {"seats": set(), "newest": "", "held": False,
                                        "annotated": False})
-            if ANNOTATION in note:
+            if ANNOTATION in note or RE_READ in note or NOPANEL in note:
                 d["annotated"] = True
                 continue
             if HELD in note:
diff --git a/tools/pipeline/check_stage_panels.py b/tools/pipeline/check_stage_panels.py
index 9f79606..5d532dc 100644
--- a/tools/pipeline/check_stage_panels.py
+++ b/tools/pipeline/check_stage_panels.py
@@ -82,6 +82,49 @@ ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"
 #  promote a filing into a short stage without anyone deciding to.
 RE_READ = "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]"
 
+#  A THIRD EXEMPTION, 2026-09-18, and like the second it exists because neither older token was
+#  TRUE of the situation -- which is the only reason this file ever gains a token.
+#
+#  A session read 23 UNREAD SEAT ANSWERS off disk and recorded each onto the row it discussed.
+#  That is strictly an improvement to the record: this project has three times found real
+#  defects sitting in an unread review.  **It took both stage gates from GREEN to RED, creating
+#  19 violations where HEAD had zero** -- because recording a seat's remark about row X makes
+#  row X's stage go from ABSENT (or a 1-seat filing) to a 2..8-seat "short panel", and a short
+#  panel is what this check reddens on.
+#
+#  *** SO THE GATE FIRED BECAUSE THE RECORD GOT MORE HONEST, AND THE ONLY WAY TO GREEN IT WITH
+#  THE OLDER TOKENS WOULD HAVE BEEN TO WRITE A FALSE SENTENCE INTO THE LEDGER. ***  RE_READ says
+#  SINGLE-SEAT, and several of these carry 2, 3, 4, 6 and even 8 recorded seats; ANNOTATION
+#  asserts a pre-2026-08-16 vintage that is simply untrue of a 2026-09-17 entry.  The comment on
+#  RE_READ already records the last time someone reached for the nearest token to turn a gate
+#  green, and that attempt was backed out.  This is that lesson obeyed rather than re-learned.
+#
+#  THE DISCRIMINATOR, and it is mechanical rather than a judgement call: read the `ev` field for
+#  the panel dir, open that dir's `brief_sent.md`, and ask **WAS THIS PANEL CONVENED ON THIS
+#  ROW?**  If the brief's subject is this row (or a deliberate multi-row late review naming it),
+#  the stage RAN and this token is a lie.  If the brief is about some other row and a seat merely
+#  mentioned this one in passing, no panel was ever convened here.
+#
+#  *** THAT TEST OVERTURNED THE AUTHOR'S FIRST SORTING, WHICH IS WHY IT IS WRITTEN DOWN AS A
+#  COMMAND AND NOT AS ADVICE. ***  Seat COUNT was used first -- "+8 seats must mean a real panel"
+#  -- and it was wrong three times over: `diskimagesign`, `pcc2c040assertrow` and
+#  `pcc2genctlc040alias` all cite ONE dir, `panel_20260917_100431`, whose brief IS convened on
+#  them, so they are real stages; while `asiceventaddr` carries a full EIGHT recorded seats that
+#  all cite `panel_20260826_222557`, a pass 2 on a COMMENT-ONLY commit to a vendored header --
+#  a different subject entirely, and therefore not a stage at all.  **The count is a CORRELATE
+#  of "a panel ran"; the brief's subject is the thing itself.
+#
+#  *** THE TOKEN STATES THE GENERAL CLAIM AND THE NOTE CARRIES THE SPECIFIC REASON, WHICH IS A
+#  DELIBERATE BREAK FROM THE TWO TOKENS ABOVE. ***  Those bake their reason into the literal,
+#  and that is exactly what made RE_READ unusable here -- it says SINGLE-SEAT, so a true
+#  situation with three seats had no token that fitted.  A first draft of THIS token repeated
+#  the mistake: it read INCIDENTAL SEAT MENTION, which is true of eleven of the twelve stages
+#  and FALSE of `ip30abortkill' assess, whose two entries are a rung-3 WITNESS BUILD and a
+#  ship-order ADJUDICATION -- real work on that very row, and not a panel seat answer at all.
+#  The checkable claim both gates need is only ever "no panel was convened on this stage";
+#  everything else is provenance, and provenance belongs in prose a reader can check.**
+NOPANEL = "[NOT A PANEL STAGE: NO PANEL CONVENED]"
+
 #  *** A STAGE DELIBERATELY HELD FOR A NAMED SEAT IS NOT A STAGE THAT MOVED ON. ***
 #
 #  Added 2026-08-17.  Fable usage ran high and the owner said to queue Fable work and carry on
@@ -119,7 +162,8 @@ def main(argv):
     for row in ledger["rows"]:
         by_stage = {}
         for ent in row.get("entries", []):
-            if ANNOTATION in ent.get("note", "") or RE_READ in ent.get("note", ""):
+            if (ANNOTATION in ent.get("note", "") or RE_READ in ent.get("note", "")
+                    or NOPANEL in ent.get("note", "")):
                 by_stage.setdefault(ent.get("phase"), {})["_annotated"] = True
                 continue
             if HELD in ent.get("note", ""):
diff --git a/tools/pipeline/gen_dashboard.py b/tools/pipeline/gen_dashboard.py
index 0b81cc6..a40eca5 100644
--- a/tools/pipeline/gen_dashboard.py
+++ b/tools/pipeline/gen_dashboard.py
@@ -82,9 +82,37 @@ BADGE_TIP = {"A": "the author did this review (shown, not hidden)",
 STATE_ORDER = {"active": 0, "held": 1, "pending": 2, "closed": 9, "dropped": 10}
 
 
+#  *** AN ANNOTATION IS NOT AN ANSWER, AND UNTIL 2026-09-18 THIS FILE COULD NOT TELL THEM APART.
+#  ***
+#  `check_stage_panels.py` and `check_fable_queue.py` both SKIP entries carrying a stage token
+#  before tallying seats -- an annotation exists to say WHY a stage is short, so counting it as one
+#  of the seats that answered would let marking a gap CLOSE it.  This file never learned that, and
+#  `cell()` matched on `seat` + `phase` alone.
+#
+#  The tokens are conventionally written with `seat: "fable5"`, so every one of them rendered as a
+#  FABLE CELL -- **the dashboard asserted that the flagship seat had answered a stage on which no
+#  panel was ever convened.**  That is not a cosmetic slip: it is the inverted form of the failure
+#  this whole layer exists to prevent.  A missing cell reads as "seat failure, never agreement",
+#  which the legend says out loud; a FABRICATED cell reads as agreement from the one seat whose
+#  agreement carries the most weight, and nothing anywhere contradicts it.
+#
+#  Found 2026-09-18 by asking what the OTHER tools do with a token this file does not know -- the
+#  same question that had just found `check_fable_queue.py` blind to RE_READ.  **Two tools, two
+#  blind spots, one cause: a token was added where it was needed and never mirrored.**
+STAGE_TOKENS = ("[RUN UNDER THE PRE-2026-08-16 POLICY]",
+                "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]",
+                "[NOT A PANEL STAGE: NO PANEL CONVENED]",
+                "[HELD AWAITING SEAT:")
+
+
+def _is_answer(x):
+    note = x.get("note") or ""
+    return not any(t in note for t in STAGE_TOKENS)
+
+
 def cell(row, phase, seat):
     ents = [x for x in row.get("entries", [])
-            if x["seat"] == seat["id"] and x.get("phase") == phase]
+            if x["seat"] == seat["id"] and x.get("phase") == phase and _is_answer(x)]
     if not ents:
         return '<td class="c none"><span class="g">·</span></td>'
     ent = ents[-1]
```

## 3. QUESTIONS
Q1. Is `[NOT A PANEL STAGE: NO PANEL CONVENED]` the right SHAPE -- a general claim with the specific reason in
    the note -- or should it have been two specific tokens, given the two existing tokens bake their reason into
    the literal?
Q2. The token is honoured by FILTERING -- an annotated stage is skipped by H and I.  **What stops it being used to
    silence a stage that DID run short?**  Name the concrete misuse and say whether any check can catch it.  (The
    RE_READ comment records one attempt to reach for the nearest token to turn a gate green.)
Q3. gen_dashboard.py now DROPS annotated entries from cells, so they render BLANK -- and the legend reads blank as
    "no answer / seat failure (not agreement)".  Is a blank for a never-convened stage a NEW conflation of two
    states?  Should it render a distinct glyph?
Q4. The smallest edit to this diff that breaks a property it claims and still passes the negative controls.
