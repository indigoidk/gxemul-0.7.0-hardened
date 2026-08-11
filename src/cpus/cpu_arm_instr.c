/*
 *  Copyright (C) 2005-2021  Anders Gavare.  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright  
 *     notice, this list of conditions and the following disclaimer in the 
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
 *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 *  SUCH DAMAGE.
 *
 *
 *  ARM instructions.
 *
 *  Individual functions should keep track of cpu->n_translated_instrs.
 *  (If no instruction was executed, then it should be decreased. If, say, 4
 *  instructions were combined into one function and executed, then it should
 *  be increased by 3.)
 *
 *  Note: cpu->pc is prefered over r[ARM_PC]. r[ARM_PC] is only used in a
 *        few places, and should always be kept in synch with the real
 *        program counter.
 */


/*  #define GATHER_BDT_STATISTICS  */


#ifdef GATHER_BDT_STATISTICS
/*
 *  update_bdt_statistics():
 *
 *  Gathers statistics about load/store multiple instructions.
 *
 *  NOTE/TODO: Perhaps it would be more memory efficient to swap the high
 *  and low parts of the instruction word, so that the lllllll bits become
 *  the high bits; this would cause fewer host pages to be used. Anyway, the
 *  current implementation works on hosts with lots of RAM.
 *
 *  The resulting file, bdt_statistics.txt, should then be processed like
 *  this to give a new cpu_arm_multi.txt:
 *
 *  uniq -c bdt_statistics.txt|sort -nr|head -256|cut -f 2 > cpu_arm_multi.txt
 */
static void update_bdt_statistics(uint32_t iw)
{
	static FILE *f = NULL;
	static long long *counts;
	static char *counts_used;
	static long long n = 0;

	if (f == NULL) {
		size_t s = (1 << 24) * sizeof(long long);
		f = fopen("bdt_statistics.txt", "w");
		if (f == NULL) {
			fprintf(stderr, "update_bdt_statistics(): :-(\n");
			exit(1);
		}
		counts = zeroed_alloc(s);
		counts_used = zeroed_alloc(65536);
	}

	/*  Drop the s-bit: xxxx100P USWLnnnn llllllll llllllll  */
	iw = ((iw & 0x01800000) >> 1) | (iw & 0x003fffff);

	counts_used[iw & 0xffff] = 1;
	counts[iw] ++;

	n ++;
	if ((n % 500000) == 0) {
		int i;
		long long j;
		fatal("[ update_bdt_statistics(): n = %lli ]\n", (long long) n);
		fseek(f, 0, SEEK_SET);
		for (i=0; i<0x1000000; i++)
			if (counts_used[i & 0xffff] && counts[i] != 0) {
				/*  Recreate the opcode:  */
				uint32_t opcode = ((i & 0x00c00000) << 1)
				    | (i & 0x003fffff) | 0x08000000;
				for (j=0; j<counts[i]; j++)
					fprintf(f, "0x%08x\n", opcode);
			}
		fflush(f);
	}
}
#endif


/*****************************************************************************/


/*
 *  Helper definitions:
 *
 *  Each instruction is defined like this:
 *
 *	X(foo)
 *	{
 *		code for foo;
 *	}
 *	Y(foo)
 *
 *  The Y macro defines 14 copies of the instruction, one for each possible
 *  condition code. (The NV condition code is not included, and the AL code
 *  uses the main foo function.)  Y also defines an array with pointers to
 *  all of these functions.
 *
 *  If the compiler is good enough (i.e. allows long enough code sequences
 *  to be inlined), then the Y functions will be compiled as full (inlined)
 *  functions, otherwise they will simply call the X function.
 */

uint8_t condition_hi[16] = { 0,0,1,1, 0,0,0,0, 0,0,1,1, 0,0,0,0 };
uint8_t condition_ge[16] = { 1,0,1,0, 1,0,1,0, 0,1,0,1, 0,1,0,1 };
uint8_t condition_gt[16] = { 1,0,1,0, 0,0,0,0, 0,1,0,1, 0,0,0,0 };

#define Y(n) void arm_instr_ ## n ## __eq(struct cpu *cpu,		\
			struct arm_instr_call *ic)			\
	{  if (cpu->cd.arm.flags & ARM_F_Z)				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __ne(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (!(cpu->cd.arm.flags & ARM_F_Z))				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __cs(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (cpu->cd.arm.flags & ARM_F_C)				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __cc(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (!(cpu->cd.arm.flags & ARM_F_C))				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __mi(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (cpu->cd.arm.flags & ARM_F_N)				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __pl(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (!(cpu->cd.arm.flags & ARM_F_N))				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __vs(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (cpu->cd.arm.flags & ARM_F_V)				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __vc(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (!(cpu->cd.arm.flags & ARM_F_V))				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __hi(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (condition_hi[cpu->cd.arm.flags])				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __ls(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (!condition_hi[cpu->cd.arm.flags])			\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __ge(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (condition_ge[cpu->cd.arm.flags])				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __lt(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (!condition_ge[cpu->cd.arm.flags])			\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __gt(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (condition_gt[cpu->cd.arm.flags])				\
		arm_instr_ ## n (cpu, ic);		}		\
	void arm_instr_ ## n ## __le(struct cpu *cpu,			\
			struct arm_instr_call *ic)			\
	{  if (!condition_gt[cpu->cd.arm.flags])			\
		arm_instr_ ## n (cpu, ic);		}		\
	void (*arm_cond_instr_ ## n  [16])(struct cpu *,		\
			struct arm_instr_call *) = {			\
		arm_instr_ ## n ## __eq, arm_instr_ ## n ## __ne,	\
		arm_instr_ ## n ## __cs, arm_instr_ ## n ## __cc,	\
		arm_instr_ ## n ## __mi, arm_instr_ ## n ## __pl,	\
		arm_instr_ ## n ## __vs, arm_instr_ ## n ## __vc,	\
		arm_instr_ ## n ## __hi, arm_instr_ ## n ## __ls,	\
		arm_instr_ ## n ## __ge, arm_instr_ ## n ## __lt,	\
		arm_instr_ ## n ## __gt, arm_instr_ ## n ## __le,	\
		arm_instr_ ## n , arm_instr_never };

#define cond_instr(n)	( arm_cond_instr_ ## n  [condition_code] )


/*****************************************************************************/


/*
 *  invalid:  Invalid instructions end up here.
 */
X(invalid) {
	uint32_t low_pc;
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	fatal("FATAL ERROR: An internal error occured in the ARM"
	    " dyntrans code. This could be due to an unimplemented instruction"
	    " encoding. pc = 0x%08" PRIx32"\n",
	    (uint32_t)cpu->pc);

	cpu->cd.arm.next_ic = &nothing_call;
}


/*
 *  never:  So far unimplemented "never" instructions end up here.
 *  (Those are the ones using the "0xf" condition prefix.)
 */
X(never) {
	uint32_t low_pc;
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	fatal("[ ARM: unimplemented 0xf instruction at pc = 0x%08" PRIx32" ]\n", (uint32_t)cpu->pc);

	cpu->cd.arm.next_ic = &nothing_call;
}


/*
 *  nop:  Do nothing.
 */
X(nop)
{
}


/*
 *  b:  Branch (to a different translated page)
 *
 *  arg[0] = relative offset from start of page
 */
X(b)
{
	cpu->pc = (uint32_t)((cpu->pc & 0xfffff000) + (int32_t)ic->arg[0]);

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);
}
Y(b)


/*
 *  b_samepage:  Branch (to within the same translated page)
 *
 *  arg[0] = pointer to new arm_instr_call
 *  arg[1] = pointer to the next instruction.
 *
 *  NOTE: This instruction is manually inlined.
 */
X(b_samepage) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *) ic->arg[0];
}
X(b_samepage__eq) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_Z? 0 : 1];
}
X(b_samepage__ne) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_Z? 1 : 0];
}
X(b_samepage__cs) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_C? 0 : 1];
}
X(b_samepage__cc) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_C? 1 : 0];
}
X(b_samepage__mi) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_N? 0 : 1];
}
X(b_samepage__pl) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_N? 1 : 0];
}
X(b_samepage__vs) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_V? 0 : 1];
}
X(b_samepage__vc) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[cpu->cd.arm.flags & ARM_F_V? 1 : 0];
}
X(b_samepage__hi) {
	cpu->cd.arm.next_ic = (condition_hi[cpu->cd.arm.flags])?
	    (struct arm_instr_call *) ic->arg[0] :
	    (struct arm_instr_call *) ic->arg[1];
}
X(b_samepage__ls) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[condition_hi[cpu->cd.arm.flags]];
}
X(b_samepage__ge) {
	cpu->cd.arm.next_ic = (condition_ge[cpu->cd.arm.flags])?
	    (struct arm_instr_call *) ic->arg[0] :
	    (struct arm_instr_call *) ic->arg[1];
}
X(b_samepage__lt) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[condition_ge[cpu->cd.arm.flags]];
}
X(b_samepage__gt) {
	cpu->cd.arm.next_ic = (condition_gt[cpu->cd.arm.flags])?
	    (struct arm_instr_call *) ic->arg[0] :
	    (struct arm_instr_call *) ic->arg[1];
}
X(b_samepage__le) {
	cpu->cd.arm.next_ic = (struct arm_instr_call *)
	    ic->arg[condition_gt[cpu->cd.arm.flags]];
}
void (*arm_cond_instr_b_samepage[16])(struct cpu *,
	struct arm_instr_call *) = {
	arm_instr_b_samepage__eq, arm_instr_b_samepage__ne,
	arm_instr_b_samepage__cs, arm_instr_b_samepage__cc,
	arm_instr_b_samepage__mi, arm_instr_b_samepage__pl,
	arm_instr_b_samepage__vs, arm_instr_b_samepage__vc,
	arm_instr_b_samepage__hi, arm_instr_b_samepage__ls,
	arm_instr_b_samepage__ge, arm_instr_b_samepage__lt,
	arm_instr_b_samepage__gt, arm_instr_b_samepage__le,
	arm_instr_b_samepage, arm_instr_nop };


/*
 *  bx:  Branch, potentially exchanging Thumb/ARM encoding
 *
 *  arg[0] = ptr to rm
 */
X(bx)
{
	uint32_t old_cpsr = cpu->cd.arm.cpsr;
	cpu->pc = reg(ic->arg[0]);
	if (cpu->pc & 1)
		cpu->cd.arm.cpsr |= ARM_FLAG_T;
	else
		cpu->cd.arm.cpsr &= ~ARM_FLAG_T;

	if (cpu->cd.arm.cpsr != old_cpsr)
		cpu->cd.arm.next_ic = &nothing_call;

	if (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {
		fatal("[ ARM pc misaligned? 0x%08x ]\n", (int)cpu->pc);
		cpu->running = 0;
		cpu->n_translated_instrs --;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);
}
Y(bx)


/*
 *  bx_trace:  As bx, but with trace enabled, arg[0] = the link register.
 *
 *  arg[0] = ignored
 */
X(bx_trace)
{
	uint32_t old_cpsr = cpu->cd.arm.cpsr;
	cpu->pc = cpu->cd.arm.r[ARM_LR];
	if (cpu->pc & 1)
		cpu->cd.arm.cpsr |= ARM_FLAG_T;
	else
		cpu->cd.arm.cpsr &= ~ARM_FLAG_T;

	if (cpu->cd.arm.cpsr != old_cpsr)
		cpu->cd.arm.next_ic = &nothing_call;

	if (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {
		fatal("[ ARM pc misaligned? 0x%08x ]\n", (int)cpu->pc);
		cpu->running = 0;
		cpu->n_translated_instrs --;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	cpu_functioncall_trace_return(cpu);

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);
}
Y(bx_trace)


/*
 *  bl:  Branch and Link (to a different translated page)
 *
 *  arg[0] = relative address
 *  arg[1] = offset within current page to the instruction
 */
X(bl)
{
	uint32_t pc = ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[1];
	cpu->cd.arm.r[ARM_LR] = pc + 4;

	/*  Calculate new PC from this instruction + arg[0]  */
	cpu->pc = pc + (int32_t)ic->arg[0];

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);
}
Y(bl)


/*
 *  blx_imm:  Branch and Link, always switching to THUMB encoding
 *
 *  arg[0] = relative address
 *  arg[1] = offset within current page to the current instruction
 */
X(blx_imm)
{
	uint32_t pc = ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[1];
	uint32_t old_cpsr = cpu->cd.arm.cpsr;
	cpu->cd.arm.r[ARM_LR] = pc + 4;

	/*  Calculate new PC from this instruction + arg[0]  */
	cpu->pc = pc + (int32_t)ic->arg[0];

	if (cpu->pc & 1)
		cpu->cd.arm.cpsr |= ARM_FLAG_T;
	else {
		fatal("[ blx_imm internal error. Should have switched to THUMB! 0x%08x ]\n", (int)cpu->pc);
		cpu->running = 0;
		cpu->n_translated_instrs --;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	if (cpu->cd.arm.cpsr != old_cpsr)
		cpu->cd.arm.next_ic = &nothing_call;

	if (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {
		fatal("[ ARM pc misaligned? 0x%08x ]\n", (int)cpu->pc);
		cpu->running = 0;
		cpu->n_translated_instrs --;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	if (cpu->machine->show_trace_tree)
		cpu_functioncall_trace(cpu, cpu->pc);

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);
}


/*
 *  blx_reg:  Branch and Link, potentially exchanging Thumb/ARM encoding
 *
 *  arg[0] = ptr to rm
 *  arg[2] = offset within current page to the instruction to return to
 */
X(blx_reg)
{
	uint32_t lr = ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
	cpu->cd.arm.r[ARM_LR] = lr;
	cpu->pc = reg(ic->arg[0]);

	uint32_t old_cpsr = cpu->cd.arm.cpsr;
	if (cpu->pc & 1)
		cpu->cd.arm.cpsr |= ARM_FLAG_T;
	else
		cpu->cd.arm.cpsr &= ~ARM_FLAG_T;

	if (cpu->cd.arm.cpsr != old_cpsr)
		cpu->cd.arm.next_ic = &nothing_call;

	if (cpu->pc & 2 && ((cpu->pc & 1) == 0)) {
		fatal("[ ARM pc misaligned? 0x%08x ]\n", (int)cpu->pc);
		cpu->running = 0;
		cpu->n_translated_instrs --;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);
}
Y(blx_reg)


/*
 *  bl_trace:  Branch and Link (to a different translated page), with trace
 *
 *  Same as for bl.
 */
X(bl_trace)
{
	uint32_t pc = ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[1];
	cpu->cd.arm.r[ARM_LR] = pc + 4;

	/*  Calculate new PC from this instruction + arg[0]  */
	cpu->pc = pc + (int32_t)ic->arg[0];

	cpu_functioncall_trace(cpu, cpu->pc);

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);
}
Y(bl_trace)


/*
 *  bl_samepage:  A branch + link within the same page
 *
 *  arg[0] = pointer to new arm_instr_call
 */
X(bl_samepage)
{
	cpu->cd.arm.r[ARM_LR] =
	    ((uint32_t)cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
	cpu->cd.arm.next_ic = (struct arm_instr_call *) ic->arg[0];
}
Y(bl_samepage)


/*
 *  bl_samepage_trace:  Branch and Link (to the same page), with trace
 *
 *  Same as for bl_samepage.
 */
X(bl_samepage_trace)
{
	uint32_t low_pc, lr = (cpu->pc & 0xfffff000) + ic->arg[2];

	/*  Link and branch:  */
	cpu->cd.arm.r[ARM_LR] = lr;
	cpu->cd.arm.next_ic = (struct arm_instr_call *) ic->arg[0];

	/*  Synchronize the program counter:  */
	low_pc = ((size_t)cpu->cd.arm.next_ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	/*  ... and show trace:  */
	cpu_functioncall_trace(cpu, cpu->pc);
}
Y(bl_samepage_trace)


/*
 *  clz: Count leading zeroes.
 *
 *  arg[0] = ptr to rm
 *  arg[1] = ptr to rd
 */
X(clz)
{
	uint32_t rm = reg(ic->arg[0]);
	int i = 32, n = 0, j;
	while (i>0) {
		if (rm & 0xff000000) {
			for (j=0; j<8; j++) {
				if (rm & 0x80000000)
					break;
				n ++;
				rm <<= 1;
			}
			break;
		} else {
			rm <<= 8;
			i -= 8;
			n += 8;
		}
	}
	reg(ic->arg[1]) = n;
}
Y(clz)


/*
 *  mul: Multiplication
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rm
 *  arg[2] = ptr to rs
 */
X(mul)
{
	reg(ic->arg[0]) = reg(ic->arg[1]) * reg(ic->arg[2]);
}
Y(mul)
X(muls)
{
	uint32_t result;
	result = reg(ic->arg[1]) * reg(ic->arg[2]);
	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N);
	if (result == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (result & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
	reg(ic->arg[0]) = result;
}
Y(muls)


/*
 *  mla: Multiplication with addition
 *
 *  arg[0] = copy of instruction word
 */
X(mla)
{
	/*  xxxx0000 00ASdddd nnnnssss 1001mmmm (Rd,Rm,Rs[,Rn])  */
	uint32_t iw = ic->arg[0];
	int rd, rs, rn, rm;
	rd = (iw >> 16) & 15; rn = (iw >> 12) & 15,
	rs = (iw >> 8) & 15;  rm = iw & 15;
	cpu->cd.arm.r[rd] = cpu->cd.arm.r[rm] * cpu->cd.arm.r[rs]
	    + cpu->cd.arm.r[rn];
}
Y(mla)
X(mlas)
{
	/*  xxxx0000 00ASdddd nnnnssss 1001mmmm (Rd,Rm,Rs[,Rn])  */
	uint32_t iw = ic->arg[0];
	int rd, rs, rn, rm;
	rd = (iw >> 16) & 15; rn = (iw >> 12) & 15,
	rs = (iw >> 8) & 15;  rm = iw & 15;
	cpu->cd.arm.r[rd] = cpu->cd.arm.r[rm] * cpu->cd.arm.r[rs]
	    + cpu->cd.arm.r[rn];
	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N);
	if (cpu->cd.arm.r[rd] == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (cpu->cd.arm.r[rd] & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
}
Y(mlas)


/*
 *  mla: Multiplication with subtraction
 *
 *  arg[0] = copy of instruction word
 */
X(mls)
{
	/*  xxxx0000 0110dddd aaaammmm 1001nnnn  mls Rd,Rn,Rm,Ra  */
	uint32_t iw = ic->arg[0];
	int rd = (iw >> 16) & 15;
	int rn = (iw >>  0) & 15;
	int rm = (iw >>  8) & 15;
	int ra = (iw >> 12) & 15;

	cpu->cd.arm.r[rd] = cpu->cd.arm.r[ra] -
	    cpu->cd.arm.r[rn] * cpu->cd.arm.r[rm];
}
Y(mls)


/*
 *  mull: Long multiplication
 *
 *  arg[0] = copy of instruction word
 */
X(mull)
{
	/*  xxxx0000 1UAShhhh llllssss 1001mmmm  */
	uint32_t iw; uint64_t tmp; int u_bit, a_bit;
	iw = ic->arg[0];
	u_bit = iw & 0x00400000; a_bit = iw & 0x00200000;
	tmp = cpu->cd.arm.r[iw & 15];
	if (u_bit)
		tmp = (int64_t)(int32_t)tmp
		    * (int64_t)(int32_t)cpu->cd.arm.r[(iw >> 8) & 15];
	else
		tmp *= (uint64_t)cpu->cd.arm.r[(iw >> 8) & 15];
	if (a_bit) {
		uint64_t x = ((uint64_t)cpu->cd.arm.r[(iw >> 16) & 15] << 32)
		    | cpu->cd.arm.r[(iw >> 12) & 15];
		x += tmp;
		cpu->cd.arm.r[(iw >> 16) & 15] = (x >> 32);
		cpu->cd.arm.r[(iw >> 12) & 15] = x;
	} else {
		cpu->cd.arm.r[(iw >> 16) & 15] = (tmp >> 32);
		cpu->cd.arm.r[(iw >> 12) & 15] = tmp;
	}
}
Y(mull)


/*
 *  smulXY:  16-bit * 16-bit multiplication (32-bit result)
 *
 *  arg[0] = ptr to rm
 *  arg[1] = ptr to rs
 *  arg[2] = ptr to rd
 */
X(smulbb)
{
	reg(ic->arg[2]) = (int32_t)(int16_t)reg(ic->arg[0]) *
	    (int32_t)(int16_t)reg(ic->arg[1]);
}
Y(smulbb)
X(smultb)
{
	reg(ic->arg[2]) = (int32_t)(int16_t)(reg(ic->arg[0]) >> 16) *
	    (int32_t)(int16_t)reg(ic->arg[1]);
}
Y(smultb)
X(smulbt)
{
	reg(ic->arg[2]) = (int32_t)(int16_t)reg(ic->arg[0]) *
	    (int32_t)(int16_t)(reg(ic->arg[1]) >> 16);
}
Y(smulbt)
X(smultt)
{
	reg(ic->arg[2]) = (int32_t)(int16_t)(reg(ic->arg[0]) >> 16) *
	    (int32_t)(int16_t)(reg(ic->arg[1]) >> 16);
}
Y(smultt)


/*
 *  mov_reg_reg:  Move a register to another.
 *
 *  arg[0] = ptr to source register
 *  arg[1] = ptr to destination register
 */
X(mov_reg_reg)
{
	reg(ic->arg[1]) = reg(ic->arg[0]);
}
Y(mov_reg_reg)


/*
 *  mov_reg_pc:  Move the PC register to a normal register.
 *
 *  arg[0] = offset compared to start of current page + 8
 *  arg[1] = ptr to destination register
 */
X(mov_reg_pc)
{
	reg(ic->arg[1]) = ((uint32_t)cpu->pc&0xfffff000) + (int32_t)ic->arg[0];
}
Y(mov_reg_pc)


/*
 *  ret_trace:  "mov pc,lr" with trace enabled
 *  ret:  "mov pc,lr" without trace enabled
 *
 *  arg[0] = ignored
 */
X(ret_trace)
{
	uint32_t old_pc, mask_within_page;
	old_pc = cpu->pc;
	mask_within_page = ((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT) |
	    ((1 << ARM_INSTR_ALIGNMENT_SHIFT) - 1);

	/*  Update the PC register:  */
	cpu->pc = cpu->cd.arm.r[ARM_LR];

	cpu_functioncall_trace_return(cpu);

	/*
	 *  Is this a return to code within the same page? Then there is no
	 *  need to update all pointers, just next_ic.
	 */
	if ((old_pc & ~mask_within_page) == (cpu->pc & ~mask_within_page)) {
		cpu->cd.arm.next_ic = cpu->cd.arm.cur_ic_page +
		    ((cpu->pc & mask_within_page) >> ARM_INSTR_ALIGNMENT_SHIFT);
	} else {
		/*  Find the new physical page and update pointers:  */
		quick_pc_to_pointers_arm(cpu);
	}
}
Y(ret_trace)
X(ret)
{
	cpu->pc = cpu->cd.arm.r[ARM_LR];
	quick_pc_to_pointers_arm(cpu);
}
Y(ret)


/*
 *  msr: Move to status register from a normal register or immediate value.
 *
 *  arg[0] = immediate value
 *  arg[1] = mask
 *  arg[2] = pointer to rm
 *
 *  msr_imm and msr_imm_spsr use arg[1] and arg[0].
 *  msr and msr_spsr use arg[1] and arg[2].
 */
X(msr_imm)
{
	uint32_t mask = ic->arg[1];

	if ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_USR32) {
		mask &= 0xff000000;
	}

	int switch_register_banks = (mask & ARM_FLAG_MODE) &&
	    ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) !=
	    (ic->arg[0] & ARM_FLAG_MODE));
	uint32_t new_value = ic->arg[0];

	cpu->cd.arm.cpsr &= 0x0fffffff;
	cpu->cd.arm.cpsr |= (cpu->cd.arm.flags << 28);

	if (switch_register_banks)
		arm_save_register_bank(cpu);

	cpu->cd.arm.cpsr &= ~mask;
	cpu->cd.arm.cpsr |= (new_value & mask);

	cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;

	if (switch_register_banks)
		arm_load_register_bank(cpu);
}
Y(msr_imm)
X(msr)
{
	ic->arg[0] = reg(ic->arg[2]);
	instr(msr_imm)(cpu, ic);
}
Y(msr)
X(msr_imm_spsr)
{
	uint32_t mask = ic->arg[1];
	uint32_t new_value = ic->arg[0];
	switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
	case ARM_MODE_FIQ32:
		cpu->cd.arm.spsr_fiq &= ~mask;
		cpu->cd.arm.spsr_fiq |= (new_value & mask);
		break;
	case ARM_MODE_ABT32:
		cpu->cd.arm.spsr_abt &= ~mask;
		cpu->cd.arm.spsr_abt |= (new_value & mask);
		break;
	case ARM_MODE_UND32:
		cpu->cd.arm.spsr_und &= ~mask;
		cpu->cd.arm.spsr_und |= (new_value & mask);
		break;
	case ARM_MODE_IRQ32:
		cpu->cd.arm.spsr_irq &= ~mask;
		cpu->cd.arm.spsr_irq |= (new_value & mask);
		break;
	case ARM_MODE_SVC32:
		cpu->cd.arm.spsr_svc &= ~mask;
		cpu->cd.arm.spsr_svc |= (new_value & mask);
		break;
	default:fatal("msr_spsr: unimplemented mode %i\n",
		    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
		{
			/*  Synchronize the program counter:  */
			uint32_t old_pc, low_pc = ((size_t)ic - (size_t)
			    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
			cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
			cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
			old_pc = cpu->pc;
			printf("msr_spsr: old pc = 0x%08" PRIx32"\n", old_pc);
		}
		cpu->running = 0;
		cpu->cd.arm.next_ic = &nothing_call;
	}
}
Y(msr_imm_spsr)
X(msr_spsr)
{
	ic->arg[0] = reg(ic->arg[2]);
	instr(msr_imm_spsr)(cpu, ic);
}
Y(msr_spsr)


/*
 *  mrs: Move from status/flag register to a normal register.
 *
 *  arg[0] = pointer to rd
 */
X(mrs)
{
	cpu->cd.arm.cpsr &= 0x0fffffff;
	cpu->cd.arm.cpsr |= (cpu->cd.arm.flags << 28);
	reg(ic->arg[0]) = cpu->cd.arm.cpsr;
}
Y(mrs)


/*
 *  mrs: Move from saved status/flag register to a normal register.
 *
 *  arg[0] = pointer to rd
 */
X(mrs_spsr)
{
	switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
	case ARM_MODE_FIQ32: reg(ic->arg[0]) = cpu->cd.arm.spsr_fiq; break;
	case ARM_MODE_ABT32: reg(ic->arg[0]) = cpu->cd.arm.spsr_abt; break;
	case ARM_MODE_UND32: reg(ic->arg[0]) = cpu->cd.arm.spsr_und; break;
	case ARM_MODE_IRQ32: reg(ic->arg[0]) = cpu->cd.arm.spsr_irq; break;
	case ARM_MODE_SVC32: reg(ic->arg[0]) = cpu->cd.arm.spsr_svc; break;
	case ARM_MODE_USR32:
	case ARM_MODE_SYS32: reg(ic->arg[0]) = 0; break;
	default:fatal("mrs_spsr: unimplemented mode %i\n", cpu->cd.arm.cpsr & ARM_FLAG_MODE);
		cpu->running = 0;
		cpu->cd.arm.next_ic = &nothing_call;
	}
}
Y(mrs_spsr)


/*
 *  mcr_mrc:  Coprocessor move
 *  cdp:      Coprocessor operation
 *
 *  arg[0] = copy of the instruction word
 */
X(mcr_mrc) {
	uint32_t low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
	arm_mcr_mrc(cpu, ic->arg[0]);
}
Y(mcr_mrc)
X(cdp) {
	uint32_t low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
	arm_cdp(cpu, ic->arg[0]);
}
Y(cdp)


/*
 *  openfirmware:
 */
X(openfirmware)
{
	/*  TODO: sync pc?  */
	of_emul(cpu);
	cpu->pc = cpu->cd.arm.r[ARM_LR];
	if (cpu->machine->show_trace_tree)
		cpu_functioncall_trace_return(cpu);
	quick_pc_to_pointers_arm(cpu);
}


/*
 *  reboot:
 */
X(reboot)
{
	cpu->running = 0;
	cpu->n_translated_instrs --;
	cpu->cd.arm.next_ic = &nothing_call;
}


/*
 *  swi:  Software interrupt.
 */
X(swi)
{
	/*  Synchronize the program counter first:  */
	cpu->pc &= 0xfffff000;
	cpu->pc += ic->arg[0];
	arm_exception(cpu, ARM_EXCEPTION_SWI);
}
Y(swi)


/*
 * bkpt:  Breakpoint instruction.
 */
X(bkpt)
{
	/*  Synchronize the program counter first:  */
	cpu->pc &= 0xfffff000;
	cpu->pc += ic->arg[0];
	arm_exception(cpu, ARM_EXCEPTION_PREF_ABT);
}
Y(bkpt)


/*
 *  und:  Undefined instruction.
 */
X(und)
{
	/*  Synchronize the program counter first:  */
	cpu->pc &= 0xfffff000;
	cpu->pc += ic->arg[0];
	arm_exception(cpu, ARM_EXCEPTION_UND);
}
Y(und)


/*
 *  movt:  Move Top.
 *
 *  arg[1] = 32-bit immediate value. Top 16 bits are those of interest.
 *  arg[2] = ptr to rd
 */
X(movt)
{
	reg(ic->arg[2]) &= 0xffff;
	reg(ic->arg[2]) |= ic->arg[1];
}
Y(movt)


/*
 *  movw:  Move (Word).
 *
 *  arg[1] = 32-bit immediate value.
 *  arg[2] = ptr to rd
 */
X(movw)
{
	reg(ic->arg[2]) = ic->arg[1];
}
Y(movw)


/*
 *  rev:  Reverse endian.
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rm
 */
X(rev)
{
	uint32_t v = reg(ic->arg[1]);

	reg(ic->arg[0]) = (v >> 24) | ((v & 0x00ff0000) >> 8)
		| ((v & 0x0000ff00) << 8) | ((v & 0xff) << 24);
}
Y(rev)


/*
 *  uxtb:  Unsigned Extend Byte.
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rm
 *  arg[2] = rotation amount (shift works too)
 */
X(uxtb)
{
	uint32_t x = reg(ic->arg[1]);
	reg(ic->arg[0]) = (uint8_t)(x >> ic->arg[2]);
}
Y(uxtb)


/*
 *  sxth:  Signed Extend Halfword.
 *
 *  TODO: Could be optimized so that the rotation amount is "inlined".
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rm
 *  arg[2] = rotation amount
 */
X(sxth)
{
	uint32_t x = reg(ic->arg[1]);

	switch (ic->arg[2]) {
	case 0:	break;
	case 8: x >>= 8; break;
	case 16: x >>= 16; break;
	case 24: x = (x >> 24) | ((x & 255) << 8); break;
	}

	int16_t rotated = x;
	reg(ic->arg[0]) = (int32_t)rotated;
}
Y(sxth)


/*
 *  uxth:  Unsigned Extend Halfword.
 *
 *  TODO: Could be optimized so that the rotation amount is "inlined".
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rm
 *  arg[2] = rotation amount
 */
X(uxth)
{
	uint32_t x = reg(ic->arg[1]);

	switch (ic->arg[2]) {
	case 0:	break;
	case 8: x >>= 8; break;
	case 16: x >>= 16; break;
	case 24: x = (x >> 24) | ((x & 255) << 8); break;
	}

	uint16_t rotated = x;
	reg(ic->arg[0]) = (uint32_t)rotated;
}
Y(uxth)


/*
 *  uxtah:  Unsigned Extend and Add Byte.
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rn
 *  arg[2] = ptr to rm
 */
X(uxtab)
{
	reg(ic->arg[0]) = reg(ic->arg[1]) + (uint8_t)reg(ic->arg[2]);
}
Y(uxtab)


/*
 *  dpis_imm_rotc:  A flag-setting logical data-processing instruction whose
 *		    ROTATED immediate came out small.
 *
 *  #320: ARM's shifter carry-out for an immediate operand is "unchanged if the
 *  rotate is zero, otherwise bit 31 of the rotated value". The dpi template
 *  decides that from the VALUE, treating "greater than 255" as a proxy for
 *  "was rotated" -- which is right in every case except a rotate whose result
 *  lands at or below 255, where the architecture says clear the carry and the
 *  proxy leaves it alone. The decoder used to answer that by stopping the
 *  emulator, and it stopped it far more widely than the hazard: the rejection
 *  ignored both the S bit and the opcode, so even `mov r0, #4 ROR 2`, which
 *  writes no flags at all, halted the machine.
 *
 *  Only the eight logical opcodes consume the shifter carry, and only when S
 *  is set -- the same set the REGISTER path twenty lines above already names
 *  for itself. Those are routed here; everything else now decodes normally.
 *  The carry is CLEARED unconditionally, because bit 31 of a value at or below
 *  255 is zero.
 *
 *  Carrying the instruction word (the `mla` shape) rather than a marker bit is
 *  what makes this portable: the argument slots hold the value and two
 *  register pointers, and a marker above bit 31 would exist only on a 64-bit
 *  host -- and would be invisible anyway, since the template reads the operand
 *  as a uint32_t.
 *
 *  arg[0] = the instruction word
 *  arg[1] = the rotated immediate
 */
X(dpis_imm_rotc)
{
	uint32_t iw = ic->arg[0], b = ic->arg[1], a, c;
	int op = (iw >> 21) & 15;
	int rn = (iw >> 16) & 15;

	if (rn == ARM_PC) {
		/*
		 *  #322: reading the PC as the source yields this
		 *  instruction's address plus 8, which has to be
		 *  reconstructed from the ic slot exactly as the template
		 *  does -- r[15] is not maintained during execution.
		 *
		 *  The first version of this handler simply refused rn == PC
		 *  and left those encodings on the old path, on the stated
		 *  grounds that a cold handler could not reach the
		 *  computation. That was wrong: it needs only ic,
		 *  cur_ic_page and cpu->pc, all of which are right here.
		 */
		uint32_t low_pc = ((size_t)ic - (size_t)
		    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
		a = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
		    << ARM_INSTR_ALIGNMENT_SHIFT);
		a += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
	} else
		a = cpu->cd.arm.r[rn];

	switch (op) {
	case 0x0:				/*  AND  */
	case 0x8: c = a & b; break;		/*  TST  */
	case 0x1:				/*  EOR  */
	case 0x9: c = a ^ b; break;		/*  TEQ  */
	case 0xc: c = a | b; break;		/*  ORR  */
	case 0xd: c = b; break;			/*  MOV  */
	case 0xe: c = a & ~b; break;		/*  BIC  */
	default:  c = ~b; break;		/*  MVN  */
	}

	/*  TST and TEQ compute their flags and write no register.  */
	if (op != 0x8 && op != 0x9)
		cpu->cd.arm.r[(iw >> 12) & 15] = c;

	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N | ARM_F_C);
	if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if ((int32_t)c < 0)
		cpu->cd.arm.flags |= ARM_F_N;
	/*  V is untouched, and C stays clear.  */
}
Y(dpis_imm_rotc)


/*
 *  uxtab_rot:  Unsigned Extend and Add Byte, with a non-zero rotation.
 *
 *  #319: a rotate used to reach `goto bad`, which stops the emulator on an
 *  instruction the decoder otherwise implements. There is no room for the
 *  rotate in the three argument slots -- rd, rn and rm already fill them --
 *  so this variant carries the instruction word instead and re-extracts,
 *  the same shape `mla` and the block-transfer handlers use.
 *
 *  A BYTE extract gives the same answer under a rotate as under a shift at
 *  every encodable amount, because the bits that wrap land above bit 7.
 *
 *  arg[0] = the instruction word
 */
X(uxtab_rot)
{
	uint32_t iw = ic->arg[0];
	uint32_t x = cpu->cd.arm.r[iw & 15];

	cpu->cd.arm.r[(iw >> 12) & 15] = cpu->cd.arm.r[(iw >> 16) & 15]
	    + (uint8_t)(x >> (((iw >> 10) & 3) * 8));
}
Y(uxtab_rot)


/*
 *  uxtah:  Unsigned Extend and Add Halfword.
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rn
 *  arg[2] = ptr to rm
 */
X(uxtah)
{
	reg(ic->arg[0]) = reg(ic->arg[1]) + (uint16_t)reg(ic->arg[2]);
}
Y(uxtah)


/*
 *  uxtah_rot:  Unsigned Extend and Add Halfword, with a non-zero rotation.
 *
 *  #319: as uxtab_rot above -- but a HALFWORD extract is not a shift at a
 *  rotate of 24. There the low byte of rm wraps into bits 15:8, which a
 *  plain shift would drop; the sibling uxth and sxth already spell that
 *  case out, and copying the byte form's shift here would have been silently
 *  wrong for exactly one of the four encodings.
 *
 *  arg[0] = the instruction word
 */
X(uxtah_rot)
{
	uint32_t iw = ic->arg[0];
	uint32_t x = cpu->cd.arm.r[iw & 15];
	int rot = ((iw >> 10) & 3) * 8;

	if (rot == 24)
		x = (x >> 24) | ((x & 0xff) << 8);
	else
		x >>= rot;

	cpu->cd.arm.r[(iw >> 12) & 15] = cpu->cd.arm.r[(iw >> 16) & 15]
	    + (uint16_t)x;
}
Y(uxtah_rot)


/*
 *  ubfx:  Unsigned Bit-Field Extract.
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rn
 *  arg[2] = (width << 16) + lsb
 */
X(ubfx)
{
	uint32_t x = reg(ic->arg[1]);

	int lsb = (uint8_t)ic->arg[2];
	int width = ic->arg[2] >> 16;

	uint32_t mask = (1 << width) - 1;

	x >>= lsb;
	x &= mask;

	reg(ic->arg[0]) = x;
}
Y(ubfx)


/*
 *  sbfx:  Signed Bit-Field Extract.
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rn
 *  arg[2] = (width << 16) + lsb
 */
X(sbfx)
{
	uint32_t x = reg(ic->arg[1]);

	int lsb = (uint8_t)ic->arg[2];
	int width = ic->arg[2] >> 16;

	uint32_t mask = (1 << width) - 1;
	x >>= lsb;
	x &= mask;

	uint32_t topBitMask = 1 << (width-1);
	if (x & topBitMask && width < 32)
		x |= ~mask;

	reg(ic->arg[0]) = x;
}
Y(sbfx)


/*
 *  bfi:  Bit-Field Insert.
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rn
 *  arg[2] = (msb << 16) + lsb
 */
X(bfi)
{
	uint32_t x = reg(ic->arg[1]);

	int lsb = (uint8_t)ic->arg[2];
	int msb = ic->arg[2] >> 16;
	int width = msb - lsb + 1;

	x <<= lsb;

	uint32_t mask = (1 << width) - 1;

	mask <<= lsb;

	reg(ic->arg[0]) &= ~mask;
	reg(ic->arg[0]) |= (x & mask);
}
Y(bfi)


/*
 *  swp, swpb:  Swap (word or byte).
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rm
 *  arg[2] = ptr to rn
 */
X(swp)
{
	uint32_t addr = reg(ic->arg[2]), data, data2;
	unsigned char d[4];

	/*  Synchronize the program counter:  */
	uint32_t low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	if (!cpu->memory_rw(cpu, cpu->mem, addr, d, sizeof(d), MEM_READ,
	    CACHE_DATA)) {
		fatal("swp: load failed\n");
		return;
	}
	data = d[0] + (d[1] << 8) + (d[2] << 16) + ((uint32_t)d[3] << 24);
	data2 = reg(ic->arg[1]);
	d[0] = data2; d[1] = data2 >> 8; d[2] = data2 >> 16; d[3] = data2 >> 24;
	if (!cpu->memory_rw(cpu, cpu->mem, addr, d, sizeof(d), MEM_WRITE,
	    CACHE_DATA)) {
		fatal("swp: store failed\n");
		return;
	}
	reg(ic->arg[0]) = data;
}
Y(swp)
X(swpb)
{
	uint32_t addr = reg(ic->arg[2]), data;
	unsigned char d[1];

	/*  Synchronize the program counter:  */
	uint32_t low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	if (!cpu->memory_rw(cpu, cpu->mem, addr, d, sizeof(d), MEM_READ,
	    CACHE_DATA)) {
		fatal("swp: load failed\n");
		return;
	}
	data = d[0];
	d[0] = reg(ic->arg[1]);
	if (!cpu->memory_rw(cpu, cpu->mem, addr, d, sizeof(d), MEM_WRITE,
	    CACHE_DATA)) {
		fatal("swp: store failed\n");
		return;
	}
	reg(ic->arg[0]) = data;
}
Y(swpb)


extern void (*arm_load_store_instr[1024])(struct cpu *,
	struct arm_instr_call *);
X(store_w1_word_u1_p0_imm);
X(store_w0_byte_u1_p0_imm);
X(store_w0_word_u1_p0_imm);
X(store_w0_word_u1_p1_imm);
X(load_w0_word_u1_p0_imm);
X(load_w0_word_u1_p1_imm);
X(load_w1_word_u1_p0_imm);
X(load_w0_byte_u1_p1_imm);
X(load_w0_byte_u1_p1_reg);
X(load_w1_byte_u1_p1_imm);

extern void (*arm_load_store_instr_pc[1024])(struct cpu *,
	struct arm_instr_call *);

extern void (*arm_load_store_instr_3[2048])(struct cpu *,
	struct arm_instr_call *);

extern void (*arm_load_store_instr_3_pc[2048])(struct cpu *,
	struct arm_instr_call *);

extern uint32_t (*arm_r[8192])(struct cpu *, struct arm_instr_call *);
extern uint32_t arm_r_r3_t0_c0(struct cpu *cpu, struct arm_instr_call *ic);

extern void (*arm_dpi_instr[2 * 2 * 2 * 16 * 16])(struct cpu *,
	struct arm_instr_call *);
extern void (*arm_dpi_instr_regshort[2 * 16 * 16])(struct cpu *,
	struct arm_instr_call *);
X(cmps);
X(teqs);
X(tsts);
X(sub);
X(add);
X(subs);
X(eor_regshort);
X(cmps_regshort);


#include "cpu_arm_instr_misc.c"


/*
 *  Shared between regular ARM and the THUMB encoded 'pop'.
 */
void arm_pop(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint32_t iw)
{
	uint32_t addr = *np;
	unsigned char data[4];
	unsigned char *page;
	int i, return_flag = 0;
	uint32_t new_values[16];

	if (s_bit) {
		/*  Load to USR registers:  */
		if ((cpu->cd.arm.cpsr & ARM_FLAG_MODE) == ARM_MODE_USR32) {
			fatal("[ bdt_load: s-bit: in usermode? ]\n");
			s_bit = 0;
		}
		if (iw & 0x8000) {
			s_bit = 0;
			return_flag = 1;
		}
	}

	for (i=(u_bit? 0 : 15); i>=0 && i<=15; i+=(u_bit? 1 : -1)) {
		uint32_t value;

		if (!((iw >> i) & 1)) {
			/*  Skip register i:  */
			continue;
		}

		if (p_bit) {
			if (u_bit)
				addr += sizeof(uint32_t);
			else
				addr -= sizeof(uint32_t);
		}

		page = cpu->cd.arm.host_load[addr >> 12];
		if (page != NULL) {
			uint32_t *p32 = (uint32_t *) page;
			value = p32[(addr & 0xfff) >> 2];
			/*  Change byte order of value if
			    host and emulated endianness differ:  */
#ifdef HOST_LITTLE_ENDIAN
			if (cpu->byte_order == EMUL_BIG_ENDIAN)
#else
			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
#endif
				value = ((value & 0xff) << 24) |
				    ((value & 0xff00) << 8) |
				    ((value & 0xff0000) >> 8) |
				    ((value & 0xff000000) >> 24);
		} else {
			if (!cpu->memory_rw(cpu, cpu->mem, addr, data,
			    sizeof(data), MEM_READ, CACHE_DATA)) {
				/*  load failed  */
				return;
			}
			if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
				value = data[0] +
				    (data[1] << 8) + (data[2] << 16)
				    + ((uint32_t)data[3] << 24);
			} else {
				value = data[3] +
				    (data[2] << 8) + (data[1] << 16)
				    + ((uint32_t)data[0] << 24);
			}
		}

		new_values[i] = value;

		if (!p_bit) {
			if (u_bit)
				addr += sizeof(uint32_t);
			else
				addr -= sizeof(uint32_t);
		}
	}

	for (i=(u_bit? 0 : 15); i>=0 && i<=15; i+=(u_bit? 1 : -1)) {
		if (!((iw >> i) & 1)) {
			/*  Skip register i:  */
			continue;
		}

		if (!s_bit) {
			cpu->cd.arm.r[i] = new_values[i];
		} else {
			switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
			case ARM_MODE_USR32:
			case ARM_MODE_SYS32:
				cpu->cd.arm.r[i] = new_values[i];
				break;
			case ARM_MODE_FIQ32:
				if (i >= 8 && i <= 14)
					cpu->cd.arm.default_r8_r14[i-8] =
					    new_values[i];
				else
					cpu->cd.arm.r[i] = new_values[i];
				break;
			case ARM_MODE_SVC32:
			case ARM_MODE_ABT32:
			case ARM_MODE_UND32:
			case ARM_MODE_IRQ32:
				if (i >= 13 && i <= 14)
					cpu->cd.arm.default_r8_r14[i-8] =
					    new_values[i];
				else
					cpu->cd.arm.r[i] = new_values[i];
				break;
			}
		}
	}

	if (w_bit)
		*np = addr;

	if (return_flag) {
		uint32_t new_cpsr;
		int switch_register_banks;

		switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
		case ARM_MODE_FIQ32:
			new_cpsr = cpu->cd.arm.spsr_fiq; break;
		case ARM_MODE_ABT32:
			new_cpsr = cpu->cd.arm.spsr_abt; break;
		case ARM_MODE_UND32:
			new_cpsr = cpu->cd.arm.spsr_und; break;
		case ARM_MODE_IRQ32:
			new_cpsr = cpu->cd.arm.spsr_irq; break;
		case ARM_MODE_SVC32:
			new_cpsr = cpu->cd.arm.spsr_svc; break;
		default:fatal("bdt_load: unimplemented mode %i\n",
			    cpu->cd.arm.cpsr & ARM_FLAG_MODE);
			cpu->running = 0;
			cpu->cd.arm.next_ic = &nothing_call;
			return;
		}

		switch_register_banks = (cpu->cd.arm.cpsr & ARM_FLAG_MODE) !=
		    (new_cpsr & ARM_FLAG_MODE);

		if (switch_register_banks)
			arm_save_register_bank(cpu);

		cpu->cd.arm.cpsr = new_cpsr;
		cpu->cd.arm.flags = cpu->cd.arm.cpsr >> 28;

		if (switch_register_banks)
			arm_load_register_bank(cpu);
	}

	/*  NOTE: Special case: Loading the PC  */
	if (iw & 0x8000) {
		cpu->pc = cpu->cd.arm.r[ARM_PC] & 0xfffffffc;
		if (cpu->machine->show_trace_tree)
			cpu_functioncall_trace_return(cpu);
		/*  TODO: There is no need to update the
		    pointers if this is a return to the
		    same page!  */
		/*  Find the new physical page and update the
		    translation pointers:  */
		quick_pc_to_pointers_arm(cpu);
	}
}


/*
 *  Shared between regular ARM and the THUMB encoded 'push'.
 */
void arm_push(struct cpu* cpu, uint32_t* np, int p_bit, int u_bit, int s_bit, int w_bit, uint16_t regs)
{
	int i;
	uint32_t value, addr = *np;
	unsigned char data[4];
	unsigned char *page;

	for (i=(u_bit? 0 : 15); i>=0 && i<=15; i+=(u_bit? 1 : -1)) {
		if (!((regs >> i) & 1)) {
			/*  Skip register i:  */
			continue;
		}

		value = cpu->cd.arm.r[i];

		if (s_bit) {
			switch (cpu->cd.arm.cpsr & ARM_FLAG_MODE) {
			case ARM_MODE_FIQ32:
				if (i >= 8 && i <= 14)
					value = cpu->cd.arm.default_r8_r14[i-8];
				break;
			case ARM_MODE_ABT32:
			case ARM_MODE_UND32:
			case ARM_MODE_IRQ32:
			case ARM_MODE_SVC32:
				if (i >= 13 && i <= 14)
					value = cpu->cd.arm.default_r8_r14[i-8];
				break;
			case ARM_MODE_USR32:
			case ARM_MODE_SYS32:
				break;
			}
		}

		/*  NOTE/TODO: 8 vs 12 on some ARMs  */
		if (i == ARM_PC)
			value = cpu->pc + 12;

		if (p_bit) {
			if (u_bit)
				addr += sizeof(uint32_t);
			else
				addr -= sizeof(uint32_t);
		}

		page = cpu->cd.arm.host_store[addr >> 12];
		if (page != NULL) {
			uint32_t *p32 = (uint32_t *) page;
			/*  Change byte order of value if
			    host and emulated endianness differ:  */
#ifdef HOST_LITTLE_ENDIAN
			if (cpu->byte_order == EMUL_BIG_ENDIAN)
#else
			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
#endif
				value = ((value & 0xff) << 24) |
				    ((value & 0xff00) << 8) |
				    ((value & 0xff0000) >> 8) |
				    ((value & 0xff000000) >> 24);
			p32[(addr & 0xfff) >> 2] = value;
		} else {
			if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
				data[0] = value;
				data[1] = value >> 8;
				data[2] = value >> 16;
				data[3] = value >> 24;
			} else {
				data[0] = value >> 24;
				data[1] = value >> 16;
				data[2] = value >> 8;
				data[3] = value;
			}
			if (!cpu->memory_rw(cpu, cpu->mem, addr, data,
			    sizeof(data), MEM_WRITE, CACHE_DATA)) {
				/*  store failed  */
				return;
			}
		}

		if (!p_bit) {
			if (u_bit)
				addr += sizeof(uint32_t);
			else
				addr -= sizeof(uint32_t);
		}
	}

	if (w_bit)
		*np = addr;
}


/*
 *  bdt_load:  Block Data Transfer, Load
 *
 *  arg[0] = pointer to uint32_t in host memory, pointing to the base register
 *  arg[1] = 32-bit instruction word. Most bits are read from this.
 */
X(bdt_load)
{
	uint32_t *np = (uint32_t *)ic->arg[0];
	uint32_t low_pc;
	uint32_t iw = ic->arg[1];  /*  xxxx100P USWLnnnn llllllll llllllll  */
	int p_bit = iw & 0x01000000;
	int u_bit = iw & 0x00800000;
	int s_bit = iw & 0x00400000;
	int w_bit = iw & 0x00200000;

#ifdef GATHER_BDT_STATISTICS
	if (!s_bit)
		update_bdt_statistics(iw);
#endif

	/*  Synchronize the program counter:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	arm_pop(cpu, np, p_bit, u_bit, s_bit, w_bit, (uint16_t)iw);
}
Y(bdt_load)


/*
 *  bdt_store:  Block Data Transfer, Store
 *
 *  arg[0] = pointer to uint32_t in host memory, pointing to the base register
 *  arg[1] = 32-bit instruction word. Most bits are read from this.
 */
X(bdt_store)
{
	uint32_t *np = (uint32_t *)ic->arg[0];
	uint32_t low_pc;
	uint32_t iw = ic->arg[1];  /*  xxxx100P USWLnnnn llllllll llllllll  */
	int p_bit = iw & 0x01000000;
	int u_bit = iw & 0x00800000;
	int s_bit = iw & 0x00400000;
	int w_bit = iw & 0x00200000;

#ifdef GATHER_BDT_STATISTICS
	if (!s_bit)
		update_bdt_statistics(iw);
#endif

	/*  Synchronize the program counter:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	arm_push(cpu, np, p_bit, u_bit, s_bit, w_bit, (uint16_t)iw);
}
Y(bdt_store)


/*
 *  Load Register Exclusive (ARM "load linked"):
 *
 *  A Load Register Exclusive instruction initiates a RMW (read-modify-write)
 *  sequence.
 *
 *  A Store Register Exclusive instruction ends the sequence.
 *
 *  arg[0] = ptr to rt
 *  arg[1] = ptr to rn
 *  arg[2] = int32_t imm offset
 */
X(ldrex)
{
	uint32_t addr = reg(ic->arg[1]) + (int32_t)ic->arg[2];
	int low_pc;
	uint8_t word[sizeof(uint32_t)];

	/*  Synchronize the program counter:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	if (addr & (sizeof(word)-1)) {
		fatal("TODO: ldrex unaligned access: exception\n");
		cpu->running = 0;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	if (!cpu->memory_rw(cpu, cpu->mem, addr, word,
	    sizeof(word), MEM_READ, CACHE_DATA)) {
		/*  An exception occurred.  */
		return;
	}

	cpu->cd.arm.rmw = 1;
	cpu->cd.arm.rmw_addr = addr;
	cpu->cd.arm.rmw_len = sizeof(word);

	if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
		reg(ic->arg[0]) = word[0] + (word[1] << 8)
		    + (word[2] << 16) + ((uint32_t)word[3] << 24);
	else
		reg(ic->arg[0]) = word[3] + (word[2] << 8)
		    + (word[1] << 16) + ((uint32_t)word[0] << 24);
}
Y(ldrex)
/*
 *  Store Register Exclusive
 *
 *  arg[0] = ptr to rd
 *  arg[1] = ptr to rn
 *  arg[2] = ptr to rt
 */
X(strex)
{
	uint32_t addr = reg(ic->arg[1]);
	uint64_t r = reg(ic->arg[2]);
	int low_pc, i;
	uint8_t word[sizeof(uint32_t)];
	
	/*  Synchronize the program counter:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

	if (addr & (sizeof(word)-1)) {
		fatal("TODO: strex unaligned access: exception\n");
		cpu->running = 0;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
		word[0]=r; word[1]=r>>8; word[2]=r>>16; word[3]=r>>24;
	} else {
		word[3]=r; word[2]=r>>8; word[1]=r>>16; word[0]=r>>24;
	}

	/*  If rmw is 0, then the store failed.  (This cache-line was written
	    to by someone else.)  */
	if (cpu->cd.arm.rmw == 0 || cpu->cd.arm.rmw_addr != addr
	    || cpu->cd.arm.rmw_len != sizeof(word)) {
		reg(ic->arg[0]) = 1;	// 1 = fail.
		cpu->cd.arm.rmw = 0;
		return;
	}

	if (!cpu->memory_rw(cpu, cpu->mem, addr, word,
	    sizeof(word), MEM_WRITE, CACHE_DATA)) {
		/*  An exception occurred.  */
		return;
	}

	/*  We succeeded. Let's invalidate everybody else's store to this
	    cache line:  */
	for (i=0; i<cpu->machine->ncpus; i++) {
		if (cpu->machine->cpus[i]->cd.arm.rmw) {
			uint64_t yaddr = addr, xaddr = cpu->machine->cpus[i]->
			    cd.arm.rmw_addr;

			/*  8-2048 bytes, implementation dependent :-(  */			
			/*  https://stackoverflow.com/questions/11383125/do-the-arm-instructions-ldrex-strex-have-to-operate-on-cache-aligned-data  */
			uint64_t mask = 2047;

			xaddr &= mask;
			yaddr &= mask;
			if (xaddr == yaddr)
				cpu->machine->cpus[i]->cd.arm.rmw = 0;
		}
	}

	reg(ic->arg[0]) = 0;	// 0 = success
	cpu->cd.arm.rmw = 0;
}
Y(strex)


/*  Various load/store multiple instructions:  */
extern uint32_t *multi_opcode[256];
extern void (**multi_opcode_f[256])(struct cpu *, struct arm_instr_call *);
X(multi_0x08b15018);
X(multi_0x08ac000c__ge);
X(multi_0x08a05018);


/*****************************************************************************/


/*
 *  netbsd_memset:
 *
 *  The core of a NetBSD/arm memset.
 *
 *  f01bc420:  e25XX080     subs    rX,rX,#0x80
 *  f01bc424:  a8ac000c     stmgeia ip!,{r2,r3}   (16 of these)
 *  ..
 *  f01bc464:  caffffed     bgt     0xf01bc420      <memset+0x38>
 */
X(netbsd_memset)
{
	unsigned char *page;
	uint32_t addr;

	do {
		addr = cpu->cd.arm.r[ARM_IP];

		instr(subs)(cpu, ic);

		if (((cpu->cd.arm.flags & ARM_F_N)?1:0) !=
		    ((cpu->cd.arm.flags & ARM_F_V)?1:0)) {
			cpu->n_translated_instrs += 16;
			/*  Skip the store multiples:  */
			cpu->cd.arm.next_ic = &ic[17];
			return;
		}

		/*  Crossing a page boundary? Then continue non-combined.  */
		if ((addr & 0xfff) + 128 > 0x1000)
			return;

		/*  R2/R3 non-zero? Not allowed here.  */
		if (cpu->cd.arm.r[2] != 0 || cpu->cd.arm.r[3] != 0)
			return;

		/*  printf("addr = 0x%08x\n", addr);  */

		page = cpu->cd.arm.host_store[addr >> 12];
		/*  No page translation? Continue non-combined.  */
		if (page == NULL)
			return;

		/*  Clear:  */
		memset(page + (addr & 0xfff), 0, 128);
		cpu->cd.arm.r[ARM_IP] = addr + 128;
		cpu->n_translated_instrs += 16;

		/*  Branch back if greater:  */
		cpu->n_translated_instrs += 1;
	} while (((cpu->cd.arm.flags & ARM_F_N)?1:0) ==
	    ((cpu->cd.arm.flags & ARM_F_V)?1:0) &&
	    !(cpu->cd.arm.flags & ARM_F_Z));

	/*  Continue at the instruction after the bgt:  */
	cpu->cd.arm.next_ic = &ic[18];
}


/*
 *  netbsd_memcpy:
 *
 *  The core of a NetBSD/arm memcpy.
 *
 *  f01bc530:  e8b15018     ldmia   r1!,{r3,r4,ip,lr}
 *  f01bc534:  e8a05018     stmia   r0!,{r3,r4,ip,lr}
 *  f01bc538:  e8b15018     ldmia   r1!,{r3,r4,ip,lr}
 *  f01bc53c:  e8a05018     stmia   r0!,{r3,r4,ip,lr}
 *  f01bc540:  e2522020     subs    r2,r2,#0x20
 *  f01bc544:  aafffff9     bge     0xf01bc530
 */
X(netbsd_memcpy)
{
	unsigned char *page_0, *page_1;
	uint32_t addr_r0, addr_r1;
	/*
	 *  #358: count the 32-byte iterations this call actually folded, so the
	 *  marker can be COUNT-AND-SUMMARISE. Unlike the other four marked folds
	 *  this handler has a real loop, so one DISPATCH emits one line however
	 *  many iterations it folded. A copy that never straddles a page is a
	 *  single dispatch and therefore a single line; a straddling copy bails,
	 *  runs one genuine iteration, and the back-branch re-dispatches this
	 *  slot, so it costs roughly one line per crossing. (An earlier draft of
	 *  this comment said "one line per call by construction", which is false
	 *  for exactly the straddling case the next paragraph describes -- a 1 MB
	 *  copy bails about 512 times. The flood conclusion survives: lines track
	 *  crossings, not the 32-byte iterations, and stay far below the
	 *  per-dispatch volume accepted for the loopless folds.)
	 *
	 *  The guard on the mid-loop markers below is about TRUTHFULNESS, not
	 *  flood control, and must not be confused with strlen's `n_loops > 1`
	 *  guard, which exists to suppress low-information lines. Both of this
	 *  fold's bail-outs are INSIDE the loop: a bail on the first iteration
	 *  folded nothing, while a bail on iteration k > 1 follows k-1 completed
	 *  32-byte copies. So a summary-only marker would under-report every
	 *  page-straddling copy (a 1 MB copy bails about 512 times), and an
	 *  unguarded bail marker would over-report the zero-work entries at page
	 *  ends. Reporting the count is what makes a row able to check that the
	 *  pieces sum to the copy the register advance implies.
	 */
	unsigned n_iter = 0;

	do {
		addr_r0 = cpu->cd.arm.r[0];
		addr_r1 = cpu->cd.arm.r[1];

		/*  printf("addr_r0 = %08x  r1 = %08x\n", addr_r0, addr_r1);  */

		/*  Crossing a page boundary? Then continue non-combined.  */
		if ((addr_r0 & 0xfff) + 32 > 0x1000 ||
		    (addr_r1 & 0xfff) + 32 > 0x1000) {
			if (n_iter)			/*  #358  */
				debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_memcpy",
				    VERBOSITY_DEBUG,
				    "combined %u iterations, page boundary",
				    n_iter);
			instr(multi_0x08b15018)(cpu, ic);
			return;
		}

		page_0 = cpu->cd.arm.host_store[addr_r0 >> 12];
		page_1 = cpu->cd.arm.host_store[addr_r1 >> 12];

		/*  No page translations? Continue non-combined.  */
		if (page_0 == NULL || page_1 == NULL) {
			if (n_iter)			/*  #358  */
				debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_memcpy",
				    VERBOSITY_DEBUG,
				    "combined %u iterations, no page", n_iter);
			instr(multi_0x08b15018)(cpu, ic);
			return;
		}

		/*  #354: the real `ldmia r1!,{r3,r4,ip,lr}` leaves those four
		    registers holding the LAST 16 bytes loaded -- the final
		    iteration's SECOND ldmia (src+16..+31). The fold moved the
		    bytes with memcpy but never wrote the registers, so the guest
		    read them stale ("publishes only r0/r1"). Direct host read,
		    NO byteswap, base masked to a word -- matching the handler
		    this fold emulates (multi_0x08b15018, generated by
		    generate_arm_multi.c:117: `addr &= 0xffc`, then a plain
		    `r[k] = p[k]`) and the page-cross / NULL-page bail-outs above,
		    which delegate to that same handler. So fold == handler ==
		    bail-out: an on-page copy cannot leave different registers
		    than an identical copy that straddles a page. Each iteration
		    overwrites r3/r4/ip/lr, so the final iteration's block
		    persists, as the architecture leaves it.

		    The mask is NOT cosmetic. ARM's LDM ignores addr[1:0] rather
		    than requiring alignment, and this matcher matches code SHAPE,
		    not register values, so a guest with r1 & 3 != 0 does fold:
		    measured at r1 = SRC+1, the masked read publishes what the
		    genuine sequence publishes, while `& 0xfff` would publish
		    byte-rotated words. `(r1 & 0xfff) + 16 <= 0xff0` rules out a
		    carry past bit 11, so (r1 & 0xffc) + 16 is bit-for-bit the
		    address the real second ldmia reads. Bound: the entry guard
		    gives (r1 & 0xfff) <= 0xfe0, and masking only lowers that, so
		    +16..+31 stays inside the page.

		    Published BEFORE the memcpy, and NOT because that makes
		    overlap safe -- it does not. The real second ldmia runs AFTER
		    the first stmia, so on a FORWARD overlap it loads post-store
		    bytes, which no placement around a single memcpy can
		    reproduce (measured: dst = src+16 diverges either way). The
		    reason is determinism: publish-after would read bytes a
		    UB-on-overlap memcpy had just written, so the registers would
		    depend on the host memcpy's direction and vector width.
		    Publish-before is identical to publish-after in every case
		    this fold is correct in (no overlap) and deterministic
		    otherwise. The overlap and unaligned-copy divergences are
		    pre-existing and recorded in OUTSTANDING_BUGS.  */
		{
			uint32_t *pw = (uint32_t *)
			    (page_1 + (addr_r1 & 0xffc) + 16);
			cpu->cd.arm.r[3]      = pw[0];   /* +16 */
			cpu->cd.arm.r[4]      = pw[1];   /* +20 */
			cpu->cd.arm.r[ARM_IP] = pw[2];   /* +24  (r12) */
			cpu->cd.arm.r[ARM_LR] = pw[3];   /* +28  (r14) */
		}

		memcpy(page_0 + (addr_r0 & 0xfff),
		    page_1 + (addr_r1 & 0xfff), 32);
		cpu->cd.arm.r[0] = addr_r0 + 32;
		cpu->cd.arm.r[1] = addr_r1 + 32;
		n_iter ++;				/*  #358  */

		cpu->n_translated_instrs += 4;

		instr(subs)(cpu, ic + 4);
		cpu->n_translated_instrs ++;

		/*  Loop while greater or equal:  */
		cpu->n_translated_instrs ++;
	} while (((cpu->cd.arm.flags & ARM_F_N)?1:0) ==
	    ((cpu->cd.arm.flags & ARM_F_V)?1:0));

	/*  #358: normal exit -- summarise. Unguarded, because reaching here means
	    the loop body ran at least once (the bail-outs return early), so the
	    count is always >= 1.  */
	debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_memcpy",
	    VERBOSITY_DEBUG, "combined %u iterations", n_iter);

	/*  Continue at the instruction after the bge:  */
	cpu->cd.arm.next_ic = &ic[6];
	cpu->n_translated_instrs --;
}


/*
 *  netbsd_cacheclean:
 *
 *  The core of a NetBSD/arm cache clean routine, variant 1:
 *
 *  f015f88c:  e4902020     ldr     r2,[r0],#32
 *  f015f890:  e2511020     subs    r1,r1,#0x20
 *  f015f894:  1afffffc     bne     0xf015f88c
 *  f015f898:  ee070f9a     mcr     15,0,r0,cr7,cr10,4
 */
X(netbsd_cacheclean)
{
	uint32_t r1 = cpu->cd.arm.r[1];
	uint32_t n;

	/*  #350: a counter that is not a multiple of 32 never reaches zero,
	    so the real bne loop never exits -- the closed form below would
	    terminate a loop the architecture does not terminate. Fall back
	    to the genuine load handler (the netbsd_memcpy bail-out shape,
	    cf. :2028): r1 mod 32 is invariant under the loop's -0x20, so
	    every re-entry falls back too and the guest keeps its infinite
	    loop, its loads, its faults and its interruptibility. r1 == 0
	    stays folded: that loop terminates, after 2^27 iterations whose
	    2^32 bytes of base advance wrap r0 to itself.  */
	if (r1 & 0x1f) {
		instr(load_w0_word_u1_p0_imm)(cpu, ic);
		return;
	}

	n = r1 == 0 ? (uint32_t)1 << 27 : r1 >> 5;

	/*  #349: fold-fired marker. Once #348 made this fold write the
	    loop's true exit state, the genuine sequence became
	    architecturally transparent, so gate 14's fold detector reads
	    this DEBUG-gated line (and the stale r2, while the skipped load
	    stays unfixed). Deliberately NOT pre-gated with
	    ENOUGH_VERBOSITY(), per the #278 convention: a pre-gate would
	    hide it under -V step and keep `breakpoint subsystem cpu` from
	    firing here.  */
	debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_cacheclean",
	    VERBOSITY_DEBUG, "combined %u iterations", (unsigned) n);

	/*  #350: bill the skipped instructions against the batch budget,
	    CLAMPED to the room left. n*3 reaches 3*2^27, the limit is only
	    tested per dispatch group, and the r1 == 0 fold is a fixed point
	    (it leaves r1 == 0), so an unclamped add is guest-drivable into
	    signed overflow -- the #169 class, sharpened by this round. A
	    #169-style bail would disable the fold for every counter above
	    a few tens of KB, so the overshoot is dropped instead; only the
	    total instruction statistics under-count in that corner.  */
	{
		uint64_t add = (uint64_t) n * 3;
		int room = N_SAFE_DYNTRANS_LIMIT - cpu->n_translated_instrs;
		if (room > 0)
			cpu->n_translated_instrs +=
			    (add > (uint64_t) room) ? room : (int) add;
	}
	cpu->cd.arm.r[0] += r1;

	/*  #348: the loop ends on `subs r1,r1,#0x20` reaching zero, which
	    owes N/Z/C/V. Delegate the final subtraction to the real dpi
	    handler, the netbsd_memcpy fold's own pattern (:2048); ic here
	    is the LOAD slot, so &ic[1] is the subs the matcher pinned to
	    (r1, #0x20, r1). Every terminating counter's final operand is
	    0x20 -- nonzero multiples end 32 -> 0, and the r1 == 0 wrap
	    ends on the same operand -- so this leaves r1 = 0 with Z|C set
	    and N|V clear, exactly as the loop does.  */
	cpu->cd.arm.r[1] = 0x20;
	instr(subs)(cpu, &ic[1]);

	cpu->cd.arm.next_ic = &ic[4];
}


/*
 *  netbsd_cacheclean2:
 *
 *  The core of a NetBSD/arm cache clean routine, variant 2:
 *
 *  f015f93c:  ee070f3a     mcr     15,0,r0,cr7,cr10,1
 *  f015f940:  ee070f36     mcr     15,0,r0,cr7,cr6,1
 *  f015f944:  e2800020     add     r0,r0,#0x20
 *  f015f948:  e2511020     subs    r1,r1,#0x20
 *  f015f94c:  8afffffa     bhi     0xf015f93c
 */
X(netbsd_cacheclean2)
{
	/*
	 *  #347: this handler used to update NO GUEST REGISTERS AT ALL. It
	 *  advanced n_translated_instrs and jumped to ic[5], so the two MCRs,
	 *  the add, the subs and the branch were all skipped and every register
	 *  came out exactly as it went in. That is wrong even for the NetBSD
	 *  sequence above -- unlike variant 1, which at least performs
	 *  r[0] += r[1]; r[1] = 0. Measured on the committed build with the
	 *  two-pass free-running driver, r0 = 0x9100 and r1 = 0x40: the fold
	 *  returned r0 = 0x9100 and r1 = 0x40, where the identical program with
	 *  one MCR replaced by a nop -- so that nothing combines at all --
	 *  returns r0 = 0x9140 and r1 = 0.
	 *
	 *  The closed form is NOT variant 1's `r[0] += r[1]; r[1] = 0`. This
	 *  loop ends on `bhi`, which is C && !Z, so it exits either when the
	 *  subs reaches zero OR when the subs BORROWS, and that second exit is
	 *  the one taken by every counter that is not a nonzero multiple of 32.
	 *  The branch is also at the BOTTOM, so one iteration always runs and a
	 *  partial tail costs a whole extra one. Hence
	 *
	 *      n = (r1 == 0 || (r1 & 31) != 0)? (r1 >> 5) + 1 : (r1 >> 5)
	 *
	 *  which was checked against the un-combined loop for r1 = 0, 1, 0x1f,
	 *  0x20, 0x21, 0x30, 0x40, 0x60 and 0x7f and agrees on all nine.
	 *  `r[0] += r[1]; r[1] = 0` -- variant 1's form, and what the bug record
	 *  proposed -- agrees on THREE of those nine, 0x20, 0x40 and 0x60, the
	 *  only nonzero multiples of 32 in the set. r1 = 0x30 really leaves r0
	 *  advanced by 0x40 and r1 at 0xfffffff0, where that form gives 0x30 and
	 *  0; r1 = 0 really advances r0 by 0x20 and leaves r1 at 0xffffffe0,
	 *  where that form leaves r0 alone.
	 *
	 *  The wraparound is deliberate. At r1 = 0xffffffff, n is 0x8000000 and
	 *  n << 5 truncates to 0 -- which is exactly what advancing a 32-bit
	 *  register by 2^32 bytes does.
	 *
	 *  #348: the flags. The subs that ends the loop owes N/Z/C/V; the
	 *  final subtraction is delegated to the real dpi handler, the
	 *  netbsd_memcpy fold's own pattern (:2048). ic here is the FIRST
	 *  MCR slot, so &ic[3] is the subs the matcher pinned to
	 *  (r1, #0x20, r1). r1 is left at the final iteration's operand,
	 *  before_last = r1 - ((n-1) << 5), which lies in [0, 0x20] for
	 *  every uint32 counter (0 for r1 == 0; r1 & 31 for non-multiples;
	 *  0x20 for nonzero multiples), so the stored result is
	 *  byte-identical to the closed form above and V is structurally
	 *  0: a zero exit answers Z|C, a borrow exit answers N, both
	 *  measured against the un-combined loop.
	 *
	 *  #349: the marker. That delegation makes the genuine sequence
	 *  architecturally transparent folded or unfolded, so gate 14's
	 *  fold detector is this DEBUG-gated line -- the old control row
	 *  read the MISSING flags and was retired in the same change.
	 *  Deliberately NOT pre-gated with ENOUGH_VERBOSITY(), per the
	 *  #278 convention: a pre-gate would hide it under -V step and
	 *  keep `breakpoint subsystem cpu` from firing here.
	 */
	uint32_t r1 = cpu->cd.arm.r[1];
	uint32_t n = (r1 == 0 || (r1 & 31) != 0)? (r1 >> 5) + 1 : (r1 >> 5);

	debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_cacheclean2",
	    VERBOSITY_DEBUG, "combined %u iterations", (unsigned) n);

	/*  #350: clamped for the same reason as netbsd_cacheclean above --
	    (n*5)-1 reaches ~5*2^27 and the batch limit is only tested per
	    dispatch group.  */
	{
		uint64_t add = (uint64_t) n * 5 - 1;
		int room = N_SAFE_DYNTRANS_LIMIT - cpu->n_translated_instrs;
		if (room > 0)
			cpu->n_translated_instrs +=
			    (add > (uint64_t) room) ? room : (int) add;
	}
	cpu->cd.arm.r[0] += n << 5;
	cpu->cd.arm.r[1] = r1 - ((n - 1) << 5);
	instr(subs)(cpu, &ic[3]);
	cpu->cd.arm.next_ic = &ic[5];
}


/*
 *  netbsd_scanc:
 *
 *  f01bccbc:  e5d13000     ldrb    r3,[r1]
 *  f01bccc0:  e7d23003     ldrb    r3,[r2,r3]
 *  f01bccc4:  e113000c     tsts    r3,ip
 */
X(netbsd_scanc)
{
	unsigned char *page = cpu->cd.arm.host_load[cpu->cd.arm.r[1] >> 12];
	uint32_t t;

	/*
	 *  #361: name the reason this fold declined, in the SAME expression the
	 *  guard tests -- the #360 shape. Unlike copyin/copyout, the two bail-outs
	 *  CANNOT share one `why` chain: the second tests a page derived from the
	 *  byte the first bail-out proves unreadable, so the reasons must be
	 *  printed at their own guards, in order. The text avoids the word
	 *  "combined" because the probes count fires by matching "<name>:
	 *  combined"; the two reasons are also spelled differently so a row can
	 *  tell WHICH page missed.
	 */
	if (page == NULL) {
		debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_scanc", VERBOSITY_DEBUG,
		    "declined (str-no-page) r1=0x%x", (unsigned) cpu->cd.arm.r[1]);
		instr(load_w0_byte_u1_p1_imm)(cpu, ic);
		return;
	}

	t = page[cpu->cd.arm.r[1] & 0xfff];
	t += cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_load[t >> 12];

	if (page == NULL) {
		debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_scanc", VERBOSITY_DEBUG,
		    "declined (tbl-no-page) t=0x%x", (unsigned) t);
		instr(load_w0_byte_u1_p1_imm)(cpu, ic);
		return;
	}

	/*  #358: fold-fired marker. Transparent otherwise -- byte loads need no
	    mask, N is cleared and never set (correct only because r3 holds a
	    freshly loaded BYTE, so r3 & ip <= 255), C is left alone (correct
	    because the register form of TST takes no shifter-carry path), and the
	    billing is 2 + 1 for the 3 instructions replaced.

	    After BOTH bail-outs, and that placement is the one a plausible-looking
	    patch gets wrong: the second miss is reachable after the first passes,
	    because the table address `t` is computed from the byte just loaded, so
	    a marker between them would fire on a call that wrote no guest state.
	    Both bail-outs are host-page misses, not a "character found" exit, so
	    neither is a legitimate fold completion.  */
	debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_scanc",
	    VERBOSITY_DEBUG, "combined 3 instrs");

	cpu->cd.arm.r[3] = page[t & 0xfff];

	t = cpu->cd.arm.r[3] & cpu->cd.arm.r[ARM_IP];
	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N);
	if (t == 0)
		cpu->cd.arm.flags |= ARM_F_Z;

	cpu->n_translated_instrs += 2;
	cpu->cd.arm.next_ic = &ic[3];
}


/*
 *  netbsd_idle:
 *
 *  L:	ldr     rX,[rY]
 *	teqs    rX,#0
 *	bne     X (samepage)
 *	teqs    rZ,#0
 *	beq     L (samepage)
 *	....
 *	X:  somewhere else on the same page
 */
X(netbsd_idle)
{
	uint32_t rY = reg(ic[0].arg[0]);
	uint32_t *p;
	uint32_t rX;

	p = (uint32_t *) cpu->cd.arm.host_load[rY >> 12];
	if (p == NULL) {
		instr(load_w0_word_u1_p1_imm)(cpu, ic);
		return;
	}

	rX = p[(rY & 0xfff) >> 2];
	/*  No need to convert endianness, since it's only a 0-test.  */

	/*  This makes execution continue on the first teqs instruction,
	    which is fine.  */
	if (rX != 0) {
		instr(load_w0_word_u1_p1_imm)(cpu, ic);
		return;
	}

	/*  #351: both fast paths below are reached only with rX == 0, and the
	    loop they stand in for executes `ldr rX,[rY]` (writing rX) and
	    `teqs rZ,#0` (writing N/Z) before either exit -- the fold wrote
	    NEITHER, so the guest read a stale destination and stale flags.
	    Measured on the committed build via translation read-ahead (which
	    installs the fold before the ldr ever runs, so the destination is
	    whatever it held on entry): the rZ != 0 exit returned dest = seed
	    and NZCV = seed where the loop owes dest = 0 and the second teqs's
	    flags.

	    Write the destination FIRST, then delegate the second teqs to the
	    real dpi handler at its matcher-pinned slot (the netbsd_memcpy
	    fold's own pattern). Writing dest first is load-bearing: it makes a
	    loop whose second teqs ALIASES the load destination (the matcher
	    pins rZ != rY but not rZ != rX) read the freshly-written 0 and idle
	    correctly, instead of reading the stale register and wrongly exiting.
	    The store of rX is safe ONLY because rX is provably 0 here -- it is the
	    raw host word from the inline 0-test read above, which skips byte-swap
	    precisely because a 0-test needs none. The rX != 0 case never reaches
	    this store: it falls back to instr(load_w0_word_u1_p1_imm), the real
	    load that DOES byte-swap. So do not reuse this store for a future
	    non-zero fast path without byte-swapping first.

	    Call instr(teqs) BY NAME, never ic[3].f: this same combiner rewrote
	    ic[3] to teqs_beq_samepage (the beq folded its predecessor), whose
	    handler would branch instead of computing flags.  */
	reg(ic[0].arg[2]) = rX;
	instr(teqs)(cpu, &ic[3]);

	if (cpu->cd.arm.flags & ARM_F_Z) {
		/*  Synch the program counter.  The teqs delegation ran BEFORE
		    this handoff, so the flags an interrupt banks into SPSR are
		    the architectural post-teqs value.  */
		uint32_t low_pc = ((size_t)ic - (size_t)
		    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
		cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1)
		    << ARM_INSTR_ALIGNMENT_SHIFT);
		cpu->pc += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);

		cpu->wants_to_idle = true;
		/*  Idle-path billing is deliberately just N_DYNTRANS_IDLE_BREAK,
		    NOT the exit path's `+= 4`: this is the batch-break the other
		    architectures' idle combiners also use, subtracted back when
		    the machine actually idles (cpu_dyntrans.c), and per-instruction
		    rate accounting is meaningless while idling. The asymmetry with
		    the exit path is intended.  */
		cpu->n_translated_instrs += N_DYNTRANS_IDLE_BREAK;
		cpu->cd.arm.next_ic = &nothing_call;
		return;
	}

	/*  #352: fold-fired marker on the EXIT path only. This path became
	    architecturally transparent once #351 wrote the dest and flags, so
	    the marker is gate 14's fold-fired detector here. The idle path is
	    deliberately NOT marked: it re-enters ~2000x/s while the guest
	    idles (a flood), and it needs no marker -- `wants_to_idle` is the
	    only ARM setter of that flag, so it is already a fold detector.
	    Not pre-gated with ENOUGH_VERBOSITY(), per the #278 convention, so
	    `breakpoint subsystem cpu` can catch a fold in flight.
	    #351: the exit stands in for five architectural instructions and
	    billed none; owe the other four.  */
	debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_idle", VERBOSITY_DEBUG,
	    "combined idle-loop exit");
	cpu->n_translated_instrs += 4;
	cpu->cd.arm.next_ic = &ic[5];
}


/*
 *  strlen:
 *
 *  S: e5f03001   ldrb  rY,[rX,#1]!
 *     e3530000   cmps  rY,#0
 *     1afffffc   bne   S
 */
X(strlen)
{
	unsigned int n_loops = 0;
	uint32_t rY, rX = reg(ic[0].arg[0]);
	unsigned char *p;
	/*
	 *  #356: the walk used to run to the end of the string with no bound,
	 *  inside ONE dispatch. Two consequences, the second measured:
	 *
	 *  - The host is unresponsive for the duration: ^C, the console and the
	 *    debugger are only polled between dispatch groups, so a multi-KB
	 *    walk is unbreakable while it runs, and the emulated
	 *    instructions-per-tick ratio is distorted by up to ~6000x for that
	 *    call. (No tick is SKIPPED -- machine_run decrements by a constant
	 *    and discards run_instr's return -- so the earlier "no device
	 *    ticks" wording was wrong.)
	 *  - n_translated_instrs is an int, reset once per run_instr, not per
	 *    fold entry, and this walk is REPLAYABLE: measured, twenty
	 *    back-to-back walks accumulated 983,080 instructions into one int
	 *    with no group boundary. So the signed overflow needs only ~18-24
	 *    MB of non-NUL memory at the DEFAULT -M 64 -- from a ~6-instruction
	 *    guest program, in seconds -- not the ~700 MB a per-entry reading
	 *    suggests. Past overflow the `>= N_SAFE_DYNTRANS_LIMIT` test fails
	 *    on a negative value, cpu->ninstrs can run BACKWARDS (guest-visible
	 *    through the test machine's MP cycle register), and the arithmetic
	 *    is UB under this project's own sanitizer sweeps.
	 *
	 *  The budget test is at the BOTTOM of the do-while, which structurally
	 *  guarantees at least one completed iteration. That is load-bearing,
	 *  not stylistic: `if (room <= 0) return;` at the top would skip the
	 *  ldrb and still fall through to the genuine cmps (the dispatcher
	 *  POST-increments next_ic, so an untouched return resumes at ic[1]),
	 *  and a guest arriving with r3 == 0 would then take the not-taken bne
	 *  and leave its loop having never loaded a byte -- a new divergence of
	 *  exactly the class this round is fixing. room <= 0 at entry is
	 *  reachable, and the dominant producer is THIS FOLD'S OWN previous
	 *  yield inside the same group: the first entry eats the whole budget,
	 *  and the remaining dispatches of that group of 120 re-enter with
	 *  nothing left. (The group's +120 lands AFTER the group, so it alone
	 *  always leaves room >= 1 at a group start; a sibling fold such as
	 *  netbsd_idle, which adds N_DYNTRANS_IDLE_BREAK == the whole limit,
	 *  is the other producer.) Consequence worth knowing: once the budget
	 *  is gone the rest of the group advances one byte per dispatch, so a
	 *  long walk moves ~2850 bytes per batch rather than 2731 and ~4% of
	 *  its dispatches are near-empty. Progress is still guaranteed.
	 *
	 *  Because the loop is bounded, n_loops * 3 <= room + 2 <= 8193 and
	 *  neither the unsigned wrap nor the signed conversion is reachable any
	 *  more -- the bound SUBSUMES a #350-style min(add, room) clamp, so
	 *  only one of the two is shipped. The (int) cast in the condition is
	 *  kept regardless: without it a negative room would promote to ~4
	 *  billion and the bound would silently vanish.
	 */
	int room = N_SAFE_DYNTRANS_LIMIT - cpu->n_translated_instrs;

	do {
		rX ++;
		p = cpu->cd.arm.host_load[rX >> 12];
		if (p == NULL) {
			cpu->n_translated_instrs += (n_loops * 3);
			instr(load_w1_byte_u1_p1_imm)(cpu, ic);
			return;
		}

		rY = reg(ic[0].arg[2]) = p[rX & 0xfff];	/*  load  */
		reg(ic[0].arg[0]) = rX;			/*  writeback  */
		n_loops ++;

		/*  Compare rY to zero:  */
		cpu->cd.arm.flags = ARM_F_C;
		if (rY == 0)
			cpu->cd.arm.flags |= ARM_F_Z;
	} while (rY != 0 && (int) (n_loops * 3) < room);

	cpu->n_translated_instrs += (n_loops * 3) - 1;

	if (rY != 0) {
		/*
		 *  #356: budget exhausted mid-walk. Yield to the dispatcher so
		 *  the group can end, the host can breathe and the batch limit
		 *  can be tested; then re-enter here. next_ic = &ic[0] is what
		 *  the guest's own taken `bne` would do, and it keeps the
		 *  billing identical to the normal exit (3n-1 owed plus the
		 *  dispatcher's 1 for this call = 3n exactly). Falling through
		 *  instead would re-execute the genuine cmps and bne and owe
		 *  3n-3, i.e. a second accounting constant for no gain.
		 *
		 *  Every entry completes at least one iteration, so this cannot
		 *  spin without advancing, and the yielded state -- r3 = the
		 *  last byte (nonzero), the base at its address, flags C set
		 *  with Z clear -- is exactly the state the genuine loop is in
		 *  after a taken bne, so an interrupt at the group boundary sees
		 *  an architecturally reachable machine.
		 *
		 *  The marker corroborates the yield (the round's hard witness
		 *  is the test machine's cycle counter, which needs no marker)
		 *  and is deliberately NOT pre-gated with ENOUGH_VERBOSITY(),
		 *  per the #278 convention, so `breakpoint subsystem cpu`
		 *  catches a yield in flight. The `n_loops > 1` guard is what
		 *  makes "only on a long walk" TRUE: without it a SHORT,
		 *  ordinary strlen dispatched into a group whose budget sibling
		 *  folds had already exhausted would fire a one-byte marker on
		 *  each of up to a group's worth of dispatches. Every genuinely
		 *  long walk still fires at least one big-chunk line.
		 */
		if (n_loops > 1)
			debugmsg_cpu(cpu, SUBSYS_CPU, "strlen", VERBOSITY_DEBUG,
			    "yielded after %u bytes", n_loops);
		cpu->cd.arm.next_ic = &ic[0];
		return;
	}

	cpu->cd.arm.next_ic = &ic[3];
}


/*
 *  xchg:
 *
 *  e02YX00X     eor     rX,rY,rX
 *  e02XY00Y     eor     rY,rX,rY
 *  e02YX00X     eor     rX,rY,rX
 */
X(xchg)
{
	uint32_t tmp = reg(ic[0].arg[0]);

	/*  #358: fold-fired marker. No bail-out, so anywhere in the body is
	    exact. Transparent otherwise: eor_regshort is the S == 0 table entry so
	    no flags are touched, and the billing is 2 + 1 for the three EORs
	    replaced. Post-#342's `a != b` guard the fold and three real EORs are
	    indistinguishable in every register and flag, which is what left the
	    gate's own two swap rows unable -- by its own admission -- to tell
	    folded-and-correct from not-folded-and-correct.  */
	debugmsg_cpu(cpu, SUBSYS_CPU, "xchg",
	    VERBOSITY_DEBUG, "combined 3 eors");

	cpu->n_translated_instrs += 2;
	cpu->cd.arm.next_ic = &ic[3];
	reg(ic[0].arg[0]) = reg(ic[1].arg[0]);
	reg(ic[1].arg[0]) = tmp;
}


/*
 *  netbsd_copyin:
 *
 *  e4b0a004     ldrt    sl,[r0],#4
 *  e4b0b004     ldrt    fp,[r0],#4
 *  e4b06004     ldrt    r6,[r0],#4
 *  e4b07004     ldrt    r7,[r0],#4
 *  e4b08004     ldrt    r8,[r0],#4
 *  e4b09004     ldrt    r9,[r0],#4
 */
X(netbsd_copyin)
{
	uint32_t r0 = cpu->cd.arm.r[0], ofs = (r0 & 0xffc), index = r0 >> 12;
	unsigned char *p = cpu->cd.arm.host_load[index];
	uint32_t *p32 = (uint32_t *) p, *q32;
	int ok = cpu->cd.arm.is_userpage[index >> 5] & (1 << (index & 31));

	/*
	 *  #360: name the reason this fold declined, in the SAME expression the
	 *  guard tests, so the diagnosis cannot drift away from the condition it
	 *  describes. Duplicating the three terms in a separate print would be a
	 *  second thing to keep in sync; a short-circuit chain evaluated once
	 *  cannot disagree with itself.
	 *
	 *  Why a bail marker at all: with only the #358 fire marker, a red row is
	 *  ambiguous between causes that need different fixes. Adding this one and
	 *  the install marker in COMBINE() below makes the triple readable in one
	 *  look -- install 1 / fire 1 / bail 0 is healthy; install 1 / fire 0 /
	 *  bail 1 means the fold was reached and DECLINED, and the text says which
	 *  clause; install 1 / fire 0 / bail 0 means the slot was never dispatched
	 *  (a misplaced breakpoint); install 0 means the matcher declined -- or the
	 *  session itself broke, which is why every row also asserts the verbosity
	 *  echo and a value witness.
	 *
	 *  The text deliberately avoids the word "combined": the probes count fire
	 *  markers by matching "<name>: combined", and a bail line containing it
	 *  would be tallied as a fold that fired.
	 */
	const char *why = ofs > 0x1000 - 6*4 ? "page-end" :
	    !ok ? "not-user" : p == NULL ? "no-page" : NULL;

	if (why != NULL) {
		debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_copyin", VERBOSITY_DEBUG,
		    "declined (%s) ofs=0x%x user=%d", why, (unsigned) ofs,
		    ok ? 1 : 0);
		instr(load_w1_word_u1_p0_imm)(cpu, ic);
		return;
	}

	/*
	 *  #358: fold-fired marker. This fold is otherwise UNOBSERVABLE: its
	 *  registers, the addresses it reads and its instruction billing are all
	 *  identical to the six genuine ldrt's, so a harness row asserting its
	 *  result passes whether or not the fold ever fires. #357 removed the one
	 *  witness that existed -- before it, the template masked its base
	 *  writeback while this fold did not, so an unaligned base gave r0 =
	 *  0x10019 folded against 0x10018 genuine. That one-bit difference was
	 *  the detector; now both paths agree, and any row asserting "the fold
	 *  fired" is unsatisfiable without this line.
	 *
	 *  Placed AFTER the bail-out on purpose. The bail-out delegates the first
	 *  ldrt to the genuine handler and returns without setting next_ic, so
	 *  the remaining five run genuinely too; a marker before it would report
	 *  a fold that did no folding. Not pre-gated with ENOUGH_VERBOSITY(), per
	 *  the #278 convention, so `breakpoint subsystem cpu` catches a fold in
	 *  flight -- which is also why a static first-N latch was rejected here:
	 *  it would gate the breakpoint path too and kill that capability after
	 *  N folds. This fold has no internal loop, so there is nothing to
	 *  summarise and no information-content guard analogous to strlen's
	 *  `n_loops > 1`; the volume is accepted and the rows copy blocks, not
	 *  megabytes.
	 */
	debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_copyin",
	    VERBOSITY_DEBUG, "combined 6 loads");

	q32 = &cpu->cd.arm.r[6];
	ofs >>= 2;
	q32[0] = p32[ofs+2];
	q32[1] = p32[ofs+3];
	q32[2] = p32[ofs+4];
	q32[3] = p32[ofs+5];
	q32[4] = p32[ofs+0];
	q32[5] = p32[ofs+1];
	cpu->cd.arm.r[0] = r0 + 24;
	cpu->n_translated_instrs += 5;
	cpu->cd.arm.next_ic = &ic[6];
}


/*
 *  netbsd_copyout:
 *
 *  e4a18004     strt    r8,[r1],#4
 *  e4a19004     strt    r9,[r1],#4
 *  e4a1a004     strt    sl,[r1],#4
 *  e4a1b004     strt    fp,[r1],#4
 *  e4a16004     strt    r6,[r1],#4
 *  e4a17004     strt    r7,[r1],#4
 */
X(netbsd_copyout)
{
	uint32_t r1 = cpu->cd.arm.r[1], ofs = (r1 & 0xffc), index = r1 >> 12;
	unsigned char *p = cpu->cd.arm.host_store[index];
	uint32_t *p32 = (uint32_t *) p, *q32;
	int ok = cpu->cd.arm.is_userpage[index >> 5] & (1 << (index & 31));

	/*  #360: see X(netbsd_copyin) above for why the reason is computed in the
	    guard's own short-circuit and why the text avoids "combined". Note this
	    fold reads host_STORE, so "no-page" here means the destination page has
	    never been written -- a load-only warm-up leaves it NULL and this fold
	    declines, which is why a copyout row's warm-up must be a store.  */
	const char *why = ofs > 0x1000 - 6*4 ? "page-end" :
	    !ok ? "not-user" : p == NULL ? "no-page" : NULL;

	if (why != NULL) {
		debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_copyout", VERBOSITY_DEBUG,
		    "declined (%s) ofs=0x%x user=%d", why, (unsigned) ofs,
		    ok ? 1 : 0);
		instr(store_w1_word_u1_p0_imm)(cpu, ic);
		return;
	}

	/*  #358: fold-fired marker -- see X(netbsd_copyin) above for why this
	    fold is otherwise unobservable and why the marker sits after the
	    bail-out rather than before it.  */
	debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_copyout",
	    VERBOSITY_DEBUG, "combined 6 stores");

	q32 = &cpu->cd.arm.r[6];
	ofs >>= 2;
	p32[ofs  ] = q32[2];
	p32[ofs+1] = q32[3];
	p32[ofs+2] = q32[4];
	p32[ofs+3] = q32[5];
	p32[ofs+4] = q32[0];
	p32[ofs+5] = q32[1];
	cpu->cd.arm.r[1] = r1 + 24;
	cpu->n_translated_instrs += 5;
	cpu->cd.arm.next_ic = &ic[6];
}


/*
 *  cmps by 0, followed by beq (inside the same page):
 */
X(cmps0_beq_samepage)
{
	uint32_t a = reg(ic->arg[0]);
	cpu->n_translated_instrs ++;
	if (a == 0) {
		cpu->cd.arm.flags = ARM_F_Z | ARM_F_C;
	} else {
		/*  Semi-ugly hack which sets the negative-bit if a < 0:  */
		cpu->cd.arm.flags = ARM_F_C | ((a >> 28) & 8);
	}
	if (a == 0)
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
	else
		cpu->cd.arm.next_ic = &ic[2];
}


/*
 *  cmps followed by beq (inside the same page):
 */
X(cmps_beq_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if (c == 0) {
		cpu->cd.arm.flags |= ARM_F_Z;
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
	} else {
		cpu->cd.arm.next_ic = &ic[2];
		if (c & 0x80000000)
			cpu->cd.arm.flags |= ARM_F_N;
	}
}


/*
 *  cmps followed by beq (not the same page):
 */
X(cmps_0_beq)
{
	uint32_t a = reg(ic->arg[0]);
	cpu->n_translated_instrs ++;
	if (a == 0) {
		cpu->cd.arm.flags = ARM_F_Z | ARM_F_C;
		cpu->pc = (uint32_t)(((uint32_t)cpu->pc & 0xfffff000)
		    + (int32_t)ic[1].arg[0]);
		quick_pc_to_pointers_arm(cpu);
	} else {
		/*  Semi-ugly hack which sets the negative-bit if a < 0:  */
		cpu->cd.arm.flags = ARM_F_C | ((a >> 28) & 8);
		cpu->cd.arm.next_ic = &ic[2];
	}
}
X(cmps_pos_beq)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if ((int32_t)a < 0 && (int32_t)c >= 0)
		cpu->cd.arm.flags |= ARM_F_V;
	if (c == 0) {
		cpu->cd.arm.flags |= ARM_F_Z;
		cpu->pc = (uint32_t)(((uint32_t)cpu->pc & 0xfffff000)
		    + (int32_t)ic[1].arg[0]);
		quick_pc_to_pointers_arm(cpu);
	} else {
		cpu->cd.arm.next_ic = &ic[2];
		if (c & 0x80000000)
			cpu->cd.arm.flags |= ARM_F_N;
	}
}
X(cmps_neg_beq)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if ((int32_t)a >= 0 && (int32_t)c < 0)
		cpu->cd.arm.flags |= ARM_F_V;
	if (c == 0) {
		cpu->cd.arm.flags |= ARM_F_Z;
		cpu->pc = (uint32_t)(((uint32_t)cpu->pc & 0xfffff000)
		    + (int32_t)ic[1].arg[0]);
		quick_pc_to_pointers_arm(cpu);
	} else {
		cpu->cd.arm.next_ic = &ic[2];
		if (c & 0x80000000)
			cpu->cd.arm.flags |= ARM_F_N;
	}
}


/*
 *  cmps by 0, followed by bne (inside the same page):
 */
X(cmps0_bne_samepage)
{
	uint32_t a = reg(ic->arg[0]);
	cpu->n_translated_instrs ++;
	if (a == 0) {
		cpu->cd.arm.flags = ARM_F_Z | ARM_F_C;
	} else {
		/*  Semi-ugly hack which sets the negative-bit if a < 0:  */
		cpu->cd.arm.flags = ARM_F_C | ((a >> 28) & 8);
	}
	if (a == 0)
		cpu->cd.arm.next_ic = &ic[2];
	else
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
}


/*
 *  cmps followed by bne (inside the same page):
 */
X(cmps_bne_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if (c == 0) {
		cpu->cd.arm.flags |= ARM_F_Z;
		cpu->cd.arm.next_ic = &ic[2];
	} else {
		if (c & 0x80000000)
			cpu->cd.arm.flags |= ARM_F_N;
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
	}
}


/*
 *  cmps followed by bcc (inside the same page):
 */
X(cmps_bcc_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (c & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
	else if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if (a >= b)
		cpu->cd.arm.next_ic = &ic[2];
	else
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
}


/*
 *  cmps (reg) followed by bcc (inside the same page):
 */
X(cmps_reg_bcc_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]), c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (c & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
	else if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if (a >= b)
		cpu->cd.arm.next_ic = &ic[2];
	else
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
}


/*
 *  cmps followed by bhi (inside the same page):
 */
X(cmps_bhi_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (c & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
	else if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if (a > b)
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
	else
		cpu->cd.arm.next_ic = &ic[2];
}


/*
 *  cmps (reg) followed by bhi (inside the same page):
 */
X(cmps_reg_bhi_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]), c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (c & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
	else if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if (a > b)
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
	else
		cpu->cd.arm.next_ic = &ic[2];
}


/*
 *  cmps followed by bgt (inside the same page):
 */
X(cmps_bgt_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (c & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
	else if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if ((int32_t)a > (int32_t)b)
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
	else
		cpu->cd.arm.next_ic = &ic[2];
}


/*
 *  cmps followed by ble (inside the same page):
 */
X(cmps_ble_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a - b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags = ((uint32_t)a >= (uint32_t)b)? ARM_F_C : 0;
	if (c & 0x80000000)
		cpu->cd.arm.flags |= ARM_F_N;
	else if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (((int32_t)a >= 0 && (int32_t)b < 0 && (int32_t)c < 0) ||
	    ((int32_t)a < 0 && (int32_t)b >= 0 && (int32_t)c >= 0))
		cpu->cd.arm.flags |= ARM_F_V;
	if ((int32_t)a <= (int32_t)b)
		cpu->cd.arm.next_ic = (struct arm_instr_call *) ic[1].arg[0];
	else
		cpu->cd.arm.next_ic = &ic[2];
}


/*
 *  teqs followed by beq (inside the same page):
 */

/*
 *  arm_combined_shifter_carry():  #340
 *
 *  The shifter carry-out that the STANDALONE teqs/tsts perform and the
 *  *_samepage handlers did not. For a data-processing IMMEDIATE with the S bit
 *  set, ARM sets C from bit 31 of the rotated immediate, and the test used is
 *  "is the EXPANDED OPERAND > 255?". In the dpi template that is a documented
 *  approximation, because a nonzero rotation can still expand to a small value.
 *  Here it is EXACT, and a review seat established why: the decoder routes that
 *  ambiguous case -- nonzero rotation whose expanded value is under 256 -- to
 *  dpis_imm_rotc, which clears C explicitly, so no such instruction is ever
 *  eligible for teqs/tsts folding in the first place. What matters here is that
 *  FOLDING A COMPARE INTO A BRANCH
 *  MUST NOT CHANGE THE FLAGS, and it did: the teqs combiner has no operand
 *  guard at all, and the tsts one guards only bit 31 -- which is about N, since
 *  with the top bit clear a & b cannot be negative, not about C.
 *
 *  Measured with a two-pass free-running probe, because nothing else can see
 *  it: combining is disabled under single-step, and the combiner rewrites the
 *  PREVIOUS instruction while the branch is translated, so the folded handler
 *  first executes on the second pass over the loop. Committed build answered
 *  C=1 (untouched) where the standalone path answered C=0.
 */
#ifndef ARM_COMBINED_SHIFTER_CARRY_INCLUDED
#define ARM_COMBINED_SHIFTER_CARRY_INCLUDED
static void arm_combined_shifter_carry(struct cpu *cpu, uint32_t b)
{
	if (b > 255) {
		if (b & 0x80000000)
			cpu->cd.arm.flags |= ARM_F_C;
		else
			cpu->cd.arm.flags &= ~ARM_F_C;
	}
}
#endif

X(teqs_beq_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a ^ b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N);
	arm_combined_shifter_carry(cpu, ic->arg[1]);
	if (c == 0) {
		cpu->cd.arm.flags |= ARM_F_Z;
		cpu->cd.arm.next_ic = (struct arm_instr_call *)
		    ic[1].arg[0];
	} else {
		if (c & 0x80000000)
			cpu->cd.arm.flags |= ARM_F_N;
		cpu->cd.arm.next_ic = &ic[2];
	}
}


/*
 *  tsts followed by beq (inside the same page):
 *  (arg[1] must not have its highest bit set))
 */
X(tsts_lo_beq_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a & b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N);
	arm_combined_shifter_carry(cpu, ic->arg[1]);
	if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (c == 0)
		cpu->cd.arm.next_ic = (struct arm_instr_call *)
		    ic[1].arg[0];
	else
		cpu->cd.arm.next_ic = &ic[2];
}


/*
 *  teqs followed by bne (inside the same page):
 */
X(teqs_bne_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a ^ b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N);
	arm_combined_shifter_carry(cpu, ic->arg[1]);
	if (c == 0) {
		cpu->cd.arm.flags |= ARM_F_Z;
	} else {
		if (c & 0x80000000)
			cpu->cd.arm.flags |= ARM_F_N;
	}
	if (c == 0)
		cpu->cd.arm.next_ic = &ic[2];
	else
		cpu->cd.arm.next_ic = (struct arm_instr_call *)
		    ic[1].arg[0];
}


/*
 *  tsts followed by bne (inside the same page):
 *  (arg[1] must not have its highest bit set))
 */
X(tsts_lo_bne_samepage)
{
	uint32_t a = reg(ic->arg[0]), b = ic->arg[1], c = a & b;
	cpu->n_translated_instrs ++;
	cpu->cd.arm.flags &= ~(ARM_F_Z | ARM_F_N);
	arm_combined_shifter_carry(cpu, ic->arg[1]);
	if (c == 0)
		cpu->cd.arm.flags |= ARM_F_Z;
	if (c == 0)
		cpu->cd.arm.next_ic = &ic[2];
	else
		cpu->cd.arm.next_ic = (struct arm_instr_call *)
		    ic[1].arg[0];
}


/*****************************************************************************/


X(end_of_page)
{
	/*  Update the PC:  (offset 0, but on the next page)  */
	cpu->pc &= ~((ARM_IC_ENTRIES_PER_PAGE-1) << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (ARM_IC_ENTRIES_PER_PAGE << ARM_INSTR_ALIGNMENT_SHIFT);

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers_arm(cpu);

	/*  end_of_page doesn't count as an executed instruction:  */
	cpu->n_translated_instrs --;
}


/*****************************************************************************/


/*
 *  Combine: netbsd_memset():
 *
 *  Check for the core of a NetBSD/arm memset; large memsets use a sequence
 *  of 16 store-multiple instructions, each storing 2 registers at a time.
 */
void COMBINE(netbsd_memset)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
#ifdef HOST_LITTLE_ENDIAN
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back >= 17) {
		int i;
		for (i=-16; i<=-1; i++)
			if (ic[i].f != instr(multi_0x08ac000c__ge))
				return;
		if (ic[-17].f == instr(subs) &&
		    ic[-17].arg[0]==ic[-17].arg[2] && ic[-17].arg[1] == 128 &&
		    ic[ 0].f == instr(b_samepage__gt) &&
		    ic[ 0].arg[0] == (size_t)&ic[-17]) {
			ic[-17].f = instr(netbsd_memset);
		}
	}
#endif
}


/*
 *  Combine: netbsd_memcpy():
 *
 *  Check for the core of a NetBSD/arm memcpy; large memcpys use a
 *  sequence of ldmia instructions.
 */
void COMBINE(netbsd_memcpy)(struct cpu *cpu, struct arm_instr_call *ic,
	int low_addr)
{
#ifdef HOST_LITTLE_ENDIAN
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back >= 5) {
		if (ic[-5].f==instr(multi_0x08b15018) &&
		    ic[-4].f==instr(multi_0x08a05018) &&
		    ic[-3].f==instr(multi_0x08b15018) &&
		    ic[-2].f==instr(multi_0x08a05018) &&
		    ic[-1].f == instr(subs) &&
		    ic[-1].arg[0]==ic[-1].arg[2] && ic[-1].arg[1] == 0x20 &&
		    ic[ 0].f == instr(b_samepage__ge) &&
		    ic[ 0].arg[0] == (size_t)&ic[-5]) {
			ic[-5].f = instr(netbsd_memcpy);
		}
	}
#endif
}


/*
 *  Combine: netbsd_cacheclean():
 *
 *  Check for the core of a NetBSD/arm cache clean. (There are two variants.)
 */
void COMBINE(netbsd_cacheclean)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back >= 3) {
		/*  #345: the register checks are REQUIRED, and their absence was
		    guest-visible. This matcher tested the SHAPE of the loop -- a
		    post-indexed word load, `subs rX,rX,#32`, a branch back -- and
		    never which registers it used, while X(netbsd_cacheclean)
		    hardcodes `r[0] += r[1]; r[1] = 0`. A loop built on any other
		    pair therefore had r0 and r1 clobbered and its own registers
		    left stale. Measured with a two-pass free-running probe on a
		    loop using r5 and r6: r0 came back 0x33 for a seeded 0x11 (it
		    had been given r1's 0x22) and r1 came back 0. Same species as
		    #342's missing `a != b`, and worse in consequence -- that one
		    needed a degenerate encoding, this one fires on ordinary code
		    that merely happens to match the shape.  */
		/*  #346: #345 checked the two registers the handler WRITES and
		    stopped there; the load's own two remaining operands were
		    still unchecked, and the first of them is a stride. The
		    closed form `r[0] += r[1]` is arithmetic that is only true
		    when each iteration advances the base by 32, so the load's
		    post-index immediate is part of the contract, not decoration.
		    Measured on the committed build with the two-pass driver, on
		    `ldr r2,[r0],#4 / subs r1,r1,#32 / bne / mcr`: r0 came back
		    0x9120 where the architecture -- the identical program with
		    the MCR replaced by a nop, so nothing combines -- returns
		    0x9104. Eight times the real advance, from a loop a compiler
		    can emit. arg[2] is checked for the same reason the base is:
		    the handler never writes the load's destination, so a fold
		    that fires on any other Rd strands that register too; pinning
		    it to r2 confines the stale value to the one register the
		    NetBSD sequence above uses. That staleness is NOT fixed here
		    -- see OUTSTANDING_BUGS -- only its blast radius.  */
		if (ic[-3].f==instr(load_w0_word_u1_p0_imm) &&
		    ic[-3].arg[0] == (size_t)(&cpu->cd.arm.r[0]) &&
		    ic[-3].arg[1] == 0x20 &&
		    ic[-3].arg[2] == (size_t)(&cpu->cd.arm.r[2]) &&
		    ic[-2].f == instr(subs) &&
		    ic[-2].arg[0] == (size_t)(&cpu->cd.arm.r[1]) &&
		    ic[-2].arg[0]==ic[-2].arg[2] && ic[-2].arg[1] == 0x20 &&
		    ic[-1].f == instr(b_samepage__ne) &&
		    ic[-1].arg[0] == (size_t)&ic[-3]) {
			ic[-3].f = instr(netbsd_cacheclean);
		}
	}
}


/*
 *  Combine: netbsd_cacheclean2():
 *
 *  Check for the core of a NetBSD/arm cache clean. (Second variant.)
 */
void COMBINE(netbsd_cacheclean2)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back >= 4) {
		/*  #347: the register checks are REQUIRED, for the same reason
		    they were in COMBINE(netbsd_cacheclean) above -- and unlike
		    netbsd_memset, whose operands turned out to be pinned already
		    by the exact iwords its matcher demands, these two really are
		    free. instr(add) and instr(subs) are the GENERIC dpi table
		    entries (arm_dpi_instr[], cpu_arm_instr_dpi.c:72-74:
		    arg[0] = &Rn, arg[1] = immediate, arg[2] = &Rd), so
		    `add rX,rX,#32` and `subs rY,rY,#32` select them for ANY X
		    and Y, and this matcher tested only that each had rn == rd
		    and an immediate of 32.

		    That r0 and r1 are the right registers to demand is not a
		    convention: the two MCRs are pinned by exact iword and both
		    name Rd = r0, so the address the cache ops walk IS r0, and a
		    loop advancing anything else is not this loop.

		    Measured on the committed build with the two-pass
		    free-running driver, r1 = 0x40:
		      add r5,r5,#32 / subs r1,r1,#32 -> folded; r5 stayed at its
		        seeded 0x9100 where the loop owes 0x9140, r1 at 0x40
		        where the loop owes 0;
		      add r0,r0,#32 / subs r6,r6,#32 -> folded; r6 stayed at 0x40
		        where the loop owes 0.
		    Both were invisible before this round only because the
		    handler wrote nothing at all. Now that it writes r[0] and
		    r[1] by name, an unguarded match would additionally CLOBBER
		    those two in a loop that never mentions them -- #345's defect
		    exactly, reintroduced by fixing the other half.

		    ic[0] needs no check of its own: this combiner is armed only
		    from iword == 0x8afffffa (the case-0xa arming in
		    to_be_translated below; a NUMERIC line cite here has gone
		    stale twice in two rounds), which is `bhi`
		    with offset -6, so its target is ic[-4] by encoding, and
		    n_back >= 4 keeps ic[-4] inside the same instruction page.  */
		if (ic[-4].f == instr(mcr_mrc) && ic[-4].arg[0] == 0xee070f3a &&
		    ic[-3].f == instr(mcr_mrc) && ic[-3].arg[0] == 0xee070f36 &&
		    ic[-2].f == instr(add) &&
		    ic[-2].arg[0] == (size_t)(&cpu->cd.arm.r[0]) &&
		    ic[-2].arg[0]==ic[-2].arg[2] && ic[-2].arg[1] == 0x20 &&
		    ic[-1].f == instr(subs) &&
		    ic[-1].arg[0] == (size_t)(&cpu->cd.arm.r[1]) &&
		    ic[-1].arg[0]==ic[-1].arg[2] && ic[-1].arg[1] == 0x20) {
			ic[-4].f = instr(netbsd_cacheclean2);
		}
	}
}


/*
 *  Combine: netbsd_scanc():
 */
void COMBINE(netbsd_scanc)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back < 2)
		return;

	if (ic[-2].f == instr(load_w0_byte_u1_p1_imm) &&
	    ic[-2].arg[0] == (size_t)(&cpu->cd.arm.r[1]) &&
	    ic[-2].arg[1] == 0 &&
	    ic[-2].arg[2] == (size_t)(&cpu->cd.arm.r[3]) &&
	    ic[-1].f == instr(load_w0_byte_u1_p1_reg) &&
	    ic[-1].arg[0] == (size_t)(&cpu->cd.arm.r[2]) &&
	    ic[-1].arg[1] == (size_t)arm_r_r3_t0_c0 &&
	    ic[-1].arg[2] == (size_t)(&cpu->cd.arm.r[3])) {
		ic[-2].f = instr(netbsd_scanc);
		debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_scanc",   /*  #361  */
		    VERBOSITY_DEBUG, "installed at ic[-2]");
	}
}


/*
 *  Combine: strlen():
 */
void COMBINE(strlen)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back < 2)
		return;

	/*  #355: the load's base and destination must DIFFER. This is not a
	    wrong-answer fix -- `ldrb r3,[r3,#1]!` is UNPREDICTABLE in the
	    architecture, so the fold's answer is not "wrong" -- it is a
	    self-consistency fix: without the term, THIS emulator gives two
	    different answers for one program, selected by whether the
	    combination happened. Measured on the committed build: folded, the
	    walk exits at the first NUL byte (the loop condition tests the local
	    byte); genuine, the writeback overwrites the loaded byte so the cmps
	    compares an ADDRESS, never zero, and the loop runs on (r3 observed
	    at 0x037a2557, still climbing). Which one a guest gets depended on
	    -J, on a breakpoint, on instruction tracing, or on the loop's page
	    offset -- and gate 14 uses -J as its architectural oracle
	    throughout, so the divergence was an oracle defect regardless of
	    what ARM permits.

	    One term suffices and rejects exactly one iword (0xe5f33001): the
	    cmps reads ic[-1].arg[0], pinned to r3, and the load writes back
	    ic[-2].arg[0], so the writeback can only corrupt the compared value
	    when base == dest. No genuine strlen is rejected -- a base==dest
	    walk cannot traverse a string at all. The guard is first in the
	    chain, the shape #342 used; note that #342 is precedent for the
	    SHAPE only, not licence for this fix -- its `eor rX,rX,rX` case is
	    well-defined ARM and produced a demonstrably wrong value.

	    The rejected alternative, recorded so it is not revisited: making
	    the HANDLER faithful instead (test the written-back register after
	    the writeback) would put the guest's genuine infinite loop INSIDE
	    one C call -- an unkillable host hang. Failing the match instead
	    leaves the guest spinning on real dispatched instructions, which
	    remain interruptible.  */
	if (ic[-2].f == instr(load_w1_byte_u1_p1_imm) &&
	    ic[-2].arg[0] != ic[-2].arg[2] &&
	    ic[-2].arg[1] == 1 &&
	    ic[-2].arg[2] == (size_t)(&cpu->cd.arm.r[3]) &&
	    ic[-1].f == instr(cmps) &&
	    ic[-1].arg[0] == (size_t)(&cpu->cd.arm.r[3]) &&
	    ic[-1].arg[1] == 0) {
		ic[-2].f = instr(strlen);
	}
}


/*
 *  Combine: xchg():
 */
void COMBINE(xchg)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);
	size_t a, b;

	if (n_back < 2)
		return;

	a = ic[-2].arg[0]; b = ic[-1].arg[0];

	/*  #342: a != b is REQUIRED, and its absence was guest-visible. The XOR
	    swap is only a swap for two DISTINCT registers; with a == b the same
	    three encodings are `eor rX,rX,rX` three times over, and each of those
	    ZEROES rX. X(xchg) exchanges rX with itself, so the register comes out
	    unchanged instead of cleared. Measured with a two-pass free-running
	    probe: r0 re-seeded to 0x5a at the top of the loop read back 0x5a where
	    the architecture owes 0. That byte is unambiguous -- three standalone
	    EORs cannot leave a nonzero value, so only the folded handler can
	    produce it, which makes the row its own proof that the fold happened.  */
	if (a != b &&
	    ic[-2].f == instr(eor_regshort) &&
	    ic[-1].f == instr(eor_regshort) &&
	    ic[-2].arg[0] == a && ic[-2].arg[1] == b && ic[-2].arg[2] == b &&
	    ic[-1].arg[0] == b && ic[-1].arg[1] == a && ic[-1].arg[2] == a &&
	    ic[ 0].arg[0] == a && ic[ 0].arg[1] == b && ic[ 0].arg[2] == b) {
		ic[-2].f = instr(xchg);
		/*  #361: one line per TRANSLATION. X(xchg) has no bail path, so
		    there is no decline marker to add here -- for this fold the
		    negative control is the MATCHER declining, and this line is
		    what makes that visible: install 0 / fire 0 says the a != b
		    term rejected the shape, install 1 / fire 0 would say the
		    slot was installed but never dispatched.  */
		debugmsg_cpu(cpu, SUBSYS_CPU, "xchg",
		    VERBOSITY_DEBUG, "installed at ic[-2]");
	}
}


/*
 *  Combine: netbsd_copyin():
 */
void COMBINE(netbsd_copyin)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
#ifdef HOST_LITTLE_ENDIAN
	int i, n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back < 5)
		return;

	for (i=-5; i<0; i++) {
		if (ic[i].f != instr(load_w1_word_u1_p0_imm) ||
		    ic[i].arg[0] != (size_t)(&cpu->cd.arm.r[0]) ||
		    ic[i].arg[1] != 4)
			return;
	}

	if (ic[-5].arg[2] == (size_t)(&cpu->cd.arm.r[10]) &&
	    ic[-4].arg[2] == (size_t)(&cpu->cd.arm.r[11]) &&
	    ic[-3].arg[2] == (size_t)(&cpu->cd.arm.r[6]) &&
	    ic[-2].arg[2] == (size_t)(&cpu->cd.arm.r[7]) &&
	    ic[-1].arg[2] == (size_t)(&cpu->cd.arm.r[8])) {
		ic[-5].f = instr(netbsd_copyin);
		/*  #360: one line per TRANSLATION, not per execution, so this is
		    free even in a hot guest. It is the term that separates "the
		    matcher declined" from "the slot was installed but never
		    dispatched" -- without it those both read fire 0 / bail 0.  */
		debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_copyin",
		    VERBOSITY_DEBUG, "installed at ic[-5]");
	}
#endif
}


/*
 *  Combine: netbsd_copyout():
 */
void COMBINE(netbsd_copyout)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
#ifdef HOST_LITTLE_ENDIAN
	int i, n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);

	if (n_back < 5)
		return;

	for (i=-5; i<0; i++) {
		if (ic[i].f != instr(store_w1_word_u1_p0_imm) ||
		    ic[i].arg[0] != (size_t)(&cpu->cd.arm.r[1]) ||
		    ic[i].arg[1] != 4)
			return;
	}

	if (ic[-5].arg[2] == (size_t)(&cpu->cd.arm.r[8]) &&
	    ic[-4].arg[2] == (size_t)(&cpu->cd.arm.r[9]) &&
	    ic[-3].arg[2] == (size_t)(&cpu->cd.arm.r[10]) &&
	    ic[-2].arg[2] == (size_t)(&cpu->cd.arm.r[11]) &&
	    ic[-1].arg[2] == (size_t)(&cpu->cd.arm.r[6])) {
		ic[-5].f = instr(netbsd_copyout);
		debugmsg_cpu(cpu, SUBSYS_CPU, "netbsd_copyout",   /*  #360  */
		    VERBOSITY_DEBUG, "installed at ic[-5]");
	}
#endif
}


/*
 *  Combine: cmps + beq, etc:
 */
void COMBINE(beq_etc)(struct cpu *cpu,
	struct arm_instr_call *ic, int low_addr)
{
	int n_back = (low_addr >> ARM_INSTR_ALIGNMENT_SHIFT)
	    & (ARM_IC_ENTRIES_PER_PAGE-1);
	if (n_back < 1)
		return;
	if (ic[0].f == instr(b__eq)) {
		if (ic[-1].f == instr(cmps)) {
			if (ic[-1].arg[1] == 0)
				ic[-1].f = instr(cmps_0_beq);
			else if (ic[-1].arg[1] & 0x80000000)
				ic[-1].f = instr(cmps_neg_beq);
			else
				ic[-1].f = instr(cmps_pos_beq);
		}
		return;
	}
	if (ic[0].f == instr(b_samepage__eq)) {
		if (ic[-1].f == instr(cmps)) {
			if (ic[-1].arg[1] == 0)
				ic[-1].f = instr(cmps0_beq_samepage);
			else
				ic[-1].f = instr(cmps_beq_samepage);
		}
		if (ic[-1].f == instr(tsts) &&
		    !(ic[-1].arg[1] & 0x80000000)) {
			ic[-1].f = instr(tsts_lo_beq_samepage);
		}
		if (n_back >= 4 &&
		    ic[-4].f == instr(load_w0_word_u1_p1_imm) &&
		    ic[-4].arg[0] != ic[-4].arg[2] &&
		    ic[-4].arg[1] == 0 &&
		    ic[-4].arg[2] == ic[-3].arg[0] &&
		    /*  Note: The teqs+bne is already combined!  */
		    ic[-3].f == instr(teqs_bne_samepage) &&
		    ic[-3].arg[1] == 0 &&
		    ic[-2].f == instr(b_samepage__ne) &&
		    ic[-1].f == instr(teqs) &&
		    ic[-1].arg[0] != ic[-4].arg[0] &&
		    ic[-1].arg[1] == 0 &&
		    /*  #353: the beq MUST target the ldr, or this is not an idle
			loop. Without this the matcher accepted a FORWARD beq
			(any same-page target), and X(netbsd_idle) then treated a
			non-loop as an idle loop and HUNG the guest -- measured on
			the committed build (pc parked at the fold slot, the real
			target never reached). All same-page conditional branches
			carry their target ic as arg[0], so the loop-back beq has
			arg[0] == &ic[-4].  */
		    ic[0].arg[0] == (size_t)(&ic[-4])) {
			ic[-4].f = instr(netbsd_idle);
		}
		if (ic[-1].f == instr(teqs)) {
			ic[-1].f = instr(teqs_beq_samepage);
		}
		return;
	}
	if (ic[0].f == instr(b_samepage__ne)) {
		if (ic[-1].f == instr(cmps)) {
			if (ic[-1].arg[1] == 0)
				ic[-1].f = instr(cmps0_bne_samepage);
			else
				ic[-1].f = instr(cmps_bne_samepage);
		}
		if (ic[-1].f == instr(tsts) &&
		    !(ic[-1].arg[1] & 0x80000000)) {
			ic[-1].f = instr(tsts_lo_bne_samepage);
		}
		if (ic[-1].f == instr(teqs)) {
			ic[-1].f = instr(teqs_bne_samepage);
		}
		return;
	}
	if (ic[0].f == instr(b_samepage__cc)) {
		if (ic[-1].f == instr(cmps)) {
			ic[-1].f = instr(cmps_bcc_samepage);
		}
		if (ic[-1].f == instr(cmps_regshort)) {
			ic[-1].f = instr(cmps_reg_bcc_samepage);
		}
		return;
	}
	if (ic[0].f == instr(b_samepage__hi)) {
		if (ic[-1].f == instr(cmps)) {
			ic[-1].f = instr(cmps_bhi_samepage);
		}
		if (ic[-1].f == instr(cmps_regshort)) {
			ic[-1].f = instr(cmps_reg_bhi_samepage);
		}
		return;
	}
	if (ic[0].f == instr(b_samepage__gt)) {
		if (ic[-1].f == instr(cmps)) {
			ic[-1].f = instr(cmps_bgt_samepage);
		}
		return;
	}
	if (ic[0].f == instr(b_samepage__le)) {
		if (ic[-1].f == instr(cmps)) {
			ic[-1].f = instr(cmps_ble_samepage);
		}
		return;
	}
}


/*****************************************************************************/


static void arm_switch_clear(struct arm_instr_call *ic, int rd,
	int condition_code)
{
	switch (rd) {
	case  0: ic->f = cond_instr(clear_r0); break;
	case  1: ic->f = cond_instr(clear_r1); break;
	case  2: ic->f = cond_instr(clear_r2); break;
	case  3: ic->f = cond_instr(clear_r3); break;
	case  4: ic->f = cond_instr(clear_r4); break;
	case  5: ic->f = cond_instr(clear_r5); break;
	case  6: ic->f = cond_instr(clear_r6); break;
	case  7: ic->f = cond_instr(clear_r7); break;
	case  8: ic->f = cond_instr(clear_r8); break;
	case  9: ic->f = cond_instr(clear_r9); break;
	case 10: ic->f = cond_instr(clear_r10); break;
	case 11: ic->f = cond_instr(clear_r11); break;
	case 12: ic->f = cond_instr(clear_r12); break;
	case 13: ic->f = cond_instr(clear_r13); break;
	case 14: ic->f = cond_instr(clear_r14); break;
	}
}


static void arm_switch_mov1(struct arm_instr_call *ic, int rd,
	int condition_code)
{
	switch (rd) {
	case  0: ic->f = cond_instr(mov1_r0); break;
	case  1: ic->f = cond_instr(mov1_r1); break;
	case  2: ic->f = cond_instr(mov1_r2); break;
	case  3: ic->f = cond_instr(mov1_r3); break;
	case  4: ic->f = cond_instr(mov1_r4); break;
	case  5: ic->f = cond_instr(mov1_r5); break;
	case  6: ic->f = cond_instr(mov1_r6); break;
	case  7: ic->f = cond_instr(mov1_r7); break;
	case  8: ic->f = cond_instr(mov1_r8); break;
	case  9: ic->f = cond_instr(mov1_r9); break;
	case 10: ic->f = cond_instr(mov1_r10); break;
	case 11: ic->f = cond_instr(mov1_r11); break;
	case 12: ic->f = cond_instr(mov1_r12); break;
	case 13: ic->f = cond_instr(mov1_r13); break;
	case 14: ic->f = cond_instr(mov1_r14); break;
	}
}


static void arm_switch_add1(struct arm_instr_call *ic, int rd,
	int condition_code)
{
	switch (rd) {
	case  0: ic->f = cond_instr(add1_r0); break;
	case  1: ic->f = cond_instr(add1_r1); break;
	case  2: ic->f = cond_instr(add1_r2); break;
	case  3: ic->f = cond_instr(add1_r3); break;
	case  4: ic->f = cond_instr(add1_r4); break;
	case  5: ic->f = cond_instr(add1_r5); break;
	case  6: ic->f = cond_instr(add1_r6); break;
	case  7: ic->f = cond_instr(add1_r7); break;
	case  8: ic->f = cond_instr(add1_r8); break;
	case  9: ic->f = cond_instr(add1_r9); break;
	case 10: ic->f = cond_instr(add1_r10); break;
	case 11: ic->f = cond_instr(add1_r11); break;
	case 12: ic->f = cond_instr(add1_r12); break;
	case 13: ic->f = cond_instr(add1_r13); break;
	case 14: ic->f = cond_instr(add1_r14); break;
	}
}


/*****************************************************************************/


/*
 *  arm_instr_to_be_translated():
 *
 *  Translate an instruction word into an arm_instr_call. ic is filled in with
 *  valid data for the translated instruction, or a "nothing" instruction if
 *  there was a translation failure. The newly translated instruction is then
 *  executed.
 */
X(to_be_translated)
{
	uint32_t addr, low_pc, iword, imm = 0;
	unsigned char *page;
	unsigned char ib[4];
	int condition_code, main_opcode, secondary_opcode, s_bit, rn, rd, r8;
	int p_bit, u_bit, w_bit, l_bit, regform, rm, any_pc_reg; // , c, t
	void (*samepage_function)(struct cpu *, struct arm_instr_call *);

	/*  Figure out the address of the instruction:  */
	low_pc = ((size_t)ic - (size_t)cpu->cd.arm.cur_ic_page)
	    / sizeof(struct arm_instr_call);
	addr = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	addr += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT);
	cpu->pc = addr;
	addr &= ~((1 << ARM_INSTR_ALIGNMENT_SHIFT) - 1);

	/*  Read the instruction word from memory:  */
	page = cpu->cd.arm.host_load[addr >> 12];

	if (page != NULL) {
		/*  fatal("TRANSLATION HIT! 0x%08x\n", addr);  */
		memcpy(ib, page + (addr & 0xfff), sizeof(ib));
	} else {
		/*  fatal("TRANSLATION MISS! 0x%08x\n", addr);  */
		if (!cpu->memory_rw(cpu, cpu->mem, addr, &ib[0],
		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
			fatal("to_be_translated(): "
			    "read failed: TODO\n");
			return;
		}
	}

	if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
		iword = READ_WORD_LE(ib);
	else
		iword = READ_WORD_BE(ib);


#define DYNTRANS_TO_BE_TRANSLATED_HEAD
#include "cpu_dyntrans.c"
#undef  DYNTRANS_TO_BE_TRANSLATED_HEAD


	/*  The idea of taking bits 27..24 was found here:
	    http://armphetamine.sourceforge.net/oldinfo.html  */
	condition_code = iword >> 28;
	main_opcode = (iword >> 24) & 15;
	secondary_opcode = (iword >> 21) & 15;
	u_bit = iword & 0x00800000;
	w_bit = iword & 0x00200000;
	s_bit = l_bit = iword & 0x00100000;
	rn    = (iword >> 16) & 15;
	rd    = (iword >> 12) & 15;
	r8    = (iword >> 8) & 15;
	// c     = (iword >> 7) & 31;
	// t     = (iword >> 4) & 7;
	rm    = iword & 15;

	/*
	 *  Translate the instruction:
	 */

	if ((iword >> 28) == 0xf) {
		/*  The "never" condition is nowadays used for special encodings.  */
		if ((iword & 0xfc70f000) == 0xf450f000) {
			/*  Preload:  TODO.  Treat as NOP for now.  */
			ic->f = instr(nop);
			goto okay;
		}

		if (iword == 0xf10c0040) {
			/*  cpsid f. Treat as NOP for now.  */
			ic->f = instr(nop);
			goto okay;
		}

		if (iword == 0xf10c0080) {
			/*  cpsid i. Treat as NOP for now.  */
			ic->f = instr(nop);
			goto okay;
		}

		if (iword == 0xf57ff04f) {
			/*  dsb sy. Treat as NOP for now.  */
			ic->f = instr(nop);
			goto okay;
		}

		if (iword == 0xf57ff05f) {
			/*  dmb sy. Treat as NOP for now.  */
			ic->f = instr(nop);
			goto okay;
		}

		if (iword == 0xf57ff06f) {
			/*  isb sy. Treat as NOP for now.  */
			ic->f = instr(nop);
			goto okay;
		}

		switch (main_opcode) {
		case 0xa:
		case 0xb:
			ic->f = instr(blx_imm);

			/*  arg 1 = offset of current instruction  */
			ic->arg[1] = addr & 0xffc;

			/*  arg 0 = relative jump distance + 1 (to enable THUMB)  */
			ic->arg[0] = (iword & 0x00ffffff) << 2;
			/*  Sign-extend:  */
			if (ic->arg[0] & 0x02000000)
				ic->arg[0] |= 0xfc000000;
			if (main_opcode == 0xb)
				ic->arg[0] += 2;
			ic->arg[0] = (int32_t)(ic->arg[0] + 8 + 1);
			break;
		default:
			goto bad;
		}
		goto okay;
	}

	switch (main_opcode) {

	case 0x0:
	case 0x1:
	case 0x2:
	case 0x3:
		/*  Check special cases first:  */
		if ((iword & 0x0ff00fff) == 0x01900f9f) {
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
			ic->arg[2] = 0;

			if (rd == ARM_PC || rn == ARM_PC) {
				if (!cpu->translation_readahead)
					fatal("ldrex with pc register: TODO\n");
				goto bad;
			}
			
			ic->f = cond_instr(ldrex);
			break;
		}

		if ((iword & 0x0ff00ff0) == 0x01800f90) {
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);

			if (rd == ARM_PC || rm == ARM_PC || rn == ARM_PC ||
			    rd == rm || rd == rn) {
				if (!cpu->translation_readahead)
					fatal("strex with bad register: TODO\n");
				goto bad;
			}
			
			ic->f = cond_instr(strex);
			break;
		}

		if ((iword & 0x0ff000f0) == 0x00600090) {
			ic->arg[0] = iword;
			ic->f = cond_instr(mls);
			break;
		}
		
		if ((iword & 0x0fc000f0) == 0x00000090) {
			/*
			 *  Multiplication:
			 *  xxxx0000 00ASdddd nnnnssss 1001mmmm (Rd,Rm,Rs[,Rn])
			 */
			if (iword & 0x00200000) {
				if (s_bit)
					ic->f = cond_instr(mlas);
				else
					ic->f = cond_instr(mla);
				ic->arg[0] = iword;
			} else {
				if (s_bit)
					ic->f = cond_instr(muls);
				else
					ic->f = cond_instr(mul);
				/*  NOTE: rn means rd in this case:  */
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
				ic->arg[2] = (size_t)(&cpu->cd.arm.r[r8]);
			}
			break;
		}
		if ((iword & 0x0f8000f0) == 0x00800090) {
			/*  Long multiplication:  */
			if (s_bit) {
				if (!cpu->translation_readahead)
					fatal("TODO: sbit mull\n");
				goto bad;
			}
			ic->f = cond_instr(mull);
			ic->arg[0] = iword;
			break;
		}
		if ((iword & 0x0f900ff0) == 0x01000050) {
			if (!cpu->translation_readahead)
				fatal("TODO: q{,d}{add,sub}\n");
			goto bad;
		}
		if ((iword & 0x0ff000d0) == 0x01200010) {
			/*  bx or blx  */
			if (iword & 0x20)
				ic->f = cond_instr(blx_reg);
			else {
				if (cpu->machine->show_trace_tree &&
				    rm == ARM_LR)
					ic->f = cond_instr(bx_trace);
				else
					ic->f = cond_instr(bx);
			}
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rm]);
			ic->arg[2] = (addr & 0xffc) + 4;
                        break;
                }
		if ((iword & 0x0fb00ff0) == 0x1000090) {
			if (iword & 0x00400000)
				ic->f = cond_instr(swpb);
			else
				ic->f = cond_instr(swp);
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rn]);
			break;
		}
		if ((iword & 0x0fff0ff0) == 0x016f0f10) {
			ic->f = cond_instr(clz);
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rm]);
			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rd]);
			break;
		}
		if ((iword & 0x0ff00090) == 0x01000080) {
			/*  TODO: smlaXX  */
			goto bad;
		}
		if ((iword & 0x0ff00090) == 0x01400080) {
			/*  TODO: smlalY  */
			goto bad;
		}
		if ((iword & 0x0ff000b0) == 0x01200080) {
			/*  TODO: smlawY  */
			goto bad;
		}
		if ((iword & 0x0ff0f090) == 0x01600080) {
			/*  smulXY (16-bit * 16-bit => 32-bit)  */
			switch (iword & 0x60) {
			case 0x00: ic->f = cond_instr(smulbb); break;
			case 0x20: ic->f = cond_instr(smultb); break;
			case 0x40: ic->f = cond_instr(smulbt); break;
			default:   ic->f = cond_instr(smultt); break;
			}
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rm]);
			ic->arg[1] = (size_t)(&cpu->cd.arm.r[r8]);
			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rn]); /*  Rd  */
			break;
		}
		if ((iword & 0x0ff0f0b0) == 0x012000a0) {
			/*  TODO: smulwY  */
			goto bad;
		}
		if ((iword & 0x0fb0fff0) == 0x0120f000 ||
		    (iword & 0x0fb0f000) == 0x0320f000) {
			/*  msr: move to [S|C]PSR from a register or
			    immediate value  */
			if (iword & 0x02000000) {
				if (iword & 0x00400000)
					ic->f = cond_instr(msr_imm_spsr);
				else
					ic->f = cond_instr(msr_imm);
			} else {
				if (rm == ARM_PC) {
					if (!cpu->translation_readahead)
						fatal("msr PC?\n");
					goto bad;
				}
				if (iword & 0x00400000)
					ic->f = cond_instr(msr_spsr);
				else
					ic->f = cond_instr(msr);
			}
			imm = iword & 0xff;
			while (r8-- > 0)
				imm = (imm >> 2) | ((imm & 3) << 30);
			ic->arg[0] = imm;
			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
			{
				uint32_t arg1 = 0;
				if (iword & (1<<16)) arg1 |= 0x000000ff;
				if (iword & (1<<17)) arg1 |= 0x0000ff00;
				if (iword & (1<<18)) arg1 |= 0x00ff0000;
				if (iword & (1<<19)) arg1 |= 0xff000000;
				ic->arg[1] = arg1;
				if (arg1 == 0)
					ic->f = instr(nop);
			}
			break;
		}
		if ((iword & 0x0fbf0fff) == 0x010f0000) {
			/*  mrs: move from CPSR/SPSR to a register:  */
			if (rd == ARM_PC) {
				if (!cpu->translation_readahead)
					fatal("mrs PC?\n");
				goto bad;
			}
			if (iword & 0x00400000)
				ic->f = cond_instr(mrs_spsr);
			else
				ic->f = cond_instr(mrs);
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
			break;
		}
		if ((iword & 0x0e000090) == 0x00000090) {
			regform = !(iword & 0x00400000);
			imm = ((iword >> 4) & 0xf0) | (iword & 0xf);
			p_bit = main_opcode & 1;
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rd]);
			if (rd == ARM_PC || rn == ARM_PC) {
				ic->f = arm_load_store_instr_3_pc[
				    condition_code + (l_bit? 16 : 0)
				    + (iword & 0x40? 32 : 0)
				    + (w_bit? 64 : 0)
				    + (iword & 0x20? 128 : 0)
				    + (u_bit? 256 : 0) + (p_bit? 512 : 0)
				    + (regform? 1024 : 0)];
				if (rn == ARM_PC)
					ic->arg[0] = (size_t)
					    (&cpu->cd.arm.tmp_pc);
				if (!l_bit && rd == ARM_PC)
					ic->arg[2] = (size_t)
					    (&cpu->cd.arm.tmp_pc);
			} else
				ic->f = arm_load_store_instr_3[
				    condition_code + (l_bit? 16 : 0)
				    + (iword & 0x40? 32 : 0)
				    + (w_bit? 64 : 0)
				    + (iword & 0x20? 128 : 0)
				    + (u_bit? 256 : 0) + (p_bit? 512 : 0)
				    + (regform? 1024 : 0)];
			if (regform)
				ic->arg[1] = (size_t)(void *)arm_r[iword & 0xf];
			else
				ic->arg[1] = imm;
			break;
		}

		if (iword & 0x80 && !(main_opcode & 2) && iword & 0x10) {
			if (!cpu->translation_readahead)
				fatal("reg form blah blah\n");
			goto bad;
		}

		/*  "bkpt", ARMv5 and above  */
		if ((iword & 0x0ff000f0) == 0x01200070) {
			ic->f = cond_instr(bkpt);
			ic->arg[0] = addr & 0xfff;
			break;
		}

		/*  "mov pc,lr":  */
		if ((iword & 0x0fffffff) == 0x01a0f00e) {
			if (cpu->machine->show_trace_tree)
				ic->f = cond_instr(ret_trace);
			else
				ic->f = cond_instr(ret);
			break;
		}

		/*  "mov reg,reg" or "mov reg,pc":  */
		if ((iword & 0x0fff0ff0) == 0x01a00000 && rd != ARM_PC) {
			if (rm != ARM_PC) {
				ic->f = cond_instr(mov_reg_reg);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rm]);
			} else {
				ic->f = cond_instr(mov_reg_pc);
				ic->arg[0] = (addr & 0xfff) + 8;
			}
			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rd]);
			break;
		}

		/*  "mov reg,#0":  */
		if ((iword & 0x0fff0fff) == 0x03a00000 && rd != ARM_PC) {
			arm_switch_clear(ic, rd, condition_code);
			break;
		}

		/*  "mov reg,#1":  */
		if ((iword & 0x0fff0fff) == 0x03a00001 && rd != ARM_PC) {
			arm_switch_mov1(ic, rd, condition_code);
			break;
		}

		/*  "add reg,reg,#1":  */
		if ((iword & 0x0ff00fff) == 0x02800001 && rd != ARM_PC
		    && rn == rd) {
			arm_switch_add1(ic, rd, condition_code);
			break;
		}

		if ((iword & 0x0ff00000) == 0x03000000) {
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
			ic->arg[1] = (((iword & 0xf0000) >> 4) | (iword & 0xfff));
			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rd]);
			ic->f = cond_instr(movw);
			if (rd == ARM_PC) {
				if (!cpu->translation_readahead)
					fatal("movw with rd = pc?\n");
				goto bad;
			}
			break;
		} else if ((iword & 0x0ff00000) == 0x03400000) {
			ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
			ic->arg[1] = (((iword & 0xf0000) >> 4) | (iword & 0xfff)) << 16;
			ic->arg[2] = (size_t)(&cpu->cd.arm.r[rd]);
			ic->f = cond_instr(movt);
			if (rd == ARM_PC) {
				if (!cpu->translation_readahead)
					fatal("movt with rd = pc?\n");
				goto bad;
			}
			break;
		}

		/*
		 *  Generic Data Processing Instructions:
		 */
		if ((main_opcode & 2) == 0)
			regform = 1;
		else
			regform = 0;

		if (regform) {
			/*  0x1000 signifies Carry bit update on rotation,
			    which is not necessary for add,adc,sub,sbc,
			    rsb,rsc,cmp, or cmn, because they update the
			    Carry bit manually anyway.  */
			int q = 0x1000;
			if (s_bit == 0)
				q = 0;
			if ((secondary_opcode >= 2 && secondary_opcode <= 7)
			    || secondary_opcode==0xa || secondary_opcode==0xb)
				q = 0;
			ic->arg[1] = (size_t)(void *)arm_r[(iword & 0xfff) + q];
		} else {
			int steps = r8;

			imm = iword & 0xff;
			
			while (r8-- > 0)
				imm = (imm >> 2) | ((imm & 3) << 30);

			ic->arg[1] = imm;

			/*
			 *  #320: a rotate whose result came out at or below
			 *  255. The dpi template cannot tell that from an
			 *  unrotated immediate -- it judges by magnitude --
			 *  so the carry it owes (clear) would be left alone.
			 *  This used to `goto bad`, stopping the emulator, and
			 *  it did so for EVERY opcode and regardless of the S
			 *  bit, though only the eight logical opcodes with S
			 *  set can consume the shifter carry at all. That set
			 *  is the one the register path names for itself just
			 *  above; the rest now decode normally.
			 *
			 *  Note there is no `imm != 0` here, unlike the test
			 *  this replaces: a rotate of an imm8 of zero has the
			 *  same carry owing, and being exempt from the halt is
			 *  precisely why it went out WRONG rather than loudly.
			 *
			 *  Placed before the mvn rewrite below so MVN arrives
			 *  with its true operand and its own opcode.
			 */
			if (s_bit && steps != 0 && imm < 256
			    && !((secondary_opcode >= 2 &&
			    secondary_opcode <= 7) || secondary_opcode == 0xa
			    || secondary_opcode == 0xb)
			    && rd != ARM_PC) {
				/*
				 *  #322: rn == PC is allowed through -- the
				 *  handler reconstructs PC+8 itself. Three
				 *  independent diff-review seats named the
				 *  rn == PC carve-out as this round's one
				 *  remaining defect and one supplied the
				 *  witness (`tst pc, #4 ROR 2`, measured
				 *  leaving the carry set where the
				 *  architecture clears it), which is what
				 *  overturned the decision to leave it.
				 *
				 *  rd == PC stays out: writing the PC with the
				 *  S bit set is an exception return, and the
				 *  existing handler restores the flags from
				 *  SPSR afterwards -- so the shifter carry
				 *  there is overwritten rather than lost, and
				 *  routing it would break the return.
				 */
				ic->arg[0] = iword;
				ic->f = cond_instr(dpis_imm_rotc);
				break;
			}
		}

		/*
		 *  mvn #imm ==> mov #~imm
		 *
		 *  #321: only when the S bit is CLEAR. The rewrite complements
		 *  the operand here, at decode time, and the dpi template then
		 *  judges the shifter carry from whatever value it is handed --
		 *  so with S set it was reading the carry off the COMPLEMENT,
		 *  which inverts the answer in every band. Measured on the
		 *  committed build: `mvns r0,#1` set the carry where the
		 *  architecture leaves it alone, `mvns r0,#0x3fc` set it where
		 *  the architecture clears it, and `mvns r0,#0xff000000`
		 *  cleared it where the architecture sets it.
		 *
		 *  The flag-setting form has its own table entries already --
		 *  the generator emits all sixteen opcodes for S=1, and the
		 *  immediate mvns slots were simply unreachable because this
		 *  rewrite always fired first. The template's own MVN arm
		 *  computes ~b and runs the carry test on the TRUE operand,
		 *  which is what the architecture asks for.
		 */
		if (secondary_opcode == 0xf && !regform && !s_bit) {
			secondary_opcode = 0xd;
			ic->arg[1] = ~ic->arg[1];
		}

		ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
		ic->arg[2] = (size_t)(&cpu->cd.arm.r[rd]);
		any_pc_reg = 0;
		if (rn == ARM_PC || rd == ARM_PC)
			any_pc_reg = 1;

		if (!any_pc_reg && regform && (iword & 0xfff) < ARM_PC) {
			ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
			ic->f = arm_dpi_instr_regshort[condition_code +
			    16 * secondary_opcode + (s_bit? 256 : 0)];
		} else
			ic->f = arm_dpi_instr[condition_code +
			    16 * secondary_opcode + (s_bit? 256 : 0) +
			    (any_pc_reg? 512 : 0) + (regform? 1024 : 0)];

		if (ic->f == instr(eor_regshort))
			cpu->cd.arm.combination_check = COMBINE(xchg);
		if (iword == 0xe113000c)
			cpu->cd.arm.combination_check = COMBINE(netbsd_scanc);
		break;

	case 0x4:	/*  Load and store...  */
	case 0x5:	/*  xxxx010P UBWLnnnn ddddoooo oooooooo  Immediate  */
	case 0x6:	/*  xxxx011P UBWLnnnn ddddcccc ctt0mmmm  Register  */
	case 0x7:
		// Special non-loadstore encodings:
		if (main_opcode >= 6 && iword & 0x10) {
			if ((iword & 0x0fff0ff0) == 0x06bf0f30) {
				ic->f = cond_instr(rev);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
			} else if ((iword & 0x0fff03f0) == 0x06bf0070) {
				ic->f = cond_instr(sxth);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
				ic->arg[2] = ((iword & 0xc00) >> 10) << 3;
			} else if ((iword & 0x0fff03f0) == 0x06ef0070) {
				ic->f = cond_instr(uxtb);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
				ic->arg[2] = ((iword & 0xc00) >> 10) << 3;
			} else if ((iword & 0x0ff003f0) == 0x06e00070) {
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
				ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
				ic->f = cond_instr(uxtab);
				if (iword & 0xc00) {
					/*  #319: a rotate is legal here; it
					    used to stop the emulator.  */
					ic->arg[0] = iword;
					ic->f = cond_instr(uxtab_rot);
				}
			} else if ((iword & 0x0fff03f0) == 0x06ff0070) {
				ic->f = cond_instr(uxth);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
				ic->arg[2] = ((iword & 0xc00) >> 10) << 3;
			} else if ((iword & 0x0ff003f0) == 0x06f00070) {
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rn]);
				ic->arg[2] = (size_t)(&cpu->cd.arm.r[rm]);
				ic->f = cond_instr(uxtah);
				if (iword & 0xc00) {
					/*  #319  */
					ic->arg[0] = iword;
					ic->f = cond_instr(uxtah_rot);
				}
			} else if ((iword & 0x0fe00070) == 0x07c00010) {
				ic->f = cond_instr(bfi);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
				int lsb = (iword >> 7) & 31;
				int msb = (iword >> 16) & 31;
				ic->arg[2] = (msb << 16) + lsb;
			} else if ((iword & 0x0fe00070) == 0x07e00050) {
				ic->f = cond_instr(ubfx);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
				int lsb = (iword >> 7) & 31;
				int width = 1 + ((iword >> 16) & 31);
				ic->arg[2] = (width << 16) + lsb;
			} else if ((iword & 0x0fe00070) == 0x07a00050) {
				ic->f = cond_instr(sbfx);
				ic->arg[0] = (size_t)(&cpu->cd.arm.r[rd]);
				ic->arg[1] = (size_t)(&cpu->cd.arm.r[rm]);
				int lsb = (iword >> 7) & 31;
				int width = 1 + ((iword >> 16) & 31);
				ic->arg[2] = (width << 16) + lsb;
			} else {
				/*
				 *  #312: a word reaching here takes the
				 *  Undefined Instruction exception. It must not
				 *  stop the emulator, which is what used to
				 *  happen: `goto bad` reaches the shared label
				 *  in cpu_dyntrans.c, which sets
				 *  cpu->running = 0. On the ARMv4 CPUs this
				 *  tree actually models, the whole space is
				 *  architecturally undefined -- it holds ARM's
				 *  permanently-undefined encoding and the word
				 *  GDB plants for breakpoints -- so und is the
				 *  faithful answer as well as the safe one.
				 *  For the ARMv6 models that share this decoder
				 *  some of these words are real instructions
				 *  (REV16 and the rest of the media set) that
				 *  nobody has implemented; und is then an
				 *  approximation, which is what the warning
				 *  below is for. Halting was never right for
				 *  either.
				 *
				 *  Worse, the halt happened HERE, during
				 *  decode, so a CONDITIONAL undefined word
				 *  whose condition was false -- one the guest
				 *  would never have executed -- stopped the
				 *  emulator too. Routing to und fixes that as
				 *  well: the exception is raised only if the
				 *  condition passes.
				 *
				 *  This is where the und routing lives now. The
				 *  copy that used to sit further down this case
				 *  was unreachable -- its predicate was exactly
				 *  this block's guard, and every path here ends
				 *  in a break -- so it is gone.
				 */
				if (cpu->translation_readahead)
					goto bad;
				if ((iword & 0x0ff000f0) != 0x07f000f0) {
					/*
					 *  Not the permanently-undefined
					 *  pattern, so it may instead be an
					 *  extension nobody has implemented
					 *  yet. Say so once -- a guest can sit
					 *  in a loop on one of these.
					 */
					static int warned_undef = 0;
					if (!warned_undef) {
						warned_undef = 1;
						debugmsg_cpu(cpu, SUBSYS_CPU,
						    "opcode",
						    VERBOSITY_WARNING,
						    "unimplemented special "
						    "non-loadstore encoding "
						    "0x%08" PRIx32 " -- routing "
						    "to Undefined Instruction. "
						    "Only printing this once.",
						    (uint32_t) iword);
					}
				}
				ic->f = cond_instr(und);
				ic->arg[0] = addr & 0xfff;
			}
			break;
		}
	
		ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
		ic->arg[2] = (size_t)(&cpu->cd.arm.r[rd]);
		if (rd == ARM_PC || rn == ARM_PC) {
			ic->f = arm_load_store_instr_pc[((iword >> 16)
			    & 0x3f0) + condition_code];
			if (rn == ARM_PC)
				ic->arg[0] = (size_t)(&cpu->cd.arm.tmp_pc);
			if (!l_bit && rd == ARM_PC)
				ic->arg[2] = (size_t)(&cpu->cd.arm.tmp_pc);
		} else {
			ic->f = arm_load_store_instr[((iword >> 16) &
			    0x3f0) + condition_code];
		}
		imm = iword & 0xfff;
		if (main_opcode < 6)
			ic->arg[1] = imm;
		else
			ic->arg[1] = (size_t)(void *)arm_r[iword & 0xfff];
		/*  Special case: pc-relative load within the same page:  */
		if (rn == ARM_PC && rd != ARM_PC && main_opcode < 6 && l_bit) {
			unsigned char *p = page;
			int ofs = (addr & 0xfff) + 8, max = 0xffc;
			int b_bit = iword & 0x00400000;
			if (b_bit)
				max = 0xfff;
			if (u_bit)
				ofs += (iword & 0xfff);
			else
				ofs -= (iword & 0xfff);
			/*  NOTE/TODO: This assumes 4KB pages,
			    it will not work with 1KB pages.  */
			if (ofs >= 0 && ofs <= max && p != NULL) {
				unsigned char cbuf[4];
				int len = b_bit? 1 : 4;
				uint32_t x, a = (addr & 0xfffff000) | ofs;
				/*  ic->f = cond_instr(mov);  */
				ic->f = arm_dpi_instr[condition_code + 16*0xd];
				ic->arg[2] = (size_t)(&cpu->cd.arm.r[rd]);

				memcpy(cbuf, p + (a & 0xfff), len);

				if (b_bit) {
					x = cbuf[0];
				} else {
					if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
						x = cbuf[0] + (cbuf[1]<<8) +
						    (cbuf[2]<<16) + (cbuf[3]<<24);
					else
						x = cbuf[3] + (cbuf[2]<<8) +
						    (cbuf[1]<<16) + (cbuf[0]<<24);
				}
				
				ic->arg[1] = x;
			}
		}
		if (iword == 0xe4b09004)
			cpu->cd.arm.combination_check = COMBINE(netbsd_copyin);
		if (iword == 0xe4a17004)
			cpu->cd.arm.combination_check = COMBINE(netbsd_copyout);
		break;

	case 0x8:	/*  Multiple load/store...  (Block data transfer)  */
	case 0x9:	/*  xxxx100P USWLnnnn llllllll llllllll  */
		ic->arg[0] = (size_t)(&cpu->cd.arm.r[rn]);
		ic->arg[1] = (size_t)iword;
		/*  Generic case:  */
		if (l_bit)
			ic->f = cond_instr(bdt_load);
		else
			ic->f = cond_instr(bdt_store);
#if defined(HOST_LITTLE_ENDIAN) && !defined(GATHER_BDT_STATISTICS)
		/*
		 *  Check for availability of optimized implementation:
		 *  xxxx100P USWLnnnn llllllll llllllll
		 *           ^  ^ ^ ^        ^  ^ ^ ^   (0x00950154)
		 *  These bits are used to select which list to scan, and then
		 *  the list is scanned linearly.
		 *
		 *  The optimized functions do not support show_trace_tree,
		 *  but it's ok to use the unoptimized version in that case.
		 */
		if (!cpu->machine->show_trace_tree) {
			int i = 0, j = iword;
			j = ((j & 0x00800000) >> 16) | ((j & 0x00100000) >> 14)
			  | ((j & 0x00040000) >> 13) | ((j & 0x00010000) >> 12)
			  | ((j & 0x00000100) >>  5) | ((j & 0x00000040) >>  4)
			  | ((j & 0x00000010) >>  3) | ((j & 0x00000004) >>  2);
			while (multi_opcode[j][i] != 0) {
				if ((iword & 0x0fffffff) ==
				    multi_opcode[j][i]) {
					ic->f = multi_opcode_f[j]
					    [i*16 + condition_code];
					break;
				}
				i ++;
			}
		}
#endif
		if (rn == ARM_PC) {
			if (!cpu->translation_readahead)
				fatal("TODO: bdt with PC as base\n");
			goto bad;
		}
		break;

	case 0xa:					/*  B: branch  */
	case 0xb:					/*  BL: branch+link  */
		if (main_opcode == 0x0a) {
			ic->f = cond_instr(b);
			samepage_function = cond_instr(b_samepage);

			/*  Abort read-ahead on unconditional branches:  */
			if (condition_code == 0xe &&
			    cpu->translation_readahead > 1)
                                cpu->translation_readahead = 1;

			if (iword == 0xcaffffed)
				cpu->cd.arm.combination_check =
				    COMBINE(netbsd_memset);
			if (iword == 0xaafffff9)
				cpu->cd.arm.combination_check =
				    COMBINE(netbsd_memcpy);
		} else {
			if (cpu->machine->show_trace_tree) {
				ic->f = cond_instr(bl_trace);
				samepage_function =
				    cond_instr(bl_samepage_trace);
			} else {
				ic->f = cond_instr(bl);
				samepage_function = cond_instr(bl_samepage);
			}
		}

		/*  arg 1 = offset of current instruction  */
		/*  arg 2 = offset of the following instruction  */
		ic->arg[1] = addr & 0xffc;
		ic->arg[2] = (addr & 0xffc) + 4;

		ic->arg[0] = (iword & 0x00ffffff) << 2;
		/*  Sign-extend:  */
		if (ic->arg[0] & 0x02000000)
			ic->arg[0] |= 0xfc000000;
		/*
		 *  Branches are calculated as PC + 8 + offset.
		 */
		ic->arg[0] = (int32_t)(ic->arg[0] + 8);

		/*
		 *  Special case: branch within the same page:
		 *
		 *  arg[0] = addr of the arm_instr_call of the target
		 *  arg[1] = addr of the next arm_instr_call.
		 */
		{
			uint32_t mask_within_page =
			    ((ARM_IC_ENTRIES_PER_PAGE-1) <<
			    ARM_INSTR_ALIGNMENT_SHIFT) |
			    ((1 << ARM_INSTR_ALIGNMENT_SHIFT) - 1);
			uint32_t old_pc = addr;
			uint32_t new_pc = old_pc + (int32_t)ic->arg[0];
			if ((old_pc & ~mask_within_page) ==
			    (new_pc & ~mask_within_page)) {
				ic->f = samepage_function;
				ic->arg[0] = (size_t) (
				    cpu->cd.arm.cur_ic_page +
				    ((new_pc & mask_within_page) >>
				    ARM_INSTR_ALIGNMENT_SHIFT));
				ic->arg[1] = (size_t) (
				    cpu->cd.arm.cur_ic_page +
				    (((addr & mask_within_page) + 4) >>
				    ARM_INSTR_ALIGNMENT_SHIFT));
			} else if (main_opcode == 0x0a) {
				/*  Special hack for a plain "b":  */
				ic->arg[0] += ic->arg[1];
			}
		}

		if (main_opcode == 0xa && (condition_code <= 1
		    || condition_code == 3 || condition_code == 8
		    || condition_code == 12 || condition_code == 13))
			cpu->cd.arm.combination_check = COMBINE(beq_etc);

		if (iword == 0x1afffffc)
			cpu->cd.arm.combination_check = COMBINE(strlen);

		/*  Hm. Does this really increase performance?  */
		if (iword == 0x8afffffa)
			cpu->cd.arm.combination_check =
			    COMBINE(netbsd_cacheclean2);
		break;

	case 0xc:
	case 0xd:
		/*
		 *  xxxx1100 0100nnnn ddddcccc oooommmm    MCRR c,op,Rd,Rn,CRm
		 *  xxxx1100 0101nnnn ddddcccc oooommmm    MRRC c,op,Rd,Rn,CRm
		 */
		if ((iword & 0x0fe00fff) == 0x0c400000) {
			/*  Special case: mar/mra DSP instructions  */
			if (!cpu->translation_readahead)
				fatal("TODO: mar/mra DSP instructions!\n");
			/*  Perhaps these are actually identical to MCRR/MRRC */
			goto bad;
		}

		if ((iword & 0x0fe00000) == 0x0c400000) {
			if (!cpu->translation_readahead)
				fatal("MCRR/MRRC: TODO\n");
			goto bad;
		}

		/*
		 *  TODO: LDC/STC
		 *
		 *  For now, treat as Undefined instructions. This causes e.g.
		 *  Linux/ARM to emulate these instructions (floating point).
		 */
#if 1
		ic->f = cond_instr(und);
		ic->arg[0] = addr & 0xfff;
#else
		if (!cpu->translation_readahead)
			fatal("LDC/STC: TODO\n");
		goto bad;
#endif
		break;

	case 0xe:
		if ((iword & 0x0ff00ff0) == 0x0e200010) {
			/*  Special case: mia* DSP instructions  */
			/*  See Intel's 27343601.pdf, page 16-20  */
			if (!cpu->translation_readahead)
				fatal("TODO: mia* DSP instructions!\n");
			goto bad;
		}
		if (iword & 0x10) {
			/*  xxxx1110 oooLNNNN ddddpppp qqq1MMMM  MCR/MRC  */
			ic->arg[0] = iword;
			ic->f = cond_instr(mcr_mrc);
		} else {
			/*  xxxx1110 oooonnnn ddddpppp qqq0mmmm  CDP  */
			ic->arg[0] = iword;
			ic->f = cond_instr(cdp);
		}
		if (iword == 0xee070f9a)
			cpu->cd.arm.combination_check =
			    COMBINE(netbsd_cacheclean);
		break;

	case 0xf:
		/*  SWI:  */
		/*  Default handler:  */
		ic->f = cond_instr(swi);
		ic->arg[0] = addr & 0xfff;
		if (iword == 0xef8c64eb) {
			/*  Hack for rebooting a machine:  */
			ic->f = instr(reboot);
		} else if (iword == 0xef8c64be) {
			/*  Hack for openfirmware prom emulation:  */
			ic->f = instr(openfirmware);
		}
		break;

	default:goto bad;
	}

okay:

#define	DYNTRANS_TO_BE_TRANSLATED_TAIL
#include "cpu_dyntrans.c" 
#undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
}

