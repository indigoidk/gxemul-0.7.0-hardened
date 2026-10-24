# T36 (`m88kbuserrregs`) -- the builder's spec, round `#570` (2026-10-23; DRAFT pending section E of PASS1_RULINGS.md)

Everything here is a pointer into `PASS1_RULINGS.md` (A1-A11, B1-B14, C1-C5) and `CHECKS_mainloop.md` (#1-#10) in
this directory, with the concrete steps and the order the carrier requires.  Record OUTPUT, never assertion.  Section
10 (amendments from GPT-6 Astra's adjudication) overrides whatever it names.

## 0. Ground rules (the brief is the only sandbox)
* Project root `C:\DocumentNoSnc\cc\GXEMUL`; the repo and the only tree under edit: `GXEMUL-SEC/` (git root).  The
  tree under review is `GXEMUL-SEC/src/`; `./src/`, `_archive/**/src/` and `GXEMUL_upstream_2021/` are pristine 2021
  upstream -- never read them for facts.  `est/` is the untracked twin (shared files byte-identical); `build/` (pmax),
  `build-asan/` and WSL `/tmp/gxsec-build` are NO-VPATH build trees.
* Git: object reads only (`git show`, `git log`, `git ls-files`).  Never `git add/commit/status/diff/stash/checkout/
  restore` -- another process may hold the index.  Nothing under `tools/` is edited EXCEPT the two MANIFEST lines in
  `tools/pipeline/check_probe_wiring.py` (B11) -- that file carries uncommitted peer edits: read it at HEAD
  (`git show HEAD:tools/pipeline/check_probe_wiring.py`), make your two-line insertion in BOTH the working-tree file and
  a staged copy built from the HEAD blob (`table1_20261023/staged/check_probe_wiring.py`), and `diff` the two insertions.
  The peer's files are never touched: `src/cpus/cpu_alpha_palcode.c`, `src/devices/dev_lca.c`, `src/devices/dev_pcc2.c`,
  `src/devices/dev_sh4.c`, `src/include/thirdparty/mvme_pcctworeg.h`, `regress/sh4_chcr_probe.py`,
  `regress/gate_sh_rounding.sh`, `regress/gdrom_default_probe.py`, `regress/diff_wdc_identify.c`, `tools/adjudicate.sh`.
  `regress/gate_offline.sh` is NOT edited this round (the gate home is gate 14).
* Builds and gate runs happen under `wsl -d Gentoo` (the default distro has no `make`): invoke scripts as
  `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/...`; write helper scripts to the session scratchpad
  (`C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\t36\build\`),
  never to git-bash `/tmp`.  `rm src/cpus/*.o` before a build tree's `make`; freshness is `[ binary -nt source ]`, never
  the make rc.  FOREGROUND ONLY: no plain `&`, no `nohup`; one job at a time; never two gate invocations at once; no
  gate while a panel seat runs (ask the main loop if unsure -- it will tell you when the panel is idle).  Never `rm -rf`
  outside your own scratch dirs.  The witness's clone `/tmp/gxt36/base` (HEAD binary, md5 `2efeec55...`) is the BASE
  tree; make the WORK tree as `/tmp/gxt36/work` by `cp -a` of `build/` with the peer's five dirty files replaced by
  their HEAD blobs exactly as the witness did (`..\witness_20261023\build_base.sh.txt`, `headblobs_MD5.txt`), and name
  the baseline (HEAD `7fca7187`; the four product files `cmp` clean against GXEMUL-SEC before mutant 1).  Kill-table
  legs run in `/tmp/gxt36/legs/<leg>/` copies, never in the repo and never in `build/`; each leg's tree carries a
  clone-local `.MUTANT` sentinel while mutated and is restored by `cmp` against GXEMUL-SEC (never against the leg's own
  backup).  Drivers run from a FROZEN copy (`cp driver.sh driver.run-<stamp>.sh`).
* Text hygiene: the probe and the gates are LF files; write with a tool that preserves LF (python `io.open(...,
  newline="")` both ways; `file -b` to check).  Line numbers below are HEAD `7fca7187`'s; re-read before editing.
* If a response of yours is stopped by the harness's safety classifier, STOP: report what was done and where, and do
  not re-issue the stopped content in any form.  Keep variant work in files; describe variants only by the ids and
  answer-file lines used below; never paste their diffs into a reply.  Your report is dispositions, scores and paths.

## 1. Read first (all in this directory unless noted)
`PASS1_RULINGS.md` (A, B, C and E), `CHECKS_mainloop.md`, `packet.md` sections 2 (the witness, whole), 3.4 (the
upstream hunks: the arm and the `cpu_m88k.c` include), 7 (the partition), 8.1-8.3 (the three edit regions whole, line
numbers at HEAD), 9 (gate-14 / `#568` patterns, the MANIFEST lines), `drafter_NOTES.md`.  Seat rows: `grok_t36p1.txt:
30-34` (the include and its order), `:98-111` (variant -> row), `:137-147` (header edits, gate form); `codex_t36p1.txt:
15, 54-62, 112-118, 153-155`; `ollama_glm_t36p1_Q34.txt:10, 16, 30`; `ollama_glm_t36p1_Q12.txt:46`.  Repo patterns:
`regress/vme_default_probe.py` (the session shape the witness copied), `regress/gate_arm.sh` (gate 14: the skip chain
after `arm_flags_probe.py`, `#568`'s block -- the `count "$LOG" "^$v  .*ok$"` loop and its pins), `regress/lib.sh`
(`check`, `count`, `gate_skip`, `need_file`), `regress/run.sh` (one gate alone; `LOGDIR`), `tools/pipeline/
check_probe_wiring.py` at HEAD (the MANIFEST; `#568`'s CLASS_DETECTOR and CLASS_WITNESS lines), `regress/gate_ab.sh:214`
(the luna boot-to-`login:` check shape), `regress/gate_m88k_rounding.sh:32-39` (gate 11's image/boot `need_file`s).

## 2. Baseline receipts -- BEFORE any edit (artifacts dir `regress/artifacts/m88kbuserrregs/table1_20261023/`)
1. `BASELINE.out`: HEAD sha; md5 of `src/cpus/memory_rw.c`, `src/cpus/cpu_m88k.c`, `src/devices/dev_luna88k.c`,
   `src/devices/dev_m8820x.c` in GXEMUL-SEC, est/, build/, build-asan/, /tmp/gxsec-build (if present), /tmp/gxt36/work;
   the WSL `cc --version`; `[ gxemul -nt src/cpus/memory_rw.c ]` for every binary.
2. `PRETABLE.out`, written BEFORE table 1 runs (its mtime proves the order): SIBLING PARITY (the MEM_M88K arm against
   the neighbouring arch arms of the same device-failure block -- which write fault metadata, which do not); CLAIM ->
   ROW for every sentence the `#570` comments will assert (the `memory_rw.c` writes, the `dev_luna88k.c` case, the
   `dev_m8820x.c` comment corrections); GUARD FIELD vs BODY FIELD with the body-induced partition per lvalue (B9's
   corrected partition: `res`, `no_exceptions`, `cache`, the `cmmu[]` pointer, `orig_paddr`, `writeflag` for `debug()`
   only; the device-range / translation / running-transition conditions that dominate the arm; EXHAUSTED / SAMPLED per
   lvalue); CHANNEL per row -- the mutant it kills and the observable that differs (B6: grok:98-111 with codex:112-118's
   corrections), for the 24 witness rows AND the 7 new rows of step 3.  Diff this list against the brief's section 7 and
   say what changed.

## 3. The detector (B1, B5, B10, B11) -- `regress/m88k_buserr_probe.py` + a GATE 14 block + two MANIFEST lines
* Copy `..\witness_20261023\m88k_buserr_probe.py` to `regress/m88k_buserr_probe.py` (the witness file itself stays
  byte-identical where it is; its `MANIFEST.md5` must still verify).  Header edits (B1): the `no_exceptions` sentence's
  reason (B5b), the VA != PA sentence (B5's P7 reason), the FOUR-file edit set, the claim limit (A8), `icmmu` wants
  `kept`, the variant table marked as predictions until the legs run, the instruction cell's outcome (B5a), the (c)
  record line left as "measured at <artifact>" to be filled from step 6.
* New rows, each emitted exactly once with a name of at most 15 characters in the `%-16s` format:
  - `ifetch route`, `ifetch pfsr`, `ifetch pfar`, `ifetch dcmmu` (B5a): the witness's `INFO ifetch` observation scored
    (mvme187 `unreadable` window; stepped; wants v2 / SXIP 0xfff46013, iPFSR 0x00030000, iPFAR 0xfff46010, data seeds
    kept); the row comments name the R2 dependency and the re-root obligation.
  - `dbg noexc` (B5b): in the mvme187 session after the seeds, a debugger `dump` (or the probe's existing debugger-read
    idiom) of the `unreadable` window; wants: zeros returned, four seeds unchanged, no vector taken, cpu running.
  - `null surv`, `null route` (B5c): a SEPARATE mvme187 `-n 2` session.  Design constraints: both cpus start at one pc
    (`emul.c:742-745`), so the program begins with a RAM-flag dispatcher (cpu 0 runs alone until `pause 1`, sets the
    flag, takes the seeded refused-load path and its handler; after `pause 1` + `continue`, cpu 1 sees the flag, sets its
    OWN VBR, performs the refused load from the `unreadable` window, its handler stores a HANDLED marker to RAM, and the
    instruction after the load stores a FELL marker); cpu 1 NEVER accesses the CMMU register window (`dev_m8820x.c:108`
    dereferences the accessing cpu's NULL cmmu -- C5); the session ends on a breakpoint both paths reach or by the
    probe's existing end-of-session idiom; the debugger reads the two markers from RAM.  Wants: `null surv` = the
    session alive to its end (exit status, sentinel of the transcript), `null route` = HANDLED set, FELL clear.  If a
    `pause`-started cpu does not execute (CHECKS #2's refuter), record the session as NOT BUILDABLE with the transcript
    and STOP -- the main loop re-rules B5c; do not substitute a different machine or a device_add.
* Scoring: `RESULT=<ok>/<N>` with N the final count (31 if all seven land), `M88K_BUSERR_CONTROL=OK|FAIL`,
  `M88K_BUSERR_SYMPTOM=PRESENT n/m | ABSENT | MIXED`, `M88K_BUSERR_RED=<names>`, sentinel `M88K_BUSERR_PROBE_DONE`;
  the probe exits non-zero on any red.
* GATE 14 block in `regress/gate_arm.sh`, inserted directly AFTER `#568`'s block (so after `arm_flags_probe.py`'s skip
  chain, B10), modelled on `#568`'s: the probe run with `|| true` into `$LOGDIR`; the sentinel present (== 1); the name
  list of ALL N rows held in the gate, each `count "$LOG" "^$v  .*ok$"` == 1; rows run == N and rows correct == N by
  LITERAL equality; red == 0; `M88K_BUSERR_CONTROL=OK` == 1; `M88K_BUSERR_SYMPTOM=ABSENT` == 1.  No `check_min`.  Same
  insertion in the working-tree file and in a staged copy from `git show HEAD:regress/gate_arm.sh`
  (`table1_20261023/staged/gate_arm.sh`); `diff` the two insertions.
* MANIFEST (B11): `CLASS_DETECTOR` line for `regress/m88k_buserr_probe.py` (gate 14, N rows), `CLASS_WITNESS` line for
  `artifacts/m88kbuserrregs/witness_20261023/m88k_buserr_probe.py`; working tree + staged copy as in section 0.

## 4. Pre-fix RED (clause (a)) -- the finished detector on the HEAD binary (`/tmp/gxt36/base/gxemul`)
`table1_20261023/prefix_HEAD.out`: expect the witness's eight reds plus `ifetch pfsr` and `ifetch pfar` red (10 of N),
`null *` and `dbg noexc` GREEN (HEAD has no writes to misfire and delivers the exception), controls green; its mtime
precedes every edit of step 5.  If it is not red for the reason under test, stop and report.

## 5. The fix (A1-A7), tag `#570` -- four product files, byte-identical in GXEMUL-SEC and est/
1. `src/cpus/cpu_m88k.c`: `#include "thirdparty/m8820x.h"` directly after `#include "thirdparty/m8820x_pte.h"` (`:53`),
   with a one-line `/* #570: ... */` comment (A6).
2. `src/cpus/memory_rw.c`, the MEM_M88K device-failure arm (section 8.1; HEAD `:603-624`): replace the TODO comment
   (`:615-619`) with the upstream-shaped writes -- select `cpu->cd.m88k.cmmu[cache == CACHE_INSTRUCTION ? 0 : 1]`; if
   non-NULL, `reg[CMMU_PFSR] = CMMU_PFSR_BERROR << 16` and `reg[CMMU_PFAR] = (uint32_t) orig_paddr`; nothing else moves
   (A3, A4).  `/* #570: */` tag in the file's style.
3. `src/devices/dev_luna88k.c:624-627`: the case body becomes `return 0;` (the PFSR store deleted; the case and its
   comment kept, the comment amended to say the access now faults through `memory_rw.c`'s arm) (A5).
4. `src/devices/dev_m8820x.c`: comment-only corrections at `:293-294`, `:325-327`, `:453`, `:500-501` (A7).
5. Build `/tmp/gxt36/work` (`rm src/cpus/*.o; make`), `[ gxemul -nt src/cpus/memory_rw.c ]`, zero new warnings
   (`-Wall -Wextra -Wshadow`); `cmp` the four files against GXEMUL-SEC.  Run the detector: GREEN, `RESULT=N/N`,
   `SYMPTOM=ABSENT`, sentinel -> `table1_20261023/fixed.out`.  Run the FROZEN witness probe (the untouched
   `witness_20261023` file) against the same binary -> `fixed_witness24.out`: 24/24, `SYMPTOM=ABSENT` (B2).

## 6. The table (B2-B6) -- legs in `/tmp/gxt36/legs/<leg>/`, each a `cp -a` of the WORK tree, rebuilt per leg
| leg | what | expected |
|---|---|---|
| L1 | clause (a): the frozen witness post-fix (step 5.5) | 24/24 ABSENT |
| L2 | clause (a): the final detector pre-fix (step 4) and post-fix (step 5.5) | 10 red of N; then N/N |
| L3 | clause (b): the ARM reinstated verbatim from HEAD, the LUNA case fixed | witness rows: uld/ust/vme pfsr+pfar, `luna pfsr`, `luna pfar` red; `luna route` green; plus `ifetch pfsr/pfar` red |
| L4 | clause (b): the LUNA case reinstated verbatim from HEAD, the arm fixed | `luna route`, `luna pfar` red; `luna pfsr` green |
| L5 | clause (c): an exit-1 non-emulator stub in the binary's place | predicted 1/N, `CONTROL=FAIL`, sentinel printed, exit 1 -- RECORD THE MEASURED NUMBER |
| L5b | clause (c): the binary absent | no sentinel (the gate's sentinel pin is what reds) |
| L6 | (d) the ADDED selector weakened to always-data (`grok_t36p1.txt:100`'s cell, inverted) | `ifetch pfsr`, `ifetch pfar` red |
| L7 | (d) the `!no_exceptions` conjunct dropped from the guard | `dbg noexc` red |
| L8 | (d) the ADDED NULL check removed | `null surv` red (the session dies) |
| L9 | (d) the exception moved inside the NULL check | `null route` red (FELL set) |
| L10-L19 | the named variants at `grok_t36p1.txt:98-111`, one leg each: raw 3; device-relative `paddr`; PFSR-only; both CMMUs; sibling cleared; direction-conditioned; device-keyed; exception dropped; writes outside `res <= 0`; `res <= 1` | the row(s) that table names, each red; nothing else red |
| L20 | the LUNA case left returning 1 (its write kept) | `luna route`, `luna pfar` red |
| L21 | the LUNA write deleted, the case still returning 1 | `luna route`, `luna pfsr`, `luna pfar` red |
Each leg: `table1_20261023/L<n>_<tag>.out` (the detector's full output), `L<n>.diff` (the variant vs the fixed source,
`diff -u`, a FILE only), and the leg tree restored (`cmp` clean against GXEMUL-SEC, sentinel removed, binary rebuilt or
the tree discarded).  `SCORES.txt`: per leg `rows red / N`, the artifact, the red rows by name, one line on why the red
is the reason under test.  A leg that is not red is a RESULT (mis-built / dead target / mis-cut row) -- record which;
never re-aim it silently.  The variants named NOT CLAIMED in the contract (PFAR := `vaddr`; a sub-word PFAR) are NOT
built (clause (e), disclosed).

## 7. Propagation and the two-part clearance
Copy the four fixed files to `est/src/...`, `build/src/...`, `build-asan/src/...`, `/tmp/gxsec-build/src/...` (where
the tree exists).  Rebuild each BUILD tree (`rm src/cpus/*.o; make` under WSL, foreground, one at a time).
`CLEARANCE.out`: per tree, `cmp` of the four files against GXEMUL-SEC and `[ binary -nt src/cpus/memory_rw.c ]`;
`est/: source tree, part 2 N/A`.  `build/` carries the peer's five dirty files -- leave them exactly as they are.

## 8. Gates and measurements -- alone, one at a time, after step 7, with the panel idle
GATE 14 (`gate_arm.sh`) once via `regress/run.sh`'s single-gate form -> green, the new block's N rows green with the
pinned total; GATE 11 (`gate_m88k_rounding.sh`) once (the luna rig image is present) -> green (B13); the `#568` pin
measured 38/38 inside gate 14's log; `grep -rn 3ffffff0 regress/*.py regress/*.sh` (committed probes touching the LUNA
address -- report the hits).  A11: the luna rig boot A/B -- boot the rig image to `login:` once with
`/tmp/gxt36/base/gxemul` and once with the rebuilt `build/gxemul`, in `gate_ab.sh:214`'s shape; preserve both
transcripts in `table1_20261023/boot_ab/`; if the post-fix boot does not reach `login:`, STOP and report.  Preserve every
gate log's tail with its completion line.

## 9. Report -- `table1_20261023/BUILD_REPORT.md`, then STOP (pass 2 is the main loop's)
What was done in order; the diff stat (files, +/- lines) of the four product files and the three harness files;
N and the row list; every score with its artifact; the clearance output; the gate results and the boot A/B; anything
that disagreed with this spec or with a ruling (by id); open questions.  Dispositions, scores and paths only.

## 10. AMENDMENTS from GPT-6 Astra's adjudication of pass 1 (`adj/codex_t36p1adj.txt`, VERDICT AMEND; PASS1_RULINGS.md
## section E) -- these OVERRIDE the sections they name; §5 (the repair) is unchanged except §5.1's rationale.
* **§0 / §3 (`null` session): the C5 prohibition is WITHDRAWN** -- `m8820x_command()` receives the OWNING cpu
  (`dev_m8820x.c:250`, `:284`); cpu 1 MAY read CMMU registers (it has none of its own to read, so there is nothing for it
  to observe there -- keep cpu 0's seeded state isolated from cpu 1's writes instead).
* **§3 (`null surv` / `null route`): the session must close the INSTRUCTION x NULL joint cell conjunctively.**  cpu 1's
  path: set its own VBR; refused DATA load from the `unreadable` window (its handler stores HANDLED; the instruction after
  the load stores FELL); then JUMP INTO the `unreadable` window (an instruction-fetch refusal with `cmmu[0] == NULL`:
  vector 2, then the dyntrans tail halts cpu 1 and the debugger prompt returns).  cpu 0 parks in a self-loop after its
  own handler so no machine-wide breakpoint ends the session before cpu 1 is done (`cpu_dyntrans.c:1802-1804`).  The
  markers are zero-initialised by the probe, written only by cpu 1's path, and read after the session completes under
  either outcome.  `null surv` = the transcript reaches the post-ifetch prompt with both markers readable; `null route` =
  HANDLED set, FELL clear.  If cpu 1 does not execute at all after `pause 1`, record NOT BUILDABLE and stop (CHECKS #2).
* **§3 (`ifetch route`): a CONTROL, not the selector's row** -- the vector expression (`memory_rw.c:620-622`) reads
  `cache` independently of the added selector.  Its named variant is "exception dropped / mis-routed" (L17).  `ifetch
  pfsr` and `ifetch pfar` carry L6.  Say so in the header's CHANNEL column.
* **§3 (header / scoring): the disassembly census is RE-DERIVED for the new sessions** (the frozen `115/115` covers the
  five scored sessions; the instruction INFO is excluded at probe `:556, :572-576`); every newly scored session gets its
  prerequisite rows (`devsig` / `cmmu rt` or the equivalent) before its scored rows; the header DISCLOSES that gate 14's
  earlier `gate_skip`s (`gate_arm.sh:100-105`) can prevent the new block from running.
* **§2 PRETABLE**: enumerate the {data, instruction} x {present, absent} cross-product explicitly with the row(s) holding
  each cell; name WHICH body each field list enumerates (the outer refusal guard's -- `paddr` is read there by `debug()` --
  versus the inner NULL guard's); distinguish PFAR-VALUE corruption variants from guard-OPERAND swaps.
* **§5.1**: the include goes after `m8820x_pte.h` because that is upstream's placement (the transferred warrant); do not
  write "order matters" in the comment.  **§5.4**: `:453` does not say "only" -- correct the incomplete writer citation
  without quoting words that are not there.  Four product files; `dev_m8820x.c` is comment-only.
* **§6**: the clause-(b) predictions (16/24, 22/24) are for the FROZEN 24-row witness; run L3/L4 on BOTH instruments and
  record each score against its own denominator and instrument revision; FREEZE the detector copy before its table and
  name the revision in `SCORES.txt`.  **Add L8b**: the NULL check conditioned on the data label only (`#499`'s shape) ->
  `null surv` red (cpu 1's instruction fetch dereferences NULL); and L17 as `ifetch route`'s variant.
* **§8 ORDER**: run the A11 luna boot A/B right after §5 (the fixed WORK binary vs the BASE binary), BEFORE the table of
  §6 -- a failed boot stops the round before the expensive legs.  Then §6, §7, the gates.
* **§9**: the report ties every score to its instrument revision and denominator; C5 is reported as WITHDRAWN (not a
  finding); C4 as conditional on a nonzero bootstrap cpu, source-derived.

## 11. RULINGS on `table1_20261023/BUILDER_QUESTIONS.md` (main loop, 2026-10-23 ~22:35) -- all 22, by id; these bind
* **Q1 APPROVED: the STEPPED conjunctive form** (E5's shape): no `continue`, no pty, no breakpoint, no dispatcher; cpu 1
  set up by `focus 1` (pc, r5, markers, VBR); part 1 `step 3` (the data refusal), markers + `reg 1,0`; part 2 `step 5`
  (the instruction refusal), markers again.  The contract DISCLOSES that the instruction cell rides the R2 pre-read and
  that the NULL-check observable (L8/L8b) survives an R2 fix while the after-fault flow changes.  Free-running is NOT
  required (a `pty.fork` token could move a gate-6 pin; a wall-clock budget is a load-sensitive oracle).
* **Q2 ACCEPTED: the instruction refusal after the data fault is delivered as ERROR, vector 10** (PSR.SFRZ set by the
  data fault, `cpu_m88k.c:811-819`; E5 measured).  `null surv`'s want is independent of the vector; cpu 1 parks at
  VBR1+0x10 and VBR1+0x50.  Record the mechanism in the row comment and the CHANGELOG; do NOT add an `rte` (it would
  resume at SNIP and write a false FELL).
* **Q3 APPROVED: the debugger sets cpu 1's VBR** (`focus 1` + `VBR=`), no hand-assembled `stcr`.
* **Q4 APPROVED: (a)** -- cpu 0 keeps its seeded `uld` path (31 placed words), nothing scored from it, NO cpu-0
  prerequisite on the null rows (so L19 reds the null rows only through cpu 1's own prerequisites, if at all).
* **Q5 noted**: report C5 as WITHDRAWN with E3's measurement (CMMU-less cpu 1 read both IDR windows and issued an SCR
  command; exit 0).
* **Q6 APPROVED: a dedicated `dbg noexc` session cloned from `ok`** (E1's shape) -- hosting it in `ok` or `uld` would
  blur L7's channel.
* **Q7 APPROVED: prerequisites as `prereq_bad()`'s cause-free strings inside each scored row; N = 31.**
* **Q8 APPROVED: `ifetch route` is an ATTRIBUTION row in the CHANNEL column, not in `CONTROL_ROWS`.**
* **Q9 APPROVED: the unasm literal is 192** (115 + 23 + 23 + 31), re-derived by hand from the FINAL program listing before
  the first run and pinned by equality.
* **Q10 APPROVED: `ifetch pfsr` and `ifetch pfar` join the SYMPTOM set** (STALE = the instruction seeds); HEAD prints
  `PRESENT 10/10`, the fix `ABSENT`.
* **Q11 APPROVED: drop `INFO ifetch` (four rows score it); keep `INFO unclaimed`.**
* **Q12 APPROVED: the header names all 11 earlier gate-14 skip points**, derived by `grep -n 'gate_skip\|need_exec'
  regress/gate_arm.sh` (`:84`, `:85`, `:93`, and the eight probe-completion skips).
* **Q13 APPROVED: L20 is L4** (HEAD's case verbatim IS "left returning 1, write kept"); mark L20 "= L4, not run".
* **Q14 APPROVED: the leg criterion is "the MEASURED red set equals PRETABLE §5's predicted set (as amended)"**; a
  mismatch is a RESULT (mis-built / dead target / mis-cut row / wrong prediction) recorded in `SCORES.txt`, never
  re-aimed silently.  **L18 = the NULL-checked writes moved to just before the outer guard** (25 red predicted via the
  readback prerequisite; L19 27 red via the first IDR load -- both as PRETABLE says).
* **Q15 APPROVED: L8b = `if (cmmu != NULL || cache == CACHE_INSTRUCTION)`**; predicted `null surv` red (part 2 dies),
  `null route` green (part 1's dump flushed before the crash, `debugger.c:380-383`).
* **Q16 APPROVED: add L6b** (always `cmmu[0]`; 12 red / 19 of 31 predicted).
* **Q17 APPROVED: L16 excludes the VME device** (`vme pfsr`, `vme pfar` red; 29/31).
* **Q18 APPROVED: add L22, the LUNA case deleted** (`default:` stops the cpu; luna route/pfsr/pfar/icmmu red through
  `prereq:handler`; 27/31 predicted) -- it measures the comment's counterfactual clause (CL15).
* **Q19 APPROVED: frozen copies and drivers under `regress/artifacts/` are `*.py.txt` / `*.sh.txt`** (the MANIFEST stays
  at B11's two lines).
* **Q20 APPROVED: gates 14 and 11 run once each on `build/gxemul` after §7**; if a block OUTSIDE `#570`'s is red, re-run
  that gate alone with `PMAX=/tmp/gxt36/work/gxemul` to attribute it, and report both runs.
* **Q21 CONFIRMED: the boot pair is `/tmp/gxt36/work/gxemul` vs `/tmp/gxt36/base/gxemul`**, `gate_ab.sh`'s `luna_run`
  shape (`-N -e luna-88k -d R:<image> boot`, LUNA_BUDGET / LUNA_STALL / LUNA_BACKSTOP 12e9 / 120 / 1800), BEFORE the table.
* **Q22 APPROVED: compare `dev_m8820x.o`'s md5 before and after the comment-only edit** (identical expected; it turns
  CL16-CL19's no-row sentence into a measurement).
GO-AHEAD for §3-§9 under §10 and §11; order: §3 detector (frozen copy before any table) -> §4 pre-fix red on the base
binary -> §5 fix + fixed.out + fixed_witness24.out -> §8's A11 boot A/B -> §6 table (L1-L22 as amended) -> §7 propagation
+ clearance -> §8 gates 14 and 11 + the `#568` pin + the 3ffffff0 grep -> §9 report.  The panel is idle; gates may run.
