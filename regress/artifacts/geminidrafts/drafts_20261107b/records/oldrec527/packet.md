# Reading task: oldrec527 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC527-9827` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #527 ppcrlwimiwidth (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 8483-8597 of CHANGELOG_8d9df658.md; each line carries its own number -- cite those numbers)

```text
 8483| # `#527` (ppcrlwimiwidth, ppcrldimimask): two PowerPC rotate-and-insert instructions computed wrong results — `rlwimi` rotated a 32-bit word at 64-bit width and never wrote a wrapping mask's high word; `rldimi`'s rotate loop consumed its own shift count, so every insert mask was built from `sh == -1`
 8484| 
 8485| Both are sibling handlers in `src/cpus/cpu_ppc_instr.c` and share one commit and one joint kill table,
 8486| because one build exercises both and each probe is the other's cross-check.  The architecture is Book I
 8487| v2.01 (`_scratchpad/ppc_uisa_book1_v201.txt`): rlwimi `r <- ROTL32((RS)32:63, SH); m <- MASK(MB+32,
 8488| ME+32); RA <- (r & m) | ((RA) & ~m)` with MASK wrapping when x > y (`:578`), and ROTL32 duplicating the
 8489| word into both halves; rldimi `r <- ROTL64((RS), sh); m <- MASK(mb, 63-sh)`.
 8490| 
 8491| **rlwimi — two defects in one handler.**  (1) `MODE_uint_t tmp = reg(rs)` held all 64 bits, so
 8492| `(tmp << sh) | (tmp >> (32 - sh))` pulled high-word bits DOWN into the rotated low word.  (2) A
 8493| wrapping mask (MB > ME) covers the WHOLE high word, which must receive the rotated word; the handler
 8494| only walked the low word.  **FIX:** narrow on read, `uint32_t tmp = (uint32_t)reg(rs)`, and BEFORE the
 8495| insertion loop `if (mb > me) ra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);` — before, because the
 8496| loop walks `mb` to `me` and a guard placed after it would never fire (`R_POST_LOOP` measures exactly
 8497| that).  A 19-line comment records why a 32-bit `MODE_uint_t` build keeps only the low word, and that this
 8498| is NOT a claim that 32-bit MODE removes half the register (Book I §1.2).
 8499| 
 8500| **rldimi — two defects in one handler.**  (1) `while (sh-- != 0)` rotated correctly and left `sh == -1`,
 8501| so the mask end `63 - sh` was 64 for every encoding.  (2) The mask loop `m ++` never wrapped past bit 63.
 8502| **FIX:** rotate a copy (`int m, n = sh;  while (n-- != 0)`) and make the loop circular
 8503| (`m = (m + 1) & 63; } while (m != ((64 - sh) & 63))`).
 8504| 
 8505| **WITNESSES, rung 3, unmodified in-tree `-E bareppc -M 64` (PPC970).**  rlwimi: committed **14/28**, fix
 8506| **28/28** (`artifacts/ppcrlwimiwidth/witness_{committed,fix}.out`, agy's witness).  rldimi: committed
 8507| **17/27**, fix **27/27** (`artifacts/ppcrldimimask/witness_*.out`, the Opus seat's).  No Book I error in
 8508| either fix: codex checked all 32,768 rlwimi and 4,096 rldimi immediate combinations against a model of
 8509| the RTL; grok and kimi re-derived both from Book I independently.
 8510| 
 8511| ## The detectors — `regress/ppc_rlwimi_probe.py` (28 rows) and `regress/ppc_rldimi_probe.py` (29 rows), wired in `gate_ppc.sh`
 8512| 
 8513| Promoted from the witnesses: RESULT/CONTROL/DONE protocol; CONTROL includes TARGET-INSTRUCTION rows (a no-op
 8514| instruction would otherwise read CONTROL=OK); `census run` and `disasm total` want LITERALS (rlwimi 129 and
 8515| 146/146, rldimi 495 and 513/513) because the derived wants self-satisfied a shrunk census.  Each header
 8516| carries a CONTRACT and a clause-(e) list.  The gate section runs BEFORE gate 13's NetBSD prerequisite, so a
 8517| missing image cannot turn a red detector into a SKIP.
 8518| 
 8519| | table | legs | result |
 8520| |---|---|---|
 8521| | 1 `ppcrlwimiwidth/killtable_20260911/`, `ppcrldimimask/killtable_20260911/` | 8 + 8 | all killed; **the first rlwimi NULL_MEDIUM leg was byte-identical to BASE and scored a vacuous 28/28** -- corrected in `killtable_nullmedium_20260911/` (rlwimi 12/28, rldimi 13/27) |
 8522| | 2 `ppcrlwimiwidth/killtable2_20260912/` (+ `table2b/`) | 15 | 14 on prediction; five R_ legs REFUSED by a driver leg-name bug and re-run in `table2b/` rather than scored |
 8523| | 3 `ppcrlwimiwidth/killtable3_20260912/` | 17 | 15 on prediction, zero escapes, cross-check held on every leg |
 8524| 
 8525| Table 3's two misses, as what they are (POSTTABLE.out): **D_NO_MERGE** predicted 26, measured 25 — my
 8526| arithmetic, the row-level prediction was right; **D_NOCIRC** predicted 21, measured 22 — `full rot` PASSED
 8527| under that undefined-shift mutant (measured; the slow-circular mechanism is NOT measured).  The shipped
 8528| probes differ from table 3's frozen instruments ONLY in header and comment text written after the §F2 pass
 8529| (the corrections below); `POSTTABLE.out` records the non-comment-filtered diff, and no executable line differs.
 8530| 
 8531| ## Pass 2, and the two gaps it found (both rldimi)
 8532| 
 8533| Nine-seat pass 2 (`_scratchpad/panel_20260912_095238_ppcpass2`, Opus measuring, the §F2 adjudication pass
 8534| `panel_20260912_104522_xpadjud`, then Fable last): *is there a clause-(d) mutant this detector does not see?*
 8535| 
 8536| * **codex: `while (n-- != 0 && mb != ((64 - sh) & 63))`** skips the rotate exactly when the mask is full
 8537|   width.  Every full-width row and census cell used the ALL-ONES source, which no rotate changes.  Row
 8538|   **`full rot`** (SH=24, MB=40 from 0xDEADBEEFCAFEF00D): table 3 `D_SKIP_FULL_ROT` 28/29, failing it alone.
 8539| * **glm: no rA == rS row in rldimi** while rlwimi has three — a sibling-parity gap.  **glm's literal mutant
 8540|   (`tmp & cpu->cd.ppc.gpr[rs]`) is NOT an aliasing mutant: it reads the UNROTATED source and is wrong for
 8541|   every SH != 0 whatever the aliasing** — found by simulating it before building.  The leg built is glm's own
 8542|   "equivalently" form (re-read after the clear, then rotate).  Row **`alias rs=ra`**: table 3
 8543|   `D_ALIAS_REREAD` 28/29, failing it alone.
 8544| 
 8545| **Grade: L1 construction** (the detectors were unshipped).  Fable ruled codex's three LATER gaps (below)
 8546| clause (e), and closed the repair chain on this pass with its denominator: D_SKIP_FULL_ROT and
 8547| D_ALIAS_REREAD measured killed; the Opus seat's `mb >= me` (27/28, `census wrong` its sole killer),
 8548| unrotated high word (24/28), `n-- > 1` (25/27) and end-test-without-`& 63` (17/27) measured killed; the rest
 8549| enumerated as (e).
 8550| 
 8551| ## Records corrected (L4), several by the panels
 8552| 
 8553| * **F15 — MY RECORD WAS WRONG AND EVERY SEAT MISSED WHY (Fable).**  I recorded deleting rlwimi's `sh ?`
 8554|   guard as "pre-existing, host-equivalent, not a gap".  But pre-fix `tmp` was 64-bit, so `tmp >> 32` at
 8555|   SH = 0 was DEFINED and the guard redundant; **the fix narrowed `tmp` to `uint32_t`, which makes that shift
 8556|   undefined and the guard LOAD-BEARING for definedness.**  The fix changed the guard's status.  No row can
 8557|   pin it (the mutant is host-equivalent if equivalent at all); `R_NOGUARD` (predicted 28/28) is FILED.
 8558| * **The literal pins DO carry a measured kill** — my table-2 note said they did not.  The Opus seat's
 8559|   end-test-without-`& 63` leg read `census run 0/495`, `disasm total 8/16`.  **And the caveat (codex, kimi,
 8560|   Fable), verbatim: measured for the hang case, redundantly with CONTROL; unmeasured for the shrink case.**
 8561|   `CENSUS_SHRINK` (the fixed build with a shortened census) is FILED.
 8562| * **"controls green on every build"** in both probes was false — tables 2 and 3 show CONTROL=FAIL on
 8563|   R_REV_COND, R_NULL, D_MUT63, D_NOCIRC, D_NOKEEP_SH, D_NO_MERGE and D_NULL (codex).  CONTROL=OK certifies the
 8564|   apparatus, never that a leg is harmless.
 8565| * **D_NOCIRC "hangs and aborts at 182"** was load-dependent: table 1 hit the 90 s session timeout, table 2
 8566|   completed all 495 cells in 394 s.  A correct build runs the whole probe in 0.1 s.
 8567| * **`wrap fullword` "31 bits low"** — it is all 32 (codex).  **The patterned SH list** is 0, 8, 24, 40 (codex).
 8568| * **The `>` bound** is pinned only by the census's MB == ME cells — disclosed (grok, Opus).
 8569| 
 8570| ## Disclosed and FILED, not built (clause (e), Fable)
 8571| 
 8572| `n = sh & ~7` (every patterned SH is a multiple of 8 — FOLDED with F16 into ONE item carrying Fable's spec:
 8573| ADD a full-mask patterned row at **SH=63, MB=1** (want 0xEF56DF77E57F7806; a byte-rounded rotate gives
 8574| 0x0DDEADBEEFCAFEF0), which pins every dropped SH bit — do not modify `full rot`, table 3's cited killer;
 8575| costs a table 4 and pin 29 -> 30); a stale re-read confined to WRAPPING masks (the one alias row is
 8576| non-wrapping); an insertion skipped only when Rc=1 (both record-form rows check CR presence only);
 8577| `CENSUS_SHRINK`; `R_NOGUARD`.
 8578| 
 8579| ## Scope, stated by name
 8580| 
 8581| **`regress/ppc_rldicl_probe.py` is modified in the working tree and is NOT in this commit** — an earlier
 8582| session's `mask_range` oracle re-pin (`ppcwitnessmaskoracle`), not reviewed by this round's panels; it
 8583| waits for its own record.  Likewise `tools/{BRIEF_TEMPLATE.md, CLAUDE.md, PIPELINE.md, panel.sh}` and
 8584| `tools/pipeline/fable_queue.md`.  `SCORE_CLAIMS_MANIFEST` 25 -> **28**: the two new gate pins (28, 29) AND `#526`'s xscale pin, which `#526` shipped QUOTED (`"30"`) so that `check_score_claims.py`'s PIN regex could not see it -- for one commit the score-claims check guarded nothing there.  The gate behaved identically (a string compare); the literal is unquoted here, with a comment saying why.  Also carried: `#526`'s pass-2 receipt in `regress/pass2_ledger.tsv` and its ledger `commits` field (eb26590).
 8585| 
 8586| ## Seats
 8587| 
 8588| Pass 2: codex, kimi (CLI), grok, glm, deepseek, minimax, kimi-k3:cloud — 7/7; Opus 5 measured; **agy
 8589| DELIBERATELY NOT FIRED**; §F2: the same seven; Fable 5.1 last (subagent pinned to `model: fable`, opened
 8590| naming `claude-fable-5-1`; verbatim at `artifacts/xscaleinten/fable_adjudication_20260912.md`).
 8591| 
 8592| ## Gate
 8593| 
 8594| `gate_ppc.sh` (gate 13) with the rlwimi/rldimi section — parse before score, each protocol KEY exactly once
 8595| and well formed, rows run and correct pinned to 28 and 29: **gate 13 PASS, 110 checks**, every rlwimi/rldimi row `ok` (protocol parsed, controls OK, run and correct 28 and 29), 0 FAIL, GATE_EXIT=0, run from a FROZEN copy of `gate_ppc.sh`; log `regress/artifacts/ppcrlwimiwidth/gate_ppc_20260912.log`.  The section was restored from `_scratchpad/gate_ppc.ppcround.sh` (parked out of the tree so the probes could stay untracked) and its pins were checked against the shipped probes' `row(` counts (28, 29) and table 3's BASE (28/28, 29/29) before it ran.  Negative controls on the gate
 8596| section: **11 of 11 as specified** (`regress/artifacts/ppcrlwimiwidth/gate_negctl_20260912.sh` / `.out`): the section is EXTRACTED from the gate itself, its probe calls replaced by fixture logs derived from table 3's BASE, and run under counting stubs -- the untouched fixture passes, and a shrunk denominator (each probe), one red row, a duplicated RESULT, a malformed extra RESULT, a missing DONE, a missing RESULT, CONTROL=FAIL, a duplicated CONTROL and an empty log each fail on the intended check.  Build trees: two-part clearance RUN before the gate -- `cpu_ppc_instr.c` p1=CLEAN p2=FRESH in `build/`, `build-asan/` and `/tmp/gxsec-build`; `est/` p1=CLEAN, p2 N/A (source tree, no binary).
 8597| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_527: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC527: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
