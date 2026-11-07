# Reading task: oldrec580 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC580-6f1d` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #580 mipsprimundec (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 771-867 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
  771| # `#580` Records (follow-up, 2026-11-04): `mipsprimundec` names its landing commit `68c0d60b`; the committed-tree proofs; the pass-2 receipt
  772| 
  773| `git ls-tree 68c0d60b`, md5s hashed in Python from the committed bytes: `src/cpus/cpu_mips_instr.c` blob `0df67fd9e38a`, md5 `c35bf86a5114`; `regress/mips_primundec_probe.py` blob `6adba356a8d8`, md5 `dae62682d838`; `regress/gate_mips_folds.sh` blob `83275c9b67fd`, md5 `a4e3546e4da2`.  The working tree matches each (cpu_mips_instr.c same, mips_primundec_probe.py same, gate_mips_folds.sh same).
  774| 
  775| The row's `commits` field names `68c0d60b` and its state note names the landing commit.  The `regress/pass2_ledger.tsv` receipt line for `68c0d60b`, a landing line in OUTSTANDING_BUGS.md's `#580` section and `matrix.html` re-rendered complete this records commit.
  776| 
  777| **Filed (LOW): `seatsreadstemcollide`.**  The landing's pretest (`regress/artifacts/mipsprimundec/landing_20261104/PRETEST_580.out`) printed, under section G, `panel_20261104_014913: AMBIGUOUS -- 4 dirs share this stem` and then `cited but NOT ON DISK; cannot verify`.  The four directories exist and every citation names its full path; `check_seats_read.py`'s `PANEL_RE` keeps only the timestamp stem, and `resolve_dir` declines to guess among four.  So no answer in the four same-second wsf panels is checked by G (#580's were recorded by the landing's digest).  A checker change owes its own round with two negative controls.
  778| 
  779| # `#580` (2026-11-04) -- `mipsprimundec`: eight MIPS primary opcodes with no working translator arm now raise Reserved Instruction or Coprocessor Unusable instead of stopping the emulated CPU
  780| 
  781| **The defect.**  `src/cpus/cpu_mips_instr.c`, `X(to_be_translated)`: the primary-opcode switch had no case for 0x1d (JALX), 0x32 (LWC2),
  782| 0x36 (LDC2), 0x3a (SWC2), 0x3b (SWC3) and 0x3e (SDC2), so those words fell to `default: goto bad`; the 0x1e arm off the R5900 (MDMX) and the
  783| 0x33 arm below ISA IV (LWC3) printed a TODO and also went to `bad`.  `bad:` stops the emulated CPU ("UNIMPLEMENTED instruction") -- one
  784| guest word, no privilege test, no exception delivered.  Filed 2026-10-22 from the external-fixes research (`regress/artifacts/
  785| research_20261022/TRIAGE.md` row T120, class CPU-STOP, reach U; external-research batch 7 of 10).
  786| 
  787| **The ruling of record** (cloud Fable 5.1, `regress/artifacts/mipsprimundec/adj_20261104/FABLE_FINAL.md`: 11 rulings, 2 changes, 24
  788| rows, GO-WITH-CHANGES): adopt the main loop's measured v3 (`v3_20261104/MEASURED.md`: the draft plus the share-findings consensus) plus the
  789| v3b alternative (Reserved Instruction for LWC3/SWC3 on ISA III) plus one comment amendment on 0x1d.  Per word and level: R1 JALX RI
  790| everywhere; R2 0x1e off the R5900 RI; R3 the R5900's 0x1e (LQ, a real EE instruction this tree does not implement) NOT changed -- it still
  791| stops, outside this fix (row `mipsr5900lqsq`); R4 LWC2/SWC2 Coprocessor Unusable with CE = 2 everywhere; R5 LDC2/SDC2 RI on ISA I; R6 CpU
  792| CE = 2 from ISA II; R7 LWC3 CpU CE = 3 on ISA I and II; R8 RI on ISA III; R9 PREF on ISA IV, MIPS32 and MIPS64, unchanged from HEAD; R10
  793| SWC3 CpU CE = 3 on ISA I and II (the follow-up `FABLE_U1.md`: R10 STANDS); R11 SWC3 RI from ISA III.  A same-model replication
  794| (`FABLE_FINAL_r2.md`: 12 rulings, GO-WITH-CHANGES) is banked beside it.
  795| 
  796| **The fix.**  In `X(to_be_translated)`'s primary switch: LWC2/SWC2 -> `instr(cpu)` with `arg[0] = 2`; LDC2/SDC2 -> `instr(reserved)` below
  797| ISA II, else `instr(cpu)` with 2; SWC3 -> `instr(reserved)` from ISA III, else `instr(cpu)` with 3; 0x1d -> `instr(reserved)`; LWC3 keeps its
  798| PREF arm for ISA IV and up, gains `else if (isa_level == 3)` -> `instr(reserved)`, and below that `instr(cpu)` with 3 replaces the TODO and
  799| `goto bad`; 0x1e off the R5900 -> `instr(reserved)` replaces the TODO and `goto bad`.  Every arm carries a `#580` comment in the
  800| adjudication's final words (below).  Byte-identical in est/; propagated to and rebuilt in the three build trees (two-part clearance
  801| `CLEAR` on each: `build/`, `build-asan/`, `/tmp/gxsec-build`; zero compiler warnings).
  802| 
  803| **Witness (rung 3).**  `regress/artifacts/mipsprimundec/witness_20261104/`: the 80-row probe on unmodified `-E testmips` (each word placed
  804| with `put w` and stepped once on an R4400 and an R3000): 16/80 on the pre-fix build with the symptom PRESENT (`witness_20261104/prefix_build.out`), 80/80 on
  805| the fix (`impl_20261104/probe_final.out`); 16/80 on both dead-binary legs (`witness_20261104/null.out`, `witness_20261104/nobin.out`).
  806| 
  807| **Detector.**  `regress/mips_primundec_probe.py`, 122 rows over cold `-E testmips` sessions -- the R4400 (ISA III, the 64-bit translator)
  808| and the R3000 (ISA I, the MODE32 translator) for all eight words, the R5000, 24KEc and 5KE for the coprocessor words, a jalx and an lwc2 in
  809| a branch delay slot, and one R5900 row -- each `exc` row wanting the EXACT ExcCode and CE.  Wired into `regress/gate_mips_folds.sh` (gate
  810| 16): RESULT pinned 122/122 by equality, every row by name, CONTROL=OK and SYMPTOM=ABSENT required, and the denominator pinned unquoted
  811| (`mips_primundec rows run` 122, with `rows green` 122 and `rows red` 0) in the form `check_score_claims.py` reads;
  812| `tools/precommit_check.sh` SCORE_CLAIMS_MANIFEST 44 -> 45; `tools/pipeline/check_probe_wiring.py` MANIFEST entries for the probe and
  813| every artifact script.  HEAD 29/122 (the 121-row instrument: 28/121), the fix 122/122, `/bin/true` and an absent binary 16/122 with
  814| CONTROL=FAIL (`killtable_20261104/d31_20261104/SCORES_D31.txt`), and `/bin/false` 17/122 with CONTROL=FAIL -- the neg row
  815| green too, as the regress review predicted (`landing_20261104/false.out`).  Gate 16 alone on the fixed build: PASS 293
  816| (`wiring122_20261104/gate16.out`; again on the final bytes, `landing_20261104/gate16_final.out`).
  817| 
  818| **Test-variant tables** (`regress/artifacts/mipsprimundec/killtable_20261104/TABLE.md`; WSL scratch clones of `build/`, clone-local
  819| `.MUTANT` sentinels cleared only after a `cmp`-verified, rebuilt restore; a PRETABLE written before each run): table 1, 29 variants, 25 red;
  820| the supplement, the five the pass 2 named (D27-D31), 3 red; and the D31 row (cloud Fable's follow-up, below), red.  **29 of 34 red.**
  821| Undetected and disclosed in the probe's contract: D01, D11 and D30 (the ISA II cells -- the R6000 and Allegrex exit 1 before the prompt on
  822| testmips, `isa2_*.out`) and D22a/D22b (an exception raised without the PC sync: a single-stepped word's PC is already in sync, so the sync is
  823| invisible to this probe).  **Floor**: (a) 28/121 and 29/122 on the pre-fix build; (b) B1-B6 reinstate each removed defect verbatim at its
  824| site, all red; (c) 16/122 on `/bin/true` and on an absent binary, 17/122 on `/bin/false`, CONTROL=FAIL on all three; (d) every DEPENDS-ON variant red but the disclosed ISA II
  825| edges.  CHANNEL predictions checked mechanically: 26 of 27 matched; B1 named two rows the probe does not have.
  826| 
  827| **Pass 2** on the real diff and the 121-row detector (`_scratchpad/panel_20261104_182430_p2_mipsprimundec/`;
  828| `adj_20261104/P2_FABLE.md`, `P2_OPUS.md`): cloud Fable 5.1 (95 checked, 3 false, 4 floor gaps), cloud Opus 5.5 (171 / 4 / 4), Grok 4.7
  829| (65 / 3 / 0), GLM 5.3 (61 / 2 / 2) -- all four REPAIR-NEEDED, text only (the code ships as it stands), and all four ruled D22 DISCLOSE.
  830| GPT-6 Astra was walled until 2026-11-09 and Gemini 4 Argon's pass-2 packet failed three times on the web app's generic error: two seat
  831| failures, recorded by name, never agreement.
  832| 
  833| **The adjudication** (cloud Fable 5.1, `adj_20261104/ADJ_P2_FABLE.md`: 23 rulings, 16 text changes, 2 filed, APPLY-WITH-CHANGES; it named
  834| five of the main loop's proposals wrong as proposed -- P1, P4, P6, P12, P19 -- and supplied their final texts).  Applied: the product comments
  835| P1-P6 (comment text only -- the file with comments stripped equals the measured base); the docstring P8-P14 and the absent-binary comment
  836| P12; gate 16's comment P15 and P17; P16's synthetic replay, extracted verbatim from the gate but for two marked lines, on which a truncated
  837| log, a doubled sentinel, a line after the sentinel and a nonzero probe exit each red for their own reason
  838| (`wiring122_20261104/GATE16_REPLAY122.out`); P19's identity record (`killtable_20261104/SOURCE_IDENTITY.md`: the shipped probe's syntax tree
  839| equals the measured 122-row copy's, and minus the D31 block equals the 121-row copy's); P20's annotations (`adj_20261104/ANNOTATIONS.md`).
  840| **The adjudication packet carried a false premise of mine** -- that the R5900 has no constructible session on testmips (measured only for
  841| the two ISA II CPUs).  Measured before applying: `-E testmips -C R5900` constructs, and 0x1e there stops with "UNIMPLEMENTED instruction".
  842| Cloud Fable's follow-up on the corrected premise (`adj_20261104/ADJ2_D31_FABLE.md`): D31 ROW-OWED, in a form that does not pin the stop,
  843| HOLD until measured.  The row `r59 mdmx notRI` (`-C R5900`, 0x1e: exit 0, the cause line read, ExcCode not 10) measured as predicted
  844| (`killtable_20261104/d31_20261104/PRETABLE_D31.out` before the run): D31 121/122 with only that row red, the fix 122/122, HEAD 29/122 (the row green -- HEAD's arm already
  845| sent the R5900 to its LQ branch).  `killtable_20261104/TABLE.md` corrected in place, quoting the two sentences it refutes.
  846| 
  847| **Landing edits, none changing code**: `#NNN` -> `#580`; the DETECTOR paragraph's ExcCode/CE pairs reworded into words, since
  848| `check_score_claims.py` reads "10/0" as a score claim; gate 16's three denominator checks; the MANIFEST entries; the regress review's two
  849| docstring corrections (below).  **The citation gate cannot select this block**: `check_cited_artifacts.py` keys on `## Round <digits>` headings,
  850| which this file's newer blocks, this one included, do not use (`citeprefixblind`, filed by `#554`).  Its own resolver, run over
  851| the block by hand at landing, resolves all 13 citations inside this round's artifacts -- after four bare ones were stamped with
  852| their directories: the bare citation of the witness's null leg had resolved, by walk order, to another round's file of the same name.
  853| 
  854| **Seats.**  Every answer is recorded on the row, one entry each, read whole before it was written (the out-of-roster answers by an Opus digest agent at the landing, the rest when they landed).  Pass 1 (research): agy 27, codex 6, deepseek 6, fable5 3, glm 8, grok 8, kimi 6, minimax 2, opus5 4 entries -- the six 2026-11-03 stage panels (`_scratchpad/panel_20261103_103048_next5_mipsprimundec/`, `panel_20261103_103050_next5_mipsprimundec_draft/`, `panel_20261103_111231_next5_mipsprimundec_manual/`, `panel_20261103_111232_next5_mipsprimundec_siblings/`, `panel_20261103_111233_next5_mipsprimundec_witness/`, `panel_20261103_111234_next5_mipsprimundec_port/`), the witness share-findings and v3-review panels (`_scratchpad/panel_20261104_014913_wsf_mipsprimundec/`, `_scratchpad/panel_20261104_044334_v3r_mipsprimundec/`), the Gemini web (Argon) jobs under `_scratchpad/gweb/jobs_20261102_next5/` and `jobs_20261103_adj/`, the 02:0x Opus batch (`_scratchpad/opus_20261104/`) and the cloud Fable rulings.  The agy CLI, deepseek, kimi-k3 and minimax answered the 2026-11-03 panels before the owner's noon roster ruling; they were weighed in no ruling and are recorded as answered outside that roster.  Pass 2 (review): agy 5, codex 1, deepseek 1, fable5 3, glm 1, grok 1, kimi 1, minimax 1, opus5 1 entries (`_scratchpad/panel_20261104_182430_p2_mipsprimundec/`, the cloud answers in `adj_20261104/`); GPT-6 Astra walled until 2026-11-09 and Argon's three failed tries are seat failures, and kimi, deepseek and minimax were not fired under the 11-04 roster, each recorded by name.  The Claude seats ran as Claude Code Cloud routines (owner, 2026-11-04).
  855| 
  856| **The regress review** (Fable-only; cloud Fable 5.1, `adj_20261104/FABLE_REGRESS.md`): 26 checks, 0 floor breaches, 2 record findings, REGRESS-WITH-FINDINGS.  Both record findings (L4, the probe's catches clause: D15 reds the 64 lwc3 exc, epc and pc rows, not "the 64 lwc3 rows"; D16 and D24, both measured red, were missing) are applied in its words, docstring only -- the docstring-stripped syntax tree is unchanged (`killtable_20261104/SOURCE_IDENTITY.md`, regenerated).  Its two UNSETTLED items were settled by measurement: the shipped probe against the measured 122-row copy is P19's identity record, which its packet lacked; and gate 16's totals reconcile -- 289 with the 121-row probe and 293 with the 122-row probe plus the three denominator checks, the other 161 checks identical in both runs (the packet had put the 293 beside the 80-row witness).  A fresh in-situ gate 16 run on the final bytes: PASS 293 (`landing_20261104/gate16_final.out`).  Its extra null medium, `/bin/false`, was measured rather than filed: 17/122, CONTROL=FAIL, as predicted before the run (`landing_20261104/false.out`); `killtable_20261104/TABLE.md` records all of it.  A second lens on the same packet, Gemini 4 Argon (recorded under review, the stage being Fable-only), also returned REGRESS-WITH-FINDINGS; both of its BROKEN claims fall to the packet's own text -- the PC-sync variants sit under the docstring's 'discloses, not claimed' heading, and '29 of 34' counts D31 red through the 122-row probe's R5900 row.
  857| 
  858| **Assessed, not changed.**  Seven pass-1 answers in the port stage asked for a once-only notice on the new arms, as #309's REGIMM default has.  #309 latches its warning because it reports a DEFICIENCY of the emulator, a defined opcode nobody implemented (#279); #580's arms deliver the architectural result on every modelled CPU (Reserved Instruction where the encoding is reserved, Coprocessor Unusable where no coprocessor is present), so there is no deficiency to announce, and no ruling ordered one.  The R3000 sessions plant at the 64-bit address and pass because the address is truncated (GLM, share-findings); were that to change, the R3000 controls would red, so it cannot pass silently.  The VR5432 does not construct on testmips either (measured at landing, `killtable_20261104/vr5432_construct.out`); its ISA IV cells are the R5000 session's, so the detector loses no cell.  The Opus answers the rulings consumed are banked at `adj_20261104/opus/` (two of them only from their transcripts: they had been summarised and never saved).  The adjudication's P7 (whether pmax attaches a coprocessor-3 object: "No coprocessor-3 load or store is
  859| implemented" is true either way), P18 (the variant numbering gaps, recorded in `TABLE.md`) and P22 (superseded by P1).  The ruling of
  860| record's filing (d), the witness's loose `exc` rows that accept 10 or 11, is discharged by the detector, whose `exc` rows want the exact
  861| ExcCode and CE.
  862| 
  863| **Filed, not fixed here.**  From the adjudication: P21, the probe's `mkdtemp` directory is never removed (`mpuprobetmpdir`); D, a
  864| free-running PC-sync row in the shape cloud Fable named -- a breakpoint at the vector reusing the exc/epc/pc reader, admitted only if its
  865| four-part prediction holds (`mpupcsyncrow`).  From the ruling of record: (c) the ISA II CPUs fail to construct on testmips -- with the
  866| VR5432 (`mipscpuconstruct`, all three measured); (a) and (b) ride the existing rows `mipsr5900lqsq` and `mipscop3pmaxstop`.
  867| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_580: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC580: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
