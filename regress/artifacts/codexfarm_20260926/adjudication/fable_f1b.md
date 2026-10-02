VERDICT: 2 adopt, 3 adopt-with-changes, 0 reject, of 5 answers
FABLE_FARM_f1b_ALIVE_0926
CHECKPOINT.md first line, verbatim: `# CHECKPOINT -- 2026-09-26 09:35 (087a90 sections rewritten; the peer's sections below are untouched)`

CODEX FARM 2026-09-26 -- FABLE ADJUDICATION, batch f1b.  Fable 5.1 seat, read-only.  Every premise below was checked
against `git -C GXEMUL-SEC show HEAD:<path>` at HEAD `8ea26abb` (the commit every answer cites) and against
`_scratchpad/*.txt` by `awk NR` -- never the working tree, never any other `src/`.  I built nothing and ran nothing;
"checked" means opened and read.  Where an answer's next step or fix design rests on an inference rather than a fact, I
say so and rule on the inference.

PROVENANCE (from the launch logs, and it belongs in each ledger entry): `armmsrmodekill`, `fbctrlcmdkill` and
`armthumbabortkill` were REFUSED by GPT-6 Astra (content filter, `access_programs.c` named) and answered by the AUP
fallback `gpt-daybreak-blue-latest` at `ultra`; `ppcrlwhighhalf` and `pit8253lsbnotimer` were answered by Astra.  Record
the seat by the model that answered.  Nothing below discounts the three fallback answers for that reason -- their
citations checked out as well as Astra's.

PRIORITY SCALE used throughout is the brief's: HIGH = a guest can end the process, corrupt emulator memory or hang it
today; MED = guest-visible behaviour contrary to the documentation; LOW = records / diagnostics / latent.  Where the
ledger carries a different word I say so; the ledger's `sev` is a records field and is not changed by this file.

--------------------------------------------------------------------------------------------------------------------
## 1. `armmsrmodekill` -- ADOPT WITH CHANGES     priority HIGH
--------------------------------------------------------------------------------------------------------------------

**Recommendation as given:** add an MP device-signature control, run the unmodified-HEAD witness, then fix BOTH
`default:` arms with one atomic member-3 decline shared by the direct-MSR and the two SPSR-return paths, with both
helper defaults made non-fatal.

**Premises checked at HEAD -- all TRUE:**
* `src/cpus/cpu_arm.c:525-563` `arm_save_register_bank`: SVC32 arm `:541-546`; `default:` `:559-561` is
  `fatal(...) ; exit(1)`.  `:572-610` `arm_load_register_bank`: `default:` `:606-608`, same shape.  Seven M[4:0]
  values handled (USR32/SYS32/FIQ32/IRQ32/SVC32/ABT32/UND32, constants `src/include/cpu_arm.h:103-114`); 25 of 32
  enter a default.  Count of TWO process-ending sites holds.
* `src/cpus/cpu_arm_instr.c:822-848` `X(msr_imm)`: USR-only mask `:826-828`; `switch_register_banks` computed from
  the OLD vs NEW mode field `:830-832`; Save on the old mode `:838-839`; the unvalidated control byte written
  `:841-842`; Load on the new mode `:846-847`.  So `MSR CPSR_c,#0x14` from boot SVC32 (cpsr `0xd3`, `cpu_arm.c:127-137`)
  saves through the SVC32 arm and dies in Load's default -- Load is first-hit, Save is not.  CONFIRMED.
* The second path is real and unvalidated: `X(msr_imm_spsr)` `:856-880` stores any value into `spsr_svc` `:877-880`;
  `cpu_arm_instr_dpi.c:207-232` (`MOVS pc,...`) calls Save UNCONDITIONALLY at `:218`, copies SPSR into CPSR with no
  mode check `:219-230`, then Load `:232`; `cpu_arm_instr.c:1780-1813` (`LDM {..,pc}^`) does the same at `:1802-1812`.
* Save's default is unreachable at HEAD by a guest: every caller (`:838`, dpi `:218`, `:1806`, `cpu_arm.c:669`) runs
  Save on the CURRENT mode, and no reserved mode can become current because Load exits first.  The answer's "repair
  count two, first-hit count one" is exactly right and matches the ledger's own `SAVE IS NOT FIRST-HIT` sentence.
* Witness vehicle facts: `-M 64` gives SP `0x03fff000` (`src/machines/machine_test.c:198-199`); MP is installed by
  `default_test` (`:148-152`) at `DEV_MP_ADDRESS 0x11000000` with `DEV_MP_NCPUS +0x10` (`src/include/testmachine/
  dev_mp.h:22,31`), served by `src/devices/dev_mp.c:88-90` (`odata = machine->ncpus`).  IRQ dispatch is inside
  `if (!single_step)` at `src/cpus/cpu_dyntrans.c:206-209`, so STAY ON `step` is right.
* Tracking state: `git ls-files` lists NEITHER `regress/arm_msrmode_probe.py` NOR `regress/artifacts/armmsrmodekill/`
  (both exist in the working tree); ledger `tools/pipeline/ledger.json:47372-47373` has `witness: null`, `commits: []`;
  `regress/gate_hygiene.sh:377,418,429-430` names the probe as untracked/grandfathered.  No committed `regress/*.py`
  contains `E321F014` (grep of HEAD).
* Manuals: `ddi0100i.txt:1877-1879` (other M[4:0] values UNPREDICTABLE), `:9577-9578` (MSR: Exceptions None),
  `:9690-9693` (reserved mode value UNPREDICTABLE), `:45062-45065` (UNPREDICTABLE "must not halt or hang the processor,
  or any parts of the system"); `ddi0406.txt:102530-102537`, `:103921-103930`, `:143206-143212` ("can be implemented
  as UNDEFINED").  All as cited.
* NOT re-derived by me: the decoder trace `:4019-4063` / `:4294-4328`; the ledger's second grok firing already traced
  instruction-to-switch and I did not repeat it.

**Premises found FALSE:** none load-bearing.  Two small ones: `dev_mp.c:84-90` is WHOAMI; NCPUS is `:88-90`.  And the
DDI 0406 "UNPREDICTABLE may be implemented as UNDEFINED" clause is ARMv7 text; every in-tree ARM CPU here is SA-110 /
SA1110 (`machine_test.c:206-215`), so DDI 0100I governs and it has no such clause -- the answer's softening of the row's
"hardware cannot take UND" is fair as a records note but is NOT a licence for member 5, and the disposition (member 3)
stands either way.

**Ruling: ADOPT WITH CHANGES.**  The shared atomic validator is the right shape and it is the ledger's own constraint
("THE DECLINE MUST SIT BEFORE SAVE ... callers write cpsr BETWEEN save and load") applied at all three transition sites.
The changes:
1. **Witness the scope the fix takes.**  The ledger discloses "SPSR-then-MOVS pc" under clause (e) and rows nothing for
   it; the answer widens the fix to the two SPSR-return sites.  The reopening rule admits a second site into a round
   only if it is WITNESSED and covered by the same detector with no new oracle.  The probe is untracked and has never
   run, so this is L1 construction and cheap: add ONE session -- SVC32, `MSR SPSR_c,#0x14`, `MOVS pc,lr` -- to the
   same survival + `m=13 sp once` oracle BEFORE the first run, and re-derive the named-red tally in the spec artifact
   (four named reds on HEAD, not three).  Update `regress/artifacts/armmsrmodekill/WITNESSSPEC_REWRITE_grok_20260917.txt`,
   never the ledger note, per the ledger's own "build from the artifact" instruction.
2. **The two `default:` arms become LATCHED TRIPWIRES, not silent no-ops.**  Once the validator sits before Save at the
   three sites, both defaults are unreachable from any guest path; but if reached (debugger `reg cpsr=`, a future edit)
   cpsr holds a reserved mode over the previous bank -- the ledger names that as why member 1 is WRONG.  So: one
   `(once)` announce per CPU, no `exit(1)`, a comment saying it is unreachable after the guard and kept as the #549
   DATA-arm-shaped tripwire.  "Defensive and nonfatal" without that latch would be the silent form.
3. **Sibling parity, name it in PRETABLE.out:** `cpu_arm_instr.c:1795-1799` (`bdt_load: unimplemented mode`,
   `cpu->running = 0`) is the same class on the CURRENT-mode side and stays unreachable after the fix -- no edit, one
   sentence.
4. Records: the "hardware cannot take UND" sentence in the row is softened only as far as DDI 0100I allows -- i.e. not
   at all for SA1110; say the ARMv7 clause exists and does not apply.

**Next action (one line):** add the MP-signature and SPSR-return sessions to the untracked probe, run it once against
unmodified HEAD (expect EXACTLY the named reds: `kill 14`, `kill 15`, `save 2s`, and the new SPSR row), preserve the run
under `regress/artifacts/armmsrmodekill/`, then the fix round (member 3 shared validator at three sites + latched
defaults), pass-1 brief from the template.  The ledger's ship order ("commit first, then this") is discharged -- #549
is HEAD.

**Priority: HIGH** -- one privileged instruction ends the process today.  Ordering stays below `ip30abortkill` per the
ledger's reachability reading (a correct kernel does not program a reserved mode); that is ordering among HIGHs, not a
demotion.

**MISSED by the answer (mine):** `cpu_arm_instr.c:881-894` -- `X(msr_imm_spsr)`'s `default:` fires for a CURRENT mode
of USR32 or SYS32 (no SPSR) and does `fatal(); printf(); cpu->running = 0`.  The decoder applies no privilege test I can
find, and the USR-only mask at `:826-828` guards `msr_imm`, not `msr_imm_spsr`.  By reading, an UNPRIVILEGED guest
executing `MSR SPSR_c,#0` halts the emulated machine with one instruction.  Different class (halt, not process death;
absent-SPSR mode, not reserved mode), so it is NOT this row: FILE it as its own row with a rung-3 attempt owed
(`testarm`, `MSR CPSR_c,#0x10` to enter USR32, then `MSR SPSR_c,#0`; expect the `msr_spsr: unimplemented mode 16`
line and the CPU stopped).  Needs a witness before it is ranked; by the brief's scale it reads as the hang class.

--------------------------------------------------------------------------------------------------------------------
## 2. `fbctrlcmdkill` -- ADOPT     priority HIGH
--------------------------------------------------------------------------------------------------------------------

**Recommendation as given:** decline unsupported commands behind a SEPARATE per-device `(once)` latch (not
`warned_port`), always `break`; defer FILL/COPY (no operand/geometry/COPY-source semantics exist to implement); record
the corrections listed in its section 5.

**Premises checked at HEAD -- all TRUE:**
* `src/devices/dev_fbctrl.c:63` reads `cmd = port[COMMAND]`; cases at `:68/:71/:88`; `default:` `:101-102`
  `fatal(...); exit(1)`.  Other terminators: `:143-144` (invalid `current_port`, now behind #549's refusal
  `:120-135`, kept as a tripwire `:139-140`), `:158-160` (unknown offset), and `:174` `CHECK_ALLOCATION` ->
  `src/include/misc.h:181-193` (`exit(1)` at `:187`, host OOM only).  No `abort()`.
* The path: DATA arm `:138`, range check `:141-145`, store BEFORE dispatch `:150`, call at `:151-152`.  A fresh device
  is zeroed (`:175`) so `current_port == 0 == COMMAND` at power-on: one `sw` of 3 to `+0x10` is the whole witness.
* Attachment: `src/machines/machine_test.c:154-156` (shared `default_test`) and `:337-339` (testmips) -- every test
  machine.  `dev_fb.h:51-53` marks FILL/COPY `TODO`; `HISTORY:2852-2855` calls fill/copy future work.
* Precedents: `dev_dreamcast_gdrom.c:897-921` (#490 decline, OWN latch bit, `:901-904` says why a shared bit escaped),
  `:887-895` (Mount: silent no-op); `dev_wdc.c:1114-1129` (one line per DEVICE, not per opcode -- the flood bound);
  `dev_ps2_gif.c:384-392` (unlatched `fatal()` per unknown command, `running = 0` commented out -- the flood shape a
  bare delete would produce); `lk201.c:337-339` (`debug()` only); `dev_8259.c:138-140` (`running = 0`);
  `dev_m8820x.c:75-97` (why complain-and-continue, not `running = 0`, for a model gap).  `framebuffer_blockcopyfill`
  `dev_fb.c:269-285`, overlap undefined `:281`.  Access-failure exceptions are MIPS/M88K only: `memory_rw.c:603-624`.
* #549's probe: `regress/fbctrl_port_probe.py` sessions C `:411-416` (GET_RESOLUTION once), A `:423-442` (NOP at port
  0 only), R `:469-476`, V `:492-504`, Y `:534-542`; the disclosure of THIS row at `:156-159`; rows `:608-617`, `:656`
  (COMMAND reads back 2), `:669` (reads back 1).  Gate pin 117 at `regress/gate_mips_folds.sh:99-101`.  Opus walk:
  `regress/artifacts/fbctrlportkill_20260924/opus549_measured/walk_probe.py` (tracked) and `runs/walk_fix.out:29-32`
  -- `+0x10` at widths 1/2/4/8 all `CMD-UNIMPL`.
* The row text, `OUTSTANDING_BUGS.md:22544-22554`: "documented FILL and COPY" (the row itself says "the source marks
  them TODO"), "#549 made one path more direct", "session C already drives COMMAND" -- the answer's three qualifications
  are all fair readings of what the tree shows.
* The C fact: `idata` (`uint64_t`) into `int port[]` at `:150` is implementation-defined for out-of-range values (C99
  6.3.1.3p3), so "any command other than 0-2" is exact of the stored `int`, not of every 64-bit payload.  TRUE and
  worth one clause in the row.

**Premises found FALSE:** none.  Cosmetic: its three exit links anchor at the arm starts (`:101`, `:139`, `:157`) while
the labels give the exit lines (`:102`, `:144`, `:160`); the labels are the correct lines.

**Ruling: ADOPT.**  Member 3 with its own latch is the house idiom and the gdrom #490 precedent is the exact shape;
FILL/COPY are named constants with no specification, and the ADDITION LICENCE does not admit inventing one inside a
fix.  Two things the round must carry that the answer states but does not list as owed rows: (a) the COMMAND cell holds
the refused value after the decline (store-before-dispatch at `:150` is kept) -- pin that readback in a row and write
it into the contract, or the next reader will assume the #549 "previous value kept" shape; (b) one announce per
DEVICE across TWO different unknown opcodes (the wdc `unimpl 2op` shape), and independence from `warned_port` in BOTH
directions (a refused selector must not silence the first command decline, and vice versa -- the gdrom `M3shared`
escape).  Widths `sb/sh/sw/sd` at `+0x10` are in scope per #549's own disclosure.

**Next action (one line):** fix round -- witness first on unmodified `-E testmips` (one `sw` of 3 to `+0x10`; expect
`fbctrl_command: Unimplemented command 3.` then process death; preserve it), then member 3 with `warned_command`, the
probe extended by command-3/4/5 sessions at four widths plus the two rows above, gate pin re-derived from the run.

**Priority: HIGH** -- one unprivileged guest store ends the process today on all six test machines.

**MISSED by the answer (mine):** nothing that changes the disposition.  One records point: the queue's parenthetical
"including the documented FILL and COPY" should read "including the NAMED-but-TODO FILL and COPY" -- the answer says
this; I am only marking it as the one edit the queue text owes now rather than at the round.

--------------------------------------------------------------------------------------------------------------------
## 3. `armthumbabortkill` -- ADOPT WITH CHANGES     priority HIGH (weakest of the three; see below)
--------------------------------------------------------------------------------------------------------------------

**Recommendation as given:** delete only `cpu->running = 0` at each of the five sites, keep `return 0`, let the
already-delivered abort vector run; site 1227 is bypassed for a clean MMU fetch fault; site 1557 additionally
misclassifies a data load as `CACHE_INSTRUCTION`; witness on cold CATS by clearing one L1 descriptor.

**Premises checked at HEAD -- TRUE:**
* The five sites are verbatim as quoted: `src/cpus/cpu_arm.c:1223-1228`, `:1554-1559`, `:1597-1602`, `:1626-1631`,
  `:1650-1655`; each is `fatal(); cpu->running = 0; return 0;`.  The common tail `:1814` is `cpu->pc += 2`.
* Dispatch order: `src/cpus/cpu_dyntrans.c:177-191` runs `DYNTRANS_PC_TO_POINTERS` at function entry; the Thumb test and
  call are at `:255-262` and the interpreter's return value is discarded (`return 1`).  `:670-723`: a PC page with no
  host pointer is translated with `FLAG_INSTR`, and on failure "the PC is now set to the exception handler".  So a clean
  MMU instruction-fetch fault takes PREF_ABT before Thumb dispatch, T is cleared, and site 1227 is never reached --
  CONFIRMED, and it is the ledger's own HOLE 3 (`ledger.json:47363`).
* `memory_rw.c:245-269`: `FLAG_INSTR` only for `CACHE_INSTRUCTION`; a failed translation returns FAILED after the
  exception.  `memory_arm.c:131-149` reads the L1 descriptor fresh from host memory each translation; type 0 ->
  `FAULT_TRANS_S` `:157-159`; `:257-276` delivers PREF_ABT if `instr`, else sets FAR/FSR and DATA_ABT.
  `cpu_arm.c:616-734`: T cleared `:693`, ABT mode `:697-698`, LR `:730`, PC = vector `:731-733`.
* CATS: `machine_cats.c:131` TTB `7*1048576-32768 = 0x006f8000`; `cpu_arm.c:226-256` writes a section descriptor for
  every 1 MB of VA (16 aliases of the low 256 MB) into guest RAM -- writable, as the answer says.  CP15 c8 invalidate:
  `cpu_arm_coproc.c:230-243`.  Cold-CATS MMU-on vehicle exists and is gated: `regress/gate_arm.sh:1072-1073`,
  `:1137-1140`.
* ARM-mode parity sites: `cpu_arm_instr_loadstore.c:233-238` and `:367-372` -- "an exception was generated", set
  `next_ic = &nothing_call` only if `!cpu->running`, `return`.  Thumb push/pop go through `arm_push`/`arm_pop`
  (`cpu_arm.c:1667-1687`), not through these sites.
* Site 1557: `:1554-1555` requests `CACHE_INSTRUCTION` for the `LDR Rd,[PC,#imm]` DATA load -- a real, separate
  misclassification (an MMU fault there becomes PREF_ABT, and per `memory_arm.c:268-269` no FAR/FSR is set).
* Manuals: `ddi0100i.txt:954-960`, `:2194-2228` (Prefetch Abort entry / return), `:2230-2269` (Data Abort entry /
  return), `:20337-20353` (Thumb exceptions switch to ARM, LR values); `ddi0406.txt:56489-56501` ("7. Execution
  continues from the address held in the PC"), `:57197-57213` (TE selects handler state -- ARMv7 only).  All as cited.

**Premise found FALSE -- and it is the one the fix rests on:** *"let the delivered abort vector run"* presumes that every
failure at these five sites HAS delivered an abort.  It has not:
* `memory_rw.c:583-625`: a device whose handler returns 0 makes `memory_rw` return FAILED with NO ARM exception (the
  exception at `:608-623` is MIPS/M88K only).  PC is unchanged, `running` is still 1.
* With `running = 0` deleted and `return 0` kept, the tail's `pc += 2` is skipped, the next `DYNTRANS_RUN_INSTR` call
  re-dispatches the SAME Thumb instruction, it fails identically, and the site's `fatal()` prints again -- an unbounded
  spin with one stderr line per iteration.  That converts today's halt into a HANG plus a flood, which the brief's own
  scale ranks as the class this row exists to remove.
* The ARM-mode "precedent" the answer transfers does not do this: at `cpu_arm_instr_loadstore.c:233-238` `next_ic` has
  already advanced, so a no-exception failure SKIPS the access and continues with the next instruction.  Parity is
  "skip and continue", not "re-execute".
* The out-of-RAM class is NOT this hazard, checked so nobody re-argues it: `src/core/memory.c:605-606` returns false
  within 256 KB past RAM (the access proceeds and reads zeros, `memory_rw.c:681-683`); beyond that it warns and returns
  true ONLY under `halt_on_nonexistant_memaccess`, having already halted every CPU (`:645-654`), so deleting the site's
  assignment changes nothing there.  The live class is a refusing DEVICE reached by Thumb code; the answer's own
  section 5 names that class and then does not carry it into section 3.

**Ruling: ADOPT WITH CHANGES.**  Member 1 is still the disposition -- the architecture requires the handler to run and no
in-tree ARM abort site halts -- but the deletion must be CONDITIONED on the abort having been delivered, and the
no-exception branch must match ARM mode:
1. At each of the four data sites (`:1600`, `:1629`, `:1653`, and `:1557` after item 3): on a failed `memory_rw`, if
   `cpu->pc` changed (equivalently: mode is now ABT32 and T is clear) -> `return 0` as proposed; else fall through to the
   common tail so `pc += 2` runs and the access is skipped -- the `cpu_arm_instr_loadstore.c:233-238` behaviour.  One
   comparison per site, or a four-line helper.  Keep each `fatal()` but LATCH it (`(once)` per CPU) -- unlatched it is
   guest-drivable on the no-exception branch, the #464/#465 flood class.
2. At site `:1227` (instruction fetch): the exception-delivered branch drops the halt exactly as at the others; the
   no-exception branch KEEPS today's halt, because there is no sane continuation from an unreadable instruction and the
   ARM-mode analogue (`cpu_arm_instr.c:4052-4056`, `read failed: TODO`) is itself a known-bad disposition, not a
   precedent to copy.  The ledger already records the clean-fault path as bypassing this site.
3. Site `:1557`'s `CACHE_INSTRUCTION` on a PC-relative DATA load is a different semantic class (wrong abort type and no
   FAR/FSR, vs halt-after-abort).  FILE it as its own row rather than folding it in; the reopening rule is one fix design
   per round, and this round's detector cannot see abort TYPE without a new oracle (FSR/FAR readback).
4. The witness plan (cold CATS, clear the descriptor at `0x006f8004` for VA `0x00100000`, `mcr c8` invalidate, `bx`
   into Thumb, `ldr r0,[r1,#0]`; handler publishes marker + ABT32/T=0 + FAR + FSR=0x05; ARM `LDR` control in a fresh
   process) is sound by reading and answers the ledger's "no unmapped VA on cats" hole: the table is guest RAM.  ADD one
   control cell the plan lacks and item 1 needs: a Thumb load from a REFUSING device (or any in-tree ARM device window
   whose handler returns 0 -- the round greps for one; if none exists on CATS/testarm, say so and the branch is
   disclosed, not rowed) proving the repaired code does not spin.  That is the accept-side row for the predicate the
   fix adds.
5. Records, all confirmed by reading: "five sites ... after the abort is already delivered" -> four reachable after an
   abort plus 1227 on a non-clean path; "reachable by any Thumb guest taking a memory fault" (`ledger.json:47318`) is
   too broad (PUSH/POP bypass, 1227 bypass); the reopen condition ("an MMU-on ARM vehicle") is met by the gated
   cold-CATS footbridge probe -- reopen the witness attempt.

**Next action (one line):** reopen the witness attempt on cold CATS as specified (plus the no-exception control cell),
measure HEAD (halt, handler marker unchanged) and preserve it; then the fix round with the exception-delivered
discriminator and latched diagnostics; file the `:1557` classification row separately.

**Priority: HIGH by the ledger's grading and by the brief's "hang it" clause (a `running = 0` ends the guest's session:
`emul.c:1046-1052` ends the run when no CPU is running) -- but it is the weakest HIGH in this batch: not process death,
Thumb-with-MMU-on only, and no in-tree booting guest is known to take that path.  Keep it behind `ip30abortkill`,
`armmsrmodekill` and `fbctrlcmdkill`.

**MISSED by the answer (mine):** the no-exception branch above is the substantive one.  Two smaller: (i) the four data
sites' `fatal()` calls are UNLATCHED, so any repair that lets execution continue past them turns a guest-repeatable
fault into a per-iteration stderr line -- latch them in the same diff; (ii) `cpu_arm_instr.c:4052-4056` (ARM-mode
instruction read failure: prints and returns without translating, every slot) is the ARM-side sibling of site 1227 and
is a flood/continuation defect of its own; note it in PRETABLE.out's sibling parity line and file if a witness exists.

--------------------------------------------------------------------------------------------------------------------
## 4. `ppcrlwhighhalf` -- ADOPT     priority MED
--------------------------------------------------------------------------------------------------------------------

**Recommendation as given:** build a Book I-based rung-3 witness on `bareppc` (`rlwinm. r4,r3,1,31,0`, r3=1: HEAD
`r4 = 0`, CR0 = EQ; Book I `r4 = 0x0000000200000000`, CR0 = GT), then repair BOTH bases by recovering MB/ME from
`arg[2]` and installing the unmasked 32-bit rotation in the high half when MB > ME; `MODE32` compile guard, no runtime
SF test; records corrections.

**Premises checked at HEAD -- all TRUE:**
* `src/cpus/cpu_ppc_instr.c:2567-2578` `X(rlwnm)` (shift `gpr[rb] & 0x1f` `:2572`, store of masked `uint32_t` at
  `:2576`, `DOT0` `:2578`); `:2588-2598` `X(rlwinm)` (store at `:2596`).  Both zero-extend into a 64-bit `reg()`
  (`generate_tail.c:121-126`; `cpu_ppc.c:120` selects the wide implementation for a 64-bit model).  Two sites, four forms
  via `DOT0` `:208-209`.  Count holds.
* Decoder `:4535-4556`: 32-bit wrapping low mask built from a mutated `mb` (`:4541-4547`), dispatch `:4550`/`:4552`,
  `arg[2] = iword` `:4556`; `mask` is `uint32_t` at `:4074`.  `cpu.h:76`: args are `uintptr_t` (a 64-bit mask cannot
  portably ride in a slot).  The sibling repair exists at `:2639-2640` (`rlwimi`), and `rldimi` keeps its shift and
  cursors separate `:2541-2552`.  `MODE32` idiom at `:3109-3111`.
* Witness facts: `bareppc` defaults to PPC970 (`machine_test.c:448-450`), PVR `0x00390000` (`cpu_ppc.h:87`, installed
  `cpu_ppc.c:100`); `update_cr0` compares at 64 bits when `bits == 64` (`cpu_ppc.c:1803-1813`), so CR0 EQ->GT is the
  right prediction.  Arithmetic re-done: rotate 1 by 1 = 2; MASK(63,32) is bit 63 plus bits 0..32 = `0xffffffff80000001`;
  `(2||2) & mask = 0x0000000200000000`.  496 wrapping / 528 non-wrapping (MB,ME) pairs: 32*31/2 and 496+32.
* Manuals: `ppc_uisa_book1_v201.txt:501-504` (ROTL32 rotates `x||x`), `:578-580` (MASK wraps if x > y), `:4015-4029`
  (64-bit mask wraps 63 -> 0), `:4125-4128` and `:4236-4242` (`m = MASK(MB+32, ME+32)`; `RA = r & m`), `:4195-4196`
  and `:4291-4292` ("For all the uses given above, the high-order 32 bits ... are cleared" -- QUALIFIED), `:342-344`
  (both modes affect all 64 bits); `ppc_pem_32and64_2005.txt:302` (defers to Architecture 2.01), `:30065`
  (unconditional clearing), `:30074` (qualified); `ppc_pem32_rev2_2001.txt:15668` (pseudocode is for 32-bit
  implementations).  All as cited, and identical to the carrier's own Book I entry.
* Gates/probes: `regress/gate_ppc.sh:105-106` runs `ppc_rlwimi_probe.py` and pins 28/28 at `:121-122`, `rldimi` 29/29
  at `:146-147`; that probe's `mask32` is full-width (`:156-159`) and its `rlwinm` control is non-wrapping (`:263`,
  `:284`); HEAD `regress/ppc_rldicl_probe.py:158-167` still carries the low-only `mask32` -- reusing it would rebuild
  the oracle defect.
* Ledger `ledger.json:46273-46279`: `witness: null`, no `entries`; the note's later text reads "RESOLVED 2026-09-10 BY
  FETCHING THE DOCUMENT THE PEM DEFERS TO.  IT IS A DEFECT, NOT A DISPUTE, AND THIS ROW IS RAISED TO HIGH" and carries the
  `:4195` correction -- so the TITLE ("the dispute is unresolved") and `OUTSTANDING_BUGS.md:19175-19189` ("(MED) ...
  DISPUTE rather than a defect ... adopts neither reading") are stale against the same row's own note.  The answer is
  right that these are records errors.
* The ledger note's worked case still says "Same for `X(rlwnm)` when the register shift's low five bits are zero";
  `:2572-2576` show every shift count is affected (the mask is applied after any rotation).  The answer's correction
  is right.

**Premises found FALSE:** none.

**Ruling: ADOPT.**  The design (recover MB/ME from `iword`, keep the rotation at 32 bits, high half = rotated word iff
MB > ME, guarded like `extsb`) is the `rlwimi` idiom already in the file, and the two "shortcuts" it disproves (testing
the decoder's exhausted `mb == me`; inferring wrap from the low mask, since (1,0) and (0,31) both give `0xffffffff`)
are correctly disproved by reading.  The detector list it gives -- both opcodes, both Rc forms, nonzero shifts, equal
endpoints, a NON-wrapping companion (needed to kill unconditional high-word replication), differing source halves,
register aliases (`RA = RS`, `RA = RB`), `rb` = 1 vs 33 -- is the right accept-side set.

**Next action (one line):** build the rung-3 witness on `bareppc` from `ppc_rlwimi_probe.py`'s session helper and its
full-width `mask32` (never the HEAD `rldicl` helper), measure HEAD red (`r4 = 0`, CR0 EQ) and preserve it; then the repair
round for both bases with the row set above; records in the same commit: retitle the row (resolved, defect), correct
the `OUTSTANDING_BUGS.md:19175` header, delete the "low five bits are zero" qualifier.

**Priority: MED** by the brief's scale -- guest-visible results contrary to Book I, no process/memory/hang consequence,
and no in-tree BOOTING guest runs a 64-bit PowerPC model (PPC970 is the bare/test default only).  The ledger's `high`
predates this scale; say so in the records fix rather than silently carrying two words.

**MISSED by the answer (mine):** nothing that changes the disposition.  One caution for the round: `ppcwitnessmaskoracle`
is `in work` and the corrected `ppc_rldicl_probe.py` helper is UNCOMMITTED -- the new witness must not import from that
file in either state; copy the `rlwimi` probe's `mask32` and say so in the probe header.

--------------------------------------------------------------------------------------------------------------------
## 5. `pit8253lsbnotimer` -- ADOPT WITH CHANGES     priority MED
--------------------------------------------------------------------------------------------------------------------

**Recommendation as given:** reconcile with `i8253zero` (one restructure, completion-based recompute, zero = 65536),
witness on stock CATS (four byte stores; HEAD composes `0x40ff` = 16639 -> 72 Hz where `0x4000` = 16384 -> 73 Hz is
required), then IMPLEMENT: clear the SELECTED count register at a programming control word (after the latch early-out),
commit the rate when a load completes; and REDESIGN the shipped `A1` control because it goes red under that clearing.

**Premises checked at HEAD -- TRUE:**
* `src/devices/dev_8253.c:166-170` resolves the half from `mode_byte & 0x30`, using `wr_msb[]` only for `0x30`;
  `:174-177` LSB arm masks `0xff00` and installs nothing; `:178-203` MSB arm masks `0x00ff`, recomputes `hz` `:181-186`,
  creates/retunes `timer0` `:191-197`; `:198`/`:200` are UNLATCHED `fatal("TODO...")` for counters 1/2; `:303-308` latch
  early-out; `:310` ONE shared `mode_byte`; `:311-312`; `:320-321` per-counter rewind.  Two defective write sites, three
  behavioural failures.  Count holds.  `I8253_TIMER_FREQ 1193182` (`i8253reg.h:75`); 1193182/16639 + .5 -> 72,
  /16384 + .5 -> 73; 255 -> 4679 Hz.  Arithmetic re-done.
* Path: `machine_cats.c:63-65` -> `dev_footbridge.c:882-884` (ali_m1543) -> `bus_pci.c:475-478` (ISA at `0x7c000000`)
  -> `bus_isa.c:241-244` (8253 at `+0x40`, `isa.0`) -> `dev_8253.c:386-388`.  `timer.c:136-141`, `:197-210`
  (`t->freq == new_freq` early-out; the clamp complaint is per CHANGE), `:322-329`.  `dev_mc146818.c:448-452` precedent.
* `regress/pit8253_latch_probe.py:111-125`: A1 programs `0x34`, writes `0xAA` then `0x55`, rewrites `0x34` (rewind),
  reads `0xAA`; asserted at `:511`; the probe's own comment `:107-109` says A1 "survives the flip-flop fix on purpose
  ... never doubles as the thing under test".  Gated with an 18-row literal at `regress/gate_arm.sh:1787-1826`.
* Ledger: `pitlsb` `ledger.json:16179-16182` dropped, MERGED into `i8253zero` `:16302-16306` ("TIMER_LSB census: zero
  hits"); `:9443-9447` specifies the helper under a "load complete per programmed format" predicate with count 0 ->
  65536; this row `:47018-47053` -- kimi, opus5, fable5 (09-17) and the 09-18 NOPANEL note.  `OUTSTANDING_BUGS.md:
  19833-19880`, where `:19852-19853` is MY OWN seat's sentence: "clear `counter[sel]` at the CONTROL WORD".
* Datasheet `i8254.txt:15` (8254 is a superset of the 8253), `:168-172` (CRM/CRL cleared when the Counter is
  programmed; other byte zero for one-byte formats), `:219-224`, `:243-249`, `:481-486`, `:528`, `:671-673`.  All as
  cited.  Also read for this ruling: `:149-159` (a read returns the OL, which "follows" the CE; the CE cannot be read
  directly) and `:642-645` (a Control Word resets the Control Logic; nothing says it zeroes the CE).
* `timer.h:81`: `TIMER_MAX_FREQUENCY` is INT_MAX, so an LSB-only count's 4679 Hz never clamps -- a hazard I checked
  and can rule out.

**Premise found FALSE (an inference, and it is the fix placement):** *"the documented control-word clearing" must be
represented by clearing `counter[]` at the control word.*  This model has ONE `counter[]` standing in for CR, CE and OL
together (`dev_8253.c:30-35`: the timers do not count; "split counter[] into reset value and current value" is the
file's own open TODO).  Clearing it at the control word therefore zeroes the model's only counting element, and a read
after ANY control word returns 0 -- which the datasheet's read path never does (the OL follows the CE, `:149-159`; the
control word resets the control logic, `:642-645`, and the count is transferred to the CE only when written, `:164-168`).
A1 goes red under that placement because A1 pins the hardware-true property that a control word does not zero the
count.  So the answer proposes to REDESIGN a shipped, gated control to fit a fix placement that is itself
hardware-wrong -- the oracle-correction rule's laundering shape, reached with good intentions.  I wrote the sentence it
follows, on 09-17, and it was the wrong placement: the datasheet names WHERE the hardware clears its CR; this model has
no CR to clear.

**Ruling: ADOPT WITH CHANGES.**
1. **Placement: the one-byte write ARMS, conditioned on the programmed format, not the control word.**  In the LSB arm:
   if `(mode_byte & 0x30) == I8253_TIMER_16BIT` merge as today, else `counter = idata & 0xff` (MSB zero); in the MSB arm:
   16-bit -> merge, else `counter = (idata & 0xff) << 8`.  The format test already exists in the file at `:259` and
   `:280`.  The composed count and rate are IDENTICAL to the control-word placement for every one-byte load (I derived
   both: `0xff` -> `0x00ff`; `0x40` -> `0x4000`); the two differ only where the model has no hardware-faithful answer
   anyway (a read between a control word and a completed load), and there the arm placement returns the retained count,
   which is what the OL does.  A1 stays green UNTOUCHED.  Do not redesign A1.
2. Keep everything else the answer specifies and the `i8253zero` merge already ordered: hoist recompute +
   `timer_add`/`timer_update_frequency` into one helper called when a load is complete per format (one-byte: every
   write; 16-bit: the MSB), count 0 -> 65536, never on a 16-bit pair's first byte (R6 pins that).
3. **Latch `:198` and `:200` in the same diff.**  Today the LSB arm is silent; routing LSB-only writes on counters 1/2
   through the completion helper makes each one print `TODO: DMA refresh?` / `TODO: 8253 tone generation?` --
   guest-repeatable, unlatched, the flood class (`pit8253flood` is the neighbour).  The answer sees the reach and does not
   name the latch.
4. **Disclose the shared `mode_byte`.**  `:310` stores ONE format byte for all three counters, so the format test in
   item 1 (and the existing `:259`/`:280` tests) answers with the LAST control word written to ANY counter -- the
   `pitclobber` row.  The fix inherits it, must not be blocked on it, and the witness must not interleave counters.
5. Witness as specified (CATS, MMU off via CP15 and read back, the four stores), with the note that the 72/73 Hz line is
   `debug()` (`:187`) -- run at the verbosity that shows it, as the existing probe does (row T counts "8253 log lines").
   The device signature the answer proposes (a completed two-byte pair read back byte-by-byte without another control
   word) is good and additionally does not pre-install `timer0` before the LSB observation.

**Next action (one line):** the fix round for this row TOGETHER with `i8253zero` (one restructure, per the ledger's
`:9445` merge), witness first on stock CATS measured HEAD-red and preserved, A1 untouched, `:198`/`:200` latched, the
shared-format dependency written into the contract; records: correct `OUTSTANDING_BUGS.md:19852-19853` (the fable5
placement sentence) in place, quoting it.

**Priority: MED** by the brief's scale (wrong host timer rate / a never-started counter-0 timer, contrary to the
datasheet); the ledger's MED-HIGH stands as its own record.  No in-tree guest uses LSB-only (`:16304-16306` census), and
the manufacturer's own timing diagrams do (`:528`) -- both true, which is why this is a real fix and not urgent.

**MISSED by the answer (mine):** items 1, 3 and 4 above.  And a self-correction that belongs in the record: the "clear at
the control word" shape was the Fable seat's finding on 09-17, verified by the main loop as a DATASHEET fact -- which it
is -- and adopted as a FIX SHAPE, which it is not, because the model lacks the register the datasheet clears.  A seat
reviewing its own earlier finding is supposed to be harder on it; this is that.

--------------------------------------------------------------------------------------------------------------------
## Cross-cutting notes
--------------------------------------------------------------------------------------------------------------------

* **No answer proposed a CLOSE or a DROP**, so the closure-conditions test (measured detector, or the three OVERTAKEN
  conditions) did not arise in this batch.  Every recommendation is a witness-then-fix; three of the five are amended in
  their fix DESIGN, none in their disposition class.
* **Two answers transferred an ARM-mode precedent without checking what it does on the branch that matters** (Thumb:
  the no-exception failure; PIT: the register the datasheet clears).  Both were found by asking "what happens when the
  thing the fix presumes is FALSE" -- the same question the pre-table CHANNEL line asks of a row.
* **Seat identity for the ledger:** three Daybreak-fallback answers, two Astra.  The refusal itself is a seat-failure
  class already on record (`agentrefusal` is in this farm's own batch); it did not lower answer quality here, but a
  ledger entry crediting "codex" for a Daybreak answer is a wrong record.
* Priorities by the brief's scale: HIGH `armmsrmodekill`, HIGH `fbctrlcmdkill`, HIGH (weakest) `armthumbabortkill`,
  MED `ppcrlwhighhalf`, MED `pit8253lsbnotimer`.  Suggested order of rounds: `fbctrlcmdkill` (cheapest witness, every
  test machine, unprivileged), `armmsrmodekill` (probe exists, one run away), `armthumbabortkill`, then the two MEDs with
  `pit8253lsbnotimer` ahead of `ppcrlwhighhalf` only because it rides on the already-ordered `i8253zero` restructure.

Read-only: this file is the only thing written.  Nothing was built, run, or edited anywhere else.
