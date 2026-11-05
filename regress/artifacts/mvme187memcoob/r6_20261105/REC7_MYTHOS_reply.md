VERDICT: all ten findings UPHELD and corrected; zero-floor disposition unchanged; text-only proof PASS.

- R1 upheld: R16/R17 read each field once per controller (probe :586-599, :636-637); header now says "one readback per field per controller" (:32).
- R4 upheld: re-counted from PRETABLE_5.out:7788-9459: 517 representatives = 452 inside + 65 supplementary (44 CI/CR high-bit UNFIRED, 21 ME UNOBSERVED); 48/12 were summary lines. Fixed in all three ERRATA, NOTE table, FILING headers, plus the NOCHANGE-by-statement exception.
- R6 upheld: 3,634 unbuilt green = 2,406 NOCHANGE + 1,036 UNFIRED + 192 UNOBSERVED equivalents (sums verified); ERRATA_T5_PREP item 6 fixed.
- R9 upheld: ungated `M ^= idata` at ME is L_ME_M_xori_any, built, NOCHANGE 206/206 (PRETABLE:7792, SCORES:2917); only the bit-1-gated D example is VACUOUS. Fixed in probe CONTRACT, both ERRATA, FILING item 6.
- F1 upheld: idata-bit and VACUOUS cells were walked (PRETABLE:18-20, walker:791-795); CONTRACT now says "nonvacuous", names the supplementary alphabet under family (1), splits WALKED-BUT-NOT-CLOSED from NOT WALKED.
- F2 upheld: ME is after the write block (dev_mvme187.c:105-119); SCORES:570 nC 201/206 vs :2999 W.nC 206/206. W.nC restored in probe, ERRATA_T5_PREP item 8, NOTE (d), FILING 2(vi); NB4's controller exclusion added to FILING's universal sentence.
- F3 upheld: pc now +20 alone / +28 with 2(i) readbacks (five instructions after the F5 fix), 0x100b4 to 0x100c8/0x100d0.
- F4 upheld: r9 is 0xff in R12 (probe :509); source now r5/r9, second value 0xffffff00, two latch states (R12 and R17 phase 01); claim narrowed to a sketch.
- F5 upheld: complementary pairs 0x07-then-0x00 (phase 10) and 0xff-then-0x00 (phase 11); R18 gains readbacks after its 0x07 store.
- F6 upheld: R9's controller-1 stores are followed by chipid/chiprev reads (:440-447); fixed to its third store; added lone 0xff byte stores for ob3c/ob4c, a second R9 default read for the DB nW.C.M cases, an extra controller-1 chipid read in R17 for L_CI_M_xor1 C.D.

Text-only proof re-run: TEXTONLY_CHECK=PASS, exit 0 (check 1 EQUAL, 836/836 constants, the same three note strings differ, now at :323/:342/:430). Gate patch re-dry-run applies; gate_arm.sh md5 unchanged.

Files touched: regress/mvme187_memc_probe.py (docstring only); in r6_20261105/: the three ERRATA files, FILING_memccoverdebt.md, RECORDS6_NOTE.md (new section 6 "SECOND READING"), gate_memc_comment.patch, TEXTONLY_PROOF.txt, each with a .pre_rec7 copy; new mvme187_memc_probe.py.pre_rec7 and .rec7.diff.
