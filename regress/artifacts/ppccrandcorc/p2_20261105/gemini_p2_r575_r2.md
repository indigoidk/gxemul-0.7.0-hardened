# Gemini 4 Argon (gemini web proxy) -- job `p2_r575_r2`, banked at the #575 landing (kit built 2026-11-05)

* source: _scratchpad/gweb/jobs_20261105_rounds/p2_r575_r2/gemini_web.out (mtime 2026-11-05 01:42:52 local, 1321 bytes, md5 e6eab2f87c06ba6b0f4f9ee3eac48266)
* sender verdict line: GWEBP2RFIVER: 6 ATTACKS 2 BROKEN 4 HOLDS 0 UNSETTLED DRAFTABLE:NO (sender: exit 0)
* NOTE: the sender RE-SENDS a job whose answer lacked a verdict line and OVERWRITES its .out, so this file is the
  answer on disk at banking time; an earlier answer to the same job, if any, survives only where a disposition quotes it.

---
1. **FLOOR on the composite:** Edit `X(crandc)` line 2732 to drop the bitmask: `ba = (cpu->cd.ppc.cr >> (31-ba));`. This is an undetectable logic equivalent because the subsequent condition `if (ba & !bb)` inherently isolates the least significant bit of `ba` (since `!bb` reduces strictly to `0` or `1`). Any higher-order bits present in an unmasked `ba` are annihilated by the bitwise AND, leaving the boolean truth value completely unchanged. This keeps all 62 rows green and bypasses all variants. Denominator: 10 sites (2 reads, 1 clear, 1 condition, 1 set across 2 handlers) × multiple edit shapes.
2. **THE DIFF:** The product lines are exactly correct against Book I. However, the record sentence `(3) ... an input at index 0 or 31 is not separately rowed` is **FALSE**. The new `64 crandc hi` row explicitly uses `BA=31`, meaning an input at index 31 *is* separately rowed. 
3. **MISSING:** Initial logic and parameters are validated. Standard processing applied. The pass-1 ruling R9 ("Correct the three §3 premises in the brief") is absent from the diff, but the diff only encompasses source files, meaning no source-level requirement was missed.
4. **VERDICT:** REPAIR (Floor breach identified, false record identified).

P-GWEBP2RFIVER-0cd0
GWEBP2RFIVER: 6 ATTACKS 2 BROKEN 4 HOLDS 0 UNSETTLED DRAFTABLE:NO
