# #565 -- the shared-findings (§F2) pass: wiring `regress/ppc_rldicl_probe.py` into gate 13

**Please do not simply ratify.**  Every pass-2 finding is below with my disposition; the load-bearing question is which of
my dispositions is WRONG.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; ignore any other `src/`.  READ-ONLY:
write nothing to any project tree.  `regress/gate_ppc.sh`, `regress/ppc_rldicl_probe.py` and `tools/precommit_check.sh`
in the working tree are exactly this round's edit; `tools/pipeline/check_probe_wiring.py` there ALSO carries lines from
other uncommitted work, so section 3b (HEAD -> the staged text) is the authority for that file.

**Seats.**  Pass 2 was answered by GPT-6 Astra (ultra), Grok 4.7 (xhigh) and GLM 5.3; this pass goes to the same three
and to Gemini Argon (packet-fed).  Fable 5.1 is HELD by owner ruling 2026-10-17; Opus, agy, kimi, deepseek and minimax
are deliberately not fired (owner roster).  **Self-review is disclosed:** each seat below adjudicates its own findings
-- be HARDER on them, and check that my FIX is right, not only that your finding was.  GPT-6 Astra: D1 sets your
2026-09-11 filing against your 2026-10-18 reading; rule between them.

## 1. Findings and my dispositions

| # | raised by | finding | disposition, and what changed |
|---|---|---|---|
| F1 | Astra | the VACUITY comment says the `vacuous cell` row "could never fail, whatever the handler does"; M_NOMASK's receipt shows it red (`killtable_20260910/t2/probe_M_NOMASK.raw:18`: got 0xffffffff00000000, want 0x0) | ACCEPTED, L4: a dated note beside the sentence limits it to the always-zero defect |
| F2 | Astra | the docstring, the `disasm total` row's printed note and section R's MANIFEST say EVERY placed word is disassembler-checked; the candidate-row session's three words are not (`xregs, _, xT, xhow = session(` discards its disassembly) | ACCEPTED, L4 at all three places.  The printed note is the ONE non-comment change in the probe -- a string no comparison reads |
| F3 | Astra (Q3), Grok (Q3); prescreen NL7 | MANIFEST: the t2 frozen copy is "byte-identical to the shipped" probe -- true of `e777ff06` only | ACCEPTED as NL7 (upheld 2026-10-16 by Fable 5.1 as an L4 to land where its file is next touched).  Verified: the frozen copy and `e777ff06`'s blob are both md5 7ea10ea4b141, raw; `a05660af`'s is 0a0c2f881fd9 |
| F4 | GLM | the bold `**THIS FILE HAS 19 ROWS, NOT 24**` stays unqualified on its own line; the note below it is not where a grep lands | ACCEPTED: an inline `[19-row era: 24 since pass 2, see #565's note below]` |
| F5 | GLM | the brief's premise "`count` is `grep -ac` ... (0 for an absent file)" does not follow from `grep -ac` | REJECTED as a defect: `regress/lib.sh`'s `count()` begins `[ -f "$1" ] \|\| { echo 0; return; }`; the brief compressed the wrapper into a parenthesis.  No record changed |
| F6 | GLM | the DISCHARGED note says the exemption "came due 2026-10-22"; deleted on 10-18, it never came due | ACCEPTED: "was dated 2026-10-22 ... and would have refused every commit from 2026-10-23" |
| F7 | Grok | the docstring cites its two M_NOMASK receipts from two roots | ACCEPTED: one root, stated |
| F8 | Grok (Q2); prescreen NL6 | the docstring says "Four controls:" and lists five | ACCEPTED as NL6 (upheld 2026-10-16): "Five controls (this said `Four' until #565; NL6):" |
| F9 | Astra (Q1), Grok (Q1); GLM (Q1, block side) | the smallest escape is the PROBE's comparator: `ok = (got == want)` -> `ok = True` (Grok: every mutant 24/24), or `>=` (Astra: M_CR0 23 -> 24/24); block-side it takes four coordinated relaxations or a log rewrite (GLM) | REFINED: not repaired.  The block's comment now carries a CONTRACT: it transmits the probe's verdicts and re-derives none, as every block in this tree that scores a probe's own tokens does |
| F10 | GLM (Q5) | the block's direct `grep -cx` / `grep -c '^SCORE '` lack the `-a` that `count` carries | REJECTED as a change: every miscount direction is fail-closed (a red), and the mk48 block it is modelled on reads the same way.  Recorded here only |
| F11 | Astra, Grok, GLM (Q5) | the probe's first docstring line says `RUNG-3 WITNESS` (section R's advisory SELFLABEL note) and its usage string names `ppc_rldicl_witness.py` | FILED by all three; I propose ONE new LOW row for both (with Astra's "runtime WITNESS banner") |
| F12 | Grok (Q5) | `nullmediumlegs`' rldicl sentence ("exempt until 2026-10-22 ... clause (c) unmeasured") goes stale with this commit | ACCEPTED: the row gains a dated note -- see D2 for what it says is still owed |
| F13 | mine | `ppcprobescorestale` (open, LOW) names two defects: the 19-vs-24 row-count comments, and `naive fix wrong` documented "carried-not-counted" while `SCORE` includes it; its repair "is to make the code and the prose agree ... and to pin the denominator with a check row against a literal" | ACCEPTED: the 19-row comments are corrected (F4 and pass 1's notes), gate 13 now pins the denominator by EQUALITY (`rows run` 24, `SCORE 24/24`), and the docstring says what the code does (D1).  I propose to CLOSE it with this commit |

## 2. Disagreements

**D1 -- what "CARRIED-NOT-COUNTED" means.**  `ppcprobescorestale` (filed 2026-09-11 from a GPT-6 Astra answer): *"`naive
fix wrong' still contributes to `SCORE' through `row()', despite its 'carried-not-counted' description."*  GPT-6 Astra,
#565 pass 2: *"'CARRIED-NOT-COUNTED' denotes denied detection credit in the originating review, which explicitly
retained the row to preserve scores; its inclusion in 24/24 is not a new contradiction."*  The originating record
(`#522`'s CHANGELOG block) says only *"It is now declared carried-not-counted, the disposition already invented for a row
in `#520`"*; `vacuous cell`, the other carried-not-counted row, is also in the 24.  **My ruling:** the second reading,
written into the docstring so the prose cannot be read the first way again.  Warrant: the code has always counted both
rows, the closing table (t2) scores 24/24 with them, and the gate now pins that 24.

**D2 -- clause (c) for this detector.**  `nullmediumlegs` (filed 2026-10-09 from Fable 5.1's 7n-1 ruling as corrected
by GPT-6 Astra) owes a MEASURED null-medium leg because the probe had *"no runtime gate wiring or an equality pin"*, and
names the leg's object as *"an instruction handler's IDENTITY BODY (decode and retire, write nothing)"*.  This commit
(a) adds the wiring and the equality pins, so the by-construction reading now succeeds -- a dead run reds the sentinel
or named rows -- and (b) MEASURES two dead-run media (absent binary: 1 of 1 checks red; `/bin/true`: 22 of 30).  It
does NOT build the identity body.  **My position:** the rldicl half of `nullmediumlegs` is discharged in the
`(c): measured at <artifact>` form for a runtime probe, and the identity-body leg -- the carrier's recommended default
for an instruction-handler round, not its only object -- is not owed.  **The other side**, in the row's own words: its
object is the identity body.  I keep the row OPEN for `alpha_tbi_probe.py` either way.

## 3. The repair since pass 2 (every hunk inlined by a script)

### 3a. `regress/ppc_rldicl_probe.py` (pass-2 text -> now)

```diff
--- a/regress/ppc_rldicl_probe.py
+++ b/regress/ppc_rldicl_probe.py
@@ -24,10 +24,11 @@ pass-2 seat caught it still standing here after the product comment was correcte
     architecture says AND -- 126 of 190 cells wrong.  That is the M_NAIVE leg.
   * deleting the `& tmp2' outright, ON THE FIXED CODE, ships ROTL64 ALONE with the
     mask IGNORED, measured as M_NOMASK -- 16/19 on the 19-row instrument (the pass-2
-    seat: artifacts/ppcrldiclzero/pass2_20260910/opus_nomask.log) and 19/24 on the
-    24 rows it carries now (killtable_20260910/t2/probe_M_NOMASK.raw).  (Before the fix
-    it would have shipped the OR, because the mask was in `tmp'; witness_naive.out
-    measured THAT function, not this one.)
+    seat) and 19/24 on the 24 rows it carries now.  Receipts, both under
+    regress/artifacts/ppcrldiclzero/: pass2_20260910/opus_nomask.log and
+    killtable_20260910/t2/probe_M_NOMASK.raw.  (Before the fix it would have shipped
+    the OR, because the mask was in `tmp'; witness_naive.out measured THAT function,
+    not this one.)
 *** THE `naive fix' ROW BELOW IS AN ARITHMETIC IDENTITY OVER THIS FILE'S OWN
 CONSTANTS AND CANNOT FAIL UNDER ANY MUTATION OF THE EMULATOR. ***  It never touches
 the binary, the registers or any session, and it is green in every leg of every table
@@ -36,6 +37,9 @@ measurable rather than argued'; it does not, and a pass-2 seat named it as the
 check-that-cannot-fail shape sitting inside a detector whose whole purpose is to be
 failable.  **THE M_NAIVE KILL-TABLE LEG is what makes the claim measurable.**  The row
 is CARRIED-NOT-COUNTED, the disposition already used for `vacuous cell'.
+[#565, 2026-10-18: CARRIED means it stays IN `SCORE' -- the 24 the gate pins includes it --
+and NOT COUNTED means it is credited with no kill; it never meant left out of `SCORE', which
+the code has never done (`ppcprobescorestale' read it that way).]
 
 ARCHITECTURE, read locally -- _scratchpad/ppc_pem_32and64_2005.txt:29736 (rldiclx):
         n <- sh[5] || sh[0-4]
@@ -57,7 +61,7 @@ own MACHINE_DEFAULT_CPU is PPC970, which is 64-bit in the in-tree CPU table, and
 64-bit is what the decoder requires (`if (cpu->cd.ppc.bits == 32) goto bad').
 
 THE ORACLE is a guest-visible wrong VALUE, not a process death, so it is read
-directly out of the destination register.  Four controls:
+directly out of the destination register.  Five controls (this said `Four' until #565; NL6):
   live          `li r9,0x1234' in the same session reads back 0x1234 -- the guest
                 really executes and the readback path really works.
   seed holds    a destination register seeded with a sentinel and then stepped
@@ -70,6 +74,9 @@ directly out of the destination register.  Four controls:
                 disassembler (cpu_ppc.c, a DIFFERENT code path from the execute
                 handler in cpu_ppc_instr.c) and compared against the operands the
                 encoder intended.  Guards the hand-assembled-encoding trap.
+                [#565, 2026-10-18: NOT every word -- the control and census sessions'
+                196 (6 + 190) are; the candidate-row session's three are not re-read,
+                its disassembly result is discarded (GPT-6 Astra, #565 pass 2).]
   rldicr        the correctly-written sibling, same rotate-and-mask shape, same
                 session -- attributes the failure to X(rldicl) rather than to the
                 encoding, the machine, the rotate or this program.
@@ -459,6 +466,10 @@ row("bits32 rld bad", "TODO" if "TODO: rld" in b32T else "no-msg", "TODO",
 # ===================================================== VACUITY (question 3) ===
 # A cell where the ARCHITECTURAL answer is itself zero: a detector row placed
 # here could never fail, whatever the handler does.
+# [#565, 2026-10-18: TOO STRONG.  It cannot fail on the ALWAYS-ZERO defect this file was
+# written for, but it fails when the handler writes something else: under M_NOMASK it read
+# 0xffffffff00000000 and was red (killtable_20260910/t2/probe_M_NOMASK.raw:18; GPT-6 Astra,
+# #565 pass 2).]
 RS_VAC = 0xFFFFFFFF00000000
 vregs, _, vT, vhow = session(seed([(SRC, RS_VAC)] + [(r, SENT) for r in DESTS]),
                              [RLDICL(4, SRC, 0, 32), RLDICL(5, SRC, 0, 0)])
@@ -519,7 +530,7 @@ row("census zero", census_zero, 0,
     "cells that returned EXACTLY ZERO -- want 0 after a fix")
 row("disasm total", "%d/%d" % (disasm_ok, disasm_checked),
     "%d/%d" % (disasm_checked, disasm_checked),
-    "every placed word re-read by the tree's own disassembler")
+    "control + census words re-read by the tree's own disassembler (not the 3 cand words)")
 
 # ================================ WHY THE SIBLING ROWS ARE NOT HERE =============
 #
@@ -537,10 +548,10 @@ row("disasm total", "%d/%d" % (disasm_ok, disasm_checked),
 #  or into a detector of its own -- that is a decision for those rounds, not this one.
 #
 #  MEASURED: witness 19/27 committed and 24/27 fixed, the five flipped rows being
-#  exactly the ones kept below.  **THIS FILE HAS 19 ROWS, NOT 24** -- an earlier draft
-#  of this note carried the witness's own post-fix count straight across, which a
-#  pass-2 seat caught.  It is 19/19 on the fix and 14/19 pre-fix
-#  (killtable_20260910/SCORES.txt).
+#  exactly the ones kept below.  **THIS FILE HAS 19 ROWS, NOT 24** [19-row era: 24 since
+#  pass 2, see #565's note below] -- an earlier draft of this note carried the witness's
+#  own post-fix count straight across, which a pass-2 seat caught.  It is 19/19 on the
+#  fix and 14/19 pre-fix (killtable_20260910/SCORES.txt).
 #  [#565, 2026-10-18: TRUE OF THE 19-ROW FILE IT DESCRIBED, AND FALSE SINCE PASS 2 -- the
 #  five rows under `ROWS ADDED BY PASS 2' below make it 24, which gate_ppc.sh now pins:
 #  24/24 on the fix and 16/24 on the pre-fix HEAD (killtable_20260910/t2/SCORES.txt),
```

### 3b. `tools/pipeline/check_probe_wiring.py` (the pass-2 staged text -> now)

```diff
--- a/tools/pipeline/check_probe_wiring.py
+++ b/tools/pipeline/check_probe_wiring.py
@@ -1703,14 +1703,14 @@ MANIFEST = {
     #  red and SCORE counts pinned; its EXEMPT entry is DISCHARGED below.  "EXEMPT below rather than wired" above is
     #  historical.
     "ppc_rldicl_probe.py":
-        (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word.  BASE 24/24, whole-file pre-fix leg 16/24 (clause (a); 'null medium' until 2026-10-09, 7n-1), EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),
+        (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word [#565: of the control and census sessions' 196 words -- the candidate-row session's three are not re-read].  BASE 24/24, whole-file pre-fix leg 16/24 (clause (a); 'null medium' until 2026-10-09, 7n-1), EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),
 
     #  The frozen copies are the instruments as-run.  t1 is the 19-row form that pass 2
     #  escaped TWICE; t2 is the 24-row closure; t0 is an apparatus failure kept on purpose.
     "artifacts/ppcrldiclzero/killtable_20260910/t1/ppc_rldicl_probe.frozen.py":
         (CLASS_RESEARCH, "ppcrldiclzero (#522) table 1: the as-run 19-row instrument -- pass 2 escaped it TWICE at 19/19 (a shift-decode mutant it was blind to BY CONSTRUCTION, and a CR0 mutant that is the sibling handler's own shipping token)"),
     "artifacts/ppcrldiclzero/killtable_20260910/t2/ppc_rldicl_probe.frozen.py":
-        (CLASS_RESEARCH, "ppcrldiclzero (#522) table 2: the CLOSING 24-row instrument, byte-identical to the shipped regress/ppc_rldicl_probe.py"),
+        (CLASS_RESEARCH, "ppcrldiclzero (#522) table 2: the CLOSING 24-row instrument, byte-identical to the shipped regress/ppc_rldicl_probe.py [#565: AS SHIPPED AT e777ff06 -- a05660af changed its helper oracles and #565 its comments since; NL7]"),
     "artifacts/ppcrldiclzero/killtable_20260910/t0_apparatus_failure/ppc_rldicl_probe.frozen.py":
         (CLASS_RESEARCH, "ppcrldiclzero (#522) table 0: an APPARATUS FAILURE preserved rather than deleted -- the driver was derived by substitution from #521 and called THAT round's mutator, which replied `unknown mutant'.  The hard-fail refused rather than measuring an unmutated tree, but the table looked HALF-HEALTHY because both mutators define BASE and answered it identically.  No number from it is cited anywhere"),
 
@@ -3172,8 +3172,9 @@ EXEMPT = {
     #  gate_arm.sh beside footbridge_sites_probe.py, all four timers, --expect-cap 762.
     #  Deleted in the SAME edit as the wiring, for the same reason.
     #  ppc_rldicl_probe.py's exemption is DISCHARGED, 2026-10-18 (#565) -- wired into gate_ppc.sh beside the
-    #  rlwimi/rldimi blocks on the same -E bareppc -M 64, every row scored by name.  It came due 2026-10-22 after
-    #  two re-dates by owner ruling.  Deleted in the SAME edit as the wiring, for the same reason.
+    #  rlwimi/rldimi blocks on the same -E bareppc -M 64, every row scored by name.  It was dated 2026-10-22,
+    #  after two re-dates by owner ruling, and would have refused every commit from 2026-10-23 (`d < today').
+    #  Deleted in the SAME edit as the wiring, for the same reason.
     #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
```

### 3c. `regress/gate_ppc.sh` (pass-2 text -> now)

```diff
--- a/regress/gate_ppc.sh
+++ b/regress/gate_ppc.sh
@@ -170,6 +170,12 @@ fi
 # SCORE line, each pinned to a literal so a shrunk or renamed table cannot pass -- 30 checks when
 # green.  Names sit in a %-18s column and none is longer than 15, so `^name  ' cannot match a
 # neighbour (the padded-column trap).  The rows-run line is in the form check_score_claims.py pins.
+# CONTRACT: the block TRANSMITS the probe's verdicts and re-derives none -- each row's ok/FAIL and its
+# SCORE come from one comparison in the probe's row(), so an edit there (Grok 4.7's `ok = True', GPT-6
+# Astra's `>=', #565 pass 2) lets a mutant through, as it would through any block scoring a probe's own
+# tokens.  The exit status is ignored on purpose: this probe exits 0 with failed rows (probeexitzero).
+# Floor (c), measured: an absent binary reds the sentinel check and /bin/true reds 22 of the 30
+# (regress/artifacts/ppcrldiclzero/gatewire_20261018/nullmedium/).
 RLCLOG=$LOGDIR/ppc_rldicl.log
 python3 -u ppc_rldicl_probe.py "$PMAX" gate > "$RLCLOG" 2>&1 || true
 if [ "$(grep -cx 'PPC_RLDICL_PROBE_DONE' "$RLCLOG")" != 1 ]; then
```

### 3d. The whole round against HEAD (`--numstat`)

```
39	1	regress/gate_ppc.sh                                INLINED (pass 2 brief, plus 3a-3c here)
29	30	regress/ppc_rldicl_probe.py                       INLINED (pass 2 brief, plus 3a-3c here)
3	1	tools/precommit_check.sh                            INLINED (pass 2 brief, plus 3a-3c here)
9	25	tools/pipeline/check_probe_wiring.py (HEAD -> the staged text) INLINED (pass 2 brief, plus 3a-3c here)
regress/artifacts/ppcrldiclzero/gatewire_20261018/   NEW: briefs, packets, seat answers, controls, null medium -- SUMMARIZED (section 4)
tools/pipeline/ledger.json, CHANGELOG.md, matrix.html   NOT YET WRITTEN (section 5)
```

## 4. Re-verified on the final files (receipts under `regress/artifacts/ppcrldiclzero/gatewire_20261018/`)

* The probe once on `build/gxemul` (2026-10-17 22:14): `rldicl_final_build_20261018.log`, `SCORE 24/24`, all 24 rows
  `ok`, the DONE line present.
* The block's scoring text on the doctored logs (`controls/controls_final_20261018.out`), green log = the line above:

```
V0  green log                      checks=30  fails=0  want=0  ok
V1  DONE removed                   checks=1   fails=1  want=1  ok [ppc_rldicl probe completed got=no]
V2  DONE duplicated                checks=1   fails=1  want=1  ok [ppc_rldicl probe completed got=no]
V3  one row renamed                checks=30  fails=1  want=1  ok [ppc_rldicl row: live got=0]
V4  one row ok -> FAIL             checks=30  fails=3  want=3  ok [ppc_rldicl row: census zero got=0] [ppc_rldicl rows green got=23] [ppc_rldicl rows red got=1]
V5  one row deleted (23 rows)      checks=30  fails=3  want=3  ok [ppc_rldicl row: census zero got=0] [ppc_rldicl rows run got=23] [ppc_rldicl rows green got=23]
V6  stray line ending ok           checks=30  fails=2  want=2  ok [ppc_rldicl rows run got=25] [ppc_rldicl rows green got=25]
V7  one row duplicated             checks=30  fails=3  want=3  ok [ppc_rldicl row: census zero got=2] [ppc_rldicl rows run got=25] [ppc_rldicl rows green got=25]
V8  SCORE removed                  checks=30  fails=2  want=2  ok [ppc_rldicl score lines got=0] [ppc_rldicl score 24/24 got=0]
V9  SCORE 23/24                    checks=30  fails=1  want=1  ok [ppc_rldicl score 24/24 got=0]
V10 valid SCORE duplicated         checks=30  fails=2  want=2  ok [ppc_rldicl score lines got=2] [ppc_rldicl score 24/24 got=2]
V11 contradictory SCORE appended   checks=30  fails=1  want=1  ok [ppc_rldicl score lines got=2]
V12 PRE-FIX binary's log           checks=30  fails=11 want=>0 ok
     red: [ppc_rldicl row: zx32 rldicl got=0] [ppc_rldicl row: rot8 rldicl got=0] [ppc_rldicl row: vac neighbour got=0] [ppc_rldicl row: census wrong got=0] [ppc_rldicl row: census zero got=0] [ppc_rldicl row: sh63 rldicl got=0] [ppc_rldicl row: sh32 rldicl got=0] [ppc_rldicl row: rc cr0 got=0] [ppc_rldicl rows green got=16] [ppc_rldicl rows red got=8] [ppc_rldicl score 24/24 got=0]
CONTROLS_DONE
```

* Section R (`controls/r_legs_final/`, staged checker = 3b's result):

```
G   PROBEWIRING_PASS  76/85 detectors run by a gate, 9 dated-exempt, 44 witnesses correctly ungated
S   PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
      FAIL  STALE EXEMPTION  ppc_rldicl_probe.py is RUN by gate_ppc.sh:180 and still carries an exemption dated 2026-10-22 -- the debt is paid, delete the line
G1  PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
      FAIL  EXPIRED EXEMPTION  alpha_tbi_probe.py came due 2026-10-22 (today 2026-10-23) and is still run by no gate
U   PROBEWIRING_FAIL  1 problem(s); 75/85 detectors run by a gate, 9 dated-exempt
      FAIL  UNWIRED DETECTOR  ppc_rldicl_probe.py is run by NO gate and has no dated exemption.
H0  PROBEWIRING_PASS  75/85 detectors run by a gate, 10 dated-exempt, 44 witnesses correctly ungated
H1  PROBEWIRING_FAIL  2 problem(s); 75/85 detectors run by a gate, 10 dated-exempt
      FAIL  EXPIRED EXEMPTION  alpha_tbi_probe.py came due 2026-10-22 (today 2026-10-23) and is still run by no gate
      FAIL  EXPIRED EXEMPTION  ppc_rldicl_probe.py came due 2026-10-22 (today 2026-10-23) and is still run by no gate
```

* Section U (`controls/score_claims_u_final_20261018.out`): `SCORE_CLAIMS_PINNED=34`, `SCORE_CLAIMS_PASS`.
* The null medium with the FINAL probe and gate (`nullmedium/NULLMEDIUM.out`; the first run, probe md5 f1098186, is kept
  in `nullmedium/run1_probe_f1098186/`):

```
probe: 1428cb6f783f11023fd52268dfbb4eb8  regress/ppc_rldicl_probe.py
gate:  9c5ef69325a26c5934fca7e326019135  regress/gate_ppc.sh
LEG absent  binary=/nonexistent/gxemul  probe_rc=1     0s  gate checks=1   fails=1   RED (clause c holds)
     red: [ppc_rldicl probe completed got=no]
     log tail:                ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/gxemul'|
LEG nonemu  binary=/bin/true            probe_rc=0     0s  gate checks=30  fails=22  RED (clause c holds)
     red: [ppc_rldicl row: live got=0] [ppc_rldicl row: seed holds got=0] [ppc_rldicl row: src intact got=0] [ppc_rldicl row: disasm xcheck got=0] [ppc_rldicl row: zx32 rldicl got=0] [ppc_rldicl row: zx32 rldicr got=0] [ppc_rldicl row: rot8 rldicl got=0] [ppc_rldicl row: rot8 rldicr got=0] [ppc_rldicl row: neg apparatus got=0] [ppc_rldicl row: bits32 live got=0] [ppc_rldicl row: bits32 rld bad got=0] [ppc_rldicl row: vacuous cell got=0] [ppc_rldicl row: vac neighbour got=0] [ppc_rldicl row: census wrong got=0] [ppc_rldicl row: disasm total got=0] [ppc_rldicl row: cr parsed got=0] [ppc_rldicl row: sh63 rldicl got=0] [ppc_rldicl row: sh32 rldicl got=0] [ppc_rldicl row: rc cr0 got=0] [ppc_rldicl rows green got=5] [ppc_rldicl rows red got=19] [ppc_rldicl score 24/24 got=0]
     log tail: FAILING: live, seed holds, src intact, disasm xcheck, zx32 rldicl, zx32 rldicr, rot8 rldicl, rot8 rldicr, neg apparatus, bits32 live, bits32 rld bad, vacuous cell, vac neighbour, census wrong, disasm 
NULLMEDIUM_DONE
```

## 5. Still owed, and where I may be fooling myself

* **Gate 13 has not run in full.**  It runs ALONE after this pass; nothing ships before it does.
* The ledger notes, the CHANGELOG block and the new LOW row (F11) are not written yet.
* F9 rests on a judgement that a gate block need not re-derive a probe's verdicts.  If you think one or two value
  anchors in the block (for example `rc cr0`'s got column) are cheap enough to owe, say which and why.
* D2 is the ruling I am least sure of: I am discharging a row's half with a medium the row did not name.
* "The probe's AST is identical to HEAD's" held after pass 1; after this repair it does NOT -- one printed note string
  changed (F2).  The verdict logic is untouched; the final green run and the controls are the evidence.

## 6. Questions

**Q1.**  Adjudicate F1..F13 and D1..D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each, with a reason.
**Q2.**  WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?  I accepted or refined eleven of thirteen; that is a suspicious
number, and agreement is not evidence.
**Q3.**  WHAT DID ALL OF US MISS?  You now have the whole panel's output.
**Q4.**  Is any repair in section 3 itself wrong -- a new false sentence, a citation that does not resolve, a qualifier
that over- or under-states its receipt?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q4.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
