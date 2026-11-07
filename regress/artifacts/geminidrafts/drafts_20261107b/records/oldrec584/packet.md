# Reading task: oldrec584 (Gemini web; 2026-11-07)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-GWEBOLDREC584-d92f` on a line of its own.

# GXemul hardened fork -- RECORDS CHECK of one landed round's CHANGELOG block: #584 fmtattr (a defensive project's bookkeeping)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator and this fork records each
fix in a CHANGELOG round block.  The block below has landed; a flagship review of it is still owed.  You cannot read files, so
judge the block AS WRITTEN.  Do not simply ratify it.  A bracketed dated note inside the block is this project's in-place
correction form (it quotes the text it corrects); it is not by itself a contradiction.

## The round block (CHANGELOG.md lines 195-270 of CHANGELOG_521d136a.md; each line carries its own number -- cite those numbers)

```text
  195| # `#584` Records (follow-up, 2026-11-05): `fmtattr` names its landing commit `ccd1c502`; the committed-tree proofs; the pass-2 receipt
  196| 
  197| `git ls-tree ccd1c502`, md5s hashed in Python from the committed bytes: `src/include/misc.h` blob `39fe40c52198`, md5 `a824683b06a8`; `src/disk/bootblock.c` blob `1fa97b1392d4`, md5 `1f1fb1da6288`; `src/cpus/cpu_alpha_palcode.c` blob `39ae212f6487`, md5 `f69c02e83030`; `regress/fmt_bootblock_probe.py` blob `29526c98e48e`, md5 `5728fc0761fd`; `regress/gate_build.sh` blob `07409171f4f4`, md5 `362b6640ce40`; `tools/precommit_check.sh` blob `014582d94c23`, md5 `7c878c20dc21`; `tools/pipeline/check_probe_wiring.py` blob `804c1cff80fb`, md5 `eacfa4ff9575`; `.github/workflows/codeql.yml` blob `3c1a4c7e1d4b`, md5 `271a042209e9`; the 47 committed `src/` files' blob md5s, hashed in order, `0172902f0f14`.  The working copy against each: misc.h the same; bootblock.c the same; cpu_alpha_palcode.c plus the peer session's uncommitted lines (1 hunk(s), 23 lines); fmt_bootblock_probe.py the same; gate_build.sh the same; precommit_check.sh the same; check_probe_wiring.py plus other rounds' uncommitted MANIFEST entries (2 hunk(s)); codeql.yml the same.
  198| 
  199| The four trees took the committed files in the landing window and keep them (no restore owed: `regress/artifacts/fmtattr/landing_20261105/UPDATE_FMT.out`); `cpu_alpha_palcode.c` there keeps the peer session's lines and this round's two.  The palcode hook step's trees were put back after the commit: each tree's `cpu_alpha_palcode.c` is again the working copy's -- the peer session's lines and this round's two -- with `cpu_alpha_palcode.o` rebuilt and both clearance parts passing (`regress/artifacts/fmtattr/landing_20261105/HOOKRESTORE_FMT.out`).  The `commits` fields of `fmtattr`, `fmtmissarg` and `codeqlscope` (still open: the repository setting is the owner's) name `ccd1c502`.  The `regress/pass2_ledger.tsv` receipt line for `ccd1c502`, a landing line in OUTSTANDING_BUGS.md's `#584` section and `matrix.html` re-rendered complete this records commit.
  200| 
  201| # `#584` (2026-11-05) -- `fmtattr`: the four diagnostic functions are printf-checked by the compiler, every call matches its format (`fmtmissarg`'s three missing arguments included), and gate 1 enforces it
  202| 
  203| **The defect.**  `debug()`, `fatal()`, `debugmsg()` and `debugmsg_cpu()` (`src/include/misc.h`) are printf-like and carried no
  204| format attribute, so nothing checked their calls.  GitHub CodeQL raised 116 wrong-type and 3 wrong-number format alerts on the
  205| pushed `759f7131`; GCC, with the four declarations given `format(printf, ...)` in a scratch build of HEAD `f58105b7`, gave 181
  206| format warnings -- 145 `-Wformat=` (the three missing arguments among them), 13 `-Wformat-extra-args`, 19 `-Wformat-zero-length`,
  207| 4 `-Wformat-overflow=` (`regress/artifacts/fmtattr/scan_20261105/fmtscan.out`, `regress/artifacts/fmtattr/scan_20261105/fmt_warnings.tsv`) -- none of them introduced after the push
  208| (`regress/artifacts/fmtattr/scan_20261105/PREMISE_A.txt`).  On x86-64 the effect is a truncated, garbled or unspecified number in a diagnostic: `x11.c`'s stray
  209| comma made a `%i` consume a string pointer, and `fmtmissarg`'s three calls (a guest read of a PS2 timer 2/3 hold register, a
  210| non-byte MB89352 access, the debugger's PPC601 register dump) printed whatever the varargs held.  Filed by `79df4277` from the
  211| code-scanning triage (`regress/artifacts/fmtattr/scan_20261105/CODESCAN_TRIAGE.md`).
  212| 
  213| **Adjudication.**  GPT-6 Astra at ultra (`regress/artifacts/fmtattr/adj_20261105/astra/codex_csadj.txt`) and Gemini 4 Argon (`regress/artifacts/fmtattr/adj_20261105/gemini_adj_items/reply.txt`)
  214| agree on one combined format round with `fmtmissarg` folded in, `disasmnullmnem` a false positive (no row) and the no-action list;
  215| Astra adds an ENFORCED failure policy, a negative control per function, each message's radix and meaning kept, and mb89352's
  216| unsupported value field removed.  Owner rulings 2026-11-05: the enforcement is a gate check and the build stays warning-only; `cpu_alpha_palcode.c` is
  217| fixed in HEAD and in the peer session's working copy, two lines only; the round is tagged in this block, not per call.
  218| 
  219| **The fix** (47 files, 124 hunks, +236 -217 lines: `regress/artifacts/fmtattr/landing_20261105/COMPOSITE.diff`).  Built outside the repo from HEAD
  220| `79df4277`: Gemini 4 Argon drafted 127 exact-text edits in eight packets (`regress/artifacts/fmtattr/drafts_20261105/`); 126 call sites replaced, 2
  221| rejected (`regress/artifacts/fmtattr/stage_20261105/SUMMARY.txt`, `regress/artifacts/fmtattr/stage_20261105/REJECTS.txt`, `regress/artifacts/fmtattr/stage_20261105/WHY.txt`); x11.c's comma removed and cpu_mips.c's ASID cast by hand (`fix_hand.py`);
  222| the 19 empty-line calls given `"%s", ""` and an unreachable `default: mnem = "?"` in the three disassembler switches the overflow
  223| warnings named (`fix_hand2.py`); `GX_PRINTF(f, a)` -- the attribute under `__GNUC__`, empty elsewhere -- on the four
  224| declarations (`fix_misc_h.py`); pass 2's seven repairs (`fix_hand3.py`) and pass 2b's one (`fix_hand4.py`).  The rules: `PRIx64`
  225| with a `(uint64_t)` cast for a wide hex value, an `(int)` cast only where the value is small by construction, `%zu` for
  226| `size_t`, a missing argument added only where its value exists.  The round number fills the four structural comments (misc.h's
  227| macro, the three `default:`s); the one-line call fixes carry no tag.  `cpu_alpha_palcode.c` is HEAD plus its two lines (:136-137);
  228| the peer session's uncommitted lines in that file stay in its working copy and the four trees, which took the two lines in place.
  229| The SEC working copy and the four trees took the 46 staged files, and the palcode copy only its two lines, in the landing window; the three build trees rebuilt from scratch with both clearance parts passing on all 47 files (compiler warnings: build 0 build-asan 6 gxsec-build 0; build-asan's are sanitizer-only, 0 format-class), and on each rebuilt binary the staged probe scored FMTBB_RESULT=3/3, CONTROL=OK and the four seeded controls warned 4 of 4 (`regress/artifacts/fmtattr/landing_20261105/UPDATE_FMT.out`).  For the commit's hook only, est/, build/, build-asan/ and /tmp/gxsec-build held the committed cpu_alpha_palcode.c (the peer session's copies backed up byte for byte and put back after the commit by palcode_hookrestore_fmt.sh), with cpu_alpha_palcode.o rebuilt and both clearance parts passing (`regress/artifacts/fmtattr/landing_20261105/HOOKSWAP_FMT.out`).
  230| 
  231| **Detector.**  The class detector is the compiler: with `GX_PRINTF` permanent a mismatched call is a warning, and gate 1
  232| (`regress/gate_build.sh`) already fails on any warning in either tree.  Its new fmtattr block (14 checks, above `gate_end`):
  233| one deliberate mismatch per function, each on its own line, compiled with the tree's own CC and CWARNINGS, must warn -- 4 of 4,
  234| no other warning; and `regress/fmt_bootblock_probe.py` (new, 3 rows; Astra pass 2b's output row) pins the one representative
  235| type-compatible repair no compiler sees -- bootblock.c's SGI loading line on unmodified `-E sgi -e ip32` must print disk offset
  236| `0x100000000` (a one-sector image naming `sash` at block 0x00800000) -- RESULT pinned 3/3 by equality, CONTROL=OK, every row by
  237| name.  `tools/precommit_check.sh` SCORE_CLAIMS_MANIFEST 49 -> 50; `tools/pipeline/check_probe_wiring.py` entries for the probe and
  238| 8 artifact scripts (`regress/artifacts/fmtattr/landing_20261105/MANIFEST_fmt.txt`).  Measured on the stage before the landing: HEAD + the stage, built as a user
  239| builds it, 0 warnings and 4/4 controls (`regress/artifacts/fmtattr/stage_20261105/fmtverify2.out`); the probe 3/3 on the fix, and the radix (`PRIx64` -> `PRIu64`)
  240| and narrowing (`(uint64_t)(uint32_t)`) mutants 2/3 each with 0 build warnings (`regress/artifacts/fmtattr/row_20261105/bb_kill.out` and its build logs; its base
  241| predates pass 2b's file_ecoff.c repair by seconds, a file off the probe's path).  Gate 1's fmtattr block, as staged, ran alone before the landing over fifteen legs and the restored base, 16 of 16 red sets as predicted (`regress/artifacts/fmtattr/landing_20261105/DRYRUN_fmt.out`; the predictions written first, `regress/artifacts/fmtattr/landing_20261105/PRETABLE_fmt.out`): the fix's scratch build (`git archive HEAD` plus the 47 staged files, 0 warnings) green on all 14 checks before and after the product legs, and every check red on at least one leg.
  242| Gate 1 ran in situ at the landing with the staged gate_build.sh on the updated trees: clean-build: PASS (32 checks), the fmtattr block's 14 checks ok, FMTBB_RESULT=3/3, the four controls 4 of 4 (`regress/artifacts/fmtattr/landing_20261105/GATE1_INSITU_fmt.out`).
  243| 
  244| **Floor** (`regress/artifacts/fmtattr/landing_20261105/DRYRUN_fmt.out`).  (a) HEAD: controls 0 of 4 and the probe 2/3 (offset 0x0) on both HEAD build trees; (b) HEAD's bootblock.c
  245| restored in the fixed tree: its build warns twice and the probe reds; (c) /bin/true, /bin/false and an absent binary: CONTROL=FAIL;
  246| (d) the attribute nulled -- dropped from one declaration, defined empty, or `(4, 0)` -- reds exactly the controls it silences; (e)
  247| the probe's contract: one representative wide-hex row; the other type-compatible radix and value edits -- Astra counted 48 calls
  248| exposed to the radix mutation and 39 to the narrowing one (`regress/artifacts/fmtattr/p2_20261105/astra/codex_fmtp2.txt`) -- are disclosed, not claimed.
  249| 
  250| **Review (pass 2).**  GPT-6 Astra on the diff (`regress/artifacts/fmtattr/p2_20261105/astra/codex_fmtp2.txt`: `FMTP2: 7 EDITS WRONG, 4 NARROWINGS UNSAFE, 3 OTHER; VERDICT
  251| fix first`) -- the seven repaired; then on the composite (`regress/artifacts/fmtattr/p2b_20261105/astra/codex_fmtp2b.txt`: `FMTP2B: 0 REPAIRS WRONG, 1 NEW DEFECTS, ROW owed,
  252| TRUNCATIONS file`) -- file_ecoff.c's two `off_t` values repaired, the row built as the probe, the inherited narrowings filed.  Owed,
  253| and held with its question on the rows' regress stage (`_scratchpad/pipe/FABLE_QUEUE.md` item 4): Fable's final ruling on the
  254| round as committed, which is also the repair chain's closing pass on pass 2b's repair.
  255| 
  256| **Filed** (ledger and OUTSTANDING_BUGS.md's `#584` section): `fmttruncinherited` (LOW) -- narrowings this round inherited and left
  257| (Astra: luna88k :919, lunafb :85/:177, memory.c :626, arcbios's A1/A2, ps2_bios's A1, dev_ether :125/:130, LE's writes
  258| :1014/:1034/:1052, bt455 :82, staged numbering), each printing the low 32 bits of a value that can be wider.  `codeqlscope`
  259| stays open: the CodeQL advanced-setup workflow and config land here (`.github/workflows/codeql.yml`,
  260| `.github/codeql/codeql-config.yml`: paths-ignore regress/artifacts and experiments); the OWNER switches Code scanning to Advanced
  261| after the next push.
  262| 
  263| **Seats.**  One ledger entry per seat file of each stage on `fmtattr`, the non-firings and seat failures by name.  Research: 17 entries, 10 of them answers (codex 1, the adjudication; agy 9, Gemini 4 Argon's adjudication and its eight fix drafts); review: 10 entries, 2 answers (codex 2, Astra's passes 2 and 2b).  Grok 4.7 (402) and GLM 5.3 (monthly limit) are seat failures; kimi, deepseek and minimax were off the roster; Opus 5.5 built the round and Gemini drafted it, so neither reviewed it.  Fable's final is HELD on `fmtattr`'s and `fmtmissarg`'s regress stage with its question.
  264| 
  265| **Of the round's evidence** the commit carries 94 files under `regress/artifacts/fmtattr/` (`regress/artifacts/fmtattr/landing_20261105/ART_fmt.txt`: destination, md5,
  266| source), copied from `_scratchpad/codescan/` and `_scratchpad/gweb/`, with the five measurement scripts that lived only in the
  267| session scratchpad.
  268| 
  269| **Landing.**  The citation gate cannot select this block (`check_cited_artifacts.py` keys on `## Round <digits>` headings: `citeprefixblind`, filed by `#554`); its own resolver, run over the block by hand at the landing, resolves all 18 citations to this round's files.
  270| 
```

## Questions -- verdict line first

1. Does the block contradict itself anywhere -- two different numbers for one quantity, a total that its own parts do not sum
   to, a claim in one paragraph that another paragraph undoes?  Quote both places, with their line numbers.
2. Which claims are stated as MEASURED but cite no artifact, or cite one only by a bare file name that could be ambiguous?
3. Which sentences overclaim -- 'every', 'all', 'never', 'exactly' -- where the block's own evidence covers less?
4. What would a reviewer checking this block against its artifacts most likely find wrong?
When you count items the block enumerates, list them by name before giving the count.

End with one line: `RECBLOCK_584: <c> CONTRADICTIONS, <u> UNCITED, <o> OVERCLAIMS`.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`GWEBOLDREC584: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
