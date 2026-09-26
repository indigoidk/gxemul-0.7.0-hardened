# #550 exemptredate -- THE §F2 PASS: every seat's pass-1 findings, and my disposition on each

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (ignore any other `src/`).  **FIRST LINE:**
`VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.  **The load-bearing question: WHICH OF
MY DISPOSITIONS BELOW IS WRONG?  Name the count.**  If you raised a finding, be HARDER on it than on anyone else's,
including whether the fix I propose for it is right.  If you cannot read files, everything you need is inlined.

## SETTLED PREMISES (re-inlined; do not re-derive)

* Owner ruling 2026-09-24, verbatim: "Re-date all ten individually -- each gets its own date and reason now; no wiring
  work this week."  Owner ruling 2026-09-25 (the option chosen, verbatim): "Fix wdc_identify now -- a harness round
  right after #549 ... done before 09-28.  Only ieee_store gets re-dated."  So ieee_store's re-date IS the owner's
  (glm asked for this text; here it is).
* `check_probe_wiring.py` compares `d < today`: an entry is valid ON its date and red the day after; an expired entry
  STAYS in the failure list, and any failure blocks every commit.  Gate 2's SC_EXEMPT expiry reds one gate row.
* The pass-1 brief's diff and measurements: `p1_brief.md` in this directory (ten dates 2026-10-08..11-17; ieee_store
  2026-11-30; selftest 22/22; the expiry schedule).

## PASS 1 -- WHO SAID WHAT (panel_20260925_141424 + dedicated jobs; Opus measured)

SHIP WITH CHANGES: agy, grok (panel), glm, deepseek, minimax, grok (dedicated), Opus 5.5 (measured).  SHIP:
kimi-k3:cloud.  codex: WALLED (usage limit, resets 2026-09-26 07:01), panel seat and dedicated job -- a SEAT FAILURE,
not agreement.  kimi CLI: weekly wall, covered by kimi-k3:cloud.

## FINDINGS AND MY DISPOSITIONS (records = L4, fixed in this diff)

* **R1 (grok, glm, grok ded.): gate_offline.sh keeps "these are valid ON 2026-09-27 and RED from 2026-09-28" and
  "Owner row: `scexempt` -- ... before then" above a line that re-dates ieee_store.**  -> narrow both to wdc_identify.
* **R2 (grok ded.; Opus #551): the wdc_identify exemption reason ("nine row functions", "nothing to feed a mismatch
  to") is stale** -- the file has had `chk(name, got, want)` carrying 24 rows since #484.  My `#550` line repeated it.
  -> reword: "the owner ruled it FIXED -- #551 gives it a comparator self-check before 2026-09-28"; #551 replaces the
  stale paragraph itself.
* **R3 (Opus, grok ded.; MEASURED): ieee_store has NINE pass counters, not six** -- `diff_ieee_store.c`'s pass test is
  `abs_bad == 0 && unexplained == 0 && missed == 0 && ... inrange_diff == 0 && ... rm_rn_bad == 0 && rm_rz_bad == 0 &&
  ... rm_d_bad == 0 && rm_vec_bad == 0 && interp_bad == 0` (plus floors and three exact pins).  agy said six -- agy read
  the same lines and listed six; the source says nine.  -> "nine inline counters (the `== 0` terms of its DIFF_PASS
  test)".
* **R4 (Opus, grok ded.; MEASURED): 2026-11-30 is already a pile** -- gate 9's AB_EXEMPT dates all twelve of its
  entries 2026-11-30 (its own comment calls that a placeholder).  -> ieee_store moves (see the schedule).
* **R5 (Opus, grok, grok ded.; MEASURED): the ppc_rldicl reason is false as a dependency.**  No scored row calls
  `want_rldimi`/`want_rlwimi`/`want_rlwinm`/`mask32`; the parked working-tree edit touches only those; HEAD's probe and
  the parked one score 24/24 identically; `gate_ppc.sh` already runs this `-M 64` machine and scores the rldimi/rlwimi
  siblings with RESULT/CONTROL.  The comment the diff leaves -- "could only score its exit status" -- is false too (the
  probe prints ok/FAIL rows, `SCORE n/m` and a DONE line).  -> owed work restated: "RESULT/CONTROL lines, then a
  gate_ppc.sh block beside rldimi/rlwimi"; the false sentence corrected; and this becomes the FIRST date, as the cheapest.
* **R6 (Opus, grok, agy; MEASURED): the ip30 reason.**  "Binary-only" is true but true of all five cold-debugger probes;
  the kept #531 comment's `grep -ln "E sgi|-e ip30"` matches nothing as written (`|` is literal in a basic regex); and
  "no gate ... could host it today" is false -- `gate_arm.sh` already runs seven `-V -x -E sgi -e ip32` probes.  And
  it is not cheap: 568 s wall for 33/33 on `build/gxemul` (no session sends `quit`; each waits out a 12 s poll).
  -> reason restated ("gate_arm.sh hosts sgi cold-debugger probes; the probe must first stop waiting out a 12 s poll
  per session"); the #531 comment's grep and its "no gate" sentence corrected; SECOND date.
* **R7 (grok, grok ded.; read): the 4bit reason is false** -- `wdc_altoffset_4bit_probe.py` imports the encoder and
  `Emu` but runs its own `run_leg`; a single-leg mode in its sibling's `main()` does not carry over.  -> "its own leg
  loop owes its own single-leg mode".  And (Opus) the sig probe imports `wdc_altoffset_probe` too, so "shared with the
  4bit sibling" undercounts.
* **R8 (grok ded., grok; read): the Alpha reason's "parked LCA/Alpha adoption" is not a blocker** -- the four probes
  score committed fixes; the parked diff is #540's `PHYSICAL` flag and a comment.  What is true: no gate executes
  `-E alpha -e alphabook1`.  -> reason restated: "one harness round gives alphabook1 a gate home".
* **R9 (Opus): the `#520` paragraph sits above the ppc block, not above alpha_tbi; "Six exemptions remain" is present
  tense and stale; the four wdc entries name no queue row.**  -> move the paragraph, date the sentence as history, name
  `wiringcliff` in each wdc line.
* **R10 (deepseek): the title's "eleven" is false.**  -> **REJECTED**: ten checker entries + ieee_store = eleven
  entries re-dated (kimi reconciled the same arithmetic).

## THE SCHEDULE (the substantive change -- please rule on it)

* **S1 (Opus, grok, grok ded., kimi, minimax, glm): one-day spacing is a block under another name.**  The four Alpha
  probes share ONE prerequisite; dated 10-20..10-23 they go red Wed-Sat, and an expired entry stays red, so a slip is a
  four-entry push.  Same for the two wdc pairs.
  **PROPOSED:** weekly spacing, in owed-work order, every date its own Thursday, none on any other list's date:

      ppc_rldicl 2026-10-08   ip30 2026-10-15   alpha_tbi 2026-10-22   lca_badval 2026-10-29
      lca_widewrite 2026-11-05   lca_isalane 2026-11-12   wdc_altoffset 2026-11-19
      wdc_altoffset_4bit 2026-11-26   wdc_altoffset_sig 2026-12-03   wdc_addtoinbuf 2026-12-10
      ieee_store (gate 2) 2026-12-17

  The alternative: keep this week's horizon (ending 11-17) and only open the one-day clumps.  A week is the time one
  wiring round plausibly takes alongside other work, which is what makes "its own decision" true rather than asserted.
* **S2 (Opus, glm, kimi, deepseek, minimax; MEASURED by Opus): nothing enforces distinct dates** -- `"2026-10-22"` ->
  `"2026-10-21"` passes the checker, its selftest (22/22) and gate 2; and `DATE_RE` accepts `2026-19-08` (the known
  `exemptcal` gap).  **PROPOSED: FILE** a checker invariant (every dated DETECTOR exemption parses with `fromisoformat`,
  and no two share a date; two selftest mutants, the pin 22 -> 24), merged with `exemptcal`; and say in the header,
  now, that nothing enforces distinct dates.  Not built in #550: the owner scoped this week to dates, and a checker
  behaviour change owes its own negative controls.
* **S3 (Opus, grok ded.): gate 2's two entries share ONE row**, so while wdc_identify is red, ieee_store's expiry is
  invisible.  -> recorded; #551 removes wdc_identify before 09-28.
* **S4 (Opus; MEASURED): the commit mechanics.**  The working copy of `check_probe_wiring.py` carries #529's and #549's
  uncommitted lines; the pre-commit hook runs the ON-DISK file.  -> #550's edit is applied to the working copy too, and
  committed by the swap recipe (the committed blob is HEAD + #550 only).

## QUESTIONS
1. Which of my dispositions is wrong -- name the count.  Especially S1 (weekly) and S2 (file, not build).
2. Is there a reason line in R5-R8 that is STILL false as I restated it?
If, while verifying a claim, you found something ELSE -- say so.
