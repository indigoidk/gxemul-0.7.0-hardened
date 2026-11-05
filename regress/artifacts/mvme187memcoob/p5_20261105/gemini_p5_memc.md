# Gemini 4 Argon -- job `p5_memc`, banked 2026-11-05 10:47Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p5_memc/gemini_web.out (mtime 2026-11-05 04:35:45 local, 1923 bytes)
* sender verdict line: GWEBP5MEMC: 4 ATTACKS 0 BROKEN 4 HOLDS 0 UNSETTLED DRAFTABLE:YES

---

VERDICT: CLOSE. Zero floor breaches, zero false records, with the denominator.

1. **THE FLOOR QUESTION**: All 517 survivor groups, plus NB3 and NB4, are clause-(e) coverage debt, not FLOOR cells. 
*Why*: The project's floor rule restricts row debts to the "cross-product of the guard's dominating predicates with the device-STATE lvalues the fix's own repair path reads that are JOINTLY REACHABLE". An INSERTED statement that introduces a new gate (e.g., mixing `M` and `D`, or `controller` at the memconf latch body where the guarded body does not branch on it) exceeds the DEPENDS-ON bound. Because the guarded body's own code does not distinguish these artificial joint partitions, they fall outside the floor bound and are correctly classed as clause-(e) coverage debt.

2. **NB4**: The `&=` keep under `!controller` into `chiprev` and `memconf` is a literal NOCHANGE.
*Why*: As Section 6 (Item 11) notes, every controller-0 first memconf store writes `0x07`, `0xff`, or `0xffffffff`. Because the emulator only models the low bits (bit 0 for `chiprev`, bits 0-2 for `memconf`), these bits in the stored value are all `1`. A bitwise AND with `1` leaves the state perfectly unmodified (`X & 1 == X`). It is not an unobserved change; no state transition occurred at all.

3. **THE DIFF**: Yes, each new row catches what its note claims. 
*Check*: For example, R16's `ST_B(0,3,0x100)` storing `0` to `chipid` followed by `LD_BU` correctly expects `0x80`, as `chipid` ignores writes (1:95-97). R16's notice fragment `"memconf write 0x7 (controller 0) ignored, not modelled (once) ]"` perfectly matches the `fatal` template at 1:113-115 with `idata` = `0x07`. The records correctly document the test bounds and no sentence in the new records is false.

4. **VERDICT**: CLOSE. Zero floor breaches exist under the project's DEPENDS-ON bounds.

P-GWEBP5MEMC-4f8a
GWEBP5MEMC: 4 ATTACKS 0 BROKEN 4 HOLDS 0 UNSETTLED DRAFTABLE:YES