# Reading task: oldrec585 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC585-4a4e` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #585 fbsdrampair (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 124-194 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
  124| # `#585` Records (follow-up, 2026-11-06): `fbsdrampair` names its landing commit `54613aa1`; the committed-tree proofs; the pass-2 receipt; the five record repairs its REGRESS adjudication ruled owed
  125| 
  126| `git ls-tree 54613aa1`, md5s hashed in Python from the committed bytes: `src/devices/dev_footbridge.c` blob `77f7d960d505`, md5 `3de599da2438`; `regress/footbridge_sites_probe.py` blob `4fcc500731c3`, md5 `e0c4a48b9bf1`; `regress/gate_arm.sh` blob `bd310152b24e`, md5 `a059e4392267`; `tools/pipeline/check_probe_wiring.py` blob `d333328563d9`, md5 `4162e7452c7a`.  The working copy against each: dev_footbridge.c the same; footbridge_sites_probe.py the same; gate_arm.sh plus other rounds' uncommitted edits (1 hunk(s)), none in the footbridge block; check_probe_wiring.py plus other rounds' uncommitted MANIFEST entries (2 hunk(s)).
  127| 
  128| The four trees took the committed `dev_footbridge.c` in the landing window and keep it (no restore owed: `regress/artifacts/fbsdrampair/landing_20261105/UPDATE_FBS.out`).  The row's `commits` field names `54613aa1` and its state note names the landing commit.  The `regress/pass2_ledger.tsv` receipt line for `54613aa1`, a landing line in OUTSTANDING_BUGS.md's `#585` section and `matrix.html` re-rendered complete this records commit.
  129| 
  130| **The REGRESS ruling's reviews, adjudicated.**  By the owner's flow of 2026-11-06 ("Land commit and have astra and Grok review then sending back to Fable"), GPT-6 Astra (`ASTRACONF_FBS: DISSENT 2 points`) and Grok 4.7 (`GROKCONF_FBS: DISSENT 4 points`) reviewed Fable 5.1's REGRESS ruling once the landing commit was in its hook, and Fable 5.1 adjudicated their reviews: `FABLEADJ_FBS: 6 ACCEPTED 0 REJECTED VERDICT:LAND-AFTER-RECORDS` (`regress/artifacts/fbsdrampair/regress_20261106/ADJ_FBS.md`; the two reviews and the three briefs are banked beside it).  Both seats confirm the floor (a)-(f); six points, five distinct, all text -- no floor breach, no detector or code repair, no table, probe or gate run owed, no number changed.  This commit makes the five repairs, each in place and quoting what it replaces: (A1) the `fbsdramwrites` row's state note no longer gives the datasheet as "reset 00FC0000h and 0" -- normal reset is 0 for both registers, 00FC0000h only the mask's blank-ROM-programming default (`regress/artifacts/fbsdrampair/adj_p1_20261105/RESET_PREMISE_NOTE.md`); (A2) the probe's docstring no longer says that any extra footbridge diagnostic reds the row -- only M3, O3, X1 and U1 compare the whole list; (G3) arm U is one read of each register (+0x100 into r7, +0x104 into r9), not "M's reads" -- the probe's docstring and two comments, gate 14's comment and the `#585` block below; (G4) the `fbsdramwidth` row's state note gives the common tail's write of `odata` 0, not the `#95` pre-zero, as why a diverted sub-word read still reads 0; (G1, G4) the ruling's C08 and F2, in `regress/artifacts/fbsdrampair/regress_20261106/REG_FABLE_ERRATA.md` beside it -- the banked ruling is kept as written.  The `#585` block's REGRESS paragraph is amended ("no repair owed" held for the fix and the detector, not for the records); the row's regress stage records the two reviews and the adjudication; OUTSTANDING_BUGS.md's `#585` section names the adjudication, and its `fbsdramwidth` line, whose title the landing cut mid-word, is restored whole.
  131| 
  132| **The probe and the gate, checked on the bytes this commit stages.**  `regress/footbridge_sites_probe.py` blob `7b1f3bf22e0f`, md5 `2e8a7cbe2af7`: its AST with every docstring removed equals the landed probe's and `regress/artifacts/fbsdrampair/table1_20261105/probe56_frozen.py`'s, and its tokens outside comments and the module docstring are the landed ones -- so table 1, the settle run and the replay still measure the shipping instrument.  `regress/gate_arm.sh` blob `7461dfd25e3e`, md5 `47be54a210da`: the diff touches comment lines only, and `bash -n` passes.
  133| 
  134| # `#585` (2026-11-06) -- `fbsdrampair`: a guest read of the Footbridge SDRAM base-address mask or offset register no longer ends the emulator; both reads are declined with 0 and announced once
  135| 
  136| Short paths below are under `regress/artifacts/fbsdrampair/`.
  137| 
  138| **The defect.**  `src/devices/dev_footbridge.c`, `DEVICE_ACCESS(footbridge)`: a guest READ of SDRAM_BA_MASK (+0x100) or SDRAM_BA_OFFSET
  139| (+0x104) hit `fatal("[ footbridge read from sdram_ba_mask ]\n"); exit(1);` (and its offset twin), though the DC21285 datasheet gives
  140| both registers as read/write (7.3.9, 7.3.10).  Filed 2026-09-19 from `#539`'s panels, re-graded HIGH by `#554`
  141| (`regress/artifacts/astraretro_20260926/DISPOSITIONS.md`), queued 2026-10-22 as the external-research batch tail 1
  142| (`regress/artifacts/research_20261022/TRIAGE.md` T12; `regress/artifacts/research_20261022/adj_20261022/ADJ_RULINGS.md` D: DECLINE).
  143| 
  144| **Witness (rung 3, before any edit).**  `regress/artifacts/fbsdrampair/witness_20261105/witness_HEAD.out`: `fbsdram_witness.py` on
  145| unmodified `-E cats` (cold debugger, one SDRAM site per run) against `build/gxemul` built from the pre-fix source
  146| (`witness_20261105/CLEARANCE.txt`): W1 (+0x100) and W2 (+0x104) died at the site with exit status 1, each printing HEAD's fatal text
  147| once; W3, the same load with the MMU left on, survived with no diagnostic; `FBSDRAM_WITNESS=SHOWN`, controls OK.  On the fix
  148| (`impl_20261105/witness_FIX.out`) both reads survive and return 0: `FBSDRAM_WITNESS=NOT-SHOWN`.
  149| 
  150| **The fix** (three hunks, `regress/artifacts/fbsdrampair/landing_20261105/STAGED_DIFFS_fbs.md`).  `struct footbridge_data` gains
  151| `warned_sdram_mask_r` and `warned_sdram_offset_r`; each read arm now declines: `odata` stays 0, the common tail returns it (the
  152| `break` is kept), and the register announces once -- `[ footbridge: read of sdram_ba_mask declined, reads 0 (written values are
  153| not kept) (once) ]`, likewise for the offset.  The write arms are unchanged.  The three `#NNN` comment tags are filled with
  154| `#585` (comment-only).  Design: option-set member 3, DECLINE with a per-register latched announce, the declined value ZERO
  155| (`regress/artifacts/fbsdrampair/adj_p1_20261105/ADJ_MYTHOS.md`, `MYTHOSADJP1FBSDRAM: 6 RULINGS 7 ROWS 1 FILED VERDICT:3/ZERO`).  Its two
  156| replications ruled 0x00FC0000 for the mask on the packet's premise that it is the documented reset value; read in the datasheet it
  157| is the blank-ROM programming default, and 7.3.9 and 7.3.10 give reset 0 (`adj_p1_20261105/RESET_PREMISE_NOTE.md`), so ZERO was
  158| implemented (`impl_20261105/IMPL_NOTE.md`).  The SEC working copy and the four trees took the staged dev_footbridge.c in the landing window (comment-only), the three build trees rebuilt with both clearance parts passing (compiler warnings 0 0 0), and the staged probe scored 56 of 56, CONTROL=OK, on the rebuilt build/ (`regress/artifacts/fbsdrampair/landing_20261105/UPDATE_FBS.out`).
  159| 
  160| **Detector.**  `regress/footbridge_sites_probe.py` grows from 37 to 56 rows: six cold-debugger arms, one process each -- M and O read
  161| one register three times, X reads both, W only writes, B writes, reads and writes again, U makes one read of each register (+0x100 into r7, +0x104 into r9) with the MMU on *[corrected 2026-11-06 by the records commit after the landing (`regress/artifacts/fbsdrampair/regress_20261106/ADJ_FBS.md`, G3): this said "U repeats M's reads"; arm M is three reads of +0x100]* as a
  162| control -- each arm's control taken before its first SDRAM access, so the pre-fix build reds the defect rows under green controls;
  163| the 37 older rows print as before (`impl_20261105/IMPL_NOTE.md`).  In `regress/gate_arm.sh` (gate 14) the footbridge block pins
  164| `ROWS=56 of 56` and adds six checks -- the six controls and the thirteen SDRAM rows by distinct green id, M2's and O2's three zero
  165| reads, X1's announce order, B1's and B2's unkept writes: 29 checks on a run.  Measured: the fix 56 of 56, CONTROL=OK
  166| (`impl_20261105/probe_FIX.out`); the pre-fix build 46 of 56, CONTROL=OK, red M1-M3, O1-O3, X1, B1-B3 (`impl_20261105/probe_HEAD.out`);
  167| the block alone on the fix, 29 checks, 0 FAIL (`impl_20261105/fbblock_check.out`).  `check_probe_wiring.py` entries for 4
  168| artifact scripts (`landing_20261105/MANIFEST_fbs.txt`).  Gate 14's footbridge block ran in situ alone at the landing on the updated build/gxemul: 29 checks, 0 FAIL, ROWS=56 of 56, FOOTBRIDGE_SITES_CONTROL=OK (`regress/artifacts/fbsdrampair/landing_20261105/INSITU_fbs.out`).
  169| 
  170| **Table and floor.**  Test-variant table 1 in a scratch clone under a sentinel, its PRETABLE first: 46 legs, each on exactly its
  171| predicted red set and control (`table1_20261105/VERDICT.md`, `table1_20261105/COMPARE.txt`).  Floor (`table1_20261105/SCORES.txt`): (a) HEAD 46/56;
  172| (b) HEAD's two lines reinstated verbatim, `b_exit_mask` and `b_exit_offset`, 49/56 each; (c) an absent binary, `/bin/true` and
  173| `/bin/false`, 1/56 each with CONTROL=FAIL; (d) of all 40 variants (those two, the mask's kept exit and 37 null-repair, latch and announce edits) 34 red, the six
  174| green all predicted: five equivalent (`d_exchanged`, `d_predlatch_mask`, `d_predlatch_offset`, `d_earlyret_mask`, `d_earlyret_offset`) and `d_predlen_mask`,
  175| the disclosed width debt; (e) the probe's SDRAM CONTRACT and NOT COVERED list.  The settle run (`settle_20261105/SCORES.txt`):
  176| `b_exitkept_offset` 51/56, red O1, O2, B1, B2, B3 -- the contract's offset kept-exit, now measured; `d_latchafter_mask` 56/56,
  177| equivalent as predicted.
  178| 
  179| **Pass 2.**  GPT-6 Astra (ultra), `CODEXP2FBS: 8 CELLS SWEPT 0 BREACHES 3 FALSE RECORDS VERDICT:REPAIR`
  180| (`p2_20261105/codex_codex_fbs_p2.txt`): the floor chain closes over two registers x read/write x own latch; width is clause-(e) debt;
  181| three coverage records repaired text-only (`p2_20261105/RECORD_FIXES.md`, `p2_20261105/AST_PROOF.txt`), read by Gemini 4 Argon, the
  182| third then measured by the settle run.  Argon on the pass itself, GLM 5.3 and Grok 4.7: seat failures (`p2_20261105/DISPOSITION.md`).
  183| 
  184| **Regress review** (the Fable-only stage): `FABLEREGFBS: 34 CHECKS 0 FLOOR-BREACHES 1 RECORD-FINDING 1 FILED VERDICT:LAND` (`regress/artifacts/fbsdrampair/regress_20261106/REG_FABLE.md`): the 56-row detector as it ships discharges the floor -- (a) HEAD 46/56 under green controls; (b) the verbatim reinstatement 49/56 at each site, the exit kept after the announce 50/56 (mask) and 51/56 (offset, settle run); (c) three null media 1/56 with CONTROL=FAIL (`table1_20261105/SCORES.txt`), ROWS=56 pinned by equality; (d) the DEPENDS-ON closure (`writeflag` x each arm's latch) rowed in all four cells per arm, accept rows W1/W2/B3 measured failable, and the six green variants re-derived from source -- five equivalent, one disclosed clause-(e) width escape (`len` is tested nowhere in `DEVICE_ACCESS(footbridge)`); (e) the SDRAM CONTRACT's row lists are true of `table1_20261105/SCORES.txt` and `table1_20261105/KILLS.txt`; (f) the zero-valued rows are anchored by their announce rows and the VENDOR_ID control, never alone.  The pass-2 record repairs ship (AST minus docstrings == table 1's frozen instrument).  Gemini 4 Argon's B2 question is settled: `d_misname_mask` prints the offset's line, so B2's `count(SD_OFFSET) == 1` reds, as PRETABLE predicted.  Findings: one INFO (the NOT COVERED list omits the measured-equivalent latch-after-announce form); the width escape is FILED as `fbsdramwidth` (LOW).  No floor breach, no repair owed: land. *[Amended 2026-11-06 by the records commit after the landing.  GPT-6 Astra and Grok 4.7 reviewed this ruling and Fable 5.1 adjudicated their reviews (`regress/artifacts/fbsdrampair/regress_20261106/ADJ_FBS.md`, `FABLEADJ_FBS: 6 ACCEPTED 0 REJECTED VERDICT:LAND-AFTER-RECORDS`): "no repair owed" held for the fix and the detector, not for the records.  The five findings it had passed were repaired text-only in that commit, after the landing rather than before it -- the `fbsdramwrites` row's reset premise (A1), the probe's extra-diagnostic sentence (A2), the ruling's C08 (G1), "M's reads" for arm U in the probe, gate 14's comment and this block (G3), and F2's pre-zero reason in the ruling and the `fbsdramwidth` row (G4); the ruling is kept as banked, its errata beside it (`regress/artifacts/fbsdrampair/regress_20261106/REG_FABLE_ERRATA.md`).]*
  185| 
  186| **Replay.**  Gate 14's footbridge block, as staged, replayed over table 1's 46 banked logs and 11 synthetic logs, the probe call replaced by each log (`regress/artifacts/fbsdrampair/landing_20261105/DRYRUN_fbs.out`): green on exactly the 8 logs the probe scored 56/56 (base, restored, d_earlyret_mask, d_earlyret_offset, d_exchanged, d_predlatch_mask, d_predlatch_offset, d_predlen_mask); HEAD red (7 of 29 checks); the null media red (absent 28 of 29, true 28 of 29, false 28 of 29); every variant the probe scored red, red; the 11 synthetic logs each red on exactly their target pin; every one of the block's 30 checks failed on at least one leg.  The probe ships table 1's instrument with its twelve `#NNN` tags filled
  187| (`landing_20261105/PROBE_IDENTITY_fbs.md`).
  188| 
  189| **Seats.**  One ledger entry per seat file of every stage, from a MECHANICAL inventory (`landing_20261105/inv/fbs_inventory.jsonl`: each file's seat, transport and verdict line, the note naming the stage's ruling or disposition), the non-firings and seat failures by name.  Research: 20 entries, 13 of them answers (agy 4, codex 1, deepseek 1, fable5 9, glm 1, grok 1, kimi 1, minimax 1, opus5 1).  Review: 12 entries, 3 answers (agy 3, codex 1, deepseek 1, fable5 1, glm 1, grok 1, kimi 1, minimax 1, opus5 2).  Regress: the hold and Fable 5.1's answer.  **Filed** (ledger and OUTSTANDING_BUGS.md's `#585` section; LOW): `fbsdramwrites` (the write side: 0x8FFC0000 missing from the mask whitelist, the mask's rejection announce unlatched, the offset announcing every non-zero write; member 7 IMPLEMENT its natural joint disposition with this round's two declines); `fbsdramwidth`.
  190| 
  191| **Of the round's folder** the commit carries 59 of 177 files, 0.76 of 1.86 MB (the coordinator's rule, `landing_20261105/ARTSET_RULE.md`: what a committed record cites, the records, each table's base, HEAD and null logs; `landing_20261105/ARTSET_fbs_why.txt` gives each file's rule).  The other 118 (per-variant build and probe logs, run scripts, pty transcripts, the codex reasoning stream, the generated stubs) stay on disk, denied by the folder's new `.gitignore`, which re-includes the selection and leaves any later file visible (`landing_20261105/ARTGI_fbs.txt`; `landing_20261105/ARTSET_fbs_excluded.txt`).
  192| 
  193| **Landing.**  The citation gate cannot select this block (`check_cited_artifacts.py` keys on `## Round <digits>` headings: `citeprefixblind`, filed by `#554`); its own resolver, run over the block by hand at the landing, resolves all 19 citations to this round's files or the sources it names.
  194| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_585: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC585: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
