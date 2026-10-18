**Your token: `GROK_IP30WIREF2_20261018`** -- open your answer with it.

# #566 -- wiring `ip30_abort_probe.py` into gate 14: F2, the shared-findings pass

**This is the adjudication pass: every seat's pass-2 findings, my disposition of each, the repair, and the receipts
re-run on the repaired bytes.  Please do not simply ratify** -- the question that matters is which of my dispositions is
WRONG.  A seat reviewing its own finding: be harder on it, and on whether my FIX of it is right.  A seat whose finding I
rejected: say whether the rejection holds.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD 2036a3d5;
ignore any other `src/`.  READ-ONLY: write nothing to any project tree.  Pass 2 was GPT-6 Astra (9 flags), GLM 5.3 (5)
and Grok 4.7 (12); Fable 5.1 was not tried on pass 1 or pass 2 -- an omission against the owner's 2026-10-17 directive
(one try per pass) -- and is tried on this one.

## 0. Settled premises (each with its warrant)
* The block's scoring text is extracted from `gate_arm.sh` (everything after the probe's exec line through `fi`) and
  sourced against logs; `count` is `lib.sh`'s (`grep -ac`, 0 for an absent file).  The probe's AST with its module
  docstring excluded is identical to HEAD's (re-checked after every edit, last after the repairs below).
* `session()` (ip30_abort_probe.py) reads the transcript during settle, per-command and spin waits only; after spin it
  polls `waitpid(WNOHANG)` for 12 s without reading, then `os.kill(SIGKILL)` and a blocking `os.waitpid(pid, 0)`, and
  returns `alive=True` for a child it killed.  `kill 20 rd`/`kill 28 rd` each score their `txt` row from the same session;
  so do the three write arms and `tick 50`; `xbit isr` and `xbit tick` share one; `tick 49`, `acc 30 rd` and each of
  the six count rows the block names are sessions of their own.
* Kill table 5 (33 rows): base 33/33, V1_assign20wr 32/33 (`xbit rev` red), V2_assigntick 32/33 (`xbit rev2` red), V8_len4
  33/33.  Kill table 4 (32 rows): V2_assigntick 32/32 -- the escape `xbit rev2` was added for.

## 1. Pass-2 findings and my dispositions -- which is WRONG?

| # | finding (seat) | disposition |
|---|---|---|
| A1 | the block's opening comment says every arm "declined with a latched announce" (Astra; Grok K1) | TAKEN: loads decline silently, 0x10020/0x10028 stores keep their effect, the 0x10030 store is dropped, the three stores announce once between them and the tick once |
| A2 | the parse comment says a crash or killed run "leaves none and reds here"; a death AFTER the report passes it (Astra) | TAKEN: it now says the exit-status check catches that (selftest n11) |
| A3 | the probe note put both escapes under DOES NOT CATCH; the counter one is under MEASURED ESCAPES (Astra) | TAKEN |
| A4 | the pin comment says U reads only `#` lines; `comment_lines()` takes `#`, `*` and `//` (Astra) | TAKEN |
| A5 | the CONTRACT's "every CATCH below has a MEASURED kill in killtable{,2}" is unsupported for reinstating the four `abort()` calls (Astra) | TAKEN: a note bullet -- that CATCH rests on the pre-fix build (clause (a)); no table holds a fixed-file reinstatement (clause (b)) |
| A6 | the stall disclosure misses partial execution and output printed during the poll (Astra; Grok K4) | TAKEN: rewritten; and FILED as `ip30stallgreen` (LOW): on V2_assigntick a stall before `xbit rev2`'s second ISR store leaves all 41 checks green |
| A7 | the ledger rows still carry superseded status (Astra) | TAKEN: `wiringcliff` and `ip30abortkill` state notes in this commit; the 33-row pair added beside the 21-row witness |
| A8 | the held flagship work has no queue entry (Astra) | TAKEN, see D3: #566's Fable stages become HELD markers with a `hold_question`, the queue regenerated; today's eight `NOT FIRED` fable5 entries on seven rows FILED as `fableheldform` (MED), since an untokened note counts as an ANSWER to `stage_tokens.is_answer()` |
| A9 | my pass-1 rejection of GLM's g3 claimed every wait is bounded; the reap after SIGKILL blocks (Astra; Grok K3) | TAKEN: corrected, and the block comment now says nothing times the probe out |
| L1 | "568 s ... #550 and #566 each measured it"; #566's leg measured 567 s (GLM; Grok K2) | TAKEN: "568 s on build/gxemul (#550), 567 s on a HEAD rebuild (#566)" |
| L2 | the CHANGELOG describes five of the six section R legs (GLM) | TAKEN: G1 described (wired, `--today 2026-10-31`: only the other session's four expiries) |
| L3 | the seat headcounts do not reconcile with the disposition rows (GLM) | TAKEN: the rows were grouped; Astra's pass 1 had 4 FLAGs (A1-A4) plus a controls list; GLM's 11 FLAGs had four without a row -- S4's U mechanism (as G1), the commit staging of the dirty checker (the commit copy is HEAD + #566's hunks), the S5/Q6 MANIFEST "contradiction" (REJECTED: Q6 listed candidates) and the gatewire dir (committed with the round) |
| L4 | the section R receipt cannot be tied to the diff's bytes (GLM) | TAKEN: re-run on the final gate, md5 recorded (section 3) |
| L5 | the 2a and 2d hunks show one added line fewer than their headers (GLM) | REJECTED: both diffs were inlined byte-for-byte (checked by substring match): 67 added + 6 context = 73, and 6 + 6 = 12 |
| K5 | the note's "`xbit rev2` after V2_assigntick scored 32/32 there" reads as xbit rev2 scoring 32/32 (Grok) | TAKEN: reworded |
| K6 | "ten cells, all rowed (THE LATCH-AXIS CLASS CLOSURE)" -- that section has no `xbit rev2` (Grok) | TAKEN: ten enumerated and rowed there; a measured escape then added `xbit rev2` |
| K7 | the note said the CONTRACT "was not updated" -- its DOES NOT CATCH was (Grok) | TAKEN |
| K8 | the note missed "All FIVE ISR sites" and THE CLAIM UNDER TEST (Grok) | TAKEN: two bullets; the CLAIM's `kill 30 rd` is the row named `acc 30 rd` in every copy of the probe |
| K9 | 10/33 replaced a red COUNT (13 of 21) (Grok) | TAKEN: "reds 23 of 33 rows, scoring 10/33" |
| K10 | "a scratch clone of build/" (Grok) | REJECTED: `legs/legs566.sh` (now preserved) does `cp -a build /tmp/gx566` and sets five sources to HEAD; build/ untouched |
| K11 | the bug file dates #531's pass 2 to 2026-09-18 (Grok) | TAKEN: pass 2 `panel_20260917_215210` (09-17); F2 and tables 3-5 (09-18); the owed line annotated in place |
| K12 | the bug file required a #527-shaped commit with a new carrier (Grok) | TAKEN in part: the bullet lists what is owed (witness, clause (b)) and leaves the carrier question to the closure, with Grok's "no"; target before the 2026-10-25 battery (GLM's deadline) |

**D3 -- how Fable's stage is recorded.**  Astra: "Record the hold reason and question without firing the held seat."
Grok: "`tools/pipeline/fable_queue.md` has no `#566` line, and this wiring diff creates no queue obligation."  The owner's
2026-10-17 directive: "Fable's stage is recorded as a HELD marker carrying its question ([HELD AWAITING SEAT: fable5]
plus a hold_question) and is answered when the seat comes back.  Still try Fable once per pass ... record a wall as a SEAT
FAILURE, never as agreement."  **Mine: HELD marker + `hold_question` + the regenerated queue, and Fable tried on this
pass.**  D1 (keep `ip30abortkill` in work) and D2 (correct the probe's records here) were upheld by all three seats.

## 2. The repair since pass 2 (pass-2 state -> now)
```diff
--- a/regress/gate_arm.sh (pass 2)
+++ b/regress/gate_arm.sh (now)
@@ -1509,22 +1509,28 @@
 
 #  ---- #566 ip30abortkill (#531, 686d179c): dev_sgi_ip30.c's four guest-reachable abort() calls -- a guest load or
 #  ---- store at 0x0ff10020 or 0x0ff10028, a store to 0x0ff10030, and DEVICE_TICK once a legal imask0 write sets bit
-#  ---- 50 -- have declined with a latched announce since #531.  Its detector shipped with that fix and ran in no gate:
+#  ---- 50 -- are gone since #531: the two loads decline silently, the 0x10020/0x10028 stores keep their effect, the
+#  ---- 0x10030 store is dropped, and the three stores announce once between them (one shared ISR latch) and the tick
+#  ---- once (its own).  Its detector shipped with that fix and ran in no gate:
 #  ---- check_probe_wiring.py held it EXEMPT, dated 2026-09-20 and re-dated three times (eec0f4a3 to 09-27, #550's
 #  ---- 04500deb to 10-15, 7b23b785 on 2026-10-16 to 10-30), and HEAD's checker run with --today 2026-10-31 FAILS on it
 #  ---- (measured 2026-10-18).  This block discharges that exemption.  The probe's CONTRACT, its MEASURED ESCAPES and
 #  ---- its DOES NOT CATCH list are in its header; its kill tables are in regress/artifacts/ip30abortkill/.  At depth 0,
 #  ---- so another probe's missing sentinel cannot swallow it.
 #  ----
-#  ---- RUN TIME, about 9.5 minutes: 568 s for the 33 rows on build/gxemul (#550 and #566 each measured it), because every
+#  ---- RUN TIME, about 9.5 minutes -- 568 s on build/gxemul (#550), 567 s on a HEAD rebuild (#566) -- because every
 #  ---- session that survives waits out the probe's 12 s death poll.  That poll is what stops a slow abort reading as
-#  ---- `alive', so it is not shortened here.  The waits are wall-clock, and a load stall is NOT always a red: a
-#  ---- session the poll kills before its stepped access has run reports `alive', and every row that wants `alive' or
-#  ---- `no' reads it green.  The three write-arm sessions and the bit-50 tick session also score an announce row that
-#  ---- wants `yes', which reds; the `kill 20 rd' and `kill 28 rd' sessions do not -- their `txt' rows want NO announce,
-#  ---- since the read arms decline silently -- so a stalled read session reads GREEN twice on a build that would have
-#  ---- aborted, and a stalled `tick 49' session reads green alone.  gate_arm.sh runs in the weekly battery, alone,
-#  ---- and as an attended targeted gate -- never per commit.
+#  ---- `alive', so it is not shortened here.  Every wait is wall-clock up to that poll's SIGKILL; the reap after it
+#  ---- blocks, and nothing here times the probe out.  A load stall is NOT always a red.  A session the poll kills
+#  ---- reports `alive' with only the transcript read before the poll began (nothing printed during it is collected),
+#  ---- so it reads like a run whose remaining accesses never happened.  Rows that want `alive' or `no' then read green:
+#  ---- `acc 30 rd', `tick 49' and both rows of the `kill 20 rd' and `kill 28 rd' sessions read a stall green outright --
+#  ---- the read sessions on a build that would have aborted -- while the write-arm and bit-50 tick sessions also score
+#  ---- an announce row that wants `yes', which reds.  The count rows that want ONE announce (`latch 1x', `latch 28wr',
+#  ---- `latch 30wr', `latch tick', `xbit rev', `xbit rev2') read a stall before their second access as green; on
+#  ---- V2_assigntick only `xbit rev2' reds, so a stall in that session leaves all 41 checks green on that mutant.
+#  ---- Filed as ip30stallgreen.  gate_arm.sh runs in the weekly battery, alone, and as an attended targeted gate --
+#  ---- never per commit.
 #  ----
 #  ---- Run from its artifacts path, as gate_sh_rounding.sh runs gdrom_pio_null_probe.py; a missing file fails the parse
 #  ---- check below -- a FAIL, never a SKIP.
@@ -1532,8 +1538,8 @@
 ip30rc=0
 python3 -u artifacts/ip30abortkill/ip30_abort_probe.py "$PMAX" gate > "$IP30LOG" 2>&1 || ip30rc=$?
 
-#  PARSE BEFORE SCORE: exactly one well-formed RESULT, CONTROL and DONE line.  A crash, a killed run or a missing file
-#  leaves none and reds here.
+#  PARSE BEFORE SCORE: exactly one well-formed RESULT, CONTROL and DONE line.  A crash or kill before the report, or a
+#  missing file, leaves none and reds here; a death AFTER the report passes here and reds `probe exit status' below.
 if [ "$(grep -c '^IP30ABORT_RESULT=' "$IP30LOG")" != "1" ] ||
    ! grep -Eq '^IP30ABORT_RESULT=(0|[1-9][0-9]*)/(0|[1-9][0-9]*)$' "$IP30LOG" ||
    [ "$(grep -c '^IP30ABORT_CONTROL=' "$IP30LOG")" != "1" ] ||
--- a/regress/artifacts/ip30abortkill/ip30_abort_probe.py (pass 2)
+++ b/regress/artifacts/ip30abortkill/ip30_abort_probe.py (now)
@@ -12,27 +12,38 @@
 the pass-2 class closure.
 
 ================================================================================
-[#566, 2026-10-18 -- a records correction; the CONTRACT below is kept as it was written on
-2026-09-18, for the 27-row instrument.  The file's later sections were updated and this one
-was not.]  The probe that ships has 33 rows, and five statements below are no longer true:
+[#566, 2026-10-18 -- a records correction; the text below it is kept as it was written.]
+The CATCHES list, the fourteen-cell paragraph and "THE CLOSURE IS OWED" below are the 27-row
+instrument's of 2026-09-18; the DOES NOT CATCH list was updated later and is current.  The
+probe that ships has 33 rows, and these statements below are no longer true of it:
   * the F13 silent-decline repair made both READ arms (0x10020, 0x10028) decline WITHOUT an
-    announce, so there are FOUR announce sites, not six, and `kill 20 rd txt' / `kill 28 rd
-    txt' now pin the SILENCE (want `no');
+    announce: there are FOUR announce sites, not six; THREE ISR sites print the shared string,
+    not five (THE ATTRIBUTION RULE); and `kill 20 rd txt' / `kill 28 rd txt' pin the SILENCE
+    (want `no');
   * `latch 1x' was re-aimed onto the two WRITE arms (0x10020-WR, then 0x10028-WR) when the
     read arms went silent;
-  * the latch axis is {4 announce sites} x {announce fires, latch sets} + {2 collision
-    directions} = TEN cells, all rowed (THE LATCH-AXIS CLASS CLOSURE, below);
-  * "THE CLOSURE IS OWED" was DONE in-round: `latch 1x' (0x10020-WR), `latch 28wr', `latch
-    30wr', `latch tick' (ME_nolatchsettick) and `xbit rev' (MA_assign20wr) -- kill table 4,
-    32 rows -- and `xbit rev2' after V2_assigntick (MD's shape) scored 32/32 there; kill table
-    5 then: base 33/33, V1_assign20wr 32/33, V2_assigntick 32/33 (regress/artifacts/
-    ip30abortkill/killtable4_20260918/, killtable5_20260918/).  MF's cell, a latch set on the
-    0x10028 READ, no longer exists: that arm no longer announces;
-  * the pre-fix red is no longer `13 rows': on this instrument the pre-fix build scores 10/33
-    (#566's prefix leg, regress/artifacts/ip30abortkill/gatewire_20261018/legs/probe_prefix.log).
-V7_nocounter (MH's shape, 32/32 in table 4) and the WIDTH axis (V8_len4, 33/33 in table 5)
-remain DISCLOSED, as DOES NOT CATCH says.  Since #566 this probe runs in gate 14
-(regress/gate_arm.sh).
+  * THE LATCH-AXIS CLASS CLOSURE, further down, enumerated TEN cells -- {4 announce sites} x
+    {announce fires, latch sets} + {2 collision directions} -- and rowed them: `latch 1x'
+    (0x10020-WR), `latch 28wr', `latch 30wr', `latch tick' (ME_nolatchsettick) and `xbit rev'
+    (MA_assign20wr), each killing its mutant in kill table 4 (32 rows).  V2_assigntick (MD's
+    shape: the tick's latch set made an assignment) still escaped that table at 32/32, so
+    `xbit rev2' (ISR -> TICK -> ISR) was added; kill table 5 measured base 33/33,
+    V1_assign20wr 32/33 and V2_assigntick 32/33 (regress/artifacts/ip30abortkill/
+    killtable4_20260918/, killtable5_20260918/).  MF's cell, a latch set on the 0x10028 READ,
+    no longer exists;
+  * the pre-fix red is no longer `13 rows': on this instrument the pre-fix build reds 23 of 33
+    rows, scoring 10/33 (#566's prefix leg, clause (a): regress/artifacts/ip30abortkill/
+    gatewire_20261018/legs/probe_prefix.log);
+  * `Every CATCH below has a MEASURED kill in killtable{,2}' overstates the first CATCH:
+    reinstating the four abort() calls rests on the PRE-FIX build (clause (a): the 21-row
+    PREFIX_21row_20260917.out and the 33-row leg above); no table here holds abort()
+    re-inserted into the FIXED file (clause (b));
+  * THE CLAIM UNDER TEST quotes the PRE-FIX dev_sgi_ip30.c (`at HEAD' there meant HEAD before
+    #531), and the row it calls `kill 30 rd' is named `acc 30 rd' in every copy of this probe.
+Two escapes remain DISCLOSED: MH_nocounter (V7_nocounter, 32/32 in table 4), under MEASURED
+ESCAPES below, and the WIDTH axis (V8_len4, 33/33 in table 5), under DOES NOT CATCH.  Since
+#566 this probe runs in gate 14 (regress/gate_arm.sh); a load stall can read green there
+(ip30stallgreen).
 ================================================================================
 THE CONTRACT -- vacuity-floor clause (e).  A detector that says what it catches is
 FALSIFIABLE; one that claims completeness is not.  Every CATCH below has a MEASURED
--- a/tools/precommit_check.sh (pass 2)
+++ b/tools/precommit_check.sh (now)
@@ -349,9 +349,10 @@
 	#  (#565, pinned UNQUOTED in gate_ppc.sh at 24 rows).
 	#  RAISED 34 -> 35 ON 2026-10-18, DELIBERATELY.  One newly gated probe:
 	#  artifacts/ip30abortkill/ip30_abort_probe.py (#566, pinned UNQUOTED in gate_arm.sh at 33 rows
-	#  under the stem ip30_abort).  The checker reads only `#' lines that contain the stem, and only a
-	#  docstring at regress/<stem>_probe.py or regress/<stem>.py; no comment line names ip30_abort and
-	#  the probe lives under artifacts/, so for this pin it checks no prose -- only the pin is counted.
+	#  under the stem ip30_abort).  The checker reads only comment lines (`#', `*' or `//') that contain
+	#  the stem, and only a docstring at regress/<stem>_probe.py or regress/<stem>.py; no comment line
+	#  names ip30_abort and the probe lives under artifacts/, so for this pin it checks no prose -- only
+	#  the pin is counted.
 	SCORE_CLAIMS_MANIFEST=35
 	_spinned=$(printf '%s\n' "$out" | sed -n 's/^SCORE_CLAIMS_PINNED=//p')
 	if [ -z "$_spinned" ]; then
--- a/OUTSTANDING_BUGS.md (pass 2)
+++ b/OUTSTANDING_BUGS.md (now)
@@ -21616,7 +21616,7 @@
 >
 > **The shipped instrument's POST-FIX figure IS measured: 28/28** (`killtable3_20260918/base.raw`, sentinel `IP30ABORT_DONE`).  What is not measured is its PRE-FIX counterpart.  **OWED: one clone build to take PRE-FIX at 28 rows**, which would give a matched pair on the instrument that actually ships.  Deliberately not run while a measuring seat is in flight.  *(The 18-row pair 11/18 -> 18/18 is SUPERSEDED: pass 2 found four defects, and repairing them grew the instrument.  The re-pin's own order proof stays on the 18-row form by design.)*
 >
-> *** [#566, 2026-10-18] THE SHIPPED INSTRUMENT IS **33 ROWS**, AND ITS PRE-FIX COUNTERPART IS NOW MEASURED ON IT. ***  The latch-axis class closure took it 28 -> 32 (kill table 4) -> 33 (`xbit rev2`, kill table 5, base 33/33).  `#566` rebuilt HEAD in a scratch clone with `dev_sgi_ip30.c` set to `686d179c^`'s (all four `abort()` calls back): **PRE-FIX 10/33, POST-FIX 33/33 on the one 33-row instrument** (`regress/artifacts/ip30abortkill/gatewire_20261018/legs/`) -- the matched pair owed above.  The 8/21 -> 21/21 pair is unchanged: a 21-row witness, not a claim about the file that ships.  The "Still owed before close: panel pass 2" line below was discharged on 2026-09-18 by `#531`'s own pass 2, its F2 adjudication (fable5, roster 9/9) and kill tables 3-5.
+> *** [#566, 2026-10-18] THE SHIPPED INSTRUMENT IS **33 ROWS**, AND ITS PRE-FIX COUNTERPART IS NOW MEASURED ON IT. ***  The latch-axis class closure took it 28 -> 32 (kill table 4) -> 33 (`xbit rev2`, kill table 5, base 33/33).  `#566` rebuilt HEAD in a scratch clone with `dev_sgi_ip30.c` set to `686d179c^`'s (all four `abort()` calls back): **PRE-FIX 10/33, POST-FIX 33/33 on the one 33-row instrument** (`regress/artifacts/ip30abortkill/gatewire_20261018/legs/`) -- the matched pair owed above.  The 8/21 -> 21/21 pair is unchanged: a 21-row witness, not a claim about the file that ships.  The "Still owed before close: panel pass 2" line below was discharged by `#531`'s own pass 2 (`_scratchpad/panel_20260917_215210`, 2026-09-17), its F2 adjudication (fable5, roster 9/9, 2026-09-18) and kill tables 3-5 (2026-09-18).
 
 Four guest-reachable `abort()` calls in `dev_sgi_ip30.c` on the advertised `-E sgi -e ip30`.
 **Three `exit(` sweeps of this queue walked past all four**, because `abort()` contains no
@@ -21639,7 +21639,7 @@
 re-pinned oracle was measured on a pre-fix clone — **8/18, those three rows failing** — before
 being trusted.
 
-**Still owed before close: panel pass 2 on the real diff.**
+**Still owed before close: panel pass 2 on the real diff.**  *[#566, 2026-10-18: discharged -- see the dated note at the top of this entry.]*
 
 
 ### `asiceventaddr` -- **A THIRD PARTIAL GUARD IN ONE HEADER, from an unread review.** Recorded
@@ -24950,15 +24950,28 @@
   disposition had made their carrier.  Coverage debt and named measurements; none a floor breach.
 * **`ppcgateimageskip` CLOSED as discharged** -- the rlwimi, rldimi and rldicl blocks run before `need_file` in gate 13.
 
-### 2026-10-18 -- `#566`: `ip30_abort_probe.py` wired into gate 14 (`wiringcliff` stays open; `ip30abortkill` stays in work)
+### 2026-10-18 -- `#566`: `ip30_abort_probe.py` wired into gate 14 (`wiringcliff` stays open; `ip30abortkill` stays in work); two rows filed
 
 * **`wiringcliff` (MED, in work)** -- `#566` wired `regress/artifacts/ip30abortkill/ip30_abort_probe.py` into gate 14
   (`regress/gate_arm.sh`, 41 checks: one parse check, controls, exit status, the 33 rows by name, five pinned counts) and
   deleted its 2026-10-30 exemption.  Next due: `alpha_tbi_probe.py` 2026-10-22 and the three `lca_*` probes 10-23 / 10-26
   / 10-27 (the other session's), then the four `wdc_*` probes 11-05 .. 12-03.
 * **`ip30abortkill` (HIGH, in work)** -- its detector now runs in gate 14, and the pre-fix counterpart on the shipped
-  33-row instrument is measured (10/33 against 33/33).  Still owed before it closes, in a records commit of `#527`'s
-  shape: a carrier row for the two measured escapes (`V7_nocounter` 32/32 in kill table 4; the width axis, `V8_len4`
-  33/33 in kill table 5), a witness field naming the 33-row pair rather than the 21-row one, and an answer to whether
-  `#531`'s clause (b) -- `abort()` re-inserted at each fixed site of the FIXED file -- was ever measured (no kill table
-  holds such a mutant; `#566`'s pre-fix leg is clause (a)).
+  33-row instrument is measured: 10/33, 23 rows red, against 33/33.  Still owed before it closes: the witness field still
+  leads with the 21-row pair (the 33-row pair is added beside it here); clause (b) -- `abort()` re-inserted at each fixed
+  site of the FIXED file, re-run at 33 rows -- is held by no kill table (`#566`'s pre-fix leg is clause (a)); and the
+  closure decides whether the two disclosed escapes (`V7_nocounter`; the width axis `V8_len4` -- both in the row's state
+  note and the probe's CONTRACT) need a carrier that survives the close (Grok 4.7: no).  Target: before the 2026-10-25
+  weekly battery.
+* **`ip30stallgreen` (LOW, open)** -- `ip30_abort_probe.py`'s `session()` returns `alive=True` for a session its 12 s
+  poll kills, holding only the transcript read before the poll; a load stall therefore reads as a run whose remaining
+  accesses never happened.  The kill rows, `acc 30 rd`, `tick 49` and the read arms' `txt` rows read it green, and the six
+  count rows read a stall before their second access as green -- on `V2_assigntick` only `xbit rev2` reds, so a stall in
+  that session leaves all 41 gate-14 checks green.  Repair shape: a per-session completion marker every row requires (a
+  probe change, owing a kill table).  GPT-6 Astra and Grok 4.7, `#566` pass 2.
+* **`fableheldform` (MED, open)** -- seven rows (`mapledmaaddr`, `ppcgateimageskip`, `ppcrldimimask`, `ppcrlwimiwidth`,
+  `sgirandomcolour`, `wiringcliff`, `xscaleinten`) carry eight 2026-10-18 fable5 entries reading `NOT FIRED -- ... held
+  by the owner's 2026-10-17 directive`.  The directive's form is a HELD marker carrying a `hold_question`, queued; an
+  untokened note is an ANSWER to `stage_tokens.is_answer()`, so `check_fable_queue.py` and `check_stage_panels.py` count
+  Fable as having answered and nothing queued the work.  Owed: the eight entries converted to HELD markers with questions
+  and the queue regenerated, in a records commit after `#566`.  Found from GPT-6 Astra's `#566` pass-2 queue flag.
```

## 3. Receipts re-run on the repaired bytes (regress/artifacts/ip30abortkill/gatewire_20261018/)
legs/RESCORE.out (the four leg logs re-scored by the final scoring text; the probe not re-run):
```
gate_arm.sh md5 d3f4dc9793b85ec23cb21cf33216c6f2
scoring text: 42 lines, md5 21d7b87406948ce0c1f69eb03dec0c11
probe md5 now 8a46231609f8806bee52e3028c0a4550 (the legs ran 5bf04f2de35af34d517bd286499d5b98, before #566's docstring note)
LEG base    rc=0 gate checks=41  fails=0   GREEN as required
LEG prefix  rc=0 gate checks=41  fails=26  RED   as required
LEG absent  rc=0 gate checks=41  fails=38  RED   as required
LEG nonemu  rc=0 gate checks=41  fails=38  RED   as required
RESCORE_DONE
```
selftest/SELFTEST.out (16 cases):
```
scoring text: 42 lines, md5 21d7b87406948ce0c1f69eb03dec0c11
n15: python3 on a missing probe file exited 2; log: /usr/lib/python-exec/python3.13/python3: can't open file '/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/regress/artifacts/ip
good            rc=0  checks=41  fails=0   GREEN as-expected
n1_onefail      rc=0  checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: kill 30 wr got=0] [ip30_abort rows green got=32] [ip30_abort rows red got=1]
n2_rowlost      rc=0  checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: tick 49 got=0] [ip30_abort rows emitted got=32] [ip30_abort rows green got=32]
n3_rowdup       rc=0  checks=41  fails=2   RED   as-expected
      red: [ip30_abort row: tick 50 got=2] [ip30_abort row: tick 49 got=0]
n4_dead         rc=0  checks=41  fails=38  RED   as-expected
      red: [ip30_abort controls got=DEAD] [ip30_abort row: live got=0] [ip30_abort row: devsig got=0] [ip30_abort row: acc 18 got=0] [ip30_abort row: acc 30 rd got=0] [ip30_abort row: acc 20000 got=0] [ip30_abort row: acc 30000 go
n5_empty        rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n6_nodone       rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n7_tworesult    rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n8_contra       rc=0  checks=41  fails=3   RED   as-expected
      red: [ip30_abort row: latch tick got=0] [ip30_abort rows green got=32] [ip30_abort rows red got=1]
n9_shrunk       rc=0  checks=41  fails=5   RED   as-expected
      red: [ip30_abort row: xbit rev2 got=0] [ip30_abort rows run got=32] [ip30_abort rows correct got=32] [ip30_abort rows emitted got=32] [ip30_abort rows green got=32]
n10_renamed     rc=0  checks=41  fails=1   RED   as-expected
      red: [ip30_abort row: acc imask got=0]
n11_goodrc1     rc=1  checks=41  fails=1   RED   as-expected
      red: [ip30_abort probe exit status got=1]
n12_twocontrol  rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n13_badcontrol  rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n14_twodone     rc=0  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
n15_noprobe     rc=2  checks=1   fails=1   RED   as-expected
      red: [ip30_abort probe output parses got=no]
SCORE_SELFTEST_DONE
```
controls/R_CONTROLS.out:
```
commit checker md5 07b31a6ce4e19c745b2804b02f284a78; HEAD checker md5 175bf266dc076c17c14f061fffba64cd
HEAD checker == git show HEAD:
gate_arm.sh md5 d3f4dc9793b85ec23cb21cf33216c6f2
G    rc=0  last: PROBEWIRING_PASS  77/85 detectors run by a gate, 8 dated-exempt, 44 witnesses correctly ungated
S    rc=1  last: PROBEWIRING_FAIL  1 problem(s); 77/85 detectors run by a gate, 8 dated-exempt
        18:  FAIL  STALE EXEMPTION  artifacts/ip30abortkill/ip30_abort_probe.py is RUN by gate_arm.sh:1539 and still carries an exemption dated 2026-10-30 -- the debt is paid, delete the line
G1   rc=1  last: PROBEWIRING_FAIL  4 problem(s); 77/85 detectors run by a gate, 8 dated-exempt
U    rc=1  last: PROBEWIRING_FAIL  1 problem(s); 76/85 detectors run by a gate, 8 dated-exempt
        18:  FAIL  UNWIRED DETECTOR  artifacts/ip30abortkill/ip30_abort_probe.py is run by NO gate and has no dated exemption.
H0   rc=0  last: PROBEWIRING_PASS  76/85 detectors run by a gate, 9 dated-exempt, 44 witnesses correctly ungated
H1   rc=1  last: PROBEWIRING_FAIL  5 problem(s); 76/85 detectors run by a gate, 9 dated-exempt
        19:  FAIL  EXPIRED EXEMPTION  artifacts/ip30abortkill/ip30_abort_probe.py came due 2026-10-30 (today 2026-10-31) and is still run by no gate
RESTORE: gate_arm.sh cmp-clean against its backup
RESTORE: exec lines now 1
R_CONTROLS_DONE
```

## 4. Questions
**Q1.**  Which of my dispositions in section 1 is WRONG -- and for each TAKEN, is the FIX right?  Cite `file:line`.
**Q2.**  Is any sentence in the section-2 repair false or over-qualified -- the probe note's bullets and the stall
paragraph against the probe's `session()`, its rows and kill tables 4 and 5?
**Q3.**  Rule on D3.
**Q4.**  What is still owed before the full gate 14 run and the commit?  Still to come: the ledger (state notes, the
witness addition, the two filed rows, this round's seat entries, Fable's HELD markers and `hold_question`), the queue
regeneration, the matrix re-render, the gate run, a confirm pass, the commit and its hash follow-up.

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q4.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
