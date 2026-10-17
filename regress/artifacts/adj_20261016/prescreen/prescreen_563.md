# #563 `wdc473floor` -- pre-screen of the grok, grok-reconcile and Argon readings (nine jobs)

Pre-screen seat: Opus 5.5, 2026-10-16. Read-only; this file is the only write. Nothing was built or run except
`git show` / `git log` / `git diff --stat`, `grep`, `md5sum`, `wc`.

**Jobs:** adj_563_ruling, c563_candidates, c563_contract, c563_edges, c563_records, c563_seats, c563_widths,
changelog_563_draft, wdcrearmwalk_tape.

**Seat tags:** `G` = grok's answer (`agypack_20261013/<id>/grok_<id>.txt`); `GR` = grok's reconcile run
(`grok_reconcile_<id>.txt`; the four `.2reads` versions were read for their FOR-THE-ADJUDICATOR sections); `A` = Gemini
Argon (`_scratchpad/gweb/jobs_20261014_argonpack6/<id>/gemini_web.out`, its FLAG lines, BROKEN points and tally, plus
its `HARVEST_ARGON.md` section). agy's answers were opened only to check who a reconcile attributes a claim to. agy's
wdcrearmwalk_tape job never answered (`agy_wdcrearmwalk_tape.err`: 429 quota wall). That job has no reconcile.

**Abbreviations used in the evidence column** (all paths under `GXEMUL-SEC/regress/artifacts/` unless shown):
`R3` = `wdc473floor/repair3_20261013/REPAIR3.c.txt` (md5 246b0840bb43a88478e67925bc982132, verified) ·
`R2` = `wdc473floor/f2_20261009/opus5_r2/REPAIR2.c.txt` · `TABLE3`, `SUMMARY3`, `PRE_N` = `repair3_20261013/{TABLE3.txt,
SUMMARY3.txt, logs/PRE_N_raw.txt}` · `R3PASS` = `wdc473floor/r3pass_20261013/` · `ADJ` =
`wdc473floor/adj_20261013/fable5_563_adjudication.md` (v1 :1-167, v2 :170-206) · `R4SPEC` / `R4ADV` =
`agypack_20261013/repair4_spec/grok_repair4_spec.txt` / `repair4_spec_adv/grok_repair4_spec_adv.txt` · `RULING` =
`wdc473floor/f2_20261009/fable5/fable5_ruling_v2.md` · `ASTRA` = `wdc473floor/f2_20261009/astra_confirm/codex_astra_confirm_v2.txt` ·
`RECADJ` = `recordfix_20261013/adj_20261013/fable5_records_adjudication.md` · `HARVEST` = `agypack_20261013/HARVEST.md` ·
`dev_wdc.c`, `diskimage*.c`, `ledger.json`, `CHANGELOG.md`, `OUTSTANDING_BUGS.md` = `git show e483d931:<path>` (HEAD's
dev_wdc.c md5 714071619d8f98e85fe48ae566139345, identical to the working tree's).

**Disposition sources read:** HARVEST (all); ADJ (all); RECADJ (:1-40, :150-170, :259-276); SUMMARY3, `repair3_20261013/STATUS.md`,
TABLE3 (all runs), PRE_N, R3's contract (:997-1319) and every row cited below, `gate_offline.repair3.sh.txt` (grep);
R3PASS `opus5/{STATUS.md, SCORES.txt}`, `fable5/fable5_r3pass.md`, `codex_rerun/codex_r3pass_records.txt`,
`grok_adversarial_r3pass.txt`; R4SPEC and R4ADV (all); RULING (:34-40, :60-70, :105-145); ASTRA (:48-61);
`f2_20261009/F2_packet.md` (:140-153); `opus5_r2/SUMMARY2.txt`; `close_20261013/fable5/RESULTS.txt` and `fable5_close.md` (grep);
`final_20261009/FINAL_TABLE.txt`; `pass1_20261009/opus5_union.md` (:60-76); `wdcchunking/killtable_20260827/TABLE.txt`;
`wdcrearmzero/review_20261009/` (listing; `opus5_wdcrearmzero.md` :98-101); tools/CLAUDE.md at e483d931 and in the
working tree (greps only).

**Categories.** DISPOSED / LIVE / REFUTED / CANNOT SETTLE as the brief defines them. LIVE is read strictly: the finding
applies to R3 as frozen or to R4SPEC as drafted, and it is in neither R4SPEC's 2 rows and R1-R17 nor R4ADV. Three jobs
(adj_563_ruling, c563_records, changelog_563_draft) are about the records the commit will carry. A finding that still
applies to those records and that no disposition covers is also LIVE, tagged `(records)`. Four findings are live but
lie outside #563's material: a harness tool, the `wdcrearmwalk` row and an upstream doc page. They are tagged
`(outside #563)` and listed separately below. **Evidence marks:** READ means I opened the line or ran the grep.
REASONED means I inferred it from code I read, without a run.

> **CAUTION FOR THE ADJUDICATORS (READ).** The final three-reading reconciles for **c563_records** and **c563_seats**
> swap agy and grok in their disagreement lists. Their file facts are right, but the seat names are reversed. Example:
> "the grok reading's three substitute verdict sentences are not in the seat files". Those three sentences are agy's
> (`agy_c563_seats.txt:58`, `:59`, `:78`), while grok's lines are correct (`grok_c563_seats.txt:48`, `:56`). Likewise
> `ledger.json:50400-50560` is agy's (`agy_c563_records.txt:124`). The `.2reads` versions of both reconciles attribute
> correctly, and so does ADJ v2 point 11 (:196). Every row below uses the corrected attribution. Do not copy seat names
> out of those two final reconciles.

---

## adj_563_ruling

G: 17 flags. GR: 6 disagreements and 5 for-the-adjudicator items. A: 24 substantive and 10 transport flags, tally
105/13 BROKEN/64/28.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, GR, A | RULING:100-101 calls W4 a DATAIN sole cell. It is BE/2/COMPLETED, sole row `write route: COMPLETED store refused` | DISPOSED | READ: ADJ:37 (F13) and :126 (errata list); R3:1093-1095 names W4; TABLE3 `v_W4_495_ex_be2_completed 1/150 1/159` | none beyond the RULING errata already listed |
| 2 | G | ASTRA:7 cites SUMMARY2:36 for W4, but that line only counts W runs | DISPOSED | READ: the attribution is in TABLE3 (v_W4 line) and in ADJ F13's R2TABLE_SUMMARY.txt:78 | cite TABLE3, not SUMMARY2:36 |
| 3 | G, GR, A | Rule D2 is absent from e483d931:tools/CLAUDE.md, and ASTRA's rule links use the parent CLAUDE.md's numbering | DISPOSED | READ: `grep -c 'PINNED AT ITS EDGE'` gives 0 at e483d931 and 1 in the WT; ADJ:176 (v2 pt 1); R3:1131-1133 and :6818 say "not in e483d931's"; R4SPEC R5 | none; cite anchors, never ASTRA's line numbers |
| 4 | G, A | RULING:38-39 ("the owner's ruling today keeps DEPENDS-ON off write targets tested later") and ASTRA:50 ("the owner's write-target exclusion") cite a rule that no carrier text contains | **LIVE (records)** | READ: `write target` / `write-target` has 0 hits in e483d931:tools/CLAUDE.md, the WT tools/CLAUDE.md and the root CLAUDE.md; it is absent from ADJ's errata list (:126) and from R4SPEC | RULING errata should name the warrant actually used (the committed DEPENDS-ON bound, or the 2026-10-09 derived-input ruling), or the owner says where the rule lives. The CHANGELOG must not cite it as carrier text |
| 5 | A, GR | R2:6833-6834 (= R3:7462-7463) cites "CLAUDE.md's clause-(c) ruling of 2026-10-09", which is not in e483d931 | **LIVE** | READ: `WHAT A NULL MEDIUM IS` has 1 hit in the WT tools/CLAUDE.md and 0 at e483d931; R4SPEC R5 lists only R3:1150 and :1212 as uncommitted-ruling citations | extend R5's sentence to R3:7463 (moot if the carrier copy lands in the same commit) |
| 6 | A | RULING:77-78/:109 ask that no residual (d) wording survive, yet R2:1005-1007 and :1014-1015 still tag assignments (d) | DISPOSED | READ: R3:1046-1049 and :1063-1065 split them to (e), bracketed | none |
| 7 | A, GR | RULING:110-112 asked that the `[IDENTITY]` comment be corrected in place. R2 kept the "clause (c)" sentence and appended a bracket | DISPOSED | READ: R3:7458-7463 keeps the sentence with a bracketed correction, which is the carrier's correct-in-place form | none |
| 8 | A | The closure omits the push loops, the #495 guard, `case wd_data` and `writeflag` (RULING:112-115) | DISPOSED | READ: R3:1124-1215 | none |
| 9 | A | The N3 disclosure and the "F4-shaped resets" exclusion that RULING:117-118 and :126 order are absent from R2 | DISPOSED | READ: N3 is rowed (R3:1060-1062, :1196-1198; TABLE3 `p2_N3 0/150 1/159`); R3:1258 carries the exclusion | none |
| 10 | A | "SIX #473 ROWS" is kept with an appended bracket | DISPOSED | READ: R3:1227 is now past tense, and :1234-1235 carries the bracket; ADJ:41 (F17) | none |
| 11 | A | "cite HEAD e483d931" (RULING:120) never landed in R2 | DISPOSED | READ: R3:1132 and :6818 | none |
| 12 | A | The clean-clone gate 2 was not run (RULING:128-129, ASTRA:48) | DISPOSED | READ: `f2_20261009/gate2_clean_20261013/gate2.out:2343` (381 checks); SUMMARY3 "GATE 2 IN A CLEAN CLONE" (REGRESS_PASS, 390 checks) | none |
| 13 | G, GR, A | "Every dispatch arm irq-checked" (RULING:146-147) was not established, because the `res == 0` arm had no row | DISPOSED | READ: R3:7120 adds the row `rejected command: COMPLETED, latched`; its oracle (R3:6687-6688) wants irq 1 and the latch set; contract R3:1069-1073 | none |
| 14 | G, GR, A | P2 `io_enabled`: ASTRA grades it floor, R2 grouped it (e), and RULING never grades it | DISPOSED | READ: ADJ:83 (B.1 item 4); R3:1104-1105 grades it (d); TABLE3 `x_P2 0/150 1/159` | none |
| 15 | G, GR | ASTRA grades P1 (e), but P1 is a dominating guard, not a dispatch label | DISPOSED | READ: R3:1055-1059 rows P1 and records both gradings pending owner rule question 3; ADJ:153 (B.5) | owner rule question 3 (open) |
| 16 | G, GR, A | F4 warrant: ASTRA applies the addition licence to a detector row, and A says RULING:87-88 contradicts that licence | DISPOSED | READ: the licence opens "Additions to product code" (tools/CLAUDE.md, THE ADDITION LICENCE); R3:1090 grades the 2nd-transfer row (e) and does not cite the licence; GR D2 rejects A's reading | none |
| 17 | G | "109 runs = 86 sources" (RULING:122) appears in no named file | REFUTED | READ: `final_20261009/FINAL_TABLE.txt:3` reads "distinct mutant sources: 86 (of 109 runs; 23 duplicate copies)" | none |
| 18 | G, A | "five drop-it seats" (RULING:84) | DISPOSED | READ: ADJ:126 (errata list); SUMMARY3 "NOT DONE HERE" lists it | RULING errata (already listed) |
| 19 | A | RULING:65-66 says five seats (codex, the main loop, glm, deepseek, minimax) applied dominance literally on D3; A calls that unsupported | REFUTED | READ: `f2_20261009/panel_20261009_211021/ollama_glm.txt:14`, `ollama_deepseek.txt:5`, `ollama_minimax.txt:5` and `f2_20261009/codex/codex_astra_f2.txt:33` each take the dominance/floor side | none |
| 20 | G | The I8 prediction miss is in neither SUMMARY2 nor PRETABLE2 | DISPOSED | READ: ADJ:125 (B.3); SUMMARY3 "Records inside REPAIR3 ... I8's miss" | none |
| 21 | G, GR, A | "F18 overturned" (RULING:95-97) loses the LEFT/RIGHT split, and Q5 measured the RIGHT operand | DISPOSED | READ: ADJ:39 (F15) and :126 (errata); R3:1032-1034 spells both predicates | RULING errata (already listed) |
| 22 | G, GR, A | RULING:93 calls Q1 and Q2 measured sole kills, while ASTRA says Q1's sole status is historical; GR says no result file records either | REFUTED | READ: the TABLE3 REPAIR2 column has `p2_Q1 2/150` (shared) and `p2_Q2 1/150`, and TABLE3:96 shows `v_V1` as the sole kill on the completion-ireason row. That is measured, and ASTRA:18 is right | none (ASTRA already corrects RULING:93) |
| 23 | G, A | D2 and the duplicate 32767 push row: the ruling says it is owed, ASTRA says D2 does not mandate it | DISPOSED | READ: R3:1121-1122 keeps the row "held as D2's below-bound edge; no sole kill" | none |
| 24 | A | RULING omits F23 ("160 retained lines") | DISPOSED | READ: ADJ:126 (errata); SUMMARY3 LEGS ("F23 ... lives in the CHANGELOG draft / briefs") | RULING errata (already listed) |
| 25 | A | The closing pass did not build every shape RULING:141-144 names, and kimi's stale-`data_in` shape has no concrete target | DISPOSED | READ: `close_20261013/fable5/RESULTS.txt` has a VG line (`VG_stale_transfer_reused`), which `fable5_close.md:35` calls the ruling's kimi shape; R3 kills `n_F_VG` (TABLE3) | none |
| 26 | A | F2_packet.md:8 says HEAD 23012be9, while the ruling cites e483d931 | DISPOSED | READ: `git diff --stat 23012be9 e483d931 -- src/` is empty | none |
| 27 | A | #473's commit message says 23 rows, while its CHANGELOG and TABLE.txt say 22 | DISPOSED | READ: CHANGELOG.md, #473 block "The archive contradicted itself" (codex found the archived runs at 22 rows; the set was re-derived at 24) | none |
| 28 | A | #473's CHANGELOG says dev_wdc.c is byte-identical in est/build/build-asan, but its OUTSTANDING_BUGS says build-asan was not synced | REFUTED | READ: `git show 1f1a02bb` CHANGELOG +186 is about dev_wdc.c only; the OUTSTANDING_BUGS +154 lines concern other device files (A's own flag says dev_wdc.c matched) | none |
| 29 | A | #473's detector and gate cite `kill473_table.txt`, which was never committed | DISPOSED | READ: `git log --all -- '*kill473_table.txt'` returns nothing; R3:1001-1003; `gate_offline.repair3.sh.txt:1742` | none |
| 30 | A | #473's re-arm comment said "the ring is empty", which was false at 1f1a02bb | DISPOSED | READ: dev_wdc.c:1373-1376 carries the #473 L4 correction. Its residual "no phase guard" sentence is F24, routed to the held #560 batch (ADJ:26 F8, :128; SUMMARY3 NOT DONE) | held #560 batch (already routed) |
| 31 | A | #473's contract says "the rows pin the FIRST re-arm" | DISPOSED | READ: R3:1248-1249 | none |
| 32 | A | 10 transport flags: SUMMARY2, PRETABLE2, RULING_PROVENANCE, the seat files and diskimage*.c are not in the bundle | DISPOSED | READ: all of them exist on disk, and the claims that depended on them are settled in rows 1-31 | none |

## c563_candidates

G: 1 flag plus 7 predictions. GR: 9 disagreements. A: 8 flags, 0 BROKEN.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, A, GR | C1, the re-arm test widened "or data_in_len == 0": no row reds on REPAIR2, because row_odd_zerolen reads only atapi_len | DISPOSED | READ: PRE_N:52 `n_C1_rearm_or_len0 ... [150 rows, 0 failures]`; TABLE3 `n_C1 0/150 2/159`; R3:1039-1045 grades it (e) | none |
| 2 | G, A, GR | C2, `<= data_in_len - 1` on size_t: no row reds; only the zero-length cell differs | DISPOSED | READ: PRE_N:53 gives 150/0; TABLE3 `n_C2 0/150 2/159`; R3:1039-1045 | none |
| 3 | A | A's verdict line says candidates 2 and 5 turn rows red | REFUTED | READ: PRE_N:53 (C2 150/0); A retracts it in its own FLAG (`gemini_web.out:7`); GR D2 | none |
| 4 | A | The contract's `data_in_len - 1` tightening sentence (R2:1008-1011) reads as if `<=` were killed | DISPOSED | READ: R3:1035-1038 covers the strict tightening (killed) and :1039-1045 covers candidate 2 as (e) | none |
| 5 | G, A, GR | C3, the reject-arm steal: no row reds; only the reject latch and a fatal() differ | DISPOSED | READ: PRE_N:54 gives 150/0; R3's no-data oracle now wants `warned_atapi_err == 0` (R3:6684-6685); TABLE3 `n_C3 0/150 1/159`; contract R3:1074-1077 | none |
| 6 | G, A, GR | C4, `relative_addr /= addr_mult` deleted: no row reds because every fixture uses addr_mult 1. The smallest differing input is addr_mult 2 at offset 1 | DISPOSED | READ: PRE_N:55 gives 150/0; TABLE3 `n_C4 0/150 1/159` (the landisk row); R3:1109-1110 | none |
| 7 | GR | agy's and A's "any relative_addr > 0 with addr_mult > 1 diverges" is false: offset 16 reaches `default:` either way | DISPOSED | REASONED (GR D6, dev_wdc.c:2038-2044); no record carries the universal form | none |
| 8 | G, A, GR | C5, the #475 clamp deleted: G says "six rows", A says "7"/"9", GR says nine labels in six functions; the first red is `odd chunk: the count stops at zero` | DISPOSED | READ: PRE_N:56 `9 failures` on REPAIR2; TABLE3 `n_C5 9/150 10/159`; R3:1111-1113; ADJ:182 (v2 pt 4) | none (cite 9 rows in 6 fixtures on REPAIR2, 10 on R3) |
| 9 | G (GR D7) | G says that under C5 "the null-xfer fatal runs in the child" | REFUTED | READ: dev_wdc.c:1312-1316 needs atapi_len == 0, and with the clamp gone it is -2; R3:1943-1945 says the same | none |
| 10 | G, A, GR | C6, `writeflag == MEM_READ && len != 8`: no row reds; an 8-byte read would take the write arm and return eight zero bytes | DISPOSED | READ: PRE_N:57 gives 150/0; TABLE3 `n_C6` survives at 0/159; R3:1305-1311 | none |
| 11 | G, A, GR | C7, `if (!io_enabled)` -> `if (0)`: no row reds, because io_enabled is always 1 and wdc_set_io_enabled is never called | DISPOSED | READ: TABLE3 `x_P2 0/150 1/159`; R3:1104-1105 | none |
| 12 | G | G could not run git show and read `R3PASS/opus5/work/dev_wdc.HEAD.c` instead | DISPOSED | READ: that snapshot's md5 is 714071619d8f..., the same as e483d931's dev_wdc.c | none |
| 13 | GR | agy's PHASE_DATAIN value (0x02) and four of its line cites are wrong | DISPOSED | READ: HARVEST's c563_candidates line routed agy's table to measurement, not to records; ADJ:97-105 (B.2) | none |
| 14 | GR | build() memsets io_enabled to 0 | DISPOSED | REASONED (GR D8): build() never calls dev_wdc_access | none |

## c563_contract

G: 24 flags. GR: 24 disagreements. A: 3 substantive and 12 transport flags, 2 BROKEN.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, GR, A | The (d) tag covers the completion arm's phase change (R2:1005-1007) | DISPOSED | READ: R3:1046-1049; ADJ:38 (F14) | none |
| 2 | G, GR, A | The (d) tag covers the no-data phase change and the `atapi_len = 0` deletion (R2:1014-1015) | DISPOSED | READ: R3:1063-1065 | none |
| 3 | G, GR (A said "corrected") | R2:1028-1029 lumps W4 under (d) with width and byte order and credits it to "the write route rows" | DISPOSED | READ: ADJ:37 (F13) says the (d) tag is right and the wrong record is RULING:100-101; R3:1093-1095 names W4's cell and its sole row | none |
| 4 | G, GR (A said "corrected") | F18's two predicates are not spelled out (R2:1005-1007, :6618-6621) | DISPOSED | READ: R3:1032-1034 spells `atapi_len < data_in_len` and `received < atapi_len`; ADJ:39 (F15) held the LEFT/RIGHT wording sufficient, and R3:7247-7249 keeps it | none |
| 5 | G, GR (A said "corrected") | "the write route" is listed among the synthesised rows after the driven ones (R2:1093-1095) | DISPOSED | READ: R3:1242-1252 (bracketed correction) | none |
| 6 | G, GR, A | "SIX #473 ROWS" (R2:1077) still stands; does an appended annotation cure it? | DISPOSED | READ: R3:1227 is now past tense, with :1234-1235; ADJ:41 (F17) | none |
| 7 | G, GR | "re-quoted ... FOUR TIMES ... a ledger row title, that row's only entry, a CHANGELOG block and a commit message" is unverified | REFUTED | READ: ledger.json:26476 (the entry that quotes it); :26486 (the correction, "repeated four times in one day"); commit f42d747d (`git log --grep='still UNBOUNDED'`). "Only entry" was true when written on 2026-08-30 | none |
| 8 | G, GR | "no such file was ever committed" (kill473_table.txt) is unverified | REFUTED | READ: `git log --all -- '*kill473_table.txt'` returns nothing, so the claim is true | none |
| 9 | G, GR | "swept 23 rows clean" (R2:985-986) has no source | REFUTED | READ: CHANGELOG.md #473 block: "MEASURED: 23 rows, 0 failures. A clean sweep" | none |
| 10 | G, GR | "swept 24 rows clean" and the ASan heap-buffer-overflow READ (R2:987-989) have no source | REFUTED | READ: `e483d931:regress/diff_wdc_identify.c:993-1001` records Opus's #473 pass-2 measurement and its ASan negative control | none |
| 11 | G, GR | "One weakening of each was MEASURED" (R2:1036-1037) | DISPOSED | READ: R3:1135-1137 replaces it ("every one-token move named here was BUILT and MEASURED", TABLE3) | none |
| 12 | G, GR | `res == 1`'s widening is tagged (e) and attributed to D3 as "floor by dominance, (e) by the label clause", while F2_packet rules it floor | REFUTED | READ: the credited RULING:62-70 grades `res == 1` (e) and carries both gradings. F2_packet.md:146-148 was the proposal it overruled. R3:1066-1068 matches the ruling | none |
| 13 | G, GR | "D3 grades the three NOT ROWED selectors P1, P2, P6" (R2:1064-1065) | DISPOSED | READ: the sentence is gone from R3's contract (only a history line remains in the io row, R3:6924); P1 and P6 carry both gradings (R3:1055-1059, :1069-1073); P2 is (d) at :1104-1105 | none |
| 14 | G, GR | R2:991-1033 claims "measured killed" without naming a table for the clamp moves and operand swaps, the refill and arm index edits, the k values, `== PHASE_DATAIN`, the completion irq (E1), S1, and the #495 zero-value, COMPLETED and atapi_st cells | DISPOSED | READ: R3:1018-1019 points at TABLE3, which scores each one killed: o1_ra_*, o1_aa_*, fb_M*, o1_rc_op_recv, o1_ac_op_recv; o1_O_frozenj/halfj/revwalk, o1_ri_2j/jmask255/plus1; o1_O_armfrozen, o1_ai_*, o1_c_arm_idx2j; p2_E1-E5; fb_Ej; v_V1; p2_S1; p2_G1-G5, G7, G11, G12 | none |
| 15 | GR | R2:1011-1012 credits k = 4096 to the 1-left row, but F2_packet:36-37 says the long-transfer row caught it | REFUTED | READ: TABLE3 `p2_E4_recv_plus4096 2/150 2/159` reds both `re-arm: last chunk of a long transfer` and `re-arm: 1 left re-arms as DATA-IN` | none |
| 16 | G, GR (A: holds) | "the R-rows below, which call the primitive DIRECTLY and assert the refusal" is false of R5, R7 and R8 | **LIVE** | READ: R3:1230-1231 still says it, while R3:5242 says "R7 and R8 cover the BULK arm, which bypasses wdc_addtoinbuf() entirely" and R5 drives the sink through the handler; the sentence is not in R4SPEC R1-R17 | REPAIR4 records batch: bracket-correct R3:1230-1231 (R1, R2, R4 and R6 call the primitive directly; R5 goes through the handler; R7/R8 cover the bulk arm) |
| 17 | GR | The "still UNBOUNDED" bullet stands beside its "FALSE AT HEAD" annotation | DISPOSED | READ: R3:1218-1241 keeps it as the quotation source, annotated, in the quote-what-you-refute form | none |
| 18 | A | `SCSI_MAX_XFER_BYTES` = 64 MiB (R2:1113-1114) is unsupported | REFUTED | READ: diskimage_scsicmd.c:59 `#define SCSI_MAX_XFER_BYTES (64*1024*1024)` | none |
| 19 | A | 12 transport flags: TABLE.txt, PRETABLE2.out and the R2TABLE logs are not in the bundle | DISPOSED | READ: those files exist, and the claims are settled in rows 8-15 | none |
| 20 | G | G read the working-tree dev_wdc.c rather than running git show | DISPOSED | READ: the working-tree dev_wdc.c md5 is 714071619d8f..., the same as e483d931's | none |
| 21 | GR | agy's line numbers (D23) and its `atapi_len <= 0` cite (D24) are wrong | DISPOSED | READ: agy's audit was harvested for flags only; R3:1274 lists `<= 0` as EQUIVALENT; TABLE3 `o2_re_len0_le 0/159` | none |

## c563_edges

G: 21 flags. GR: 14 disagreements and 5 for-the-adjudicator items. A: 14 flags, 14 BROKEN.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, GR, A | The closure omits `switch (relative_addr)` / `case wd_data` | DISPOSED | READ: R3:1140-1143 | none |
| 2 | G, GR, A | The closure omits `writeflag == MEM_READ` (:1197) and the idata selector `writeflag == MEM_WRITE` (:1179) | DISPOSED | READ: R3:1144-1147; `R3PASS/fable5/fable5_r3pass.md:42` traces the :1179/:1180 moves to `CDB: six BE words arrive in order`, and its :102 leaves them as optional sentences | none |
| 3 | G, GR, A | The closure is scoped to #473's two sites, so #495's guard conjuncts are absent | DISPOSED | READ: R3:1124-1126, :1204-1215; R4SPEC R6 already rewrites the "dominators are the arm's" wording | none |
| 4 | G | A one-step of the write-side `byte_order == EMUL_LITTLE_ENDIAN` (:1579) moves no row | REFUTED | READ: `LIVENESS: the LE arm really ran` stores 0x34, 0x12 and wants the LE order (R3:3895; GR D13) | none |
| 5 | G, A | The closure omits the byte-order tests (:1200, :1579) and the write-side `switch (len)` (:1580, :1614) | DISPOSED | READ: R3:1212-1215 lists the labels #495's refusal skips, and :1177 the `!badlen_this` carrier; :1200 is a reconverging read-side statement (fable5_r3pass.md:102; R4SPEC:84) | none |
| 6 | G, GR | A `case 3:` that accepts width 3 in CMDOUT passes every row. `a rejected width issues no command` stores width 8, and no width-3 store is rowed | **LIVE** | READ: no `case 3` mutant appears in any `*.diff` under wdc473floor/ (grep: 0); R3:1177 and :1215 cover width 8 and the refused phases only; R4SPEC R3 names the read-side width edits, not the write side | REPAIR4 records batch: add one (e) sentence beside R3:1177 (the accept set is upstream of `badlen_this`, whose two cells are both rowed), or build the one-line mutant and record its score |
| 7 | G | The closure omits `if (d->data_debug)` (:1216, :1486) | DISPOSED | READ: dev_wdc.c:1216, :1486 is a debug print on a reconverging path, not a dominator per ADJ:23 (F5) and :180 (v2 pt 3) | none |
| 8 | G, A | The closure omits #475's `consumed > atapi_len` | DISPOSED | READ: R3:1154-1155 | none |
| 9 | G, A | The closure omits both push loops (:1460, :1797) | DISPOSED | READ: R3:1170-1171, :1202-1203 | none |
| 10 | G, A | The closure omits `while (inbuf_len < 0)`, and both its edges are unrowed | DISPOSED | READ: R3:1185-1189 discloses it (e); R4SPEC R4 replaces its wrong "a CDB never wraps" reason | none |
| 11 | G | The closure omits the free test (:1733), the CDB copy loop (:1739) and the opcode compares that set cmd_len (:1747-1749) | DISPOSED | READ: dropping the free is VG (R3:1078-1079; TABLE3 `n_F_VG 0/150 1/159`); :1739 is at R3:1190-1191 and R4SPEC R11; :1747-1749 is R4SPEC R7 (`cmdlen_ms10` 0/159) | none |
| 12 | G | The closure omits the data-unexpected latch test (:1498-1500) | DISPOSED | READ: dev_wdc.c:1498-1505 is a latched host fatal() on a reconverging path, not a dominator (ADJ:23, :180) | none |
| 13 | G, GR, A | `inbuf_len == 12` has no row at 11, and the overshoot row sits at 14, not 13 | DISPOSED | READ: R3 adds rows `CDB: 11 waits, 12 dispatches` and `CDB: occupancy 13 does not dispatch` (R3:1100-1103, :1183-1184; TABLE3 `n_E_disp12_or11`, `_or13` 1/159) | none |
| 14 | G, GR | `received < data_in_len` coverage is credited to "the refill rows" | DISPOSED | READ: R3:1166-1167 names the 1-left, completion and zero-length rows | none |
| 15 | G, GR, A | The `re-arm: >32768 left` fixture comment says "68930 remain", but the compare sees 68928 | **LIVE** | READ: R3:837 still says 68930 while R3:6241 says the clamp meets 68928; OUTSTANDING_BUGS.md:24607 lists remainder 68930; no ADJ, R3PASS, R4SPEC or R4ADV text names it | REPAIR4 records batch: R3:837 -> 68928 at the compare (68930 before the read); correct OUTSTANDING_BUGS.md:24607 in the commit |
| 16 | G, GR | The read-arm flag's "NOT ROWED" covers only `if (1)` | DISPOSED | READ: R3's P1 row (R3:1055-1059, :1149) | none |
| 17 | G, GR | `!io_enabled` is "NOT ROWED"; its writers include bus_pci.c's PCI command write | DISPOSED | READ: R3's io row (R3:1104-1105, :1139) | none |
| 18 | G, GR | `res == 0` is "NOT ROWED", and pkt_cdb_case stays green under `if (0)` | DISPOSED | READ: R3's rejected-command row (R3:1069-1073; oracle R3:6687-6688) | none |
| 19 | G | `== PHASE_DATAIN` is credited to "the stray read" right beside the wedge row, and DATAOUT is unrowed | DISPOSED | READ: R3:1162-1165 | none |
| 20 | G, GR | The no-transfer fixture's PHASE_DATAIN is synthetic, and widening the latch's `atapi_len == 0` to 1 moves no row | DISPOSED | READ: R3:1964 (#556: "a synthetic packet command state"); R3:1156-1158 (`<= 1` EQUIVALENT; TABLE3 `n_E_nlen0_le1 0/159`) | none |
| 21 | G, GR, A | The guard's `atapi_len == 0` has no row at its past edge, 1 | DISPOSED | READ: R3 adds `re-arm guard: 1 left does not fire` (R3:1050-1052, :1160-1161; TABLE3 `n_E_rlen0_le1 0/150 1/159`) | none |
| 22 | G, GR | `<= 1` on that guard reds `write route: 1-byte store is refused` on REPAIR2 (GR D7 rules "RIGHT: grok") | REFUTED | READ: PRE_N:18 `n_E_rlen0_le1 ... repair2 rc=0 [150 rows, 0 failures]`, as ADJ:25 (F7) predicted from the constant 0xc3 fill | none |
| 23 | G, GR | The product comment at dev_wdc.c:1660-1674 ("NOTHING RESETS THE PHASE") is stale since #479 | DISPOSED | READ: routed to the held #560 `src/` batch (ADJ:26 F8, :128; SUMMARY3 NOT DONE HERE) | held #560 batch (already routed) |
| 24 | G, GR | The detector's stale-phase row still says the phase is not reset (R2:2608-2609, :2625-2631) | **LIVE** | READ: R3:2778 ("NOTHING RESETS THE PHASE") and R3:2818-2819 ("the phase is NOT reset, which is the state under test") are present tense next to the row's own oracle correction (R3:2822ff), and dev_wdc.c:917-918, :938 contradict them. The quoted pre-#479 code is legitimate provenance. ADJ F8 judged the correction note enough; R4SPEC lacks it | REPAIR4 records batch: bracket-correct R3:2778 and :2818-2819 in place (the carrier rule says a re-pinned oracle beside an uncorrected claim reads as laundering) |
| 25 | A | `bound_arm_case` never asserts atapi_len or the guest count, so "either side" is unsupported | REFUTED | READ: it asserts occupancy (R2:6152), which an arm-clamp move changes (GR D14); TABLE3 `o1_aa_32767`, `o1_aa_32769`, `fb_M2d_arm_relax32769`, `fb_M3c_arm_lower32766` are all killed | none |
| 26 | A | The zero-length, non-NULL `data_in` cell is never walked through the arm | DISPOSED | READ: R3's zero-length DATA-IN row (N3; R3:1060-1062, :1196-1198) | none |
| 27 | A | #495's DATAOUT cell is unrowed, and row_midxfer_phases checks only stub_frees | DISPOSED | READ: R3:1208-1211 and :1291-1293 disclose it (e); p2_G6 and p2_G14 survive | none |
| 28 | A | The width-3/8 exemption of #495 is unrowed although warned_badlen is observable | DISPOSED | READ: R3:1295-1296 discloses it (only the latch differs; `v_V5` 0/159); whether a latch counts as a channel is R4SPEC open question 2 | none |
| 29 | A | The swap of #495's flag to atapi_st is held only when write_in_progress != 0 | DISPOSED | READ: R4SPEC:65 (G8): the body is empty, so no clause-(2) swap exists, and the guard's own swap is held (TABLE3 `p2_G7 1/159`) | none |
| 30 | GR | agy's phase values, its #495 line, its PKT producer and its io_enabled cites are wrong | DISPOSED | READ: HARVEST ("Opus VERIFIES the enumeration at build"); ADJ:162 (reversal 4) | none |
| 31 | GR | Re-arm remainder 32769 is reachable only through an IDE tape's variable READ | DISPOSED | READ: F2_packet.md:149-152 (D4); diskimage_scsicmd.c tape arm (a byte count when cmd[1] bit 0 is clear) | none |
| 32 | GR | Grade the closure against every if/switch/loop, including compares whose both arms reach the site | DISPOSED | READ: ADJ:23 (F5) and :180 (v2 pt 3) rule reconverging statements out; R4SPEC:84 | none |

## c563_records

G: 6 flags. GR: 9 disagreements. A: 14 flags, 2 BROKEN.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, GR, A | The brief's premise is wrong: HEAD has no "5 failures of 145", and its notes are the 128-row zero-failure text | DISPOSED | READ: HARVEST (c563_records); ADJ:45 (F18, BRIEF DEFECT) | none |
| 2 | G, GR | The notes' number: 6 of 150 (REPAIR2) or 6 of 159 (R3) | DISPOSED | READ: `repair3_20261013/notes/NOTES3_*.diff` carry "6 failures of 159" (SUMMARY3 DELIVERED); `R3PASS/opus5/STATUS.md:11` re-measures 6/159 on 246b0840 | none (the commit lands R3's figure) |
| 3 | G, GR | There are two gate-2 receipts, 376 (7c42a272) and 381 (0f5807b8), and wrapper.log has no total | DISPOSED | READ: `gate2_clean_20261013/gate2.out:2343` gives 381; the commit's receipt is R3's 390 (SUMMARY3) | cite gate2.out, not wrapper.log |
| 4 | G, GR, A | "30 survivors" against FINAL_TABLE's 10 runs / 9 distinct; the tables must be kept apart | DISPOSED | READ: SUMMARY2.txt:35-38 (193 runs: d145 129, REPAIR2 163, 30 survivors); FINAL_TABLE.txt:3-10; RULING:120-122 | none |
| 5 | A | 150, 6, 163/193, 129, 30, HEAD 150/0, 485, the gate PASS counts and the `<= 12` breach are not found | DISPOSED | READ: a packet gap; they are at SUMMARY2.txt:5, :30-31, :35-38, :53; close RESULTS.txt:6-10; gate2.out:2343 | none |
| 6 | A | 485 null-medium errors contradicts 445 | REFUTED | READ: different builds: opus5_union.md:27 is the pass-1 union and SUMMARY2.txt:53 is REPAIR2; R3's is 537 (SUMMARY3 LEGS) | none (each count names its run) |
| 7 | A | opus5_union.md:182, "24 of 148 ... the other 116", does not add up | REFUTED | REASONED: 24 + 8 + 116 = 148, the same shape as gate_offline.sh's 24 + 8 + 96 = 128 (GR D6) | none |
| 8 | A | check_probe_wiring.py:145 is the CLASSES tuple | REFUTED | READ: at e483d931 :144 is the tuple and :145 is blank | none |
| 9 | GR | The final reconcile attributes `ledger.json:50400-50560`, "exists solely" and the 381 gloss to grok | REFUTED | READ: they are agy's (`agy_c563_records.txt:124`, `:147`); grok cites `:26140` (`grok_c563_records.txt:47`); the `.2reads` reconcile attributes them correctly | do not cite the final reconcile's seat names |
| 10 | GR | agy's census of committed "5 failures" lines is incomplete | DISPOSED | REASONED (GR D7): no record carries agy's census | none |

## c563_seats

G: 15 flags. GR: 8 disagreements. A: 13 substantive and 2 transport flags, 3 BROKEN.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, GR, A | The adjudication-pass and closing-pass codex.txt are content-filter refusals that were scored "answered" through quoted verdicts | DISPOSED | READ: ADJ:49-50 (F19, F20), :140, :143 (B.4); seatverdictrefusal v3 adopted (RECADJ v2.1; HARVEST 23:1x) | records commit (v3 scorer) |
| 2 | G, GR, A | The 284-byte kimi 403 wall is scored as a "format miss" | DISPOSED | READ: ADJ:51 (F21); RECADJ v3 adds the kimi wall phrase (HARVEST 23:1x; a stronger kimi control is owed) | records commit |
| 3 | G, GR, A | deepseek's 712-byte BREACH is marked SUSPECT/"no answer", falls below check_seats_read's 800-byte floor, and its own body says NOT CHECKABLE | DISPOSED | READ: ADJ:52 (F22), :143 (record by hand), :102 (B.2 item 4: the BREACH is over-graded, the row is right); RECADJ:153 (item 2 remedy) | the commit unit records it by hand |
| 4 | G, GR | SEATS.txt and SEAT_VERDICTS.txt give different byte counts for seven closing seats | **LIVE (outside #563)** | READ: `e483d931:tools/pipeline/seat_verdicts.py:354` labels the column "bytes", but :361 reads the file as decoded text and :535 prints `len(t)`. The ledger figures are settled, because ADJ B.4 uses wc -c | a one-line harness fix: print os.path.getsize, or relabel the column |
| 5 | G, A | grok's VERDICT sits mid-line, and agy wraps its VERDICT in backticks | DISPOSED | READ: ADJ:56 (F26); close SEAT_VERDICTS.txt:3 scores agy "BREACH answered" | none |
| 6 | G, GR | Ledger row wdc473floor has no entries, so section G is empty for it | DISPOSED | READ: ADJ:53 (F23); the commit unit writes B.4 | commit unit |
| 7 | G, GR | The pass-1 copy exists; the copies are not set-identical (the F2 copy lacks the .err files, and the closing copy adds two files) | DISPOSED | READ: ADJ:198 (v2 pt 12) | none |
| 8 | GR | The final reconcile says "the grok reading's three substitute verdict sentences are not in the seat files", and credits grok with codex.txt:4323, "not duplicated", seat_verdicts.py:480/:486-488, check_seats_read.py:25 and precommit_check.sh:177 | REFUTED | READ: all of those are agy's (`agy_c563_seats.txt:21`, `:58-59`, `:78-79`, `:127`, `:133`), while grok's lines are correct (`grok_c563_seats.txt:48`, `:56`); the `.2reads` reconcile and ADJ:196 attribute them correctly | do not cite the final reconcile's seat names |
| 9 | GR | A's line spans are wrong: codex :1088, agy's end lines, and a fourth kimi line | REFUTED | READ: the close kimi.txt has 3 lines (wc -l); the other spans follow GR D8 | none |
| 10 | A | No readable seat file carries the refusal string, and 32 files could not be read | DISPOSED | READ: a packet gap; the two refusals are row 1 | none |

## c563_widths

G: 4 flags. GR: 4 disagreements. A: 3 substantive and 1 transport flag, 0 BROKEN.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, GR, A | "every other row issues a FOUR-byte read" (R2:1421-1423) is false | DISPOSED | READ: R3:1611-1621 carries the bracket in ADJ v2 pt 5's wording | none |
| 2 | G (GR .2reads) | The `wdcoddstep` comment calls `consumed` "what the reads actually POP", but it counts pop attempts | **LIVE** | READ: R3:1449 has no bracket. dev_wdc.c:1229-1245 says `consumed` "counts ATTEMPTS too -- row wdcconsumedattempts" (ledger.json:37303, open, med). R4SPEC R1-R17 lacks it | REPAIR4 records batch: bracket R3:1449 ("pop ATTEMPTS; see wdcconsumedattempts") |
| 3 | G (GR .2reads; A on the contract variant) | Row comments still describe the pre-#495 write arm: "pushes guest bytes with NO PHASE CHECK" and "a len-3 write pushes ZERO bytes -- the width switch's `default:` arm only latches" | **LIVE** | READ: R3:1996-1998 and R3:2172-2173 have no bracket, while the same claim at R3:919 carries "[#563: true when written; since #495 ...]". dev_wdc.c:1576-1578 refuses first, and these rows' stub_frees oracle cannot tell which refusal fired. R4SPEC lacks it | REPAIR4 records batch: bracket both the way R3:919 is |
| 4 | G | The IDENTIFY read at R2:3906 (width 2, atapi_len 0) never reaches the clamp | DISPOSED | READ: this agrees with the measured C5 census (TABLE3 `n_C5`) | none |
| 5 | G, GR | #475 clamp: eight sites, with six fixtures (nine labels) red and two green | DISPOSED | READ: PRE_N:56 (9 on REPAIR2); TABLE3 (10 on R3); R3:1111-1113 | none |
| 6 | A | "all 8 red if the clamp is deleted" | REFUTED | READ: the no-transfer row and the stray CDB read stay green (R3:1943-1945; SUMMARY3 C5) | none |
| 7 | G, A, GR | The only width-1 reads are the 32768 in the 1-byte write-route case | DISPOSED | READ: R3:1151-1152; `codex_r3pass_records.txt:120-129`; the fable5_close finding-2 erratum (ADJ:127) | none |
| 8 | GR | write_route_case's drain endpoints; agy's cylinder and BE-arm cites | DISPOSED | READ: `codex_r3pass_records.txt:120-129` (width census); agy's cites reach no record | none |
| 9 | A | `R4 fifo` pops through wdc_get_inbuf, not through the handler | DISPOSED | READ: it is a direct-primitive row by design (R3:5323) | none |
| 10 | A | dispatch_result_case reads CYL for DATA-OUT but never asserts it | DISPOSED | READ: R4SPEC R14 (R3:6591-6594, :6694); `codex_r3pass_records.txt:100` | R4SPEC R14 |
| 11 | A | `stub_byte_order` defaults to 0 | DISPOSED | READ: SUMMARY3 HYGIENE (EMUL_BIG_ENDIAN in rep_fresh, bound_arm_case and row_arm_overrun) | none |
| 12 | GR | agy misquotes pass-2 ollama_kimi.txt:7, and A's "78 rows" disagrees with its own table's 87 | DISPOSED | READ: ADJ:31 (F10); A's count reaches no record | none |

## changelog_563_draft

G: 15 flags. GR: 11 disagreements and 5 for-the-adjudicator items. A: 14 flags, 6 BROKEN.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G | git show was refused, so the house style came from the working-tree CHANGELOG | DISPOSED | REASONED: affects style only, no record | none |
| 2 | G, GR | 25 duplicates and 84 behaviours (the union) do not reconcile with 23 duplicates and 86 sources (FINAL) | DISPOSED | READ: FINAL_TABLE.txt:3 is computed by source, while opus5_union.md:67 is a hand count on the pass-1 union; RULING:120-122 keeps the counts apart | cite FINAL_TABLE |
| 3 | G | PASS2_brief.md:27 says every pass-1 seat said BUILD WITH CHANGES, but grok-adversarial said ESCAPE | DISPOSED | READ: ADJ:134 (B.4 pass 1) lists grok adversarial as ESCAPE | none |
| 4 | G | RULING:12 calls the F2 codex.txt a refusal, "but that phrase is not in the panel file" | REFUTED | READ: `ERROR: This content was flagged` occurs twice in both copies (grep -c = 2; codex.txt:4329-4330) | none |
| 5 | G, GR | The closing SEAT_VERDICTS credits codex with a SPLIT verdict built from quoted strings | DISPOSED | READ: ADJ:50 (F20), :143 (B.4): a seat failure, answered by `codex_rerun/codex_close.txt` | none |
| 6 | G | fable5_close.md:123's 381 checks are cited to wrapper.log | DISPOSED | READ: the count is at gate2.out:2343 | cite gate2.out |
| 7 | G, GR | P2's grade is unsettled between ASTRA (floor) and fable5_close (disclosed) | DISPOSED | READ: ADJ:83 (B.1 item 4); R3:1104-1105 | none |
| 8 | G, GR | grok-adversarial-close's 150-row claims were reasoned, not run | DISPOSED | READ: they were measured later: PRE_N:52-54 (C1, C2, C3 each 150/0) | none |
| 9 | G, GR | The flagship did not adopt the codex re-run's N3 BREACH | DISPOSED | READ: ADJ:62-72 (section C) upholds it as FLOOR; TABLE3 `p2_N3 0/150 1/159` | none |
| 10 | G, GR | R3, its pass 2 and the adjudication supersede "REPAIR3 is owed"; agy writes "151 rows" | DISPOSED | READ: SUMMARY3 (159 rows); `R3PASS/opus5/STATUS.md`; the block's TO-MEASURE section is superseded | rebase the block on R3 and REPAIR4 |
| 11 | G, GR | RULING:124-126 says the BE case-4 byte-lane shift is "Filed", but no ledger slug exists | **LIVE (records)** | READ: no lane or case-4 row exists in the WT or e483d931 ledger (greps; wdc ids listed); SUMMARY3's NOT DONE HERE list omits it; R3:1312-1318 discloses the 4-byte accept lanes (V6) as (e) | commit unit: file it as coverage debt, or add "Filed" to the RULING errata |
| 12 | G | Seat line anchors were not re-checked | DISPOSED | REASONED: no record effect | none |
| 13 | G | The eight 0-of-128 variants have no logs among the named artifacts | REFUTED | READ: `wdcrearmzero/review_20261009/{fable5_meas, opus5_meas}`, which ledger.json:62366 names | cite that directory |
| 14 | GR | "eight one-token variants" (the PASS2/CLOSE briefs and the ledger title at ledger.json:62365) vs CHANGELOG.md:197-198, "four one-token moves ... four content variants" | **LIVE (records)** | READ: Opus's content variants are not all one-token (`opus5_wdcrearmzero.md:98-101`: `+ j` dropped, `+ j/2`, `- j`, `j` -> `0`) | the #563 block uses the committed split; the commit unit, which writes the wdc473floor row, may correct its title |
| 15 | G | CLOSE_brief.md:32 places ASTRA's confirmation under astra/ | DISPOSED | READ: the file is `astra_confirm/codex_astra_confirm_v2.txt` (ADJ:140) | none |
| 16 | G | The "5 failures of 145" notes are still separate | DISPOSED | READ: R3's NOTES3 diffs say 6 of 159 | none |
| 17 | GR | agy's pass-1 verdict counts and its 22-edit partition are wrong | DISPOSED | READ: ADJ:134 (B.4) carries the values from the files | none |
| 18 | GR | The null-medium counts differ by run (436 / 445 / 485) | DISPOSED | READ: SUMMARY2.txt:53 gives 485, opus5_union.md:27 gives 445, and R3's is 537 (SUMMARY3) | each count names its run |
| 19 | GR | D3: `data_in != NULL` is floor and `res == 1` is (e) | DISPOSED | READ: RULING:62-70 | none |
| 20 | A | 68930 vs 68928 (OUTSTANDING_BUGS.md:24607, det137.c:776) | **LIVE** | the same item as c563_edges F15 | see c563_edges F15 |
| 21 | A | Under fake_cpu's byte_order 0, `&& byte_order != EMUL_BIG_ENDIAN` on #495 escaped the 128-144-row detectors | DISPOSED | READ: SUMMARY3 HYGIENE; TABLE3 `o1_g_notBE 5/150 5/159` | none |
| 22 | A | The detector and gate_offline.sh:1740-1741 cite a ghost `kill473_table.txt` ("8 of 8") | DISPOSED | READ: R3:1001-1003; `gate_offline.repair3.sh.txt:1742` | none |
| 23 | A | The shipped contract says the write arm pushes with no phase guard and that the rows pin the FIRST re-arm | DISPOSED | READ: R3:1248-1249 and the bracket at R3:919; the two row comments still without a bracket are c563_widths F3 | see c563_widths F3 |
| 24 | A | "32769 is unreachable at the re-arm; the smallest remainder above 32768 is 33280" | REFUTED | READ: an IDE tape's variable READ takes a byte count (diskimage_scsicmd.c tape arm); F2_packet.md:149-152 (D4) | none |
| 25 | A | Opus's scratch PROPOSED.diff left "want 128" in the identity printf | DISPOSED | READ: the diff was scratch only; R3's identity row checks 159 (R3:7466) | none |
| 26 | A | grok's pass-1 `+`-to-OR combiner escape is equivalent on every reachable state | DISPOSED | READ: R3:1276-1278 (EQUIVALENT; `o1_ri_bitor` and `p2_I1` survive) | none |
| 27 | A | The bundle was truncated at F17 | DISPOSED | REASONED: a transport limit, no record | none |

## wdcrearmwalk_tape

G: 5 flags and 11 facts. A: 3 flags, 2 BROKEN. agy hit a 429 wall. No reconcile exists.

| F | seats | claim (one line) | category | evidence | proposed disposition |
|---|---|---|---|---|---|
| 1 | G, A | An IDE tape is attachable (`it:`, or a bare `t:` on IDE-default machines), ATAPI_PKT_CMD is not gated on a CD-ROM, and a tape READ can set data_in_len above 65536 | DISPOSED | READ: diskimage.c:1699-1712 (default disk type); diskimage_scsicmd.c tape arm (a 24-bit byte count, times the block size when cmd[1] bit 0 is set; 64 MiB cap); F2_packet.md:149-152 (D4); R3:1242-1252 keeps the walk OUT OF CONTRACT (filed) | none |
| 2 | G (A: unsettled) | No in-tree guest or rig attaches an IDE tape | DISPOSED | READ: regress/*.sh has no tape prefix (grep: 0); the row already says "no witness exists" (ledger.json:26691) | none |
| 3 | G, A | The row's ranking ("no witness exists, the single crossing is the one a real driver takes most often") omits that the probe's own `ciR:` CD-ROM reaches multi-re-arm transfers through READ(10) with more than 128 blocks | **LIVE (outside #563)** | READ: diskimage_scsicmd.c READ(10) arm, `retlen = (cmd[7] << 8) + cmd[8]` and `size = retlen * logical_block_size` (512), 64 MiB cap; the shipped probe asks for 128 blocks (G fact 10) | wdcrearmwalk row: record the reachable command; a rung-3 multi-crossing walk can be built on ciR: |
| 4 | G | The state_note says a later chunk overruns "when head + 32768 == 262656 after eight drained chunks", but 8 x 32768 = 262144, so head 229888 is 7 chunks + 512 | **LIVE (outside #563)** | READ: ledger.json:26688; the text came from commit d894e35d; the seat's original wording was not located | wdcrearmwalk row: correct or qualify the arithmetic |
| 5 | G | The 2026-10-09 sentence "any transfer length is reachable on an IDE tape" is false, and it appears in no record | DISPOSED | READ: the phrase exists only in the brief; F2_packet.md:149-152 states it precisely (a BYTE count when cmd[1] bit 0 is clear) | none |
| 6 | G | doc/misc.html says `-d t4:mytape.img` makes SCSI id 4 a tape, but on an IDE-default machine it is an IDE tape | **LIVE (outside #563)** | READ: doc/misc.html:254-256; diskimage.c:1699-1712 | file a LOW doc row (the text is upstream) |
| 7 | A | dev_wdc.c's "MEASURED band [65537, 262655]" implies that transfers stop at 262655 | REFUTED | READ: dev_wdc.c:1362-1367 reports the band over which #473's pre-fix defect was measured, not a length bound | none |
| 8 | A | The row's "COVERAGE DEPTH, not a live defect" is contradicted by reachability | REFUTED | REASONED: reachability is not a defect, and no file shows a second re-arm misbehaving (G §REASONED); the reachability fact is F3 | none |

---

## LIVE items for the adjudicators

Fourteen distinct items. changelog_563_draft F20 is the same item as c563_edges F15, so it appears once. None of them
is floor: every item below is a records correction or a clause-(e) sentence, and none adds a row. They are absent from
R4SPEC's two rows, from R1-R17, and from R4ADV.

**In R3 as frozen (ride the REPAIR4 records batch):**
1. c563_edges F15: R3:837 says "68930 remain", but the compare sees 68928 (R3:6241 says 68928). OUTSTANDING_BUGS.md:24607 carries 68930 too.
2. c563_contract F16: R3:1230-1231 says "the R-rows ... call the primitive DIRECTLY". That is false for R5 (through the handler) and for R7/R8 (bulk arm, R3:5242).
3. c563_widths F2: R3:1449 calls `consumed` "what the reads actually POP", but it counts attempts (dev_wdc.c:1229-1245; ledger row `wdcconsumedattempts`).
4. c563_widths F3: R3:1996-1998 ("NO PHASE CHECK") and R3:2172-2173 ("default: arm only latches") describe the pre-#495 write arm without the bracket that R3:919 carries.
5. c563_edges F24: R3:2778 ("NOTHING RESETS THE PHASE") and R3:2818-2819 ("the phase is NOT reset") stand uncorrected next to the row's own oracle correction. Note that ADJ F8 judged that correction note sufficient.
6. adj_563_ruling F5: R3:7462-7463 cites the uncommitted 2026-10-09 clause-(c) ruling. Add it to R4SPEC R5's list of uncommitted-ruling citations.
7. c563_edges F6: a `case 3:` that widens the write-side accept set in CMDOUT is unnamed and was never built (0 `case 3` mutants). It needs one (e) sentence beside R3:1177, or a measured mutant.

**In the records the commit carries:**

8. adj_563_ruling F4: RULING:38-39 and ASTRA:50 cite an owner's "write-target exclusion" that has no text in any carrier. Add it to the RULING errata, or have the owner name where the rule lives.
9. changelog_563_draft F11: RULING:124-126 says the BE case-4 byte-lane shift is "Filed", but no ledger row exists. File it as coverage debt, or add it to the errata.
10. changelog_563_draft F14: "eight one-token variants" (the ledger title at ledger.json:62365 and two briefs) disagrees with the committed CHANGELOG.md:197-198 split of four one-token moves and four content variants.

**Outside #563's material:**

11. c563_seats F4: `tools/pipeline/seat_verdicts.py:354` labels its column "bytes" but prints `len(t)` of decoded text (:361, :535).
12. wdcrearmwalk_tape F3: the `wdcrearmwalk` row's ranking omits that the probe's own `ciR:` CD-ROM reaches multi-re-arm transfers through READ(10) with more than 128 blocks.
13. wdcrearmwalk_tape F4: the `wdcrearmwalk` state_note arithmetic ("head + 32768 == 262656 after eight drained chunks", ledger.json:26688) is inconsistent.
14. wdcrearmwalk_tape F6: `doc/misc.html:254-256` says `t4:` means SCSI. On IDE-default machines it is an IDE tape.

## Counts

| job | DISPOSED | LIVE | REFUTED | CANNOT SETTLE | total |
|---|---|---|---|---|---|
| adj_563_ruling | 26 | 2 | 4 | 0 | 32 |
| c563_candidates | 12 | 0 | 2 | 0 | 14 |
| c563_contract | 13 | 1 | 7 | 0 | 21 |
| c563_edges | 26 | 3 | 3 | 0 | 32 |
| c563_records | 6 | 0 | 4 | 0 | 10 |
| c563_seats | 7 | 1 | 2 | 0 | 10 |
| c563_widths | 9 | 2 | 1 | 0 | 12 |
| changelog_563_draft | 21 | 3 | 3 | 0 | 27 |
| wdcrearmwalk_tape | 3 | 3 | 2 | 0 | 8 |
| **all** | **123** | **15** (14 distinct) | **28** | **0** | **166** |

Of the 15 LIVE rows, 8 apply to R3 as frozen (7 distinct, because changelog_563_draft F20 duplicates c563_edges F15),
3 to the commit's records, and 4 lie outside #563's material. CANNOT SETTLE is 0 because every checkable claim was
checked. By a mechanical count of the evidence column, 157 rows rest on READ evidence and 8 on REASONED evidence
(c563_candidates F7, F14; c563_records F7, F10; changelog F1, F12, F27; wdcrearmwalk_tape F8). The remaining row,
changelog F20, is a pointer to c563_edges F15.
