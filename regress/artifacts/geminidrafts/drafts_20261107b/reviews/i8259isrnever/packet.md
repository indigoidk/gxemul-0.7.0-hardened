# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `i8259isrnever` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `i8259isrnever`, state `open`)

**title:** devices/dev_8259.c + devices/dev_prep.c IACK -- ISR is never set (read-ISR returns 0) and the PReP IACK read has no acknowledge side effect -- WRONG-RESULT

**state_note (head):** NARROWED by #574 on 2026-10-25: the OCW3 poll read and the GT64120 IACK read now set ISR (pic8259_acknowledge()); what remains is the PReP (dev_prep.c) and footbridge (dev_footbridge.c) vector reads, which return isa_pic_data.last_int with no acknowledge -- their guests' specific EOIs keep #574's legacy consume, so nothing regressed; converting them is this row's remaining work (no witness machine here).  ||  Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T51 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: medium; report rows: A5-27, A(c)#11).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/598ab108cacb56dfbeae33eb463fd2b8c18393dd, https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/174448c390ede42e884e26bd0b627ab43169dd11.  Our site at de8c7547: src/devices/dev_8259.c:108; src/devices/dev_prep.c:52-62.  Portable fix: yes -- port rs6000 598ab10, rs6000 174448c.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**The drafter's own reading:** STILL PRESENT: YES -- `odata = cpu->machine->isa_pic_data.last_int;`

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/devices/dev_prep.c b/src/devices/dev_prep.c
index dccb58f4..553692a1 100644
--- a/src/devices/dev_prep.c
+++ b/src/devices/dev_prep.c
@@ -44,6 +44,8 @@ struct prep_data {
 	uint32_t		int_status;
 };
 
+struct pic8259_data;
+extern int pic8259_acknowledge(struct pic8259_data *d, struct machine *m);
 
 DEVICE_ACCESS(prep)
 {
@@ -55,6 +57,9 @@ DEVICE_ACCESS(prep)
 
 	if (writeflag == MEM_READ) {
 		odata = cpu->machine->isa_pic_data.last_int;
+		/* #i8259isrnever: acknowledge the interrupt to update ISR */
+		if (cpu->machine->isa_pic_data.pic1)
+			pic8259_acknowledge(cpu->machine->isa_pic_data.pic1, cpu->machine);
 	} else {
 		fatal("[ prep: write to interrupt register? idata = 0x%016" PRIx64" ]\n", idata);
 	}
```

## Every edited function, after the fix

### `src/devices/dev_prep.c` -- post-edit lines 1-91 (`+` marks a line the diff added or the point of a deletion)

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
   47|+ struct pic8259_data;
   48|+ extern int pic8259_acknowledge(struct pic8259_data *d, struct machine *m);
   49|  
   50|  DEVICE_ACCESS(prep)
   51|  {
   52|  	/*  struct prep_data *d = extra;  */
   53|  	uint64_t idata = 0, odata = 0;
   54|  
   55|  	if (writeflag == MEM_WRITE)
   56|  		idata = memory_readmax64(cpu, data, len);
   57|  
   58|  	if (writeflag == MEM_READ) {
   59|  		odata = cpu->machine->isa_pic_data.last_int;
   60|+ 		/* #i8259isrnever: acknowledge the interrupt to update ISR */
   61|+ 		if (cpu->machine->isa_pic_data.pic1)
   62|+ 			pic8259_acknowledge(cpu->machine->isa_pic_data.pic1, cpu->machine);
   63|  	} else {
   64|  		fatal("[ prep: write to interrupt register? idata = 0x%016" PRIx64" ]\n", idata);
   65|  	}
   66|  
   67|  	if (writeflag == MEM_READ)
   68|  		memory_writemax64(cpu, data, len, odata);
   69|  
   70|  	return 1;
   71|  }
   72|  
   73|  
   74|  DEVINIT(prep)
   75|  {
   76|  	struct prep_data *d;
   77|  
   78|  	CHECK_ALLOCATION(d = (struct prep_data *) malloc(sizeof(struct prep_data)));
   79|  	memset(d, 0, sizeof(struct prep_data));
   80|  
   81|  	memory_device_register(devinit->machine->memory, devinit->name,
   82|  	    0xbffff000, 0x1000, dev_prep_access, d, DM_DEFAULT, NULL);
   83|  
   84|  	/*  This works for at least the IBM 6050:  */
   85|  	bus_isa_init(devinit->machine, devinit->interrupt_path,
   86|  	    BUS_ISA_IDE0 | BUS_ISA_IDE1, 0x80000000, 0xc0000000);
   87|  
   88|  	return 1;
   89|  }
   90|  
   91|  
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_I8259ISRNEVER: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_I8259ISRNEVER: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
