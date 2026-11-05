# D8 settled by the first run: r1's reading, not the merged one

`fixed_first.out` (the 43-row draft on `build/gxemul`, the fixed build, with ROW 3's want unset): the session
`srr0=SENT; pc=0x02040000; step 1; step 1; continue; continue` under `-T` printed **2** "non-existant" lines -- the first step's
two -- and nothing for the second step or either continue.  pc stayed 0x2040000, SRR0 the sentinel; no UNIMPLEMENTED, no
`read failed`, no `[ PPC Exception`, no checkstop text; the prompt came back after the repeats.  Every other row was green
(RESULT 42 of 43, the one red the unset want).

`PREDICTION_again.md` (written two seconds before the run) named two readings: 6 (r2, the ruling as merged: every repeat
re-enters the arm) or 2 (r1: the run loop stays parked on `nothing_call` and does not re-resolve next_ic from pc).  **2 is r1's.**
The reconciliation's section 5 names this outcome as the one that overturns its weakest ruling: "r1's want is restored, and the
're-enters the arm' sentences in both rulings need rewording."  ROW 3's want is frozen at 2 (`AGAIN_NONEX = 2`).

**Owed from it, to the fix (comment text only):** the arm's opening comment says "the slot stays TO_BE_TRANSLATED, so a later fetch
of this address re-enters this arm".  The slot does stay untranslated, but the sentence implies the repeats re-fetch, and they do
not: after a `-T` halt the CPU stays parked until something re-resolves next_ic.  To be reworded with the pass-2 text changes, and
the rewording measured comment-only (the file with comments stripped equal to the measured one).

## CORRECTION, 2026-11-05 -- the count stands, the cause given above is wrong

Ruled P1 and P8 by the adjudication (adj_20261104/ADJ_FABLE.md, ADJ_OPUS.md), on table 1's evidence.  This file says the 2 holds because
"the run loop stays parked on `nothing_call` and does not re-resolve next_ic from pc", and that "after a `-T` halt the CPU stays parked
until something re-resolves next_ic".  Table 1 refutes the park as the cause: D3_c_nopark (arm (c) without its park; pc moves to
0x2040004) and D4_b_inv (arm (b)'s refresh taken) both leave `again nonex` at 2 -- neither lists again_nonex red in table1/SCORES.txt.
The cause is memory.c: the -T report clears every CPU's running, so the run loop does not enter the CPU again and a further step or
continue runs nothing, whichever exit the arm takes.  The park in (c) only ends the current batch and keeps pc at the failing address.
The fix's arm (c) comment now says so ("A -T halt is terminal whichever exit is taken"), and the probe's AGAIN_NONEX comment cites D3 and
D4.  `again nonex` = 2 measures that a halted CPU is not resumed; it measures nothing about re-entry (PRETABLE.errata.md, item 3).
