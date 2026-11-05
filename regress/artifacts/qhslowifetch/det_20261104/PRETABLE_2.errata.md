# PRETABLE_2.out errata -- qhslowifetch table 2

PRETABLE_2.out is table 2's order proof, so it is NOT edited. Each prediction that table 2 (table2/SCORES.txt) did not match exactly is
quoted here and corrected. Written 2026-11-05, after the table ran. None changes a catch: every variant below is red either way.

1. **W5_dec_tail** -- predicted "W5's set ... ; T ra nonex (the read-ahead slot is translated from garbage, so no real fetch) and maybe
   pc", 11 red, 45/56. **Measured 43/56**: the ten -T rows of W5's table-1 set plus T_ra_pc, T_ra_nonex and T_ra_addr. The garbage-decoded
   read-ahead slot also changed which addresses the halt reports name. PRETABLE_2 already marked this variant BUILD-DEPENDENT (P25:
   the uninitialised instruction word decides which rows red, never whether any does), and the measured set fits that disclosure.

2. **D7_dom_run** -- predicted "as W5, T ra included", 11 red, 45/56. **Measured 43/56, the same thirteen rows as W5**, for the same
   reason: memory_rw clears running before it returns, so the failure arm is skipped and the uninitialised word decodes.

3. **D12_else_ra** -- predicted "T ra nonex addr stopped ... the session may run on to its timeout", 3 red. **Measured 3 red with a
   different set**: T_ra_pc, T_ra_nonex and T_ra_addr. `T ra stopped` stayed green: the machine did stop, so running reached 0
   (CORRECTED 2026-11-05 by the repair-pass-2 adjudication, p2r_20261105/ADJ_FABLE.md Q7 and D2 -- this line said "why is not
   measured: presumably the garbage-decoded slot stopped the run".  The transcript, table2/sessions_D12_else_ra/T_ra.txt, shows ONE
   halt report, `memory READ: from non-existant paddr=0xfec00208 len=4 pc=0xfec00208`.  The decoded word was the stale ib buffer,
   the subfic word from the previous read, so the 128 read-ahead slots from 0xfec00008 to 0xfec00204 ran harmlessly -- the
   transcript's r24 is 0x00000e00, the value table2/sessions_base/T_ra.txt shows on the fix -- and the real fetch at 0xfec00208
   failed and took arm (c)), and pc moved instead. The count matched by coincidence; the row set was predicted wrong.

4. **B1_exit_head** (repair-pass-2 adjudication, Q15) -- the line lists `again session` twice, inside `again: session text prompt
   pc srr0` and again on its own.  The predicted score counts it once (23 rows red -> 33/56), and table 2 measured 33/56.

Every other variant reddened exactly the rows PRETABLE_2 named, including V7 (15 rows), D15 (5), W7 (T_ra_nonex alone) and the HEAD leg
and B1 (33/56 each).
