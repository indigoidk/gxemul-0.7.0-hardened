# GXemul hardened fork -- DRAFT A FIX for one filed issue, `i8259isrnever` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `i8259isrnever`, state `open`, severity `MED`)

**title:** devices/dev_8259.c + devices/dev_prep.c IACK -- ISR is never set (read-ISR returns 0) and the PReP IACK read has no acknowledge side effect -- WRONG-RESULT

**state_note (head):**

NARROWED by #574 on 2026-10-25: the OCW3 poll read and the GT64120 IACK read now set ISR (pic8259_acknowledge()); what remains is the PReP (dev_prep.c) and footbridge (dev_footbridge.c) vector reads, which return isa_pic_data.last_int with no acknowledge -- their guests' specific EOIs keep #574's legacy consume, so nothing regressed; converting them is this row's remaining work (no witness machine here).  ||  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T51 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A5-27, A(c)#11).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/598ab108cacb56dfbeae33eb463fd2b8c18393dd, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/174448c390ede42e884e26bd0b627ab43169dd11.  Our site at de8c7547: src/devices/dev_8259.c:108; src/devices/dev_prep.c:52-62.  Portable fix: yes -- port rs6000 598ab10, rs6000 174448c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port rs6000 598ab10, rs6000 174448c is available

## The code at the cited lines

### `src/devices/dev_8259.c` around the row's cited line 108 (HEAD d2a6f233, lines 63-153)

```c
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
```

### `src/devices/dev_prep.c` around the row's cited line 52 (HEAD d2a6f233, lines 7-86)

```c
    7|  *  1. Redistributions of source code must retain the above copyright
    8|  *     notice, this list of conditions and the following disclaimer.
    9|  *  2. Redistributions in binary form must reproduce the above copyright  
   10|  *     notice, this list of conditions and the following disclaimer in the 
   11|  *     documentation and/or other materials provided with the distribution.
   12|  *  3. The name of the author may not be used to endorse or promote products
   13|  *     derived from this software without specific prior written permission.
   14|  *
   15|  *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|  *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
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
   28|  *  COMMENT: PReP machine mainbus (ISA bus + interrupt controller)
   29|  */
   30| 
   31| #include <stdio.h>
   32| #include <stdlib.h>
   33| #include <string.h>
   34| 
   35| #include "bus_isa.h"
   36| #include "cpu.h"
   37| #include "device.h"
   38| #include "machine.h"
   39| #include "memory.h"
   40| #include "misc.h"
   41| 
   42| 
   43| struct prep_data {
   44| 	uint32_t		int_status;
   45| };
   46| 
   47| 
   48| DEVICE_ACCESS(prep)
   49| {
   50| 	/*  struct prep_data *d = extra;  */
   51| 	uint64_t idata = 0, odata = 0;
   52| 
   53| 	if (writeflag == MEM_WRITE)
   54| 		idata = memory_readmax64(cpu, data, len);
   55| 
   56| 	if (writeflag == MEM_READ) {
   57| 		odata = cpu->machine->isa_pic_data.last_int;
   58| 	} else {
   59| 		fatal("[ prep: write to interrupt register? idata = 0x%016" PRIx64" ]\n", idata);
   60| 	}
   61| 
   62| 	if (writeflag == MEM_READ)
   63| 		memory_writemax64(cpu, data, len, odata);
   64| 
   65| 	return 1;
   66| }
   67| 
   68| 
   69| DEVINIT(prep)
   70| {
   71| 	struct prep_data *d;
   72| 
   73| 	CHECK_ALLOCATION(d = (struct prep_data *) malloc(sizeof(struct prep_data)));
   74| 	memset(d, 0, sizeof(struct prep_data));
   75| 
   76| 	memory_device_register(devinit->machine->memory, devinit->name,
   77| 	    0xbffff000, 0x1000, dev_prep_access, d, DM_DEFAULT, NULL);
   78| 
   79| 	/*  This works for at least the IBM 6050:  */
   80| 	bus_isa_init(devinit->machine, devinit->interrupt_path,
   81| 	    BUS_ISA_IDE0 | BUS_ISA_IDE1, 0x80000000, 0xc0000000);
   82| 
   83| 	return 1;
   84| }
   85| 
   86| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_prep.c` -- `struct prep_data {` (HEAD lines 43-45)

```c
   43| struct prep_data {
   44| 	uint32_t		int_status;
   45| };
```

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

End with one line: `FIXDRAFT_I8259ISRNEVER: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.

## YOUR PREVIOUS DRAFT FAILED -- correct it

An earlier draft for this row was applied to the code above and checked.  It failed like this:

```text
BUILD FAILED (make rc=2 errors=1 warnings_in_edited=0):
dev_prep.c:60:25: error: implicit declaration of function 'pic8259_acknowledge' [-Wimplicit-function-declaration]
```

The previous edits:

```json
[
  {
    "file": "src/devices/dev_prep.c",
    "old": "\tif (writeflag == MEM_READ) {\n\t\todata = cpu->machine->isa_pic_data.last_int;\n\t} else {",
    "new": "\tif (writeflag == MEM_READ) {\n\t\todata = cpu->machine->isa_pic_data.last_int;\n\t\t/* #i8259isrnever: acknowledge the interrupt to update ISR */\n\t\tif (cpu->machine->isa_pic_data.pic1)\n\t\t\tpic8259_acknowledge(cpu->machine->isa_pic_data.pic1, cpu->machine);\n\t} else {",
    "why": "Acknowledge the interrupt on PReP IACK read to set the ISR."
  }
]
```


Return a CORRECTED draft in the same form.  If an `old` string occurred more than once, lengthen it with a distinctive
neighbouring line; if it occurred zero times, copy it exactly from the code shown; use only names that appear in this
packet.  If the fix cannot be written from what is shown, say `STILL PRESENT: UNSETTLED` and name what is missing.
