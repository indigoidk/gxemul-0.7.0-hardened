# Gemini 4 Argon (gemini web proxy) -- job `p6_qhs`, banked by the main loop at 2026-11-05 08:54Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p6_qhs/gemini_web.out (mtime 2026-11-05 02:23:12 local, 2531 bytes)
* sender verdict line: GWEBP6QHS: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO
* NOTE: the sender RE-SENDS a job whose answer lacked a verdict line and OVERWRITES its .out, so this file is the
  answer on disk at banking time; an earlier answer to the same job, if any, survives only where a disposition quotes it.

---

VERDICT: REPAIR (A floor breach exists, and the docstring contains a mathematically false statement about the failure counts).

1. **FLOOR on the composite:** 
   - **Edit:** In arm (b), mutating the aligned compare `if ((cpu->pc & ~(uint64_t)3) != addr)` to `if (cpu->pc < addr)`. (Alternatively, in arm (d), mutating `if (cpu->cd.ppc.msr & PPC_MSR_ME)` to `if (cpu->cd.ppc.msr)` also survives).
   - **Derivation:** For the measured `isi` and `isi1` sessions, `pc` is moved to a low exception vector (`0x400`) and `addr` is the high instruction address (`0x2000`); since `0x400 < 0x2000` is true, the mutation correctly takes arm (b), matching the fix. For `T blr`, `pc` is `0x02040007` and `addr` is `0x02040004`, making `pc < addr` false, which correctly skips arm (b) and parks in (c). For `T ra odd` (real fetch), `pc` is `0xfec00009` and `addr` is `0xfec00008`, which is also false. For standard fetching sessions (like `T cont`), `pc == addr`, so `<` is predictably false. Every single row executes identically to the fix. 
   - **Row:** All 82 rows remain green (e.g., `isi pc`, `T blr nonex`, and `T ra odd nonex` all stay green).
   - **DENOMINATOR:** 4 predicates swept (the guards for arms a, b, c, and d) × 13 distinct test shapes (`ctl`, `neg`, `isi`, `isi1`, `noT`, `T cont`, `T step`, `again`, `T me`, `T ra`, `T ra me`, `T blr`, `T ra odd`).

2. **THE DIFF:**
   - **Do new rows catch what notes claim?** Yes. `T ra odd` catches the conjoined guards (`R6_a_pceq` and `R6_a_align` explicitly turn `T_ra_odd_nonex` red). `T blr` re-seeded to `0x02040007` successfully catches the widened mask (`R6_mask7` turns `T_blr_nonex` red).
   - **Is any sentence false?** YES. In the docstring (Section 2b), the sentence *"On this 82-row probe the pre-fix build scores 40 of the 82 rows with the symptom PRESENT"* is FALSE. A score of `40/82` means 40 rows are *GREEN* (symptom absent). As shown in PRETABLE_6 (`42 red -> 40/82`) and the list of red rows in SCORES.txt, there are **42** rows with the symptom PRESENT, not 40.
   - **Is the 'at least' wording honestly recorded?** Yes. VERDICT.md (Section 4c) is perfectly transparent, explicitly stating: *"that wording was WRONG for two build-dependent variants (the claim the probe makes for them is 'some row reds', which holds)."*

3. **VERDICT:** REPAIR. The floor breach (`<` operator in arm b) needs a row or a disclosure, and the docstring's count of red rows must be corrected to 42.

P-GWEBP6QHS-2ad4
GWEBP6QHS: 4 ATTACKS 2 BROKEN 2 HOLDS 0 UNSETTLED DRAFTABLE:NO