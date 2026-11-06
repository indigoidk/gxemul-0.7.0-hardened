# fbsdrampair pass 2 -- the three coverage-record repairs (R1-R3 of codex_codex_fbs_p2.txt), text only

Each claim was checked against table1_20261105/SCORES.txt / KILLS.txt and the probe before editing, and its siblings
were grepped (probe, IMPL_NOTE, gate_arm.sh, table1_20261105/): each false claim had exactly ONE copy.

| | where | was | now | evidence |
|---|---|---|---|---|
| R1 | impl_20261105/IMPL_NOTE.md:25 | "O2 is a pin against an early return (equivalent, F2) but does kill a NONZERO declined value at +0x104" | "O2 pins zero readback against a nonzero declined value; it does not detect the equivalent early return" | d_earlyret_offset 56/56 |
| R2 | regress/footbridge_sites_probe.py:862-864 (comment) | "M and O each run one register, so a latch SHARED ... or one arm setting the other's latch is visible only here" | "a latch SHARED ... or one arm setting the other's latch reds X1" -- exclusivity dropped | d_shared_offusesmask / d_shared_maskusesoff RED=X1,B2; d_setswap_mask RED=M3,X1,B2; d_setswap_offset RED=O3,X1 |
| R3 | regress/footbridge_sites_probe.py:209-211 (docstring) | "kept after the new announce (M1/M2 or O1/O2, X1, B1-B3)" | "kept after the new announce (mask: M1/M2, X1, B1-B3; offset, DERIVED -- table 1 measured only the mask form: O1/O2, B1-B3)" | b_exitkept_mask RED=M1,M2,X1,B1,B2,B3 (the only kept-exit variant measured); for the offset form X1's expected list [mask, offset] is already complete when the exit fires, and X1 tests no survival (:868) |

Left standing: probe:839 "M1 kills the exit reinstated at +0x100 (or kept after the announce)" -- mask-specific and
measured.  PRETABLE_1.out is a frozen record and makes no R1-R3 claim (its kept-exit line is the mask variant).

**PROOF the probe edits are comment/docstring only -- AST_PROOF.txt:** the AST with every docstring removed (comments are
never in the AST) of regress/footbridge_sites_probe.py (md5 58399f14) EQUALS table1_20261105/probe56_frozen.py's
(md5 a52267ff).  Controls: raw text and module docstring differ (the edits happened); the pre-change probe and a
one-constant code change both make the comparison FAIL; a comment-only change leaves it equal.  Text diff: 2 hunks,
5 lines out, 6 in.  So table 1's measurements apply to the edited probe unchanged.

Not touched: src/ and the trees (dev_footbridge.c md5 ccaf09d4 in SEC, est/, build/), gate_arm.sh.

**FOUND, NOT FIXED (gate_arm.sh is not mine to edit):** gate_arm.sh was rewritten at 10:35:19 by another party
(md5 cbb9d843), and its footbridge block (lines 1081-1171) is now byte-identical to the PRE-fbsdrampair block.  It
pins `ROWS=37 of 37` and carries none of the six SDRAM checks, while the working-copy probe emits `ROWS=56 of 56` --
so that check reds on the next gate_arm.sh run.  The three hunks are preserved in impl_20261105/gate_arm.sh.fbs.diff
(verified in situ 29/29, impl_20261105/fbblock_check.out) and must go back in before fbsdrampair lands.
