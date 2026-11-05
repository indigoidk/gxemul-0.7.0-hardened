# mvme187memcoob sanitizer legs -- predictions, written BEFORE asan_memc.sh runs (this file's mtime precedes SCORES.txt's)

The reconciliation's R1 (-O3, address + undefined -- build-asan's flags) and R2 (-O0, address only, the device object):

| leg | predicted `asan reports` | predicted RESULT | why |
|---|---|---|---|
| O3_fix  | 0  | 56/56 | no indexed read remains |
| O0_fix  | 0  | 56/56 | same |
| O3_B3   | >0 | below 56 | B3 reinstates the indexed read before the switch, and the fix's default arm forwards odata: the +0xff loads read past the 132-byte struct (memcreg 124 bytes + the two latches) -- a live heap over-read |
| O0_B3   | >0 | below 56 | same, unoptimised |
| O3_HEAD | 0  | 27/56 (HEAD's plain score) | the reconciliation: "no AddressSanitizer report on the old build at -O3" -- HEAD's exiting arms never use the value, so the compiler may drop the read |
| O0_HEAD | >0 | below 56 | at -O0 the read before the switch runs for every access, +0x7c included (HEAD's struct is 124 bytes) |

A prediction that fails is reported as such, not refitted.
