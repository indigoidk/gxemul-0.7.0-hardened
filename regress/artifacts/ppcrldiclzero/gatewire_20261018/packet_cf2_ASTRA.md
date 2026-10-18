# #565 -- MICRO-CONFIRM: your four confirm flags, fixed

**Please do not simply ratify.**  READ-ONLY.  Your confirm answer is `regress/artifacts/ppcrldiclzero/gatewire_20261018/codex_rldiclcf.txt` (4 flags).  Each was verified at source before the edit -- `eec0f4a3` moves this probe 2026-09-20 -> 2026-09-27; `main.c` exits on the failed machine lookup; the 04:57 wall was 2026-10-18; the split note had no FILE ruling.  The same wrong date sat in two entries committed earlier today, corrected in place here as well.  The probe and the gate changed in COMMENTS only, and every measurement was then RE-RUN on the exact staged files (section 3).

## 1. Product and harness files (pre-fix -> staged)

```diff
--- a/regress/ppc_rldicl_probe.py
+++ b/regress/ppc_rldicl_probe.py
@@ -76,11 +76,11 @@ directly out of the destination register.  Five controls (this said `Four' until
                 disassembler (cpu_ppc.c, a DIFFERENT code path from the execute
                 handler in cpu_ppc_instr.c) and compared against the operands the
                 encoder intended.  Guards the hand-assembled-encoding trap.
-                [#565, 2026-10-18: NOT every word.  Every session disassembles what it
-                places, but only the control and census sessions' 196 words (6 + 190)
-                are COMPARED; the bogus-machine (1, never reaches a machine), 32-bit (2),
-                vacuity (2) and candidate-row (3) sessions' results are not (#565 pass 2
-                and F2: GPT-6 Astra, Grok 4.7, GLM 5.3).]
+                [#565, 2026-10-18: NOT every word.  Only the control and census sessions'
+                196 words (6 + 190) are COMPARED.  The 32-bit (2), vacuity (2) and
+                candidate-row (3) sessions' seven are disassembled and not compared, and
+                the bogus-machine session's one is never placed -- its machine does not
+                exist (#565 pass 2, F2 and confirm: GPT-6 Astra, Grok 4.7, GLM 5.3).]
   rldicr        the correctly-written sibling, same rotate-and-mask shape, same
                 session -- attributes the failure to X(rldicl) rather than to the
                 encoding, the machine, the rotate or this program.
```

```diff
--- a/regress/gate_ppc.sh
+++ b/regress/gate_ppc.sh
@@ -160,9 +160,9 @@ else
 fi
 
 # ---- ppcrldiclzero (#522) + #565: X(rldicl) wrote ZERO on every execution -- its 24-row detector --------
-# Shipped EXEMPT with e777ff06 (2026-09-10) and re-dated twice by owner ruling (2026-09-24 with the
-# other nine, then 04f3e7c0 on 2026-10-09) because no block here scored it; #565 discharges that
-# exemption.  BEFORE the NetBSD prerequisite for the reason the rlwimi block gives: `-E bareppc -M 64`
+# Shipped EXEMPT with e777ff06 (2026-09-10) and re-dated three times by owner ruling (2026-09-18 with
+# ten others, eec0f4a3; 2026-09-24 with nine others; 04f3e7c0 on 2026-10-09) because no block here
+# scored it; #565 discharges that exemption.  BEFORE the NetBSD prerequisite for the reason the rlwimi block gives: `-E bareppc -M 64`
 # needs no image, so a red row is recorded first.  A stalled guest cannot hang the gate: the probe's
 # own subprocess backstops (90 s; 60 s for the bogus-machine and 32-bit sessions) turn it into
 # failing rows.  The probe prints no RESULT/CONTROL protocol, so it is scored as gate_arm.sh scores
```

```diff
--- a/tools/pipeline/check_probe_wiring.py (staged)
+++ b/tools/pipeline/check_probe_wiring.py (staged)
@@ -1703,7 +1703,7 @@ MANIFEST = {
     #  red and SCORE counts pinned; its EXEMPT entry is DISCHARGED below.  "EXEMPT below rather than wired" above is
     #  historical.
     "ppc_rldicl_probe.py":
-        (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word [#565: COMPARED for the control and census sessions' 196 words only -- the other sessions' words are disassembled, not compared].  BASE 24/24, whole-file pre-fix leg 16/24 (clause (a); 'null medium' until 2026-10-09, 7n-1), EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),
+        (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word [#565: COMPARED for the control and census sessions' 196 words only -- seven more are disassembled and not compared, and the bogus-machine session's one is never placed].  BASE 24/24, whole-file pre-fix leg 16/24 (clause (a); 'null medium' until 2026-10-09, 7n-1), EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),
 
     #  The frozen copies are the instruments as-run.  t1 is the 19-row form that pass 2
     #  escaped TWICE; t2 is the 24-row closure; t0 is an apparatus failure kept on purpose.
@@ -3173,7 +3173,8 @@ EXEMPT = {
     #  Deleted in the SAME edit as the wiring, for the same reason.
     #  ppc_rldicl_probe.py's exemption is DISCHARGED, 2026-10-18 (#565) -- wired into gate_ppc.sh beside the
     #  rlwimi/rldimi blocks on the same -E bareppc -M 64, every row scored by name.  It was dated 2026-10-22,
-    #  after two re-dates by owner ruling, and would have refused every commit from 2026-10-23 (`d < today').
+    #  after three re-dates by owner ruling (2026-09-18 in eec0f4a3, 2026-09-24, 2026-10-09), and would have
+    #  refused every commit from 2026-10-23 (`d < today').
     #  Deleted in the SAME edit as the wiring, for the same reason.
     #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
```

## 2. Records (final text of every changed sentence)

### CHANGELOG paragraphs

**The cliff.**  Section R (`tools/pipeline/check_probe_wiring.py`) held `#522`'s detector for `rldicl` writing zero,
`ppc_rldicl_probe.py`, in its EXEMPT table, dated 2026-10-22 after three re-dates by owner ruling (2026-09-18 in
`eec0f4a3`, 2026-09-24, then `04f3e7c0` on 2026-10-09).  With `d < today` it would have refused every commit from 2026-10-23.  Witness `harness:` --
the round's subject is the test apparatus: no `regress/gate_*.sh` named the probe at HEAD `69253c3c`, and section R
reported it exempt.

**The records the new pin exposed, corrected** -- each beside the sentence it corrects, in the probe unless named:
* the docstring's M_NOMASK `16/19` is the 19-row figure (`pass2_20260910/opus_nomask.log:3`); on today's 24 rows it is
  19/24 (`killtable_20260910/t2/probe_M_NOMASK.raw:30`) -- section U's flag;
* `**THIS FILE HAS 19 ROWS, NOT 24**` qualified on its own line (24 since pass 2), and the second verbatim copy of `WHY
  THE SIBLING ROWS ARE NOT HERE` -- present twice since `e777ff06` -- deleted;
* the VACUITY comment's `could never fail, whatever the handler does`: `vacuous cell` is red under M_NOMASK (GPT-6 Astra),
  and under M_NAIVE, M_MASKEND and M_NOAND too, though it shares `naive fix wrong`'s CARRIED-NOT-COUNTED label (Grok 4.7);
* `every placed word` is disassembler-checked: only the control and census sessions' 196 words are COMPARED -- the
  32-bit, vacuity and candidate-row sessions' seven are disassembled and not compared, and the bogus-machine session's
  one is never placed (GPT-6 Astra, Grok 4.7, GLM 5.3) -- in the docstring, the printed note and the MANIFEST;
* `Four controls:` lists five (NL6), and the MANIFEST's t2 frozen copy is byte-identical to the shipped probe only AS
  SHIPPED AT `e777ff06` (NL7) -- both upheld by Fable 5.1 on 2026-10-16 as L4s to land when their file is next touched.

### OUTSTANDING_BUGS.md section

### 2026-10-18 -- `#565`: `ppc_rldicl_probe.py` wired into gate 13 (`wiringcliff` stays open); `nullmediumlegs`' rldicl half measured; one row filed

* **`wiringcliff` (MED, in work)** -- `#565` wired `regress/ppc_rldicl_probe.py` into gate 13 and deleted its 2026-10-22
  exemption (30 checks; gate 13 PASS 140).  Next due: `alpha_tbi_probe.py` 2026-10-22 (refuses every commit from 10-23;
  the other session's Alpha area -- a gate block or an owner re-date), then the three `lca_*` probes 10-23 / 10-26 /
  10-27, `ip30_abort_probe.py` 10-30 and the four `wdc_*` probes 11-05 .. 12-03.
* **`nullmediumlegs` (LOW, open)** -- the rldicl half MEASURED with the identity body (11 of gate 13's 30 rldicl checks
  red); the `alpha_tbi_probe.py` half is still owed.
* **`ppcprobescorestale` (LOW, open)** -- part 1 done by `#565`; the flagship's 2026-09-11 demotion of `naive fix wrong`
  to a print is still owed (it moves gate 13's literals 24 -> 23).
* **`ppcrldiclbanner` (LOW, open)** -- the probe calls itself a WITNESS (docstring line 2 and its runtime banner; section
  R's advisory SELFLABEL note), its usage string names `ppc_rldicl_witness.py`, and `vacuous cell`'s split note makes a
  red log read `GREEN on a FAIL`.  Cosmetic: the label and the usage string FILED by all three seats; the split note
  is Grok 4.7's, filed by the author.


### ledger: this round's changed entries

* design/glm: #565 PASS 1 (the design brief): 7 flags -- GLM 5.3, packet-fed: the same truncated transcript; `re-dated once' undercounts (taken as `twice', and it was THREE times -- 2026-09-18 in eec0f4a3, 2026-09-24, 2026-10-09 -- as GPT-6 Astra's confirm found); no duplicated-row control (V7 added) and no stated scope for a stalled probe (the probe's own 90 s / 60 s backstops, now in the block comment); three premises not settle-able from the packet -- section R's wiring test, the mk48 model, the same-commit companions -- each settled by a measurement or a reading.
* design/fable5: #565 PASS 1 (the design brief): NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 2026-10-18).
* review/fable5: #565 PASS 2 and the F2 shared-findings pass: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled again, HTTP 429, at 04:57 on 2026-10-18).
* review/codex: #565 F2 (the shared-findings pass): 3 flags, all on my own repair wording -- GPT-6 Astra: `not re-read' is false (the sessions disassemble what they place; only the control and census 196 words are COMPARED); `an absent binary reds the sentinel' holds for the block's scoring text, not gate 13 (need_exec SKIPs first); nullmedium.sh's header still said `comment-only'.  All corrected.  It UPHELD my D1 (keep `naive fix wrong' in the 24) on #522 pass 2's retention reason -- but the flagship's later ruling (2026-09-11, `demote it to a print') governs; D1 was withdrawn.
* review/grok: #565 F2 (the shared-findings pass): 5 flags -- Grok 4.7: OVERTURNED my D1 and my proposal to close `ppcprobescorestale' on the flagship's 2026-09-11 ruling (the probe note that redefined CARRIED-NOT-COUNTED was withdrawn; the row stays open with the demotion owed); `vacuous cell' carries that label and has kills (noted beside it); the unchecked disassembly is eight words in four sessions (refined by GPT-6 Astra's confirm: seven are disassembled and not compared, and the bogus-machine session's one is never placed); the CONTRACT's `any block' (gate_arm.sh pins some got= values); the t2 qualifier omitted the printed-note change.  All corrected.

### ledger: the two siblings committed earlier today

* `mapledmaaddr` entry 50 (review/fable5): mapledmaaddr CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled, HTTP 429, at 04:57 the same day).  [2026-10-18, #565's confirm (GPT-6 Astra): WRONG DATE -- that 04:57 HTTP 429 was on 2026-10-18, the day AFTER the 2026-10-17 directive, not the same day.]
* `xscaleinten` entry 21 (review/fable5): xscaleinten CLOSURE check: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled, HTTP 429, at 04:57 the same day).  [2026-10-18, #565's confirm (GPT-6 Astra): WRONG DATE -- that 04:57 HTTP 429 was on 2026-10-18, the day AFTER the 2026-10-17 directive, not the same day.]

### ledger: the new row's state_note

filed 2026-10-18 by #565 (the gate wiring of this probe).  Raised by GPT-6 Astra, Grok 4.7 and GLM 5.3 on #565's pass 2: all three seats ruled the WITNESS label and the usage string FILE, not fix (GPT-6 Astra adding the runtime banner); the split note is Grok 4.7's F2 finding, filed by the author with no seat's ruling on it.  Section R reports the first as an ADVISORY `SELFLABEL' note (check_probe_wiring.py's self_label; it fails nothing); the usage string prints only when the probe gets fewer than two arguments, which gate 13 never does; the split note is Grok 4.7's (#565 F2).  Cosmetic: no gate, kill or score rests on any of the three.  A round touching the probe's docstring -- `ppcprobescorestale''s demotion is the next one -- can close it.

## 3. Re-measured on the staged files

```
probe: 9cc0ee8453cba2fc7da0bd002512495e  regress/ppc_rldicl_probe.py
gate:  7a970b9a979dcd73da0f265abbecb847  regress/gate_ppc.sh
LEG absent  binary=/nonexistent/gxemul  probe_rc=1     0s  gate checks=1   fails=1   RED (clause c holds)
     red: [ppc_rldicl probe completed got=no]
     log tail:                ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/gxemul'|
LEG nonemu  binary=/bin/true            probe_rc=0     0s  gate checks=30  fails=22  RED (clause c holds)
     red: [ppc_rldicl row: live got=0] [ppc_rldicl row: seed holds got=0] [ppc_rldicl row: src intact got=0] [ppc_rldicl row: disasm xcheck got=0] [ppc_rldicl row: zx32 rldicl got=0] [ppc_rldicl row: zx32 rldicr got=0] [ppc_rldicl row: rot8 rldicl got=0] [ppc_rldicl row: rot8 rldicr got=0] [ppc_rldicl row: neg apparatus got=0] [ppc_rldicl row: bits32 live got=0] [ppc_rldicl row: bits32 rld bad got=0] [ppc_rldicl row: vacuous cell got=0] [ppc_rldicl row: vac neighbour got=0] [ppc_rldicl row: census wrong got=0] [ppc_rldicl row: disasm total got=0] [ppc_rldicl row: cr parsed got=0] [ppc_rldicl row: sh63 rldicl got=0] [ppc_rldicl row: sh32 rldicl got=0] [ppc_rldicl row: rc cr0 got=0] [ppc_rldicl rows green got=5] [ppc_rldicl rows red got=19] [ppc_rldicl score 24/24 got=0]
     log tail: FAILING: live, seed holds, src intact, disasm xcheck, zx32 rldicl, zx32 rldicr, rot8 rldicl, rot8 rldicr, neg apparatus, bits32 live, bits32 rld bad, vacuous cell, vac neighbour, census wrong, disasm 
NULLMEDIUM_DONE

probe frozen: 9cc0ee8453cba2fc7da0bd002512495e  (copy kept as ppc_rldicl_probe.frozen.py.txt)
gate:         7a970b9a979dcd73da0f265abbecb847  regress/gate_ppc.sh
=== LEG BASE (the clone's baseline, rebuilt by nullid_prep.sh) ===
  probe rc=0  SCORE 24/24  elapsed=0.1s  binary=/tmp/gx565id/gxemul  label=BASE
  GATE BLOCK: checks=30 fails=0
=== LEG NULL_MEDIUM ===
  probe rc=0  SCORE 16/24  elapsed=0.1s  binary=/tmp/gx565id/gxemul  label=NULL_MEDIUM
  GATE BLOCK: checks=30 fails=11 [ppc_rldicl row: zx32 rldicl got=0] [ppc_rldicl row: rot8 rldicl got=0] [ppc_rldicl row: vacuous cell got=0] [ppc_rldicl row: vac neighbour got=0] [ppc_rldicl row: census wrong got=0] [ppc_rldicl row: sh63 rldicl got=0] [ppc_rldicl row: sh32 rldicl got=0] [ppc_rldicl row: rc cr0 got=0] [ppc_rldicl rows green got=16] [ppc_rldicl rows red got=8] [ppc_rldicl score 24/24 got=0]
=== LEG RESTORED ===
  probe rc=0  SCORE 24/24  elapsed=0.1s  binary=/tmp/gx565id/gxemul  label=RESTORED
  GATE BLOCK: checks=30 fails=0
  part 1 (cmp vs SEC) = CLEAN   part 2 (binary -nt source) = FRESH
  SENTINEL CLEARED
IDENTITY_DONE

gate13 start 09:03:40 HEAD 69253c3c gate md5 7a970b9a979d probe md5 9cc0ee8453cb
gate13 rc=0 end 09:05:08
gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl: PASS (140 checks)
```

## 4. Questions

**Q1.**  Is each of your four flags fixed as you meant it?  **Q2.**  Does any fix -- or the sibling correction -- introduce a new false sentence?  **Q3.**  Do the re-run receipts support the records' numbers (11 of 30, 22 of 30, gate 13's count)?

**Format:** open with the token `ASTRA_RLDICLWIRE_CF2_20261018`, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line starting `FLAG:`.  Facts and flags only.
