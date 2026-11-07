# GXemul hardened fork -- DRAFT A FIX for one filed issue, `gssiglblid` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at lines the coordinator LOCATED from names the row uses (the row cites none) (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `gssiglblid`, state `open`, severity `MED`)

**title:** ps2_gs: N_GS_REGS excludes the file's own highest register, so SIGLBLID (0x1080) is refused -- writes dropped, reads 0

**state_note (head):**

GOVERNING TEXT (from the dispositions file, cut at 400 characters): omised (dev_rtc.c:54-82, :158; doc/experiments.html:512). * `gssiglblid` MED -- ps2_gs: `N_GS_REGS 0x108` excludes the file's own highest register, so SIGLBLID (0x108) is refused (writes dropped, reads 0) by #99's guard (dev_ps2_gs.c:46, :77-81, :94-105). No GS manual on disk; ruled on the file's own table (the draft's DOUBTFUL overturned). * `mpstartupsp` MED -- dev_mp ST

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- The register constant failing to encompass its own documented highest register is a logic defect.

## The code at the cited lines

### `src/devices/dev_ps2_gs.c` around line 46 -- LOCATED BY THE COORDINATOR from the name `N_GS_REGS` the row uses (the row cites no line; check this is the defect's site) (HEAD 8d9df658, lines 1-166)

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
   28|  *  COMMENT: PlayStation 2 graphics system
   29|  */
   30| 
   31| #include <stdio.h>
   32| #include <stdlib.h>
   33| #include <string.h>
   34| 
   35| #include "device.h"
   36| #include "machine.h"
   37| #include "memory.h"
   38| #include "misc.h"
   39| 
   40| 
   41| #define	DEV_PS2_GS_LENGTH		0x2000
   42| 
   43| /*  NOTE/TODO: This should be the same as in ps2_stuff:  */
   44| #define	DEV_PS2_GIF_FAKE_BASE		0x50000000
   45| 
   46| #define	N_GS_REGS	0x108
   47| 
   48| struct gs_data {
   49| 	uint64_t	reg[N_GS_REGS];		/*  GS registers  */
   50| };
   51| 
   52| #define	GS_S_PMODE_REG		0x00
   53| #define	GS_S_SMODE1_REG		0x01
   54| #define	GS_S_SMODE2_REG		0x02
   55| #define	GS_S_SRFSH_REG		0x03
   56| #define	GS_S_SYNCH1_REG		0x04
   57| #define	GS_S_SYNCH2_REG		0x05
   58| #define	GS_S_SYNCV_REG		0x06
   59| #define	GS_S_DISPFB1_REG	0x07
   60| #define	GS_S_DISPLAY1_REG	0x08
   61| #define	GS_S_DISPFB2_REG	0x09
   62| #define	GS_S_DISPLAY2_REG	0x0a
   63| #define	GS_S_EXTBUF_REG0	0x0b
   64| #define	GS_S_EXTDATA_REG	0x0c
   65| #define	GS_S_EXTWRITE_REG	0x0d
   66| #define	GS_S_BGCOLOR_REG	0x0e
   67| 
   68| //static const char *gs_reg_names[15] = {
   69| //	"PMODE", "SMODE1", "SMODE2", "SRFSH",
   70| //	"SYNCH1", "SYNCH2", "SYNCV", "DISPFB1",
   71| //	"DISPLAY1", "DISPFB2", "DISPLAY2", "EXTBUF",
   72| //	"EXTDATA", "EXTWRITE", "BGCOLOR"  };
   73| 
   74| #define	GS_S_CSR_REG		0x100
   75| #define	GS_S_IMR_REG		0x101
   76| #define	GS_S_BUSDIR_REG		0x104
   77| #define	GS_S_SIGLBLID_REG	0x108
   78| 
   79| //static const char *gs_reg_high_names[4] = {
   80| //	"CSR", "IMR", "BUSDIR", "SIGLBLID"
   81| //	};
   82| 
   83| 
   84| DEVICE_ACCESS(ps2_gs)
   85| {
   86| 	struct gs_data *d = (struct gs_data *) extra;
   87| 	uint64_t idata = 0, odata = 0;
   88| 	size_t i;
   89| 	int regnr;
   90| 
   91| 	if (writeflag == MEM_WRITE)
   92| 		idata = memory_readmax64(cpu, data, len);
   93| 
   94| 	regnr = relative_addr / 16;
   95| 	if (regnr < 0 || regnr >= N_GS_REGS) {	/* #99: guest offset can exceed reg[] */
   96| 		static int warned = 0;	/* #119: loud-once (course-correction; was debug) */
   97| 		if (!warned) {
   98| 			fatal("[ gs: register access out of range (addr 0x%x); "
   99| 			    "ignored ]\n", (int)relative_addr);
  100| 			warned = 1;
  101| 		}
  102| 		if (writeflag == MEM_READ)
  103| 			memory_writemax64(cpu, data, len, 0);
  104| 		return 1;
  105| 	}
  106| 	if (relative_addr & 0xf) {
  107| 		debug("[ gs unaligned access, addr 0x%x ]\n",
  108| 		    (int)relative_addr);
  109| 		return 0;
  110| 	}
  111| 
  112| 	/*  Empty the GS FIFO:  */
  113| 	d->reg[GS_S_CSR_REG] &= ~(3 << 14);
  114| 	d->reg[GS_S_CSR_REG] |=  (1 << 14);
  115| 
  116| 	switch (relative_addr) {
  117| 	default:
  118| 		if (writeflag==MEM_READ) {
  119| 			debug("[ gs read from addr 0x%x ]\n",
  120| 			    (int)relative_addr);
  121| 			odata = d->reg[regnr];
  122| 		} else {
  123| 			debug("[ gs write to addr 0x%x:", (int)relative_addr);
  124| 			for (i=0; i<len; i++)
  125| 				debug(" %02x", data[i]);
  126| 			debug(" ]\n");
  127| 			d->reg[regnr] = idata;
  128| 			return 1;
  129| 		}
  130| 	}
  131| 
  132| 	if (writeflag == MEM_READ)
  133| 		memory_writemax64(cpu, data, len, odata);
  134| 
  135| 	return 1;
  136| }
  137| 
  138| 
  139| /*
  140|  *  devinit_ps2_gs():
  141|  *
  142|  *  Initialize the Playstation 2 graphics system. This is a bit tricky.
  143|  *  'gs' is the memory mapped device, as seen by the main processor.
  144|  *  'gif' is another thing which has its own memory.  DMA is used to
  145|  *  transfer stuff to the gif from the main memory.
  146|  *  There is also a framebuffer, which is separated from the main
  147|  *  memory.
  148|  *
  149|  *  TODO:  Make this clearer.
  150|  */
  151| DEVINIT(ps2_gs)
  152| {
  153| 	struct gs_data *d;
  154| 	char str[100];
  155| 
  156| 	CHECK_ALLOCATION(d = (struct gs_data *) malloc(sizeof(struct gs_data)));
  157| 	memset(d, 0, sizeof(struct gs_data));
  158| 
  159| 	snprintf(str, sizeof(str) - 1, "ps2_gif addr=0x%llx",
  160| 	    (long long)DEV_PS2_GIF_FAKE_BASE);
  161| 	device_add(devinit->machine, str);
  162| 
  163| 	memory_device_register(devinit->machine->memory, devinit->name,
  164| 	    devinit->addr, DEV_PS2_GS_LENGTH, dev_ps2_gs_access, d,
  165| 	    DM_DEFAULT, NULL);
  166| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_ps2_gs.c` -- `struct gs_data {` (HEAD lines 48-50)

```c
   48| struct gs_data {
   49| 	uint64_t	reg[N_GS_REGS];		/*  GS registers  */
   50| };
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

End with one line: `FIXDRAFT_GSSIGLBLID: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
