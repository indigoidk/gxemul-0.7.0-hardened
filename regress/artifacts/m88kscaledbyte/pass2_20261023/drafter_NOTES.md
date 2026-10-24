# T1 (`m88kscaledbyte`, round `#569`) pass-2 brief -- drafter's notes: inconsistencies found, with dispositions

Read 2026-10-23 ~10:40-11:00 at the working tree over HEAD `5986c137`; read-only throughout (git object reads only; no
status, no diff, no index access; nothing run).  Artifact paths are relative to
`GXEMUL-SEC/regress/artifacts/m88kscaledbyte/`.  Ranked by what each could change in the round.  Each item: the
finding, then **Disposition**.

## 1. GATE 2 `PASS (502 checks)` (and GATE 11 `PASS (111)`) describe the WORKING TREE, not the commit (measurements vs records)
`table1_20261022/BUILD_REPORT.md:86-91` ("502 = the last battery's 376 + 126"; D-10 at `:115-117`) and
`table1_20261022/GATE2_tail.out:5-6`.  The working tree's `regress/gate_offline.sh` carries three foreign hunks (+58 -3;
HEAD lines ~1738, ~1832, ~2273); the second adds 17 `check` calls (`#563`'s WDC IDENTIFY presence rows; all 17 listed in
`brief2_FULL.md` 9.15), and GATE 2 also compiles the foreign-modified `regress/diff_wdc_identify.c`.  The battery's 376
(2026-10-11, 2026-10-18) came from `TREE_DIRTY=YES` runs with BOTH files modified
(`_scratchpad/nightly/verdict_20261011_180002.txt:2-7`, `verdict_20261018_231924.txt:2-7`); the 2026-10-04 battery at
HEAD `1329d894` -- the last commit to touch `gate_offline.sh`, `diff_wdc_identify.c` or `lib.sh` (`git log
1329d894..HEAD` on them: 0) -- reported 359 with neither modified (`verdict_20261004_180001.txt:2-7`,
`battery_20261004_180001.log:2325`).  So the COMMITTED form (`table1_20261022/staged/gate_offline.sh` = HEAD + the
round's hunk) should report 485, not 502 -- DERIVED; the staged copy was never run.
**Disposition:** brief P2, asked in Q4(d).  The record must name the tree measured; either GATE 2 is run once on a
clean clone (HEAD + the staged gate + the round's four files), or no check count is claimed for the committed tree.

## 2. The block runs before GATE 2's compiler detection (diff vs gate design)
Inserted after the `#375` block (staged `gate_offline.sh:74-118`); GATE 2 detects `cc || gcc` only at HEAD
`gate_offline.sh:183-185`, `regress/lib.sh` does not export `CC`, and the driver defaults `CC=${CC:-cc}`
(`regress/diff_m88k_loadstore_gen.sh:92`).  A gcc-only host reds `gen_compiles` while the gate's own differentials would
run; a no-compiler host turns GATE 2 from SKIP into FAIL (`BUILD_REPORT.md:112-114`, D-9; `lib.sh:137-145`).  The
`b1w` comment directly below the insertion says compiler-free checks sit before the compiler check "on purpose".  The
placement came from `BUILD_SPEC.md:69-70` / CHECKS #11 (keep away from the foreign hunks); compiler dependence was not
weighed in pass 1.
**Disposition:** brief P3, asked in Q4(a).  Not ruled here.

## 3. The `#569` comment says all 24 slots are consumed; 8 are not (diff vs rulings)
`src/cpus/generate_m88k_loadstore.c:258-261` (working tree): "They were NULL, and xmem_slow() calls them unguarded while
the ld/st decoder installs them as ic->f".  A6 / B8-as-amended (`pass1_20261022/PASS1_RULINGS.md:24`, `:63`) and the
driver's own header (`diff_m88k_loadstore_gen.sh:37-39`, "(no consumer)") say 424 440 480 484 488 496 500 504 have no
consumer today.  `table1_20261022/PRETABLE.out:75-78` maps the sentence (C6) to NO ROW.  The gate block's comment
(staged `gate_offline.sh:76-78`) uses the singular ("calls the slot") and does not over-state.
**Disposition:** brief P1, asked in Q1(c); a possible L4 wording repair, for the panel.

## 4. The `-x` row cannot go red on this machine, and the new file's mode must be set by hand at staging (diff vs landing)
`BUILD_REPORT.md:30`: "must be added with mode 100755 (the gate tests `-x`; `core.fileMode=false` here, and WSL shows rwx
regardless)".  `git config core.filemode` = false; the precedent `regress/diff_autodev_gen.sh` is 100755
(`C0_OUTPUT.txt` part 3).  With `core.fileMode=false` the mode has to be given explicitly when staging (`--chmod=+x`)
and is observable only by `git ls-files -s` afterwards (or on a host that honours modes).
**Disposition:** brief P4 / S19, asked in Q4(a); a landing step, not a code change.

## 5. The landing must commit the STAGED gate copy, not the working-tree file (diff vs landing)
Staged copy md5 `7a7fd8bc` = HEAD + one hunk (+45 -0); working-tree file `74d84bc1` = that + the three foreign hunks.
`staged/insert_HEAD.diff` and `staged/insert_WT.diff` differ only in their two header lines (checked).  Committing
`regress/gate_offline.sh` from the working tree would ship another session's in-flight `#563` hunks under `#569`; none
of the 18 other modified paths (`C0_OUTPUT.txt` part 6) belongs to the round either.
**Disposition:** stated in brief section 0 and 7.3; Q4(b).

## 6. Records owed at landing (records vs rulings)
Ledger row (HEAD == working tree): no `entries` field at all -- the pass-1 seats (`codex_t1p1.txt`, `grok_t1p1.txt`,
`ollama_glm_t1p1_Q12/Q34.txt`, `ollama_deepseek_t1p1_Q12/Q34.txt`), Argon's seat failure (`argon_t1p1.DROPPED.txt`), the
Fable hold (`fable5.HELD.txt`, with its hold question) and the adjudication (`adj/codex_t1p1adj.txt`) are unrecorded, and
no panel directory is cited; `witness: none`; the state_note still says "Fix shape DISPUTED".  `OUTSTANDING_BUGS.md:28-29`
and `:25260-25263` still say "fix shape disputed; pass 1 settles it".  `m88kxmemaddrovl` and `m88klepsrbo` (C1/C2) are in
neither the ledger nor OUTSTANDING_BUGS.  `witness_attempt_20261022/WITNESS_ATTEMPT.md` and the whole artifacts directory
are untracked, while the new driver cites `WITNESS_ATTEMPT.md` (`diff_m88k_loadstore_gen.sh:67-69`) and three
`table1_20261022/` files (`:76-79`).  HEAD's newest round `#568` landed "held for Fable" (`2ca79b90`), the precedent
for a row whose Fable stage is HELD.
**Disposition:** Q5(a).

## 7. `PASS1_RULINGS.md:3-11` still carries the pre-adjudication roster (records vs records)
":3 of 4 rostered seats", ":9 NOT FIRED by owner roster: agy, kimi, deepseek, minimax, opus5. Every seat answered; no
seat failure." -- but DeepSeek was fired (`ollama_deepseek_t1p1_Q12.txt` 09:34:57, `_Q34.txt` 09:35:57) and Argon failed.
The adjudication asked for the replacement (`adj/codex_t1p1adj.txt:73`); section E's heading (`PASS1_RULINGS.md:52-55`)
supersedes it only by reference; `BUILD_REPORT.md:118-119` lists it as main-loop records work.  If corrected,
`pass1_20261022/MANIFEST.md5` (27 entries, all `OK` at drafting) must be regenerated.
**Disposition:** quoted in Q5(a).

## 8. The pre-fix order: the only pre-edit-dated red is driver v1's (measurements vs rules)
`driver_v1/prefix_HEAD.out` 09:46:19.436 (122 rows, unmodified repository) < generator edit 09:46:58.650; the shipped v3
(123 rows) was measured pre-fix at 10:03:08.950 through `GEN=`/`TABLE=` on byte-exact HEAD blob copies (`RUNS.log:4-7`).
Drafter's check: the 54 index -> expected-name pairs are identical v2 -> v3 (`driver_v2_to_v3.diff`; only class letters
F/E -> R/N and four descriptions change) and v1 -> v2 adds 5 comment lines (`driver_v1/RERUN_v2.txt:3-4`); v3 adds
`gen_stdout` and the identity column.  Carrier R17 (`tools/CLAUDE.md:2518-2523`) separates "a red" from "an authentic
pre-edit DATE".  BUILD_REPORT D-4 and open question 1 ask the same.
**Disposition:** brief P5, asked in Q3(d).

## 9. Nothing outside the GATE 2 block holds the driver (detector vs harness)
`#406`'s driver re-runs its own variant lane every gate run (HEAD `gate_offline.sh:1914-1917`, `:1925-1926`); GATE 2's
self-variant manifest covers `diff_*.c` only (HEAD `:1155`); `tools/pipeline/check_probe_wiring.py:1247-1248` (HEAD) is
`.py`-only.  So the `#569` driver's sensitivity rests on the one-time table, and its wiring on the block itself.
**Disposition:** brief P6 / S20, asked in Q2(e) and Q4(e); a FILE candidate unless a seat shows a floor breach.

## 10. COMPACT is over the 90 KB aim (brief form)
`brief2_COMPACT.md` 113,742 bytes.  The diffs alone are ~26 KB (the new driver 16.0, the table 4.9, the gate hunk 3.8,
the generator 0.8, numstat 1.7); S/P/Q ~19.8 KB; opener and section 0 ~5.4 KB; the verbatim rulings (A cells, five B
rows, E, Astra's verdict + Q3, BUILD_SPEC section 10) ~13.8 KB; the rule quotes ~10.5 KB; the measurement lines ~22 KB.
Under 90 KB needs one of: dropping the rule quotes (~10 KB), the A/B/E text (~9.6 KB), or SCORES' per-run measured sets
plus the BUILD_REPORT D-list (~8.5 KB) -- each something a question reads.  Pass 1's packet-fed firings used ~92 KB
packets split by question (`pass1_20261022/packet_glm_Q12.md`, `packet_glm_Q34.md`).
**Disposition:** left at 114 KB with every diff line; if a smaller packet is wanted, fire Q1+Q2 and Q3-Q5 separately
(the builder scripts are in this directory's `work/`).

## 11. Two deliberate deviations from the coordinator's wording (brief form)
(a) Q2(f), the ask-again: the request was "Name the smallest edit to the generator or the table that would pass all 123
rows".  `tools/BRIEF_TEMPLATE.md` section C5 rule 3 ("Do not ask codex for a mutant ... or 'the smallest edit that
re-opens this'") binds any text that reaches codex, and panel.sh fires codex with the brief; Q2(f) uses C5's clean
form (say whether one exists; name where it acts and the row expected to stay green; no patch text).  (b) Reading
scope: C5 rule 2 says "do not read `regress/artifacts/`"; the brief permits THIS ROUND'S directory only (every cited
artifact is there; the leg-variant `.diff` files are named "need not be opened").
**Disposition:** for the coordinator; restore the literal ask for a non-codex seat if wanted.

## 12. BUILD_REPORT carries D-1..D-10; the brief request named D-1..D-9 (brief scope)
`BUILD_REPORT.md:93-120`.  D-10 (both gates measured the working tree) is the record behind item 1.
**Disposition:** Q5(b) asks D-1..D-10 and open questions 1-4.

## 13. Volatile helper scripts cited by durable records (records)
`SCORES.txt:3` names its scorer `scratchpad t1/build/score3.py`; `BUILD_REPORT.md:126-128` (open question 3) says the
variant builder, runners and scorer live only in the session scratchpad.  The leg variants themselves are preserved as
`L*.diff` / `S*.diff`.
**Disposition:** Q5(b).  Any `.py` preserved under `regress/artifacts/` needs a `check_probe_wiring.py` MANIFEST line.

## 14. Trivial drifts (no action beyond a note)
* `PRETABLE_v3.out:6` "before the generator edit at 09:47" -- the generator's mtime is 09:46:58.650 (`FIX.out:2`); the
  table's is 09:47:51.  The order holds either way.
* `FIX.out:33` "lines: head 4251 new 4251" counts `split('\n')` pieces; the file has 4,250 newline-terminated lines
  (`BASELINE.out:39-40`, `wc -l`).
* `CHECKS_mainloop.md:16` "the `#406` block at HEAD `gate_offline.sh:1886` (WT `:1938`)" -- the working-tree position
  is now `:1983` after this round's +45 insertion (`:1931` in the staged copy).
* `PRETABLE.out:46` "four sites index unguarded" lists three; `BUILD_REPORT.md:105-107` (D-5) already records it.
**Disposition:** none required; listed so a seat that finds them does not spend an answer on them.
