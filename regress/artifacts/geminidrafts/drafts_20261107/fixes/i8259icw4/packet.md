# GXemul hardened fork -- DRAFT A FIX for one filed issue, `i8259icw4` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `i8259icw4`, state `open`, severity `MED`)

**title:** devices/dev_8259.c init sequence -- ICW1 SNGL/IC4 are ignored, so with IC4=0 the guest's first OCW1 mask write is swallowed as ICW4 -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T50 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A5-26, A(c)#11).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/598ab108cacb56dfbeae33eb463fd2b8c18393dd.  Our site at de8c7547: src/devices/dev_8259.c:183-206.  Portable fix: yes -- port rs6000 598ab10.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 598ab10 is available

## The code at the cited lines

### `src/devices/dev_8259.c` around the row's cited line 183 (HEAD d2a6f233, lines 138-228)

```c
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

End with one line: `FIXDRAFT_I8259ICW4: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
