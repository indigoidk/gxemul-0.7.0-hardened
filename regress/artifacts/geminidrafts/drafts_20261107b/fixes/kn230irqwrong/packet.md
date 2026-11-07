# GXemul hardened fork -- DRAFT A FIX for one filed issue, `kn230irqwrong` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `kn230irqwrong`, state `open`, severity `MED`)

**title:** src/devices/dev_kn230.c:72-75,89-92 -- the SII/LANCE condition (assert3) asserts and deasserts mips_irq_2 instead of mips_irq_3, so those interrupts arrive on MIPS interrupt 2 and the deassert can drop line 2 while a DZ or option-slot source is still pending -- WRONG-RESULT (MIPSMATE 5100)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- incorrect interrupt line assertion causes emulator logic errors and must be routed to mips_irq_3.

## The code at the cited lines

### `src/devices/dev_kn230.c` around the row's cited line 72 (HEAD 8d9df658, lines 1-175)

```c
    1| /*
    2|  *  Copyright (C) 2003-2009  Anders Gavare.  All rights reserved.
    3|  *
    4|  *  Redistribution and use in source and binary forms, with or without
    5|  *  modification, are permitted provided that the following conditions are met:
    6|  *
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
   28|  *  COMMENT: DEC KN230 (MIPSMATE 5100) stuff
   29|  */
   30| 
   31| #include <stdio.h>
   32| #include <stdlib.h>
   33| #include <string.h>
   34| 
   35| #include "device.h"
   36| #include "interrupt.h"
   37| #include "machine.h"
   38| #include "memory.h"
   39| #include "misc.h"
   40| 
   41| #include "thirdparty/dec_5100.h"
   42| 
   43| 
   44| #define	DEV_KN230_LENGTH		0x1c00000
   45| 
   46| struct kn230_data {
   47| 	struct interrupt	mips_irq_2;
   48| 	struct interrupt	mips_irq_3;
   49| 
   50| 	uint32_t		csr;
   51| };
   52| 
   53| 
   54| /*  
   55|  *  kn230_interrupt_assert():
   56|  *  kn230_interrupt_deassert():
   57|  *
   58|  *  Called whenever a KN230 interrupt is asserted/deasserted.
   59|  */
   60| void kn230_interrupt_assert(struct interrupt *interrupt)
   61| {
   62| 	struct kn230_data *d = (struct kn230_data *) interrupt->extra;
   63| 	int assert2 = 0, assert3 = 0;
   64| 
   65| 	d->csr |= interrupt->line;
   66| 	if (d->csr & (KN230_CSR_INTR_SII | KN230_CSR_INTR_LANCE))
   67| 		assert3 = 1;
   68| 	if (d->csr & (KN230_CSR_INTR_DZ0 |
   69| 	    KN230_CSR_INTR_OPT0 | KN230_CSR_INTR_OPT1))
   70| 		assert2 = 1;
   71| 
   72| 	if (assert2)
   73|                 INTERRUPT_ASSERT(d->mips_irq_2);
   74| 	if (assert3)
   75|                 INTERRUPT_ASSERT(d->mips_irq_2);
   76| }
   77| void kn230_interrupt_deassert(struct interrupt *interrupt)
   78| {
   79| 	struct kn230_data *d = (struct kn230_data *) interrupt->extra;
   80| 	int assert2 = 0, assert3 = 0;
   81| 
   82| 	d->csr &= ~interrupt->line;
   83| 	if (d->csr & (KN230_CSR_INTR_SII | KN230_CSR_INTR_LANCE))
   84| 		assert3 = 1;
   85| 	if (d->csr & (KN230_CSR_INTR_DZ0 |
   86| 	    KN230_CSR_INTR_OPT0 | KN230_CSR_INTR_OPT1))
   87| 		assert2 = 1;
   88| 
   89| 	if (!assert2)
   90|                 INTERRUPT_DEASSERT(d->mips_irq_2);
   91| 	if (!assert3)
   92|                 INTERRUPT_DEASSERT(d->mips_irq_2);
   93| }
   94| 
   95| 
   96| DEVICE_ACCESS(kn230)
   97| {
   98| 	struct kn230_data *d = (struct kn230_data *) extra;
   99| 	uint64_t idata = 0, odata = 0;
  100| 
  101| 	if (writeflag == MEM_WRITE)
  102| 		idata = memory_readmax64(cpu, data, len);
  103| 
  104| 	switch (relative_addr) {
  105| 	case 0:
  106| 		if (writeflag==MEM_READ) {
  107| 			odata = d->csr;
  108| 			/* debug("[ kn230: read from CSR: 0x%08x ]\n",
  109| 			    (int)odata); */
  110| 		} else {
  111| 			/* debug("[ kn230: write to CSR: 0x%08x ]\n",
  112| 			    (int)idata); */
  113| 		}
  114| 		break;
  115| 	default:
  116| 		if (writeflag==MEM_READ) {
  117| 			debug("[ kn230: read from 0x%08lx ]\n",
  118| 			    (long)relative_addr);
  119| 		} else {
  120| 			debug("[ kn230: write to  0x%08lx: 0x%08x ]\n",
  121| 			    (long)relative_addr, (int)idata);
  122| 		}
  123| 	}
  124| 
  125| 	if (writeflag == MEM_READ)
  126| 		memory_writemax64(cpu, data, len, odata);
  127|   
  128| 	return 1;
  129| }
  130| 
  131| 
  132| DEVINIT(kn230)
  133| {
  134| 	struct kn230_data *d;
  135| 	char tmpstr[300];
  136| 	int i;
  137| 
  138| 	CHECK_ALLOCATION(d = (struct kn230_data *) malloc(sizeof(struct kn230_data)));
  139| 	memset(d, 0, sizeof(struct kn230_data));
  140| 
  141| 	/*
  142| 	 *  devinit->interrupt_path points to the MIPS cpu itself.
  143| 	 *  The KN230 interrupt controller interrupts at MIPS interrupts
  144| 	 *  2 and 3, depending on which KN230 is asserted.
  145| 	 */
  146| 	snprintf(tmpstr, sizeof(tmpstr), "%s.2", devinit->interrupt_path);
  147| 	INTERRUPT_CONNECT(tmpstr, d->mips_irq_2);
  148| 	snprintf(tmpstr, sizeof(tmpstr), "%s.3", devinit->interrupt_path);
  149| 	INTERRUPT_CONNECT(tmpstr, d->mips_irq_3);
  150| 
  151| 	/*  Register KN230 interrupts 8..15:  */
  152| 	for (i=8; i<=15; i++) {
  153| 		struct interrupt templ;
  154| 		char tmpstr2[300];
  155| 		snprintf(tmpstr2, sizeof(tmpstr2), "%s.kn230.0x%x",
  156| 		    devinit->interrupt_path, 1 << i);
  157| 		memset(&templ, 0, sizeof(templ));
  158| 		templ.line = (uint32_t)1 << i;
  159| 		templ.name = tmpstr2;
  160| 		templ.extra = d;
  161|                 templ.interrupt_assert = kn230_interrupt_assert;
  162|                 templ.interrupt_deassert = kn230_interrupt_deassert;
  163| 		interrupt_handler_register(&templ);
  164| 	}
  165| 
  166| 	memory_device_register(devinit->machine->memory, devinit->name,
  167| 	    devinit->addr, DEV_KN230_LENGTH, dev_kn230_access, d,
  168| 	    DM_DEFAULT, NULL);
  169| 
  170| 	devinit->return_ptr = d;
  171| 
  172| 	return 1;
  173| }
  174| 
  175| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_kn230.c` -- `struct kn230_data {` (HEAD lines 46-51)

```c
   46| struct kn230_data {
   47| 	struct interrupt	mips_irq_2;
   48| 	struct interrupt	mips_irq_3;
   49| 
   50| 	uint32_t		csr;
   51| };
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

End with one line: `FIXDRAFT_KN230IRQWRONG: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
