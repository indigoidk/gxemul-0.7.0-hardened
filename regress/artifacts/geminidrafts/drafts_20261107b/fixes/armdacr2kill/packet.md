# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armdacr2kill` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 2d25df65).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armdacr2kill`, state `open`, severity `MED-LOW`)

**title:** src/cpus/memory_arm.c:78-79: arm_check_access() case 2: fatal(..."1 shouldn't be used"); exit(1).  cpu_arm_coproc.c:203 stores MCR's operand into dacr unfiltered; memory_arm.c:153 derives dav from it -- a guest writing 0b10 into any domain field and touching that domain ends the process.  Architecturally reserved; the fix is one case 2: treated as no-access.  Witness: rung 3, MMU ON, DACR written by a guest mcr.  kimi CLI (:254) and the main loop's follow-up read (:79), fbdeclinefive pass 1; fab [... 7 more characters not shown]

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- change case 2 in arm_check_access() to treat as no-access instead of exiting fatally

## The code at the cited lines

### `src/cpus/memory_arm.c` around the row's cited line 78 (HEAD 2d25df65, lines 33-123)

```c
   33| #include <stdio.h>
   34| #include <stdlib.h>
   35| #include <string.h>
   36| 
   37| #include "arm_cpu_types.h"
   38| #include "cpu.h"
   39| #include "memory.h"
   40| #include "misc.h"
   41| 
   42| #include "thirdparty/armreg.h"
   43| 
   44| 
   45| extern int quiet_mode;
   46| 
   47| 
   48| /*
   49|  *  arm_translate_v2p():
   50|  *
   51|  *  Address translation with the MMU disabled. (Just treat the virtual address
   52|  *  as a physical address.)
   53|  */
   54| int arm_translate_v2p(struct cpu *cpu, uint64_t vaddr64,
   55| 	uint64_t *return_paddr, int flags)
   56| {
   57| 	*return_paddr = vaddr64 & 0xffffffff;
   58| 
   59| 	return 2;
   60| }
   61| 
   62| 
   63| /*
   64|  *  arm_check_access():
   65|  *
   66|  *  Helper function.  Returns 0 for no access, 1 for read-only, and 2 for
   67|  *  read/write.
   68|  */
   69| static int arm_check_access(struct cpu *cpu, int ap, int dav, int user)
   70| {
   71| 	int s, r;
   72| 
   73| 	switch (dav) {
   74| 	case 0:	/*  No access at all.  */
   75| 		return 0;
   76| 	case 1:	/*  Normal access check.  */
   77| 		break;
   78| 	case 2:	fatal("arm_check_access(): 1 shouldn't be used\n");
   79| 		exit(1);
   80| 	case 3:	/*  Anything is allowed.  */
   81| 		return 2;
   82| 	}
   83| 
   84| 	switch (ap) {
   85| 	case 0:	s = (cpu->cd.arm.control & ARM_CONTROL_S)? 1 : 0;
   86| 		r = (cpu->cd.arm.control & ARM_CONTROL_R)? 2 : 0;
   87| 		switch (s + r) {
   88| 		case 0:	return 0;
   89| 		case 1:	return user? 0 : 1;
   90| 		case 2:	return 1;
   91| 		}
   92| 		fatal("arm_check_access: UNPREDICTABLE s+r value!\n");
   93| 		return 0;
   94| 	case 1:	return user? 0 : 2;
   95| 	case 2:	return user? 1 : 2;
   96| 	}
   97| 
   98| 	/*  "case 3":  */
   99| 	return 2;
  100| }
  101| 
  102| 
  103| /*
  104|  *  arm_translate_v2p_mmu():
  105|  *
  106|  *  Return values:
  107|  *	0  Failure
  108|  *	1  Success, the page is readable only
  109|  *	2  Success, the page is read/write
  110|  *
  111|  *  If this is a 1KB page access, then the return value is ORed with
  112|  *  MEMORY_NOT_FULL_PAGE.
  113|  */
  114| int arm_translate_v2p_mmu(struct cpu *cpu, uint64_t vaddr64,
  115| 	uint64_t *return_paddr, int flags)
  116| {
  117| 	unsigned char *q;
  118| 	uint32_t addr, d=0, d2 = (uint32_t)(int32_t)-1, ptba, vaddr = vaddr64;
  119| 	int instr = flags & FLAG_INSTR;
  120| 	int writeflag = (flags & FLAG_WRITEFLAG)? 1 : 0;
  121| 	int useraccess = flags & MEMORY_USER_ACCESS;
  122| 	int no_exceptions = flags & FLAG_NOEXCEPTIONS;
  123| 	int user = (cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_USR32;
```

## WHAT TO RETURN

1. One line: `STILL PRESENT: YES|NO|UNSETTLED -- <the line of code shown that shows it>`.  The cited line numbers may have
   moved since the row was written; judge from the code shown.  If NO, say what already fixed it and STOP (no edits).
2. If YES: EXACTLY ONE fenced ```json block -- a list of edits, the smallest fix that removes the defect without changing any
   other behaviour: [{"file": "src/...", "old": "<exact text from the code above, without the line-number prefix; it must occur
   EXACTLY ONCE in that file>", "new": "<replacement>", "why": "<one line>"}].  Use JSON escapes (\t, \n).  Tabs stay tabs;
   lines within 79 columns; tag a new comment `/* #NNN: ... */`.  Prefer the file's existing idioms (a decline, a once-per-
   device announce, a clamp) over new machinery.
3. After the block: what the fix deliberately does NOT change, and anything you could not settle from the code shown.

End with one line: `FIXDRAFT_ARMDACR2KILL: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
