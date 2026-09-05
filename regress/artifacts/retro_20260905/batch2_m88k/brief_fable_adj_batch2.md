# FABLE 5.1 ADJUDICATION -- RETROSPECTIVE BATCH 2 (the two shipped m88k CPU fixes), 2026-09-05

Liveness: open your answer with the token FABLE_ADJ_B2_20260905 and a VERBATIM quote of the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\retro_batch2_m88k\codex.txt` (prompt delivery and file access proven, not assumed).

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  Check the premises, not just
the derivations -- open the files; a seat that re-derives a fact from something this brief did NOT give it outranks one that
agrees.  THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` (HEAD 99b92f9).  `C:\DocumentNoSnc\CC\GXEMUL\src\` is pristine 2021
upstream, NOT this fork -- if your line numbers disagree with the ones below by hundreds you are reading it.

READ-ONLY.  Never write to GXEMUL-SEC/, build/, est/, build-asan/ or /tmp/gxsec-build; do not build anything (three codex
jobs are running and a build would contend).  Return your whole answer as TEXT in your final message -- the harness blocks
seat file writes; the main loop preserves it.

## YOUR HAT
This is the ADJUDICATION of a retrospective review, not another review.  The owner asked (2026-09-04) that previously shipped
fixes be re-checked by GPT-6 Astra at max effort and adjudicated by Fable 5.1.  Astra's batch-2 answer is inlined below in
full.  Decide, per finding: DEFECT (becomes a queue row -- give id, severity, witness shape, option set), RECORD (L4, corrected
in place -- give the exact sentence and the correction), FILE (coverage debt -- give the row id and rank), or DROP (with the
measurement or reading that kills it).  Anything checkable in under two minutes gets CHECKED, not judged.

## THE TWO COMMITS
| sha | round | subject |
|---|---|---|
| d12114d | #323 | bcnd: the M5 condition-mask decode -- 27 -> 96 handlers, generated table `src/cpus/tmp_m88k_bcnd.c` from `generate_m88k_bcnd.c` |
| ed242c0 | #380 | the idle-loop fold (`X(idle_with_tb1_n)`, `COMBINE(idle)`) executed the branch's delay slot wrongly; #381 (ee4b69b) later changed the gate and records |

`git -C GXEMUL-SEC show --format= <sha> -- <file>` gives a diff without the message; `git show --format=%B <sha>` the message.
CHANGELOG blocks: `grep -n '^# Round' GXEMUL-SEC/CHANGELOG.md` (newest at the top); the #323 block anchor is
`## Seventy-sixth round (#323)`.  Manual: `_scratchpad/mc88100.txt` (pdftotext; tables may stagger -- prefer the prose).

## WHAT THE MAIN LOOP ALREADY CHECKED (each is a QUESTION if you can re-derive it)
1. `GXEMUL-SEC/src/cpus/cpu_m88k.c`, the switch after `bool implemented = false;` (lines 692-773 today): ONLY
   RESET / INTERRUPT / INSTRUCTION_ACCESS / DATA_ACCESS set `implemented = true`.  MISALIGNED_ACCESS, UNIMPLEMENTED_OPCODE,
   PRIVILEGE_VIOLATION, BOUNDS_CHECK_VIOLATION, ILLEGAL_INTEGER_DIVIDE, INTEGER_OVERFLOW, ERROR, SFU1_PRECISE, SFU1_IMPRECISE
   each print a VERBOSITY_ERROR debugmsg and `break` with implemented still false.  Then (line 775):
       if (vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented) { debugmsg "unimplemented vector=.. pc=..";
           for (j..ncpus) cpus[j]->running = false; m88k_pc_to_pointers(cpu); return; }
   -- so those NINE classes stop every guest CPU instead of being delivered.  (Is that reading right?  What does the emulator
   do when every cpu's `running` is false -- exit, or drop to the debugger?  Check src/core/emul.c / machine.c.)
2. Raise sites, deriver `grep -o -E 'm88k_exception\(cpu, *M88K_EXCEPTION_[A-Z0-9_]+' src/cpus/cpu_m88k*.c | sort | uniq -c`
   run 2026-09-05: SFU1_PRECISE 58, PRIVILEGE_VIOLATION 10 (9 in cpu_m88k_instr.c + 1 in cpu_m88k_instr_loadstore.c),
   ILLEGAL_INTEGER_DIVIDE 4, INTEGER_OVERFLOW 3, MISALIGNED_ACCESS 1, UNIMPLEMENTED_OPCODE 1; plus three
   `m88k_exception(cpu, ic->arg[2], 1)` sites (tb0/tb1/the delayed form) with a guest-chosen vector.
3. No existing queue row covers the halt: the ledger's m88k/luna rows are es438, m8batc, m88kexit (memory_m88k.c exit(1) on
   CMMU_PFSR_SUCCESS -- a DIFFERENT site), lunafuse, m8lanecomment, m8sarrows.  OUTSTANDING_BUGS.md mentions the #380
   `vector >= USER_TRAPS_START` restriction at its line ~4025 and nothing about the fallback.
4. The generator sentence Astra names exists verbatim: `generate_m88k_bcnd.c:54` "#323: every other mask value. These are
   legal encodings that the assembler has no mnemonic for".  `cpu_m88k_instr.c:2683` carries "delay-slot state wrong
   (delay_slot flag, XIP_E, and the vector-dependent"; `:2697` "test would be dead always (the #360/#361 fold-shipped-dead
   shape)"; `CHANGELOG.md:21475` "which is exactly why no post-loop witness can see the defect".
5. Astra noted the batch brief's QUESTIONS section carried a PowerPC parenthetical ("twenty-four encodings / FPSCR /
   straddle") copied from batch 1 -- a brief defect of the main loop's, to be recorded as such.

## ASTRA'S ANSWER, VERBATIM (codex.txt, 9,216 bytes; the .err stream ends with the same text and `tokens used 158,820`)
d12114d (#323): **RECORD** — mask repair is correct; stale legality claims remain, and the detector covers only part of the repaired domain.  
ed242c0 (#380): **DEFECT** — the repaired fallback exposes a pre-existing privilege-exception path that stops guest CPUs; detector and record gaps also remain.  
BATCH: **DEFECT** — reviewed HEAD `2bb9cb4`; native builds, gate reruns, and mutation measurements remain unverified in this read-only workspace.

I reviewed only `GXEMUL-SEC/`. The four product files are unchanged since `ed242c0`; later `ee4b69b` (#381) changed the idle gate and records. Source anchors below were verified unique with literal matching (`rg -n -F`).

**For d12114d, the mask repair is correct at HEAD.** The producer extracts five bits, giving exactly 32 field values. The manual derives the condition from the sign bit and NOR of the lower 31 bits. Its `eq0 = 0x02` row calibrates the ordering; bit 4 is unused but must be zero for future compatibility. See [MC88100 manual](C:/DocumentNoSnc/CC/GXEMUL/_scratchpad/mc88100.txt), extracted lines **4105, 4106, 4123, 4156, 4160, 4162, 4164, 4166**.

Here is the complete enumeration. `P` = positive; `Z` = zero; `N` = negative excluding `0x80000000`; `M` = `0x80000000`.

| M5, reserved bit clear | M5, reserved bit set | HEAD selects |
|---|---|---|
| 00 | 10 | Nothing |
| 01 | 11 | P |
| 02 | 12 | Z |
| 03 | 13 | P, Z |
| 04 | 14 | N |
| 05 | 15 | P, N |
| 06 | 16 | Z, N |
| 07 | 17 | P, Z, N |
| 08 | 18 | M |
| 09 | 19 | P, M |
| 0a | 1a | Z, M |
| 0b | 1b | P, Z, M |
| 0c | 1c | N, M |
| 0d | 1d | P, N, M |
| 0e | 1e | Z, N, M |
| 0f | 1f | P, Z, N, M |

The right column agrees with the manual’s selection logic throughout. The reserved-bit-set forms are accepted tolerantly, with the manual’s compatibility restriction still applying.

The generator and tracked output agree structurally: function names, predicates, table entries, and all three execution protocols. I checked all 128 table entries and evaluated the 96 emitted predicates at six class/boundary representatives—**576 comparisons, zero mismatches**. The nine old predicates also agree across all four classes.

The enumerated counts are **27 → 96 handlers** and **101 → 32 NULL entries**. The remaining NULLs are exclusively the same-page-plus-delay-slot optimization entries; the decoder retains the generic delayed handler. References:

- [generate_m88k_bcnd.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/generate_m88k_bcnd.c), anchor `void print_condition(int m5)`.
- [tmp_m88k_bcnd.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/tmp_m88k_bcnd.c), anchor `X(bcnd_n_eq0)`.
- [cpu_m88k_instr.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k_instr.c), anchor `ic->f = m88k_bcnd[d + 32 * (op26 & 1)];`.

**Its detector pins the original failure only partially.** Gate 11’s seven rows are anchored by `for v in "bcnd m5=4 -1 taken"` in [gate_m88k_rounding.sh](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gate_m88k_rounding.sh). Their producer is `BCND_ROWS = [` in [m88k_rounding_probe.py](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/m88k_rounding_probe.py).

All seven encode plain `bcnd`, displacement `+16`, and a same-page target. They cover six masks: `0,1,2,4,c,f`. The `m5=4 MIN fall` row correctly distinguishes ordinary negatives from MIN.

A small surviving regression is to extend the generator’s **table-emission** NULL predicate with `|| m5 == 6`, then regenerate. That restores rejection of a conforming encoding while leaving every existing bcnd row’s mask untouched. This is a source-predicted survivor, not a measured mutation. The rows use independent expected PCs; their weakness is coverage, not self-round-tripping.

**The RECORD verdict has concrete grounds.** In [CHANGELOG.md](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/CHANGELOG.md), anchor `## Seventy-sixth round (#323)`, the later paragraph correctly distinguishes accepted reserved-bit forms from legal encodings. Nevertheless, the generator still says `every other mask value. These are legal encodings`. That mutable sentence needs correction in place.

Also distinguish **nine pre-existing GXemul cases** from the manual’s **six listed assembler mnemonics**. The newly implemented compatibility-compliant masks are seven values: `0,4,6,9,a,b,f`; the other sixteen newly accepted values set the reserved bit.

The counts of handlers, NULLs, seven detector rows, and fifty tracked generated C files check out. I did not locate a retained deriver supporting the claimed roughly **1.9 million comparisons**, or an original artifact establishing all eight historical halts. Those historical measurements remain unverified. I found no live defect in the repaired mask decisions.

**For ed242c0, the intended slot-dispatch repair is present.** At `X(idle_with_tb1_n)` in `cpu_m88k_instr.c`, the handler snapshots the branch decision, establishes the branch PC and delay target, dispatches the slot once, and preserves exception ownership when `EXCEPTION_IN_DELAY_SLOT` is set. Both taken and untaken paths dispatch the slot. The architectural requirement is supported by manual extracted lines **851, 852, 3714, 3715, 3716, 4113, 4114**.

I enumerated the matcher’s actual domains at anchor `void COMBINE(idle)`:

- The arming expression produces 32 source-register fields; the matcher excludes `r0`.
- The delayed pattern fixes displacement at **−8 bytes**.
- Of 1,024 branch indices, the bounds admit **2 through 1022**, exactly **1,021 positions**. Their slots remain real page entries.
- The nine-bit vector predicate admits **128 through 511**, exactly **384 values**.

The documented once-per-idle-break approximation remains; this is not a proof of arbitrary delay-slot equivalence across collapsed iterations.

**The detector kills the original omission but still cannot prove exactly-once execution.** Its rows are `taken`, `takenj`, and `untaken`, defined beneath `PROG = (` in [m88k_idle_probe.py](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/m88k_idle_probe.py). The HEAD gate’s unique counter anchor is:

`idle counters: arm3 fired, slot==ntn, ntp=0, guard quiet`

#381 correctly strengthened the predicate to require `slot == ntn` and `ntp == 0`.

However, **duplicating the single slot-call statement while leaving the adjacent counter increment unchanged** survives those assertions by inspection. Both calls store the same value; all three value rows remain unchanged, and the counters still compare equal. The unique product anchor is `ic[3].f(cpu, &ic[3]);`. Thus counter equality does not independently establish execution multiplicity. The probe also lacks fault-context, boundary, and low-vector privilege rows.

**The smallest live residual I found is the privilege-exception fallback.** The new vector restriction correctly declines low-vector folds. The native `tb1` handler then performs its user-mode privilege check, but [cpu_m88k.c](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/cpus/cpu_m88k.c), anchor `vector < M88K_EXCEPTION_USER_TRAPS_START && !implemented`, treats privilege violation as unimplemented and sets **every guest CPU’s `running` to false**, returning before exception delivery.

The required result is a privilege exception at **VBR + 0x30**, including when the trap condition is false: manual extracted lines **6195, 6196, 9257, 9264**. This is a pre-existing exception-core defect exposed while checking #380’s fallback, not a defect introduced by the new matcher. The current idle probe uses vector `0xff` and cannot detect it.

**The #380 record needs further correction in place.**

- At CHANGELOG anchor `The commit message additionally listed XIP_E`, #381 attributes the error to an immutable message. **`ed242c0`’s message contains no `XIP_E`.** The erroneous claim remains in the mutable source comment anchored by `delay-slot state wrong (delay_slot flag, XIP_E`. Actual XIP_E filing does not depend on delay-slot state.
- The source still says `test would be dead always`, although #381 corrected the CHANGELOG to acknowledge an already-translated slot.
- The claim anchored by `exactly why no post-loop witness can see the defect` is too broad. An accepted slot that changes the polled word can make loop exit itself distinguish the implementations.
- The shipped **68 → 74 checks**, **+6**, and **34,415 + 3,648 = 38,063** arithmetic checks out. Original artifacts for the quoted **6,172 entries**, mutation run, and **129.7-second boot** were not located.

For the batch, the committed [August 29 battery log](C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/batteryreds/battery_20260829_160646.log) supplies later passing evidence, including the unique anchor `M380_COUNTERS=installs:0/0/1,ntp:0,ntn:6551,slot:6551,ds:0`. It does not establish a run against today’s HEAD or substantiate the earlier exact measurements.

A measuring seat should build a fresh writable Linux checkout of **GXEMUL-SEC at `2bb9cb4`**, regenerate and compare `tmp_m88k_bcnd.c`, run gate 11, measure the two detector-surviving mutations above, and verify privilege-exception delivery. The brief’s “twenty-four encodings / FPSCR / straddle” parenthesis does not describe either shipped fix.

## QUESTIONS
Q1 THE DEFECT.  Is the privilege-exception finding right, and is Astra's SCOPE too narrow?  The main loop reads the class as
   all nine unimplemented vectors (77 raise sites), reachable from USER MODE: a user program executing `tb1` with vector <
   128, a privileged instruction (ldcr/stcr/rte...), a divide by zero (`divu`/`divs` -- ILLEGAL_INTEGER_DIVIDE), a signed
   overflow (INTEGER_OVERFLOW), or any FP instruction while SFU1 is disabled, stops the emulated machine -- where real
   hardware delivers VBR + 8*vector and OpenBSD's kernel turns it into a signal.  Check reachability per class by reading the
   raise sites (which are conditional on guest state the guest controls?).  Then: (a) queue id and severity rank against
   the live queue (the head of OUTSTANDING_BUGS.md "OPEN LIST"); (b) the WITNESS shape -- a rung-3 cold-debugger probe on
   the committed luna88k machine (`regress/m88k_*probe.py` are the exemplars): which instruction, which observable on the
   pre-fix build (the "unimplemented vector=0x006" line and the machine stopping) and post-fix (PC == VBR+0x30, SXIP/SNIP/
   SFIP and PSR shadow state); (c) the OPTION SET for the fix -- the common path after `/*  Stuff common for all exceptions:
   */` already handles SFRZ, the shadow registers and the vector jump for the four implemented classes; what, per vector,
   would delivering the other nine additionally need (SFU1: FPECR/FPRH/FPRL/FPIT/FPSR state? MISALIGNED: DMT/DMA/DMD? the
   E bits in SXIP?) -- read the manual's exception chapter (`mc88100.txt`) and cite extracted-text lines by `grep -n`.
   Name what a measuring seat should build.  Say plainly if the finding should instead be SPLIT (e.g. the trap-like classes
   that need no extra state vs SFU1/MISALIGNED that do).
Q2 THE RECORD items -- verify each by opening the file and give the exact correction or DROP it:
   (i) the generator's "These are legal encodings" (reserved-bit-set forms are accepted tolerantly, per the manual and per the
   #323 CHANGELOG's own later paragraph); (ii) `cpu_m88k_instr.c:2683` XIP_E attribution -- run
   `git -C GXEMUL-SEC show --format=%B ed242c0 | grep -c XIP_E` yourself; (iii) `:2697` "test would be dead always" vs #381's
   CHANGELOG correction; (iv) `CHANGELOG.md:21475` "exactly why no post-loop witness can see the defect" -- is Astra's
   counter (an accepted slot that changes the polled word makes loop exit distinguish) right?; (v) #381's "The commit
   message additionally listed XIP_E" sentence.
Q3 THE DETECTOR RESIDUALS: the `|| m5 == 6` NULL-predicate survivor (source-predicted, not measured) and the duplicated
   `ic[3].f(cpu, &ic[3]);` survivor (counters compare equal by construction).  Under the vacuity floor these are SHIPPED
   detectors: is either a floor breach (clause a/b/c/d -- say which) or coverage debt to FILE?  Give the row ids and rank
   them below live defects.
Q4 UNVERIFIED MEASUREMENTS (the "roughly 1.9 million comparisons", "6,172 entries", "129.7-second boot", "eight historical
   halts"): the carrier's rule is that a score claim names its artifact FORWARD-ONLY and legacy counts are not retro-audited.
   Disposition: annotate "artifact not located (retrospective review 2026-09-05)" beside each without altering the number,
   or leave them?  Rule, with the reason.
Q5 THE BRIEF DEFECT (item 5 above): confirm it is a campaign records correction and say whether any batch-2 answer content
   was distorted by it.
Q6 WHICH OF THE MAIN LOOP'S PROPOSED DISPOSITIONS IS WRONG?  Proposed: DEFECT -> ONE new row `m88kexcunimpl`, HIGH,
   class-wide (nine vectors), witness owed at rung 3 before any edit; RECORD (i)-(v) -> L4 in place in one records commit;
   Q3 residuals -> FILED LOW under two ids; Q4 numbers -> annotated, not altered.  Name the wrong one(s) and why.

VERDICT LINE FIRST (one line per commit: HOLDS / DEFECT / RECORD, then a batch line), then Q1-Q6, then a NUMBERED
DISPOSITION LIST the main loop can file verbatim (id, severity, one-line title, witness shape, provenance = Astra batch 2 +
this adjudication).  Cite by grep anchor, not line number, except across files with the qualifier on the citation.
