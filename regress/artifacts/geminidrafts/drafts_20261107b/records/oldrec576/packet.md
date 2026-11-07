# Reading task: oldrec576 (Gemini web; 2026-11-06)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC576-6eba` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #576 shfcnvsdfpul (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 908-1064 at HEAD 116c5aa9; each line carries its own number -- cite those numbers)

```text
  908| # `#576` Records (follow-up, 2026-11-03): `shfcnvsdfpul` names its landing commit `7ccd4e42`; the committed-tree proofs; the pass-2 receipt; the owner's rulings on `#577`/`#578`
  909| 
  910| `git ls-tree 7ccd4e42` shows `regress/sh_rounding_probe.py` at `100644 blob f7bdc5d31ec0fc1cd469db1718b953a0085cbe34`, blob md5 `73bd60027f35` (the shipped revision; its eight `#576` row tuples are byte-identical to the reconstructed as-run copy, `regress/artifacts/shfcnvsdfpul/killtable_20261102/ASRUN_NOTE.txt`); `src/cpus/cpu_sh_instr.c` md5 `15269057c4f0` (byte-identical in `est/`; the two-part clearance `regress/artifacts/shfcnvsdfpul/landing_20261103/PREP_GATE.out`).  `git diff --numstat 7ccd4e42^ 7ccd4e42`: `9 4 regress/gate_sh_rounding.sh; 51 1 regress/sh_rounding_probe.py; 5 1 src/cpus/cpu_sh_instr.c; 19 1 tools/pipeline/check_probe_wiring.py`; 97 artifact files under `regress/artifacts/shfcnvsdfpul/`.  Gate 10 before the landing: `regress/artifacts/shfcnvsdfpul/landing_20261103/GATE10_RUN.txt`.  The row's `commits` field now names `7ccd4e42`; it stays `held` (the Opus-seat question, the Fable-only regress review, the late seats' findings).
  911| 
  912| **The owner's rulings recorded here.**  02:1x, on `#578`'s deletion ruling: "Reopen" -- a follow-up round weighs pass 1's conditional deassert guard against the shipped deletion; filed as a new queue row (the shipped deletion stays, per the late-dissent rule), and `jazzvecdeassert`'s hold question records the answer.  02:1x, on the Fable-only regress reviews of `#577` and `#578`: "main loop as the seat"; 09:1x, the owner moved the main loop from Fable 5.1 to Opus 5.5 and held any Fable adjudication -- so the 02:1x answer is suspended and both rows keep waiting for Fable's regress review (their hold questions say so).
  913| 
  914| Ledger (the `commits` field and the state note's date; two hold questions; one row filed), this block, the `regress/pass2_ledger.tsv` receipt line, a landing line and a dated section in OUTSTANDING_BUGS.md, `matrix.html` and `fable_queue.md` re-rendered.
  915| 
  916| **Records correction (L4) of `#577`'s follow-up `1630c0d8`.**  Its Records block (and its commit message, which cannot be amended) gave both md5s as
  917| `d41d8cd98f00` -- the md5 of EMPTY input.  Its generator ran `bash -c "git -C C:/... show ... | md5sum"` from Windows Python, where `bash`
  918| is the WSL launcher and the `C:` path does not resolve, so `md5sum` read nothing.  Measured at `bb672a16` with `git show <sha>:<path> | md5sum`
  919| in git-bash: `regress/sh_tlbmulti_probe.py` `fd386f177d33` (its blob id `34cf5ea3...` was right -- `git ls-tree` ran natively),
  920| `src/cpus/cpu_sh.c` `db65b19bab44`; both corrected in place in that block, quoting the old value.  `#578`'s follow-up `87a73fdc` wrote
  921| its md5s as literals and they are right (`37cbfc835297`, `098103e4f82e`).  This follow-up's generator now hashes in Python.
  922| 
  923| # `#576` (2026-11-02, landed 2026-11-03) -- `shfcnvsdfpul`: the SuperH FCNVSD handler stored a truncated integer into FPUL, a register the instruction only reads
  924| 
  925| **The defect.**  `src/cpus/cpu_sh_instr.c`, `X(fcnvsd_fpul_drn)` (HEAD `987cb596` :3049-3063): after interpreting the single-precision
  926| value in FPUL the handler executed `cpu->cd.sh.fpul = (int32_t) op1.f;` before storing the widened double into DRn.  FCNVSD FPUL,DRn
  927| is defined as "(double) FPUL -> DRn" (`_scratchpad/sh4_programming.txt` 9.29, :10866-10871; the pseudocode `fcnvsd(int n, float *FPUL)`
  928| at :10891-10909 assigns only `DR[n>>1]`), so FPUL is read and never written.  Upstream residue: `git log -L3049,3063` returns only the
  929| 0.7.0 import.  Guest-visible consequence: any guest that reads FPUL after an FCNVSD (STS FPUL,Rn; a following FLOAT or FSCA) saw the
  930| truncated integer of the single -- MEASURED 0x00000001 for 1.5, 0xffffffff for -1.5, 0x00000000 for anything below 1 in size and for
  931| -0, and the host's indefinite 0x80000000 for +Inf and a NaN, where the C cast is undefined; for finite values of 2^31 or more the same
  932| indefinite is expected BY READING, not by a row (exactly -2^31, 0xcf000000, is a defined cast and also gives 0x80000000).  The stored
  933| line was the same store FTRC makes, apparently copied; `#297` had GUARDED the FTRC casts behind a range ladder (they remain at :3016
  934| and :3038), it did not remove them -- the bug file's prose row said "removed" and is corrected in place in this commit.  WRONG-RESULT,
  935| MED; no host failure path in the handler.
  936| 
  937| **The witness (rung 3).**  `regress/artifacts/shfcnvsdfpul/witness_20261102/sh_fcnvsd_witness.py` on the unmodified in-tree `-E landisk
  938| -M 64` (the rig kernel loaded for construction only), the cold debugger seeding `fpscr` (DN|PR|RN), `fpul` and the DR2 pair with the
  939| sentinel 0xdeadbeef, the guest executing `fcnvsd fpul,dr2` then `sts fpul,r2 ; mov.l r2,@r1` into a sentinel word (or `fmov.s fr2/fr3,@r1`
  940| for the DRn halves), read back with `dump`.  On a fresh clone of HEAD built in WSL (`/tmp/gxdivw`, binary newer than source):
  941| `witness_head.out` RESULT=3/6 -- the three FPUL rows FAILED-FOR-THE-REASON-UNDER-TEST (got exactly the truncation), the two DRn
  942| liveness rows ok, the FCNVDS control ok (the sibling writes FPUL by design, so the FPUL write channel was live).  The same script on the
  943| fixed clone: `witness_fixed.out` RESULT=6/6.
  944| 
  945| **The fix.**  Delete the one line; a five-line `#576` comment stands where it was.  Nothing else in the handler, its sibling
  946| `X(fcnvds_drm_fpul)` or the decoder (:5061-5068) changes.  Option set: DELETE -- there is no value to ACCEPT or storage to BACK (the
  947| architecture defines no FPUL write), nothing to DECLINE or FAULT (the instruction is legal), and a guarded cast would keep the defect
  948| (pass 1, Fable Q4; Grok Q4).  Diff: `src/cpus/cpu_sh_instr.c` +5 -1 (`killtable_20261102/product.diff`, the final wording; the scratch
  949| clones that were measured carried the pre-adjudication wording "the FTRC store, mis-copied" -- comment-only, and the build does not see
  950| comment text: HEAD and the verbatim-reinstatement mutant, which differ by exactly that comment, share one binary md5), byte-identical in
  951| `GXEMUL-SEC` and `est/`.
  952| 
  953| **The detector.**  Eight rows appended to `regress/sh_rounding_probe.py`'s VECTORS, every row under PR (the manual's defined arm),
  954| each run in both rounding modes: six FPUL readbacks -- `fcnvsd fpul 1.5` / `-1.5` / `0.1` / `-0` / `inf` / `snan` -- and the two DRn halves
  955| `fcnvsd dr hi` / `fcnvsd dr lo` (0x3dcccccd -> 3fb99999 a0000000, the one FINITE input with a nonzero low word; the sNaN widens to the
  956| encoder's all-ones double whose low word is 0xffffffff, measured in `M_h.raw`).  `-0` carries NODN so the table has a DN=0 leg; `0.1`
  957| targets DR0 (0xf0ad) while the others target DR2 (0xf2ad), both halves of the destination seeded with the sentinel; 0x7fc00000 is a
  958| signaling NaN under the SH-4 convention (fraction MSB = 1, manual :4980-4989), hence `snan`, and the existing `ftrcS-nan` row is relabelled
  959| `sNaN+` by the same convention (its oracle unchanged).  Contract (the probe's `#576` comment): disclosed and not rowed -- finite |v| >=
  960| 2^31 (except exactly -2^31, defined), -Inf, a quiet NaN, a subnormal input, +0 (the fixed point); the destination axis is measured only
  961| as the split {DR0, not DR0} on the FPUL channel, the DRn VALUE is read at DR2 only, so a store keyed on DR4..DR14 or a DRn store
  962| suppressed at DR0 escapes; the state axes FPSCR.SZ, FPSCR.FR, the reserved RM encodings 10/11, the FPSCR cause/enable/flag bits and a
  963| delay slot are not varied; every row runs with FD clear, PR set and SZ clear ([SZ,PR] = 11 is reserved, manual :5148).
  964| `regress/gate_sh_rounding.sh`: `vector-mode pairs run` 36 -> 52 (EQUALITY), the eight names in the per-row `both modes correct` loop,
  965| `vectors that discriminate the two modes` unchanged at 9, the two prose counts corrected.
  966| 
  967| **The pre-table check and the kill table** (`regress/artifacts/shfcnvsdfpul/killtable_20261102/`; scratch clones only, a `.MUTANT`
  968| sentinel per mutant; each `<leg>.raw` names its binary, md5 and freshness):
  969| 
  970|     base_head (HEAD)                              40/52   the six FPUL rows red in both modes
  971|     fixed                                         52/52
  972|     M_b   the store reinstated verbatim (b)       40/52   the six FPUL rows   (binary md5 == HEAD's: the reinstatement IS the pre-fix build)
  973|     M_c   identity body, writes nothing (c)       48/52   dr hi, dr lo
  974|     M_d   store 0x80000000 for Inf/NaN only       48/52   inf, snan
  975|     M_f   store only when FPSCR.DN is clear        50/52   -0 (the NODN row alone)
  976|     M_g   store for every destination but DR0     42/52   the five DR2 rows
  977|     M_gm  store for DR0 only (M_g's mirror)        50/52   0.1 (the DR0 row alone)
  978|     M_h   the result's low half stored into FPUL  40/52   the six FPUL rows
  979|     M_i   the two DRn halves exchanged             48/52   dr hi, dr lo
  980|     M_z   store 0 on a zero operand                50/52   -0
  981| 
  982| Floor: (a) 40/52; (b) 40/52; (c): measured at `killtable_20261102/M_c.raw`, carried by the two DRn rows only, as the contract says;
  983| (d) the fix is a pure deletion, so (d) is the removed store re-introduced under a different predicate -- DN (M_f), destination in both
  984| directions (M_g, M_gm) and zero-operand (M_z), all red; (e) the contract above; (f) not applicable.  Provenance of the predictions:
  985| `PRETABLE.out` was written before the base leg BY THE AUTHOR'S ACCOUNT; its own mtime no longer proves the order because the M_g
  986| correction was written into it in place at 17:29 (future rounds: write corrections to a sibling file).  The EVIDENCED pre-leg record is
  987| `IMPLEMENTATION_PLAN_20261102_1715.md` (mtime 17:15:08), which predicts the base, fixed, M_b, M_c, M_h, M_i and M_z scores as measured,
  988| predicts M_f conditionally ("green unless the NODN row exists") and M_g only for the all-DR2 shape it describes, and is silent on M_d and
  989| the mirror; the M_g prediction for the DR0 instrument exists only in `PRETABLE.out`, inverted (it named the DR0 row as the red one; the
  990| five DR2 rows are), and M_gm was built after the table to measure the mirror the DR0 row exists for.  `PRETABLE.out`'s CHANNEL line
  991| names a mutant `M_e` (an RZ-only store) that was not built: PREDICTED caught, not measured -- M_b's toward-zero legs showed the FPUL channel red under a store in that mode.  The base
  992| leg ran under its own invocation (17:17:4x-17:18:13) that `KILLTABLE.log` does not record; the first M_gm apply failed on a malformed
  993| string in the mutator and was repaired before the leg ran (`KILLTABLE.log` carries both lines; the preserved `mutate576.py` is the
  994| repaired copy -- the first preserved copy did not parse, caught at pass 2).  The instrument the table ran is preserved as the
  995| reconstruction `sh_rounding_probe.ASRUN_1716.py` (HEAD plus the hunk the pass-2 packet inlined; `ASRUN_NOTE.txt`); the raw logs print the
  996| as-run label `ftrcS-nan qNaN+`, the shipped probe prints `sNaN+` and carries the post-table contract comments; the eight row tuples are
  997| byte-identical in both.  No dead session in any leg.
  998| 
  999| **The panel** (owner roster 2026-11-02: GPT-6 Astra, Fable 5.1, glm-5.3, Argon = Gemini web, Grok 4.7).  Pass 1
 1000| (`regress/artifacts/shfcnvsdfpul/pass1_20261102/`, copied at the landing from `_scratchpad/w576/pass1_20261102/`; the brief from the 2026-10-30 scoping draft with the measured witness inlined): Argon PROCEED, glm-5.3
 1001| PROCEED WITH CHANGES (4), Grok 4.7 PROCEED WITH CHANGES (4), Fable 5.1 PROCEED WITH CHANGES (4), Astra PROCEED WITH CHANGES (3) on its
 1002| third attempt (two earlier attempts: a wall, then an empty answer with no wall text).  Findings F1-F9 and their dispositions are in the
 1003| pass-2 packet's section 0: PR on every row (Grok); DR2 encoded with both halves seeded (Grok); one row on DR0 (Fable); one FPUL row
 1004| DN-clear via NODN at zero cost (Fable; glm had asked for a row, Grok for a disclosure); `nan` -> `snan` (Fable); the disclosed classes
 1005| (Fable, Grok); `#297` "guarded" not "removed" (all); `inf` kept against Fable's drop (Grok: 16 sessions proportionate; Fable withdrew on
 1006| the measured cost); Astra's three: the record wording, an explicit contract, the validation completed before shipping.  Pass 2
 1007| (`pass2_20261102/`, the diff, the handler after the edit, the detector diff, PRETABLE and the table inlined): Argon SHIP; glm-5.3 SHIP
 1008| WITH CHANGES (2); Grok 4.7 SHIP WITH CHANGES (3); Fable 5.1 SHIP WITH CHANGES (3); Astra SEAT WALLED (the hotmail login's weekly limit,
 1009| "try again at Nov 8th").  Every seat: the code is right; the changes were to artifacts and records -- the preserved mutator (above), the
 1010| destination-axis overclaim and the undisclosed state axes (now in the contract), the `ftrcS-nan` relabel, the gate prose, the PRETABLE
 1011| timing sentence, "the one FINITE input", "apparently copied", the indefinite "by reading", the PR-reserved class never filed, the M_b/HEAD
 1012| md5 equality, `M_e` not built.  The adjudication pass (`f2_20261102/`): Fable 5.1 adjudicating, F2 VERDICT: RATIFY WITH CHANGES (5) --
 1013| P1-P13 upheld or refined, D1 ruled DISCLOSE (no re-target, no added rows: the body tests nothing on the destination, every destination
 1014| cell is clause (e), and a row change after pass 2 would owe its own pass and a re-stamped table), D2 ruled withdraw-the-literal-and-cite-
 1015| the-plan; Grok 4.7 RATIFY WITH CHANGES (5), agreeing on D1 and D2 and adding the [SZ,PR] reservation and the wider PR class; Argon
 1016| upheld D1 and refined "numeric" to "finite"; glm-5.3 SEAT DOWN (the Ollama cloud endpoint answered `403 Forbidden, error code 1010` to
 1017| every model); Astra's F2 RATIFY WITH CHANGES (5) arrived at 20:3x after its first reset.  **The owner ruled (17:4x) that this commit HOLDS until Astra
 1018| answers**; Astra's PASS 2 arrived at 01:50 on 2026-11-03 after the 01:10 reset, SHIP WITH CHANGES (4): the product comment's "writes DRn
 1019| only" (architectural FCNVSD also has FPSCR cause/flag effects the model does not implement -- recorded here, the comment left as written:
 1020| it names the registers the handler touches), the contract's destination and state disclosures and exactly -2^31 (present), the PRETABLE
 1021| mtime wording (the paragraph above already says the mtime no longer proves the order), and four record corrections -- the FTRC casts at
 1022| :3016/:3038 GUARDED (done), "destroys FPUL on every FCNVSD" false for +0 (the bug file's prose row now says "spuriously overwrites"),
 1023| the gate prose's vector count (27 vectors: 25 two-mode plus two single-mode, nine discriminating -- corrected in the staged gate), the
 1024| PR-reserved class given its filing (`shfpprreserved`, below).  It also named two escapes the contract discloses: an FD=1 reinstatement
 1025| (every row runs with FD clear) and a store keyed to DR4 (the destination axis).  The owner lifted the hold at 02:1x ("Land it now").
 1026| **Late seats under the owner's 21:3x roster** (agy, Grok, GLM 5.3, Codex): agy (file-reading) pass 1 PROCEED WITH CHANGES (5) and F2 RATIFY WITH CHANGES (5); GLM 5.3 F2 RWC (6) (its 17:53
 1027| firing was the 403/1010 transport failure); DeepSeek pass 1 PWC (2) and F2 RWC (1); minimax pass 1 PWC (5) and F2 RWC (4); kimi pass 1 PWC (4)
 1028| and F2 RWC (3) -- every late seat holds the one-line deletion right and complete.  **Their findings are NOT adjudicated here**: at 09:1x
 1029| the owner moved the main loop to Opus 5.5 and held any Fable adjudication, so they are the row's hold question.  The main loop applied
 1030| only three corrections that make the record state what was measured or what the diff does: the staged gate's vector-count prose now
 1031| reads "25 two-mode vectors x 2 + #303's two single-mode rows = 52" (the disposition Fable wrote before the switch; comment-only, made
 1032| AFTER the gate-10 run, which ran the same checks); the Records paragraph below describes the bug-file edit as the diff makes it; and the
 1033| unbuilt `M_e`'s sentence says predicted, not caught.  A sweep GLM asked for, run as a fact: `cpu_sh_instr.c` writes `cd.sh.fpul` only in
 1034| FTRC's two arms (the guarded casts at :3016/:3038 and their 0x80000000/0x7fffffff ladders) and in FCNVDS (:3079).  The Opus seat was on none of this round's
 1035| rosters and is held with its question (the row's hold question).
 1036| 
 1037| **Not changed (assessed, intentionally left).**  FCNVDS writes FPUL by design and keeps its arm.  The DN=1 subnormal input widens to
 1038| its true value where the manual treats it as zero: `#303`'s named gap, untouched.  The reserved precision combinations (below) and the
 1039| DRn NaN pattern (`shnanquiet`) are filed class rows, not this round's.
 1040| 
 1041| **Records.**  `OUTSTANDING_BUGS.md`: the `shfcnvsdfpul` id entry (:24099) marked fixed by this commit; the prose row (:8241) keeps its
 1042| text and gains a dated bracket that marks it fixed and corrects two of its claims in place -- "the same UB `(int32_t)` cast `#297` removed
 1043| from FTRC" (`#297` GUARDED the FTRC casts behind a range ladder; they remain at :3016 and :3038) and "destroys FPUL on every FCNVSD" (false
 1044| for +0: the store spuriously overwrites FPUL, corrupting inputs such as -1.5); two filings -- `shfpprreserved` (LOW: the manual's pseudocode calls `undefined_operation()` at SEVEN sites,
 1045| `grep -n undefined_operation _scratchpad/sh4_programming.txt` -- FCNVDS :10770 and FCNVSD :10883 at PR=0, FIPR :11251, FMAC :11429, FRCHG
 1046| :12234, FSCHG :12270 and FTRV :12852 at PR=1 -- and never defines it; the manuals call the combination "undefined", not an exception; the
 1047| model performs the operation; `#316`'s FSRRA (`cpu_sh_instr.c:3279-3295`) is the fork's one precedent for a reserved precision
 1048| combination; a POLICY is owed, not a wrong-result fix) and `shnanquiet` (LOW: SH NaN RESULTS use the shared encoder's all-ones pattern,
 1049| which SH-4 classes as signaling where hardware emits the quiet 0x7fbfffff / 0x7ff7ffff...; the MIPS model canonicalises, `#255`; the SH
 1050| tree does not).  Ledger: `shfcnvsdfpul` set `held` (the Opus-seat question; the Fable-only regress review precedes closing), witness
 1051| `probe:regress/artifacts/shfcnvsdfpul/witness_20261102/sh_fcnvsd_witness.py`, detector rows named, seat entries per pass naming their dirs
 1052| (`regress/artifacts/shfcnvsdfpul/pass1_20261102/`, `pass2_20261102/`, `f2_20261102/`); the two rows opened.  `_scratchpad/scope_sh_20261030/SCOPING.md`'s "removed" wording is the
 1053| same correction (scratch, not committed).  The gate file's working copy holds three unrelated uncommitted hunks (the peer's; old :530/:590/:822);
 1054| the commit stages the gate from a HEAD-based copy carrying only this round's two hunks (#548 recipe; HEAD already carries `#577`'s), and the
 1055| peer's hunks are merged back into the working tree.  **Landing** (`regress/artifacts/shfcnvsdfpul/landing_20261103/PREP_GATE.out`): two-part
 1056| clearance on `build/`, `build-asan/` and WSL `/tmp/gxsec-build` (cmp CLEAN against SEC, binary newer than `cpu_sh_instr.c`; `est/`: source
 1057| tree, part 2 N/A); gate 10 run end to end on the applied tree with the staged gate in place: 416 of 417 checks ok (`landing_20261103/GATE10_RUN.txt`) --
 1058| `vector-mode pairs run` 52 and `vector-mode pairs correct` 52, all six FPUL rows correct in both modes; the one red, `gdrom_default rows run`
 1059| got=62 want=60, is the peer's uncommitted 62-row `gdrom_default_probe.py` in the working tree against HEAD's pin of 60, a file this commit
 1060| leaves at HEAD's copy (the same red `#572`'s run recorded at `wdclbaaddr/pass2_20261024/GATE10_RUN.txt:362`).  The gate as run was HEAD
 1061| plus the round's hunk; the committed copy differs from it in two comment lines only, the vector-count prose corrected after the run
 1062| started (`landing_20261103/GATE_ASRUN_NOTE.txt`: comment-stripped compare identical).  Process notes carried to the carrier's PRETABLE rule: write corrections to a sibling file so the original's mtime keeps
 1063| proving the order; preserve the as-run instrument beside the table at run time, not afterwards.
 1064| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_576: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC576: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
