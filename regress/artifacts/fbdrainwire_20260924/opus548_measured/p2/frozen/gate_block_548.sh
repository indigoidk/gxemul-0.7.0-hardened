#  #548 fbdrainwire: #442's RUNG-3 DRAIN PROBE, wired before its exemption lapsed.
#
#  The guest arms footbridge timer N at 762.94 Hz (TIMER_FCLK_256, load 256, -E cats' 50 MHz),
#  free-runs 4 s WITHOUT acking, freezes the timer and counts the backlog one TIMER_x_CLEAR at
#  a time.  #442's bound resets the counter to 1 once it reaches (int)762.94 = 762, so the
#  count can never exceed 762 -- the tightest cap that cannot false-fail.
#
#  ALL FOUR TIMERS, because ONE WAS MEASURED NOT TO BE ENOUGH (#548 pass 1, the Opus seat): a
#  bound applied only while the timer is enabled, with timer 0 exempt, reads 3/3 on timer 0
#  and X=3051 on timer 1, passes BOTH gate-2 differentials (every arm there is enabled), and
#  brings #442's dead clock back at rung 3.  Arm X -- disabled through the accrual -- is the
#  battery's only witness of a bound gated on TIMER_ENABLE, and it sees it only on the timer
#  it runs.  Clause-(e) debt of #442 (footbridge_pending() reads no control bit), closed here.
#  About 17 s per timer.
#
#  THE CONTRACT (clause e).  The count is ((N-1) mod B)+1 for N delivered ticks and bound B.
#    CATCHES  the bound REMOVED on any timer (3051 on all four, measured); a bound gated on a
#             control bit X's CTRL=0 write clears -- TIMER_ENABLE, and TIMER_FCLK_256, which
#             gate 2's unprescaled cases also catch; and any B >= N, which reads N.
#    NOT CLAIMED  a raise to 762 < B < N fails only when its residue exceeds 762 (freq * 2,
#             B = 1525, reads 1 and passes), and `>` for `>=` only when N is a multiple of
#             763.  A LOWERING, reset-to-0, a deleted ceiling or a bound moved into DEVICE_TICK
#             cannot show at all -- the FREEZE sets the bound to 1 before the drain counts, so
#             a clamp outside the callback collapses the backlog first (X=1).  All of those
#             are gate 2's (diff_fbpending_bound.c R1/R3/R5/R6).  So is `==` for `>=`, which
#             never fires once a re-arm lowers the bound below the count: it passed every row
#             here and in gate 2 until #548 gave R6 its second cell (a re-arm with 4096 owed).
#             A bound skipped in TIMER_MODE_PERIODIC passes EVERY instrument -- neither this
#             probe nor gate 2 ever sets that bit.  FILED as `fbboundmodes`.
#    LOAD     N follows the SIGALRM clock.  Pinned to one core behind 12 busy loops the
#             removed-bound mutant still read 1183: a starved run LOSES TEETH SILENTLY, it
#             never reds falsely.
#
#  `gatedevicesplit` is OWED (#498): one more device probe in the ARM gate, on this gate's own
#  -E cats machine like footbridge_sites_probe.py above.  Recorded, not compounded silently.
for t in 0 1 2 3; do
    FBDLOG=$LOGDIR/fbpending_drain_t$t.log
    fdrc=0
    python3 -u fbpending_drain_probe.py "$PMAX" "$STUB" --expect-cap 762 --accrue 4 --timer "$t" \
        > "$FBDLOG" 2>&1 || fdrc=$?
    grep -E '^  FAIL |^FBDRAIN_' "$FBDLOG" | sed 's/^/       /'
    #  ONE verdict line, and a DECIDING one: REPORT-ONLY (a failed control, or no cap parsed)
    #  must not read as completion.
    if [ "$(grep -c '^FBDRAIN_VERDICT=' "$FBDLOG")" != "1" ] ||
       ! grep -Eqx 'FBDRAIN_VERDICT=(PASS|FAIL)' "$FBDLOG"; then
        note "fbpending drain probe, timer $t: no unique PASS/FAIL verdict; last lines follow"
        tail -5 "$FBDLOG" | sed 's/^/       /'
        check "fbdrain t$t: the probe reached a verdict" "no" "yes"
        continue
    fi
    check "fbdrain t$t: the probe reached a verdict" "yes" "yes"
    #  THE CONTROLS FIRST.  FBDRAIN_CONTROL=OK is an AGGREGATE that stays OK if a row is DELETED
    #  from the probe, so the twelve control rows are pinned by DISTINCT GREEN ids as well.
    check "fbdrain t$t: controls prove the probe measures" \
          "$(grep -cx 'FBDRAIN_CONTROL=OK' "$FBDLOG")" "1"
    check "fbdrain t$t: R0 C1 C2 A1 A2 E H1 H2 T L1 L2 P, twelve DISTINCT green ids" \
          "$(grep -E '^  ok   (R0|C1|C2|A1|A2|E|H1|H2|T|L1|L2|P) ' "$FBDLOG" | awk '{print $2}' | sort -u | wc -l | tr -d ' ')" "12"
    #  The cap the probe PARSED, both clocks, the verdict, the exit status.  CLOCK_DEAD is matched
    #  as a WHOLE LINE: an extract compared to "" is green on a log with no such line (measured).
    check "fbdrain t$t: bounded at the asserted cap 762" \
          "$(grep -cx 'FBDRAIN_BOUNDED=YES  (cap asserted: 762)' "$FBDLOG")" "1"
    check "fbdrain t$t: both clocks alive (no zero-tick drain)" \
          "$(grep -cx 'FBDRAIN_CLOCK_DEAD=' "$FBDLOG")" "1"
    check "fbdrain t$t: verdict PASS" "$(grep -cx 'FBDRAIN_VERDICT=PASS' "$FBDLOG")" "1"
    check "fbdrain t$t: probe exit status" "$fdrc" "0"
done
