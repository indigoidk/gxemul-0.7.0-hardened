# T36 / #570 -- BUILDER_QUESTIONS.md (the builder, Opus 5.5, 2026-10-23 ~22:3x; written after BASELINE.out and PRETABLE.out)

Scope: BUILD_SPEC.md sections 3-9 **and section 10**, which was already in the spec file when I re-read it (mtime
21:53:27; PASS1_RULINGS.md section E beside it).  Every item says where it comes from (spec section, ruling id or seat
line), what I found (with the measurement or source line), and what I propose.  **Nothing below has been built.**  The
only runs after the baseline were three explorations on the unmodified HEAD-equivalent work binary
(`explore_20261023/`): E1-E2 `explore_null_dbg.out`, E3-E4 `explore_c5_ixnull.out`, E5 `explore_conj.out`.  They are
explorations: not rows, not legs, not the detector.

Items Q1-Q4, Q14 and Q15 need a ruling before section 3 can be written.  The rest have a proposed default that I will use
unless told otherwise.

## Section 3 / 10 -- the null session (B5c)

**Q1 (RULING) -- stepped, not free-running.**  Section 10's conjunctive design reads as free-running: R1's tail halts
cpu 1 and the prompt returns, and cpu 0 parks so that a machine-wide breakpoint cannot end the session.  But the
probe's piped-stdin idiom cannot carry a `continue`: "the debugger reads MAIN_CONSOLE, which is also the guest
console's input" (`regress/vme_default_probe.py:46-48`).  Free-running would need `run_pty`, which has two costs:
- a `pty.fork` token in the probe.  grok:141 notes the gate-6 hygiene pins key on such tokens, so the move could shift a
  gate-6 pin this round does not plan to touch;
- a wall-clock `continue` budget, which is a load-sensitive oracle.

**Proposal:** the STEPPED conjunctive form, measured as E5 on HEAD.  It uses no `continue`, no breakpoint, no pty and no
dispatcher.  cpu 1 is set up by `focus 1` with `pc=`, `r5=`, two marker values and `VBR=`.  The RAM markers at
0xf000 (HANDLED) and 0xf004 (FELL) are zeroed by `put`.  Then:
- part 1, `step 3`: the data refusal.  Then dump the markers and read `reg 1,0`.
- part 2, `step 5`: the instruction refusal.  Then dump the markers again.

E5 measured: HANDLED set and FELL clear after both parts.  cpu 1's instruction fetch reached the arm (a device-failed
line) with cmmu[0] NULL.  cpu 1 ended parked, and the session exited 0.  The rows and the predictions are in PRETABLE
AM-1 and AM-6.

**On robustness:** the instruction cell rides the R2 pre-read today, but the NULL-check observable survives an R2 fix.
With the pre-read silenced, the step's own fetch (`to_be_translated`, `cpu_m88k_instr.c:2989-2990`) reaches the same arm
with CACHE_INSTRUCTION, so L8b still dereferences there.  Only the after-fault flow changes: R1 halts the cpu instead
of it parking at the ERROR vector.

**Ask:** approve the stepped form, or require free-running.  If free-running, I add `run_pty` from vme_default_probe.py,
and the gate-6 question has to be answered first.

**Q2 (RULING) -- "vector 2" in section 10 does not match the source.**  The data fault sets PSR.SFRZ, and any later
non-trap fault while SFRZ is set becomes ERROR, vector 10 (`cpu_m88k.c:811-819`).  E5 measured it: one
"SFRZ already set in PSR => ERROR" line, and cpu 1 at VBR1+0x50.  The NULL test is unaffected, because the arm runs
before `m88k_exception` (`memory_rw.c:614-622`).  Restoring vector 2 would need an `rte` in the data handler, and `rte`
resumes at SNIP, which is the FELL store, so it would write a false FELL.

**Proposal:** accept ERROR.  `null surv`'s want does not depend on the vector, and the design parks cpu 1 at both
VBR1+0x10 and VBR1+0x50.

**Q3 -- "set its own VBR".**  This can be done by the debugger (`focus 1` + `VBR=0x30000`; E5 shows `VBR=0x00030000`
before cpu 1 runs) or by a guest `stcr`.  The guest form is a new hand-assembled encoding that `unassemble` would have to
cross-check (the hand-assembled-encoding trap).  The debugger already sets pc and registers in every session.
**Proposal:** the debugger.

**Q4 (RULING) -- cpu 0's role in the null session.**  Section 3 and section 10 have cpu 0 run the seeded `uld` path and
then park.  In the stepped form no breakpoint exists, so the parking rationale (`cpu_dyntrans.c:1802-1804`) does not
arise.  In my design cpu 0 feeds no null row; the null rows' prerequisites are all cpu 1's.  Options:
- (a) keep cpu 0's `uld` path as the spec says.  This adds 31 placed words and nothing is scored from it.
- (b) pause cpu 0 from the start, as in E2.  This adds 8 placed words.

There is a separate question: should cpu 0's own checks (IDR, readback) gate the null rows as a machine-identity
prerequisite?  If yes, L19 also reds both null rows, because cpu 0's first IDR load faults under L19.
**Proposal:** (a), with no cpu-0 prerequisite.

**Q5 -- C5 and the CMMU-window prohibition: settled, and now measured.**  Section E withdrew both.  E3 measured it on
HEAD: CMMU-less cpu 1 read both IDR windows (cpu 0's 0x00a90000) and stored FLUSH_SUPER_ALL to SCR, which reaches
`m8820x_command()` and `:108`.  The run exited 0 with no fault.  This is for the section 9 report ("C5 WITHDRAWN").  No ruling
needed.

## Section 3 -- the other new rows, header and scoring

**Q6 -- where `dbg noexc` runs (B5b says "an existing mvme187 session").**
**Proposal:** a dedicated session cloned from `ok`.  E1 measured it on HEAD: zeros, pc 0x10028 unchanged, fall, seeds
kept.  The alternatives each blur the result:
- In `ok`, L7's dump-fault would also red `ok route` and `ok regs`.
- In `uld`, `ust` or `vme`, a later fault overwrites the evidence (section E, D3).  L7's dump-fault also writes the same
  PFSR and PFAR values (0x30000 and 0xfff46010) that those rows want.

The cost is one session and 23 more unasm words.  **Ask:** the dedicated session, or `ok`.

**Q7 -- section 10's "prerequisite rows (devsig / cmmu rt) or the equivalent".**
**Proposal:** "the equivalent" means `prereq_bad()`'s cause-free strings inside each scored row, as `uld`, `ust` and `vme`
already do.  N stays 31.  If separate CONTROL rows are wanted, N grows (ifetch 2, dbg 2, null at least 1) and the gate
pins follow.

**Q8 -- `ifetch route` as a CONTROL.**  Adding it to `CONTROL_ROWS` would turn L17 into `CONTROL=FAIL`.
**Proposal:** label it an attribution row in the CHANNEL column, as the uld, ust and vme route rows already are, and
leave it out of `CONTROL_ROWS`.

**Q9 -- the unasm literal.**  Re-derived by hand before the first run: 115 + ifetch 23 + dbg 23 + null.  The null session
adds 31 under Q4(a), giving **192**, or 8 under Q4(b), giving 169.  The literal counts the placed words of every scored
session.

**Q10 -- SYMPTOM.**  **Proposal:** add `ifetch pfsr` and `ifetch pfar`, with STALE meaning the instruction seeds.  HEAD then
prints `PRESENT 10/10` (section 4 expects both red on HEAD) and the fix prints `ABSENT`.

**Q11 -- INFO lines.**  **Proposal:** drop `INFO ifetch`, since four rows now score it, and keep `INFO unclaimed`.

**Q12 -- the header must list every earlier gate-14 skip, not only `:100-105`.**  Section 10 requires disclosure of the
earlier skips.  `grep -n 'gate_skip\|need_exec' regress/gate_arm.sh` lists 11 points ahead of the insertion point:
- `:84` need_exec;
- `:85` python3 missing;
- `:93` the load stub could not be written;
- eight probe-completion skips at `:105`, `:389`, `:430`, `:515`, `:638`, `:695`, `:816`, `:949`.

**Proposal:** the header names all of them, derived by that command.

## Section 6 -- the table

**Q13 -- L20 is the same as L4.**  L4 reinstates the HEAD case verbatim, and the HEAD case is exactly "left returning 1,
write kept".  The source is identical, so the binary is identical.  A `return 1;` in place of `break;` behaves the same,
because `#95`'s memset already zeroed the read buffer and the tail writes odata 0.  **Ask:** drop L20, or define it.

**Q14 (RULING) -- the "nothing else red" criterion, and L18's form.**  Any L18 that writes on served accesses also writes
after the probe's own served CMMU seed stores and readbacks.  So the readback prerequisite fails first in every
CMMU-seeding session: 25 red predicted.  L19 fires at the first IDR load: 27 red predicted (PRETABLE section 5,
codex:116).  So "nothing else red" cannot hold for L18 or L19 by construction.  It also fails for:
- L10-L14, each of which also reds its ifetch counterpart;
- L17, which also reds the four ifetch rows (R1's halt) and `null route`;
- L6, which also reds `ifetch dcmmu`.

**Proposal:** the criterion becomes "the measured red set equals PRETABLE section 5 as amended", and L18 = the
NULL-checked writes moved to just before the outer guard.

**Q15 (RULING) -- L8b's exact form.**  **Proposal:** `if (cmmu != NULL || cache == CACHE_INSTRUCTION)`.  The check then
covers data accesses only, and an instruction access with a NULL slot dereferences it.  Predicted: `null surv` red
(sig11 in part 2) and `null route` green, because part 1's dump is flushed before the crash (`debugger.c:380-383`).

**Q16 -- L6b.**  The other selector weakening, always cmmu[0] (grok:100's own cell), is in no leg.  Predicted 12 red,
19/31 (PRETABLE section 5).  **Proposal:** add it.  It is one build.

**Q17 -- L16: which device to exclude.**  **Proposal:** VME (`vme pfsr` and `vme pfar` red, 29/31).  Excluding luna88k is
symmetric.  Excluding `unreadable` reds six rows (uld, ust and ifetch pfsr and pfar).

**Q18 -- the CL15 counterfactual.**  The LUNA comment says "kept: default: would stop the cpu".  Its channel is
`luna route`'s handler prerequisite.  **Proposal:** keep the clause and add L22, "case deleted".  Predicted: luna
route, pfsr, pfar and icmmu red through `prereq:handler`, 27/31.  The alternative is to drop the clause from the
comment.

## Sections 0, 7 and 8

**Q19 -- frozen copies and the MANIFEST.**  Frozen probe copies and drivers under `regress/artifacts/...` will be named
`*.py.txt` or `*.sh.txt`.  That keeps check_probe_wiring.py's MANIFEST at B11's two lines, since a staged `.py` anywhere
under regress/ needs a line.  The explorations already follow this.

**Q20 -- which binary gates 14 and 11 test.**  Both default to `PMAX=$ROOT/build/gxemul`.  `build/` carries the peer's
dirty `dev_pcc2.c` and `mvme_pcctworeg.h`, and gate 14's pcc2_* blocks exercise both.
**Proposal:** run each gate once on `build/` after section 7, as section 8 says.  If a block outside `#570` is red, re-run that gate
alone with `PMAX=/tmp/gxt36/work/gxemul` (HEAD plus the fix only) to attribute it, and report both runs.

**Q21 -- the A11 boot pair.**  Section 10 moves the boot ahead of the table and pairs it as "the fixed WORK binary vs the
BASE binary".  I read that as `/tmp/gxt36/work/gxemul` against `/tmp/gxt36/base/gxemul`, not `build/gxemul` (section 8's
original text).  The shape is gate_ab.sh's `luna_run`: `-N -e luna-88k -d R:<image> boot`, with LUNA_BUDGET,
LUNA_STALL and LUNA_BACKSTOP 12e9 / 120 / 1800.  **Confirm.**

**Q22 -- confirming "comment-only" for dev_m8820x.c (no ruling needed).**  In step 5 I will compare `dev_m8820x.o`'s md5
before and after the edit.  An identical object is expected, which turns PRETABLE CL16-CL19's no-row sentence into a
measurement.
