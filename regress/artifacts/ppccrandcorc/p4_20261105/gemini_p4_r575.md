# Gemini 4 Argon (gemini web proxy) -- job `p4_r575`, banked by the main loop at 2026-11-05 09:03Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p4_r575/gemini_web.out (mtime 2026-11-05 03:02:47 local, 4722 bytes)
* sender verdict line: (none -- the answer did not end in the requested line, so the sender scored it exit 1; it is a reading, read in full: its first line says CLOSE)

---

VERDICT: CLOSE. The single-constant closure over 453 cells is sound, the four new test rows are mutually irredundant, and the whole-CR assertions leave host state untouched while strictly tightening the testing bounds.

**Defensive Review & Refutation Attempts:**

*   **Claim (`2a:293`):** "The BA read shifts by 0, so `a = CR & m`: every mask `m` with ANY bit 1..31 set reads nonzero".
    *   *Refutation attempt:* If `BT=17` and `BA=31`, the bitwise shift in the C implementation (`cpu_ppc_instr.c:2759`) is `31 - ba = 31 - 31 = 0`. The read is indeed `(cr >> 0) & m`. The seed is `0xFFFFFFFE`. Because PowerPC CR bit 0 is the MSB (`1b:244`), a seed of `0xFFFFFFFE` has a 0 at bit 31 (LSB) and 1s everywhere else (bits 0..30). Any bit index from 1 to 31 in the standard integer representation corresponds to CR bits 0..30, which are all 1s. The claim cannot be refuted; it correctly evaluates to non-zero. 

*   **Claim (`2a:296`):** "The BB read shifts by 0: every mask `m` with any bit 2..31 set reads nonzero, `!bb = 0, 0`... bit 1 = `CR[30] = 0` here".
    *   *Refutation attempt:* The seed for `bbread` is `0xFFFFFFFC`. The two LSBs of this integer are 0, meaning CR bits 30 and 31 are 0. Standard integer bits 2..31 correspond to CR bits 0..29, which are all 1s. Therefore, a mask checking bit 1 (like `& 3`) hits a 0 and reads 0, but a mask with bits in 2..31 hits a 1, making `bb != 0`, and `!bb = 0`. This flips the `crorc` result from 1 to 0, correctly turning the test row red. The logic is impenetrable.

*   **Claim (`2a:297-298`):** "the set shifts by 0, so a literal `1+2^k` also sets `CR[31-k]`: zero in the seed for `k = 2..31`... `k = 1` lands on `CR[30]=1`, the source, and is red on `64 crandc 01`".
    *   *Refutation attempt:* In `64 crandc setbits`, `BT=31`, so the set shift is `31 - 31 = 0`. A set literal of `1 + (1<<k)` will apply `cr |= 1 | (1<<k)`. The seed `0x00000002` only has bit 1 set (CR bit 30). For any `k >= 2`, `(1<<k)` sets a bit that is currently 0 in the seed, polluting the whole-CR result (`want_cr=0x00000003`) and triggering a failure. For `k=1`, it sets bit 1, which is already 1, evading detection on this row. However, `64 crandc 01` checks `crandc 9,0,1`. Its set shift is `31 - 9 = 22`. `(1<<1) << 22 = 1<<23`. This alters bit 8 in the CR, which fails the `01` row's exact match. The claim is completely airtight.

*   **Claim (`2d:361`):** "With an EQUAL pre-set, the single row `crandc 16,16,31 over 0xfffffffe, want 1` sees the clear moved before the reads... every BB field mask 0..30... BB <- BT and the BB read masks... three rows, not four, was the minimum."
    *   *Refutation attempt:* If the `crandc` result is supposed to be 1 (`want 1`), pre-setting CR[16] to 1 (EQUAL) implies `a=1`. If the clear operation occurs *before* the reads, `a` becomes 0 before being evaluated, meaning `0 & !0 = 0`, yielding 0 instead of 1. This exposes the order-of-operations defect instantly without requiring the inverse pre-set setup previously claimed. The historical correction in the errata is strictly accurate.

*   **Claim (`3:455-460`):** "WHY FOUR AND NO FEWER... (ii) needs ones where (iv) needs zeros (the extra set bits of (iv) at BT-26, BT-27 lie in 0..5 for any BT, inside (ii)'s ones at 0..29..."
    *   *Refutation attempt:* To satisfy (ii), `CR[0..29]` must be 1. To satisfy (iv) with `BT=31`, the target bits are `31-26=5` and `31-27=4`. These bits fall cleanly inside the `0..29` range. A single seed cannot simultaneously have 1s at indices 4/5 (for ii) and 0s at indices 4/5 (for iv). Combining them is mathematically impossible. 

*   **State Preservation & Side Effects (`2a:286`):** 
    *   *Refutation attempt:* The newly introduced `cr_row` executes `MFCR(10)`. Moving the CR into guest `r10` mutates the guest register state. However, this execution occurs strictly within `session()`, which spins up an ephemeral bare-metal guest environment. Once the row completes, the state is discarded. At no point is the host emulator process's memory corrupted or improperly persisted, meaning the test instrumentation acts defensively without side effects on the `GXemul` runtime itself. 

*   **UNSETTLED Claims:**
    *   The claim in Section 0 (`0:154`) that "all 53 predicted lines exact, 0 misses" for Table 3 cannot be settled. Section 4a truncates the list of variants after `m1_crandc_mask`, meaning the full 53 variants are not enumerated in this packet. Resolving this requires inspecting the full `PRETABLE_3.out` file to verify the 53 exact variant names and red counts.

P-GWEBP4RFIVE-f013
The repair is robust, strictly bounds the problem space, and correctly expands the test oracle without modifying the emulator's runtime behavior.