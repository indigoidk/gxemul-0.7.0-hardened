## 7. Pass 14's findings, consolidated -- with the coordinator's disposition on each

G1 (Fable 5.1) the floor is {7 labels} x {SFRZ} x {delay_slot}, 28 cells; v22 rowed 19.  **ACCEPTED** -- v23 rows all 28 (the
   grid in section 4 is printed by `derive_cells.py`, not hand-written).  The two shapes Fable PREDICTED to sweep v22 are
   MEASURED there in table 19b.
G2 (Fable 5.1 + GPT-6 Astra) BOUNDS/ERROR x {slot} are FLOOR, overturning pass 13's F2.  Fable: reachability is derived from
   the WRITERS of each value, never from architectural legality; "a cell rowed under contradiction [`dslot`, whose else-arm
   the manual contradicts] cannot be refused under silence"; and the exempting mutant re-introduces this round's own host
   stop.  **ACCEPTED**: `dslotbounds`, `dsloterror`, pinned as this emulator behaves and saying so.  Grok 4.7 and GLM 5.3
   held them disclosed -- D4.
G3 (GPT-6 Astra) the SFRZ re-route's two sides x {slot} are floor.  **ACCEPTED, MEASURED** (table 17: both 63/63 on v22) --
   they are the (SFRZ set, slot) column of G1's grid, rowed per label.  Grok held them a disclosed joint -- D3.
G4 (all four) {fallback} x {slot} is clause (e) by the tests-not-reads criterion.  **ACCEPTED** -- and rowed anyway
   (`usfu1dslot`) because its escape was measured (table 17, 63/63): a measured delta licenses a detector row whether or not
   it is owed.
G5 (Fable 5.1) `br.n +16` in a handler at 0x40 targets 0x50, the ERROR entry -- a lost delivery reads DELIVER.  **ACCEPTED**:
   every v23 handler uses `br.n +8`; the table-18 candidate that used +16 is not shipped (`NAMING.txt`).
G6 (Fable 5.1) the trap route at the five instruction labels x (SFRZ set, slot) is clause (e) -- a second sub-cell of a cell the
   fault row already holds.  **ACCEPTED**, disclosed by count with the mutant `if (!is_trap || (vector == L &&
   cpu->delay_slot))`, MEASURED as an escape at each of the five in table 19.
G7 (all four, Q4) the pass-13 F5 sentence is right: only SFRZ is TESTED, so {site} x {MODE, SFD1, IND, C, SER} is clause (e) at
   every site and the L2 grades on v16/v17/v19 were given under a reads-PSR criterion.  Fable added: that criterion came from
   clause (d)(2), which "enumerates MUTANTS TO BUILD, not CELLS TO ROW"; GLM asked that the record NAME the criterion; Astra
   limited it to the five named bits.  **ACCEPTED with all three**: the criterion is "a state value the delivery path
   TESTS", which is exactly why `delay_slot` is floor and the five PSR bits are not.
G8 (all four, Q5) `m88ksfd1row`: the ledger line carries the warrant (table 16b's measured 62/63 plus the two asserts); NO
   addition-licence wording.  Grok and GLM had asked for wording on the close pass and withdrew it on pass 14 once 16b
   measured the row's delta.  **ACCEPTED** -- the owner question is withdrawn with them.
G9 (Grok 4.7) `OUTSTANDING_BUGS.md` still called the row pending at 58/58.  **ACCEPTED**: corrected in place.
G10 (GPT-6 Astra, Fable 5.1) appending table 16b's prediction to `PRETABLE.out` spent its mtime as table 16's order proof.
   **ACCEPTED**: `PRETABLE_ORDER.txt` records the file's NTFS birth time (17:59:43, before table 16's configure at 18:00:57)
   and the append (18:10:15, before 16b); every later table has its own PRETABLE file.
G11 (Fable 5.1) state the `m88kdslotshadow` re-pin once, in the shared scoring branch; comment the `%-9s` name column
   (`dslotpriv` is exactly nine wide); credit the under-enumeration in the docstring.  **ACCEPTED**, all three in v23.
G12 (Fable 5.1) the deriver encoded the overturned dispositions.  **ACCEPTED**: its delay-slot section is now the 28-cell grid.
G13 (Fable 5.1) the F8 correction was not yet in the ledger.  **ACCEPTED**: it lands in this commit's ledger write.
G14 (GLM 5.3) name the trap-exemption site and arms 0..3 in the disclosures.  **ACCEPTED**: the contract names both.
G15 (GPT-6 Astra) the pass-14 roster cannot report zero breaches while candidates survive; (Fable 5.1) pass 14's validity
   statement is "breaches found and enumerated".  **ACCEPTED** -- this pass is the one that may close.

## 8. Disagreements, both sides in their own words

D3 -- is (SFRZ set, slot set) floor, or a disclosed joint?
   * Grok 4.7: "`if (!is_trap && !cpu->delay_slot)` at line 816 is a predicted 63/63, and it is the disclosed joint: it adds
     `delay_slot` to the `is_trap` test."
   * GPT-6 Astra: "SFRZ and non-trap status identify the existing site; varying `delay_slot` adds one tested axis there."
   * Fable 5.1: "the floor is {label} x {SFRZ} x {delay_slot}, 28 cells, and the chain's own precedent agrees: killtable5
     closed {SFRZ set, non-trap} x {class} PER CLASS ... against label-level conjuncts of exactly the shape above."
   * GLM 5.3: "clause (e) there rests on an unstated premise: that EXCEPTION_IN_DELAY_SLOT vs NOT_DELAYED is unobservable to
     the probe" -- it IS observable: `X(br_n)` reads it (section 3), and table 19's M_DS865 is the measurement.
   * Coordinator: floor, by Fable's grid; and moot for closure either way, because the cells are rowed.  Grok, attack it.
D4 -- BOUNDS/ERROR x {slot}: floor (Fable, Astra) or disclosed (Grok, GLM)?
   * GLM 5.3: "if traps in slots are illegal, no legitimate guest reaches the cell; if legal, the cell exists but its correct
     oracle is unknown."
   * Fable 5.1: "The fork's ethos does not condition a guest-drivable host kill on the guest being well-behaved.  What
     legality governs is what the row may CLAIM."
   * Coordinator: floor; the rows claim emulator policy only, and say so.

## 9. Questions (VERDICT LINE FIRST)

Q1. Verify the grid in section 4 against the rows in section 5: for each of the 28 cells, does the credited row really raise
    that label with that SFRZ state and that slot state?  Name any mis-credited cell.
Q2. Is any of the ten new rows vacuous -- its channel unable to vary under the mutant it is credited with?  (Table 19 measures
    each; check that the right row is the one that reds.)
Q3. Inside the enumerated floor, is there any single edit to `m88k_exception()` that sweeps the 73-row probe?  Name it with
    its predicted score.  Do not propose cells outside the enumeration unless you can show the enumeration is incomplete.
Q4. Is the disclosed remainder complete and correctly classified: the frozen trap route at the five instruction labels in a
    slot (measured escapes), {delay slot} x {a PSR bit other than SFRZ}, three-or-more-axis joints, vectors 0..3's own
    delay-slot code (upstream, `m88kexchwtraps`)?
Q5. D3 and D4: is either ruling wrong?
Q6. Which of the coordinator's ACCEPTED dispositions G1-G15 is wrong?  (All fifteen are marked ACCEPTED.)
Q7. If nothing survives: CLOSE, with the denominator -- the delay-slot grid 28/28 (floor); the five PSR bits other than SFRZ at
    the seven labels 33/33 (35 less MODE at BOUNDS/ERROR, unreachable; the PSR grid's SFRZ column is NOT counted again, because
    the delay-slot grid's slot-0 half re-expresses it); fallback x six bits 6/6; non-trap re-route 5/5; trap exemption 5/5;
    fallback x {slot} 1/1 -- 78 enumerated cells, 28 of them floor, the other 50 clause (e) by G7 and G4, closed
    voluntarily.  Is it complete, and is the overlap removal right?

Seat notes: Fable 5.1 -- the grid is yours; check it harder than anyone, including the frozen rows' traces (`errdslotdiv0`
clears SFD1 with `stcr` first so its `divu` raises DIV0 rather than SFU1).  GPT-6 Astra -- G3 was yours; check the rows that
discharge it.  Grok 4.7 -- D3 is your call to defend or withdraw.  GLM 5.3 -- you cannot read files; say "not checkable from
the packet" where that is true.
