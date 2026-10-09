# PASS 1 (design) -- `armmmuvehicle`: an MMU-ON ARM probe vehicle on the unmodified `-E testarm` machine

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.  The working tree also carries an UNCOMMITTED round (`#562`, four ARM files:
`cpu_arm.c`, `cpu_arm_instr.c`, `cpu_arm_instr_dpi.c`, `cpu_arm.h`) that shifts `cpu_arm.c`
by about +42 lines against HEAD `ef577140`; nothing in this brief depends on it.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation: `VERDICT: BUILD AS DESIGNED /
BUILD WITH CHANGES (<n>) / REDESIGN -- <one line>`.

## What this round is, and what it is NOT

This is a **TEST-APPARATUS round**: it changes NO product code.  It builds the first ARM probe
in this tree that runs guest code with the **MMU ON**.  Three filed defects need it as their
vehicle, and none of them is fixed here:

* `armthumbabortkill` (HIGH): five Thumb sites in `cpu_arm.c` set `cpu->running = 0` AFTER an
  MMU abort was already delivered and T cleared, so the guest's abort handler never runs.  Its
  witness was attempted on 2026-09-17 and condemned across 13 holes (summarised in §2 below);
  its recorded reopen condition is exactly this vehicle.
* `armdesc3kill`: an L1 descriptor of type 3 (fine page table) reaches `exit(1)` in the walk.
* `armdacr2kill`: a DACR domain value of 2 reaches `exit(1)` in `arm_check_access`.

**So the vehicle must reach the MMU fault path WITHOUT touching those three defects** -- they are
later rounds, each with its own witness.  The vehicle's own rows pin the MMU behaviour that is
CORRECT today (translation faults, aborts, FAR/FSR), so a mutant of that path reddens them.
Its witness kind is `harness:` -- proved by a kill table over MMU-path mutants, built in a
scratch clone.  Expected score on HEAD: all green (no defect is claimed).

## §1. SETTLED PREMISES (each checked in THIS tree on 2026-10-09; the warrant is named)

1. `-E testarm`'s default CPU is `SA1110` (`machine_test.c`, `MACHINE_DEFAULT_CPU(testarm)`).
   The emulator has NO per-CPU Thumb capability flag: the CPSR T bit alone sends execution to
   `arm_cpu_interpret_thumb_SLOW` (`cpu_dyntrans.c`, `if (cpu->cd.arm.cpsr & ARM_FLAG_T)`).
   *(Source: agy's 2026-10-08 reading, re-checked.)*
2. `MACHINE_SETUP(testarm)` sets `SP = RAM_MB * 1048576 - 4096`, `LR = SP + 32`, and plants a
   three-word halt stub at LR: `0xe3a00201` (`mov r0,#0x10000000`), `0xe5c00010`
   (`strb r0,[r0,#16]`), `0xeafffffe` (`b .`).  With `-M 64` that stub sits at `0x03fff020`, in
   the LAST 1 MB section -- unmapped by any table that maps only section 0.
3. CP15 c1/c2/c3/c8 are NOT settable from the debugger -- the guest must `MCR` them.
   `cpu_arm_coproc.c`: c1 writes `control` and, when the M bit changes, swaps
   `cpu->translate_v2p` between `arm_translate_v2p` (identity) and `arm_translate_v2p_mmu`
   **with no cache invalidation**; c2 stores `r[rd] & 0xffffc000`; c3 stores `r[rd]` whole;
   c5 (FSR) and c6 (FAR) are READABLE AND WRITABLE (`MRC`/`MCR`), so a guest can plant sentinels
   in them; c8 with opcode2 == 0 is `INVALIDATE_ALL`, otherwise `INVALIDATE_VADDR`.
4. Control-register reset (`arm_cpu_new`): `PROG32 | DATA32 | CACHE | ICACHE | ALIGN`, plus
   **exactly one of** `ARM_CONTROL_S` (when `prom_emulation`) or `ARM_CONTROL_R` (otherwise).
   So with AP = 0 the walk's `arm_check_access` returns 1 (read-only) for a privileged access in
   both cases -- **an AP=0 LOAD succeeds and only a STORE takes the permission fault.**
5. Exceptions (`cpu_arm.c`, `arm_exception`; condensed, non-contiguous lines):
   `retaddr = cpu->pc;` ... `case ARM_EXCEPTION_DATA_ABT: retaddr += 4;` ...
   `retaddr += (cpu->cd.arm.cpsr & ARM_FLAG_T ? 2 : 4);` ... `cpsr &= ~ARM_FLAG_T;` ...
   `cpsr |= ARM_FLAG_I;` ... `r[ARM_LR] = retaddr;`
   `pc = exception_nr * 4 + ((control & ARM_CONTROL_V) ? 0xffff0000 : 0);`
   with `ARM_EXCEPTION_PREF_ABT = 3` (vector `0x0c`) and `ARM_EXCEPTION_DATA_ABT = 4` (`0x10`).
   So in ARM state: data abort `LR_abt = pc + 8`, prefetch abort `LR_abt = pc + 4`.
6. The debugger: `put w` goes through `store_32bit_word` (exceptions ENABLED, and it warms the
   dyntrans translation for that page); the byte/halfword `put` paths and `dump` use
   `CACHE_NONE | NO_EXCEPTIONS`.  Entering the debugger calls `cpu_create_or_reset_tc` and
   `invalidate_translation_caches(..., INVALIDATE_ALL)`; it returns early (no invalidation)
   only inside one `step N` / `step call`.  *(#562 measured the consequence: a cached
   translation is only observable by a guest loop that re-runs inside ONE `step N`.)*
7. `regress/arm_msrmode_probe.py` (#562, 47 rows, uncommitted) carries the session machinery a
   vehicle needs: `-A` raw mode, an in-stream `dump` of a DEST word after the guest STRs into
   it, and a `step N` discipline.  `regress/sh4_pcic_probe.py` is the in-tree precedent for an
   IMPORTABLE probe: a gated detector with its own `main()` whose helpers (`session`, `poke`,
   `dumped`, ...) ten other probes `import`.

## §2. THE 13 HOLES THAT CONDEMNED THE 2026-09-17 THUMB SPEC (grok; each re-derived against source)

1. **Plant while the MMU is OFF**, and do not zero the 16 KB table (RAM is already zero; 4096
   `put w` round-trips stall the session).  Plant the descriptors you need, nothing more.
2. **`MCR c8` (invalidate all) AFTER the M bit, always**: enabling the MMU invalidates nothing,
   and a `put w` made while identity was live leaves a warm translation that services a load the
   table says is unmapped.  Prove the hole with debugger `dump UNMAP` (NO_EXCEPTIONS, translates,
   does not warm) -- want `memory access failed`, not the planted word.
3. ARM `BX` to an unmapped Thumb address prefetch-aborts in the GENERIC `pc_to_pointers` before
   the Thumb check, so one of the five Thumb sites (`1227` then) is unreachable by that route.
4. One probe, two row classes (data-abort sites vs prefetch-abort sites); a prefetch abort
   writes NO FAR/FSR, so a prefetch row must not pin them.
5. **No `-T`** (it turns a physical miss into a second halt); `-V` already returns the prompt.
6. A named `LIVE` address, planted with a known word.
7. Values that live only in CP15 or CPSR leave the guest by `MRC`/`MRS` -> `STR` to DEST ->
   `dump`, never by a debugger `print` regex.
8. **An abort is a one-way door into ABT32**: rows after it in the same process run the handler,
   not the stimulus.  One process per abort row; controls share a process that never aborts.
9. Check every planted instruction word against its intended encoding (`enc ok`), or a typo
   reads as the defect.
10. The vector words: at `0x0c` `B` to the prefetch handler, at `0x10` `B` to the data handler
    (`B` is pc + 8 relative -- e.g. `0x0c -> 0x8400` is `0xEA0020FB`, `0x10 -> 0x8500` is
    `0xEA00213A`).
11. **`step N` only, N counted exactly**; never `continue`: after the M bit the testarm LR stub is
    unmapped, so overrunning the handler falls into a PREFETCH abort and a prefetch row reads
    green for the wrong reason.  End each handler in an ARM `b .` inside section 0.
12. Build the session from `arm_msrmode_probe.py`'s machinery (§1.7), not from an older probe's
    dump-once-at-the-end wrapper.
13. (Thumb-specific: `return 0` is load-bearing in any later fix.)

## §3. THE PROPOSED DESIGN -- attack it

**File and shape.**  `regress/arm_mmu_probe.py`: a gated DETECTOR (gate 14, `gate_arm.sh`) with
its own rows, whose plant/arm/flush sequence, handler stubs and parsers are importable by the
three consumer rounds (the `sh4_pcic_probe.py` precedent).  Command line
`gxemul -V -A -E testarm -M 64` -- no `-T`, no `-q` (the fault diagnostic is a channel).

**Memory map** (all code, data, table and handlers inside section 0, VA = PA `0x00000000-0x000fffff`):

| what | address | notes |
|---|---|---|
| L1 table (TTB) | `0x00004000` | 16 KB aligned; only the words below are planted |
| L2 coarse table | `0x00005000` | 1 KB aligned |
| CODE (stimulus) | `0x00008000` | |
| prefetch handler | `0x00008400` | records LR, CPSR, FSR, FAR to DEST, ends in `b .` |
| data handler | `0x00008500` | same |
| DEST (dump target) | `0x00009000` | |
| LIVE word | `0x00009100` | planted `0x11111111` |

**L1 descriptors planted with `put w` while the MMU is OFF** (VA section -> TTB word):

| VA section | TTB word | descriptor | meaning |
|---|---|---|---|
| `0x000xxxxx` | `0x4000` | `0x00000c02` | section, identity, AP=3, domain 0 |
| `0x001xxxxx` | `0x4004` | `0` (not planted) | UNMAPPED -> section translation fault, FSR `0x05` |
| `0x002xxxxx` | `0x4008` | `0x00300c02` | REMAP: VA `0x002xxxxx` -> PA `0x003xxxxx` |
| `0x004xxxxx` | `0x4010` | `0x00005001` | coarse table at `0x5000`, domain 0 |
| `0x005xxxxx` | `0x4014` | `0x00500c22` | section, domain 1 (DACR no-access) -> domain fault, FSR `0x19` |
| `0x006xxxxx` | `0x4018` | `0x00600002` | section, AP=0 (privileged read-only per §1.4) |

L2 at `0x5000`: entry 0 (VA `0x00400000`) = `0x00600ff2` (small page -> PA `0x00600000`, AP0-3 = 3);
entry 1 (VA `0x00401000`) = 0 -> page translation fault, FSR `0x07`.

**Guest arming sequence** (ARM, in CODE): `MCR p15,0,r1,c2,c0,0` (TTB `0x4000`);
`MCR p15,0,r2,c3,c0,0` (DACR `0x00000001`: domain 0 client, domain 1 no-access, **never a 2**);
`MRC p15,0,r0,c1,c0,0`; `ORR r0,r0,#1`; `MCR p15,0,r0,c1,c0,0`; `MCR p15,0,r0,c8,c7,0`; then the
stimulus.  r1/r2 preset by the debugger.

**Rows (proposed).**  Controls (one process, never aborts): `live` (MMU-off load of LIVE);
`mmu bit` (`MRC c1` & 1 via STR+dump); `ttb rd` (`MRC c2` == `0x4000`); `remap` (MMU-on load of VA
`0x00200000` returns the word planted at PA `0x00300000`, NOT the one at PA `0x00200000` -- the
device-signature analog: identity cannot produce it); `page map` (VA `0x00400000` -> PA
`0x00600000`'s word); `hole dump` (debugger `dump 0x00100000` after the M bit fails).
Abort rows, ONE PROCESS EACH: `data trans` (LDR VA `0x00100000`: FAR `0x00100000`, FSR `0x05`,
mode `0x17`, LR = faulting pc + 8, handler ran); `pref trans` (`B` to `0x00100000`: LR = target
+ 4, mode `0x17`, FSR and FAR still equal to sentinels the guest planted with `MCR c5/c6` first);
`page trans` (LDR VA `0x00401000`: FSR `0x07`); `domain` (LDR VA `0x00500000`: FSR `0x19`);
`perm` (STR to VA `0x00600000`: FSR `0x0d`; plus an AP=0 LOAD that SUCCEEDS, as its accept row).
Plus `enc ok` over every planted instruction word and descriptor, and identity rows.

## §4. THE CODE THE VEHICLE EXERCISES -- `src/cpus/memory_arm.c`, VERBATIM (`arm_check_access` and `arm_translate_v2p_mmu`)

```c
/*
 *  arm_check_access():
 *
 *  Helper function.  Returns 0 for no access, 1 for read-only, and 2 for
 *  read/write.
 */
static int arm_check_access(struct cpu *cpu, int ap, int dav, int user)
{
	int s, r;

	switch (dav) {
	case 0:	/*  No access at all.  */
		return 0;
	case 1:	/*  Normal access check.  */
		break;
	case 2:	fatal("arm_check_access(): 1 shouldn't be used\n");
		exit(1);
	case 3:	/*  Anything is allowed.  */
		return 2;
	}

	switch (ap) {
	case 0:	s = (cpu->cd.arm.control & ARM_CONTROL_S)? 1 : 0;
		r = (cpu->cd.arm.control & ARM_CONTROL_R)? 2 : 0;
		switch (s + r) {
		case 0:	return 0;
		case 1:	return user? 0 : 1;
		case 2:	return 1;
		}
		fatal("arm_check_access: UNPREDICTABLE s+r value!\n");
		return 0;
	case 1:	return user? 0 : 2;
	case 2:	return user? 1 : 2;
	}

	/*  "case 3":  */
	return 2;
}


/*
 *  arm_translate_v2p_mmu():
 *
 *  Return values:
 *	0  Failure
 *	1  Success, the page is readable only
 *	2  Success, the page is read/write
 *
 *  If this is a 1KB page access, then the return value is ORed with
 *  MEMORY_NOT_FULL_PAGE.
 */
int arm_translate_v2p_mmu(struct cpu *cpu, uint64_t vaddr64,
	uint64_t *return_paddr, int flags)
{
	unsigned char *q;
	uint32_t addr, d=0, d2 = (uint32_t)(int32_t)-1, ptba, vaddr = vaddr64;
	int instr = flags & FLAG_INSTR;
	int writeflag = (flags & FLAG_WRITEFLAG)? 1 : 0;
	int useraccess = flags & MEMORY_USER_ACCESS;
	int no_exceptions = flags & FLAG_NOEXCEPTIONS;
	int user = (cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_USR32;
	int domain, dav, ap0,ap1,ap2,ap3, ap = 0, access = 0;
	int fs = 2;		/*  fault status (2 = terminal exception)  */
	int subpage = 0;

	if (useraccess)
		user = 1;

	addr = ((vaddr & 0xfff00000ULL) >> 18);

	if (cpu->cd.arm.translation_table == NULL ||
	    cpu->cd.arm.ttb != cpu->cd.arm.last_ttb) {
		cpu->cd.arm.translation_table = memory_paddr_to_hostaddr(
		    cpu->mem, cpu->cd.arm.ttb & 0x0fffffff, 0);
		cpu->cd.arm.last_ttb = cpu->cd.arm.ttb;
	}

	if (cpu->cd.arm.translation_table != NULL) {
		d = *(uint32_t *)(cpu->cd.arm.translation_table + addr);
#ifdef HOST_LITTLE_ENDIAN
		if (cpu->byte_order == EMUL_BIG_ENDIAN)
#else
		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
#endif
			d = ((d & 0xff) << 24) | ((d & 0xff00) << 8) |
			    ((d & 0xff0000) >> 8) | ((d & 0xff000000) >> 24);
	}

	/*  Get the domain from the descriptor, and the Domain Access Value:  */
	domain = (d >> 5) & 15;
	dav = (cpu->cd.arm.dacr >> (domain * 2)) & 3;

	switch (d & 3) {

	case 0:	domain = 0;
		fs = FAULT_TRANS_S;
		goto exception_return;

	case 1:	/*  Course Pagetable:  */
		if (dav == 0) {
			fs = FAULT_DOMAIN_P;
			goto exception_return;
		}
		ptba = d & 0xfffffc00;
		addr = ptba + ((vaddr & 0x000ff000) >> 10);

		q = memory_paddr_to_hostaddr(cpu->mem, addr & 0x0fffffff, 0);
		if (q == NULL) {
			/*  #193: (Codex/Fable) an L2 page-table page outside mapped
			    RAM must fault the guest, not exit() the host.  */
			fs = FAULT_TRANS_P;
			goto exception_return;
		}
		d2 = *(uint32_t *)(q);
#ifdef HOST_LITTLE_ENDIAN
		if (cpu->byte_order == EMUL_BIG_ENDIAN)
#else
		if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
#endif
			d2 = ((d2 & 0xff) << 24) | ((d2 & 0xff00) << 8) |
			     ((d2 & 0xff0000) >> 8) | ((d2 & 0xff000000) >> 24);

		switch (d2 & 3) {
		case 0:	fs = FAULT_TRANS_P;
			goto exception_return;
		case 1:	/*  16KB page:  */
			ap = (d2 >> 4) & 255;
			switch (vaddr & 0x0000c000) {
			case 0x4000:	ap >>= 2; break;
			case 0x8000:	ap >>= 4; break;
			case 0xc000:	ap >>= 6; break;
			}
			ap &= 3;
			*return_paddr = (d2 & 0xffff0000)|(vaddr & 0x0000ffff);
			break;
		case 3:	if (cpu->cd.arm.cpu_type.flags & ARM_XSCALE) {
				/*  4KB page (Xscale)  */
				subpage = 0;
			} else {
				/*  1KB page  */
				subpage = 1;
				ap = (d2 >> 4) & 3;
				*return_paddr = (d2 & 0xfffffc00) |
				    (vaddr & 0x000003ff);
				break;
			}
			/*  NOTE: Fall-through for XScale!  */
			// fall through
		case 2:	/*  4KB page:  */
			ap3 = (d2 >> 10) & 3;
			ap2 = (d2 >>  8) & 3;
			ap1 = (d2 >>  6) & 3;
			ap0 = (d2 >>  4) & 3;
			switch (vaddr & 0x00000c00) {
			case 0x000: ap = ap0; break;
			case 0x400: ap = ap1; break;
			case 0x800: ap = ap2; break;
			default:    ap = ap3;
			}
			/*  NOTE: Ugly hack for XScale:  */
			if ((d2 & 3) == 3) {
				/*  Treated as 4KB page:  */
				ap = ap0;
			} else {
				if (ap0 != ap1 || ap0 != ap2 || ap0 != ap3)
					subpage = 1;
			}
			*return_paddr = (d2 & 0xfffff000)|(vaddr & 0x00000fff);
			break;
		}
		access = arm_check_access(cpu, ap, dav, user);
		if (access > writeflag)
			return access | (subpage? MEMORY_NOT_FULL_PAGE : 0);
		fs = FAULT_PERM_P;
		goto exception_return;

	case 2:	/*  Section descriptor:  */
		if (dav == 0) {
			fs = FAULT_DOMAIN_S;
			goto exception_return;
		}
		*return_paddr = (d & 0xfff00000) | (vaddr & 0x000fffff);
		ap = (d >> 10) & 3;
		access = arm_check_access(cpu, ap, dav, user);
		if (access > writeflag)
			return access;
		fs = FAULT_PERM_S;
		goto exception_return;

	default:fatal("TODO: descriptor for vaddr 0x%08x: 0x%08x ("
		    "unimplemented type %i)\n", vaddr, d, d&3);
		exit(1);
	}

exception_return:
	if (no_exceptions)
		return 0;

	if (!quiet_mode) {
		fatal("{ arm memory fault: vaddr=0x%08x domain=%i dav=%i ap=%i "
		    "access=%i user=%i", (int)vaddr, domain, dav, ap,
		    access, user);
		fatal(" d=0x%08x d2=0x%08x pc=0x%08x }\n", d, d2, (int)cpu->pc);
	}

	if (instr)
		arm_exception(cpu, ARM_EXCEPTION_PREF_ABT);
	else {
		cpu->cd.arm.far = vaddr;
		cpu->cd.arm.fsr = (domain << 4) | fs;
		arm_exception(cpu, ARM_EXCEPTION_DATA_ABT);
	}

	return 0;
}
```

## §5. QUESTIONS -- answer as `<n> | <answer>`

1. **Premise audit -- each premise below is a QUESTION, not a fact:**
   a. After a DATA abort sets `pc = 0x10` with only section 0 mapped (identity), does the next
      fetch reach the handler through the SAME translation, or is there a path that fetches the
      vector some other way (a physical fetch, a cached pointer from before the M bit, or the
      generic `pc_to_pointers` "could not find physical address of the exception handler" exit in
      `cpu_dyntrans.c`)?
   b. Does `MCR c8` INVALIDATE_ALL drop EVERYTHING that could serve a stale translation -- the
      dyntrans `host_load`/`host_store` pages AND any cached instruction-translation pages -- so that
      a `put w` made while identity was live cannot service a load after the flush?  Note
      `arm_translate_v2p_mmu` caches only the L1 table's HOST POINTER (keyed on `ttb != last_ttb`)
      and reads every descriptor fresh.
   c. With the MMU on and only section 0 mapped, does any step of a debugger-driven session touch
      an unmapped address implicitly -- the testarm halt stub at `0x03fff020`, a console device,
      `step`'s own disassembly of the next instruction, the debugger's pc/register display?
   d. Is §1.4 right that one of S/R is always set at reset, so an AP=0 section is privileged
      READ-ONLY and only a store faults?  Is `prom_emulation` set for `-E testarm`, and does it
      matter here?
   e. ENUMERATE each fault row's FSR from the verbatim walk in §4: `0x05`, `0x07`, `0x19`, `0x0d`.
      Note that `case 0:` zeroes `domain` but the coarse-table `case 0:` (`d2 & 3 == 0`) does
      not -- what is the page-translation-fault FSR if the coarse descriptor named domain 3?
   f. After a data abort inside a `step N`, the remaining steps execute the handler (§2.8).  Is
      there any instruction in an abort handler that could itself fault with only section 0
      mapped, giving a nested abort that overwrites `LR_abt`/`SPSR_abt` before DEST is written?
2. **The smallest edit that breaks the MMU fault path and keeps the proposed rows green.**  Name
   the edit and the row you expect to stay green.  Candidates to consider, not a closed list: the
   FAR assignment dropped; `domain << 4` dropped or shifted; `FAULT_TRANS_S` and `FAULT_TRANS_P`
   swapped; the `case 0:` domain zeroing removed; `PREF_ABT`/`DATA_ABT` swapped; `retaddr += 4`
   removed; the section base mask `0xfff00000` narrowed; the coarse index shift `>> 10` changed;
   c8 made a no-op; c2's `& 0xffffc000` removed; the `ttb != last_ttb` re-resolution removed.
3. **Option-set completeness.**  (i) PACKAGING: one importable gated probe (the `sh4_pcic_probe.py`
   precedent), or a probe plus a separate helper module, or a self-contained probe the consumer
   rounds copy?  Grep `regress/` for how importable probes are wired into `check_probe_wiring.py`.
   (ii) ROW SET: is there a behaviour one of the three consumer rounds will need that these rows do
   not establish -- e.g. high vectors (c1.V, `0xffff0000`), a mapped-code Thumb entry by `BX`, a
   USR-mode access, a second process re-planting after an abort?  (iii) Is anything here going to
   reach `armdesc3kill` (type-3 descriptor), `armdacr2kill` (DACR value 2) or the vector-fetch
   exit by accident?  (iv) Any member this brief did not name.
4. **Session plan.**  Which rows can share a process, what exact `step N` each abort row needs
   (arming + stimulus + handler up to its `b .`), and how a row proves it ran the step count it
   claims (a DEST word the LAST handler instruction writes is the obvious marker -- is it enough?).

**If, while verifying a claim, you found something ELSE -- say so.**  (One candidate the brief's
author noticed and has NOT verified: in Thumb state a DATA abort gets `retaddr = pc + 4 + 2`,
i.e. `LR_abt = pc + 6`, where DDI 0100I's data-abort entry gives the aborted instruction + 8 in
both states.  It is out of this round's scope -- `armthumbabortkill`'s round owns it -- but say
whether it is true.)


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
