# GXemul hardened fork -- DRAFT A FIX for one filed issue, `i8259initread` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `i8259initread`, state `open`, severity `LOW`)

**title:** src/devices/dev_8259.c:231-258 -- the data port's init-sequence arm has no writeflag test, so a READ during initialisation advances init_state (at the ICW2 step it sets irq_base from the zero idata) and returns 0 instead of the mask register -- WRONG-RESULT

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- Missing writeflag test allows reads to advance init_state.

## The code at the cited lines

### `src/devices/dev_8259.c` around the row's cited line 231 (HEAD 8d9df658, lines 111-334)

```c
  111| 					fatal("[ 8259: TODO: Level "
  112| 					    "triggered (MCA bus) ]\n");
  113| 				if (idata & 0x04)
  114| 					fatal("[ 8259: WARNING: Bit 2 set ]\n");
  115| 				/*  Bit 1: 0=cascade, 1=single  */
  116| 				/*  Bit 0: 1=4th init byte  */
  117| 				/*  This happens on non-x86 systems:
  118| 				    if (!(idata & 0x01))
  119| 					fatal("[ 8259: WARNING: Bit 0 NOT set!"
  120| 					    "!! ]\n");  */
  121| 				d->init_state = 1;
  122| 				break;
  123| 			}
  124| 
  125| 			/*  TODO: Is it ok to abort init state when there
  126| 			    is a non-init command?  */
  127| 			if (d->init_state)
  128| 				fatal("[ 8259: WARNING: Was in init-state, but"
  129| 				    " it was aborted? ]\n");
  130| 			d->init_state = 0;
  131| 
  132| 			if (idata == 0x0a) {
  133| 				d->current_command = 0x0a;
  134| 			} else if (idata == 0x0b) {
  135| 				d->current_command = 0x0b;
  136| 			} else if (idata == 0x0c) {
  137| 				/*  Put Master in Buffered Mode  */
  138| 				d->current_command = 0x0c;
  139| 			} else if (idata == 0x20) {
  140| 				/*  Non-specific End Of Interrupt.  #574: resets
  141| 				    the highest-priority in-service bit (the lowest
  142| 				    set ISR bit, fixed priority) and nothing else;
  143| 				    the request bits belong to the lines and to the
  144| 				    acknowledge (pic8259_acknowledge).  This arm
  145| 				    also did irr &= ~isr; isr = 0 -- a no-op on
  146| 				    irr while nothing set isr.  */
  147| 				/*  TODO: in buffered mode, is this an EOI 0? */
  148| 				if (d->isr)
  149| 					d->isr &= ~(d->isr & -d->isr);
  150| 			} else if ((idata >= 0x21 && idata <= 0x27) ||
  151| 			    (idata >= 0x60 && idata <= 0x67) ||
  152| 			    (idata >= 0xe0 && idata <= 0xe7)) {
  153| 				/*  Specific EOI.  #574: when the line is in
  154| 				    service (an acknowledge -- the poll read, or
  155| 				    the GT IACK read -- moved its request to ISR),
  156| 				    the EOI resets that ISR bit and leaves the
  157| 				    request bit alone, as on the chip.  When it is
  158| 				    NOT (a guest whose vector read acknowledges
  159| 				    nothing -- dev_prep.c, dev_footbridge.c -- or
  160| 				    none at all), the EOI still consumes the
  161| 				    request as it always did here: that consume
  162| 				    is the only one those machines have.  */
  163| 				int bit = 1 << (idata & 7);
  164| 				if (d->isr & bit) {
  165| 					d->isr &= ~bit;
  166| 				} else {
  167| 					int old_irr = d->irr;
  168| 					d->irr &= ~bit;
  169| 					if ((old_irr & ~d->ier) !=
  170| 					    (d->irr & ~d->ier)) {
  171| 						if (d->irr & ~d->ier)
  172| 							INTERRUPT_ASSERT(d->irq);
  173| 						else
  174| 							INTERRUPT_DEASSERT(d->irq);
  175| 					}
  176| 				}
  177| 			} else if (idata == 0x68) {
  178| 				/*  Set Special Mask Mode  */
  179| 				/*  TODO  */
  180| 			} else if (idata >= 0xc0 && idata <= 0xc7) {
  181| 				/*  Set IRQ Priority Order  */
  182| 				/*  TODO  */
  183| 			} else {
  184| 				fatal("[ 8259: unimplemented command 0x%02x"
  185| 				    " ]\n", (int)idata);
  186| 				cpu->running = 0;
  187| 			}
  188| 		} else {
  189| 			switch (d->current_command) {
  190| 			case 0x0a:
  191| 				odata = d->irr;
  192| 				break;
  193| 			case 0x0b:
  194| 				odata = d->isr;
  195| 				break;
  196| 			case 0x0c:
  197| 				/*  The read after an OCW3 poll.  #574: it is the
  198| 				    interrupt acknowledge (the datasheet's "sets
  199| 				    the appropriate IS bit"), of the highest
  200| 				    unmasked request -- the raw irr scan that stood
  201| 				    here returned masked lines too.  One read per
  202| 				    poll: later reads return the IRR until the next
  203| 				    OCW3.  */
  204| 				i = pic8259_acknowledge(d, cpu->machine);
  205| 				odata = i < 0 ? 0x00 : (0x80 | i);
  206| 				d->current_command = 0x0a;
  207| 				break;
  208| 			default:
  209| 				odata = 0x00;
  210| 				for (i=0; i<8; i++)
  211| 					if ((d->irr >> i) & 1) {
  212| 						odata = 0x80 | i;
  213| 						break;
  214| 					}
  215| 				break;
  216| 			/*
  217| 			 *  TODO: The "default" label should really do
  218| 			 *  something like this:
  219| 			 *
  220| 			 *	fatal("[ 8259: unimplemented command 0x%02x"
  221| 			 *	    " while reading ]\n", d->current_command);
  222| 			 *	cpu->running = 0;
  223| 			 *
  224| 			 *  but Linux seems to read from the secondary PIC
  225| 			 *  in a manner which works better the way things
  226| 			 *  are coded right now.
  227| 			 */
  228| 			}
  229| 		}
  230| 		break;
  231| 	case 0x01:
  232| 		if (d->init_state > 0) {
  233| 			if (d->init_state == 1) {
  234| 				d->irq_base = idata & 0xf8;
  235| 				/*  This happens on non-x86 machines:
  236| 				    if (idata & 7)
  237| 					fatal("[ 8259: WARNING! Lowest"
  238| 					    " bits in Init Cmd 1 are"
  239| 					    " non-zero! ]\n");  */
  240| 				d->init_state = 2;
  241| 			} else if (d->init_state == 2) {
  242| 				/*  Slave attachment. TODO  */
  243| 				d->init_state = 3;
  244| 			} else if (d->init_state == 3) {
  245| 				if (idata & 0x02) {
  246| 					/*  Should not be set in PCs, but
  247| 					    on CATS, for example, it is set.  */
  248| 					debug("[ 8259: WARNING! Bit 1 i"
  249| 					    "n Init Cmd 4 is set! ]\n");
  250| 				}
  251| 				if (!(idata & 0x01))
  252| 					fatal("[ 8259: WARNING! Bit 0 "
  253| 					    "in Init Cmd 4 is not"
  254| 					    " set! ]\n");
  255| 				d->init_state = 0;
  256| 			}
  257| 			break;
  258| 		}
  259| 
  260| 		if (writeflag == MEM_WRITE) {
  261| 			int old_ier = d->ier;
  262| 			d->ier = idata;
  263| 
  264| 			/*  Recalculate interrupt assertions,
  265| 			    if necessary:  */
  266| 			if ((d->irr & ~old_ier) != (d->irr & ~d->ier)) {
  267| 				if (d->irr & ~d->ier)
  268| 					INTERRUPT_ASSERT(d->irq);
  269| 				else
  270| 					INTERRUPT_DEASSERT(d->irq);
  271| 			}
  272| 		} else {
  273| 			odata = d->ier;
  274| 		}
  275| 		break;
  276| 	default:
  277| 		if (writeflag == MEM_WRITE) {
  278| 			fatal("[ 8259: unimplemented write to address 0x%x"
  279| 			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
  280| 			cpu->running = 0;
  281| 		} else {
  282| 			fatal("[ 8259: unimplemented read from address 0x%x "
  283| 			    "]\n", (int)relative_addr);
  284| 			cpu->running = 0;
  285| 		}
  286| 	}
  287| 
  288| 	if (writeflag == MEM_READ)
  289| 		memory_writemax64(cpu, data, len, odata);
  290| 
  291| 	return 1;
  292| }
  293| 
  294| 
  295| /*
  296|  *  devinit_8259():
  297|  *
  298|  *  Initialize an 8259 PIC. Important notes:
  299|  *
  300|  *	x)  Most systems use _TWO_ 8259 PICs. These should be registered
  301|  *	    as separate devices.
  302|  *
  303|  *	x)  The irq number specified is the number used to re-calculate
  304|  *	    CPU interrupt assertions.  It is _not_ the irq number at
  305|  *	    which the PIC is connected. (That is left to machine specific
  306|  *	    code in src/machine.c.)
  307|  */
  308| DEVINIT(8259)
  309| {
  310| 	struct pic8259_data *d;
  311| 	char *name2;
  312| 	size_t nlen = strlen(devinit->name) + 20;
  313| 
  314| 	CHECK_ALLOCATION(d = (struct pic8259_data *) malloc(sizeof(struct pic8259_data)));
  315| 	memset(d, 0, sizeof(struct pic8259_data));
  316| 
  317| 	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);
  318| 
  319| 	CHECK_ALLOCATION(name2 = (char *) malloc(nlen));
  320| 	snprintf(name2, nlen, "%s", devinit->name);
  321| 	if ((devinit->addr & 0xfff) == 0xa0) {
  322| 		strlcat(name2, " [secondary]", nlen);
  323| 		d->irq_base = 8;
  324| 	}
  325| 
  326| 	memory_device_register(devinit->machine->memory, name2,
  327| 	    devinit->addr, DEV_8259_LENGTH, dev_8259_access, d,
  328| 	    DM_DEFAULT, NULL);
  329| 
  330| 	devinit->return_ptr = d;
  331| 	return 1;
  332| }
  333| 
  334| 
```

## The data structures those files define (every field that exists)

### `src/include/devices.h` -- `struct pic8259_data` (HEAD lines 63-75)

```c
   63| struct pic8259_data {
   64| 	struct interrupt irq;
   65| 
   66| 	int		irq_base;
   67| 	int		current_command;
   68| 
   69| 	int		init_state;
   70| 
   71| 	int		priority_reg;
   72| 	uint8_t		irr;		/*  interrupt request register  */
   73| 	uint8_t		isr;		/*  interrupt in-service register  */
   74| 	uint8_t		ier;		/*  interrupt enable register  */
   75| };
```

RULES FOR THE EDITS: change ONLY text that appears in this packet; use ONLY fields, functions and macros that appear in it
(a draft that calls an undeclared function or a field that does not exist does not compile); make each `old` long enough to
occur exactly once in its file -- include a distinctive neighbouring line when a statement repeats.

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_I8259INITREAD: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
