FABLEREC9: 10 ACCEPTED 4 AMENDED 0 REJECTED VERDICT:LAND-RECORDS

# Records ruling on the nine oldest held rounds' CHANGELOG blocks (#569-#574, #576-#578)

Fable 5.1, adjudicating seat, 2026-11-06.  Records-only: no round's regress review is touched or discharged here; no test,
probe, mutant or code design is asked for or given.  Tree: `GXEMUL-SEC` at `cbba52c0` (CHANGELOG.md byte-identical to
`116c5aa9`'s; every line number below is that file's at `cbba52c0`).  Inputs: `OLDEST3_RECORDS.md` (body, Addenda 1-3, agy
notes), `REC570_EDITS.json`, `REC_OTHERS_EDITS.json`.  Method: every one of the fourteen old strings was located in
`git show cbba52c0:CHANGELOG.md` (each occurs EXACTLY ONCE, at its stated line; the file is LF); every confirmed item's
evidence was re-run by me with `git show`, `git diff --numstat`, `git ls-tree`, `grep` or a file read, never taken from the
main loop's quotation.  The working tree holds a staged records commit (`wrec1106`); nothing here was written into it.

Nothing in the fourteen is wrong in substance.  Four NEW wordings are themselves imprecise and are amended with exact text;
one of them (#577) embeds same-file line numbers that the in-flight commit will move, and its measured time differs from the
proposed "before 20:21" -- the liveness answer is on disk at 20:10.

## 1. The fourteen edits

| # | round | line | verdict | reason (evidence I checked) |
|---|---|---|---|---|
| 1 | #570 item 1 | 2114 | **ACCEPT** | `git show c8fcb5ff:regress/m88k_buserr_probe.py \| wc -l` = 848; `repair1_20261024/rev2c_equivalence.txt:3-5` = rev 2 836 lines / rev 2c 848 lines.  836 is the measured rev 2's count, as the new text says. |
| 2 | #570 item 2a | 2120 | **AMEND** | The cited `rev2b.*` files do not exist at `repair1_20261024/` in `c8fcb5ff`; `rev2c.docstring.diff` / `rev2c_equivalence.txt` do, and carry the block's numbers (stripped 28,722 bytes both, `cmp` IDENTICAL, `:8-11`; AST 209/209, `rev2c_ast_identity.out:6`).  But the new bracket says 2b's proofs "live in `superseded_9046d774/`" -- SAME-NAMED `rev2b_*` files also sit in `superseded_fe8cc784/`, whose README calls itself "an INTERMEDIATE documentation revision 2b" too.  Name the md5 and the twin (text below). |
| 3 | #570 item 2b | 2122 | **ACCEPT** | `rev2c_rowcompare.txt:7` = "row/INFO lines: 33 vs 33" (the block's 33); `rev2b_rowcompare.txt` is under both `superseded_*/`, not at the cited path. |
| 4 | #570 item 3 | 2167 | **ACCEPT** | `git diff --numstat c8fcb5ff^ c8fcb5ff -- tools/pipeline/check_probe_wiring.py` = `15 0`; `table1_20261023/BUILD_REPORT.md:33` = `+11 -0`; `repair1_20261024/REPAIR_REPORT.md:25-26` shows the file growing 4271 -> 4275 (staged 4256 -> 4260) IN the repair, so "pre-repair count" is the right attribution. |
| 5 | #570 item 4 | 2258 | **ACCEPT** | `repair1_20261024/objmd5_before.txt` = 224 lines; `grep -v '\.o$'` leaves one: `3cd0501c...  gxemul`.  223 objects + the binary. |
| 6 | #570 item 5 | 2093 | **ACCEPT** | `memory_rw.c:626` at `c8fcb5ff` reads "callers (e.g. the debugger's dump) never get here" (absent at `c8fcb5ff^`); `cpu_dyntrans.c:287-288` at `c8fcb5ff` is the single-step pre-read: `cpu->memory_rw(..., MEM_READ, CACHE_INSTRUCTION)` -- NO `NO_EXCEPTIONS`, so "the debugger's STEP pre-read is unsuppressed" is true, and `git grep NO_EXCEPTIONS c8fcb5ff -- src` lists 30+ non-debugger callers (emul.c, memory.c, cpu_m88k.c:1124/1187, dev_luna88k.c, dev_dec21143.c ...).  "-- the debugger --" as THE caller set was an overclaim the round had already removed from product code. |
| 7 | #570 item 6 | 2144 | **ACCEPT** | `cpu_m88k.c` at `c8fcb5ff^`: the SFRZ block is `:811-819`; at `c8fcb5ff`: `:815-823` (same text, +4).  Qualifier form matches the block's own `m88kcitedrift570` finding. |
| 8 | #572 | 1776 | **ACCEPT** | `pass2_20261024/CLONE_PROVENANCE.txt:2` lists NINE differing paths; `:23-24` attributes `src/devices/.index` and `src/machines/.index` as generated; `tools/est_divergence.txt` at `2956c32d` has six entries including `src/devices/.index` but NOT `src/machines/.index`.  dev_wdc.c + ppc decoder + six = eight; the ninth was unnamed, in the artifact's own VERDICT (`:25-26`) as well. |
| 9 | #574 a | 1436 | **ACCEPT** | `landing_clearance/CLEARANCE.out:12`: "newer than all three edited sources"; the fix's numstat (block line 1434) names three product files (dev_8259.c, dev_gt.c, devices.h). |
| 10 | #574 b | 1507 | **ACCEPT** | `pass2_20261025/PASS2_RULINGS.md:3`: "Six answers (codex ...; grok ...; glm Q12/Q34; deepseek Q12/Q34)" -- one seat (codex DO NOT SHIP) against three.  The "GLM B's count" attribution is confirmed by `pass2_20261025/f2b_20261025/F2B_RULINGS.md:62` ("GLM B: 'split 1-4' counts five answers from three seats") -- NOTE the path: OLDEST3 writes it without its `pass2_20261025/` parent, where it does not exist.  Optional: add that path to the bracket. |
| 11 | #576 | 987 | **AMEND** | `killtable_20261102/IMPLEMENTATION_PLAN_20261102_1715.md:70` predicts M_h as "`fpul 0.1` red (0xa0000000)" -- ONE row; `M_h.raw` = 40/52 with TWELVE red rows: six FPUL values (1.5, -1.5, 0.1, -0, inf, snan) x two modes (nearest, toward-zero), lines 40-51.  The new text's "all six FPUL rows red" undercounts the rows by half (six VALUES, twelve ROWS).  `PRETABLE.out:30` does carry 40/52 -- say so, since the sentence is about which pre-leg record predicted what. |
| 12 | #577 | 1204 | **AMEND** | The "20:4x" is wrong, and I found WHERE it came from: `_scratchpad/w578/liveness/astra_live.md` (mtime 20:10:07) is the prompt and is itself STAMPED "2026-11-02 20:4x" with token `ASTRA_SEAT_ALIVE_20261102_2040`; the hotmail answer `astra_hotmail.txt` carries the token at mtime **20:10:17**; `astra_catchup.sh` 20:12:13; the pass-2 codex dir 20:13:28; the pass-2 answer `pass2_20261102/codex/codex_shblresetp2.txt` 20:21:53; the F2 answer `f2_20261102/codex/codex_shblresetf2.txt` 20:37:23 (all mtimes, -0600, mutually consistent, and consistent with the block's own `20:2x` / `20:2x-20:3x` at lines 1174 and 1206).  So "before 20:21" is true but weaker than the evidence, and the new text's "as :1174 and :1206 say" embeds SAME-FILE LINE NUMBERS that the in-flight `wrec1106` commit moves -- the citation-form rule forbids exactly that.  Replace with the measured time, the cause, and positional references (text below).  The liveness files are on a VOLATILE path and must be BANKED for the citation to be durable. |
| 13 | #578 a | 1342 | **AMEND** | `killtable3_20261102/ASRUN_NOTE3.txt:8-25` records three POST-TABLE docstring edits (Opus change 1; GLM 5.3 / kimi / minimax; Grok change 1), and the block's sentence is a copy of `ASRUN_NOTE3.txt:10-11`, written before EDITs 2-3 were appended.  `diff -u jazz_vector_probe.ASRUN.py <(git show 2a24d9b7:regress/jazz_vector_probe.py)` = TWO hunks, headers `@@ -8,9 +8,10 @@` and `@@ -63,16 +64,27 @@`, both inside the module docstring (md5s 7b3e17e7d3f0 / 37cbfc835297 as the block says).  The new text's "the `diff` has hunks 11-14 and 67-87" is the shipped side's replaced LINE ranges, labelled as hunks -- a reader running `diff` sees neither number.  Say two hunks with their headers (text below). |
| 14 | #578 b | 1344 | **ACCEPT** | `ASRUN_NOTE3.txt:2-6`: pre-table edit (1) is the driver's `quit` flag, (2) is "docstring only".  One driver edit, not two. |

### The four amended texts (apply by OLD STRING; each old string occurs once at `cbba52c0`; `<DATE>` filled at landing)

**A1 -- #570 item 2a (line 2120).**
old: `` `repair1_20261024/rev2b.docstring.diff`, `rev2b_equivalence.txt`), ``
new: `` `repair1_20261024/rev2c.docstring.diff`, `rev2c_equivalence.txt` [corrected <DATE>, records: said `rev2b.docstring.diff`, `rev2b_equivalence.txt` -- revision 2b's receipts (md5 `9046d774`), kept under `repair1_20261024/superseded_9046d774/`; the `fe8cc784` intermediate's same-named receipts are under `superseded_fe8cc784/`]), ``

**A2 -- #576 (line 987).**
old: `which predicts the base, fixed, M_b, M_c, M_h, M_i and M_z scores as measured,`
new: `` which predicts the base, fixed, M_b, M_c, M_i and M_z scores as measured [corrected <DATE>, records: listed M_h too -- the plan's M_h line (`killtable_20261102/IMPLEMENTATION_PLAN_20261102_1715.md:70`) predicts one red row, `fpul 0.1` (0xa0000000), and M_h measured 40/52 with every FPUL row red: six values in both rounding modes, twelve rows (`killtable_20261102/M_h.raw`); `PRETABLE.out:30` carries the 40/52], ``

**A3 -- #577 (line 1204).**  Requires banking `_scratchpad/w578/liveness/astra_live.md`, `astra_hotmail.txt`, `astra_hotmail.err` (and the `astra_gmail.*` pair, the other login's attempt) to `regress/artifacts/shblreset/liveness_20261102/` in the same commit; without the banking, drop the parenthetical that cites them and keep the rest.
old: `answered a liveness test at 20:4x on the hotmail login`
new: `` answered a liveness test at 20:1x [corrected <DATE>, records: said `at 20:4x` -- the time the liveness prompt and its token `ASTRA_SEAT_ALIVE_20261102_2040` were STAMPED with; the hotmail answer file is 20:10:17 by mtime (`liveness_20261102/astra_hotmail.txt`, banked from `_scratchpad/w578/liveness/`), the pass-2 answer `pass2_20261102/codex/codex_shblresetp2.txt` 20:21:53 and the F2 answer `f2_20261102/codex/codex_shblresetf2.txt` 20:37:23, as this block's roster sentence (`answered at 20:2x after its reset`) and hold sentence (`20:2x-20:3x`) already say] on the hotmail login ``

**A4 -- #578 a (line 1342; the old string spans a line break after "one").**
old: `the shipped probe differs from it by one` + newline + `docstring passage (the contract's "at the values the rows drive" wording, Opus F2 change 1; `` `ASRUN_NOTE3.txt` ``) and by nothing else`
new: `the shipped probe differs from it by three` + newline + `` docstring edits in two passages (`ASRUN_NOTE3.txt`'s POST-TABLE EDITs 1-3: the contract's "at the values the rows drive" wording, Opus F2 change 1; the mechanism clause and the contract's disclosures, GLM 5.3 / kimi / minimax; the OpenBSD access shapes, Grok change 1) [corrected <DATE>, records: said `by one docstring passage`, copied from `ASRUN_NOTE3.txt:10-11` before EDITs 2 and 3 were appended -- `diff -u` of the as-run copy against the shipped file has two hunks, `@@ -8,9 +8,10 @@` and `@@ -63,16 +64,27 @@`, both inside the module docstring] and by nothing else ``

## 2. The qualifiers: which ride, which are left alone

Rule applied: a qualifier RIDES only if (a) I verified its fact here, (b) its old string occurs exactly once at `cbba52c0`,
and (c) it is one phrase.  Everything else is LEFT for the round's own regress review, which is owed anyway.

### RIDE (exact old -> new, each old string checked unique at `cbba52c0`)

| id | round | line | old | new | evidence |
|---|---|---|---|---|---|
| Q-A | #573 | 1573 | `Landing numstat (310 files):` | `Landing numstat (310 files; the six code and harness entries):` | `git diff --numstat 9ac43a17^ 9ac43a17 \| wc -l` = 310; 11 outside `regress/artifacts/`; the six listed are the code/harness files (omitted: CHANGELOG, OUTSTANDING_BUGS, fable_queue, ledger, matrix) |
| Q-B | #573 | 1679 | `Every seat ratified L4` | `Every answering seat ratified L4` | lines 1683-1686 name Argon's failure, Fable HELD, three not fired |
| Q-C | #573 | 1691 | `(TM1986 1513)` | `(TM1986 1515-1516)` | `_scratchpad/lance/TM1986.txt:1515-1516` = "CSR1 and CSR2 must be reloaded / when the STOP bit is set."; `:1513` opens the paragraph with the CSR3 sentence |
| Q-D | #574 | 1556 | `(clamped to 1e-8 Hz), MEASURED)` | `` (clamped to 1e-8 Hz), MEASURED: `pass1_20261025/rate_explore_20261025/RUN_IDENTITY.txt:8`) `` | that line: "rate_073805 count 0x0000 ... 60M instructions, s2 = 0, IRR bit 0 = 0, no delivery".  NOTE the `pass1_20261025/` parent, which OLDEST3 omits |
| Q-E | #576 | 1009 | `Every seat: the code is right` | `Every answering seat: the code is right` | "Astra SEAT WALLED" is the clause immediately before it (line 1008) |
| Q-F | #577 | 1245 | `held for the F2 ruling on D1)` | `held for the completion of the F2 ruling on D1, provisional on 3 of 5 seats)` | line 1190: Fable's F2 ruling "on 3 of 5 rostered seats and provisional on its face", D1 UPHELD |
| Q-G | #571 | 1911 | `(PEM :6253)` | `` (`ppc_pem_32and64_2005.txt:6253`) `` | that file's line 6253 reads "...illegal on 32-bit implementations: 2, 30, 58, 62"; two local PEMs exist, so the bare name is ambiguous |
| Q-H | #570 | 2124 | `` rev-2b `:250` `` | `` rev-2b and the shipped rev-2c `:250` `` | `git show c8fcb5ff:regress/m88k_buserr_probe.py \| grep -n '^REVISION = 2'` = 250; `rev2c_vs_2b.txt`: line count unchanged 2b -> 2c.  The same stale-2b label as item 2, one line down -- the sibling the edits missed |

**The pre-fix line-number class -- RIDE where verified (13 occurrences, four blocks).**  Each shift below is measured from the
landing commit's own diff; each old string is unique at `cbba52c0`.  Form kept uniform: `(at <X>^; <new> at <X>)`.

| id | round | line | old | new | shift evidence |
|---|---|---|---|---|---|
| P1 | #572 | 1740 | `` (`:947-954`, `:1155`) `` | `` (`:947-954`, `:1155` at `0901b388^`; one line lower at `0901b388`) `` | `dev_wdc.c` 947/954/1155 at `0901b388^` = `if (!diskimage_exist` / `}` / `d->error \|= WDCE_ABRT;`; 946/953/1154 at `0901b388` |
| P2 | #572 | 1825 | `` `dev_wdc.c:1081-1082` (`#485`) `` | `` `dev_wdc.c:1081-1082` at `0901b388^` (`#485`; `:1080-1081` at `0901b388`) `` | "NO SPECIFICATION IS CITED..." at 1081-1082 pre, 1080-1081 post |
| P3 | #572 | 1826 | `` while `:640` (`#525`) `` | `` while `:640` at `0901b388^` (`#525`; `:639` at `0901b388`) `` | the `ata2_x3t10_948d.txt:1529-1531` comment at 640 pre, 639 post |
| P4 | #576 | 946 | `the decoder (:5061-5068)` | `` the decoder (`:5061-5068` at `7ccd4e42^`; `:5065-5072` at `7ccd4e42`) `` | the FCNVSD/FCNVDS decoder arms at 5061-5068 pre, 5065-5072 post; the fix's single hunk `@@ -3054,7 +3054,11 @@` (+4) |
| P5 | #576 | 1047 | `` (`cpu_sh_instr.c:3279-3295`) `` | `` (`cpu_sh_instr.c:3279-3295` at `7ccd4e42^`; `:3283-3299` at `7ccd4e42`) `` | `X(fsrra_frn)` 3270 pre, 3274 post; same +4 hunk above it |
| P6 | #577 | 1083 | `` guest-distinguishability comment at `:985-989` `` | `` guest-distinguishability comment at `:985-989` (at `bb672a16^`; `:994-998` at `bb672a16`) `` | `cpu_sh.c` single hunk `@@ -910,11 +910,20 @@` (+9); 985-989 pre = the EXPEVT-survives comment |
| P7 | #577 | 1099 | `` the intevt path at `:945-947` `` | `` the intevt path at `:945-947` (at `bb672a16^`; `:954-956` at `bb672a16`) `` | 945-947 pre = `if (intevt > 0) {` ... `expevt = -1;` |
| P8 | #577 | 1101 | `` (`:1015-1021`) are untouched `` | `` (`:1015-1021` at `bb672a16^`; `:1024-1030` at `bb672a16`) are untouched `` | 1015-1021 pre = the three RESET cases through `break;` |
| P9 | #577 | 1108 | `` `:1083-1085` `` | `` `:1083-1085` (at `bb672a16^`; `:1092-1094` at `bb672a16`) `` | the `default:` ... `exit(1);` at 1083-1085 pre, 1092-1094 post (the one the main loop also checked) |
| P10 | #577 | 1227 | `` written at `:941-942` `` | `` written at `:941-942` (at `bb672a16^`; `:950-951` at `bb672a16`) `` | 941-942 pre = `spc = cpu->pc; ssr = sr` |
| P11 | #577 | 1229 | `` The `#457` comment at `:985-989` `` | `` The `#457` comment at `:985-989` (at `bb672a16^`; `:994-998` at `bb672a16`) `` | as P6 |

(`bb672a16^` = `87a73fdc`, whose `cpu_sh.c` is byte-identical to `987cb596`'s, the commit the round's witness names; `7ccd4e42^` = `d082eacb`; `0901b388^` = `cc1f69cc`.)

### LEAVE ALONE (with the reason)

* **#577's three `OUTSTANDING_BUGS.md` citations (`:24063`, `:8238`, `:23283`) -- NOT members of the class; the main loop
  ACCEPTED agy's claim and agy was wrong.**  `OUTSTANDING_BUGS.md` lines 8238, 23283 and 24063 are byte-identical at
  `bb672a16^` and `bb672a16` (the round's hunks are at 8236 same-count, 24091 +1, 26414 +37 -- all below or beside them).
  They were correct at landing and need no qualifier.  This also corrects OLDEST3's census ("about sixteen"): the CHANGELOG
  population is **13 occurrences across four blocks** (#570 1, #572 4, #576 2, #577 6) -- all 13 ride above.
* **#572 headline (line 1702, "every LBA-mode request").**  The 48-bit commands are aborted before and after (line 1767 lists
  them BLIND), so "every LBA28 transfer request" is the exact form -- but a round-block HEADER is machine-read (`mk_next4.py`
  derives block ranges from headers; other checkers may key on it), the commit subject cannot change, and the body already
  discloses the 48-bit set.  For the regress review: a body sentence, not a header edit.
* **#569 bare `fixed.out`** -- resolvable through its bullet's directory; two copies exist but the sentence names which.
* **#569 "11 checks"** -- not a defect (row 12 is the Astra adjudication, which the next sentence IS).  **#569 two time
  sources** -- run start vs mtime, both in the bundle; not a defect.
* **#571 `:4295` (line 1915)** -- correct at `cb21331c`, moved by LATER rounds (+89): ordinary drift, not the pre-fix class.
  **#571 "(Argon's pass-1 census)" source** -- OPEN; a citation cannot be added to a file nobody has located.  For the review.
* **#574 "only `dev_8259.c`/`dev_gt.c` never read it" (line 1505)** -- facts right (`git grep irq_base c1c74b2b`: written at
  dev_8259.c:234/323, read only at dev_footbridge.c:434/436; dev_gt.c has no match), wording awkward ("only ... never").  It
  sits inside an existing F2b in-place correction; optional for the review: "dev_footbridge.c reads it; the fix's two files
  never do".
* **#574 "12 of 15 killed" (line 1488)** -- `SCORES_v2c.txt`'s status column says KILLED for 12 of 15, one of them
  (`D_gt_nocasc`, 75/77) with `CONTROL=FAIL`; the sentence transcribes the file and says "kept as the record of what it
  measured".  Not L4.  The review may add "(one with CONTROL=FAIL)"; it is a superseded table (v2d..v2g followed).
* **#576 "two comment lines only" (line 1061)** -- `GATE_ASRUN_NOTE.txt`: `59c59,60` and `68c69`, comment-stripped compare
  IDENTICAL.  "Comment lines only" is the load-bearing claim and is true; two as-run lines became three.  Leave.
* **#576 M_gm "built after the table", the `.out` citation at line 930; #574 rate "once per tick"** -- optional glosses, not
  wrong records.  Leave.
* **#573 `floor_20261025/` directory-level citation (line 1652)** -- two leg-named files carry the numbers; minor.  Leave.

## 3. Rejected seat claims -- any to reinstate?

**None reinstated as a wrong record.**  Each rejection I re-tested held:
* #570 "27 MATCH vs 25": `table1_20261023/SCORES.txt` SUMMARY says "27 measurements MATCH", and the legs are pre, fix, L1, L3,
  L3/w24, L4, L4/w24, L5, L5b, L6, L6b, L7, L8, L8b, L9-L19, L21, L22 = 27 (`grep -c MATCH` = 28 because the SUMMARY line
  carries the word).  Gemini's 25 missed L1, L3/w24, L4/w24 as the main loop said.
* #570 "every product edit kept its line count": lines 2255-2257 describe the pre-commit repair's comment hunks, not the fix.
* #571 L5 `CONTROL=FAIL`: `SCORES.txt:13` PREDICTED and MEASURED 17/39 CONTROL=FAIL -- the null medium behaving as predicted.
* #572 "256 select bytes": lines 1724-1725 say "so every one ... reads back as written (the four parts are disjoint and cover
  the byte)" -- a derivation, stated as one.  "seven LAND WITH CHANGES" and the bare md5 -- #571's follow-up, packet boundary.
* #573 `ls _scratchpad/*.pdf` -- the lance PDFs are in `_scratchpad/lance/`; the sentence is right.
* #574 "five of eight" (PASS1_RULINGS.md:3 "eight pass-1 answers"), 7,415 deliveries (RUN_IDENTITY.txt:11-15 reconciles it),
  `irq_base` (above), `L0/L3` paths (under `legs_133457/`).
* #576 M_gm (own runner, merged listing), FD-clear vs the FD=1 escape (consistent by construction).
* #577 "EVERY exception code" (the BL block; a user break never reaches it), "every value the fix stores has an arm"
  (`cpu_sh.c:926` stores `EXPEVT_RESET_MANUAL`, `:1025` is its `case`, both at `bb672a16`).
* #578 "8 forms" (`killtable2_20261102/`: M_b, M_cond, M_offs0, M_offs2, M_offsne0, M_rd, M_uart, M_wr, plus the null leg
  `M_c_absent`), "(c) measured, `/bin/true`" (`M_c_absent`, table 2's 0/22).
* #569 C1, the two time sources, #571 agy U2 (PEM :6253 is right; agy misread which sentence was cited).

**One ACCEPTED claim is REVERSED** (section 2): agy's "#577 OUTSTANDING_BUGS.md citations in pre-fix numbering" -- false at
`bb672a16`.  *A correction is not safer than the thing it corrects* applies to seat-sourced qualifiers too.

**Errata for the evidence file before it is banked** (write a one-line note beside `OLDEST3_RECORDS.md`, do not rewrite it):
(i) `f2b_20261025/F2B_RULINGS.md` is at `pass2_20261025/f2b_20261025/F2B_RULINGS.md`; (ii) `rate_explore_20261025/RUN_IDENTITY.txt`
is at `pass1_20261025/rate_explore_20261025/RUN_IDENTITY.txt`; (iii) the pre-fix class census is 13, not "about sixteen", and
#577's `OUTSTANDING_BUGS.md` citations are not members; (iv) the #577 liveness time is 20:10 by the answer file's mtime, with
the prompt itself stamped 20:4x -- the error's source, not merely its symptom.

## 4. The CLASS proposal

**ADOPT, as one line, and put it where the block is WRITTEN.**  The obligation already exists in the carrier's citation-form
rule ("line numbers only ACROSS files, with the qualifier ON the citation"); what this census shows is that the rule did not
FIRE in four of nine blocks written under it -- the carrier's own trigger-versus-memory finding.  There is no file named
"CHANGELOG round-block template" in the tree: the artifact present at the moment a round block is drafted is the `/round`
skill, `.claude/commands/round.md` at the project root (UNTRACKED -- it is the owner's artifact; whether it gets a tracked copy
in `tools/` the way `CLAUDE.md` did is the owner's call), and the carrier's lifecycle step 7 ("Docs (CHANGELOG round block ...)").
The line, for both: *"A line number this block cites into a file THIS ROUND EDITS names its tree on the citation -- `<sha>^`
for the pre-fix file or `<sha>` for the landing; files the round does not edit need no qualifier (later drift is handled by
re-deriving)."*  Scope is deliberately the round's OWN edited files: that is the whole measured population (13 of 13), it is
derivable from the diff by reading, and it cannot grow into qualifying every citation in the file.  **No checker**: the
citation-form rule's pre-specified escalation (a MEASURED decision consumed by a stale citation) was met by none of these --
every one was caught by a seat re-reading, which is the rule's own prediction about this class.  File the thirteen's
disposition in the records commit (they ride, section 2); nothing else is owed to the class.

## 5. Verdict and landing conditions

**VERDICT:LAND-RECORDS.**  The fourteen edits (ten as drafted, four as amended above), the eight wording qualifiers Q-A..Q-H
and the eleven pre-fix qualifiers P1..P11 may land now as ONE records-only commit, ahead of the rounds' regress reviews.  The
warrant is the late-dissent rule's first disposition: a WRONG RECORD is L4, corrected in place, and "closure is no shield for
false prose" -- a held round's review is not a shield either.  None of these touches code, a detector, a score or a verdict;
every one is quoted-what-it-refutes in the `CHANGELOG.md:1540` form.  Conditions:

1. **Apply by OLD STRING after the staged `wrec1106` commit lands** -- every line number here is `cbba52c0`'s and will move.
   Re-run the uniqueness check against the then-HEAD before applying (one python loop; I ran it at `cbba52c0`: 14/14 and
   19/19 unique).  Headers are NOT edited.
2. **Bank the evidence under `regress/artifacts/`** in the same commit: `OLDEST3_RECORDS.md` (+ the errata note of section 3),
   `REC570_EDITS.json`, `REC_OTHERS_EDITS.json`, the seat outputs the records file names, this `RULING.md`, and the #577
   liveness files to `regress/artifacts/shblreset/liveness_20261102/` (A3 cites them; `check_cited_artifacts.py` will red on a
   cited path that does not exist, and the carrier forbids citing `_scratchpad/` from a durable record).
3. `<DATE>` = the landing date in every bracket (2026-11-07 if it lands then).
4. The commit message is written FROM THE DIFF: 14 corrections + 19 qualifiers, by round, and the one reversed seat claim.
   Run the precommit hook as usual; section U already sees four `40/52` strings in the #576 block, so A2's fifth is not new.
5. **Nothing here discharges any regress review.**  The nine rounds stay `held`; each review inherits the corrected block and
   the LEAVE list above as its records agenda.

Evidence basis of this ruling: every claim in sections 1-3 was checked by me against `git show`/`git diff`/`git ls-tree` on
`GXEMUL-SEC` or a direct read of the named artifact; nothing was taken from a seat's or the main loop's quotation.  No file
other than this one was written; no build, gate, probe or script that writes was run.
