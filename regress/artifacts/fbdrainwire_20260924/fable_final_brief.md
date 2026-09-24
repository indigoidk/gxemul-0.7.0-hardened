# `#548` fbdrainwire -- the FLAGSHIP seat's FINAL pass (you fire LAST; you already ruled on pass 1)

Open with the line `FABLE548F_ALIVE`, then the FIRST LINE of `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`
verbatim, then `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>` and numbered findings.  READ-ONLY for
`C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\`; measure, if at all, only in a scratch copy under
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fable548\`.  Keep the answer under about 1500 words, verdict and any ruling you
would change at the top.

## Where the round stands

Your pass-1 ruling (`fable5_p1.md`) was applied.  Since then (all under `GXEMUL-SEC/regress/artifacts/fbdrainwire_20260924/`):
* **pass 2** (`p2_brief.md`, `panels/panel_20260924_055454`, `panels/codex_dedicated_p2.txt`, `opus5_p2.md`) -- every seat
  SHIP WITH CHANGES; the Opus seat measured M_cmp0 (`pending_bound[0]` in the compare) passing every row: an L2 floor
  breach -> revision 2;
* **table 3** (`opus5_p3.md`) -- its one ask found R6's pin retargetable -> revision 3;
* **the SF2 adjudication pass** (`f2_brief.md`, `panels/panel_20260924_071301`, `panels/codex_dedicated_f2.txt`,
  `opus5_f2.md`) -- the Opus seat MEASURED M_eq_n2 (`==` on every timer but timer 2) passing everything, 4529 owed at
  rung 3: the third breach of one class -> revision 4, the CLASS CLOSURE (R6 = every timer x {re-armed at count 0,
  re-armed owing 8192} at distinct rates; per-timer R5; whole-line gate-2 pins; the drain block pins load/ctrl and
  counts D and X separately);
* **the closing pass** on revision 4 (`c_brief.md`, `panels/panel_20260924_075202`, `panels/codex_dedicated_c.txt`,
  `opus5_c.md`, `t4_rev4/`) -- ZERO floor breaches inside the enumeration from seven of eight transports, both codex
  jobs (all relational operators on every timer subset; all 256 `nr`-only index maps at three sites; 65,536 joint maps)
  and the Opus seat (18 new mutants of the fix's own predicate, reset and store, all red).  Comment-only corrections
  applied afterwards (code identical, checked).  `CORRECTIONS.md` records every false sentence in the dated artifacts.
* **final gates** on the committed text: gate 2 PASS, 359 checks, 171 s, both named-row pins ok (`gates_final/gate2.out`); gate 14 PASS, 1095 checks (1082 + the 13 new), all 41 drain checks green, 4017 s (`gates_final/gate14.out`).
* **records drafts**: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\u3_cpp\cl548_draft.md` (CHANGELOG block),
  `bugs548_draft.md` (six filings), `ledger_548.py` (the row, every seat's verdict, the filings, three notes).

## The rulings I need from you

1. **P_win** (the Opus seat, closing pass, MEASURED): `count >= bound && count <= bound + W` with W wide enough to hold
   the owed 8192 passes every row; W = 10000 left 49603 owed against 762 at rung 3.  I graded it **clause (e) -- FILED**:
   it splits the ROWED past-the-bound cell at a value the body never tests, whereas `==` (L2) escaped because that cell
   was NOT rowed.  The Opus seat raised the counter-argument itself: this round graded `==` L2 for its consequence, P_win
   has the same consequence, and clause (d) lists "a condition qualified" as a canonical (d) form.  The closure is one
   constant (owe the largest debt a correct build can hold).  **Rule: L2 (fix in-round) or clause (e) (file)?**
2. **deepseek's closing-pass DO NOT SHIP** counts the filed store guards (M_neqB, M_zge, M_upskip) as floor breaches.
   I overruled it on the floor rule's text (a guard a mutant ADDS to an unconditioned store is not a DEPENDS-ON cell);
   five seats argued the same.  Uphold or overturn.
3. **Which of my closing-pass dispositions is wrong?**  Name the count.  In particular: is the contract text in the gate
   block and in R6's comment now TRUE sentence by sentence?  (Every pass of this round found at least one false one.)
4. **May the chain close and the round ship?**  If not, what exactly remains.
5. **The records drafts:** anything false, missing, or mis-graded in the CHANGELOG block, the filings or the ledger
   script -- including the late-dissent line owed to #442's own record.
