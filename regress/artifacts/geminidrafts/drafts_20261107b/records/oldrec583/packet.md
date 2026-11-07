# Reading task: oldrec583 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC583-5519` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #583 pvrrenderexit (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 271-347 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
  271| # `#583` Records (follow-up, 2026-11-05): `pvrrenderexit` names its landing commit `e1a091e4`; the committed-tree proofs; the pass-2 receipt
  272| 
  273| `git ls-tree e1a091e4`, md5s hashed in Python from the committed bytes: `src/devices/dev_pvr.c` blob `0b92af702196`, md5 `f2fc508e34c5`; `regress/pvr_zwrite_probe.py` blob `c3b6a971b29b`, md5 `c70b1d2fd8f7`; `regress/gate_arm.sh` blob `3c18ef5026ba`, md5 `36f7b1bed04c`; `tools/precommit_check.sh` blob `b73e831d38d2`, md5 `ce25fc040cc2`; `tools/pipeline/check_probe_wiring.py` blob `807f15c11c1c`, md5 `88b4d0728cf5`.  The working copy against each: dev_pvr.c the same; pvr_zwrite_probe.py the same; gate_arm.sh plus other rounds' uncommitted edits (4 hunk(s)), none touching the pvr block; precommit_check.sh the same; check_probe_wiring.py plus other rounds' uncommitted MANIFEST entries (2 hunk(s)).
  274| 
  275| The four trees took the committed `dev_pvr.c` in the landing window and keep it (no restore owed: `regress/artifacts/pvrrenderexit/landing_20261105/UPDATE_PVR.out`).  The row's `commits` field names `e1a091e4` and its state note names the landing commit.  The `regress/pass2_ledger.tsv` receipt line for `e1a091e4`, a landing line in OUTSTANDING_BUGS.md's `#583` section and `matrix.html` re-rendered complete this records commit.
  276| 
  277| # `#583` (2026-11-05) -- `pvrrenderexit`: a Dreamcast PowerVR render with the Z-write-disable bit set no longer ends the emulator; the bit is honoured -- the depth test kept, only the depth store skipped
  278| 
  279| **The defect.**  `src/devices/dev_pvr.c`, `pvr_render()`: a polygon header whose ISP/TSP word 1 sets bit 26 (Z-write disable) hit
  280| `fatal("pvr: no zwrite? not implemented yet.\n"); exit(1);`.  Filed 2026-10-02 by `#554` (batch 3d, `devpvr:F4`:
  281| `regress/artifacts/astraretro_20260926/DISPOSITIONS.md`); queued 2026-10-22 as research batch 10 of 10
  282| (`regress/artifacts/research_20261022/TRIAGE.md` T5), this exit only: the file's other three exits keep their own disposition.
  283| 
  284| **Witness (rung 3, before any edit).**  `regress/artifacts/pvrrenderexit/witness_20261104/WITNESS.md`: the 9-row first probe on
  285| unmodified `-E dreamcast` (guest stores through the SH-4 decoder: one polygon header, then STARTRENDER) scored 7/9, SYMPTOM=PRESENT,
  286| on a clone of HEAD `ebe5af82` and on `build/gxemul`, the Z-off session ending with exit status 1; `/bin/true` 3/9, a missing binary
  287| 0/9, CONTROL=FAIL.
  288| 
  289| **The fix** (five hunks, `regress/artifacts/pvrrenderexit/landing_20261105/STAGED_DIFFS_pvr164.md`).  `struct pvr_data` gains
  290| `zwrite_disabled`; `pvr_render()` clears it at every render and sets it from each polygon header's bit 26 in place of the exit;
  291| `simpleline()` and `texturedline()` keep the depth test and skip only the `vram_z` store while it is set.  The six `#NNN` comment tags
  292| are filled with `#583` (comment-only).  Design: disposition 7 IMPLEMENT, no announce, a per-render reset
  293| (`regress/artifacts/pvrrenderexit/adj_20261104/FABLE_FINAL_r2.md`, `CLOUDFINAL ... VERDICT:GO-WITH-CHANGES`; merged by
  294| `regress/artifacts/pvrrenderexit/adj_20261104/RECON_FABLE.md`, `VERDICT:MERGE`).  The SEC working copy and the four trees took the staged dev_pvr.c in the landing window (comment-only), the three build trees rebuilt with both clearance parts passing (compiler warnings 0 0 0), and the staged probe scored 164/164, CONTROL=OK, SYMPTOM=ABSENT on the rebuilt build/ (`regress/artifacts/pvrrenderexit/landing_20261105/UPDATE_PVR.out`).
  295| 
  296| **Detector.**  `regress/pvr_zwrite_probe.py`, 164 rows over 62 cold `-E dreamcast` debugger sessions, pixels read back through the
  297| linear VRAM window.  In `regress/gate_arm.sh` (gate 14) before the `hpcmipsctor` block: 173 checks, RESULT pinned 164/164 by equality,
  298| CONTROL=OK, SYMPTOM=ABSENT, every row by name; SCORE_CLAIMS_MANIFEST 48 -> 49; `check_probe_wiring.py` entries for the probe
  299| and 53 artifact scripts (`landing_20261105/MANIFEST_pvr.txt`).  Final instrument (`r7_20261105/table7/SCORES.txt`): HEAD 78/164
  300| SYMPTOM=PRESENT, the fix 164/164, `/bin/true` 9/164, an absent binary 0/164, `/bin/false` 1/164, each CONTROL=FAIL.  Last in situ on
  301| the 51-row probe (`regress/artifacts/pvrrenderexit/wiring_20261105/gate14_pvr_zwrite.log`).  Gate 14's pvr block ran in situ alone at the landing on the updated build/gxemul: 173 checks, 0 FAIL, PVR_ZWRITE_RESULT=164/164, PVR_ZWRITE_CONTROL=OK (`regress/artifacts/pvrrenderexit/landing_20261105/INSITU_pvr.out`).
  302| 
  303| **Tables and floor.**  Six test-variant tables, 51 to 164 rows (`det_20261104/table1/` .. `r7_20261105/table7/`), each in a scratch
  304| clone under a sentinel, a PRETABLE first.  Table 7 (`r7_20261105/table7/CHECK.txt`: `TABLE7_CHECK hits=208 misses=0
  305| not_predicted=4`): 206 variants, 172 red on exactly their predicted rows, 30 green, 4 undefined-behaviour variants not predicted.
  306| Floor (`r7_20261105/table7/SCORES.txt`): (a) HEAD 78/164; (b) the exit reinstated verbatim (`B1_exit`) 78/164; (c) the three null media
  307| above; (d) repair 7's twelve register cells red on their predicted rows
  308| (`regress/artifacts/pvrrenderexit/regress_20261105/REG2_MYTHOS_local.md`); (e) the contract in the probe's docstring.
  309| 
  310| **The repair chain.**  Pass 2 on the 51-row detector (GLM 5.3, Grok 4.7, Argon, cloud Fable 5.1 and Opus 5.5: the detector short,
  311| the fix right, `p2_20261105/R2_SUMMARY.md`), ruled by cloud Mythos 5.1; GPT-6 Astra's passes 3 to 8, ruled by local Mythos 5.1:
  312| class closures (repair 3, 128 rows), the swap's exchange bodies and fractional compares under round rule D2-F (repair 4, 140), the
  313| deletion closure and negative starts (repair 5, 148), every edit shape of the exchange bodies enumerated and graded DEBT (pass 6);
  314| pass 7, 0 breaches over 272 cells.  The regress review's candidate, the guards' constant 0 against `fb_base`, was graded FLOOR by
  315| reading (i) and closed by repair 7 (164 rows); pass 8, 0 breaches over 67 cells.  Verdict lines (under
  316| `regress/artifacts/pvrrenderexit/`):
  317| 
  318| ```
  319| p2 ruling  p2_20261105/ADJ_MYTHOS_r4.md  MYTHOSADJP2PVR: 26 RULINGS 3 CHANGES 3 FILED VERDICT:APPLY-WITH-CHANGES
  320| p3         p3_20261105/codex_codex_pvr_p3.txt  CODEXP3PVR: 84 CELLS SWEPT 15 BREACHES 5 FALSE RECORDS VERDICT:REPAIR
  321| p4         p4_20261105/codex_codex_pvr_p4.txt  CODEXP4PVR: 177 CELLS SWEPT 14 BREACHES 8 FALSE RECORDS VERDICT:REPAIR
  322| p4 ruling  adj_p4_20261105/ADJ_MYTHOS_local.md  MYTHOSADJP4PVR: 11 FLOOR 3 DEBT 8 RECORDS UPHELD VERDICT:REPAIR-4
  323| p5         p5_20261105/codex_codex_pvr_p5.txt  CODEXP5PVR: 181 CELLS SWEPT 27 BREACHES 2 FALSE RECORDS VERDICT:REPAIR
  324| p5 ruling  adj_p5_20261105/ADJ_MYTHOS_local.md  MYTHOSADJP5PVR: 3 FLOOR 26 DEBT 2 RECORDS UPHELD VERDICT:REPAIR-5
  325| p6         p6_20261105/codex_codex_pvr_p6.txt  CODEXP6PVR: 108 CELLS SWEPT 20 BREACHES 1 FALSE RECORDS VERDICT:REPAIR
  326| p6 ruling  adj_p6_20261105/ADJ_MYTHOS_local.md  MYTHOSADJP6PVR: 0 FLOOR 29 DEBT 1 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS
  327| p7         p7_20261105/codex_codex_pvr_p7.txt  CODEXP7PVR: 272 CELLS SWEPT 0 BREACHES 7 FALSE RECORDS VERDICT:REPAIR
  328| reg ruling adj_reg_20261105/ADJ_MYTHOS_local.md  MYTHOSADJREGPVR: 16 FLOOR 1 DEBT VERDICT:REPAIR-7  [16 FLOOR corrected to 12 by pass 8: adj_reg_20261105/ADJ_MYTHOS_local.errata.md]
  329| p8         p8_20261105/codex_codex_pvr_p8.txt  CODEXP8PVR: 67 CELLS SWEPT 0 BREACHES 1 FALSE RECORDS VERDICT:REPAIR
  330| ```
  331| 
  332| **Regress review** (the Fable-only stage, local Mythos 5.1 in the fable5 slot): `MYTHOSREGPVR: 32 CHECKS 0 FLOOR-BREACHES 5 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS` (`regress/artifacts/pvrrenderexit/regress_20261105/REG_MYTHOS_local.md`): the floor discharged, the pins sound, the 30 greens placed; one candidate cell for the ruler; R1, R3, R5 fixed in the probe's text, R2 and R4 carried here.  Its follow-up on the 164 rows, `MYTHOSREG2PVR: 23 CHECKS 0 FLOOR-BREACHES 1 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS` (`regress/artifacts/pvrrenderexit/regress_20261105/REG2_MYTHOS_local.md`): the candidate closed, measured; one record, this re-pin.  The 148-row records it read are banked
  333| unchanged (`landing_20261105/REGRESS_pvr.md`, `landing_20261105/DRYRUN_pvr.out`); the re-pinned ones carry the suffix 164.
  334| 
  335| **Replay.**  Gate 14's pvrrenderexit block, as staged, replayed over table 7's 212 banked logs and 18 synthetic logs, the probe call replaced by each log (`regress/artifacts/pvrrenderexit/landing_20261105/DRYRUN_pvr164.out`): base (the fix) green; HEAD red (90 of 173); /bin/true red (159 of 173); an absent binary red (168 of 173); /bin/false red (167 of 173); restored green; the 30 variants the probe scored green green and the 176 it scored red red, each log's failing row pins exactly its PVR_ZWRITE_RED list; the 17 synthetic logs that should red each red on the pins they target, and a line after the sentinel stays green; every one of the block's 173 checks failed on at least one leg.  The probe ships table 7's instrument with its docstring brought to the landing: the round number, eighteen
  336| older N/M scores in words (`landing_20261105/PROBE_IDENTITY_pvr164.md`).
  337| 
  338| **Seats.**  One ledger entry per seat file of every stage, from a MECHANICAL inventory (`landing_20261105/inv/pvr_inventory.jsonl`: each file's seat, transport and verdict line, the note quoting the stage's DISPOSITION.md or JOB.txt), the non-firings and seat failures by name.  Research: 75 entries, 63 of them answers (per seat: agy 31, codex 9, deepseek 6, fable5 7, glm 6, grok 7, kimi 3, minimax 3, opus5 3).  Review: 39 entries, 31 answers (per seat: agy 7, codex 8, deepseek 1, fable5 11, glm 3, grok 3, kimi 1, minimax 1, opus5 4); kimi, deepseek and minimax not fired.  Regress: two.  **Filed** (ledger and OUTSTANDING_BUGS.md's `#583` section; all LOW): `pvrswapdebt` (the exchange bodies' debt), `pvruvfpundet` (8 UV cells to measure), `pvrdepth2bpp` (a sampled value equal to a body-read field or a guard's constant), `dcstdincap` (the dreamcast debugger's stdin cap), `pvrmodvolbit26` (bit 26 in a modifier-volume header).
  339| 
  340| **Owner flags, open:** D2-F into the carrier beside rule D2 (`regress/artifacts/pvrrenderexit/adj_p4_20261105/ADJ_MYTHOS_local.md`
  341| section 2, with its R3 corrections); reading (i), which widens the clause-(2) swap sources every later round enumerates
  342| (`regress/artifacts/pvrrenderexit/adj_reg_20261105/ADJ_MYTHOS_local.md`).
  343| 
  344| **Of the round's folder** the commit carries 1827 of 51335 files, 84.4 of 890.0 MB (the coordinator's rule, `landing_20261105/ARTSET_RULE.md`: what a committed record cites, the records, each table's base, HEAD and null logs; `landing_20261105/ARTSET_pvr_why.txt` gives each file's rule).  The other 49508 (session transcripts, build and probe logs) stay on disk, denied by the folder's new `.gitignore`, which re-includes the selection and leaves any later file visible (`landing_20261105/ARTGI_pvr.txt`; `landing_20261105/ARTSET_pvr_excluded.txt`).
  345| 
  346| **Landing.**  The citation gate cannot select this block (`check_cited_artifacts.py` keys on `## Round <digits>` headings: `citeprefixblind`, filed by `#554`); its own resolver, run over the block by hand at the landing, resolves all 11 citations to this round's files or the sources it names.
  347| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_583: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC583: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
