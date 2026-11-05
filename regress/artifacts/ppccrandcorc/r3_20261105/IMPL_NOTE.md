# #575 ppccrandcorc -- ROUND 3 implementation note (2026-11-05, Mythos 5.1)

The fix (src/cpus/cpu_ppc_instr.c:2735 `if (ba & !bb)`, :2762 `if (ba | !bb)`) is untouched.  This round closes the detector over
the FULL single-constant space at the sites round 2 had put in scope with a narrower vocabulary (pass 3, codex B1-B4), corrects
the seven false records R1-R7, and prepares table 3.  No table was run here (the main loop runs it); no source, build or git
action was taken; gate_ppc.sh was NOT edited (another implementer holds it): its #575 block is in gate_575_block.new.

## Codex's pass-3 findings, checked one by one (CLOSURE3.md; simulator v575c.py)

v575c.py extends r2_20261105/v575b.py (read mask = any constant; set literal; clear/set re-addressing; clear between the reads;
swapped reads) and first re-derives table 2's 29 legs on the 66 rows: `check66` matches PRETABLE_2.out on all 29, which licenses
the extension.  Then:

    codex's 54 survivors (B1 29, B2 1, B3 22, B4 2):  54 CONFIRMED (none red on the 66 rows), 0 refuted; all 54 red on the 70.
    codex's 35 equivalents:                            35 CONFIRMED (proof + 40000 random differential trials), 0 refuted.
    denominator: 453 cells = codex's 447 + k = 31 at the four read sites (4) and at the two set literals (2), in bound (same
                 constant sites, one more constant).  Partition on the 70 rows: 416 detected (360 by the 62/66 rows, 56 closed
                 by the 4 new rows), 36 EQUIVALENT (codex's 35 + crandc BA `& 0x80000001`), 1 disclosed (crandc clear -> toggle),
                 0 undetected.
    beyond the enumeration: CLOSURE3.md's PROOF section closes every 2^32 constant at the four read sites and the two set literals
                 (the enumerated families are the sampled representatives), so the contract names the whole site.
    appendix (outside the denominator, not claimed): the clear literal 1 -> 1+2^k (an extra CLEAR, disclosed (e)(5)); the new
                 whole-CR rows happen to see most crorc ones (k = 1..30) and no crandc one above k = 10.

## Rows added (4): N = 66 -> 70 (single-instruction sessions shaped like the `hi'/pin rows; each compares the WHOLE CR)

    64 crorc baread    crorc  17,31,5   seed 0xfffffffe  want CR 0xffffbffe  (B2; also every BA field mask 0..30 incl. 16: R1)
    64 crorc bbread    crorc  30,30,31  seed 0xfffffffc  want CR 0xfffffffe  (B1, k = 2..31)
    64 crandc setbits  crandc 31,30,31  seed 0x00000002  want CR 0x00000003  (B3, k = 2..31; k = 1 is red on `64 crandc 01')
    64 crorc setbits   crorc  31,0,31   seed 0x00000000  want CR 0x00000001  (B4, every k)

`cr_row` reads the CR from the register dump and from mfcr r10 and reports a disagreement as the got value.  Why 4 and no fewer:
CLOSURE3.md, "WHY FOUR AND NO FEWER" (the four families need pairwise incompatible seeds/results in one instruction).

## Base run (base70/probe_base70.out, build/gxemul; CLEARANCE.txt: cmp identical, binary newer than source)

    PPC_CRLOGIC_RESULT=70/70
    PPC_CRLOGIC_CONTROL=OK
    PPC_CRLOGIC_PROBE_DONE          (elapsed 0.3s; 70 rows ok, 0 FAIL; row order == v575c.py `names`)

No row was red on the fix, so no row was re-derived; no want was fitted to the binary (the four wants are the architectural CRs).

## Records corrected (each quotes what it corrects)

- probe (in place): R1 -- clause (e)(3) and the pin-block comment: `64 crorc bamask' has CR[16] = 0 (its EQUAL pre-set), so mask
  16 is not flipped there (red on `64 crorc 11'; now also on `64 crorc baread', uniform 0xfffffffe).  R3 -- the `64 crandc bbmask'
  comment: `& 3' gives bb = 2, `& 7' gives bb = 6.  R2 (probe side) -- "(BT == BA is a fixed point ...)" holds for an INVERSE pre-set
  only; crandc 16,16,31 over 0xfffffffe would have closed both crandc needs; the four round-2 rows are NOT the minimum and are kept
  as measured.  Clause (e) gains the ROUND 3 paragraph (the contract: covered / deliberately uncovered cells) and (5) is reworded
  for the whole-CR rows.
- r2_20261105/CLOSURE.errata.md: R2 ("WHY THESE FOUR AND NO FEWER"; the three-row design verified by simulation to leave the same
  5 cells) and the vocabulary-narrower-than-the-class note.
- r2_20261105/table2/VERDICT.errata.md: R4 (m5-m9 single-bit, m10 removes three bits), R5 (earliest file: probe66_frozen.py
  02:10:35.403, then cpu_ppc_instr.c.fix575, then MD5.txt; PRETABLE_2 still predates all).
- r2_20261105/PRETABLE_2.errata.md: R6 (the control seed is CTL_CR 0x12345678; the manifest printed the simulator's placeholder 0;
  no prediction depends on it).
- gate_575_block.new: R7 ("every destination pre-set to the INVERSE" -> the truth-table/edge/hi rows inverse, two round-2 rows
  EQUAL, four round-3 rows whole-CR), RESULT=70/70, rows run/green 70, header "70-row", the names list = the base run's 70 names in
  order (one line), the comment's counts (239 / 453 cells, 56 escaped the 66, 0 escape the 70).  Taken from the CURRENT gate block
  (gate lines 331-361 at the time of writing) and changed only there; `bash -n` clean.
- PRETABLE_2.out, SCORES.txt, VERDICT.md, CLOSURE.md: not rewritten.

## Table-3 inputs (written BEFORE any table; the main loop runs the table)

- variants/*.c: 51 = table 2's 27 re-created (cmp-identical to r2_20261105/variants/) + 24 round-3 representatives, each one exact
  edit of GXEMUL-SEC/src/cpus/cpu_ppc_instr.c (one changed statement; u7/u8 move one statement; c_identity is table 1's two-handler
  edit): r1-r4 crorc BB read `& 0x5`, `& 0x8001`, `& 0x40000001`, `& 0x80000001u` (B1 at k = 2, 15, 30 and k = 31); r5 crorc BA
  `& 0x8001` (B2); x1-x4 crandc set literal 0x81u, 0x80001u, 0x40000001u, 0x80000001u (B3 at k = 7, 19, 30 and k = 31); x5-x6
  crorc set literal 0x04000001u, 0x08000001u (B4); z0/z2/z4/z6 the read masks & 0, 2, 4, 6 (one per site); u1-u8 the non-equivalent
  structural families (clear/set re-addressed to (31-ba), (31-bb), bt; the clear between the reads); u9 crorc reads swapped
  (predicted 0 red = EQUIVALENT, like g2).
- PRETABLE_3.out: the 70-row manifest with the REAL control seed 0x12345678 and, per variant, the EXACT red set v575c.py computes;
  the four R5 bt-substitutions PREDICTED ONLY (4, 5, 6, 4 red).  Expectation: base 70/70; HEAD 60/70 (the same ten DISC rows);
  49 variants red exactly as listed; g2 and u9 0 red.
- table3_575.sh: table2_575.sh adapted (clone /tmp/gx575t3, clone-local .MUTANT first, refuses without PRETABLE_3.out and the
  frozen probe table3/probe70_frozen.py -- copy base70/probe70_run.py there; it must be cmp-identical to the in-tree probe -- restore
  = cp from GXEMUL-SEC + cmp + rebuild + `[ gxemul -nt source ]` before the sentinel goes; "[70 rows]" in SCORES.txt); `bash -n` clean.

## Files touched

    edited:  regress/ppc_crlogic_probe.py (docstring clause (e); pin-block comments; +cr_row and 4 rows)
    written: r3_20261105/{ppc_crlogic_probe.py.pre_r3, gate_ppc.sh.pre_r3, v575c.py, CLOSURE3.md, CLEARANCE.txt, PRETABLE_3.out,
             gate_575_block.new, table3_575.sh, IMPL_NOTE.md, base70/probe70_run.py, base70/probe_base70.out, variants/*.c (51)}
             r2_20261105/{CLOSURE.errata.md, PRETABLE_2.errata.md, table2/VERDICT.errata.md}
    not touched: regress/gate_ppc.sh, src/, build/, git.
