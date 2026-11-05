# PRETABLE.out errata -- qhslowifetch

Ruled P18 by the adjudication (adj_20261104/ADJ_FABLE.md, ADJ_OPUS.md).  PRETABLE.out is the order proof for table 1, so it is NOT
edited; each refuted sentence is quoted here as it stands, then corrected.  Written 2026-11-05.

1. **PRETABLE.out:12** -- "and MSR = 0 on every -T session measured -- so the chkstop rows are the one channel that sees (c) deleted or
   inverted".  Two errors.  MSR is 0 on `T step`, `T cont` and `again`; `T me` sets MSR[ME] (0x1000), as the next clause of the same
   sentence says.  And the chkstop rows are not the one channel: table 1 (table1/SCORES.txt) has D1_c_inv and D2_c_del red on T_me_pc,
   T_me_srr0 and T_me_exc as well as on the three chkstop rows (44/50 each).  On the ME-clear sessions the checkstop text is the only
   channel that differs; on `T me`, arm (c) deleted or inverted delivers the machine check and moves pc and SRR0.

2. **PRETABLE.out:43** -- "again nonex -- D4 (re-entering repeats print 6, not 2)", and **:55** -- "red: again nonex only (the repeats
   re-enter: 6, not 2)".  Measured otherwise: D4_b_inv is red on T_cont_nonex only (49/50), and `again nonex` stays 2 under D4 and under
   D3_c_nopark.  A -T halt leaves running at 0 (memory.c), so the repeats run nothing whichever exit the arm takes.

3. **PRETABLE.out:17** -- "'the slot stays TO_BE_TRANSLATED, so a later fetch of this address re-enters this arm' -> again nonex = 2
   MEASURES THE OPPOSITE".  It measures neither reading: no debugger session can produce a later fetch after a -T halt, because nothing
   restores running.  `again nonex` = 2 measures that a halted CPU is not resumed -- nothing about re-entry, which no row on this harness
   can test.  The probe's contract now discloses re-entry as not claimed.
