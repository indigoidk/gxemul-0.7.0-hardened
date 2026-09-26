# #551d's own pass -- EVERY SEAT'S FINDINGS, WITH MY DISPOSITION ON EACH (for the adjudication)

Pass: `pass551d_brief.md` (31 KB, the #551c -> #551d diff inlined, the whole self-check and trailer inlined, the #551c
pass's findings shared).  Answered: **agy** SHIP WITH CHANGES; **glm** SHIP WITH CHANGES; **deepseek** DO NOT SHIP;
**minimax** SHIP; **kimi-k3:cloud** (the kimi substitute) SHIP WITH CHANGES; **Opus 5.5** measuring seat SHIP WITH
CHANGES (33 shapes measured, `opus5_pass551d.md`, clean opus-5-5); **grok** (panel) and the **dedicated grok** job:
see the GROK section at the end.  **Codex (GPT-6 Astra) walled** (usage limit until 2026-09-26 07:01) and **the kimi
CLI walled** (weekly limit; covered by kimi-k3) -- SEAT FAILURES, not agreement.  Panel dir
`_scratchpad/panel_20260925_174800/`.

Gate 2's checks on this log, read from `gate_offline.sh` (these decide several dispositions below):
`grep -oE '[0-9]+ failures'` must be 0 (the PRINTED count); `grep -oE '^[0-9]+ rows'` must be AT LEAST 42
(`check_min`, not exact); `WDC_IDENTIFY_PASS` exactly once; 16 named rows present once each; `high byte` once; the G
text; the `@@SELFCHECK@@` token; the self-mutant lane (its failing row, `row_wide_geometry`, is INLINE and runs AFTER
`row_ring_occupancy_sound()`).

## FINDINGS

* **G1 -- MULTI-EDIT SHAPES KEEP GATE 2 GREEN.**  Opus (MEASURED, dropold / drqring / w57hi): (a) the verdict's
  `cmp_fails == 0 &&` deleted + `failures -= cmp_fails;` after the reconciliation; (b) the same verdict edit + the
  reconciliation rewritten `>=`/`-=`; (c) the verdict `failures == cmp_fails && sc_g` + the trailer printing `failures -
  cmp_fails`; and a THREE-edit shape inside the block (the probe's cmp_fails check weakened `!=` -> `>`, `chk()`'s
  increment deleted, `failures` reset).  glm (REASONED): the "trailer triple" -- verdict and exit reverted to #551c's
  form, the reconciliation deleted, `failures = 0;` after the covered rows.
  **MY DISPOSITION: NOT a floor breach -- DISCLOSE by class.**  Every one is a composite whose parts are each red or
  harmless ALONE (Opus measured every single edit: 24 of 24 red outside the disclosed classes).  The carrier licenses a
  multi-part floor mutant only as a verbatim reinstatement or a composite whose every added part is GREEN alone; here
  the reset part is red alone.  The disclosure's "A reset of BOTH tallies is, and is disclosed" does not describe them,
  so it becomes: "Two coordinated edits, one on each tally's path to the verdict (the verdict's cmp_fails term dropped
  and `failures' reset, say), or three inside this block (a probe's cmp_fails check weakened with the increment it
  guards and a reset), keep gate 2 green: measured on #551's passes; disclosed, not chased."
* **G2 -- THE POSITIONAL SHAPE (d)** (Opus, MEASURED; no seat raised it before): move `row_ring_occupancy_sound();` after
  the PASS/FAIL printf and re-pin the identity row 128 -> 104 -- the covered rows print their FAILs after the token.
  Green on dropold and drqring.  Opus measured an optional closure: the LAST self-check requires `chk()` 24 and
  `row_cmp()` 8 calls -- the move-and-re-pin then prints WDC_IDENTIFY_FAIL, healthy logs identical on 5 variants.
  **MY DISPOSITION: DISCLOSE now; FILE the call-count pin** (with `wdcidcomparators`).  It is a two-edit composite
  (each part red alone), the pin is two more constants to maintain beside the identity row's 128, and adopting it is a
  detector change that owes one more pass.  *This is the call I am least sure of -- it is cheap and measured.*
* **G3 -- deepseek, DO NOT SHIP: delete a covered row AND (a) delete the identity row, or (b) reset `failures` after
  it.**  **MY DISPOSITION: (b) REJECTED -- the self-mutant lane catches it** (a reset after the identity row erases the
  lane's inline failure; the lane needs WDC_IDENTIFY_FAIL; Opus measured this family red in #551c, `C_reset1_after`).
  **(a) is REAL but pre-dates #551 and is not a floor breach of it**: gate 2 pins rows only as `>= 42`, so the file's
  own identity row is the only exact pin, and deleting it plus an UNNAMED covered row is green.  A composite (deleting
  the identity row alone is harmless; deleting a row alone is red), and row deletion is inside "'Covered' means the
  COMPARATOR is live, not that a row is".  **FILE** a gate-side exact pin (`wdcrowpin`, LOW) carrying deepseek's text.
* **G4 -- glm, kimi-k3: "24 of 128 ... 16 of chk()'s 24 calls" does not add up (32 rows go through the comparators).**
  **MY DISPOSITION: REJECTED -- a packet omission, not a false sentence.**  The bullet's own first lines, cut off by
  the diff's context, say "8 more hand chk() a 0/1 verdict computed at the call (derive: `grep -cE '\? [01] : [01],
  1\);' regress/diff_wdc_identify.c`)" -- 8 on today's file.  Those 8 compare AT THE CALL; chk() then compares two
  constants.  16 + 8 covered, 8 verdict-handed, 96 inline = 128.  agy verified the grep independently.
* **G5 -- kimi-k3: the measured `reset2` is gate-CAUGHT (the lane sees it); only a reset conditioned on `cmp_fails` is
  gate-green.**  **MY DISPOSITION: REJECTED on placement, REFINEMENT ACCEPTED.**  `reset2` sits right after
  `row_ring_occupancy_sound();`, BEFORE the lane's row, so the lane's failure lands after the reset and survives: gate
  green (Opus's lane measurement agrees).  kimi-k3 is right for a reset placed AFTER the lane's row -- the lane catches
  that -- so the disclosure should say where the both-tally reset is green.
* **G6 -- minimax, Opus: "(reasoned: the block edits measured so far are caught)" is overtaken** -- Opus MEASURED a
  green three-edit block shape (G1), and `scnoforce` alone is harmless on a healthy run.  **ACCEPTED:** the parenthetical
  is replaced by G1's sentence.
* **G7 -- the sum form (`got57 + got60 != 2*sectors` agrees on every probe, misses compensating pairs).**  agy and
  minimax: add a ninth probe `(2, 3, 1)`.  glm: name the CLASS in the disclosure, no probe.  kimi-k3: do NOT name it.
  Opus: measured -- it answers all 13 probes right and still reds w57hi.  **MY DISPOSITION: name the class, no probe**
  (see D1).
* **G8 -- the reconciliation line** (Opus, minimax, agy, kimi-k3: keep it).  **ACCEPTED:** keep it; its comment says it
  keeps the PRINTED count honest after a reset placed before it, and that the verdict and exit read cmp_fails.  (Gate 2's
  "row failures" row reads that printed count; its PASS-token row is what reds `recon2` / `subafter`.)
* **G9 -- glm: "one pair that must NOT fail"** -- each comparator has one probe that must not fail.  **ACCEPTED:** "one
  probe per comparator that must NOT fail".
* **G10 -- glm: `reset2` has no pristine row in the measurement.**  **ACCEPTED** for the re-measurement.
* **G11 -- Opus: my F9 named the wrong location** -- the first `cmp_fails ++` (the file's :520) is in `row_cmp()`; the
  one minimax asked about (:4870) is in `chk()`.  **ACCEPTED** (round record).
* **G12 -- Opus: srstbit's eleven failing rows are ALL inline** (measured on pass 2), so "some ... do not go through
  chk()" should be "none go through chk()".  **ACCEPTED** (round record).
* **G13 -- agy: `where[0] == 'f'` is a fragile prefix test.**  **REJECTED:** both call sites pass literals, settled; a
  change is churn with no reachable difference.
* **G14 -- glm: my brief's paraphrase "no edit of `failures` alone, anywhere, turns the run green" is overbroad** (an
  inline row's failure CAN be hidden that way).  **ACCEPTED as a brief-wording fix**; the source sentence is scoped to
  covered rows ("among them") and stands.
* **G15 -- glm: a covered-row lane (the filed F15) must use the FIRST covered row**, or a reset before it silences every
  earlier covered row.  **ACCEPTED** into the filing.
* **G16 -- minimax, agy: "0 failures" printed beside WDC_IDENTIFY_FAIL under `recon2` / `subafter` is confusing.**
  **NO CHANGE:** the healthy trailer line must stay byte-identical, and the verdict is what gate 2 decides on.

## DISAGREEMENTS

* **D1 -- G7's sum form: probe or disclose?**  agy and minimax: one probe `(2, 3, 1)` closes a KNOWN blind spot and is
  not the unbounded "probe per clever predicate".  glm, kimi-k3, Opus: disclose; kimi-k3 would not even name it
  ("naming one member of an inexhaustible class implies the unnamed are safe").  **My ruling: name the CLASS ("a
  comparator rewritten to agree with the original on every probe while differing elsewhere -- the sum of the two gots
  against twice the want, say"), no probe.**
* **D2 -- G2's call-count pin: adopt or file?**  Opus: "your call".  **My ruling: file** (see G2).
* **D3 -- G3(a): deepseek's DO NOT SHIP.**  deepseek: a floor breach.  **My ruling: a real, pre-existing composite,
  filed as `wdcrowpin`, not a breach of #551.**

## WHAT IS STILL OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* The chain's closing condition: a VALID pass with zero floor breaches and its denominator.  Opus: 24 single edits
  measured, every one outside the disclosed classes red; agy, kimi-k3, minimax: zero, each with a denominator; glm and
  deepseek: composites only.  **I am treating that as the closing zero.**  If a composite should count as a floor
  breach, the chain does NOT close and #551e owes a pass.
* The wording changes (G1, G2, G5, G6, G7, G8, G9) are comments only -- code-identical by comment-stripped
  preprocessing, which I will measure -- so I am NOT planning another panel pass on them.  Say if that is wrong.
* Astra (codex GPT-6 Astra) has not seen #551b, c or d; by owner ruling nothing commits before it confirms after 07:01.
* Accepted: G1, G2, G5 (refined), G6, G7, G8, G9, G10, G11, G12, G14, G15 -- twelve.  Rejected: G3(b), G4, G13, G16 --
  four.  Filed: G2's pin and G3(a).  The ones I most want tested: G1 (composites are not floor breaches), G2 (filing a
  measured, cheap closure), G3(a) (filing rather than fixing).

## GROK (appended as each grok job lands)

* **G17 -- the DEDICATED grok job (`grok_dedicated_551d.txt`, SHIP WITH CHANGES, reasoned from the inlined trailer and
  the tree's call sites, not recompiled): the trailer can score the DIFFERENCE.**  Replace the three raw reads --
  `printf(... failures)`, `if (failures == 0 && cmp_fails == 0 && sc_g)`, `return (failures || cmp_fails || !sc_g)` --
  with `failures - cmp_fails`.  Nothing is assigned; the self-check is untouched; a covered-only failure makes the
  difference 0 while the lane's inline geometry failure keeps it 1.  Its one-site cousin (PASS whenever `failures ==
  cmp_fails`, the count still raw) leaves "2 failures" printed, so gate 2's row-failures check still sees it; the
  three-site form is the one that also zeroes the count.  This is the same family as Opus's shape (c) (two sites, the
  return left raw -- gate 2 discards the exit status).  Its proposed in-file close: **make the pass/fail decision a
  function the self-check probes** -- (failures, cmp_fails, sc_g) = (1, 1, 1) must fail, (1, 0, 1) must fail, (0, 0, 1)
  must pass -- which turns a rewrite of the decision into a probe failure and leaves only an edit of its ARGUMENTS
  (the disclosed feed class).  Also: F1 REFINE ("the closure is not finished"), F12 UPHOLD with the measured reason
  (srstbit stays at ORIG's 11 under a chk()-only edit, so none of the eleven goes through chk()), F14 name the sum
  pair, no ninth probe; D1-D3 upheld.
  **MY DISPOSITION: the same as G1 -- a multi-site composite, each site red or harmless alone, so disclosure by class,
  not a floor breach.**  The probed decision function is the class closure for G1, G2 and G17 together; it is a
  detector change that would owe one more pass, and I would FILE it (with G2's call-count pin) rather than open
  #551e.  **This is the decision I most want the adjudication to test: two passes in a row have now found the trailer
  class in new composite forms, and the carrier's rule is that the next repair owes the CLASS closure when two
  consecutive passes find BREACHES of one class -- I am reading composites as not breaches.**

* **G18 -- the PANEL grok seat (`panel_20260925_174800/grok.txt`, SHIP WITH CHANGES, 11 shapes, walked not compiled):
  ONE edit -- the verdict `failures == 0 && cmp_fails == 0 && sc_g` becomes `failures == cmp_fails && sc_g` -- prints
  WDC_IDENTIFY_PASS on drqring (2, 2) and w57hi (4, 4) while pristine and the self-mutant lane stay as shipped.**
  **MY DISPOSITION: REJECTED -- gate 2's count check catches it.**  Its own table says "print still 2": the trailer
  prints `failures`, and gate 2 requires `grep -oE '[0-9]+ failures'` to read 0 (the check at `wdc IDENTIFY: row
  failures`).  Opus MEASURED THIS EXACT EDIT: `D_v_eq` in `opus551_measured_d/analyze6.out` is red on dropold (3
  failures printed), drqring (2) and w57hi (4) -- PASS is printed, and the count check reds -- while
  `D_v_eq_printf_sub`, the same verdict with the printed count changed to `failures - cmp_fails` (its shape (c)), is
  green on all three.  The dedicated grok job reached the same
  split ("the defect log still says 2 failures, so the count check still sees the row; the three-site form is the one
  that also makes it read 0").  The seat's premise that "gate 2 never runs drqring" applies to every variant here; the
  question all passes asked is what gate 2 WOULD say of that log.
  Also from this seat, ACCEPTED: F12 is understated -- the rows-keyed edit (`postinc`, the same edit as `rows`) is green
  on drqring, a covered defect, not only on pristine; the above-want probes all have want 0, so a comparator that sees
  "above" only at sectors 0 (`<` plus `sectors == 0 && (got57 | got60)`) agrees with every probe and misses `(2, 3, 2)`
  -- the same class as the sum form (G7); and the exit status is not a gate-2 input (gate 2 discards it and the lane
  reads stdout), so the return line's `cmp_fails` term protects callers other than gate 2.  F6: a wipe of `cmp_fails` at
  the top of the LAST self-check keeps the lane -- the block-edit class, disclosed.
