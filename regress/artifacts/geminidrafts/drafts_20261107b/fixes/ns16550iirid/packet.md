# GXemul hardened fork -- DRAFT A FIX for one filed issue, `ns16550iirid` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `ns16550iirid`, state `open`, severity `MED`)

**title:** devices/dev_ns16550.c DEVICE_TICK / IIR read -- IIR ORs RXRDY and TXRDY flag bits (RX + THRE reads 0x6, the line-status ID) and every IIR read clears THRE -- WRONG-RESULT (shared UART model)

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T48 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: small; report rows: A3-34, A5-11, A(c)#7).  Source URLs: https://github.com/jroark/GXemul/commit/2a1a395a693cbcd2f635d88b9204842c88d6b902, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/f58d6d745800f300eecab01e97d8630c15e20daf, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/705f50bff202ca43b5c79f1cc3e303e120f26ba4.  Our site at de8c7547: src/devices/dev_ns16550.c:83-104, :212-213.  Portable fix: yes -- port jroark 2a1a395 / rs6000 f58d6d7, rs6000 705f50b (fixed independently twice).  Filing check (TRIAGE.md): `lcaisalane` notes "IIR read clears TXRDY" as a disclosure only.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port jroark 2a1a395

## The code at the cited lines

### `src/devices/dev_ns16550.c` around the row's cited line 83 (HEAD 8d9df658, lines 1-203)

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
   28|  *  COMMENT: NS16550 serial controller
   29|  *
   30|  *  TODO: Implement the FIFO.
   31|  */
   32| 
   33| #include <stdio.h>
   34| #include <stdlib.h>
   35| #include <string.h>
   36| 
   37| #include "console.h"
   38| #include "cpu.h"
   39| #include "device.h"
   40| #include "interrupt.h"
   41| #include "machine.h"
   42| #include "memory.h"
   43| #include "misc.h"
   44| 
   45| #include "thirdparty/comreg.h"
   46| 
   47| 
   48| /*  #define debug fatal  */
   49| 
   50| #define	TICK_SHIFT		14
   51| #define	DEV_NS16550_LENGTH	8
   52| 
   53| struct ns_data {
   54| 	int		addrmult;
   55| 	int		in_use;
   56| 	const char	*name;
   57| 	int		console_handle;
   58| 	int		enable_fifo;
   59| 
   60| 	struct interrupt irq;
   61| 
   62| 	unsigned char	reg[DEV_NS16550_LENGTH];
   63| 	unsigned char	fcr;		/*  FIFO control register  */
   64| 	int		int_asserted;
   65| 	int		dlab;		/*  Divisor Latch Access bit  */
   66| 	int		divisor;
   67| 
   68| 	int		databits;
   69| 	char		parity;
   70| 	const char	*stopbits;
   71| };
   72| 
   73| 
   74| DEVICE_TICK(ns16550)
   75| {
   76| 	/*
   77| 	 *  This function is called at regular intervals. An interrupt is
   78| 	 *  asserted if there is a character available for reading, or if the
   79| 	 *  transmitter slot is empty (i.e. the ns16550 is ready to transmit).
   80| 	 */
   81| 	struct ns_data *d = (struct ns_data *) extra;
   82| 
   83| 	d->reg[com_iir] &= ~IIR_RXRDY;
   84| 	if (console_charavail(d->console_handle))
   85| 		d->reg[com_iir] |= IIR_RXRDY;
   86| 
   87| 	/*
   88| 	 *  If interrupts are enabled, and interrupts are pending, then
   89| 	 *  cause a CPU interrupt.
   90|  	 */
   91| 
   92| 	if (((d->reg[com_ier] & IER_ETXRDY) && (d->reg[com_iir] & IIR_TXRDY)) ||
   93| 	    ((d->reg[com_ier] & IER_ERXRDY) && (d->reg[com_iir] & IIR_RXRDY))) {
   94| 		d->reg[com_iir] &= ~IIR_NOPEND;
   95| 		if (d->reg[com_mcr] & MCR_IENABLE) {
   96| 			INTERRUPT_ASSERT(d->irq);
   97| 			d->int_asserted = 1;
   98| 		}
   99| 	} else {
  100| 		d->reg[com_iir] |= IIR_NOPEND;
  101| 		if (d->int_asserted)
  102| 			INTERRUPT_DEASSERT(d->irq);
  103| 		d->int_asserted = 0;
  104| 	}
  105| }
  106| 
  107| 
  108| DEVICE_ACCESS(ns16550)
  109| {
  110| 	uint64_t idata = 0, odata=0;
  111| 	size_t i;
  112| 	struct ns_data *d = (struct ns_data *) extra;
  113| 
  114| 	if (writeflag == MEM_WRITE)
  115| 		idata = memory_readmax64(cpu, data, len);
  116| 
  117| #if 0
  118| 	/*  The NS16550 should be accessed using byte read/writes:  */
  119| 	if (len != 1)
  120| 		fatal("[ ns16550 (%s): len=%i, idata=0x%16llx! ]\n",
  121| 		    d->name, len, (long long)idata);
  122| #endif
  123| 
  124| 	/*
  125| 	 *  Always ready to transmit:
  126| 	 */
  127| 	d->reg[com_lsr] |= LSR_TXRDY | LSR_TSRE;
  128| 	d->reg[com_msr] |= MSR_DCD | MSR_DSR | MSR_CTS;
  129| 
  130| 	d->reg[com_iir] &= ~0xf0;
  131| 	if (d->enable_fifo)
  132| 		d->reg[com_iir] |= ((d->fcr << 5) & 0xc0);
  133| 
  134| 	d->reg[com_lsr] &= ~LSR_RXRDY;
  135| 	if (console_charavail(d->console_handle))
  136| 		d->reg[com_lsr] |= LSR_RXRDY;
  137| 
  138| 	relative_addr /= d->addrmult;
  139| 
  140| 	if (relative_addr >= DEV_NS16550_LENGTH) {
  141| 		fatal("[ ns16550 (%s): outside register space? relative_addr="
  142| 		    "0x%llx. bad addrmult? bad device length? ]\n", d->name,
  143| 		    (long long)relative_addr);
  144| 		return 0;
  145| 	}
  146| 
  147| 	switch (relative_addr) {
  148| 
  149| 	case com_data:	/*  data AND low byte of the divisor  */
  150| 		/*  Read/write of the Divisor value:  */
  151| 		if (d->dlab) {
  152| 			/*  Write or read the low byte of the divisor:  */
  153| 			if (writeflag == MEM_WRITE)
  154| 				d->divisor = (d->divisor & 0xff00) | idata;
  155| 			else
  156| 				odata = d->divisor & 0xff;
  157| 			break;
  158| 		}
  159| 
  160| 		/*  Read/write of data:  */
  161| 		if (writeflag == MEM_WRITE) {
  162| 			if (d->reg[com_mcr] & MCR_LOOPBACK)
  163| 				console_makeavail(d->console_handle, idata);
  164| 			else
  165| 				console_putchar(d->console_handle, idata);
  166| 			d->reg[com_iir] |= IIR_TXRDY;
  167| 		} else {
  168| 			int x = console_readchar(d->console_handle);
  169| 			odata = x < 0? 0 : x;
  170| 		}
  171| 		dev_ns16550_tick(cpu, d);
  172| 		break;
  173| 
  174| 	case com_ier:	/*  interrupt enable AND high byte of the divisor  */
  175| 		/*  Read/write of the Divisor value:  */
  176| 		if (d->dlab) {
  177| 			if (writeflag == MEM_WRITE) {
  178| 				/*  Set the high byte of the divisor:  */
  179| 				d->divisor = (d->divisor & 0xff) | (idata << 8);
  180| 				debug("[ ns16550 (%s): speed set to %i bps ]\n",
  181| 				    d->name, (int)(115200 / d->divisor));
  182| 			} else
  183| 				odata = d->divisor >> 8;
  184| 			break;
  185| 		}
  186| 
  187| 		/*  IER:  */
  188| 		if (writeflag == MEM_WRITE) {
  189| 			/*  This is to supress Linux' behaviour  */
  190| 			if (idata != 0)
  191| 				debug("[ ns16550 (%s): write to ier: 0x%02x ]"
  192| 				    "\n", d->name, (int)idata);
  193| 
  194| 			/*  Needed for NetBSD 2.0.x, but not 1.6.2?  */
  195| 			if (!(d->reg[com_ier] & IER_ETXRDY)
  196| 			    && (idata & IER_ETXRDY))
  197| 				d->reg[com_iir] |= IIR_TXRDY;
  198| 
  199| 			d->reg[com_ier] = idata;
  200| 			dev_ns16550_tick(cpu, d);
  201| 		} else
  202| 			odata = d->reg[com_ier];
  203| 		break;
```

## The data structures those files define (every field that exists)

### `src/devices/dev_ns16550.c` -- `struct ns_data {` (HEAD lines 53-71)

```c
   53| struct ns_data {
   54| 	int		addrmult;
   55| 	int		in_use;
   56| 	const char	*name;
   57| 	int		console_handle;
   58| 	int		enable_fifo;
   59| 
   60| 	struct interrupt irq;
   61| 
   62| 	unsigned char	reg[DEV_NS16550_LENGTH];
   63| 	unsigned char	fcr;		/*  FIFO control register  */
   64| 	int		int_asserted;
   65| 	int		dlab;		/*  Divisor Latch Access bit  */
   66| 	int		divisor;
   67| 
   68| 	int		databits;
   69| 	char		parity;
   70| 	const char	*stopbits;
   71| };
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

End with one line: `FIXDRAFT_NS16550IIRID: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
