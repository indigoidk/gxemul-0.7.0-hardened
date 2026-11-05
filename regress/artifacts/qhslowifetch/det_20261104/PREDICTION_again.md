# qhslowifetch detector, ROW 3 -- the two hypotheses, written BEFORE the first run (this file's mtime precedes `fixed_first.out`'s)

ROW 3 (cloud Fable's reconciliation, `../adj_20261104/RECON_FABLE.md` section 4) repeats the halt in one `-T` session:
`srr0=SENT`, `pc=0x02040000`, `step 1`, `step 1`, `continue`, `continue`.  Its want is PROVISIONAL and "frozen from the first run";
the reconciliation names D8 as its weakest ruling, and the first run decides between two readings:

* **r2's reading (the ruling as merged):** the slot stays TO_BE_TRANSLATED and a later fetch re-enters the arm, so every repeat
  prints again -- two "non-existant" lines per step and one per continue, as rows 1 and 2 measure singly: **6** in all.
* **r1's reading (restored if the first run says so):** after the first halt the run loop parks on `nothing_call` and does not
  re-resolve next_ic from pc, so the repeats print nothing new: **2** in all (the first step's two).  Then the "re-enters this arm"
  sentence in the fix's comment and in both rulings needs rewording, as the reconciliation's section 5 says.

Any other count is neither reading and is reported as such before anything is frozen.  pc and SRR0 must stay 0x2040000 and the
sentinel under both, with no UNIMPLEMENTED, no `read failed`, no `[ PPC Exception` and no checkstop text.
