F2 VERDICT: RATIFY WITH CHANGES (5)

OPUS 5.5 seat, #577 `shblreset`, adjudication packet `brief_shblreset_f2.md`. Read-only. HEAD source via `git show HEAD:`
(HEAD is now c7f86d4a, records only; src unchanged). The artifacts are under
`GXEMUL-SEC/regress/artifacts/shblreset/killtable_20261102/`. The manual is read with `awk NR`.

**The product diff is right and complete, and I re-derived that independently.** None of the five changes touches code. One
(change 1) is a wrong order-proof that the packet still asserts in three dispositions. One (change 4) is a citation in the product
comment.

## What I measured (read-only)

* Every raw's `SH_TLBMULTI_RESULT` and FAIL rows: base 7/10 (bl trapa, bl mhit, bl ldmis at 0x000), fixed 10/10, M_b 7/10,
  M_c 8/10 (0x160, 0x0e0), M_noex 9/10, M_wrongex 8/10, M_lt100 8/10, M_trapaonly 9/10, M_power 8/10, M_guard 9/10 (`tlbm trapa`
  0x020), M_resinst 10/10. **All match the packet.**
* `mutate577.py`'s branches build exactly the texts named. MGUARD.log and MUTLEG_M_resinst.log carry the one-line diffs.
* **P6's AST claim, re-run on the CURRENT shipped copy**: `ast.dump` of `sh_tlbmulti_probe.ASRUN.py` (md5 d41edccdee1c) and of
  `sh_tlbmulti_probe.NEW.py` (with five edits now), docstrings blanked: **equal (True)**. `NEW.py` in artifacts `cmp`s equal to
  `_scratchpad/w577/sh_tlbmulti_probe.NEW.py`.
* Gate hunk: the continuation is a real `\` + LF (`od -c`), not the two characters. The four names fit `%-14s ` with two spaces
  (`tlbm bl trapa` is 13 characters). `^tlbm trapa  ` cannot match `tlbm bl trapa`. The pin is 10, EQUALITY.
* Manual: `:12372-12384` is 5.6.1 (2) Manual Reset, with sources at `:12376` and the code sentence at `:12383-12384`. `:12452-12462`
  is (4) INSTRUCTION TLB multiple hit and `:12490-12500` is (5) OPERAND TLB multiple hit.
* `PRETABLE_CORRECTION.out` mtime **20:12:28.4**, later than both legs (M_guard.raw 19:14:12, M_resinst.raw 19:24:09).

## Q1 -- P1..P18, D1..D2

| # | ruling | reason |
|---|---|---|
| P1 | **REFINE** | The measurement stands (9/10, the predicted row and value). **The order proof in the disposition, "written FIRST into `PRETABLE_CORRECTION.out` (mtime 19:08:32)", is false**: that file is rewritten at every addendum, and its mtime is now 20:12:28. The file itself carries the correction (Fable, 19:50: the pre-leg evidence is the pass-2 answers' mtimes and `run_mguard577.sh` 19:10:42). The round block must take the file's text, not this packet's |
| P2 | UPHOLD | `:12383-12384` verified |
| P3 | UPHOLD + extend | The undriven list (H'040-H'0C0, H'100, H'120, H'180, H'1A0, H'800, H'820) is complete against `sh4_exception.h` for raised general codes. Extension: see change 3 (MD) |
| P4 | UPHOLD | `M_c` replaces only the two fix lines with `;` |
| P5 | UPHOLD | HEAD `OUTSTANDING_BUGS.md:8238` (`cpu_sh.c:653` prose row) and `:24063` both verified |
| P6 | **REFINE** | "THREE post-table edits now" is stale: `ASRUN_NOTE.txt` lists FIVE (edits 4 and 5 landed after this packet). AST identity holds for the five-edit copy (verified above). The round block cites the note's final count |
| P7 | UPHOLD | witness fixed md5 b7b0d0b5f5ae (17:47) = fixed.raw md5 (18:11) despite different comments; see P11 |
| P8 | **REFINE** | Measured escape stands. Same false order proof as P1 ("prediction's mtime 19:20:29 precedes"); the file now says so itself |
| P9 | UPHOLD | |
| P10 | **REFINE** (wording) | "PRETABLE.out 18:10:13 < KILLTABLE.log 18:11:05": 18:11:05 is the log's FIRST-LINE timestamp. Its mtime is 18:39:34 (its last write). The mtime proof is PRETABLE.out 18:10:13 < BUILD_FIXED.log 18:11:05 / base_head.raw 18:14:06, and that holds |
| P11 | UPHOLD + extend | M_b.raw md5 b76a7799a3ea = base_head's, verified. **And it is stronger than stated**: M_b KEEPS the new twelve-line #577 comment (mutate577 replaces only the two code lines) and is built in another directory, yet its binary is HEAD's byte for byte. So in cpu_sh.c neither line shifts nor the build path reach the binary: nothing after the block uses `__LINE__` |
| P12 | UPHOLD | |
| P13 | **OVERTURN the "no change"** -> change 4 | The tree's ONLY raiser of H'140 is the UTLB associative write (dev_sh4.c:1178), which 3.7.4 calls a DATA TLB multiple hit, i.e. (5) at `:12499`. The product comment cites `:12461`, the ITLB case that nothing in the tree raises. The code value is true and the sentence is the wrong one. This is a citation correction, not style, so D2's reasoning does not cover it |
| P14 / D2 | UPHOLD (leave the wording) | true as written; the no-raiser fact goes in the round block |
| P15 | UPHOLD | "undefined" licenses any value |
| P16 | UPHOLD | `cpu_sh_instr.c:260-263` refuses under BL, verified |
| P17 | **OVERTURN** | "the mtime is the order proof" is false for a file rewritten at every addendum. That is the very correction now inside PRETABLE_CORRECTION.out. The structural rule there (one file per pre-leg prediction, never rewritten) is the right disposition |
| P18 | UPHOLD | |
| D1 | UPHOLD (file LOW) | A measured above-floor escape is filed with its evidence. The objection ("a row nobody will close") is answered by the filing carrying its cheapest row (`mov.l r2,@r1`, 0x2122, r1 odd) |

## Q2 -- which accepted disposition is wrong

**P1 and P8, through the order proof they assert, and P17, which mints the false rule behind both.** All three say the prediction is
proven pre-leg by `PRETABLE_CORRECTION.out`'s mtime. That file's mtime (20:12:28) is after both legs, and a rewrite-at-every-addendum
file can never prove that order. The predictions ARE pre-leg, but by OTHER artifacts (the pass-2 answers at 18:43-19:01, and the
run scripts and mutator branch mtimes 19:10:42 / 19:20:21). The file was corrected in place at 19:50, after this packet was written
at 19:28. **The risk is that the round block is drafted from this packet**, which would ship the self-referential timestamp as a
proof. Change 1.

Runner-up: P13's "no change". The citation points a future reader at the instruction-side exception the tree never raises.

## Q3 -- what did all of us miss

1. **An MD-qualified guard is unrowed AND undisclosed.** Every BL row presets MD|BL (0x500000f0). Edit 4's disclosure names RB and
   IMASK as the states no BL row varies, but not MD. `if ((cpu->cd.sh.sr & SH_SR_BL) && (cpu->cd.sh.sr & SH_SR_MD))` keeps all ten
   rows green (prediction, not measured) and changes a reachable cell: BL=1, MD=0 by `ldc Rm,SR` or by `rte` with such an SSR. The
   body tests nothing on MD, so this is clause (e), not floor. **Add MD to edit 4's list** (change 3). Cheapest row if ever wanted:
   sr=0x100000f0, `trapa #1`, want H'020. Note that a user-mode fetch from CODE in P1 raises an instruction address error first.
   That is also a general exception under BL and also wants H'020, so the row is valid either way, and under the mutant it reads
   the raw code.
2. **P13's citation** (change 4): `:12499`, or both `:12461` and `:12499`.
3. **A cross-round fact this table settles, for #578.** P11 shows that comment-only and path-only differences do NOT change
   cpu_sh.c's binary. #578's M_b differed from HEAD's md5 in both its tables, with its cause written as "not established". The
   difference is that `dev_jazz.c:712` `CHECK_ALLOCATION` expands `FAILURE()` (`misc.h:181-184`), which formats `__LINE__`. The
   #578 comment shifts that line, so a string constant changes. The build-directory hypothesis I offered in #578's pass 2 is
   refuted by this table: M_b here was built in `/tmp/gxmut577` and still matched HEAD. I have appended that correction to my #578
   answer. (Change 5: the #578 record should cite this rather than "line info".)
4. **TEA/PTEH on the multiple hit** (`:12496-12498`) are not set (vaddr 0 at dev_sh4.c:1178). This is pre-existing (#457), not this
   round's, and CANNOT SETTLE what TEA should hold for an associative array write. It is a filing question at most.

Everything else every seat checked, I checked again and found true.

## Changes

1. The round block takes its order proofs from PRETABLE_CORRECTION.out's corrected text (pass-2 answer mtimes and script mtimes),
   never "this file's mtime". Mark P1/P8/P17 accordingly.
2. P6 and P10 wording: five post-table edits; cite base_head.raw / BUILD_FIXED.log mtimes, not KILLTABLE.log's first line.
3. Contract: add SR.MD to the guard-qualification disclosure.
4. Product comment cite: the operand-side multiple hit `:12499` (the only one raised here).
5. Carry the `__LINE__` explanation (P11 extension) to #578's M_b md5 record.

F2 VERDICT: RATIFY WITH CHANGES (5)
