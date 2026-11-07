# GXemul hardened fork -- REVISE ONE FIX DRAFT after a review, `i8259isrnever` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork
removes crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  You drafted a fix for the
issue below; it compiles at HEAD 8d9df658.  A separate review then reported problems with it.  You cannot read files; work
from this text.  This is a DRAFTING task: FIX ONLY, as exact edits -- no tests, probes or reproduction steps.

## The issue (ledger row `i8259isrnever`, state `open`)

**title:** devices/dev_8259.c + devices/dev_prep.c IACK -- ISR is never set (read-ISR returns 0) and the PReP IACK read has no acknowledge side effect -- WRONG-RESULT

**state_note (head):** NARROWED by #574 on 2026-10-25: the OCW3 poll read and the GT64120 IACK read now set ISR (pic8259_acknowledge()); what remains is the PReP (dev_prep.c) and footbridge (dev_footbridge.c) vector reads, which return isa_pic_data.last_int with no acknowledge -- their guests' specific EOIs keep #574's legacy consume, so nothing regressed; converting them is this row's remaining work (no witness machine here).  ||  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T51 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A5-27, A(c)#11).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/598ab108cacb56dfbeae33eb463fd2b8c18393dd, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/174448c390ede42e884e26bd0b627ab43169dd11.  Our site at de8c7547: src/devices/dev_8259.c:108; src/devices/dev_prep.c:52-62.  Portable fix: yes -- port rs6000 598ab10, rs6000 174448c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

## Every function your previous draft changed, as it reads AT HEAD (your new edits apply to THIS text)

### `src/devices/dev_prep.c` -- AT HEAD, lines 1-86 (`*` marks a line your previous draft changed)

```c
    1|  /*
    2|   *  Copyright (C) 2005-2020  Anders Gavare.  All rights reserved.
    3|   *
    4|   *  Redistribution and use in source and binary forms, with or without
    5|   *  modification, are permitted provided that the following conditions are met:
    6|   *
    7|   *  1. Redistributions of source code must retain the above copyright
    8|   *     notice, this list of conditions and the following disclaimer.
    9|   *  2. Redistributions in binary form must reproduce the above copyright  
   10|   *     notice, this list of conditions and the following disclaimer in the 
   11|   *     documentation and/or other materials provided with the distribution.
   12|   *  3. The name of the author may not be used to endorse or promote products
   13|   *     derived from this software without specific prior written permission.
   14|   *
   15|   *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
   16|   *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   17|   *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   18|   *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
   19|   *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   20|   *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
   21|   *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
   22|   *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
   23|   *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
   24|   *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
   25|   *  SUCH DAMAGE.
   26|   *   
   27|   *
   28|   *  COMMENT: PReP machine mainbus (ISA bus + interrupt controller)
   29|   */
   30|  
   31|  #include <stdio.h>
   32|  #include <stdlib.h>
   33|  #include <string.h>
   34|  
   35|  #include "bus_isa.h"
   36|  #include "cpu.h"
   37|  #include "device.h"
   38|  #include "machine.h"
   39|  #include "memory.h"
   40|  #include "misc.h"
   41|  
   42|  
   43|  struct prep_data {
   44|  	uint32_t		int_status;
   45|  };
   46|  
   47|* 
   48|  DEVICE_ACCESS(prep)
   49|  {
   50|  	/*  struct prep_data *d = extra;  */
   51|  	uint64_t idata = 0, odata = 0;
   52|  
   53|  	if (writeflag == MEM_WRITE)
   54|  		idata = memory_readmax64(cpu, data, len);
   55|  
   56|  	if (writeflag == MEM_READ) {
   57|  		odata = cpu->machine->isa_pic_data.last_int;
   58|* 	} else {
   59|  		fatal("[ prep: write to interrupt register? idata = 0x%016" PRIx64" ]\n", idata);
   60|  	}
   61|  
   62|  	if (writeflag == MEM_READ)
   63|  		memory_writemax64(cpu, data, len, odata);
   64|  
   65|  	return 1;
   66|  }
   67|  
   68|  
   69|  DEVINIT(prep)
   70|  {
   71|  	struct prep_data *d;
   72|  
   73|  	CHECK_ALLOCATION(d = (struct prep_data *) malloc(sizeof(struct prep_data)));
   74|  	memset(d, 0, sizeof(struct prep_data));
   75|  
   76|  	memory_device_register(devinit->machine->memory, devinit->name,
   77|  	    0xbffff000, 0x1000, dev_prep_access, d, DM_DEFAULT, NULL);
   78|  
   79|  	/*  This works for at least the IBM 6050:  */
   80|  	bus_isa_init(devinit->machine, devinit->interrupt_path,
   81|  	    BUS_ISA_IDE0 | BUS_ISA_IDE1, 0x80000000, 0xc0000000);
   82|  
   83|  	return 1;
   84|  }
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


## Your previous draft's edits

```json
[
  {
    "file": "src/devices/dev_prep.c",
    "old": "struct prep_data {\n\tuint32_t\t\tint_status;\n};\n\n\nDEVICE_ACCESS(prep)",
    "new": "struct prep_data {\n\tuint32_t\t\tint_status;\n};\n\nstruct pic8259_data;\nextern int pic8259_acknowledge(struct pic8259_data *d, struct machine *m);\n\nDEVICE_ACCESS(prep)",
    "why": "Declare pic8259_acknowledge locally to allow calling it without an implicit declaration."
  },
  {
    "file": "src/devices/dev_prep.c",
    "old": "\tif (writeflag == MEM_READ) {\n\t\todata = cpu->machine->isa_pic_data.last_int;\n\t} else {",
    "new": "\tif (writeflag == MEM_READ) {\n\t\todata = cpu->machine->isa_pic_data.last_int;\n\t\t/* #i8259isrnever: acknowledge the interrupt to update ISR */\n\t\tif (cpu->machine->isa_pic_data.pic1)\n\t\t\tpic8259_acknowledge(cpu->machine->isa_pic_data.pic1, cpu->machine);\n\t} else {",
    "why": "Acknowledge the interrupt on PReP IACK read to set the ISR, matching the OCW3 poll read behaviour."
  }
]
```

## The review of that draft (it can be WRONG -- judge each point against the code above)

```text
FIXREVIEW_I8259ISRNEVER: DEFECT, 1 FINDINGS
1. The diff removes the defect at `src/devices/dev_prep.c`. However, it misses `src/devices/dev_footbridge.c`, which is explicitly named in the issue's state note as part of the remaining work.
2. No. The added code does not contain any `return`, `goto`, or `break` statements. Control flow proceeds naturally to the common tail: `memory_writemax64(cpu, data, len, odata);` and `return 1;` at lines 68-70.
3. No. The function continues to return `1` on all paths. The shown code implies that returning 1 signifies a successful memory access operation.
4. Calling `pic8259_acknowledge()` alters the emulator state of the 8259 PIC (specifically setting the corresponding bit in the In-Service Register, ISR), which means subsequent PIC I/O port reads by the guest will see a different ISR value. 
5. The diff adheres to the house idioms. The new comment `/* #i8259isrnever: acknowledge the interrupt to update ISR */` correctly includes the issue tag, and the added lines stay within the 79-column limit.
dev_footbridge.c:UNSETTLED DEFECT The patch omits the required fix for the `dev_footbridge.c` vector reads entirely; apply equivalent acknowledgment logic to that file.
```

## WHAT TO RETURN

1. For EACH review finding, one line: `ACCEPT` or `REJECT`, and why, citing the code shown.  A suggestion that uses a
   function, macro or field that appears nowhere in this packet does not exist in HEAD: reject it or replace it with an
   idiom the packet shows.
2. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code that shows it>`.
3. If YES: EXACTLY ONE fenced ```json block -- the COMPLETE corrected edit list (not a delta), applying to the HEAD text
   above: [{"file": "src/...", "old": "<exact HEAD text, occurring EXACTLY ONCE in that file>", "new": "<replacement>",
   "why": "<one line>"}].  JSON escapes (\t, \n); tabs stay tabs; lines within 79 columns; a new comment carries
   `/* #NNN: ... */`.  Never an empty list and never comment-only edits for a defect in behaviour.  If every finding is
   rejected, return the previous edits unchanged.
4. After the block: what the fix deliberately does not change.

End with two lines: `REVISION_I8259ISRNEVER: <a> ACCEPTED, <r> REJECTED` and `FIXDRAFT_I8259ISRNEVER: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
