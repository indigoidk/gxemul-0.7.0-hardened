# CLOSING PASS -- `#548` fbdrainwire: the repair chain's pass on REVISION 4

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree under review is `GXEMUL-SEC/` (ignore any other `src/`).  2026-09-24.
**FIRST LINE:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.  **Please do not simply
ratify** -- every pass of this round has found something the one before accepted, including in corrections.  If you
cannot read files, that is expected: the whole diff is inlined (section 5).  In the working tree, `regress/gate_arm.sh`
and `tools/pipeline/check_probe_wiring.py` also carry another unit's uncommitted lines; the diff is HEAD -> revision 4
and is exactly what will be committed (built from HEAD's own blobs, not from the working files).

## 0. WHY THIS PASS EXISTS

The SF2 pass (all nine seats but Fable, who fires last) found a FLOOR BREACH in revision 3, measured by the Opus seat:
R6 built each re-arm cell on ONE timer, so `==` for `>=` on every timer but timer 2 (M_eq_n2) passed every row in the
battery and left a timer owing 4529 against a bound of 762 at rung 3.  That is the third breach of one class in a row
(`==`, then `pending_bound[0]`, then the timer x re-arm cells), so under this project's rule the repair owes the CLASS
CLOSURE -- enumerate the space, close every cell in one diff, write the contract -- and **this pass VERIFIES THE
ENUMERATION rather than hunting cells.**  The chain closes on the first valid pass that finds ZERO floor breaches in
the shipped composite; a zero must come with what was checked.

## 1. WHAT THE SF2 PASS OVERTURNED, AND WHAT REVISION 4 DID

* F5 ("R6b closes the class") OVERTURNED -- Opus (measured M_eq_n2, M_pend_n0), grok, both codex jobs.  **R6 now builds
  EVERY timer in BOTH re-arm cells** (re-armed at count 0; re-armed owing 8192), each timer re-armed to its OWN rate
  (762/1525/3051/6103), across two structs that swap the roles; it prints owed/peak/END for all eight, and gate 2 pins
  the whole line.  The END count, ((8192-1) mod B)+1, ties each peak to its own timer.
* F6/D4 ("R5 unchanged") OVERTURNED -- codex (a store `(int) bound & ~(timer_nr << 16)` lowers timers 2-3 at the 50 MHz
  case, hidden by R5's maximum), Opus.  **R5 now requires the LOWEST timer's peak to match as well.**
* F14 and F18 were incompletely repaired (the probe header still said "gate 2 -- every arm of it enabled", and "3051,
  identical to D" cannot show the disable executed) -- codex x2.  Rewritten; #548's M_en IS the evidence the disable ran.
* Three sibling wrong records the round had not touched: the harness header's "overflows at a higher emulated_hz", R3's
  "the rung-3 guest probe cannot see the difference at all", the probe's assembler comment "every generated word is still
  checked" -- codex panel.  All corrected.
* The backlog row counted RECORDS, not arms (two D lines passed) -- codex x2.  **Now one D and one X, each in [1, 762].**
* CTRL_ON was unpinned (0x88 -> 0x80 passes every drain row) -- grok, by arithmetic.  **The probe's FBDRAIN_TIMER line
  now carries `load=0x100 ctrl=0x88`, pinned whole.**
* The gate comment's blanket "gate 2's (R1/R2/R3/R5/R6/R6b)" overclaimed -- agy.  **Now per mutant, each to its row.**
* "Clause-(e) ... closed here" still overstated -- grok, minimax.  Now: witnessed on every timer, if X's disable ran.
* The checker's "detectors that NOTHING RUNS" heading was false of all four entries -- agy.  Corrected.
* F28 (upward re-arm) was settled on the wrong mutant; F24/F31's runtime bound is false (wait() resets on output); the
  SF2 packet's CTRL_ON sentence was false -- all recorded in `CORRECTIONS.md` (the dated artifacts stay unedited).
* FILED, not rowed: `fbbounddebt` -- a STORE conditioned by a mutant on the count (M_neqB, M_zge; the 1..761 cell is
  worth a third cell) or on direction (M_upskip, measured passing everything), and an index read from another field
  (`nr & (timer_load[nr]-1)`, codex; `timer_control[nr] & TIMER_FCLK_256 ? nr : 0`, grok); `fbharnessedits` -- edits
  to the probe's or the harness's own logic that keep the pins green (codex dedicated's eight-row table, the kimi seat's
  X-for-D substitution, Opus's three-token R6 edit); `fbboundmodes`, `fbdrainxdisable`, `fbdrainonepass`, `asanstaleobjs`.

## 2. THE ENUMERATION REVISION 4 CLAIMS (verify THIS)

`footbridge_pending(d, nr)`'s guard reads `pending_timer_interrupts[nr]` and `pending_bound[nr]`; `nr` is a floor axis
because it indexes both.  The body tests one partition: count < bound, count >= bound.
* **R6 (re-arm):** {timer 0..3} x {re-armed at count 0 (below), re-armed owing 8192 (at/above)} = 8 cells, all rowed,
  every timer to a distinct new rate.  Downward re-arms (50 MHz -> slower).
* **R6b (first arm):** {timer 0..3} armed first, all at distinct rates, then driven: cross-slot stores and reads show.
* **R5 (the bound's value):** every timer, at seven (hz, load, control) cases; lowest and highest peak must both match.
* **Not rowed, filed:** store guards a mutant ADDS (count == B, 0 < count < B, upward re-arm); index expressions reading a
  field other than `nr`; control values no instrument drives the callback with (PERIODIC, FCLK_16, EXTERNAL).

## 3. REVISION 4, MEASURED BY THE AUTHOR (badge A: self-measurement -- the Opus seat re-measures independently)

Gate 2's harness compiled exactly as `gate_offline.sh` compiles it, against build/'s objects; the two pins read out of
`gate_offline.sh` itself (`t4_rev4/`).  Columns: FBBOUND verdict, count of red R5 rows, R6, R6b, IDENTITY, the pins,
then R6's printed owed/peak/end cells.

```
base               PASS=1 R5=0    R6=ok   R6b=ok   IDENT=ok   pinR6=1 pinR6b=1 | 0/762/572 0/1525/567 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/3051/2090 0/6103/208
M_eq               PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/1525/567 8192/16384/16384 8192/16384/16384 8192/16384/16384 8192/16384/16384 0/3051/2090
M_idle             PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/1525/567 8192/16384/16384 8192/16384/16384 8192/16384/16384 8192/16384/16384 0/3051/2090
M_pendguard        PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/8192/8192 0/8192/8192 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/8192/8192 0/8192/
M_frozen           PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/8192/8192 0/8192/8192 8192/16384/16384 8192/16384/16384 8192/16384/16384 8192/16384/16384 0/8192/8
M_idx0             PASS=0 R5=6    R6=FAIL R6b=FAIL IDENT=ok   pinR6=0 pinR6b=0 | 0/762/572 0/1/1 1/1/1 1/1/1 8192/762/572 1/1/1 0/1/1 0/1/1
M_cmp0             PASS=0 R5=0    R6=FAIL R6b=FAIL IDENT=ok   pinR6=0 pinR6b=0 | 0/762/572 0/762/572 8192/762/572 8192/762/572 8192/762/572 8192/762/572 0/762/572 0/762/572
M_pct3             PASS=0 R5=6    R6=FAIL R6b=FAIL IDENT=ok   pinR6=0 pinR6b=0 | 0/762/572 0/1525/567 8192/3051/2090 1/1/1 8192/762/572 8192/1525/567 0/3051/2090 0/1/1
M_rst2             PASS=0 R5=1    R6=ok   R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/582 0/1525/572 8192/3051/2093 8192/6103/2091 8192/762/583 8192/1525/573 0/3051/2092 0/6103/209
M_neqB             PASS=1 R5=0    R6=ok   R6b=ok   IDENT=ok   pinR6=1 pinR6b=1 | 0/762/572 0/1525/567 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/3051/2090 0/6103/208
M_zge              PASS=1 R5=0    R6=ok   R6b=ok   IDENT=ok   pinR6=1 pinR6b=1 | 0/762/572 0/1525/567 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/3051/2090 0/6103/208
M_lowonly          PASS=0 R5=6    R6=FAIL R6b=FAIL IDENT=ok   pinR6=0 pinR6b=0 | 0/1/1 0/1/1 1/1/1 1/1/1 1/1/1 1/1/1 0/1/1 0/1/1
M_nobound          PASS=0 R5=7    R6=FAIL R6b=FAIL IDENT=ok   pinR6=0 pinR6b=0 | 0/8192/8192 0/8192/8192 8192/16384/16384 8192/16384/16384 8192/16384/16384 8192/16384/16384 0/8192/8
M_x2               PASS=0 R5=4    R6=FAIL R6b=FAIL IDENT=ok   pinR6=0 pinR6b=0 | 0/1525/567 0/3051/2090 8192/6103/2089 8192/12207/4177 8192/1525/567 8192/3051/2090 0/6103/2089 0/819
M_eq_n2            PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/1525/567 8192/3051/2090 8192/16384/16384 8192/16384/16384 8192/16384/16384 0/3051/2090 0
M_pend_n0          PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/8192/8192 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/8192/8192 0/8192/81
M_upskip           PASS=1 R5=0    R6=ok   R6b=ok   IDENT=ok   pinR6=1 pinR6b=1 | 0/762/572 0/1525/567 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/3051/2090 0/6103/208
M_mask16           PASS=0 R5=1    R6=ok   R6b=ok   IDENT=ok   pinR6=1 pinR6b=1 | 0/762/572 0/1525/567 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/3051/2090 0/6103/208
H_retarget_base    PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/762/0 8192/762/8192 8192/762/8192 8192/762/572 8192/762/8192 0/762/0 0/762/0
H_retarget_M_eq    PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/762/0 8192/762/8192 8192/762/8192 8192/16384/16384 8192/24576/8192 0/32768/0 0/40960/0
H_and_base         PASS=1 R5=0    R6=ok   R6b=ok   IDENT=ok   pinR6=1 pinR6b=1 | 0/762/572 0/1525/567 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/3051/2090 0/6103/208
H_and_M_eq         PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/1525/567 8192/16384/16384 8192/16384/16384 8192/16384/16384 8192/16384/16384 0/3051/2090
H_pre0_base        PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/1525/567 0/3051/2090 0/6103/2089 0/762/572 0/1525/567 0/3051/2090 0/6103/2089
H_pre0_M_eq        PASS=0 R5=0    R6=FAIL R6b=ok   IDENT=ok   pinR6=0 pinR6b=1 | 0/762/572 0/1525/567 0/3051/2090 0/6103/2089 0/762/572 0/1525/567 0/3051/2090 0/6103/2089
```

Gate 14's block on revision 4 is not yet run (it owes one clean run before commit, ~67 min).  Revision 3's block ran
41/41 on base in the Opus seat's table 3; revision 4 adds `load`/`ctrl` to one pin and splits the backlog row by arm.

## 4. QUESTIONS

1. **Verify the enumeration.**  Is any cell of {timer} x {re-arm below, re-arm at/above}, or any per-timer value cell of
   R5, still unrowed?  Is the "not rowed" list honest about each item's position relative to this project's floor?
2. **The floor question, of the SHIPPED COMPOSITE** (the whole diff below, not only what changed): name any clean-sweep
   mutant of the fix's own predicate or store -- inside the enumeration -- that passes every row.  Say "none" only with
   what you checked.
3. **Records:** is any sentence the diff adds still false?  (Every pass of this round has found at least one.)
4. May the chain close on this pass?  Say which of your findings, if any, is a floor breach and why.

## 5. THE DIFF, HEAD -> revision 4 (20 hunks, 1 line of context; exactly what will be committed)

```diff
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1162,2 +1162,94 @@
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
+#  and X=3051 on timer 1, and passes BOTH gate-2 differentials (diff_fbpending_bound.c arms
+#  every timer enabled; diff_footbridge.c never calls the callbacks).  Arm X -- disabled
+#  through the accrual -- is the battery's only GATED witness of a bound gated on
+#  TIMER_ENABLE, and it sees it only on the timer it runs, and only if its disable executed
+#  (FILED: fbdrainxdisable).  About 17 s per timer.  Each run is PINNED to its timer, load and
+#  control, and the loop to all four: a mistyped --timer is ignored and runs timer 0 (pass 2).
+#
+#  THE CONTRACT (clause e).  From zero, with nothing acked, N >= 1 delivered ticks and bound B
+#  leave the count at ((N-1) mod B)+1.  At 4 s N is about 3051; it follows the SIGALRM clock.
+#    CATCHES  the bound REMOVED on any timer (3051 on all four, measured); a bound gated on a
+#             control bit X's CTRL=0 write clears -- TIMER_ENABLE, and TIMER_FCLK_256, which
+#             gate 2's unprescaled cases also catch; and any B >= N, which reads N (M_x8,
+#             measured).  All three only while N > 762.
+#    NOT CLAIMED  a raise to 762 < B < N fails only when that count exceeds 762 (freq * 2,
+#             B = 1525, reads 1); `>` for `>=` only when N is a multiple of 763, and reset-to-0
+#             only then too, as a dead clock; a reset to 2 never.  A LOWERING stays under the
+#             cap by construction, and a deleted ceiling does not bind at 762 Hz.  A bound
+#             moved into DEVICE_TICK reads 1 on both arms: the FREEZE sets the bound to 1 and
+#             DEVICE_TICK clamps the count before the drain counts it.  Gate 2
+#             (diff_fbpending_bound.c) carries each: a lowering R5 (every timer) and R6/R6b;
+#             reset-to-0 R3; a reset to 2 R5's slowest case and R6's end counts; a deleted
+#             ceiling R1/R5; `>` R5; DEVICE_TICK R1/R2/R5/R6; and `==` for `>=` -- which never
+#             fires once a re-arm lowers the bound below an un-acked count -- R6, on every
+#             timer since #548.  A bound skipped under a control value no instrument drives the
+#             callback with -- TIMER_MODE_PERIODIC and TIMER_FCLK_16 measured, TIMER_EXTERNAL
+#             by reading -- passes every row here and in gate 2: FILED as `fbboundmodes`.
+#             Edits to the probe's own logic (what it counts, which arm it reports) are
+#             reviewed, not rowed, beyond the pins below: FILED as `fbharnessedits`.
+#    LOAD     Pinned to one core behind 12 busy loops, N fell from 3051 to 1183 and the
+#             removed-bound mutant still went red; below N = 763 it would pass SILENTLY.
+#             Neither starved run failed a correct build, but the probe's own waits could.
+#
+#  `gatedevicesplit` is OWED (#498): one more device probe in the ARM gate, on this gate's own
+#  -E cats machine like footbridge_sites_probe.py above.  Recorded, not compounded silently.
+fbd_ran=""
+for t in 0 1 2 3; do
+    FBDLOG=$LOGDIR/fbpending_drain_t$t.log
+    fdrc=0
+    python3 -u fbpending_drain_probe.py "$PMAX" "$STUB" --expect-cap 762 --accrue 4 --timer "$t" \
+        > "$FBDLOG" 2>&1 || fdrc=$?
+    grep -E '^  FAIL |^FBDRAIN_' "$FBDLOG" | sed 's/^/       /'
+    #  ONE verdict line, and a DECIDING one: REPORT-ONLY (a failed control, or no cap parsed)
+    #  must not read as completion.  When it fires, the rows below do not run for this timer.
+    if [ "$(grep -c '^FBDRAIN_VERDICT=' "$FBDLOG")" != "1" ] ||
+       ! grep -Eqx 'FBDRAIN_VERDICT=(PASS|FAIL)' "$FBDLOG"; then
+        note "fbpending drain probe, timer $t: no unique PASS/FAIL verdict; last lines follow"
+        tail -5 "$FBDLOG" | sed 's/^/       /'
+        check "fbdrain t$t: the probe reached a verdict" "no" "yes"
+        continue
+    fi
+    check "fbdrain t$t: the probe reached a verdict" "yes" "yes"
+    #  WHICH TIMER RAN and WHAT IT WAS ASKED.  Without these, one token -- a mistyped --timer, or
+    #  the probe's load, control or --accrue changed -- keeps every row green while measuring
+    #  timer 0 four times, or at a rate where a removed bound reads under the cap (measured).
+    fbdtimer="FBDRAIN_TIMER=$t base=0x$(printf '%03x' $((0x300 + 0x20 * t))) load=0x100 ctrl=0x88"
+    fbdn=$(grep -cx "$fbdtimer" "$FBDLOG")
+    [ "$fbdn" = "1" ] && fbd_ran="$fbd_ran$t"
+    check "fbdrain t$t: the run measured timer $t at load 0x100, control 0x88" "$fbdn" "1"
+    check "fbdrain t$t: asked for 4 s at 762.94 Hz (uncapped prediction 3052)" \
+          "$(grep -cx '  UNCAPPED prediction: backlog = 3052' "$FBDLOG")" "1"
+    #  THE CONTROLS FIRST.  FBDRAIN_CONTROL=OK is an AGGREGATE that stays OK if a row is DELETED
+    #  from the probe, so the twelve control rows are pinned by DISTINCT GREEN ids as well.
+    check "fbdrain t$t: controls prove the probe measures" \
+          "$(grep -cx 'FBDRAIN_CONTROL=OK' "$FBDLOG")" "1"
+    check "fbdrain t$t: R0 C1 C2 A1 A2 E H1 H2 T L1 L2 P, twelve DISTINCT green ids" \
+          "$(grep -E '^  ok   (R0|C1|C2|A1|A2|E|H1|H2|T|L1|L2|P) ' "$FBDLOG" | awk '{print $2}' | sort -u | wc -l | tr -d ' ')" "12"
+    #  The cap the probe PARSED, the counts, both clocks, the verdict, the exit status.  A
+    #  correct build always owes at least one tick (the reset is to 1), so a count of 0 that is
+    #  not the poison word is a measurement that did not happen; D and X are counted SEPARATELY,
+    #  so two D lines cannot stand in for a missing X.  CLOCK_DEAD is matched as a WHOLE LINE:
+    #  an extract compared to "" is green on a log with no such line (measured).
+    check "fbdrain t$t: bounded at the asserted cap 762" \
+          "$(grep -cx 'FBDRAIN_BOUNDED=YES  (cap asserted: 762)' "$FBDLOG")" "1"
+    check "fbdrain t$t: one D and one X backlog, each in [1, 762]" \
+          "$(grep -Ecx 'FBDRAIN_BACKLOG_D=([1-9]|[1-9][0-9]|[1-6][0-9]{2}|7[0-5][0-9]|76[0-2])' "$FBDLOG"):$(grep -Ecx 'FBDRAIN_BACKLOG_X=([1-9]|[1-9][0-9]|[1-6][0-9]{2}|7[0-5][0-9]|76[0-2])' "$FBDLOG")" "1:1"
+    check "fbdrain t$t: both clocks alive (no zero-tick drain)" \
+          "$(grep -cx 'FBDRAIN_CLOCK_DEAD=' "$FBDLOG")" "1"
+    check "fbdrain t$t: verdict PASS" "$(grep -cx 'FBDRAIN_VERDICT=PASS' "$FBDLOG")" "1"
+    check "fbdrain t$t: probe exit status" "$fdrc" "0"
+done
+check "fbdrain: timers 0 1 2 3 each ran, each pinned" "${fbd_ran:-none}" "0123"
+
+#  ---------------------------------------------------------------------------------------
 #  #439/#440 PIT 8253 latch + LSB/MSB selector -- pitlatch / pitclobber.
--- a/tools/pipeline/check_probe_wiring.py
+++ b/tools/pipeline/check_probe_wiring.py
@@ -2371,3 +2371,6 @@
 
-    # -- detectors that NOTHING RUNS.  Each carries a dated exemption below. --------------
+    # -- detectors that NOTHING RAN when this group was written.  *** #548: NONE OF THE FOUR
+    #    IS UNRUN NOW -- pit8253 and sh4_bsc_width (2026-08-30), hpcmips (#536) and
+    #    fbpending_drain (#548) are gated, and none carries an exemption.  The grouping is
+    #    history; EXEMPT below and the checker's own derivation are the live record. *** ---
     #  pit8253's docstring line 1 calls it a "witness"; its rows assert the FIXED behaviour
@@ -2501,2 +2504,5 @@
 #
+#  *** #548, 2026-09-24: THE OTHER HALF IS GONE TOO. ***  fbpending_drain_probe.py is wired
+#  into gate_arm.sh and its entry deleted, so TEN of those eleven remain, still one block.
+#
 #  These are wiring jobs, not design ones.  NOT every probe here prints a verdict token or exits
@@ -2524,5 +2530,5 @@
     #  in the SAME edit as the wiring, for the same reason.
-    "fbpending_drain_probe.py": ("2026-09-27",
-                                 "REPORT-ONLY by default: EXPECT_CAP must be set before a "
-                                 "gate row can mean anything, so wiring is a design step first"),
+    #  fbpending_drain_probe.py's exemption is DISCHARGED, 2026-09-24 (#548) -- wired into
+    #  gate_arm.sh beside footbridge_sites_probe.py, all four timers, --expect-cap 762.
+    #  Deleted in the SAME edit as the wiring, for the same reason.
     #  Both #494 probes are TWO-LEG DIFFERENTIALS: they take a PRE-FIX binary and
--- a/regress/fbpending_drain_probe.py
+++ b/regress/fbpending_drain_probe.py
@@ -48,3 +48,3 @@
 
-ARM X -- THE PLACEMENT DISCRIMINATOR, and the reason it is not merely a second run.
+ARM X -- the reason it is not merely a second run.
   dev_footbridge.c never calls timer_remove() and never lowers the core frequency when
@@ -54,4 +54,13 @@
   disables it, free-runs, re-enables (which does NOT clear the counter) and then
-  measures.  A non-zero result proves the counter accrues while the device is disabled
-  -- which is exactly the state in which a bound placed in DEVICE_TICK cannot run.
+  measures.  #442 measured 3051 on the PRE-FIX build, identical to arm D -- which alone
+  cannot show the disable executed.  #548's M_en did: with the bound gated on ENABLE,
+  X read 3051 against D's 3.  No row re-checks it per run: FILED as `fbdrainxdisable`.
+  *** #548: THE HEADING SAID "THE PLACEMENT DISCRIMINATOR" AND X IS NOT ONE -- MEASURED.
+  A bound moved into DEVICE_TICK reads X=1 and PASSES: the FREEZE's LOAD write sets the
+  bound to 1, and DEVICE_TICK clamps the count before the drain counts it.  gate 2
+  (diff_fbpending_bound.c R1/R2/R5/R6) catches that placement.  What X DOES catch is a
+  bound gated on a control bit its CTRL=0 write clears: TIMER_ENABLE, which
+  diff_fbpending_bound.c -- every arm of which is enabled -- cannot see, and
+  TIMER_FCLK_256, which that file's unprescaled cases catch too.  X is the only GATED
+  rung-3 witness of either. ***
 
@@ -72,7 +81,12 @@
 Every RAM output word is poisoned with 0xDEADBEEF first and every verdict row requires
-the values it consults to be PRESENT.  Every planted instruction is checked, as it
-EXECUTES, against the emulator's own disassembly (the hand-assembled-encoding trap).
-
-usage: fbpending_drain.py <gxemul-binary> <four-byte-raw-stub>
-                          [--accrue S] [--expect-cap N] [--learn]
+the values it consults to be PRESENT.  Every STEPPED instruction is read back, and every
+stepped NON-branch instruction is compared, as it EXECUTES, with the emulator's own
+disassembly (the hand-assembled-encoding trap): the 21-word prologue, and arm D's drain
+body (0x70-0xe4) in arm E, whose seven branch words carry no expected text and are read
+back only.  *** #548: THIS SAID "EVERY PLANTED INSTRUCTION".  The accrual loop
+(0x54-0x6c) and arm X's disable and re-enable words (0x54/0x58, 0x70/0x74) FREE-RUN
+unchecked.  Filed as `fbdrainxdisable`. ***
+
+usage: fbpending_drain_probe.py <gxemul-binary> <four-byte-raw-stub>
+         [--accrue S] [--expect-cap N] [--timer N] [--fast] [--only ARM] [--learn]
 """
@@ -142,5 +156,7 @@
 # ---------------------------------------------------------------- assembler
-#  Encodings are GENERATED, not typed.  Every generated word is still checked
-#  against the emulator's own disassembly as it executes (arm E of the witness
-#  found this class of error four times in this project).
+#  Encodings are GENERATED, not typed.  Every generated word that is STEPPED is read
+#  back, and each stepped non-branch word is compared with the emulator's own
+#  disassembly as it executes (arm E of the witness found this class of error four
+#  times in this project).  #548: this said EVERY generated word -- the accrual loop
+#  and arm X's disable words free-run, and branch words carry no expected text.
 def _imm12(v):
@@ -805,2 +821,6 @@
     print("=" * 78)
+    #  #548: WHICH timer this run measured, and the load and control it armed, so gate 14
+    #  can pin them -- _opt() ignores an unknown flag (a mistyped --timer runs timer 0), and
+    #  a changed LOAD_RUN or CTRL_ON moves the rate with every other row green.
+    print("FBDRAIN_TIMER=%d base=0x%03x load=0x%x ctrl=0x%x" % (TIMER_NR, TBASE, LOAD_RUN, CTRL_ON))
     print("FBDRAIN_CONTROL=%s" % ("OK" if ok else "FAILED"))
--- a/regress/diff_fbpending_bound.c
+++ b/regress/diff_fbpending_bound.c
@@ -18,3 +18,5 @@
  *    - a bound with no ABSOLUTE ceiling (mutant m6, cap == (int)freq alone) is correct
- *      at cats' 50 MHz and overflows at a higher emulated_hz.  A guest probe cannot
+ *      at cats' 50 MHz and at a higher emulated_hz lets the debt reach INT_MAX before
+ *      the compare-first reset -- NOT an overflow (#548 measured R2 green with the
+ *      ceiling deleted; this said "overflows" until then).  A guest probe cannot
  *      reach that in bounded time: the core delivers at most TIMER_MAX_CATCHUP *
@@ -175,3 +177,3 @@
 		for (c = 0; c < sizeof(cases)/sizeof(cases[0]); c++) {
-			int worst_peak = INT_MIN, worst_trough = INT_MAX;
+			int worst_peak = INT_MIN, worst_trough = INT_MAX, best_peak = INT_MAX;
 			d = (struct footbridge_data *) calloc(1, sizeof(*d));
@@ -183,2 +185,4 @@
 					worst_peak = peak;
+				if (peak < best_peak)
+					best_peak = peak;
 				if (trough < worst_trough)
@@ -212,2 +216,6 @@
 			 *  `f` was already computed for the message above.
+			 *
+			 *  *** #548: ON EVERY TIMER, NOT THE MAXIMUM.  A store lowering timers
+			 *  2-3 alone (`(int) bound & ~(timer_nr << 16)`) hid behind timer 0's
+			 *  correct peak at every case here.  The lowest peak must match too. ***
 			 */
@@ -220,5 +228,5 @@
 				row("R5 the bound IS this timer's rate",
-				    worst_peak == want,
-				    "%-28s peak %11d  want %11d", cases[c].what,
-				    worst_peak, want);
+				    worst_peak == want && best_peak == want,
+				    "%-28s peak %11d  want %11d  lowest %d", cases[c].what,
+				    worst_peak, want, best_peak);
 			}
@@ -232,4 +240,5 @@
 			 *  only one of the four that separates reset-to-1 from
-			 *  reset-to-0, and the rung-3 guest probe cannot see the
-			 *  difference at all.
+			 *  reset-to-0, and the rung-3 guest probe sees it only when
+			 *  the delivered count is a multiple of 763, as a dead clock
+			 *  (#548; this said "cannot see the difference at all").
 			 */
@@ -273,27 +282,101 @@
 	 *
-	 *  So: arm two timers at DIFFERENT rates, then RE-ARM one at a third, and
-	 *  require each timer's bound to track its own current rate.  Same oracle as
-	 *  R5 -- the peak the counter reaches -- so no new oracle is introduced.
+	 *  So: RE-ARM each timer at a different rate and require its bound to track
+	 *  the new one (R6), and give every timer a rate no other timer shares (R6b).
+	 *  Same oracle as R5 -- the peak the counter reaches -- plus the count the
+	 *  timer is LEFT with, so no new oracle is introduced.
+	 *
+	 *  *** #548: A RE-ARM HAS TWO CELLS, AND EVERY TIMER OWES BOTH. ***  The
+	 *  callback's `>=` splits a re-arm by where the count sits against the NEW
+	 *  bound: below it (re-armed at count 0) or at or past it (re-armed owing 8192).
+	 *  `==` for `>=` is identical in the first cell and, while nothing acks, never
+	 *  fires again in the second; it passed every row in the battery, and one guest
+	 *  CONTROL write left it 4529 owed against a bound of 762 (measured).  And `nr`
+	 *  indexes both lvalues the guard reads, so the timer is a floor axis too: a
+	 *  first repair that built the owed cell on timer 2 alone let `==` on the other
+	 *  three timers pass everything, 4529 owed again at rung 3 (measured).  So all
+	 *  EIGHT cells, each timer re-armed to its OWN rate (762/1525/3051/6103), so a
+	 *  re-arm that stores into another timer's slot shows as well.  The END counts --
+	 *  ((8192-1) mod B)+1 under the bound -- tie each peak to its own timer.
+	 *
+	 *  THE CONTRACT: covered, every timer x {re-armed at count 0, re-armed owing
+	 *  8192}, downward re-arms from 50 MHz.  NOT rowed, and filed (fbbounddebt): a
+	 *  STORE conditioned by a mutant on the count (`pending != (int)bound` at a
+	 *  count of exactly B, `pending == 0 || pending >= (int)bound` at 1..B-1) or
+	 *  on the direction (a store skipped on an UPWARD re-arm), and an index read
+	 *  from another field (`timer_load[nr]`, `timer_control[nr]`).  The fix's own
+	 *  store is unconditioned and its index is `timer_nr` alone; these cells are
+	 *  not built for proportion, not because a rule excuses them.
 	 */
 	{
-		int peak, trough;
-		struct footbridge_data *r6 =
-		    (struct footbridge_data *) calloc(1, sizeof(*r6));
-
+		static const uint32_t rl[N_FOOTBRIDGE_TIMERS] = { 256, 128, 64, 32 };
+		int s, t, bad = 0, owe, want, owed[2][N_FOOTBRIDGE_TIMERS],
+		    pk[2][N_FOOTBRIDGE_TIMERS], end[2][N_FOOTBRIDGE_TIMERS];
+		char line[640];
+		size_t o = 0;
+
+		/*  Struct 0 re-arms timers 0-1 at count 0 and timers 2-3 owing 8192;
+		    struct 1 swaps the roles.  */
 		fake_machine.emulated_hz = 50000000;
-		arm(r6, 0, 1, TIMER_ENABLE);			/*  50 MHz  */
-		arm(r6, 1, 256, TIMER_ENABLE | TIMER_FCLK_256);	/*  762 Hz  */
-
-		/*  RE-ARM timer 0 much slower.  A frozen bound keeps 50e6 here.  */
-		arm(r6, 0, 256, TIMER_ENABLE | TIMER_FCLK_256);
-		drive(r6, 0, 4096, &peak, &trough);
-		row("R6 a re-armed timer's bound follows its NEW rate",
-		    peak == 762, "timer 0 re-armed 50 MHz -> 762 Hz: peak %d want 762",
-		    peak);
-
-		/*  And timer 1 must carry ITS own bound, not timer 0's.  */
-		drive(r6, 1, 4096, &peak, &trough);
-		row("R6b each timer carries its OWN bound",
-		    peak == 762, "timer 1: peak %d want 762", peak);
-		free(r6);
+		for (s = 0; s < 2; s++) {
+			struct footbridge_data *r6 =
+			    (struct footbridge_data *) calloc(1, sizeof(*r6));
+			for (t = 0; t < N_FOOTBRIDGE_TIMERS; t++) {
+				arm(r6, t, 1, TIMER_ENABLE);		/*  50 MHz  */
+				if (((t >> 1) ^ s) & 1)
+					drive(r6, t, 8192, &peak, &trough);
+			}
+			for (t = 0; t < N_FOOTBRIDGE_TIMERS; t++) {
+				owe = (((t >> 1) ^ s) & 1) ? 8192 : 0;
+				want = (int) (50000000.0 / (double) footbridge_effective_cycles(
+				    rl[t], TIMER_ENABLE | TIMER_FCLK_256, 1));
+				owed[s][t] = r6->pending_timer_interrupts[t];
+				arm(r6, t, rl[t], TIMER_ENABLE | TIMER_FCLK_256);
+				drive(r6, t, 8192, &pk[s][t], &trough);
+				end[s][t] = r6->pending_timer_interrupts[t];
+				if (owed[s][t] != owe || pk[s][t] != want ||
+				    end[s][t] < 1 || end[s][t] > want)
+					bad++;
+			}
+			free(r6);
+		}
+		for (s = 0; s < 2; s++)
+			for (t = 0; t < N_FOOTBRIDGE_TIMERS; t++)
+				o += (size_t) snprintf(line + o, sizeof(line) - o, "%s%d/%d/%d",
+				    (s || t) ? " " : "", owed[s][t], pk[s][t], end[s][t]);
+		row("R6 a re-armed timer's bound follows its NEW rate", bad == 0,
+		    "owed/peak/end, 4 timers x 2 structs: %s", line);
+	}
+
+	/*
+	 *  R6b -- EVERY TIMER CARRIES ITS OWN BOUND, AT A RATE NO OTHER TIMER SHARES.
+	 *
+	 *  *** #548: THIS ROW CHECKED TIMER 1 AT 762 Hz -- THE RATE TIMER 0 HAD ALSO
+	 *  ENDED AT -- SO A TIMER READING ANOTHER TIMER'S BOUND READ THE SAME NUMBER AND
+	 *  PASSED. ***  Measured: the compare reading `pending_bound[0]` for every timer
+	 *  passed every row in the battery.  At four DISTINCT rates a timer that stores
+	 *  into, or compares against, another timer's slot -- or an unset one -- reads a
+	 *  different peak.  All four are armed FIRST, so a store that overwrites another
+	 *  timer's slot shows too.  Index maps of `nr` alone are what this closes; an
+	 *  index computed from another field is outside it (fbbounddebt, above).
+	 */
+	{
+		static const uint32_t ld[N_FOOTBRIDGE_TIMERS] = { 256, 128, 64, 32 };
+		int pk[N_FOOTBRIDGE_TIMERS], want[N_FOOTBRIDGE_TIMERS], trough, t, bad = 0;
+		struct footbridge_data *r6b =
+		    (struct footbridge_data *) calloc(1, sizeof(*r6b));
+
+		fake_machine.emulated_hz = 50000000;
+		for (t = 0; t < N_FOOTBRIDGE_TIMERS; t++)
+			arm(r6b, t, ld[t], TIMER_ENABLE | TIMER_FCLK_256);
+		for (t = 0; t < N_FOOTBRIDGE_TIMERS; t++) {
+			want[t] = (int) (50000000.0 / (double) footbridge_effective_cycles(ld[t],
+			    TIMER_ENABLE | TIMER_FCLK_256, 1));
+			drive(r6b, t, 8192, &pk[t], &trough);
+			if (pk[t] != want[t])
+				bad++;
+		}
+		row("R6b each timer carries its OWN bound", bad == 0,
+		    "distinct rates: peaks %d %d %d %d want %d %d %d %d", pk[0], pk[1],
+		    pk[2], pk[3], want[0], want[1], want[2], want[3]);
+		free(r6b);
 	}
--- a/src/devices/dev_footbridge.c
+++ b/src/devices/dev_footbridge.c
@@ -289,7 +289,7 @@
 	 *  IT IS ALSO NOT OPTIONAL, which a purely rate-relative bound hides.
-	 *  MEASURED: with `-I 2147483647` and load 1 the requested rate is
-	 *  2147483647.0, so (int)freq is INT_MAX and a bound of "the timer's own
-	 *  rate" never fires -- the overflow returns, reachable through a
-	 *  documented command-line flag.  Deleting these two lines is the
-	 *  smallest edit that still passes the rung-3 probe.
+	 *  With `-I 2147483647`, load 1 and no prescaler the requested rate is
+	 *  2147483647.0, so (int)freq is INT_MAX: a debt of 2^31-1 ticks, 31.5 s
+	 *  at the most the core delivers -- NOT an overflow, as this said until
+	 *  #548: the compare precedes the ++ (R2 measured green at INT_MAX).
+	 *  Deleting these two lines passes the rung-3 probe; R1/R5 catch it.
 	 *
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -1310,3 +1310,4 @@
 #  witness ladder's mechanical discriminator classes as never-a-reproduction.  The
-#  reproduction is regress/fbpending_drain_probe.py (rung 3) and it is NOT run here.
+#  reproduction is regress/fbpending_drain_probe.py (rung 3) and it is NOT run here --
+#  gate 14 (gate_arm.sh) runs it on all four timers, since #548.
 #
@@ -1324,4 +1325,6 @@
 #  and R2 with trough -2147483648 (the overflow itself); reset-to-0 fails R3 x7; a fix applied
-#  to one callback only fails R1 x7; no-ceiling fails R1 on the two high-hz cases and R2 with
-#  peak 2147483647.
+#  to one callback only fails R1 x7; no-ceiling fails R1 (and, since R5 exists, R5) on the two
+#  high-hz cases -- and NOT R2, which this said until #548: R2 stays green at peak 2147483647,
+#  trough 1, because the compare precedes the ++ (measured: regress/artifacts/
+#  fbdrainwire_20260924/opus548_measured/runs_p1/diff_fbb_M_noceil.out).
 FBBIN=$LOGDIR/diff_fbpending_bound
@@ -1345,2 +1348,11 @@
         check_min "fbpending bound: rows actually run"               "$(grep -cE '^  (ok|FAIL) ' "$FBLOG")" 15
+        #  #548: NAMED ROWS for R6 and R6b, each the sole detector of its cells, pinned as WHOLE
+        #  LINES -- the row name, "ok", and every PRINTED value (owed counts, peaks, end counts) --
+        #  so an edit to the row itself (a weakened condition, a smaller precharge, a drive aimed
+        #  at the wrong timer, a renamed row) cannot pass a wrong value.  Edits that separate the
+        #  printed values from the exercised state are reviewed, not rowed: fbharnessedits.
+        check "fbpending bound: R6 every timer in both re-arm cells" \
+              "$(grep -cxF "  ok   R6 a re-armed timer's bound follows its NEW rate owed/peak/end, 4 timers x 2 structs: 0/762/572 0/1525/567 8192/3051/2090 8192/6103/2089 8192/762/572 8192/1525/567 0/3051/2090 0/6103/2089" "$FBLOG")" "1"
+        check "fbpending bound: R6b four timers at four distinct rates" \
+              "$(grep -cxF "  ok   R6b each timer carries its OWN bound         distinct rates: peaks 762 1525 3051 6103 want 762 1525 3051 6103" "$FBLOG")" "1"
     fi
```
