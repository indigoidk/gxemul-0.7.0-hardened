# NOTES -- T36 / `m88kbuserrregs` pass-1 brief: inconsistencies found while drafting

Drafted 2026-10-23 against HEAD `7fca7187`.  It compares three sources: the seat answers
(`regress/artifacts/research_20261022/crit_20261022/codex_rescrit.txt` = GPT-6 Astra, `grok_crit.txt` = Grok 4.7,
and the merged ruling `CRIT_RULINGS.md`:14), the witness (`regress/artifacts/m88kbuserrregs/witness_20261023/`,
UNTRACKED at HEAD) and the source at HEAD.  Repo paths are relative to `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC`.
Each item gives the disagreement by file:line, then where the brief carries it.  Nothing here was fixed, built
or run; the drafter made no variants.  Items are ordered by how much the round depends on them.

## 1. A fourth product file that nobody names: `src/cpus/cpu_m88k.c`

* Ruling: `CRIT_RULINGS.md`:14 places the writes in the refused-device arm (`memory_rw.c`) and the LUNA case
  (`dev_luna88k.c`:624-627).  Witness: "the three files the round will edit" are `memory_rw.c`, `dev_luna88k.c` and
  `dev_m8820x.c` (`WITNESS_REPORT.md`:22).
* Source: the arm compiles inside `cpu_m88k.c`'s translation unit (`cpu_m88k.c`:1685 includes `tmp_m88k_tail.c`,
  whose :38-40 is `#define MEMORY_RW m88k_memory_rw` / `#define MEM_M88K` / `#include "memory_rw.c"`).
  `cpu_m88k.c`:53-55 includes only `m8820x_pte.h`, `m88k_dmt.h` and `mvmeprom.h`.  `git grep 'm8820x\.h' HEAD -- src`
  finds only `memory_m88k.c`:46, `dev_luna88k.c`:71, `dev_m8820x.c`:42 (plus a comment at :342), `dev_mvme187.c`:44
  and the header itself.  `CMMU_PFSR`, `CMMU_PFAR` and `CMMU_PFSR_BERROR` are defined only in
  `src/include/thirdparty/m8820x.h`:65-66 and :125.  `memory_m88k.c` is its own object: it is not on the
  `cpu_m88k.o:` dependency line (`src/cpus/Makefile.skel`:128-129).  `tmp_m88k_tail.c` is generated
  (`Makefile.skel`:140-141), so it cannot be where the include lands.
* Port source: upstream added `#include "thirdparty/m8820x.h"` to `cpu_m88k.c`
  (`regress/artifacts/research_20261022/trunk_src.diff`:1917-1922).  Neither seat and not the ruling cites that hunk.
* `est/src/cpus/cpu_m88k.c` is byte-identical to HEAD and is not in `tools/est_divergence.txt`, so it is a shared
  file (C0 part 5).
* **Disposition:** settled as fact S16 and asked as premise question P1 (do the macros collide with anything; does
  the file join the edit set and the two-part clearance).  Q1 depends on it.

## 2. The instruction label of the selector the fix adds cannot be seen free-running

* Grok (`grok_crit.txt`:42): "A second cell reads `cmmu[0]` after an instruction fetch."  Astra
  (`codex_rescrit.txt`:37) lists "instruction refusals" among the required observations.
* Witness: R1 (`WITNESS_REPORT.md`:145-148) and the probe contract (`m88k_buserr_probe.py`:157-162).  Free-running,
  the fetch takes vector 2.  Then the translator's read failure (`src/cpus/cpu_m88k_instr.c`:2989-2993) reaches the
  dyntrans `bad:` tail (`src/cpus/cpu_dyntrans.c`:1983-2014) before the vector runs.  Stepped, vector 2 comes only from
  the step loop's own disassembly pre-read (`cpu_dyntrans.c`:287-290: `CACHE_INSTRUCTION` without `NO_EXCEPTIONS`;
  this is R2), which is an artifact of single-stepping.  The witness does not claim the cell (NOT CLAIMED).
* **Disposition:** P5 and Q2: is this label a floor axis of the edited guard, and is the stepped route admissible,
  or is it clause-(e) with R1 as the derivation, or should R1 be sequenced first?  R1 and R2 go to Q4 by id.

## 3. The `no_exceptions` cell: the witness gives the device call as its reason, but the cell is about the arm's guard

* Witness (`m88k_buserr_probe.py`:156): NOT CLAIMED because "the debugger's put/dump/unassemble never reach a
  DM_DEFAULT handler, memory_rw.c:584".  Astra (`codex_rescrit.txt`:37) requires "suppressed exceptions".
* Source: the stated reason is true of the device call (`memory_rw.c`:584-585; all three refusing devices register
  `DM_DEFAULT`: `dev_unreadable.c`:49-51, `dev_vme.c`:241-243, `dev_luna88k.c`:990-992).  The arm itself is still
  reached for those callers.  `res` stays 0 (:583) and becomes -1 (:595-596), and only the arm's own `!no_exceptions`
  term (:603) keeps them out.  The debugger's reads pass `CACHE_NONE | NO_EXCEPTIONS`
  (`src/debugger/debugger_cmds.c`:716-717).  So the cell exists on an unmodified machine, and the repaired writes
  depend on its guard term.
* **Disposition:** P6 and Q2: is a row owed?  If the cell is disclosed instead, the disclosure has to give the
  right reason.

## 4. The sibling CMMU: the ruling says "keep"; HEAD's translation path says "reset"

* Grok (`grok_crit.txt`:34): "Do not clear the sibling."  The witness pins it as `kept` in its four `icmmu` rows
  (`WITNESS_headbin.out`:13, 17, 21, 27) and labels that want as the ruling's premise, which a contrary decision would
  change (`m88k_buserr_probe.py`:170-171).  Astra says nothing about the sibling.
* Source: HEAD's translation-fault writer sets the faulting CMMU's PFSR and resets the other CMMU's PFSR to SUCCESS
  (`src/cpus/memory_m88k.c`:382-384).  OpenBSD 2.2 saves both PFSRs on exception entry
  (`C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\sys\arch\mvme88k\mvme88k\eh.S`:1013-1018).  Its user-fault path
  branches when EITHER one is BERROR (`...\mvme88k\trap.c`:405-411), and it never writes the hardware PFSR.
* **Disposition:** P3 and Q1: can a stale sibling change what the guest does, and on what warrant is `kept` right?

## 5. The absent-CMMU cell: Astra requires an observation; the drafter's reading is that no unmodified machine reaches it

* Astra (`codex_rescrit.txt`:37): "absent CMMU".  Ruling: "NULL check around the two writes only".  Witness: NOT
  CLAIMED (`m88k_buserr_probe.py`:154-155).
* Source: CMMUs are attached only by `dev_mvme187.c`:136-149 and `dev_luna88k.c`:934-965.  On MVME187 that is the
  bootstrap cpu, the only one started (`src/core/emul.c`:747-748); on LUNA-88K it is every cpu below `ncpus`.  The
  88110 machines and mvme188 attach none (`cpu_m88k.c`:340-342).  Among those, testm88k has one device that can
  refuse, at `dev_fb.c`:719-721 (an access past `framebuffer_size`).  It is fenced twice: `memory_rw.c`'s end-of-device
  clamp (:495-523) and `#182`'s length update (`dev_fb.c`:205-212, through `memory_device_update_length`,
  `src/core/memory.c`:354-375).
* **Disposition:** P4 and Q1.  The NULL check then rests on a transferred warrant (upstream; `memory_m88k.c`:131-132).
  Witness-ladder clause (iii) forbids adding a machine just to reach the site.

## 6. The accept row: Grok proposes a population-2 decline; the witness uses a cased register

* Grok (`grok_crit.txt`:42): "An accept row: a population-2 decline still returns success and does not write PFSR."
* Witness: `ok route` and `ok regs` load VME VBR at 0xfff40088, a CASED register served by `dev_vme.c`:144
  (`m88k_buserr_probe.py`:83-84, 105-108, 498-506).  A population-2 decline goes through a different arm of the same
  device (`dev_vme.c`:150-205).
* **Disposition:** P11 and Q2: which accept row or rows are owed?

## 7. PFAR's low two bits are not established, and the witness cannot tell them apart

* Ruling and Grok: PFAR = `orig_paddr` (`CRIT_RULINGS.md`:14; `grok_crit.txt`:42), which is a BYTE address
  (`memory_rw.c`:437).  Upstream's arm writes the same value (`trunk_src.diff`:4677).
* Against it: DMA0 holds the word address (`src/cpus/cpu_m88k_instr_loadstore.c`:131, `addr & ~0x3`), and the data
  P bus carries a word address plus byte enables (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\mc88100.txt`:7870-7874).
  The MC88200 manual is not on disk (`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\vmesbcp2.txt`:139 names it as a related
  document).
* Witness: all three refused addresses are word-aligned (0xfff46010, 0xfff40090, 0x3ffffff0), and the contract lists
  sub-word accesses as NOT CLAIMED (`m88k_buserr_probe.py`:165-166).
* **Disposition:** P2 and Q1(b): answer with a warrant, or say UNKNOWN.

## 8. One in-code citation is already stale at HEAD, and three comments become incomplete with the fix

* `src/devices/dev_m8820x.c`:326 cites `dev_luna88k.c:614` for the LUNA PFSR write.  The write is at
  `dev_luna88k.c`:626 (the case label is at :624).
* After the fix `memory_rw.c` also writes both registers, so these comments stop being complete:
  `dev_m8820x.c`:293-294 ("the model writes only PFSR and PFAR (memory_m88k.c:382-405)"), :325-327, and :500-501
  ("PFSR and PFAR written at :382-405").
* **Disposition:** P9 (the witness's third edited file is presumably for these comments; the brief asks whether they
  are L4 in this diff).

## 9. The LUNA half changes what a booting guest sees, and nobody has measured it

* Ruling: the 0x3ffffff0 case returns 0 through the repaired path (`CRIT_RULINGS.md`:14), so a load that HEAD serves
  (`dev_luna88k.c`:624-627, tail :927-930) will fault.  Upstream replaced the case with a failing RAM device, with the
  comment "Guest OSes such as OpenBSD probe memory by reading 0x3ffffff0" (`trunk_src.diff`:5373-5375).
* No OpenBSD/luna88k source is on disk: `C:\DocumentNoSnc\cc\GXEMUL\_guest-src-openbsd22\sys\arch\` has `mvme88k`
  and no `luna88k`.  Gate 11 skips without the luna rig image (`regress/gate_m88k_rounding.sh`:32-39).  The luna
  boot-to-`login:` leg is in gate 7 (battery).
* **Disposition:** P8 and Q1(f).

## 10. R1's wording versus the source (wording only)

* `WITNESS_REPORT.md`:146 says the `bad:` tail "stops every cpu".  The tail sets `cpu->running = 0` for the faulting
  cpu only (`cpu_dyntrans.c`:2014), sets the global `about_to_enter_single_step = true` (:2002) and calls
  `debugger_reset()` (:2021).  The emulator drops to the debugger, and only the faulting cpu is marked not running.
  On MVME187 (one started cpu) the effect is the same.
* **Disposition:** R1 is carried verbatim, by id; the source is quoted in brief section 8.10.  This is not a finding.

## 11. Records state

* The witness baseline is `66920157` (`WITNESS_REPORT.md`:21); HEAD is `7fca7187`, a records-only commit.
  `git log 66920157..HEAD -- src regress/*.py regress/*.sh` is empty.  **Disposition:** C0 part 0; the witness holds
  at HEAD.
* The witness directory has 0 tracked files.  The ledger row still says witness `none`, commits `''`, no stages, and
  the row is identical in HEAD and the working tree.  **Disposition:** C0 verdict; recording the witness is the
  round's job.
* The carrier and the template are ahead of HEAD in the working tree.  `tools/CLAUDE.md` is 4104 lines there
  (byte-identical to the root `C:\DocumentNoSnc\cc\GXEMUL\CLAUDE.md`) against 3846 at HEAD; `tools/BRIEF_TEMPLATE.md`
  is 854 against 702.  The 2026-10-09 clause-(c) block and rule D2, quoted in the brief as R2 and R8, exist only in
  the working tree.  **Disposition:** provenance is stated in brief section 10.
* These working-tree files differ from HEAD (`cmp` against `git show HEAD:`): `src/devices/dev_pcc2.c` and
  `src/include/thirdparty/mvme_pcctworeg.h` (both on MVME187), `regress/gate_offline.sh`,
  `tools/pipeline/check_probe_wiring.py`, and records in flight (`tools/pipeline/ledger.json`, nine other rows;
  `tools/pipeline/matrix.html`).  Every source file the brief cites is byte-identical to HEAD.  The witness built
  from HEAD blobs for the peer files (`WITNESS_REPORT.md`:25-26); `build/` still carries them.  **Disposition:** the
  FULL brief's section 0 names all four.

## Checked and consistent (so nobody re-derives them)

* The ledger row's citations `memory_rw.c`:437, :494 and :603-624 match HEAD; both seats' corrections to the crit
  packet (`orig_paddr` saved at :437, made device-relative at :494) hold.
* `vme_default_probe.py` reads neither register.  No top-level `regress/*.py` at HEAD mentions PFSR or PFAR (107
  files, 0 hits), so Grok's "those oracles stay green" (`grok_crit.txt`:38) holds.
* Upstream's beyond-RAM hunk (`trunk_src.diff`:4739-4755) writes both registers on the UNCLAIMED path with the
  exception commented out.  The ruling refuses it (S18), and the witness's INFO `unclaimed` row shows HEAD writes
  nothing there (R3).
* `memory_m88k.c`:383 dereferences the sibling CMMU without a NULL test.  It runs only after a translation fault,
  which needs a non-NULL faulting CMMU (:130-132), and both CMMUs are always attached together.  This is an
  observation, not this round's (S9).
