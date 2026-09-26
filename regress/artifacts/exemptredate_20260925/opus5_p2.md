**VERDICT: SHIP WITH CHANGES.** The schedule and selftest numbers in section 4 hold exactly. Four of the fourteen rulings are implemented wrongly or only in part (R1, R2, R6, S1), and one reason line cites the wrong queue item. Each fix is a phrase in a comment. No date needs to move.

1. **Q3: section 4 is confirmed (measured).** I exported HEAD into WSL `/tmp` and swapped in the three v2 blobs.
   - **Control:** HEAD's own checker passes on 09-27 and fails with 10 problems on 09-28, so the apparatus can go red.
   - **Every day from 09-25 to 12-31, with the v2 checker:** it passes through 10-08 (14 days). There are exactly 10 transition days: 10-09, 10-16, 10-23, 10-24, 10-27, 10-28, 11-06, 11-13, 11-20 and 12-04.
   - **One entry per day:** at most one new expiry on any day, and no non-expiry failure on any day. 12-03 shows 9 expired and 12-04 shows 10. Every line in section 4 matches.
   - **`--selftest`:** 22/22.
   - **Gate 2's helper beside gate 9's list:** wdc_identify goes red from 09-28, gate 9's twelve entries from 12-01, and ieee_store from 12-11. ieee_store's day is its own.

2. **S4: the commit mechanics are sound (measured).**
   - The committed checker blob contains no crime_width or fbctrl lines, and the committed `precommit_check.sh` keeps HEAD's pin of 30.
   - The working copies keep their parked hunks (pin 32; 16 crime_width lines, 1 fbctrl line) and contain all of #550's added lines (62 of 62 and 2 of 2).
   - The v2 `gate_offline.sh` is identical to the working-copy version (it has no parked hunk).

3. **Q1: four rulings are implemented wrongly or only in part.**
   - **R2 (measured).** The new line says `chk()` "has carried 24 got/want rows". HEAD has 24 `chk()` calls: 16 got/want, and 8 that hand it a 0/1 verdict (lines 4870, 4878, 4932, 4948, 4956, 4974, 5066, 5072). The ruling's own #551 item 2 says 16 + 8, so #550's line would contradict #551's bullet in the same series. The quote is also only a fragment ("The nine row functions"). And the nine functions still exist, with 16 call statements; what is stale is that the paragraph leaves out `chk()`'s rows. Suggested wording: "since #484, 24 `chk()` calls: 16 got/want, 8 handing it a 0/1 verdict".
   - **R6 (measured).** "It searches gate_*.sh, where the machine never appears" is false. `gate_asan_sweep.sh:594` runs `"$ASAN_HEAD" -E sgi -e "$s"`, which is exactly what the extended regex matched. Suggested wording: "where only gate 9's construction sweep names the machine; guest-session probes exec it themselves".
   - **S1 (measured).** The lca_badval, lca_widewrite and lca_isalane lines each end "so they fall due together". They don't: the four Alpha entries expire on four separate days (10-23, 10-24, 10-27, 10-28). The header's "within days of each other" is right. Use the ruling's text: "same alphabook1 home; one round discharges all four".
   - **R1 (read).** The dates are split per entry, but ieee_store lost its owner action. "Owner row: `scexempt` -- discharge, re-decide or delete before then" is gone, and `scexempt` is named only once, in the shared line. Suggested fix, one clause: "ieee_store … RED from 2026-12-11; owner row `scexempt`: discharge, re-decide or delete before then."
   - **Implemented as ruled:** R3 (nine counters at both sites, matching the `== 0` terms of DIFF_PASS), R4 (12-10 collides with nothing), R7 (i)-(iii), R8, R9, R10, S2's header sentence, S3, S4 and the "22 mutants" rider. R5's deriver is thin: it lacks the ruling's "against 568 s for ip30".

4. **Q2: are any of the ten reasons still false? (read, and measured where marked)**
   - **ppc_rldicl:** holds. HEAD and parked probes both score 24/24 with identical rows.
   - **ip30:** holds (measured). gate_arm.sh runs seven `-E sgi -e ip32` probes; the run took 568 s for 33/33; no session sends `quit`, and any exit scores as not-alive.
   - **The four Alpha probes:** holds. Each sends `quit` and prints its RESULT and DONE tokens.
   - **4bit and addtoinbuf:** hold. No gate builds a poisoned CD image.
   - **wdc_altoffset (the parent): misattributed.** It cites `wdcaltoffleg` (a), but (a) asks for an exit status. The probe does exit 0 whatever `ok` says (no `sys.exit`). The real reason it needs a pre-fix binary is that every ROWS entry carries a committed-leg want `wb` (lines 606-608). `b_hit and f_hit` only say both legs parked, and that weaker wording was mine at F2. Name both owed items.
   - **sig:** "gate 10 already carries the malta image" is imprecise. `wdc-scratch-64m.img` runs on landisk (wdc_flood), and gate 10's malta session (wdc_altdigin) writes its own 8 MB disk. What is true is simpler: sig takes any image as `argv[2]` and adds `ciR:` itself.
   - **Order:** right. The cheapest comes first, the Alpha four are one decision on consecutive working days, the wdc entries are weekly, and ieee_store falls last.

5. **Q5: wrong records in the added comments.**
   - ppc's line says "The parked working-tree edit of its want_rldimi touches no scored row". That is committed text about uncommitted state; it means nothing in a fresh clone and goes stale once the edit is adopted. The edit also rewrites `mask32`, not just `want_rldimi`.
   - "About 570 s" and "24/24 in under a second" name no deriver, and their logs were in `/tmp`. I preserved them under `opus550_measured_p2/p1_runs/`; cite that path.
   - "Filed as `exemptdistinct`" is not filed yet (measured: no hit in OUTSTANDING_BUGS.md). OUTSTANDING_BUGS.md:21900-21905 (`scexempt`) still says "nine row functions" and "Decide before 2026-09-28". Both must land in the same commit.

6. **Q6 (read):** ppc_rldicl is cheaper to wire than to re-date: a few print lines plus a gate_ppc block copied from its two siblings, and it runs in under a second. Recorded as a finding only, since the owner ruled out wiring this week.

Everything is saved in `GXEMUL-SEC/regress/artifacts/exemptredate_20260925/opus550_measured_p2/`. `schedule_daily.out`, `selftest_550v2.out` and `control_and_lists.out` carry section 4's check. The other logs are `s4_blobs.out`, `chk_census.out`, `chk_calls_HEAD.txt` and `reason_facts.out`, plus the scripts and `sched550v2.py.txt`. Every log ends in its completion sentinel. `p1_runs/` holds the pass-1 logs; the lca_isalane log there is incomplete and marked so. I also corrected a wrong line in my own list log: "AB:n=1" for an empty set now reads n=0. Nothing else under the project was written, and all of my processes are stopped.

---
*Recorded by the main loop: agent a8c6fd47a6c9c37ac (resumed for the pass 2 on the final diff), `agent_models.py` = clean, claude-opus-5-5; final text 2026-09-25T21:19:29.948Z UTC.  Same model family as the main loop: badge s.*
