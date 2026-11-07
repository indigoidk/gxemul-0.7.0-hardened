# GXemul hardened fork -- DRAFT A FIX for one filed issue, `i8259pollcomment` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `i8259pollcomment`, state `open`, severity `LOW`)

**title:** src/devices/dev_8259.c:137 -- the 0x0c arm's comment Put Master in Buffered Mode describes ICW4's BUF bit, but 0x0c on the command port is the OCW3 poll command -- RECORD

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- The comment misidentifies the 0x0c command.

## The code at the cited lines

### `src/devices/dev_8259.c` around the row's cited line 137 (HEAD 8d9df658, lines 17-257)

```c
   17|  *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|  *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|  *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|  *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|  *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|  *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|  *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|  *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|  *  SUCH DAMAGE.
   26|  *   
   27|  *
   28|  *  COMMENT: Intel 8259 Programmable Interrupt Controller
   29|  *
   30|  *  See the following URL for more details:
   31|  *	http://www.nondot.org/sabre/os/files/MiscHW/8259pic.txt
   32|  */
   33| 
   34| #include <stdio.h>
   35| #include <stdlib.h>
   36| #include <string.h>
   37| 
   38| #include "cpu.h"
   39| #include "device.h"
   40| #include "devices.h"
   41| #include "emul.h"
   42| #include "machine.h"
   43| #include "memory.h"
   44| #include "misc.h"
   45| 
   46| 
   47| #define	DEV_8259_LENGTH		2
   48| 
   49| /*  #define DEV_8259_DEBUG  */
   50| 
   51| 
   52| /*
   53|  *  pic8259_acknowledge():
   54|  *
   55|  *  #574: The acknowledge this model never had.  The chip moves the highest-priority
   56|  *  unmasked request to service when the CPU acknowledges it (the INTA cycle, or the
   57|  *  read that follows an OCW3 poll): the ISR bit is set and, in edge mode -- the only
   58|  *  mode this tree's guests program (ICW1 0x11) -- the IRR bit is reset.  Called from
   59|  *  the poll read below and from the GT64120 interrupt-acknowledge read (dev_gt.c).
   60|  *  Line 0 of pic1 is the 8253, whose pending-event count is retired here: dev_8253.c
   61|  *  publishes it through machine->isa_pic_data, and bus_isa.c's own decrement runs
   62|  *  only inside a deassert the 8253 never issues.  Returns the acknowledged line, or
   63|  *  -1 when no unmasked request is pending (nothing changes).
   64|  */
   65| int pic8259_acknowledge(struct pic8259_data *d, struct machine *m)
   66| {
   67| 	struct isa_pic_data *p = &m->isa_pic_data;
   68| 	int pending = d->irr & ~d->ier, n = 0;
   69| 
   70| 	if (pending == 0)
   71| 		return -1;
   72| 	while (!(pending & (1 << n)))
   73| 		n ++;
   74| 	d->isr |= 1 << n;
   75| 	d->irr &= ~(1 << n);
   76| 	if (d == p->pic1 && n == 0 && p->pending_timer_interrupts != NULL &&
   77| 	    *p->pending_timer_interrupts > 0)
   78| 		(*p->pending_timer_interrupts) --;
   79| 	/*  pic2's irq is the cascade line (bus_isa.c folds it into pic1 bit 2).  */
   80| 	if (d->irr & ~d->ier)
   81| 		INTERRUPT_ASSERT(d->irq);
   82| 	else
   83| 		INTERRUPT_DEASSERT(d->irq);
   84| 	return n;
   85| }
   86| 
   87| 
   88| DEVICE_ACCESS(8259)
   89| {
   90| 	struct pic8259_data *d = (struct pic8259_data *) extra;
   91| 	uint64_t idata = 0, odata = 0;
   92| 	int i;
   93| 
   94| 	if (writeflag == MEM_WRITE)
   95| 		idata = memory_readmax64(cpu, data, len);
   96| 
   97| #ifdef DEV_8259_DEBUG
   98| 	if (writeflag == MEM_READ)
   99| 		fatal("[ 8259: read from 0x%x ]\n", (int)relative_addr);
  100| 	else
  101| 		fatal("[ 8259: write to 0x%x: 0x%x ]\n",
  102| 		    (int)relative_addr, (int)idata);
  103| #endif
  104| 
  105| 	switch (relative_addr) {
  106| 	case 0x00:
  107| 		if (writeflag == MEM_WRITE) {
  108| 			if ((idata & 0x10) == 0x10) {
  109| 				/*  Bit 3: 0=edge, 1=level  */
  110| 				if (idata & 0x08)
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
```

## The data structures those files define (every field that exists)

### `src/include/machine.h` -- `struct isa_pic_data` (HEAD lines 48-54)

```c
   48| struct isa_pic_data {
   49| 	struct pic8259_data	*pic1;
   50| 	struct pic8259_data	*pic2;
   51| 
   52| 	int			*pending_timer_interrupts;
   53| 	int			last_int;
   54| };
```

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

End with one line: `FIXDRAFT_I8259POLLCOMMENT: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
