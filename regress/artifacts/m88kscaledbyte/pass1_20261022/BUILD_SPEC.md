# T1 (`m88kscaledbyte`) -- the builder's spec, round `#569` (2026-10-22)

Everything here is a pointer into `PASS1_RULINGS.md` (A1-A6, B1-B12, D1-D6) and `CHECKS_mainloop.md` (#1-#11) in this
directory, with the concrete steps and the order the carrier requires.  Record OUTPUT, never assertion.

## 0. Ground rules (the brief is the only sandbox)
* Project root `C:\DocumentNoSnc\cc\GXEMUL`; the repo and the only tree under edit: `GXEMUL-SEC/` (git root).  The
  tree under review is `GXEMUL-SEC/src/`; `./src/`, `_archive/**/src/` and `GXEMUL_upstream_2021/` are pristine 2021
  upstream -- never read them for facts.  `est/` is the untracked twin (shared files byte-identical); `build/`
  (pmax), `build-asan/` and WSL `/tmp/gxsec-build` are NO-VPATH build trees.
* Git: object reads only (`git show`, `git log`, `git ls-files`).  Never `git add/commit/status/diff/stash/checkout/
  restore` -- another process may hold the index.  Nothing under `tools/` is edited.  The peer's files are never
  touched: `src/cpus/cpu_alpha_palcode.c`, `src/devices/dev_lca.c`, `src/devices/dev_pcc2.c`, `src/devices/dev_sh4.c`,
  `src/include/thirdparty/mvme_pcctworeg.h`, `regress/sh4_chcr_probe.py`, `regress/gate_sh_rounding.sh`,
  `regress/gdrom_default_probe.py`, `tools/adjudicate.sh`.  `regress/gate_offline.sh` carries foreign uncommitted
  hunks (CHECKS #11): INSERT your block only; change nothing else in it.
* Builds and gate runs happen under `wsl -d Gentoo` (the default distro has no `make`): invoke scripts as
  `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/...`; write helper scripts to the session scratchpad
  (`C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\t1\build\`),
  never to git-bash `/tmp`.  `rm src/cpus/*.o` before a build tree's `make`; a build's freshness is `[ binary -nt source ]`,
  never the make rc.  FOREGROUND ONLY: no plain `&`, no `nohup`; one job at a time; never two gate invocations at once.
  Never `rm -rf` outside your own scratch dirs.  Never run the generator INSIDE the repo tree (it prints to stdout; redirect
  only into your scratch dir, then copy the result where step 5 says).
* Text hygiene: the generator and the regress scripts are LF files; write with a tool that preserves LF (python
  `io.open(..., newline="")` both ways; `file -b` to check).  Line numbers below are HEAD `cb2eba1e`'s; re-read before
  editing (a later records commit may have moved HEAD without touching these files -- `git log -1 -- <file>`).
* If a response of yours is stopped by the harness's safety classifier, STOP: report what was done and where, and do
  not re-issue the stopped content in any form.  Keep variant work in files; describe test variants only by the ids
  and answer-file lines used below; never paste their diffs into a reply.

## 1. Read first (all in this directory unless noted)
`PASS1_RULINGS.md` (the rulings), `CHECKS_mainloop.md` (settled facts), `packet.md` sections 7 (the 24 indices and
12 names -- the expectation table), 8.1 (the generator, whole), 8.7 (the make rule), 9.1-9.2 (the gate patterns),
`drafter_NOTES.md`.  Seat rows: `codex_t1p1.txt:146-164, 182-192`, `grok_t1p1.txt:91-116, 124`,
`ollama_glm_t1p1_Q12.txt:60-69`, `ollama_glm_t1p1_Q34.txt:19-26`.  Repo patterns: `regress/diff_autodev_gen.sh`
(whole; the generator-vs-inputs idiom), HEAD `regress/gate_offline.sh:47-72` (the `#375` reader) and `:1886-1900`
(the `#406` wiring), `regress/lib.sh` (`check`, `check_min`, `gate_skip`, `need_file`), `regress/run.sh` (how one gate is
run alone and where `LOGDIR` goes).

## 2. Baseline receipts on HEAD -- BEFORE any edit (D1; artifacts dir `regress/artifacts/m88kscaledbyte/table1_20261022/`)
1. `BASELINE.out`: HEAD sha; md5 of `src/cpus/generate_m88k_loadstore.c`, `src/cpus/tmp_m88k_loadstore.c`,
   `src/cpus/cpu_m88k_instr_loadstore.c` in GXEMUL-SEC, est/, build/, build-asan/, /tmp/gxsec-build (if present);
   the WSL `cc --version`.
2. In a WSL scratch dir (`/tmp/gxt1/base/`): copy the HEAD generator, compile it, run it to `fresh_HEAD.c`, and
   `cmp` against the committed table (CHECKS #6 -- the agreement at HEAD; if they differ, record the diff and
   STOP before step 5: the regenerated table must not carry unrelated churn).  Record NULL count (expect 296),
   entry count (512), `#define LS_N` count (198), and the generator's stderr `generated_functions`.
3. `PRETABLE.out` (D2), written before any table run: sibling parity (the other three NULL arms and the byte-endianness
   early-return idiom at `:101-102`/`:74-75`), claim -> row for every sentence the `#569` comment will assert, guard
   field vs body field for the deleted arm's predicate (`size == 0 && scaledness`, with the body-induced partitions
   of `size` and `scaledness` -- which pins hold which cell), and per row the leg it reds under and the observable
   (the symbol text at that index; the count; the compile status).

## 3. The detector (B1-B12) -- `regress/diff_m88k_loadstore_gen.sh` + a GATE 2 block
* POSIX `sh`, on `diff_autodev_gen.sh`'s skeleton: `WORK` scratch; copy the generator source into WORK; compile
  with `${CC:-cc}`; run to `$WORK/fresh.c`; capture stderr.  Env overrides `GEN=` (generator source path) and
  `TABLE=` (committed table path) defaulting to the repo files, so the legs in step 6 run WITHOUT mutating the repo.
* A reader parametrized by file and array (`m88k_loadstore`, 512): the `#375` awk with `\[512\]` and the file as an
  argument (CHECKS #2).  Rows (equality unless stated), each emitted once per artifact (fresh / committed):
  - the 24 absolute name pins (expected names from `packet.md` section 7, hard-coded in the driver, never read
    from the table);
  - accept pins 161, 177, 434, 438, 418, 422, 144, 400, 404 (B3) and the 24 counterparts at index-32;
  - exactly one 512-entry initializer; NULL count == 272; `#define LS_N` blocks == 198;
  - generator stderr `generated_functions` == 198 (fresh only);
  - fresh == committed byte-for-byte (`cmp`);
  - the generator COMPILED (an explicit red row on failure -- never `need_file`/`gate_skip`, B5); the committed table
    PRESENT and parseable (explicit red row);
  - a final `ROWS=<n> FAIL=<m>` line and a completion sentinel (`M88KLS_DONE`) so a killed run cannot read as green.
* The GATE 2 block, inserted in `regress/gate_offline.sh` directly after the `#375` block (after HEAD line 72, before
  the `b1w` comment), modelled on the `#406` block: driver executable; row failures == 0; rows run == the pinned
  total (EQUALITY, so a deleted row is red); the sentinel present.  Apply the SAME insertion to (a) the working-tree
  file and (b) a staged copy built from `git show HEAD:regress/gate_offline.sh`, saved as
  `table1_20261022/staged/gate_offline.sh`; `diff` the two insertions to prove they are identical.
* The driver's header carries the CONTRACT (B8, B11): the 24-cell output contract with Grok's 16-floor / 8-clause-(e)
  split; what it does not observe (handler bodies, the exchange itself -- the owner's witness record); `(c)` recorded
  as measured (step 6).

## 4. Pre-fix RED (clause (a)) -- run the finished driver on unmodified HEAD
`table1_20261022/prefix_HEAD.out`: expect exactly the 24 name pins red in BOTH artifacts, NULL count red (296), the
rest green; its mtime precedes every edit of step 5.  If it is not red for the reason under test, stop and report.

## 5. The fix (A1-A5), tag `#569`
1. `src/cpus/generate_m88k_loadstore.c`: delete the whole arm (`:254-257` at HEAD -- the `if`, its `printf("\tNULL")`,
   the `continue`, the brace) and put in its place a comment in the file's own style:
   `/* #569: scaled byte accesses take the unscaled byte handler (scale 1 is no scaling; print_function_name already
   omits "_scaled" for size 0), so no NULL arm: 24 table slots were NULL and cpu_m88k_instr.c's xmem path indexes
   them unguarded. */` -- adjust wording to the surrounding comment density; `:104-105` untouched; no other change.
2. Regenerate `src/cpus/tmp_m88k_loadstore.c` from the FIXED generator (compile and run in `/tmp/gxt1/fix/`, copy the
   stdout file over the repo's table).  Verify: `diff` against HEAD's table is EXACTLY 24 changed lines, each `NULL` ->
   the expected name; NULL count 272; 512 entries; LF endings preserved.
3. Run the driver on the fixed repo files: GREEN, `ROWS=<n> FAIL=0`, sentinel present -> `table1_20261022/fixed.out`.

## 6. The table (B6, B7, B3) -- legs run through the env overrides against copies in `/tmp/gxt1/legs/`, never in the repo
| leg | what | expected |
|---|---|---|
| L1 | GEN = HEAD's generator, TABLE = the fixed table | fresh-side name pins red; committed side green; `cmp` red |
| L2 | GEN = fixed generator, TABLE = HEAD's table | committed-side pins red; fresh green; `cmp` red |
| L3 | GEN = a comment-only generator source | the compile row red (clause (c), measured) |
| L4 | TABLE = a comment-only table | every committed-side row red (clause (c), measured) |
| L5 | the v2 variant as specified at `grok_t1p1.txt:76` / `codex_t1p1.txt:100` (first difference 416) | fresh-side pins red from 416; `cmp` red |
| L6 | the endianness narrowing named at `ollama_glm_t1p1_Q12.txt:52` (one endian half left as before the fix) | the 12 pins of that half red |
| L7 | the v6 form at `grok_t1p1.txt:80` / `codex_t1p1.txt:130` (`:80`'s compare moved by one) | the halfword pins 161/177 red; word pins green |
Each leg: `table1_20261022/L<n>_<tag>.out` (the driver's full output) and `L<n>.diff` (the variant vs the fixed source,
`diff -u`, a file only).  `SCORES.txt`: per leg `rows red / rows total`, the artifact name, and the one-line reason
the red is the reason under test.  A leg that is not red is a RESULT (mis-built / dead target / mis-cut row) -- record
which, do not re-aim it silently.

## 7. Propagation and the two-part clearance (D5)
Copy the fixed generator and the regenerated table to `est/src/cpus/`, `build/src/cpus/`, `build-asan/src/cpus/`,
`/tmp/gxsec-build/src/cpus/` (where the tree exists).  Rebuild each BUILD tree (`rm src/cpus/*.o; make` under WSL,
foreground, one at a time; the make rule regenerates the table in-tree -- afterwards `cmp` the tree's table against
GXEMUL-SEC's: it must be clean, which is the agreement row in a real build).  `CLEARANCE.out`: for each tree, the
`cmp` of both files against GXEMUL-SEC and `[ binary -nt source ]`; `est/: source tree, part 2 N/A`.

## 8. Gates (D5) -- alone, one at a time, after step 7
GATE 2 (`gate_offline.sh`) once, from `regress/run.sh`'s invocation form for a single gate, LOGDIR per its convention ->
green, the new block's rows green with its pinned total; GATE 11 (`gate_m88k_rounding.sh`) once on the rebuilt
`build/gxemul` -> green.  Preserve both logs' tails (with their completion lines) in `table1_20261022/`.

## 10. AMENDMENTS from GPT-6 Astra's adjudication of pass 1 (2026-10-23 ~09:55, `adj/codex_t1p1adj.txt` Q3) -- these
## override the sections they name; §5 (the repair) is unchanged.  Sent to the builder by message at ~10:00.
* §2: `PRETABLE.out` distinguishes the 24 generator-output cells (the FLOOR) from the 16 current guest-consumer cells;
  the halfword acceptance's warrant is R12 (adjacent modelled size), not D2.
* §3: the contract header states the floor as ALL 24 cells (16 = the current consumer subset; the 8 others are NOT
  coverage debt); an explicit RED row for unsuccessful generator EXECUTION (non-zero exit / empty stdout) beside the
  compile and missing-table rows; every row carries an identity string that occurs exactly once and the gate block pins
  each identity's presence (`== 1`) as well as the total and the sentinel; the row total is ENUMERATED in the driver
  header and in `SCORES.txt` (54 distinct name pins per artifact = 24 + 24 + 6, or 57 if the three overlapping accept /
  counterpart indices are emitted twice -- say which); the `#define LS_N == 198` and `generated_functions == 198` rows
  are described as a narrow suppression-count control, NOT a definition-integrity check (which is disclosed as outside
  the contract).
* §6: L5 is Grok's v2 at `grok_t1p1.txt:76` only (first difference 416; the `codex_t1p1.txt:100` variant first differs
  at 256 overall and is NOT L5); L7 keeps the halfword pins but is recorded as also producing duplicate definition NAMES
  that the driver does not compile -- the table token at 161 is its observable, not "silence"; L8 (all-NULL table) is
  SUPPLEMENTARY evidence with its own receipt, not a prerequisite of clause (c).
* §7: regeneration is dependency-driven -- after each rebuild `cmp` the tree's table against GXEMUL-SEC's and record
  whether the tree regenerated or kept the copied file.
* §9: the report carries the corrected classifications, every receipt by file, the actual row count, and C1/C2 as
  "filed outside T1" only.

## 9. Report -- `table1_20261022/BUILD_REPORT.md`, then STOP (pass 2 is the main loop's)
What was done in order; the diff stat (files, +/- lines) of the four changed/added repo files; every score with its
artifact; the clearance output; the gate results; anything that disagreed with this spec or with a seat ruling
(by id); open questions.  Dispositions and pointers only.
