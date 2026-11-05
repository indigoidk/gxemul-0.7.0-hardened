# ERRATA for r5_20261105/T5_PREP.md -- records 6, 2026-11-05 (adj_p5_20261105/ADJ_MYTHOS_local.md R3, R6, R7, R8, R9)

T5_PREP.md is not rewritten; each item quotes the sentence it corrects.  Line numbers are T5_PREP.md's.

1. **:4 (superseded premise).**  Quoted: "ruling implemented: p4_20261105/CONS_MYTHOS_local.md section 3 (the closed enumeration L)".
   Correction: CONS section 3 is SUPERSEDED by the pass-5 ruling (ADJ_MYTHOS_local.md section 2).  Its "closed enumeration" was a
   coverage walk, not the fix's floor, and its closure claim ("every access kind in every phase, with a memconf store, a default
   access AND served read-backs after each") is not what the 206 rows do -- T5_PREP's own :90-91 says so, and :70-75 shows the two
   undriven contexts.  The contract now lives in the probe's CONTRACT paragraph (regress/mvme187_memc_probe.py, header).

2. **:34-35 (R3).**  Quoted: "all 81 conjunctions of literals over {W, C, M, D} incl. always ("ANY boolean function" of the ruling,
   restricted to conjunctions: disjunctions, two-bit masks, bit-with-predicate joints and len are the ruling's disclosed OUT-cells,
   not walked)".
   Correction: the walked alphabet is the 81 conjunctions PLUS the TO disjunctions `!x || G` on the two existing latch tests (:38).
   CONS :42 claims "ANY boolean function" and CONS :52's disclosed list names no disjunctions, so arbitrary Boolean gates were
   neither walked nor covered: they are disclosed in the probe's CONTRACT ("disjunctions and other non-conjunctive gates,
   multi-bit masks, len"), not "the ruling's disclosed OUT-cells".

3. **:41-42 (R9, the example).**  Quoted: "VACUOUS 6,676: semantically no-op at the position for every access the function can see
   there (gate unsatisfiable, e.g. `M` inside the memconf latch body; ...)".
   Correction: position MB is AFTER the set `d->warned_memconf = 1;` (memc_variants_5.py:88 SET_M, :116-117 inserts after it;
   reach(MB) keeps only states with M = 1, :688), so inside the memconf latch body `M` is tautological and `!M` is the
   unsatisfiable gate.  The same error is in the walker's docstring (memc_variants_5.py:38-39, "`M` inside the memconf latch body
   before the set"): the body is before the set in the C text, the walk's MB is after it.

4. **:41 (R9, the definition).**  Quoted: "semantically no-op at the position for every access the function can see there".
   Correction: VACUOUS means "no-op under the Boolean-latch abstraction for a SINGLE access": semantic_vacuous (:703-728) evaluates
   one access over Boolean reach states (:716-721, `bool(new) != bool(cur)`).  The 6,676 therefore carry a cross-call caveat:
   `if (idata & 2) D ^= idata` after the default test is discarded because 1 ^ v is nonzero, yet across calls D goes 1 -> 2 (a
   default store of 0x03) -> 0 (a store of 0x02) and the next default access re-announces.  The ungated `M ^= idata` at the memconf
   arm's end escapes the same way (M: 1 -> 2 -> 0 over memconf stores of 0x03 then 0x02) but is NOT inside the 6,676: the walker's
   idata = 1 sample clears a set latch (memc_variants_5.py:698, :716-721), so it was BUILT -- L_ME_M_xori_any, NOCHANGE, 206/206
   (PRETABLE_5.out:7792-7794, SCORES.txt:2917).  On this probe both stay truthy on every session; neither is a semantic no-op.
   (Second reading, rec6 R9: this item first put both among the discarded cells.)  Filed: r6_20261105/FILING_memccoverdebt.md
   item 6.

5. **:49 (R7).**  Quoted: "one per statement for NOCHANGE (148 built for 1,083 groups: fired but changed nothing -- ...)".
   Correction: "fired but changed no field byte and no latch truth value".  memc_variants_5.py:377 and :388-389 compare latch
   TRUTHINESS (`was = bool(cur)` ... `bool(cur) != was`); fields compare exact bytes (:397, :407-408).

6. **:51-52 (R6).**  Quoted: "Cells NOT made into a variant: the 6,676 vacuous (not mutants), the 24,201 RED-EQUIV and 935
   GREEN-NOCHANGE cells (each measured by its built representative; ...)".
   Correction: 6,676 + 24,201 + 935 = 31,812, but 37,974 cells - 3,463 L-walk variants = 34,511.  The green cells are 4,299 (:48),
   665 of them built, so 3,634 green cells are unbuilt.  Their partition, summing each green representative's `equiv (n)` line in
   PRETABLE_5.out:7788-9459: NOCHANGE 148 representatives + 2,406 equivalents = 2,554 cells; UNFIRED 106 + 1,036 = 1,142;
   UNOBSERVED 411 + 192 = 603 (2,554 + 1,142 + 603 = 4,299).  The unbuilt 3,634 are therefore 2,406 NOCHANGE cells and 1,228
   UNFIRED/UNOBSERVED cells.  6,676 + 24,201 + 3,634 = 34,511.  (Second reading, rec6 R6: this item first said "935 NOCHANGE +
   2,699 UNFIRED/UNOBSERVED" -- 935 = 1,083 - 148 counts NOCHANGE GROUPS, not cells, and 2,699 was the remainder.)

7. **:76 (R8).**  Quoted: "UNOBSERVED (411 groups; the statement fired and changed a latch or field, and no later access read it
   back), chiefly:".
   Correction: "fired and changed the state, with no observed difference on the probe, cancellation included".  `changed` is sticky
   (memc_variants_5.py:358 initialised, :388-389 and :407-408 set, never cleared) and UNOBSERVED is "fired and changed, trace
   unchanged" (:779-780, :828).  The summary's DA ob2s, DT ob2s, H ob3c, TL ob3c and TL ob4c entries (PRETABLE_5.out:9579, :9609,
   :9615, :9696-9697) are toggles that WERE read back and cancelled -- T5_PREP's own :84-86 says so of ob2s/ob3c.

8. **:76-88 (addition, not a correction: the "chiefly" list).**  One UNOBSERVED kind the pass-5 ruling's family (b) list also missed:
   `d->warned_memconf = idata` at the memconf arm's end (ME) under `writeflag == MEM_WRITE && !controller` (PRETABLE_5.out:9637
   `ME W.nC`, :9639 `ME W.nC.M`, L_ME_M_idat).  The WRITE test is part of the survivor: ME lies after the memconf arm's write block
   (dev_mvme187.c:105-119), a controller-0 memconf READ has idata 0, so under `!controller` alone the statement clears M on reads
   and is red -- SCORES.txt:570 L_ME_M_idat_nC 201/206 (R3_lines, R3_no_0x5, R9_lines, R12_lines, R16_lines) against :2999
   L_ME_M_idat_W.nC 206/206.  Under W.nC it clears M on a controller-0 memconf store of 0x00, and every such store (R3's second,
   R7's second, R9's third) is the last memconf store of its session, so nothing observes the cleared latch.  Disclosed in the
   probe's CONTRACT under (2); a controller-0 0x00 memconf store in R16's phase 10 closes it (FILING item 1).  (Second reading,
   rec6 F2: this item first wrote the gate as `!controller`.)

9. **:68-70 and :92 (R4, no correction, a clarification).**  :68-69 correctly places the CI/CR idata-bit-8..31 groups outside the
   ruling's alphabet; the ME groups (PRETABLE_5.out:9632-9643) are likewise the walk's superset (:31-32 added ME).  Counted in
   REPRESENTATIVES (the green records at PRETABLE_5.out:7788-9459, one per (statement, deviation set)): UNFIRED 106 = 44
   supplementary (CI/CR under idata bits 8..31) + 62 inside the ruling's alphabet; UNOBSERVED 411 = 21 supplementary (ME) + 390
   inside.  So of the 517 UNFIRED/UNOBSERVED representatives, 452 lie inside CONS section 3's alphabet and 65 are the implemented
   superset.  The 48 (:9461-9508) and 12 (:9632-9643) are counts of (position, gate) SUMMARY LINES, into which green_summary
   (memc_variants_5.py:856-865) expands each representative's members -- :7880-7882 is one representative for all 24 high bits,
   :8017-8019 one ME representative whose W.nC and W.nC.M members appear as two lines (:9637, :9639).  The summary has 58 UNFIRED
   and 179 UNOBSERVED lines in all; and ME also owns 12 NOCHANGE representatives, inside the 148, outside the 517.
   table5/VERDICT.md:16-17 says "517 ... inside the ruling's own denominator"; see ERRATA_table5_VERDICT_20261105.md item 2.
   (Second reading, rec6 R4: this item first said "457 (58 + 399) inside, 60 superset", mixing summary lines with representatives.)
