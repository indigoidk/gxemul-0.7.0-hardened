# n6 / #539 -- FLAGSHIP ADJUDICATION of pass 2 + §F2, fired LAST.  SHORT by design: every fact is inlined; bounded reads.

Open with the token FABLE_SEAT_ALIVE_20260919_N6F2 and the verbatim first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.  VERDICT LINE FIRST.  Read-only; run nothing.  Read AT MOST these
files, in this order, and stop reading when you have what you need: (1) `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\n6\p2\f2_packet_BUILT.md`
(13 KB: the 23 findings with my dispositions, D1-D3, table 2); (2) this file's digest below; (3) the v4 diff
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\n6\p2\diff539_4files.v4.patch` (790 lines) and `diff539_gate.v4.patch` (56 lines) -- the
working tree of `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` is at exactly this state; (4) only if a ruling needs it, one
seat file under `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\panel_20260919_035324\` (§F2) or `panel_20260919_021100\` (pass 2).
Your pass-1 ruling is `_scratchpad\n6\fable5_p1_20260919.md`; you hold two hats again (ninth seat + adjudicator).

## WHAT HAPPENED SINCE YOUR PASS-1 RULING (digest, all inlined)
* IMPLEMENTED as you ruled: fix = member 4; K arm bridged to +0x18c (`0xE590718C`, text `ENABLE CLEAR`) in all three
  probes; arm E with EC1,EA1,E0,E1,E2,E3,E6,E5,E4 (19 rows); (j) disclosed; F11 done with codex L3's drafts (drain to
  EOF, survived(), K rows require complaint AND exit 1).  Records sentence you said does not exist DOES exist with other
  words: OUTSTANDING_BUGS.md:2681-2682 "#218-#223 ... footbridge ... guest-reachable exit(1)s -> graceful" (corrected in
  place at the records step).
* TABLE 1 (scratch clone, PRETABLE before it): pre-fix RED 10/19; base 19/19; (a)(b)(f)(l) killed by E-arm death,
  (c)(d) by E1, (e) by E4 alone, (g) E2+E5, (h) E2+E3+E6, (i) E5, (k) K1, (j) ESCAPED 19/19 as disclosed.
* PASS 2 (8 transports + a dedicated codex job; Opus WALLED by the Anthropic session limit -- SEAT FAILURE):
  codex GO-WITH-CHANGES, agy GO-WITH-CHANGES, grok RATIFY, kimi CLI STALLED on its 50 KB read cap then ACCEPT on a
  paged re-fire, glm/deepseek/minimax/kimi-k3 ACCEPT with nits.  All applied (v2): bounded reap in all three probes;
  sites teardown drains to EOF, fatals after; gate: distinct-id check, exact excerpt grep, E2 label; A2 ':548';
  7.3.32->7.3.33; drain header K arm; 'neither is a rotated immediate' (false for Q); (k) wording; TIMER_x_LOAD ->
  `case TIMER_1_LOAD`; '!(idata & TIMER_ENABLE)' literal; tested patterns.  minimax's "I=0 means register offset" was
  REFUTED (I=0 is the immediate form; D1 0 mismatches).
* TABLE 2 (v2 instrument): base green on all three probes; x_exit2 (complaint then exit(2)) and y_sigkill (complaint
  then SIGKILL) each RED 3/3 K rows.
* §F2 (7 live transports; codex WALLED 'usage limit ... 6:59 AM' -- SEAT FAILURE): deepseek/glm/kimi-k3/minimax/agy/
  grok/kimi CLI.  CONVERGED on ONE real miss: a HEALTHY child slower than the 5 s budget (LeakSanitizer at exit on the
  asan build; a loaded host) is SIGKILLed by the harness and reads byte-identical to y_sigkill's red -- a false red
  attributed to the product.  APPLIED (v3): budgets 20 s drain + 10 s reap (patience, not an oracle: a healthy child
  exits in ms; base sites runs 4 arms in ~1 s) and a HARNESS-fired kill is LABELLED `HARNESS-KILL(<sig>)` in the reaped
  status so a red from it is attributed to the harness.  grok (self-review of its RATIFY) OVERTURNED my F14 partial:
  "exit 1 without the complaint" is a one-line PRODUCT mutant, not a mock -> TABLE 3 built it (z_silentexit); grok also
  found three leftovers, applied: the gate comment's `TIMER_x_LOAD`, the drain/witness T rows' `rT.get(6) != VENDOR`
  (None != VENDOR is True: keys now required), and the contract's "bits 30/31" (bit 31 never set -> "bit 30; bit 31
  UNTESTED").  glm's F7 doubt (is 0x18c really IRQEnableClear?) is settled by the inlined Table 7-10 line 6827
  "18Ch -- IRQEnableClear".  kimi-k3/glm's "the drain is unbounded" is a packet-blind guess: rd() returns True on
  timeout and the loop breaks only on EOF or the deadline (kimi CLI read it).  agy's "the sites drain spins 5 s every
  arm" is refuted by the measured wall: 4 arms in ~1 s.
* TABLE 3 (v3 instrument): base_v3 green on all three probes (sites 19/19; drain CONTROL=OK; witness PASS); z_silentexit (CLEAR read:
  exit(1) kept, the complaint DELETED) RED 3/3 K rows (sites K1; drain K exit=1 no complaint; witness K likewise)
  -- `regress/artifacts/n6/killtable_20260919/table3_v3/TABLE3.log`.
* THEN the kimi CLI's §F2 self-review (143 KB, answered late) found two residuals in the v3 teardown, APPLIED as v4
  (`diff539_4files.v4.patch` md5 b9706294; the gate diff unchanged, 2d7831b9): (1) the reap poll's `except OSError:
  break` fell INTO the SIGKILL branch -- on ECHILD the pid may be recycled and a kill there is certainly wrong; a
  `gone` flag now skips it; (2) a drain-deadline expiry closes the master under a LIVE child and the reaped SIGHUP
  read like a product death; the expiry is now recorded and the status labelled HARNESS-CLOSE(<sig>).  Its third
  residual -- the final waitpid after SIGKILL is unbounded for a child in uninterruptible sleep -- is RECORDED, not
  fixed (a hang there is a probe timeout, never a wrong verdict).  TABLE 4 = base_v4 on the three probes: sites 19/19, drain CONTROL=OK (K exit=1), witness PASS (`table4_v4/TABLE4.log`).

## QUESTIONS (one set)
 Q1 SHIP or HOLD: is the v4 diff right -- the fix, the bridge, arm E, the teardown as now written (20 s + 10 s,
    HARNESS-KILL label), the gate checks?  Name any floor breach (a)-(f) or L4 in the diff.
 Q2 WHICH OF MY DISPOSITIONS IS WRONG?  I accepted 17/23 on pass 2 and applied every §F2 correction that four or more
    seats converged on; the ones I REJECTED are F16 (744 vs 897 = two files), F17 (the if-branch is NO-PROMPT), F18
    (minimax's I-bit).  Be harder on the corrections I applied in response to §F2 than on the findings themselves.
 Q3 The seat record: two codex refusals + one codex wall + one Opus wall + one kimi read-cap stall this round.  Does the
    round SHIP on that roster (8 transports on pass 2, 7 on §F2, your ruling last), or HOLD for the Opus measurement
    (its base/mutant runs were cut off by the 429)?  The main loop's tables 1-3 are the round's only measurement.
 Q4 Standing licence: anything all of us missed.
End with the seat record: model, files read (which of the four), nothing run; and write your answer verbatim to
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\n6\fable5_f2_20260919.md`.
