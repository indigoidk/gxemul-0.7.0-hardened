# #565 -- CONFIRM: the F2 repair, two measurements made after F2, and the records drafts

**Please do not simply ratify.**  You are the confirm seat (today's pattern: GPT-6 Astra confirms before a commit).  The
tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; READ-ONLY.  `regress/gate_ppc.sh`, `regress/ppc_rldicl_probe.py` and
`tools/precommit_check.sh` in the working tree are exactly the text this commit stages; for
`tools/pipeline/check_probe_wiring.py` the staged text is the working copy MINUS other uncommitted lines (the #563 hunk
and another session's MANIFEST lines), so section 1b below is the authority for it.  The F2 packet and the three F2
answers are in `regress/artifacts/ppcrldiclzero/gatewire_20261018/` (`brief_f2_body.md`, `codex_rldiclf2.txt`,
`grok_f2.txt`, `glm_f2.txt`).

## 0. What changed after F2

* **D1 withdrawn.**  My F2 disposition kept `naive fix wrong` in SCORE and a probe note said so; the flagship ruled on
  2026-09-11 that the row be DEMOTED TO A PRINT (`regress/artifacts/heldqueue/fable_adjudication_20260911.md:177-180`),
  which the F2 packet did not carry.  Grok 4.7 overturned D1 on that ruling; the note is removed; `ppcprobescorestale`
  stays OPEN with the demotion owed (it changes the row count, so it is its own round).
* **D2 settled by measurement**: the identity body was BUILT (section 2a).
* Every F2 flag on my own repair wording is fixed (section 1).

## 1. The repair since F2 (inlined by script)

### 1a. `regress/ppc_rldicl_probe.py`
```diff
--- a/regress/ppc_rldicl_probe.py
+++ b/regress/ppc_rldicl_probe.py
@@ -37,9 +37,11 @@ measurable rather than argued'; it does not, and a pass-2 seat named it as the
 check-that-cannot-fail shape sitting inside a detector whose whole purpose is to be
 failable.  **THE M_NAIVE KILL-TABLE LEG is what makes the claim measurable.**  The row
 is CARRIED-NOT-COUNTED, the disposition already used for `vacuous cell'.
-[#565, 2026-10-18: CARRIED means it stays IN `SCORE' -- the 24 the gate pins includes it --
-and NOT COUNTED means it is credited with no kill; it never meant left out of `SCORE', which
-the code has never done (`ppcprobescorestale' read it that way).]
+[#565, 2026-10-18: of those two rows only `naive fix wrong' can never fail.  `vacuous cell'
+has kills -- it is red under M_NAIVE, M_MASKEND, M_NOAND and M_NOMASK (killtable_20260910/
+t2/SCORES.txt; Grok 4.7, #565 F2) -- see the VACUITY note below.  The flagship ruled on
+2026-09-11 that `naive fix wrong' be demoted to a print; that is owed under
+`ppcprobescorestale'.]
 
 ARCHITECTURE, read locally -- _scratchpad/ppc_pem_32and64_2005.txt:29736 (rldiclx):
         n <- sh[5] || sh[0-4]
@@ -74,9 +76,11 @@ directly out of the destination register.  Five controls (this said `Four' until
                 disassembler (cpu_ppc.c, a DIFFERENT code path from the execute
                 handler in cpu_ppc_instr.c) and compared against the operands the
                 encoder intended.  Guards the hand-assembled-encoding trap.
-                [#565, 2026-10-18: NOT every word -- the control and census sessions'
-                196 (6 + 190) are; the candidate-row session's three are not re-read,
-                its disassembly result is discarded (GPT-6 Astra, #565 pass 2).]
+                [#565, 2026-10-18: NOT every word.  Every session disassembles what it
+                places, but only the control and census sessions' 196 words (6 + 190)
+                are COMPARED; the bogus-machine (1, never reaches a machine), 32-bit (2),
+                vacuity (2) and candidate-row (3) sessions' results are not (#565 pass 2
+                and F2: GPT-6 Astra, Grok 4.7, GLM 5.3).]
   rldicr        the correctly-written sibling, same rotate-and-mask shape, same
                 session -- attributes the failure to X(rldicl) rather than to the
                 encoding, the machine, the rotate or this program.
@@ -530,7 +534,7 @@ row("census zero", census_zero, 0,
     "cells that returned EXACTLY ZERO -- want 0 after a fix")
 row("disasm total", "%d/%d" % (disasm_ok, disasm_checked),
     "%d/%d" % (disasm_checked, disasm_checked),
-    "control + census words re-read by the tree's own disassembler (not the 3 cand words)")
+    "the 196 control + census words checked against the tree's own disassembler")
 
 # ================================ WHY THE SIBLING ROWS ARE NOT HERE =============
 #
```
### 1b. `tools/pipeline/check_probe_wiring.py` (staged text, F2 -> now)
```diff
--- a/tools/pipeline/check_probe_wiring.py
+++ b/tools/pipeline/check_probe_wiring.py
@@ -1703,14 +1703,14 @@ MANIFEST = {
     #  red and SCORE counts pinned; its EXEMPT entry is DISCHARGED below.  "EXEMPT below rather than wired" above is
     #  historical.
     "ppc_rldicl_probe.py":
-        (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word [#565: of the control and census sessions' 196 words -- the candidate-row session's three are not re-read].  BASE 24/24, whole-file pre-fix leg 16/24 (clause (a); 'null medium' until 2026-10-09, 7n-1), EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),
+        (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word [#565: COMPARED for the control and census sessions' 196 words only -- the other sessions' words are disassembled, not compared].  BASE 24/24, whole-file pre-fix leg 16/24 (clause (a); 'null medium' until 2026-10-09, 7n-1), EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),
 
     #  The frozen copies are the instruments as-run.  t1 is the 19-row form that pass 2
     #  escaped TWICE; t2 is the 24-row closure; t0 is an apparatus failure kept on purpose.
     "artifacts/ppcrldiclzero/killtable_20260910/t1/ppc_rldicl_probe.frozen.py":
         (CLASS_RESEARCH, "ppcrldiclzero (#522) table 1: the as-run 19-row instrument -- pass 2 escaped it TWICE at 19/19 (a shift-decode mutant it was blind to BY CONSTRUCTION, and a CR0 mutant that is the sibling handler's own shipping token)"),
     "artifacts/ppcrldiclzero/killtable_20260910/t2/ppc_rldicl_probe.frozen.py":
-        (CLASS_RESEARCH, "ppcrldiclzero (#522) table 2: the CLOSING 24-row instrument, byte-identical to the shipped regress/ppc_rldicl_probe.py [#565: AS SHIPPED AT e777ff06 -- a05660af changed its helper oracles and #565 its comments since; NL7]"),
+        (CLASS_RESEARCH, "ppcrldiclzero (#522) table 2: the CLOSING 24-row instrument, byte-identical to the shipped regress/ppc_rldicl_probe.py [#565: AS SHIPPED AT e777ff06 -- a05660af changed its helper oracles, and #565 its comments and one printed note, since; NL7]"),
     "artifacts/ppcrldiclzero/killtable_20260910/t0_apparatus_failure/ppc_rldicl_probe.frozen.py":
         (CLASS_RESEARCH, "ppcrldiclzero (#522) table 0: an APPARATUS FAILURE preserved rather than deleted -- the driver was derived by substitution from #521 and called THAT round's mutator, which replied `unknown mutant'.  The hard-fail refused rather than measuring an unmutated tree, but the table looked HALF-HEALTHY because both mutators define BASE and answered it identically.  No number from it is cited anywhere"),
 
```
### 1c. `regress/gate_ppc.sh`
```diff
--- a/regress/gate_ppc.sh
+++ b/regress/gate_ppc.sh
@@ -172,10 +172,13 @@ fi
 # neighbour (the padded-column trap).  The rows-run line is in the form check_score_claims.py pins.
 # CONTRACT: the block TRANSMITS the probe's verdicts and re-derives none -- each row's ok/FAIL and its
 # SCORE come from one comparison in the probe's row(), so an edit there (Grok 4.7's `ok = True', GPT-6
-# Astra's `>=', #565 pass 2) lets a mutant through, as it would through any block scoring a probe's own
-# tokens.  The exit status is ignored on purpose: this probe exits 0 with failed rows (probeexitzero).
-# Floor (c), measured: an absent binary reds the sentinel check and /bin/true reds 22 of the 30
-# (regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/).
+# Astra's `>=', #565 pass 2) lets a mutant through, as it would through any block that scores only a
+# probe's ok/FAIL tokens (some gate_arm.sh blocks also pin a got= value; this one, like mk48's, does not).
+# The exit status is ignored on purpose: this probe exits 0 with failed rows (probeexitzero).
+# Floor (c), measured (regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/): an IDENTITY
+# BODY for X(rldicl) -- decode and retire, write nothing -- reds 11 of the 30 (identity/), and
+# /bin/true 22 of the 30.  An absent binary reds the sentinel check in this block's scoring text, but
+# in gate 13 need_exec turns it into a SKIP before any check.
 RLCLOG=$LOGDIR/ppc_rldicl.log
 python3 -u ppc_rldicl_probe.py "$PMAX" gate > "$RLCLOG" 2>&1 || true
 if [ "$(grep -cx 'PPC_RLDICL_PROBE_DONE' "$RLCLOG")" != 1 ]; then
```

## 2. Measured after F2

### 2a. The identity-body leg (`nullmedium/identity/IDENTITY.out`; mutator `ppcw/mutate_rldicl_null.py`, its diff `mutant.diff`)
```
identity leg  2026-10-18T13:48:09Z  HEAD 69253c3c
probe frozen: 890fab46b4f691c1522d5459b747a5fe  (copy kept as ppc_rldicl_probe.frozen.py.txt)
gate:         654bd92217f613ac125caf9d22a93add  regress/gate_ppc.sh
=== LEG BASE (the clone's baseline, rebuilt by nullid_prep.sh) ===
  probe rc=0  SCORE 24/24  elapsed=0.1s  binary=/tmp/gx565id/gxemul  label=BASE
  FAILING: 
  GATE BLOCK: checks=30 fails=0
=== LEG NULL_MEDIUM ===
  MUTATION NULL_MEDIUM: X(rldicl) body (66 lines) replaced by the identity body
  mutant diff: 68 changed lines (mutant.diff)
  build rc=0  binary=FRESH
  probe rc=0  SCORE 16/24  elapsed=0.1s  binary=/tmp/gx565id/gxemul  label=NULL_MEDIUM
  FAILING: zx32 rldicl, rot8 rldicl, vacuous cell, vac neighbour, census wrong, sh63 rldicl, sh32 rldicl, rc cr0
  GATE BLOCK: checks=30 fails=11 [ppc_rldicl row: zx32 rldicl got=0] [ppc_rldicl row: rot8 rldicl got=0] [ppc_rldicl row: vacuous cell got=0] [ppc_rldicl row: vac neighbour got=0] [ppc_rldicl row: census wrong got=0] [ppc_rldicl row: sh63 rldicl got=0] [ppc_rldicl row: sh32 rldicl got=0] [ppc_rldicl row: rc cr0 got=0] [ppc_rldicl rows green got=16] [ppc_rldicl rows red got=8] [ppc_rldicl score 24/24 got=0]
=== LEG RESTORED ===
  MUTATION RESTORED: baseline copied over the target
  build rc=0  binary=FRESH
  probe rc=0  SCORE 24/24  elapsed=0.1s  binary=/tmp/gx565id/gxemul  label=RESTORED
  FAILING: 
  GATE BLOCK: checks=30 fails=0
=== CLEARANCE ===
  part 1 (cmp vs SEC) = CLEAN   part 2 (binary -nt source) = FRESH
  SENTINEL CLEARED
IDENTITY_DONE
```
### 2b. Gate 13, alone (`gate13/RUN.txt`, `gate13/gate_ppc.out`)
```
gate13 start 08:50:22 HEAD 69253c3c gate md5 654bd92217f6 probe md5 890fab46b4f6
gate13 rc=0 end 08:51:49
gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl: PASS (140 checks)
```
Also re-run on the final files: the probe green 24/24; `/bin/true` 22 of 30 red; the absent binary 1 of 1 in the block's
scoring text; the block controls 13 legs, zero unexpected; section R's six legs as before; section U 34 PASS.

## 3. The records drafts

### 3a. The CHANGELOG block (`{CONFIRM}` is filled from your answer)
```
# `#565` (wiringcliff): `regress/ppc_rldicl_probe.py` is wired into gate 13 five days before its exemption would refuse every commit -- 30 checks score all 24 rows by name; floor clause (c) measured three ways, the identity body among them; the probe's records the new pin exposed are corrected

**The cliff.**  Section R (`tools/pipeline/check_probe_wiring.py`) held `#522`'s detector for `rldicl` writing zero,
`ppc_rldicl_probe.py`, in its EXEMPT table, dated 2026-10-22 after two re-dates by owner ruling (2026-09-24, then
`04f3e7c0` on 2026-10-09).  With `d < today` it would have refused every commit from 2026-10-23.  Witness `harness:` --
the round's subject is the test apparatus: no `regress/gate_*.sh` named the probe at HEAD `69253c3c`, and section R
reported it exempt.

**What ships.**
* `regress/gate_ppc.sh` -- a block after the rldimi block and before the NetBSD prerequisite (`-E bareppc -M 64` needs no
  image, so a red row is recorded rather than skipped): the completion sentinel, exactly once; all 24 rows by name
  (`^name  .*ok$` once each); rows run / green / red pinned to 24 / 24 / 0; then EVERY `^SCORE ` line counted (it must be
  one) and `SCORE 24/24` read -- 30 checks when green.  Its comment carries a CONTRACT: the block transmits the probe's
  verdicts and re-derives none.  The gate's title gains "rldicl".
* `tools/pipeline/check_probe_wiring.py` -- the probe's EXEMPT tuple and its comment deleted; a dated DISCHARGED note
  beside `#536`'s and `#548`'s; the MANIFEST entry's `EXEMPT below rather than wired` marked historical; two MANIFEST
  qualifiers (below).
* `tools/precommit_check.sh` -- `SCORE_CLAIMS_MANIFEST` 33 -> 34, for the new `ppc_rldicl rows run ... 24` pin.
* `regress/ppc_rldicl_probe.py` -- records only.  Its verdict logic is unchanged: against HEAD's, its AST (docstring
  excluded) differs in ONE string constant, the `disasm total` row's printed note.

**Measured** (all under `regress/artifacts/ppcrldiclzero/gatewire_20261018/`).
* Gate 13, alone: PASS 140 checks, rc 0, the rldicl block's 30 among them (`gate13/`).
* The block's scoring text, extracted from the shipped gate and sourced against doctored copies of a green log
  (`controls/controls_final_20261018.out`): 13 legs, each red exactly where it should be -- the DONE line removed or
  doubled; a row renamed, turned FAIL, deleted or duplicated; a stray `ok` line; the SCORE line removed, wrong, doubled
  or contradicted -- and the pre-`#522` build's log (`02af7f3e`, SCORE 16/24) reds 11 of the 30.
* Section R (`controls/r_legs_final/`): the staged checker with the wired gate passes; HEAD's checker (tuple kept)
  reports STALE EXEMPTION; the exec line commented out reports UNWIRED DETECTOR; HEAD's checker with the gate unwired
  passes today and, at `--today 2026-10-23`, reports the probe EXPIRED -- the cliff this round removes.
* Section U: `SCORE_CLAIMS_PINNED=34`, PASS.  With HEAD's probe and the new gate it FAILED -- `STALE ppc_rldicl_probe.py
  docstring claims 16/19, pin is 24` (`controls/score_claims_u_headprobe_FAIL_20261018.out`) -- which is how this round
  came to read the probe's records.
* Floor clause (c), the null medium (`nullmedium/`): an IDENTITY BODY for X(rldicl) -- decode and retire, write nothing
  -- built in a scratch clone of `build/`: SCORE 16/24 and 11 of the block's 30 checks red; restored, 24/24, the clone
  `cmp`-clean and its binary fresh (`identity/IDENTITY.out`).  `/bin/true`: 22 of 30 red.  An absent binary reds the
  sentinel in the block's scoring text; in gate 13 `need_exec` turns it into a SKIP first.  Five rows stay green on
  `/bin/true` by construction -- `session` and `cand session` test exit status, `naive fix wrong` is arithmetic, `census
  run` counts the cells the probe drives, `census zero` counts parsed zeros -- recorded; not a breach.

**The records the new pin exposed, corrected** -- each beside the sentence it corrects, in the probe unless named:
* the docstring's M_NOMASK `16/19` is the 19-row figure (`pass2_20260910/opus_nomask.log:3`); on today's 24 rows it is
  19/24 (`killtable_20260910/t2/probe_M_NOMASK.raw:30`) -- section U's flag;
* `**THIS FILE HAS 19 ROWS, NOT 24**` qualified on its own line (24 since pass 2), and the second verbatim copy of `WHY
  THE SIBLING ROWS ARE NOT HERE` -- present twice since `e777ff06` -- deleted;
* the VACUITY comment's `could never fail, whatever the handler does`: `vacuous cell` is red under M_NOMASK (GPT-6 Astra),
  and under M_NAIVE, M_MASKEND and M_NOAND too, though it shares `naive fix wrong`'s CARRIED-NOT-COUNTED label (Grok 4.7);
* `every placed word` is disassembler-checked: every session disassembles, but only the control and census sessions'
  196 words are COMPARED -- the bogus-machine, 32-bit, vacuity and candidate-row sessions' eight are not (GPT-6 Astra,
  Grok 4.7, GLM 5.3) -- in the docstring, the printed note and the MANIFEST;
* `Four controls:` lists five (NL6), and the MANIFEST's t2 frozen copy is byte-identical to the shipped probe only AS
  SHIPPED AT `e777ff06` (NL7) -- both upheld by Fable 5.1 on 2026-10-16 as L4s to land when their file is next touched.

**Not done here, and why.**  The flagship ruled on 2026-09-11 that `naive fix wrong` be demoted to a print
(`ppcprobescorestale`); that changes the row count and belongs to its own round.  A note written after pass 2 that
redefined CARRIED-NOT-COUNTED to keep the row in SCORE contradicted that ruling and was withdrawn before commit: Grok 4.7
overturned it on F2, and GPT-6 Astra had upheld it without the ruling in its packet.  The probe's smallest escapes are
its own comparator -- `ok = True` (Grok 4.7) or `got >= want` (GPT-6 Astra) in `row()` -- which a block that scores only
ok/FAIL tokens cannot see; disclosed in the CONTRACT, and no value anchor added.  `alpha_tbi_probe.py`'s exemption comes
due the same day; it is the other session's Alpha area.

**The panel.**  Pass 1 on the design brief, pass 2 on the diff and the §F2 shared-findings pass, each by GPT-6 Astra
(ultra), Grok 4.7 (xhigh) and GLM 5.3; Gemini Argon gets the F2 packet when its quota window reopens.  Fable 5.1 NOT
FIRED -- held by the owner's 2026-10-17 directive; Opus, agy, kimi, deepseek and minimax deliberately not fired (owner
roster).  Flags: pass 1 3 + 4 + 7, pass 2 2 + 1 + 3, F2 3 + 5 + 4 -- every one taken, refined or rejected with its reason
(`brief_f2_body.md`, the ledger's `wiringcliff` entries).  D2 -- whether clause (c) needed the identity body -- was
settled by building it, not by vote.  {CONFIRM}

**Filed:** `ppcrldiclbanner` (LOW).  **Noted:** `wiringcliff` (next due: `alpha_tbi_probe.py`), `ppcprobescorestale` (part
1 done, the demotion owed), `nullmediumlegs` (the rldicl half measured, the alpha half owed), `ppcrldiclzero`.
```
### 3b. OUTSTANDING_BUGS.md -- the two in-place notes and the appended section
```diff
@@ -138,2 +138,5 @@
 >
+> *[2026-10-18, `#565`: the 19-row comments are corrected in place and gate 13 pins the 24-row denominator
+> by equality.  The demotion above is STILL OWED; doing it moves gate 13's literals 24 -> 23.]*
+>
 > ### OPEN -- filed 2026-09-11 from #524's table 4: a probe's memory read indexed dump COLUMNS by
@@ -24762,2 +24765,4 @@ other unreviewed deltas; HEAD's `panel.sh` does not yet.
   (neither has runtime wiring or an equality pin); the identity-body medium is the recommended form.
+  *[2026-10-18, `#565`: the rldicl half is MEASURED with the identity body -- 11 of gate 13's 30 rldicl checks red
+  (`regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/identity/`).  The `alpha_tbi_probe.py` half stays owed.]*
 * **`nullmediumsweep` (LOW, open)** -- the ~165-unit clause-(c) sweep has no durable artifact; a reproducible census
@@ -24912 +24917,15 @@ Fable 5.1, GPT-6 Astra, Grok 4.7).  Each row's ledger `state_note` carries its s
   `#564`'s own probe covers the other direction -- a new bit aliased onto bits 0-12 -- with its crossbit session.
+
+### 2026-10-18 -- `#565`: `ppc_rldicl_probe.py` wired into gate 13 (`wiringcliff` stays open); `nullmediumlegs`' rldicl half measured; one row filed
+
+* **`wiringcliff` (MED, in work)** -- `#565` wired `regress/ppc_rldicl_probe.py` into gate 13 and deleted its 2026-10-22
+  exemption (30 checks; gate 13 PASS 140).  Next due: `alpha_tbi_probe.py` 2026-10-22 (refuses every commit from 10-23;
+  the other session's Alpha area -- a gate block or an owner re-date), then the three `lca_*` probes 10-23 / 10-26 /
+  10-27, `ip30_abort_probe.py` 10-30 and the four `wdc_*` probes 11-05 .. 12-03.
+* **`nullmediumlegs` (LOW, open)** -- the rldicl half MEASURED with the identity body (11 of gate 13's 30 rldicl checks
+  red); the `alpha_tbi_probe.py` half is still owed.
+* **`ppcprobescorestale` (LOW, open)** -- part 1 done by `#565`; the flagship's 2026-09-11 demotion of `naive fix wrong`
+  to a print is still owed (it moves gate 13's literals 24 -> 23).
+* **`ppcrldiclbanner` (LOW, open)** -- the probe calls itself a WITNESS (docstring line 2 and its runtime banner; section
+  R's advisory SELFLABEL note), its usage string names `ppc_rldicl_witness.py`, and `vacuous cell`'s split note makes a
+  red log read `GREEN on a FAIL`.  Cosmetic; filed, not fixed, by all three seats.
```
### 3c. Ledger: the new state_note heads and the new row
* `wiringcliff` state_note, the NEW head (before its first `  ||  `):
  *** STATUS 2026-10-18 (#565): ppc_rldicl_probe.py WIRED into gate_ppc.sh (gate 13) and its exemption DELETED, five days before it would have refused every commit (dated 2026-10-22; `d < today').  Gate 13 PASS 140 checks, the rldicl block's 30 among them (regress/artifacts/ppcrldiclzero/gatewire_20261018/gate13/).  NEXT DUE: alpha_tbi_probe.py 2026-10-22 -- refuses from 10-23; the other session's Alpha area, so its gate block or an owner re-date is owed; then lca_badval 10-23, lca_widewrite 10-26, lca_isalane 10-27, ip30_abort_probe 10-30 and the four wdc_* probes 11-05..12-03.  THIS ROW STAYS OPEN. ***
* `ppcrldiclzero` state_note, the NEW head (before its first `  ||  `):
  [2026-10-18, #565] Its detector regress/ppc_rldicl_probe.py is WIRED into gate 13 (30 checks: the sentinel, all 24 rows by name, run/green/red, and the SCORE line counted then read) and its section-R exemption is deleted.  Floor clause (c) MEASURED (regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/): an identity body for X(rldicl) reds 11 of the 30, /bin/true 22.  Section U then read the probe's docstring and the round corrected the records it found there (#565's CHANGELOG block).
* `ppcprobescorestale` state_note, the NEW head (before its first `  ||  `):
  [2026-10-18, #565] PART 1 DONE: the 19-row comments are corrected in place (the bold `THIS FILE HAS 19 ROWS, NOT 24' qualified on its own line; the second verbatim copy of `WHY THE SIBLING ROWS ARE NOT HERE' deleted), and gate 13 now pins the denominator by EQUALITY (`ppc_rldicl rows run' 24, `SCORE 24/24').  PART 2 STILL OWED, as the flagship ruled on 2026-09-11 (regress/artifacts/heldqueue/fable_adjudication_20260911.md:177-180): demote `naive fix wrong' to a print.  That moves gate_ppc.sh's literals 24 -> 23 and its green-path count 30 -> 29; section U's stem count stays 34.  A #565 note that redefined CARRIED-NOT-COUNTED to keep the row in SCORE contradicted that ruling and was withdrawn before commit (Grok 4.7, #565 F2).
* `nullmediumlegs` state_note, the NEW head (before its first `  ||  `):
  [2026-10-18, #565] THE rldicl HALF IS DISCHARGED, MEASURED with the medium this row names: an IDENTITY BODY for X(rldicl) -- decode and retire, write nothing -- built in a scratch clone of build/ scores SCORE 16/24 and reds 11 of gate 13's 30 rldicl checks; restored, 24/24, clone cmp-clean and the binary fresh (regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/identity/IDENTITY.out).  Also measured: /bin/true 22 of 30; an absent binary reds the sentinel in the block's scoring text and is a SKIP in gate 13 (need_exec).  The probe is now wired with equality pins, so the by-construction reading holds as well.  The alpha_tbi_probe.py half is STILL OWED (its exemption comes due 2026-10-22).
* NEW ROW `ppcrldiclbanner` (sev LOW, state open):
  title: regress/ppc_rldicl_probe.py calls itself a WITNESS -- docstring line 2 and its runtime banner say `RUNG-3 WITNESS' while section R's MANIFEST classes it a detector -- its usage string names `ppc_rldicl_witness.py', and `vacuous cell''s note is split across two rows, so a red log reads `GREEN on a FAIL'
  state_note: filed 2026-10-18 by #565 (the gate wiring of this probe).  Raised by GPT-6 Astra, Grok 4.7 and GLM 5.3 on #565's pass 2 and shared-findings pass; all three ruled FILE, not fix.  Section R reports the first as an ADVISORY `SELFLABEL' note (check_probe_wiring.py's self_label; it fails nothing); the usage string prints only when the probe gets fewer than two arguments, which gate 13 never does; the split note is Grok 4.7's (#565 F2).  Cosmetic: no gate, kill or score rests on any of the three.  A round touching the probe's docstring -- `ppcprobescorestale''s demotion is the next one -- can close it.

### 3d. Ledger: the seat entries added to `wiringcliff`
* design / codex / regress/artifacts/ppcrldiclzero/gatewire_20261018/codex_rldiclp1.txt: #565 PASS 1 (the design brief): 3 flags -- GPT-6 Astra: the packet's transcript of `naive fix wrong' was truncated at `M_NOM' (a packet error; the probe prints the whole row); no control isolated the SCORE check, and an appended contradictory `SCORE 0/24' passed (TAKEN: a `score lines' check counting EVERY ^SCORE line, controls V8-V11); the refusal date is 2026-10-23, not 10-22 -- `d < today' (TAKEN; MEASURED by legs H1/G1).
* design / grok / regress/artifacts/ppcrldiclzero/gatewire_20261018/grok_p1.txt: #565 PASS 1 (the design brief): 4 flags -- Grok 4.7: run as a whole the block truncates its log before scoring it (the controls source ONLY the scoring text); section R's STALE EXEMPTION and UNWIRED DETECTOR legs (MEASURED); the proposed 24s were quoted and labelled `rows emitted', invisible to section U (now `ppc_rldicl rows run' unquoted; SCORE_CLAIMS_MANIFEST 33 -> 34); the MANIFEST comment would still say `EXEMPT below rather than wired' (a dated note, and a DISCHARGED note beside mk48's and fbpending's).
* design / glm / regress/artifacts/ppcrldiclzero/gatewire_20261018/glm_p1.txt: #565 PASS 1 (the design brief): 7 flags -- GLM 5.3, packet-fed: the same truncated transcript; `re-dated once' undercounts (re-dated twice, 2026-09-24 and 2026-10-09); no duplicated-row control (V7 added) and no stated scope for a stalled probe (the probe's own 90 s / 60 s backstops, now in the block comment); three premises not settle-able from the packet -- section R's wiring test, the mk48 model, the same-commit companions -- each settled by a measurement or a reading.
* design / fable5 / -: #565 PASS 1 (the design brief): NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled, HTTP 429, at 04:57 the same day).
* review / codex / regress/artifacts/ppcrldiclzero/gatewire_20261018/codex_rldiclp2.txt: #565 PASS 2 (the diff): 2 flags -- GPT-6 Astra: the probe's VACUITY comment says `vacuous cell' `could never fail, whatever the handler does' and M_NOMASK's receipt shows it red (killtable_20260910/t2/probe_M_NOMASK.raw:18); `every placed word' is disassembler-checked overclaims, in the docstring, the printed note and the MANIFEST.  Both corrected in place.  Its smallest escape is the probe's own comparator (`got >= want' in row()), disclosed in the block's CONTRACT.
* review / grok / regress/artifacts/ppcrldiclzero/gatewire_20261018/grok_p2.txt: #565 PASS 2 (the diff): 1 flag -- Grok 4.7: the docstring cited its two M_NOMASK receipts from two roots (one root now).  Its smallest escape is `ok = True' in row() (disclosed).  It named NL6 (`Four controls' lists five) and NL7 (the t2 `byte-identical' sentence), both upheld by Fable 5.1 on 2026-10-16 as L4s to land where their file is next touched -- landed here.
* review / glm / regress/artifacts/ppcrldiclzero/gatewire_20261018/glm_p2.txt: #565 PASS 2 (the diff): 3 flags -- GLM 5.3, packet-fed: the bold `THIS FILE HAS 19 ROWS, NOT 24' stayed unqualified on its own line (qualified there now); the DISCHARGED note's `came due 2026-10-22' for an exemption deleted on 10-18 (reworded); the brief's `count' premise (REJECTED: lib.sh's count() returns 0 for an absent file before grep runs).
* review / fable5 / -: #565 PASS 2 and the F2 shared-findings pass: NOT FIRED -- Fable adjudication is held by the owner's 2026-10-17 directive (walled, HTTP 429, at 04:57 the same day).
* review / codex / regress/artifacts/ppcrldiclzero/gatewire_20261018/codex_rldiclf2.txt: #565 F2 (the shared-findings pass): 3 flags, all on my own repair wording -- GPT-6 Astra: `not re-read' is false (every session disassembles; only the control and census 196 words are COMPARED); `an absent binary reds the sentinel' holds for the block's scoring text, not gate 13 (need_exec SKIPs first); nullmedium.sh's header still said `comment-only'.  All corrected.  It UPHELD my D1 (keep `naive fix wrong' in the 24) on #522 pass 2's retention reason -- but the flagship's later ruling (2026-09-11, `demote it to a print') governs; D1 was withdrawn.
* review / grok / regress/artifacts/ppcrldiclzero/gatewire_20261018/grok_f2.txt: #565 F2 (the shared-findings pass): 5 flags -- Grok 4.7: OVERTURNED my D1 and my proposal to close `ppcprobescorestale' on the flagship's 2026-09-11 ruling (the probe note that redefined CARRIED-NOT-COUNTED was withdrawn; the row stays open with the demotion owed); `vacuous cell' carries that label and has kills (noted beside it); the unchecked disassembly is eight words in four sessions; the CONTRACT's `any block' (gate_arm.sh pins some got= values); the t2 qualifier omitted the printed-note change.  All corrected.
* review / glm / regress/artifacts/ppcrldiclzero/gatewire_20261018/glm_f2.txt: #565 F2 (the shared-findings pass): 4 flags -- GLM 5.3, packet-fed: the vacuity session's discarded disassembly; the t2 qualifier; the F2 packet mislabelled section 3b's base (a packet defect, no shipped record); and it would not co-sign D2 (discharging nullmediumlegs' rldicl half without the identity body the row names) -- D2 was then SETTLED BY MEASUREMENT: an identity body for X(rldicl) reds 11 of the block's 30 checks (nullmedium/identity/IDENTITY.out).

## 4. Questions

**Q1.**  Is each F2 flag fixed CORRECTLY (Astra 1-3, Grok's five and its two Q3 items, GLM's four) -- and does any fix
introduce a new false sentence?
**Q2.**  Is every claim in section 3 true against its receipt -- each number, path, date, seat attribution and commit?
Name each false one with the line that refutes it.
**Q3.**  Is anything owed before this commit that is not done or recorded as owed?

**Format:** open with the token `ASTRA_RLDICLWIRE_CF_20261018`, then ONE line `VERDICT: <n> flags -- <one line>`, then
Q1..Q3.  Every defect is a line starting `FLAG:`.  Facts and flags only.
