# Gemini 4 Argon -- job `p7_qhs_r2` (a LATE answer: the pass-7 replication answered on a later re-send), banked 2026-11-05 10:32Z

* source: _scratchpad/gweb/jobs_20261105_rounds/p7_qhs_r2/gemini_web.out (mtime 2026-11-05 04:12:35 local, 2286 bytes); sender verdict line: GWEBP7QHSR: 4 ATTACKS 0 BROKEN 4 HOLDS 0 UNSETTLED

---

1. VERDICT FIRST: CLOSE (denominator 129).

1. VERIFY THE CLOSURE:
The arm-(a) read-ahead class is correctly closed. The grid consists of exactly 8 cells (pc low bits {00, 01, 10, 11} crossed with MSR[ME] {clear, set}). With repair 7b, each of the 8 cells now pins all 8 channels (session, pc, nonex, addr, stopped, msr, chkstop, srr0). There are no in-bound single edits to the failure block left green that are not among the variants or the disclosures. The reachability arguments for the disclosures are fully supported:
- **G1**: Arm (b) is taken only when the translator's own read raises an exception, which does not happen on pmppc because the generic dispatch lookup delivers the exception before the translator runs.
- **G2**: Arm (d) is never reached on pmppc because no device declines an instruction fetch while running (measured absent).
- **G3**: Arm (a) is reached via read-ahead failures which are `-T` halts, meaning `memory.c` has already cleared `cpu->running`. Thus, `&& !cpu->running` is trivially true and indistinguishable from the baseline.
- **SRR1**: Arm (d) is unreached, so SRR1 cannot be modelled or tested here.
The closure is mathematically complete and verified. The denominator is 129.

2. THE FAILURE-TEST NARROWINGS:
The non-deterministic rows caused by the failure-test narrowings (which decode the uninitialised fetch buffer `ib` when they skip the block) are an acceptable discharge today. Section 0 and Section 3 explicitly note that the buffer's zero-initialisation is already a "filed queue item". Because the work to initialize the buffer is tracked elsewhere, it does not need to be owed or deterministically rowed in this specific diff. 

3. THE DIFF:
Each new row correctly catches what its note claims, perfectly matching the table 8 measurements. For example, `R7b_a_srr0un` is caught exactly by the 6 new unaligned `srr0` rows, and `R7b_a_chkun` is caught exactly by the 6 new unaligned `chkstop` rows. The parity edits (`addr` and `stopped` for `T ra me`) also correctly reflect the measured gaps. There are no false records or statements against the measurements in sections 1-4.

4. VERDICT:
CLOSE. Zero breaches, zero false records. Denominator: 129.

P-GWEBP7QHSR-8562
GWEBP7QHSR: 4 ATTACKS 0 BROKEN 4 HOLDS 0 UNSETTLED DRAFTABLE:YES