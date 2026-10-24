# T36 / round #570 (m88kbuserrregs) -- BUILD_REPORT.md (the builder, Opus 5.5, 2026-10-23/24)

Dispositions, scores and paths.  All paths are relative to `regress/artifacts/m88kbuserrregs/table1_20261023/` unless
noted.  Nothing was staged or committed; git was used for object reads only.  Pass 2 is the main loop's.

## 1. What was done, in order (BUILD_SPEC sections 2-9 under sections 10 and 11)

| step | result | artifact |
|---|---|---|
| 2.1 baseline | HEAD `7fca7187`; the four product files md5-identical in GXEMUL-SEC, est/, build/, build-asan/, /tmp/gxsec-build and the work clone; the work clone (build/ + the peer's five files at their HEAD blobs) built unmodified to a binary BYTE-IDENTICAL to the witness's base (`2efeec55`); the frozen witness on it: 16/24, the same eight reds, all 35 row/INFO/summary lines identical | `BASELINE.out`, `base_witness24.out` |
| 2.2 PRETABLE | 31 rows; sibling parity, CLAIM->ROW (CL1-CL19), guard/body fields with the body-induced partition, CHANNEL per row, predicted red set per leg; AMENDMENT 1 (section 10's conjunctive null session, the 2x2 cross-product, which body, VALUE vs GUARD-OPERAND variants, L8b, re-derived predictions) -- written 22:15/22:28, before every table run | `PRETABLE.out` |
| questions | 22 items, all ruled in BUILD_SPEC section 11 | `BUILDER_QUESTIONS.md` |
| explorations (HEAD binary, not rows) | E1 debugger dump works piped; E2 `pause 1` starts CMMU-less cpu 1, `focus 1` sets it up; E3 C5's NULL dereference does not exist; E4 the instruction x NULL cell is reachable stepped; E5 the conjunctive stepped null session works end to end | `explore_20261023/` |
| 3 detector | `regress/m88k_buserr_probe.py` revision 2, 31 rows; smoke-run once unfrozen on the HEAD binary (identical rows to the official pre-fix run, kept as `smoke_HEAD_unfrozen.out`), then FROZEN (md5 `d57c12ab`, the shipped file is byte-identical to it) before any table run | `m88k_buserr_probe.rev2.frozen.py.txt` |
| 4 pre-fix RED | HEAD binary `2efeec55`: **21/31**, CONTROL=OK, **SYMPTOM=PRESENT 10/10**, the ten predicted reds (uld/ust/vme pfsr+pfar, luna route, luna pfar, ifetch pfsr, ifetch pfar), exit 1 | `prefix_HEAD.out` |
| 5 fix | four files, byte-identical in GXEMUL-SEC and est/; work clone rebuilt: 0 warnings, binary FRESH (`3cd0501c`); 221 of 224 objects+binary byte-identical to the unmodified build -- only `gxemul`, `cpu_m88k.o`, `dev_luna88k.o` changed; **`dev_m8820x.o` byte-identical (Q22: comment-only, measured)**, and every other arch's cpu object rebuilt identical (the change is MEM_M88K-only) | `fix570.diff`, `build_work_fixed.out`, `objmd5_work_*.txt` |
| 5.5 post-fix | detector **31/31, SYMPTOM=ABSENT**, exit 0; the FROZEN witness **24/24, SYMPTOM=ABSENT** (witness clause (i), L1) | `fixed.out`, `fixed_witness24.out` |
| A11 boot A/B | luna rig, gate_ab.sh's luna_run shape: BASE `2efeec55` reason=MARKER, 7,651,336,103 instrs, 125 s, markers 1:1:1; FIXED `3cd0501c` reason=MARKER, 7,550,665,157 instrs, 120 s, markers 1:1:1 -- **the post-fix boot reaches `login:`**; the consoles differ only in the overlay temp name, the loader spinner's wrap, one line break and the date | `boot_ab/`, `boot_base.out`, `boot_work.out` |
| 6 table | **27 measurements, 27 MATCH their PRETABLE prediction, 0 RESULT**; L20 = L4, not run | `SCORES.txt`, `L*.out`, `L*.diff`, `legs_batch*.out` |
| 7 propagation | the four files into build/, /tmp/gxsec-build, build-asan/ (est/ in step 5); each rebuilt (rm src/cpus/*.o; make), 0 warnings; the peer's five files md5-identical before and after in all three | `prop_*.out`, `CLEARANCE.out` |
| 8 gates | GATE 14 (`gate_arm.sh`, `run.sh 14`, build/gxemul `931e69fa`, LOGDIR /tmp/gxt36/gatelogs14): **PASS, 1310 checks, 0 FAIL, REGRESS_PASS**, wall 7974 s; the #570 block **31/31** (all 31 per-row checks, controls, SYMPTOM absent, sentinel once); the **#568 pin 38/38**.  GATE 11 (`gate_m88k_rounding.sh`, `run.sh 11`): **PASS, 111 checks**, wall 247 s.  `grep 3ffffff0` over regress/*.py and regress/*.sh: no committed probe or gate at HEAD; the only working-tree hits are this round's probe and the new gate-14 comment | `gates/` |

## 2. Diff stat

| file | +/- | note |
|---|---|---|
| `src/cpus/memory_rw.c` | +24 -5 | the MEM_M88K arm: the TODO replaced by the selector, the NULL-checked PFSR/PFAR writes (a braced block, the file's declaration style) |
| `src/cpus/cpu_m88k.c` | +4 -0 | `#include "thirdparty/m8820x.h"` after m8820x_pte.h, with its comment |
| `src/devices/dev_luna88k.c` | +7 -3 | `case 0x3ffffff0:` -> `return 0;`, the PFSR write deleted, the case and an amended comment kept |
| `src/devices/dev_m8820x.c` | +25 -25 | comment-only at the four sites; line count unchanged (551), so the object is byte-identical |
| `regress/m88k_buserr_probe.py` | +836 (new) | revision 2 of the witness probe (+417 -186 against it) |
| `regress/gate_arm.sh` | +31 -0 | the #570 block after #568's; working tree == `staged/gate_arm.sh` (HEAD-based) |
| `tools/pipeline/check_probe_wiring.py` | +11 -0 | two MANIFEST entries; inserted identically into the working tree (which keeps the peer's lines) and `staged/check_probe_wiring.py.txt` (HEAD-based) |

## 3. N = 31, the rows

neg apparatus, mv devsig, mv cmmu rt, ok route, ok regs, uld route/pfsr/pfar/icmmu, ust route/pfsr/pfar/icmmu, vme
route/pfsr/pfar/icmmu, luna devsig, luna cmmu rt, luna route/pfsr/pfar/icmmu, ifetch route/pfsr/pfar/dcmmu, dbg noexc,
null surv, null route, unasm.  CONTROL_ROWS unchanged (the six witness controls); `ifetch route` is an attribution
row (Q8); SYMPTOM has ten members (Q10); unasm literal 192/192 (Q9, measured 192/192 on every live run).

## 4. Every score, with its instrument and denominator

Detector = rev 2 frozen (`m88k_buserr_probe.rev2.frozen.py.txt`, md5 `d57c12ab`, N = 31).  Witness = rev 1 frozen
(`witness_20261023/m88k_buserr_probe.py`, md5 `d59798b0`, N = 24).  Every variant leg: a clone of the fixed work tree,
one file replaced, rebuilt FRESH with 0 warnings, restored by cp from GXEMUL-SEC + cmp, tree discarded.

| leg | score | instrument / N | artifact | vs PRETABLE |
|---|---|---|---|---|
| pre | 21/31 | rev2/31 | `prefix_HEAD.out` | MATCH |
| fix | 31/31 | rev2/31 | `fixed.out` | MATCH |
| L1 | 24/24 | rev1/24 | `fixed_witness24.out` | MATCH |
| L3 | 21/31 | rev2/31 | `L3_armHEAD.out` | MATCH |
| L3/w24 | 16/24 | rev1/24 | `L3_armHEAD_witness24.out` | MATCH |
| L4 | 29/31 | rev2/31 | `L4_caseHEAD.out` | MATCH |
| L4/w24 | 22/24 | rev1/24 | `L4_caseHEAD_witness24.out` | MATCH |
| L5 | 1/31 | rev2/31 | `L5_stub.out` | MATCH |
| L6 | 28/31 | rev2/31 | `L6_seldata.out` | MATCH |
| L6b | 19/31 | rev2/31 | `L6b_selinstr.out` | MATCH |
| L7 | 30/31 | rev2/31 | `L7_noexcdrop.out` | MATCH |
| L8 | 29/31 | rev2/31 | `L8_nullrm.out` | MATCH |
| L8b | 30/31 | rev2/31 | `L8b_nulldata.out` | MATCH |
| L9 | 30/31 | rev2/31 | `L9_excinnull.out` | MATCH |
| L10 | 26/31 | rev2/31 | `L10_raw3.out` | MATCH |
| L11 | 26/31 | rev2/31 | `L11_pfarrel.out` | MATCH |
| L12 | 26/31 | rev2/31 | `L12_pfsronly.out` | MATCH |
| L13 | 26/31 | rev2/31 | `L13_bothcmmu.out` | MATCH |
| L14 | 26/31 | rev2/31 | `L14_sibclear.out` | MATCH |
| L15 | 29/31 | rev2/31 | `L15_readonly.out` | MATCH |
| L16 | 29/31 | rev2/31 | `L16_novme.out` | MATCH |
| L17 | 22/31 | rev2/31 | `L17_excdrop.out` | MATCH |
| L18 | 6/31 | rev2/31 | `L18_preguard.out` | MATCH |
| L19 | 4/31 | rev2/31 | `L19_res1.out` | MATCH |
| L21 | 28/31 | rev2/31 | `L21_casewrdel.out` | MATCH |
| L22 | 27/31 | rev2/31 | `L22_casedel.out` | MATCH |
| L5b | no sentinel | rev2/31 | `L5b_absent.out` | MATCH |
| L20 | not run (= L4, Q13) | -- | -- | -- |

Per-leg red rows, predicted sets and reasons: `SCORES.txt`.

Clause (c): measured at `L5_stub.out` (exit-1 non-emulator: 1/31, only `neg apparatus` green by design, CONTROL=FAIL,
SYMPTOM=MIXED, sentinel printed, exit 1) and `L5b_absent.out` (binary absent: FileNotFoundError, no rows, no
sentinel).  Clause (b): L3 and L4 on both instruments (31-row 21/31 and 29/31; 24-row 16/24 and 22/24, as B3
predicted).  Clause (d): L6, L6b, L7, L8, L8b, L9 each red on exactly its predicted rows.

## 5. Two-part clearance (`CLEARANCE.out`)

```
  /mnt/c/DocumentNoSnc/CC/GXEMUL/est part1 CLEAN      part2 N/A (source tree, no binary); no sentinel
  /mnt/c/DocumentNoSnc/CC/GXEMUL/build part1 CLEAN      part2 FRESH (binary 931e69fad962, 2026-10-23 23:11:37); no sentinel
  /mnt/c/DocumentNoSnc/CC/GXEMUL/build-asan part1 CLEAN      part2 FRESH (binary 9d0e06809a1d, 2026-10-23 23:14:18); no sentinel
  /tmp/gxsec-build                   part1 CLEAN      part2 FRESH (binary 8d882c052a5b, 2026-10-23 23:12:15); no sentinel
  /tmp/gxt36/work                    part1 CLEAN      part2 FRESH (binary 3cd0501cf7c8, 2026-10-23 22:48:32); no sentinel
  leg trees left in /tmp/gxt36/legs: 0
```
Re-run at 01:36 after both gates (`CLEARANCE_final.out`), identical to the 23:14 run (`CLEARANCE.out`).  est/ is a source tree: part 2 N/A.  build/'s five peer files are md5-identical before and after (`prop_build.out`).

## 6. Where this build disagreed with the spec or a ruling (by id)

1. **BUILD_SPEC section 10, section 5.1's rationale.**  It says "after m8820x_pte.h because that is upstream's placement".
   Upstream placed the include BEFORE m8820x_pte.h (`research_20261022/trunk_src.diff:1921-1922`, as packet.md 3.4
   quotes it).  I placed it after `:53` as sections 5.1, 10 and 11 direct; the comment claims only that upstream adds the
   same include to this file, not its position.  The position is not load-bearing (NBSG is expanded only at a use, and
   nothing uses it).
2. **The staged checker copy is named `staged/check_probe_wiring.py.txt`**, not `.py`.  This follows Q19: a `.py` under
   regress/artifacts that is ever staged needs a MANIFEST line itself.  The copy is byte-for-byte what the commit should
   carry.
3. **The working-tree insertions into `gate_arm.sh` and the checker were made after section 7, not in section 3.**  The
   staged copies were made at the same moment, and the insertions are measured identical.  The working-tree gate 14
   therefore never ran the new block against a build/ that did not yet carry the fix.
4. **Gate 14 ran as a harness-tracked background job, not in the foreground.**  Its last full run took about 2 h 12 min
   (the /tmp/gxregress logs of 2026-10-19), and the Bash tool's foreground cap is 10 min.  A timed-out foreground WSL
   call orphans the job, which the carrier warns against.  It ran alone, one job at a time, with a private LOGDIR.
   Gate 11 and the boots ran in the foreground.
5. **The unfrozen detector was smoke-run once on the HEAD binary before the freeze** (`smoke_HEAD_unfrozen.out`).  Its
   rows are identical to the official `prefix_HEAD.out`.  It is disclosed so that no number is read as fitted.
6. **dev_m8820x.c's comments were rewrapped so the line count did not change**, because `FAILURE()` embeds `__LINE__` at
   `:537`.  One wording changed at the `:453` site to fit: "dropping the handler's store" became "dropping its store".
7. **C5 is WITHDRAWN** (section E) and is also MEASURED: on the HEAD binary, CMMU-less cpu 1 read both IDR windows
   (cpu 0's 0x00a90000) and stored an SCR command that reaches `m8820x_command()` (`:108`); exit 0, no fault
   (`explore_20261023/explore_c5_ixnull.out`, E3).  **C4** stays conditional on a NONZERO bootstrap cpu,
   source-derived and unmeasured.
8. **Records were not edited** (CHANGELOG, OUTSTANDING_BUGS, ledger, matrix); they are the main loop's.  For Q2's
   "record the SFRZ mechanism in the CHANGELOG", a draft sentence: *In the `null` session cpu 1's instruction-fetch
   refusal follows its data fault while PSR.SFRZ is still set (no `rte` clears it: an `rte` would resume at SNIP, the
   FELL store), so m88k_exception delivers it as ERROR (vector 10) -- the arm, and its NULL test, run before the
   exception either way; measured E5 and in every null-session transcript.*

## 7. Open items (for pass 2 and the main loop)

* B14: the one ask-again on this clean table is the main loop's.
* The R2 re-root obligation of the four `ifetch` rows and of the null session's instruction cell goes with C1/C2
  (the contract discloses it).
* The working-tree `check_probe_wiring.py` now reports 7 GHOSTs: the 5 earlier unowned ones plus this round's two,
  until the two `.py` files are staged.  A simulated staging run (domain() patched, no index touched) of the
  HEAD-based staged copy gives PROBEWIRING_PASS: the detector is "RUN by gate_arm.sh:1927" and the witness "not run
  (correct)" (`drivers/sim_staged_wiring.py.txt`).
* `/tmp/gxt36/work` now holds the FIXED tree (binary `3cd0501c`); `/tmp/gxt36/base` is the HEAD baseline (`2efeec55`).
  No leg tree is left, and no `.MUTANT` sentinel exists anywhere.
