# mvme187memcoob -- test-variant table 2: verdict against PRETABLE_2

Instrument: `probe74_frozen.py` (74 rows, md5 e83a52280553). Baseline: `../dev_mvme187.c.fix2`, the final candidate, cmp-equal to
GXEMUL-SEC. Run in the WSL clone /tmp/gxmemc2. Record: `SCORES.txt` in this directory, where every line names its row count
(ADJ_MYTHOS.md M20). `../PRETABLE_2.out` was written first.

**Every predicted red count held.**

- **Legs**: base 74/74, CONTROL=OK, SYMPTOM=ABSENT, ASAN=0. The HEAD leg scored 25/74 with SYMPTOM=PRESENT and CONTROL=OK (predicted
  25/74). /bin/true scored 16/74, an absent binary 2/74 and /bin/false 3/74, each with CONTROL=FAIL.
- **Red: 29 of 29 variants.** All nineteen of table 1, rerun on this instrument (M20), and the ten the adjudication added:
  - T2_D9b_chipid_swap: 69/74.
  - T2_valprint: 71/74.
  - T2_mlatch_perctl and T2_mlatch_ctl1: 72/74 each. Both reddened `R3 lines` as well as `R3 no 0x5` (grok's missed item 1 and
    Opus's M2 note, both measured here).
  - T2_mnotice_ctl0: 73/74.
  - T2_mlatch_hoist: 72/74.
  - T2_dlatch_rd00, T2_dlatch_rd04 and T2_dlatch_rd08: 72/74 each.
  - T2_keepstore: 73/74.
- **Mythos's F1 is measured.** T2_dlatch_rd08, a latch writer on the memconf read path, reddened `R3 lines` and `R3 7c line`, so R3
  already rows that form. The "unrowed, disclosed" sentence it would have replaced is therefore dropped (X1).
- **F2 is measured.** B3 (the indexed read reinstated) scored 71/74, red on exactly R3 7c r4, R8 7c r4 and R8 80 r8: the low byte of
  each latch, read on this little-endian x86_64 host. R4 ff and R8 84..87 read past the 132-byte allocation under B3. PRETABLE_2 marked
  them INDETERMINATE, and they read 0 (green) in this run.
- **CONTROL=OK on every variant.** With the ctl r2 rows reclassified as detector rows (M12), D7, D9 and D10 now red those rows without
  reporting CONTROL=FAIL, which table 1 did.
- **The clone was restored**: cmp clean against GXEMUL-SEC, binary fresh, sentinel cleared (the run log).
