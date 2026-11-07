# GXemul hardened fork -- DRAFT A FIX for one filed issue, `armldrexbhdspin` (a defensive code-quality task)

PROJECT FRAMING -- a defensive software-robustness project: GXemul is a computer-architecture emulator, and this fork removes
crash-on-malformed-input and wrong-behaviour defects from its device and CPU models.  Below is one filed issue, inlined from
the project's ledger, and the current code at each source line it cites (HEAD 8d9df658).  You cannot read files; work from the text.
This is a DRAFTING task: write the FIX ONLY, as exact edits.  Do not write tests, probes or reproduction steps.

## The issue (ledger row `armldrexbhdspin`, state `open`, severity `MED`)

**title:** src/cpus/cpu_arm_instr.c:208-221 -- LDREXB/H/D and STREXB/H/D decode to X(invalid) (the extra load/store table's s = 0, h = 0 entry), which prints and ends the run without stopping the CPU or moving the PC, so the same instruction runs again and again -- CPU-HANG (the emulated CPU livelocks; the host keeps running)

**state_note (head):**



**hold_question:** (none)

**An earlier triage pass proposed:** FIX-NOW -- guest instruction triggers emulated CPU livelock (guest hang)

## The code at the cited lines

### `src/cpus/cpu_arm_instr.c` around the row's cited line 208 (HEAD 8d9df658, lines 88-328)

```c
   88| 		fatal("[ update_bdt_statistics(): n = %lli ]\n", (long long) n);
   89| 		fseek(f, 0, SEEK_SET);
   90| 		for (i=0; i<0x1000000; i++)
   91| 			if (counts_used[i & 0xffff] && counts[i] != 0) {
   92| 				/*  Recreate the opcode:  */
   93| 				uint32_t opcode = ((i & 0x00c00000) << 1)
   94| 				    | (i & 0x003fffff) | 0x08000000;
   95| 				for (j=0; j<counts[i]; j++)
   96| 					fprintf(f, "0x%08x\n", opcode);
   97| 			}
   98| 		fflush(f);
   99| 	}
  100| }
  101| #endif
  102| 
  103| 
  104| /*****************************************************************************/
  105| 
  106| 
  107| /*
  108|  *  Helper definitions:
  109|  *
  110|  *  Each instruction is defined like this:
  111|  *
  112|  *	X(foo)
  113|  *	{
  114|  *		code for foo;
  115|  *	}
  116|  *	Y(foo)
  117|  *
  118|  *  The Y macro defines 14 copies of the instruction, one for each possible
  119|  *  condition code. (The NV condition code is not included, and the AL code
  120|  *  uses the main foo function.)  Y also defines an array with pointers to
  121|  *  all of these functions.
  122|  *
  123|  *  If the compiler is good enough (i.e. allows long enough code sequences
  124|  *  to be inlined), then the Y functions will be compiled as full (inlined)
  125|  *  functions, otherwise they will simply call the X function.
  126|  */
  127| 
  128| uint8_t condition_hi[16] = { 0,0,1,1, 0,0,0,0, 0,0,1,1, 0,0,0,0 };
  129| uint8_t condition_ge[16] = { 1,0,1,0, 1,0,1,0, 0,1,0,1, 0,1,0,1 };
  130| uint8_t condition_gt[16] = { 1,0,1,0, 0,0,0,0, 0,1,0,1, 0,0,0,0 };
  131| 
  132| #define Y(n) void arm_instr_ ## n ## __eq(struct cpu *cpu,		\
  133| 			struct arm_instr_call *ic)			\
  134| 	{  if (cpu->cd.arm.flags & ARM_F_Z)				\
  135| 		arm_instr_ ## n (cpu, ic);		}		\
  136| 	void arm_instr_ ## n ## __ne(struct cpu *cpu,			\
  137| 			struct arm_instr_call *ic)			\
  138| 	{  if (!(cpu->cd.arm.flags & ARM_F_Z))				\
  139| 		arm_instr_ ## n (cpu, ic);		}		\
  140| 	void arm_instr_ ## n ## __cs(struct cpu *cpu,			\
  141| 			struct arm_instr_call *ic)			\
  142| 	{  if (cpu->cd.arm.flags & ARM_F_C)				\
  143| 		arm_instr_ ## n (cpu, ic);		}		\
  144| 	void arm_instr_ ## n ## __cc(struct cpu *cpu,			\
  145| 			struct arm_instr_call *ic)			\
  146| 	{  if (!(cpu->cd.arm.flags & ARM_F_C))				\
  147| 		arm_instr_ ## n (cpu, ic);		}		\
  148| 	void arm_instr_ ## n ## __mi(struct cpu *cpu,			\
  149| 			struct arm_instr_call *ic)			\
  150| 	{  if (cpu->cd.arm.flags & ARM_F_N)				\
  151| 		arm_instr_ ## n (cpu, ic);		}		\
  152| 	void arm_instr_ ## n ## __pl(struct cpu *cpu,			\
  153| 			struct arm_instr_call *ic)			\
  154| 	{  if (!(cpu->cd.arm.flags & ARM_F_N))				\
  155| 		arm_instr_ ## n (cpu, ic);		}		\
  156| 	void arm_instr_ ## n ## __vs(struct cpu *cpu,			\
  157| 			struct arm_instr_call *ic)			\
  158| 	{  if (cpu->cd.arm.flags & ARM_F_V)				\
  159| 		arm_instr_ ## n (cpu, ic);		}		\
  160| 	void arm_instr_ ## n ## __vc(struct cpu *cpu,			\
  161| 			struct arm_instr_call *ic)			\
  162| 	{  if (!(cpu->cd.arm.flags & ARM_F_V))				\
  163| 		arm_instr_ ## n (cpu, ic);		}		\
  164| 	void arm_instr_ ## n ## __hi(struct cpu *cpu,			\
  165| 			struct arm_instr_call *ic)			\
  166| 	{  if (condition_hi[cpu->cd.arm.flags])				\
  167| 		arm_instr_ ## n (cpu, ic);		}		\
  168| 	void arm_instr_ ## n ## __ls(struct cpu *cpu,			\
  169| 			struct arm_instr_call *ic)			\
  170| 	{  if (!condition_hi[cpu->cd.arm.flags])			\
  171| 		arm_instr_ ## n (cpu, ic);		}		\
  172| 	void arm_instr_ ## n ## __ge(struct cpu *cpu,			\
  173| 			struct arm_instr_call *ic)			\
  174| 	{  if (condition_ge[cpu->cd.arm.flags])				\
  175| 		arm_instr_ ## n (cpu, ic);		}		\
  176| 	void arm_instr_ ## n ## __lt(struct cpu *cpu,			\
  177| 			struct arm_instr_call *ic)			\
  178| 	{  if (!condition_ge[cpu->cd.arm.flags])			\
  179| 		arm_instr_ ## n (cpu, ic);		}		\
  180| 	void arm_instr_ ## n ## __gt(struct cpu *cpu,			\
  181| 			struct arm_instr_call *ic)			\
  182| 	{  if (condition_gt[cpu->cd.arm.flags])				\
  183| 		arm_instr_ ## n (cpu, ic);		}		\
  184| 	void arm_instr_ ## n ## __le(struct cpu *cpu,			\
  185| 			struct arm_instr_call *ic)			\
  186| 	{  if (!condition_gt[cpu->cd.arm.flags])			\
  187| 		arm_instr_ ## n (cpu, ic);		}		\
  188| 	void (*arm_cond_instr_ ## n  [16])(struct cpu *,		\
  189| 			struct arm_instr_call *) = {			\
  190| 		arm_instr_ ## n ## __eq, arm_instr_ ## n ## __ne,	\
  191| 		arm_instr_ ## n ## __cs, arm_instr_ ## n ## __cc,	\
  192| 		arm_instr_ ## n ## __mi, arm_instr_ ## n ## __pl,	\
  193| 		arm_instr_ ## n ## __vs, arm_instr_ ## n ## __vc,	\
  194| 		arm_instr_ ## n ## __hi, arm_instr_ ## n ## __ls,	\
  195| 		arm_instr_ ## n ## __ge, arm_instr_ ## n ## __lt,	\
  196| 		arm_instr_ ## n ## __gt, arm_instr_ ## n ## __le,	\
  197| 		arm_instr_ ## n , arm_instr_never };
  198| 
  199| #define cond_instr(n)	( arm_cond_instr_ ## n  [condition_code] )
  200| 
  201| 
  202| /*****************************************************************************/
  203| 
  204| 
  205| /*
  206|  *  invalid:  Invalid instructions end up here.
  207|  */
  208| X(invalid) {
  209| 	uint32_t low_pc;
  210| 	low_pc = ((size_t)ic - (size_t)
  211| 	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
  212| 	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
  213| 	    << ARM_INSTR_ALIGNMENT_SHIFT);
  214| 	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
  215| 
  216| 	fatal("FATAL ERROR: An internal error occured in the ARM"
  217| 	    " dyntrans code. This could be due to an unimplemented instruction"
  218| 	    " encoding. pc = 0x%08" PRIx32"\n",
  219| 	    (uint32_t)cpu->pc);
  220| 
  221| 	cpu->cd.arm.next_ic = &nothing_call;
  222| }
  223| 
  224| 
  225| /*
  226|  *  never:  So far unimplemented "never" instructions end up here.
  227|  *  (Those are the ones using the "0xf" condition prefix.)
  228|  */
  229| X(never) {
  230| 	uint32_t low_pc;
  231| 	low_pc = ((size_t)ic - (size_t)
  232| 	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
  233| 	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
  234| 	    << ARM_INSTR_ALIGNMENT_SHIFT);
  235| 	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
  236| 
  237| 	fatal("[ ARM: unimplemented 0xf instruction at pc = 0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);
  238| 
  239| 	cpu->cd.arm.next_ic = &nothing_call;
  240| }
  241| 
  242| 
  243| /*
  244|  *  nop:  Do nothing.
  245|  */
  246| X(nop)
  247| {
  248| }
  249| 
  250| 
  251| /*
  252|  *  b:  Branch (to a different translated page)
  253|  *
  254|  *  arg[0] = relative offset from start of page
  255|  */
  256| X(b)
  257| {
  258| 	cpu->pc = (uint32_t)((cpu->pc & 0xfffff000) + (int32_t)ic->arg[0]);
  259| 
  260| 	/*  Find the new physical page and update the translation pointers:  */
  261| 	quick_pc_to_pointers_arm(cpu);
  262| }
  263| Y(b)
  264| 
  265| 
  266| /*
  267|  *  b_samepage:  Branch (to within the same translated page)
  268|  *
  269|  *  arg[0] = pointer to new arm_instr_call
  270|  *  arg[1] = pointer to the next instruction.
  271|  *
  272|  *  NOTE: This instruction is manually inlined.
  273|  */
  274| X(b_samepage) {
  275| 	cpu->cd.arm.next_ic = (struct arm_instr_call *) ic->arg[0];
  276| }
  277| X(b_samepage__eq) {
  278| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  279| 	    ic->arg[cpu->cd.arm.flags & ARM_F_Z? 0 : 1];
  280| }
  281| X(b_samepage__ne) {
  282| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  283| 	    ic->arg[cpu->cd.arm.flags & ARM_F_Z? 1 : 0];
  284| }
  285| X(b_samepage__cs) {
  286| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  287| 	    ic->arg[cpu->cd.arm.flags & ARM_F_C? 0 : 1];
  288| }
  289| X(b_samepage__cc) {
  290| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  291| 	    ic->arg[cpu->cd.arm.flags & ARM_F_C? 1 : 0];
  292| }
  293| X(b_samepage__mi) {
  294| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  295| 	    ic->arg[cpu->cd.arm.flags & ARM_F_N? 0 : 1];
  296| }
  297| X(b_samepage__pl) {
  298| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  299| 	    ic->arg[cpu->cd.arm.flags & ARM_F_N? 1 : 0];
  300| }
  301| X(b_samepage__vs) {
  302| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  303| 	    ic->arg[cpu->cd.arm.flags & ARM_F_V? 0 : 1];
  304| }
  305| X(b_samepage__vc) {
  306| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  307| 	    ic->arg[cpu->cd.arm.flags & ARM_F_V? 1 : 0];
  308| }
  309| X(b_samepage__hi) {
  310| 	cpu->cd.arm.next_ic = (condition_hi[cpu->cd.arm.flags])?
  311| 	    (struct arm_instr_call *) ic->arg[0] :
  312| 	    (struct arm_instr_call *) ic->arg[1];
  313| }
  314| X(b_samepage__ls) {
  315| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  316| 	    ic->arg[condition_hi[cpu->cd.arm.flags]];
  317| }
  318| X(b_samepage__ge) {
  319| 	cpu->cd.arm.next_ic = (condition_ge[cpu->cd.arm.flags])?
  320| 	    (struct arm_instr_call *) ic->arg[0] :
  321| 	    (struct arm_instr_call *) ic->arg[1];
  322| }
  323| X(b_samepage__lt) {
  324| 	cpu->cd.arm.next_ic = (struct arm_instr_call *)
  325| 	    ic->arg[condition_ge[cpu->cd.arm.flags]];
  326| }
  327| X(b_samepage__gt) {
  328| 	cpu->cd.arm.next_ic = (condition_gt[cpu->cd.arm.flags])?
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

End with one line: `FIXDRAFT_ARMLDREXBHDSPIN: <YES|NO|UNSETTLED> PRESENT, <n> EDITS`.
