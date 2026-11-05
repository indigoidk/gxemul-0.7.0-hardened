# #575 ppccrandcorc -- CLASS CLOSURE BY SIMULATION, ROUND 3 (2026-11-05)

Simulator: r3_20261105/v575c.py (r2_20261105/v575b.py extended; `v575c.py check66' re-derives table 2's 27 predictions on
the 66 rows and matches r2_20261105/PRETABLE_2.out exactly, which licenses the extension).  Handlers simulated statement by
statement: src/cpus/cpu_ppc_instr.c X(crandc) :2729-2737 and X(crorc) :2756-2764; dispatch :4638 and :4641.

WHAT PASS 3 FOUND (p3_20261105/codex_codex_r575_p3.txt).  Round 2's enumeration had put the read-mask sites (:2732-2733,
:2759-2760) and the set statements (:2736, :2763) in scope with a vocabulary narrower than the class: read masks {& 3, & 7} only,
the set edited only to `deleted' and `^='.  This round enumerates the FULL single-constant family at those sites that codex
named (1+2^k at every read site and every set literal, {0,2,4,6} at every read site), adds k = 31 at the same sites (in bound:
the same constant sites, one more constant), the 16 structural cells of codex's denominator, and then PROVES the rest of the
2^32-constant space at each site by argument (section PROOF below), so the contract can name the whole site.

ENUMERATION (one edit per cell, per handler): round 2's 239 cells unchanged (field mask m in 0..30 at BT, BA, BB; each source
read taking another field's index; the read mask & 3 / & 7; the clear moved before the reads, deleted or toggled; the set
deleted or ^=; the condition edits; the dispatch re-bindings; c) PLUS: the read mask `& 1' -> `& (1|1<<k)' for k = 2..31 and
-> & 0, & 2, & 4, & 6 at each of the four read sites (34 x 4 = 136); the set literal `1' -> the unsigned constant 1+2^k,
k = 1..31, in each handler (31 x 2 = 62); and 16 structural cells: the clear's and the set's `(31-bt)' -> `(31-ba)' / `(31-bb)'
(ba, bb hold the READ VALUES there, so the edit addresses CR[a] / CR[b]) and -> `bt' (bit position bt = CR index 31-bt), the
clear moved between the two reads, and the two read statements swapped (8 x 2 = 16).

DENOMINATOR: 453 cells = 6 clear + 15 cond + 12 decode + 186 mask + 8 read + 8 rmask + 136 rmask3 + 4 set + 62 setlit + 16 struct.
codex's denominator was 447: the same cells without k = 31 at the four read sites (4 cells) and at the two set literals
(2 cells).  Its partition (357 detected, 35 equivalent, 54 breaches, 1 disclosed) is checked cell by cell below.

## CODEX'S 54 SURVIVORS, ONE BY ONE (red on the 66 rows = none means the survivor is CONFIRMED; red on 70 = the round-3 rows)

| # | family | cell | red on 66 | verdict | red on 70 |
|---|---|---|---|---|---|
| 1 | B1 | crorc BB read mask &0x5 (1|1<<2) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 2 | B1 | crorc BB read mask &0x9 (1|1<<3) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 3 | B1 | crorc BB read mask &0x11 (1|1<<4) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 4 | B1 | crorc BB read mask &0x21 (1|1<<5) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 5 | B1 | crorc BB read mask &0x41 (1|1<<6) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 6 | B1 | crorc BB read mask &0x81 (1|1<<7) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 7 | B1 | crorc BB read mask &0x101 (1|1<<8) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 8 | B1 | crorc BB read mask &0x201 (1|1<<9) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 9 | B1 | crorc BB read mask &0x401 (1|1<<10) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 10 | B1 | crorc BB read mask &0x801 (1|1<<11) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 11 | B1 | crorc BB read mask &0x1001 (1|1<<12) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 12 | B1 | crorc BB read mask &0x2001 (1|1<<13) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 13 | B1 | crorc BB read mask &0x4001 (1|1<<14) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 14 | B1 | crorc BB read mask &0x8001 (1|1<<15) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 15 | B1 | crorc BB read mask &0x10001 (1|1<<16) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 16 | B1 | crorc BB read mask &0x20001 (1|1<<17) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 17 | B1 | crorc BB read mask &0x40001 (1|1<<18) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 18 | B1 | crorc BB read mask &0x80001 (1|1<<19) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 19 | B1 | crorc BB read mask &0x100001 (1|1<<20) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 20 | B1 | crorc BB read mask &0x200001 (1|1<<21) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 21 | B1 | crorc BB read mask &0x400001 (1|1<<22) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 22 | B1 | crorc BB read mask &0x800001 (1|1<<23) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 23 | B1 | crorc BB read mask &0x1000001 (1|1<<24) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 24 | B1 | crorc BB read mask &0x2000001 (1|1<<25) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 25 | B1 | crorc BB read mask &0x4000001 (1|1<<26) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 26 | B1 | crorc BB read mask &0x8000001 (1|1<<27) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 27 | B1 | crorc BB read mask &0x10000001 (1|1<<28) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 28 | B1 | crorc BB read mask &0x20000001 (1|1<<29) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 29 | B1 | crorc BB read mask &0x40000001 (1|1<<30) | none | CONFIRMED (survives 66) | 64_crorc_bbread |
| 30 | B2 | crorc BA read mask &0x8001 (1|1<<15) | none | CONFIRMED (survives 66) | 64_crorc_baread |
| 31 | B3 | crandc set literal 0x00000081u (1+2^7) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 32 | B3 | crandc set literal 0x00000201u (1+2^9) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 33 | B3 | crandc set literal 0x00000801u (1+2^11) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 34 | B3 | crandc set literal 0x00001001u (1+2^12) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 35 | B3 | crandc set literal 0x00002001u (1+2^13) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 36 | B3 | crandc set literal 0x00004001u (1+2^14) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 37 | B3 | crandc set literal 0x00008001u (1+2^15) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 38 | B3 | crandc set literal 0x00010001u (1+2^16) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 39 | B3 | crandc set literal 0x00020001u (1+2^17) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 40 | B3 | crandc set literal 0x00040001u (1+2^18) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 41 | B3 | crandc set literal 0x00080001u (1+2^19) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 42 | B3 | crandc set literal 0x00100001u (1+2^20) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 43 | B3 | crandc set literal 0x00200001u (1+2^21) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 44 | B3 | crandc set literal 0x00400001u (1+2^22) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 45 | B3 | crandc set literal 0x00800001u (1+2^23) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 46 | B3 | crandc set literal 0x01000001u (1+2^24) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 47 | B3 | crandc set literal 0x02000001u (1+2^25) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 48 | B3 | crandc set literal 0x04000001u (1+2^26) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 49 | B3 | crandc set literal 0x08000001u (1+2^27) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 50 | B3 | crandc set literal 0x10000001u (1+2^28) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 51 | B3 | crandc set literal 0x20000001u (1+2^29) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 52 | B3 | crandc set literal 0x40000001u (1+2^30) | none | CONFIRMED (survives 66) | 64_crandc_setbits |
| 53 | B4 | crorc set literal 0x04000001u (1+2^26) | none | CONFIRMED (survives 66) | 64_crorc_setbits |
| 54 | B4 | crorc set literal 0x08000001u (1+2^27) | none | CONFIRMED (survives 66) | 64_crorc_setbits |

codex's survivors: 54 CONFIRMED, 0 REFUTED.

## CODEX'S 35 EQUIVALENTS, ONE BY ONE (`rand-equiv' = 40000 random (cr,BT,BA,BB) found no difference from the fix; the proof is the WHY)

| # | cell | red on 66 | red on 70 | rand-equiv | verdict | why |
|---|---|---|---|---|---|---|
| 1 | crandc BA read mask &3 | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 2 | crandc BA read mask &7 | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 3 | crandc set |= -> ^= | none | none | True | CONFIRMED | the clear at :2734 has just zeroed the bit, so ^= and |= set it alike |
| 4 | crorc set |= -> ^= | none | none | True | CONFIRMED | the clear at :2761 has just zeroed the bit, so ^= and |= set it alike |
| 5 | crandc BA read mask &0x5 (1|1<<2) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 6 | crandc BA read mask &0x9 (1|1<<3) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 7 | crandc BA read mask &0x11 (1|1<<4) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 8 | crandc BA read mask &0x21 (1|1<<5) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 9 | crandc BA read mask &0x41 (1|1<<6) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 10 | crandc BA read mask &0x81 (1|1<<7) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 11 | crandc BA read mask &0x101 (1|1<<8) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 12 | crandc BA read mask &0x201 (1|1<<9) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 13 | crandc BA read mask &0x401 (1|1<<10) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 14 | crandc BA read mask &0x801 (1|1<<11) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 15 | crandc BA read mask &0x1001 (1|1<<12) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 16 | crandc BA read mask &0x2001 (1|1<<13) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 17 | crandc BA read mask &0x4001 (1|1<<14) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 18 | crandc BA read mask &0x8001 (1|1<<15) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 19 | crandc BA read mask &0x10001 (1|1<<16) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 20 | crandc BA read mask &0x20001 (1|1<<17) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 21 | crandc BA read mask &0x40001 (1|1<<18) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 22 | crandc BA read mask &0x80001 (1|1<<19) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 23 | crandc BA read mask &0x100001 (1|1<<20) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 24 | crandc BA read mask &0x200001 (1|1<<21) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 25 | crandc BA read mask &0x400001 (1|1<<22) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 26 | crandc BA read mask &0x800001 (1|1<<23) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 27 | crandc BA read mask &0x1000001 (1|1<<24) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 28 | crandc BA read mask &0x2000001 (1|1<<25) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 29 | crandc BA read mask &0x4000001 (1|1<<26) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 30 | crandc BA read mask &0x8000001 (1|1<<27) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 31 | crandc BA read mask &0x10000001 (1|1<<28) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 32 | crandc BA read mask &0x20000001 (1|1<<29) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 33 | crandc BA read mask &0x40000001 (1|1<<30) | none | none | True | CONFIRMED | `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition |
| 34 | crandc read statements swapped | none | none | True | CONFIRMED | the two reads are independent of each other and of the clear (which follows both) |
| 35 | crorc read statements swapped | none | none | True | CONFIRMED | the two reads are independent of each other and of the clear (which follows both) |

codex's equivalents: 35 CONFIRMED, 0 REFUTED.  One more equivalent cell is in this denominator and not in codex's:
crandc BA read mask &0x80000001 (1|1<<31), by the same proof.

## CELL -> ROW MAP (every cell of the 453; 62/66/70 = red rows of the probe at that stage)

| class | cell | status | red on 62 | red on 66 | red on 70 |
|---|---|---|---|---|---|
| mask | crandc BT mask &0 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &1 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &2 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &3 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &4 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &5 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &6 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &7 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &8 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &9 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_setbits,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &10 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &11 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BT mask &12 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &13 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_setbits,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &14 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &15 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BT mask &16 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &17 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &18 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &19 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &20 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &21 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &22 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &23 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &24 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &25 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_setbits,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &26 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &27 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BT mask &28 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &29 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_setbits,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &30 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,64_crandc_setbits,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BA mask &0 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &1 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &2 | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &3 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &4 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &5 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &6 | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &7 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &8 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &9 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &10 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &11 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &12 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &13 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &14 | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &15 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &16 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &17 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &18 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &19 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &20 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &21 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &22 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &23 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &24 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &25 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &26 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &27 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi | 64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &28 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_10 |
| mask | crandc BA mask &29 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi,64_crandc_setbits |
| mask | crandc BA mask &30 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 |
| mask | crandc BB mask &0 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &1 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask,64_crandc_order | 64_crandc_hi,64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &2 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &3 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask,64_crandc_order | 64_crandc_hi,64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &4 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &5 | CLOSED by round 2 | none | 64_crandc_bbmask,64_crandc_order | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &6 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &7 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask,64_crandc_order | 64_crandc_hi,64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &8 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &9 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| mask | crandc BB mask &10 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &11 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| mask | crandc BB mask &12 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &13 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| mask | crandc BB mask &14 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &15 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask | 64_crandc_hi,64_crandc_bbmask |
| mask | crandc BB mask &16 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &17 | CLOSED by round 2 | none | 64_crandc_bbmask,64_crandc_order | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &18 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &19 | CLOSED by round 2 | none | 64_crandc_bbmask,64_crandc_order | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &20 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &21 | CLOSED by round 2 | none | 64_crandc_bbmask,64_crandc_order | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &22 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &23 | CLOSED by round 2 | none | 64_crandc_bbmask,64_crandc_order | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &24 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &25 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| mask | crandc BB mask &26 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &27 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| mask | crandc BB mask &28 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &29 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| mask | crandc BB mask &30 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_11 |
| read | crandc BA read <- BB index | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| read | crandc BA read <- BT index | DETECTED(62) | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10 | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10 | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_setbits,32_crandc_00,32_crandc_10 |
| read | crandc BB read <- BA index | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crandc_bbmask,64_crandc_order,32_crandc_10 | 64_crandc_10,64_crandc_bbmask,64_crandc_order,32_crandc_10 |
| read | crandc BB read <- BT index | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask | crandc BA read mask &3 | EQUIVALENT rand-equiv | none | none | none |
| rmask | crandc BA read mask &7 | EQUIVALENT rand-equiv | none | none | none |
| rmask | crandc BB read mask &3 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask,64_crandc_setbits |
| rmask | crandc BB read mask &7 | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask,64_crandc_setbits |
| clear | crandc clear moved before the reads | CLOSED by round 2 | none | 64_crandc_order | 64_crandc_order |
| clear | crandc clear deleted | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,32_crandc_00,32_crandc_01,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11 |
| clear | crandc clear -> toggle (^=) | EXCLUDED (disclosed) | none | none | none |
| set | crandc set deleted | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| set | crandc set |= -> ^= | EQUIVALENT rand-equiv | none | none | none |
| cond | crandc cond b1  !(ba & bb)  (NAND restored) | DETECTED(62) | 64_crandc_00,64_crandc_01,edge_crandc_bt0,32_crandc_00,32_crandc_01 | 64_crandc_00,64_crandc_01,edge_crandc_bt0,32_crandc_00,32_crandc_01 | 64_crandc_00,64_crandc_01,edge_crandc_bt0,32_crandc_00,32_crandc_01 |
| cond | crandc cond d1  !ba & bb | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_hi,32_crandc_01,32_crandc_10 | 64_crandc_01,64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_01,32_crandc_10 | 64_crandc_01,64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_01,32_crandc_10 |
| cond | crandc cond d3  ba & bb   (complement dropped) | DETECTED(62) | 64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_10,32_crandc_11 | 64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_10,32_crandc_11 | 64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_10,32_crandc_11 |
| cond | crandc cond d5  ba | !bb  (operator crossed) | DETECTED(62) | 64_crandc_00,64_crandc_11,edge_crandc_bt0,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11 |
| cond | crandc cond r5a bt & !bb | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 |
| cond | crandc cond r5b ba & !bt | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| cond | crandc identity body | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| decode | crandc dispatch -> instr(crand) | DETECTED(62) | 64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_10,32_crandc_11 | 64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_10,32_crandc_11 | 64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_10,32_crandc_11 |
| decode | crandc dispatch -> instr(creqv) | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_10,32_crandc_11 |
| decode | crandc dispatch -> instr(cror) | DETECTED(62) | 64_crandc_01,64_crandc_11,32_crandc_01,32_crandc_11 | 64_crandc_01,64_crandc_11,64_crandc_order,32_crandc_01,32_crandc_11 | 64_crandc_01,64_crandc_11,64_crandc_order,32_crandc_01,32_crandc_11 |
| decode | crandc dispatch -> instr(crorc) | DETECTED(62) | 64_crandc_00,64_crandc_11,edge_crandc_bt0,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11 |
| decode | crandc dispatch -> instr(crnor) | DETECTED(62) | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10 | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_bbmask,32_crandc_00,32_crandc_10 | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_00,32_crandc_10 |
| decode | crandc dispatch -> instr(crxor) | DETECTED(62) | 64_crandc_01,32_crandc_01 | 64_crandc_01,32_crandc_01 | 64_crandc_01,32_crandc_01 |
| mask | crorc BT mask &0 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &1 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &2 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &3 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &4 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &5 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &6 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &7 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &8 | DETECTED(62) | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &9 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &10 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &11 | DETECTED(62) | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &12 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &13 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &14 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_11 |
| mask | crorc BT mask &15 | DETECTED(62) | edge_crorc_bt31,edge_others,64_crorc_hi | edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask | edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits |
| mask | crorc BT mask &16 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &17 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &18 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &19 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &20 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &21 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbmask,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &22 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &23 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbmask,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &24 | DETECTED(62) | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &25 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,64_crorc_setbits,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &26 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &27 | DETECTED(62) | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,64_crorc_setbits,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &28 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &29 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_bbmask,64_crorc_bbread,64_crorc_setbits,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &30 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_11 |
| mask | crorc BA mask &0 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &1 | DETECTED(62) | edge_crorc_bt31,64_crorc_hi | edge_crorc_bt31,64_crorc_hi,64_crorc_bamask | edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &2 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &3 | DETECTED(62) | edge_crorc_bt31,64_crorc_hi | edge_crorc_bt31,64_crorc_hi,64_crorc_bamask | edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &4 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &5 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &6 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &7 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &8 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &9 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask | edge_crorc_bt31,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &10 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &11 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask | edge_crorc_bt31,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &12 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &13 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &14 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &15 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &16 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &17 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask | edge_crorc_bt31,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &18 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &19 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask | edge_crorc_bt31,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &20 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &21 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &22 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &23 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &24 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &25 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask | edge_crorc_bt31,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &26 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &27 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask | edge_crorc_bt31,64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &28 | DETECTED(62) | 64_crorc_11,64_crorc_hi,32_crorc_11 | 64_crorc_11,64_crorc_hi,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_hi,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BA mask &29 | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| mask | crorc BA mask &30 | DETECTED(62) | 64_crorc_11,64_crorc_hi,32_crorc_11 | 64_crorc_11,64_crorc_hi,64_crorc_bamask,32_crorc_11 | 64_crorc_11,64_crorc_hi,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| mask | crorc BB mask &0 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &1 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &2 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &3 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &4 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &5 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &6 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &7 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &8 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &9 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &10 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &11 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &12 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &13 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &14 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &15 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &16 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &17 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &18 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &19 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &20 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &21 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &22 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &23 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &24 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &25 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &26 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &27 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask | 64_crorc_hi,64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &28 | DETECTED(62) | 64_crorc_01,32_crorc_01 | 64_crorc_01,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| mask | crorc BB mask &29 | CLOSED by round 2 | none | 64_crorc_bbmask | 64_crorc_bbmask,64_crorc_bbread |
| mask | crorc BB mask &30 | DETECTED(62) | 64_crorc_01,32_crorc_01 | 64_crorc_01,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_bbmask,32_crorc_01 |
| read | crorc BA read <- BB index | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01 |
| read | crorc BA read <- BT index | DETECTED(62) | 64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_01,32_crorc_11 | 64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_11 | 64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,32_crorc_01,32_crorc_11 |
| read | crorc BB read <- BA index | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| read | crorc BB read <- BT index | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask |
| rmask | crorc BA read mask &3 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| rmask | crorc BA read mask &7 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| rmask | crorc BB read mask &3 | DETECTED(62) | 64_crorc_00,32_crorc_00 | 64_crorc_00,32_crorc_00 | 64_crorc_00,32_crorc_00 |
| rmask | crorc BB read mask &7 | DETECTED(62) | 64_crorc_00,32_crorc_00 | 64_crorc_00,32_crorc_00 | 64_crorc_00,64_crorc_bbread,32_crorc_00 |
| clear | crorc clear moved before the reads | CLOSED by round 2 | none | 64_crorc_bbmask | 64_crorc_bbmask |
| clear | crorc clear deleted | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,32_crorc_01 |
| clear | crorc clear -> toggle (^=) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask |
| set | crorc set deleted | DETECTED(62) | 64_crorc_00,64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_10,64_crorc_11,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11 |
| set | crorc set |= -> ^= | EQUIVALENT rand-equiv | none | none | none |
| cond | crorc cond b2  !(ba | bb)  (NOR restored) | DETECTED(62) | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 |
| cond | crorc cond d2  !ba | bb | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_hi,32_crorc_01,32_crorc_10 | 64_crorc_01,64_crorc_10,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_01,32_crorc_10 | 64_crorc_01,64_crorc_10,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01,32_crorc_10 |
| cond | crorc cond d4  ba | bb   (complement dropped) | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_hi,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01 |
| cond | crorc cond d6  ba & !bb  (operator crossed) | DETECTED(62) | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 | 64_crorc_00,64_crorc_11,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_11 |
| cond | crorc cond r5c bt | !bb | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01 |
| cond | crorc cond r5d ba | !bt | DETECTED(62) | 64_crorc_00,32_crorc_00 | 64_crorc_00,32_crorc_00 | 64_crorc_00,64_crorc_bbread,64_crorc_setbits,32_crorc_00 |
| cond | crorc identity body | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| decode | crorc dispatch -> instr(crand) | DETECTED(62) | 64_crorc_00,64_crorc_10,32_crorc_00,32_crorc_10 | 64_crorc_00,64_crorc_10,32_crorc_00,32_crorc_10 | 64_crorc_00,64_crorc_10,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10 |
| decode | crorc dispatch -> instr(crandc) | DETECTED(62) | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 | 64_crorc_00,64_crorc_11,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_11 |
| decode | crorc dispatch -> instr(creqv) | DETECTED(62) | 64_crorc_10,32_crorc_10 | 64_crorc_10,32_crorc_10 | 64_crorc_10,32_crorc_10 |
| decode | crorc dispatch -> instr(cror) | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_hi,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01 |
| decode | crorc dispatch -> instr(crnor) | DETECTED(62) | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 |
| decode | crorc dispatch -> instr(crxor) | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_11 |
| cond | c   both bodies identity | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,64_crandc_hi,64_crorc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,64_crandc_hi,64_crorc_hi,64_crandc_order,64_crorc_bbmask,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,64_crandc_hi,64_crorc_hi,64_crandc_order,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crandc_setbits,64_crorc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| rmask3 | crandc BA read mask &0x5 (1|1<<2) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x9 (1|1<<3) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x11 (1|1<<4) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x21 (1|1<<5) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x41 (1|1<<6) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x81 (1|1<<7) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x101 (1|1<<8) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x201 (1|1<<9) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x401 (1|1<<10) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x801 (1|1<<11) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x1001 (1|1<<12) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x2001 (1|1<<13) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x4001 (1|1<<14) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x8001 (1|1<<15) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x10001 (1|1<<16) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x20001 (1|1<<17) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x40001 (1|1<<18) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x80001 (1|1<<19) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x100001 (1|1<<20) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x200001 (1|1<<21) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x400001 (1|1<<22) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x800001 (1|1<<23) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x1000001 (1|1<<24) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x2000001 (1|1<<25) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x4000001 (1|1<<26) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x8000001 (1|1<<27) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x10000001 (1|1<<28) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x20000001 (1|1<<29) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x40000001 (1|1<<30) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0x80000001 (1|1<<31) | EQUIVALENT rand-equiv | none | none | none |
| rmask3 | crandc BA read mask &0 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| rmask3 | crandc BA read mask &2 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| rmask3 | crandc BA read mask &4 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| rmask3 | crandc BA read mask &6 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| rmask3 | crandc BB read mask &0x5 (1|1<<2) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x9 (1|1<<3) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x11 (1|1<<4) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x21 (1|1<<5) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x41 (1|1<<6) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x81 (1|1<<7) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x101 (1|1<<8) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x201 (1|1<<9) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x401 (1|1<<10) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x801 (1|1<<11) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x1001 (1|1<<12) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x2001 (1|1<<13) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x4001 (1|1<<14) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x8001 (1|1<<15) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x10001 (1|1<<16) | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask | 64_crandc_hi,64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x20001 (1|1<<17) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x40001 (1|1<<18) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x80001 (1|1<<19) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x100001 (1|1<<20) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x200001 (1|1<<21) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x400001 (1|1<<22) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x800001 (1|1<<23) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x1000001 (1|1<<24) | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask | 64_crandc_hi,64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x2000001 (1|1<<25) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x4000001 (1|1<<26) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x8000001 (1|1<<27) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x10000001 (1|1<<28) | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask | 64_crandc_hi,64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x20000001 (1|1<<29) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x40000001 (1|1<<30) | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask | 64_crandc_hi,64_crandc_bbmask |
| rmask3 | crandc BB read mask &0x80000001 (1|1<<31) | CLOSED by round 2 | none | 64_crandc_bbmask | 64_crandc_bbmask |
| rmask3 | crandc BB read mask &0 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_order,32_crandc_11 |
| rmask3 | crandc BB read mask &2 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_11 |
| rmask3 | crandc BB read mask &4 | CLOSED by round 2 | none | 64_crandc_bbmask,64_crandc_order | 64_crandc_bbmask,64_crandc_order |
| rmask3 | crandc BB read mask &6 | CLOSED by round 2 | none | 64_crandc_bbmask,64_crandc_order | 64_crandc_bbmask,64_crandc_order,64_crandc_setbits |
| rmask3 | crorc BA read mask &0x5 (1|1<<2) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x9 (1|1<<3) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x11 (1|1<<4) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x21 (1|1<<5) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x41 (1|1<<6) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x81 (1|1<<7) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x101 (1|1<<8) | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x201 (1|1<<9) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x401 (1|1<<10) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x801 (1|1<<11) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x1001 (1|1<<12) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x2001 (1|1<<13) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x4001 (1|1<<14) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x8001 (1|1<<15) | CLOSED by round 3: 64_crorc_baread | none | none | 64_crorc_baread |
| rmask3 | crorc BA read mask &0x10001 (1|1<<16) | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x20001 (1|1<<17) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x40001 (1|1<<18) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x80001 (1|1<<19) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x100001 (1|1<<20) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x200001 (1|1<<21) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x400001 (1|1<<22) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x800001 (1|1<<23) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x1000001 (1|1<<24) | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x2000001 (1|1<<25) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x4000001 (1|1<<26) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x8000001 (1|1<<27) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x10000001 (1|1<<28) | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask | 64_crorc_hi,64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x20000001 (1|1<<29) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x40000001 (1|1<<30) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0x80000001 (1|1<<31) | CLOSED by round 2 | none | 64_crorc_bamask | 64_crorc_bamask,64_crorc_baread |
| rmask3 | crorc BA read mask &0 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,32_crorc_11 |
| rmask3 | crorc BA read mask &2 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| rmask3 | crorc BA read mask &4 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| rmask3 | crorc BA read mask &6 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,64_crorc_baread,32_crorc_11 |
| rmask3 | crorc BB read mask &0x5 (1|1<<2) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x9 (1|1<<3) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x11 (1|1<<4) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x21 (1|1<<5) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x41 (1|1<<6) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x81 (1|1<<7) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x101 (1|1<<8) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x201 (1|1<<9) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x401 (1|1<<10) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x801 (1|1<<11) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x1001 (1|1<<12) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x2001 (1|1<<13) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x4001 (1|1<<14) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x8001 (1|1<<15) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x10001 (1|1<<16) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x20001 (1|1<<17) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x40001 (1|1<<18) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x80001 (1|1<<19) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x100001 (1|1<<20) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x200001 (1|1<<21) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x400001 (1|1<<22) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x800001 (1|1<<23) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x1000001 (1|1<<24) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x2000001 (1|1<<25) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x4000001 (1|1<<26) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x8000001 (1|1<<27) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x10000001 (1|1<<28) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x20000001 (1|1<<29) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x40000001 (1|1<<30) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0x80000001 (1|1<<31) | CLOSED by round 3: 64_crorc_bbread | none | none | 64_crorc_bbread |
| rmask3 | crorc BB read mask &0 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01 |
| rmask3 | crorc BB read mask &2 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_hi,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01 |
| rmask3 | crorc BB read mask &4 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_01 |
| rmask3 | crorc BB read mask &6 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_hi,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_bbread,32_crorc_00,32_crorc_01 |
| setlit | crandc set literal 0x00000003u (1+2^1) | DETECTED(62) | 64_crandc_01,32_crandc_01 | 64_crandc_01,32_crandc_01 | 64_crandc_01,32_crandc_01 |
| setlit | crandc set literal 0x00000005u (1+2^2) | DETECTED(62) | 64_crandc_00,32_crandc_00 | 64_crandc_00,32_crandc_00 | 64_crandc_00,64_crandc_setbits,32_crandc_00 |
| setlit | crandc set literal 0x00000009u (1+2^3) | DETECTED(62) | 64_others,32_others | 64_others,32_others | 64_others,64_crandc_setbits,32_others |
| setlit | crandc set literal 0x00000011u (1+2^4) | DETECTED(62) | 64_others,32_others | 64_others,32_others | 64_others,64_crandc_setbits,32_others |
| setlit | crandc set literal 0x00000021u (1+2^5) | DETECTED(62) | 64_others,32_others | 64_others,32_others | 64_others,64_crandc_setbits,32_others |
| setlit | crandc set literal 0x00000041u (1+2^6) | DETECTED(62) | 64_others,32_others | 64_others,32_others | 64_others,64_crandc_setbits,32_others |
| setlit | crandc set literal 0x00000081u (1+2^7) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00000101u (1+2^8) | DETECTED(62) | 64_crorc_00,64_others,32_crorc_00,32_others | 64_crorc_00,64_others,32_crorc_00,32_others | 64_crorc_00,64_others,64_crandc_setbits,32_crorc_00,32_others |
| setlit | crandc set literal 0x00000201u (1+2^9) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00000401u (1+2^10) | DETECTED(62) | 64_crorc_01,64_others,32_crorc_01,32_others | 64_crorc_01,64_others,32_crorc_01,32_others | 64_crorc_01,64_others,64_crandc_setbits,32_crorc_01,32_others |
| setlit | crandc set literal 0x00000801u (1+2^11) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00001001u (1+2^12) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00002001u (1+2^13) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00004001u (1+2^14) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00008001u (1+2^15) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00010001u (1+2^16) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00020001u (1+2^17) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00040001u (1+2^18) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00080001u (1+2^19) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00100001u (1+2^20) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00200001u (1+2^21) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00400001u (1+2^22) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x00800001u (1+2^23) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x01000001u (1+2^24) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x02000001u (1+2^25) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x04000001u (1+2^26) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x08000001u (1+2^27) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x10000001u (1+2^28) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x20000001u (1+2^29) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x40000001u (1+2^30) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crandc set literal 0x80000001u (1+2^31) | CLOSED by round 3: 64_crandc_setbits | none | none | 64_crandc_setbits |
| setlit | crorc set literal 0x00000003u (1+2^1) | DETECTED(62) | 64_crandc_11,64_crorc_01,edge_others,32_crandc_11,32_crorc_01 | 64_crandc_11,64_crorc_01,edge_others,32_crandc_11,32_crorc_01 | 64_crandc_11,64_crorc_01,edge_others,64_crorc_setbits,32_crandc_11,32_crorc_01 |
| setlit | crorc set literal 0x00000005u (1+2^2) | DETECTED(62) | 64_crorc_01,edge_others,32_crorc_01 | 64_crorc_01,edge_others,32_crorc_01 | 64_crorc_01,edge_others,64_crorc_setbits,32_crorc_01 |
| setlit | crorc set literal 0x00000009u (1+2^3) | DETECTED(62) | 64_crandc_01,64_crandc_11,edge_others,32_crandc_01,32_crandc_11 | 64_crandc_01,64_crandc_11,edge_others,32_crandc_01,32_crandc_11 | 64_crandc_01,64_crandc_11,edge_others,64_crorc_setbits,32_crandc_01,32_crandc_11 |
| setlit | crorc set literal 0x00000011u (1+2^4) | DETECTED(62) | 64_crandc_00,64_crandc_11,edge_others,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_others,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_others,64_crorc_setbits,32_crandc_00,32_crandc_11 |
| setlit | crorc set literal 0x00000021u (1+2^5) | DETECTED(62) | 64_crandc_01,64_others,edge_others,32_crandc_01,32_others | 64_crandc_01,64_others,edge_others,32_crandc_01,32_others | 64_crandc_01,64_others,edge_others,64_crorc_setbits,32_crandc_01,32_others |
| setlit | crorc set literal 0x00000041u (1+2^6) | DETECTED(62) | 64_crandc_00,64_crandc_01,64_others,edge_others,32_crandc_00,32_crandc_01,32_others | 64_crandc_00,64_crandc_01,64_others,edge_others,32_crandc_00,32_crandc_01,32_others | 64_crandc_00,64_crandc_01,64_others,edge_others,64_crorc_setbits,32_crandc_00,32_crandc_01,32_others |
| setlit | crorc set literal 0x00000081u (1+2^7) | DETECTED(62) | 64_crandc_00,64_others,edge_others,32_crandc_00,32_others | 64_crandc_00,64_others,edge_others,32_crandc_00,32_others | 64_crandc_00,64_others,edge_others,64_crorc_setbits,32_crandc_00,32_others |
| setlit | crorc set literal 0x00000101u (1+2^8) | DETECTED(62) | 64_others,edge_others,32_others | 64_others,edge_others,32_others | 64_others,edge_others,64_crorc_setbits,32_others |
| setlit | crorc set literal 0x00000201u (1+2^9) | DETECTED(62) | 64_others,edge_others,32_others | 64_others,edge_others,32_others | 64_others,edge_others,64_crorc_setbits,32_others |
| setlit | crorc set literal 0x00000401u (1+2^10) | DETECTED(62) | 64_others,edge_others,32_others | 64_others,edge_others,32_others | 64_others,edge_others,64_crorc_setbits,32_others |
| setlit | crorc set literal 0x00000801u (1+2^11) | DETECTED(62) | 64_others,edge_others,32_others | 64_others,edge_others,32_others | 64_others,edge_others,64_crorc_setbits,32_others |
| setlit | crorc set literal 0x00001001u (1+2^12) | DETECTED(62) | 64_crorc_01,64_others,edge_others,32_crorc_01,32_others | 64_crorc_01,64_others,edge_others,32_crorc_01,32_others | 64_crorc_01,64_others,edge_others,64_crorc_setbits,32_crorc_01,32_others |
| setlit | crorc set literal 0x00002001u (1+2^13) | DETECTED(62) | 64_others,edge_others,32_others | 64_others,edge_others,32_others | 64_others,edge_others,64_crorc_setbits,32_others |
| setlit | crorc set literal 0x00004001u (1+2^14) | DETECTED(62) | 64_others,edge_others,32_others | 64_others,edge_others,32_others | 64_others,edge_others,64_crorc_setbits,32_others |
| setlit | crorc set literal 0x00008001u (1+2^15) | DETECTED(62) | 64_others,edge_others,32_others | 64_others,edge_others,32_others | 64_others,edge_others,64_crorc_setbits,32_others |
| setlit | crorc set literal 0x00010001u (1+2^16) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x00020001u (1+2^17) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x00040001u (1+2^18) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x00080001u (1+2^19) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x00100001u (1+2^20) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x00200001u (1+2^21) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x00400001u (1+2^22) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x00800001u (1+2^23) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x01000001u (1+2^24) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x02000001u (1+2^25) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x04000001u (1+2^26) | CLOSED by round 3: 64_crorc_setbits | none | none | 64_crorc_setbits |
| setlit | crorc set literal 0x08000001u (1+2^27) | CLOSED by round 3: 64_crorc_setbits | none | none | 64_crorc_setbits |
| setlit | crorc set literal 0x10000001u (1+2^28) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x20000001u (1+2^29) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x40000001u (1+2^30) | DETECTED(62) | edge_others | edge_others | edge_others,64_crorc_setbits |
| setlit | crorc set literal 0x80000001u (1+2^31) | DETECTED(62) | edge_crandc_bt0 | edge_crandc_bt0 | edge_crandc_bt0,64_crorc_setbits |
| struct | crandc clear (31-bt) -> (31-ba) | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_11,64_crorc_01,64_crorc_11,64_others,32_crandc_00,32_crandc_01,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| struct | crandc clear (31-bt) -> (31-bb) | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| struct | crandc set (31-bt) -> (31-ba) | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10 |
| struct | crandc set (31-bt) -> (31-bb) | DETECTED(62) | 64_crandc_10,64_crorc_01,64_others,64_crandc_hi,32_crandc_10,32_crorc_01,32_others | 64_crandc_10,64_crorc_01,64_others,64_crandc_hi,64_crandc_bbmask,32_crandc_10,32_crorc_01,32_others | 64_crandc_10,64_crorc_01,64_others,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10,32_crorc_01,32_others |
| struct | crandc clear (31-bt) -> bt | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,32_crandc_00,32_crandc_01,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11 |
| struct | crandc set (31-bt) -> bt | DETECTED(62) | 64_crandc_10,64_others,64_crandc_hi,32_crandc_10,32_others | 64_crandc_10,64_others,64_crandc_hi,64_crandc_bbmask,32_crandc_10,32_others | 64_crandc_10,64_others,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10,32_others |
| struct | crandc clear moved between the reads | CLOSED by round 2 | none | 64_crandc_order | 64_crandc_order |
| struct | crandc read statements swapped | EQUIVALENT rand-equiv | none | none | none |
| struct | crorc clear (31-bt) -> (31-ba) | DETECTED(62) | 64_crorc_01,64_crorc_11,64_others,64_crorc_hi,32_crorc_01,32_crorc_11,32_others | 64_crorc_01,64_crorc_11,64_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_11,32_others | 64_crorc_01,64_crorc_11,64_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,32_crorc_01,32_crorc_11,32_others |
| struct | crorc clear (31-bt) -> (31-bb) | DETECTED(62) | 64_crorc_01,64_crorc_11,64_others,64_crorc_hi,32_crorc_01,32_crorc_11,32_others | 64_crorc_01,64_crorc_11,64_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_11,32_others | 64_crorc_01,64_crorc_11,64_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,32_crorc_01,32_crorc_11,32_others |
| struct | crorc set (31-bt) -> (31-ba) | DETECTED(62) | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11,32_others |
| struct | crorc set (31-bt) -> (31-bb) | DETECTED(62) | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11,32_others |
| struct | crorc clear (31-bt) -> bt | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,32_crorc_01 |
| struct | crorc set (31-bt) -> bt | DETECTED(62) | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,32_crorc_00,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,32_crorc_00,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11,32_others |
| struct | crorc clear moved between the reads | CLOSED by round 2 | none | 64_crorc_bbmask | 64_crorc_bbmask |
| struct | crorc read statements swapped | EQUIVALENT rand-equiv | none | none | none |

CLOSED BY THE 4 ROUND-3 ROWS (56 cells; missed by the 66 rows):
  - crorc BA read mask &0x8001 (1|1<<15)
  - crorc BB read mask &0x5 (1|1<<2)
  - crorc BB read mask &0x9 (1|1<<3)
  - crorc BB read mask &0x11 (1|1<<4)
  - crorc BB read mask &0x21 (1|1<<5)
  - crorc BB read mask &0x41 (1|1<<6)
  - crorc BB read mask &0x81 (1|1<<7)
  - crorc BB read mask &0x101 (1|1<<8)
  - crorc BB read mask &0x201 (1|1<<9)
  - crorc BB read mask &0x401 (1|1<<10)
  - crorc BB read mask &0x801 (1|1<<11)
  - crorc BB read mask &0x1001 (1|1<<12)
  - crorc BB read mask &0x2001 (1|1<<13)
  - crorc BB read mask &0x4001 (1|1<<14)
  - crorc BB read mask &0x8001 (1|1<<15)
  - crorc BB read mask &0x10001 (1|1<<16)
  - crorc BB read mask &0x20001 (1|1<<17)
  - crorc BB read mask &0x40001 (1|1<<18)
  - crorc BB read mask &0x80001 (1|1<<19)
  - crorc BB read mask &0x100001 (1|1<<20)
  - crorc BB read mask &0x200001 (1|1<<21)
  - crorc BB read mask &0x400001 (1|1<<22)
  - crorc BB read mask &0x800001 (1|1<<23)
  - crorc BB read mask &0x1000001 (1|1<<24)
  - crorc BB read mask &0x2000001 (1|1<<25)
  - crorc BB read mask &0x4000001 (1|1<<26)
  - crorc BB read mask &0x8000001 (1|1<<27)
  - crorc BB read mask &0x10000001 (1|1<<28)
  - crorc BB read mask &0x20000001 (1|1<<29)
  - crorc BB read mask &0x40000001 (1|1<<30)
  - crorc BB read mask &0x80000001 (1|1<<31)
  - crandc set literal 0x00000081u (1+2^7)
  - crandc set literal 0x00000201u (1+2^9)
  - crandc set literal 0x00000801u (1+2^11)
  - crandc set literal 0x00001001u (1+2^12)
  - crandc set literal 0x00002001u (1+2^13)
  - crandc set literal 0x00004001u (1+2^14)
  - crandc set literal 0x00008001u (1+2^15)
  - crandc set literal 0x00010001u (1+2^16)
  - crandc set literal 0x00020001u (1+2^17)
  - crandc set literal 0x00040001u (1+2^18)
  - crandc set literal 0x00080001u (1+2^19)
  - crandc set literal 0x00100001u (1+2^20)
  - crandc set literal 0x00200001u (1+2^21)
  - crandc set literal 0x00400001u (1+2^22)
  - crandc set literal 0x00800001u (1+2^23)
  - crandc set literal 0x01000001u (1+2^24)
  - crandc set literal 0x02000001u (1+2^25)
  - crandc set literal 0x04000001u (1+2^26)
  - crandc set literal 0x08000001u (1+2^27)
  - crandc set literal 0x10000001u (1+2^28)
  - crandc set literal 0x20000001u (1+2^29)
  - crandc set literal 0x40000001u (1+2^30)
  - crandc set literal 0x80000001u (1+2^31)
  - crorc set literal 0x04000001u (1+2^26)
  - crorc set literal 0x08000001u (1+2^27)

EQUIVALENT (36 cells; proved, and 40000 random trials found no difference):
  - crandc BA read mask &3: `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &7: `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc set |= -> ^=: the clear at :2734 has just zeroed the bit, so ^= and |= set it alike
  - crorc set |= -> ^=: the clear at :2761 has just zeroed the bit, so ^= and |= set it alike
  - crandc BA read mask &0x5 (1|1<<2): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x9 (1|1<<3): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x11 (1|1<<4): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x21 (1|1<<5): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x41 (1|1<<6): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x81 (1|1<<7): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x101 (1|1<<8): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x201 (1|1<<9): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x401 (1|1<<10): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x801 (1|1<<11): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x1001 (1|1<<12): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x2001 (1|1<<13): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x4001 (1|1<<14): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x8001 (1|1<<15): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x10001 (1|1<<16): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x20001 (1|1<<17): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x40001 (1|1<<18): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x80001 (1|1<<19): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x100001 (1|1<<20): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x200001 (1|1<<21): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x400001 (1|1<<22): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x800001 (1|1<<23): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x1000001 (1|1<<24): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x2000001 (1|1<<25): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x4000001 (1|1<<26): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x8000001 (1|1<<27): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x10000001 (1|1<<28): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x20000001 (1|1<<29): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x40000001 (1|1<<30): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc BA read mask &0x80000001 (1|1<<31): `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can reach the condition
  - crandc read statements swapped: the two reads are independent of each other and of the clear (which follows both)
  - crorc read statements swapped: the two reads are independent of each other and of the clear (which follows both)

EXCLUDED / DISCLOSED (1 cell):
  - crandc clear -> toggle (^=): disclosed in the probe's clause (e)(5): every crandc row with result 0 pre-sets the inverse

STILL UNDETECTED BY THE 70 ROWS (0 cells):

## THE 4 ROUND-3 ROWS (single-instruction sessions shaped like the `hi'/pin rows; each compares the WHOLE CR, from the
register dump and from mfcr r10, with the architectural CR)

  64 crorc baread   crorc BT=17 BA=31 BB=5 seed=0xfffffffe want CR=0xffffbffe  CR[BT] pre-set inverse (1)
  64 crorc bbread   crorc BT=30 BA=30 BB=31 seed=0xfffffffc want CR=0xfffffffe  CR[BT] pre-set inverse (0) = the BA source
  64 crandc setbits crandc BT=31 BA=30 BB=31 seed=0x00000002 want CR=0x00000003  CR[BT] pre-set inverse (0)
  64 crorc setbits  crorc BT=31 BA=0 BB=31 seed=0x00000000 want CR=0x00000001  CR[BT] pre-set inverse (0) = the BB source

  64 crorc baread   crorc 17,31,5 over 0xfffffffe: a = CR[31] = 0, b = CR[5] = 1 -> 0.  The BA read shifts by 0, so a = CR & m: every
                    mask m with ANY bit 1..31 set reads nonzero and gives 1 (codex B2's & 0x8001 reads CR[16] = 1 here; the
                    round-2 `64 crorc bamask' row has CR[16] = 0, its destination).  Also: every BA field mask 0..30 (CR[m] = 1),
                    mask 16 included, which repairs R1.
  64 crorc bbread   crorc 30,30,31 over 0xfffffffc: a = CR[30] = 0, b = CR[31] = 0 -> 1 at CR[30] (its own pre-set inverse 0 IS
                    the a = 0 source).  The BB read shifts by 0: every mask m with any bit 2..31 set reads nonzero, !bb = 0, 0
                    (B1, k = 2..31); bit 1 = CR[30] = 0 here, and `& 3' / `& 7' are red on `64 crorc 00' (its BB = 2 read is 2).
  64 crandc setbits crandc 31,30,31 over 0x00000002: a = CR[30] = 1, b = CR[31] = 0 -> 1 at CR[31]; the set shifts by 0, so a
                    literal 1+2^k also sets CR[31-k]: zero in the seed for k = 2..31 (B3 and k = 31); k = 1 lands on CR[30] = 1,
                    the source, and is red on `64 crandc 01' (crandc 10,1,0 sets CR[9] after `crandc 9' cleared it).
  64 crorc setbits  crorc 31,0,31 over 0: a = b = 0 -> 1 at CR[31]; every extra bit CR[31-k], k = 1..31, lands on a zero (B4).

WHY FOUR AND NO FEWER (single-instruction sessions).  The four open families need, respectively: (i) crorc with a = 0, b = 1,
result 0 and CR[16] = 1 (B2); (ii) crorc with a = 0, b = 0 (result 1) and CR[0..29] all 1 so that a BB read shifted by 0 has
bits 2..31 set (B1); (iii) crandc with result 1 and zeros at CR[BT-k] for k = 7, 9, 11..31 (B3); (iv) crorc with result 1 and
zeros at CR[BT-26], CR[BT-27] (B4).  (i) and (ii)/(iv) differ in the result; (ii) needs ones where (iv) needs zeros (the
extra set bits of (iv) at BT-26, BT-27 lie in 0..5 for any BT, inside (ii)'s ones at 0..29, and moving BT below 27 shifts
(iv)'s bits out); (iii) is crandc.  So no single instruction serves two families, and 4 rows is the minimum; a multi-
instruction session would cost more rows (session/others/mfcr/disasm), as the edge session shows.  (The round-2 rows are
kept as measured: they were not the minimum, see r2_20261105/CLOSURE.errata.md.)

## PROOF: the whole 2^32 constant space at the six sites (what the contract may claim beyond the enumerated cells)

A read is a = (cr >> (31-x)) & m with x the field index; call q = cr >> (31-x), whose bit j is CR[x-j] (j <= x, zero above).
  crandc BA (:2732):  the condition `ba & !bb' is bitwise with !bb in {0,1}, so only bit 0 of a counts.  m with bit 0 set:
                      EQUIVALENT (32 of them enumerated here).  m with bit 0 clear: a & 1 = 0, the result is always 0, red on
                      `64 crandc 10' (want 1).  Closed for every m.
  crandc BB (:2733):  `!bb' sees only bb != 0.  `64 crandc bbmask' (BB = 31, q = 0xfffffffe, want 1 needs bb = 0): any m with a
                      bit in 1..31 reads nonzero -> red.  m = 0: bb = 0 always, crandc becomes CR[BA], red on `64 crandc 11'.
                      Closed for every m != 1.
  crorc BA (:2759):   `ba | !bb' sees only a != 0.  `64 crorc baread' (BA = 31, q = 0xfffffffe, want 0 needs a = 0): any m with
                      a bit in 1..31 -> red.  m = 0: a = 0 always, crorc becomes !CR[BB], red on `64 crorc 11'.  Closed.
  crorc BB (:2760):   `64 crorc bbread' (BB = 31, q = 0xfffffffc, want 1 needs bb = 0): any m with a bit in 2..31 -> red; m
                      with bit 1: `64 crorc 00' (q = 2, want 1) -> red; m = 0: bb = 0 always, result always 1, red on
                      `64 crorc 01'.  Closed.
  set literal C (:2736, :2763): cr |= (C << (31-BT)).  C without bit 0: CR[BT] is never set, red on every result-1 row.  C with
                      bit 0 and some other bit j: on the `setbits' rows (BT = 31) the extra bit lands on CR[31-j], a zero for
                      j = 2..31 (crandc) and j = 1..31 (crorc), seen by the whole-CR compare; j = 1 at crandc is red on
                      `64 crandc 01'.  Closed for every C != 1 (and C = 0 is `set deleted').
  The field masks `& 31' (:2730-2731, :2757-2758) are closed over 0..30 by enumeration; a mask with bits above 4 is the fix
  (the field is 5 bits), so the mask sites are closed over every constant too.

## WHAT STAYS UNDETECTED, AND WHY

  - the 36 EQUIVALENT cells above (proved; no row can see them);
  - crandc clear -> toggle (^=): DISCLOSED in the probe's clause (e)(5) (every crandc row with result 0 pre-sets the inverse,
    and the round-3 `64 crandc setbits' row pre-sets 0 with result 1: a toggle of 0 then |= gives 1 too);
  - OUTSIDE the denominator (disclosed, (e)(5)): an extra CLEAR (clear literal 1+2^k).  The round-3 whole-CR rows see some of
    them incidentally (appendix); the rest need ones at non-source, non-destination bits, which the set-literal rows cannot
    carry.  Not claimed.

## PROBE CONTRACT TEXT (clause (e), round 3)

  ROUND 3 (regress/artifacts/ppccrandcorc/r3_20261105/CLOSURE3.md): the four whole-CR rows after the round-2 pins close the
  single-constant space at the four read-mask sites and the two set literals.  COVERED: every read mask `& m' other than the
  fix's at crandc BB, crorc BA and crorc BB (all 2^32 m, by the proof; 1+2^k for k = 1..31 and 0, 2, 4, 6 enumerated and
  simulated), every crandc BA read mask with bit 0 clear; every set literal C != 1 in both handlers (1+2^k, k = 1..31,
  enumerated); the clear/set addressing cells (31-bt) -> (31-ba), (31-bb), bt and the clear moved between the reads.
  DELIBERATELY UNCOVERED: crandc BA read masks with bit 0 set (EQUIVALENT: `ba & !bb' sees only bit 0 of ba); `|=' -> `^='
  at either set (EQUIVALENT after the clear); the read statements swapped (EQUIVALENT); the crandc toggle of (5); an extra
  CLEAR of a non-source, non-destination bit (5).

OLD rows: 62 (table 1), 66 (round 2).  NEW rows: 4 (N = 70).

## APPENDIX (outside the denominator): the clear literal 1 -> 1+2^k, what the 70 rows happen to see

| cell | red on 66 | red on 70 |
|---|---|---|
| crandc clear literal 0x00000003u (1+2^1) | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crandc_setbits,32_crandc_10 |
| crandc clear literal 0x00000005u (1+2^2) | none | none |
| crandc clear literal 0x00000009u (1+2^3) | none | none |
| crandc clear literal 0x00000011u (1+2^4) | none | none |
| crandc clear literal 0x00000021u (1+2^5) | 64_crandc_11,64_others,32_crandc_11,32_others | 64_crandc_11,64_others,32_crandc_11,32_others |
| crandc clear literal 0x00000041u (1+2^6) | 64_crandc_11,64_others,32_crandc_11,32_others | 64_crandc_11,64_others,32_crandc_11,32_others |
| crandc clear literal 0x00000081u (1+2^7) | 64_crandc_10,64_crorc_01,64_others,32_crandc_10,32_crorc_01,32_others | 64_crandc_10,64_crorc_01,64_others,32_crandc_10,32_crorc_01,32_others |
| crandc clear literal 0x00000101u (1+2^8) | 64_crandc_10,64_crorc_01,64_others,32_crandc_10,32_crorc_01,32_others | 64_crandc_10,64_crorc_01,64_others,32_crandc_10,32_crorc_01,32_others |
| crandc clear literal 0x00000201u (1+2^9) | 64_crorc_01,64_crorc_11,64_others,32_crorc_01,32_crorc_11,32_others | 64_crorc_01,64_crorc_11,64_others,32_crorc_01,32_crorc_11,32_others |
| crandc clear literal 0x00000401u (1+2^10) | 64_crorc_01,64_crorc_11,64_others,32_crorc_01,32_crorc_11,32_others | 64_crorc_01,64_crorc_11,64_others,32_crorc_01,32_crorc_11,32_others |
| crandc clear literal 0x00000801u (1+2^11) | none | none |
| crandc clear literal 0x00001001u (1+2^12) | none | none |
| crandc clear literal 0x00002001u (1+2^13) | none | none |
| crandc clear literal 0x00004001u (1+2^14) | none | none |
| crandc clear literal 0x00008001u (1+2^15) | none | none |
| crandc clear literal 0x00010001u (1+2^16) | none | none |
| crandc clear literal 0x00020001u (1+2^17) | none | none |
| crandc clear literal 0x00040001u (1+2^18) | none | none |
| crandc clear literal 0x00080001u (1+2^19) | none | none |
| crandc clear literal 0x00100001u (1+2^20) | none | none |
| crandc clear literal 0x00200001u (1+2^21) | none | none |
| crandc clear literal 0x00400001u (1+2^22) | none | none |
| crandc clear literal 0x00800001u (1+2^23) | none | none |
| crandc clear literal 0x01000001u (1+2^24) | none | none |
| crandc clear literal 0x02000001u (1+2^25) | none | none |
| crandc clear literal 0x04000001u (1+2^26) | none | none |
| crandc clear literal 0x08000001u (1+2^27) | none | none |
| crandc clear literal 0x10000001u (1+2^28) | none | none |
| crandc clear literal 0x20000001u (1+2^29) | none | none |
| crandc clear literal 0x40000001u (1+2^30) | none | none |
| crandc clear literal 0x80000001u (1+2^31) | none | none |
| crorc clear literal 0x00000003u (1+2^1) | 64_crorc_00,64_crorc_10,32_crorc_00,32_crorc_10 | 64_crorc_00,64_crorc_10,64_crorc_baread,64_crorc_bbread,32_crorc_00,32_crorc_10 |
| crorc clear literal 0x00000005u (1+2^2) | 64_crandc_10,64_crorc_00,32_crandc_10,32_crorc_00 | 64_crandc_10,64_crorc_00,64_crorc_baread,64_crorc_bbread,32_crandc_10,32_crorc_00 |
| crorc clear literal 0x00000009u (1+2^3) | 64_crandc_10,64_crorc_00,32_crandc_10,32_crorc_00 | 64_crandc_10,64_crorc_00,64_crorc_baread,64_crorc_bbread,32_crandc_10,32_crorc_00 |
| crorc clear literal 0x00000011u (1+2^4) | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crorc_baread,64_crorc_bbread,32_crandc_10 |
| crorc clear literal 0x00000021u (1+2^5) | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crorc_baread,64_crorc_bbread,32_crandc_10 |
| crorc clear literal 0x00000041u (1+2^6) | none | 64_crorc_baread,64_crorc_bbread |
| crorc clear literal 0x00000081u (1+2^7) | none | 64_crorc_baread,64_crorc_bbread |
| crorc clear literal 0x00000101u (1+2^8) | none | 64_crorc_baread,64_crorc_bbread |
| crorc clear literal 0x00000201u (1+2^9) | 64_others,32_others | 64_others,64_crorc_baread,64_crorc_bbread,32_others |
| crorc clear literal 0x00000401u (1+2^10) | 64_others,32_others | 64_others,64_crorc_baread,64_crorc_bbread,32_others |
| crorc clear literal 0x00000801u (1+2^11) | 64_crorc_01,64_others,32_crorc_01,32_others | 64_crorc_01,64_others,64_crorc_baread,64_crorc_bbread,32_crorc_01,32_others |
| crorc clear literal 0x00001001u (1+2^12) | 64_crorc_11,64_others,32_crorc_11,32_others | 64_crorc_11,64_others,64_crorc_baread,64_crorc_bbread,32_crorc_11,32_others |
| crorc clear literal 0x00002001u (1+2^13) | 64_crorc_11,64_others,32_crorc_11,32_others | 64_crorc_11,64_others,64_crorc_baread,64_crorc_bbread,32_crorc_11,32_others |
| crorc clear literal 0x00004001u (1+2^14) | 64_others,32_others | 64_others,64_crorc_baread,64_crorc_bbread,32_others |
| crorc clear literal 0x00008001u (1+2^15) | none | 64_crorc_baread,64_crorc_bbread |
| crorc clear literal 0x00010001u (1+2^16) | none | 64_crorc_baread,64_crorc_bbread |
| crorc clear literal 0x00020001u (1+2^17) | none | 64_crorc_baread,64_crorc_bbread |
| crorc clear literal 0x00040001u (1+2^18) | none | 64_crorc_bbread |
| crorc clear literal 0x00080001u (1+2^19) | none | 64_crorc_bbread |
| crorc clear literal 0x00100001u (1+2^20) | none | 64_crorc_bbread |
| crorc clear literal 0x00200001u (1+2^21) | none | 64_crorc_bbread |
| crorc clear literal 0x00400001u (1+2^22) | none | 64_crorc_bbread |
| crorc clear literal 0x00800001u (1+2^23) | none | 64_crorc_bbread |
| crorc clear literal 0x01000001u (1+2^24) | none | 64_crorc_bbread |
| crorc clear literal 0x02000001u (1+2^25) | none | 64_crorc_bbread |
| crorc clear literal 0x04000001u (1+2^26) | edge_others | edge_others,64_crorc_bbread |
| crorc clear literal 0x08000001u (1+2^27) | edge_others | edge_others,64_crorc_bbread |
| crorc clear literal 0x10000001u (1+2^28) | none | 64_crorc_bbread |
| crorc clear literal 0x20000001u (1+2^29) | none | 64_crorc_bbread |
| crorc clear literal 0x40000001u (1+2^30) | none | 64_crorc_bbread |
| crorc clear literal 0x80000001u (1+2^31) | none | none |
