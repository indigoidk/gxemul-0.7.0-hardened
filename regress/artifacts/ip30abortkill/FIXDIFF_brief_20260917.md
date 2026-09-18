# **WRITE THE `ip30abortkill` FIX DIFF.**  Everything is settled except the code.
## VERDICT LINE FIRST.  TREE: `GXEMUL-SEC/` under `C:/DocumentNoSnc/CC/GXEMUL`.  HEAD `9c91999`.

## *** DO NOT RATIFY.  A proposed edit is a SKETCH until it has been run against the enclosing
## function's real control flow -- and four independent readers once wrote the same broken
## `return` into a function none of them noticed had a tail.  THE FULL ENCLOSING FUNCTION IS
## INLINED BELOW, every exit path and the common tail included. ***

## SETTLED -- do not re-open, but say so if any of it is wrong

* **WITNESSED, rung 3, measured:** a guest LOAD at `0x0ff10020` kills the host (SIGABRT); so
  does a load at `0x10028`; so does a WRITE at `0x10030`; a READ at `0x10030` is SERVICED.
  The tick also kills: arm `imask0` bit 50 and **`step 1`** is enough, because
  `machine_add_tickfunction` sets `ticks_till_next[n] = 0`, so the first `machine_run()` fires
  every tick function.  **Arming needs `sd` -- a 4-byte `sw` cannot set bit 50** (`case 0x10000`
  reads through `memory_readmax64`).
* **DISPOSITION, 8-seat adjudicated:** member 3 (decline + LATCHED announce) + member 4 on the
  stores that already compute the update + the `writeflag` test, **ONE diff**, **TWO latch bits**
  (tick vs ISR-recalc; one shared bit lets a Set-ISR write silence the timer diagnostic forever).
* **MEMBER 7 IS AVAILABLE-BUT-UNWARRANTED**, not unavailable: `cpu_interrupt()` is gone (five
  occurrences tree-wide, all comments) but the live API `interrupt_assert` via `struct interrupt`
  exists and is what `dev_sgi_ip32.c` uses for CRIME.  Delivery is a subsystem; it is FILED.
* **THE HEART REFERENCE, fetched with the owner's approval and verified offset-by-offset against
  this file:** Linux `arch/mips/include/asm/sgi/heart.h` --
  `imr[] +0x10000`, `set_isr +0x10020`, `clear_isr +0x10028`, `isr +0x10030 "(read-only)"`,
  `count +0x20000`, `compare +0x30000`, base `0x0ff00000`.  **The code cites this document
  itself** ("according to Linux/IP30", three times).
  * So `0x10020`/`0x10028` are **WRITE-SIDE** registers: a READ has no defined meaning ->
    **DECLINE the read**, do NOT mirror `d->isr`.
  * **AND `isr` IS READ-ONLY, while this file implements a WRITE arm for it** --
    `/* Clear-on-write (TODO: is this correct?) */ d->isr &= ~idata;`.  The cited document
    answers that TODO: **no**.  Clearing goes through `clear_isr`, which the file already has.

## QUESTIONS

**Q1 -- WRITE THE DIFF.**  Unified, against the function inlined below.  Terse portable C99,
minimal surgical change, `/* #NNN: */` tags in this fork's style.  **Use `break`, never an early
`return`** -- `:180-183` is the common tail.

**Q2 -- THE `isr` WRITE ARM.**  Decline it, or keep clear-on-write with the warrant stated as an
emulator-compatibility choice rather than as architecture?  **The addition licence allows a
measured delta or a transferred warrant, never "cannot hurt".**  Which do you have?

**Q3 -- THE LATCH.**  Two bits, per device instance, with the house marker.  The tree's marker
family is `(once)` and its qualified forms -- **derive the current spelling census yourself
rather than trusting any number I could quote, because that count has rotted five times here.**

**Q4 -- WHAT DOES THE DE-ESCALATION CLAUSE OWE?**  This diff deletes host-fatal guards, which
destroys the accidental tripwire that made guard growth self-announcing.  Enumerate from YOUR
diff every predicate that used to gate death, and name the accept row each one owes.

**Q5 -- WHAT IS THE SMALLEST EDIT THAT BREAKS YOUR FIX AND STILL PASSES** a detector whose rows
are `live`, `devsig`, `acc 18`, `acc 20000`, `acc 30000`, `acc imask`, `acc 30 rd`,
`kill 20 rd`, `kill 28 rd`, `kill 30 wr`, plus a tick row and an ISR-unchanged row?  A
clean-sweep mutant is a FLOOR BREACH, so name it now rather than after the table.

## THE FULL ENCLOSING FUNCTION (lines 63-184), INCLUDING THE COMMON TAIL

```
c
   1| 	/*  ip30_5:  */
   2| 	uint64_t                reg_0x00000;
   3| };
   4| 
   5| 
   6| DEVICE_TICK(sgi_ip30)
   7| {
   8| 	struct sgi_ip30_data *d = (struct sgi_ip30_data *) extra;
   9| 
  10| 	d->reg_0x20000 += 1000;
  11| 
  12| 	if (d->imask0 & ((int64_t)1<<50)) {
  13| 		/*  TODO: Only interrupt if reg 0x20000 (the counter)
  14| 			has passed the compare (0x30000).  */
  15| fatal("IP30 legacy interrupt rewrite: TODO\n");
  16| abort();
  17| //		cpu_interrupt(cpu, 8+1 + 50);
  18| 	}
  19| }
  20| 
  21| 
  22| DEVICE_ACCESS(sgi_ip30)
  23| {
  24| 	struct sgi_ip30_data *d = (struct sgi_ip30_data *) extra;
  25| 	uint64_t idata = 0, odata = 0;
  26| 
  27| 	if (writeflag == MEM_WRITE)
  28| 		idata = memory_readmax64(cpu, data, len);
  29| 
  30| 	switch (relative_addr) {
  31| 
  32| 	case 0x20:
  33| 		/*  Memory bank configuration:  */
  34| 		odata = 0x80010000ULL;
  35| 		break;
  36| 
  37| 	case 0x10000:	/*  Interrupt mask register 0:  */
  38| 		if (writeflag == MEM_WRITE) {
  39| 			d->imask0 = idata;
  40| 		} else {
  41| 			odata = d->imask0;
  42| 		}
  43| 		break;
  44| 
  45| 	case 0x10018:
  46| 		/*
  47| 		 *  If this is not implemented, the IP30 PROM complains during
  48| 		 *  bootup:
  49| 		 *
  50| 		 *           *FAILED*
  51| 		 *    Address: 0xffffffffaff10018, Expected:
  52| 		 *        0x0000000000000001, Received: 0x0000000000000000
  53| 		 */
  54| 		if (writeflag == MEM_WRITE) {
  55| 			d->reg_0x10018 = idata;
  56| 		} else {
  57| 			odata = d->reg_0x10018;
  58| 		}
  59| 		break;
  60| 
  61| 	case 0x10020:	/*  Set ISR, according to Linux/IP30  */
  62| 		d->isr = idata;
  63| 		/*  Recalculate CPU interrupt assertions:  */
  64| fatal("IP30 legacy interrupt rewrite: TODO\n");
  65| abort();
  66| //		cpu_interrupt(cpu, 8);
  67| 		break;
  68| 
  69| 	case 0x10028:	/*  Clear ISR, according to Linux/IP30  */
  70| 		d->isr &= ~idata;
  71| 		/*  Recalculate CPU interrupt assertions:  */
  72| fatal("IP30 legacy interrupt rewrite: TODO\n");
  73| abort();
  74| //		cpu_interrupt(cpu, 8);
  75| 		break;
  76| 
  77| 	case 0x10030:	/*  Interrupt Status Register  */
  78| 		if (writeflag == MEM_WRITE) {
  79| 			/*  Clear-on-write  (TODO: is this correct?)  */
  80| 			d->isr &= ~idata;
  81| 			/*  Recalculate CPU interrupt assertions:  */
  82| fatal("IP30 legacy interrupt rewrite: TODO\n");
  83| abort();
  84| //			cpu_interrupt(cpu, 8);
  85| 		} else {
  86| 			odata = d->isr;
  87| 		}
  88| 		break;
  89| 
  90| 	case 0x20000:
  91| 		/*  A counter  */
  92| 		if (writeflag == MEM_WRITE) {
  93| 			d->reg_0x20000 = idata;
  94| 		} else {
  95| 			odata = d->reg_0x20000;
  96| 		}
  97| 		break;
  98| 
  99| 	case 0x30000:
 100| 		if (writeflag == MEM_WRITE) {
 101| 			d->reg_0x30000 = idata;
 102| 		} else {
 103| 			odata = d->reg_0x30000;
 104| 		}
 105| 		break;
 106| 
 107| 	default:
 108| 		if (writeflag == MEM_WRITE) {
 109| 			debug("[ sgi_ip30: unimplemented write to address "
 110| 			    "0x%x, data=0x%02x ]\n", (int)relative_addr,
 111| 			    (int)idata);
 112| 		} else {
 113| 			debug("[ sgi_ip30: unimplemented read from address"
 114| 			    " 0x%x ]\n", (int)relative_addr);
 115| 		}
 116| 	}
 117| 
 118| 	if (writeflag == MEM_READ)
 119| 		memory_writemax64(cpu, data, len, odata);
 120| 
 121| 	return 1;
 122| }
```

## HONESTY
If the right answer is "do not write this diff yet because X is unsettled", say that.  Name X.
