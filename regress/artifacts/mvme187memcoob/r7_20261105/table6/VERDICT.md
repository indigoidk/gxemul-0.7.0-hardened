# mvme187memcoob -- test-variant TABLE 6 (repair 6: session R18, 213 rows), 2026-11-05 12:42:44Z-13:04:45Z

Driver `../table6_memc.run.sh` (a frozen copy of table6_memc.sh), WSL scratch clone /tmp/gxmemc8 under a clone-local .MUTANT;
restored to GXEMUL-SEC and rebuilt fresh, sentinel cleared (../table6_run.log).  Instrument `probe213_frozen.py` (md5
1d69cc4e6cb1499894fdf1fcbe3049bd).  `../PRETABLE_6.out` (12:41:39Z) and its machine form PRED_MAP_6.txt predate every table output.
Scores: SCORES.txt (673 lines, each ending in the probe's sentinel); tally: TALLY.txt.

## MISSES AGAINST PRETABLE_6 (one)

* **B3_idx_read (a leg), SCORES.txt:8.**  Predicted exactly R3_7c_r4, R8_7c_r4, R8_80_r8, R11_180_r4 (table 5's measured set,
  carried).  Measured those four plus **R17_f3_r2**: 0xd8 where 0x0 is wanted (probe_B3_idx_read.out; transcript
  sessions_B3_idx_read/R17.txt, `ld.bu r2,r3,0xf3` then `r2 = 0x000000d8`).  Under B3 the default-arm load at +0xf3 returns the
  byte at that offset of the device struct, 111 bytes past its 132-byte allocation.  Table 5's B3 run read 0x0 there.  One B3
  binary run three times (../b3repeat/, md5 in MD5_B3_binary.txt) read 0x66, 0x34 and 0x15: the value varies run to run.
  PRETABLE_6 was right that R18 adds no B3 row (no R18 row is red under B3) and wrong to carry the 206-row set as exact.
  B3 is red in every run, on the same four rows each time.

No other miss: every other leg and all 665 variants matched their exact predictions.

## RESULTS

* Legs: base 213/213 CONTROL=OK SYMPTOM=ABSENT; HEAD 29/213 SYMPTOM=PRESENT; /bin/true 28/213, an absent binary 4/213,
  /bin/false 5/213, each CONTROL=FAIL; B1 81/213, B2 42/213 (both SYMPTOM=PRESENT); B3 208/213 (above).  SCORES.txt:1-8.
* The eight own-latch variants (each 206/206 in table 5 and in ../step1/SCORES.txt): each **212/213, red on R18_lines alone**,
  as predicted (SCORES.txt:9-16).  R18 lines read 4 under the four ungated toggles and 3 under the other four
  (probe_<name>.out; sessions_<name>/R18.txt).
* Table 5's 665 green representatives: **24 red, 641 green**, every red set exactly as predicted.  The 24: the eight; four more
  own-latch toggles at the head and tail (L_H_D_xori_D, L_TL_D_xori_D, L_H_M_xori_M, L_TL_M_xori_M); six tail toggles PRETABLE_5
  classed UNOBSERVED (L_TL_M_xori_ib5c, L_TL_D_xori_nM, L_TL_M_xori_ob4c, L_TL_D_xori_W.nM, L_TL_D_xori_nC.nM,
  L_TL_D_xori_W.nC.nM) -- all eighteen on R18_lines; and six memconf keeps on R18_08_r4 (K_MB_memconf_and_D, K_DT_memconf_and_ib0s,
  K_DB_memconf_and_ib0s, K_DA_memconf_and_ib0s, K_H_memconf_xor_nC.M.D, K_H_memconf_xor_W.nC.M.D).  By PRETABLE_5 class: 16
  NOCHANGE, 8 UNOBSERVED red; 132 NOCHANGE, 106 UNFIRED, 403 UNOBSERVED green.
* Build failures 0; text not found 0.  An independent recheck of all 673 lines against PRED_MAP_6.txt agrees: one disagreement,
  B3's extra R17_f3_r2.
