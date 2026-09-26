# #550 + #551 -- the ADJUDICATION of the F2 pass on pass 2 (Fable 5.1, LAST; Astra confirms after 07:01)

Open with `FABLE550551F2B_ALIVE`, then `VERDICT #550: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>` and `VERDICT #551: <...>`,
numbered rulings, and **the count of my dispositions below that you change**; under ~1200 words.  READ-ONLY under
`C:\DocumentNoSnc\cc\GXEMUL\`; measure only in WSL `/tmp` if at all.  Owner ruling 2026-09-25: codex (Astra) is walled
until 2026-09-26 07:01; you adjudicate on the seats that answered; nothing is committed before Astra confirms.

## Evidence (all under `GXEMUL-SEC/regress/artifacts/`)

* The F2 packet I sent (my first dispositions, P1-P19 for #550, Q1-Q10 for #551, and the repair then):
  `wdcidselfcheck_20260925/f2b/f2b_brief_550_551.md`.
* The seats that answered it: `wdcidselfcheck_20260925/panels/panel_20260925_163352/` (agy SHIP/SHIP; grok, glm,
  minimax, kimi-k3:cloud SHIP WITH CHANGES; deepseek SHIP/SHIP, short but complete; codex WALLED -- a seat failure; the
  kimi CLI walled, covered), `wdcidselfcheck_20260925/f2b/grok_dedicated_f2b.txt`, and the Opus 5.5 measuring seats
  (`exemptredate_20260925/opus5_f2b.md`, `wdcidselfcheck_20260925/opus5_f2b.md`; both `agent_models.py` = clean).
* The findings, as I queued and CHECKED them: `exemptredate_20260925/fable_f2b/pending_f2b_550.md` (A-G, L) and
  `wdcidselfcheck_20260925/fable_f2b/pending_f2b_551.md` (H-K).
* The repair as it now stands -- #550 v3 final and #551c, both BUILT and MEASURED:
  `exemptredate_20260925/fable_f2b/diff550_HEAD_v3_cpw.diff`, `diff550_HEAD_v3_goff.diff` (and `diff550_v2_v3final_cpw.diff`
  for what changed since pass 2); `wdcidselfcheck_20260925/fable_f2b/diff551c_HEAD_wdcid.diff`,
  `diff551c_on550v3_goff.diff` (and `diff551_b_c_wdcid.diff` for what changed since the F2 packet).
* Measurements: #550 -- the checker's schedule and selftest re-run on a HEAD export carrying v3 final: the same
  problem count on every step date (1 on 10-09 ... 10 on 12-04) and `--selftest` 22/22 (`exemptredate_20260925/measured/`).
  #551c -- `wdcidselfcheck_20260925/measured/run551c.out`: 14 of 14 byte-identical to HEAD's file except the SELFCHECK
  lines, same exit codes, seven device variants at -O2 and -O0; RED: chk() / row_cmp() stubbed, each disjunct dropped,
  `&& got`, u16, sect4, minimax's `<`, `&& sectors`, the tally reset (drqring "2 failures", w57hi "4 failures", FAIL),
  and the double edit (now "1 failures", FAIL); GREEN as disclosed: the post-increment rows test, the name test,
  `want-165`, the feed edit, the phase (name-prefix) test; the block deleted: PASS with no G line and no token.

## What changed since the F2 packet, and my disposition on each (please rule on EACH)

**#550 (comments and manifest strings only; no date moves):**
1. P5's fix was itself FALSE (Opus, grok ded., grok): 14 of the parent's 18 ROWS have wb == wf -- CHECKED by parsing.
   Now: "owes an exit status (`wdcaltoffleg' (a) ...) and a single-leg form: four of its 18 rows want the committed
   build's defect, which the gate's one binary cannot supply."
2. P2's fix named the wrong block (grok ded., grok): the extended pattern matches ONE line, gate 9's #450 row -- CHECKED.
   Now names the #450 row; the seven-probe deriver is digit-safe (glm) and "each execs -e ip32" is stated per probe.
3. P8: the 568 s now cites `keep_p1_logs.out` (from file mtimes) and the twelve-deriver keys on the list's own quotes
   (Opus, glm); P9: "(gate 9 only constructs them)" (Opus, grok ded.); P15: the ppc owed-line no longer states the premise
   the sentence above it refutes, and P7's claim carries a deriver (Opus, grok, kimi-k3); P12: "10-29, the Thursday
   after, is unused: the ruling's schedule gives it no entry", and 11-26 is named (glm, grok, kimi-k3, Opus).
4. P14 -- NO TEXT CHANGE, but my stated reason was FALSE (Opus): a gate home for alphabook1 is the same kind of work as
   ip30's (gate_arm.sh already runs non-ARM probes).  The order stands on the real reasons, which the round record will
   carry: #540's parked PHYSICAL change sits in dev_lca.c, and the Alpha four run longer together.
5. P16: a NOTE beside `schedule_v2.out` that its 12-04 "7" is my script's cut of "71" (v3's run prints it whole).

**#551 (#551c, measured):**
6. H -- the tally reset (Opus MEASURED; grok ded., agy): FIXED -- `cmp_fails`, counted only by the comparators and
   restored by the self-check, and the trailer reports the larger; untampered runs byte-identical.  (Alternative: disclose.)
7. I + minimax -- `&& sectors` and `<` for `!=` answered every row_cmp() probe right: FIXED -- two probes, (sectors 0, 1, 0)
   and (0, 0, 1), each disjunct wrong alone with got ABOVE its want.  "Each operand zero and past 32 bits" is now true.
8. grok (panel) -- the double edit's trailer read "0 failures" with FAIL: FIXED -- a self-check that did not pass counts
   one failure.
9. kimi-k3, grok -- a phase flag / probe-identity key; glm -- an edit of the block's own bookkeeping: DISCLOSED, in glm's
   general form: "the self-check proves only that the comparators answer right on ITS OWN calls, so an edit that keeps
   those answers and changes the rest keeps every gate-2 row green -- a value, a name, a position or the self-check's own
   phase the probes do not share; a feed edit; an edit of this block itself".
10. glm -- clear `sc_g` on entry: NO CHANGE -- `main(void)` calls the block exactly twice; the line would have no
    measurable effect (the addition licence).
11. J -- my F2 packet's Q10 said H greps the run's output: WRONG, it greps the SOURCE; and the record will carry the
    second deletion form (block and calls deleted, `sc_g` left: the run FAILs) -- records only.

## Questions

1. **Which of 1-11 is wrong?  Name the count.**  Be hardest on 6 (fix vs disclose) and 10 (no change).
2. **Does #551c owe its own pass?**  It adds detector material (two probes, `cmp_fails`, the trailer lines) in response
   to the F2 pass.  My position: yes, one pass on #551c's diff, closing on a valid zero -- and it can be tomorrow's
   Astra confirmation plus the codex seat's re-fire on the same packet, rather than another full panel tonight.  Is that
   a valid pass under the repair-chain rule, or does it need the panel?
3. **#550 closes on this adjudication?**  Its changes since pass 2 are records only.
4. **The commit order and the clock:** #550 then #551 then #549, all after Astra (07:01); wdc_identify's exemption is
   valid ON 2026-09-27 and #550 alone keeps it -- #551 must land by then.  Anything wrong with that plan?

If, while verifying a claim, you found something ELSE -- say so.
