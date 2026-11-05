# ERRATA for r5_20261105/table5/VERDICT.md -- records 6, 2026-11-05 (adj_p5_20261105/ADJ_MYTHOS_local.md R4, R5, R10)

table5/VERDICT.md is the table's verdict of record and is not rewritten; each item quotes the sentence it corrects.  Line numbers
are VERDICT.md's.

1. **:11 (R5).**  Quoted: "3,575 variants (112 from table 4 + 3,463 L-walk representatives): PRED=match 3,523, PRED=atleast-ok 56,
   PRED=MISS 1, build failures 0, text-not-found 0."
   Correction: 3,523 + 56 + 1 = 3,580, which is 3,575 variants plus the five control legs -- SCORES.txt:1-5 (base, HEAD,
   null_true, null_absent, null_false) each carry PRED=match and TALLY.txt counts them.  For the VARIANTS: 3,518 PRED=match, 56
   PRED=atleast-ok, 1 PRED=MISS (D7_fold, detected 175/206).  The legs: 5 of 5 as predicted (:9-10 stands).

2. **:16-17 (R4).**  Quoted: "the representatives of the 517 predicted SURVIVOR groups inside the ruling's own denominator (UNFIRED
   106, of which 58 in-bound; UNOBSERVED 411)".
   Correction: 452 of the 517 representatives are inside CONS section 3's alphabet (62 UNFIRED and 390 UNOBSERVED); 65 are the
   walk's implemented superset -- 44 UNFIRED representatives at CI/CR under idata bits 8..31 (T5_PREP.md:68-69; 48 summary lines,
   PRETABLE_5.out:9461-9508) and 21 UNOBSERVED representatives at ME, the position the walk added (12 summary lines, :9632-9643;
   T5_PREP.md:31-32).  The quoted "of which 58 in-bound" is the count of ALL UNFIRED summary lines (:9461-9518), 48 of them the
   supplementary CI/CR lines; the in-bound UNFIRED representatives are 62, in 10 summary lines (:9509-9518).  The 665 = 517 + 148
   NOCHANGE stands.  (Second reading, rec6 R4: this item first said "457 (58 + 399) / 60", counting summary lines as groups.)

3. **:18-19 (answered).**  Quoted: "Whether those cells are floor cells owed rows, or clause-(e) coverage debt under the 09-04 floor
   bound, is the question pass 5 and the next ruling must answer."
   Answered by adj_p5_20261105/ADJ_MYTHOS_local.md: ZERO floor families, FIVE debt families -- every green family lies outside the
   repair paths' own guard-by-state product (the memconf path's {write, !M} x {memconf, M}; the default path's {default arm, !D}
   x {D}; each served arm x its own field).  The round closes on pass 5's denominator; the debt is filed with its remedies
   (r6_20261105/FILING_memccoverdebt.md) and the probe's header now carries the contract and the disclosures.

4. **:21-22 (R10).**  Quoted: "NB4 -- an `&=` keep under !controller, which PRETABLE_5 classes NOCHANGE, so the tally does not
   report it as a survivor although it passes every row."
   Correction: "NB4 -- an `&=` keep under !controller at the first memconf store: its representatives (K_MB_chiprev_and_D and
   K_MB_memconf_and_D, with nC and W.nC among their listed equivalents, PRETABLE_5.out:8199 and :8211) are among the 665 green
   variants, classed NOCHANGE and so absent from the UNFIRED/UNOBSERVED survivor summary."  The tally does report them -- inside
   its 665 (TALLY.txt:8) -- under a class name the summary at :9460 does not list.  Probe-relative: every controller-0 first
   memconf store the rows make (0x07, 0xff, 0xffffffff) leaves chiprev 0x01 and memconf 0x03 unchanged under `&=`; a 0x00 first
   store would zero both.
