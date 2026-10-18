
## 7. Questions

**Scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py` (and `regress/gate_arm.sh`).**  Do not read
`regress/artifacts/` or `tools/pipeline/ledger.json` -- everything this brief takes from them is inlined above.  This is
an ordinary code review of a regression test's coverage, and of records about it.

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT OF THE REPAIR.  Test these; do not ratify them:**
  1. every one of the 20 label x latch cells is held by the row PRETABLE3 section 3 names, and each CLEAR cell really
     is the FIRST refusal of its site in its session (no earlier refusal of that site in the same session);
  2. every new cell's transfer would WRITE if its guard were exempted -- the tile it targets is mapped, the paint is
     repainted immediately before, and a linear cell runs at depth 8, BYTEMASK 0xffffffff, COPY clear;
  3. the crossbit session sets all 13 pre-existing bits BEFORE S1..S5, and `xbit primed` proves each with a distinct
     announcement text;
  4. the repair only APPENDS -- no existing row's commands before its read changed -- and the gate pins exactly the
     68 names the probe emits, both denominators 68.

**Q2 is not asked of this seat.**

**Q3 -- ROW VALIDITY OF THE NEW ROWS.**  Is any new row's observable unable to differ under the mutant PRETABLE3
section 4 names for it?  Does pairing an S1-CLEAR and an S2-CLEAR cell in one session confound either?

**Q4 -- RECORDS.**  Every ADDED or CHANGED sentence (the comment, the contract, PRETABLE3, the errata) that asserts an
observable consequence: true of the code, and carried by a row or by an explicit no-row sentence?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: CLOSE / SHIP WITH CHANGES (<n>) / DO NOT SHIP (<one line>)`, then
Q1, Q3, Q4.
