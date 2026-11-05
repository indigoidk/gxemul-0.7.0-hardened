# Gemini 4 Argon (gemini web proxy) -- job `p6_qhs_r2`, banked by the main loop at 2026-11-05 08:54Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p6_qhs_r2/gemini_web.out (mtime 2026-11-05 02:53:00 local, 2164 bytes)
* sender verdict line: GWEBP6QHSR: 5 ATTACKS 0 BROKEN 5 HOLDS 0 UNSETTLED DRAFTABLE:YES
* NOTE: the sender RE-SENDS a job whose answer lacked a verdict line and OVERWRITES its .out, so this file is the
  answer on disk at banking time; an earlier answer to the same job, if any, survives only where a disposition quotes it.

---

VERDICT: CLOSE (zero breaches, zero false records, with the denominator: 2 predicates x 8 shapes swept).

1. **FLOOR on the composite:** Zero floor breaches found. I swept the predicates dominating the failure block's edited lines (arm (a)'s read-ahead guard and arm (b)'s alignment test) against the shapes measured by the 82-row probe. For arm (a), any weakening of `if (cpu->translation_readahead)` is either caught by the non-read-ahead rows or disclosed as unmeasured at deeper read-ahead levels. For arm (b), `if ((cpu->pc & ~(uint64_t)3) != addr)`, any widening of the mask past bits 0-1 is now caught by `T blr` (which tests bit 2 via `0x02040007`) and `T ra odd` (which tests the unmasked/conjoined forms via `0xfec00005`). Any mutation of the return/goto logic is caught by the probe (e.g., `W2`, `W3`, `B1`). No single edit inside the bound keeps all 82 rows green without falling into the documented green/disclosed classes (e.g., `R5_cb`, `R5_arun`). Denominator: 2 predicates (read-ahead, pc/addr alignment) x 8 shapes swept (normal, -T, read-ahead, unaligned pc, ME clear/set, ISI route, machine check).

2. **THE DIFF:** Each new and re-seeded row catches what its note claims. 
- `RA_ODD = 0xfec00005` correctly reaches the failure block with `pc != addr` and tests arm (a)'s unaligned behavior, catching `R6_a_pceq` and `R6_a_align`.
- `BLR_PC = 0x02040007` correctly re-seeds `T blr` to set bits 0-2, ensuring that a mask widened to bit 2 (`& ~7`) or bits 2-3 (`& ~15`) fails to match `addr = 0x02040004`, successfully catching `R6_mask7` and `R6_mask15`.
- No sentence added to the docstring or gate comment is false against sections 1-4. The updates to the docstring accurately reflect the introduction of `T ra odd` and the re-seeding of `T blr`.
- The 'at least' wording `PRETABLE_6` used for `W5` and `D7` is recorded honestly in section 4c (`VERDICT.md`), which openly acknowledges that the wording was wrong for build-dependent variants but confirms the underlying claim ("some row reds") held.

3. **VERDICT:** CLOSE. Zero breaches, zero false records.

P-GWEBP6QHSR-9cd2

GWEBP6QHSR: 5 ATTACKS 0 BROKEN 5 HOLDS 0 UNSETTLED DRAFTABLE:YES