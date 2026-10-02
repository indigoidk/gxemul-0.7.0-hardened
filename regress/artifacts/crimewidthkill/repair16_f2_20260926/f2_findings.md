## 1. WHAT CHANGED SINCE THE PASS-2 PACKET

* **Table 15a** (E9) measured the dedicated grok seat's candidate: `H_noresetclear` (the HARD_RESET branch's clear
  skipped) passes all **218** rows of repair 15's probe; so does `E_noendianclear` (the unconditional ENDIANESS clear
  skipped).
* **The Opus measuring seat** (section 5; verified claude-opus-5-5 throughout) measured the CONTROL arm's residue-text
  channel further and proposed a CONTROL-text count on the two existing ACCEPTS sessions, which already hold all ten
  accepted CONTROL writes in both latch states.
* **Repair 16** (E7) closes that channel as a CLASS in one diff: every clear the arm makes before its residue test --
  DOG, HARD_RESET, ENDIANESS -- now has a residue-count row in BOTH latch states:
  `ctlrst sw/sd msg` + `ctlrst sw/sd halt` (new sessions, latch CLEAR), `rst 4w/8w msg` (the reset sessions, a 0x0001
  twin first, latch SET at the 0x800), `rearm ctl msg` (latch SET) and `latch ctl msg` (latch CLEAR) on the ACCEPTS
  sessions.  226 rows.  Contract text: the class closure, and a list of the cells deliberately NOT rowed.
* **Table 16** (E10): 25 legs, predictions pre-registered in `PRETABLE16.out` before any build.

## 2. FINDINGS -- attribution, MY DISPOSITION, what I changed

**F1. The HARD_RESET clear skipped is undetected by all 218 rows** -- the dedicated adversarial grok seat; confirmed by the
Fable seat; MEASURED in table 15a.  **DISPOSITION: ACCEPTED, L2** (the ruling's 13/17 conditional on the arm's other
TESTED bit; the Fable seat graded it the same).  **CHANGED:** `ctlrst sw/sd msg` + halt (latch CLEAR) and `rst 4w/8w
msg` (latch SET).  Second consecutive pass finding a residue-of-a-clear cell in this arm -> the repair is the class
closure.

**F2. The ENDIANESS clear skipped is undetected too** -- the main loop; MEASURED in table 15a.  The Fable seat graded it
clause (e) (never tested) with "a text count there is a cheap optional strengthening, not owed".  **DISPOSITION:
ROWED AS THAT STRENGTHENING**, because the Opus seat's ACCEPTS-session counts carry it at no session cost (the two
0x0100 ACCEPTS entries).  **CHANGED:** `rearm ctl msg`, `latch ctl msg`.  See D4.

**F3 / F17. Width x direction x latch at INTSTAT and INTMASK: 8 of 16 cells unexercised** -- glm, kimi-k3:cloud,
deepseek, grok (panel) found the latch-SET 1-byte READ pair; the Opus seat's per-access census found all eight (1R with
the latch SET; 1W, 2R, 2W with it CLEAR) and measured six variants that pass all 218 rows there (`P_ist1r_set`,
`P_imk1r_set`, `C_istW_clr`, `C_ist2_clr`, `C_imkW_clr`, `C_imk2_clr`), with a positive control on a rowed cell
(`C_ist1r_clr`, detected 214/218).  The probe header claimed the whole {1,2} x {R,W} floor at every observable label.
**DISPOSITION (PROPOSED): NOT ROWED, disclosed** -- the decline does not test width within the narrow class nor
direction, so these are joints beyond the ruled floor {label} x {latch SET}; the header's claim is SCOPED ("each cell in
at least one latch state") and the contract names the eight cells.  **Cost if ruled owed: six sessions** (the Opus
seat's estimate).  **A RULE QUESTION -- D2.**

**F4. A clear gated on the width latch is undetected** (glm: the DOG clear; the same shape exists for HARD_RESET).  glm
also showed the contract's reason ("the CONTROL arm reads no latch") described the fixed build, not the space of edits.
**DISPOSITION: ROWED** -- `rearm ctl msg` (DOG, latch SET) and `rst 4w/8w msg` (HARD_RESET, latch SET) now carry both;
the wrong reason is removed from the contract.  **CHANGED:** as above; table 16 measures `L_dogclr` and `L_rstclr`.

**F5. The DOG stop-bit and re-arm shapes are unseen** -- glm, kimi-k3, deepseek.  **DISPOSITION: REJECTED ON THE
EVIDENCE** -- the ACCEPTS sessions (E3) write 0x0200 and continue; a re-arm reds `rearm once`, a stop reds
`rearm surv`/`latch surv`.  agy and grok verified it from the files.  A BRIEF DEFECT: those sessions were not inlined.

**F6. The `tl` rows' s1 should be large on the fixed build** -- deepseek.  **DISPOSITION: REJECTED** -- the 8-byte read
samples `d->reg[...]` before the switch's `crime_update_crime_time(d)`; the base leg measured raw 66/66/132/66 (E5); the
Opus seat measured it from the device side (s1 = 726/792/726/594 in its census run, exactly the tick's value).  See D1.

**F7. The next tick is 16383 steps after the first, not 16384** -- grok (panel).  **ACCEPTED, L4 in the pass-2 brief.**

**F8. Five completion times for four lanes** -- glm.  **REJECTED (explained):** 18 legs in 4 lanes = rounds of 5,5,4,4.

**F9. `said()` not inlined** -- glm, kimi-k3.  **ACCEPTED** -- E4.

**F10. The `tl <op> ctl` note wording** -- glm.  **REJECTED (kept):** verbatim the existing `time <op> ctl` notes.

**F11. agy's summary claimed 20 cells covered** while its matrix showed 3 ops at three labels.  **NOTED** -- that is F3.

**F12. Read the residue VALUE in the twin's text** -- glm; **and the Opus seat measured a variant only a value can see**
(F20).  **DISPOSITION: see F20.**

**F13. `-V -x` start semantics** -- kimi-k3.  **SETTLED** by grok (panel) from the source.

**F14. A latch-CLEAR-only exemption at INTSTAT/INTMASK/CONTROL** -- kimi-k3.  **PARTLY REJECTED, PARTLY F17**: the
single-axis latch-CLEAR cells are rowed (`istat lb`/`imask lb`, `sb08 msg`'s first `sb`, `sh08 run`'s first `sh`), but a
latch-CLEAR exemption keyed on width or direction at INTSTAT/INTMASK is one of F17's eight cells.

**F15. The pass-2 brief's "per label ... all four narrow ops each"** -- glm.  **ACCEPTED, L4 in the pass-2 brief.**

**F16. The fallback draft overstated** -- the Fable seat, on the text written in its name after two refusals.
**ACCEPTED** -- relabelled [NOT A SEAT ANSWER].

**F18. A latch-SET 2-byte CONTROL write with HARD_RESET clear** (`P_ctl2wrc_set`) passes all 218 rows -- the Opus seat;
host text only, and every latch-SET 2-byte write in the probe carries 0x0800.  **DISPOSITION (PROPOSED): disclosed**
(a width x bit joint).  Cheap alternative: one more latch-SET `sh 0x0201` store in the `sh08b` session.  **D5.**

**F19. A refusal at INTSTAT/INTMASK while the interrupt line is ALREADY asserted** (`P_istprev_set`) passes all 218 rows
-- the Opus seat: every row watches the line RISE, none watches it fall; even the plain INTSTAT swap is detected only
through the rise.  **DISPOSITION (PROPOSED): disclosed** (a state x label x latch joint).  **D5.**

**F20. The residue VALUE when the count does not move** (`D_dogbit0`: the DOG clear skipped when bit 0 is set) -- the
Opus seat, measured.  **DISPOSITION (PROPOSED): disclosed**; the alternative, a value-anchored text in the ctldog/ctlrst
rows, costs no session.  **D5.**

**F21. Count rows on the existing ACCEPTS sessions** -- the Opus seat's option.  **ADOPTED** (repair 16), and the same
idea applied to the reset sessions.

**F22. "Exactly ONE CRIME tick per session" is false: stepped sessions see THREE** (two after `quit`, from
`cpu_run_deinit`) -- the Opus seat.  Harmless for every row.  **ACCEPTED, L4** in the pass-2 brief's settled premises.

**F23. PRETABLE14's "DOG -> stop" example (the HARD_RESET test widened to DOG|HARD_RESET) is equivalent** -- DOG is
cleared before that test.  -- the Opus seat.  **ACCEPTED, L4**, recorded in POSTTABLE16 (PRETABLE14 is not edited).

**F24. Two sessions refuse at TIME with the latch set, not one** (the `dog` session too) -- the Opus seat.  Conclusion
unchanged.  **ACCEPTED, L4** in the pass-2 brief.

**F25. The gate pin is three lines** (`gate_arm.sh` 1916, 1921, 1922 all read 204) -- the Opus seat.  **ACCEPTED**: the
pin step moves all three.

## 3. DISAGREEMENTS AND RULE QUESTIONS -- please adjudicate, including your own

**D1 (F6).**  deepseek: s1 should be large.  Everyone else and two measurements: small.  **RULING: small.**  deepseek,
please re-walk it against E5.

**D2 (F3/F17) -- the eight INTSTAT/INTMASK width x direction x latch cells: floor, or disclosed?**  glm: below the
adjudicated floor, but the text claimed them.  kimi-k3: outside the printed enumeration, name them.  grok (panel):
outside this floor.  The Opus seat: "by the ruling's letter clause (e); by the probe's own text owed, or the text is a
wrong record ... the project's own precedent (the F2 2-byte cells) rowed a label x width narrowing rather than
disclosing it."  **MY PROPOSAL: disclosed, with the header's claim scoped** -- which corrects the wrong record without
adding rows.  The Opus seat's precedent point is the strongest argument against me: weigh it.

**D3 (was F4) -- resolved by rows** unless you judge the rows unlicensed (they catch measured variants; E10 shows it).

**D4 (F2) -- ENDIANESS rowed as a strengthening the Fable seat called "not owed".**  Is that licensed (a measured delta:
table 15a, and E10), or scope growth the adjudicator should reject?

**D5 (F18, F19, F20) -- the state- and value-conditioned cells: disclosed, or owed?**  Two have zero-session
alternatives (F18: one store in an existing session; F20: a value-anchored text).

## 3a. WHAT IS STILL OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* **Owed:** codex (GPT-6 Astra) -- the pass-2 seat and a dedicated job -- after its 07:01 reset; then the Fable seat LAST
  and Astra's confirmation; nothing commits before #549 does.
* **Fooling myself, 1:** every rule question I proposed (D2, D5) resolves toward fewer rows, while every cell I DID row
  was cheap.  The measurements are here so that can be checked rather than trusted.
* **Fooling myself, 2:** I grew the repair beyond the one L2 cell (F2, F4, F21).  The warrant is the class-closure
  amendment and measured deltas; an adjudicator may call part of it unlicensed.
* **Fooling myself, 3:** this round's kimi seat is the PACKET-FED substitute (the CLI is 403 on its subscription).
