## 9. Questions

Answer in this order, each with its number.  Facts you checked carry `path:line` or a quoted line.

**Q1 -- PREMISE AUDIT.  These are the premises the design stands on; please test them, not ratify them:**
  1. the census -- six `exit(` statements in `dev_sgi_re.c` at HEAD, five reachable (S1-S5), the sixth unreachable;
  2. each witness row reached ITS OWN site -- the attribution in section 2 is "own fatal text present, the other four
     sites' texts absent".  Is that a sufficient answer to "did it end for the reason under test?"  Could two sites
     share a text, or a row pass an earlier guard it was meant to stop at?
  3. the decline returns before ANY memory write at every site (section 7, the paragraph after the leaning);
  4. Q-b's claim that a FILL never reads the source selector;
  5. the zeroed `BYTEMASK` (a linear fill that never wrote BYTEMASK reaches S5);
  6. no completion status can hang a guest after a declined transfer.

**Q2 -- THE SMALLEST EDIT.**  Against the fix in section 7 and the rows in section 8: what is the smallest edit to
`do_mte_transfer()` that brings back a guest-visible defect at one of S1-S5 (the process ending, a write the decline
should have prevented, a flood) while every proposed row stays green?  Name the row you expect to stay green.

**Q3 -- OPTION-SET COMPLETENESS.**  Is there a disposition this brief did not name?  Grep the fork for how other
transfer or DMA engines refuse an unsupported request (`grep -rn 'declined' src/devices/*.c` is a start) -- the
tree's own precedents are part of the design space.  And is any member I set aside (4, 5, 6) actually right at one
site?

**Q4 -- the round-specific questions Q-a to Q-e in section 7**, one answer each.

**Q5 -- ROUND SCOPE.**  This project's scope rule: a round takes ONE site; a second joins only if it is witnessed, in
the same device and the same semantic class (one fix design covers both), and covered by the same detector with no new
oracle.  Do all five meet that together?  If Q-b's answer is "scope S2 to COPY", is S2 still the same class?

**Q6 -- THE DETECTOR (section 8).**  For each proposed row: can its CHANNEL actually vary under the edit it is meant to
catch?  A row whose observable is the same with and without the defect is vacuous before any table runs.  Which floor
cell is missing -- in particular the destination-label axis (`LIN_A` / `LIN_B` share S3-S5's block, and the linear body
reads `dst_tlb` to pick `re_linear_a` or `re_linear_b`) and the bounds in S2 and S5?

If, while verifying a claim, you found something ELSE -- say so.

Format: open with your token, then ONE line `VERDICT: PROCEED AS PROPOSED / PROCEED WITH CHANGES (<n>) / REDESIGN
(<one line>)`, then Q1-Q6.
