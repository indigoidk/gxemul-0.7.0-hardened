# #551 F2-on-pass-2 findings, queued until every F2 seat has answered (then Fable rules, then ONE patch)

From the Opus 5.5 seat (wdcidselfcheck_20260925/opus5_f2b.md; measured in opus551_measured_f2b/):

H. NEW ESCAPE outside the disclosed classes (MEASURED): `failures = 0;' in main() right after
   row_ring_occupancy_sound() -- after every covered call, before the self-mutant's row -- keeps gate 2 green on the
   drop-oldest, DRQ-dropped and word-57 variants: covered rows print FAIL, the trailer reads 0 failures and PASS.  The
   self-check measures its own deltas and restores the tally, so it passes and sets sc_g.
   Proposed fix (MEASURED byte-identical on 9 variants): `cmp_fails ++' beside `failures ++' in chk() and row_cmp(),
   restored with `failures' in the self-check, PASS requires cmp_fails == 0; the reset edit then FAILs, and defeating
   the fix takes two statements.  Or DISCLOSE "the tally between the comparators and the verdict".
   My proposed disposition: ADOPT (the same class as sc_g -- the run's own verdict lying) and disclose the two-statement
   form.  For Fable to rule.
I. Q4's sentence is FALSE (MEASURED): row_cmp()'s `sectors' operand is never 0 in the probes {2,2,1,3,2^32,2^32}, and
   `&& sectors' added to row_cmp() passes all 11 probes.  Fix: add the probe (sectors 0, got57 1, got60 0) -- then
   "each operand zero and past 32 bits" is true of every row_cmp() operand.  (Or reword to "each got operand".)
J. Q10's wording was wrong: H greps the SOURCE (the token leaves with the deleted block), not the run's output.  And
   the record should carry the second deletion form (block + calls deleted, sc_g and verdict left: the run FAILs,
   gate 2 reds verdict, H, G and lane) -- the likelier maintenance edit, and exactly what sc_g buys.
K. Q8 checked: at 7e3b1204 the two differentials were 1311 and 766 lines -- "true when written" holds.
