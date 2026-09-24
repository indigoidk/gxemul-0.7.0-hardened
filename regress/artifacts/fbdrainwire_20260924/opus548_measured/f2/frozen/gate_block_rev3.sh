#  #548 fbdrainwire: #442's RUNG-3 DRAIN PROBE, wired before its exemption lapsed.
#
#  The guest arms footbridge timer N at 762.94 Hz (TIMER_FCLK_256, load 256, -E cats' 50 MHz),
#  free-runs 4 s WITHOUT acking, freezes the timer and counts the backlog one TIMER_x_CLEAR at
#  a time.  #442's bound resets the counter to 1 once it reaches (int)762.94 = 762, so the
#  count can never exceed 762 -- the tightest cap that cannot false-fail.
#
#  ALL FOUR TIMERS, because ONE WAS MEASURED NOT TO BE ENOUGH (#548 pass 1, the Opus seat): a
#  bound applied only while the timer is enabled, with timer 0 exempt, reads 3/3 on timer 0
#  and X=3051 on timer 1, and passes BOTH gate-2 differentials (diff_fbpending_bound.c arms
#  every timer enabled; diff_footbridge.c never calls the callbacks).  Arm X -- disabled
#  through the accrual -- is the battery's only GATED witness of a bound gated on
#  TIMER_ENABLE, and it sees it only on the timer it runs: the ENABLE half of #442's
#  clause-(e) debt, closed here.  About 17 s per timer.  Each run is PINNED to its timer and
#  the loop to all four, because a mistyped --timer is ignored and runs timer 0 (pass 2).
#
#  THE CONTRACT (clause e).  From zero, with nothing acked, N >= 1 delivered ticks and bound B
#  leave the count at ((N-1) mod B)+1.  At 4 s N is about 3051; it follows the SIGALRM clock.
#    CATCHES  the bound REMOVED on any timer (3051 on all four, measured); a bound gated on a
#             control bit X's CTRL=0 write clears -- TIMER_ENABLE, and TIMER_FCLK_256, which
#             gate 2's unprescaled cases also catch; and any B >= N, which reads N (M_x8,
#             measured).  All three only while N > 762.
#    NOT CLAIMED  a raise to 762 < B < N fails only when that count exceeds 762 (freq * 2,
#             B = 1525, reads 1); `>` for `>=` only when N is a multiple of 763, and reset-to-0
#             only then too, as a dead clock; a reset to 2 never.  A LOWERING stays under the
#             cap by construction, and a deleted ceiling does not bind at 762 Hz.  A bound
#             moved into DEVICE_TICK reads 1 on both arms: the FREEZE sets the bound to 1 and
#             DEVICE_TICK clamps the count before the drain counts it.  All of those are gate 2's
#             (diff_fbpending_bound.c R1/R2/R3/R5/R6/R6b).  So is `==` for `>=`, which never
#             fires once a re-arm lowers the bound below an un-acked count: it passed every row
#             here and in gate 2 until #548 gave R6 its second cell (a re-arm with 4096 owed).
#             A bound skipped under a control value no instrument drives the callback with --
#             TIMER_MODE_PERIODIC and TIMER_FCLK_16 measured, TIMER_EXTERNAL by reading --
#             passes every row here and in gate 2: FILED as `fbboundmodes`.  And arm X's ENABLE
#             witness assumes its disable executed, which nothing checks on a correct build (X
#             reads 3, like D): FILED as `fbdrainxdisable`.  Edits to the probe's own logic are
#             reviewed, not rowed, beyond the pins below.
#    LOAD     Pinned to one core behind 12 busy loops, N fell from 3051 to 1183 and the
#             removed-bound mutant still went red; below N = 763 it would pass SILENTLY.
#             Neither starved run failed a correct build, but the probe's own budgets (L1 wants
#             1000 accrual iterations; its prompt waits) could.
#
#  `gatedevicesplit` is OWED (#498): one more device probe in the ARM gate, on this gate's own
#  -E cats machine like footbridge_sites_probe.py above.  Recorded, not compounded silently.
fbd_ran=""
for t in 0 1 2 3; do
    FBDLOG=$LOGDIR/fbpending_drain_t$t.log
    fdrc=0
    python3 -u fbpending_drain_probe.py "$PMAX" "$STUB" --expect-cap 762 --accrue 4 --timer "$t" \
        > "$FBDLOG" 2>&1 || fdrc=$?
    grep -E '^  FAIL |^FBDRAIN_' "$FBDLOG" | sed 's/^/       /'
    #  ONE verdict line, and a DECIDING one: REPORT-ONLY (a failed control, or no cap parsed)
    #  must not read as completion.  When it fires, the rows below do not run for this timer.
    if [ "$(grep -c '^FBDRAIN_VERDICT=' "$FBDLOG")" != "1" ] ||
       ! grep -Eqx 'FBDRAIN_VERDICT=(PASS|FAIL)' "$FBDLOG"; then
        note "fbpending drain probe, timer $t: no unique PASS/FAIL verdict; last lines follow"
        tail -5 "$FBDLOG" | sed 's/^/       /'
        check "fbdrain t$t: the probe reached a verdict" "no" "yes"
        continue
    fi
    check "fbdrain t$t: the probe reached a verdict" "yes" "yes"
    #  WHICH TIMER RAN and WHAT IT WAS ASKED.  Without these, one token -- a mistyped --timer, or
    #  the probe's load or --accrue changed -- keeps every row green while measuring timer 0 four
    #  times, or at a rate where a removed bound reads under the cap (pass 2, measured).
    fbdtimer="FBDRAIN_TIMER=$t base=0x$(printf '%03x' $((0x300 + 0x20 * t)))"
    fbdn=$(grep -cx "$fbdtimer" "$FBDLOG")
    [ "$fbdn" = "1" ] && fbd_ran="$fbd_ran$t"
    check "fbdrain t$t: the run measured timer $t" "$fbdn" "1"
    check "fbdrain t$t: asked for 4 s at 762.94 Hz (uncapped prediction 3052)" \
          "$(grep -cx '  UNCAPPED prediction: backlog = 3052' "$FBDLOG")" "1"
    #  THE CONTROLS FIRST.  FBDRAIN_CONTROL=OK is an AGGREGATE that stays OK if a row is DELETED
    #  from the probe, so the twelve control rows are pinned by DISTINCT GREEN ids as well.
    check "fbdrain t$t: controls prove the probe measures" \
          "$(grep -cx 'FBDRAIN_CONTROL=OK' "$FBDLOG")" "1"
    check "fbdrain t$t: R0 C1 C2 A1 A2 E H1 H2 T L1 L2 P, twelve DISTINCT green ids" \
          "$(grep -E '^  ok   (R0|C1|C2|A1|A2|E|H1|H2|T|L1|L2|P) ' "$FBDLOG" | awk '{print $2}' | sort -u | wc -l | tr -d ' ')" "12"
    #  The cap the probe PARSED, the counts, both clocks, the verdict, the exit status.  A
    #  correct build always owes at least one tick (the reset is to 1), so a count of 0 that is
    #  not the poison word is a measurement that did not happen.  CLOCK_DEAD is matched as a
    #  WHOLE LINE: an extract compared to "" is green on a log with no such line (measured).
    check "fbdrain t$t: bounded at the asserted cap 762" \
          "$(grep -cx 'FBDRAIN_BOUNDED=YES  (cap asserted: 762)' "$FBDLOG")" "1"
    check "fbdrain t$t: both backlogs in [1, 762]" \
          "$(grep -Ecx 'FBDRAIN_BACKLOG_[DX]=([1-9]|[1-9][0-9]|[1-6][0-9]{2}|7[0-5][0-9]|76[0-2])' "$FBDLOG")" "2"
    check "fbdrain t$t: both clocks alive (no zero-tick drain)" \
          "$(grep -cx 'FBDRAIN_CLOCK_DEAD=' "$FBDLOG")" "1"
    check "fbdrain t$t: verdict PASS" "$(grep -cx 'FBDRAIN_VERDICT=PASS' "$FBDLOG")" "1"
    check "fbdrain t$t: probe exit status" "$fdrc" "0"
done
check "fbdrain: timers 0 1 2 3 each ran, each pinned" "${fbd_ran:-none}" "0123"
