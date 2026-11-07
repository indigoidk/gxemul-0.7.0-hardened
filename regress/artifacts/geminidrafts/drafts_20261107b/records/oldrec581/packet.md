# Reading task: oldrec581 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC581-b170` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #581 mvme187memcoob (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 464-622 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
  464| # `#581` Records (follow-up, 2026-11-05): `mvme187memcoob` names its landing commit `03d97106`; the committed-tree proofs; the pass-2 receipt
  465| 
  466| `git ls-tree 03d97106`, md5s hashed in Python from the committed bytes: `src/devices/dev_mvme187.c` blob `de48f59b48ec`, md5 `97e983872a72`; `regress/mvme187_memc_probe.py` blob `1557a378ed93`, md5 `cd3e95ca72a7`; `regress/gate_arm.sh` blob `1f52059a98aa`, md5 `cbb9d843cffd`; `tools/precommit_check.sh` blob `6c252e5b5baa`, md5 `538bb143d2b1`.  The working copy against each: dev_mvme187.c same; mvme187_memc_probe.py same; gate_arm.sh plus other rounds' uncommitted blocks (fbsdrampair's footbridge rows, pvrrenderexit's old pvr block), nothing of #581's (4 hunks); precommit_check.sh plus two other rounds' uncommitted manifest raises (1 hunk(s)).
  467| 
  468| No tree swap was needed for this round (`dev_mvme187.c` carried only #581's change), so there is no restore record.
  469| 
  470| The row's `commits` field names `03d97106` and its state note names the landing commit.  The `regress/pass2_ledger.tsv` receipt line for `03d97106`, a landing line in OUTSTANDING_BUGS.md's `#581` section and `matrix.html` re-rendered complete this records commit.
  471| 
  472| # `#581` (2026-11-05) -- `mvme187memcoob`: the MVME187 memory controller no longer ends the emulator on a memconf store or an unnamed offset, and no longer reads past its 124-byte register image
  473| 
  474| **The defect.**  `src/devices/dev_mvme187.c`, `DEVICE_ACCESS(mvme187_memc)`, the memory controller's register window (0x200 bytes
  475| at 0xfff43000; controller 1's half, +0x100..+0x1ff, folds onto the same image): before its switch, on every access including reads,
  476| it ran `odata = ((uint8_t*)&d->memcreg)[relative_addr];` with the folded offset 0..0xff, while `struct memcreg` is 124 bytes (31
  477| one-byte registers each padded to four, `src/include/thirdparty/mvme_memcreg.h`) -- an out-of-bounds read in the C source for
  478| 0x7c..0xff.  A store to memconf (+0x08) and every access the switch did not name ended the emulator process (`fatal()` +
  479| `exit(1)`).  Filed 2026-09-17 from an exit hunt (`regress/artifacts/ip30abortkill/EXITHUNT_grok_20260917.txt`); queued
  480| 2026-10-22 as external-research batch 8 of 10 (`regress/artifacts/research_20261022/TRIAGE.md` T7; its adjudication,
  481| `research_20261022/adj_20261022/ADJ_RULINGS.md` D: the bounds repair first, the exits after); the two exits are census line 97 of `exitunowned76`.
  482| 
  483| **The witness (rung 3).**  `regress/artifacts/mvme187memcoob/witness_20261104/WITNESS.md`, measured 2026-11-04 before any edit: a
  484| frozen 21-row probe on unmodified `-E mvme88k -e mvme187 -M 64`, one guest `ld.bu`/`st.b` per step, on the committed build:
  485| `regress/artifacts/mvme187memcoob/witness_20261104/prefix_head.out` 13/21, CONTROL=OK (chipid 0x80, chiprev 0x1, memconf 0x3 and
  486| controller 1's chipid 0x80, values only the device supplies), SYMPTOM=PRESENT -- loads at +0x0c, +0x7c and +0xff and a memconf store
  487| each ended the process (exit status 1); `/bin/true` 8/21 and a missing binary 0/21, each CONTROL=FAIL (`regress/artifacts/mvme187memcoob/witness_20261104/null.out`, `regress/artifacts/mvme187memcoob/witness_20261104/nobin.out`).  On
  488| the sanitizer build the loads at +0x7c and +0xff produced no AddressSanitizer report (`witness_20261104/asan_head/`): the read was
  489| latent behind the exits, so removing an exit without removing the read would have made it live.  An apparatus fact from the first
  490| try (`witness_20261104/try1_negdefect/`): `-E nosuchmachine -e mvme187` still constructs the machine, so the negative control
  491| passes no `-e`.
  492| 
  493| **Pass 1 and the design (2026-11-03/04).**  Six pass-1 stages on 11-03 -- the bug, the fix draft, the manual, a sibling sweep, the
  494| witness design and the port of ajfa/mvme187-sysv88-gxemul's patch -- in `_scratchpad/panel_20261103_103051_next5_mvme187memcoob/`
  495| and its five siblings, with Gemini web on each; the owner narrowed the roster at 12:1x that day (each panel's JOB.txt, e.g.
  496| `panel_20261103_103051_next5_mvme187memcoob/JOB.txt`).  Then
  497| the adjudications of those stages, two revised drafts, a row design and a witness share-findings stage
  498| (`_scratchpad/panel_20261104_014913_wsf_mvme187memcoob/`).  The design was ruled twice in Claude Code Cloud and reconciled:
  499| cloud Fable 5.1 (`regress/artifacts/mvme187memcoob/adj_20261104/FABLE_FINAL.md`: 8 rulings, 7 changes, 6 rows, GO-WITH-CHANGES --
  500| each served arm reads its own field), cloud Mythos 5.1 (`adj_20261104/MYTHOS.md` and `MYTHOS_r2.md`: V3-RULED -- the bound plus
  501| declines, the controller number printed, the memconf store declined, unimplemented reads returning 0, one latch per notice category
  502| per device), and the reconciliation (`adj_20261104/RECON_FABLE.md`: 21 differences, 3 owed, 2 conflicts, 6 rows, MERGE), which took
  503| the per-arm field reads over a subscript kept for constant indices: "A bound that depends on what the optimizer drops is not a
  504| bound".  A measuring seat confirmed the order on a sanitizer build (`regress/artifacts/mvme187memcoob/draft_20261104/answer.md`, ORDER-CONFIRMED:
  505| removing the exits while the unbounded read stands makes the read live); its final text came from claude-opus-4-8 after a refusal
  506| fallback, and `draft_20261104/answer_resumed.md` is the resumed restatement.
  507| 
  508| **The fix** (1 file).  `struct mvme187_data` gains two `int` latches directly after `memcreg` (`warned_memconf`,
  509| `warned_default`; DEVINIT memsets the struct), with a comment that the probe reads them back at +0x7c.  Each served arm reads its
  510| own field: chipid (+0x00), chiprev (+0x04), memconf (+0x08).  A memconf store is not kept and is announced once per device
  511| (`memconf write 0x%x (controller %i) ignored, not modelled (once)`); any other offset reads 0, keeps no store and is announced once
  512| per device with its direction, offset, controller and, for a store, value.  Controller 1 folds onto the same image and its number
  513| is printed.  No indexed read remains.  On the fixed build the witness scores 21/21, SYMPTOM=ABSENT
  514| (`regress/artifacts/mvme187memcoob/impl_20261104/witness_fixed.out`); the second version of the file differs from the first only
  515| in two comments (`det_20261104/dev_mvme187.c.fix` and `.fix2`).  **No tree swap:** the commit carries the working copy byte for
  516| byte -- md5 `97e983872a72`, the source tables 5 and 6 measured -- and est/, build/, build-asan/ and WSL /tmp/gxsec-build all hold it
  517| with fresh binaries (`regress/artifacts/mvme187memcoob/landing_20261105/TREES_memc.txt`; every hunk against HEAD lies inside the
  518| struct or the access function, `landing_20261105/STAGED_DIFFS_memc213.md`).
  519| 
  520| **The detector.**  `regress/mvme187_memc_probe.py`, 213 rows: the witness's 21 (controls, the negative control and the four
  521| sessions the old code ended) plus sixteen multi-access sessions, R3 to R18 -- several accesses in one emulator lifetime, one register
  522| per load, every load into a register seeded so a load that does not retire cannot read as a green 0.  They pin the per-field reads
  523| through both controllers, both latches' once-per-device announce across the four latch phases R16 and R17 visit, the announce texts, R8's twelve bytes past
  524| `memcreg` (the latches, then past the struct), and R18's stores of 0x01 that toggle a set latch back to zero under an own-latch
  525| variant.  Its header is the CONTRACT: what is covered, the floor, and five disclosed coverage-debt families.  Wired into
  526| `regress/gate_arm.sh` (gate 14) after the `#570` block: the completion sentinel once, RESULT pinned 213/213 by equality, CONTROL=OK,
  527| SYMPTOM=ABSENT, every row by name, the emitted/green/red counts, and a layout-free source check (no `memcreg)[` and no
  528| `[relative_addr]` in the file, the old read in its old spelling); `tools/precommit_check.sh` SCORE_CLAIMS_MANIFEST raised by one;
  529| `tools/pipeline/check_probe_wiring.py` MANIFEST entries for the probe and the round's 28 artifact scripts.  Scores of the shipped
  530| instrument (`regress/artifacts/mvme187memcoob/r7_20261105/table6/SCORES.txt`, lines 1-8): base 213/213; HEAD 29/213,
  531| SYMPTOM=PRESENT; `/bin/true` 28/213, an absent binary 4/213, `/bin/false` 5/213, each CONTROL=FAIL; the three removed defects
  532| reinstated verbatim -- the memconf exit 81/213, the default exit 42/213, the indexed read 208/213.  Gate 14's memc block replayed over table 6's banked logs, the probe call replaced by each log (`regress/artifacts/mvme187memcoob/landing_20261105/DRYRUN_memc213.out`): base (the fix) green; HEAD red (188 of 223 checks); /bin/true red (189 of 223 checks); absent binary red (213 of 223 checks); /bin/false red (212 of 223 checks); B1 memconf exit reinstated red (136 of 223 checks); B2 default exit reinstated red (175 of 223 checks); B3 indexed read reinstated red (8 of 223 checks); L_MB_M_xori_any (own latch, ungated) red (4 of 223 checks); L_DT_D_idat_W.D (own latch, own gate) red (4 of 223 checks); K_MB_memconf_and_D (memconf keep) red (4 of 223 checks); L_ME_M_idat_W.nC (disclosed, green in table 6) green; HEAD source red (1 of 223 checks).  The block ran in situ at the landing, alone, from a scratch copy of regress/ holding the staged probe and source, on build/gxemul: 223 checks, 0 FAIL, MVME187_MEMC_RESULT=213/213, MVME187_MEMC_CONTROL=OK (`regress/artifacts/mvme187memcoob/landing_20261105/INSITU_memc.out`; the probe's log `regress/artifacts/mvme187memcoob/landing_20261105/INSITU_memc_probe.log`).  Before it, gate 14 had run the block only on the 74-row probe
  533| (`regress/artifacts/mvme187memcoob/wiring_20261105/gate14_mvme187_memc.log`, 74/74).
  534| 
  535| **Test-variant tables** (WSL scratch clones under clone-local `.MUTANT` sentinels, each restored, `cmp`-verified and rebuilt;
  536| predictions written before each table).  The 52-row first detector: base 52/52, HEAD 26/52, `/bin/true` 15/52, an absent binary
  537| 3/52, `/bin/false` 4/52 (`regress/artifacts/mvme187memcoob/det_20261104/SCORES.txt`).  Table 1 (the 56-row probe): 19 variants,
  538| every one red (`regress/artifacts/mvme187memcoob/det_20261104/table1/SCORES.txt`).  Table 2 (74 rows): 29, every one red (`regress/artifacts/mvme187memcoob/det_20261104/table2/SCORES.txt`).  Table 3
  539| (118 rows): 63, every one red (`regress/artifacts/mvme187memcoob/r3_20261105/table3/SCORES.txt`).  The pass-3 seats' 34 findings, measured on the 118 rows: every one
  540| green (`regress/artifacts/mvme187memcoob/p3_20261105/table_p3/SCORES.txt`).  Table 4 (148 rows): 112 variants, every one red (`regress/artifacts/mvme187memcoob/r4_20261105/table4/SCORES.txt`).
  541| Table 5 (206 rows): 3,575 variants -- table 4's 112 and 3,463 representatives of a 37,974-cell walk -- with 665 green, every one
  542| predicted green before the table (`regress/artifacts/mvme187memcoob/r5_20261105/table5/TALLY.txt`); for the variants 3,518 predictions exact, 56 at-least, one
  543| miss, `D7_fold`, itself detected at 175/206 (`r6_20261105/ERRATA_table5_VERDICT_20261105.md`, item 1).  Table 6 (213 rows): the
  544| eight legs and table 5's 665 green variants re-run -- 24 red, 641 green, every red set as predicted (`regress/artifacts/mvme187memcoob/r7_20261105/table6/TALLY.txt`)
  545| -- and one miss: the indexed-read leg also reddened `R17 f3 r2`, a byte 111 bytes past the device struct's allocation that read
  546| 0x66, 0x34 and 0x15 on three runs of one binary (`regress/artifacts/mvme187memcoob/r7_20261105/b3repeat_run.log`).  The sanitizer legs
  547| (`det_20261104/asan/READING.md`): on the shipped layout the reinstated read draws no AddressSanitizer report at -O0 or -O3 -- at
  548| +0x7c..+0x83 it reads the latches inside the struct, and why the read at +0xff goes unreported is reasoned, not measured (the
  549| probe's header) -- so the probe catches it through R3, R8 and R11 instead, a catch that holds
  550| while the latches sit directly after `memcreg`, which the struct comment pins and the gate's source check backs.  **Floor**: (a) HEAD
  551| 29/213; (b) each removed defect reinstated verbatim, red; (c) the binary null media measured (table 6, lines 3-5), a build without
  552| the device not run; (d) the floor the pass-5 ruling drew -- each repair path's own guard crossed with the state it reads -- holds no
  553| surviving cell after repair 6 (pass 2 on repair 6: 693 own-latch cells, 0 breaches); (e) the CONTRACT in the probe header; (f) the
  554| control rows and R6 pin which field each offset reaches, R8 which byte a load past `memcreg` returns.
  555| 
  556| **The review chain** -- a pass on every repair, closing on the first valid pass with zero breaches.  Pass 2 on the diff (11-04):
  557| cloud Fable 5.1 (`regress/artifacts/mvme187memcoob/adj_20261104/P2_FABLE.md`: 38 checked, 0 false, 2 floor gaps) and cloud Opus
  558| 5.5 (`P2_OPUS.md`: 24, 2, 1), Grok (24, 4, 2) and GLM 5.3 (31, 2, 3) in `_scratchpad/panel_20261104_174538_p2_mvme187memcoob/`,
  559| Gemini (7 attacks, 2 broken) -- REPAIR-NEEDED on the detector, the fix unchanged.  Its adjudication (cloud Mythos 5.1,
  560| `adj_20261104/ADJ_MYTHOS.md`: 41 rulings, 4 changes, 3 filed; cloud Opus 33, 7, 2; Grok 33, 4, 3; GLM 33, 6, 3; cloud Fable's
  561| answer withheld by a classifier, `adj_20261104/ADJ_FABLE.md`) led to repair 2 (74 rows, table 2).  The repair's pass 2
  562| (`p2r_20261105/`: cloud Fable three times -- 62 checked, 2 false, 1 floor gap; 33, 3, 1; 37, 2, 2 -- cloud Opus three times -- 16, 1,
  563| 2; 27, 3, 2; 54, 4, 4 -- Grok 47, 1, 6, GLM 18, 2, 3, Gemini CLOSE) and its adjudication (`p2r_20261105/ADJ_MYTHOS.md`: 21 rulings, 6
  564| changes, 7 filed; `ADJ_MYTHOS_r2.md` 25, 5, 3; GLM 25, 3, 4) led to repair 3, the class closure (118 rows, table 3).  Pass 3
  565| (`p3_20261105/`: codex 100 cells swept, 27 breaches, 4 false records; GLM 102, 5, 2; the seats' 34 findings measured green) and its
  566| ruling (`p3_20261105/ADJ_MYTHOS.md`: 17 families, 6 new breaches, 7 changes; a late replication, `ADJ_MYTHOS_r2.md`, found 8,
  567| cross-checked in `LATE_REPLICATIONS_20261105.md`) led to repair 4 (148 rows, table 4).  Pass 4 (`p4_20261105/`: codex 532 cells, 76
  568| breaches, 2 false records; GLM 400, 3, 1; three cloud Mythos rulings owing 27, 30 and 24 rows) and the consolidated ruling, local
  569| Mythos 5.1 (`p4_20261105/CONS_MYTHOS_local.md`: 6 families, 10 new breaches, 58 rows, 148 -> 206), led to repair 5 (206 rows, table
  570| 5).  Pass 5 (`p5_20261105/`: codex 7 families swept, 0 floor cells owed, 10 false records; Gemini twice, both arguing coverage debt)
  571| and the final ruling (`adj_p5_20261105/ADJ_MYTHOS_local.md`: 0 floor families, 5 debt families, 10 records upheld,
  572| CLOSE-AFTER-RECORDS).  Records 6 (`r6_20261105/RECORDS6_NOTE.md`) rewrote the probe's contract and filed errata; four readings by
  573| GPT-6 Astra -- rec6 to rec9, which their dispositions number the second to the fifth -- found 10, 3, 1 and 0 items to fix
  574| (`rec6_20261105/` to `rec9_20261105/`, each `DISPOSITION.md`), every fix text-only
  575| (`regress/artifacts/mvme187memcoob/r6_20261105/TEXTONLY_PROOF.txt`).
  576| 
  577| **The regress review found a floor breach, and repair 6 closed it.**  The Fable-only stage, held by local Mythos 5.1
  578| (`regress/artifacts/mvme187memcoob/regress_20261105/REG_MYTHOS_local.md`: 20 checks, 2 floor breaches, 9 record findings,
  579| REGRESS-BREACH): eight variants that table 5's predictor had classed NOCHANGE write a repair path's own latch under that path's own
  580| predicates, or under no gate, and all eight scored 206/206; the final ruling had placed the 517 survivors family by family and
  581| treated the 148 NOCHANGE as no-ops.  By the ruling's own test they are floor cells.  Repair 6 (`r7_20261105/IMPL_NOTE.md`, an Opus
  582| 5.5 implementer): measured the eight green on the 206 rows in a fresh clone (`regress/artifacts/mvme187memcoob/r7_20261105/step1/SCORES.txt`), added session R18 --
  583| two stores of 0x01 and one of 0x00 to +0x18 and to +0x08, each pair followed by a load; seven rows -- for 213 rows, wrote
  584| `regress/artifacts/mvme187memcoob/r7_20261105/PRETABLE_6.out` before table 6, where each of the eight scores 212/213, red on `R18 lines` alone
  585| (`regress/artifacts/mvme187memcoob/r7_20261105/table6/SCORES.txt`, lines 9-16), dispositioned the nine record findings (`r7_20261105/ERRATA_r7_20261105.md`), and
  586| wrote the gate block this commit carries (`r7_20261105/gate_memc_block.new`, the records-6 comment patch folded in).  Repair 6's
  587| pass 2 (`p6_20261105/`: codex 693 cells swept over the own-latch class, 0 breaches, 2 false records; Gemini's web route down) closed
  588| the chain; its two record fixes were read and accepted (`recp6_20261105/DISPOSITION.md`).  The stage's seat then read the 213-row
  589| detector again (`regress_20261105/REG2_MYTHOS_local.md`: 20 checks, 0 floor breaches, 4 record findings,
  590| REGRESS-WITH-FINDINGS): the breach is closed, measured.  Its four record items were dispositioned: A -- bank the kit's dry run,
  591| identity proof and staged diffs -- by the landing kit (`landing_20261105/`); B and C, two sentences of the probe's CONTRACT
  592| (family (2)'s set-latch clause and family (6)'s exclusions), and D, a word in repair 6's note (a synthetic replay called
  593| measured), by repair 6's implementer, text only (`regress/artifacts/mvme187memcoob/r7_20261105/TEXTONLY_PROOF_reg2.txt`; the edit:
  594| `r7_20261105/mvme187_memc_probe.py.reg2.diff`).  A reading of the three fixes accepted all three (`regress/artifacts/mvme187memcoob/recreg2_20261105/DISPOSITION.md`, GPT-6 Astra: 3 accepted, 0 to fix): B true as qualified, C's fifteen own-shape exclusions exactly the right set, D true; the round's review and records close here, and the in-situ 223-check gate run stays owed at landing.
  595| 
  596| **Seats.**  Every answer is recorded on the row, one entry each, read whole before it was written; the non-firings and seat failures are recorded by name, each with its own reason.  Research (pass 1 and the design): agy 27, codex 6, deepseek 6, fable5 5, glm 7, grok 7, kimi 2, minimax 2, opus5 4 entries -- the 11-03 next-5 panels (`_scratchpad/panel_20261103_103051_next5_mvme187memcoob/` and five siblings), Gemini web on each stage and on the adjudications and drafts, the witness share-findings panel, the Claude Code Cloud design rulings and the measuring seat.  Review (passes 2 to 5, their rulings, the records readings and repair 6's pass 2): agy 10, codex 10, deepseek 1, fable5 20, glm 7, grok 5, kimi 1, minimax 1, opus5 6 entries, of them agy 8, codex 10, fable5 19, glm 6, grok 3, opus5 6 answers; the implementer runs (repairs 5 and 6, table 5's preparation, records 6 to 8) are recorded as such and not as reviews; Grok 4.7 (a 402 billing wall), GLM 5.3 after pass 4 and Gemini after pass 5 (the Ollama limit, the web route) are seat failures on the later passes; deepseek, minimax and kimi were not fired on the review stage.  Regress: the two local Mythos 5.1 readings.  Pass-2 and later answers are banked in the round's artifacts dir or cited in their panel dirs.
  597| 
  598| **Owner flag, carried.**  Under codex's narrower bound -- an insertion is in bound only if it restores a removed operation or nulls
  599| the repair directly -- the eight own-latch variants would be coverage debt and the first regress verdict REGRESS-WITH-FINDINGS.  The
  600| ruling of record rejected that bound (`adj_p5_20261105/ADJ_MYTHOS_local.md`, "On codex's bound argument"); R18's measurement closes
  601| the eight either way.
  602| 
  603| **Landing edits, none changing code.**  The probe's docstring names the round number where it read `#NNN`, and its four
  604| table-5 scores written N/206 are put in words, because `check_score_claims.py` reads every N/M in a gated probe's docstring as a
  605| claim against the 213-row pin (`landing_20261105/PROBE_IDENTITY_memc213.md`: the syntax tree minus the docstring unchanged, and with strings normalised equal to
  606| table 6's frozen instrument).  The gate block is repair 6's, its header numbered; the working tree's own memc block (206 rows) is not
  607| committed.  The section-U raise is written fresh against HEAD: the working copy's memc raise names a stale 74-row pin.  The kit's
  608| dry run, identity proof and staged diffs are banked in `regress/artifacts/mvme187memcoob/landing_20261105/` -- the first regress
  609| review's record item 6 -- including, under the names the REGRESS packet cited, the 206-row versions it read
  610| (`regress/artifacts/mvme187memcoob/landing_20261105/DRYRUN_memc.out`; the packet as sent, `landing_20261105/REGRESS_memc.md`).  Of the round's artifact folder, 1,150 of 11,709 files (23.7 of 136.1 MB) are committed -- every file a committed record cites, followed through, with the round's records, seat answers, table summaries, frozen instruments, proofs, diffs and each table's base, HEAD and null legs (`regress/artifacts/mvme187memcoob/landing_20261105/ARTSET_memc_why.txt`); the other 10,559 files (112.4 MB) -- per-variant probe logs, session transcripts, build and patch-apply logs, codex reasoning streams -- stay on disk, kept out by the folder's deny-list `.gitignore` (the coordinator's artifact-selection rule, `landing_20261105/ARTSET_RULE.md`; the `.gitignore` proved with a dry `git add -n` in a scratch repo, `regress/artifacts/mvme187memcoob/landing_20261105/ARTGI_memc.txt`).  The citation gate cannot select this block (`check_cited_artifacts.py` keys on `## Round <digits>` headings: `citeprefixblind`, filed by `#554`); its own resolver, run over the block by hand at the landing, resolves all 28 citations to this round's files or the sources it names.
  611| 
  612| **Assessed, not changed.**  The source check sees the old read in its old spelling only; a new spelling with the latches moved
  613| would escape both it and R8 (the first regress review, P3) -- disclosed, not a floor matter, since clause (b) is verbatim.  A build
  614| without the device was not run as a null medium (repair 6 declined the review's "by construction" reading as resting on an
  615| unmeasured premise).  Under the reinstated read `R17 f3 r2` read 0x0 in table 5 and 0xd8, 0x66, 0x34 and 0x15 in table 6 and its
  616| three repeats -- allocator contents, so not a row the contract claims; the four it names were red in every run.
  617| 
  618| **Filed, not fixed here.**  `memccoverdebt` (LOW, new): table 6 leaves 641 test variants green, every one predicted green, each in a
  619| family the probe's CONTRACT discloses (the regress follow-up found no own-arm, own-target cell among them); the filing carries the untested contexts and sketched closing rows, unwalked
  620| (`regress/artifacts/mvme187memcoob/r6_20261105/FILING_memccoverdebt.md`, as amended through the fourth reading and repair 6,
  621| `r7_20261105/ERRATA_r7_20261105.md` item 4).  `exitunowned76` loses its census line 97 (this round removes both exits).
  622| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_581: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC581: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
