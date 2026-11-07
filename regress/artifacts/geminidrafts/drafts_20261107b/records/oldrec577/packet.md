# Reading task: oldrec577 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC577-98ab` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #577 shblreset (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 1069-1253 at HEAD 116c5aa9; each line carries its own number -- cite those numbers)

```text
 1069| # `#577` Records (follow-up, 2026-11-03): `shblreset` names its landing commit `bb672a16`; the committed-tree proofs; the pass-2 receipt
 1070| 
 1071| `git ls-tree bb672a16` shows `regress/sh_tlbmulti_probe.py` at `100644 blob 34cf5ea3d4557c5acc0f60d8e1fa4060ce720bca`, blob md5 `fd386f177d33` [corrected 2026-11-03 by `#576`'s follow-up: this block first printed `d41d8cd98f00`, the md5 of EMPTY input] (the shipped revision: AST-identical to the table's as-run copy `d41edccdee1c` with docstrings kept, seven comment-only edits logged in `regress/artifacts/shblreset/killtable_20261102/ASRUN_NOTE.txt`); `src/cpus/cpu_sh.c` md5 `db65b19bab44` [corrected the same way; it first printed `d41d8cd98f00`] (the measured fix source, byte-identical in `est/`; the two-part clearance `regress/artifacts/shblreset/landing_20261102/PREP.out`).  `git diff --numstat bb672a16^ bb672a16`: `4 2 regress/gate_sh_rounding.sh; 60 12 regress/sh_tlbmulti_probe.py; 14 5 src/cpus/cpu_sh.c; 23 1 tools/pipeline/check_probe_wiring.py`; 99 artifact files under `regress/artifacts/shblreset/`.  Gate 10 before the landing: `regress/artifacts/shblreset/landing_20261102/GATE10_RUN.txt` (the `#577` block 10/10; the run's one red the pre-existing gdrom_default 62-vs-60 pin, the peer's uncommitted probe, as in `#572`'s run).  The row's `commits` field now names `bb672a16`; its state stays `held` for Astra's walled pass 1 (re-fired after the 01:10 reset).
 1072| 
 1073| Ledger (the `commits` field and the state note's date), this block, the `regress/pass2_ledger.tsv` receipt line, a landing line in OUTSTANDING_BUGS.md's `#577` section, `matrix.html` and `fable_queue.md` re-rendered.
 1074| 
 1075| # `#577` (2026-11-02) -- `shblreset`: a SuperH general exception taken with SR.BL set stored the power-on reset code, and clobbered the TLB multiple-hit code
 1076| 
 1077| **The defect.**  `src/cpus/cpu_sh.c`, `sh_exception()` (HEAD `987cb596` :910-918): when SR.BL was already set the block printed its
 1078| `fatal()` and then executed `expevt = EXPEVT_RESET_POWER;` for EVERY exception code, under a `/* TODO */`.  The SH7750 manual
 1079| (`_scratchpad/sh7750_hardware.txt`) says a general exception other than a user break taken with BL set performs a MANUAL reset -- 5.5.3
 1080| `:12302-12304`, 5.6.1 (2) `:12376` -- and "Exception code H'020 is set in EXPEVT" (`:12383-12384`; 5.7.2.a `:13164-13166` repeats it as
 1081| H'0000 0020), not the power-on code H'000; and the two TLB multiple-hit exceptions are reset-category in their own right (Table 5.2
 1082| `:12006`, `:12010`) with their own code H'140 (`:12461` instruction side, `:12499` data side), which the block overwrote too -- so the
 1083| `#457` guest-distinguishability comment at `:985-989` ("a multiple hit can be told from a power-on (0x000) or a manual reset (0x020)")
 1084| was false under BL.  Guest-visible consequence: a kernel's reset handler dispatching on EXPEVT read 0x000 for a manual reset and for a
 1085| multiple hit alike.  Upstream residue (the TODO is the 0.7.0 import's).  WRONG-RESULT, MED; no host failure path (`fatal()` only prints,
 1086| `debugmsg.c:384-391`).  Two carriers in the bug file: the id entry `OUTSTANDING_BUGS.md:24063` and the prose row `:8238`.
 1087| 
 1088| **The witness (rung 3).**  `regress/artifacts/shblreset/witness_20261102/sh_blreset_witness.py` on the unmodified in-tree `-E landisk`
 1089| (the rig kernel loaded for construction only), the cold debugger presetting `sr` (MD|BL = 0x500000f0, RB clear) and `pc`, the guest
 1090| executing `trapa #1` (0xc301) or the TLB multiple-hit raiser's path, `expevt`/`pc` read back through the debugger.  On a fresh clone of
 1091| HEAD built in WSL (`/tmp/gxdivw`, binary newer than source): `witness_head.out` RESULT=2/4 -- both failures read H'000 against the wanted
 1092| H'020 and H'140 -- with the liveness control (`bl trapa pc` 0xa0000000, the reset vector) and the BL-clear control (`nobl trapa expevt`
 1093| 0x160) green.  The same script on the fixed clone (`/tmp/gxfix577`, 17:47): `witness_fixed.out` RESULT=4/4.
 1094| 
 1095| **The fix.**  In the BL block, `expevt = EXPEVT_RESET_POWER;` becomes `if (expevt != EXPEVT_RESET_TLB_MULTI_HIT) expevt =
 1096| EXPEVT_RESET_MANUAL;`, and the TODO comment becomes a twelve-line `#577` comment carrying the manual citations above, the reason the
 1097| multiple-hit code is exempt, why a user break never reaches the block (the UBC suppresses it under BL, `:41448-41452`, and
 1098| `EXPEVT_BREAK` has no raiser in this tree -- `sh4_exception.h:73` is its only occurrence), and why an interrupt cannot latch a code here
 1099| (`cpu_dyntrans.c:247` delivers none while BL is set; the intevt path at `:945-947` never stores EXPEVT for an interrupt).  Nothing else
 1100| in `sh_exception()` changes: the `fatal()` stays (its flood is `floodclass`, not this round's), the common tail and the shared reset arm
 1101| (`:1015-1021`) are untouched.  Option set: IMPLEMENT the manual's rule -- the arm already existed and only its constant was wrong; there
 1102| is nothing to DECLINE or FAULT (the exception is legal and the manual says exactly what happens), and DELETE would leave the guest's own
 1103| code in EXPEVT where the architecture mandates H'020.  Diff: `src/cpus/cpu_sh.c` +14 -5 (`killtable_20261102/product.diff`, the
 1104| shipping text; `witness_20261102/product.diff` and its `apply_fix577.py` carry the pre-pass-1 wording of the SAME code -- comment-only,
 1105| and both builds share the binary md5 `b7b0d0b5f5ae` at 17:47 and 18:11), byte-identical in `GXEMUL-SEC` and `est/`.  Every caller of
 1106| `sh_exception()` at HEAD was enumerated at pass 2 (Fable; `git grep`): no caller passes H'000 or H'020 as an exception, so the exempt set
 1107| is exactly {H'140} and every value the fix stores has an arm in the switch -- the fix opens no path to the `default: ... exit(1)` at
 1108| `:1083-1085`.
 1109| 
 1110| **The detector.**  `regress/sh_tlbmulti_probe.py`: `session()` gains `program=`/`steps=` (a short guest program run under a preset `sr`),
 1111| and four rows are appended -- `tlbm bl trapa` (sr 0x500000f0, `trapa #1`, want 0x00000020), `tlbm bl mhit` (the multiple hit under BL,
 1112| want 0x00000140), `tlbm bl ldmis` (`mov.l @r1,r2` = 0x6212 with r1 odd under BL: the misaligned-load code H'0E0 is rewritten, want
 1113| 0x00000020) and `tlbm trapa` (sr 0x400000f0, BL clear, want 0x00000160: the control that pins the general vector's own code and, measured
 1114| post-table, the sole carrier of the guard-side class).  Names stay at 13 characters or fewer (`row()` prints `%-14s`, the gate anchors
 1115| `^$v  .*ok$` with two spaces: the padded-column trap, Grok pass 1).  The docstring's "rewrites ANY expevt" note is historicised.
 1116| Contract (the probe's `#577` comment, final text after three post-table comment-only edits logged in `ASRUN_NOTE.txt`): TRAPA (H'160)
 1117| and a misaligned load (H'0E0) are the two general codes driven; any edit that moves a code between the rewritten set and the exempt set
 1118| ONLY at a code this table does not drive -- H'040-H'0C0, H'100, H'120, H'180, H'1A0, H'800, H'820 -- in either direction is clause-(e)
 1119| disclosure; the identity medium is the REWRITE deleted (the guard and its `fatal()` stay), carried by `tlbm bl trapa` and `tlbm bl ldmis`;
 1120| `tlbm bl mhit` reads H'140 either way and cannot carry it.  `regress/gate_sh_rounding.sh`: `sh_tlbmulti rows run` 6 -> 10 (EQUALITY),
 1121| the four names in the per-row loop.
 1122| 
 1123| **The pre-table check and the kill table** (`regress/artifacts/shblreset/killtable_20261102/`; scratch clones only, a `.MUTANT` sentinel
 1124| per mutant; each `<leg>.raw` names its binary, md5, freshness and -- for the post-table legs -- the instrument's md5):
 1125| 
 1126|     base_head (HEAD)                                              7/10   bl trapa, bl mhit, bl ldmis all 0x000
 1127|     fixed                                                        10/10
 1128|     M_b        the power-on store reinstated verbatim (b)         7/10   the same three (binary md5 == HEAD's)
 1129|     M_c        the rewrite deleted, guard and fatal() kept (c)    8/10   bl trapa 0x160, bl ldmis 0x0e0
 1130|     M_noex     exemption removed (d, body)                        9/10   bl mhit 0x020
 1131|     M_wrongex  exemption on TRAPA instead of the multiple hit     8/10   bl trapa 0x160, bl mhit 0x020
 1132|     M_lt100    exemption widened to every code below 0x100        8/10   bl mhit 0x020, bl ldmis 0x0e0  (predicted 9/10; corrected)
 1133|     M_trapaonly the rewrite keyed to TRAPA only (e)               9/10   bl ldmis 0x0e0
 1134|     M_power    exemption kept, constant wrong (d)                 8/10   bl trapa, bl ldmis 0x000
 1135|     M_guard    the guard widened to MD as well as BL (d, GUARD)   9/10   trapa 0x020   -- post-table leg, predicted 9/10
 1136|     M_resinst  `&& expevt != EXPEVT_RES_INST` added (e)          10/10   TOTAL ESCAPE  -- post-table leg, predicted 10/10
 1137| 
 1138| Floor: (a) 7/10; (b) 7/10 at the binary level (the reinstatement rebuilds HEAD byte for byte); (c): measured at `M_c.raw`; (d) the fix
 1139| DEPENDS ON the dominating predicate `sr & SH_SR_BL` and on the exemption it adds -- body side M_noex, M_wrongex, M_lt100, M_power, guard
 1140| side M_guard (built after the table at Fable's pass-2 ask: until it ran, `tlbm trapa`'s kill was a prediction and that row is the class's
 1141| sole carrier; it matched in score, row and value); (e) the contract above, with M_resinst as the MEASURED member of the disclosed class
 1142| (all three pass-2 seats named it independently, each with a different undriven code: ADDR_ERR_ST, RES_INST, TLB_MISS); (f) not applicable
 1143| (no address decode).  Provenance: `PRETABLE.out` (18:10:13) precedes `KILLTABLE.log`'s start (18:11:05) and was never edited after;
 1144| every correction and both post-table predictions went to the SIBLING file `PRETABLE_CORRECTION.out` -- which was then rewritten at
 1145| each addendum, so its mtime proves only that the last write followed both legs (the F2 pass caught a self-referential mtime clause in
 1146| it; corrected in place, quoting it).  The post-table predictions are pre-leg by other artifacts: the three pass-2 answers that named
 1147| the guard-side and the undriven-code classes (`argon/gemini_web.out` 18:43:04, `grok.txt` 18:53:22, `fable5.md` 19:01:50, the last
 1148| carrying M_guard's "9/10, tlbm trapa reads 0x00000020" verbatim) precede `M_guard.raw` 19:14:12 and `M_resinst.raw` 19:24:09; so do
 1149| `run_mguard577.sh` 19:10:42 and the mutator's M_resinst branch 19:20:21.  Lesson, structural: one file per pre-leg prediction, never
 1150| rewritten -- the lesson `#576` paid for the same day, learned a second time.  The M_lt100 prediction had the
 1151| direction of the sub-0x100 exemption wrong (the correction quotes it); every other prediction matched.  The instrument the table ran is
 1152| preserved as `sh_tlbmulti_probe.ASRUN.py` (copied at run time, md5 `d41edccdee1c`, the file both post-table legs ran); the shipped
 1153| `sh_tlbmulti_probe.py` differs from it by seven comment passages (`ASRUN_NOTE.txt`: the H'020 citation `:678-681` -> `:12383-12384`,
 1154| Grok pass 2; the contract's two directions and "the REWRITE deleted", Fable pass 2; the `sr=` sentence, Fable pass 2; the guard-
 1155| qualification clause, Grok F2; its IMASK wording scoped to the BL rows, Astra; SR.MD added to that clause, Opus F2; SR.FD, agy F2) and by nothing
 1156| else -- the two files' ASTs are identical with docstrings KEPT (the edits are `#` comments; ten `row()` calls each, re-checked at the landing).  The durable copies of the
 1157| table files were first made with plain `cp` (every mtime 18:40) and were re-copied with `cp -p` from the byte-identical `_scratchpad/w577`
 1158| originals at 19:2x, so they now carry the originals' mtimes; Argon's F2 objection that a restored mtime is indistinguishable from a
 1159| fabricated one is recorded here, and the `_scratchpad/w577` copies remain the primary order proof.  The mutator's `M_guard` branch first
 1160| landed with a real newline inside a C string (the heredoc backslash trap, `#576`'s P1 shape), was caught by `ast.parse` before any run and
 1161| repaired with the editor; the preserved `mutate577.py` parses and its seven table branches are byte-unchanged.  No dead session in any
 1162| leg.
 1163| 
 1164| **The panel** (owner roster 2026-11-02: GPT-6 Astra, Fable 5.1, glm-5.3, Argon = Gemini web, Grok 4.7).  Pass 1
 1165| (`_scratchpad/w577/pass1_20261102/`): Argon PROCEED (9 attacks, 9 holds); Grok 4.7 PROCEED WITH CHANGES (3); Fable 5.1 PROCEED WITH
 1166| CHANGES (3); glm-5.3 SEAT DOWN (the Ollama cloud endpoint answers `403 Forbidden, error code 1010` to every model; a 70-byte error file);
 1167| Astra SEAT WALLED (the hotmail login's weekly limit, "try again at Nov 8th 11:24").  Findings F1-F10 and their dispositions are in the
 1168| pass-2 packet's section 0; among them: the comment's citations re-anchored to the manual's body sentences (F4); a row for the misaligned
 1169| load so a sub-0x100 general code is driven (Grok); the four names cut to 13 characters (Grok, Fable); F7's `:1304` for the multiple-hit
 1170| raiser REJECTED with the fact that HEAD has it at `dev_sh4.c:1178-1179` and the working tree's uncommitted additions shift it by 126
 1171| (Grok read the working tree in plan mode); F10 the SLEEP-under-BL filing.  Pass 2 (`pass2_20261102/`, the diff, the block after the edit,
 1172| the detector diff, PRETABLE and the table inlined): Argon 5 attacks / 0 broken / 4 holds / 1 unsettled (the manual lines it cannot read);
 1173| Grok 4.7 SHIP WITH CHANGES (1); Fable 5.1 SHIP WITH CHANGES (3); glm SEAT DOWN (the helper's User-Agent, below); Astra SEAT WALLED through
 1174| the pass and answered at 20:2x after its reset, SHIP WITH CHANGES (3): the probe citation (already done), the contract's exactness (the
 1175| M_c description, both disclosure directions, the SR-state qualifications -- done), and the records sync (both bug-file carriers, "AST-
 1176| identical with comment differences", the IMASK wording scoped to the BL rows since the committed `tlbm sr' row presets IMASK 0, H'120 not
 1177| raisable).  Every answering seat: the code is right
 1178| and complete, every score reconciles with its raw, no floor cell is open; the changes were the guard-side measurement (above), the two
 1179| contract wordings, the records items (the bug file's prose row, the post-table edits, which `product.diff` ships).  The adjudication pass
 1180| (`f2_20261102/`, P1-P18 and D1-D2): Argon 20 attacks / 2 broken / 18 holds -- it overturns P10 (the `cp -p` re-copy, recorded above) and
 1181| D1 (filing the undriven-code class is "unactionable noise" against a contract that already excludes those codes), and its "what we all
 1182| missed" -- that a user break under BL is not exempted -- is REFUTED by the product comment's own two sentences (the UBC suppresses the break
 1183| under BL, `:41448-41452`; `EXPEVT_BREAK` has no raiser, `sh4_exception.h:73` its only occurrence), which the packet-fed seat could not
 1184| check; Grok 4.7 RATIFY WITH CHANGES (1): the clause-(e) sentence could not see a qualification of the GUARD itself (`&& !(sr & SH_SR_RB)`,
 1185| or an IMASK test: every row presets RB clear and IMASK 0xf, while a second exception is taken with RB set), so the contract gains that
 1186| clause as post-table edit 4 (comment-only; unmeasured, no score claimed; cheapest row if ever wanted: `sr=0x700000f0`, `trapa #1`, want
 1187| H'020) and `shblundriven` carries it; P5 REFINED (the prose row's `cpu_sh.c:653` is a stale cite, the block is at HEAD `:910`); D1
 1188| REFINED to FILE (there is no `EXPEVT_TLB_MISS`; the members are `EXPEVT_TLB_MISS_LD` H'040 and `_ST` H'060); P10 and D2 UPHELD against
 1189| Argon; and Argon's user-break exemption refuted a second way -- the switch has no H'1E0 arm, so an exemption added in this block would
 1190| fall into `default:` and its `exit(1)`.  Fable 5.1 adjudicating, F2 VERDICT: RATIFY WITH CHANGES (4), on 3 of 5 rostered seats and provisional on its face -- P1-P16 and P18
 1191| UPHELD (P1, P3, P8, P16 REFINED), P17 OVERTURNED as a record (the self-referential mtime clause, L4, corrected above), D1 UPHELD as
 1192| disclose-and-file with the row refined (the TEN raisable undriven codes H'040, H'060, H'080, H'0A0, H'0C0, H'100, H'180, H'1A0, H'800,
 1193| H'820; H'120 and H'1E0 have neither raiser nor switch arm, so an exemption at either is equivalent; the body-tested partition {H'140,
 1194| other} EXHAUSTED, the code domain within "other" SAMPLED at 2 of 12; both member families), D2 UPHELD; its own AST compare found
 1195| the as-run and shipped probes identical with docstrings KEPT; the NMI half of the deleted TODO (ICR.NMIB, manual `:40308-40317`,
 1196| `:12307-12308`, `:13169-13170`; `dev_sh4.c` models no NMI) is carried by the SLEEP-under-BL filing as the same class; HEAD moved to
 1197| `3cb8bdc1` during the pass (records only; `src/` and `regress/` unchanged since `987cb596`, the two bug-file carriers identical at
 1198| all three); Argon's two overturns rejected on measurement and its user-break claim refuted a third way (`EXPEVT_BREAK` has no arm,
 1199| so a raised break would reach `default:`'s `exit(1)` regardless of BL); GPT-6 Astra F2 (20:3x) RATIFY WITH CHANGES (4), agreeing with Fable on P17 (OVERTURN: a mutable file's mtime proves nothing about its
 1200| earlier contents), D1 (disclose AND file) and D2, refining P1/P3/P8/P10/P16 the same way, and adding the `tlbm sr' IMASK qualification and
 1201| that the misaligned-store row would catch the ADDR_ERR_ST variant but not `M_resinst`; glm SEAT DOWN -- cause found 20:0x the same evening:
 1202| `panel_ollama.py` sent urllib's default User-Agent, which the daemon forwards and Cloudflare bans (403/1010); fixed in the harness
 1203| commit that followed, every cloud seat answering a liveness token afterwards, so the three glm failures in this round were a harness
 1204| defect, not an account state; Astra, walled through all three passes, answered a liveness test at 20:4x on the hotmail login and its
 1205| pass 2 and F2 confirmation were fired then.  **The owner ruled (17:4x) that
 1206| this commit HOLDS until Astra answers**; Astra answered pass 2 and F2 at 20:2x-20:3x and the owner lifted the hold at 22:3x ("Land #577
 1207| now").  **Late seats, fired after the owner's evening rosters** (20:5x: the four Ollama cloud seats and Opus; 21:3x: agy): pass 1 -- GLM 5.3
 1208| PROCEED WITH CHANGES (2), DeepSeek PWC (1), minimax PWC (3), kimi PWC (4): all four held the fix and three of them corrected the brief's
 1209| interrupt-path sentence (the later `expevt = -1` overwrites the local before anything is latched, so the dyntrans gate is load-bearing for
 1210| the pending rule, not for the rewrite -- the product comment's "interrupts do not reach this path" is the true half); Opus 5.5 PWC (4) --
 1211| the BL-clear row and M_guard (done), the `expevt < 0x100` description (done), a second general code (done) and an MD-qualified guard
 1212| disclosed (done at F2), the multiple-hit cite `:12499` beside `:12461` (recorded below), and TEA/PTEH not set on the multiple-hit transition
 1213| (pre-existing `#457`, noted).  F2 -- GLM RWC (4) (P1 refined: M_guard measures one widening, the class's other members are unmeasured; P5
 1214| cannot settle: the prose row's `cpu_sh.c:653` is a stale cite -- marked so in the bug file), DeepSeek RWC (1) (P6: the AST compare kept
 1215| docstrings; the packet's 'once docstrings are dropped' was imprecise -- corrected here), minimax RWC (3) (M_guard-specific wording; H'000/H'020
 1216| absent from the disclosure list, both without a raiser -- D2 covers them), kimi RWC (3) ('sole carrier' holds for the guard operands the rows
 1217| vary), Opus RWC (5) -- P1/P8/P17 leaned on `PRETABLE_CORRECTION.out`'s own mtime (rewritten at every addendum: the pass-2 answers and the
 1218| script mtimes are the order proof, as the pre-table paragraph above already says), stale counts in P6/P10 of the F2 packet, SR.MD added to the
 1219| guard disclosure (probe edit 6, `ASRUN_NOTE.txt`), the `:12499` cite, the `__LINE__` explanation carried to `#578`; agy (gemini-4-argon-high, file-reading, fired 22:4x under the 21:3x roster) pass 1 PWC (3) -- all three already in the
 1220| working tree, which it checked -- and F2 RWC (3): the mtime order proof again, the artifact probe copy lagging edit 6 (synced), SR.FD added to the
 1221| guard disclosure (probe edit 7).  Astra's
 1222| PASS 1 stays OWED (walled at 17:5x; the brief is re-fired after the 01:10 reset by the session's cron) -- the row is `held` for it.
 1223| 
 1224| **Not changed (assessed, intentionally left).**  The unlatched `fatal()` in the BL block floods on every exception under BL (`floodclass`).
 1225| The manual-reset state also re-initialises the on-chip modules and VBR/SR (`:12302-12304`, `:12383`); the model performs none of that
 1226| module initialisation (`shresetinit`, `OUTSTANDING_BUGS.md:23283`), and this round changes only the code it stores.  SPC and SSR are still
 1227| written at `:941-942` where 5.7.2.a (`:13165-13166`) calls them undefined on this path: undefined permits any value.  H-UDI reset stays the
 1228| table's H'000 row with no raiser.  SLEEP under BL never wakes in this tree (`cpu_sh_instr.c:260-263` and `cpu_dyntrans.c:247` refuse under
 1229| BL) where the manual accepts an interrupt in sleep with BL set (`:13170-13171`): filed, not fixed here.  The `#457` comment at `:985-989`
 1230| becomes unconditionally true with this fix.  Two optional product-comment rewordings from pass 2 (Fable: "never stores EXPEVT for an
 1231| interrupt"; a clause that H'000 and H'020 have no raiser today, so a later RESET-pin or H-UDI raiser would need its own exemption) were
 1232| not applied after pass 2; the no-raiser fact is this sentence.
 1233| 
 1234| **Landing.**  Two-part clearance before the commit (`regress/artifacts/shblreset/landing_20261102/PREP.out`, 22:35-22:38): `build/`,
 1235| `build-asan/` and WSL `/tmp/gxsec-build` each cmp CLEAN against SEC with the binary newer than `cpu_sh.c` (`est/`: source tree, part 2 N/A).
 1236| Gate 10 (`gate_sh_rounding.sh`) run end to end on the applied tree with the HEAD-based gate copy in place: REGRESS_FAIL with ONE red that is not this round's: `gdrom_default rows run got=62 want=60` -- HEAD's gate pins gdrom_default at 60 while the working tree carries an uncommitted 62-row `gdrom_default_probe.py` (the peer session's, noted in the checkpoint since 10-25; the identical single red in `#572`'s end-to-end run); the `#577` block read `sh_tlbmulti rows run 10`, `rows correct 10`, every one of the ten names present, control OK (`regress/artifacts/shblreset/landing_20261102/GATE10_RUN.txt`).  The product comment
 1237| cites the multiple hit at `:12461` (the instruction side); `:12499` (the data side, the tree's only raiser) is the sharper cite (Opus) -- both
 1238| carry H'140, left as written.
 1239| 
 1240| **Records.**  `OUTSTANDING_BUGS.md`: the `shblreset` entry (`:24092` at 87a73fdc) AND the prose row (`:8239`, `cpu_sh.c:653` | BL already set ->
 1241| `EXPEVT_RESET_POWER`; its `:653` is a stale cite, said so in the mark) marked fixed by this commit; two filings -- `shsleepblwake` (LOW-MED, WRONG-BEHAVIOUR: a guest that executes SLEEP
 1242| with BL set is never woken by an interrupt in this tree, `cpu_sh_instr.c:260-263` requiring BL clear and `cpu_dyntrans.c:247` delivering
 1243| none under BL, while the manual accepts an interrupt in sleep with BL=1, `:13170-13171`; pass 1 F10, Fable) and `shblundriven` (LOW,
 1244| coverage debt: the measured total escape `M_resinst`, with the member list from pass 2 and the cheapest row -- a misaligned longword store
 1245| `mov.l r2,@r1` 0x2122 with r1 odd under BL, want H'020, the mirror of `tlbm bl ldmis` -- recorded; held for the F2 ruling on D1).  Ledger:
 1246| `shblreset` set `held` (for Astra's walled pass 1), witness `probe:regress/artifacts/shblreset/witness_20261102/sh_blreset_witness.py`, the four
 1247| detector rows named, seat entries per pass naming their dirs (`regress/artifacts/shblreset/pass1_20261102/`, `pass2_20261102/`,
 1248| `f2_20261102/`); the two rows opened.  The gate file is staged from a HEAD-based copy carrying this round's hunk only
 1249| (`#576` is not landing in this commit; the working copy's three unrelated 09-17 hunks stay out and are merged back after); the two-part clearance is run on `build/`,
 1250| `build-asan/` and `/tmp/gxsec-build` (`est/`: source tree, part 2 N/A) and `gate_sh_rounding.sh` run end to end on the applied tree before
 1251| the commit.  Process notes carried forward from `#576` and honoured here: corrections to a sibling of `PRETABLE.out`; the as-run instrument
 1252| preserved at run time; `cp -p` for artifact copies.
 1253| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_577: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC577: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
