Open your answer with the token FABLE_VME_P1_20261020, then ONE line:
VERDICT: PROCEED | PROCEED WITH CHANGES | DO NOT PROCEED -- <one line>

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

```
    0x0    VME2_SADDR1, VME2_SLAVECTL_SNP_NO, VME2_MASTERCTL_1SHIFT, VME2_IRQL1_TIC1SHIFT, VME2_IRQL2_LM0SHIFT, VME2_IRQL3_SW0SHIFT, VME2_IRQL4_VME1SHIFT   <- CASED
    0x4    VME2_SADDR2, VME2_SLAVECTL_BLK, VME2_TCTL1_COVF, VME2_IRQ_VME3, VME2_IRQL1_TIC2SHIFT, VME2_IRQL2_LM1SHIFT, VME2_IRQL3_SW1SHIFT, VME2_IRQL4_VME2SHIFT, VME2_MISC_DISBSYT
    0x8    VME2_SLAVELMOD1, VME2_SLAVECTL_D64, VME2_MASTERCTL_2SHIFT, VME2_IRQ_VME4, VME2_IRQL1_V1IESHIFT, VME2_IRQL2_SIG0SHIFT, VME2_IRQL3_SW2SHIFT, VME2_IRQL4_VME3SHIFT, VME2_MISC_NOELBBSY
    0xc    VME2_SLAVELMOD2, VME2_IRQL1_PESHIFT, VME2_IRQL2_SIG1SHIFT, VME2_IRQL3_SW3SHIFT, VME2_IRQL4_VME4SHIFT
    0x10   VME2_SLAVECTL, VME2_SLAVECTL_A24, VME2_MASTERCTL_3SHIFT, VME2_IRQ_VME5, VME2_IRQL1_WPESHIFT, VME2_IRQL2_SIG2SHIFT, VME2_IRQL3_SW4SHIFT, VME2_IRQL4_VME5SHIFT, VME2_MISC_DISMST
    0x14   VME2_MASTER1, VME2_IRQL1_SYSFSHIFT, VME2_IRQL2_SIG3SHIFT, VME2_IRQL3_SW5SHIFT, VME2_IRQL4_VME6SHIFT
    0x18   VME2_MASTER2, VME2_MASTERCTL_4SHIFT, VME2_IRQL1_ABSHIFT, VME2_IRQL2_DMASHIFT, VME2_IRQL3_SW6SHIFT, VME2_IRQL4_VME7SHIFT, VME2_VBR_1SHIFT
    0x1c   VME2_MASTER3, VME2_IRQL1_ACFSHIFT, VME2_IRQL2_VIASHIFT, VME2_IRQL3_SW7SHIFT, VME2_IRQL4_SPARESHIFT, VME2_VBR_0SHIFT
    0x20   VME2_MASTER4, VME2_SLAVECTL_A32, VME2_IRQ_VME6, VME2_MISC_DISSRAM
    0x24   VME2_MASTER4MOD
    0x28   VME2_MASTERCTL
    0x2c   VME2_GCSRCTL   <- CASED
    0x30   VME2_DMACTL
    0x34   VME2_DMAMODE
    0x38   VME2_DMALADDR, VME2_GCSRCTL_ROMBSPD
    0x3c   VME2_DMAVMEADDR
    0x40   VME2_DMACOUNT, VME2_SLAVECTL_USR, VME2_MASTERCTL_WP, VME2_IRQ_VME7, VME2_MISC_REVEROM
    0x44   VME2_DMATABLE
    0x48   VME2_DMASTAT
    0x4c   VME2_TCR   <- CASED
    0x50   VME2_T1CMP   <- CASED
    0x54   VME2_T1COUNT   <- CASED
    0x58   VME2_T2CMP
    0x5c   VME2_T2COUNT
    0x60   VME2_TCTL   <- CASED
    0x64   VME2_PRESCALE
    0x68   VME2_IRQSTAT
    0x6c   VME2_IRQEN   <- CASED
    0x70   VME2_SETSOFTIRQ
    0x74   VME2_IRQCLR
    0x78   VME2_IRQL1
    0x7c   VME2_IRQL2
    0x80   VME2_IRQL3, VME2_SLAVECTL_SUP, VME2_MASTERCTL_D16, VME2_IRQ_SPARE, VME2_MISC_MPIRQEN   <- CASED
    0x84   VME2_IRQL4   <- CASED
    0x88   VME2_VBR   <- CASED
    0x8c   VME2_MISC
    (values 0xc0, 0xf0, 0x100, 0x200, 0x400, 0x800 also appear: GCSRCTL_ROMSIZE, TCTL1_OVF and bit masks -- no register name)
```

Cased offsets (from the switch): 0x0, 0x2c, 0x4c, 0x50, 0x54, 0x60, 0x6c, 0x80, 0x84, 0x88.  Population 2 (word starts 0x04..0x8c not cased): 26.  Population 1 (word starts 0x90..0xffc): 988.

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

```
vme.c:452  ctl = vme2->vme2_masterctl;
vme.c:467  vme2->vme2_master3 = ((VME2_D16ENDPHYS-1) & 0xffff0000) |
vme.c:480  vme2->vme2_master4 = ((VME2_D32ENDPHYS-1) & 0xffff0000) |
vme.c:482  vme2->vme2_master4mod = (VME2_D32STARTVME & 0xffff0000) |
vme.c:494  vme2->vme2_masterctl = ctl;
vme.c:496  ctl = vme2->vme2_gcsrctl;
vme.c:513  vme2->vme2_gcsrctl = ctl;
vme.c:576  if (!(vme2->vme2_irqstat & VME2_IRQ_AB)) {
vme.c:581  vme2->vme2_irqclr = VME2_IRQ_AB;
```
(The `vme2_master1`/`vme2_master2` reads at vme.c:456-463 sit inside `#if 0` and are compiled out; `gcsrctl` at :496/:513 is CASED.)

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
  44  #include "thirdparty/mvme88k_vme.h"
  45  
  46  
  47  /*  #define debug fatal  */
  48  
  49  
  50  #define	VME_LEN			0x1000
  51  
  52  struct vme_data {
  53  	uint32_t	reg[VME_LEN / sizeof(uint32_t)];
  54  };
  55  
  56  
  57  DEVICE_ACCESS(vme)
  58  {
  59  	struct vme_data *d = (struct vme_data *) extra;
  60  	uint64_t idata = 0, odata = 0;
  61  
  62  	if (writeflag == MEM_WRITE)
  63  		idata = memory_readmax64(cpu, data, len);
  64  
  65  	if (writeflag == MEM_READ)
  66  		odata = d->reg[relative_addr / sizeof(uint32_t)];
  67  
  68  	switch (relative_addr) {
  69  
  70  	case 0:	/*  Used by OpenBSD/mvme88k when probing...  */
  71  		break;
  72  
  73  	case VME2_GCSRCTL:
  74  		debug("[ vme: unimplemented GCSRCTL ]\n");
  75  		break;
  76  
  77  	case VME2_TCR:
  78  		if (writeflag == MEM_READ)
  79  			debug("[ vme: unimplemented READ from TCR ]\n");
  80  		else
  81  			debug("[ vme: unimplemented WRITE to TCR: "
  82  			    "0x%x ]\n", (int)idata);
  83  		break;
  84  
  85  	case VME2_T1CMP:
  86  		if (writeflag == MEM_WRITE)
  87  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
  88  		break;
  89  
  90  	case VME2_T1COUNT:
  91  		if (writeflag == MEM_WRITE)
  92  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
  93  		else {
  94  			/*  NOTE! This is a quick hack. TODO: Fix!  */
  95  			d->reg[relative_addr / sizeof(uint32_t)] += 100;
  96  		}
  97  		break;
  98  
  99  	case VME2_TCTL:
 100  		if (writeflag == MEM_WRITE)
 101  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 102  
 103  		/*  TODO  */
 104  		/*  debug("[ vme: unimplemented TCTL ]\n");  */
 105  		break;
 106  
 107  	case VME2_IRQEN:
 108  		if (writeflag == MEM_READ)
 109  			debug("[ vme: unimplemented READ from IRQEN ]\n");
 110  		else
 111  			debug("[ vme: unimplemented WRITE to IRQEN: "
 112  			    "0x%x ]\n", (int)idata);
 113  		break;
 114  
 115  	case VME2_IRQL3:
 116  		if (writeflag == MEM_READ)
 117  			debug("[ vme: unimplemented READ from IRQL3 ]\n");
 118  		else
 119  			debug("[ vme: unimplemented WRITE to IRQL3: "
 120  			    "0x%x ]\n", (int)idata);
 121  		break;
 122  
 123  	case VME2_IRQL4:
 124  		if (writeflag == MEM_READ)
 125  			debug("[ vme: unimplemented READ from IRQL4 ]\n");
 126  		else
 127  			debug("[ vme: unimplemented WRITE to IRQL4: "
 128  			    "0x%x ]\n", (int)idata);
 129  		break;
 130  
 131  	case VME2_VBR:
 132  		/*  Vector Base Register.  */
 133  		if (writeflag == MEM_WRITE)
 134  			d->reg[relative_addr / sizeof(uint32_t)] = idata;
 135  		break;
 136  
 137  	default:if (writeflag == MEM_READ)
 138  			debug("[ vme: unimplemented READ from offset 0x%x ]"
 139  			    "\n", (int)relative_addr);
 140  		else
 141  			debug("[ vme: unimplemented WRITE to offset 0x%x: "
 142  			    "0x%x ]\n", (int)relative_addr, (int)idata);
 143  		exit(1);
 144  	}
 145  
 146  	if (writeflag == MEM_READ)
 147  		memory_writemax64(cpu, data, len, odata);
 148  
 149  	return 1;
 150  }
 151  
 152  
 153  DEVINIT(vme)
 154  {
 155  	struct vme_data *d;
 156  
 157  	CHECK_ALLOCATION(d = (struct vme_data *) malloc(sizeof(struct vme_data)));
 158  	memset(d, 0, sizeof(struct vme_data));
 159  
 160  	/*  According to OpenBSD/mvme88k:  */
 161  	d->reg[VME2_VBR / sizeof(uint32_t)] =
 162  	    VME2_SET_VBR0(6) + VME2_SET_VBR1(7);
 163  
 164  	memory_device_register(devinit->machine->memory, devinit->name,
 165  	    devinit->addr, VME_LEN, dev_vme_access, (void *)d,
 166  	    DM_DEFAULT, NULL);
 167  
 168  	return 1;
 169  }
```

Writers of `d->reg[]`, for Q3: the four storing cases (T1CMP, T1COUNT -- whose READ also does `+= 100` -- TCTL, VBR) and
DEVINIT's VBR seed.  Nothing else in the file assigns `d->reg[`.  (Check this.)

### 4b. `src/cpus/memory_rw.c` -- what a handler's return value does (the device-dispatch block)

```c
 583  				res = 0;
 584  				if (!no_exceptions || (mem->devices[i].flags &
 585  				    DM_READS_HAVE_NO_SIDE_EFFECTS)) {
 586  					bool running_before_device_access = cpu->running;
 587  					res = mem->devices[i].f(cpu, mem, paddr,
 588  					    data, len, writeflag,
 589  					    mem->devices[i].extra);
 590  
 591  					if (running_before_device_access && !cpu->running)
 592  						return MEMORY_ACCESS_FAILED;
 593  				}
 594  
 595  				if (res == 0)
 596  					res = -1;
 597  
 598  				/*
 599  				 *  If accessing the memory mapped device
 600  				 *  failed, then return with an exception.
 601  				 *  (Architecture specific.)
 602  				 */
 603  				if (res <= 0 && !no_exceptions) {
 604  					debug("[ %s device '%s' addr %08lx "
 605  					    "failed ]\n", writeflag?
 606  					    "writing to" : "reading from",
 607  					    mem->devices[i].name, (long)paddr);
 608  #ifdef MEM_MIPS
 609  					mips_cpu_exception(cpu,
 610  					    cache == CACHE_INSTRUCTION?
 611  					    EXCEPTION_IBE : EXCEPTION_DBE,
 612  					    0, vaddr, 0, 0, 0, 0);
 613  #endif
 614  #ifdef MEM_M88K
 615  					/*  TODO: This is enough for
 616  					    OpenBSD/mvme88k's badaddr()
 617  					    implementation... but the
 618  					    faulting address should probably
 619  					    be included somewhere too!  */
 620  					m88k_exception(cpu, cache == CACHE_INSTRUCTION
 621  					    ? M88K_EXCEPTION_INSTRUCTION_ACCESS
 622  					    : M88K_EXCEPTION_DATA_ACCESS, 0);
 623  #endif
 624  					return MEMORY_ACCESS_FAILED;
 625  				}
 626  				goto do_return_ok;
```

### 4c. `src/devices/dev_pcc2.c` -- `#501`, the ruled sibling idiom on this board (struct field and the `default:` arm)

```c
 165  	/*  #501: one bit per BYTE OFFSET (0..0x3f) for the default: arm's announce;
 166  	    relative_addr is folded to PCC2_SIZE above the switch, so the shift is
 167  	    always defined.  Zeroed by the same memset.  */
 168  	uint64_t		warned_unimpl;
   ...
 741  	default:
 742  		/*  #501 (pcc2defaultkill): this arm ended the host with exit(1) on ANY
 743  		    access to an offset with no case -- 43 of the 0x40 byte offsets:
 744  		    eighteen documented registers the model does not implement (IEICR,
 745  		    IEERR, IEBERR, GPIO, SCSIERR, the printer block, SPEED, the *IACKs),
 746  		    the bytes inside the four counter/compare words, and the unnamed
 747  		    ones -- READS included, though the memcpy above the switch had
 748  		    already served them.  A guest ld.bu or st.b at any of them was a host
 749  		    kill (rung-3 witness).  Now: a READ keeps the served byte (the array's
 750  		    current byte, said so -- inside a running COUNT word that is the
 751  		    tick's value, not a default); a WRITE is DECLINED.  Not a
 752  		    backed store: the cased siblings contradict one (SCCERR clears on
 753  		    write, the ICRs mask and reassert, PSCALECNT/SPEED/the IACKs are
 754  		    read-only), no inspected OpenBSD driver path reaches them (if_ie never
 755  		    attaches: unreadable sits at its 82596 address), and a store from the
 756  		    one arm 43 offsets reach would add a bounded-write surface.  One
 757  		    latched fatal() per offset per instance, the house `(once)' shape --
 758  		    unlike PSCALEADJ's UNLATCHED print above (pcc2pscaleflood).  The
 759  		    IACK offsets 0x23/0x25 are declined like the rest: modelling them (on
 760  		    the SCCRXIACK shape) would open two new entries into the C040 path,
 761  		    so pcc2c040kill goes first.  The %= fold above IS the real part's:
 762  		    Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as repeated
 763  		    PCCchip2 registers.  */
 764  		if (!(d->warned_unimpl & (1ULL << relative_addr))) {
 765  			d->warned_unimpl |= 1ULL << relative_addr;
 766  			if (writeflag == MEM_WRITE)
 767  				fatal("[ pcc2: unimplemented write to offset "
 768  				    "0x%x (len %d): 0x%x -- declined.  (once) ]\n",
 769  				    (int) relative_addr, (int) len, (int) idata);
 770  			else
 771  				/*  data[0] is the byte actually SERVED; a reload of the
 772  				    array could differ: on the end-span path (zero-filled,
 773  				    the array byte kept) and inside a running COUNT word,
 774  				    whose SIGALRM-driven tick (timer.c) can land between
 775  				    the copy and this line.  A wide read is labelled.  */
 776  				fatal("[ pcc2: unimplemented read from offset "
 777  				    "0x%x (len %d) -- served 0x%02x.  (once) ]\n",
 778  				    (int) relative_addr, (int) len, data[0]);
 779  		}
 780  		break;
 781  	}
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
