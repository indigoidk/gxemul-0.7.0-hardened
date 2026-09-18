FABLE_SEAT_ALIVE_20260918_534
Model: Fable 5.1, exact id `claude-fable-5-1`.
CHECKPOINT.md first line, verbatim: `# CHECKPOINT -- 2026-09-18 12:29   HEAD: e16a8b7 #533 landiskaux: landisk's wdc aux register sat at the PC-layout +0x206, so the kernel's soft reset landed on unmapped memory`

**VERDICT: RATIFY-WITH-FINDINGS -- commit #534 after one L1 fixture row and two L4 record edits (below); nothing found reaches L2 on the shipped composite.**

Conflict disclosed up front: I am the same model family as the author (badge `s`) AND as the seat that wrote the 2026-08-30 `n6` entry I am asked to classify. The owner may overrule Q1 on that ground alone; it is a records judgement, no code moves on it.

Read-only: nothing under GXEMUL-SEC was touched. Measurements: `drive_fable.py` / `drive_fable.out` in my scratch dir (wraps the shipped `run_controls.run()` unmodified, 5 added mutants, plus a real-ledger run in a temp copy).

## Q1 -- the `n6` assess entry of 2026-08-30: **(c) an adjudication record, NOT A SEAT ANSWER.**

Read from the entry itself (`ledger.json`, row `n6`, entry 4, byte-identical to HEAD):
* `outcome_note` opens `[HOLD-QUESTION-DISCHARGED]`; `grader: mainloop (Fable family) -- SELF-GRADED`; `ev: (reading-seat adjudication...)`. It was fired against the row's `hold_question` of that day (repoint / oracle-correction), not against the assess question. Its four moves -- blast radius, repoint target, accept-row oracle, title -- are DESIGN material. The assess question ("is the defect real?") was answered on 08-15 by opus5 and fable5 and has not been re-asked.
* The carrier assigns hold-question adjudication to the MAIN-LOOP hat ("seat and adjudicator are distinct hats; the adjudication happens in the main loop, not in the seat"). The entry records that hat: it was self-graded by the loop.
* It is filed under `assess` for want of a phase -- the row's other design work (two farmed codex runs 08-30, the 09-11 codex design pass) lives in `note`, not in `entries`. This entry is the odd one out in placement only.

Why not (a): rendering it as fable5's LATEST assess answer would show `d: OK` over the real 08-15 verdict -- a mis-render of the stage -- and would owe seven seats on a question nobody disputes, which is "reaching for the nearest token" in reverse: spending a panel to satisfy a rule rather than to learn something. Why not (b): agy is right on the definition. `check_stage_panels.py` minted RE_READ for "one filing plus one re-read" (the 08-21 `pitlatch2` case, still the census's only RE_READ). `n6` assess is a two-seat pre-policy stage; a RE_READ tag would also make the 08-30 entry `newest_tok` and disarm clause (i) by construction -- grok's point, and it is correct.

**Two conditions that keep (c) from being a disarm:**
1. The NOTSEAT record must name the hat and say where the content goes: `n6`'s research brief must INLINE the 08-30 material as a settled premise, so nine seats scrutinise it there. If that brief omits it, the single-seat design was hidden behind the tag -- the self-dealing shape realised.
2. **Recording this ruling hits a deadlock the author must handle by a records edit, not by an answer.** The 09-18 `[HELD AWAITING SEAT: fable5]` on `n6` assess cannot be discharged by a NOTSEAT record (by design, `M_any_entry_discharges` is killed), nor by a same-day answer (strictly-later), and an ANSWER dated 09-19+ re-fires clause (i) (`TOKEN-REFUSED ... fable5 dated ... LATER than the exemption` -- measured: with the marker removed, base H reds exactly so). The HELD token means "the stage awaits this seat's ANSWER"; this stage awaited a RULING. So: rewrite the 09-18 marker defanged (quote the question and this verdict), add the NOTSEAT record. Suggest one template line: a stage held for a RULING is released by rewriting its marker; HELD is for seat answers.

## Q2 -- is the composite floor-sound?

Base reproduces 48/48; the 32 shipped mutants I did not re-run (v3 log read). Five edits of mine, all through the shipped driver:

| edit | 48 + H2 | real-ledger effect |
|---|---|---|
| **F_selfseat_skip** -- clause (i) skips a later answer by the SEAT that wrote the exemption | **48/48** | **flips `n6` assess from TOKEN-REFUSED to grandfathered** once its 09-18 hold is discharged (measured both ways) |
| F_cutoff_gt -- `d >= POLICY_CUTOFF` -> `>` | 48/48 | none (no answer dated exactly 2026-08-16 after a token) |
| F_zero_open_skip -- open row, zero-answer live hold silently skipped | 48/48 | none in assess/research/review |
| F_no_lower in `held_seats` | 48/48 | none (zero non-canonical markers) |
| F_ii_note_too -- clause (ii) also reads the ANSWER's note | 48/48 | none today; `unreadseats23`'s answers cite dirs note-only, all named by its token |

**The first is the one that matters: the ONE real disputed case -- exemption and later answer by the same seat -- is the one shape no fixture holds.** Every `t_*late` row uses kimi as the later seat. Row owed, L1 (nothing shipped): `t_selflate` = THREE + fable5 ANNOTATION D1 + fable5 untokened answer D3, want TOKEN-REFUSED; the same row kills F_selfseat_skip. The other four are disclosures for the contract (the 08-16 boundary; zero-answer open holds; case; answer-side note citations). Also still unrepaired from codex's F2 Q4: the dashboard drops a MALFORMED hold when its filer also has an answer (the record loop excludes `is_held`) -- zero real instances; disclose.

## Q3 -- which accepted dispositions are wrong

1. **F8's record.** The CHANGELOG's pass-2 bullet still ends "...and was tagged as the re-read it is", while the F2 section reverts the tag. Chronology is fine; the phrase "the re-read it is" is a claim this ruling overturns. L4: "tagged RE_READ; reverted and ruled below".
2. **F14 (check_fix_seats.py deferred) is defensible on one fact I checked: it is wired into NOTHING** (`grep check_fix_seats tools/precommit_check.sh tools/*.sh` -> no hit; `?? untracked`). A gate that does not run needs no control yet. But `stage_tokens.py`'s docstring names it among the "four tools" whose classification "now lives here" -- three ship. Say so in the docstring (L4).
3. **The four newly-exposed holds are honest as RECORDS and favour finishing as DISPOSITIONS.** `pcc2c040kill` is SHIPPED (`9fa07fe`) with review 8/9, missing agy; `lcabadval` is in work on a commit. A HELD marker on a shipped round turns "moved on without the full panel" into "waiting" -- H's own documented blind spot (waiting is indistinguishable from forgotten; section I covers only fable5, not agy). The cheap honest move is to FIRE agy on `pcc2c040kill` review (one seat, and agy fires by directive) in this round's wake, and carry the three genuinely multi-seat holds as holds. Holding all four is not wrong; firing the one-seat gap now is better.
4. F6 as L3, F7, F9-F13, F15, F16, D1, D2: upheld on the diffs and the v3 log. The strictly-later consequence for `pcc2c040assertrow` (re-fire must be dated after 09-18) is mechanical, correctly disclosed.

## Q4 -- owner questions

* **Whether a NOTSEAT tag on a `seat: fable5` entry carrying `d: OK` is acceptable when ruled by the same model family.** The rule is right; the conflict is structural and only the owner can waive it.
* **Fire-or-hold on the four exposed stages of shipped/in-work rows** (item 3 above) -- the full-panel directive says "STOP AND ASK THE OWNER" on a seat that cannot be run; these were not stopped for, so the owner should see them by name.
* Not an owner question: everything in Q2 (L1, in-round).
