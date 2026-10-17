## 6. The close adjudication's findings, consolidated -- with the coordinator's disposition on each

F1 (Fable 5.1) "the closing pass's 56-cell denominator omits `cpu->delay_slot` -- the one CPU-state lvalue `m88k_exception()`'s
   repair path TESTS -- and {MISALIGN, UNIMPL, PRIV, OVF} x {delay slot set} are unrowed".  **ACCEPTED, MEASURED** (section 1
   item 2); L2; repair 13 is the diff in section 3.  None of the three CLOSE answers enumerated `delay_slot`.
F2 (Fable 5.1) BOUNDS and ERROR x {delay slot}: "reachable in the emulator by a `tb1` in a `.n` slot ... whether the
   architecture permits a trap instruction in a slot I could NOT settle from `mc88100.txt` -- disclosed, not counted".
   **ACCEPTED**: disclosed in the contract, with both forms MEASURED as escapes in table 16 rather than predicted.
F3 (Fable 5.1) "a frozen handler with a `.n` slot fault (`errdslot`) is cheap and I recommend it ride with the repair, but it is
   not in the floor as bounded here".  **FILED** as clause-(e) coverage, not added: outside the bound by the recommending seat's
   own statement, and a row added after PRETABLE.out was written would have re-opened table 16.
F4 (Fable 5.1) "four more rows pinned to [the else-arm] must carry the same re-pin-first note".  **ACCEPTED**: one shared
   scoring branch (`name.startswith("dslot")`), and the docstring row table says so.
F5 (Fable 5.1) the deferred cut question is ANSWERED, not moot: by the carrier's 2026-09-25 pin ("tests" = masks or compares as
   a case) and its 2026-10-09 ruling (a derived input is graded by what the body tests on it), `m88k_exception()` tests ONE PSR
   bit, SFRZ, so {site} x {MODE, SFD1, IND, C, SER} is clause-(e) coverage at every site; v16/v17/v19 were graded L2 "under a
   reads-PSR criterion the carrier's 09-25 pin does not support"; one sentence in the closure note.  **ADOPTED AS A RECORDS
   SENTENCE ONLY -- no row, no code, no rule change.  Disputed: see D1.**
F6 (all four) `m88ksfd1row`: KEEP.  **ACCEPTED**: close the row "kept, not owed" (warrant in F7 and D2).
F7 (Fable 5.1) the row's delta is not zero against every mutant: the disclosed joint `if (!is_trap || ((PSR & MODE) &&
   !(PSR & SFD1)))` "reds `trapfrozensfd1` and no other row" (REASONED); and the shared-constant hazard's structural defence is
   "two import-time asserts in the probe ... named for the cells they carry".  **ACCEPTED**: the asserts are in the diff and
   negative-controlled; the joint mutant is MEASURED in table 16b (section 4) -- it is the stated warrant for keeping the row.
F8 (GPT-6 Astra) "Table 15 reports 57/59, with two failing rows.  Removing `trapfrozensfd1` would leave 57/58 ... not 58/58."
   **ACCEPTED, L4**: corrected in place in the probe comment (this diff), and in the same commit in `fable_queue.md`, the
   CHANGELOG #502 block and the `m88ksfd1row` ledger witness, each quoting what it corrects.
F9 (Grok 4.7) "`derive_cells.py` and `CELLCENSUS.out` still stop at the 57-row instrument and still print trap-side MODE and SFD1
   open ... a records defect".  **ACCEPTED**: fixed (section 1 item 4); the new delay-slot section of its output is in section 4.
F10 (GLM 5.3) "'this four-seat adjudication is the missing roster' overstates ... The record should read 'pass-12's measurement,
   ratified by three independent audits plus the author's self-review.'"  **ACCEPTED in substance, and overtaken**: that pass
   did not close the chain.  If this pass closes it, its validity is: the diff delivered (section 3); four of nine seats by owner
   ruling, the other five named as not fired; zero breaches stated WITH the denominator (Q7).
F11 (GLM 5.3) P1-P3 (the ground for the MODE exclusion; which bits vary at the frozen sites; `trapfrozensfd1`'s stimulus).
   **SETTLED from the committed probe text** -- the third and fourth bullets of section 2.
F12 (GPT-6 Astra) "I retract pass 12's rejection of retention; its rejection of attribution as a transferred warrant and its
   zero-floor finding stand."  **RECORDED**; the zero-floor finding is refuted by F1's measurement.

## 7. Disagreements, both sides in their own words

D1 -- the deferred cut question (F5).
   * Fable 5.1: "The question is answered by the carrier's own later pins, the answer re-grades three of this round's repairs from
     L2 to voluntary clause-(e) closure, and leaving it 'for a future round' leaves the over-grade standing as the precedent that
     future round will cite."
   * GPT-6 Astra: "moot for closure, unresolved generally ... This does not retrospectively endorse pass 7's classification."
   * Grok 4.7: "Moot as stated.  No remaining cell of this round is held out by 'the arm reads no PSR bit' ... Whether that test is
     the right DEPENDS-ON cut on a future round is a rule for the owner when a live cell still depends on it."
   * GLM 5.3: "moot as to rows, not as to the denominator" (conditional on its P1, which section 2 now settles as reachability).
   * Coordinator: no seat disputed Fable's premise (only SFRZ is TESTED); the three "moot" answers address row demand, which
     Fable agrees nothing depends on, and none addresses the precedent value of the recorded L2 grades.  So the sentence goes in
     the closure record, attributed, beside the three moot rulings.  Attack this if it is wrong.

D2 -- does the addition licence need a sentence for `m88ksfd1row`?
   * Grok 4.7 (yes): "A zero-delta row is licensed when it is the only stimulus for an enumerated cell that does not share a
     constant with rows whose oracles do not observe that bit, and a one-token edit of the shared constant preserves those rows
     and deletes the stimulus ... 'Kept, not owed' will be copied onto the next zero-delta row unless the ledger line cites the
     shared-constant condition above."
   * GLM 5.3 (yes): "a 'kept, not owed' record with no warrant is unstable -- the next zero-delta pass applying 'row demand bounded
     per enumerated mutant' removes it".
   * Fable 5.1 (no): "The addition licence governs PRODUCT code; it is the wrong instrument for a detector row.  Row demand ...
     bounds what is OWED, not what is PERMITTED.  Neither says delete ... One instance does not earn carrier prose."
   * GPT-6 Astra (no): "KEEP, with no licence or row-demand change ... the carrier explicitly extends the objection to
     attribution-only detector additions, so 'PRODUCT code' alone does not settle applicability.  But neither rule mandates
     pruning every redundant row."
   * Coordinator: no carrier wording in this round -- the carrier's own structure-first rule prefers the two asserts to a
     paragraph -- but the ledger line CITES the warrant (Grok's condition plus F7's measured delta), so it cannot be copied bare.
     The wording question goes to the owner as a rule question.

## 8. Questions (VERDICT LINE FIRST)

Q1. Does v20 close {arm} x {delay slot} at the five arms an instruction reaches from a slot?  Name any edit to
    `m88k_exception()` that sweeps the 63-row probe inside the floor -- a single-axis cell of a body-TESTED lvalue at a dominating
    predicate -- with its predicted score.  Section 5 is the whole function; mind its common tail.
Q2. The delay-slot axis at the OTHER two sites.  The fallback (799) halts without reading `delay_slot`; the frozen path sets
    `update_shadow_regs = false`, so the 840 test is not reached, but the 865 write is.  Coordinator: {fallback, SFRZ re-route} x
    {delay slot} is clause (e), and `errdslot` is filed.  Floor or clause (e)?
Q3. BOUNDS / ERROR x {delay slot}: disclosed, or floor?  If floor, give the row (a `tb1` naming 7 or 10 in a `.n` slot) and its
    expected shadows.
Q4. D1: is the F5 records sentence right?
Q5. D2: licence wording, or the ledger-line warrant?
Q6. Which of the coordinator's ACCEPTED dispositions is wrong?  There are nine: F1, F2, F4, F6, F7, F8, F9, F10, F11.  (F3 is
    filed, F5 adopted under dispute, F12 recorded.)
Q7. If nothing survives: CLOSE, with this denominator -- the PSR grid 40/40 at the seven arms, fallback 6/6, non-trap re-route
    5/5, trap exemption 5/5, and the delay-slot axis 5/5 at the instruction-reachable arms = 61 enumerated cells; disclosed:
    BOUNDS/ERROR x {delay slot}, trap instructions in a slot at any arm, {fallback, re-route} x {delay slot}, multi-axis joints,
    vectors 0..3 (`m88kexchwtraps`).  Is that denominator complete?

Seat notes: Fable 5.1 -- F1 and F7 were yours; be harder on the repair than on the finding, including whether five rows pinned
to an else-arm the manual calls wrong is the right shape.  GPT-6 Astra -- your pass 12 is what this overturned; check the
repair, not only the count.  Grok 4.7 -- passes 9 and 11 were yours.  GLM 5.3 -- you cannot read files; say "not checkable from
the packet" where that is true rather than guessing.
