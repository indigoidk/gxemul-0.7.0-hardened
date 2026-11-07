> BANKED 2026-11-07 from `_scratchpad/gweb/jobs_20261106_kits/OLDEST3_RECORDS.md` by the records commit.  Fable 5.1's ruling (`RULING.md`, beside this file) SUPERSEDES it where they differ -- four texts amended, one accepted seat claim reversed (`#577`'s OUTSTANDING_BUGS.md citations are not pre-fix).  Two citations below gained their missing parent directory, the ruling's errata.  `_scratchpad/` paths named below are provenance, not durable.

# Records checks of the three oldest open rounds -- verified by the main loop, 2026-11-06 21:5x

Rounds: #569 m88kscaledbyte (`66920157`), #570 m88kbuserrregs (`c8fcb5ff`), #571 ppcdsformxo (`cb21331c`).  All three are
landed and owe their Fable regress review.  Seats: agy (gemini-4-argon-high, file-reading, every number checked against its
artifact; `agy_rec569_out.txt` / `agy_rec570_out.txt` / `agy_rec571_out.txt`) and Gemini web (packet-fed, block inlined;
`oldrec569/` / `oldrec570/` / `oldrec571/gemini_web.out`).  **Every seat claim below was checked by the main loop with git
or grep before being written here; the command's result is quoted.**  Line numbers `:NNNN` are CHANGELOG.md at
**`54613aa1`** -- the `CHANGELOG_HEAD.md` snapshot in this folder, `cmp`-identical to `git show 54613aa1:CHANGELOG.md`.
At HEAD `116c5aa9` every one of them is **+10** (the #585 records follow-up added ten lines at the top).

Seat totals: agy RECCHECK_569 145/144/1/0/0, RECCHECK_570 140/132/5/3/3, RECCHECK_571 140/134/2/4/0 (numbers, supported,
contradicted, uncited, missing paths); Gemini RECBLOCK_569 1/3/3, RECBLOCK_570 2/2/2, RECBLOCK_571 2/1/2 (contradictions,
uncited, overclaims).

## #570 m88kbuserrregs -- FIVE CONFIRMED WRONG RECORDS (L4), one citation to qualify

| # | line | the record says | measured | seat | disposition |
|---|---|---|---|---|---|
| 1 | :2104 | `regress/m88k_buserr_probe.py` (new; **836 lines**) | `git show c8fcb5ff:regress/m88k_buserr_probe.py \| wc -l` = **848** (836 is rev 2's count: `repair1_20261024/rev2c_equivalence.txt:3-5`, rev 2 836 lines, rev 2c 848) | agy | **L4 CONFIRMED** -- "(new; 848 lines; the measured rev 2 is 836)" |
| 2 | :2110, :2112 | `repair1_20261024/rev2b.docstring.diff`, `rev2b_equivalence.txt`, `rev2b_rowcompare.txt` | at c8fcb5ff these live in `repair1_20261024/superseded_9046d774/` (`git ls-tree c8fcb5ff`); the shipped rev 2c's evidence is `rev2c.docstring.diff`, `rev2c_equivalence.txt` (stripped 28,722 bytes both, cmp IDENTICAL -- the block's own numbers), `rev2c_rowcompare.txt` | agy | **L4 CONFIRMED** -- cite the rev2c files; the paragraph names the shipped file "revision 2c" and cites the superseded 2b proofs |
| 3 | :2157 | `tools/pipeline/check_probe_wiring.py` **(+11)** | `git diff --numstat c8fcb5ff^ c8fcb5ff` = **15 0** -- which the block's own :2048 states | agy | **L4 CONFIRMED** -- (+15); +11 was BUILD_REPORT.md:33's pre-repair count |
| 4 | :2248 | "every one of the **224 objects and the binary**" | `objmd5_before.txt`: 224 lines = **223** `.o` + `gxemul` (`grep -vc '\.o$'` = 1) | agy | **L4 CONFIRMED** -- "the 223 objects and the binary (224 entries)" |
| 5 | :2083 | "NO_EXCEPTIONS callers **-- the debugger --** never reach the writes" | the block's own :2241 records the round correcting this exact gloss in `memory_rw.c`: "(the debugger)" -> "(e.g. the debugger's dump)", because the debugger's STEP pre-read is unsuppressed and is the round's own `ifetch` channel | Gemini (agy checks numbers only and could not see it) | **L4 CONFIRMED** -- the record repeats the overclaim its round removed from product code |
| 6 | :2134 | `cpu_m88k.c:811-819` (SFRZ -> ERROR) | PRE-FIX numbering: the SFRZ test is at :811 in `c8fcb5ff^` and :815 in `c8fcb5ff` (the round's +4) | agy | QUALIFY -- "(pre-fix `:811-819`; `:815-823` from c8fcb5ff)"; the round itself filed `m88kcitedrift570` for eight such citations |

Not defects (checked): :2244 `dev_mvme187.c:139,151` -- TRUE at c8fcb5ff (`grep -n 'CMMU_IDR\]'` -> 139 151), moved to
186 198 by #581 `03d97106` after landing; `dev_luna88k.c:953,964` true at c8fcb5ff and HEAD.  Gemini's "27 measurements,
27 MATCH vs 25 enumerated" -- REJECTED: `table1_20261023/SCORES.txt` carries 27 MATCH legs (pre fix L1 L3 L3/w24 L4 L4/w24
L5 L5b L6 L6b L7 L8 L8b L9-L19 L21 L22); Gemini's count missed L1, L3/w24, L4/w24.  Gemini's "every product edit kept its
line count vs +4 lines" -- REJECTED: :2231 is the round's fix (+4 in cpu_m88k.c and dev_luna88k.c), :2245 the pre-commit
repair's equal-range comment hunks.  agy's three UNCITED (:2057 T36 date, :2061 OpenBSD trap.c lines, :2228-2230
mvme187cmmuowner) are low value; the trap.c passages are inlined at `pass1_20261023/packet.md:964-971` and could be cited.

## #569 m88kscaledbyte -- no confirmed wrong record

* agy C1 (:2367 "the main loop's 11 checks in `CHECKS_mainloop.md`" vs 12 rows): NOT A DEFECT -- the sentence lists what the
  PANEL settled; row #12 is labelled "Astra adjudication" (`pass1_20261022/CHECKS_mainloop.md:21`) and the next sentence
  (:2368) is that adjudication.  Optional: "(a twelfth was added in adjudication)".
* Gemini contradiction (:2330 `prefix_HEAD.out` 09:46:19 vs :2382 "driver v1's receipt ... 09:46:18"): NOT A DEFECT -- two
  time sources for one run: the receipt header `## prefix_HEAD run 2026-10-23 09:46:18 -0500` (run start) and the .out mtime
  `09:46:19.436` (both quoted in `pass2_20261023/argon_review_of_agy/argon_bundle_1.txt:2254`, `:2272`).  Optional: name both.
* Gemini uncited (bare `fixed.out`, `DUPNAMES.out`, `CLEARANCE.out`): `fixed.out` exists twice
  (`table1_20261022/fixed.out` and `table1_20261022/driver_v1/fixed.out`), so the bare name is resolvable only through the
  bullet's directory -- QUALIFY (minor).  The other two are unique.
* Gemini's three overclaims ("never read from either artifact", "every leg's red set", "keeps every row green"): not checked
  -- judgement calls about the driver's code; passed to Fable as seat opinion only.

## #571 ppcdsformxo -- no confirmed wrong record

* agy C1/C2 (:1898 `:4367-4371`, :1905 `:4295` in `cpu_ppc_instr.c`): NOT A DEFECT -- true at cb21331c
  (`pass2_20261024/PASS2_RULINGS.md:30`, `table1_20261024/PRETABLE.out:20`), shifted +89 by later rounds.  :1898 carries "in
  the committed file"; :1905 does not -- optional qualifier.
* **agy U2 is itself wrong.**  agy says the block quotes "If rA = 0 or rA = rD, the instruction form is invalid" at PEM
  :6253.  The block (:1901) cites PEM :6253 for "opcodes 58 and 62 are illegal on 32-bit implementations", and
  `_scratchpad/ppc_pem_32and64_2005.txt:6253` reads exactly that ("...illegal on 32-bit implementations: 2, 30, 58, 62").
  The citation is RIGHT; the only gap is that "PEM" names one of two local PEM files -- QUALIFY to
  `ppc_pem_32and64_2005.txt:6253` (minor).  (The rA sentence is at `:23351` and later, per-instruction.)
* Gemini contradiction ("five filed ids have zero rows" + the bracketed 2026-11-02 note, :2032): REJECTED -- the bracket is
  the mandated in-place correction that quotes what it refutes.
* Gemini contradiction ("no leg red for another reason" vs L5 17/39 CONTROL=FAIL): REJECTED -- `table1_20261024/SCORES.txt:13`
  lists L5 (IDENTITY BODY, the clause-(c) null medium) PREDICTED 17/39 CONTROL=FAIL and MEASURED 17/39 CONTROL=FAIL.
* Gemini uncited (:1978-1979 "(Argon's pass-1 census)" names no file): the bullet opens on `BUILD_SPEC.md` section 8; the
  census answer itself was not located in one grep of `pass1_20261024/` (`argon_agy_t2p1.txt` discusses 58/62 gating, not
  guest images) -- OPEN, minor: the sentence should name its source.
* agy U1 (:1881 "three store-bearing witness attempts were stopped"): uncited count -- minor.

## What this changes

Only #570 needs a records follow-up: five L4 corrections (1-5) plus one qualifier (6), all in its CHANGELOG block,
correct-in-place form.  None touches code, a detector or a score.  They belong to #570's owed Fable regress review, which
adjudicates them; nothing here has been written into the repo.  **The exact proposed edits are `REC570_EDITS.json`** (seven
old/new pairs in the `[corrected <DATE>, records: said ...]` form of `CHANGELOG.md:1540`; each old string checked to occur
exactly once, at its stated HEAD line).

# Addendum, 22:0x -- the other two of the five oldest held rounds: #572 wdclbaaddr (`0901b388` + `2956c32d`), #573 lecsrmask (`9ac43a17`)

Line numbers here are CHANGELOG.md at **HEAD `116c5aa9`** (snapshot `CHANGELOG_116c5aa9.md`, built by `mk_oldest5.py`).
Gemini web: RECBLOCK_572 2/3/2, RECBLOCK_573 2/1/1.  Its own line numbers drift by 4-10 from the real ones (it counted lines
of an unnumbered block), so every item below was located by its QUOTE.  **Packet defect, mine:** the #572 range 1702-1874 ran
past the #572 block into `# Records, 2026-10-24: ppcdsformxo ...` (:1845-1863, #571's follow-up) -- two Gemini items came
from there.  agy's two file-reading checks: pending (`run_agyrec.sh 572 573`).

## #572 -- one confirmed wrong record, the rest rejected or minor

* **L4 CONFIRMED (Gemini):** :1776 "HEAD for 496 of 505 tracked src files plus this round's dev_wdc.c; ... the pre-#571
  PowerPC decoder and the pmax (est) layout on the six declared divergence paths" accounts for 504.  The ninth differing path
  is the GENERATED `src/machines/.index` -- listed at `pass2_20261024/CLONE_PROVENANCE.txt:2` and attributed at `:23-24`, but
  not one of `tools/est_divergence.txt`'s six (which include `src/devices/.index`, not the machines one).  The artifact's own
  VERDICT line (`:25-26`) carries the same omission.  Correction: "... six declared divergence paths and the generated
  `src/machines/.index` (`CLONE_PROVENANCE.txt:23-24`)".
* REJECTED: "seven LAND WITH CHANGES" (:1856) vs "six LAND WITH CHANGES and DeepSeek's Q3-4 READY TO LAND" (:1807) -- :1856 is
  #571's records follow-up (`cb21331c`, `ppcdsformxo/pass2_20261024/`), a different round's panel; my packet boundary.
* REJECTED: "every one of the 256 select bytes reads back as written" (:1724-1725) -- a stated DERIVATION, not a measurement:
  `sdh_resv` keeps bits 7 and 5 (`idata & 0xa0`), `lba` bit 6, `drive` bit 4, `head` bits 3-0; 0xa0|0x40|0x10|0x0f = 0xff,
  disjoint and covering, as the sentence says.
* REJECTED: "the measured defect is the wrong sector" (:1740) -- a back-reference inside the option-set paragraph to the
  witness the block cites (`witness_20261024/`).  The bare md5 Gemini flagged (:1849) is #571's (packet boundary).
* MINOR (headline): ":1702 every LBA-mode request was served from the cylinder/head/sector reading" -- the 48-bit commands
  fall to ABRT before and after (:1767 lists them BLIND); "every LBA28 transfer request" is the exact form.  The commit
  subject cannot change; the CHANGELOG headline could.  For Fable.
* NOT A DEFECT: bare `SCORES2.txt` (`detector_20261024/`), `CLONE_PROVENANCE.txt`, `GATE10_RUN.txt` (`pass2_20261024/`) --
  each is unique under `regress/artifacts/wdclbaaddr/` (`find -name`).

## #573 -- no confirmed wrong record; two wording qualifiers

* REJECTED: ":1620 the carrier's `ls _scratchpad/*.pdf` does not descend" vs the manuals being `.txt` -- `_scratchpad/lance/`
  holds `TM1986.pdf`, `Am7990_ds.pdf`, `am7990_ardent.pdf` and `am79c90_bitsavers.pdf` beside their `.txt`; `ls
  _scratchpad/*.pdf` lists none of them.  The sentence is right.
* QUALIFY: :1573-1574 "Landing numstat (310 files):" then six entries -- `git diff --numstat 9ac43a17^ 9ac43a17` IS 310 lines,
  11 outside `regress/artifacts/`; the six listed are the code and harness files (omitted: CHANGELOG.md, OUTSTANDING_BUGS.md,
  fable_queue.md, ledger.json, matrix.html).  Say "(310 files; the six code and harness files:)".
* SUPPORTED: :1652 "`floor_20261025/` L0 14/18 / L3 0/18" -- `RESULTS_L0_prefix_gate.txt` and `RESULTS_L3_nullmedium.txt`
  both carry `LE_CSRMASK_RESULT=14/18` / `=0/18`; a directory-level citation of two leg-named files (minor).
* QUALIFY: :1679 "Every seat ratified L4" -- the preceding sentence enumerates the ANSWERING seats, and :1683-1686 name Argon's
  seat failure, Fable HELD and the three not fired, so no false unanimity; "every answering seat" is the exact form.

**Coverage note (22:1x):** #572's own records follow-up -- `# Records, 2026-10-24: wdclbaaddr names its landing commit 0901b388`
-- sits at :1401-1426, far from its round block, so neither the Gemini packet (:1702-1874) nor the agy prompt covered it.
`mk_next4.py` derives each range from the headers and asserts no other round's header falls inside; the next four rounds
(#574 :1427-1566, #576 :908-1064, #577 :1069-1253, #578 :1254-1400) went out that way.  Gemini first; agy after its #572/#573 pair.

# Addendum 2, 22:3x -- the next four held rounds: #574 i8259eoiirr, #576 shfcnvsdfpul, #577 shblreset, #578 jazzvecdeassert

Ranges derived by `mk_next4.py` (HEAD 116c5aa9 numbering, the packet NUMBERED each line, so Gemini's citations are exact this
time).  Gemini web: RECBLOCK_574 4/2/2, RECBLOCK_576 4/2/2, RECBLOCK_577 2/3/2, RECBLOCK_578 2/3/1.  agy: not yet fired on
these four.  Every item checked by the main loop; three confirmed wrong records in total.

## #574 i8259eoiirr (`c1c74b2b`) -- TWO CONFIRMED (L4)

* **L4:** :1436 "each binary newer than **both** edited sources" -- the fix edits three (dev_8259.c, dev_gt.c, devices.h, :1430-1431)
  and the cited `landing_clearance/CLEARANCE.out:12` says "newer than **all three** edited sources".
* **L4, inside an in-place correction:** :1506-1507 "the pass-2 verdict split was one seat against three (**five answers**), not
  '1-4'" -- `pass2_20261025/PASS2_RULINGS.md:3` says "**Six answers**" (codex, grok, glm Q12/Q34, deepseek Q12/Q34).  The seat
  count (1 v 3) is right; the answer count is not.  *A correction is not safer than the thing it corrects.*
* REJECTED: "five of eight" vs seven listed -- `pass1_20261025/PASS1_RULINGS.md:3` says eight answers; DeepSeek's three are
  QA READY WITH CHANGES + QB/QC NOT READY ("READY WITH CHANGES / NOT READY x2" -- ambiguous wording, right count).
* REJECTED: 7,415 deliveries vs "once per 2^14-instruction tick" -- the cited `pass1_20261025/rate_explore_20261025/RUN_IDENTITY.txt:13-15`
  reconciles it: ~2/3 of the 10,986 ticks, one per tick AFTER the first host-timer fire.  Optional qualifier.
* REJECTED: bare `L0/RESULTS_L0_base_gate.txt`, `L3/RESULTS_L3_null_gate.txt` -- both exist under `legs_133457/`, named on :1541.
* REJECTED: "only dev_8259.c/dev_gt.c never read it" (`irq_base`) -- `git grep irq_base c1c74b2b`: the PIC field is written by
  dev_8259.c (:234, :323) and read only by dev_footbridge.c (:434, :436); dev_eagle.c/dev_v3.c match different local arrays.
* QUALIFY: :1556 `pit8253count0` "MEASURED", uncited -- the measurement is `pass1_20261025/rate_explore_20261025/RUN_IDENTITY.txt:8`
  (rate_073805: count 0x0000, 60M instructions, no delivery).

## #576 shfcnvsdfpul (`7ccd4e42`) -- none confirmed

* REJECTED: M_gm in the table (:977) vs "built after the table" (:990) -- `killtable_20261102/run_mgm.sh` is its own runner, after
  `run_killtable.sh`; the listing is the merged table.  Optional: "after the first table run (`run_mgm.sh`)".
* REJECTED: "every row runs with FD clear" (:963) vs Astra's FD=1 escape (:1024-1025) -- consistent: the escape exists BECAUSE no
  row sets FD, and the contract discloses it.
* SUPPORTED: :930's MEASURED values -- `witness_20261102/witness_head.out:6-7` (1.5 -> 0x00000001, -1.5 -> 0xffffffff); the
  witness is cited at :937.  Optional: cite the .out at :930.
* QUALIFY: :1009 "Every seat: the code is right" immediately after "Astra SEAT WALLED" -- every ANSWERING seat.
* NOT A DEFECT: the PRETABLE in-place edit (:985-986) is disclosed with the evidenced pre-leg record named.

## #577 shblreset (`bb672a16`) -- none confirmed

* QUALIFY: :1245 "held for the F2 ruling on D1" while :1190-1192 record Fable's F2 ruling on D1 -- that ruling is PROVISIONAL on
  its face (3 of 5 seats, :1190), so the hold is right; "held for the F2 ruling's completion" says so.
* REJECTED: "for EVERY exception code" (:1078) vs the user break (:1097) -- :1078 describes the BL block, which a user break never
  reaches.  REJECTED: "every value the fix stores has an arm" (:1107) -- the fix stores EXPEVT_RESET_MANUAL (cpu_sh.c:926 at
  bb672a16) and `case EXPEVT_RESET_MANUAL:` is at :1025.  Minor uncited: the 17:47/18:11 binary md5 (:1105), the 18:40 mtimes (:1157).

## #578 jazzvecdeassert (`2a24d9b7`) -- ONE CONFIRMED (L4)

* **L4:** :1342-1344 "the shipped probe differs from [the as-run copy] by **one docstring passage** ... and by nothing else" --
  `killtable3_20261102/ASRUN_NOTE3.txt:8-25` records THREE post-table docstring edits (Opus change 1; GLM/kimi/minimax; Grok change
  1), and `diff` of `git show 2a24d9b7:regress/jazz_vector_probe.py` against `jazz_vector_probe.ASRUN.py` gives two hunks (11-14,
  67-87).  ":1256 ... the four docstring-only edits" is the true count (one pre-table + three post-table).
* REJECTED: table 2's "8 forms" vs seven enumerated -- `killtable2_20261102/` holds M_b (the DELETION form, named on :1326),
  M_offs0, M_offsne0, M_offs2, M_rd, M_wr, M_cond, M_uart = eight, plus M_c_absent, the null leg.
* REJECTED: "(c) measured, `/bin/true`" (:1339) -- table 2's "null 0/22" (:1326), `killtable2_20261102/M_c_absent.raw`.

## Running total over the nine rounds (#569-#578, no #575): NINE confirmed wrong records -- #570 five, #572 one, #574 two,
## #578 one -- plus about ten one-phrase qualifiers.  None touches code, a detector or a score; all go to each round's Fable
## regress review.  Gemini's raw totals claimed ~40 contradictions/overclaims; about one in four survived checking.

**agy RECCHECK_572 (22:3x): 182 numbers, 168 supported, 4 contradicted, 4 drifted, 6 uncited, 0 missing.**  Its four CONTRADICTED
are one class, verified: `dev_wdc.c` citations written in PRE-FIX numbering and off by one at the landing commit, because the round's
own diff moved the file by a net -1 above line 570 -- `:947-954` and `:1155` (:1739-1740; `grep -n 'd->error |= WDCE_ABRT;'` gives
1155 at `0901b388^`, 1154 at `0901b388`), `:1081-1082` (:1825; 1082 -> 1081) and `:640` (:1826; 640 -> 639).  QUALIFY all four as
pre-fix (`0901b388^`) -- the same class as #570's `cpu_m88k.c:811-819`.  Its DRIFTED four (the probe's 840 lines / 35,862 bytes /
md5 96e5fbc5, and the harness pins) were true at landing and moved later.  agy did not see the 504-of-505 omission; Gemini did --
and Gemini saw none of these four.  The two seats' finds do not overlap.

**agy RECCHECK_573 (22:1x): 248 numbers, 239 supported, 1 contradicted, 5 drifted, 3 uncited, 0 missing.**  The contradicted one,
verified: :1691 quotes TM1986 that CSR1/CSR2 "must be reloaded" at "(TM1986 1513)"; `_scratchpad/lance/TM1986.txt:1513` opens the
paragraph with the CSR3 sentence, and "CSR1 and CSR2 must be reloaded / when the STOP bit is set." is at `:1515-1516` -- QUALIFY to
1515-1516 (two lines; the same paragraph).  Its second citation, "2853-2857" ("normally not affected ... recommended to reload"),
is exact.  The five DRIFTED are the `lediagfmt` line numbers at :1695, which the block already qualifies with their commits
(`9ac43a17^` and `987cb596`) -- not defects.  The three uncited are clock times in the seat-roster prose.  #573 stays at no
confirmed wrong record.

# Addendum 3, 22:5x -- agy's file-reading checks of #574/#576/#577/#578, each item checked by the main loop

agy: RECCHECK_574 165/161/2c/0d/2u/6m, RECCHECK_576 160/147/4c/2d/7u/0m, RECCHECK_577 352/326/10c/3d/13u/0m, RECCHECK_578
108/105/2c/0d/1u/0m.  **Two agy errors caught in checking: its #574 item quotes a `TOTAL: 11 killed, 3 escaped` line that does not
exist, and its #576 item quotes a sentence that is not the block's text.**

* **#574:** "both edited sources" = the Gemini item above (agy adds that `pass2_20261025/f2b_20261025/F2B_RULINGS.md:62` flagged it at F2b as
  "'both edited files' against three hashes" -- known then, never fixed; the same line shows the "(five answers)" count came from GLM
  B, which miscounted).  REJECTED: "12 of 15 killed" (:1488) -- `killtable_20261025/SCORES_v2c.txt` is 17 lines with no TOTAL line
  (`grep -n TOTAL` empty); its status column carries 12 KILLED of 15, one of them (`D_gt_nocasc`) with CONTROL=FAIL -- worth one
  sentence for Fable, not a wrong count.  The six MISSING are paths written relative to the directory the sentence just named
  (`pass1_20261025/` or `pass2_20261025/`) plus the outer-tree manual `_scratchpad/i8259/8259A.txt` -- none missing.
* **#576, L4 CONFIRMED:** :987 says `IMPLEMENTATION_PLAN_20261102_1715.md` "predicts the base, fixed, M_b, M_c, **M_h**, M_i and M_z
  scores as measured" -- the plan's M_h line predicts only `fpul 0.1` red ("(0xa0000000)"), and the table measured M_h 40/52, all six
  FPUL rows (the low half of the double is 0 for 1.5, -1.5 ...).  M_h belongs with M_f/M_g, the mispredicted ones.  QUALIFY :946
  `:5061-5068` and :1047 `cpu_sh_instr.c:3279-3295` -- pre-fix numbering, moved +4 by the round's own edit; and :1061 "two comment
  lines only" -- two hunks, two lines becoming three.
* **#577, L4 CONFIRMED:** :1204 "answered a liveness test at **20:4x** on the hotmail login and its pass 2 and F2 confirmation were
  fired then" -- :1174 (20:2x) and :1206 (20:2x-20:3x) say otherwise, and so do the answers on disk: `pass2_20261102/codex/
  codex_shblresetp2.txt` 20:21:53, `f2_20261102/codex/codex_shblresetf2.txt` 20:37:23.  The liveness test preceded 20:21.  QUALIFY
  the other nine: line numbers into `cpu_sh.c` (:985-989 twice, :945-947, :1015-1021, :1083-1085, :941-942) and `OUTSTANDING_BUGS.md`
  (24063, :8238, 23283) written in pre-fix numbering -- one checked: the `default:` exit is :1085 at `bb672a16^`, :1094 at `bb672a16`.
* **#578, L4 CONFIRMED (a second one):** :1344-1345 "**Two driver edits** preceded table 3 ... the `quit` command had set the
  failure flag ..., and two docstring literals were reworded for section U" -- `killtable3_20261102/ASRUN_NOTE3.txt:2-4` records two
  pre-table edits, (1) the driver's quit flag and (2) "docstring only": one driver edit.  agy's N076 is the "one docstring passage"
  item above; it adds that the CHANGELOG copied ASRUN_NOTE3.txt:10-11's sentence, which went stale when EDITs 2 and 3 were appended.

## TOTAL over the nine rounds: TWELVE confirmed wrong records -- #570 five, #572 one, #574 two, #576 one, #577 one, #578 two --
## and #569, #571, #573 none.  No code, detector or score is affected.

**One CLASS, for Fable and the owner (structure first):** four of the nine blocks (#570, #572, #576, #577) cite line numbers into
files their OWN round edits in PRE-FIX numbering with no qualifier -- about sixteen citations, each off by the round's own shift at
the landing commit.  The carrier's citation-form rule asks for "the qualifier ON the citation" and leaves machinery to an escalation
trigger (a decision consumed by a stale citation) that none of these met.  The landing spot that matches the structure-first rule is
one line in the CHANGELOG round-block template: "a line number into a file this round edits names its tree -- `X^` or `X`".

**The other seven corrections are drafted too: `REC_OTHERS_EDITS.json`** (#572 x1, #574 x2, #576 x1, #577 x1, #578 x2), same form
as `REC570_EDITS.json`.  All fourteen old strings checked at `cbba52c0` (CHANGELOG.md unchanged since 116c5aa9): each occurs exactly
once, at its stated line.  Apply by old string -- the wrec1106 records commit in flight will move the line numbers.
