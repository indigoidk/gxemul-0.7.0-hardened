# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `fbfiqsilent` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `fbfiqsilent`, state `open`)

**title:** dev_footbridge.c answers FIQEnable reads with a silent constant 0 while its IRQ twin kills the host -- the whole FIQ column is softer than the IRQ column [corrected 2026-11-02: since #539 (78360718, 2026-09-19) the IRQ twin returns d->irq_enable with no exit (dev_footbridge.c:600-607 at 987cb596); the FIQ read still answers 0 (:649-652)]

**state_note (head):** *** codex ASSESS 2026-09-08.  THE ASYMMETRY IS REAL, AND BOTH SIDES ARE ACCEPT. ***

**IRQ_ENABLE_SET read (`+0x188`):**

    odata = d->irq_enable;
    fatal("[ WARNING: footbridge read from ENABLE SET? ]");
    exit(1);

*** IT COMPUTES THE CORRECT VALUE AND THEN ENDS THE HOST. ***  That is member 4 ACCEPT in its purest
form -- delete the kill, keep the value -- and it is the SAME SHAPE this project already found at
`+0x188`'s neighbour, where the datasheet showed a documented read-only register whose answer the
model produced and discarded.

**FIQ_ENABLE_SET (`+0x288`)** returns a silent constant zero.  *"Zero is correct when disabled, but
not for every configured state"* -- so the silent half is a fidelity gap, not a non-defect.

**Both warrant member 4, in SEPARATE rounds.**

*** AND IT REFUTED MY BRIEF'S PREMISE, WHICH IS THE FINDING THAT TRAVELS FURTHEST. ***  I told it
that footbridge being ARM meant FAULT might be available.  **The ARM device-failure arm does not
exist**; `memory_rw.c` has `#ifdef MEM_MIPS` and `#ifdef MEM_M88K` and nothing else.  See the
generalised note now carried on the three `dev_lca.c` rows.

**This row is NOT blocked on a manual**, which is why it was chosen: `_scratchpad/dc21285.txt` is
present, and the same datasheet has already changed one footbridge disposition in this project.

**The drafter's own reading:** STILL PRESENT: YES -- `case FIQ_ENABLE_SET:` at line 654

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_footbridge.c b/src/devices/dev_footbridge.c
index 77f7d960..5c568a80 100644
--- a/src/devices/dev_footbridge.c
+++ b/src/devices/dev_footbridge.c
@@ -654,6 +654,8 @@ DEVICE_ACCESS(footbridge)
 	case FIQ_ENABLE_SET:
 		if (writeflag == MEM_WRITE)
 			d->fiq_enable |= idata;
+		else
+			odata = d->fiq_enable;
 		break;
 
 	case FIQ_ENABLE_CLEAR:
```

## Every edited function, after the fix

### `src/devices/dev_footbridge.c` -- post-edit lines 513-808 (`+` marks a line the diff added or the point of a deletion)

```c
  513|  DEVICE_ACCESS(footbridge)
  514|  {
  515|  	struct footbridge_data *d = (struct footbridge_data *) extra;
  516|  	uint64_t idata = 0, odata = 0;
  517|  	int timer_nr = 0;
     | [... lines 518-546 not shown ...]
  547|  		break;
  548|  
  549|  	case PCI_ADDRESS_EXTENSION:
  550|  		/*  TODO: Written to by Linux.  */
  551|  		if (writeflag == MEM_WRITE && idata != 0)
  552|  			fatal("[ footbridge: TODO: write to PCI_ADDRESS_"
  553|  			    "EXTENSION: 0x%llx ]\n", (long long)idata);
  554|  		break;
  555|  
  556|  	case SA_CONTROL:
  557|  		/*  Read by Linux:  */
  558|  		odata = PCI_CENTRAL_FUNCTION;
  559|  		break;
  560|  
  561|  	case UART_DATA:
  562|  		if (writeflag == MEM_WRITE)
  563|  			console_putchar(d->console_handle, idata);
  564|  		break;
  565|  
  566|  	case UART_RX_STAT:
  567|  		/*  TODO  */
  568|  		odata = 0;
  569|  		break;
  570|  
  571|  	case UART_FLAGS:
  572|  		odata = UART_TX_EMPTY;
  573|  		break;
  574|  
  575|  	case IRQ_STATUS:
  576|  		if (writeflag == MEM_READ)
  577|  			odata = d->irq_status & d->irq_enable;
  578|  		else if (!d->warned_irq_status_w) {
  579|  			/*  #545: read-only register (7.3.29); the write is
  580|  			    declined -- no register changes, only this site's
  581|  			    warn-once latch is set -- and announced once.  */
  582|  			d->warned_irq_status_w = 1;
  583|  			fatal("[ WARNING: footbridge write to irq status? "
  584|  			    "(once) ]\n");
  585|  		}
  586|  		break;
  587|  
  588|  	case IRQ_RAW_STATUS:
  589|  		if (writeflag == MEM_READ)
  590|  			odata = d->irq_status;
  591|  		else if (!d->warned_irq_raw_w) {
  592|  			/*  #545: read-only (7.3.30); declined, announced once.  */
  593|  			d->warned_irq_raw_w = 1;
  594|  			fatal("[ footbridge write to irq_raw_status (once) ]\n");
  595|  		}
  596|  		break;
  597|  
  598|  	case IRQ_ENABLE_SET:
  599|  		if (writeflag == MEM_WRITE) {
  600|  			d->irq_enable |= idata;
  601|  			if (d->irq_status & d->irq_enable)
  602|  				INTERRUPT_ASSERT(d->irq);
  603|  			else
  604|  				INTERRUPT_DEASSERT(d->irq);
  605|  		} else {
  606|  			/*  #539: a read of 188h is documented -- IRQEnable is
  607|  			    "read-only ... can only be changed by writing to
  608|  			    the EnableSet and EnableClear registers", reset 0
  609|  			    (DC21285 Table 7-10, 7.3.31).  The value below was
  610|  			    always right; the exit(1) that followed it is gone.  */
  611|  			odata = d->irq_enable;
  612|  		}
  613|  		break;
  614|  
  615|  	case IRQ_ENABLE_CLEAR:
  616|  		if (writeflag == MEM_WRITE) {
  617|  			d->irq_enable &= ~idata;
  618|  			if (d->irq_status & d->irq_enable)
  619|  				INTERRUPT_ASSERT(d->irq);
  620|  			else
  621|  				INTERRUPT_DEASSERT(d->irq);
  622|  		} else if (!d->warned_irq_clear_r) {
  623|  			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
  624|  			    7-10 names no register at 18Ch for reads, so the read
  625|  			    is declined with 0 -- the IRQEnable value that used to
  626|  			    be computed here is 188h's answer, not 18Ch's.  */
  627|  			d->warned_irq_clear_r = 1;
  628|  			fatal("[ WARNING: footbridge read from "
  629|  			    "ENABLE CLEAR? (once) ]\n");
  630|  		}
  631|  		break;
  632|  
  633|  	case FIQ_STATUS:
  634|  		if (writeflag == MEM_READ)
  635|  			odata = d->fiq_status & d->fiq_enable;
  636|  		else if (!d->warned_fiq_status_w) {
  637|  			/*  #545: read-only (7.3.29); declined, announced once.  */
  638|  			d->warned_fiq_status_w = 1;
  639|  			fatal("[ WARNING: footbridge write to fiq status? "
  640|  			    "(once) ]\n");
  641|  		}
  642|  		break;
  643|  
  644|  	case FIQ_RAW_STATUS:
  645|  		if (writeflag == MEM_READ)
  646|  			odata = d->fiq_status;
  647|  		else if (!d->warned_fiq_raw_w) {
  648|  			/*  #545: read-only (7.3.30); declined, announced once.  */
  649|  			d->warned_fiq_raw_w = 1;
  650|  			fatal("[ footbridge write to fiq_raw_status (once) ]\n");
  651|  		}
  652|  		break;
  653|  
  654|  	case FIQ_ENABLE_SET:
  655|  		if (writeflag == MEM_WRITE)
  656|  			d->fiq_enable |= idata;
  657|+ 		else
  658|+ 			odata = d->fiq_enable;
  659|  		break;
  660|  
  661|  	case FIQ_ENABLE_CLEAR:
  662|  		if (writeflag == MEM_WRITE)
  663|  			d->fiq_enable &= ~idata;
  664|  		break;
  665|  
  666|  	case TIMER_1_LOAD:
  667|  		if (writeflag == MEM_READ)
  668|  			odata = d->timer_load[timer_nr];
  669|  		else {
  670|  			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  671|  			reload_timer_value(cpu, d, timer_nr);
  672|  			/*  debug("[ footbridge: timer %i (1-based), "
  673|  			    "value %i ]\n", timer_nr + 1,
  674|  			    (int)d->timer_value[timer_nr]);  */
  675|  			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  676|  		}
  677|  		break;
  678|  
  679|  	case TIMER_1_VALUE:
  680|  		if (writeflag == MEM_READ)
  681|  			odata = d->timer_value[timer_nr];
  682|  		else
  683|  			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
  684|  		break;
  685|  
  686|  	case TIMER_1_CONTROL:
  687|  		if (writeflag == MEM_READ)
  688|  			odata = d->timer_control[timer_nr];
  689|  		else {
  690|  			d->timer_control[timer_nr] = idata;
  691|  			/*  #432: both prescaler bits set is TIMER_EXTERNAL
  692|  			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
  693|  			    and it used to reach fatal()+exit(1) right here, so a
  694|  			    guest selecting the external clock source KILLED THE
  695|  			    HOST.  Arguably likelier than the zero load, since it
  696|  			    is a documented mode rather than a malformed value.
  697|  			    The rate an external clock would actually give is
  698|  			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
  699|  			    now gives the encoding a defined, survivable meaning
  700|  			    (the unprescaled period), and the real semantics are
  701|  			    filed for a round that has a datasheet.  */
  702|  			if (idata & TIMER_ENABLE) {
  703|  				reload_timer_value(cpu, d, timer_nr);
  704|  			} else {
  705|  				d->pending_timer_interrupts[timer_nr] = 0;
  706|  			}
  707|  			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  708|  		}
  709|  		break;
  710|  
  711|  	case TIMER_1_CLEAR:
  712|  		/*  #474: a READ must not perform the clear.  This case carried no
  713|  		    writeflag test at all, while TIMER_1_CONTROL immediately above it
  714|  		    does -- so a guest READ reloaded the counter, decremented the
  715|  		    pending count and DEASSERTED the interrupt.  A guest that merely
  716|  		    read the register silently acknowledged a pending timer interrupt;
  717|  		    the guest-visible consequence is a LOST interrupt, not a bad value.
  718|  
     | [... lines 719-778 not shown ...]
  779|  		if (writeflag == MEM_READ) {
  780|  			/*  #585: declined with 0 and announced once, as for
  781|  			    SDRAM_BA_MASK (7.3.10: R/W, reset value 0).  */
  782|  			if (!d->warned_sdram_offset_r) {
  783|  				d->warned_sdram_offset_r = 1;
  784|  				fatal("[ footbridge: read of sdram_ba_offset "
  785|  				    "declined, reads 0 (written values are "
  786|  				    "not kept) (once) ]\n");
  787|  			}
  788|  		} else {
  789|  			if (idata != 0)
  790|  				fatal("[ footbridge write to sdram_ba_offset "
  791|  				    "%#llx ]\n", (long long)idata);
  792|  		}
  793|  		break;
  794|  
  795|  	default:if (writeflag == MEM_READ) {
  796|  			fatal("[ footbridge: read from 0x%x ]\n",
  797|  			    (int)relative_addr);
  798|  		} else {
  799|  			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
  800|  			    (int)relative_addr, (long long)idata);
  801|  		}
  802|  	}
  803|  
  804|  	if (writeflag == MEM_READ)
  805|  		memory_writemax64(cpu, data, len, odata);
  806|  
  807|  	return 1;
  808|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_FBFIQSILENT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

1. Does the diff remove the defect the issue describes, at every site the issue names?  Name any site it misses.
2. CONTROL FLOW: does any added `return`, `goto`, `break` or early exit skip code the function would otherwise run -- above
   all its COMMON TAIL (for example, code after a switch that writes a read's result to the guest, then `return 1;`)?
   Quote the tail line it skips.  An edit that skips the tail hands the guest an unwritten result.
3. RETURN VALUE: does any path now return something different?  Say what the shown code implies the value means.
4. What ELSE does the diff change -- state left set or cleared, a value the guest can now see, a message on a path that
   did not print one -- beyond removing the defect?
5. House idioms (low severity): a diagnostic a guest can trigger repeatedly should print ONCE per device instance (a latch
   field) with `(once)` in the message; a new comment carries a `/* #NNN: ... */` tag; lines stay within 79 columns.

Each finding: `file:line` in the POST-EDIT numbering shown above, severity DEFECT / QUESTION / STYLE, and the smallest fix
in ONE line.  When the excerpt does not show what a question needs, say UNSETTLED and name what is missing.

End with one line: `FIXREVIEW_FBFIQSILENT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
