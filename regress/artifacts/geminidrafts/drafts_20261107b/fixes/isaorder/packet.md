# GXemul hardened fork -- DRAFT A FIX for one filed issue, `isaorder` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `isaorder`, state `held`, severity `-`)

**title:** isaorder  bus_isa copies a pointer before the device that sets it is added, so the timer-interrupt ack can never run

**state_note (head):**

*** EVIDENCE 2026-08-27: TRUE structurally, but LATENT -- no guest-visible channel exists today, so it cannot be witnessed or detected without changing the code first. ***

**True:** `bus_isa` copies a pointer before the device that sets it has been added, so `d->ptr_to_pending_timer_interrupts` is NULL afterwards.

**But nothing dereferences it.** The consumer is the ISA-device deassert of line 0 -- the `... & 1 && !(irr & 1)` test -- **which never happens**. Programming the PIT (guest I/O sets `in_use=1`) reaches the ticks and the IRQ 0 *assert*, but never that decrement path.

> **So a detector row is impossible without a product change**, and a fix on its own is unobservable. That is the definition of dormant defensive debt, and it ranks below every guest-reachable row.

*** THE FIX IDIOM IS FIFTEEN LINES ABOVE, IN THE SAME FUNCTION. *** `pic1` is taken from `device_add`'s return value -- i.e. after the device exists -- which is exactly the ordering this pointer copy fails to observe. A transferred warrant, and a cheap one.

*A seat also noted the contrast worth keeping: elsewhere (mc146818) the same-class pending ack is done LOCALLY -- the device decrements its own counter on the guest ack and deasserts there -- rather than through a copied pointer. The copied-pointer shape is the outlier.*

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- use the pic1 fix idiom from 15 lines above to properly sequence the device_add.

## The code at the cited lines

### `src/devices/bus_isa.c` around line 40 -- LOCATED BY THE COORDINATOR from the name `bus_isa` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 1-160)

```c
    1| /*
    2|  *  Copyright (C) 2005-2009  Anders Gavare.  All rights reserved.
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
   28|  *  COMMENT: Generic ISA bus framework
   29|  *
   30|  *  This is not a normal device, but it can be used as a quick way of adding
   31|  *  most of the common legacy ISA devices to a machine.
   32|  */
   33| 
   34| #include <stdio.h>
   35| #include <stdlib.h>
   36| #include <string.h>
   37| 
   38| #define BUS_ISA_C
   39| 
   40| #include "bus_isa.h"
   41| #include "device.h"
   42| #include "devices.h"
   43| #include "diskimage.h"
   44| #include "interrupt.h"
   45| #include "machine.h"
   46| #include "misc.h"
   47| 
   48| 
   49| /*
   50|  *  isa_interrupt_common():
   51|  */
   52| void isa_interrupt_common(struct bus_isa_data *d, int old_isa_assert)
   53| {
   54| 	int new_isa_assert, x;
   55| 
   56| 	/*  Any interrupt assertions on PIC2 go to irq 2 on PIC1  */
   57| 	/*  (TODO: don't hardcode this here)  */
   58| 	if (d->pic2->irr & ~d->pic2->ier)
   59| 		d->pic1->irr |= 0x04;
   60| 	else
   61| 		d->pic1->irr &= ~0x04;
   62| 
   63| 	/*  printf("ISA: irr=%02x%02x ier=%02x%02x\n",
   64| 	    d->pic2->irr, d->pic1->irr, d->pic2->ier, d->pic1->ier);  */
   65| 
   66| 	new_isa_assert = d->pic1->irr & ~d->pic1->ier;
   67| 
   68| 	if (old_isa_assert == new_isa_assert)
   69| 		return;
   70| 
   71| 	if (!new_isa_assert) {
   72| 		INTERRUPT_DEASSERT(d->irq);
   73| 		return;
   74| 	}
   75| 
   76| 	for (x=0; x<16; x++) {
   77| 		if (x == 2)
   78| 			continue;
   79| 
   80| 		if (x < 8 && (d->pic1->irr & ~d->pic1->ier & (1 << x)))
   81| 			break;
   82| 
   83| 		if (x >= 8 && (d->pic2->irr & ~d->pic2->ier & (1 << (x&7))))
   84| 			break;
   85| 	}
   86| 
   87| 	*d->ptr_to_last_int = x;
   88| 
   89| 	INTERRUPT_ASSERT(d->irq);
   90| }
   91| 
   92| 
   93| /*
   94|  *  isa_interrupt_assert():
   95|  *
   96|  *  Called whenever an ISA device asserts an interrupt (0..15).
   97|  */
   98| void isa_interrupt_assert(struct interrupt *interrupt)
   99| {
  100| 	struct bus_isa_data *d = (struct bus_isa_data *) interrupt->extra;
  101| 	int old_isa_assert, line = interrupt->line;
  102| 	int mask = 1 << (line & 7);
  103| 
  104| 	old_isa_assert = d->pic1->irr & ~d->pic1->ier;
  105| 
  106| 	if (line < 8)
  107| 		d->pic1->irr |= mask;
  108| 	else if (d->pic2 != NULL)
  109| 		d->pic2->irr |= mask;
  110| 
  111| 	isa_interrupt_common(d, old_isa_assert);
  112| }
  113| 
  114| 
  115| /*
  116|  *  isa_interrupt_deassert():
  117|  *
  118|  *  Called whenever an ISA device deasserts an interrupt (0..15).
  119|  */
  120| void isa_interrupt_deassert(struct interrupt *interrupt)
  121| {
  122| 	struct bus_isa_data *d = (struct bus_isa_data *) interrupt->extra;
  123| 	int line = interrupt->line, mask = 1 << (line & 7);
  124| 	int old_irr1 = d->pic1->irr, old_isa_assert;
  125| 
  126| 	old_isa_assert = old_irr1 & ~d->pic1->ier;
  127| 
  128| 	if (line < 8)
  129| 		d->pic1->irr &= ~mask;
  130| 	else if (d->pic2 != NULL)
  131| 		d->pic2->irr &= ~mask;
  132| 
  133| 	/*  If IRQ 0 has been cleared, then this is a timer interrupt.
  134| 	    Let's ack it here:  */
  135| 	if (old_irr1 & 1 && !(d->pic1->irr & 1) &&
  136| 	    d->ptr_to_pending_timer_interrupts != NULL &&
  137|             (*d->ptr_to_pending_timer_interrupts) > 0)
  138|                 (*d->ptr_to_pending_timer_interrupts) --;
  139| 
  140| 	isa_interrupt_common(d, old_isa_assert);
  141| }
  142| 
  143| 
  144| /*
  145|  *  bus_isa_init():
  146|  *
  147|  *  Flags are zero or more of the following, ORed together:
  148|  *
  149|  *  BUS_ISA_EXTERNAL_PIC	Don't register/use isa_interrupt_*().
  150|  *  BUS_ISA_IDE0		Include wdc0.
  151|  *  BUS_ISA_IDE1		Include wdc1.
  152|  *  BUS_ISA_FDC			Include a floppy controller. (Dummy.)
  153|  *  BUS_ISA_VGA			Include old-style (non-PCI) VGA. (*1)
  154|  *  BUS_ISA_VGA_FORCE		Include VGA even when running without X11. (*2)
  155|  *  BUS_ISA_PCKBC_FORCE_USE	Always assume keyboard console, not serial. (*3)
  156|  *  BUS_ISA_PCKBC_NONPCSTYLE	Don't set the pc-style flag for the keyboard.
  157|  *  BUS_ISA_NO_SECOND_PIC	Only useful for 8086 XT (pre-AT) emulation. :-)
  158|  *  BUS_ISA_LPTBASE_3BC		Set lptbase to 0x3bc instead of 0x378.
  159|  *
  160|  *  (*1) For machines with a PCI bus, this flag should not be used. Instead, a
```

## The data structures those files define (every field that exists)

### `src/include/bus_isa.h` -- `struct bus_isa_data` (HEAD lines 39-49)

```c
   39| struct bus_isa_data {
   40| 	struct interrupt irq;
   41| 
   42| 	struct pic8259_data* pic1;
   43| 	struct pic8259_data* pic2;
   44| 	int		*ptr_to_pending_timer_interrupts;
   45| 	int		*ptr_to_last_int;
   46| 
   47| 	uint64_t	isa_portbase;
   48| 	uint64_t	isa_membase;
   49| };
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

End with one line: `FIXDRAFT_ISAORDER: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
