# table2/VERDICT.md -- errata (2026-11-05, round 3; pass 3 = ../../p3_20261105/codex_codex_r575_p3.txt)

VERDICT.md is the measurement record of table 2 and is not rewritten (nor SCORES.txt, MD5.txt or TABLE.log).  Each item quotes
what it corrects.  No score changes.

## R4 -- m5-m10 are not all single-bit field masks

VERDICT.md says:

> m5-m10 (single-bit field masks, codex's B5-B9 and one more)

Five of the six remove one bit of the 5-bit field mask `& 31` (11111): m5 crandc BB `& 29` (11101) and m8 crorc BA `& 29`, m9 crorc
BB `& 29` remove bit value 2; m6 crandc BB `& 27` (11011) removes 4; m7 crandc BB `& 23` (10111) removes 8.  m10 crandc BB `& 17`
(10001) removes THREE bits, values 2, 4 and 8.  Correct reading: "m5-m9 single-bit field masks (codex's B5-B9); m10 a three-bit one".
The predictions and scores of all six are unaffected (SCORES.txt; ../PRETABLE_2.out).

## R5 -- the earliest file in table2/ is not MD5.txt

VERDICT.md says:

> `../PRETABLE_2.out` (02:08:00 local) predates every file in this directory (the earliest, MD5.txt, 02:10:46)

The earliest file in table2/ is probe66_frozen.py, 02:10:35.403 local (08:10:35.403Z); then cpu_ppc_instr.c.fix575, 02:10:46.645;
then MD5.txt, 02:10:46.732 (ls --full-time, 2026-11-05).  PRETABLE_2.out, 02:08:00.006, predates all three, so the claim that the
predictions precede the table stands; only the parenthetical naming MD5.txt as the earliest file was false.
