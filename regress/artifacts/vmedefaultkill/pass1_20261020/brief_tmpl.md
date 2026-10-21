# `vmedefaultkill` (HIGH) -- PASS 1 (design): `dev_vme.c`'s `default:` arm ends the emulator; the owner has ruled the disposition per population, and this pass reviews the IMPLEMENTATION SKETCH and the DETECTOR PLAN before any edit

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not
just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from
something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/` AT COMMITTED HEAD `5dbc000e`.**  There are THREE
pristine-2021-upstream copies of GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).
They are NOT this fork.  If your line numbers disagree with mine by hundreds you are reading one of them -- say so rather
than reconciling.  Nothing of this round is edited yet: `src/devices/dev_vme.c` is byte-identical to the upstream import.

**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from
this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim -- an offset set, a count of reachable addresses -- ENUMERATE it rather than
reasoning about it.**  Walk the values.  **And ENUMERATE THE RIGHT DOMAIN -- a domain is itself a premise**: ask what the
PRODUCER of these values can emit (here: which `relative_addr` / `len` pairs the m88k load/store path can deliver) before
you walk them.

**VERDICT LINE FIRST**, so your answer survives truncation.

## 1. The defect, and what is already decided

`src/devices/dev_vme.c`, `DEVICE_ACCESS(vme)` (inlined in full in section 4): the switch on the raw byte offset
`relative_addr` names TEN offsets; every other offset in the 4 KiB window reaches `default:`, which prints with
`debug()` and calls `exit(1)`.  `debug()` returns early at default verbosity while the emulator is free-running
(`src/core/debugmsg.c`: `if ((quiet_mode && !ss) || v < 0) return;`; `fatal()` has no such early-out), so the process
ends with NO visible reason.  The device is installed only on `-E mvme88k -e mvme187` (`machine_mvme88k.c`:
`snprintf(tmpstr, sizeof(tmpstr), "vme addr=0x%x", VME2_BASE);`, window 0xfff40000-0xfff40fff).

**The disposition is NOT open in this pass -- two owner rulings settled it (section 3, S2 and S3).**  This pass reviews
whether the SKETCH implements those rulings correctly against the function's real control flow, and whether the DETECTOR
PLAN meets the project's vacuity floor.  Arguing a different disposition is out of scope unless you can show the sketch
cannot implement the ruled one -- if so, say exactly why.

## 2. The populations -- DERIVED at brief-writing time (2026-10-20, HEAD 5dbc000e), not transcribed

Deriver: a python pass over `src/include/thirdparty/mvme88k_vme.h` (every `#define VME2_* <value>`) against the switch's
case labels in `dev_vme.c`.  Its raw output for word-aligned values below 0x1000 (several header names share a value
because the header also defines bit masks and shift counts; the REGISTER names are the struct-offset ones):

{CENSUS}

| population | definition | members |
|---|---|---|
| CASED (10) | offsets the switch names | 0x00 (`case 0:`), 0x2c GCSRCTL, 0x4c TCR, 0x50 T1CMP, 0x54 T1COUNT, 0x60 TCTL, 0x6c IRQEN, 0x80 IRQL3, 0x84 IRQL4, 0x88 VBR |
| **2** (26) | register WORD STARTS the header names, with NO case | 0x04 SADDR2, 0x08 SLAVELMOD1, 0x0c SLAVELMOD2, 0x10 SLAVECTL, 0x14 MASTER1, 0x18 MASTER2, 0x1c MASTER3, 0x20 MASTER4, 0x24 MASTER4MOD, 0x28 MASTERCTL, 0x30 DMACTL, 0x34 DMAMODE, 0x38 DMALADDR, 0x3c DMAVMEADDR, 0x40 DMACOUNT, 0x44 DMATABLE, 0x48 DMASTAT, 0x58 T2CMP, 0x5c T2COUNT, 0x64 PRESCALE, 0x68 IRQSTAT, 0x70 SETSOFTIRQ, 0x74 IRQCLR, 0x78 IRQL1, 0x7c IRQL2, 0x8c MISC |
| **1** (988 words) | word starts the header does NOT name | 0x90 .. 0xffc |
| **3** (filed, `vmewidthlanes`) | sub-word starts INSIDE the ten cased words | e.g. a byte at 0x51 (inside T1CMP) |
| **4** (filed, `vmewidthlanes`) | a CASED base accessed at len != 4 | e.g. `st.b` at 0x88 stores into the whole VBR word |

**A population this table does NOT classify, and the sketch below decides it implicitly: sub-word starts inside
POPULATION-2 words** (e.g. a byte at 0x29, inside MASTERCTL).  See Q4.

**The in-tree guest's accesses** (OpenBSD 2.2, `_guest-src-openbsd22/sys/arch/mvme88k/dev/vme.c`, re-derived by grep at
brief-writing time; every `struct vme2reg` field in `dev/vme.h` is `volatile u_long`, so every access is word-width):

{GUEST}

Six of the 26 population-2 registers are travelled (MASTERCTL r/w, MASTER3/MASTER4/MASTER4MOD w at attach; IRQSTAT r and
IRQCLR w in the abort handler), seven access sites.  `vmematch()` reads no VME register.  The guest makes no
population-1 access and no sub-word access.

## 3. SETTLED PREMISES (re-inlined so nobody spends an answer re-deriving them)

* **S1 -- `dev_vme.c` is untouched since the upstream import.**  `git log -- src/devices/dev_vme.c` lists one commit,
  `39748e3c Import GXemul 0.7.0`.
* **S2 -- OWNER RULING 2026-09-11, population 1: FAULT (`return 0`).**  `memory_rw.c` converts a device handler's
  `return 0` into an m88k data-access exception (section 4b).  Justified as *"an access the emulator cannot service"*,
  NOT as a claim about the real VMEchip2 (whose register chapter is not on disk: the local `vmesbcp2.txt` lacks
  chapter 4).
* **S3 -- OWNER RULING 2026-10-09, population 2: DECLINE + ANNOUNCE ONCE** -- verbatim from `OUTSTANDING_BUGS.md`'s
  2026-10-09 entry: *"OWNER: population 2 -> DECLINE + ANNOUNCE ONCE (reads 0, writes dropped, one `fatal()` per
  register, `(once)` marker); population 1 keeps FAULT."*  It names `#501`'s shape (section 4c).  BACKED ACCEPT (inventing
  storage) was ruled NOT licensed (Fable 5.1's 7n-4).
* **S4 -- populations 3 and 4 are FILED as `vmewidthlanes` (LOW), not this round.**  7n-4: the FAULT round *"DISCLOSES in
  its contract that sub-word accesses inside cased words reach the fault, as an emulator limitation, not a hardware
  claim"* and *"carries ONE row that pins that interim behaviour and is NAMED as a channel the width row will red and
  re-derive"*.
* **S5 -- MEASURED 2026-10-09 (rung 3, unmodified `-E mvme88k -e mvme187`, binaries built from commit 200671b6;
  `regress/artifacts/vmedefaultkill/measure_20261009/`), condensed from `run_HEAD.out`, `run_FAULT.out`,
  `run_DECLINE.out`:**
  * HEAD: all seven guest sites end the emulator (rc 1); the cased T1CMP round-trip control is green.
  * FAULT sketch (`exit(1)` -> `return 0`): every site vectors to PC 0x18 (VBR 0, vector 3), DMT0 0x413d (reads) /
    0x403f (writes), DMA0 = the register address; host survives.  The guest's own reading of the data CMMU's
    PFSR/PFAR returns 0 (the emulator models no CMMU fault status) -- which is why FAULT would PANIC the in-tree guest
    at attach and why population 2 was ruled DECLINE.
  * DECLINE sketch (`exit(1)` -> `odata = 0; break;`): reads return 0, writes are dropped, PC advances, liveness green.
  * A re-measurement on today's HEAD 5dbc000e is in flight (a separate seat); `dev_vme.c` is unchanged since 200671b6.
* **S6 -- `fatal()` is visible at default verbosity, `debug()` is not, when free-running** (`debugmsg.c`, quoted in
  section 1).  Under SINGLE-STEPPING both print, so a probe can only tell them apart in a FREE-RUNNING session.
* **S7 -- the house latch idiom is N = 1 per device instance with an explicit suppression marker**; `(once)` is the
  plurality spelling.  `#501`'s arm (section 4c) is the sibling on this same board.

## 4. The code, verbatim from HEAD

### 4a. `src/devices/dev_vme.c` -- the whole device (the struct, the access function with its common tail, DEVINIT)

```c
{DEV_VME}
```

Writers of `d->reg[]`, for Q3: the four storing cases (T1CMP, T1COUNT -- whose READ also does `+= 100` -- TCTL, VBR) and
DEVINIT's VBR seed.  Nothing else in the file assigns `d->reg[`.  (Check this.)

### 4b. `src/cpus/memory_rw.c` -- what a handler's return value does (the device-dispatch block)

```c
{MEMRW}
```

### 4c. `src/devices/dev_pcc2.c` -- `#501`, the ruled sibling idiom on this board (struct field and the `default:` arm)

```c
{PCC2}
```

## 5. The implementation SKETCH (a sketch, not a fix, until it survives this pass)

```c
struct vme_data {
	uint32_t	reg[VME_LEN / sizeof(uint32_t)];

	/*  #NNN: one bit per register WORD (relative_addr >> 2) for the
	    unimplemented-register announce; population 2's highest word is
	    0x8c >> 2 == 35, so the shift is defined.  Zeroed by DEVINIT's
	    memset.  */
	uint64_t	warned_unimpl;
};

	/*  (inside the switch, after VME2_VBR's case:)  */

	/*  #NNN (vmedefaultkill): registers the header names that this model
	    does not implement.  OpenBSD 2.2's vme2chip_init() writes MASTER3,
	    MASTER4, MASTER4MOD and MASTERCTL unconditionally at attach and its
	    abort handler reads IRQSTAT and writes IRQCLR; a bus error there
	    panics that guest.  Reads return 0 (nothing writes these words in
	    d->reg[]), writes are dropped, one announce per register.  */
	case VME2_SADDR2:	case VME2_SLAVELMOD1:	case VME2_SLAVELMOD2:
	case VME2_SLAVECTL:	case VME2_MASTER1:	case VME2_MASTER2:
	case VME2_MASTER3:	case VME2_MASTER4:	case VME2_MASTER4MOD:
	case VME2_MASTERCTL:	case VME2_DMACTL:	case VME2_DMAMODE:
	case VME2_DMALADDR:	case VME2_DMAVMEADDR:	case VME2_DMACOUNT:
	case VME2_DMATABLE:	case VME2_DMASTAT:	case VME2_T2CMP:
	case VME2_T2COUNT:	case VME2_PRESCALE:	case VME2_IRQSTAT:
	case VME2_SETSOFTIRQ:	case VME2_IRQCLR:	case VME2_IRQL1:
	case VME2_IRQL2:	case VME2_MISC:
		if (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {
			d->warned_unimpl |= 1ULL << (relative_addr >> 2);
			if (writeflag == MEM_WRITE)
				fatal("[ vme: unimplemented write to register "
				    "0x%x (len %d): 0x%x -- declined.  (once) ]\n",
				    (int) relative_addr, (int) len, (int) idata);
			else
				fatal("[ vme: unimplemented read from register "
				    "0x%x (len %d) -- served 0.  (once) ]\n",
				    (int) relative_addr, (int) len);
		}
		break;

	default:if (writeflag == MEM_READ)
			debug(...unchanged...);
		else
			debug(...unchanged...);
		/*  #NNN (vmedefaultkill): no register is defined here; refuse the
		    access (memory_rw raises the m88k data-access exception)
		    instead of ending the emulator.  Was exit(1).  */
		return 0;
	}
```

Things the sketch does deliberately, each open to challenge:
* the 26 labels are EXACT word starts, matching the switch's existing exact-offset style; sub-word offsets inside them
  fall to `default:` and FAULT (Q4);
* the decline arm does NOT assign `odata = 0` -- the preload above the switch already serves `d->reg[w]`, which is 0 for
  every population-2 word because nothing writes those words (Q3);
* the FAULT arm keeps its two `debug()` lines unchanged and replaces only `exit(1)` (Q6);
* `return 0` skips the common tail -- intended: a failed access writes no data back.

## 6. The DETECTOR PLAN (a new rung-3 probe; a sketch of its rows)

`regress/vme_default_probe.py`, cold-debugger sessions on unmodified `-E mvme88k -e mvme187 -M 64` (the debugger is fed
on stdin, as `regress/mk48_nvram_probe.py` does on the same machine), gated in **gate 14** (`regress/gate_arm.sh`), which
already runs `mk48_nvram_probe.py`, `pcc2_width_probe.py` and `pcc2_c040_probe.py` on mvme187.  Score pinned by equality,
every row checked by name, CONTROL/RESULT/DONE protocol lines.  Each row with the mutant it is aimed at and the observable:

| row | access | wanted on the fix | aimed at (mutant) | channel |
|---|---|---|---|---|
| `live` / `unasm` / `neg apparatus` | `or` liveness; disassembly of every placed word; a bogus machine name | 0x1234; words match; bogus run fails | apparatus | register value / text |
| `vbr reset` | `ld` at 0x88 | 0x67000000 (DEVINIT's seed) | DEVICE-SIGNATURE: RAM or a device-less build reads otherwise | value |
| `t1cmp rt` | `st` then `ld` at 0x50 | the stored word | accept side of the edited switch | value |
| `cased census` | one `ld` at each of the ten cased offsets in ONE session (distinct destinations, sentinel-seeded) | every one served, no exception (T1COUNT's read side effect asserted as +100 between two reads) | a cased label dropped -> that offset FAULTs and later loads never run | PC + sentinels left |
| `p2 rd census` | 26 `ld`, one per population-2 register, ONE session, destinations r4..r29 seeded with a sentinel | all 26 read 0, PC past the last, liveness after | any one population-2 label dropped -> that access FAULTs; HEAD -> process dies | count of zeros + PC |
| `p2 wr census` | 26 `st` of 0xa5a5a5a5, then the 26 `ld` back | all 26 read back 0 | writes STORED into `d->reg[]` (a backed-accept edit); decline conditioned on direction | read-back values |
| `p2 width` | `ld.bu` and `ld.hu` at 0x28, `ld.d` at 0x08 | 0, no exception | decline conditioned on `len == 4` | value + PC |
| `p2 announce` (FREE-RUNNING) | the 26 reads, breakpoint after, `continue` | exactly 26 `(once)` lines naming the 26 offsets, visible at default verbosity | latch shared per device (1 line); `fatal` -> `debug` (0 lines free-running) | host stdout |
| `p2 once` (FREE-RUNNING) | the 26 reads again in the same session | 0 new announce lines | latch never set (52 lines) | host stdout |
| `p1 fault lo` / `p1 fault hi` | `ld` at 0x90 and at 0xffc | exception: PC 0x18, DMA0 = the address, host alive | `return 0` -> `break` (population 1 declines); `exit(1)` reinstated (process dies) | PC, DMA0, rc |
| `p1 fault wr` | `st` at 0x90 | exception, DMT0 write form | the same, write direction | PC, DMT0 |
| `p1 p2 edge` | `ld` at 0x8c then at 0x90 | 0x8c declines, 0x90 faults | the label set's last member dropped / an extra label added | PC + value |
| `p3 interim` | `ld.bu` at 0x51 (inside cased T1CMP) | exception (the interim behaviour 7n-4 prescribes; NAMED as `vmewidthlanes`' channel) | none -- a disclosure pin | PC |

Floor plan (the project's vacuity floor): (a) HEAD red -- every session that touches population 1 or 2 dies; (b) verbatim
reinstatement of `exit(1)` at `default:` -> the population-1 rows die; reinstating the defect at the second fixed site
means removing the 26 labels -> the population-2 rows FAULT or die; (c) null medium for a device round: a build WITHOUT
the `vme` device -> `vbr reset` and `t1cmp rt` red (to be MEASURED, not claimed by construction); (d) the predicates the
fix DEPENDS ON, each weakened: one label dropped, the latch shared, the latch never set, `fatal` -> `debug`, the decline
conditioned on `writeflag` or on `len`, `return 0` -> `break`; (e) a CONTRACT in the probe header with a NOT CLAIMED list
(population 3/4 and population-2 sub-word starts, the guest's abort-handler consequence, `ld.d`/`st.d` spanning two
registers).

## 7. Questions

**Q1 -- PREMISE AUDIT.**  Check each, by enumeration where it is arithmetic: (a) the census in section 2 -- 10 cased, 26
population-2 word starts, 988 population-1 word starts; (b) `d->reg[w]` is 0 for every population-2 word for the device's
whole life (enumerate the writers in section 4a); (c) `return 0` from this handler always yields the m88k data-access
exception for a guest load/store and never a silent failure (section 4b: what are `no_exceptions` and the instruction-
fetch case?); (d) on m88k, which `(relative_addr, len)` pairs can a guest `ld`/`st` deliver inside this window -- in
particular, can a misaligned word or halfword reach the device at all, and can `ld.d` reach an offset that is 4 mod 8?

**Q2 -- THE SKETCH AGAINST THE FULL FUNCTION.**  Walk every path of section 4a with the sketch applied: the preload, each
arm, the common tail.  Is anything wrong -- an arm that reads `idata` on a read, a shift that can exceed 63, a latch bit
two registers share, the `return 0` skipping something it must not?

**Q3 -- `odata = 0;` OR NOT.**  7n-4 recommended setting `odata = 0` explicitly in the decline arm, citing the preload
serving "the containing word".  My lean is to OMIT it: for an EXACT word-start label the containing word is the register's
own `d->reg[w]`, which nothing writes, so the assignment is equivalent today -- and with it present, reads are forced to 0
whatever is stored, so a future edit that starts STORING writes would be invisible to every read-back row (`p2 wr census`
could not red).  Without it, that edit reads back non-zero and reds the row.  Is the lean right?  Is there a path where
the preload serves a non-zero value to a population-2 word-start read today?

**Q4 -- SUB-WORD STARTS INSIDE POPULATION-2 WORDS.**  Under exact labels, a byte or halfword at 0x29 (inside MASTERCTL)
FAULTs, like population 3.  Accept that as interim (disclosed; `vmewidthlanes`' scope widened to name it), or decode
population 2 by its containing word (`relative_addr & ~3`), or something else?  What does each do to the in-tree guest
(word-only) and to the detector?

**Q5 -- THE ANNOUNCE.**  One `fatal()` per register per device instance, keyed by `relative_addr >> 2` in a `uint64_t`;
text mirrors `#501`; the first access's direction decides the wording.  Anything wrong with the key, the width, the
wording, or the `%x` casts of 64-bit `idata` (`#501` also casts with `(int)`)?

**Q6 -- POPULATION 1's PATH.**  Keep the two `debug()` lines and replace only `exit(1)` with `return 0`.  Is any
host-visible trace owed for a population-1 access now that nothing dies?  (`memory_rw.c` prints its own
`[ reading from device ... failed ]`, also at `debug` level.)

**Q7 -- THE DETECTOR.**  Which row in section 6 cannot vary under its named mutant (vacuous by construction)?  Which
mutant in the (d) list has no row that reds?  What row is MISSING?  Is gate 14 the right home?

**Q8 -- WHAT IS THE SMALLEST EDIT that breaks the ruled behaviour and still passes every row in section 6?**  Name the
row you expect to stay green.

**Q9 -- OPTION-SET COMPLETENESS, scoped to the IMPLEMENTATION.**  The project's option set is 1 DELETE, 2 DECLINE (silent),
3 DECLINE + LATCHED ANNOUNCE, 4 ACCEPT, 5 FAULT, 6 BACKED ACCEPT, 7 IMPLEMENT.  The owner ruled 3 for population 2 and
5 for population 1.  Is there an implementation of THOSE members this sketch did not consider and should (grep the fork
for the idiom)?

If, while verifying a claim, you found something ELSE -- say so.

## 8. Answer format

Verdict line first (the token line, then `VERDICT: ...`), then Q1-Q9 in order, each starting with its own one-line
answer.  Every claim about the tree cites file and line (or says it is from this packet).  Say plainly what you did NOT
check.
