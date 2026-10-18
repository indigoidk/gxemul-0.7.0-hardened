**Your token: `ASTRA_CLOSE531_20261018`** -- open your answer with it.

# Closing ledger row `ip30abortkill` (#531) -- is anything still owed?  A records check

**Please do not simply ratify** -- a recent panel had seven of nine seats confirm a premise its brief stated wrongly.
Check the premises, not just the derivations.  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the commit under
review is HEAD `8faf4a16`.  READ-ONLY: write nothing to any project tree.  The working tree carries ANOTHER session's
uncommitted edits, and `tools/pipeline/ledger.json`, `matrix.html` and `check_probe_wiring.py` carry other units' lines:
judge the ledger by `git show HEAD:tools/pipeline/ledger.json`.  `src/devices/dev_sgi_ip30.c`, the probe,
`regress/gate_arm.sh`, `OUTSTANDING_BUGS.md` and `CHANGELOG.md` are clean at HEAD.  Ignore any other `src/` you find
outside `GXEMUL-SEC/` (the project root holds pristine 2021 upstream copies).

## What this is

`#531` (`686d179c`, committed 2026-09-18) took four guest-reachable `abort()` calls out of `src/devices/dev_sgi_ip30.c`.
Its detector is `regress/artifacts/ip30abortkill/ip30_abort_probe.py` (33 rows), wired into gate 14
(`regress/gate_arm.sh`) by `#566` (`8faf4a16`, this morning).  The ledger row (`ip30abortkill`, HIGH) is still `in
work`.  `#566`'s note at the head of the row's `state_note` lists what was still owed before close:

> Still owed before close (target: before the 2026-10-25 battery): the witness field still leads with the 21-row
> pair; clause (b) -- abort() re-inserted at each fixed site of the FIXED file, re-run at 33 rows -- is held by no kill
> table; and a ruling on whether V7_nocounter and V8_len4 need a carrier that survives the close (Grok 4.7: no).

This commit would CLOSE the row and change only the ledger, `OUTSTANDING_BUGS.md`, `CHANGELOG.md`, the generated queue
(`tools/pipeline/fable_queue.md`) and `matrix.html`.  No `src/` file is touched.

## The clause (b) leg (measured 15:21-15:26 today)

All in `regress/artifacts/ip30abortkill/close_20261018/`: `mutant_b_dev_sgi_ip30.c.txt` (the mutant),
`PREDICT_clause_b.txt` (the row-by-row prediction, written before the build), `legb531.sh` (the driver), `LEGB.out`
(its receipt), `probe_b.log` (the probe's output), `CLAUSE_B.txt` (the derivation and the file times, since git does
not carry mtimes), `build_mutant_b.log`, `build_restore.log`.  Outcome: `IP30ABORT_RESULT=14/33`, CONTROL=OK; gate 14's
own block text (extracted from `regress/gate_arm.sh`) on that log: 41 checks, 22 red.

## The drafted records

* `close_20261018/draft/LEDGER_preview.txt` -- every changed ledger field: `ip30abortkill` closed (closure note,
  commits, a new witness head, a new state-note head, `hold_question`, two HELD Fable entries), a new row
  `ip30abortresidual` (LOW, open), `wiringcliff`'s commits field.  The closure check's own seat entries are added after
  it answers.
* `close_20261018/draft/OB_preview.diff` -- `diff` (normal format) of `OUTSTANDING_BUGS.md`: one blockquote paragraph
  added to the `### ip30abortkill -- FIXED AS #531` entry, and a dated section at the end.
* `close_20261018/draft/CHANGELOG_block.md` -- the block prepended to `CHANGELOG.md` (`{CLOSURE_CHECK}` is filled in
  from this check's answers).

## My dispositions -- the ones to attack

* **D1 -- close now.**  The three owed items are discharged: the witness leads with the 33-row pair, clause (b) is
  measured, and the residual question is ruled (D2).
* **D2 -- a new carrier row, `ip30abortresidual` (LOW).**  `V7_nocounter` and `V8_len4` are disclosed in the probe's
  CONTRACT; Grok 4.7 said at `#566` that they need no carrier.  I chose one on `#527`'s precedent, where GPT-6 Astra
  found that its residuals had been made the closing row's to carry, so closing that row bare would have dropped them
  (they went to `ppc527residual`).  Here nothing assigned them to `ip30abortkill` in so many words; `#566`'s note only
  asked whether they need a carrier that survives the close.
* **D3 -- `#561`'s four HELD `dev_sgi_ip30.c` comment corrections (places 7-10) join that carrier.**  I first thought
  the file's latch comment (`SIX announce paths share TWO bits ... IP30_W_ISR covers FIVE (0x10020 write and read,
  0x10028 write and read, 0x10030 write)`) was a NEW finding; it is not -- `#561` ruled a replacement and HELD it with
  sixteen other `src/` comments (`regress/artifacts/recordfix_20261002/adjudication_20261006/EDITS_561.json`, key
  `held`; `OUTSTANDING_BUGS.md`'s `### #561` section ends "Still owed: the HELD edits.").  No ledger row carries those
  seventeen.  I put the four `dev_sgi_ip30.c` ones on the new row and left the `#561` section as it is.
* **D4 -- Fable: two HELD markers and one `hold_question`** covering the closure review and REGRESS (the owner's
  2026-10-17 directive: Astra + Grok + GLM rule; Fable held, tried once per pass, a wall recorded as a SEAT FAILURE).
* **D5 -- the stale product comment is NOT fixed in this commit.**  A records commit touches no `src/`; a `src/`
  comment owes `est/` byte-identity and build-tree propagation, which `#561` also declined to do in a records commit.

## Questions

1. **Is anything still owed before `ip30abortkill` may close** that the drafted records drop?  Check the row's
   `state_note` (all of it, not only the head), its entries, the `ip30abortkill` entries in `OUTSTANDING_BUGS.md`, the
   probe's CONTRACT and the CHANGELOG's `#531` and `#566` blocks.
2. **Is the leg a valid clause-(b) measurement?**  Clause (b): the detector fails "on a VERBATIM REINSTATEMENT of the
   removed defect at EVERY fixed site".  I believe placing the pair AFTER the if/else of `case 0x10020` and
   `case 0x10028` is the faithful reinstatement because the pre-fix arms had no `writeflag` test, so both a load and a
   store reached it -- check `git show 686d179c^:src/devices/dev_sgi_ip30.c`.  Is anything else about the mutant, the
   order (prediction before measurement) or the scoring wrong?
3. **D2/D3: which carrier is right?**  A new row; or close with the row (they are disclosed); or an existing row
   (`ip30setisrassign` is open on the same file; `hrecordowed` carries the harness's unplaced records); and should
   `#561`'s four places be carried at all, given the `#561` section already lists them as owed?
4. **Is every drafted fact exact** -- each number, path, hash and date in the three drafts?
5. **Which of D1-D5 is wrong?**

Answer format: open with your token, then ONE line `VERDICT: <n> flags -- <one line>`, then one `FLAG:` line per
defect with its `file:line` evidence and the replacement text, then short answers to 1-5.  A flag must be checkable.
