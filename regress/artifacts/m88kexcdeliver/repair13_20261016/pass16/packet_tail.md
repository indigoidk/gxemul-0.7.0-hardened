## 7. Pass 15's findings, consolidated -- with the coordinator's disposition on each

K1 (Fable 5.1) `is_trap` is the fourth tested input; the ten trap-in-slot cells at the five instruction labels are floor; table
   19's five 73/73 are L2.  **ACCEPTED** -- the ten rows are this diff (`dslot<L>tb`, `trapfrozen<L>dslot`); table 20.
K2 (Fable 5.1) the arm-level `implemented = !(cpu->delay_slot && is_trap)` at the five labels is a PREDICTED 73/73 sweep of v23.
   **ACCEPTED** -- MEASURED on v24 in table 20 (M_ARMTS_<L>) and killed; its SFRZ-clear-only twin M_ARMTSU_<L> isolates the
   unfrozen cell's own row.
K3 (GLM 5.3) the user-trap labels x {slot} were unnamed.  **ACCEPTED as a DISCLOSURE** (Fable's classification), with the two
   escapes MEASURED in table 20 (`!is_trap || (vector >= USER_TRAPS_START && cpu->delay_slot)` at :816;
   `cpu->delay_slot && vector < USER_TRAPS_START` at :840).  GLM's alternative -- two representative rows -- is D6.
K4 (Fable 5.1) {fallback} x {SFRZ} x {slot} should be named.  **ACCEPTED, ROWED**: `sfu1hdslot` (clause (e), rowed on its
   measured escape M_FBFRZDS).
K5 (Grok 4.7) the vectors-0..3 pointer.  **ACCEPTED, committed** (16512e9c).
K6 (Fable 5.1) name both probe md5s; (Astra) the deriver's grid is hand-transcribed, not a reachability proof.  **ACCEPTED**:
   the commit names the md5s; the grid's credits are re-checked against the row definitions by this pass (Q1).
K7 (Grok 4.7, GLM 5.3) Q7's 78 double-counted or mis-attributed the re-route buckets.  **ACCEPTED in part**: the 5+5 re-route
   buckets are PSR-bit cells at the re-route (CELLCENSUS "SFRZ RE-ROUTE" sections), not the grid's (SFRZ set, slot clear)
   cells, so they are not double-counted -- but they are clause (e) by G7 (untested PSR bits), and Q7 below drops the 78 in
   favour of naming the floor alone.
K8 (all) the ledger write must land.  **DONE**: 16512e9c's ledger carries the close adjudication, passes 14 and 15, the five
   unfired seats by name, both repairs and the m88ksfd1row closure.

## 8. Disagreements, both sides in their own words

D5 -- is `is_trap` a floor axis?
   * Grok 4.7: "Pass 11's owed floor is the switch-1 labels crossed with the device-state lvalues the repair path tests ...
     `is_trap` is a parameter, tested only inside the SFRZ block.  A joint the body distinguishes and that product does not
     owe is clause (e)."
   * GPT-6 Astra: "Under the carrier's device-state bound, `is_trap` is a per-raise selector rather than another persistent
     state axis.  Their disclosure as clause-(e) debt is therefore defensible."
   * Fable 5.1: "`is_trap` is this function's one input bit, tested as a case; `if (!is_trap || (vector == L &&
     cpu->delay_slot))` is a state x input-bit joint at a label -- the M_ICLR shape exactly ... The v23 mutant is that same
     mutant with `&& cpu->delay_slot` appended.  My 'sub-cell' argument would have excused trapfrozen4..9 too, and the chain
     did not accept it there."
   * Coordinator: Fable's, as section 1 says.  Grok and Astra -- if this is wrong, name the carrier text that excludes an input
     bit the body tests from the generating set, and say what grade the pass-5/7 repairs should then have had.
D6 -- the user-trap labels: rows (GLM) or disclosure (Fable)?
   * GLM 5.3: "Remedy: two representative rows (`usertbdslot`, a frozen 128-in-slot) or a disclosure line naming the family
     with a tracker, like the 0..3 line."
   * Fable 5.1: "outside the fix's labels (trapfrozen128/450/496/511 were voluntary closures of the exemption's label range),
     so disclose rather than row."
   * Coordinator: disclosure, with both escapes measured; the rows would pin pre-#502 behaviour the fix never touched.

## 9. Questions (VERDICT LINE FIRST)

Q1. Verify the grid in section 4 against the rows in section 5: for each of the 48 reachable cells, does the credited row raise
    that label with that SFRZ state, slot state and is_trap value?  Are the 8 unreachable cells really unreachable?
Q2. Is any of the eleven new rows vacuous -- unable to red under the mutant it is credited with?  (Table 20 measures each.)
Q3. Is the four-input claim of section 2 right?  If the function tests a fifth input, name it with a reachable cell and a
    single edit that sweeps the 84-row probe.  Otherwise: inside the 48 cells, any sweeping single edit?
Q4. Are the disclosures complete and correctly classified: user-trap labels x {slot} (measured escapes), {slot} x {PSR bits
    other than SFRZ}, vectors 0..3's own delay-slot code (`m88kexcdebt`)?
Q5. D5 and D6.
Q6. Which of the coordinator's ACCEPTED dispositions K1-K8 is wrong?
Q7. If nothing survives: CLOSE, with the denominator -- the floor is the 48 reachable cells of {7 labels} x {SFRZ} x
    {delay_slot} x {is_trap}, all rowed and each killed under its own mutant in table 20; everything else enumerated is
    clause (e) (closed voluntarily or disclosed with a measured escape).  Is that complete?

Seat notes: Fable 5.1 -- the is_trap axis was yours; check the ten rows' traces and the unreachable-cell claim harder than
anyone.  GPT-6 Astra and Grok 4.7 -- D5 was ruled against you; answer it on the carrier's text.  GLM 5.3 -- D6 is yours;
say "not checkable from the packet" where that is true.
