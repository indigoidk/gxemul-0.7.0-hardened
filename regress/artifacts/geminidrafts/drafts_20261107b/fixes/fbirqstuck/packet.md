# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `fbirqstuck` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `fbirqstuck`, state `open`)

**title:** dev_footbridge.c: the CPU interrupt line can STICK HIGH while IRQ_STATUS reads 0.  footbridge_interrupt_deassert() lowers d->irq only when d->irq_asserted is set, and the IRQEnableSet / IRQEnableClear write arms call INTERRUPT_ASSERT(d->irq) without setting it.  Sequence (Opus seat, #545 repair pass 2, measured in its in-process differential -- regress/artifacts/fbd5/q2_20260923/p2r_20260923/opus_q2r/dom_witness.txt 'model check'): a device line (cats ISA, line 10) asserts while its enable bit i [... 1024 more characters not shown]

**state_note (head):** 

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_footbridge.c` -- AT HEAD, lines 513-806 (`*` marks a line your previous draft changed)

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
  601|* 			if (d->irq_status & d->irq_enable)
  602|* 				INTERRUPT_ASSERT(d->irq);
  603|* 			else
  604|* 				INTERRUPT_DEASSERT(d->irq);
  605|* 		} else {
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
  618|* 			if (d->irq_status & d->irq_enable)
  619|* 				INTERRUPT_ASSERT(d->irq);
  620|* 			else
  621|* 				INTERRUPT_DEASSERT(d->irq);
  622|* 		} else if (!d->warned_irq_clear_r) {
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
  657|  		break;
  658|  
  659|  	case FIQ_ENABLE_CLEAR:
  660|  		if (writeflag == MEM_WRITE)
  661|  			d->fiq_enable &= ~idata;
  662|  		break;
  663|  
  664|  	case TIMER_1_LOAD:
  665|  		if (writeflag == MEM_READ)
  666|  			odata = d->timer_load[timer_nr];
  667|  		else {
  668|  			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
  669|  			reload_timer_value(cpu, d, timer_nr);
  670|  			/*  debug("[ footbridge: timer %i (1-based), "
  671|  			    "value %i ]\n", timer_nr + 1,
  672|  			    (int)d->timer_value[timer_nr]);  */
  673|  			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
  674|  		}
  675|  		break;
  676|  
  677|  	case TIMER_1_VALUE:
  678|  		if (writeflag == MEM_READ)
  679|  			odata = d->timer_value[timer_nr];
  680|  		else
  681|  			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
  682|  		break;
     | [... lines 683-776 not shown ...]
  777|  		if (writeflag == MEM_READ) {
  778|  			/*  #585: declined with 0 and announced once, as for
  779|  			    SDRAM_BA_MASK (7.3.10: R/W, reset value 0).  */
  780|  			if (!d->warned_sdram_offset_r) {
  781|  				d->warned_sdram_offset_r = 1;
  782|  				fatal("[ footbridge: read of sdram_ba_offset "
  783|  				    "declined, reads 0 (written values are "
  784|  				    "not kept) (once) ]\n");
  785|  			}
  786|  		} else {
  787|  			if (idata != 0)
  788|  				fatal("[ footbridge write to sdram_ba_offset "
  789|  				    "%#llx ]\n", (long long)idata);
  790|  		}
  791|  		break;
  792|  
  793|  	default:if (writeflag == MEM_READ) {
  794|  			fatal("[ footbridge: read from 0x%x ]\n",
  795|  			    (int)relative_addr);
  796|  		} else {
  797|  			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
  798|  			    (int)relative_addr, (long long)idata);
  799|  		}
  800|  	}
  801|  
  802|  	if (writeflag == MEM_READ)
  803|  		memory_writemax64(cpu, data, len, odata);
  804|  
  805|  	return 1;
  806|  }
```



## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_footbridge.c",
    "old": "\t\t\td->irq_enable |= idata;\n\t\t\tif (d->irq_status & d->irq_enable)\n\t\t\t\tINTERRUPT_ASSERT(d->irq);\n\t\t\telse\n\t\t\t\tINTERRUPT_DEASSERT(d->irq);",
    "new": "\t\t\td->irq_enable |= idata;\n\t\t\tif (d->irq_status & d->irq_enable) {\n\t\t\t\td->irq_asserted = 1;\n\t\t\t\tINTERRUPT_ASSERT(d->irq);\n\t\t\t} else {\n\t\t\t\td->irq_asserted = 0;\n\t\t\t\tINTERRUPT_DEASSERT(d->irq);\n\t\t\t}",
    "why": "Track the asserted state when asserting or deasserting via IRQ_ENABLE_SET so footbridge_interrupt_deassert() can correctly lower the line."
  },
  {
    "file": "src/devices/dev_footbridge.c",
    "old": "\t\t\td->irq_enable &= ~idata;\n\t\t\tif (d->irq_status & d->irq_enable)\n\t\t\t\tINTERRUPT_ASSERT(d->irq);\n\t\t\telse\n\t\t\t\tINTERRUPT_DEASSERT(d->irq);",
    "new": "\t\t\td->irq_enable &= ~idata;\n\t\t\tif (d->irq_status & d->irq_enable) {\n\t\t\t\td->irq_asserted = 1;\n\t\t\t\tINTERRUPT_ASSERT(d->irq);\n\t\t\t} else {\n\t\t\t\td->irq_asserted = 0;\n\t\t\t\tINTERRUPT_DEASSERT(d->irq);\n\t\t\t}",
    "why": "Track the asserted state when asserting or deasserting via IRQ_ENABLE_CLEAR so footbridge_interrupt_deassert() can correctly lower the line."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_FBIRQSTUCK: DEFECT, 2 FINDINGS
1. The diff removes the missing assert flag, but introduces a new defect that breaks deassertion. The issue states `footbridge_interrupt_deassert()` lowers the line *only when `d->irq_asserted` is set*. By setting `d->irq_asserted = 0` before the call, `INTERRUPT_DEASSERT` will see a false condition and fail to lower the line.
2. CONTROL FLOW: No added `return`, `goto`, or `break` skips any code. The common tail (`memory_writemax64(cpu, data, len, odata);` and `return 1;`) is reached exactly as before.
3. RETURN VALUE: No path returns something different. The function continues to return `1` (implying a successful/handled memory access).
4. What ELSE does the diff change: The diff clears `d->irq_asserted` right before `INTERRUPT_DEASSERT(d->irq)` rather than after, which inadvertently suppresses the deassertion logic.
5. House idioms: No idiom violations. Added lines are short and no new diagnostic prints or comments were added.
src/devices/dev_footbridge.c:605 DEFECT swap lines 605 and 606 to clear `d->irq_asserted` AFTER `INTERRUPT_DEASSERT(d->irq)`.
src/devices/dev_footbridge.c:625 DEFECT swap lines 625 and 626 to clear `d->irq_asserted` AFTER `INTERRUPT_DEASSERT(d->irq)`.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_FBIRQSTUCK: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_FBIRQSTUCK: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
