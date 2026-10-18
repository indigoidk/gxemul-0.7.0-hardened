**Your token: `ASTRA_FHF_P1_20261018`** -- open your answer with it.

# `fableheldform` -- how should sixteen walled Fable entries be recorded, when nine of them sit on rows already CLOSED?  A design question about records (pass 1)

**Please do not simply ratify.**  A recent panel had seven of nine seats confirm a premise its brief stated wrongly.
Check the premises, not just the derivations.  The tree under review is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` (ignore
any other `src/` under the project root).  READ-ONLY.

## The defect (filed by `#566`, 2026-10-18, as row `fableheldform`, MED)

The owner's 2026-10-17 directive: *"do not block a ruling or a commit on Fable: Astra + Grok + GLM 5.3 rule; Fable's stage
is recorded as a HELD marker carrying its question (`[HELD AWAITING SEAT: fable5]` plus a `hold_question`) and is answered
when the seat comes back.  Still try Fable once per pass (a wall is a moment, not a state) and record a wall as a SEAT
FAILURE, never as agreement."*

Since then sixteen `fable5` ledger entries on ten rows recorded a wall or a deliberate non-firing in PROSE ("NOT FIRED",
"SEAT FAILURE", "HTTP 429") with NO stage token.  `tools/pipeline/stage_tokens.py` `is_answer()` returns True for ANY
entry without a token, so the checkers count each of these as Fable having ANSWERED -- the agreement the directive says a
wall must never be.  The census, derived from the ledger at 16:1x today, is `CENSUS.txt` (inlined below for the
packet-fed seat): 16 entries; NINE of the ten rows are CLOSED (`sgirekills`, `sgirandomcolour`, `mapledmaaddr`,
`xscaleinten`, `ppcrldimimask`, `ppcrlwimiwidth`, `ppcgateimageskip`, `cxlaunchquotation`, `dashokclass`), one is in work
(`wiringcliff`).  All nine closed rows already carry a `hold_question` -- for their REGRESS stage (regress is FABLE-ONLY,
batched), not for the walled review.

## The rule the fix collides with

`tools/pipeline/check_stage_panels.py` (precommit section H; `H_excerpt.txt`): `STAGES = ("assess", "research",
"review")`; for each, a LIVE hold (a `[HELD AWAITING SEAT: X]` marker with no later answer from X in the same phase) on a
row whose state is `closed` is a violation, CLOSED-WHILE-HELD: *"a round may not close while a stage awaits a seat"*.
The `regress` phase is not in `STAGES`, so a REGRESS hold does not block a close.

**Measured today, one hour ago, on `ip30abortkill`'s closure:** my draft recorded Fable's walled closure review as a
`[NOT A SEAT ANSWER]` entry and closed the row; GPT-6 Astra's confirm overturned it -- *"substitutes a non-answer record for
the review hold ... the draft reports review `ok 9/9`, using historical answers, with no review hold.  Retain `state: in
work`, omit the closure object"*.  That row was committed `held` (state semantics: *"Something outstanding, waiting on a
NAMED party or event, and carrying the QUESTION it is held for"*).  If that ruling is right, the nine closures above got
past section H only because of this very defect.

## Options for the nine closed rows (the set is not claimed complete -- name a member it lacks)

* **A. REOPEN.**  Give each of the sixteen entries the HELD token (keeping its prose and receipt), extend each row's
  `hold_question` with the walled stage's question, and move the nine rows `closed` -> `held`.  Their closure objects:
  kept as the drafted closure, or moved into the state note?  The dashboard then shows nine rows held for Fable.
* **B. KEEP CLOSED, NON-ANSWER TOKEN.**  Mark each entry `[NOT A SEAT ANSWER]` -- not an answer, not a hold.  The form
  Astra overturned this afternoon: the review stage then reads complete on older answers and the gap is invisible.
* **C. KEEP CLOSED, CARRIED ON REGRESS.**  B, plus the walled review's question carried on the row's REGRESS hold.  The form
  I chose for `ip30abortkill` before Astra's confirm.
* **D. LEAVE AS IS.**  The defect.

## Questions (answer each; premises are stated as questions on purpose)

1. **Which option, and why?**  Is A what the owner's directive and section H jointly require, or is there a reading of
   "do not block a ruling or a commit on Fable" under which a CLOSE (a state change) is not something Fable may hold?
2. **`cxlaunchquotation` and `dashokclass`**: Fable ANSWERED their earlier passes (V3-V6 / V2-V6, same review stage) and
   walled only on the last (V7).  Is that review stage held, or discharged by the earlier answers?  (The repair-chain rule
   says the chain closes on the first VALID pass that finds zero breaches, and a valid pass has its roster complete or its
   misses NAMED.)  Same question for `sgirekills`, whose research AND review walls are `#564`'s passes 1-3.
3. **The conversion's form**: prefix the token to the existing entry (one entry, provenance kept), or add a new marker
   beside a re-tagged old one?  Note `stage_tokens.is_held()` keys on the literal and `live_holds()` discharges a marker
   only by a LATER answer from that seat in the same phase.
4. **Is this an OWNER decision** (reopening nine closed rows) rather than a seats' one?  If so, what is the single
   question to put to the owner?
5. **Which of my premises is wrong?**  In particular: is the census complete (16 / 10)?  Does any of the nine rows have a
   later Fable answer that already discharges its stage?

Answer format: open with your token, then ONE line `VERDICT: <option> -- <one line>`, then `FLAG:` lines for any premise
you find false (with `file:line` or census evidence), then short answers to 1-5.

Files beside this brief: `CENSUS.txt`, `H_excerpt.txt`, `stage_tokens_excerpt.txt`.  The ledger is `tools/pipeline/ledger.json`; the working tree carries other units' uncommitted lines in it, so cite entries by row id and entry index from `CENSUS.txt`.
