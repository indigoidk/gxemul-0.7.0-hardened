# PASS 2 -- `#548` fbdrainwire: the DIFF (6 files, 9 hunks), for review before commit

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree under review is `GXEMUL-SEC/` (ignore any other `src/`).
2026-09-24.  **FIRST LINE:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this project's author stated wrongly, and on THIS round's pass 1
the flagship seat found two false sentences in drafts that were written to CORRECT false sentences.  **Check the premises
and every sentence the diff adds, not just the derivations.**  If you cannot read files, that is expected -- the whole
diff is inlined below; name any premise you cannot settle from this packet.  Seats that read files: the diff's six files
and `GXEMUL-SEC/regress/artifacts/fbdrainwire_20260924/` (the pass-1 evidence) are in scope.  `regress/gate_arm.sh`
and `tools/pipeline/check_probe_wiring.py` in the WORKING tree also carry another unit's uncommitted lines -- the diff
below is against HEAD and is exactly what will be committed; review THAT, not the working files.

## 0. WHAT PASS 1 DECIDED (nine seats + the Opus measuring seat; Fable 5.1 last: PROCEED WITH CHANGES)

`regress/fbpending_drain_probe.py` is `#442`'s rung-3 detector for the footbridge pending-tick bound
(`src/devices/dev_footbridge.c`: `footbridge_pending()`, and the bound block in `reload_timer_value()`).  It ran in no gate
and its exemption lapses 2026-09-27.  Pass 1 wired it into gate 14 on ALL FOUR timers (one timer was measured
insufficient), rewrote its contract (the draft claimed "any RAISE above 762" -- false), repaired gate 2's R6 (the `==`
cutoff escaped every shipped #442 detector -- an L2 floor breach), and corrected three wrong records.  Filed, not fixed:
`fbboundmodes` (a bound skipped in TIMER_MODE_PERIODIC escapes every instrument), `fbdrainxdisable` (nothing proves
arm X was disabled on a correct build), `fbdrainonepass` (a single-process four-timer probe mode would halve the cost).

## 1. SETTLED PREMISES (measured unless marked read; evidence under `regress/artifacts/fbdrainwire_20260924/`)

* The bound at the probe's rate is (int)(50e6 / 65536) = (int)762.939453125 = 762.  The drained count is
  ((N-1) mod B) + 1 for N delivered ticks and bound B; N = 3051 at 4 s on an idle host (`opus5_p1.md`).
* HEAD: D = X = 3 on all four timers, VERDICT=PASS.  Bound removed (M_nobound): 3051 on all four, FAIL.
* M_en0 (`if ((nr == 0 || (d->timer_control[nr] & TIMER_ENABLE)) && ...)`): drain timer 0 PASS, timer 1 FAIL
  (X = 3051); BOTH gate-2 differentials PASS; rung 3: `CLOCK_DEAD=X` after 45 s disabled at 50 MHz.
* M_en (enable-gated, all timers): drain FAIL via arm X only; gate 2 PASS (every gate-2 arm is enabled -- read).
* M_fclk (bound only under FCLK_256): drain X = 3051 on all four; gate 2 FAILS 11 rows (its unprescaled cases).
* M_devtick (bound moved into DEVICE_TICK): drain PASS on all four (X = 1: the FREEZE sets the bound to 1 before the
  drain counts); gate 2 FAILS (R1/R2/R5/R6).
* M_x2 (`freq * 2`): drain PASS (reads 1); gate 2 FAILS (R5/R6).  M_noceil (ceiling deleted): drain PASS; gate 2 R1/R5
  fail on the two high-hz cases and **R2 prints `ok ... peak 2147483647 trough 1`** -- no overflow.
* M_nper (bound skipped in PERIODIC mode): passes the drain on all four timers AND both gate-2 differentials.
* M_eq (`==` for `>=`): passes gate 2 at HEAD (R6 peak 762) and the drain (D = X = 3).  Rung 3: a guest CONTROL write
  from 12207 Hz to 762.94 Hz left it 4529 owed against a bound of 762 (HEAD: 1).  `opus5_p1b.md`.
* R6both (this diff's R6) across 15 mutants: M_eq red (timer 2 peak 8192), M_pendguard red (timer 0 peak 4096), no
  mutant red -> green, IDENTITY 28 rows unchanged.  The one-cell alternative (owe 4096 before timer 0's re-arm) LOST
  M_pendguard.  `opus548_measured/harness_matrix.txt`.
* The `dev_footbridge.c` hunk is comment-only with the same line count.  Built with build-asan's exact flags (-g, ASAN,
  UBSAN), HEAD's and this file compile to BYTE-IDENTICAL objects; `build/` and `/tmp/gxsec-build` rebuilt md5-identical.
* `check_probe_wiring.py` as committed (HEAD + this hunk): `PROBEWIRING_PASS 71/81 detectors run by a gate, 10
  dated-exempt`; `--selftest` 22/22.  A one-line `for ...; do python3 ...` would read as UNWIRED (measured, pass 1).
* Gate 14 as committed (HEAD + this block): PASS, 1082 checks, exit 0 (`gate14_20260924/gate14.out`).  All 28 fbdrain rows green, D = X = 3 on every timer; the four drain runs took 67 s of a 4015 s gate (the rest is the pre-existing SGI/PCC2 probes).  Gate 2's fbpending section with this R6, against build/'s objects: FBBOUND_PASS, R2 ran, IDENTITY 28, R6 `timer 0 at count 0 peak 762, timer 2 owing 4096 peak 762`.

## 2. THE DIFF (against HEAD bead6ad9; exactly what will be committed)

```diff
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1160,6 +1160,74 @@
 fi
 
 #  ---------------------------------------------------------------------------------------
+#  #548 fbdrainwire: #442's RUNG-3 DRAIN PROBE, wired before its exemption lapsed.
+#
+#  The guest arms footbridge timer N at 762.94 Hz (TIMER_FCLK_256, load 256, -E cats' 50 MHz),
+#  free-runs 4 s WITHOUT acking, freezes the timer and counts the backlog one TIMER_x_CLEAR at
+#  a time.  #442's bound resets the counter to 1 once it reaches (int)762.94 = 762, so the
+#  count can never exceed 762 -- the tightest cap that cannot false-fail.
+#
+#  ALL FOUR TIMERS, because ONE WAS MEASURED NOT TO BE ENOUGH (#548 pass 1, the Opus seat): a
+#  bound applied only while the timer is enabled, with timer 0 exempt, reads 3/3 on timer 0
+#  and X=3051 on timer 1, passes BOTH gate-2 differentials (every arm there is enabled), and
+#  brings #442's dead clock back at rung 3.  Arm X -- disabled through the accrual -- is the
+#  battery's only witness of a bound gated on TIMER_ENABLE, and it sees it only on the timer
+#  it runs.  Clause-(e) debt of #442 (footbridge_pending() reads no control bit), closed here.
+#  About 17 s per timer.
+#
+#  THE CONTRACT (clause e).  The count is ((N-1) mod B)+1 for N delivered ticks and bound B.
+#    CATCHES  the bound REMOVED on any timer (3051 on all four, measured); a bound gated on a
+#             control bit X's CTRL=0 write clears -- TIMER_ENABLE, and TIMER_FCLK_256, which
+#             gate 2's unprescaled cases also catch; and any B >= N, which reads N.
+#    NOT CLAIMED  a raise to 762 < B < N fails only when its residue exceeds 762 (freq * 2,
+#             B = 1525, reads 1 and passes), and `>` for `>=` only when N is a multiple of
+#             763.  A LOWERING, reset-to-0, a deleted ceiling or a bound moved into DEVICE_TICK
+#             cannot show at all -- the FREEZE sets the bound to 1 before the drain counts, so
+#             a clamp outside the callback collapses the backlog first (X=1).  All of those
+#             are gate 2's (diff_fbpending_bound.c R1/R3/R5/R6).  So is `==` for `>=`, which
+#             never fires once a re-arm lowers the bound below the count: it passed every row
+#             here and in gate 2 until #548 gave R6 its second cell (a re-arm with 4096 owed).
+#             A bound skipped in TIMER_MODE_PERIODIC passes EVERY instrument -- neither this
+#             probe nor gate 2 ever sets that bit.  FILED as `fbboundmodes`.
+#    LOAD     N follows the SIGALRM clock.  Pinned to one core behind 12 busy loops the
+#             removed-bound mutant still read 1183: a starved run LOSES TEETH SILENTLY, it
+#             never reds falsely.
+#
+#  `gatedevicesplit` is OWED (#498): one more device probe in the ARM gate, on this gate's own
+#  -E cats machine like footbridge_sites_probe.py above.  Recorded, not compounded silently.
+for t in 0 1 2 3; do
+    FBDLOG=$LOGDIR/fbpending_drain_t$t.log
+    fdrc=0
+    python3 -u fbpending_drain_probe.py "$PMAX" "$STUB" --expect-cap 762 --accrue 4 --timer "$t" \
+        > "$FBDLOG" 2>&1 || fdrc=$?
+    grep -E '^  FAIL |^FBDRAIN_' "$FBDLOG" | sed 's/^/       /'
+    #  ONE verdict line, and a DECIDING one: REPORT-ONLY (a failed control, or no cap parsed)
+    #  must not read as completion.
+    if [ "$(grep -c '^FBDRAIN_VERDICT=' "$FBDLOG")" != "1" ] ||
+       ! grep -Eqx 'FBDRAIN_VERDICT=(PASS|FAIL)' "$FBDLOG"; then
+        note "fbpending drain probe, timer $t: no unique PASS/FAIL verdict; last lines follow"
+        tail -5 "$FBDLOG" | sed 's/^/       /'
+        check "fbdrain t$t: the probe reached a verdict" "no" "yes"
+        continue
+    fi
+    check "fbdrain t$t: the probe reached a verdict" "yes" "yes"
+    #  THE CONTROLS FIRST.  FBDRAIN_CONTROL=OK is an AGGREGATE that stays OK if a row is DELETED
+    #  from the probe, so the twelve control rows are pinned by DISTINCT GREEN ids as well.
+    check "fbdrain t$t: controls prove the probe measures" \
+          "$(grep -cx 'FBDRAIN_CONTROL=OK' "$FBDLOG")" "1"
+    check "fbdrain t$t: R0 C1 C2 A1 A2 E H1 H2 T L1 L2 P, twelve DISTINCT green ids" \
+          "$(grep -E '^  ok   (R0|C1|C2|A1|A2|E|H1|H2|T|L1|L2|P) ' "$FBDLOG" | awk '{print $2}' | sort -u | wc -l | tr -d ' ')" "12"
+    #  The cap the probe PARSED, both clocks, the verdict, the exit status.  CLOCK_DEAD is matched
+    #  as a WHOLE LINE: an extract compared to "" is green on a log with no such line (measured).
+    check "fbdrain t$t: bounded at the asserted cap 762" \
+          "$(grep -cx 'FBDRAIN_BOUNDED=YES  (cap asserted: 762)' "$FBDLOG")" "1"
+    check "fbdrain t$t: both clocks alive (no zero-tick drain)" \
+          "$(grep -cx 'FBDRAIN_CLOCK_DEAD=' "$FBDLOG")" "1"
+    check "fbdrain t$t: verdict PASS" "$(grep -cx 'FBDRAIN_VERDICT=PASS' "$FBDLOG")" "1"
+    check "fbdrain t$t: probe exit status" "$fdrc" "0"
+done
+
+#  ---------------------------------------------------------------------------------------
 #  #439/#440 PIT 8253 latch + LSB/MSB selector -- pitlatch / pitclobber.
 #
 #  WIRED HERE, ALONGSIDE footbridge_sites_probe.py, BECAUSE gate_hygiene.sh SAID SO.  Its
--- a/tools/pipeline/check_probe_wiring.py
+++ b/tools/pipeline/check_probe_wiring.py
@@ -2499,6 +2499,9 @@
 #  BY OWNER RULING, so those eleven again fall due as ONE block: the cliff `exemptcliff` names
 #  is re-created a week out, deliberately and dated, not by copying.
 #
+#  *** #548, 2026-09-24: THE OTHER HALF IS GONE TOO. ***  fbpending_drain_probe.py is wired
+#  into gate_arm.sh and its entry deleted, so TEN of those eleven remain, still one block.
+#
 #  These are wiring jobs, not design ones.  NOT every probe here prints a verdict token or exits
 #  nonzero on failure: mk48_nvram_probe.py printed MK48_RESULT=n/m and a DONE sentinel and exited 0
 #  with rows red, so the gate_arm.sh section #536 wired for it scores ROWS, not a token (agy, #536
@@ -2522,9 +2525,9 @@
     #  (#536) -- both wired into gate_arm.sh, mk48 on the mvme187 machine that file already
     #  drives for the PCC2 probes, hpcmips as a construction check with no rig image.  Deleted
     #  in the SAME edit as the wiring, for the same reason.
-    "fbpending_drain_probe.py": ("2026-09-27",
-                                 "REPORT-ONLY by default: EXPECT_CAP must be set before a "
-                                 "gate row can mean anything, so wiring is a design step first"),
+    #  fbpending_drain_probe.py's exemption is DISCHARGED, 2026-09-24 (#548) -- wired into
+    #  gate_arm.sh beside footbridge_sites_probe.py, all four timers, --expect-cap 762.
+    #  Deleted in the SAME edit as the wiring, for the same reason.
     #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
     #  a post-fix one and compare.  No gate builds a second leg, so wiring them is
     #  a change to the instrument -- a single-leg mode asserting only the fix-side
--- a/regress/fbpending_drain_probe.py
+++ b/regress/fbpending_drain_probe.py
@@ -46,14 +46,20 @@
   which re-arms at a different rate) -- and they exist because a one-token mutant
   (`freq / 100.0`) destroyed 99% of the guest's clock while passing this probe.
 
-ARM X -- THE PLACEMENT DISCRIMINATOR, and the reason it is not merely a second run.
+ARM X -- the reason it is not merely a second run.
   dev_footbridge.c never calls timer_remove() and never lowers the core frequency when
   the guest DISABLES a timer: TIMER_x_CONTROL without TIMER_ENABLE zeroes the counter
   once (the same `= 0` store) and leaves the struct timer running.  So timer_tickN keeps incrementing a
   counter that DEVICE_TICK will never look at.  Arm X arms the timer, immediately
   disables it, free-runs, re-enables (which does NOT clear the counter) and then
-  measures.  A non-zero result proves the counter accrues while the device is disabled
-  -- which is exactly the state in which a bound placed in DEVICE_TICK cannot run.
+  measures.  A non-zero result proves the counter accrues while the device is disabled.
+  *** #548: THE HEADING SAID "THE PLACEMENT DISCRIMINATOR" AND X IS NOT ONE -- MEASURED.
+  A bound moved into DEVICE_TICK reads X=1 and PASSES: the FREEZE's LOAD write sets the
+  bound to 1 before the drain counts, so any clamp outside the callback collapses the
+  backlog first.  gate 2 (diff_fbpending_bound.c R1/R2/R5/R6) catches that placement.
+  What X DOES catch is a bound gated on a control bit its CTRL=0 write clears:
+  TIMER_ENABLE, which gate 2 -- every arm of it enabled -- cannot see, and TIMER_FCLK_256,
+  which gate 2's unprescaled cases catch too.  X is the only RUNG-3 witness of either. ***
 
 ARMS
   D  enabled throughout.  Backlog after T seconds.
@@ -70,11 +76,15 @@
      their own predicates -- harness edits, reviewed, not rowed (footbridge_sites_probe.py).
 
 Every RAM output word is poisoned with 0xDEADBEEF first and every verdict row requires
-the values it consults to be PRESENT.  Every planted instruction is checked, as it
-EXECUTES, against the emulator's own disassembly (the hand-assembled-encoding trap).
-
-usage: fbpending_drain.py <gxemul-binary> <four-byte-raw-stub>
-                          [--accrue S] [--expect-cap N] [--learn]
+the values it consults to be PRESENT.  Every STEPPED instruction is checked, as it
+EXECUTES, against the emulator's own disassembly (the hand-assembled-encoding trap): the
+21-word prologue, and arm D's drain body (0x70-0xe4) in arm E.  *** #548: THIS SAID "EVERY
+PLANTED INSTRUCTION".  The accrual loop (0x54-0x6c) and arm X's disable and re-enable
+words (0x54/0x58, 0x70/0x74) FREE-RUN unchecked, and on a correct build nothing proves X
+was disabled at all -- it reads 3, like D.  Filed as `fbdrainxdisable`. ***
+
+usage: fbpending_drain_probe.py <gxemul-binary> <four-byte-raw-stub>
+         [--accrue S] [--expect-cap N] [--timer N] [--fast] [--only ARM] [--learn]
 """
 import os, pty, re, select, signal, struct, sys, time
 
--- a/regress/diff_fbpending_bound.c
+++ b/regress/diff_fbpending_bound.c
@@ -274,22 +274,37 @@
 	 *  So: arm two timers at DIFFERENT rates, then RE-ARM one at a third, and
 	 *  require each timer's bound to track its own current rate.  Same oracle as
 	 *  R5 -- the peak the counter reaches -- so no new oracle is introduced.
+	 *
+	 *  *** #548: A RE-ARM HAS TWO CELLS AND THIS ROW BUILT ONE. ***  The callback's
+	 *  `>=` splits a re-arm by where the count sits against the NEW bound: below it
+	 *  (timer 0, re-armed at count 0) or already past it (timer 2, re-armed with
+	 *  4096 owed).  `==` for `>=` is identical in the first cell and never fires
+	 *  again in the second; it passed every row in the battery, and one guest
+	 *  CONTROL write left it 4529 owed against a bound of 762 (measured).  Owing
+	 *  4096 before timer 0's own re-arm would have TRADED the cells, not added one:
+	 *  a bound recomputed only while a backlog is owed then passed.  Both, one row.
 	 */
 	{
-		int peak, trough;
+		int peak, trough, peak2, trough2;
 		struct footbridge_data *r6 =
 		    (struct footbridge_data *) calloc(1, sizeof(*r6));
 
 		fake_machine.emulated_hz = 50000000;
 		arm(r6, 0, 1, TIMER_ENABLE);			/*  50 MHz  */
 		arm(r6, 1, 256, TIMER_ENABLE | TIMER_FCLK_256);	/*  762 Hz  */
+		arm(r6, 2, 1, TIMER_ENABLE);			/*  50 MHz  */
+		drive(r6, 2, 4096, &peak2, &trough2);		/*  4096 owed  */
 
 		/*  RE-ARM timer 0 much slower.  A frozen bound keeps 50e6 here.  */
 		arm(r6, 0, 256, TIMER_ENABLE | TIMER_FCLK_256);
 		drive(r6, 0, 4096, &peak, &trough);
+		/*  and timer 2, whose debt is ABOVE the new bound when it lands.  */
+		arm(r6, 2, 256, TIMER_ENABLE | TIMER_FCLK_256);
+		drive(r6, 2, 4096, &peak2, &trough2);
 		row("R6 a re-armed timer's bound follows its NEW rate",
-		    peak == 762, "timer 0 re-armed 50 MHz -> 762 Hz: peak %d want 762",
-		    peak);
+		    peak == 762 && peak2 == 762,
+		    "re-armed 50 MHz -> 762 Hz: timer 0 at count 0 peak %d, timer 2 owing "
+		    "4096 peak %d; want 762", peak, peak2);
 
 		/*  And timer 1 must carry ITS own bound, not timer 0's.  */
 		drive(r6, 1, 4096, &peak, &trough);
--- a/src/devices/dev_footbridge.c
+++ b/src/devices/dev_footbridge.c
@@ -287,11 +287,11 @@
 	 *  at that value can never throttle a legitimately fast timer.
 	 *
 	 *  IT IS ALSO NOT OPTIONAL, which a purely rate-relative bound hides.
-	 *  MEASURED: with `-I 2147483647` and load 1 the requested rate is
-	 *  2147483647.0, so (int)freq is INT_MAX and a bound of "the timer's own
-	 *  rate" never fires -- the overflow returns, reachable through a
-	 *  documented command-line flag.  Deleting these two lines is the
-	 *  smallest edit that still passes the rung-3 probe.
+	 *  With `-I 2147483647` and load 1 the requested rate is 2147483647.0,
+	 *  so (int)freq is INT_MAX: a debt of 2^31-1 ticks, 31.5 s at the core's
+	 *  full delivery rate -- NOT an overflow, as this said until #548: the
+	 *  compare precedes the ++ (R2 measured green at peak INT_MAX).  Deleting
+	 *  these two lines is the smallest edit still passing the rung-3 probe.
 	 *
 	 *  Floor 1.  *** ITS ORIGINAL JUSTIFICATION WAS MEASURED FALSE and is
 	 *  corrected here rather than quietly dropped: *** the comment claimed a
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -1308,7 +1308,8 @@
 #  THIS ROW IS A DETECTOR, NOT THE REPRODUCTION, and the distinction is load-bearing here.
 #  It #includes the shipped dev_footbridge.c and calls timer_tickN() directly, which the
 #  witness ladder's mechanical discriminator classes as never-a-reproduction.  The
-#  reproduction is regress/fbpending_drain_probe.py (rung 3) and it is NOT run here.
+#  reproduction is regress/fbpending_drain_probe.py (rung 3) and it is NOT run here --
+#  gate 14 (gate_arm.sh) runs it on all four timers, since #548.
 #
 #  BOTH SHIP BECAUSE NEITHER ALONE IS ENOUGH -- measured, not assumed:
 #    * the rung-3 probe cannot reach the boundary.  The core delivers at most
@@ -1322,8 +1323,10 @@
 #  It links every object EXCEPT main.o and dev_footbridge.o, so it runs the REAL timer.c and
 #  the REAL footbridge rather than re-implementations.  Measured kills: pre-fix fails R1 x7
 #  and R2 with trough -2147483648 (the overflow itself); reset-to-0 fails R3 x7; a fix applied
-#  to one callback only fails R1 x7; no-ceiling fails R1 on the two high-hz cases and R2 with
-#  peak 2147483647.
+#  to one callback only fails R1 x7; no-ceiling fails R1 on the two high-hz cases -- and NOT
+#  R2, which this said until #548: R2 stays green at peak 2147483647, trough 1, because the
+#  compare precedes the ++ (measured: regress/artifacts/fbdrainwire_20260924/
+#  opus548_measured/runs_p1/diff_fbb_M_noceil.out).
 FBBIN=$LOGDIR/diff_fbpending_bound
 FBLOG=$LOGDIR/diff_fbpending_bound.log
 FBOBJS=$(find "$SEC/../build/src" -name '*.o' ! -name 'main.o' ! -name 'dev_footbridge.o' 2>/dev/null | sort)
```

## 3. THE PRE-TABLE CHECK'S CHANNEL SECTION (written before the pass-2 kill table; `PRETABLE.out`)

```
4. CHANNEL -- per row, the mutant it kills and the observable that differs under it
   gate 14, per timer t:
     "reached a verdict"        a probe that crashes, hangs to the harness budget, or prints REPORT-ONLY (a control
                                failed / no cap parsed) -> no unique PASS|FAIL line.
     "controls prove ..."       any control failing -> FBDRAIN_CONTROL=FAILED.
     "twelve DISTINCT green ids" a control row DELETED or renamed in the probe -> 11 ids (CONTROL=OK cannot see it).
     "bounded at the asserted cap 762"  M_nobound / M_en / M_fclk / M_x8 -> BOUNDED=NO; a probe edit that parses a
                                different cap -> "(cap asserted: N)" differs.
     "both clocks alive"        a zero-tick drain (poisoned count) -> "FBDRAIN_CLOCK_DEAD=D ..." (whole-line match).
     "verdict PASS"             every bound mutant above -> VERDICT=FAIL.
     "probe exit status"        VERDICT=FAIL or a failed control -> exit 1.
   Under M_nobound the verdict, BOUNDED and exit rows vary (3051 > 762).  No row's named channel is constant under
   its named mutant.
   gate 2 R6: M_eq -> timer 2 peak 8192; M_pendguard -> timer 0 peak 4096; M_frozen -> peak 4096/8192;
     M_idx0 -> R6 (peak 1) and R6b.

```

## 4. QUESTIONS

1. **Premise audit.**  Check the premises above and every sentence the diff ADDS.  Name any that is false, overstated,
   or true only for the case measured.
2. **The floor, for the new gate-14 rows AND for R6.**  What is the smallest edit -- to `dev_footbridge.c`, to the probe,
   or to the gate block itself -- that breaks a property this diff CLAIMS and still passes every row?  Name it concretely
   (the line, the token), and say whether it is inside the contract's NOT CLAIMED list (disclosed) or outside it (a
   breach).  Check the gate block's own shell: quoting, `continue`, `|| fdrc=$?`, the `grep -x` patterns, the awk field.
3. **R6both.**  Is the two-cell closure complete?  Does the added comment say only what was measured?
4. **The records hunks** (the device comment, gate_offline.sh, the probe header, the checker paragraph): true now?
5. **Anything else**, including a member of the option set nobody named.
