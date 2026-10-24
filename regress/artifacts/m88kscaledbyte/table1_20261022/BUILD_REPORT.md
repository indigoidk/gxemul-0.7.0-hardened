# T1 (`m88kscaledbyte`), round `#569` -- builder's report (resumed 2026-10-23; HEAD `5986c137`, unchanged throughout)

Spec: `pass1_20261022/BUILD_SPEC.md` sections 3-9, plus three mid-task additions from the coordinator: L8
(`ollama_deepseek_t1p1_Q34.txt:20-21`) and the GPT-6 Astra pass-1 adjudication (`pass1_20261022/adj/codex_t1p1adj.txt`,
verdict AMEND, the repair UPHELD).  No git write of any kind was made; nothing under `tools/` was edited; the peer's
files were not touched.  Pass 2 is the main loop's.  Every number below names the file that holds it.

## 1. What was done, in order
| when (10-23) | step | receipt |
|---|---|---|
| 10-22 23:40-23:45 | steps 2.1-2.3 by the previous builder, REUSED unchanged after checking them against the source and the packet: HEAD md5s in five trees, fresh `generate_m88k_loadstore` output == committed table at HEAD (CHECKS #6 discharged), 296 NULL / 512 / 198 | `BASELINE.out`, `PRETABLE.out` |
| 09:40 | L8 prediction written before any table run | `PRETABLE_L8.out` |
| 09:4x | driver v1 + GATE 2 block v1 (identical insertion into the working-tree file and a staged HEAD copy); a shake-down against scratch HEAD copies (construction, not recorded) | `driver_v1/` |
| 09:46:19 | step 4, pre-fix RED: v1 on unmodified HEAD (repo defaults), `ROWS=122 FAIL=50`: the 24 name pins in both artifacts (all `NULL`) and both NULL counts (296); the rest green, `cmp` identical | `driver_v1/prefix_HEAD.out` (+ `.meta`) |
| 09:46:58, 09:47:51 | step 5: the generator fix (`#569`); the table regenerated from it in `/tmp/gxt1/fix` and copied over the repo's -- exactly 24 changed lines, each `NULL` -> the design name at a pinned index, 512 entries, 272 NULL, LF | `FIX.out` |
| 09:47-09:51 | v1: `fixed.out` 122/0; legs L1-L8, L5b, S1, all equal to PRETABLE's predicted red sets row by row; v2 = v1 + the clause-(c) record comment (5 lines), every v1 run reproduced byte-identically by v2 | `driver_v1/SCORES.txt`, `driver_v1/RERUN_v2.txt`, `driver_v1/driver_v1_to_v2.diff` |
| 09:53-09:54 | step 7 begun: `est/` propagated; `build/` rebuilt | `CLEARANCE.out` |
| 09:55-10:02 | the adjudication applied: v1 receipts moved to `driver_v1/` (mtimes kept); driver v3; GATE 2 block v3; `PRETABLE_v3.out` written at 10:02:21, before any v3 run | `driver_v2_to_v3.diff`, `PRETABLE_v3.out`, `staged/` |
| 10:03 | the v3 table, 16 runs, ONE instrument (driver md5 `cc2f3cf1...` checked before every run); every measured red set == its predicted set, row by row, and every output carries all 123 identities exactly once | `RUNS.log`, `SCORES.txt` |
| 10:03 | L7's duplicate definition names, measured outside the driver | `DUPNAMES.out` |
| 10:04-10:07 | `build-asan/` and `/tmp/gxsec-build` rebuilt; the two-part clearance re-run over all four trees | `CLEARANCE.out` |
| 10:09-10:12 | GATE 2 alone (`run.sh 2`): PASS (502 checks), REGRESS_PASS | `GATE2_tail.out`, `GATE2_diff_m88k_loadstore_gen.log` |
| 10:12-10:17 | GATE 11 alone (`run.sh 11`) on the rebuilt `build/gxemul`: PASS (111 checks), REGRESS_PASS | `GATE11_tail.out` |

## 2. Diff stat -- the four repo files (plain `diff` against `git show HEAD:<file>`; all LF)
| file | + | - | |
|---|---|---|---|
| `src/cpus/generate_m88k_loadstore.c` | 8 | 4 | the whole arm at HEAD `:254-257` removed, the `#569` comment in its place; `:104-105` untouched |
| `src/cpus/tmp_m88k_loadstore.c` | 24 | 24 | regenerated, never hand-edited (`FIX.out`) |
| `regress/diff_m88k_loadstore_gen.sh` | 276 | 0 | NEW, untracked -- **must be added with mode 100755** (the gate tests `-x`; `core.fileMode=false` here, and WSL shows rwx regardless) |
| `regress/gate_offline.sh` | 45 | 0 | the block after the `#375` block; commit `staged/gate_offline.sh` (= HEAD + this hunk). The working-tree file = the same hunk + the foreign hunks untouched (`staged/insert_HEAD.diff` and `staged/insert_WT.diff` add identical lines at the same position, nothing removed) |

`est/` holds byte-identical copies of the two `src/` files (precommit section A).

## 3. The detector as built (driver v3, the file to commit)
* **The 24 output cells vs the 16 consumer cells.**  All 24 repaired cells are the FLOOR (adjudication B8: `main()`'s
  loops emit all 24), pinned by absolute name in both artifacts.  16 are today's guest-consumer subset, marked
  `(consumer)` (160 164 168 176 180 184 224 228 232 240 244 248 416 420 432 436); the 8 others are marked
  `(no consumer)`, which is a fact about today's callers, not a weaker pin.
* **Rows: 123** = 4 generator status rows (`gen_compiles`, `gen_exit`, `gen_stdout` -- new, B5 --, `gen_count`) + 2
  artifacts x (5 structural + **54 distinct name pins**) + 1 `cmp`.  54 = 24 repairs + 24 counterparts + 6 further
  accepts; the three counterparts that are also accepts (144 400 404) are emitted ONCE, as accept rows.
* Every row's first field is an identity that occurs exactly once in the output; GATE 2 pins each of the 123 from its
  OWN index lists (`== 1`), plus `ROWS == 123`, `FAIL == 0` and the `M88KLS_DONE` sentinel.
* Halfword accept 161/177 warranted by R12 (B3); `LS_N`/`generated_functions == 198` stated as a narrow suppression-
  count control, not definition integrity (B4); the header's NOT-OBSERVED list names handler bodies and the xmem
  exchange (the BLOCKED witness record) and the generated definitions beyond their count.

## 4. Scores (every one from its artifact; v3, 123 rows; `SCORES.txt` compares each red set row by row)
| run | red/rows | artifact | what it is |
|---|---|---|---|
| PRE | 50/123 | `prefix_HEAD_v3.out` | clause (a) on the HEAD blobs through the overrides (see D-4) |
| FIX | 0/123 | `fixed.out` | the fixed repo files, repo defaults |
| L1 | 26/123 | `L1_headgen.out` | clause (b) at the generator site |
| L2 | 26/123 | `L2_headtable.out` | clause (b) at the table site |
| L3 | 64/123 | `L3_commentgen.out` | clause (c), measured: comment-only generator |
| L4 | 60/123 | `L4_commenttable.out` | clause (c), measured: comment-only table |
| L5 | 14/123 | `L5_v2nopcsync.out` | clause (d): `grok_t1p1.txt:76`'s v2, first difference 416 |
| L6 | 14/123 | `L6_lehalf.out` | clause (d): the little-endian half left as before the fix |
| L7 | 3/123 | `L7_v6halfword.out` | accept edge: 161/177 red, word pins green; NOT silent -- 24 duplicated `#define LS_N` names (`DUPNAMES.out`) |
| L8 | 56/123 | `L8_allnull.out` | SUPPLEMENTARY: all-NULL initializer (the coordinator's 24 pins + accepts + NULL count, and also the 21 committed counterparts) |
| L5b | 30/123 | `L5b_codexnopcsync.out` | SUPPLEMENTARY only: `codex_t1p1.txt:100`'s different predicate (first overall difference 256) -- not L5 |
| S1 | 3/123 | `S1_noearlyreturn.out` | SUPPLEMENTARY (B4 control): `:104-105` deleted, `gen_count` and `fresh_lsn` 210 |
| S2 | 1/123 | `S2_exit1.out` | SUPPLEMENTARY (B5): exit 1 -> `gen_exit` only |
| S3 | 62/123 | `S3_emptyout.out` | SUPPLEMENTARY (B5): exit 0, empty stdout -> `gen_stdout` and every fresh row |
| S4 | 60/123 | `S4_notable.out` | SUPPLEMENTARY (B5): table absent -> red, not a skip |
| S5 | 64/123 | `S5_nogen.out` | SUPPLEMENTARY (B5): generator absent -> red, not a skip |

The variant of each leg is a file only: `L<n>.diff` / `S<n>.diff` (S4/S5 are absent paths, no diff).  The v1 table
(122 rows: PRE 50, FIX 0, L1 26, L2 26, L3 63, L4 60, L5 14, L6 14, L7 3, L8 56, L5b 30, S1 3) is in `driver_v1/`.
**(c): measured at** `L3_commentgen.out` and `L4_commenttable.out` (first by v1: `driver_v1/L3_commentgen.out`
63/122, `driver_v1/L4_commenttable.out` 60/122); L8 is supplementary, not a prerequisite.

## 5. Clearance (`CLEARANCE.out`, run 10:07:46 over all four trees; neither file is in the derived divergence set)
```
est         part 1 CLEAN, CLEAN      part 2  est/: source tree, part 2 N/A (no binary exists)
build       part 1 CLEAN, CLEAN      part 2  [ gxemul -nt generator ] yes, [ gxemul -nt table ] yes   (gxemul 09:54:12)
build-asan  part 1 CLEAN, CLEAN      part 2  yes, yes                                                 (gxemul 10:06:40)
gxsec-build part 1 CLEAN, CLEAN      part 2  yes, yes                                                 (gxemul 10:07:16)
```
In each build tree make itself re-ran `./generate_m88k_loadstore > tmp_m88k_loadstore.c` (once, shown by its log
line) and the in-tree table then `cmp`s CLEAN against GXEMUL-SEC's: the agreement row, measured in a real build.
`rm src/cpus/*.o; make -j8`, rc 0, no `.MUTANT` anywhere, no concurrent job.

## 6. Gates (each once, alone, `bash regress/run.sh <n>`, LOGDIR = lib.sh default `/tmp/gxregress`)
* **GATE 2** `offline-differential: PASS (502 checks)`, `REGRESS_PASS`, rc 0, 171 s.  The #569 block's 126 checks all
  ok; 0 gate-level FAIL rows; 502 = the last battery's 376 + 126.  The gate-side driver log is byte-identical to
  `fixed.out`.
* **GATE 11** `gate 11: m88k rounding mode (#298): PASS (111 checks)`, `REGRESS_PASS`, rc 0, 247 s, binary
  `build/gxemul` (09:54:12).  111 = the last battery's count.
Both measured the WORKING TREE (see D-10).

## 7. What disagreed with the spec or a ruling (by id), and deviations
* **D-1 (BUILD_SPEC section 6, L5; B7).**  The spec's L5 pointer named `grok_t1p1.txt:76` and `codex_t1p1.txt:100`,
  which are two different predicates (first differences 416 and 256).  The adjudication (B7) resolved L5 to Grok's;
  Codex's is kept only as the labelled supplementary L5b.
* **D-2 (B8; PRETABLE.out section 0).**  The 16-floor / 8-clause-(e) split is superseded: all 24 are floor; 16 is the
  consumer subset.  PRETABLE.out is left as written; `PRETABLE_v3.out` records the change.
* **D-3 (B3, B4, B5, B10, B12).**  Applied as the adjudication amended them (section 3).  B10's per-identity pins raise
  GATE 2 from 376 to 502 checks; nothing in `tools/` or `regress/` pins that count (searched).
* **D-4 (BUILD_SPEC section 4).**  v3's pre-fix run (`prefix_HEAD_v3.out`) went through the GEN/TABLE overrides on the
  byte-exact HEAD blobs AFTER the step-5 edit, because the adjudication arrived after the fix.  The authentic
  pre-edit-dated receipt is `driver_v1/prefix_HEAD.out` (09:46:19, before the 09:46:58 generator edit).  The repo
  was not reverted to re-date it.
* **D-5 (PRETABLE.out, two small inaccuracies, not rewritten).**  Section 5 predicted `0` for L3's fresh LS_N row and the
  driver reports `absent` (red either way).  Section 1 says "four sites index unguarded" while listing three; the
  fourth, the immediate form at `cpu_m88k_instr.c:3087`, cannot form a scaled index.
* **D-6 (supplementary legs beyond the spec).**  L5b and S1 (from PRETABLE.out), S2-S5 (added for the B5 rows).
* **D-7 (section 7).**  `make -j8`, one make job, instead of a plain `make`.
* **D-8 (coordinator's L8 expectation).**  The measured red set also includes the 21 committed-side counterpart rows
  (all NULL by construction): 56, as `PRETABLE_L8.out` predicted.
* **D-9 (placement, observation).**  The block sits before `gate_offline.sh`'s compiler check, as specified.  On a host
  with no C compiler it reds via `gen_compiles` (B5's explicit red), and the gate's later "no C compiler" `gate_skip`
  then reports FAIL, not SKIP (`lib.sh`: a skip after failures is a FAIL).
* **D-10 (trees).**  The five peer files are uncommitted in GXEMUL-SEC and byte-identical in every build tree (already
  compiled into the old binaries); `rm src/cpus/*.o` recompiled `cpu_alpha` with the peer's `cpu_alpha_palcode.c` as it
  stands.  Both gates therefore measured the working tree, `gate_offline.sh`'s foreign hunks included.
* **C1 / C2:** filed outside T1 only (adjudication C1/C2); nothing here touches them.  The adjudication's corrections
  to PASS1_RULINGS (roster line) and CHECKS #4/#6/#7 are records work for the main loop.  CHECKS #6 is discharged by
  `BASELINE.out` section 3.

## 8. Open questions for the main loop
1. Is the post-edit v3 pre-fix run (D-4) acceptable beside the v1 pre-edit receipt?
2. 123 individual identity checks (as amended) or one aggregated check that names any failing identity?  (Each adds
   one gate line; GATE 2 now prints 123 more.)
3. The helper scripts (variant builder, runners, scorer) live only in the session scratchpad
   `t1/build/`.  Any `.py` copied under `regress/artifacts/` needs a `check_probe_wiring.py` MANIFEST line.  The diff
   files already specify every variant.
4. The Fable stage is HELD (`fable5.HELD.txt`), so the rulings this build follows are provisional on their face.

BUILD_REPORT_DONE
