# Reading task: F2 shblreset (#577) adjudication (Gemini web; 2026-11-02)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBF2SHBLRESET-c503` on a line of its own.

# ADJUDICATION PASS (F2) -- `shblreset` (#577): the panel shares its pass-2 findings; adjudicate them

Fired 2026-11-02 19:3x.  HEAD `20bfde13` (a records-only commit landed after pass 2; the product tree is unchanged since `987cb596`,
and every line number below is HEAD's unless it says "fixed clone").  Roster (owner 2026-11-02): GPT-6 Astra, Fable 5.1, glm-5.3,
Argon (Gemini web), Grok 4.7.  **Astra is on its WEEKLY wall from the hotmail login** ("try again at Nov 8th, 11:24 AM"); its pass 2
and this adjudication are OWED, recorded as SEAT WALLED, not as agreement.  **glm-5.3 is DOWN**: the whole Ollama cloud transport
answers `HTTP 403 Forbidden, error code: 1010` (owner-side).  **The owner has ruled that the commit HOLDS until Astra answers.**
Fable 5.1 ADJUDICATES this pass (the owner's 09-25 rule: codex walled means Fable adjudicates and Astra confirms later); Grok and
Argon answer the three questions.  Fable: P1, P3-P7, P9-P12 and P14 are yours -- disclosed self-review, be harder on them.

## READ THIS FIRST

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at HEAD; the diff is applied only in the scratch clone `/tmp/gxfix577`.**  No project
tree is edited.  Packet-fed seats: everything you need is inlined, including the manual lines (section 3b).  **VERDICT LINE FIRST AND
LAST**: `F2 VERDICT: RATIFY / RATIFY WITH CHANGES (<n>) / NOT RATIFY`.  Count the arguments, not the seats.

## 1. Pass 2 as answered (`_scratchpad/w577/pass2_20261102/`)

| seat | verdict | where it stands |
|---|---|---|
| Argon (Gemini web, proxy) | 5 ATTACKS 0 BROKEN 4 HOLDS 1 UNSETTLED | the six manual citations UNSETTLED (it cannot read the manual: inlined in 3b); names the undriven-code conjunct escape (`&& expevt != EXPEVT_TLB_MISS`); F7's rejection confirmed; the records list judged accurate |
| Grok 4.7 | SHIP WITH CHANGES (1) | the probe comment cited the revision-history reprint `:678-681` for H'020 -> `:12383-12384` (applied 18:54); the RES_INST conjunct escape; the shipping text is the kill-table `product.diff`; every score reconciled against its raw |
| Fable 5.1 | SHIP WITH CHANGES (3) | MEASURE the guard-side clause-(d) mutant (not built); two contract wordings; three records items (bug-file prose row, the post-table comment edits in the round block, `product.diff` provenance) |
| glm-5.3 | SEAT DOWN | Ollama cloud 403/1010 |
| GPT-6 Astra | WALLED (weekly) | owed |

Every answering seat: the two-line product diff is right and complete; the nine table scores reconcile with their raw logs; no floor
cell is open ({BL set, BL clear} x {H'140, other}: all four rowed).

## 2. Findings P1..P18, attributed, with MY DISPOSITION and what changed

| # | finding | raised by | disposition |
|---|---|---|---|
| P1 | every built mutant was BODY-side; the fix DEPENDS ON the dominating predicate `cpu->cd.sh.sr & SH_SR_BL` (HEAD `cpu_sh.c:910`) and no mutant weakened it, so `tlbm trapa`'s kill was a PREDICTION and that row is the SOLE carrier of the class | Fable | **ACCEPTED, MEASURED 19:11-19:14**: `M_guard` = `if (cpu->cd.sh.sr & (SH_SR_BL \| SH_SR_MD))`, built on the fixed clone, scored with the AS-RUN instrument: **9/10, `tlbm trapa` reads 0x00000020 (want 0x00000160)**, the nine other rows green -- the prediction matched in score, row and value.  The prediction was written FIRST into `PRETABLE_CORRECTION.out` (mtime 19:08:32) and the leg's raw is 19:14:12; the CHANNEL line for `tlbm trapa` is now measured (section 3a) |
| P2 | the probe comment's `(:678-681)` cite for H'020 is the front-matter revision-history reprint; the body sentence is 5.6.1 (2) `:12383-12384` | Grok | **ACCEPTED, DONE 18:54** (post-table edit 1, comment-only, logged in `ASRUN_NOTE.txt`) |
| P3 | the clause-(e) sentence named ONE direction (the rewrite keyed to an undriven code) while the Q3 edit is the OTHER (an exemption added at one) | Fable | **ACCEPTED, DONE** (post-table edit 2): the contract now names both directions and lists the undriven codes (section 3a) |
| P4 | "the identity medium ... is the BL block DELETED" misdescribes `M_c`, which deletes only the two rewrite lines (guard and `fatal()` stay) | Fable | **ACCEPTED, DONE** (edit 2): "the REWRITE deleted (the guard and its fatal() stay)" |
| P5 | `OUTSTANDING_BUGS.md` carries the defect TWICE: the id entry `:24063` and the prose row `:8238` (`cpu_sh.c:653` \| BL already set -> `EXPEVT_RESET_POWER`); the records list marked only the first | Fable | **ACCEPTED**: the landing marks both; the round's records list names both lines |
| P6 | the round block must carry the post-table comment edits; the pass-2 brief's "byte-identical to the shipped copy" is stale by them | Fable | **ACCEPTED**: the round block cites `ASRUN_NOTE.txt` (THREE post-table edits now, all comment-only) rather than the brief; verified 19:2x that the as-run and shipped probes have an IDENTICAL AST once docstrings are dropped (comments are not in an AST), so rows and oracles are the same instrument |
| P7 | the shipping text is `killtable_20261102/product.diff`; `witness_20261102/product.diff` and its `apply_fix577.py` carry the pre-F4 comment (code identical; both binaries md5 `b7b0d0b5f5ae`, 17:47 and 18:11) | Fable, Grok | **ACCEPTED**: the round block names the kill-table copy as the shipping text and the witness copy as the pre-F4 comment form of the same code |
| P8 | an ADDED conjunct exempting a code the table does not drive keeps all ten rows green and changes guest-visible EXPEVT under BL: `&& expevt != EXPEVT_ADDR_ERR_ST` (Fable, first differs on a misaligned longword store under BL, H'100), `!= EXPEVT_RES_INST` (Grok, H'180), `!= EXPEVT_TLB_MISS` (Argon) | Fable, Grok, Argon -- independently | **ACCEPTED as DISCLOSURE (P3) and MEASURED ONCE**: `M_resinst` = `&& expevt != EXPEVT_RES_INST`, predicted 10/10 (a total escape) in `PRETABLE_CORRECTION.out` addendum 2 before its leg; measured **10/10 at 19:24 -- a TOTAL ESCAPE, as predicted** (`M_resinst.raw`, mutant md5 `2fc3306dd0b2`, the as-run instrument; the prediction's mtime 19:20:29 precedes the raw's 19:24:09).  Filing -> D1 |
| P9 | the probe comment's reason for RB clear ("so the bank-0 seeds are the ones the program uses") is not the mechanism: the debugger's `sr=` writes the field through `CPU_SETTINGS_ADD_REGISTER32`, not `sh_update_sr()`, so no bank swap happens at pre-set | Fable (Q4, optional) | **ACCEPTED, DONE** (post-table edit 3): "RB clear as in the committed rows; the debugger's `sr=' writes the field without a bank swap" |
| P10 | the copies under `regress/artifacts/` were made with plain `cp`, so every mtime there read 18:40 and the PRETABLE-before-table order proof survived only in `_scratchpad/w577` | Fable | **ACCEPTED, REPAIRED 19:2x**: the byte-identical table files were re-copied with `cp -p` from the `w577` originals, so the durable copies now carry the original mtimes (PRETABLE.out 18:10:13 < KILLTABLE.log 18:11:05); the post-table legs were copied with `cp -p` from the start |
| P11 | `M_b`'s binary has HEAD's md5 (`b76a7799a3ea`): reinstating the one line rebuilds HEAD byte for byte, so clause (b) holds at the BINARY level and the fixed clone differs from HEAD only in this block | Fable | **RECORDED** in the round block |
| P12 | the pass-2 brief's section 2 mixed HEAD line numbers with fixed-clone ones; "round #576's two staged hunks" could be read as the git index, which held an unrelated records batch | Fable | **ACCEPTED**: the round block cites HEAD lines or construct names; the landing checklist says "the two hunks of `_scratchpad/w576/gate_sh_rounding.NEW.sh` against HEAD", staged by path from HEAD-based copies |
| P13 | the data-side multiple-hit sentence is `:12499` (same H'140); the product comment cites `:12461` (the instruction side) | Grok, Fable | **RECORDED**: the round block cites both; the product comment is unchanged (its cite is true) |
| P14 | optional wordings for the product comment: "discards expevt before storing it" -> "never stores EXPEVT for an interrupt"; add that H'000 and H'020 have no raiser today, so a later RESET-pin or H-UDI raiser (both H'000) would need its own exemption | Fable (not counted) | **REJECTED as a product-comment change after pass 2**: the sentence is true as written and both file-reading seats verified it against `:945-947`; the no-raiser fact goes into the round block.  -> D2 |
| P15 | SPC and SSR are still written at `:941-942` while 5.7.2.a (`:13165-13166`) calls them undefined on this path | Grok | **RECORDED, no change**: undefined permits any value; nothing to fix |
| P16 | SLEEP under BL never wakes in the tree (`cpu_sh_instr.c:260-263` and `cpu_dyntrans.c:247` refuse under BL) while the manual (`:13170-13171`) accepts an interrupt in sleep with BL set | Grok, Fable (pass 1 F10) | **RECORDED**: the pass-1 filing stands; it ships in this round's records as its own open row |
| P17 | the `PRETABLE_CORRECTION.out` addendum first carried a hand-written time ("ADDENDUM 18:5x") | me | **CORRECTED before the leg ran**: the mtime is the order proof, no hand-written time (the frozen-number class) |
| P18 | the mutator's `M_guard` branch first landed with a real newline inside a C string (the heredoc backslash trap, the shape of #576's P1) | me | **CAUGHT by `ast.parse` before any run**, repaired with the editor tool; the preserved `mutate577.py` parses and its seven table branches are byte-unchanged |

Also from pass 2, recorded without a change: H-UDI reset stays the table's H'000 row with no raiser (Grok); Argon's A1 (the six
citations) is SETTLED by the two file-reading seats and by section 3b.

## 3. The texts as they now stand

### 3a. The probe's `#577` contract comment (comment-only edits 2 and 3; the measured instrument is unchanged)

```
#  with the multiple-hit code exempt.  Rows run under sr = MD|BL (0x500000f0, RB clear as in the
#  committed rows; the debugger's `sr=' writes the field without a bank swap -- Fable, pass 2);
#  `tlbm trapa' is the BL-CLEAR control that pins
#  the general vector's own code.  Contract: TRAPA (H'160) and a misaligned load (H'0E0) are
#  the two general codes driven; any edit that moves a code between the rewritten set and the
#  exempt set ONLY at a code this table does not drive -- H'040-H'0C0, H'100, H'120, H'180,
#  H'1A0, H'800, H'820 -- in either direction (the rewrite keyed to such a code, or an exemption
#  added at one) is clause-(e) disclosure.  The identity medium for this predicate round is the
#  REWRITE deleted (the guard and its fatal() stay): `tlbm bl trapa' and `tlbm bl ldmis' then
#  read their own codes (red); `tlbm bl mhit' reads H'140 either way and cannot carry it.
```

`PRETABLE_CORRECTION.out`, the measured addendum (verbatim): "MEASURED (M_guard.raw, MGUARD.log; leg 19:11:02-19:14:13; mutant binary
md5 8e53c40288fa, newer than its source; instrument sh_tlbmulti_probe.ASRUN.py md5 d41edccdee1c): SH_TLBMULTI_RESULT=9/10 -- `tlbm
trapa' 0x00000020 (want 0x00000160) FAIL; the other nine rows ok ... CHANNEL line for `tlbm trapa', now measured rather than disclosed:
it kills M_guard (the guard widened to MD) through EXPEVT, which reads the rewritten H'020 instead of TRAPA's own H'160".
Addendum 2 (M_resinst), verbatim: "MEASURED (M_resinst.raw, MUTLEG_M_resinst.log; leg 19:20:56-19:24:09; mutant binary md5 2fc3306dd0b2,
newer than its source; instrument the AS-RUN copy, md5 d41edccdee1c): SH_TLBMULTI_RESULT=10/10 -- a TOTAL ESCAPE, as predicted (this
file's mtime 19:20:29 precedes the raw's 19:24:09).  The class is therefore a MEASURED above-floor escape and is filed as coverage debt
(`shblundriven') with this leg as its evidence, per the carrier".

### 3b. The manual lines the product comment cites, as `awk 'NR>=A && NR<=B'` prints them from `_scratchpad/sh7750_hardware.txt` (2,426,348 bytes)

```
12302: When the BL bit in SR is 1 and a general exception other than a user break is generated, the CPU's
12303: internal registers and the registers of the other modules are set to their states following a manual
12304: reset, and the CPU branches to the same address as in a reset (H'A000 0000). For the operation in
12376:      When a general exception other than a user break occurs while the BL bit is set to 1 in SR
12383:     Exception code H'020 is set in EXPEVT, initialization of VBR and SR is performed, and a
12384:     branch is made to PC = H'A000 0000.
12006:                      Instruction TLB multiple-hit  1       3   H'A000 0000 --  H'140
12010:                      Data TLB multiple-hit exception 1     4   H'A000 0000 --  H'140
12461:     Exception code H'140 is set in EXPEVT, initialization of VBR and SR is performed, and a
12499:     Exception code H'140 is set in EXPEVT, initialization of VBR and SR is performed, and a
41448: 3. The operation when a break condition is satisfied depends on the BL bit (in the CPU's SR
41449:     register). When the BL bit is 0, exception handling is started and the condition match flag
41450:     (CMFA/CMFB) for the respective channel is set for the matched condition. When the BL bit is
41451:     1, the condition match flag (CMFA/CMFB) for the respective channel is set for the matched
41452:     condition but exception handling is not started.
13164:         When a general exception other than a user break occurs, a manual reset is executed. The
13165:         value in EXPEVT at this time is H'0000 0020; the value of the SPC and SSR registers is
13166:         undefined.
```

The product diff is unchanged since pass 2 (the fixed clone's `cpu_sh.c:913-926`): the `#577` comment, then
`if (expevt != EXPEVT_RESET_TLB_MULTI_HIT) expevt = EXPEVT_RESET_MANUAL;` replacing `expevt = EXPEVT_RESET_POWER;`.

## 4. Disagreements D1..D2 -- each side in its own words, my ruling, its warrant

**D1 -- the undriven-code conjunct class (P8): file it as coverage debt, or leave it disclosed?**
* Grok: "No row catches it.  The probe's clause-(e) sentence already discloses it ... The same sentence covers it."
* Argon: "No new row is strictly owed since the identity of the predicate is proven on the codes contracted."
* Fable: "Not owed: a filter may reject or repair a row, never demand one, and the contract discloses the class.  Coverage debt; file
  it or leave it disclosed."  Cheapest row if ever wanted: "a misaligned longword store (`mov.l r2,@r1`, 0x2122, r1 odd, want H'020;
  the mirror of `tlbm bl ldmis`)".
* **My ruling: DISCLOSE (done, P3) AND FILE** a LOW coverage-debt row (`shblundriven`) carrying the measured `M_resinst` escape, the
  three seats' member list and Fable's cheapest row -- **no in-round row**.  Warrant: the carrier's rule that an above-floor MEASURED
  escape is filed with its escape list; I measured one member precisely so the disclosure rests on a measurement rather than three
  predictions, and a measured escape nobody files is the unread-review shape.  Against me: the class has as many members as there are
  undriven codes, a filed row that no round will ever close is noise, and the contract already says it in both directions.

**D2 -- the product comment after pass 2 (P14): reword it, or leave it?**
* Fable (not counted as a change): "could be 'never stores EXPEVT for an interrupt'; and the comment could say in one clause that H'000
  and H'020 have no raiser today ... No code for that: the addition licence has no measured delta to point at."
* **My ruling: LEAVE IT.**  The sentence is true and twice verified; a comment edit to the product after pass 2 would make the F2 text
  differ from the text pass 2 reviewed for a stylistic gain, and the no-raiser fact belongs in the round block, where a later raiser's
  author will find it beside the exemption's warrant.  Against me: the product comment is what a future editor reads first, and the
  round block is not.

## 5. What is still OWED, and where I might be fooling myself

* Astra's pass 2 and its confirmation of this adjudication (weekly wall; Nov 8 11:24 or a gmail `codex login`).  **The commit holds for
  it by owner ruling.**  glm's pass 2 is a seat failure (transport down), recorded as such.
* Application: the diff and the two detector files are NOT in any project tree.  Owed at landing: `GXEMUL-SEC` + `est/` byte-identical;
  `build/`, `build-asan/`, `/tmp/gxsec-build` propagated and REBUILT with the two-part clearance per tree (`est/`: source tree, part 2
  N/A); `gate_sh_rounding.sh` run end to end on the applied tree (the tlbmulti pin 6 -> 10, expecting 10/10); the gate file staged from
  the HEAD-based copy (the working copy's three unrelated 09-17 hunks stay out), reconciled with #576's two hunks in the same file.
* Records: the CHANGELOG round block (cites HEAD lines, `ASRUN_NOTE.txt`'s three edits, both `product.diff` copies, the M_guard and
  M_resinst legs, the binary md5 facts); `OUTSTANDING_BUGS.md` `:24063` AND `:8238`; the SLEEP-under-BL filing; `shblundriven` if D1
  holds; the ledger close with a `probe:` witness term and the dashboard re-rendered.
* The shipped probe differs from the as-run copy by three comment passages.  The AST check says the rows are identical; if the
  adjudicator wants the table of record re-run on the shipped text, it is ten legs of about three minutes.
* I accepted fifteen of the sixteen counted findings (P14 rejected; P15-P18 are records).  That is a suspicious number and agreement
  is not evidence -- question 2 below.

## 6. The three questions

1. Adjudicate P1..P18 and D1..D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?  I accepted fifteen of sixteen; name the one most likely wrong and why.
3. WHAT DID ALL OF US MISS?  You now have the whole panel's output, the measured table and its two post-table legs.

End with `F2 VERDICT: RATIFY / RATIFY WITH CHANGES (<n>) / NOT RATIFY`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBF2SHBLRESET: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
