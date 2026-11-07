# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `i8259pollcomment` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `i8259pollcomment`, state `open`)

**title:** src/devices/dev_8259.c:137 -- the 0x0c arm's comment Put Master in Buffered Mode describes ICW4's BUF bit, but 0x0c on the command port is the OCW3 poll command -- RECORD

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- 137| 				/*  Put Master in Buffered Mode  */

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_8259.c b/src/devices/dev_8259.c
index 2f224d90..17b6e809 100644
--- a/src/devices/dev_8259.c
+++ b/src/devices/dev_8259.c
@@ -134,7 +134,7 @@ DEVICE_ACCESS(8259)
 			} else if (idata == 0x0b) {
 				d->current_command = 0x0b;
 			} else if (idata == 0x0c) {
-				/*  Put Master in Buffered Mode  */
+				/*  Poll command  */
 				d->current_command = 0x0c;
 			} else if (idata == 0x20) {
 				/*  Non-specific End Of Interrupt.  #574: resets
```

## Every edited function, after the fix

### `src/devices/dev_8259.c` -- post-edit lines 88-292 (`+` marks a line the diff added or the point of a deletion)

```c
   88|  DEVICE_ACCESS(8259)
   89|  {
   90|  	struct pic8259_data *d = (struct pic8259_data *) extra;
   91|  	uint64_t idata = 0, odata = 0;
   92|  	int i;
   93|  
   94|  	if (writeflag == MEM_WRITE)
   95|  		idata = memory_readmax64(cpu, data, len);
   96|  
   97|  #ifdef DEV_8259_DEBUG
   98|  	if (writeflag == MEM_READ)
   99|  		fatal("[ 8259: read from 0x%x ]\n", (int)relative_addr);
  100|  	else
  101|  		fatal("[ 8259: write to 0x%x: 0x%x ]\n",
  102|  		    (int)relative_addr, (int)idata);
  103|  #endif
  104|  
  105|  	switch (relative_addr) {
  106|  	case 0x00:
  107|  		if (writeflag == MEM_WRITE) {
  108|  			if ((idata & 0x10) == 0x10) {
  109|  				/*  Bit 3: 0=edge, 1=level  */
  110|  				if (idata & 0x08)
  111|  					fatal("[ 8259: TODO: Level "
  112|  					    "triggered (MCA bus) ]\n");
  113|  				if (idata & 0x04)
  114|  					fatal("[ 8259: WARNING: Bit 2 set ]\n");
  115|  				/*  Bit 1: 0=cascade, 1=single  */
  116|  				/*  Bit 0: 1=4th init byte  */
  117|  				/*  This happens on non-x86 systems:
  118|  				    if (!(idata & 0x01))
  119|  					fatal("[ 8259: WARNING: Bit 0 NOT set!"
  120|  					    "!! ]\n");  */
  121|  				d->init_state = 1;
  122|  				break;
  123|  			}
  124|  
  125|  			/*  TODO: Is it ok to abort init state when there
  126|  			    is a non-init command?  */
  127|  			if (d->init_state)
  128|  				fatal("[ 8259: WARNING: Was in init-state, but"
  129|  				    " it was aborted? ]\n");
  130|  			d->init_state = 0;
  131|  
  132|  			if (idata == 0x0a) {
  133|  				d->current_command = 0x0a;
  134|  			} else if (idata == 0x0b) {
  135|  				d->current_command = 0x0b;
  136|  			} else if (idata == 0x0c) {
  137|+ 				/*  Poll command  */
  138|  				d->current_command = 0x0c;
  139|  			} else if (idata == 0x20) {
  140|  				/*  Non-specific End Of Interrupt.  #574: resets
  141|  				    the highest-priority in-service bit (the lowest
  142|  				    set ISR bit, fixed priority) and nothing else;
  143|  				    the request bits belong to the lines and to the
  144|  				    acknowledge (pic8259_acknowledge).  This arm
  145|  				    also did irr &= ~isr; isr = 0 -- a no-op on
  146|  				    irr while nothing set isr.  */
  147|  				/*  TODO: in buffered mode, is this an EOI 0? */
  148|  				if (d->isr)
  149|  					d->isr &= ~(d->isr & -d->isr);
  150|  			} else if ((idata >= 0x21 && idata <= 0x27) ||
  151|  			    (idata >= 0x60 && idata <= 0x67) ||
  152|  			    (idata >= 0xe0 && idata <= 0xe7)) {
  153|  				/*  Specific EOI.  #574: when the line is in
  154|  				    service (an acknowledge -- the poll read, or
  155|  				    the GT IACK read -- moved its request to ISR),
  156|  				    the EOI resets that ISR bit and leaves the
  157|  				    request bit alone, as on the chip.  When it is
  158|  				    NOT (a guest whose vector read acknowledges
  159|  				    nothing -- dev_prep.c, dev_footbridge.c -- or
  160|  				    none at all), the EOI still consumes the
  161|  				    request as it always did here: that consume
  162|  				    is the only one those machines have.  */
  163|  				int bit = 1 << (idata & 7);
  164|  				if (d->isr & bit) {
  165|  					d->isr &= ~bit;
  166|  				} else {
  167|  					int old_irr = d->irr;
  168|  					d->irr &= ~bit;
  169|  					if ((old_irr & ~d->ier) !=
  170|  					    (d->irr & ~d->ier)) {
  171|  						if (d->irr & ~d->ier)
  172|  							INTERRUPT_ASSERT(d->irq);
  173|  						else
  174|  							INTERRUPT_DEASSERT(d->irq);
  175|  					}
  176|  				}
  177|  			} else if (idata == 0x68) {
  178|  				/*  Set Special Mask Mode  */
  179|  				/*  TODO  */
  180|  			} else if (idata >= 0xc0 && idata <= 0xc7) {
  181|  				/*  Set IRQ Priority Order  */
  182|  				/*  TODO  */
  183|  			} else {
  184|  				fatal("[ 8259: unimplemented command 0x%02x"
  185|  				    " ]\n", (int)idata);
  186|  				cpu->running = 0;
  187|  			}
  188|  		} else {
  189|  			switch (d->current_command) {
  190|  			case 0x0a:
  191|  				odata = d->irr;
  192|  				break;
  193|  			case 0x0b:
  194|  				odata = d->isr;
  195|  				break;
  196|  			case 0x0c:
  197|  				/*  The read after an OCW3 poll.  #574: it is the
  198|  				    interrupt acknowledge (the datasheet's "sets
  199|  				    the appropriate IS bit"), of the highest
  200|  				    unmasked request -- the raw irr scan that stood
  201|  				    here returned masked lines too.  One read per
  202|  				    poll: later reads return the IRR until the next
  203|  				    OCW3.  */
  204|  				i = pic8259_acknowledge(d, cpu->machine);
  205|  				odata = i < 0 ? 0x00 : (0x80 | i);
  206|  				d->current_command = 0x0a;
  207|  				break;
  208|  			default:
  209|  				odata = 0x00;
  210|  				for (i=0; i<8; i++)
  211|  					if ((d->irr >> i) & 1) {
  212|  						odata = 0x80 | i;
  213|  						break;
  214|  					}
  215|  				break;
  216|  			/*
  217|  			 *  TODO: The "default" label should really do
  218|  			 *  something like this:
  219|  			 *
  220|  			 *	fatal("[ 8259: unimplemented command 0x%02x"
  221|  			 *	    " while reading ]\n", d->current_command);
  222|  			 *	cpu->running = 0;
  223|  			 *
  224|  			 *  but Linux seems to read from the secondary PIC
  225|  			 *  in a manner which works better the way things
  226|  			 *  are coded right now.
  227|  			 */
  228|  			}
  229|  		}
  230|  		break;
  231|  	case 0x01:
  232|  		if (d->init_state > 0) {
  233|  			if (d->init_state == 1) {
  234|  				d->irq_base = idata & 0xf8;
  235|  				/*  This happens on non-x86 machines:
  236|  				    if (idata & 7)
  237|  					fatal("[ 8259: WARNING! Lowest"
  238|  					    " bits in Init Cmd 1 are"
  239|  					    " non-zero! ]\n");  */
  240|  				d->init_state = 2;
  241|  			} else if (d->init_state == 2) {
  242|  				/*  Slave attachment. TODO  */
  243|  				d->init_state = 3;
  244|  			} else if (d->init_state == 3) {
  245|  				if (idata & 0x02) {
  246|  					/*  Should not be set in PCs, but
  247|  					    on CATS, for example, it is set.  */
  248|  					debug("[ 8259: WARNING! Bit 1 i"
  249|  					    "n Init Cmd 4 is set! ]\n");
  250|  				}
  251|  				if (!(idata & 0x01))
  252|  					fatal("[ 8259: WARNING! Bit 0 "
  253|  					    "in Init Cmd 4 is not"
  254|  					    " set! ]\n");
  255|  				d->init_state = 0;
  256|  			}
  257|  			break;
  258|  		}
  259|  
  260|  		if (writeflag == MEM_WRITE) {
  261|  			int old_ier = d->ier;
  262|  			d->ier = idata;
  263|  
  264|  			/*  Recalculate interrupt assertions,
  265|  			    if necessary:  */
  266|  			if ((d->irr & ~old_ier) != (d->irr & ~d->ier)) {
  267|  				if (d->irr & ~d->ier)
  268|  					INTERRUPT_ASSERT(d->irq);
  269|  				else
  270|  					INTERRUPT_DEASSERT(d->irq);
  271|  			}
  272|  		} else {
  273|  			odata = d->ier;
  274|  		}
  275|  		break;
  276|  	default:
  277|  		if (writeflag == MEM_WRITE) {
  278|  			fatal("[ 8259: unimplemented write to address 0x%x"
  279|  			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
  280|  			cpu->running = 0;
  281|  		} else {
  282|  			fatal("[ 8259: unimplemented read from address 0x%x "
  283|  			    "]\n", (int)relative_addr);
  284|  			cpu->running = 0;
  285|  		}
  286|  	}
  287|  
  288|  	if (writeflag == MEM_READ)
  289|  		memory_writemax64(cpu, data, len, odata);
  290|  
  291|  	return 1;
  292|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_I8259POLLCOMMENT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_I8259POLLCOMMENT: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
