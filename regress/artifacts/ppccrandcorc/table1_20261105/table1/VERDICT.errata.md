# VERDICT.errata.md -- correction to VERDICT.md (#575 ppccrandcorc, table 1), dated 2026-11-05 (round 2)

VERDICT.md is a historical record and is NOT rewritten.  The correction comes from pass 2 (p2_20261105/codex_codex_r575_p2.txt F6)
and was checked against adj_p1_20261105/MYTHOS_local.md (the R5 table) and SCORES.txt.

## F6 -- "the four the ruling listed per variant"

VERDICT.md lines 12-13 say: "d1-d6 (operand complement moved, dropped, operator crossed) -- 5 each, the four the ruling listed
per variant plus a hi row on d1-d4".

Correction: the pass-1 ruling's R5 table did not list four rows for every d variant.  It listed FOUR for d1-d4 (64/32 crandc 01, 10;
64/32 crorc 01, 10; 64/32 crandc 10, 11; 64/32 crorc 00, 01) and FIVE for d5 and d6 (64/32 crandc 00, 11 plus edge crandc bt0;
64/32 crorc 00, 11 plus edge crorc bt31).  The measured 5-each (SCORES.txt lines 9-14) therefore decomposes as:

    d1-d4: the ruling's four rows plus that handler's `hi` row (the ruling wrote the table before the hi rows existed, and its
           parenthetical "the owed rows stay green under all nine" is false for c and d1-d4 -- SCORES.txt lines 8-12);
    d5-d6: the ruling's five rows, unchanged (the hi rows stay green: (1,0) and (0,1) are not fixed points of the crossed
           operator for the 00/11 cells, but the hi inputs (1,0) -> 1|!0 = 1 and (0,1) -> 0&!1 = 0 equal the wants).

Nothing else in VERDICT.md changes: 15 of 15 variants red, 17 of 17 legs exactly as predicted, the null-media and HEAD lines stand.
