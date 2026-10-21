# Late-review ADJUDICATION: three Argon (Gemini web) readings of committed rounds, checked against HEAD -- which of my dispositions is wrong?

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  A seat that re-derives a disposition from something this packet did NOT give it is worth more
than a seat that agrees.

**THE TREE IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` AT COMMITTED HEAD `1a59a47e`** (records-only over `5dbc000e`).
Ignore every other `src/` under the project root (pristine 2021 upstream copies).  The working tree carries unrelated
uncommitted edits -- cite HEAD (`git show HEAD:<path>`), not the working file.  **If you cannot read files that is
expected** -- the dispositions, the evidence and the small diffs are inlined; name any premise you cannot settle.
**VERDICT LINE FIRST.**

## 1. What this is

Argon (Gemini 4 web, a packet-fed lens) read the packets of three rounds that have SINCE COMMITTED, and returned flags:
`rldiclf2` (#565's shared-findings pass), `ip30wirep2` (#566's pass 2), `fhfp1` (`fableheldform`'s design pass).  It read
PRE-COMMIT DRAFTS, so many flags are already satisfied at HEAD.  Three Opus 5.5 sub-agents then checked every flag
against HEAD (reading only; their full reports, with HEAD quotes and line numbers, are the files named below).  **The
project's LATE-DISSENT RULE governs** (verbatim): *"A panel stage fired after a round closes adjudicates like any other
finding.  Closure changes the LICENSE, never the truth-value.  Three dispositions, exhaustive: 1. WRONG RECORD -> L4,
correct in place.  2. MEASURED FALSE PASS against the shipped detector's floor, contract or obligations -> L2/L3 per the
existing rules, in a follow-up commit.  3. EVERYTHING ELSE, design dissents included -> FILES AS A NEW QUEUE ITEM ...
Never amend shipped code under a closed round's number."*

Full reports (file-reading seats: please open them; packet-fed seats: the table below is their summary):
* `C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/rldiclf2/FLAGS45.md` (+ `flags45.diff`)
* `C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/argonlate/ip30wirep2/FLAGS.md` (+ `edits.diff`)
* `C:/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/argonlate/fhfp1/FLAGS.md` (+ `edits.diff`, `work/`)
* Argon's own answers: `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/gweb/jobs_20261018_argonpack17/rldiclf2/gemini_web.out`,
  `.../jobs_20261018_argonpack17/ip30wirep2/gemini_web.out`, `.../jobs_20261018_argonpack18/fhfp1/gemini_web.out`

## 2. The dispositions (mine; each on the checker's evidence)

### A. `rldiclf2` -> `regress/ppc_rldicl_probe.py` (#565, gated in gate 13)
| # | item | finding at HEAD | my disposition |
|---|---|---|---|
| A0 | Argon flags 1-3 (disasm-coverage count; "comments only"; dead-run vs identity body) | HEAD's text already enumerates all four sessions; the manifest note already says "its comments and one printed note"; the identity-body leg was MEASURED at `regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/identity/` | OVERTAKEN |
| A1 | "the five flipped rows being exactly the ones kept below" (probe docstring block `WHY THE SIBLING ROWS ARE NOT HERE`) | the five rows that flip are all ABOVE it; below are the five pass-2 rows, three of which flip pre-fix; `git log -L` shows "below" was never positionally true | L4, in place |
| A2 | the printed banner `wants derived from ...:29736 (rldiclx), :6878 (ROTL32)` | no scored row uses ROTL32 (all 24 `row(` calls enumerated); the rldicr wants' source (`:29822`) is missing | L4: banner text (prints in every gate-13 log; no gate check reads it) |
| A3 | docstring "EVERY 'want' in this probe is computed from those five lines, never from the tree" (+ the TEST-FIRST SHAPE sentence) | 9 wants from those lines; 3 from other text (two rldicr rows, one literal CR0); 2 from the tree (a decoder string, an exit status) | L4: narrow to "every rldicl VALUE want".  A matching comment at `src/cpus/cpu_ppc_instr.c:2470` is LEFT OUT (a `src/` edit makes this a source commit); FILED for the next PowerPC round |
| A4 | CONTRACT "every entry was established by a mutant that was built and scored" | 14 entries; 6 map to built mutants, 1 partially, 7 have none | L4: mark the 7 as REASONED (not measured) |
| A5 | knock-on: `tools/pipeline/check_probe_wiring.py`'s manifest note for the t2 frozen copy lists what changed since e777ff06 | becomes incomplete once A1-A4 land | L4: extend the note |
| A6 | `regress/artifacts/ppcrldiclzero/killtable_20260910/t2/SCORES.txt` line 1 reads `#521 mk48nvramkill` | wrong round (only t1's header was fixed) | L4: bracketed correction at the header |

### B. `fhfp1` -> `fableheldform` (records round 6c2840d7)
| # | item | finding at HEAD | my disposition |
|---|---|---|---|
| B0 | F2-F9, M1, M2 | already done by 6c2840d7, or settled by reading (13 counted Fable answers since 10-16, all genuine) | OVERTAKEN (M1 = owner option E stays OPEN; Argon's one caution: an E keyed to the fable5 SEAT would also let alphavmkill's 2026-09-19 first-hand hold close -- key it to the 2026-10-17 directive instead) |
| B1 | WR-1 `fableheldform.state_note`: "the cxlaunchquotation and dashokclass V3-V6 passes" | cxlaunchquotation's V3 STALLED and its V6 WALLED -- not answers | L4 |
| B2 | WR-2 the v2/V3 stalls called walls (CHANGELOG, bug file, ledger, two seat entries) | Astra and Grok said V3 stalled | L4 |
| B3 | WR-3 passes Fable was NOT FIRED on, recorded as walls | 8 of the 15 HELD entries; five rows' `state_note`/`reopened` and the summaries contradict each row's own `hold_question` | L4 |
| B4 | M3 Argon's "same-day discharge fix" in `stage_tokens.py` (compare `(date, index)`) | the strictly-later-date rule is deliberate (the 2026-08-30 same-date mis-clears, `tools/CLAUDE.md`); index ordering re-opens them; zero holds at HEAD would change | REFUTED |
| B5 | X1a LATENT DEFECT: `sgirekills` assess [2] holds for kimi+opus5; notes [70]/[71] (2026-10-18) say "NOT FIRED -- ... it never answered" but carry no token, so `live_holds` counts them as answers and `--list` prints `ok sgirekills assess 9/9` | measured on ledger copies: HEAD-form re-closed -> section H PASSES; with the non-answer token on [70]/[71] -> CLOSED-WHILE-HELD 7/9.  The row is HELD now, so nothing passes falsely TODAY | FILE into `untokenedanswers` (its owner ruling item (2) is owed before sgirekills re-closes) -- see Q2 for the alternative |
| B6 | S1 a structural check that REQUIRES a positive answer marker | new; 7 genuine answers since 10-01 would trip a keyword check | FILE (extends `untokenedanswers`) |
| B7 | X1b `fableheldform`'s own review stage is 1/9 and becomes 2/9 the moment Fable's answer is recorded -- section H reds | its narrowed roster lives only in CHANGELOG prose | FILE |

### C. `ip30wirep2` -> `regress/artifacts/ip30abortkill/ip30_abort_probe.py` (#566, gated in gate 14)
| # | item | finding at HEAD | my disposition |
|---|---|---|---|
| C0 | F1-F3, F5 (most), F6, F7, Q4 | HEAD already carries them (Argon read drafts of four of five files) | OVERTAKEN |
| C0' | F8, the UNSETTLED items, Q3 | refuted or settled by reading/re-derivation (section U re-derived at 8faf4a16: PINNED=35, PASS) | REFUTED |
| C1 | W1: the probe's #566 note says no table holds clause (b) | `d42c76a8` MEASURED it 14/33 (`close_20261018/CLAUSE_B.txt`) | L4 |
| C2 | W2-W9: eight more probe sentences false of the shipped probe (five ISR sites -> three since F13; "both announce" / "the announce still fires" where the read arms decline silently; a CONTRACT "every CATCH has a MEASURED kill" with two unmeasured; "TWO declined ISR accesses" that are stored writes; "the 27-row instrument's" list whose M11 line is row 28; "a mutant that scored 12/12" that was a prediction) | -- | L4 via ONE dated block inside the docstring (W6/W7 sit in string literals; in-place edits would change the AST -- the block keeps the AST, docstring excluded, identical; verified) + one bracketed line in #566's CHANGELOG block |
| C3 | the ledger cites `regress/artifacts/ip30abortkill/PROBEATTACK_grok_20260917.txt` three times as durable, and it is UNTRACKED | -- | commit the file in the same unit (it is the warrant for W9's correction) |
| C4 | five `opus_killtable_20260917` drivers listed in `check_probe_wiring.py`'s MANIFEST under #531 target `dev_sgi_re.c` / `cpu_arm_instr.c` | misattributed classification notes | L4 in place (the checker file carries other units' uncommitted lines: HEAD + this hunk only) |

**One records unit lands A1-A6, B1-B3, C1-C4 (+ the B5/B6/B7 filings).  No `src/` file.  Ledger entries record each
review under its row with this adjudication's verdicts.**

## 3. The small diffs, verbatim (proposed; not applied)

### 3a. `regress/ppc_rldicl_probe.py` (A1-A4)
```diff
--- a/regress/ppc_rldicl_probe.py
+++ b/regress/ppc_rldicl_probe.py
@@ -55,6 +55,12 @@
 that is 0x00000000ffffffff, which is why `rldicl rA,rS,0,32' is the canonical
 32-bit zero-extend (`clrldi rA,rS,32', manual :29758).
 EVERY `want' in this probe is computed from those five lines, never from the tree.
+[#NNN, 2026-10-20: TOO BROAD.  True of the rldicl VALUE wants -- the six rows that call
+want_rldicl, and the census's and `naive fix wrong''s comparisons.  The two rldicr controls
+use rldicrx (:29822, MASK(0, e)) and `rc cr0' wants a literal CR0=GT; the apparatus rows want
+literals or this file's own counts; and `bits32 rld bad' and `neg apparatus' want the TREE's
+own decoder text (`TODO: rld') and exit status (exit1) -- which also makes TEST-FIRST SHAPE's
+`every want is the ARCHITECTURAL value' below untrue of those two and of the apparatus rows.]
 
 RUNG 3: real PowerPC instructions fetched from guest RAM, decoded by the real
 decoder and executed by the real handler, on the UNMODIFIED in-tree `-E bareppc'.
@@ -389,8 +395,12 @@
 print("ppcrldiclzero RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
 print("machine: -E bareppc -M 64 (UNMODIFIED in-tree; MACHINE_DEFAULT_CPU=PPC970,"
       " 64-bit)")
+#  [#NNN, 2026-10-20: this printed `:6878 (ROTL32)' from e777ff06, carried from the family
+#  witness, whose rlwinm/rlwimi rows consumed rotl32.  No row here does (the CONTRACT above
+#  want_rldicl).  :6878 also defines ROTL64, which every rldicl and rldicr want uses, and the
+#  two rldicr controls take their mask from rldicrx, :29822.]
 print("wants derived from _scratchpad/ppc_pem_32and64_2005.txt:29736 (rldiclx),"
-      " :6878 (ROTL32)")
+      " :29822 (rldicrx), :6878 (ROTL64)")
 print("%-18s %-20s %-20s %-48s %s" % ("row", "got", "want", "note", ""))
 t0 = time.time()
 disasm_checked = 0
@@ -552,7 +562,8 @@
 #  or into a detector of its own -- that is a decision for those rounds, not this one.
 #
 #  MEASURED: witness 19/27 committed and 24/27 fixed, the five flipped rows being
-#  exactly the ones kept below.  **THIS FILE HAS 19 ROWS, NOT 24** [19-row era: 24 since
+#  exactly the ones kept below [#NNN: ABOVE this block, not below it -- see its end].
+#  **THIS FILE HAS 19 ROWS, NOT 24** [19-row era: 24 since
 #  pass 2, see #565's note below] -- an earlier draft of this note carried the witness's
 #  own post-fix count straight across, which a pass-2 seat caught.  It is 19/19 on the
 #  fix and 14/19 pre-fix (killtable_20260910/SCORES.txt).
@@ -563,6 +574,14 @@
 #  rldicl_prefix_02af7f3e.log).  The 19-row figures are in killtable_20260910/t1/SCORES.txt;
 #  the bare `killtable_20260910/SCORES.txt' above names no file.  This block also stood
 #  here TWICE, verbatim, from e777ff06 until #565 deleted the copy after the pass-2 rows.]
+#  [#NNN, 2026-10-20: `kept below' is positional and true in no revision on record.  The five
+#  flipped rows -- zx32 rldicl, rot8 rldicl, vac neighbour, census wrong, census zero -- are
+#  rows this file KEPT, as against the sibling rows left in the witness, and they sit ABOVE this
+#  block, which has followed them since the 19-row frozen draft,
+#  killtable_20260910/t1/ppc_rldicl_probe.frozen.py.  The five rows below it are pass 2's, which
+#  the witness does not have, and only three of them flip pre-fix (sh63, sh32, rc cr0:
+#  killtable_20260910/t2/SCORES.txt).  Deleting the second copy did not move this one: it has
+#  had the pass-2 rows below it since e777ff06.]
 
 # ================== ROWS ADDED BY PASS 2, WHICH FOUND TWO TOTAL ESCAPES =========
 #
@@ -614,6 +633,14 @@
 #  WHAT THIS DETECTOR IS DESIGNED TO CATCH, and what it is NOT.  The boundary below
 #  is MEASURED -- every entry was established by a mutant that was built and scored,
 #  not by reasoning about the row set.
+#  [#NNN, 2026-10-20: NOT EVERY ENTRY.  No mutant was built for the mask END bound (`mb <= 62'
+#  was "Recorded rather than re-run", killtable_20260910/PRETABLE.out), rotate-versus-shift,
+#  the destination width, the `ra' decode, the rotate amount at SH=0, or any NOT CAUGHT entry:
+#  those are reasoned.  The rest are M_ORIG, M_MASKEND (the bit positions), M_NAIVE, M_NOMASK,
+#  M_MB5, M_SH5 (SH=32, 63) and M_CR0 in killtable_20260910/t2/SCORES.txt, and SH=8 is M_ROTAMT
+#  against the 19-row instrument only (pass2_20260910/opus_killtable_SCORES.txt).  The box came
+#  from section 4 of pass2_20260910/opus_pass2_20260910.md, `Measured, the boundary is', which
+#  mixed the two.]
 #
 #  CAUGHT:  the mask variable; the mask bit positions; the mask end bound; `&' -> `|';
 #           the mask ignored entirely; the `mb'-field decode INCLUDING its high bit;
```

### 3b. the IP30 probe docstring block + the #566 CHANGELOG line (C1, C2)
```diff
diff --git a/regress/artifacts/ip30abortkill/ip30_abort_probe.py b/regress/artifacts/ip30abortkill/ip30_abort_probe.py
--- a/regress/artifacts/ip30abortkill/ip30_abort_probe.py
+++ b/regress/artifacts/ip30abortkill/ip30_abort_probe.py
@@ -46,6 +46,26 @@
 ESCAPES below, and the WIDTH axis (V8_len4, 33/33 in table 5), under DOES NOT CATCH.  Since
 #566 this probe runs in gate 14 (regress/gate_arm.sh); a load stall can read green there
 (ip30stallgreen).
+[2026-10-20, records -- the note above and the text below re-checked at 5dbc000e and kept as
+written.]  More statements in this file are no longer true of the probe that ships:
+  * the note's fifth bullet is out of date: clause (b) WAS measured after #566 -- the removed
+    fatal() + abort() pair re-inserted at all four fixed sites of the fixed file scores 14/33
+    (regress/artifacts/ip30abortkill/close_20261018/CLAUSE_B.txt).  And `Every CATCH below
+    has a MEASURED kill in killtable{,2}' overstates two more CATCHes: no kill table deletes
+    the 0x10020 store or reds `isr keep' (M1 deletes the 0x10028 store and reds `isr clr'),
+    and M11 was killed in killtable3_20260918, not in killtable{,2};
+  * the CATCHES list is not only the 27-row instrument's: its M11 line names row 28,
+    `isr 28 rd val', added at the F2 sibling-parity repair (killtable3_20260918, base 28/28);
+  * the first two bullets' F13 corrections have siblings below, also kept as written:
+    `ALL FIVE ISR announces' (the `kill 30 txt' comment) and `all five ISR sites' (the
+    write-arm `txt' comment) are three since F13; the SIBLING PARITY comment's `both
+    announce' and the note of `isr 28 rd val', `(the announce still fires)', predate F13 --
+    the read arms decline silently, and `kill 28 rd txt' stays green under M11 because that
+    arm stays silent; the note of `latch 1x', `TWO declined ISR accesses', predates its
+    re-aim -- they are two WRITES, whose stores the arms keep;
+  * over the PROBE ATTACK rows, `Every one of these closes a mutant that scored 12/12' quotes
+    a READING: that attack ran no emulator, and the rows were written CONSTRUCTED, not
+    MEASURED; no kill table holds M_tick_abort, M_wf20_abort_wr or M_wf28_abort_wr.
 ================================================================================
 THE CONTRACT -- vacuity-floor clause (e).  A detector that says what it catches is
 FALSIFIABLE; one that claims completeness is not.  Every CATCH below has a MEASURED
diff --git a/CHANGELOG.md b/CHANGELOG.md
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -239,6 +239,7 @@
   five; `latch 1x` on the write arms; the ten enumerated latch cells and the `xbit rev2` a measured escape added after
   them; the pre-fix red now 23 of 33 rows; the first CATCH resting on the pre-fix build, not a kill table; THE CLAIM
   UNDER TEST quoting the pre-fix file).  Its AST, docstring excluded, is identical to HEAD's.
+  *[2026-10-20, records: the CATCHES list was not only the 27-row instrument's -- its M11 line names `isr 28 rd val`, row 28.]*
 * `OUTSTANDING_BUGS.md` -- the `ip30abortkill` entry's "28 ROWS ... PRE-FIX owed ... pass 2 owed" corrected in place
   (pass 2 `panel_20260917_215210`, 2026-09-17; F2 and kill tables 3-5, 2026-09-18), and a `#566` section.
 * `tools/pipeline/ledger.json` -- `wiringcliff`'s state note and this round's seat entries, Fable's two stages as HELD
```

### 3c. `fableheldform` -- the CHANGELOG and bug-file hunks (B1-B3, and the B5/B6 filing text); the ledger hunks are
listed below rather than inlined (each is one long JSON line)
```diff
diff --git a/CHANGELOG.md b/CHANGELOG.md
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -107,3 +107,3 @@
 **The defect** (filed by `#566`).  The owner's 2026-10-17 directive records a Fable wall as a SEAT FAILURE with a HELD
-marker and a question, never as agreement.  Seventeen `fable5` entries since 2026-10-16 recorded one in untokened prose
+marker and a question, never as agreement.  Seventeen `fable5` entries since 2026-10-16 recorded a non-answer in untokened prose
 ("NOT FIRED", "SEAT FAILURE", "HTTP 429"), and `stage_tokens.is_answer()` counts any untokened entry as an answer -- so
@@ -114,6 +114,7 @@
 **What this commit does** (records only):
-* tags fifteen walls with the HELD token, keeping each entry's prose and receipt, and `cxlaunchquotation`'s 2026-10-16
-  v2 and V3 walls with the non-answer token instead -- a later pass superseded each and Fable answered that one (V4,
+* tags fifteen non-answers (seven walls, eight passes Fable was not fired on) with the HELD token, keeping each entry's
+  prose and receipt, and `cxlaunchquotation`'s 2026-10-16 v2 and V3 stalls with the non-answer token instead -- a later
+  pass superseded each and Fable answered that one (V4,
   2026-10-17); no same-day answer can clear a HELD tag on V3 under the strictly-later rule (a later-date one could), and
-  one on the v2 wall would already be cleared by V4 (Grok 4.7; GPT-6 Astra's confirm corrected `forever');
+  one on the v2 stall would already be cleared by V4 (Grok 4.7; GPT-6 Astra's confirm corrected `forever');
 * moves nine rows `closed` -> `held` -- `sgirekills`, `sgirandomcolour`, `mapledmaaddr`, `xscaleinten`,
@@ -121,3 +122,4 @@
   object as the record of the close, naming in `reopened` every commit whose subject called it closed (section L),
-  heading its state note with the warrant, and adding to its `hold_question` the packet of the pass Fable walled on;
+  heading its state note with the warrant, and adding to its `hold_question` the packet of the pass Fable walled on or
+  was not fired on;
 * adds `#565`'s two Fable stages to `wiringcliff`'s held work, with their question;
@@ -139,3 +141,4 @@
 is answered, rulings and commits proceed and closes wait.  Flags taken: the census's date cutoff missed
-`cxlaunchquotation`'s 2026-10-16 wall (Astra, GLM); `cxlaunchquotation` walled on V3 and V6 as well as V7 (all three);
+`cxlaunchquotation`'s 2026-10-16 stall (Astra, GLM); `cxlaunchquotation` did not answer V3 (it stalled) or V6 (it
+walled) as well as V7 (all three);
 my brief said `ip30abortkill` "was committed held" while that commit was still in its hook (GLM); `ppcgateimageskip`'s
@@ -149,2 +152,11 @@
 2026-10-17 roster).  `ledger.json`, `OUTSTANDING_BUGS.md`, `fable_queue.md`, `matrix.html` and this block only.
+
+*Corrected 2026-10-20, from a records check of a late Gemini (Argon) reading of the design pass: this block said
+`walled Fable entries`, `fifteen walls`, `v2 and V3 walls`, `the 2026-10-16 wall` and `walled on V3`.  Of the
+seventeen, seven are walls (HTTP 429); `cxlaunchquotation`'s v2 and V3 entries STALLED (stream watchdog, 600 s), as
+both entries say and GPT-6 Astra and Grok 4.7 said of V3; eight record a pass Fable was not fired on after an earlier
+wall that day -- and the carrier keeps a seat failure and a seat deliberately not fired apart.  The ledger's own counts
+give the four Fable walls of 2026-10-17 without V3: V6 at 07:17 and its 07:5x re-fire, `dashokclass` V7 (its third
+wall that morning) and `cxlaunchquotation` V7 (its fourth wall that day).  The heading keeps the commit subject's
+wording.*
 
diff --git a/OUTSTANDING_BUGS.md b/OUTSTANDING_BUGS.md
--- a/OUTSTANDING_BUGS.md
+++ b/OUTSTANDING_BUGS.md
@@ -25012,7 +25012,8 @@
 * **`fableheldform` (MED) HELD for fable5** -- the conversion is done.  Under the owner's 2026-10-17 directive a Fable
-  wall is a SEAT FAILURE recorded as a HELD marker with a question, never agreement; seventeen entries had recorded one
-  in untokened prose, which `stage_tokens.is_answer()` counts as an answer.  Fifteen now carry the HELD token (prose and
-  receipt kept); `cxlaunchquotation`'s 2026-10-16 v2 wall and its V3 wall carry the non-answer token instead, because a
+  wall is a SEAT FAILURE recorded as a HELD marker with a question, never agreement; seventeen entries had recorded a
+  non-answer in untokened prose, which `stage_tokens.is_answer()` counts as an answer.  Fifteen (seven walls, eight
+  passes Fable was not fired on) now carry the HELD token (prose and receipt kept); `cxlaunchquotation`'s 2026-10-16 v2
+  stall and its V3 stall carry the non-answer token instead, because a
   later pass superseded each and Fable answered that one (V4, 2026-10-17).  No same-day answer can clear a HELD tag on V3
-  under the strictly-later discharge rule (a later-date one could), and one on the v2 wall would already be cleared
+  under the strictly-later discharge rule (a later-date one could), and one on the v2 stall would already be cleared
   by V4 (Grok 4.7, corrected by GPT-6 Astra's confirm).  Design pass 1 (`regress/artifacts/fableheldform/
@@ -25022,7 +25023,9 @@
   `ppcrldimimask`, `ppcrlwimiwidth`, `ppcgateimageskip`, `cxlaunchquotation`, `dashokclass`.  Each was shut on 2026-10-17
-  or 2026-10-18 while its review stage (and `sgirekills`' research stage) held a Fable wall written as an untokened
-  note; a row may not close while a stage awaits a seat (`check_stage_panels.py`, CLOSED-WHILE-HELD), so with the token
+  or 2026-10-18 while its review stage (and `sgirekills`' research stage) held a Fable wall, or a pass Fable was not
+  fired on, written as an untokened note; a row may not close while a stage awaits a seat (`check_stage_panels.py`,
+  CLOSED-WHILE-HELD), so with the token
   in place each is held until Fable answers.  Each keeps its closure object (the record of that close), names in
   `reopened` every commit whose subject called it closed (section L), heads its state note with the warrant, and adds to
-  its `hold_question` the packet of the pass Fable walled on.  GPT-6 Astra's confirm on `ip30abortkill` earlier the same
+  its `hold_question` the packet of the pass Fable walled on or was not fired on.  GPT-6 Astra's confirm on
+  `ip30abortkill` earlier the same
   afternoon is the precedent.  **The owner question the panel named** -- may a row close while its research or review
@@ -25039,2 +25042,8 @@
   of the history when a round touches it (no sweep).
+* **Corrected 2026-10-20** (a records check of a late Gemini (Argon) reading of the design pass): this section said
+  `walled Fable entries`, `v2 wall`, `V3 wall` and `held a Fable wall` throughout.  Seven of the seventeen are walls;
+  `cxlaunchquotation`'s v2 and V3 entries STALLED (stream watchdog), as both entries say; eight record a pass Fable
+  was not fired on after an earlier wall that day.  `untokenedanswers` gains two measured consequences -- an untokened
+  non-answer also DISCHARGES a live hold (`sgirekills`' assess stage), and `fableheldform`'s own review stage reds
+  section H when Fable's answer lands -- and a keyword-free option for its forward-only check.
 
```
Ledger hunks (fhfp1 `edits.diff`): 
* `@@ -44499,4 +44499,4 @@` field `state_note`: ..."state_note": "[2026-10-18, REOPENED -> held for fable5 (fableheldform)] Closed on 2026-10-18 (d9990129) while its review stage (its closure check) he...
* `@@ -44726,4 +44726,4 @@` field `state_note`: ..."state_note": "[2026-10-18, REOPENED -> held for fable5 (fableheldform)] Closed on 2026-10-18 (0d5f7cfc) while its review stage (its closure check) he...
* `@@ -47645,4 +47645,4 @@` field `state_note`: ..."state_note": "[2026-10-18, REOPENED -> held for fable5 (fableheldform)] Closed on 2026-10-18 (22c278cd) while its review stage (the #527 closure chec...
* `@@ -47880,4 +47880,4 @@` field `state_note`: ..."state_note": "[2026-10-18, REOPENED -> held for fable5 (fableheldform)] Closed on 2026-10-18 (22c278cd) while its review stage (the #527 closure chec...
* `@@ -48401,3 +48401,3 @@` field `state_note`: ..."state_note": "[2026-10-18, REOPENED -> held for fable5 (fableheldform)] Closed on 2026-10-18 (22c278cd) while its review stage (the #527 closure chec...
* `@@ -48487,3 +48487,3 @@` field `reopened`: ..."reopened": "2036a3d5 22c278cd -- each subject called this row closed; REOPENED to held on 2026-10-18 by fableheldform: the close came while its revie...
* `@@ -64536,4 +64536,4 @@` field `state_note`: ..."state_note": "[2026-10-18, HELD for fable5 -- the conversion is done] The records commit tokened the 17 untokened Fable non-answers the census found ...
* `@@ -64545,3 +64545,3 @@` field `note`: ..."note": "fableheldform DESIGN pass 1: option A -- GPT-6 Astra: tag each of the walls in place, move the nine closed rows to held, keep the historical ...
* `@@ -64561,3 +64561,3 @@` field `note`: ..."note": "fableheldform DESIGN pass 1, packet-fed: option A -- GLM 5.3: tagging the walls is the directive's own instruction under every reading, prefi...
* `@@ -64627,3 +64627,3 @@` field `state_note`: ..."state_note": "filed 2026-10-18 by fableheldform -- from broader keyword reconnaissance motivated by GLM 5.3's finding on its design pass; GLM's own s...

## 4. Questions

**Q1 -- WHICH OF MY DISPOSITIONS IS WRONG?**  I accepted the checker's reading on all 21 items (A0-A6, B0-B7,
C0-C4).  That is a suspicious unanimity; name the ones you would overturn or grade differently (L4 vs FILE vs REFUTED vs
OVERTAKEN), with the reason.  For an L4, say whether the proposed replacement text is itself true -- a correction is not
safer than the thing it corrects.

**Q2 -- B5 (`sgirekills`).**  FILE into `untokenedanswers` (wait for its owner ruling), or TOKEN notes [70]/[71] now with
the non-answer marker, as `6c2840d7` tokened seventeen Fable walls?  Tokening makes section H refuse the row's future
re-close until kimi and opus5 answer or are recorded otherwise.  Which is right, and is either a decision the OWNER must
make?

**Q3 -- A3's `src/` comment.**  Leave `src/cpus/cpu_ppc_instr.c:2470`'s matching sentence for the next PowerPC round (that
round is owner-blocked as of 2026-10-09), or include it here and accept a source commit (and its pass-2 receipt)?

**Q4 -- the docstring-block form (C2).**  Is correcting nine sentences by ONE dated addendum block, rather than in place,
honest enough -- does a reader of the printed row notes (W6/W7 print in every gate-14 log) still see the wrong text?

**Q5 -- WHAT DID THE CHECKERS MISS?**  Anything in Argon's three answers that no disposition above covers.

If, while verifying a claim, you found something ELSE -- say so.

## 5. Answer format
Verdict line first: `VERDICT: ADOPT | ADOPT WITH CHANGES | DO NOT ADOPT -- <one line>`, then Q1-Q5, each with its own
one-line answer first.  Cite file and line at HEAD for every claim, or say it is from this packet.  Say what you did not check.
