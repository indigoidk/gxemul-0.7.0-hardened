# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `fbirqstuck` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `fbirqstuck`, state `open`)

**title:** dev_footbridge.c: the CPU interrupt line can STICK HIGH while IRQ_STATUS reads 0.  footbridge_interrupt_deassert() lowers d->irq only when d->irq_asserted is set, and the IRQEnableSet / IRQEnableClear write arms call INTERRUPT_ASSERT(d->irq) without setting it.  Sequence (Opus seat, #545 repair pass 2, measured in its in-process differential -- regress/artifacts/fbd5/q2_20260923/p2r_20260923/opus_q2r/dom_witness.txt 'model check'): a device line (cats ISA, line 10) asserts while its enable bit i [... 1024 more characters not shown]

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- `src/devices/dev_footbridge.c:603` and `src/devices/dev_footbridge.c:620` (as modified by the previous draft, the condition to assert/deassert lacks proper state tracking ordering)

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_footbridge.c b/src/devices/dev_footbridge.c
index 77f7d960..192fb5c2 100644
--- a/src/devices/dev_footbridge.c
+++ b/src/devices/dev_footbridge.c
@@ -598,10 +598,13 @@ DEVICE_ACCESS(footbridge)
 	case IRQ_ENABLE_SET:
 		if (writeflag == MEM_WRITE) {
 			d->irq_enable |= idata;
-			if (d->irq_status & d->irq_enable)
+			if (d->irq_status & d->irq_enable) {
+				d->irq_asserted = 1;
 				INTERRUPT_ASSERT(d->irq);
-			else
+			} else {
 				INTERRUPT_DEASSERT(d->irq);
+				d->irq_asserted = 0;
+			}
 		} else {
 			/*  #539: a read of 188h is documented -- IRQEnable is
 			    "read-only ... can only be changed by writing to
@@ -615,10 +618,13 @@ DEVICE_ACCESS(footbridge)
 	case IRQ_ENABLE_CLEAR:
 		if (writeflag == MEM_WRITE) {
 			d->irq_enable &= ~idata;
-			if (d->irq_status & d->irq_enable)
+			if (d->irq_status & d->irq_enable) {
+				d->irq_asserted = 1;
 				INTERRUPT_ASSERT(d->irq);
-			else
+			} else {
 				INTERRUPT_DEASSERT(d->irq);
+				d->irq_asserted = 0;
+			}
 		} else if (!d->warned_irq_clear_r) {
 			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
 			    7-10 names no register at 18Ch for reads, so the read
```

## Every edited function, after the fix

### `src/devices/dev_footbridge.c` -- post-edit lines 513-812 (`+` marks a line the diff added or the point of a deletion)

```c
  513|  DEVICE_ACCESS(footbridge)
  514|  {
  515|  	struct footbridge_data *d = (struct footbridge_data *) extra;
  516|  	uint64_t idata = 0, odata = 0;
  517|  	int timer_nr = 0;
  518|  
  519|  	if (writeflag == MEM_WRITE)
  520|  		idata = memory_readmax64(cpu, data, len);
  521|  
  522|  	if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {
  523|  		timer_nr = (relative_addr >> 5) & (N_FOOTBRIDGE_TIMERS - 1);
  524|  		relative_addr &= ~0x060;
  525|  	}
  526|  
  527|  	switch (relative_addr) {
  528|  
  529|  	case VENDOR_ID:
  530|  		odata = 0x1011;  /*  DC21285_VENDOR_ID  */
  531|  		break;
  532|  
  533|  	case DEVICE_ID:
  534|  		odata = 0x1065;  /*  DC21285_DEVICE_ID  */
  535|  		break;
  536|  
  537|  	case 0x04:
  538|  	case 0x0c:
  539|  	case 0x10:
  540|  	case 0x14:
  541|  	case 0x18:
  542|  		/*  TODO. Written to by Linux.  */
  543|  		break;
  544|  
  545|  	case REVISION:
  546|  		odata = 3;  /*  footbridge revision number  */
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
  601|+ 			if (d->irq_status & d->irq_enable) {
  602|+ 				d->irq_asserted = 1;
  603|  				INTERRUPT_ASSERT(d->irq);
  604|+ 			} else {
  605|  				INTERRUPT_DEASSERT(d->irq);
  606|+ 				d->irq_asserted = 0;
  607|+ 			}
  608|  		} else {
  609|  			/*  #539: a read of 188h is documented -- IRQEnable is
  610|  			    "read-only ... can only be changed by writing to
  611|  			    the EnableSet and EnableClear registers", reset 0
  612|  			    (DC21285 Table 7-10, 7.3.31).  The value below was
  613|  			    always right; the exit(1) that followed it is gone.  */
  614|  			odata = d->irq_enable;
  615|  		}
  616|  		break;
  617|  
  618|  	case IRQ_ENABLE_CLEAR:
  619|  		if (writeflag == MEM_WRITE) {
  620|  			d->irq_enable &= ~idata;
  621|+ 			if (d->irq_status & d->irq_enable) {
  622|+ 				d->irq_asserted = 1;
  623|  				INTERRUPT_ASSERT(d->irq);
  624|+ 			} else {
  625|  				INTERRUPT_DEASSERT(d->irq);
  626|+ 				d->irq_asserted = 0;
  627|+ 			}
  628|  		} else if (!d->warned_irq_clear_r) {
  629|  			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
  630|  			    7-10 names no register at 18Ch for reads, so the read
  631|  			    is declined with 0 -- the IRQEnable value that used to
  632|  			    be computed here is 188h's answer, not 18Ch's.  */
  633|  			d->warned_irq_clear_r = 1;
  634|  			fatal("[ WARNING: footbridge read from "
  635|  			    "ENABLE CLEAR? (once) ]\n");
  636|  		}
  637|  		break;
  638|  
  639|  	case FIQ_STATUS:
  640|  		if (writeflag == MEM_READ)
  641|  			odata = d->fiq_status & d->fiq_enable;
  642|  		else if (!d->warned_fiq_status_w) {
  643|  			/*  #545: read-only (7.3.29); declined, announced once.  */
  644|  			d->warned_fiq_status_w = 1;
  645|  			fatal("[ WARNING: footbridge write to fiq status? "
  646|  			    "(once) ]\n");
  647|  		}
  648|  		break;
  649|  
  650|  	case FIQ_RAW_STATUS:
  651|  		if (writeflag == MEM_READ)
  652|  			odata = d->fiq_status;
  653|  		else if (!d->warned_fiq_raw_w) {
  654|  			/*  #545: read-only (7.3.30); declined, announced once.  */
  655|  			d->warned_fiq_raw_w = 1;
  656|  			fatal("[ footbridge write to fiq_raw_status (once) ]\n");
  657|  		}
  658|  		break;
  659|  
  660|  	case FIQ_ENABLE_SET:
  661|  		if (writeflag == MEM_WRITE)
  662|  			d->fiq_enable |= idata;
  663|  		break;
  664|  
  665|  	case FIQ_ENABLE_CLEAR:
  666|  		if (writeflag == MEM_WRITE)
  667|  			d->fiq_enable &= ~idata;
  668|  		break;
  669|  
  670|  	case TIMER_1_LOAD:
  671|  		if (writeflag == MEM_READ)
  672|  			odata = d->timer_load[timer_nr];
  673|  		else {
  674|  			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  675|  			reload_timer_value(cpu, d, timer_nr);
  676|  			/*  debug("[ footbridge: timer %i (1-based), "
  677|  			    "value %i ]\n", timer_nr + 1,
  678|  			    (int)d->timer_value[timer_nr]);  */
  679|  			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  680|  		}
  681|  		break;
  682|  
  683|  	case TIMER_1_VALUE:
  684|  		if (writeflag == MEM_READ)
  685|  			odata = d->timer_value[timer_nr];
  686|  		else
  687|  			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
     | [... lines 688-782 not shown ...]
  783|  		if (writeflag == MEM_READ) {
  784|  			/*  #585: declined with 0 and announced once, as for
  785|  			    SDRAM_BA_MASK (7.3.10: R/W, reset value 0).  */
  786|  			if (!d->warned_sdram_offset_r) {
  787|  				d->warned_sdram_offset_r = 1;
  788|  				fatal("[ footbridge: read of sdram_ba_offset "
  789|  				    "declined, reads 0 (written values are "
  790|  				    "not kept) (once) ]\n");
  791|  			}
  792|  		} else {
  793|  			if (idata != 0)
  794|  				fatal("[ footbridge write to sdram_ba_offset "
  795|  				    "%#llx ]\n", (long long)idata);
  796|  		}
  797|  		break;
  798|  
  799|  	default:if (writeflag == MEM_READ) {
  800|  			fatal("[ footbridge: read from 0x%x ]\n",
  801|  			    (int)relative_addr);
  802|  		} else {
  803|  			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
  804|  			    (int)relative_addr, (long long)idata);
  805|  		}
  806|  	}
  807|  
  808|  	if (writeflag == MEM_READ)
  809|  		memory_writemax64(cpu, data, len, odata);
  810|  
  811|  	return 1;
  812|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_FBIRQSTUCK: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_FBIRQSTUCK: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
