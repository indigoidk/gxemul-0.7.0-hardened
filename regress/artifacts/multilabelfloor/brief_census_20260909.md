# multilabelfloor -- CLASS CENSUS: which shipped detectors sit at a multi-label switch block whose selector flows into the repair's operands, and row only one label?

Please do not simply ratify. Check the premises, not just the derivations. ANALYSIS only -- no patch, no
code, no guest sequences. VERDICT LINE FIRST, then a table.

## THE TREE
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. Ignore any other `src/` under the project root. Read
`src/devices/*.c` and `regress/*_probe.py` / `regress/*_witness.py` as needed; the kill-table rounds are the
ones with a `regress/artifacts/<row>/killtable*` directory (derive the list with `ls`; do not trust a count
from this packet).

## THE RULE THIS CENSUS APPLIES (adjudicated 2026-09-09 on `sgimtedepth4dead` 7g-1, measured)
A dispatch LABEL is a FLOOR axis of an edited guard when the selector's value FLOWS INTO an lvalue the guarded
body reads or writes within the enclosing function, or when the body re-tests the selector after the join
(the pcc2 TxICR shape). A label that reaches the edit and touches nothing the body reads is clause (e) and
owes a disclosure sentence, not rows. The floor a qualifying label adds is {labels} x the guard operand's
body-tested partition -- never the labels' cross-product with everything. The measured instance:
`dev_sgi_re.c` `do_mte_transfer()`, `switch (dst_tlb) { case A: case B: case C: { ... dst_mode = (dst_tlb << 10)
+ ...; if (depth == 32) { src_mode |= RGBA; dst_mode |= RGBA; } ... } }` -- every row of
`regress/sgi_mte_fill_probe.py` drives label A, and `&& dst_tlb == MTE_TLB_A` scored 14/14 against a 14/14
base with the closed defect live at B and C. The counter-case: `mode & MTE_MODE_COPY` is tested later in the
loop and only the DEPTH field of `mode` flows into the repair's operands, so a COPY-conditioned mutant is (e).

## THE QUESTIONS -- answer extensionally
**Q1.** Enumerate every kill-table round's FIX SITE (the `/* #NNN: */`-tagged edit its detector defends; the
CHANGELOG block or the probe header names it). For each, is the edited guard inside a `switch` block served by
MORE THAN ONE case label (fall-through labels sharing a block)? Give file:line of the switch and the labels.
**Q2.** For each multi-label site from Q1: does the selector's value flow into an lvalue the guarded body
reads or writes within the enclosing function (name the lvalue and the line), or does the body re-test the
selector after the join? If neither, mark (e).
**Q3.** For each site marked FLOOR in Q2: which labels do the shipped detector's rows drive? (Read the probe:
how it programs the selector.) Name the labels with NO row. That list is the census result -- rows owed.
**Q4.** Name the ONE candidate you would measure first (highest severity, cheapest mutant), the mutant's exact
edit, and the row that would kill it. Do not build it.
Give the deriver for every count (the command you ran). State what you read versus what you took from
this packet. If the population is zero beyond the measured instance, say so plainly; a zero with its
denominator is a result.
