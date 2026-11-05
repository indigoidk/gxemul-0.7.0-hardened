# Gemini 4 Argon -- job `p9_qhs_r2`, banked 2026-11-05 10:58Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p9_qhs_r2/gemini_web.out (mtime 2026-11-05 04:49:01 local, 2223 bytes)
* sender verdict line: GWEBP9QHSR: 5 ATTACKS 0 BROKEN 5 HOLDS 0 UNSETTLED DRAFTABLE:YES

---

VERDICT: CLOSE. Zero breaches, zero false records, denominator 153.

1. **VERIFY THE CLOSURE:** The arm-(a) read-ahead class is closed. The 8 alignment/MSR cells now uniformly pin all 9 channels the block writes on that path: `session`, `pc`, `nonex`, `msr`, `addr`, `stopped`, `chkstop`, `srr0`, and `unimpl`. This was achieved because repair 7b added `addr` and `stopped` to `T ra me` (3:Repair 7b, Step 1), and repair 8 added `unimpl` to all eight read-ahead sessions (3:Repair 8). No in-bound single edit escapes; the stated disclosures successfully cover the unreachable paths. The reachability arguments hold against the measured evidence: G1 (translator reads don't raise exceptions on pages with host memory, 3:G1), G2 (no pmppc session reaches arm d, 3:G2), and G3 (read-ahead failing with running=1 requires a device to decline a fetch, which is measured absent on pmppc, 3:G3). The denominator is safely 153.

2. **THE VISIT COUNT:** No state the block writes is still able to change and change back unseen. Because `T cont`, `T step`, `T me`, and `again` cover the 00 alignment, and `T blr o1`, `T blr o2`, and `T blr` cover 01, 10, and 11 respectively, every low-bit pattern now has a strict ONE-ENTRY failure session. The breakpoint active in the `T blr` sessions successfully suppresses read-ahead (1b:1939), meaning the block is entered exactly once. Therefore, any parity-dependent toggle triggered by the failure block will leave a permanent visible residue in the machine state, caught by the corresponding 1-entry session (3:Repair 9). 

3. **THE DIFF:** Each new row catches exactly what its inline note claims. `T blr o1 msr` successfully catches the `R9_tog_me1` mutation (an MSR toggle at 01), and `T blr o2 msr` successfully catches the `R9_tog_me2` mutation (an MSR toggle at 10), as proven by their 152/153 scores (4d:VERDICT). The correction to R1 regarding the `bad:` transfer returning silently on read-ahead matches the code (1b:1990-1991). No sentence of the new records is false against the measurements in sections 1-4.

4. **VERDICT:** CLOSE (zero breaches, zero false records, with the denominator 153).

P-GWEBP9QHSR-7bc2
GWEBP9QHSR: 5 ATTACKS 0 BROKEN 5 HOLDS 0 UNSETTLED DRAFTABLE:YES