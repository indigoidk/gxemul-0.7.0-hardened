# GXemul hardened fork -- REVIEW ONE PROPOSED FIX for a filed issue, `armldrexbhdspin` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below: one filed issue (from the
project's ledger), a PROPOSED fix drafted earlier (it compiles at HEAD 8d9df658 with no new warnings), and EVERY FUNCTION THE FIX
EDITS, shown as it reads AFTER the fix.  You cannot read files; work from this text.  This is a REVIEW: report findings, do
not rewrite the fix, and do not write tests, probes or reproduction steps.  Do not simply approve it.

## The issue (ledger row `armldrexbhdspin`, state `open`)

**title:** src/cpus/cpu_arm_instr.c:208-221 -- LDREXB/H/D and STREXB/H/D decode to X(invalid) (the extra load/store table's s = 0, h = 0 entry), which prints and ends the run without stopping the CPU or moving the PC, so the same instruction runs again and again -- CPU-HANG (the emulated CPU livelocks; the host keeps running)

**state_note (head):** 

**The drafter's own reading:** STILL PRESENT: YES -- src/cpus/cpu_arm_instr.c:221

## The proposed fix (unified diff against HEAD)

```diff
diff --git a/src/cpus/cpu_arm_instr.c b/src/cpus/cpu_arm_instr.c
index 5443a695..a25036bc 100644
--- a/src/cpus/cpu_arm_instr.c
+++ b/src/cpus/cpu_arm_instr.c
@@ -218,6 +218,8 @@ X(invalid) {
 	    " encoding. pc = 0x%08" PRIx32"\n",
 	    (uint32_t)cpu->pc);
 
+	/* #001: Move the PC to avoid livelocking on the same instruction */
+	cpu->pc += (1 << ARM_INSTR_ALIGNMENT_SHIFT);
 	cpu->cd.arm.next_ic = &nothing_call;
 }
 
@@ -236,6 +238,8 @@ X(never) {
 
 	fatal("[ ARM: unimplemented 0xf instruction at pc = 0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
 
+	/* #002: Move the PC to avoid livelocking on the same instruction */
+	cpu->pc += (1 << ARM_INSTR_ALIGNMENT_SHIFT);
 	cpu->cd.arm.next_ic = &nothing_call;
 }
```

## Every edited function, after the fix

### `src/cpus/cpu_arm_instr.c` -- post-edit lines 60-244 (`+` marks a line the diff added or the point of a deletion)

```c
   60|  static void update_bdt_statistics(uint32_t iw)
   61|  {
   62|  	static FILE *f = NULL;
   63|  	static long long *counts;
   64|  	static char *counts_used;
   65|  	static long long n = 0;
   66|  
   67|  	if (f == NULL) {
   68|  		size_t s = (1 << 24) * sizeof(long long);
   69|  		f = fopen("bdt_statistics.txt", "w");
   70|  		if (f == NULL) {
   71|  			fprintf(stderr, "update_bdt_statistics(): :-(\n");
   72|  			exit(1);
   73|  		}
   74|  		counts = zeroed_alloc(s);
   75|  		counts_used = zeroed_alloc(65536);
   76|  	}
   77|  
   78|  	/*  Drop the s-bit: xxxx100P USWLnnnn llllllll llllllll  */
   79|  	iw = ((iw & 0x01800000) >> 1) | (iw & 0x003fffff);
   80|  
   81|  	counts_used[iw & 0xffff] = 1;
   82|  	counts[iw] ++;
   83|  
   84|  	n ++;
   85|  	if ((n % 500000) == 0) {
   86|  		int i;
   87|  		long long j;
   88|  		fatal("[ update_bdt_statistics(): n = %lli ]\n", (long long) n);
   89|  		fseek(f, 0, SEEK_SET);
   90|  		for (i=0; i<0x1000000; i++)
   91|  			if (counts_used[i & 0xffff] && counts[i] != 0) {
   92|  				/*  Recreate the opcode:  */
   93|  				uint32_t opcode = ((i & 0x00c00000) << 1)
   94|  				    | (i & 0x003fffff) | 0x08000000;
   95|  				for (j=0; j<counts[i]; j++)
   96|  					fprintf(f, "0x%08x\n", opcode);
   97|  			}
   98|  		fflush(f);
   99|  	}
  100|  }
  101|  #endif
  102|  
  103|  
  104|  /*****************************************************************************/
  105|  
  106|  
  107|  /*
  108|   *  Helper definitions:
  109|   *
  110|   *  Each instruction is defined like this:
  111|   *
  112|   *	X(foo)
  113|   *	{
  114|   *		code for foo;
  115|   *	}
  116|   *	Y(foo)
  117|   *
  118|   *  The Y macro defines 14 copies of the instruction, one for each possible
  119|   *  condition code. (The NV condition code is not included, and the AL code
  120|   *  uses the main foo function.)  Y also defines an array with pointers to
  121|   *  all of these functions.
  122|   *
  123|   *  If the compiler is good enough (i.e. allows long enough code sequences
  124|   *  to be inlined), then the Y functions will be compiled as full (inlined)
  125|   *  functions, otherwise they will simply call the X function.
  126|   */
  127|  
  128|  uint8_t condition_hi[16] = { 0,0,1,1, 0,0,0,0, 0,0,1,1, 0,0,0,0 };
  129|  uint8_t condition_ge[16] = { 1,0,1,0, 1,0,1,0, 0,1,0,1, 0,1,0,1 };
  130|  uint8_t condition_gt[16] = { 1,0,1,0, 0,0,0,0, 0,1,0,1, 0,0,0,0 };
  131|  
  132|  #define Y(n) void arm_instr_ ## n ## __eq(struct cpu *cpu,		\
  133|  			struct arm_instr_call *ic)			\
  134|  	{  if (cpu->cd.arm.flags & ARM_F_Z)				\
  135|  		arm_instr_ ## n (cpu, ic);		}		\
  136|  	void arm_instr_ ## n ## __ne(struct cpu *cpu,			\
  137|  			struct arm_instr_call *ic)			\
  138|  	{  if (!(cpu->cd.arm.flags & ARM_F_Z))				\
  139|  		arm_instr_ ## n (cpu, ic);		}		\
  140|  	void arm_instr_ ## n ## __cs(struct cpu *cpu,			\
  141|  			struct arm_instr_call *ic)			\
  142|  	{  if (cpu->cd.arm.flags & ARM_F_C)				\
  143|  		arm_instr_ ## n (cpu, ic);		}		\
  144|  	void arm_instr_ ## n ## __cc(struct cpu *cpu,			\
  145|  			struct arm_instr_call *ic)			\
  146|  	{  if (!(cpu->cd.arm.flags & ARM_F_C))				\
  147|  		arm_instr_ ## n (cpu, ic);		}		\
  148|  	void arm_instr_ ## n ## __mi(struct cpu *cpu,			\
  149|  			struct arm_instr_call *ic)			\
  150|  	{  if (cpu->cd.arm.flags & ARM_F_N)				\
  151|  		arm_instr_ ## n (cpu, ic);		}		\
  152|  	void arm_instr_ ## n ## __pl(struct cpu *cpu,			\
  153|  			struct arm_instr_call *ic)			\
  154|  	{  if (!(cpu->cd.arm.flags & ARM_F_N))				\
  155|  		arm_instr_ ## n (cpu, ic);		}		\
  156|  	void arm_instr_ ## n ## __vs(struct cpu *cpu,			\
  157|  			struct arm_instr_call *ic)			\
  158|  	{  if (cpu->cd.arm.flags & ARM_F_V)				\
  159|  		arm_instr_ ## n (cpu, ic);		}		\
  160|  	void arm_instr_ ## n ## __vc(struct cpu *cpu,			\
  161|  			struct arm_instr_call *ic)			\
  162|  	{  if (!(cpu->cd.arm.flags & ARM_F_V))				\
  163|  		arm_instr_ ## n (cpu, ic);		}		\
  164|  	void arm_instr_ ## n ## __hi(struct cpu *cpu,			\
  165|  			struct arm_instr_call *ic)			\
  166|  	{  if (condition_hi[cpu->cd.arm.flags])				\
  167|  		arm_instr_ ## n (cpu, ic);		}		\
  168|  	void arm_instr_ ## n ## __ls(struct cpu *cpu,			\
  169|  			struct arm_instr_call *ic)			\
  170|  	{  if (!condition_hi[cpu->cd.arm.flags])			\
  171|  		arm_instr_ ## n (cpu, ic);		}		\
  172|  	void arm_instr_ ## n ## __ge(struct cpu *cpu,			\
  173|  			struct arm_instr_call *ic)			\
  174|  	{  if (condition_ge[cpu->cd.arm.flags])				\
  175|  		arm_instr_ ## n (cpu, ic);		}		\
  176|  	void arm_instr_ ## n ## __lt(struct cpu *cpu,			\
  177|  			struct arm_instr_call *ic)			\
  178|  	{  if (!condition_ge[cpu->cd.arm.flags])			\
  179|  		arm_instr_ ## n (cpu, ic);		}		\
  180|  	void arm_instr_ ## n ## __gt(struct cpu *cpu,			\
  181|  			struct arm_instr_call *ic)			\
  182|  	{  if (condition_gt[cpu->cd.arm.flags])				\
  183|  		arm_instr_ ## n (cpu, ic);		}		\
  184|  	void arm_instr_ ## n ## __le(struct cpu *cpu,			\
  185|  			struct arm_instr_call *ic)			\
  186|  	{  if (!condition_gt[cpu->cd.arm.flags])			\
  187|  		arm_instr_ ## n (cpu, ic);		}		\
  188|  	void (*arm_cond_instr_ ## n  [16])(struct cpu *,		\
  189|  			struct arm_instr_call *) = {			\
  190|  		arm_instr_ ## n ## __eq, arm_instr_ ## n ## __ne,	\
  191|  		arm_instr_ ## n ## __cs, arm_instr_ ## n ## __cc,	\
  192|  		arm_instr_ ## n ## __mi, arm_instr_ ## n ## __pl,	\
  193|  		arm_instr_ ## n ## __vs, arm_instr_ ## n ## __vc,	\
  194|  		arm_instr_ ## n ## __hi, arm_instr_ ## n ## __ls,	\
  195|  		arm_instr_ ## n ## __ge, arm_instr_ ## n ## __lt,	\
  196|  		arm_instr_ ## n ## __gt, arm_instr_ ## n ## __le,	\
  197|  		arm_instr_ ## n , arm_instr_never };
  198|  
  199|  #define cond_instr(n)	( arm_cond_instr_ ## n  [condition_code] )
  200|  
  201|  
  202|  /*****************************************************************************/
  203|  
  204|  
  205|  /*
  206|   *  invalid:  Invalid instructions end up here.
  207|   */
  208|  X(invalid) {
  209|  	uint32_t low_pc;
  210|  	low_pc = ((size_t)ic - (size_t)
  211|  	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
  212|  	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
  213|  	    << ARM_INSTR_ALIGNMENT_SHIFT);
  214|  	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
  215|  
  216|  	fatal("FATAL ERROR: An internal error occured in the ARM"
  217|  	    " dyntrans code. This could be due to an unimplemented instruction"
  218|  	    " encoding. pc = 0x%08" PRIx32"\n",
  219|  	    (uint32_t)cpu->pc);
  220|  
  221|+ 	/* #001: Move the PC to avoid livelocking on the same instruction */
  222|+ 	cpu->pc += (1 << ARM_INSTR_ALIGNMENT_SHIFT);
  223|  	cpu->cd.arm.next_ic = &nothing_call;
  224|  }
  225|  
  226|  
  227|  /*
  228|   *  never:  So far unimplemented "never" instructions end up here.
  229|   *  (Those are the ones using the "0xf" condition prefix.)
  230|   */
  231|  X(never) {
  232|  	uint32_t low_pc;
  233|  	low_pc = ((size_t)ic - (size_t)
  234|  	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
  235|  	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
  236|  	    << ARM_INSTR_ALIGNMENT_SHIFT);
  237|  	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
  238|  
  239|  	fatal("[ ARM: unimplemented 0xf instruction at pc = 0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
  240|  
  241|+ 	/* #002: Move the PC to avoid livelocking on the same instruction */
  242|+ 	cpu->pc += (1 << ARM_INSTR_ALIGNMENT_SHIFT);
  243|  	cpu->cd.arm.next_ic = &nothing_call;
  244|  }
```

## Questions -- answer each; verdict line FIRST

Line 1: `FIXREVIEW_ARMLDREXBHDSPIN: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.

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

End with one line: `FIXREVIEW_ARMLDREXBHDSPIN: <SOUND|DEFECT|UNSETTLED>, <n> FINDINGS`.
