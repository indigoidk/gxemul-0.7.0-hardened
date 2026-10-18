# #527's closure unit, REVISED after the closure check -- CONFIRM

**Please do not simply ratify.**  READ-ONLY.  The closure check: your answer `codex_close527.txt` (4 flags) and Grok 4.7's `grok_close527.txt` (1 flag), both in `regress/artifacts/ppcrlwimiwidth/close_20261018/`.  All five were taken.  ONE DISAGREEMENT, settled by reading: Grok found nothing owed, on Fable's 2026-09-12 ruling (`not owed before commit ... file it if not taken`); you found the residuals carried, on the 2026-10-02 disposition (`regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md:65-70`).  Both hold: Fable said FILE them and the later record made `ppcrldimimask` their carrier, so they move to a new LOW carrier row and both HIGH rows close.  Your flag 4 (the REGRESS queue form): the unit adds a held regress entry to each closed row besides the hold_question, and section I passes on the built ledger (below).

## 1. The changed records, as built from HEAD's blobs

### `ppcrlwimiwidth` -> closed
* closure.note: CLOSED by its closure-records commit (2026-10-18): #527 (7e39a49e, 2026-09-12) made X(rlwimi) rotate the 32-bit word at 32-bit width and write a wrapping mask's high word, as Book I's RTL does.  Detector: regress/ppc_rlwimi_probe.py, 28 rows, wired into gate 13 (gate_ppc.sh, pin 28; PASS 110 checks at the time, regress/artifacts/ppcrlwimiwidth/gate_ppc_20260912.log).  Kill table 3 (regress/artifacts/ppcrlwimiwidth/killtable3_20260912/SCORES.txt): the fix 28/28, the pre-fix HEAD leg 14/28, the identity body 12/28, all six R_ mutants killed (the joint table: 17 legs, zero escapes).  The repair chain CLOSED on the §F2 adjudication pass by Fable 5.1's ruling (regress/artifacts/xscaleinten/fable_adjudication_20260912.md: zero floor breaches, denominator named).  #527's five residuals, which the 2026-10-02 disposition made `ppcrldimimask`'s to carry, move to `ppc527residual` (LOW) in this commit.
* hold_question: REGRESS (held 2026-10-18 at the #527 closure): do regress/ppc_rlwimi_probe.py and regress/ppc_rldimi_probe.py still score 28/28 and 29/29 with CONTROL=OK on a build of HEAD, and 14/28 and 17/29 on a build of 7e39a49e's parent eb26590b -- kill table 3's BASE and HEAD legs (killtable3_20260912/SCORES.txt)?  eb26590b (#526) changed no PowerPC source, so its cpu_ppc_instr.c is the pre-#527 file table 3's HEAD leg measured.
* state_note head: [2026-10-18, CLOSED] The closure-records commit closed the row on Fable 5.1's 2026-09-12 ruling; REGRESS is held for the flagship (hold_question).
* NOTE, the sentence and its new bracket: ...manifest.py apply).  ALL UNMEASURED.  OWED: run both, re-table against frozen copies (rldimi M_NOCIRC by name), gate negative controls. *** [2026-10-18, at the #527 closure (Grok 4.7): DONE before #527 committed -- kill table 3 (killtable3_20260912/), the gate log (gate_ppc_20260912.log, PASS 110 checks) and the eleven gate negative controls (gate_negctl_20260912.out).  History, not open debt.]

FILED 2026-09-10 from the [[ppcrldiclzero]] witness's sibling audit.  M...
* entries added: review/codex; review/grok; review/glm; review/fable5; regress/fable5

### `ppcrldimimask` -> closed
* closure.note: CLOSED by its closure-records commit (2026-10-18): #527 (7e39a49e, 2026-09-12) stopped X(rldimi)'s rotate loop from consuming its own shift count -- the post-decrement had left sh == -1, so every insert mask was built to bit 63 -- and made the mask walk circular.  Detector: regress/ppc_rldimi_probe.py, 29 rows, wired into gate 13 (gate_ppc.sh, pin 29; PASS 110 checks at the time, regress/artifacts/ppcrlwimiwidth/gate_ppc_20260912.log).  Kill table 3 (regress/artifacts/ppcrlwimiwidth/killtable3_20260912/SCORES.txt): the fix 29/29, the pre-fix HEAD leg 17/29, the identity body 13/29, all nine D_ mutants killed (the joint table: 17 legs, zero escapes).  The repair chain CLOSED on the §F2 adjudication pass by Fable 5.1's ruling (regress/artifacts/xscaleinten/fable_adjudication_20260912.md: zero floor breaches, denominator named).  This row CARRIED #527's five residuals by the 2026-10-02 disposition (regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md: 'the carrier owes its recorded work whenever its round runs'); they move to `ppc527residual` (LOW) in this commit, so no named work closes with the row.
* hold_question: REGRESS (held 2026-10-18 at the #527 closure): do regress/ppc_rlwimi_probe.py and regress/ppc_rldimi_probe.py still score 28/28 and 29/29 with CONTROL=OK on a build of HEAD, and 14/28 and 17/29 on a build of 7e39a49e's parent eb26590b -- kill table 3's BASE and HEAD legs (killtable3_20260912/SCORES.txt)?  eb26590b (#526) changed no PowerPC source, so its cpu_ppc_instr.c is the pre-#527 file table 3's HEAD leg measured.
* state_note head: [2026-10-18, CLOSED] The closure-records commit closed the row on Fable 5.1's 2026-09-12 ruling; REGRESS is held for the flagship (hold_question).
* TITLE now: cpu_ppc_instr.c X(rldimi): the rotate loop's post-decrement leaves sh == -1, so the insert mask always runs to bit 63 instead of 63-SH -- the instruction OVERWRITES the 64-SH destination bits the architecture requires it to PRESERVE, for every SH != 0 [CORRECTED 2026-10-18 at the #527 closure (GPT-6 Astra): the bit counts are wrong -- for a non-wrapping mask the defect overwrote the LOW SH bits that must survive, and for a wrapping mask it omitted the required insertion into positions 0..63-SH (OUTSTANDING_BUGS.md, `ppcrldimimask` DESIGNED 2026-09-10).]
* NOTE, the sentence and its new bracket: ...manifest.py apply).  ALL UNMEASURED.  OWED: run both, re-table against frozen copies (rldimi M_NOCIRC by name), gate negative controls. *** [2026-10-18, at the #527 closure (Grok 4.7): DONE before #527 committed -- kill table 3 (killtable3_20260912/), the gate log (gate_ppc_20260912.log, PASS 110 checks) and the eleven gate negative controls (gate_negctl_20260912.out).  History, not open debt.]

FILED 2026-09-10 from the [[ppcrldiclzero]] witness's sibling audit.  M...
* entries added: review/codex; review/grok; review/glm; review/fable5; regress/fable5

### `ppcgateimageskip` -> closed
* closure.note: CLOSED 2026-10-18 as DISCHARGED, on #527's closure check (GPT-6 Astra): every bareppc-only detector in gate_ppc.sh now runs BEFORE `need_file "$IMAGES/netbsd401-macppc-GENERIC"` -- the rlwimi and rldimi blocks, placed there 'ON PURPOSE' by #527 (7e39a49e), and the rldicl block by #565 (8d038908) -- so a missing image no longer turns their coverage into a SKIP.  The sections after need_file boot NetBSD and need the image by construction.  Gate 13 on the current tree: PASS 140 (regress/artifacts/ppcrldiclzero/gatewire_20261018/gate13/).
* hold_question: REGRESS (held 2026-10-18 at the ppcgateimageskip closure): with $IMAGES/netbsd401-macppc-GENERIC absent, does gate 13 still run and score the rlwimi, rldimi and rldicl blocks before it reaches need_file -- so that a red row in those blocks reports FAIL rather than a SKIP?
* state_note head: [2026-10-18, CLOSED as discharged] REGRESS is held for the flagship (hold_question).
* commits: 7e39a49e 8d038908 | witness: harness:regress/gate_ppc.sh -- the three bareppc blocks (python3 -u ppc_rlwimi_probe.py, ppc_rldimi_probe.py, ppc_rldicl_probe.py) precede need_file "$IMAGES/netbsd401-macppc-GENERIC"; gate 13 PASS 140 (regress/artifacts/ppcrldiclzero/gatewire_20261018/gate13/)
* entries added: review/codex; review/grok; review/glm; review/fable5; review/opus5; review/agy; review/kimi; review/deepseek; review/minimax; regress/fable5

### NEW ROW `ppc527residual` (sev LOW, open)
* title: #527's five residuals, moved here from `ppcrldimimask` at its closure: the SH=63/MB=1 full-mask rldimi row, the wrapping stale-rS alias row, the Rc=1-only insertion skip, CENSUS_SHRINK and R_NOGUARD -- coverage debt and named measurements on regress/ppc_rlwimi_probe.py and ppc_rldimi_probe.py, none a floor breach
* state_note: filed 2026-10-18 by #527's closure-records commit.  Fable 5.1's 2026-09-12 closing ruling (regress/artifacts/xscaleinten/fable_adjudication_20260912.md) graded each clause (e) or a named measurement, not owed before #527's commit, and asked that they be FILED; the 2026-10-02 disposition (regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md, flags #10-#14) then made `ppcrldimimask` their carrier -- 'the carrier owes its recorded work whenever its round runs'.  This row carries them now, so that row could close (GPT-6 Astra, #527's closure check).  The five, specified in OUTSTANDING_BUGS.md under `ppcrldimimask` -- SHIPPED: (1) ADD a full-mask patterned rldimi row at SH=63, MB=1 from 0xDEADBEEFCAFEF00D, want 0xEF56DF77E57F7806 (costs a table 4 and pin 29 -> 30); (2) an alias row at SH=40, MB=40 for a stale rS re-read on WRAPPING masks (codex's arithmetic, not built); (3) an insertion skipped only when Rc=1 survives both probes (both CONTRACTs disclose it); (4) CENSUS_SHRINK -- one run of the fixed build with a shortened census, the literal pins' unique channel; (5) R_NOGUARD -- delete rlwimi's `sh ?` guard, predicted 28/28, load-bearing for definedness since the fix narrowed tmp (Fable).

### `wiringcliff` commits: 8404520 eec0f4a -> 8404520 eec0f4a 8d038908

## 2. OUTSTANDING_BUGS.md

```diff
@@ -128,2 +128,4 @@
 > image that may be absent, and the failure renders as SKIP rather than red.
+> *[2026-10-18: CLOSED as discharged -- the rlwimi and rldimi blocks (`#527`) and the rldicl block (`#565`) run
+> BEFORE `need_file`, so a missing image no longer skips them (GPT-6 Astra, `#527`'s closure check).]*
 >
@@ -19623,2 +19625,7 @@ Filed, each ruled clause (e) or a named measurement, NOT owed:
 
+*[2026-10-18, `#527`'s closure-records commit: both rows CLOSED.  The 2026-10-02 disposition had made `ppcrldimimask`
+the carrier of these five (`regress/artifacts/idlessaudit_20261002/AGY_FLAGS_DISPOSITION.md`), so they move to
+`ppc527residual` (LOW, open) rather than close with it -- GPT-6 Astra, the closure check.  "none owed" above means
+none owed before `#527` committed.]*
+
 ### `mapledmaaddr` -- SHIPPED as `#528` (2026-09-12); residuals FILED, none owed
@@ -24932 +24939,11 @@ Fable 5.1, GPT-6 Astra, Grok 4.7).  Each row's ledger `state_note` carries its s
   is Grok 4.7's, filed by the author.
+
+### 2026-10-18 -- `#527`'s rows close (`ppcrlwimiwidth`, `ppcrldimimask`); their residuals move to `ppc527residual`; `ppcgateimageskip` closes as discharged
+
+* **`ppcrlwimiwidth`, `ppcrldimimask` CLOSED** -- `#527` (`7e39a49e`, 2026-09-12) shipped both fixes with 28- and 29-row
+  detectors in gate 13; kill table 3 zero escapes; Fable 5.1 closed the chain on 2026-09-12.  REGRESS held for the
+  flagship (each row's hold_question).
+* **`ppc527residual` (LOW, open)** -- #527's five residuals (the SH=63/MB=1 rldimi row, the wrapping stale-rS alias row,
+  the Rc=1-only insertion skip, `CENSUS_SHRINK`, `R_NOGUARD`), moved here from `ppcrldimimask`, which the 2026-10-02
+  disposition had made their carrier.  Coverage debt and named measurements; none a floor breach.
+* **`ppcgateimageskip` CLOSED as discharged** -- the rlwimi, rldimi and rldicl blocks run before `need_file` in gate 13.
```

## 3. The closure check's entries (on each closed row)

* review/codex: #527 CLOSURE check: 4 flags -- GPT-6 Astra: the five residuals had a carrier, `ppcrldimimask` (the 2026-10-02 disposition: 'the carrier owes its recorded work whenever its round runs'), so the rows could not close as drafted -- moved to `ppc527residual`; the rldimi title's bit counts (corrected in place); `ppcgateimageskip` stale -- the #527 and #565 blocks run before need_file (closed as discharged); the REGRESS hold needs its queued form (the held regress entry and hold_question this commit adds).
* review/grok: #527 CLOSURE check: 1 flag -- Grok 4.7: the drafted '(17 legs, zero escapes)' is the joint table's count, not a per-family one (reworded).  It found nothing else owed and every drafted fact true -- the commit and its parent, both fixes, the pins, the gate log, table 3's BASE/HEAD/identity scores, and eb26590b changing no PowerPC source -- and named the notes' 'ALL UNMEASURED. OWED' as stale history (annotated).  On the residuals it read Fable's 09-12 'not owed before commit ... file it if not taken'; the 10-02 carrier record, which it did not weigh, decided the move.
* review/glm: #527 CLOSURE check: DELIBERATELY NOT FIRED -- a records question that needs the rows' files opened, and GLM is packet-fed.
* review/fable5: #527 CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 2026-10-18).

## 4. The CHANGELOG block (`{CONFIRM}` is filled from your answer)

```
# Records, 2026-10-18: `ppcrlwimiwidth` and `ppcrldimimask` close -- `#527` finished on 2026-09-12 and was left in work; its five residuals move to `ppc527residual`; `ppcgateimageskip` closes as discharged

`#527` committed both PowerPC fixes as `7e39a49e` on 2026-09-12 -- `rlwimi` rotates the 32-bit word at 32-bit width and
writes a wrapping mask's high word; `rldimi`'s rotate loop no longer consumes its own shift count, and its mask walk is
circular -- with `regress/ppc_rlwimi_probe.py` (28 rows) and `regress/ppc_rldimi_probe.py` (29 rows) pinned in gate 13
(PASS 110 checks then, `regress/artifacts/ppcrlwimiwidth/gate_ppc_20260912.log`).  Kill table 3: the fixes 28/28 and
29/29, the pre-fix HEAD legs 14/28 and 17/29, the identity bodies 12/28 and 13/29, all fifteen mutants killed (17 legs,
zero escapes; `killtable3_20260912/`).  Fable 5.1's ruling closed the chain (`regress/artifacts/xscaleinten/
fable_adjudication_20260912.md`).  Both ledger rows were nevertheless still `in work` five weeks later.  This commit:

* CLOSES both rows, each with REGRESS held for the flagship: its hold_question asks whether both probes still score
  28/28 and 29/29 on HEAD, and 14/28 and 17/29 on `7e39a49e`'s parent `eb26590b` -- which changed no PowerPC source, so
  it carries the file table 3's HEAD leg measured;
* MOVES #527's five residuals to a new carrier, `ppc527residual` (LOW, open).  Fable's ruling graded them clause (e) or
  named measurements and asked that they be filed; the 2026-10-02 disposition (`regress/artifacts/idlessaudit_20261002/
  AGY_FLAGS_DISPOSITION.md`) made `ppcrldimimask` their carrier, and a carrier "owes its recorded work whenever its
  round runs" -- so closing it bare would have dropped them (GPT-6 Astra's closure check; Grok 4.7 read Fable's ruling
  alone and found nothing owed);
* CORRECTS in place `ppcrldimimask`'s title, whose bit counts were wrong (the defect overwrote the LOW SH bits for a
  non-wrapping mask and omitted the insertion for a wrapping one), and both notes' stale "ALL UNMEASURED.  OWED" (done
  before `#527` committed: table 3, the gate log, the eleven negative controls -- Grok 4.7);
* CLOSES `ppcgateimageskip` as discharged: the rlwimi and rldimi blocks (`#527`) and the rldicl block (`#565`) all run
  before `need_file`, so a missing NetBSD image no longer turns their coverage into a SKIP (GPT-6 Astra); its REGRESS
  question asks for the image-absent run;
* adds `#565`'s `8d038908` to `wiringcliff`'s commits field (section L had graded its absence SOFT).

Closure check (`regress/artifacts/ppcrlwimiwidth/close_20261018/`): GPT-6 Astra 4 flags and Grok 4.7 1, all taken;
{CONFIRM}  GLM 5.3 deliberately not fired (a records question needing the files; GLM is packet-fed); Fable 5.1 NOT FIRED
(held by the owner's 2026-10-17 directive).  Ledger, bug file, matrix and this block only.
```

## 5. Pretests on the built ledger

* section I (`check_fable_queue.py`): `FABLE_QUEUE_PASS ... 0 closed rows owing a regress review`
* section H (`check_stage_panels.py`): `STAGE_PANELS_PASS` -- after recording the five seats outside the owner's 2026-10-17 roster as NOT FIRED on `ppcgateimageskip`, whose review stage this unit opens (it FAILED at 4/9 without them)
* section L (`check_commit_attribution.py`): `ATTRIBUTION_PASS 0 hard`; the witness check and bug-file sync pass

## 6. Questions

**Q1.**  Is each of the five closure-check flags handled correctly?  **Q2.**  Is any changed sentence above false or overstated against its receipt?  **Q3.**  Is anything still owed before this unit commits?

**Format:** open with the token `ASTRA_CLOSE527B_20261018`, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line starting `FLAG:`.  Facts and flags only.
