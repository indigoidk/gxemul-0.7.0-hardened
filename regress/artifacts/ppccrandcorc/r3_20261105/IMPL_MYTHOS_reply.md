MYTHOSIMPLR575C

VERDICT: REPAIR 3 DONE. N = 70. Base run on the fix: `PPC_CRLOGIC_RESULT=70/70`, `PPC_CRLOGIC_CONTROL=OK`, sentinel last; every row green on the first run, no row re-derived (r3_20261105/base70/probe_base70.out; CLEARANCE.txt: cmp rc=0, binary-newer rc=0).

**Codex's claims, checked by simulation (v575c.py; `check66` first reproduces all 29 table-2 legs on the 66 rows).** All 54 survivors CONFIRMED (none red on the 66, all red on the 70), 0 refuted. All 35 equivalents CONFIRMED (proof plus 40000 random differential trials), 0 refuted. R2's three-row claim verified: 62 rows plus `crandc 16,16,31` over 0xfffffffe plus the two crorc pins leave exactly the same 5 cells as the four round-2 rows.

**Closure denominator: 453 cells** = codex's 447 + k=31 at the four read sites (4) and at the two set literals (2). On the 70 rows: 416 detected (56 closed by the 4 new rows), 36 EQUIVALENT (codex's 35 + crandc BA `& 0x80000001`, same proof), 1 disclosed (crandc clear-to-toggle), 0 undetected. CLOSURE3.md also proves the whole 2^32 constant space at the four read sites and both set literals, so the contract names entire sites. Left uncovered, deliberately: the equivalents, the disclosed crandc toggle, and extra CLEARs (outside the denominator; the appendix shows the whole-CR rows catch most crorc ones incidentally, no crandc one above k=10).

**Rows added (4, whole-CR compare via register dump and mfcr):** `64 crorc baread` (crorc 17,31,5 / 0xfffffffe → 0xffffbffe; B2, and every BA mask incl. 16), `64 crorc bbread` (crorc 30,30,31 / 0xfffffffc → 0xfffffffe; B1 k=2..31), `64 crandc setbits` (crandc 31,30,31 / 0x2 → 0x3; B3 k=2..31), `64 crorc setbits` (crorc 31,0,31 / 0 → 0x1; B4). Minimality argument in CLOSURE3.md.

**Records corrected:** probe in place (R1 clause (e)(3) and pin comment, R3 `& 7` gives 6, R2 probe-side: four rows not the minimum, kept as measured); r2_20261105/CLOSURE.errata.md (R2 + narrow-vocabulary note), table2/VERDICT.errata.md (R4, R5: earliest file is probe66_frozen.py 02:10:35), PRETABLE_2.errata.md (R6: CTL_CR 0x12345678); R7 in gate_575_block.new. Nothing measured was rewritten.

**Table-3 inputs (written before any table):** 51 variants (table 2's 27 cmp-identical re-creations + 24 new: B1 k=2,15,30,31; B2; B3 k=7,19,30,31; B4 k=26,27; read masks 0/2/4/6 one per site; 8 non-equivalent structural cells + the crorc swap predicted 0 red), each a one-hunk edit of GXEMUL-SEC's source; PRETABLE_3.out (real control seed, exact red sets; expectation base 70/70, HEAD 60/70, 49 red as listed, g2 and u9 green); table3_575.sh (`bash -n` clean; refuses without PRETABLE_3.out and table3/probe70_frozen.py, which the main loop copies from base70/probe70_run.py).

**Files touched:** edited regress/ppc_crlogic_probe.py; wrote r3_20261105/{v575c.py, CLOSURE3.md, CLEARANCE.txt, PRETABLE_3.out, gate_575_block.new, table3_575.sh, IMPL_NOTE.md, base70/, variants/, *.pre_r3} and the three errata beside the table-2 files. gate_ppc.sh, src/, build/ and git untouched (the gate backup now differs from the live file at line 287, the other implementer's block, above the #575 block at 331).

**Not done:** nothing in scope was skipped; the table itself is for the main loop.
