# T2 (`ppcdsformxo`) -- the builder's spec, round `#571` (2026-10-24; DRAFT until section 10 carries the adjudication)

The builder is an Opus 5.5 measuring agent.  It reads this file and the files section 1 names, builds and measures in
scratch clones, writes its deliverables where this file says, and reports in `BUILD_REPORT.md`.  Pass 2 (the diff
review), the adjudication and the landing commit are the main loop's.

## 0. Ground rules (the brief is the only sandbox)
* Project root `C:\DocumentNoSnc\cc\GXEMUL`; the repo and the only tree under edit: `GXEMUL-SEC/` (git root).  The
  tree under review is `GXEMUL-SEC/src/`; `./src/`, `_archive/**/src/` and `GXEMUL_upstream_2021/` are pristine 2021
  upstream -- never read them for facts.  `est/` is the untracked twin (shared files byte-identical); `build/` (pmax),
  `build-asan/` and WSL `/tmp/gxsec-build` are NO-VPATH build trees.
* Git: object reads only (`git show`, `git log`, `git ls-files`).  Never `git add/commit/status/diff/stash/checkout/
  restore` -- another process may hold the index.  Nothing under `tools/` is edited EXCEPT the two MANIFEST lines in
  `tools/pipeline/check_probe_wiring.py` (B12) -- that file carries uncommitted peer edits: read it at HEAD
  (`git show HEAD:tools/pipeline/check_probe_wiring.py`), make your two-line insertion in BOTH the working-tree file and
  a staged copy built from the HEAD blob (`table1_20261024/staged/check_probe_wiring.py.txt`), and `diff` the two
  insertions.  The peer's files are never touched: `src/cpus/cpu_alpha_palcode.c`, `src/devices/dev_lca.c`,
  `src/devices/dev_pcc2.c`, `src/devices/dev_sh4.c`, `src/include/thirdparty/mvme_pcctworeg.h`,
  `regress/sh4_chcr_probe.py`, `regress/gate_sh_rounding.sh`, `regress/gdrom_default_probe.py`,
  `regress/diff_wdc_identify.c`, `regress/wdc_addtoinbuf_probe.py`, `regress/gate_offline.sh`,
  `regress/artifacts/recordfix_20261002/chk_hrec.py.txt`, everything else under `tools/`.
* Builds and gate runs happen under `wsl -d Gentoo` (the default distro has no `make`): invoke scripts as
  `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/...`; write helper scripts to the session scratchpad
  (`C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\t2\build\`),
  never to git-bash `/tmp`.  `rm src/cpus/*.o` before a build tree's `make`; freshness is `[ binary -nt source ]`, never
  the make rc.  FOREGROUND ONLY: no plain `&`, no `nohup`; one job at a time; never two gate invocations at once; no
  gate while a panel seat runs (ask the main loop if unsure -- it will tell you when the panel is idle).  Never `rm -rf`
  outside your own scratch dirs.  The witness's clone `/tmp/gxt2/base` (HEAD c8fcb5ff source == add098b9 source, binary
  md5 `3cd0501cf7c854e0662797ccee1fce64`, made as `..\witness_20261024\receipts\build_base.out` records: `build/` copied
  with the peer's dirty files replaced by their HEAD blobs) is the BASE tree -- never edited; make the WORK tree as
  `/tmp/gxt2/work` by `cp -a /tmp/gxt2/base /tmp/gxt2/work`, and name the baseline (HEAD `add098b9`;
  `src/cpus/cpu_ppc_instr.c` `cmp` clean against GXEMUL-SEC before mutant 1).  Kill-table legs run in
  `/tmp/gxt2/legs/<leg>/` copies, never in the repo and never in `build/`; each leg's tree carries a clone-local
  `.MUTANT` sentinel while mutated and is restored by `cmp` against GXEMUL-SEC (never against the leg's own backup).
  Drivers run from a FROZEN copy (`cp driver.sh driver.run-<stamp>.sh`).
* Text hygiene: the probe and the gates are LF files; write with a tool that preserves LF (python `io.open(...,
  newline="")` both ways; `file -b` to check).  Line numbers below are HEAD `add098b9`'s; re-read before editing.
* If a response of yours is stopped by the harness's safety classifier, STOP: report what was done and where, and do
  not re-issue the stopped content in any form.  Keep variant work in files; describe variants only by the leg ids
  below; never paste their diffs into a reply; never list many variants in one reply.  Your replies are dispositions,
  scores and paths -- no code.

## 1. Read first (all in this directory unless noted)
`PASS1_RULINGS.md` (M1-M5, A, B, C, D, E), `adj/codex_t2p1adj.txt` and `adj/grok_t2p1adj.txt` (the adjudications;
section 10 below says what they changed), `packet.md` sections 2 (the witness, whole), 3 (the settled design),
5-7 (premises, partition), 8.2 (the D/DS-form arm whole, `cpu_ppc_instr.c:4268-4352`), 8.7-8.8 (the generic handler and
the generated table), 9 (gate 13's `#565` block and the MANIFEST lines), `drafter_NOTES.md`.  Seat rows:
`grok_t2p1.txt:62-139` (rows, legs, channels; the row list at :139), `codex_t2p1.txt:88-199` (the store observables table
at :92-98, the partials at :106-111, the variant table at :168-174), `argon_agy_t2p1.txt:83-96` (the store rows with
their values), `ollama_glm_t2p1_Q12.txt:9-19` (D-A..D-E), `ollama_glm_t2p1_Q34.txt:9-31`.  The witness:
`..\witness_20261024\ppc_dsform_probe.py` (the base of the detector; its `encode()`, `session()`, `row()`, scoring and
sentinel), `WITNESS_REPORT.md`, `receipts\`.  Repo patterns: `regress/ppc_rldicl_probe.py` (multi-session stepped probe
with a stop word last after a liveness `li`; `tempfile`; the disassembler cross-check), `regress/gate_ppc.sh:162-201`
(the `#565` block: `count "$LOG" "^$v  .*ok$"` loop, the literal pins, `|| true`), `regress/lib.sh` (`check`, `count`,
`gate_skip`, `need_file`), `regress/run.sh` (one gate alone; `LOGDIR`), `tools/pipeline/check_probe_wiring.py` at HEAD
(the MANIFEST; `#570`'s CLASS_DETECTOR and CLASS_WITNESS lines), `regress/artifacts/m88kbuserrregs/table1_20261023/`
(`PRETABLE.out`, `SCORES.txt`, `BUILD_REPORT.md`, `prefix_HEAD.out` -- the shapes to copy).

## 2. Baseline receipts -- BEFORE any edit (artifacts dir `regress/artifacts/ppcdsformxo/table1_20261024/`)
1. `BASELINE.out`: HEAD sha; md5 of `src/cpus/cpu_ppc_instr.c` in GXEMUL-SEC, est/, build/, build-asan/,
   /tmp/gxsec-build (if present), /tmp/gxt2/base, /tmp/gxt2/work; the WSL `cc --version`;
   `[ gxemul -nt src/cpus/cpu_ppc_instr.c ]` for every binary; the base binary's md5 re-checked.
2. `PRETABLE.out`, written BEFORE table 1 runs (its mtime proves the order): SIBLING PARITY (the five DS forms against
   each other -- which write RA, which sign-extend -- and the arm's D-form siblings `lwz`/`lwzu`/`lha`: the same flags
   reached by a different route); CLAIM -> ROW for every sentence the `#571` comment will assert; GUARD FIELD vs BODY
   FIELD with the body-induced partition per lvalue (`main_opcode` labels; `iword & 3`; `imm == 0`; `ra == 0 && update`;
   `fp`; `ra == 0`; EXHAUSTED / SAMPLED per lvalue); CHANNEL per row -- the mutant (leg id, section 6) it kills and the
   observable that differs -- for every row of section 3.  Diff this list against the brief's section 7 (26 cells) and
   PASS1_RULINGS.md B4-B7 and say what changed.

## 3. The detector (B1-B7, B11, B12) -- `regress/ppc_dsform_probe.py` + a GATE 13 block + two MANIFEST lines
* Copy `..\witness_20261024\ppc_dsform_probe.py` to `regress/ppc_dsform_probe.py` (the witness file itself stays
  byte-identical where it is; its `MANIFEST.md5` must still verify).  In the copy: banner "RUNG-3 DETECTOR for the
  64-bit DS-form loads and stores (opcodes 58 and 62, #571)"; `tempfile.mkdtemp(prefix="ppc_dsform_")` for the dummy
  boot file, removed in `finally:`; the CONTRACT per B11 (CLAIMED / NOT CLAIMED / the census sentence / the P15 rule
  / the two behaviour changes); SYMPTOM = the red-on-BASE rows of section 4; CONTROL = the controls.
* Every word placed by `encode()`, never a typed constant; the expected XO for the census from a label-keyed map
  (`ld` 0, `ldu` 1, `lwa` 2, `std` 0, `stdu` 1), the census expectation = the tree's CURRENT disassembler text
  (`ld`/`std` + the raw halfword), one `unasm census` row over every placed word of every session (unassemble before
  stepping, in each session), one `word pins` row pinning the three witness words to the literals `e894ff90`,
  `e8b5ffa1`, `e8d6000a`.
* Sessions (TEN), all `-E bareppc -M 64`, debugger-stepped, each with its own liveness `li` row:
  1. **loads**: seeds (sentinel regs), DATA counting pattern at 0x20000.. by `put b`; words: `ld` DS != 0 (C1),
     `ldu` DS != 0 RA != RT (C4), `ldu` DS = 0 (C5; a second base register), `lwa` DS != 0 at a word with bit 31 set (C8),
     `lwa` DS = 0 (C10), `lwz` +8 (kept), `lwz` +6 (C21: D & 3 != 0; expect 0x06070809 of the pattern), `li` last.
     Rows: `ld value`, `ld RA after`, `ldu value`, `ldu RA after`, `ldu ds0 value`, `lwa value`, `lwa RA after`,
     `lwa ds0 value`, `lwz value`, `lwz odd`, `live`.
  2. **stores**: a pre-seeded scratch window (counting pattern) at 0x21000..; each store's 8-byte source is EIGHT DISTINCT
     bytes absent from the pattern (built with `lis`/`ori`/`sldi`/`oris` -- D-form and opcode-30/31 words, none of them
     58/62); words: `std` DS != 0 (C13), `stdu` DS != 0 RA != RS (C15), `stdu` DS = 0 (C16, own base), `stdu rA,DS(rA)`
     RA = RS DS != 0 (C18), `stw` +6 (C22), `li` last.  Readback by the debugger's `dump` over EA-1 .. EA+11 per store.
     Rows: `std value`, `std RA after`, `stdu value`, `stdu neigh` (the flank bytes EA-1 and EA+8..EA+11 unchanged),
     `stdu RA after`, `stdu ds0 value`, `stdu alias val` (MEM(EA) = old RS), `stdu alias RA`, `stw odd`, `st live`.
  3.-9. **seven stop sessions**, each: seeds, a liveness `li`, then the word LAST: `xo58_3` (58/XO 3), `xo62_2`,
     `xo62_3`, `ldu ra0` (`ldu rT,DS(0)` DS != 0), `stdu ra0` (DS != 0), `ldu ra0z` (DS = 0), `stdu ra0z` (DS = 0).
     Rows per session: `<name> live` and `<name> bad` -- the `bad` row wants ALL of: the `UNIMPLEMENTED instruction`
     line present in the transcript (M1: it prints under `step`), RT still the sentinel (loads) / the pre-seeded
     window unchanged (stores; for the RA = 0 forms the window at the ABSOLUTE target EXTS(DS || XO), pre-seeded by
     `put b`), RA unchanged.  On BASE every `bad` row is RED (the word executes: the sentinel or the window changes and
     no stop line prints).
  10. **neg apparatus**: the bogus machine TYPE (`-E nosuchmachine`), the witness's `exit1/-0x1` row.
  Names: at most 15 characters, unique (the probe's asserts), `%-16s` column.  N is the final count (about 38);
  the gate pins N by LITERAL equality after the instrument is frozen -- never predict N into the gate before that.
* Scoring: `PPC_DSFORM_RESULT=<ok>/<N>`, `PPC_DSFORM_CONTROL=OK|FAIL`, `PPC_DSFORM_SYMPTOM=PRESENT n/m | ABSENT |
  MIXED`, `PPC_DSFORM_RED=<names>|none`, sentinel `PPC_DSFORM_PROBE_DONE` last; the probe exits non-zero on any red.
* GATE 13 block in `regress/gate_ppc.sh`, inserted directly AFTER the `#565` rldicl block (its last `check`, ~:201)
  and BEFORE `need_file "$IMAGES/netbsd401-macppc-GENERIC"` (:203), modelled on the `#565`/`#570` shape: the probe run
  with `|| true` into `$LOGDIR`; the sentinel present exactly once; the name list of ALL N rows held in the gate, each
  `count "$LOG" "^$v  .*ok$"` == 1; rows run == N and rows correct == N by LITERAL equality; red == 0;
  `PPC_DSFORM_CONTROL=OK` == 1; `PPC_DSFORM_SYMPTOM=ABSENT` == 1; `PPC_DSFORM_RED=none` == 1 (each prefix also counted
  exactly once).  No `check_min`.  Same insertion in the working-tree file and in a staged copy from
  `git show HEAD:regress/gate_ppc.sh` (`table1_20261024/staged/gate_ppc.sh.txt`); `diff` the two insertions.
* MANIFEST (B12): `CLASS_DETECTOR` line for `ppc_dsform_probe.py` (gate 13, N rows, the kill-table path),
  `CLASS_WITNESS` line for `artifacts/ppcdsformxo/witness_20261024/ppc_dsform_probe.py`; working tree + staged copy as in
  section 0.  Frozen copies and drivers under the artifacts dir are `*.py.txt` / `*.sh.txt`.

## 4. Pre-fix RED (clause (a)) -- the finished detector on the BASE binary (`/tmp/gxt2/base/gxemul`)
`table1_20261024/prefix_BASE.out`: expect RED on `ldu value`, `ldu RA after`, `ldu ds0 value`, `lwa value`,
`lwa ds0 value`, `stdu value`, `stdu neigh`, `stdu RA after`, `stdu ds0 value`, `stdu alias val`, `stdu alias RA`, and
the seven `* bad` rows (18 of N); every control green (`ld value`, `ld RA after`, `lwa RA after`, `lwz value`, `lwz odd`,
`std value`, `std RA after`, `stw odd`, every `live`, `unasm census`, `word pins`, `neg apparatus`); `CONTROL=OK`,
`SYMPTOM=PRESENT 18/18`; its mtime precedes every edit of step 5.  If any row is red or green for a reason other than
the one under test, stop and report.  This file is the STORE half's clause-(a) artifact (B1); the frozen witness stays
the LOAD half's.

## 5. The fix (A1-A4), tag `#571` -- ONE product file, byte-identical in GXEMUL-SEC and est/
`src/cpus/cpu_ppc_instr.c`, the D/DS-form arm (HEAD `:4293-4327`): inside the inner `switch (main_opcode)`, the two
cases become DS-form decodes -- `case PPC_HI6_LD:` re-assigns the shared `imm` to `(int16_t)(iword & ~3)` (so the table
index at `:4335` and `ic->arg[2]` at `:4351` both see the masked displacement, A2), sets `load = 1; size = 3`, and
dispatches on `iword & 3`: 0 nothing more (`ld`), 1 `update = 1` (`ldu`), 2 `size = 2; zero = 0` (`lwa`), 3 `goto bad`
(reserved; bare, no message, A3).  `case PPC_HI6_STD:` the same mask, `size = 3`, XO 0 nothing more (`std`), 1
`update = 1` (`stdu`), 2 and 3 `goto bad`.  Nothing else in the arm moves: the RA = 0 guard at `:4338-4342` now fires
for `ldu`/`stdu` with RA = 0 (A4, a behaviour change the comment names).  One `/* #571: ... */` comment in the file's
style naming the DS-form layout, the two behaviour changes and the 32-bit disclosure (A6: no width test; the same
source builds the MODE32 decoder, whose table has real doubleword handlers -- M2).  Build `/tmp/gxt2/work`
(`rm src/cpus/*.o; make`), `[ gxemul -nt src/cpus/cpu_ppc_instr.c ]`, zero new warnings; `cmp` the file against
GXEMUL-SEC.  Run the detector: GREEN, `RESULT=N/N`, `SYMPTOM=ABSENT`, `RED=none`, sentinel -> `table1_20261024/
fixed.out`.  Run the FROZEN witness probe (the untouched `witness_20261024` file) against the same binary ->
`fixed_witness8.out`: 8/8, `SYMPTOM=ABSENT` (B9's clause-(a) load half, same script).

## 6. The table (B8-B10) -- legs in `/tmp/gxt2/legs/<leg>/`, each a `cp -a` of the WORK tree, rebuilt per leg
| leg | what | expected |
|---|---|---|
| L1 | clause (a): the frozen witness post-fix (step 5) | 8/8 ABSENT |
| L2 | clause (a): the detector pre-fix (step 4) and post-fix (step 5) | 18 red of N; then N/N |
| L3 | clause (b): the arm reinstated verbatim from HEAD (both cases, the shared `imm`) | the 18 symptom rows red; controls green; nothing stops |
| L4a | clause (b) partial: the mask line reinstated (raw `imm`), both XO dispatches kept | `ldu value`, `lwa value`, `stdu value`, the DS=0 value rows, `stdu neigh` red; stop rows GREEN |
| L4b | clause (b) partial: the opcode-58 case reinstated, mask and opcode-62 case kept | `ldu RA after`, `lwa value`, `xo58_3 bad`, `ldu ra0*` red; `ldu value` GREEN (the address is still masked) |
| L4c | clause (b) partial: the opcode-62 case reinstated, mask and opcode-58 case kept | `stdu RA after`, `xo62_2 bad`, `xo62_3 bad`, `stdu ra0*` red; `stdu value` GREEN |
| L5 | clause (c): IDENTITY BODY for 58 and 62 (decode, set the no-op handler, write nothing, reserved XO retired) | predicted from the frozen detector source BEFORE the run and recorded beside the measurement; `CONTROL=FAIL`; record form `(c): measured at L5_identity.out` |
| L5b | clause (c): the binary absent | no sentinel (the gate's sentinel pin is what reds) |
| L6a/L6b | (d) mask kept, `update` dropped for 58/1 resp. 62/1 | `ldu RA after` + `ldu ra0*` bad resp. `stdu RA after` + `stdu ra0*` bad red |
| L7 | (d) `update` kept, raw `imm` kept (no mask) | every value/destination row of 58/1, 58/2, 62/1 red |
| L8a | (d) the XO-2 branch reverted to the XO-0 flags (8-byte load) | `lwa value`, `lwa ds0 value` red |
| L8b | (d) `lwa` with `zero` left 1 (zero-extension) | `lwa value` red (the sign-extended oracle) |
| L8c | (d) `lwa` `size` 3 with `zero` 0 (slot 11, `ppc_instr_invalid`) | HOST EXIT: the loads session dies, the sentinel is absent -- score as "host exit", not as a row count |
| L9 | growth: XO 0 treated as XO 1 (`update` on `ld`/`std`) | `ld RA after`, `std RA after` red |
| L10 | growth: `update = 1` for all five forms | `ld RA after`, `lwa RA after`, `std RA after` red |
| L11 | the mask applied at the SHARED assignment (every opcode of the arm) | `lwz odd`, `stw odd` red |
| L12a/L12b | the reserved test narrowed: 62 stops only on XO 2 (XO 3 stores) resp. 58's XO 3 not refused | `xo62_3 bad` resp. `xo58_3 bad` red |
Each leg: `table1_20261024/L<n>_<tag>.out` (the detector's full output), `L<n>.diff` (the variant vs the fixed source,
`diff -u`, a FILE only), and the leg tree restored (`cmp` clean against GXEMUL-SEC, sentinel removed, binary rebuilt or
the tree discarded).  `SCORES.txt`: per leg `rows red / N`, the artifact, the red rows by name, one line on why the red
is the reason under test.  A leg that is not red is a RESULT (mis-built / dead target / mis-cut row) -- record which;
never re-aim it silently.  Variants named NOT CLAIMED in the contract (RA = RT checks; a 32-bit width test; translation
on; indexed forms; the disassembler) are NOT built (clause (e), disclosed).

## 7. Propagation and the two-part clearance
Copy the fixed `src/cpus/cpu_ppc_instr.c` to `est/src/cpus/`, `build/src/cpus/`, `build-asan/src/cpus/`,
`/tmp/gxsec-build/src/cpus/` (where the tree exists).  Rebuild each BUILD tree (`rm src/cpus/*.o; make` under WSL,
foreground, one at a time).  `CLEARANCE.out`: per tree, `cmp` of the file against GXEMUL-SEC and
`[ binary -nt src/cpus/cpu_ppc_instr.c ]`; `est/: source tree, part 2 N/A`.  `build/` carries the peer's dirty files --
leave them exactly as they are.

## 8. Gates and measurements -- alone, one at a time, after step 7, with the panel idle
GATE 13 (`gate_ppc.sh`) once via `regress/run.sh`'s single-gate form -> green: the new block's N rows green with the
pinned total, the `#565` rldicl pin still 24, and the image-gated rounding probe (138 rows; `_images/
netbsd401-macppc-GENERIC` is present) green -- it is the one other consumer of the edited arm (its FP D-forms and `stw`).
Preserve every gate log's tail with its completion line.  No boot A/B is owed (no PowerPC guest image boots in this
tree's battery through opcodes 58/62 -- Argon's census, `argon_agy_t2p1.txt:217-225`); say so in the report.

## 9. Report -- `table1_20261024/BUILD_REPORT.md`, then STOP (pass 2 is the main loop's)
What was done in order; the diff stat (files, +/- lines) of the product file and the three harness files; N and the
row list; every score with its artifact (and the identity leg's prediction beside its measurement); the clearance
output; the gate result; anything that disagreed with this spec or with a ruling (by id); open questions in
`BUILDER_QUESTIONS.md` (written BEFORE the detector if a ruling is needed; the main loop answers in section 11).
Dispositions, scores and paths only.

## 10. AMENDMENTS from GPT-6 Astra's adjudication (`adj/codex_t2p1adj.txt`, VERDICT AMEND; PASS1_RULINGS.md section
## F1) -- these OVERRIDE the sections they name.  (Grok's adjudication is appended as section 10b when it lands; if it
## lands after you start, the main loop sends you its deltas by message -- do not stop for it.)
1. **Edit sites (overrides §5, §6 L3/L4).**  The repair lives in the TWO CASE BODIES (`case PPC_HI6_LD:` and
   `case PPC_HI6_STD:` of the inner switch); each carries its own mask; the shared `imm = (int16_t)iword;` at `:4295`
   is NOT edited.  Clause (b) legs: **L3** = both cases reinstated verbatim from HEAD (`load=1; size=3; break;` and
   `size=3; break;`); **L4b** = only the 58 case reinstated verbatim (its mask goes with it), the 62 case repaired;
   **L4c** = only the 62 case reinstated, the 58 case repaired; **L4a** is a SEMANTIC PARTIAL, not a reinstatement:
   both cases keep their XO dispatch but drop their mask (raw `imm`) -- name it so in `SCORES.txt`.  Record the
   actual edited lines in `BUILD_REPORT.md` (the site inventory), and if for any reason you edit the shared assignment
   instead, STOP and report: the D-form label analysis (B7) must be redone first.
2. **Eight more rows (overrides §3 and §4).**  Legal-access cells the floor owes, value/destination channel, no new
   session: loads session adds `ld ds0 value` (`ld` DS = 0 from a second base), `ld ra0 value` (`ld rT,D(0)`: absolute
   EA = EXTS(DS||00) -- seed a counting window at 0x7000.. with `put b`; D = 0x7000), `ld both val` (`ld rT,0(0)`:
   address 0 -- seed 0x0..0xf), `lwa ra0 value` (`lwa rT,0x7004(0)`, a word with bit 31 set in the seeded window),
   `lwa ra0z value` (`lwa rT,0(0)`); stores session adds `std ds0 value` (own base), `std ra0 value` (`std rS,0x7100(0)`,
   dumped), `std both val` (`std rS,0(0)`, address 0 dumped -- place it so no other row's window overlaps).  Each new
   row's expected value names its seeded offset; its RA-unchanged observation is an ungraded `obs()` (RA = 0 cannot carry
   an RA row).  The §4 pre-fix expectation gains nothing red from these eight (XO 0 is correct on BASE) -- they are
   controls; SYMPTOM stays 18 rows.  N is now about 46 -- the literal comes from the frozen instrument.
3. **Leg table corrections (overrides §6).**  **L7** (raw `imm`, XO dispatch kept = L4a; one leg, not two): red =
   the 58/1, 58/2, 62/1 value/destination rows and the DS = 0 value rows; XO-0 rows and the D-form controls GREEN.
   **L8c** (`lwa` `size` 3 with `zero` 0): the EMULATOR terminates (`ppc_instr_invalid`, `cpu_ppc_instr.c:241`); the
   detector CONTINUES -- it records the return, supplies missing registers as -1, emits that session's rows red and
   prints the sentinel -- so expected = "loads session rows red, CONTROL=FAIL, sentinel PRESENT"; never score it as a
   wrong-width transfer and never predict a missing sentinel.  **L9** is split: **L9a** "XO 0 decoded as XO 1"
   (transfer kept, RA written) -> `ld RA after`, `std RA after` red; **L9b** "EA + 1 on XO 0" (an extra +1 in the
   displacement of the XO-0 forms) -> `ld value`, `std value` (+ `std neigh` if rowed) red, RA rows green.
4. **Predictions are written per leg BEFORE the leg runs**, derived from the FROZEN detector source (a `PREDICTIONS.txt`
   line per leg: rows expected red, by name, with the channel).  The identity leg's prediction comes from the grown
   detector, never the witness's 4/8.  `SCORES.txt` records prediction beside measurement and names every miss.
5. **Freeze before the BASE run (overrides §4 order).**  The detector's row list and oracles are frozen (md5 of
   `regress/ppc_dsform_probe.py` in `BASELINE.out`) BEFORE `prefix_BASE.out`; the post-fix run uses that same file; any
   later edit to the probe re-runs both.
6. **Gate pins (overrides §3's pin list).**  For each protocol key `PPC_DSFORM_RESULT=`, `PPC_DSFORM_CONTROL=`,
   `PPC_DSFORM_SYMPTOM=`, `PPC_DSFORM_RED=`: count every line starting with the key (== 1), THEN the well-formed /
   accepted form (`RESULT=N/N` literal, `CONTROL=OK`, `SYMPTOM=ABSENT`, `RED=none`, each == 1) -- the `gate_ppc.sh:140`
   idiom; `PPC_DSFORM_PROBE_DONE` exactly once and last; every row name once and green; rows emitted / green / red by
   literal; the census row covers the frozen placed-word set.  MANIFEST entries are needed as soon as the files are
   STAGED (the checker's domain is tracked-or-staged `.py`), so write them with the detector, not after.
7. **Comment and record wording.**  The `#571` comment must NOT say that pre-`goto bad` `fatal()` sites mark only
   unimplemented features (false: the RA = 0 guard diagnoses an invalid form).  The 32-bit disclosure says: 58/62 are
   illegal on 32-bit implementations; before and after this fix a 32-bit CPU decodes them through the same arm; the
   MODE32 table has real doubleword handlers (`tmp_ppc_loadstore.c:1923+`); after the fix the legal forms select those
   handlers and reserved XO / RA = 0 updates stop there too; no width test this round.  The C4 census in the report
   says "at least fourteen" (with `cmpd`/`cmpld`) and notes `extsw`'s MODE32 handler diagnoses and returns.
8. **Names.**  Every `live` and `bad` row carries its session prefix (`xo58_3 live`, `xo58_3 bad`, ... `stdu ra0z live`
   is 14 characters); `live` and `bad` alone would collide with the probe's uniqueness assert.  The negative-apparatus
   session has no guest liveness row by design.

## 10b. AMENDMENTS from Grok 4.7's adjudication (`adj/grok_t2p1adj.txt`, VERDICT AMEND; PASS1_RULINGS.md section F2)
## -- these OVERRIDE sections 3, 4, 6 and 10 where they conflict.
1. **Sessions: EIGHT, not ten (overrides §3 and §10 item 2's count).**  The stop sessions are FIVE: `xo58_3`, `xo62_2`,
   `xo62_3`, `ldu ra0` (DS != 0), `stdu ra0` (DS != 0).  The DS = 0 RA = 0 update cells (`ldu ra0z`, `stdu ra0z`) are
   NOT built; the contract discloses them under NOT CLAIMED with the sentence "the only observer of an update conditioned
   on a non-zero displacement".  The RA = 0 stop sessions pre-seed and dump the window at the ABSOLUTE target
   EXTS(DS || 01) (DS = 0x10 -> bytes 0x11..0x18 on BASE).
2. **The eight legal-access rows of §10 item 2 become FIVE**: keep `ld ds0 value`, `ld ra0 value`, `lwa ra0 value`,
   `std ds0 value`, `std ra0 value`; do NOT build `ld both val`, `std both val`, `lwa ra0z value` (disclosed joints).
   N is about 39 (loads 14, stores 12, stops 10, global 3); the literal follows the frozen instrument.
3. **Names are capped at 14 characters (overrides §3's 15).**  Change the promoted probe's assert to `len(name) <= 14`
   with a comment that the gate pin `^name  ` needs two spaces after the name inside the `%-16s` column; keep `%-16s`.
   Every name in §3/§10/§10b is 14 or shorter -- check them all in the probe's own assert, not by eye.
4. **L8c scoring**: by the session's `how=exit1` on the REAL machine plus the transcript line
   `PPC: invalid(): INTERNAL ERROR`, the loads session's rows red, `CONTROL=FAIL`, sentinel PRESENT.  It is a kill-table
   leg, not part of the gate's N.
5. **Record wording**: the DS = 0 value rows are rowed for the ADDRESS channel -- never write that they prove which table
   half ran; the rounding-probe re-run is recorded as "collateral: the D-form consumers still execute", never as low-bit
   coverage (its displacements are all multiples of 4; C21/C22 are that control); C5's sentence: the translation-off
   failure path exists and is gated by `-T` (`halt_on_nonexistant_memaccess`), which the probe does not pass.
6. **A3 comment citations**: name `:4340` (the RA = 0 guard) and `:4604` (the `rld*` width guard) as the tree's
   `fatal`-then-`goto bad` sites; do not cite `:4815` or `:4997`.
