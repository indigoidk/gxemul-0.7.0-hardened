## 9. Questions

**Scope your reading to `GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`.**  Do not read `regress/artifacts/` or
`tools/pipeline/ledger.json` -- everything this brief takes from them is inlined above.  This is an ordinary review of
error handling in a device model: what the code does when a guest programs a transfer the model does not support.

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT.  These are the premises the design stands on; please test them, not ratify them:**
  1. the census -- six `exit(` statements in `dev_sgi_re.c` at HEAD, five reachable (S1-S5), the sixth unreachable;
  2. each measured row in section 2 reached ITS OWN site -- the attribution is "own diagnostic text present, the other
     four sites' texts absent".  Is that a sufficient answer to "did it stop for the reason under test?"  Could two
     sites share a text, or a row pass an earlier check it was meant to stop at?
  3. the proposed handling returns before ANY memory write at every site (section 7, the paragraph after the leaning);
  4. Q-b's claim that a FILL never reads the source selector;
  5. the zeroed `BYTEMASK` (a linear fill that never wrote BYTEMASK reaches S5);
  6. no completion status can leave a guest waiting after a refused transfer.

**Q2 is not asked of this seat.**

**Q3 -- OPTION-SET COMPLETENESS.**  Is there a disposition this brief did not name?  Look at how other transfer or DMA
engines in `src/devices/*.c` refuse an unsupported request (`grep -rn 'declined' src/devices/*.c` is a start) -- the
tree's own precedents are part of the design space.  And is any member I set aside (4, 5, 6) actually right at one
site?

**Q4 -- the round-specific questions Q-a to Q-e in section 7**, one answer each.

**Q5 -- ROUND SCOPE.**  This project's scope rule: a round takes ONE site; a second joins only if it is reproduced, in
the same device and the same semantic class (one design covers both), and covered by the same test with no new oracle.
Do all five meet that together?  If Q-b's answer is "scope S2 to COPY", is S2 still the same class?

**Q6 -- THE TEST (section 8).**  For each proposed row: can its observable actually differ between the correct code and
the defect it is meant to catch?  A row whose observable is the same either way tells us nothing.  Which cell of the
input space is missing -- in particular the destination-label axis (`LIN_A` / `LIN_B` share S3-S5's block, and the
linear body reads `dst_tlb` to pick `re_linear_a` or `re_linear_b`) and the bounds in S2 and S5?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: PROCEED AS PROPOSED / PROCEED WITH CHANGES (<n>) / REDESIGN
(<one line>)`, then Q1 and Q3-Q6.
