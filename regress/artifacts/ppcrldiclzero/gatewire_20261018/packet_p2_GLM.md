**Your token: `GLM_RLDICLWIRE2_20261018`** -- open your answer with it.

# Wiring `regress/ppc_rldicl_probe.py` into gate 13 -- #565, pass 2 on the diff

**Please do not simply ratify.**  A recent panel had seven of nine seats confirm a premise its brief stated wrongly, and
this round's own pass-1 brief carried a transcription error that two seats caught.  Check the premises against the files,
not just the reasoning.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; ignore any other `src/` you find.
READ-ONLY: write nothing to any project tree.

**Which text is authoritative.**  `regress/gate_ppc.sh`, `regress/ppc_rldicl_probe.py` and `tools/precommit_check.sh` in
the working tree are exactly this round's edit (`git diff HEAD -- <file>` shows only it).  `tools/pipeline/check_probe_wiring.py`
in the working tree ALSO carries another session's uncommitted lines (MANIFEST entries for probes it has not committed);
the diff in section 2 is HEAD -> what this commit stages, and it is the authority for that file.  Every other dirty file
belongs to that other session: ignore it.

## 0. What the round does, and what pass 1 changed

Section R (`tools/pipeline/check_probe_wiring.py`) holds `ppc_rldicl_probe.py` -- `#522`'s 24-row detector for `rldicl`
writing zero on every execution -- in its EXEMPT table, dated 2026-10-22; with `d < today` it first refuses EVERY commit on
2026-10-23.  This round wires the probe into `regress/gate_ppc.sh` (gate 13) and deletes the exemption.  Witness kind
`harness:` -- the round's subject is the test apparatus.  Pass 1 (Astra, Grok 4.7, GLM 5.3) raised 14 flags; every one was
taken or settled by a measurement:

| # | seat | pass-1 flag | disposition |
|---|---|---|---|
| 1 | Astra, GLM | the brief's transcript of `naive fix wrong` was truncated at `M_NOM`, dropping ` ok` | a PACKET error: the probe prints the whole row (`...see M_NOMASK ok`); this brief inlines its receipts mechanically |
| 2 | Astra | no control isolates the SCORE check; an appended contradictory `SCORE 0/24` would pass | TAKEN: a `score lines` check counts EVERY `^SCORE ` line (must be 1) beside `score 24/24`; controls V8-V11 |
| 3 | Astra | refusal date one day early -- `d < today`, so 2026-10-22 is still valid | TAKEN; MEASURED by legs H1/G1 (`--today 2026-10-23`) |
| 4 | Grok | the whole block truncates `$RLCLOG` before the `if`, so a doctored log is never scored | TAKEN: controls source ONLY the text after the exec line; the 23-row doctor keeps exactly one DONE |
| 5 | Grok | section R's STALE EXEMPTION and UNWIRED DETECTOR legs not named | TAKEN; MEASURED (legs S, U) |
| 6 | Grok | the 24s were quoted and the label was `rows emitted`, invisible to section U | TAKEN: `check "ppc_rldicl rows run" "$rlcrun" 24`, unquoted; manifest 33 -> 34 |
| 7 | Grok | the MANIFEST comment would still say `EXEMPT below rather than wired`; prior discharges leave a DISCHARGED note | TAKEN: both notes, section 2b |
| 8 | GLM | section R's wiring test not settle-able from the packet | settled by MEASUREMENT (legs G/S/U) |
| 9 | GLM | the mk48 manner claim was asserted, not evidenced | settled by reading `gate_arm.sh`'s mk48 block: sentinel, every row by name, counts |
| 10 | GLM | "re-dated once" undercounts (2026-09-24 and 2026-10-09) | TAKEN: "re-dated twice by owner ruling" |
| 11 | GLM | the exemption text's RESULT/CONTROL sentences read as contradictory | moot: the tuple and its comment are deleted |
| 12 | GLM | no duplicated-row control; no stated scope for a stalled probe | TAKEN: V7; the block comment states the probe's own 90 s / 60 s subprocess backstops |
| 13 | GLM | same-commit companions (count pins, manifests, title) not settle-able | settled: section U's manifest is the one (row 6); nothing pins the title or the check count |
| 14 | GLM | the 24 (count-of-rows) premise rests on every row ending ok/FAIL | settled with row 1: all 24 rows end ` ok` in the green log |

## 1. Settled premises (each with its warrant; challenge any you can refute)

* `regress/lib.sh`: `count` is `grep -ac -- "$2" "$1"` (0 for an absent file); `check` compares its 2nd and 3rd arguments as
  strings, exactly.
* Section U (`tools/pipeline/check_score_claims.py`) sees a pin only in the form
  `check\s+"(\S+)\s+rows\s+run"\s+"[^"]*"\s+(\d+)` -- an UNQUOTED literal and an actual with no `"` inside -- and its stem
  (`ppc_rldicl`) selects `<stem>_probe.py`, whose DOCSTRING it then checks for `n/m` score claims against the pin.
  `tools/precommit_check.sh` pins the number of such probes by EQUALITY (`SCORE_CLAIMS_MANIFEST`), so a new pin raises it.
* Section R recognises wiring by an exec site -- `python3 -u <probe>.py` in command position in a `regress/gate_*.sh`; a
  wired probe that keeps a tuple is `STALE EXEMPTION`, an unwired one without a tuple is `UNWIRED DETECTOR`.
* Nothing pins gate 13's title or check count: `grep -rn 'gate 13' tools/ regress/*.sh regress/*.py` finds only comments,
  and `regress/run.sh`'s `GATE_MANIFEST=16` counts gates, not checks.

## 2. The diff -- four files (9 hunks)

### 2a. `regress/gate_ppc.sh`

```diff
--- a/regress/gate_ppc.sh
+++ b/regress/gate_ppc.sh
@@ -95,7 +95,7 @@ set -u
 cd "$(dirname "$0")"
 . ./lib.sh
 
-gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi"
+gate_begin "gate 13: PowerPC FP conversion + FPSCR (#304/#305/#324-#330) + rlwimi/rldimi/rldicl"
 
 PMAX=${PMAX:-$ROOT/build/gxemul}
 LOG=$LOGDIR/gate_ppc.log
@@ -159,6 +159,38 @@ else
     check "rldimi protocol parsed" "no" "yes"
 fi
 
+# ---- ppcrldiclzero (#522) + #565: X(rldicl) wrote ZERO on every execution -- its 24-row detector --------
+# Shipped EXEMPT with e777ff06 (2026-09-10) and re-dated twice by owner ruling (2026-09-24 with the
+# other nine, then 04f3e7c0 on 2026-10-09) because no block here scored it; #565 discharges that
+# exemption.  BEFORE the NetBSD prerequisite for the reason the rlwimi block gives: `-E bareppc -M 64`
+# needs no image, so a red row is recorded first.  A stalled guest cannot hang the gate: the probe's
+# own subprocess backstops (90 s; 60 s for the bogus-machine and 32-bit sessions) turn it into
+# failing rows.  The probe prints no RESULT/CONTROL protocol, so it is scored as gate_arm.sh scores
+# mk48's: its completion sentinel, then EVERY row by name, then the run/green/red counts and its own
+# SCORE line, each pinned to a literal so a shrunk or renamed table cannot pass -- 30 checks when
+# green.  Names sit in a %-18s column and none is longer than 15, so `^name  ' cannot match a
+# neighbour (the padded-column trap).  The rows-run line is in the form check_score_claims.py pins.
+RLCLOG=$LOGDIR/ppc_rldicl.log
+python3 -u ppc_rldicl_probe.py "$PMAX" gate > "$RLCLOG" 2>&1 || true
+if [ "$(grep -cx 'PPC_RLDICL_PROBE_DONE' "$RLCLOG")" != 1 ]; then
+    note "ppc_rldicl: completion sentinel missing or duplicated; last lines follow"
+    tail -5 "$RLCLOG" | sed 's/^/       /'
+    check "ppc_rldicl probe completed" "no" "yes"
+else
+    check "ppc_rldicl probe completed" "yes" "yes"
+    for v in "session" "live" "seed holds" "src intact" "disasm xcheck" "zx32 rldicl" "zx32 rldicr" "rot8 rldicl" "rot8 rldicr" "naive fix wrong" "neg apparatus" "bits32 live" "bits32 rld bad" "vacuous cell" "vac neighbour" "census run" "census wrong" "census zero" "disasm total" "cand session" "cr parsed" "sh63 rldicl" "sh32 rldicl" "rc cr0"; do
+        check "ppc_rldicl row: $v" "$(count "$RLCLOG" "^$v  .*ok$")" "1"
+    done
+    rlcok=$(count "$RLCLOG" " ok$"); rlcbad=$(count "$RLCLOG" " FAIL$"); rlcrun=$((rlcok + rlcbad))
+    check "ppc_rldicl rows run"   "$rlcrun" 24
+    check "ppc_rldicl rows green" "$rlcok" 24
+    check "ppc_rldicl rows red"   "$rlcbad" 0
+    #  EVERY SCORE line is counted, then the one is read: counting only `SCORE 24/24' lines let an
+    #  appended contradictory `SCORE 0/24' pass (GPT-6 Astra, pass 1).
+    check "ppc_rldicl score lines"  "$(grep -c '^SCORE ' "$RLCLOG")" "1"
+    check "ppc_rldicl score 24/24"  "$(grep -c '^SCORE 24/24 ' "$RLCLOG")" "1"
+fi
+
 need_file "$IMAGES/netbsd401-macppc-GENERIC"
 
 note "binary : $PMAX"
```

### 2b. `tools/pipeline/check_probe_wiring.py` (HEAD -> the staged text)

```diff
--- a/tools/pipeline/check_probe_wiring.py
+++ b/tools/pipeline/check_probe_wiring.py
@@ -1699,6 +1699,9 @@ MANIFEST = {
     #  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] the PowerPC gates
     #  historically drove 32-bit parts before gate_ppc.sh wired 64-bit ppc_rldimi_probe.py.  (hcheckprobewiring:F11:
     #  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
+    #  [#565, 2026-10-18] WIRED: gate_ppc.sh (gate 13) now runs it and scores every row by name, with its run, green,
+    #  red and SCORE counts pinned; its EXEMPT entry is DISCHARGED below.  "EXEMPT below rather than wired" above is
+    #  historical.
     "ppc_rldicl_probe.py":
         (CLASS_DETECTOR, "ppcrldiclzero (#522): 24 rows on unmodified -E bareppc.  A 190-cell (SH,MB) census, value rows at SH 0/8/32/63, a record-form CR0 row, a deliberately-vacuous cell showing where the vacuity boundary is, a negative-apparatus control asserting its own liveness oracle CAN go red, and a disassembler cross-check of every placed word.  BASE 24/24, whole-file pre-fix leg 16/24 (clause (a); 'null medium' until 2026-10-09, 7n-1), EIGHT mutants 16-23/24, ZERO ESCAPES (killtable_20260910/t2/SCORES.txt)"),
 
@@ -3168,6 +3171,9 @@ EXEMPT = {
     #  fbpending_drain_probe.py's exemption is DISCHARGED, 2026-09-24 (#548) -- wired into
     #  gate_arm.sh beside footbridge_sites_probe.py, all four timers, --expect-cap 762.
     #  Deleted in the SAME edit as the wiring, for the same reason.
+    #  ppc_rldicl_probe.py's exemption is DISCHARGED, 2026-10-18 (#565) -- wired into gate_ppc.sh beside the
+    #  rlwimi/rldimi blocks on the same -E bareppc -M 64, every row scored by name.  It came due 2026-10-22 after
+    #  two re-dates by owner ruling.  Deleted in the SAME edit as the wiring, for the same reason.
     #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
@@ -3192,29 +3198,6 @@ EXEMPT = {
     "wdc_addtoinbuf_probe.py":     ("2026-12-03",
                                     "two-leg differential AND needs a poisoned CD "
                                     "image the battery does not build"),
-    #  #522's detector.  Single-leg, 0.2 s, green on the fix.  It lacks a gate that RUNS a
-    #  64-bit PowerPC CPU: gate 9 constructs them but has no result oracle, and both PowerPC
-    #  gates drive a 32-bit part.  Closing that is a harness round, filed to wiringcliff.
-    #  *** ITS REASON EXPIRES WITH THE rlwimi/rldimi WIRING: gate_ppc.sh now EXECUTES -M 64. ***
-    #  What remains is a gate block: this probe prints ok/FAIL rows, `SCORE n/m' and a DONE line, which a
-    #  gate can score by rows, as gate_arm.sh scores mk48's; it prints no RESULT/CONTROL lines, and adding
-    #  them is one way to write that block, not a prerequisite for it.  (This said "What remains is the
-    #  instrument: this probe prints no RESULT/CONTROL lines", and before #550 went on "so a gate could only
-    #  score its exit status" -- both false: GPT-6 Astra, late on the F2b pass.)
-    #  #550 (2026-09-25, re-dated individually by owner ruling 2026-09-24): the cheapest of
-    #  the ten -- 24/24 in under a second on a machine gate_ppc.sh already runs (the run:
-    #  regress/artifacts/exemptredate_20260925/opus550_measured_p2/p1_runs/); owed: a gate_ppc.sh block
-    #  beside rldimi/rlwimi, scoring its rows -- or RESULT/CONTROL lines, then that block.  None of
-    #  want_rldimi, want_rlwimi, want_rlwinm or mask32 is called outside the helpers' own definitions
-    #  (grep -nE '(want_rldimi|want_rlwimi|want_rlwinm|mask32)[(]' on the probe), so an edit of them
-    #  is no prerequisite.
-    #  Re-dated 2026-10-08 -> 2026-10-22 on 2026-10-09 by owner ruling, in its own commit: it came due with its
-    #  gate_ppc.sh block still owed and refused every commit.  A re-date is not a discharge.
-    "ppc_rldicl_probe.py":         ("2026-10-22",
-                                    "gate_ppc.sh now executes -M 64 (rlwimi/rldimi); owed: a "
-                                    "gate_ppc.sh block scoring its ok/FAIL rows as gate_arm.sh "
-                                    "scores mk48's -- RESULT/CONTROL lines first is a chosen "
-                                    "approach, not a prerequisite; filed to wiringcliff"),
     #  #520's detector.  NOT a two-leg differential and not awaiting a design -- it is a
     #  single-leg 15-row instrument that runs green on the fix today.  What it lacks is a
     #  HOME: no gate in this tree runs an Alpha guest session -- gate 9's sweep constructs alphabook1
```

### 2c. `tools/precommit_check.sh`

```diff
--- a/tools/precommit_check.sh
+++ b/tools/precommit_check.sh
@@ -345,7 +345,9 @@ elif out=$(python "$SCORECHK" 2>&1); then
 	#  2026-09-13, re-telling this history with #529 in the 29 -> 30 slot).
 	#  RAISED 32 -> 33 ON 2026-10-09, DELIBERATELY.  One newly gated probe: arm_msrmode_probe.py
 	#  (#562, pinned UNQUOTED in gate_arm.sh at 47 rows).
-	SCORE_CLAIMS_MANIFEST=33
+	#  RAISED 33 -> 34 ON 2026-10-18, DELIBERATELY.  One newly gated probe: ppc_rldicl_probe.py
+	#  (#565, pinned UNQUOTED in gate_ppc.sh at 24 rows).
+	SCORE_CLAIMS_MANIFEST=34
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
 		bad "check_score_claims printed no SCORE_CLAIMS_PINNED line -- the count cannot be pinned"
```

### 2d. `regress/ppc_rldicl_probe.py` -- comment-only (its AST, docstring excluded, is identical to HEAD's)

Pinning the probe made section U read its docstring, and U then FAILED the tree:
`STALE  ppc_rldicl_probe.py docstring  claims 16/19, pin is 24 (if that is a deliberate historical quote, write '19-row'
on the same line)`.  The edit qualifies that claim, deletes the SECOND of two verbatim copies of `WHY THE SIBLING ROWS ARE
NOT HERE` (`git show e777ff06:regress/ppc_rldicl_probe.py | grep -c 'WHY THE SIBLING ROWS'` is 2), and corrects the
surviving copy's `THIS FILE HAS 19 ROWS, NOT 24` in place.

```diff
--- a/regress/ppc_rldicl_probe.py
+++ b/regress/ppc_rldicl_probe.py
@@ -23,7 +23,9 @@ pass-2 seat caught it still standing here after the product comment was correcte
   * replacing the `&' with `|' ships ROTL64(rS,SH) | MASK(MB,63), an OR where the
     architecture says AND -- 126 of 190 cells wrong.  That is the M_NAIVE leg.
   * deleting the `& tmp2' outright, ON THE FIXED CODE, ships ROTL64 ALONE with the
-    mask IGNORED -- 16/19, measured as M_NOMASK by the pass-2 seat.  (Before the fix
+    mask IGNORED, measured as M_NOMASK -- 16/19 on the 19-row instrument (the pass-2
+    seat: artifacts/ppcrldiclzero/pass2_20260910/opus_nomask.log) and 19/24 on the
+    24 rows it carries now (killtable_20260910/t2/probe_M_NOMASK.raw).  (Before the fix
     it would have shipped the OR, because the mask was in `tmp'; witness_naive.out
     measured THAT function, not this one.)
 *** THE `naive fix' ROW BELOW IS AN ARITHMETIC IDENTITY OVER THIS FILE'S OWN
@@ -539,6 +541,13 @@ row("disasm total", "%d/%d" % (disasm_ok, disasm_checked),
 #  of this note carried the witness's own post-fix count straight across, which a
 #  pass-2 seat caught.  It is 19/19 on the fix and 14/19 pre-fix
 #  (killtable_20260910/SCORES.txt).
+#  [#565, 2026-10-18: TRUE OF THE 19-ROW FILE IT DESCRIBED, AND FALSE SINCE PASS 2 -- the
+#  five rows under `ROWS ADDED BY PASS 2' below make it 24, which gate_ppc.sh now pins:
+#  24/24 on the fix and 16/24 on the pre-fix HEAD (killtable_20260910/t2/SCORES.txt),
+#  16/24 again on a pre-#522 build at #565 (gatewire_20261018/controls/
+#  rldicl_prefix_02af7f3e.log).  The 19-row figures are in killtable_20260910/t1/SCORES.txt;
+#  the bare `killtable_20260910/SCORES.txt' above names no file.  This block also stood
+#  here TWICE, verbatim, from e777ff06 until #565 deleted the copy after the pass-2 rows.]
 
 # ================== ROWS ADDED BY PASS 2, WHICH FOUND TWO TOTAL ESCAPES =========
 #
@@ -585,27 +594,6 @@ row("sh32 rldicl", hex(xregs.get(11, -1)), hex(want_rldicl(RS_VAL, 32, 32)),
 row("rc cr0", hex(_crv), hex(0x40000000),
     "rldicl. -> CR0=GT.  defect gives EQ(0x2...), update_cr0(cpu,tmp) gives LT(0x8...)")
 
-# ================================ WHY THE SIBLING ROWS ARE NOT HERE =============
-#
-#  The witness this file is derived from is a FAMILY instrument: it also rows
-#  X(rldimi) and X(rlwimi), which carry their OWN measured defects (ppcrldimimask,
-#  ppcrlwimiwidth) that #522 does not touch and must not touch.  Shipping those rows
-#  in a DETECTOR would make it PERMANENTLY RED until two unrelated rounds land --
-#  a detector that cannot be green is a different fault from the one it was written
-#  to catch, and a gate row over it would have to be ignored, which is how a gate
-#  stops being read at all.
-#
-#  So this detector is scoped to X(rldicl).  The three sibling rows stay in the
-#  witness at regress/artifacts/ppcrldiclzero/, which is the EVIDENCE for those two
-#  filed rows and is correctly red there.  When either is fixed, its rows move here
-#  or into a detector of its own -- that is a decision for those rounds, not this one.
-#
-#  MEASURED: witness 19/27 committed and 24/27 fixed, the five flipped rows being
-#  exactly the ones kept below.  **THIS FILE HAS 19 ROWS, NOT 24** -- an earlier draft
-#  of this note carried the witness's own post-fix count straight across, which a
-#  pass-2 seat caught.  It is 19/19 on the fix and 14/19 pre-fix
-#  (killtable_20260910/SCORES.txt).
-
 #  =============================== CONTRACT (clause (e)) =========================
 #
 #  WHAT THIS DETECTOR IS DESIGNED TO CATCH, and what it is NOT.  The boundary below
```

## 3. Measured (receipts under `regress/artifacts/ppcrldiclzero/gatewire_20261018/`)

**3a. The block's scoring text on doctored logs** (`controls/controls_wtblock_20261018.out`): everything after the exec line
is extracted from `regress/gate_ppc.sh` -- the text that ships -- and sourced against copies of a green log
(`rldicl_once_build_20261018.log`, `build/gxemul` of 2026-10-17 22:14) and a PRE-FIX log (a pre-`#522` build at
`02af7f3e`, `controls/rldicl_prefix_02af7f3e.log`, SCORE 16/24):

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

**3b. Section R** (`controls/r_legs/R_LEGS.out`): G = staged checker + wired gate; S = HEAD checker (tuple kept) + wired
gate; U = staged checker + exec line commented out (in place, restored, `cmp`-clean); H0/H1 = HEAD checker + exec line
commented, today and `--today 2026-10-23`; G1 = G with `--today 2026-10-23`:

```
G   PROBEWIRING_PASS  76/85 detectors run by a gate, 9 dated-exempt, 44 witnesses correctly ungated
S   PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
        FAIL  STALE EXEMPTION  ppc_rldicl_probe.py is RUN by gate_ppc.sh:174 and still carries an exemption dated 2026-10-22 -- the debt is paid, delete the line
      PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
G1  PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
        FAIL  EXPIRED EXEMPTION  alpha_tbi_probe.py came due 2026-10-22 (today 2026-10-23) and is still run by no gate
      PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
U   PROBEWIRING_FAIL  1 problem(s); 75/85 detectors run by a gate, 9 dated-exempt
        FAIL  UNWIRED DETECTOR  ppc_rldicl_probe.py is run by NO gate and has no dated exemption.
      PROBEWIRING_FAIL  1 problem(s); 75/85 detectors run by a gate, 9 dated-exempt
H0  PROBEWIRING_PASS  75/85 detectors run by a gate, 10 dated-exempt, 44 witnesses correctly ungated
H1  PROBEWIRING_FAIL  2 problem(s); 75/85 detectors run by a gate, 10 dated-exempt
        FAIL  EXPIRED EXEMPTION  alpha_tbi_probe.py came due 2026-10-22 (today 2026-10-23) and is still run by no gate
        FAIL  EXPIRED EXEMPTION  ppc_rldicl_probe.py came due 2026-10-22 (today 2026-10-23) and is still run by no gate
      PROBEWIRING_FAIL  2 problem(s); 75/85 detectors run by a gate, 10 dated-exempt
restore: gate_ppc.sh cmp-clean against its backup; exec lines 1 (r_controls.sh stdout, 2026-10-18 07:5x)
```

**3c. Section U** (`controls/score_claims_u_20261018.out`): `SCORE_CLAIMS_PINNED=34`, `SCORE_CLAIMS_PASS`.  The other
session's uncommitted `gate_sh_rounding.sh` re-pins an EXISTING stem (`gdrom_default` 60 -> 62), so 34 holds in the staged
tree as well.

**3d. Floor clause (c), the null medium** (`nullmedium/NULLMEDIUM.out`): the edited probe run exactly as the gate runs it,
against an ABSENT binary and a NON-EMULATOR one (`/bin/true`), each log scored by the extracted block:

```
probe: f10981863532d115a51775bac2139b2f  regress/ppc_rldicl_probe.py
gate:  6fc4735f68dcf0c44cddb142f94568ea  regress/gate_ppc.sh
LEG absent  binary=/nonexistent/gxemul  probe_rc=1     0s  gate checks=1   fails=1   RED (clause c holds)
     red: [ppc_rldicl probe completed got=no]
     log tail:                ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/gxemul'|
LEG nonemu  binary=/bin/true            probe_rc=0     0s  gate checks=30  fails=22  RED (clause c holds)
     red: [ppc_rldicl row: live got=0] [ppc_rldicl row: seed holds got=0] [ppc_rldicl row: src intact got=0] [ppc_rldicl row: disasm xcheck got=0] [ppc_rldicl row: zx32 rldicl got=0] [ppc_rldicl row: zx32 rldicr got=0] [ppc_rldicl row: rot8 rldicl got=0] [ppc_rldicl row: rot8 rldicr got=0] [ppc_rldicl row: neg apparatus got=0] [ppc_rldicl row: bits32 live got=0] [ppc_rldicl row: bits32 rld bad got=0] [ppc_rldicl row: vacuous cell got=0] [ppc_rldicl row: vac neighbour got=0] [ppc_rldicl row: census wrong got=0] [ppc_rldicl row: disasm total got=0] [ppc_rldicl row: cr parsed got=0] [ppc_rldicl row: sh63 rldicl got=0] [ppc_rldicl row: sh32 rldicl got=0] [ppc_rldicl row: rc cr0 got=0] [ppc_rldicl rows green got=5] [ppc_rldicl rows red got=19] [ppc_rldicl score 24/24 got=0]
     log tail: FAILING: live, seed holds, src intact, disasm xcheck, zx32 rldicl, zx32 rldicr, rot8 rldicl, rot8 rldicr, neg apparatus, bits32 live, bits32 rld bad, vacuous cell, vac neighbour, census wrong, disasm 
NULLMEDIUM_DONE
```

On `/bin/true` five rows stay GREEN: `session` and `cand session` test exit status only; `naive fix wrong` is the
arithmetic identity the docstring already calls carried-not-counted; `census run` counts the cells the PROBE drives, not
results; `census zero` counts parsed zero results, so it is vacuous when nothing parses (and `census wrong` reds there).
My disposition: not a floor breach -- the gate reds on 22 checks -- recorded as detector hygiene.

**Not yet run:** gate 13 in full, alone, after this pass.

## 4. Questions

**Q1 (the ask-again).**  What is the SMALLEST edit -- to the new block, or to the probe -- that keeps the block green on the
current build's log while letting a broken `rldicl` (the pre-`#522` defect, or `t2`'s mutants: M_SH5, M_MB5, M_CR0,
M_NOMASK, M_MASKEND, M_NOAND) pass the gate?  Name the edit and the log line that would carry it through.
**Q2 (the probe's records).**  Are the three comment edits in 2d right against their receipts --
`pass2_20260910/opus_nomask.log:3` (`SCORE 16/19 ... label=M_NOMASK`), `killtable_20260910/t2/probe_M_NOMASK.raw:30`
(`SCORE 19/24`), `killtable_20260910/t2/SCORES.txt` (BASE 24/24, HEAD 16/24) and the `02af7f3e` log?  Was deleting the
duplicate the right disposition, rather than correcting both copies?  Is any OTHER sentence in the probe false now that a
gate pins it at 24 rows?
**Q3 (the checker's records).**  Are the MANIFEST note and the DISCHARGED note in 2b accurate, and placed as the earlier
discharges (`mk48` `#536`, `fbpending` `#548`) were?  Does anything else in that file name `ppc_rldicl` and become false?
**Q4 (clause (c)).**  Is any of the five rows green on `/bin/true` the SOLE carrier of a kill a real broken build needs --
i.e. would a mutant that also blinds the other rows slip through because that row is vacuous on no results?
**Q5 (same-commit completeness).**  Anything that must change in this commit and does not?  Two pre-existing nits are NOT
in the diff and I propose filing, not fixing: section R's advisory `SELFLABEL` note (the probe's first docstring line says
`RUNG-3 WITNESS` while the MANIFEST says detector) and the usage string naming `ppc_rldicl_witness.py`.  Fix or file?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q5.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
