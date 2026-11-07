# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `i8259icw4` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `i8259icw4`, state `open`)

**title:** devices/dev_8259.c init sequence -- ICW1 SNGL/IC4 are ignored, so with IC4=0 the guest's first OCW1 mask write is swallowed as ICW4 -- WRONG-RESULT

**state_note (head):** Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T50 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-26, A(c)#11).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/598ab108cacb56dfbeae33eb463fd2b8c18393dd.  Our site at de8c7547: src/devices/dev_8259.c:183-206.  Portable fix: yes -- port rs6000 598ab10.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `if (d->init_state == 1) {` at 233

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_8259.c b/src/devices/dev_8259.c
index 2f224d90..f4bdc75d 100644
--- a/src/devices/dev_8259.c
+++ b/src/devices/dev_8259.c
@@ -118,7 +118,7 @@ DEVICE_ACCESS(8259)
 				    if (!(idata & 0x01))
 					fatal("[ 8259: WARNING: Bit 0 NOT set!"
 					    "!! ]\n");  */
-				d->init_state = 1;
+				d->init_state = 1 | ((idata & 3) << 8);
 				break;
 			}
 
@@ -230,18 +230,22 @@ DEVICE_ACCESS(8259)
 		break;
 	case 0x01:
 		if (d->init_state > 0) {
-			if (d->init_state == 1) {
+			int state = d->init_state & 0xff;
+			if (state == 1) {
 				d->irq_base = idata & 0xf8;
 				/*  This happens on non-x86 machines:
 				    if (idata & 7)
 					fatal("[ 8259: WARNING! Lowest"
 					    " bits in Init Cmd 1 are"
 					    " non-zero! ]\n");  */
-				d->init_state = 2;
-			} else if (d->init_state == 2) {
+				if (d->init_state & 0x200)
+					d->init_state = (d->init_state & 0x100) ? 3 : 0;
+				else
+					d->init_state = (d->init_state & 0xff00) | 2;
+			} else if (state == 2) {
 				/*  Slave attachment. TODO  */
-				d->init_state = 3;
-			} else if (d->init_state == 3) {
+				d->init_state = (d->init_state & 0x100) ? 3 : 0;
+			} else if (state == 3) {
 				if (idata & 0x02) {
 					/*  Should not be set in PCs, but
 					    on CATS, for example, it is set.  */
```

## Every edited function, after the fix

### `src/devices/dev_8259.c` -- post-edit lines 88-296 (`+` marks a line the diff added or the point of a deletion)

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
  121|+ 				d->init_state = 1 | ((idata & 3) << 8);
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
  137|  				/*  Put Master in Buffered Mode  */
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
  233|+ 			int state = d->init_state & 0xff;
  234|+ 			if (state == 1) {
  235|  				d->irq_base = idata & 0xf8;
  236|  				/*  This happens on non-x86 machines:
  237|  				    if (idata & 7)
  238|  					fatal("[ 8259: WARNING! Lowest"
  239|  					    " bits in Init Cmd 1 are"
  240|  					    " non-zero! ]\n");  */
  241|+ 				if (d->init_state & 0x200)
  242|+ 					d->init_state = (d->init_state & 0x100) ? 3 : 0;
  243|+ 				else
  244|+ 					d->init_state = (d->init_state & 0xff00) | 2;
  245|+ 			} else if (state == 2) {
  246|  				/*  Slave attachment. TODO  */
  247|+ 				d->init_state = (d->init_state & 0x100) ? 3 : 0;
  248|+ 			} else if (state == 3) {
  249|  				if (idata & 0x02) {
  250|  					/*  Should not be set in PCs, but
  251|  					    on CATS, for example, it is set.  */
  252|  					debug("[ 8259: WARNING! Bit 1 i"
  253|  					    "n Init Cmd 4 is set! ]\n");
  254|  				}
  255|  				if (!(idata & 0x01))
  256|  					fatal("[ 8259: WARNING! Bit 0 "
  257|  					    "in Init Cmd 4 is not"
  258|  					    " set! ]\n");
  259|  				d->init_state = 0;
  260|  			}
  261|  			break;
  262|  		}
  263|  
  264|  		if (writeflag == MEM_WRITE) {
  265|  			int old_ier = d->ier;
  266|  			d->ier = idata;
  267|  
  268|  			/*  Recalculate interrupt assertions,
  269|  			    if necessary:  */
  270|  			if ((d->irr & ~old_ier) != (d->irr & ~d->ier)) {
  271|  				if (d->irr & ~d->ier)
  272|  					INTERRUPT_ASSERT(d->irq);
  273|  				else
  274|  					INTERRUPT_DEASSERT(d->irq);
  275|  			}
  276|  		} else {
  277|  			odata = d->ier;
  278|  		}
  279|  		break;
  280|  	default:
  281|  		if (writeflag == MEM_WRITE) {
  282|  			fatal("[ 8259: unimplemented write to address 0x%x"
  283|  			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
  284|  			cpu->running = 0;
  285|  		} else {
  286|  			fatal("[ 8259: unimplemented read from address 0x%x "
  287|  			    "]\n", (int)relative_addr);
  288|  			cpu->running = 0;
  289|  		}
  290|  	}
  291|  
  292|  	if (writeflag == MEM_READ)
  293|  		memory_writemax64(cpu, data, len, odata);
  294|  
  295|  	return 1;
  296|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_I8259ICW4: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_I8259ICW4: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
