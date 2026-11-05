# mvme187memcoob sanitizer legs -- the reading (run 2; run 1 was confounded by LeakSanitizer, see run1_leaks/README.md)

Measured (SCORES.txt), against PREDICTION_asan.md (written before run 1, so before run 2):

| leg | predicted | measured | |
|---|---|---|---|
| O3_fix  | 0 reports, 56/56 | 0, 56/56 | as predicted |
| O0_fix  | 0 reports, 56/56 | 0, 56/56 | as predicted |
| O3_HEAD | 0 reports, 27/56 | 0, 27/56 | as predicted -- the reconciliation's "no AddressSanitizer report on the old build at -O3" confirmed |
| O0_HEAD | >0 reports | 4 (sessions rd 0x7c and rd 0xff), 26/56 | as predicted -- R2 catches HEAD's indexed read (the reconciliation's A1) |
| O3_B3   | >0 reports | **0**, 55/56 (R3 7c r4 only) | **prediction failed** |
| O0_B3   | >0 reports | **0**, 55/56 (R3 7c r4 only) | **prediction failed** |

**Why B3 is invisible to the sanitizer, and why that is a layout fact, not a sanitizer bug.**  B3 reinstates the indexed read before the
switch, and the fix's default arm forwards odata, so the +0xff loads return a byte 123 past the end of `struct mvme187_data` -- which the
fix grew from 124 bytes (memcreg alone) to 132 (two int latches).  AddressSanitizer reports an access that lands in a poisoned red zone; a
read that far past a 132-byte chunk lands beyond it, in memory the sanitizer does not poison.  HEAD's 124-byte struct put the same offsets
inside the red zone, which is why O0_HEAD reports and O0_B3 does not.  **So the sanitizer row's catch is layout-dependent**: R1 (-O3)
catches nothing on the shipped layout, and R2 (-O0) catches HEAD's read but not B3's.

**B3 is still caught**, on every build: `R3 7c r4` reads +0x7c after a memconf store, and B3's over-read returns the first byte of
`warned_memconf` (1) where the fix returns 0 (table1/SCORES.txt, B3_idx_read: RED=R3_7c_r4; here, both B3 legs: the same single red).
That row is itself layout-dependent -- it relies on the latch sitting at offset 124 -- which the probe's contract must say.

**The reconciliation's R1 "Catches A2 (measured RED in D)"** was measured on a different struct layout (before the latches); on the
shipped layout R1 does not catch B3.  Recorded for the adjudication, not corrected silently.
