# Gemini 4 Argon -- job `p5_qhs`, banked at the qhslowifetch landing (the landing kit's bank_qhs.py)

* source: _scratchpad/gweb/jobs_20261105_rounds_retired/p5_qhs/gemini_web.out (mtime 2026-11-05 01:43:42 local, 2982 bytes)
* sender verdict line: GWEBP5QHS: 3 ATTACKS 1 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO
* the pass-5 record (p5_20261105/) cites this send by job name and did not bank it; banked here so no record of the round points at the scratch pad for it.

---

**VERDICT:** REPAIR. The product change and documentation are correct, and no `-T` session is owed, but the composite floor bound contains an untested gap where a wider mask (e.g., `~7`) would survive all 79 rows without turning red.

**1. THE NO -T SESSION:**
No `-T` session is owed. Section 3 measures the premise and proves that without `-T`, `memory_rw` does not fail but instead zero-fills and succeeds. The zero word decodes as unimplemented and the run stops. Because no arm of the failure block is reached or executed during a no `-T` run, a no `-T` row would not evaluate the modified code in arm (b) and could not red any variant of the fix. The disposition to omit it HOLDS.

**2. FLOOR ON THE COMPOSITE:**
There is a FLOOR BREACH. 
*   **Predicate:** `(cpu->pc & ~(uint64_t)3) != addr`
*   **Edit (Shape):** Substitute the mask with `~(uint64_t)7` (masking out the lower 3 bits instead of 2).
*   **Derivation:** For the unaligned `T blr` session, `pc` is `0x02040003` and `addr` is `0x02040000`. Evaluating `0x02040003 & ~7` yields `0x02040000`, which equals `addr`; the test is false, falling through to park in arm (c) just like the fix. For all other measured sessions (e.g., `T step`, `T ra`), `pc` and `addr` are identical, and every failing address used in the test suite has bit 2 clear (`0x2000`, `0x02040000`, `0xfec00008`). Therefore, masking bit 2 leaves them equal to `addr`, evaluating to false and behaving exactly like the fix.
*   **Row:** All 79 rows remain green. This mask widening is not tested (only narrowing via `R5_mask1` and `R5_mask2` are in table 5) and would break the logic for legitimate exceptions at addresses ending in 4 or C, which are currently unmeasured. 
*   **Denominator:** 1 predicate (arm (b)'s condition) x 1 shape (wider alignment mask substitution). This item is BROKEN.

**3. THE DIFF:**
*   **Product change:** The change is correct. The aligned compare evaluates to false for all aligned fetches (since `pc == addr`), leaving their routes entirely unchanged, while successfully intercepting the unaligned `T blr` pc so it skips arm (b) and parks in arm (c).
*   **Comments and Rows:** Arm (b)'s new comment accurately describes the unmasked copy behavior of `mtlr`/`bclr` and the `-T` flood it caused. Each new row catches what it claims (e.g., `T blr nonex` verifies the slot isn't re-run by confirming only 1 halt report; `T blr lr` confirms the unmasked stored value). Every added sentence in the docstring and gate comment is demonstrably true against sections 1-4.
*   **Disclosure:** `R5_arun`'s disclosure is the correct disposition. Because no measured pmppc window ends in a branch, the subsequent real fetch immediately triggers a second halt that clears `running` again, perfectly masking the early restore in arm (a). These items HOLD.

**4. VERDICT:**
REPAIR. (Zero false records, but one floor breach identified on the mask).

P-GWEBP5QHS-13da
GWEBP5QHS: 3 ATTACKS 1 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO