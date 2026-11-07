# GXemul hardened fork -- DRAFT A FIX for one filed issue, `pccmosnmi` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD d2a6f233).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `pccmosnmi`, state `open`, severity `MED`)

**title:** devices/dev_pccmos.c:DEVICE_ACCESS index port -- the index is stored without masking bit 7 (NMI disable), so such a guest misses RTC registers 0x00-0x0d -- WRONG-RESULT

**state_note (head):**

Filed 2026-10-22 from the external-fixes research: regress/artifacts/research_20261022/TRIAGE.md row T99 (class WRONG-RESULT; reach K, guest kernel, firmware or device registers; effort: one-line; report rows: A5-28).  Source URLs: https://github.com/prozacchiwawa/gxemul-rs6000-860/commit/bb3294595335d7c2480b7662f2d021d67a6a5436.  Our site at de8c7547: src/devices/dev_pccmos.c:74.  Portable fix: yes -- port the masking of rs6000 bb32945.  Filing check (TRIAGE.md): 0 hits.  witness: none -- research finding, not yet reproduced here.

**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- port the masking of rs6000 bb32945

## The code at the cited lines

### `src/devices/dev_pccmos.c` around the row's cited line 74 (HEAD d2a6f233, lines 29-119)

```c
   29|  *
   30|  *  The main point of this device is to be a "PC style wrapper" for accessing
   31|  *  the MC146818 (the RTC). In most other respects, this device is bogus, and
   32|  *  just acts as a 256-byte RAM device.
   33|  */
   34| 
   35| #include <stdio.h>
   36| #include <stdlib.h>
   37| #include <string.h>
   38| 
   39| #include "cpu.h"
   40| #include "device.h"
   41| #include "devices.h"
   42| #include "emul.h"
   43| #include "machine.h"
   44| #include "memory.h"
   45| #include "misc.h"
   46| 
   47| 
   48| #define	DEV_PCCMOS_LENGTH		2
   49| #define	PCCMOS_MC146818_FAKE_ADDR	0x1d00000000ULL
   50| 
   51| struct pccmos_data {
   52| 	unsigned char	select;
   53| 	unsigned char	ram[256];
   54| };
   55| 
   56| 
   57| DEVICE_ACCESS(pccmos)
   58| {
   59| 	struct pccmos_data *d = (struct pccmos_data *) extra;
   60| 	uint64_t idata = 0, odata = 0;
   61| 	unsigned char b = 0;
   62| 	int r = 1;
   63| 
   64| 	if (writeflag == MEM_WRITE)
   65| 		b = idata = memory_readmax64(cpu, data, len);
   66| 
   67| 	/*
   68| 	 *  Accesses to CMOS register 0 .. 0xd are rerouted to the
   69| 	 *  RTC; all other access are treated as CMOS RAM read/writes.
   70| 	 */
   71| 
   72| 	if ((relative_addr & 1) == 0) {
   73| 		if (writeflag == MEM_WRITE) {
   74| 			d->select = idata;
   75| 			if (idata <= 0x0d) {
   76| 				r = cpu->memory_rw(cpu, cpu->mem,
   77| 				    PCCMOS_MC146818_FAKE_ADDR, &b, 1,
   78| 				    MEM_WRITE, PHYSICAL);
   79| 			}
   80| 		} else
   81| 			odata = d->select;
   82| 	} else {
   83| 		if (d->select <= 0x0d) {
   84| 			if (writeflag == MEM_WRITE) {
   85| 				r = cpu->memory_rw(cpu, cpu->mem,
   86| 				    PCCMOS_MC146818_FAKE_ADDR + 1, &b, 1,
   87| 				    MEM_WRITE, PHYSICAL);
   88| 			} else {
   89| 				r = cpu->memory_rw(cpu, cpu->mem,
   90| 				    PCCMOS_MC146818_FAKE_ADDR + 1, &b, 1,
   91| 				    MEM_READ, PHYSICAL);
   92| 				odata = b;
   93| 			}
   94| 		} else {
   95| 			if (writeflag == MEM_WRITE)
   96| 				d->ram[d->select] = idata;
   97| 			else
   98| 				odata = d->ram[d->select];
   99| 		}
  100| 	}
  101| 
  102| 	if (r == 0)
  103| 		fatal("[ pccmos: memory_rw() error! ]\n");
  104| 
  105| 	if (writeflag == MEM_READ)
  106| 		memory_writemax64(cpu, data, len, odata);
  107| 
  108| 	return 1;
  109| }
  110| 
  111| 
  112| DEVINIT(pccmos)
  113| {
  114| 	int type = MC146818_PC_CMOS, len = DEV_PCCMOS_LENGTH;
  115| 	struct pccmos_data *d;
  116| 
  117| 	CHECK_ALLOCATION(d = (struct pccmos_data *) malloc(sizeof(struct pccmos_data)));
  118| 	memset(d, 0, sizeof(struct pccmos_data));
  119| 
```

## The data structures those files define (every field that exists)

### `src/devices/dev_pccmos.c` -- `struct pccmos_data {` (HEAD lines 51-54)

```c
   51| struct pccmos_data {
   52| 	unsigned char	select;
   53| 	unsigned char	ram[256];
   54| };
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

End with one line: `FIXDRAFT_PCCMOSNMI: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
