# CORRECTION to `brief_m88kexc_p10.md` -- TWO WRONG NUMBERS, both found by the kimi seat, both mine.  2026-09-06.

The pass-10 packet's verdict was upheld (grok: CLOSE THE CHAIN, 0 of 40 open; the census below reproduces it).
**Neither correction changes a measurement or a disposition.**  Both are summary numbers that were wrong while the
measurements under them were right -- which is now the THIRD consecutive human-readable summary in this chain to
fail that way, and the reason the deriver beside this note exists.

## 1.  The control's frozen-v16 score: the packet said `23/41`.  It is `27/54`.

`23/41` is that mutant's score on the **v10** instrument, from a different table on a different day.  I took a
number from the wrong column of my own artifacts.  Measured, from `killtable14/`:

    CTL_DIV0SERINV_on_v10.out          M88KEXC_RESULT=23/41      <- what the packet printed
    CTL_DIV0SERINV_on_v16.out          M88KEXC_RESULT=27/54      <- what the column was for
    CTL_DIV0SERINV.out                 M88KEXC_RESULT=30/57

The control's PURPOSE is unaffected: it reds 27 rows on both instruments, which is what makes it a control.  Note
`41` could not have been a v16 score at all -- v16 has 54 fault rows -- so the DENOMINATOR was the tell, exactly as
it was on table 13.  I did not check it.

## 2.  "the previously-closed 23" -- a total with no deriver.  The figure is **34 of 40**.

The packet's one question asked whether any of the 40 cells is missed by "the eight rows plus the previously-closed
23".  **23 is not derivable from anything.**  kimi said so plainly -- *"pre-v17 coverage is 34 of 40 cells; 23
matches nothing I can derive"* -- and flagged it as immaterial to the verdict but worth a line.  It is worth more
than a line, because I had used that same 23 an hour earlier to refute a seat's arithmetic, showing `17 + 23 = 40`.
**That refutation was wrong.**  The seat's instinct that the numbers did not add up was right even though its own
count was not, and I dismissed it with a number I could not have sourced.

`derive_cells.py` beside this note settles it mechanically and prints the GRID rather than the total, because a
per-cell breakdown is checkable and a total is not.  Its output is `CELLCENSUS.out`:

| instrument | cells closed | open |
|---|---|---|
| v16 (what pass 9 reviewed) | **34 of 40** | the SER cell at MISALIGN, UNIMPL, PRIV, DIV0, OVF, ERROR |
| v17/v18 (shipped) | **40 of 40** | none but the two declared unreachable |

**The census independently confirms pass 9's finding rather than restating it:** v16's only closed SER cell is at
BOUNDS, by `trapfrozenser` -- one arm out of seven, which is precisely what grok said v16 had done while its
contract claimed the axis.  Nobody fed the deriver that conclusion; it falls out of the row table.

It also confirms grok's pass-10 census cell-for-cell, including WHICH two cells are unreachable (BOUNDS x MODE and
ERROR x MODE), which grok named independently from the manual and the source.

### The cell definition, which is the one judgement here rather than a transcription
A mutant conditioning `implemented` on bit B at arm A -- in EITHER polarity -- is killed iff two rows enter switch 1
at A with DIFFERENT values of B.  So the cell is CLOSED iff B VARIES across A's rows.  That is polarity-free, which
is why it is the right formulation: v16's own comment observes the open cells "are always (C never set) and (IND
never clear)", i.e. the arm's rows AGREE on the bit.

## 3.  What the census ALSO settled, unasked -- the minimax challenge, answered by measurement

minimax voted ONE MORE REPAIR on the ground that `resid50ser`'s description ("the fallback, whose own blurb already
claimed every settable bit on both sides") is a row whose blurb claims an axis while the row tests one cell -- pass
9's defect shape reproduced.  **That is the right challenge and it was right to make it from the packet alone**,
which never said what the other fallback rows hold.  The census answers it:

    FALLBACK, v16:  SER open -- every row has SER=0        <- minimax's suspicion was correct about v16
    FALLBACK, v17:  all six bits closed; SER=1 by resid50ser alone

So the blurb's claim is true of the ROW SET and false of any single row -- grok's *"the axis is the set of rows, not
any one of them"*.  `resid50ser` closes exactly one cell and the sentence around it claims six; the other five are
held by `usfu1` (MODE, SFD1), `resid50c` (C), `resid50ind` (IND) and `sfu1h` (SFRZ).  Recorded because a packet that
had said this would not have cost a seat its vote.

## 4.  One thing the census found that nobody has named -- FILED, not fixed

At the SFRZ re-route's **trap side**, MODE and SFD1 do not vary: all fourteen trap rows carry MODE=1 and SFD1=1.
A widened inner guard -- `if (!is_trap || !(PSR & M88K_PSR_MODE))` -- would therefore escape the 57-row instrument,
and the cell is REACHABLE: a frozen handler can drop to user mode (as `errpriv` already does) and then take a user
trap at a vector >= 128 (as `trapfrozen128` already does), so the two halves both exist and no row combines them.

**This is DERIVED, not measured, and it is DEBT rather than a floor breach.**  The floor asks for the partitions the
guarded body itself tests; that body tests `is_trap` and the outer `PSR & SFRZ`, and both polarities of both are
rowed.  MODE at the trap side is a single-axis marginal against an lvalue the body does not test there, which
clause (e) discloses.  Filed as `m88kexcrrtrapmode`.

*And I nearly filed a FALSE L4 beside it: the contract's sentence "every stcr-settable 88100 bit now varies there"
reads like a per-branch claim and is measurably false of the trap side alone.  It governs the OUTER guard, which
sees both branches -- and over their union every bit does vary.  The claim is correct as written.  Checked before
writing, which is the only reason this paragraph is a near-miss and not a fifth wrong record.*
