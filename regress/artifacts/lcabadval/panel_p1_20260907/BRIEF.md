# DESIGN BRIEF -- `lcabadval` pass 1: six value guards in `dev_lca.c` that end the host process

**VERDICT LINE FIRST**, then the body.

## PLEASE DO NOT SIMPLY RATIFY

A recent panel here had seven of nine seats confirm a premise the brief stated wrongly -- the true
number was four times larger. **Check the premises, not just the derivations.** Several premises
below are stated as questions on purpose. If you cannot settle one from this packet, say so plainly
and name it; an honest "not checkable from here" is worth more than a guess.

**This brief carries a FORK, not a proposal. I have an argument for one side and I want it
attacked.** A clean "your argument for A is wrong because X" is the most useful answer you can give.

## The tree

The tree under review is **`GXEMUL-SEC/src/`**. Ignore any other `src/` you can reach -- there are
three pristine 2021 upstream copies under the project root, and reading one gives line numbers off
by hundreds and a different set of arms.

---

# SETTLED PREMISES -- verified this session, inlined so you need not read files

Established by a codex fix-check with a full denominator (all 10 cases plus `default:`, all six
guarded arms, both translated siblings, all nine field-read sites) and, where noted, re-verified
independently by me. **Premise 6 is the one I most want challenged.**

**1. All six arms share one shape, and THE STORE RUNS BEFORE THE GUARD.** Verbatim, using
`LCA_IOC_W_MASK0`:

```c
	case LCA_IOC_W_MASK0:
		if (writeflag == MEM_READ) {
			odata = d->window_mask_0;
		} else {
			d->window_mask_0 = idata;

			if (idata != 0x700000ULL) {
				fatal("TODO: LCA_IOC_W_MASK0 value differs ...");
				exit(1);
			}
		}
		break;
```

The six, with the value each accepts:

    LCA_IOC_CONF     idata & ~1                 accepts 0 and 1
    LCA_IOC_TB_ENA   idata & ~IOC_TB_ENA_TEN    accepts 0 and the TEN bit
    LCA_IOC_W_BASE0  idata != 0 && != 0x300800000
    LCA_IOC_W_MASK0  idata != 0x700000
    LCA_IOC_W_BASE1  idata != 0x240000000
    LCA_IOC_W_MASK1  idata != 0x3ff00000

Codex confirmed store-before-guard in **all six**, with a per-arm table of readback/store/guard
lines. This is not a generalisation from one arm.

**2. Five of the six fields are PURE STORAGE; `ioc_conf` has exactly ONE functional consumer.**
I re-verified this over the whole tree and the counts are decisive -- each field occurs exactly
three times (declaration, readback, store):

    window_base_0  3    window_mask_0  3    tlb_enable  3
    window_base_1  3    window_mask_1  3    ioc_conf    4

`ioc_conf`'s fourth occurrence is `bus = d->ioc_conf & 1;` in `DEVICE_ACCESS(lca_pci_conf)`.
**There is NO DMA-translation consumer anywhere in the tree** -- nothing reads a window base or
mask to translate an address. The window registers are write-to-nowhere plus a readback.

**3. Codex's sharpening of my own wording, which I had blurred.** Extra CONF bits are discarded
*for bus selection*, but **the IOC readback returns the STORED value**. So masking the store would
not merely be an unlicensed addition -- it would change READBACK POLICY, which is guest-visible.

**4. `fatal()` does NOT terminate.** It calls the returning printer `va_debug()`; the explicit
`exit(1)` ends the process. `debug()` additionally applies verbosity filtering and can be silenced
by `-q`; `fatal()` cannot.

**5. THIS PROJECT ALREADY REFUSED PROPOSAL A, TWICE, IN WRITING.** Round `#447` fixed four value
guards in `dev_sh4.c` and left this census in the tree, verbatim:

```
 *  #447: four value guards in the switch below ended the host process with exit(1) on
 *  ONE ordinary guest store -- TCR, DMATCR, ICR and RCR1.  ...
 *    RCR1    the store was UPSTREAM of the guard.  Dropping exit(1) alone would have
 *            turned a host kill into SILENT STATE CORRUPTION.  Moved below the guard.
 *    TCR     `timer_hz` was set from `idata & 3` BEFORE the guard and the debug() line
 *            had already announced it, so the naive fix installs a timer frequency the
 *            guest never asked for.  The guard moved ABOVE the prescaler switch.
 *    DMATCR  the store is already downstream; nothing to move.
 *    ICR     nothing is stored on any path, so there is no state to corrupt.
 *
 *  Saying "the store is upstream" once for the file would have been wrong three times
 *  out of four.  Check it per site.
```

And the RCR1 arm's own comment:

```
 *  #447: *** THE STORE WAS UPSTREAM OF THE GUARD. ***  It ran first and the guard second,
 *  so a rejected value had ALREADY landed in rtc_rcr1 and exit(1) was the only thing
 *  stopping the guest reading it back.  Dropping the exit and nothing else turns a host
 *  kill into SILENT STATE CORRUPTION -- the guest writes CIE|AIE, reads CIE|AIE back, and
 *  believes the RTC will interrupt it.  It never will.  Same shape as #443 found in
 *  dev_sh4_pcic_access(), and the ONLY one of #447's four sites that has it.  The store
 *  therefore moved below.
```

A third site says it from the other direction -- DMATCR's comment notes its store is downstream
*"unlike RCR1 and unlike every arm of `dev_sh4_pcic_access()`, where the store runs first and a
restore is needed."*

**So the tree holds two precedents where store-runs-first means the fix is NOT "just drop the
exit": RCR1 MOVED THE STORE BELOW THE GUARD, and `#443` ADDED A RESTORE.**

**6. MY ARGUMENT THAT LCA IS NEVERTHELESS DIFFERENT -- ATTACK THIS.**

RCR1's stored value has a meaning the model otherwise honours: for accepted values the model acts
on `rtc_rcr1`, so reading back `CIE|AIE` tells the guest something specific and false.

I claim LCA is not like that, because **the model implements window translation for NO value at
all**. If that is right then:

* the guest ALREADY writes `0x700000`, reads `0x700000` back, and believes the window is
  programmed -- and it is not, because nothing consumes it;
* so the silent state corruption `#447` warns about is **PRE-EXISTING and VALUE-INDEPENDENT**;
* removing `exit(1)` therefore does not CREATE a false belief. It stops killing the host over one
  wrong value while continuing to tell the same lie about the accepted one.

**Is that sound, or am I excusing a new instance of a defect because an old instance already
exists?** I can see the shape of the counter-argument and cannot tell how strong it is.

---

# THE FORK

    A  DELETE fatal()+exit(1) from all six arms, KEEP the store that already ran.
       (What premise 6 argues for.  Nothing else changes -- no mask, no default, no new state.)

    B  DECLINE the write: move the store BELOW the guard, exactly as #447 did for RCR1, so a
       rejected value never lands and the readback returns the last accepted value.

The sibling registers `LCA_IOC_W_T_BASE0` and `LCA_IOC_W_T_BASE1` -- the TRANSLATED-window
registers -- have the identical read/store shape and **no value guard at all**. Codex's caution,
which I accept: that may be evidence that accepting is correct, **or** merely that nobody wrote a
guard. It does not settle the fork by itself.

**A cost of B I want weighed:** real hardware reads back what was written. B makes the readback lie
in a DIFFERENT way -- write `X`, read back the old value -- which no hardware does. A keeps the
readback truthful about the register file and false about the window being active.

---

# THE FULL ENCLOSING FUNCTION

Four readers here once independently proposed `if (r == 3) return;` for a function whose last three
lines were the common tail that services the read; an early return would have handed the guest an
untouched buffer. **So: the whole function, every exit path and the tail, verbatim.**

```c
DEVICE_ACCESS(lca_ioc)
{
	uint64_t idata = 0, odata = 0;
	struct lca_data *d = (struct lca_data *) extra;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	switch (relative_addr + LCA_IOC_BASE) {

	case LCA_IOC_BASE:
		/*  Ignore? Linux reads from the base at startup.  */
		break;

	case LCA_IOC_CONF:
		if (writeflag == MEM_READ) {
			odata = d->ioc_conf;
		} else {
			d->ioc_conf = idata;
			/*  Only bit 0 is implemented so far, the PCI bus 0 vs
			    bus non-0 selection bit.  */
			if (idata & ~1) {
				/*  #506: was `0x%x', (int)idata -- a 64-bit guarded value
				    narrowed to 32 in the KILL diagnostic, so a write of
				    0x100000000 trips `idata & ~1' and then reports "0x0",
				    which is a value this same guard ACCEPTS.  The five
				    sibling arms below already print the full width this
				    way; this arm was the outlier among the VALUE-guard
				    diagnostics.  (Not the file's only narrowing site --
				    the default arm below has the same cast, and this
				    round fixes it too.)  */
				fatal("TODO: Write to unimplemented bit of"
				    " IOC_CONF: 0x%" PRIx64 "\n", (uint64_t)idata);
				exit(1);
			}
		}
		break;

	case LCA_IOC_TBIA:
		/*  TLB Invalidate All.  */
		/*  TODO: For now, let's just ignore it.  */
		break;

	case LCA_IOC_TB_ENA:
		if (writeflag == MEM_READ) {
			odata = d->tlb_enable;
		} else {
			d->tlb_enable = idata;
			/*  TODO: Actually implement this.  */
			if (idata & ~IOC_TB_ENA_TEN) {
				fatal("TODO: LCA_IOC_TB_ENA value "
				    " (0x%" PRIx64") has unimplemented "
				    "bits.\n", (uint64_t)idata);
				exit(1);
			}
		}
		break;

	case LCA_IOC_W_BASE0:
		if (writeflag == MEM_READ) {
			odata = d->window_base_0;
		} else {
			d->window_base_0 = idata;
			/*  TODO: Actually implement this.  */
			if (idata != 0ULL && idata != 0x300800000ULL) {
				fatal("TODO: LCA_IOC_W_BASE0 value differs"
				    " (0x%" PRIx64") from the only implemented"
				    " values\n", (uint64_t)idata);
				exit(1);
			}
		}
		break;

	case LCA_IOC_W_MASK0:
		if (writeflag == MEM_READ) {
			odata = d->window_mask_0;
		} else {
			d->window_mask_0 = idata;
			/*  TODO: Actually implement this.  */
			if (idata != 0x700000ULL) {
				fatal("TODO: LCA_IOC_W_MASK0 value differs"
				    " (0x%" PRIx64") from the only implemented"
				    " value\n", (uint64_t)idata);
				exit(1);
			}
		}
		break;

	case LCA_IOC_W_T_BASE0:
		if (writeflag == MEM_READ) {
			odata = d->window_t_base_0;
		} else {
			d->window_t_base_0 = idata;
			/*  TODO: Actually implement this.  */
		}
		break;

	case LCA_IOC_W_BASE1:
		if (writeflag == MEM_READ) {
			odata = d->window_base_1;
		} else {
			d->window_base_1 = idata;
			/*  TODO: Actually implement this.  */
			if (idata != 0x240000000ULL) {
				fatal("TODO: LCA_IOC_W_BASE1 value differs"
				    " (0x%" PRIx64") from the only implemented"
				    " value\n", (uint64_t)idata);
				exit(1);
			}
		}
		break;

	case LCA_IOC_W_MASK1:
		if (writeflag == MEM_READ) {
			odata = d->window_mask_1;
		} else {
			d->window_mask_1 = idata;
			/*  TODO: Actually implement this.  */
			if (idata != 0x3ff00000ULL) {
				fatal("TODO: LCA_IOC_W_MASK1 value differs"
				    " (0x%" PRIx64") from the only implemented"
				    " value\n", (uint64_t)idata);
				exit(1);
			}
		}
		break;

	case LCA_IOC_W_T_BASE1:
		if (writeflag == MEM_READ) {
			odata = d->window_t_base_1;
		} else {
			d->window_t_base_1 = idata;
			/*  TODO: Actually implement this.  */
		}
		break;

	default:fatal("[ lca_ioc: unimplemented %s to offset 0x%x",
		    writeflag == MEM_WRITE? "write" : "read", (int)
		    relative_addr);
		if (writeflag == MEM_WRITE)
			fatal(": 0x%" PRIx64, (uint64_t)idata);	/*  #506  */
		fatal(" ]\n");
		exit(1);
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

---

# QUESTIONS

1. **Is premise 6 sound?** Does "the model consumes these fields for nothing, so the readback is
   already a lie for the accepted value" genuinely distinguish LCA from RCR1 -- or is it the
   reasoning that would let every store-before-guard site keep its store? **Give the strongest
   version of the counter-argument even if you end up agreeing with me.**

2. **A or B?** Answer with the disposition and the ONE fact that decides it. If the honest answer is
   "this packet cannot settle it, and here is the single thing to look at", say that instead.

3. **Is the option set complete?** What I can see, drawn from this tree's own idioms: delete the
   exit and keep the store (A); decline silently by moving the store (B); decline with a once-only
   LATCHED announce; ACCEPT and announce once; MASK the stored value and announce the excluded bits
   (`dev_pcc2.c` VECBASE does this); complete with a **guest-visible device error** (`dev_wdc.c`
   sets `WDCE_ABRT` and requests an interrupt for every unsupported command); FAULT by modelling the
   space unmapped (`dev_unreadable.c`); or IMPLEMENT the windows. **Which have I missed, and is any
   obviously right here?** Note FAULT may not transfer: `memory_rw.c` dispatches an exception on a
   failed device access for MIPS and M88K, and there is no Alpha equivalent.

4. **What does this NOT close?** My understanding: the `default:` arm still diagnoses and exits **for
   both reads and writes**; neither `LCA_IOC_STAT0` nor `LCA_IOC_STAT1` has a case at all; and
   explicit exits remain in `DEVICE_ACCESS(lca_pci_conf)`, `DEVICE_ACCESS(lca_isa)` and
   `lca_interrupt_assert()`/`lca_interrupt_deassert()`. **So firmware can still terminate the
   emulator after this lands.** Is that right, and is there anything else?

5. **A witness.** This is Alpha and there is no Alpha rig here. Can any of the six be reached by a
   rung-3 cold-debugger probe -- a real guest store through real address decode on an unmodified
   in-tree machine -- or is this documented-only? **If you think a probe is possible, name the
   machine and the address; do NOT write one.**

## Rules

* Answer from the packet. Where you assert tree behaviour beyond it, name the file and function and
  flag that you are going past what was inlined.
* Disagreements here are settled by measurement, never by vote -- prefer "measure X" to "I think X".
* If, while checking this, you found something ELSE -- say so.
