MYTHOSRECMEMC6

VERDICT: RECORDS 6 DONE, text-only proof PASS; probe contract now states the floor and discloses the five debt families (plus one group the ruling's own list missed), errata filed for all three sources, gate comment change staged as a patch.

- R1: probe REPAIR 5 paragraph (:29-41) rewritten from the closure claim to what R16/R17 and the tails do, naming the three missing contexts; CONS section 3 marked superseded in ERRATA_T5_PREP item 1.
- CONTRACT (probe :43-79): the ruling's section-2 text, tightened where PRETABLE_5.out's summary refutes it: the keep sentence excluded NB3/NB4 (:9616, :8199), "(2)" regained "a latch written from an arm that does not read it", "1 ^ v stays true" qualified (false for v = 1), and `M = idata` under !controller at ME (:9637, :9639) added as debt the ruling's (b) list never named.
- Clause (e) (:81-133): table 5 is now the record (3,575 / 2,798 red reps / 665 green all predicted / 3,518-56-1 variants); 148-row numbers kept as history; HEAD 29/206 and null media 27/4/5 from SCORES.txt:1-5.
- R2: R16 comment (:569-571) and R17 comment (:622) now read as the lists do (controller 1 gets one store per field).
- R3, R6, R7, R8, R9: ERRATA_T5_PREP_20261105.md items 2-7 (alphabet, 34,511 arithmetic, truth-value wording, cancellation, `!M` at MB and the single-access VACUOUS caveat); R8/R9/R4/R10 also in ERRATA_PRETABLE_5_20261105.md.
- R4, R5, R10: ERRATA_table5_VERDICT_20261105.md (457 inside / 60 superset; 3,518 match once the five legs are removed; NB4's representative is in the 665 as NOCHANGE).
- +0x7c: `rd 0x7c` (:313), `R3 7c r4` (:332) and R8 (:412-415, :420) now say past memcreg, on the latches inside struct mvme187_data.
- Proof: `python -I textonly_check.py probe frozen` gives check 1 EQUAL (placeholdered ast.dump identical, 117,162 chars both) and check 2 exactly three differing string constants, all row notes; TEXTONLY_CHECK=PASS (TEXTONLY_PROOF.txt). A first version of the script false-passed by mutating the tree in place; caught and fixed, recorded.
- gate_memc_comment.patch: 206 rows / fifteen sessions / table 5 as record; hunk regenerated with diff, dry-run applies at :2087 with no fuzz, gate_arm.sh itself untouched (md5 7947…).
- FILING_memccoverdebt.md: six items (five families plus the cross-call caveat), each with its untested context and concrete rows (R16 phase-10/11 stores, tail readbacks, R10 memconf store, R17 third word store, new R18/R19 sessions), registers checked against every init list.
- Departure stated plainly: the AST proof and the patch dry-run were RUN (read-only python -I, scratch copy); nothing ran against the emulator or tree.
- Files touched: edited regress/mvme187_memc_probe.py; wrote r6_20261105/{mvme187_memc_probe.py.pre_r6, .r6.diff, textonly_check.py, TEXTONLY_PROOF.txt, ERRATA_T5_PREP_20261105.md, ERRATA_PRETABLE_5_20261105.md, ERRATA_table5_VERDICT_20261105.md, gate_memc_comment.patch, FILING_memccoverdebt.md, RECORDS6_NOTE.md}.
