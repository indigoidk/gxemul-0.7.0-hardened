# Reading task: oldrec582 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC582-07c4` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #582 qhslowifetch (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 348-463 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
  348| # `#582` Records (follow-up, 2026-11-05): `qhslowifetch` names its landing commit `2f83ff0a`; the committed-tree proofs; the pass-2 receipt
  349| 
  350| `git ls-tree 2f83ff0a`, md5s hashed in Python from the committed bytes: `src/cpus/cpu_ppc_instr.c` blob `508e9181982f`, md5 `dbd192fbc950`; `src/include/cpu_ppc.h` blob `beada84cba9d`, md5 `30544e73fced`; `regress/ppc_ifetch_probe.py` blob `86c750aa1246`, md5 `6a098d38c17e`; `regress/gate_ppc.sh` blob `f6bc4609ca51`, md5 `b4d4e002bb01`; `tools/precommit_check.sh` blob `2d7650296cfe`, md5 `0150bf2341a4`; `tools/pipeline/check_probe_wiring.py` blob `13a6e68bf756`, md5 `334ab5cbb1dd`.  The working copy against each: cpu_ppc_instr.c the same; cpu_ppc.h the same; ppc_ifetch_probe.py the same; gate_ppc.sh the same; precommit_check.sh plus other rounds' uncommitted manifest raises (1 hunk(s)); check_probe_wiring.py plus other rounds' uncommitted MANIFEST entries (2 hunk(s)).
  351| 
  352| The four trees took the committed `cpu_ppc_instr.c` in the landing window and keep it (no restore owed: `regress/artifacts/qhslowifetch/landing_20261105/UPDATE_QHS.out`).  The row's `commits` field names `2f83ff0a` and its state note names the landing commit.  The `regress/pass2_ledger.tsv` receipt line for `2f83ff0a`, a landing line in OUTSTANDING_BUGS.md's `#582` section and `matrix.html` re-rendered complete this records commit.
  353| 
  354| # `#582` (2026-11-05) -- `qhslowifetch`: a failed slow-path instruction fetch on the PowerPC no longer ends the emulator process; the read-failure arm returns on read-ahead, refreshes after an exception already delivered, parks on a -T halt, and raises a machine check or checkstops when a device declines the fetch while running
  355| 
  356| **The defect.**  `src/cpus/cpu_ppc_instr.c`, `X(to_be_translated)`: when the instruction word is not in a host page the translator reads it
  357| with `cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION)`; if that read failed it printed `PPC to_be_translated(): read failed: TODO` and called
  358| `exit(1)` -- one failed fetch ended the process.  Filed 2026-10-02 by `#555` from the id-less review
  359| (`regress/artifacts/idless_20261002/IDLESS_DISPOSITIONS.md`); queued 2026-10-22 as external-research batch 3 of 10
  360| (`regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md` section D; `regress/artifacts/research_20261022/TRIAGE.md` T6).
  361| 
  362| **Witness (rung 3, before any edit).**  `regress/artifacts/qhslowifetch/witness_20261104/WITNESS.md`: the 17-row first probe on unmodified
  363| `-E pmppc` scored 11/17 with the symptom PRESENT on the committed build, both as a scratch clone of HEAD `ebe5af82`
  364| (`regress/artifacts/qhslowifetch/witness_20261104/prefix_head.out`) and as `build/gxemul`
  365| (`regress/artifacts/qhslowifetch/witness_20261104/prefix_build.out`; three rounds have a `witness_20261104/` directory) -- the six `-T`
  366| rows red, each transcript ending `read failed: TODO` with exit status 1; `/bin/true` 8/17 and a missing binary 3/17, both CONTROL=FAIL.  What reaches the exit is a real-mode fetch past the end of RAM under `-T`; an ordinary ISI does
  367| not, because the dispatch lookup delivers it before the translator runs (WITNESS.md, facts 1 and 2).
  368| 
  369| **The fix** (one hunk, `regress/artifacts/qhslowifetch/landing_20261105/STAGED_DIFFS_qhs.md`).  The failed read now has four exits and a
  370| fallback, each returning before the slot is translated: (a) a read-ahead fetch returns untouched; (b) a fetch whose translation already
  371| delivered an exception (pc, its low two bits cleared, != addr) refreshes next_ic and returns; (c) a `-T` halt (memory.c cleared running)
  372| parks the CPU on `nothing_call` at the fetch's pc; (d) a device declining an instruction-width read while running takes a machine check
  373| (`ppc_exception(cpu, PPC_EXCEPTION_MC)`, vector 0x200) when MSR[ME] is set, and otherwise prints a checkstop line, clears running and parks.
  374| `src/include/cpu_ppc.h` gains `PPC_EXCEPTION_MC 0x2`.  The comments' placeholders are filled at this landing (comment-only:
  375| `STAGED_DIFFS_qhs.md` proves the comment-stripped file unchanged): `#NNN` -> `#582`, `#MMM` -> `ppcvecaddr`, `#QQQ` -> `ppcintentrymsr`,
  376| `#PPP` -> `ppcmpcheckstop`.  The design is cloud Fable 5.1's four states (`adj_20261104/FABLE_FINAL.md`, R-A to R-D) merged with its
  377| replication (`FABLE_FINAL_r2.md`) by `adj_20261104/RECON_FABLE.md` (`CLOUDRECON_QHS: 16 DIFFERENCES 6 OWED 3 CONFLICTS 5 ROWS VERDICT:MERGE`),
  378| amended by the pass-2 rulings (`adj_20261104/FINAL_FABLE.md`: `CLOUDFINALQHS: 8 RULINGS 4 CHANGES 3 FILED VERDICT:APPLY-WITH-CHANGES`) and,
  379| for arm (b)'s aligned compare, repair 5 (`p4_20261105/ADJ_MYTHOS_r2.md`: `MYTHOSADJP4QHS: 8 RULINGS 8 ROWS OWED VERDICT:REPAIR-5`); no
  380| product change since repair 5 (`r7_20261105/table12/VERDICT.md`).  The SEC working copy, est/, build/, build-asan/ and WSL /tmp/gxsec-build were set to the staged file (its four placeholders filled, a comment-only change) and the three build trees rebuilt (part 1 cmp-clean against the staged file on all four, part 2 binary newer on the three; compiler warnings 0 0 0), and the shipped probe scored 249/249 with CONTROL=OK and SYMPTOM=ABSENT on the rebuilt build/ -- exactly the committed source (`regress/artifacts/qhslowifetch/landing_20261105/UPDATE_QHS.out`).
  381| 
  382| **Detector.**  `regress/ppc_ifetch_probe.py`, 249 rows over 31 cold `-E pmppc` debugger sessions: five control sessions, four `-T` sessions
  383| at 0x02040000, eight read-ahead cells from cpc700_pci's last word (pc's low two bits x MSR[ME]), eight one-entry partners at the same full pc
  384| and MSR, and six guest-made unaligned-pc sessions (`mtlr; blr`).  Wired into `regress/gate_ppc.sh` (gate 13) before the NetBSD prerequisite:
  385| the completion sentinel once and last, each protocol key once, RESULT pinned 249/249, CONTROL=OK, SYMPTOM=ABSENT and RED=none, every row by
  386| name, and the denominator pinned unquoted (`ppc_ifetch rows run` 249, with `rows green` 249 and `rows red` 0) in the form
  387| `check_score_claims.py` reads; `tools/precommit_check.sh` SCORE_CLAIMS_MANIFEST 47 -> 48; `tools/pipeline/check_probe_wiring.py`
  388| MANIFEST entries for the probe and the 68 artifact scripts.  On the final instrument (`r7_20261105/table12/SCORES.txt`): HEAD 108/249 (141
  389| rows red, SYMPTOM=PRESENT), the fix 249/249, and the null media `/bin/true` 94/249, an absent binary 64/249 and `/bin/false` 65/249, each
  390| CONTROL=FAIL.  Gate 13 ran in situ on the updated build/ with the 249-row block: 631 checks, the qhs block's 262 among them, 0 FAIL, PPC_IFETCH_RESULT=249/249 (`regress/artifacts/qhslowifetch/landing_20261105/GATE13_INSITU_qhs.out`).
  391| 
  392| **Test-variant tables.**  Twelve, on probes of 50 to 249 rows (`det_20261104/table1/`, `table2/`, `r3_20261105/table3/`,
  393| `r4_20261105/table4/`, `r5_20261105/table5/`, `r6_20261105/table6/`, `r7_20261105/table7/` .. `table12/`), each in a scratch clone of
  394| `build/` under a clone-local sentinel, a PRETABLE written before each.  Table 12 (`r7_20261105/table12/VERDICT.md`, `r7_20261105/table12/COMPARE.out`:
  395| COMPARE12_MISSES=0): 88 variants, 73 red, 14 green -- the seven in arm (d) or the checkstop fallback and the three in arm (b)'s taken side,
  396| which no pmppc fetch reaches (`det_20261104/window_sweep.out`: WINDOW_SWEEP_ARM_D=NOT_REACHED), V3 and R5_cb equivalent wherever running is 0,
  397| and R5_arun and R7b_a_runun masked by the real fetch's second halt -- and V12, NOT PREDICTED, red on 29 rows and counted in neither tally.
  398| **Floor:** (a) HEAD 108/249; (b) the removed exit reinstated verbatim (B1_exit_head) 108/249; (c) the three null media above, CONTROL=FAIL;
  399| (d) the grid of pc's low bits x MSR[ME] x {two-entry, one-entry} held whole, with a partner per read-ahead cell (repair 11,
  400| `r7_20261105/B123_NOTE.md`; the pairing check `table12/PAIRS_base.out`, PAIRS_OK 8 of 8); (e) the contract in the probe's docstring.
  401| 
  402| **The repair chain.**  Pass 2 on the diff and the 50-row detector, then repair passes 2r and 3 to 11 on the 56- to 249-row detectors, each
  403| finding something the next repair closed: the read-ahead session's MSR[ME]-set cell (repair pass 2: `p2r_20261105/ADJ_FABLE.md`, Q1 upheld as
  404| a floor breach); msr rows on the five `-T` sessions and a read-ahead checkstop row (pass 3: `p3_20261105/ADJ_MYTHOS_r2.md`, 6 rows owed); arm
  405| (b)'s unaligned compare, a defect in the fix itself that flooded 8278 halt reports (pass 4: `p4_20261105/BLR_NOTE.md`; repair 5 by
  406| `p4_20261105/ADJ_MYTHOS_r2.md`); a widened mask and arm (a)'s guard conjoined with alignment (pass 5: `p5_20261105/MASK7_NOTE.md`,
  407| `p5_20261105/TRAODD_NOTE.md`); the whole read-ahead grid, pc's low bits x MSR[ME] (pass 6, repair 7: `r7_20261105/B123_NOTE.md`); the
  408| UNIMPLEMENTED channel (pass 7, repair 8); and one family three times -- a toggle that the two-entry read-ahead sessions cancel, conditioned on
  409| pc's low bits (pass 8), on ME with alignment (pass 9) and on the full pc (pass 10) -- closed STRUCTURALLY by the eight one-entry partners
  410| (repair 11, `r7_20261105/B123_NOTE.md`).  Pass 11 found a toggle that creates and consumes its own condition on an untested MSR bit (RI); the
  411| ruling graded it clause-(e) debt, upheld two false records and closed the chain (`adj_p11_20261105/ADJ_MYTHOS_local.md`:
  412| `MYTHOSADJP11QHS: 0 FLOOR 1 DEBT 2 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS`); the corrections were read three times by GPT-6 Astra until a
  413| reading found nothing (`rec11_20261105/` 6 accepted / 2 to fix, `rec12_20261105/` 0 / 2, `rec13_20261105/` 2 / 0).  The verdict of every
  414| pass and ruling from pass 3 on:
  415| 
  416| ```
  417| p3 ruling    p3_20261105/ADJ_MYTHOS_r2.md               MYTHOSADJP3QHS: 7 RULINGS 6 ROWS OWED VERDICT:RECORDS-AND-ROWS
  418| p4 ruling    p4_20261105/ADJ_MYTHOS_r2.md               MYTHOSADJP4QHS: 8 RULINGS 8 ROWS OWED VERDICT:REPAIR-5
  419| p5 Mythos    p5_20261105/MYTHOS_r3.md                   MYTHOSP5QHS: 39 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS VERDICT:REPAIR
  420| p6 codex     p6_20261105/codex_codex_qhs_p6.txt         CODEXP6QHS: 41 CELLS SWEPT 3 BREACHES 3 FALSE RECORDS VERDICT:REPAIR
  421| p7 codex     p7_20261105/codex_codex_qhs_p7.txt         CODEXP7QHS: 8 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS VERDICT:REPAIR
  422| p8 codex     p8_20261105/codex_codex_qhs_p8.txt         CODEXP8QHS: 8 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS VERDICT:REPAIR
  423| p9 codex     p9_20261105/codex_codex_qhs_p9.txt         CODEXP9QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS VERDICT:REPAIR
  424| p10 codex    p10_20261105/codex_codex_qhs_p10.txt       CODEXP10QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS VERDICT:REPAIR
  425| p11 codex    p11_20261105/codex_codex_qhs_p11.txt       CODEXP11QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS VERDICT:REPAIR
  426| p11 ruling   adj_p11_20261105/ADJ_MYTHOS_local.md       MYTHOSADJP11QHS: 0 FLOOR 1 DEBT 2 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS
  427| rec11 codex  rec11_20261105/codex_codex_qhs_rec11.txt   CODEXRECP11QHS: 6 ACCEPTED 2 TO FIX VERDICT:FIX
  428| rec12 codex  rec12_20261105/codex_codex_qhs_rec12.txt   CODEXREC12QHS: 0 ACCEPTED 2 TO FIX VERDICT:FIX
  429| rec13 codex  rec13_20261105/codex_codex_qhs_rec13.txt   CODEXREC13QHS: 2 ACCEPTED 0 TO FIX VERDICT:ACCEPT
  430| recreg codex recreg_20261105/codex_codex_qhs_recreg.txt CODEXRECREGQHS: 2 ACCEPTED 0 TO FIX VERDICT:ACCEPT
  431| regress      regress_20261105/REG_MYTHOS_local.md       MYTHOSREGQHS: 262 CHECKS 0 FLOOR-BREACHES 2 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS
  432| ```
  433| 
  434| **Regress review** (the Fable-only stage; Claude Mythos 5.1 run locally, the fable5 slot): `MYTHOSREGQHS: 262 CHECKS 0 FLOOR-BREACHES 2 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS` (`regress/artifacts/qhslowifetch/regress_20261105/REG_MYTHOS_local.md`): the floor's clauses (a)-(e) discharged with their SCORES.txt lines, every one of the block's 262 checks able to fail, the pairing invariant's first-visit core and both DERIVED kills re-derived from the code, no row vacuous by construction (the three never-red rows are premise controls); two record findings, R-A and R-B.  Its two record findings were applied
  435| text only by the main loop -- R-A, the gate comment's pairing sentence cut to the rec13 first-visit core
  436| (`r7_20261105/gate_ppc.sh.regrec.diff`), and R-B, a scoping sentence at the head of the probe's clause (e)
  437| (`r7_20261105/ppc_ifetch_probe.py.regrec.diff`; `r7_20261105/regrec_proof.out`: every comparison EQUAL, the negative control DIFFERENT) --
  438| and GPT-6 Astra read both (`recreg_20261105/codex_codex_qhs_recreg.txt`: `CODEXRECREGQHS: 2 ACCEPTED 0 TO FIX VERDICT:ACCEPT`).  The
  439| review read the landing kit's phase-1 records; the forms banked here are phase 2's (the placeholder fill, the decision-3 docstring, R-A
  440| and R-B), and the packet it answered is banked unchanged (`landing_20261105/REGRESS_qhs.md`).
  441| 
  442| **Gate-block replay.**  Gate 13's qhslowifetch block, as staged, replayed over table 12's 93 banked logs and 13 synthetic logs, the probe call replaced by each log (`regress/artifacts/qhslowifetch/landing_20261105/DRYRUN_qhs.out`): base (the fix) green; HEAD red (146 of 262 checks); /bin/true red (160 of 262 checks); an absent binary red (190 of 262 checks); /bin/false red (189 of 262 checks); the 14 variants the probe scored green (D10_chk_run, D11_b_noref, D6_d_inv, D9_mc_vec, R5_arun, R5_cb, R7_G1_b_lt, R7_G2_d_msr, R7b_a_runun, V2_b_del, V3_c_true, V4_d_false, V5_d_true, V6_chk_nopark) green; the 74 it scored red, red; on every banked log the failing per-row pins are exactly the rows the log's PPC_IFETCH_RED names; the 13 synthetic logs (a dead probe; the sentinel missing, doubled or not last; protocol keys missing or doubled; a row lost, added, doubled or flipped; every row removed; a RESULT line that disagrees) each red on the pins they target; every one of the block's 262 checks failed on at least one leg.  The synthetic logs and the replay script are banked beside it (`landing_20261105/pc/`).
  443| 
  444| **The probe's docstring at the landing** (the coordinator's decision 3): the working copy takes every staged edit, so the two are equal after
  445| the commit -- the round number, `PAIRS_OK 8 of 8` (section U reads N/M in a gated probe's docstring as a score claim against the 249-row
  446| pin), and the rows the contract names as filed.  Docstring only: the round's own proof script, re-run
  447| (`landing_20261105/PROOF_wtdoc_qhs.out`: every comparison EQUAL, the negative control DIFFERENT), and `landing_20261105/PROBE_IDENTITY_qhs.md`
  448| (syntax tree minus the docstring, every string kept, equal to table 12's frozen instrument; section U clean with the real checker).
  449| 
  450| **Seats.**  Every answer is recorded on the row, one entry each, each read whole at the landing by the kit's six reading agents (Opus 5.5), whose inventories give every file's verdict line verbatim and a note (`landing_20261105/inv/`, one JSON record per file); the non-firings and seat failures are recorded by name with their reasons.  Research (pass 1 and the design): agy 33, codex 7, deepseek 6, fable5 7, glm 7, grok 7, kimi 6, minimax 4, opus5 3 entries, 74 of them answers -- the six 2026-11-03 panels (bug review, fix draft, manual, siblings, witness, port; their directories are in the entries; the agy CLI, deepseek, minimax, kimi-k3:cloud and the Opus seat outside the owner's 12:1x roster), Gemini 4 Argon's answers and proposed adjudications, the witness share-findings panel and the Opus measuring seat, and the cloud Mythos and Fable design rulings.  Review (pass 2, the repair passes and the records chain): agy 18, codex 13, deepseek 1, fable5 22, glm 9, grok 5, kimi 1, minimax 1, opus5 7 entries, 63 answers -- GPT-6 Astra from pass 3 on, Grok 4.7 and GLM 5.3 until their walls, Argon on most passes, cloud Opus 5.5, cloud and local Mythos 5.1 and cloud Fable 5.1; kimi, deepseek and minimax were not fired.  Regress: the one Fable-only entry.
  451| 
  452| **Filed** (each in the ledger and in OUTSTANDING_BUGS.md's `#582` section): the fix's placeholders `ppcvecaddr` (#MMM) and `ppcmpcheckstop` (#PPP); the contract's `ppcifetchibinit` (the ib zero-init), `ppcbranchlowbits` (the branch that keeps pc's low bits) and `ppcifetchdeclineprod` (ROW 5, arm (d)'s producer); the final ruling's F4, `memrwtreadahead`; and the design's dev_vga bound, `vgagfxwindowend` -- all LOW.  #QQQ names the existing `ppcintentrymsr` (ppc_exception()'s MSR modelling), which gains a note.
  453| 
  454| **Records corrected before the landing.**  The `~HH:MMZ` time-of-day stamps the main loop wrote were guesses from its own wrong
  455| clock, up to 3.5 hours ahead of their files' timestamps.  It removed every one, each with a dated note quoting what it removed: in the
  456| dispositions of passes 6 to 11 and of the records chain, in the six repair headings of `r7_20261105/B123_NOTE.md`, in
  457| `p6_20261105/SEAT_NOTE.md` and in the pass-5 and table-6 notes (`grep -rl 'time-of-day stamp' regress/artifacts/qhslowifetch/` lists
  458| the corrected files).
  459| 
  460| **What the commit carries of the round's folder.**  793 of its 17251 files, 18.4 of 445.7 MB, by the coordinator's rule of 2026-11-05: every file a committed record or docstring cites (closed transitively), the records (every `.md`, the seat answers, the VERDICT / SCORES / TALLY / MD5 / PRETABLE / COMPARE / PAIRS files, the frozen instruments, the `.pre_*` backups, the proofs and the diffs) and each table's base, HEAD and null-leg probe logs.  The other 16458 files -- per-variant session transcripts, build logs and probe logs -- stay on disk, uncommitted.  The folder's new `.gitignore` denies those bulk classes (and the uncited one-offs present at the landing) and re-includes each cited file, so `git add` of the folder takes exactly the selection while any file added later stays visible to `git status` (`landing_20261105/ARTGI_qhs.txt`: the dry run's count and each line's reach); `landing_20261105/ARTSET_qhs_why.txt` gives each committed file's rule and `landing_20261105/ARTSET_qhs_excluded.txt` the excluded groups (computed by the landing kit's artset_qhs.py).
  461| 
  462| **Landing.**  The citation gate cannot select this block (`check_cited_artifacts.py` keys on `## Round <digits>` headings: `citeprefixblind`, filed by `#554`); its own resolver, run over the block by hand at the landing, resolves all 15 citations to this round's files or the sources it names.
  463| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_582: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC582: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
