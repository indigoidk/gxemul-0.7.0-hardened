# SF2 -- `#548` fbdrainwire: THE ADJUDICATION PASS (the panel shares its findings)

Project root C:\DocumentNoSnc\cc\GXEMUL; the tree under review is `GXEMUL-SEC/` (ignore any other `src/`).  2026-09-24.
**FIRST LINE:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then your answers to the three questions at the end.

Standing owner directive: every seat now sees every other seat's pass-2 findings and my disposition of each.  **Please
do not simply ratify.**  I accepted most findings; that is a suspicious number, and agreement is not evidence.  If you
raised a finding, you are adjudicating my handling of your own finding -- be HARDER on it, including whether my FIX is
right, not merely whether your finding was.  If you cannot read files, that is expected: the whole diff is inlined
(section 5); name any premise you cannot settle from this packet.  In the working tree, `regress/gate_arm.sh` and
`tools/pipeline/check_probe_wiring.py` also carry another unit's uncommitted lines; the diff below is HEAD -> revision 3
and is exactly what will be committed.

## 0. WHAT HAPPENED

Pass 2 on revision 1: codex (GPT-6 Astra max), agy, grok 4.7, glm, deepseek, minimax, the kimi seat through
`kimi-k3:cloud` (the kimi CLI is on its weekly limit), a dedicated adversarial codex job, and the Opus measuring seat --
**every one said SHIP WITH CHANGES.**  Revision 2 is my response; the Opus seat then measured it (table 3, section 4)
and its one ask found a hole in revision 2's own R6 pin, which revision 3 closes (F32).  Revision 3 is IN THE TREE,
rebuilt (the device edit is comment-only: all three build trees rebuilt md5-identical), and gate 2's fbpending section
passes on it (FBBOUND_PASS, IDENTITY 28, both named rows 1).  Gate 14 ran GREEN on revision 1 (1082 checks); the final
revision still owes its run.  The flagship seat (Fable) fires after this pass.

## 1. FINDINGS AND MY DISPOSITIONS (L1 = pre-ship construction, L2 = floor breach, L4 = wrong record)

F1  **The four-timer claim was unpinned** -- `--timer "$t"` -> `--timer 0` (or a typo the probe's `_opt()` ignores, or
    dropping `3` from the loop) keeps all 28 rows green.  codex (dedicated #3, panel #1), glm #1, kimi-sub #2.
    ACCEPTED, L1: the probe prints `FBDRAIN_TIMER=<nr> base=0x<TBASE>`; each run pins its own; after the loop
    `fbd_ran` must be `0123` (a timer enters it only when its pin matched).
F2  **The rate/accrual was unpinned** -- LOAD_RUN 0x100 -> 0x800 (95.37 Hz): a removed bound reads 381 and passes 28/28
    (Opus, MEASURED); `--accrue .4` the same by reasoning.  ACCEPTED, L1: pin `  UNCAPPED prediction: backlog = 3052`
    (the probe prints RATE * ACCRUE_S -- constant for a configuration).
F3  **A zero drained count passes** -- the probe's `add1("sl")` -> `add1("sp")` publishes 0, which is not the poison
    word (codex dedicated #1, measured in-memory with fixtures).  ACCEPTED, L1: both backlogs must lie in [1, 762]; a
    correct build always owes one (the reset is to 1).
F4  **X's count can be replaced by D's** (`backlog(X, ranX)` -> `backlog(D, ranX)`), and a control can be rewritten into
    a tautology (codex dedicated #2, glm #13).  REFINED: probe-LOGIC edits are reviewed, not rowed -- the contract now
    says so ("beyond the pins below"); F1-F3's pins are the probe-integrity rows that are cheap and exact.
F5  **M_cmp0 passed every row in the battery** -- `pending_bound[nr]` -> `pending_bound[0]` in footbridge_pending (Opus,
    MEASURED: gate 14 28/28, gate 2 FBBOUND_PASS, diff_footbridge 864/864).  ACCEPTED, **L2**: a weakened operand of
    the fix's own predicate, escaping #442's shipped detectors; the second label-axis escape after #442 pass 2's `[0]`,
    so the repair closes the class: **R6b arms all four timers at four DISTINCT rates and checks each** (762, 1525,
    3051, 6103), all armed before any is driven.
F6  **R5 compares only the MAX peak across timers** -- `[timer_nr % 3]` at the store leaves timer 3 unset and hidden
    (codex dedicated #4, panel #4; derived).  ACCEPTED INTO F5's closure: the distinct-rate R6b checks every timer; R5
    itself is unchanged.  MEASURED in table 3 (M_pct3).
F7  **The bound STORE can be conditioned on the count** -- `pending != (int)bound` (count exactly 762) or
    `pending == 0 || pending >= (int)bound` (1..761) -- and no R6 cell builds those counts (codex dedicated #4, panel #3;
    deepseek #3 on the boundary).  REJECTED as a floor breach: the store sits under NO predicate, so no cell is owed
    there (the flagship seat's pass-1 ruling); DISCLOSED in R6's comment; FILED `fbbounddebt`.  Measured in table 3.
F8  **R6's new cell could be undone by editing R6 itself** -- `&&` -> `||`, the precharge shrunk to 0 or <= 762 (grok #4,
    minimax, codex panel #2).  ACCEPTED, L1: `owed0 == 0 && owed2 == 4096` in the condition, both counts PRINTED, and
    gate 2 pins the whole printed line; R6b's line is pinned the same way.
F9  **"cannot show at all -- the FREEZE ..." gave one mechanism for four misses**, true only of the DEVICE_TICK placement
    (grok #1, agy, glm #7, kimi-sub #4, codex dedicated #6, panel #5).  ACCEPTED, L4: split by mechanism.
F10 **Reset-to-0 CAN show** -- `N mod (B+1)` is 0 at N = 3052, a dead clock (codex dedicated #6, panel #5).  ACCEPTED, L4.
F11 **The LOAD sentence overclaimed** -- the starved removed-bound run still went RED (1183), and "never reds falsely" is
    unproven (grok #2, codex dedicated #7, panel #5).  ACCEPTED, L4.
F12 **"Clause-(e) ... closed here" overstated** -- ENABLE only; the mode bits are filed; X's disable is assumed (grok #3,
    codex dedicated #5, glm #6, deepseek #2, minimax).  ACCEPTED, L4 (and `fbdrainxdisable` is now in the gate's list).
F13 **FCLK_16/EXTERNAL were missing, and "neither ... ever sets that bit" is false** -- diff_footbridge.c sets PERIODIC
    but never calls the callback; M_f16 passes every row (Opus, MEASURED).  ACCEPTED, L4; `fbboundmodes` widened.
F14 "(every arm there is enabled)" is false of diff_footbridge.c (codex dedicated #5).  ACCEPTED, L4.
F15 "any B >= N" needs N > 762; the residue formula needs zero start, N >= 1, no acks (codex x2).  ACCEPTED, L4.
F16 "`==` never fires" needs "while nothing acks" (codex dedicated #6).  ACCEPTED, L4.
F17 "gate 2's (R1/R3/R5/R6)" omitted R2 (glm #4, kimi-sub #6).  ACCEPTED, L4.
F18 Probe header: "A non-zero result proves ... disabled" is too strong on a correct build (codex x2, minimax).  ACCEPTED, L4.
F19 Probe header: the seven drain-body BRANCH words carry expected text `None`, so step_and_check() reads them back but
    never compares their disassembly (codex x2; confirmed by reading).  ACCEPTED, L4.
F20 Probe header: "the only RUNG-3 witness" -> "the only GATED" (fbpending_witness.py is not gated) (codex x2).  ACCEPTED, L4.
F21 Device comment: "the smallest edit still passing" is false (`>=`->`==` and M_cmp0 are one token); "load 1" needs "no
    prescaler" (grok #6, codex x2, Opus).  ACCEPTED, L4 (same line count kept).
F22 Device comment "31.5 s" -- see D2.  REFINED: the number is right, the rate was unnamed; now "31.5 s at the most the
    core delivers".
F23 gate_offline.sh's no-ceiling record omitted R5 (glm #5, kimi-sub #6).  ACCEPTED, L4.
F24 **PRETABLE's channel section was wrong** for the "controls" and "exit status" rows (they never run once the verdict
    guard `continue`s), and "harness budget" named no watchdog (codex panel #8).  ACCEPTED: `PRETABLE_ADDENDUM_r2.out`
    corrects it; PRETABLE.out itself is left unedited because its mtime is the order proof.
F25 Packet counts: 14 mutants + baseline, not 15; M_fclk's 11 substantive FAILs + the R4 aggregate (codex x2).  ACCEPTED.
F26 "residue exceeds 762" is ambiguous (minimax).  ACCEPTED: "that count exceeds 762".
F27 **A reset to 2 passes every row** (glm #2).  I predicted PASS and FILED it; **table 3 MEASURED it RED** -- R5's
    "cats, slowest legal" case (bound 1) reads peak 2 -- and revision 3's end counts red it again in R6 (291/292 against
    286).  So it is NOT debt: withdrawn from `fbboundmodes`/`fbbounddebt`; the drain's "a reset to 2 never" stands.
F28 R6 only re-arms DOWNWARD (kimi-sub #3, minimax).  REJECTED, and table 3 settled it by measurement: M_lowonly (a store
    taken only on a lowering) is RED -- every first arm raises the bound from calloc's 0.
F29 minimax: `trough2` unused, the priming drive's results overwritten; the exact-format greps are brittle.  REJECTED:
    drive() writes through both pointers; an exact whole-line pin fails SAFE (red) on a format change, by design.
F30 kimi-sub: the corrected claims now live in four files, so they can diverge.  NOTED, no change.
F31 codex panel: no external watchdog around the probe.  NOTED: its own budgets bound it (addendum); no change.
F32 **The Opus seat's one ask, table 3: revision 2's R6 pin could be passed by retargeting R6's post-re-arm drive from
    timer 2 to timer 0** -- the printed line still said `timer 2 owing 4096 peak 762`, and M_eq passed gate 2, pins
    included (MEASURED).  ACCEPTED, L1 (the R6 repair is pre-ship): R6 reads each timer's END count (286 under the
    bound), requires both in [1, 762], prints them, and gate 2's pin includes them.  Measured on the revision-3 text
    (section 4b).  **This spends the ask-again's cap: any further edit-the-harness finding is FILED, not fixed.**

## 2. DISAGREEMENTS -- please adjudicate your own

D1  **Pin the timer (F1)?**  minimax: *"Editing `--timer "$t"` to `--timer 0` would not break a runtime check (HEAD still
    passes); the all-four-timers rationale is in the comment, not enforced by code. Documented, not a covert floor."*
    codex/glm/kimi-sub: *"outside NOT CLAIMED; a breach, not a disclosure"*.  MY RULING: pin it -- the four-timer run IS
    this round's measured claim (M_en0), and a claim the rows cannot enforce is a record that can go false silently.
D2  **"31.5 s" (F22).**  glm, deepseek, kimi-sub (packet-fed): *"2^31-1 / 5e7 = 42.95 s ... no inlined rate gives 31.5 s"*
    and *"the naive arithmetic gives 1.0 s"*.  codex x2, grok (file-reading): *"INT_MAX / (1048576*65) is 31.51 s"*.
    MY RULING: both are right about what they could see -- the core delivers at most TIMER_MAX_CATCHUP (1048576) x
    TIMER_BASE_FREQUENCY (65) = 68,157,440 ticks per wall second to one timer, and the old sentence never named it.
D3  **Row the store-guard cells (F7)?**  codex: *"R6both closes the measured cases, not the whole re-arm state space ...
    add a positive count below the new bound"*.  The flagship seat, pass 1: *"The store at :333 sits under no predicate,
    so no cell is owed at that site."*  MY RULING: disclose and file, per the flagship ruling -- tell me if the ruling
    does not cover a store CONDITIONED by a mutant, which is exactly what these are.
D4  **Per-timer R5, or the distinct-rate R6b (F6)?**  codex: *"Assert rate equality per timer, rather than only on
    their maximum."*  MY RULING: R6b at distinct rates is the stronger per-timer check (M_cmp0 is invisible to ANY
    per-timer check at EQUAL rates, which is what every R1 case uses), so R5 stays as it is.

## 3. OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* Revision 2 has NOT yet run in gate 14.  It owes one clean run before commit (~67 min, the machine to itself).
* Every pin in F1-F3 and F8 is a NEW row whose failability rests on table 3 (section 4), not on argument.
* F7/D3 files a family of store mutants as debt because of a pass-1 ruling about an UNCONDITIONED store; if that ruling
  is being stretched, this is where.
* F5's "class closure" claims the label axis is now closed.  Name a label-axis mutant that still passes, if one exists.

## 4. TABLE 3 -- the Opus seat's measurements of revision 2, and the main loop's of revision 3

**(a) The Opus seat, table 3 on revision 2** (`opus5_p3.md`, `opus548_measured/p3/`; claude-opus-5-5 by its transcript):
* gate 2's harness x base + 22 mutants: every earlier red mutant stays red; M_cmp0 and M_pct3 red in R6b only (peaks
  `762 762 762 762` and `6103 1525 3051 1`); M_lowonly red (settles F28); M_neqB and M_zge PASS (the disclosed store
  cells, F7); M_en/M_en0/M_nper/M_f16 PASS gate 2 (the drain's or `fbboundmodes`'); IDENTITY 28 in every run.
  **One sealed prediction MISSED, in the safe direction: M_rst2 (reset to 2) is RED**, through R5's "cats, slowest
  legal" case (bound 1: peak 2, want 1) -- so a reset to 2 is gate 2's after all, on that one row.
* Harness self-edits: `&&` -> `||` on M_eq leaves R6 ok and FBBOUND_PASS, and ONLY the gate_offline R6 pin reds;
  the precharge shrunk to 0 or 762 reds R6 itself (`owed2 == 4096`).
* The gate-14 block verbatim: base 41/41; M_nobound 16 red; M_en0 12 red (t1-t3); M_cmp0 passes the block (R6b
  catches it); `--timer`->`--time` reds "measured timer t" on t1-t3 and `fbd_ran` = `0`; loop list `0 1 2` ->
  `fbd_ran` = `012`; `--accrue .4` and LOAD_RUN 0x800 red ONLY the "asked for" row (uncapped 305 / 381) -- and on the
  bound-removed binary they read 375 and 381, so that row is the only thing standing; `add1("sp")` reds only the
  backlog-range row (0/0).
* The addendum's claim that the UNCAPPED line sees CTRL_ON is FALSE: RATE = EMU_HZ / (LOAD_RUN x 256) reads no CTRL_ON.
  A CTRL_ON edit is caught by the bounded and range rows instead.  (Corrected here, not in the addendum, whose mtime
  is the order proof.)
* **Its one ask found a hole in revision 2's own R6 pin:** retarget R6's post-re-arm drive from timer 2 to timer 0 and
  the printed line still says `timer 2 owing 4096 peak 762` -- base, M_eq and M_idle all pass gate 2, pins included.

**(b) REVISION 3, the repair for that one finding** (the ask-again cap is now spent; anything further is FILED): R6 reads
each timer's END count after its drive -- 4096 ticks under a bound of 762 leave ((4096-1) mod 762)+1 = 286 -- requires
both in [1, 762], and prints them; gate 2's pin now includes `end 286` twice.  **Measured by the main loop (author
self-measurement, badge A; `t3b_rev3/`), the same harness compiled as gate 2 compiles it:**

    base               PASS  R6 ok    R6b ok    pins 1/1   (end 286, end 286)
    M_eq, M_idle       FAIL  R6 FAIL            pin R6 0   (timer 2 peak 8192 end 8192)
    M_pendguard        FAIL  R6 FAIL            pin R6 0   (timer 0 peak 4096 end 4096)
    M_frozen, M_idx0, M_lowonly, M_nobound, M_x2   FAIL, pin R6 0
    M_cmp0, M_pct3     FAIL  R6 ok    R6b FAIL  pin R6b 0
    M_rst2             FAIL  (R5)     pin R6 0 -- the end counts read 291/292, so R6's pin sees reset-to-2 too
    M_neqB, M_zge      PASS  (disclosed: fbbounddebt)
    H_retarget (the one ask), on base and on M_eq:  R6 FAIL (timer 2 end 4096), pin 0
    H_or on M_eq:      FBBOUND_PASS, pin R6 0 -- the pin carries it
    H_pre0 on both:    R6 FAIL (owing 0), pin 0


## 5. THE DIFF, HEAD -> revision 3 (13 hunks; exactly what will be committed)

```diff
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1161,4 +1161,96 @@
 
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
+#  TIMER_ENABLE, and it sees it only on the timer it runs: the ENABLE half of #442's
+#  clause-(e) debt, closed here.  About 17 s per timer.  Each run is PINNED to its timer and
+#  the loop to all four, because a mistyped --timer is ignored and runs timer 0 (pass 2).
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
+#             DEVICE_TICK clamps the count before the drain counts it.  All of those are gate 2's
+#             (diff_fbpending_bound.c R1/R2/R3/R5/R6/R6b).  So is `==` for `>=`, which never
+#             fires once a re-arm lowers the bound below an un-acked count: it passed every row
+#             here and in gate 2 until #548 gave R6 its second cell (a re-arm with 4096 owed).
+#             A bound skipped under a control value no instrument drives the callback with --
+#             TIMER_MODE_PERIODIC and TIMER_FCLK_16 measured, TIMER_EXTERNAL by reading --
+#             passes every row here and in gate 2: FILED as `fbboundmodes`.  And arm X's ENABLE
+#             witness assumes its disable executed, which nothing checks on a correct build (X
+#             reads 3, like D): FILED as `fbdrainxdisable`.  Edits to the probe's own logic are
+#             reviewed, not rowed, beyond the pins below.
+#    LOAD     Pinned to one core behind 12 busy loops, N fell from 3051 to 1183 and the
+#             removed-bound mutant still went red; below N = 763 it would pass SILENTLY.
+#             Neither starved run failed a correct build, but the probe's own budgets (L1 wants
+#             1000 accrual iterations; its prompt waits) could.
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
+    #  the probe's load or --accrue changed -- keeps every row green while measuring timer 0 four
+    #  times, or at a rate where a removed bound reads under the cap (pass 2, measured).
+    fbdtimer="FBDRAIN_TIMER=$t base=0x$(printf '%03x' $((0x300 + 0x20 * t)))"
+    fbdn=$(grep -cx "$fbdtimer" "$FBDLOG")
+    [ "$fbdn" = "1" ] && fbd_ran="$fbd_ran$t"
+    check "fbdrain t$t: the run measured timer $t" "$fbdn" "1"
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
+    #  not the poison word is a measurement that did not happen.  CLOCK_DEAD is matched as a
+    #  WHOLE LINE: an extract compared to "" is green on a log with no such line (measured).
+    check "fbdrain t$t: bounded at the asserted cap 762" \
+          "$(grep -cx 'FBDRAIN_BOUNDED=YES  (cap asserted: 762)' "$FBDLOG")" "1"
+    check "fbdrain t$t: both backlogs in [1, 762]" \
+          "$(grep -Ecx 'FBDRAIN_BACKLOG_[DX]=([1-9]|[1-9][0-9]|[1-6][0-9]{2}|7[0-5][0-9]|76[0-2])' "$FBDLOG")" "2"
+    check "fbdrain t$t: both clocks alive (no zero-tick drain)" \
+          "$(grep -cx 'FBDRAIN_CLOCK_DEAD=' "$FBDLOG")" "1"
+    check "fbdrain t$t: verdict PASS" "$(grep -cx 'FBDRAIN_VERDICT=PASS' "$FBDLOG")" "1"
+    check "fbdrain t$t: probe exit status" "$fdrc" "0"
+done
+check "fbdrain: timers 0 1 2 3 each ran, each pinned" "${fbd_ran:-none}" "0123"
+
+#  ---------------------------------------------------------------------------------------
 #  #439/#440 PIT 8253 latch + LSB/MSB selector -- pitlatch / pitclobber.
 #
--- a/tools/pipeline/check_probe_wiring.py
+++ b/tools/pipeline/check_probe_wiring.py
@@ -2500,4 +2500,7 @@
 #  is re-created a week out, deliberately and dated, not by copying.
 #
+#  *** #548, 2026-09-24: THE OTHER HALF IS GONE TOO. ***  fbpending_drain_probe.py is wired
+#  into gate_arm.sh and its entry deleted, so TEN of those eleven remain, still one block.
+#
 #  These are wiring jobs, not design ones.  NOT every probe here prints a verdict token or exits
 #  nonzero on failure: mk48_nvram_probe.py printed MK48_RESULT=n/m and a DONE sentinel and exited 0
@@ -2523,7 +2526,7 @@
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
--- a/regress/fbpending_drain_probe.py
+++ b/regress/fbpending_drain_probe.py
@@ -47,5 +47,5 @@
   (`freq / 100.0`) destroyed 99% of the guest's clock while passing this probe.
 
-ARM X -- THE PLACEMENT DISCRIMINATOR, and the reason it is not merely a second run.
+ARM X -- the reason it is not merely a second run.
   dev_footbridge.c never calls timer_remove() and never lowers the core frequency when
   the guest DISABLES a timer: TIMER_x_CONTROL without TIMER_ENABLE zeroes the counter
@@ -53,6 +53,14 @@
   counter that DEVICE_TICK will never look at.  Arm X arms the timer, immediately
   disables it, free-runs, re-enables (which does NOT clear the counter) and then
-  measures.  A non-zero result proves the counter accrues while the device is disabled
-  -- which is exactly the state in which a bound placed in DEVICE_TICK cannot run.
+  measures.  On the PRE-FIX build that result -- 3051, identical to arm D -- proved the
+  counter accrues while the device is disabled.  On a correct build X reads like D and
+  proves nothing about the disable: FILED as `fbdrainxdisable`.
+  *** #548: THE HEADING SAID "THE PLACEMENT DISCRIMINATOR" AND X IS NOT ONE -- MEASURED.
+  A bound moved into DEVICE_TICK reads X=1 and PASSES: the FREEZE's LOAD write sets the
+  bound to 1, and DEVICE_TICK clamps the count before the drain counts it.  gate 2
+  (diff_fbpending_bound.c R1/R2/R5/R6) catches that placement.  What X DOES catch is a
+  bound gated on a control bit its CTRL=0 write clears: TIMER_ENABLE, which gate 2 --
+  every arm of it enabled -- cannot see, and TIMER_FCLK_256, which gate 2's unprescaled
+  cases catch too.  X is the only GATED rung-3 witness of either. ***
 
 ARMS
@@ -71,9 +79,14 @@
 
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
 import os, pty, re, select, signal, struct, sys, time
@@ -804,4 +817,7 @@
     print("VERDICT")
     print("=" * 78)
+    #  #548: WHICH timer this run measured, so gate 14 can pin it -- _opt() ignores an
+    #  unknown flag, so a mistyped --timer runs timer 0 with every other row green.
+    print("FBDRAIN_TIMER=%d base=0x%03x" % (TIMER_NR, TBASE))
     print("FBDRAIN_CONTROL=%s" % ("OK" if ok else "FAILED"))
     print("FBDRAIN_BACKLOG_D=%s" % bD)
--- a/regress/diff_fbpending_bound.c
+++ b/regress/diff_fbpending_bound.c
@@ -272,10 +272,25 @@
 	 *  where all four timers always agree and nothing is ever re-armed.
 	 *
-	 *  So: arm two timers at DIFFERENT rates, then RE-ARM one at a third, and
-	 *  require each timer's bound to track its own current rate.  Same oracle as
-	 *  R5 -- the peak the counter reaches -- so no new oracle is introduced.
+	 *  So: RE-ARM a timer at a different rate and require its bound to track the
+	 *  new one (R6), and give every timer a rate no other timer shares (R6b).  Same
+	 *  oracle as R5 -- the peak the counter reaches -- so no new oracle is introduced.
+	 *
+	 *  *** #548: A RE-ARM HAS TWO CELLS AND THIS ROW BUILT ONE. ***  The callback's
+	 *  `>=` splits a re-arm by where the count sits against the NEW bound: below it
+	 *  (timer 0, re-armed at count 0) or at or past it (timer 2, re-armed with 4096
+	 *  owed).  `==` for `>=` is identical in the first cell and, while nothing acks,
+	 *  never fires again in the second; it passed every row in the battery, and one
+	 *  guest CONTROL write left it 4529 owed against a bound of 762 (measured).  Owing
+	 *  4096 before timer 0's own re-arm would have TRADED the cells, not added one: a
+	 *  bound recomputed only while a backlog is owed then passed (measured).  Both, one
+	 *  row.  The owed and end counts are PRINTED and gate 2 pins the whole line, so an
+	 *  edit to this row -- `&&` to `||`, a smaller precharge, a drive aimed at the other
+	 *  timer -- cannot hand `==` its pass back (each measured).
+	 *  NOT rowed: the bound STORE sits under no predicate, so a store conditioned on the
+	 *  count (`pending != (int)bound`, `pending == 0 || pending >= (int)bound`) can split
+	 *  the cells further, at a count of exactly 762 or of 1..761.  Filed: fbbounddebt.
 	 */
 	{
-		int peak, trough;
+		int peak, trough, peak2, trough2, owed0, owed2, end0, end2;
 		struct footbridge_data *r6 =
 		    (struct footbridge_data *) calloc(1, sizeof(*r6));
@@ -283,18 +298,60 @@
 		fake_machine.emulated_hz = 50000000;
 		arm(r6, 0, 1, TIMER_ENABLE);			/*  50 MHz  */
-		arm(r6, 1, 256, TIMER_ENABLE | TIMER_FCLK_256);	/*  762 Hz  */
+		arm(r6, 2, 1, TIMER_ENABLE);			/*  50 MHz  */
+		drive(r6, 2, 4096, &peak2, &trough2);		/*  4096 owed  */
 
 		/*  RE-ARM timer 0 much slower.  A frozen bound keeps 50e6 here.  */
+		owed0 = r6->pending_timer_interrupts[0];
 		arm(r6, 0, 256, TIMER_ENABLE | TIMER_FCLK_256);
 		drive(r6, 0, 4096, &peak, &trough);
+		end0 = r6->pending_timer_interrupts[0];
+		/*  and timer 2, whose debt is ABOVE the new bound when it lands.  */
+		owed2 = r6->pending_timer_interrupts[2];
+		arm(r6, 2, 256, TIMER_ENABLE | TIMER_FCLK_256);
+		drive(r6, 2, 4096, &peak2, &trough2);
+		end2 = r6->pending_timer_interrupts[2];
+		/*  The END counts tie each peak to its own timer: under the bound, 4096 ticks
+		    leave ((4096-1) mod 762)+1 = 286 on both, and a drive retargeted at the other
+		    timer leaves 4096 behind (pass 2's one ask, measured).  */
 		row("R6 a re-armed timer's bound follows its NEW rate",
-		    peak == 762, "timer 0 re-armed 50 MHz -> 762 Hz: peak %d want 762",
-		    peak);
-
-		/*  And timer 1 must carry ITS own bound, not timer 0's.  */
-		drive(r6, 1, 4096, &peak, &trough);
-		row("R6b each timer carries its OWN bound",
-		    peak == 762, "timer 1: peak %d want 762", peak);
+		    owed0 == 0 && owed2 == 4096 && peak == 762 && peak2 == 762 &&
+		    end0 >= 1 && end0 <= 762 && end2 >= 1 && end2 <= 762,
+		    "re-armed 50 MHz -> 762 Hz: timer 0 at count %d peak %d end %d, timer 2 "
+		    "owing %d peak %d end %d; want 762", owed0, peak, end0, owed2, peak2,
+		    end2);
 		free(r6);
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
+	 *  timer's slot shows too.
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
@@ -288,9 +288,9 @@
 	 *
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
 	 *  Floor 1.  *** ITS ORIGINAL JUSTIFICATION WAS MEASURED FALSE and is
--- a/regress/gate_offline.sh
+++ b/regress/gate_offline.sh
@@ -1309,5 +1309,6 @@
 #  It #includes the shipped dev_footbridge.c and calls timer_tickN() directly, which the
 #  witness ladder's mechanical discriminator classes as never-a-reproduction.  The
-#  reproduction is regress/fbpending_drain_probe.py (rung 3) and it is NOT run here.
+#  reproduction is regress/fbpending_drain_probe.py (rung 3) and it is NOT run here --
+#  gate 14 (gate_arm.sh) runs it on all four timers, since #548.
 #
 #  BOTH SHIP BECAUSE NEITHER ALONE IS ENOUGH -- measured, not assumed:
@@ -1323,6 +1324,8 @@
 #  the REAL footbridge rather than re-implementations.  Measured kills: pre-fix fails R1 x7
 #  and R2 with trough -2147483648 (the overflow itself); reset-to-0 fails R3 x7; a fix applied
-#  to one callback only fails R1 x7; no-ceiling fails R1 on the two high-hz cases and R2 with
-#  peak 2147483647.
+#  to one callback only fails R1 x7; no-ceiling fails R1 (and, since R5 exists, R5) on the two
+#  high-hz cases -- and NOT R2, which this said until #548: R2 stays green at peak 2147483647,
+#  trough 1, because the compare precedes the ++ (measured: regress/artifacts/
+#  fbdrainwire_20260924/opus548_measured/runs_p1/diff_fbb_M_noceil.out).
 FBBIN=$LOGDIR/diff_fbpending_bound
 FBLOG=$LOGDIR/diff_fbpending_bound.log
@@ -1344,4 +1347,12 @@
         check "fbpending bound: R2 actually ran (not SKIPPED)"               "$(grep -c 'R2 no signed overflow.*direct ticks' "$FBLOG")" "1"
         check_min "fbpending bound: rows actually run"               "$(grep -cE '^  (ok|FAIL) ' "$FBLOG")" 15
+        #  #548: NAMED ROWS for R6 and R6b, each the sole detector of its cells.  They pin the
+        #  PRINTED values -- the owed counts, every peak, the end counts -- so an edit to the
+        #  row's own condition (`&&` to `||`, a smaller precharge, a drive aimed at the other
+        #  timer) cannot pass a wrong value.
+        check "fbpending bound: R6 re-arm cells (count 0, then 4096 owed)" \
+              "$(grep -cF 'timer 0 at count 0 peak 762 end 286, timer 2 owing 4096 peak 762 end 286; want 762' "$FBLOG")" "1"
+        check "fbpending bound: R6b four timers at four distinct rates" \
+              "$(grep -cF 'distinct rates: peaks 762 1525 3051 6103 want 762 1525 3051 6103' "$FBLOG")" "1"
     fi
 fi
```

## 6. THE THREE QUESTIONS

1. Adjudicate F1..F32 and D1..D4 -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted about twenty findings in a row.  Name the count.
3. **WHAT DID ALL NINE OF US MISS?**  You now have the whole panel's output and the repair.
