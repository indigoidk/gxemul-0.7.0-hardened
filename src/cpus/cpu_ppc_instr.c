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
 *  POWER/PowerPC instructions.
 *
 *  Individual functions should keep track of cpu->n_translated_instrs.
 *  (If no instruction was executed, then it should be decreased. If, say, 4
 *  instructions were combined into one function and executed, then it should
 *  be increased by 3.)
 */


#include "float_emul.h"

/*  #330: which invalid-operation rule a two-operand op follows.  */
#define	PPC_INVOP_ADD	0
#define	PPC_INVOP_SUB	1
#define	PPC_INVOP_MUL	2
#define	PPC_INVOP_DIV	3

#ifndef PPC_FP_CLASSIFY_INCLUDED
#define PPC_FP_CLASSIFY_INCLUDED
/*
 *  #330: operand CLASSIFICATION for the exception causes.
 *
 *  These read the RAW 64-bit pattern, never `struct ieee_float_value`, and
 *  that is forced rather than preferred: ieee_interpret_float_value() collapses
 *  every NaN to the host's NAN and takes a path that skips the sign, so the
 *  struct cannot tell a signalling NaN from a quiet one -- taking VXSNAN from
 *  its `nan` field would raise on every quiet NaN.
 *
 *  ppc_is_snan() also carries its own NaN-class guard. frsp tests the quiet
 *  bit bare, which is correct only because it sits inside an already-NaN
 *  branch; copied out of that context the same test calls INFINITY a
 *  signalling NaN, since Inf has an all-ones exponent and a clear bit 51.
 */
static int ppc_is_nan(uint64_t x)
{
	return (x & 0x7ff0000000000000ULL) == 0x7ff0000000000000ULL
	    && (x & 0x000fffffffffffffULL) != 0;
}

static int ppc_is_snan(uint64_t x)
{
	return ppc_is_nan(x) && !(x & 0x0008000000000000ULL);
}

static int ppc_is_inf(uint64_t x)
{
	return (x & 0x7fffffffffffffffULL) == 0x7ff0000000000000ULL;
}

static int ppc_is_zero(uint64_t x)
{
	return (x & 0x7fffffffffffffffULL) == 0;
}

/*
 *  The invalid-operation cause owed by a two-operand arithmetic instruction,
 *  as a mask for ppc_fpscr_raise(). Detection is from the OPERANDS, never from
 *  the host result: for an fmadd whose product overflows the host, the host
 *  computes a NaN while the ISA's unrounded intermediate is an infinity and no
 *  exception is owed at all, so a result-driven test would invent one.
 *
 *  A signalling operand takes precedence and is the only cause in that case
 *  for add/sub/mul; the class-specific causes apply to numerically invalid
 *  combinations of non-signalling operands.
 */
static uint32_t ppc_invalid_cause(uint64_t a, uint64_t b, int op)
{
	if (ppc_is_snan(a) || ppc_is_snan(b))
		return PPC_FPSCR_VXNAN;

	/*  A quiet NaN operand propagates and raises nothing.  */
	if (ppc_is_nan(a) || ppc_is_nan(b))
		return 0;

	switch (op) {
	case PPC_INVOP_ADD:	/*  Inf + (-Inf)  */
		if (ppc_is_inf(a) && ppc_is_inf(b)
		    && ((a ^ b) >> 63) != 0)
			return PPC_FPSCR_VXISI;
		break;
	case PPC_INVOP_SUB:	/*  Inf - Inf, same sign  */
		if (ppc_is_inf(a) && ppc_is_inf(b)
		    && ((a ^ b) >> 63) == 0)
			return PPC_FPSCR_VXISI;
		break;
	case PPC_INVOP_MUL:	/*  Inf * 0, either order  */
		if ((ppc_is_inf(a) && ppc_is_zero(b))
		    || (ppc_is_zero(a) && ppc_is_inf(b)))
			return PPC_FPSCR_VXIMZ;
		break;
	case PPC_INVOP_DIV:
		if (ppc_is_inf(a) && ppc_is_inf(b))
			return PPC_FPSCR_VXIDI;
		if (ppc_is_zero(a) && ppc_is_zero(b))
			return PPC_FPSCR_VXZDZ;
		break;
	}

	return 0;
}
#endif	/*  PPC_FP_CLASSIFY_INCLUDED  */



/*
 *  #326: FDOT -- the floating-point twin of DOT0/1/2 below.
 *
 *  Every opcode-59/63 form with Rc=1 used to reach `goto bad`, which does not
 *  raise a program exception: it stops the emulator. That meant `fadd.`,
 *  `frsp.`, `fmr.` and the rest killed the machine, including the record
 *  forms of instructions that worked perfectly with Rc=0 -- and a compiler
 *  emits them whenever a floating-point result feeds a condition test.
 *
 *  CHECK_FOR_FPU_EXCEPTION comes FIRST, before the base handler, and that
 *  ordering is load-bearing rather than tidy. The base handler's own check
 *  returns from the BASE on MSR[FP]=0, which would leave this wrapper to
 *  write CR1 on top of a just-entered exception context, for an instruction
 *  that never executed. NetBSD/macppc does lazy FP -- MSR[FP] is clear on
 *  every process's first floating-point instruction -- so that is the
 *  ordinary path, not a corner. Checking here returns before the base runs;
 *  when FP is available the base's identical check simply passes again.
 */
#define FDOT(n) X(n ## _dot) { CHECK_FOR_FPU_EXCEPTION; \
	instr(n)(cpu,ic); update_cr1(cpu); }

#define DOT0(n) X(n ## _dot) { instr(n)(cpu,ic); \
	update_cr0(cpu, reg(ic->arg[0])); }
#define DOT1(n) X(n ## _dot) { instr(n)(cpu,ic); \
	update_cr0(cpu, reg(ic->arg[1])); }
#define DOT2(n) X(n ## _dot) { instr(n)(cpu,ic); \
	update_cr0(cpu, reg(ic->arg[2])); }

#ifndef CHECK_FOR_FPU_EXCEPTION
#define CHECK_FOR_FPU_EXCEPTION { if (!(cpu->cd.ppc.msr & PPC_MSR_FP)) { \
		/*  Synchronize the PC, and cause an FPU exception:  */  \
		uint64_t low_pc = ((size_t)ic -				 \
		    (size_t)cpu->cd.ppc.cur_ic_page)			 \
		    / sizeof(struct ppc_instr_call);			 \
		cpu->pc = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) <<	 \
		    PPC_INSTR_ALIGNMENT_SHIFT)) + (low_pc <<		 \
		    PPC_INSTR_ALIGNMENT_SHIFT);				 \
		ppc_exception(cpu, PPC_EXCEPTION_FPU);			 \
		return; } }
#endif



/*
 *  nop:  Do nothing.
 */
X(nop)
{
}


/*
 *  invalid:  To catch bugs.
 */
X(invalid)
{
	fatal("PPC: invalid(): INTERNAL ERROR\n");
	exit(1);
}


/*
 *  addi:  Add immediate.
 *
 *  arg[0] = pointer to source uint64_t
 *  arg[1] = immediate value (int32_t or larger)
 *  arg[2] = pointer to destination uint64_t
 */
X(addi)
{
	reg(ic->arg[2]) = reg(ic->arg[0]) + (int32_t)ic->arg[1];
}
X(li)
{
	reg(ic->arg[2]) = (int32_t)ic->arg[1];
}
X(li_0)
{
	reg(ic->arg[2]) = 0;
}


/*
 *  andi_dot:  AND immediate, update CR.
 *
 *  arg[0] = pointer to source uint64_t
 *  arg[1] = immediate value (uint32_t)
 *  arg[2] = pointer to destination uint64_t
 */
X(andi_dot)
{
	MODE_uint_t tmp = reg(ic->arg[0]) & (uint32_t)ic->arg[1];
	reg(ic->arg[2]) = tmp;
	update_cr0(cpu, tmp);
}


/*
 *  addic:  Add immediate, Carry.
 *
 *  arg[0] = pointer to source register
 *  arg[1] = immediate value (int32_t or larger)
 *  arg[2] = pointer to destination register
 */
X(addic)
{
	/*  TODO/NOTE: Only for 32-bit mode, so far!  */
	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
	uint64_t tmp2 = tmp;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	tmp2 += (uint32_t)ic->arg[1];
	if ((tmp2 >> 32) != (tmp >> 32))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp2;
}


/*
 *  subfic:  Subtract from immediate, Carry.
 *
 *  arg[0] = pointer to source uint64_t
 *  arg[1] = immediate value (int32_t or larger)
 *  arg[2] = pointer to destination uint64_t
 */
X(subfic)
{
	MODE_uint_t tmp = (int64_t)(int32_t)ic->arg[1];
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (tmp >= reg(ic->arg[0]))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = tmp - reg(ic->arg[0]);
}


/*
 *  addic_dot:  Add immediate, Carry.
 *
 *  arg[0] = pointer to source uint64_t
 *  arg[1] = immediate value (int32_t or larger)
 *  arg[2] = pointer to destination uint64_t
 */
X(addic_dot)
{
	/*  TODO/NOTE: Only for 32-bit mode, so far!  */
	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
	uint64_t tmp2 = tmp;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	tmp2 += (uint32_t)ic->arg[1];
	if ((tmp2 >> 32) != (tmp >> 32))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp2;
	update_cr0(cpu, (uint32_t)tmp2);
}


/*
 *  bclr:  Branch Conditional to Link Register
 *
 *  arg[0] = bo
 *  arg[1] = 31 - bi
 *  arg[2] = bh
 */
X(bclr)
{
	unsigned int bo = ic->arg[0], bi31m = ic->arg[1];
	int ctr_ok, cond_ok;
	uint64_t old_pc = cpu->pc;
	MODE_uint_t tmp, addr = cpu->cd.ppc.spr[SPR_LR];
	if (!(bo & 4))
		cpu->cd.ppc.spr[SPR_CTR] --;
	ctr_ok = (bo >> 2) & 1;
	tmp = cpu->cd.ppc.spr[SPR_CTR];
	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
	cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) == ((cpu->cd.ppc.cr >> bi31m) & 1) );
	if (ctr_ok && cond_ok) {
		uint64_t mask_within_page =
		    ((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT)
		    | ((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		cpu->pc = addr & ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		/*  TODO: trace in separate (duplicate) function?  */
		if (cpu->machine->show_trace_tree)
			cpu_functioncall_trace_return(cpu);
		if ((old_pc  & ~mask_within_page) ==
		    (cpu->pc & ~mask_within_page)) {
			cpu->cd.ppc.next_ic =
			    cpu->cd.ppc.cur_ic_page +
			    ((cpu->pc & mask_within_page) >>
			    PPC_INSTR_ALIGNMENT_SHIFT);
		} else {
			/*  Find the new physical page and update pointers:  */
			quick_pc_to_pointers(cpu);
		}
	}
}
X(bclr_20)
{
	cpu->pc = cpu->cd.ppc.spr[SPR_LR];
	quick_pc_to_pointers(cpu);
}
X(bclr_l)
{
	uint64_t low_pc, old_pc = cpu->pc;
	unsigned int bo = ic->arg[0], bi31m = ic->arg[1]  /* ,bh = ic->arg[2]*/;
	int ctr_ok, cond_ok;
	MODE_uint_t tmp, addr = cpu->cd.ppc.spr[SPR_LR];
	if (!(bo & 4))
		cpu->cd.ppc.spr[SPR_CTR] --;
	ctr_ok = (bo >> 2) & 1;
	tmp = cpu->cd.ppc.spr[SPR_CTR];
	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
	cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) == ((cpu->cd.ppc.cr >> bi31m) & 1) );

	/*  Calculate return PC:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call) + 1;
	cpu->cd.ppc.spr[SPR_LR] = cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->cd.ppc.spr[SPR_LR] += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	if (ctr_ok && cond_ok) {
		uint64_t mask_within_page =
		    ((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT)
		    | ((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		cpu->pc = addr & ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		/*  TODO: trace in separate (duplicate) function?  */
		if (cpu->machine->show_trace_tree)
			cpu_functioncall_trace_return(cpu);
		if (cpu->machine->show_trace_tree)
			cpu_functioncall_trace(cpu, cpu->pc);
		if ((old_pc  & ~mask_within_page) ==
		    (cpu->pc & ~mask_within_page)) {
			cpu->cd.ppc.next_ic =
			    cpu->cd.ppc.cur_ic_page +
			    ((cpu->pc & mask_within_page) >>
			    PPC_INSTR_ALIGNMENT_SHIFT);
		} else {
			/*  Find the new physical page and update pointers:  */
			quick_pc_to_pointers(cpu);
		}
	}
}


/*
 *  bcctr:  Branch Conditional to Count register
 *
 *  arg[0] = bo
 *  arg[1] = 31 - bi
 *  arg[2] = bh
 */
X(bcctr)
{
	unsigned int bo = ic->arg[0], bi31m = ic->arg[1];
	uint64_t old_pc = cpu->pc;
	MODE_uint_t addr = cpu->cd.ppc.spr[SPR_CTR];
	int cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) == ((cpu->cd.ppc.cr >> bi31m) & 1) );
	if (cond_ok) {
		uint64_t mask_within_page =
		    ((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT)
		    | ((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		cpu->pc = addr & ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		/*  TODO: trace in separate (duplicate) function?  */
		if (cpu->machine->show_trace_tree)
			cpu_functioncall_trace_return(cpu);
		if ((old_pc  & ~mask_within_page) ==
		    (cpu->pc & ~mask_within_page)) {
			cpu->cd.ppc.next_ic =
			    cpu->cd.ppc.cur_ic_page +
			    ((cpu->pc & mask_within_page) >>
			    PPC_INSTR_ALIGNMENT_SHIFT);
		} else {
			/*  Find the new physical page and update pointers:  */
			quick_pc_to_pointers(cpu);
		}
	}
}
X(bcctr_l)
{
	uint64_t low_pc, old_pc = cpu->pc;
	unsigned int bo = ic->arg[0], bi31m = ic->arg[1]  /*,bh = ic->arg[2] */;
	MODE_uint_t addr = cpu->cd.ppc.spr[SPR_CTR];
	int cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) == ((cpu->cd.ppc.cr >> bi31m) & 1) );

	/*  Calculate return PC:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call) + 1;
	cpu->cd.ppc.spr[SPR_LR] = cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->cd.ppc.spr[SPR_LR] += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	if (cond_ok) {
		uint64_t mask_within_page =
		    ((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT)
		    | ((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		cpu->pc = addr & ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);
		/*  TODO: trace in separate (duplicate) function?  */
		if (cpu->machine->show_trace_tree)
			cpu_functioncall_trace(cpu, cpu->pc);
		if ((old_pc  & ~mask_within_page) ==
		    (cpu->pc & ~mask_within_page)) {
			cpu->cd.ppc.next_ic =
			    cpu->cd.ppc.cur_ic_page +
			    ((cpu->pc & mask_within_page) >>
			    PPC_INSTR_ALIGNMENT_SHIFT);
		} else {
			/*  Find the new physical page and update pointers:  */
			quick_pc_to_pointers(cpu);
		}
	}
}


/*
 *  b:  Branch (to a different translated page)
 *
 *  arg[0] = relative offset (as an int32_t) from start of page
 */
X(b)
{
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (int32_t)ic->arg[0];

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers(cpu);
}
X(ba)
{
	cpu->pc = (int32_t)ic->arg[0];
	quick_pc_to_pointers(cpu);
}


/*
 *  bc:  Branch Conditional (to a different translated page)
 *
 *  arg[0] = relative offset (as an int32_t) from start of page
 *  arg[1] = bo
 *  arg[2] = 31-bi
 */
X(bc)
{
	MODE_uint_t tmp;
	unsigned int ctr_ok, cond_ok, bi31m = ic->arg[2], bo = ic->arg[1];
	if (!(bo & 4))
		cpu->cd.ppc.spr[SPR_CTR] --;
	ctr_ok = (bo >> 2) & 1;
	tmp = cpu->cd.ppc.spr[SPR_CTR];
	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
	cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) ==
	    ((cpu->cd.ppc.cr >> (bi31m)) & 1)  );
	if (ctr_ok && cond_ok)
		instr(b)(cpu,ic);
}
X(bcl)
{
	MODE_uint_t tmp;
	unsigned int ctr_ok, cond_ok, bi31m = ic->arg[2], bo = ic->arg[1];
	int low_pc;

	/*  Calculate LR:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call) + 1;
	cpu->cd.ppc.spr[SPR_LR] = cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->cd.ppc.spr[SPR_LR] += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	if (!(bo & 4))
		cpu->cd.ppc.spr[SPR_CTR] --;
	ctr_ok = (bo >> 2) & 1;
	tmp = cpu->cd.ppc.spr[SPR_CTR];
	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
	cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) ==
	    ((cpu->cd.ppc.cr >> bi31m) & 1)  );
	if (ctr_ok && cond_ok)
		instr(b)(cpu,ic);
}


/*
 *  b_samepage:  Branch (to within the same translated page)
 *
 *  arg[0] = pointer to new ppc_instr_call
 */
X(b_samepage)
{
	cpu->cd.ppc.next_ic = (struct ppc_instr_call *) ic->arg[0];
}


/*
 *  bc_samepage:  Branch Conditional (to within the same page)
 *
 *  arg[0] = new ic ptr
 *  arg[1] = bo
 *  arg[2] = 31-bi
 */
X(bc_samepage)
{
	MODE_uint_t tmp;
	unsigned int ctr_ok, cond_ok, bi31m = ic->arg[2], bo = ic->arg[1];
	if (!(bo & 4))
		cpu->cd.ppc.spr[SPR_CTR] --;
	ctr_ok = (bo >> 2) & 1;
	tmp = cpu->cd.ppc.spr[SPR_CTR];
	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
	cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) ==
	    ((cpu->cd.ppc.cr >> bi31m) & 1)  );
	if (ctr_ok && cond_ok)
		cpu->cd.ppc.next_ic = (struct ppc_instr_call *) ic->arg[0];
}
X(bc_samepage_simple0)
{
	int bi31m = ic->arg[2];
	if (!((cpu->cd.ppc.cr >> bi31m) & 1))
		cpu->cd.ppc.next_ic = (struct ppc_instr_call *) ic->arg[0];
}
X(bc_samepage_simple1)
{
	int bi31m = ic->arg[2];
	if ((cpu->cd.ppc.cr >> bi31m) & 1)
		cpu->cd.ppc.next_ic = (struct ppc_instr_call *) ic->arg[0];
}
X(bcl_samepage)
{
	MODE_uint_t tmp;
	unsigned int ctr_ok, cond_ok, bi31m = ic->arg[2], bo = ic->arg[1];
	int low_pc;

	/*  Calculate LR:  */
	low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call) + 1;
	cpu->cd.ppc.spr[SPR_LR] = cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->cd.ppc.spr[SPR_LR] += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	if (!(bo & 4))
		cpu->cd.ppc.spr[SPR_CTR] --;
	ctr_ok = (bo >> 2) & 1;
	tmp = cpu->cd.ppc.spr[SPR_CTR];
	ctr_ok |= ( (tmp == 0) == ((bo >> 1) & 1) );
	cond_ok = (bo >> 4) & 1;
	cond_ok |= ( ((bo >> 3) & 1) ==
	    ((cpu->cd.ppc.cr >> bi31m) & 1)  );
	if (ctr_ok && cond_ok)
		cpu->cd.ppc.next_ic = (struct ppc_instr_call *) ic->arg[0];
}


/*
 *  bl:  Branch and Link (to a different translated page)
 *
 *  arg[0] = relative offset (as an int32_t) from start of page
 *  arg[1] = lr offset (relative to start of current page)
 */
X(bl)
{
	/*  Calculate LR and new PC:  */
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->cd.ppc.spr[SPR_LR] = cpu->pc + ic->arg[1];
	cpu->pc += (int32_t)ic->arg[0];

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers(cpu);
}
X(bla)
{
	/*  Calculate LR:  */
	cpu->cd.ppc.spr[SPR_LR] = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) 
	    << PPC_INSTR_ALIGNMENT_SHIFT)) + ic->arg[1];

	cpu->pc = (int32_t)ic->arg[0];
	quick_pc_to_pointers(cpu);
}


/*
 *  bl_trace:  Branch and Link (to a different translated page)  (with trace)
 *
 *  arg[0] = relative offset (as an int32_t) from start of page
 *  arg[1] = lr offset (relative to start of current page)
 */
X(bl_trace)
{
	/*  Calculate LR:  */
	cpu->cd.ppc.spr[SPR_LR] = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) 
	    << PPC_INSTR_ALIGNMENT_SHIFT)) + ic->arg[1];

	/*  Calculate new PC from start of page + arg[0]  */
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (int32_t)ic->arg[0];

	cpu_functioncall_trace(cpu, cpu->pc);

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers(cpu);
}
X(bla_trace)
{
	/*  Calculate LR:  */
	cpu->cd.ppc.spr[SPR_LR] = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) 
	    << PPC_INSTR_ALIGNMENT_SHIFT)) + ic->arg[1];

	cpu->pc = (int32_t)ic->arg[0];
	cpu_functioncall_trace(cpu, cpu->pc);
	quick_pc_to_pointers(cpu);
}


/*
 *  bl_samepage:  Branch and Link (to within the same translated page)
 *
 *  arg[0] = pointer to new ppc_instr_call
 *  arg[1] = lr offset (relative to start of current page)
 */
X(bl_samepage)
{
	/*  Calculate LR:  */
	cpu->cd.ppc.spr[SPR_LR] = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) 
	    << PPC_INSTR_ALIGNMENT_SHIFT)) + ic->arg[1];

	cpu->cd.ppc.next_ic = (struct ppc_instr_call *) ic->arg[0];
}


/*
 *  bl_samepage_trace:  Branch and Link (to within the same translated page)
 *
 *  arg[0] = pointer to new ppc_instr_call
 *  arg[1] = lr offset (relative to start of current page)
 */
X(bl_samepage_trace)
{
	uint32_t low_pc;

	/*  Calculate LR:  */
	cpu->cd.ppc.spr[SPR_LR] = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) 
	    << PPC_INSTR_ALIGNMENT_SHIFT)) + ic->arg[1];

	cpu->cd.ppc.next_ic = (struct ppc_instr_call *) ic->arg[0];

	/*  Calculate new PC (for the trace)  */
	low_pc = ((size_t)cpu->cd.ppc.next_ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call);
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu_functioncall_trace(cpu, cpu->pc);
}


/*
 *  cntlzw:  Count leading zeroes (32-bit word).
 *
 *  arg[0] = ptr to rs
 *  arg[1] = ptr to ra
 */
X(cntlzw)
{
	uint32_t tmp = reg(ic->arg[0]);
	int i;
	for (i=0; i<32; i++) {
		if (tmp & 0x80000000)
			break;
		tmp <<= 1;
	}
	reg(ic->arg[1]) = i;
}


/*
 *  cmpd:  Compare Doubleword
 *
 *  arg[0] = ptr to ra
 *  arg[1] = ptr to rb
 *  arg[2] = 28 - 4*bf
 */
X(cmpd)
{
	int64_t tmp = reg(ic->arg[0]), tmp2 = reg(ic->arg[1]);
	int bf_shift = ic->arg[2], c;
	if (tmp < tmp2)
		c = 8;
	else if (tmp > tmp2)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}


/*
 *  cmpld:  Compare Doubleword, unsigned
 *
 *  arg[0] = ptr to ra
 *  arg[1] = ptr to rb
 *  arg[2] = 28 - 4*bf
 */
X(cmpld)
{
	uint64_t tmp = reg(ic->arg[0]), tmp2 = reg(ic->arg[1]);
	int bf_shift = ic->arg[2], c;
	if (tmp < tmp2)
		c = 8;
	else if (tmp > tmp2)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}


/*
 *  cmpdi:  Compare Doubleword immediate
 *
 *  arg[0] = ptr to ra
 *  arg[1] = int32_t imm
 *  arg[2] = 28 - 4*bf
 */
X(cmpdi)
{
	int64_t tmp = reg(ic->arg[0]), imm = (int32_t)ic->arg[1];
	int bf_shift = ic->arg[2], c;
	if (tmp < imm)
		c = 8;
	else if (tmp > imm)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}


/*
 *  cmpldi:  Compare Doubleword immediate, logical
 *
 *  arg[0] = ptr to ra
 *  arg[1] = int32_t imm
 *  arg[2] = 28 - 4*bf
 */
X(cmpldi)
{
	uint64_t tmp = reg(ic->arg[0]), imm = (uint32_t)ic->arg[1];
	int bf_shift = ic->arg[2], c;
	if (tmp < imm)
		c = 8;
	else if (tmp > imm)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}


/*
 *  cmpw:  Compare Word
 *
 *  arg[0] = ptr to ra
 *  arg[1] = ptr to rb
 *  arg[2] = 28 - 4*bf
 */
X(cmpw)
{
	int32_t tmp = reg(ic->arg[0]), tmp2 = reg(ic->arg[1]);
	int bf_shift = ic->arg[2], c;
	if (tmp < tmp2)
		c = 8;
	else if (tmp > tmp2)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}
X(cmpw_cr0)
{
	/*  arg[2] is assumed to be 28  */
	int32_t tmp = reg(ic->arg[0]), tmp2 = reg(ic->arg[1]);
	cpu->cd.ppc.cr &= ~(0xf0000000);
	if (tmp < tmp2)
		cpu->cd.ppc.cr |= 0x80000000;
	else if (tmp > tmp2)
		cpu->cd.ppc.cr |= 0x40000000;
	else
		cpu->cd.ppc.cr |= 0x20000000;
	cpu->cd.ppc.cr |= ((cpu->cd.ppc.spr[SPR_XER] >> 3) & 0x10000000);
}


/*
 *  cmplw:  Compare Word, unsigned
 *
 *  arg[0] = ptr to ra
 *  arg[1] = ptr to rb
 *  arg[2] = 28 - 4*bf
 */
X(cmplw)
{
	uint32_t tmp = reg(ic->arg[0]), tmp2 = reg(ic->arg[1]);
	int bf_shift = ic->arg[2], c;
	if (tmp < tmp2)
		c = 8;
	else if (tmp > tmp2)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}


/*
 *  cmpwi:  Compare Word immediate
 *
 *  arg[0] = ptr to ra
 *  arg[1] = int32_t imm
 *  arg[2] = 28 - 4*bf
 */
X(cmpwi)
{
	int32_t tmp = reg(ic->arg[0]), imm = ic->arg[1];
	int bf_shift = ic->arg[2], c;
	if (tmp < imm)
		c = 8;
	else if (tmp > imm)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}
X(cmpwi_cr0)
{
	/*  arg[2] is assumed to be 28  */
	int32_t tmp = reg(ic->arg[0]), imm = ic->arg[1];
	cpu->cd.ppc.cr &= ~(0xf0000000);
	if (tmp < imm)
		cpu->cd.ppc.cr |= 0x80000000;
	else if (tmp > imm)
		cpu->cd.ppc.cr |= 0x40000000;
	else
		cpu->cd.ppc.cr |= 0x20000000;
	cpu->cd.ppc.cr |= ((cpu->cd.ppc.spr[SPR_XER] >> 3) & 0x10000000);
}


/*
 *  cmplwi:  Compare Word immediate, logical
 *
 *  arg[0] = ptr to ra
 *  arg[1] = int32_t imm
 *  arg[2] = 28 - 4*bf
 */
X(cmplwi)
{
	uint32_t tmp = reg(ic->arg[0]), imm = ic->arg[1];
	int bf_shift = ic->arg[2], c;
	if (tmp < imm)
		c = 8;
	else if (tmp > imm)
		c = 4;
	else
		c = 2;
	/*  SO bit, copied from XER  */
	c |= ((cpu->cd.ppc.spr[SPR_XER] >> 31) & 1);
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);
}


/*
 *  dcbz:  Data-Cache Block Zero
 *
 *  arg[0] = ptr to ra (or zero)
 *  arg[1] = ptr to rb
 */
X(dcbz)
{
	MODE_uint_t addr = reg(ic->arg[0]) + reg(ic->arg[1]);
	unsigned char cacheline[128];
	size_t cacheline_size = 1 << cpu->cd.ppc.cpu_type.dlinesize;
	size_t cleared = 0;

	/*  Synchronize the PC first:  */
	cpu->pc = (cpu->pc & ~0xfff) + ic->arg[2];

	addr &= ~(cacheline_size - 1);
	memset(cacheline, 0, sizeof(cacheline));

	while (cleared < cacheline_size) {
		int to_clear = cacheline_size < sizeof(cacheline)?
		    cacheline_size : sizeof(cacheline);
#ifdef MODE32
		unsigned char *page = cpu->cd.ppc.host_store[addr >> 12];
		if (page != NULL) {
			memset(page + (addr & 0xfff), 0, to_clear);
		} else
#endif
		if (cpu->memory_rw(cpu, cpu->mem, addr, cacheline,
		    to_clear, MEM_WRITE, CACHE_DATA) != MEMORY_ACCESS_OK) {
			/*  exception  */
			return;
		}

		cleared += to_clear;
		addr += to_clear;
	}
}


/*
 *  mtfsf:  Copy FPR into the FPSCR.
 *
 *  arg[0] = ptr to frb
 *  arg[1] = mask
 */
X(mtfsf)
{
	CHECK_FOR_FPU_EXCEPTION;
	cpu->cd.ppc.fpscr &= ~ic->arg[1];
	cpu->cd.ppc.fpscr |= (ic->arg[1] & (*(uint64_t *)ic->arg[0]));
	ppc_fpscr_recompute(cpu);	/*  #327  */
}


/*
 *  mffs:  Copy FPSCR into a FPR.
 *
 *  arg[0] = ptr to frt
 */
X(mffs)
{
	CHECK_FOR_FPU_EXCEPTION;
	(*(uint64_t *)ic->arg[0]) = cpu->cd.ppc.fpscr;
}


/*
 *  fmr:  Floating-point Move
 *
 *  arg[0] = ptr to frb
 *  arg[1] = ptr to frt
 */
X(fmr)
{
	/*
	 *  This works like a normal register to register copy, but
	 *  a) it can cause an FPU exception, and b) the move is always
	 *  64-bit, even when running in 32-bit mode.
	 */
	CHECK_FOR_FPU_EXCEPTION;
	*(uint64_t *)ic->arg[1] = *(uint64_t *)ic->arg[0];
}


/*
 *  #326: the FPSCR control group -- mtfsb0, mtfsb1, mtfsfi and mcrfs. None
 *  was decoded, so each stopped the emulator on a legal encoding. Their
 *  absence mattered more than the count suggests: Book I names mcrfs,
 *  mtfsfi, mtfsf and mtfsb0 as the only four instructions that may clear a
 *  sticky exception bit, and three of those four did not exist.
 *
 *  Two rules from the FPSCR bit definitions govern all of them:
 *
 *    - FEX (bit 1) and VX (bit 2) are OR summaries. Book I: "mcrfs, mtfsfi,
 *      mtfsf, mtfsb0, and mtfsb1 cannot alter FPSCR FEX / VX explicitly."
 *      All five mask those two bits out of whatever they write, mtfsf
 *      included as of #327 -- and the two halves landed together, which
 *      the #326 version of this comment said they had to. Masking mtfsf
 *      alone would have made things worse: this fork used to STORE FEX and
 *      VX rather than derive them, so nothing lowered VX when the last
 *      cause was cleared, and mtfsf's unmasked write was the only escape
 *      from the resulting phantom. #327 added ppc_fpscr_recompute(), so
 *      the escape is no longer needed and the summaries follow the causes
 *      in both directions.
 *    - FX (bit 0) is implicitly set by "every floating-point instruction,
 *      EXCEPT mtfsfi and mtfsf", when that instruction drives an exception
 *      bit from 0 to 1. mtfsb1 is therefore subject to it; mtfsfi is not,
 *      and takes FX only from the immediate it was given.
 */
#define	PPC_FPSCR_SUMMARY	(PPC_FPSCR_FEX | PPC_FPSCR_VX)

/*  PPC_FPSCR_EXC_BITS moved to cpu_ppc.h in #330: ppc_fpscr_raise()
    needs it, and this file is compiled twice so it cannot live here.  */


/*
 *  mtfsb1:  Move To FPSCR Bit 1        #326
 *
 *  arg[0] = BT, the ISA bit number (0..31)
 */
X(mtfsb1)
{
	uint32_t bit = (uint32_t)1 << (31 - (int)ic->arg[0]);

	CHECK_FOR_FPU_EXCEPTION;

	/*  "Bits 1 and 2 (FEX and VX) cannot be explicitly set."  */
	if (bit & PPC_FPSCR_SUMMARY)
		return;

	/*  Subject to the implicit-FX rule: driving an exception bit from 0
	    to 1 sets FX too.  */
	if ((bit & PPC_FPSCR_EXC_BITS) && !(cpu->cd.ppc.fpscr & bit))
		cpu->cd.ppc.fpscr |= PPC_FPSCR_FX;

	cpu->cd.ppc.fpscr |= bit;
	ppc_fpscr_recompute(cpu);	/*  #327  */
}


/*
 *  mtfsb0:  Move To FPSCR Bit 0        #326
 *
 *  arg[0] = BT, the ISA bit number (0..31)
 */
X(mtfsb0)
{
	uint32_t bit = (uint32_t)1 << (31 - (int)ic->arg[0]);

	CHECK_FOR_FPU_EXCEPTION;

	/*  "Bits 1 and 2 (FEX and VX) cannot be explicitly reset."  */
	if (bit & PPC_FPSCR_SUMMARY)
		return;

	cpu->cd.ppc.fpscr &= ~bit;
	ppc_fpscr_recompute(cpu);	/*  #327  */
}


/*
 *  mtfsfi:  Move To FPSCR Field Immediate      #326
 *
 *  arg[0] = shift of the target field (28 - 4*BF)
 *  arg[1] = the four-bit immediate U
 */
X(mtfsfi)
{
	int shift = ic->arg[0];
	uint32_t mask = ((uint32_t)0xf << shift) & ~PPC_FPSCR_SUMMARY;

	CHECK_FOR_FPU_EXCEPTION;

	cpu->cd.ppc.fpscr &= ~mask;
	cpu->cd.ppc.fpscr |= (((uint32_t)ic->arg[1] << shift) & mask);
	ppc_fpscr_recompute(cpu);	/*  #327  */
}


/*
 *  mcrfs:  Move to Condition Register from FPSCR       #326
 *
 *  arg[0] = shift of the destination CR field (28 - 4*BF)
 *  arg[1] = shift of the source FPSCR field  (28 - 4*BFA)
 *  arg[2] = exactly which bits this BFA clears
 *
 *  The source field is copied into CR field BF, and the exception bits that
 *  were copied are then cleared -- but ONLY those. Clearing the whole
 *  four-bit field would be guest-visible damage in four separate places:
 *  field 3 also holds FR and FI (it clears VXVC only), and THREE fields --
 *  4, 6 and 7 -- clear nothing at all. Those three are the ones that would
 *  hurt most: field 4 IS the FPCC (the last compare result), field 6 is the
 *  exception ENABLES, and field 7 holds the ROUNDING MODE that #304's frsp
 *  reads -- so a blanket `mcrfs x,7` would silently reset the guest to
 *  round-to-nearest. Which bits each BFA clears is a table in Book I;
 *  computed once at decode and carried in arg[2].
 */
X(mcrfs)
{
	int dst_shift = ic->arg[0], src_shift = ic->arg[1];
	uint32_t field = (cpu->cd.ppc.fpscr >> src_shift) & 0xf;

	CHECK_FOR_FPU_EXCEPTION;

	cpu->cd.ppc.cr &= ~((uint32_t)0xf << dst_shift);
	cpu->cd.ppc.cr |= (field << dst_shift);

	/*  Never the summary bits, whatever the table says.  */
	cpu->cd.ppc.fpscr &= ~((uint32_t)ic->arg[2] & ~PPC_FPSCR_SUMMARY);
	ppc_fpscr_recompute(cpu);	/*  #327  */
}


/*
 *  fnabs:  Floating-point Negative Absolute Value      #326
 *
 *  PPC_63_FNABS was defined in opcodes_ppc.h all along with no case in the
 *  decoder. The define alone does nothing, so this halted the emulator.
 *
 *  Sign surgery in the style of fabs and fneg, and it has to stay bit
 *  transport: going through ieee_interpret_float_value would collapse every
 *  NaN to the host's NAN and lose the payload. OR, not XOR -- the result is
 *  negative for every operand, so a negative input stays negative.
 *
 *  arg[0] = ptr to frb
 *  arg[1] = ptr to frt
 */
X(fnabs)
{
	uint64_t v;
	CHECK_FOR_FPU_EXCEPTION;
	v = *(uint64_t *)ic->arg[0];
	*(uint64_t *)ic->arg[1] = v | 0x8000000000000000ULL;
}


/*
 *  fsel:  Floating-point Select        #326
 *
 *  FRT = (FRA >= 0.0 and FRA is not a NaN) ? FRC : FRB.
 *
 *  Bit transport, for the same reason as fnabs: the selected operand is
 *  moved unchanged, payload and all. The sign of zero needs no special
 *  handling -- the ISA selects FRC for -0.0, and C's `-0.0 >= 0.0` is true,
 *  so the plain comparison already agrees. The NaN test is the one that has
 *  to be explicit, and a NaN selects FRB.
 *
 *  Four register operands and only three args, so the instruction word is
 *  carried in arg[2] and frb/frc read out of it -- the same shape fmadd uses.
 *
 *  arg[0] = ptr to frt
 *  arg[1] = ptr to fra
 *  arg[2] = the instruction word
 */
X(fsel)
{
	uint32_t iw = ic->arg[2];
	int b = (iw >> 11) & 31, c = (iw >> 6) & 31;
	struct ieee_float_value fra;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &fra, IEEE_FMT_D);

	*(uint64_t *)ic->arg[0] = (!fra.nan && fra.f >= 0.0)
	    ? cpu->cd.ppc.fpr[c] : cpu->cd.ppc.fpr[b];
}


/*
 *  fabs:  Floating-point Absulute Value
 *
 *  arg[0] = ptr to frb
 *  arg[1] = ptr to frt
 */
X(fabs)
{
	uint64_t v;
	CHECK_FOR_FPU_EXCEPTION;
	v = *(uint64_t *)ic->arg[0];
	*(uint64_t *)ic->arg[1] = v & 0x7fffffffffffffffULL;
}


/*
 *  fneg:  Floating-point Negate
 *
 *  arg[0] = ptr to frb
 *  arg[1] = ptr to frt
 */
X(fneg)
{
	uint64_t v;
	CHECK_FOR_FPU_EXCEPTION;
	v = *(uint64_t *)ic->arg[0];
	*(uint64_t *)ic->arg[1] = v ^ 0x8000000000000000ULL;
}


/*
 *  fcmpu:  Floating-point Compare Unordered
 *
 *  arg[0] = 28 - 4*bf  (bitfield shift)
 *  arg[1] = ptr to fra
 *  arg[2] = ptr to frb
 */
X(fcmpu)
{
	struct ieee_float_value fra, frb;
	int bf_shift = ic->arg[0], c = 0;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &fra, IEEE_FMT_D);
	ieee_interpret_float_value(*(uint64_t *)ic->arg[2], &frb, IEEE_FMT_D);

	/*
	 *  #330: fcmpu owes VXSNAN for a signalling operand and NOTHING
	 *  else, ever. VXVC belongs exclusively to fcmpo, which is not
	 *  decoded at all yet (it halts the emulator; filed separately).
	 *  This is what the old `TODO: Signaling vs Quiet NaN` marked.
	 */
	if (ppc_is_snan(*(uint64_t *)ic->arg[1])
	    || ppc_is_snan(*(uint64_t *)ic->arg[2]))
		ppc_fpscr_raise(cpu, PPC_FPSCR_VXNAN);
	if (fra.nan | frb.nan) {
		c = 1;
	} else {
		if (fra.f < frb.f)
			c = 8;
		else if (fra.f > frb.f)
			c = 4;
		else
			c = 2;
	}
	/*  TODO: Signaling vs Quiet NaN  */

	/*
	 *  #326: the mask used to be `c & 0xe`, which discarded the UNORDERED
	 *  bit -- the one result this instruction exists to report. `c` is one
	 *  of 8/4/2/1 (LT/GT/EQ/FU), so an unordered compare wrote 0000 into
	 *  the CR field: neither less, greater, equal, NOR unordered, which is
	 *  a state hardware never produces. Measured, with the ordered rows as
	 *  controls: 1.0<2.0, 2.0>1.0 and 1.0==1.0 all gave the right nibble;
	 *  both NaN rows gave 0 where the ISA owes 1.
	 *
	 *  The mask is deleted rather than widened to 0xf, because `c` is
	 *  already exactly four bits. It reads like a transplanted template:
	 *  the INTEGER compares build the same 8/4/2 and then OR XER.SO into
	 *  the low bit, where masking off "the bit I am not supplying" is
	 *  sensible. In a floating-point compare that low bit is FU, a result.
	 */
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= ((uint32_t)c << bf_shift);

	/*
	 *  #326: FPCC is status and is rewritten by every compare, but VXSNAN
	 *  is STICKY and must not be cleared here. Book I: the exception bits
	 *  "are sticky; that is, once set to 1 they remain set to 1 until they
	 *  are set to 0 by an mcrfs, mtfsfi, mtfsf, or mtfsb0 instruction".
	 *  fcmpu is none of those four, and clearing it here erased the record
	 *  #304 had just gone to the trouble of setting.
	 */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (c << PPC_FPSCR_FPCC_SHIFT);
}


#ifndef PPC_SINGLE_NARROW_INCLUDED
#define PPC_SINGLE_NARROW_INCLUDED

/*
 *  ppc_single_narrow():  #304 -- the FINITE half of the PowerPC's
 *  double -> single narrowing, as exact bit surgery.
 *
 *  Returns the 32-bit single pattern for a finite double, rounded under `rm`
 *  (an IEEE_RM_* value, which for this CPU is just `fpscr & PPC_FPSCR_RN_MASK`).
 *  Specials never reach here: the callers handle NaN and Infinity themselves,
 *  because those classes are pattern transport, not arithmetic.
 *
 *  Why bit surgery rather than the host's own float:  a host cast rounds under
 *  the HOST's mode -- nearest, always -- which is exactly the defect this fixes,
 *  and no portable C construct rounds to single under a caller-chosen mode.
 *  Every step below is exact integer work on the significand.
 *
 *  The three ranges, and the rounding they share:
 *
 *    normal      the significand keeps 24 bits; the discarded tail decides.
 *    subnormal   the exponent is pinned at the format minimum and the
 *                significand shifts right, so the tail grows -- this is the
 *                band `stfs` truncates and `frsp` rounds.
 *    underflow   everything shifts out; only the directed modes can still
 *                deliver the smallest subnormal, on the side they round toward.
 *
 *  Rounding is decided once, from (guard, sticky, lsb, sign), and applied by
 *  incrementing the significand.  The increment is allowed to carry out of the
 *  fraction and into the exponent -- that is how a subnormal at the top of the
 *  band becomes the smallest NORMAL, and how the largest finite single becomes
 *  Infinity, with no special case for either.
 */
static uint32_t ppc_single_narrow(uint64_t d, int rm)
{
	int sign = (int) (d >> 63) & 1;
	int exp = (int) ((d >> 52) & 0x7ff);
	uint64_t frac = d & 0xfffffffffffffULL;
	uint64_t sig;			/*  significand, 24 bits wide when normal  */
	int e;				/*  the single's biased exponent  */
	int shift, round_up = 0;
	uint64_t guard_sticky = 0;

	if (exp == 0 && frac == 0)
		return (uint32_t) sign << 31;		/*  +/-0 passes through  */

	/*  Unbias to the single's frame.  A D subnormal (exp 0) is far below the
	    single format's reach, so it lands in the underflow arm below.  */
	sig = (exp == 0) ? frac : (frac | (1ULL << 52));
	e = ((exp == 0) ? 1 : exp) - 1023 + 127;

	/*  The significand is 53 bits; single wants 24.  Discard 29 -- more when
	    the value is subnormal in the single format (e <= 0), which is the
	    denormalization the ISA spells out step by step.  */
	shift = 29;
	if (e <= 0) {
		shift += 1 - e;
		e = 0;
		if (shift > 63) {
			/*  Everything shifts out.  Only a directed mode toward
			    this value's own sign can still deliver the smallest
			    subnormal; nearest and toward-zero give signed 0.  */
			if ((rm == IEEE_RM_RP && !sign) ||
			    (rm == IEEE_RM_RM && sign))
				return ((uint32_t) sign << 31) | 1;
			return (uint32_t) sign << 31;
		}
	}

	guard_sticky = sig & ((1ULL << shift) - 1);
	sig >>= shift;

	switch (rm) {
	case IEEE_RM_RN:
		{
			uint64_t half = 1ULL << (shift - 1);
			if (guard_sticky > half ||
			    (guard_sticky == half && (sig & 1)))
				round_up = 1;
		}
		break;
	case IEEE_RM_RP:
		round_up = (guard_sticky != 0) && !sign;
		break;
	case IEEE_RM_RM:
		round_up = (guard_sticky != 0) && sign;
		break;
	default:	/*  IEEE_RM_RZ and the legacy value: discard the tail  */
		break;
	}

	if (round_up) {
		sig ++;
		/*  A carry out of the 24-bit significand lifts the exponent --
		    subnormal to smallest-normal, or largest-finite to Infinity --
		    which is why the increment is done on the ASSEMBLED value and
		    not clamped first.  */
		if (sig >> 24) {
			sig >>= 1;
			e ++;
		} else if (e == 0 && (sig >> 23)) {
			e = 1;
			sig &= 0x7fffff;
		}
	}

	if (e >= 255) {
		/*  Overflow is mode-dependent (IEEE 754 s7.4, and the ISA follows
		    it): nearest carries to Infinity, toward-zero stops at the
		    largest finite value, and each directed mode gives Infinity on
		    the side it rounds toward.  */
		int to_inf = 1;
		switch (rm) {
		case IEEE_RM_RZ: to_inf = 0; break;
		case IEEE_RM_RP: to_inf = !sign; break;
		case IEEE_RM_RM: to_inf = sign; break;
		}
		if (to_inf)
			return ((uint32_t) sign << 31) | 0x7f800000;
		return ((uint32_t) sign << 31) | 0x7f7fffff;
	}

	return ((uint32_t) sign << 31) | ((uint32_t) e << 23) |
	    (uint32_t) (sig & 0x7fffff);
}


/*
 *  ppc_single_widen():  #305 -- the exact single -> double pattern conversion,
 *  including the classes the value domain cannot carry.
 *
 *  NaN is the reason this exists: a NaN's payload and sign are DATA, and the
 *  interpret/store pair destroys both (interpret reports only "is a NaN", and
 *  the store canonicalizes to all-ones).  Measured before #305: a single qNaN
 *  0xffc00001 widened to 0x7fffffffffffffff -- wrong sign, wrong payload.
 */
static uint64_t ppc_single_widen(uint32_t s)
{
	uint64_t sign = (uint64_t) (s >> 31) & 1;
	uint32_t exp = (s >> 23) & 0xff;
	uint32_t frac = s & 0x7fffff;
	struct ieee_float_value val;

	if (exp == 0xff) {
		/*  Infinity and NaN: exponent all-ones, fraction shifted into
		    place. The single's 23 fraction bits are the TOP 23 of the
		    double's 52, which is the same alignment the store's splice
		    uses in the other direction.  */
		return (sign << 63) | 0x7ff0000000000000ULL |
		    ((uint64_t) frac << 29);
	}

	/*  Finite: the value domain is exact for every single, subnormals
	    included, since #303 taught the decode to read them properly.  */
	ieee_interpret_float_value(s, &val, IEEE_FMT_S);
	return ieee_store_float_value(val.f, IEEE_FMT_D);
}
#endif	/*  PPC_SINGLE_NARROW_INCLUDED  */


/*
 *  frsp:  Floating-point Round to Single Precision
 *
 *  arg[0] = ptr to frb
 *  arg[1] = ptr to frt
 */
X(frsp)
{
	uint64_t frb_bits, res;
	int c = 0;

	CHECK_FOR_FPU_EXCEPTION;

	frb_bits = *(uint64_t *)ic->arg[0];

	/*
	 *  #304/#305: the narrowing is done on the PATTERN, under the mode the
	 *  guest asked for.  What it replaces was `float fl = frb.f` -- a host
	 *  cast, which rounds to nearest whatever FPSCR says, so the three
	 *  directed modes were unreachable and the ISA's denormalization band
	 *  was rounded by the host instead of the emulated FPU.  The NaN arm is
	 *  worse than mode-blind: it left `fl` at its initialiser, so EVERY NaN
	 *  was delivered as +0.0 (measured).
	 *
	 *  The classes, per Book I's Round-to-Single-Precision model:
	 *    NaN   the fraction truncates to the single's 23 bits and re-widens;
	 *          a signalling NaN is quieted and sets VXSNAN.  The payload and
	 *          sign are DATA and must survive.
	 *    Inf   passes through untouched.
	 *    else  round to single under FPSCR, then widen exactly.
	 */
	if ((frb_bits & 0x7ff0000000000000ULL) == 0x7ff0000000000000ULL &&
	    (frb_bits & 0xfffffffffffffULL) != 0) {
		/*  NaN.  Truncate to what a single can hold; quiet it if it
		    arrived signalling.  Without the quiet bit a signalling NaN
		    whose payload lives entirely in the discarded low bits would
		    collapse to Infinity -- the class would be lost, not just
		    the payload.  */
		int snan = !(frb_bits & 0x8000000000000ULL);
		res = frb_bits & ~0x1fffffffULL;
		if (snan) {
			res |= 0x8000000000000ULL;
			/*  VXSNAN is a STICKY exception bit: hardware sets it
			    and leaves it set until the guest clears it through
			    mtfsf/mcrfs, and VX is the OR-summary of the whole
			    invalid-operation group while FX latches the 0->1
			    transition.  The first version of this arm set
			    VXSNAN alone and the arm below then cleared it on
			    the next non-NaN frsp, so `frsp(sNaN); frsp(1.0)`
			    lost the record entirely -- worse than never
			    setting it (a diff-review seat's finding; there is
			    a gate row for the stickiness now).  Nothing here
			    implies the TRAP side works: the enable bits
			    (VE/OE/UE) remain unmodelled and stated as such.  */
			/*
			 *  #327: FX latches only on a 0->1 TRANSITION of an
			 *  exception bit. VXSNAN is sticky, so a second
			 *  signalling NaN after the guest has explicitly
			 *  cleared FX must NOT set it again -- this used to
			 *  set FX unconditionally.
			 */
			if (!(cpu->cd.ppc.fpscr & PPC_FPSCR_VXNAN))
				cpu->cd.ppc.fpscr |= PPC_FPSCR_FX;

			cpu->cd.ppc.fpscr |= PPC_FPSCR_VXNAN;

			/*
			 *  #327: and derive the summaries rather than leaving
			 *  them to whatever happened to be stored. Setting VX
			 *  by hand was right as far as it went, but nothing
			 *  here ever raised FEX, so an enabled invalid
			 *  operation left FEX clear no matter how the guest
			 *  got there.
			 *
			 *  An earlier draft of this comment claimed the old
			 *  code was ORDER-DEPENDENT here. It was not, and the
			 *  claim was never measured: with no recompute on
			 *  either path, `mtfsb1 24; frsp(sNaN)` and
			 *  `frsp(sNaN); mtfsb1 24` both answered a1001080 --
			 *  agreeing, and both missing FEX. The two gate rows
			 *  are kept because order-independence is worth
			 *  pinning now that FEX moves at all, not because
			 *  they caught a disagreement.
			 */
			ppc_fpscr_recompute(cpu);
		}
		c = 1;
	} else if ((frb_bits & 0x7fffffffffffffffULL) ==
	    0x7ff0000000000000ULL) {
		res = frb_bits;				/*  +/-Inf  */
		c = (frb_bits >> 63) ? 8 : 4;
	} else {
		uint32_t narrowed = ppc_single_narrow(frb_bits,
		    cpu->cd.ppc.fpscr & PPC_FPSCR_RN_MASK);
		res = ppc_single_widen(narrowed);
		if (res & 0x8000000000000000ULL)
			c = ((res << 1) == 0) ? 2 : 8;
		else
			c = (res == 0) ? 2 : 4;
	}

	/*  FPCC reports the class of the RESULT, so a value that rounded away to
	    zero -- or up off zero under a directed mode -- reports what the guest
	    can actually see in the register.  FPCC is a status field and is
	    rewritten every time; the exception bits above are NOT, which is the
	    whole difference between the two and why only this line clears.  */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (c << PPC_FPSCR_FPCC_SHIFT);

	(*(uint64_t *)ic->arg[1]) = res;
}


/*
 *  ppc_convert_to_word():  #326
 *
 *  The body shared by fctiw and fctiwz. The two differ only in the rounding
 *  mode: fctiwz forces toward-zero, fctiw takes FPSCR[RN].
 *
 *  The saturation is SIGN-DEPENDENT, and that is the trap in this function.
 *  It is tempting to hand the operand to ieee_store_float_value_rm() with
 *  IEEE_FMT_W, which already rounds per mode and range-checks -- but that
 *  path implements the MIPS contract (#273), where a NaN and BOTH overflow
 *  directions all return 0x7fffffff with no sign dependence. PowerPC owes
 *  0x7FFF_FFFF only for a positive out-of-range operand; a negative one and
 *  every NaN owe 0x8000_0000 (Book I, Appendix A.2: Infinity Operand and
 *  Large Operand branch on sign, SNaN and QNaN do not). Reusing the MIPS
 *  entry point would silently give PowerPC the wrong answer for exactly the
 *  cases #325 was about.
 *
 *  Rounding happens before the range test, as the ISA model does -- but only
 *  for the three directed modes. ieee_round_to_integral() deliberately
 *  returns RZ operands untouched and lets the cast truncate, so under RZ
 *  the range test still sees the UNROUNDED value: 2147483647.9 takes the
 *  saturation branch although its converted value, 2147483647, is in range.
 *  The 32-bit result is identical either way, because the saturation value
 *  equals the boundary -- so nothing is wrong today. It stops being
 *  harmless the moment these branches drive VXCVI or FR/FI, which would
 *  then be raised for operands that are perfectly convertible. Whoever
 *  adds the status bits must round RZ explicitly here first; this comment
 *  previously claimed they could be added without restructuring, and that
 *  was wrong.
 */
#ifndef PPC_CONVERT_TO_WORD_INCLUDED
#define PPC_CONVERT_TO_WORD_INCLUDED
static uint32_t ppc_convert_to_word(struct cpu *cpu, uint64_t frb_bits, int rm)
{
	struct ieee_float_value frb;
	double nf;

	ieee_interpret_float_value(frb_bits, &frb, IEEE_FMT_D);

	/*  #325: a NaN converts to the most negative value, not to zero.
	    Zero is the worse kind of wrong -- a legitimate result the guest
	    cannot tell apart from a successful conversion of 0.0.  */
	/*
	 *  #330: VXCVI, and VXSNAN for a signalling operand. The RESULT
	 *  branches below are unchanged -- what is new is that the exception
	 *  is now recorded, and it is classified SEPARATELY from them.
	 *
	 *  That separation is the whole point. Reusing the saturation
	 *  branches as the predicate would misclassify three ways, two of them
	 *  in every rounding mode: `>= 2147483647.0` fires on exactly 2^31-1
	 *  and `<= -2147483648.0` on exactly -2^31, both of which convert
	 *  perfectly, and under RZ the test sees an UNROUNDED value because
	 *  ieee_round_to_integral() deliberately passes RZ through, so
	 *  2147483647.9 would be called invalid although it truncates in
	 *  range. The predicate therefore rounds under the real mode first --
	 *  trunc() for RZ, which is host-mode-independent -- and then uses
	 *  STRICT inequalities.
	 */
	{
		uint32_t causes = 0;
		double r;

		if (ppc_is_snan(frb_bits))
			causes |= PPC_FPSCR_VXNAN;

		r = (rm == IEEE_RM_RZ) ? trunc(frb.f)
		    : ieee_round_to_integral(frb.f, rm);

		if (frb.nan || r > 2147483647.0 || r < -2147483648.0)
			causes |= PPC_FPSCR_VXCVI;

		if (causes)
			ppc_fpscr_raise(cpu, causes);
	}

	if (frb.nan)
		return 0x80000000;

	nf = ieee_round_to_integral(frb.f, rm);

	if (nf >= 2147483647.0)
		return 0x7fffffff;
	if (nf <= -2147483648.0)
		return 0x80000000;

	return (uint32_t)(int32_t) nf;
}
#endif	/*  PPC_CONVERT_TO_WORD_INCLUDED  */


/*
 *  fctiwz:  Floating-point Convert to Integer Word, Round to Zero
 *
 *  arg[0] = ptr to frb
 *  arg[1] = ptr to frt
 */
X(fctiwz)
{
	CHECK_FOR_FPU_EXCEPTION;

	*(uint64_t *)ic->arg[1] = ppc_convert_to_word(cpu,
	    *(uint64_t *)ic->arg[0], IEEE_RM_RZ);
}


/*
 *  fctiw:  Floating-point Convert to Integer Word     #326
 *
 *  Identical to fctiwz except that it rounds per FPSCR[RN] instead of
 *  toward zero. It was not decoded at all, so a legal encoding stopped the
 *  emulator.
 *
 *  arg[0] = ptr to frb
 *  arg[1] = ptr to frt
 */
X(fctiw)
{
	CHECK_FOR_FPU_EXCEPTION;

	*(uint64_t *)ic->arg[1] = ppc_convert_to_word(cpu,
	    *(uint64_t *)ic->arg[0],
	    cpu->cd.ppc.fpscr & PPC_FPSCR_RN_MASK);
}


/*
 *  fmul:  Floating-point Multiply
 *
 *  arg[0] = ptr to frt
 *  arg[1] = ptr to fra
 *  arg[2] = ptr to frc
 */
X(fmul)
{
	struct ieee_float_value fra;
	struct ieee_float_value frc;
	double result = 0.0;
	int c;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &fra, IEEE_FMT_D);
	ieee_interpret_float_value(*(uint64_t *)ic->arg[2], &frc, IEEE_FMT_D);

	/*
	 *  #330. NOTE the operands are arg[1] and arg[2] here -- arg[0] is
	 *  the DESTINATION. fadd/fsub/fdiv use arg[0] and arg[1] instead, so
	 *  a shared operand macro across these handlers would have
	 *  classified fmul's target register. A review seat caught that
	 *  before it was written.
	 */
	{
		uint32_t cause = ppc_invalid_cause(*(uint64_t *)ic->arg[1],
		    *(uint64_t *)ic->arg[2], PPC_INVOP_MUL);
		if (cause)
			ppc_fpscr_raise(cpu, cause);
	}
	/*  #336: honour FPSCR[RN]; see the note on fadd.  */
	result = ieee_mul_round_rm(fra.f, frc.f, (cpu->cd.ppc.fpscr & PPC_FPSCR_RN_MASK));
	if (isnan(result))
		c = 1;
	else {
		if (result < 0.0)
			c = 8;
		else if (result > 0.0)
			c = 4;
		else
			c = 2;
	}
	/*  TODO: Signaling vs Quiet NaN  */
	/*
	 *  #326: FPCC is status and is rewritten here; VXSNAN is STICKY and
	 *  is not ours to clear. Book I lists exactly four instructions that
	 *  may clear an exception bit -- mcrfs, mtfsfi, mtfsf, mtfsb0 -- and
	 *  this is not one of them. Clearing it here meant any arithmetic
	 *  following a signalling-NaN operation erased the record.
	 */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (c << PPC_FPSCR_FPCC_SHIFT);

	(*(uint64_t *)ic->arg[0]) =
	    ieee_store_float_value(result, IEEE_FMT_D);
}
X(fmuls)
{
	/*  TODO  */
	instr(fmul)(cpu, ic);
}


/*
 *  fmadd:  Floating-point Multiply and Add
 *
 *  arg[0] = ptr to frt
 *  arg[1] = ptr to fra
 *  arg[2] = copy of the instruction word
 */
X(fmadd)
{
	uint32_t iw = ic->arg[2];
	int b = (iw >> 11) & 31, c = (iw >> 6) & 31;
	struct ieee_float_value fra;
	struct ieee_float_value frb;
	struct ieee_float_value frc;
	double result = 0.0;
	int cc;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &fra, IEEE_FMT_D);
	ieee_interpret_float_value(cpu->cd.ppc.fpr[b], &frb, IEEE_FMT_D);
	ieee_interpret_float_value(cpu->cd.ppc.fpr[c], &frc, IEEE_FMT_D);
	/*  #335: fmadd is architecturally FUSED -- Book I defines it as rounding
	    the product-sum EXACTLY ONCE -- and `fra.f * frc.f + frb.f` rounds
	    twice unless the compiler happens to contract it into a hardware FMA.
	    That made this instruction's correctness a property of the BUILD HOST
	    rather than of this source: gate 2 asserts only that the generated
	    Makefiles do not ADD -ffp-contract=fast, which cannot see GCC's own
	    GNU-mode default, and on a baseline x86-64 target there is no FMA
	    instruction to contract into at all. Measured on this build with the
	    guest's own instruction: (1+2^-52)*(1-2^-52) + -1.0 answered
	    0000000000000000 where the ISA owes b970000000000000 (-2^-104) -- the
	    exact product needs 104 significant bits, so the first rounding
	    destroys it and the second has nothing left to keep. fma() rounds once
	    by definition, which is both the correct answer and the same answer on
	    every build host.

	    fma() rounds per the HOST mode, i.e. nearest. That is exactly right
	    while FPSCR[RN] remains unwired here -- no PowerPC arithmetic in this
	    tree reads it -- but it is NOT strictly better in every case: a review
	    seat produced an operand set where the old double rounding happened to
	    land on the toward-zero answer and the fused one does not
	    (a = 1+31u, c = 1+u, b = -1, u = 2^-52). Accidentally right is not a
	    property worth keeping, and directed-mode arithmetic is unsupported
	    either way, but the claim "no worse" would have been false.  */
	result = fma(fra.f, frc.f, frb.f);
	if (isnan(result))
		cc = 1;
	else {
		if (result < 0.0)
			cc = 8;
		else if (result > 0.0)
			cc = 4;
		else
			cc = 2;
	}
	/*  TODO: Signaling vs Quiet NaN  */
	/*
	 *  #326: FPCC is status and is rewritten here; VXSNAN is STICKY and
	 *  is not ours to clear. Book I lists exactly four instructions that
	 *  may clear an exception bit -- mcrfs, mtfsfi, mtfsf, mtfsb0 -- and
	 *  this is not one of them. Clearing it here meant any arithmetic
	 *  following a signalling-NaN operation erased the record.
	 */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (cc << PPC_FPSCR_FPCC_SHIFT);

	(*(uint64_t *)ic->arg[0]) =
	    ieee_store_float_value(result, IEEE_FMT_D);
}


/*
 *  fmsub:  Floating-point Multiply and Sub
 *
 *  arg[0] = ptr to frt
 *  arg[1] = ptr to fra
 *  arg[2] = copy of the instruction word
 */
X(fmsub)
{
	uint32_t iw = ic->arg[2];
	int b = (iw >> 11) & 31, c = (iw >> 6) & 31;
	struct ieee_float_value fra;
	struct ieee_float_value frb;
	struct ieee_float_value frc;
	double result = 0.0;
	int cc;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &fra, IEEE_FMT_D);
	ieee_interpret_float_value(cpu->cd.ppc.fpr[b], &frb, IEEE_FMT_D);
	ieee_interpret_float_value(cpu->cd.ppc.fpr[c], &frc, IEEE_FMT_D);
	/*  #335: fmsub is fmadd with frB negated, and is fused for the same
	    reason -- see the note there. Negating the ADDEND rather than the
	    result is what keeps it a single fused operation.  */
	result = fma(fra.f, frc.f, -frb.f);
	if (isnan(result))
		cc = 1;
	else {
		if (result < 0.0)
			cc = 8;
		else if (result > 0.0)
			cc = 4;
		else
			cc = 2;
	}
	/*  TODO: Signaling vs Quiet NaN  */
	/*
	 *  #326: FPCC is status and is rewritten here; VXSNAN is STICKY and
	 *  is not ours to clear. Book I lists exactly four instructions that
	 *  may clear an exception bit -- mcrfs, mtfsfi, mtfsf, mtfsb0 -- and
	 *  this is not one of them. Clearing it here meant any arithmetic
	 *  following a signalling-NaN operation erased the record.
	 */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (cc << PPC_FPSCR_FPCC_SHIFT);

	(*(uint64_t *)ic->arg[0]) =
	    ieee_store_float_value(result, IEEE_FMT_D);
}


/*
 *  fadd, fsub, fdiv:  Various Floating-point operationgs
 *
 *  arg[0] = ptr to fra
 *  arg[1] = ptr to frb
 *  arg[2] = ptr to frt
 */
X(fadd)
{
	struct ieee_float_value fra;
	struct ieee_float_value frb;
	double result = 0.0;
	int c;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[0], &fra, IEEE_FMT_D);
	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &frb, IEEE_FMT_D);

	/*
	 *  #330: the invalid-operation cause, from the OPERANDS.
	 *  Measured before this round: this instruction raised nothing
	 *  at all, so VX and FEX -- correct since #327 -- derived over
	 *  an empty cause set.
	 */
	{
		uint32_t cause = ppc_invalid_cause(*(uint64_t *)ic->arg[0], *(uint64_t *)ic->arg[1],
		    PPC_INVOP_ADD);
		if (cause)
			ppc_fpscr_raise(cpu, cause);
	}
	/*  #336: PowerPC double arithmetic computed in host double under the
	    HOST rounding mode and never read FPSCR[RN] -- only the conversions
	    frsp and fctiw did. Measured: 1.0 + 3*2^-54 under RZ answered
	    3ff0000000000001, the nearest result, where toward-zero owes
	    3ff0000000000000. #300's helpers already serve MIPS, SH and m88k.  */
	result = ieee_add_round_rm(fra.f, frb.f, (cpu->cd.ppc.fpscr & PPC_FPSCR_RN_MASK));
	if (isnan(result))
		c = 1;
	else {
		if (result < 0.0)
			c = 8;
		else if (result > 0.0)
			c = 4;
		else
			c = 2;
	}
	/*  TODO: Signaling vs Quiet NaN  */
	/*
	 *  #326: FPCC is status and is rewritten here; VXSNAN is STICKY and
	 *  is not ours to clear. Book I lists exactly four instructions that
	 *  may clear an exception bit -- mcrfs, mtfsfi, mtfsf, mtfsb0 -- and
	 *  this is not one of them. Clearing it here meant any arithmetic
	 *  following a signalling-NaN operation erased the record.
	 */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (c << PPC_FPSCR_FPCC_SHIFT);

	(*(uint64_t *)ic->arg[2]) =
	    ieee_store_float_value(result, IEEE_FMT_D);
}
X(fadds)
{
	/*  TODO  */
	instr(fadd)(cpu, ic);
}
X(fsub)
{
	struct ieee_float_value fra;
	struct ieee_float_value frb;
	double result = 0.0;
	int c;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[0], &fra, IEEE_FMT_D);
	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &frb, IEEE_FMT_D);

	/*
	 *  #330: the invalid-operation cause, from the OPERANDS.
	 *  Measured before this round: this instruction raised nothing
	 *  at all, so VX and FEX -- correct since #327 -- derived over
	 *  an empty cause set.
	 */
	{
		uint32_t cause = ppc_invalid_cause(*(uint64_t *)ic->arg[0], *(uint64_t *)ic->arg[1],
		    PPC_INVOP_SUB);
		if (cause)
			ppc_fpscr_raise(cpu, cause);
	}
	/*  #336: see fadd.  Subtraction is addition of the negated operand,
	    which is exact, so one rounding remains.  */
	result = ieee_add_round_rm(fra.f, -frb.f, (cpu->cd.ppc.fpscr & PPC_FPSCR_RN_MASK));
	if (isnan(result))
		c = 1;
	else {
		if (result < 0.0)
			c = 8;
		else if (result > 0.0)
			c = 4;
		else
			c = 2;
	}
	/*  TODO: Signaling vs Quiet NaN  */
	/*
	 *  #326: FPCC is status and is rewritten here; VXSNAN is STICKY and
	 *  is not ours to clear. Book I lists exactly four instructions that
	 *  may clear an exception bit -- mcrfs, mtfsfi, mtfsf, mtfsb0 -- and
	 *  this is not one of them. Clearing it here meant any arithmetic
	 *  following a signalling-NaN operation erased the record.
	 */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (c << PPC_FPSCR_FPCC_SHIFT);

	(*(uint64_t *)ic->arg[2]) =
	    ieee_store_float_value(result, IEEE_FMT_D);
}
X(fsubs)
{
	/*  TODO  */
	instr(fsub)(cpu, ic);
}
X(fdiv)
{
	struct ieee_float_value fra;
	struct ieee_float_value frb;
	double result = 0.0;
	int c;

	CHECK_FOR_FPU_EXCEPTION;

	ieee_interpret_float_value(*(uint64_t *)ic->arg[0], &fra, IEEE_FMT_D);
	ieee_interpret_float_value(*(uint64_t *)ic->arg[1], &frb, IEEE_FMT_D);

	/*
	 *  #330: the invalid-operation cause, from the OPERANDS.
	 *  Measured before this round: this instruction raised nothing
	 *  at all, so VX and FEX -- correct since #327 -- derived over
	 *  an empty cause set.
	 */
	{
		uint32_t cause = ppc_invalid_cause(*(uint64_t *)ic->arg[0], *(uint64_t *)ic->arg[1],
		    PPC_INVOP_DIV);
		if (!cause && ppc_is_zero(*(uint64_t *)ic->arg[1])
		    && !ppc_is_zero(*(uint64_t *)ic->arg[0])
		    && !ppc_is_inf(*(uint64_t *)ic->arg[0])
		    && !ppc_is_nan(*(uint64_t *)ic->arg[0])) {
			/*  ZX needs a FINITE NONZERO dividend: 0/0 is
			    VXZDZ not ZX, Inf/0 raises nothing, and a
			    NaN dividend is the NaN's business.  */
			cause = PPC_FPSCR_ZX;
		}
		if (cause)
			ppc_fpscr_raise(cpu, cause);
	}
	/*  #336: see fadd.  */
	result = ieee_div_round_rm(fra.f, frb.f, (cpu->cd.ppc.fpscr & PPC_FPSCR_RN_MASK));
	if (isnan(result))
		c = 1;
	else {
		if (result < 0.0)
			c = 8;
		else if (result > 0.0)
			c = 4;
		else
			c = 2;
	}
	/*  TODO: Signaling vs Quiet NaN  */
	/*
	 *  #326: FPCC is status and is rewritten here; VXSNAN is STICKY and
	 *  is not ours to clear. Book I lists exactly four instructions that
	 *  may clear an exception bit -- mcrfs, mtfsfi, mtfsf, mtfsb0 -- and
	 *  this is not one of them. Clearing it here meant any arithmetic
	 *  following a signalling-NaN operation erased the record.
	 */
	cpu->cd.ppc.fpscr &= ~PPC_FPSCR_FPCC;
	cpu->cd.ppc.fpscr |= (c << PPC_FPSCR_FPCC_SHIFT);

	(*(uint64_t *)ic->arg[2]) =
	    ieee_store_float_value(result, IEEE_FMT_D);
}
X(fdivs)
{
	/*  TODO  */
	instr(fdiv)(cpu, ic);
}


/*
 *  llsc: Load-linked and store conditional
 *
 *  arg[0] = copy of the instruction word.
 */
X(llsc)
{
	int iw = ic->arg[0], len = 4, load = 0, xo = (iw >> 1) & 1023;
	int i, rc = iw & 1, rt, ra, rb;
	uint64_t addr = 0, value;
	unsigned char d[8];

	switch (xo) {
	case PPC_31_LDARX:
		len = 8;
		// fall through
	case PPC_31_LWARX:
		load = 1;
		break;
	case PPC_31_STDCX_DOT:
		len = 8;
	case PPC_31_STWCX_DOT:
		break;
	}

	rt = (iw >> 21) & 31;
	ra = (iw >> 16) & 31;
	rb = (iw >> 11) & 31;

	if (ra != 0)
		addr = cpu->cd.ppc.gpr[ra];
	addr += cpu->cd.ppc.gpr[rb];

	if (load) {
		if (rc) {
			fatal("ll: rc-bit set?\n");
			exit(1);
		}
		if (cpu->memory_rw(cpu, cpu->mem, addr, d, len,
		    MEM_READ, CACHE_DATA) != MEMORY_ACCESS_OK) {
			/*  #216: (Codex/Fable) memory_rw() raised a DSI on the
			    faulting lwarx address; let it proceed instead of
			    exit()ing the host.  */
			return;
		}

		value = 0;
		for (i=0; i<len; i++) {
			value <<= 8;
			if (cpu->byte_order == EMUL_BIG_ENDIAN)
				value |= d[i];
			else
				value |= d[len - 1 - i];
		}

		cpu->cd.ppc.gpr[rt] = value;
		cpu->cd.ppc.ll_addr = addr;
		cpu->cd.ppc.ll_bit = 1;
	} else {
		uint32_t old_so = cpu->cd.ppc.spr[SPR_XER] & PPC_XER_SO;
		if (!rc) {
			fatal("sc: rc-bit not set?\n");
			exit(1);
		}

		value = cpu->cd.ppc.gpr[rt];

		/*  "If the store is performed, bits 0-2 of Condition
		    Register Field 0 are set to 0b001, otherwise, they are
		    set to 0b000. The SO bit of the XER is copied to to bit
		    4 of Condition Register Field 0.  */
		if (!cpu->cd.ppc.ll_bit || cpu->cd.ppc.ll_addr != addr) {
			cpu->cd.ppc.cr &= 0x0fffffff;
			if (old_so)
				cpu->cd.ppc.cr |= 0x10000000;
			cpu->cd.ppc.ll_bit = 0;
			return;
		}

		for (i=0; i<len; i++) {
			if (cpu->byte_order == EMUL_BIG_ENDIAN)
				d[len - 1 - i] = value >> (8*i);
			else
				d[i] = value >> (8*i);
		}

		if (cpu->memory_rw(cpu, cpu->mem, addr, d, len,
		    MEM_WRITE, CACHE_DATA) != MEMORY_ACCESS_OK) {
			/*  #216: (Codex/Fable) memory_rw() raised a DSI on the
			    faulting stwcx. address; let it proceed instead of
			    exit()ing the host.  */
			return;
		}

		cpu->cd.ppc.cr &= 0x0fffffff;
		cpu->cd.ppc.cr |= 0x20000000;	/*  success!  */
		if (old_so)
			cpu->cd.ppc.cr |= 0x10000000;

		/*  Clear _all_ CPUs' ll_bits:  */
		for (i=0; i<cpu->machine->ncpus; i++)
			cpu->machine->cpus[i]->cd.ppc.ll_bit = 0;
	}
}


/*
 *  mtsr, mtsrin:  Move To Segment Register [Indirect]
 *
 *  arg[0] = sr number, or for indirect mode: ptr to rb
 *  arg[1] = ptr to rt
 *
 *  TODO: These only work for 32-bit mode!
 */
X(mtsr)
{
	int sr_num = ic->arg[0];
	uint32_t old = cpu->cd.ppc.sr[sr_num];
	cpu->cd.ppc.sr[sr_num] = reg(ic->arg[1]);

	if (cpu->cd.ppc.sr[sr_num] != old)
		cpu->invalidate_translation_caches(cpu, ic->arg[0] << 28,
		    INVALIDATE_ALL | INVALIDATE_VADDR_UPPER4);
}
X(mtsrin)
{
	int sr_num = reg(ic->arg[0]) >> 28;
	uint32_t old = cpu->cd.ppc.sr[sr_num];
	cpu->cd.ppc.sr[sr_num] = reg(ic->arg[1]);

	if (cpu->cd.ppc.sr[sr_num] != old)
		cpu->invalidate_translation_caches(cpu, sr_num << 28,
		    INVALIDATE_ALL | INVALIDATE_VADDR_UPPER4);
}


/*
 *  mfsrin, mtsrin:  Move From/To Segment Register Indirect
 *
 *  arg[0] = sr number, or for indirect mode: ptr to rb
 *  arg[1] = ptr to rt
 */
X(mfsr)
{
	/*  TODO: This only works for 32-bit mode  */
	reg(ic->arg[1]) = cpu->cd.ppc.sr[ic->arg[0]];
}
X(mfsrin)
{
	/*  TODO: This only works for 32-bit mode  */
	uint32_t sr_num = reg(ic->arg[0]) >> 28;
	reg(ic->arg[1]) = cpu->cd.ppc.sr[sr_num];
}


/*
 *  rldicl:
 *
 *  arg[0] = copy of the instruction word
 */
X(rldicl)
{
	int rs = (ic->arg[0] >> 21) & 31;
	int ra = (ic->arg[0] >> 16) & 31;
	int sh = ((ic->arg[0] >> 11) & 31) | ((ic->arg[0] & 2) << 4);
	int mb = ((ic->arg[0] >> 6) & 31) | (ic->arg[0] & 0x20);
	int rc = ic->arg[0] & 1;
	uint64_t tmp = cpu->cd.ppc.gpr[rs], tmp2;
	/*  TODO: Fix this, its performance is awful:  */
	while (sh-- != 0) {
		int b = (tmp >> 63) & 1;
		tmp = (tmp << 1) | b;
	}
	tmp2 = 0;
	while (mb <= 63) {
		tmp |= ((uint64_t)1 << (63-mb));
		mb ++;
	}
	cpu->cd.ppc.gpr[ra] = tmp & tmp2;
	if (rc)
		update_cr0(cpu, cpu->cd.ppc.gpr[ra]);
}


/*
 *  rldicr:
 *
 *  arg[0] = copy of the instruction word
 */
X(rldicr)
{
	int rs = (ic->arg[0] >> 21) & 31;
	int ra = (ic->arg[0] >> 16) & 31;
	int sh = ((ic->arg[0] >> 11) & 31) | ((ic->arg[0] & 2) << 4);
	int me = ((ic->arg[0] >> 6) & 31) | (ic->arg[0] & 0x20);
	int rc = ic->arg[0] & 1;
	uint64_t tmp = cpu->cd.ppc.gpr[rs];
	/*  TODO: Fix this, its performance is awful:  */
	while (sh-- != 0) {
		int b = (tmp >> 63) & 1;
		tmp = (tmp << 1) | b;
	}
	while (me++ < 63)
		tmp &= ~((uint64_t)1 << (63-me));
	cpu->cd.ppc.gpr[ra] = tmp;
	if (rc)
		update_cr0(cpu, tmp);
}


/*
 *  rldimi:
 *
 *  arg[0] = copy of the instruction word
 */
X(rldimi)
{
	uint32_t iw = ic->arg[0];
	int rs = (iw >> 21) & 31, ra = (iw >> 16) & 31;
	int sh = ((iw >> 11) & 31) | ((iw & 2) << 4);
	int mb = ((iw >> 6) & 31) | (iw & 0x20);
	int rc = ic->arg[0] & 1;
	int m;
	uint64_t tmp, s = cpu->cd.ppc.gpr[rs];
	/*  TODO: Fix this, its performance is awful:  */
	while (sh-- != 0) {
		int b = (s >> 63) & 1;
		s = (s << 1) | b;
	}
	m = mb; tmp = 0;
	do {
		tmp |= ((uint64_t)1 << (63-m));
		m ++;
	} while (m != 63 - sh);
	cpu->cd.ppc.gpr[ra] &= ~tmp;
	cpu->cd.ppc.gpr[ra] |= (tmp & s);
	if (rc)
		update_cr0(cpu, cpu->cd.ppc.gpr[ra]);
}


/*
 *  rlwnm:
 *
 *  arg[0] = ptr to ra
 *  arg[1] = mask
 *  arg[2] = copy of the instruction word
 */
X(rlwnm)
{
	uint32_t tmp, iword = ic->arg[2];
	int rs = (iword >> 21) & 31;
	int rb = (iword >> 11) & 31;
	int sh = cpu->cd.ppc.gpr[rb] & 0x1f;
	tmp = (uint32_t)cpu->cd.ppc.gpr[rs];
	tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;
	tmp &= (uint32_t)ic->arg[1];
	reg(ic->arg[0]) = tmp;
}
DOT0(rlwnm)


/*
 *  rlwinm:
 *
 *  arg[0] = ptr to ra
 *  arg[1] = mask
 *  arg[2] = copy of the instruction word
 */
X(rlwinm)
{
	uint32_t tmp, iword = ic->arg[2];
	int rs = (iword >> 21) & 31;
	int sh = (iword >> 11) & 31;
	tmp = (uint32_t)cpu->cd.ppc.gpr[rs];
	tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;
	tmp &= (uint32_t)ic->arg[1];
	reg(ic->arg[0]) = tmp;
}
DOT0(rlwinm)


/*
 *  rlwimi:
 *
 *  arg[0] = ptr to rs
 *  arg[1] = ptr to ra
 *  arg[2] = copy of the instruction word
 */
X(rlwimi)
{
	MODE_uint_t tmp = reg(ic->arg[0]), ra = reg(ic->arg[1]);
	uint32_t iword = ic->arg[2];
	int sh = (iword >> 11) & 31;
	int mb = (iword >> 6) & 31;
	int me = (iword >> 1) & 31;   
	int rc = iword & 1;

	tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

	for (;;) {
		uint64_t mask;
		mask = (uint64_t)1 << (31-mb);
		ra &= ~mask;
		ra |= (tmp & mask);
		if (mb == me)
			break;
		mb ++;
		if (mb == 32)
			mb = 0;
	}
	reg(ic->arg[1]) = ra;
	if (rc)
		update_cr0(cpu, ra);
}


/*
 *  srawi:
 *
 *  arg[0] = ptr to rs
 *  arg[1] = ptr to ra
 *  arg[2] = sh (shift amount)
 */
X(srawi)
{
	uint32_t tmp = reg(ic->arg[0]);
	int i = 0, j = 0, sh = ic->arg[2];

	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (tmp & 0x80000000)
		i = 1;
	while (sh-- > 0) {
		if (tmp & 1)
			j ++;
		tmp >>= 1;
		if (tmp & 0x40000000)
			tmp |= 0x80000000;
	}
	if (i && j>0)
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[1]) = (int64_t)(int32_t)tmp;
}
DOT1(srawi)


/*
 *  mcrf:  Move inside condition register
 *
 *  arg[0] = 28-4*bf,  arg[1] = 28-4*bfa
 */
X(mcrf)
{
	int bf_shift = ic->arg[0], bfa_shift = ic->arg[1];
	uint32_t tmp = (cpu->cd.ppc.cr >> bfa_shift) & 0xf;
	cpu->cd.ppc.cr &= ~((uint32_t)0xf << bf_shift);
	cpu->cd.ppc.cr |= (tmp << bf_shift);
}


/*
 *  crand, crxor etc:  Condition Register operations
 *
 *  arg[0] = copy of the instruction word
 */
X(crand) {
	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
	cpu->cd.ppc.cr &= ~(1 << (31-bt));
	if (ba & bb)
		cpu->cd.ppc.cr |= (1 << (31-bt));
}
X(crandc) {
	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
	cpu->cd.ppc.cr &= ~(1 << (31-bt));
	if (!(ba & bb))
		cpu->cd.ppc.cr |= (1 << (31-bt));
}
X(creqv) {
	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
	cpu->cd.ppc.cr &= ~(1 << (31-bt));
	if (!(ba ^ bb))
		cpu->cd.ppc.cr |= (1 << (31-bt));
}
X(cror) {
	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
	cpu->cd.ppc.cr &= ~(1 << (31-bt));
	if (ba | bb)
		cpu->cd.ppc.cr |= (1 << (31-bt));
}
X(crorc) {
	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
	cpu->cd.ppc.cr &= ~(1 << (31-bt));
	if (!(ba | bb))
		cpu->cd.ppc.cr |= (1 << (31-bt));
}
X(crnor) {
	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
	cpu->cd.ppc.cr &= ~(1 << (31-bt));
	if (!(ba | bb))
		cpu->cd.ppc.cr |= (1 << (31-bt));
}
X(crxor) {
	uint32_t iword = ic->arg[0]; int bt = (iword >> 21) & 31;
	int ba = (iword >> 16) & 31, bb = (iword >> 11) & 31;
	ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
	bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
	cpu->cd.ppc.cr &= ~(1 << (31-bt));
	if (ba ^ bb)
		cpu->cd.ppc.cr |= (1 << (31-bt));
}


/*
 *  mfspr: Move from SPR
 *
 *  arg[0] = pointer to destination register
 *  arg[1] = pointer to source SPR
 */
X(mfspr) {
	/*  TODO: Check permission  */
	reg(ic->arg[0]) = reg(ic->arg[1]);
}
X(mfspr_pmc1) {
	/*
	 *  TODO: This is a temporary hack to make NetBSD/ppc detect
	 *  a CPU of the correct (emulated) speed.
	 */
	reg(ic->arg[0]) = cpu->machine->emulated_hz / 10;
}
X(mftb) {
	/*  NOTE/TODO: This increments the time base (slowly) if it
	    is being polled.  */
	if (++cpu->cd.ppc.spr[SPR_TBL] == 0)
		cpu->cd.ppc.spr[SPR_TBU] ++;
	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBL];
}
X(mftbu) {
	reg(ic->arg[0]) = cpu->cd.ppc.spr[SPR_TBU];
}


/*
 *  mtspr: Move to SPR.
 *
 *  arg[0] = pointer to source register
 *  arg[1] = pointer to the SPR
 */
X(mtspr) {
	/*  TODO: Check permission  */
	reg(ic->arg[1]) = reg(ic->arg[0]);
}
X(mtspr_sprg2) {
	if (cpu->cd.ppc.bits == 32) {
		// Ignore for now. FreeBSD/powerpc seems to write 0xffffffe0
		// here, and read it back. If it is non-zero, it assumes a 64-bit
		// cpu.
	} else {
		reg(ic->arg[1]) = reg(ic->arg[0]);
	}
}
X(mtlr) {
	cpu->cd.ppc.spr[SPR_LR] = reg(ic->arg[0]);
}
X(mtctr) {
	cpu->cd.ppc.spr[SPR_CTR] = reg(ic->arg[0]);
}


/*
 *  rfi[d]:  Return from Interrupt
 */
X(rfi)
{
	uint64_t tmp;

	reg_access_msr(cpu, &tmp, 0, 0);
	tmp &= ~0xffff;
	tmp |= (cpu->cd.ppc.spr[SPR_SRR1] & 0xffff);
	reg_access_msr(cpu, &tmp, 1, 0);

	cpu->pc = cpu->cd.ppc.spr[SPR_SRR0];
	quick_pc_to_pointers(cpu);
}
X(rfid)
{
	uint64_t tmp, mask = 0x800000000000ff73ULL;

	reg_access_msr(cpu, &tmp, 0, 0);
	tmp &= ~mask;
	tmp |= (cpu->cd.ppc.spr[SPR_SRR1] & mask);
	reg_access_msr(cpu, &tmp, 1, 0);

	cpu->pc = cpu->cd.ppc.spr[SPR_SRR0];
	if (!(tmp & PPC_MSR_SF))
		cpu->pc = (uint32_t)cpu->pc;
	quick_pc_to_pointers(cpu);
}


/*
 *  mfcr:  Move From Condition Register
 *
 *  arg[0] = pointer to destination register
 */
X(mfcr)
{
	reg(ic->arg[0]) = cpu->cd.ppc.cr;
}


/*
 *  mfmsr:  Move From MSR
 *
 *  arg[0] = pointer to destination register
 */
X(mfmsr)
{
	reg_access_msr(cpu, (uint64_t*)ic->arg[0], 0, 0);
}


/*
 *  mtmsr:  Move To MSR
 *
 *  arg[0] = pointer to source register
 *  arg[1] = page offset of the next instruction
 *  arg[2] = 0 for 32-bit (mtmsr), 1 for 64-bit (mtmsrd)
 */
X(mtmsr)
{
	MODE_uint_t old_pc;
	uint64_t x = reg(ic->arg[0]);

	/*  TODO: check permission!  */

	/*  Synchronize the PC (pointing to _after_ this instruction)  */
	cpu->pc = (cpu->pc & ~0xfff) + ic->arg[1];
	old_pc = cpu->pc;

	if (!ic->arg[2]) {
		uint64_t y;
		reg_access_msr(cpu, &y, 0, 0);
		x = (y & 0xffffffff00000000ULL) | (x & 0xffffffffULL);
	}

	reg_access_msr(cpu, &x, 1, 1);

	/*
	 *  Super-ugly hack:  If the pc wasn't changed (i.e. if there was no
	 *  exception while accessing the msr), then we _decrease_ the PC by 4
	 *  again. This is because the next ic could be an end_of_page.
	 */
	if ((MODE_uint_t)cpu->pc == old_pc)
		cpu->pc -= 4;
}


/*
 *  wrteei:  Write EE immediate  (on PPC405GP)
 *
 *  arg[0] = either 0 or 0x8000
 */
X(wrteei)
{
	/*  TODO: check permission!  */
	uint64_t x;

	/*  Synchronize the PC (pointing to _after_ this instruction)  */
	cpu->pc = (cpu->pc & ~0xfff) + ic->arg[1];

	reg_access_msr(cpu, &x, 0, 0);
	x = (x & ~0x8000) | ic->arg[0];
	reg_access_msr(cpu, &x, 1, 1);
}


/*
 *  mtcrf:  Move To Condition Register Fields
 *
 *  arg[0] = pointer to source register
 */
X(mtcrf)
{
	cpu->cd.ppc.cr &= ~ic->arg[1];
	cpu->cd.ppc.cr |= (reg(ic->arg[0]) & ic->arg[1]);
}


/*
 *  mulli:  Multiply Low Immediate.
 *
 *  arg[0] = pointer to source register ra
 *  arg[1] = int32_t immediate
 *  arg[2] = pointer to destination register rt
 */
X(mulli)
{
	reg(ic->arg[2]) = (uint32_t)(reg(ic->arg[0]) * (int32_t)ic->arg[1]);
}


/*
 *  Load/Store Multiple:
 *
 *  arg[0] = rs  (or rt for loads)  NOTE: not a pointer
 *  arg[1] = ptr to ra
 *  arg[2] = int32_t immediate offset
 */
X(lmw) {
	MODE_uint_t addr = reg(ic->arg[1]) + (int32_t)ic->arg[2];
	unsigned char d[4];
	int rs = ic->arg[0];

	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
	    / sizeof(struct ppc_instr_call);
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc |= (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	while (rs <= 31) {
		if (cpu->memory_rw(cpu, cpu->mem, addr, d, sizeof(d),
		    MEM_READ, CACHE_DATA) != MEMORY_ACCESS_OK) {
			/*  exception  */
			return;
		}

		if (cpu->byte_order == EMUL_BIG_ENDIAN)
			cpu->cd.ppc.gpr[rs] = (d[0] << 24) + (d[1] << 16)
			    + (d[2] << 8) + d[3];
		else
			cpu->cd.ppc.gpr[rs] = (d[3] << 24) + (d[2] << 16)
			    + (d[1] << 8) + d[0];

		rs ++;
		addr += sizeof(uint32_t);
	}
}
X(stmw) {
	MODE_uint_t addr = reg(ic->arg[1]) + (int32_t)ic->arg[2];
	unsigned char d[4];
	int rs = ic->arg[0];

	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
	    / sizeof(struct ppc_instr_call);
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	while (rs <= 31) {
		uint32_t tmp = cpu->cd.ppc.gpr[rs];
		if (cpu->byte_order == EMUL_BIG_ENDIAN) {
			d[3] = tmp; d[2] = tmp >> 8;
			d[1] = tmp >> 16; d[0] = tmp >> 24;
		} else {
			d[0] = tmp; d[1] = tmp >> 8;
			d[2] = tmp >> 16; d[3] = tmp >> 24;
		}
		if (cpu->memory_rw(cpu, cpu->mem, addr, d, sizeof(d),
		    MEM_WRITE, CACHE_DATA) != MEMORY_ACCESS_OK) {
			/*  exception  */
			return;
		}

		rs ++;
		addr += sizeof(uint32_t);
	}
}


/*
 *  Load/store string:
 *
 *  arg[0] = rs   (well, rt for lswi)
 *  arg[1] = ptr to ra (or ptr to zero)
 *  arg[2] = nb
 */
X(lswi)
{
	MODE_uint_t addr = reg(ic->arg[1]);
	int rt = ic->arg[0], nb = ic->arg[2];
	int sub = 0;

	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
	    / sizeof(struct ppc_instr_call);
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	while (nb > 0) {
		unsigned char d;
		if (cpu->memory_rw(cpu, cpu->mem, addr, &d, 1,
		    MEM_READ, CACHE_DATA) != MEMORY_ACCESS_OK) {
			/*  exception  */
			return;
		}

		if (cpu->cd.ppc.mode == MODE_POWER && sub == 0)
			cpu->cd.ppc.gpr[rt] = 0;
		cpu->cd.ppc.gpr[rt] &= ~(0xff << (24-8*sub));
		cpu->cd.ppc.gpr[rt] |= (d << (24-8*sub));
		sub ++;
		if (sub == 4) {
			rt = (rt + 1) & 31;
			sub = 0;
		}
		addr ++;
		nb --;
	}
}
X(stswi)
{
	MODE_uint_t addr = reg(ic->arg[1]);
	int rs = ic->arg[0], nb = ic->arg[2];
	uint32_t cur = cpu->cd.ppc.gpr[rs];
	int sub = 0;

	int low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
	    / sizeof(struct ppc_instr_call);
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);

	while (nb > 0) {
		unsigned char d = cur >> 24;
		if (cpu->memory_rw(cpu, cpu->mem, addr, &d, 1,
		    MEM_WRITE, CACHE_DATA) != MEMORY_ACCESS_OK) {
			/*  exception  */
			return;
		}
		cur <<= 8;
		sub ++;
		if (sub == 4) {
			rs = (rs + 1) & 31;
			sub = 0;
			cur = cpu->cd.ppc.gpr[rs];
		}
		addr ++;
		nb --;
	}
}


/*
 *  Shifts, and, or, xor, etc.
 *
 *  arg[0] = pointer to source register rs
 *  arg[1] = pointer to source register rb
 *  arg[2] = pointer to destination register ra
 */
X(extsb) {
#ifdef MODE32
	reg(ic->arg[2]) = (int32_t)(int8_t)reg(ic->arg[0]);
#else
	reg(ic->arg[2]) = (int64_t)(int8_t)reg(ic->arg[0]);
#endif
}
DOT2(extsb)
X(extsh) {
#ifdef MODE32
	reg(ic->arg[2]) = (int32_t)(int16_t)reg(ic->arg[0]);
#else
	reg(ic->arg[2]) = (int64_t)(int16_t)reg(ic->arg[0]);
#endif
}
DOT2(extsh)
X(extsw) {
#ifdef MODE32
	fatal("TODO: extsw: invalid instruction\n");
#else
	reg(ic->arg[2]) = (int64_t)(int32_t)reg(ic->arg[0]);
#endif
}
DOT2(extsw)
X(slw) {	reg(ic->arg[2]) = (uint64_t)reg(ic->arg[0])
		    << (reg(ic->arg[1]) & 31); }
DOT2(slw)
X(sld) {int sa = reg(ic->arg[1]) & 127;
	if (sa >= 64)	reg(ic->arg[2]) = 0;
	else reg(ic->arg[2]) = (uint64_t)reg(ic->arg[0]) << (sa & 63); }
DOT2(sld)
X(sraw)
{
	uint32_t tmp = reg(ic->arg[0]);
	int i = 0, j = 0, sh = reg(ic->arg[1]) & 31;

	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (tmp & 0x80000000)
		i = 1;
	while (sh-- > 0) {
		if (tmp & 1)
			j ++;
		tmp >>= 1;
		if (tmp & 0x40000000)
			tmp |= 0x80000000;
	}
	if (i && j>0)
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (int64_t)(int32_t)tmp;
}
DOT2(sraw)
X(srw) {	reg(ic->arg[2]) = (uint64_t)reg(ic->arg[0])
		    >> (reg(ic->arg[1]) & 31); }
DOT2(srw)
X(and) {	reg(ic->arg[2]) = reg(ic->arg[0]) & reg(ic->arg[1]); }
DOT2(and)
X(nand) {	reg(ic->arg[2]) = ~(reg(ic->arg[0]) & reg(ic->arg[1])); }
DOT2(nand)
X(andc) {	reg(ic->arg[2]) = reg(ic->arg[0]) & (~reg(ic->arg[1])); }
DOT2(andc)
X(nor) {	reg(ic->arg[2]) = ~(reg(ic->arg[0]) | reg(ic->arg[1])); }
DOT2(nor)
X(mr) {		reg(ic->arg[2]) = reg(ic->arg[1]); }
X(or) {		reg(ic->arg[2]) = reg(ic->arg[0]) | reg(ic->arg[1]); }
DOT2(or)
X(orc) {	reg(ic->arg[2]) = reg(ic->arg[0]) | (~reg(ic->arg[1])); }
DOT2(orc)
X(xor) {	reg(ic->arg[2]) = reg(ic->arg[0]) ^ reg(ic->arg[1]); }
DOT2(xor)
X(eqv) {	reg(ic->arg[2]) = ~(reg(ic->arg[0]) ^ reg(ic->arg[1])); }
DOT2(eqv)


/*
 *  neg:
 *
 *  arg[0] = pointer to source register ra
 *  arg[1] = pointer to destination register rt
 */
X(neg) {	reg(ic->arg[1]) = -reg(ic->arg[0]); }
DOT1(neg)


/*
 *  mullw, mulhw[u], divw[u]:
 *
 *  arg[0] = pointer to source register ra
 *  arg[1] = pointer to source register rb
 *  arg[2] = pointer to destination register rt
 */
X(mullw)
{
	int32_t sum = (int32_t)reg(ic->arg[0]) * (int32_t)reg(ic->arg[1]);
	reg(ic->arg[2]) = (int32_t)sum;
}
DOT2(mullw)
X(mulhw)
{
	int64_t sum;
	sum = (int64_t)(int32_t)reg(ic->arg[0])
	    * (int64_t)(int32_t)reg(ic->arg[1]);
	reg(ic->arg[2]) = sum >> 32;
}
DOT2(mulhw)
X(mulhwu)
{
	uint64_t sum;
	sum = (uint64_t)(uint32_t)reg(ic->arg[0])
	    * (uint64_t)(uint32_t)reg(ic->arg[1]);
	reg(ic->arg[2]) = sum >> 32;
}
DOT2(mulhwu)
X(divw)
{
	int32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
	int32_t sum;
	if (b == 0)
		sum = 0;
	else
		sum = a / b;
	reg(ic->arg[2]) = (uint32_t)sum;
}
DOT2(divw)
X(divwu)
{
	uint32_t a = reg(ic->arg[0]), b = reg(ic->arg[1]);
	uint32_t sum;
	if (b == 0)
		sum = 0;
	else
		sum = a / b;
	reg(ic->arg[2]) = sum;
}
DOT2(divwu)


/*
 *  add:  Add.
 *
 *  arg[0] = pointer to source register ra
 *  arg[1] = pointer to source register rb
 *  arg[2] = pointer to destination register rt
 */
X(add)     { reg(ic->arg[2]) = reg(ic->arg[0]) + reg(ic->arg[1]); }
DOT2(add)


/*
 *  addc:  Add carrying.
 *
 *  arg[0] = pointer to source register ra
 *  arg[1] = pointer to source register rb
 *  arg[2] = pointer to destination register rt
 */
X(addc)
{
	/*  TODO: this only works in 32-bit mode  */
	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
	uint64_t tmp2 = tmp;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	tmp += (uint32_t)reg(ic->arg[1]);
	if ((tmp >> 32) != (tmp2 >> 32))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp;
}


/*
 *  adde:  Add extended, etc.
 *
 *  arg[0] = pointer to source register ra
 *  arg[1] = pointer to source register rb
 *  arg[2] = pointer to destination register rt
 */
X(adde)
{
	/*  TODO: this only works in 32-bit mode  */
	int old_ca = cpu->cd.ppc.spr[SPR_XER] & PPC_XER_CA;
	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
	uint64_t tmp2 = tmp;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	tmp += (uint32_t)reg(ic->arg[1]);
	if (old_ca)
		tmp ++;
	if ((tmp >> 32) != (tmp2 >> 32))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp;
}
DOT2(adde)
X(addme)
{
	/*  TODO: this only works in 32-bit mode  */
	int old_ca = cpu->cd.ppc.spr[SPR_XER] & PPC_XER_CA;
	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
	uint64_t tmp2 = tmp;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (old_ca)
		tmp ++;
	tmp += 0xffffffffULL;
	if ((tmp >> 32) != (tmp2 >> 32))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp;
}
DOT2(addme)
X(addze)
{
	/*  TODO: this only works in 32-bit mode  */
	int old_ca = cpu->cd.ppc.spr[SPR_XER] & PPC_XER_CA;
	uint64_t tmp = (uint32_t)reg(ic->arg[0]);
	uint64_t tmp2 = tmp;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (old_ca)
		tmp ++;
	if ((tmp >> 32) != (tmp2 >> 32))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp;
}
DOT2(addze)


/*
 *  subf:  Subf, etc.
 *
 *  arg[0] = pointer to source register ra
 *  arg[1] = pointer to source register rb
 *  arg[2] = pointer to destination register rt
 */
X(subf)
{
	reg(ic->arg[2]) = reg(ic->arg[1]) - reg(ic->arg[0]);
}
DOT2(subf)
X(subfc)
{
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (reg(ic->arg[1]) >= reg(ic->arg[0]))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = reg(ic->arg[1]) - reg(ic->arg[0]);
}
DOT2(subfc)
X(subfe)
{
	int old_ca = (cpu->cd.ppc.spr[SPR_XER] & PPC_XER_CA)? 1 : 0;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (reg(ic->arg[1]) == reg(ic->arg[0])) {
		if (old_ca)
			cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	} else if (reg(ic->arg[1]) >= reg(ic->arg[0]))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;

	/*
	 *  TODO: The register value calculation should be correct,
	 *  but the CA bit calculation above is probably not.
	 */

	reg(ic->arg[2]) = reg(ic->arg[1]) - reg(ic->arg[0]) - (old_ca? 0 : 1);
}
DOT2(subfe)
X(subfme)
{
	int old_ca = cpu->cd.ppc.spr[SPR_XER] & PPC_XER_CA;
	uint64_t tmp = (uint32_t)(~reg(ic->arg[0]));
	tmp += 0xffffffffULL;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (old_ca)
		tmp ++;
	if ((tmp >> 32) != 0)
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp;
}
DOT2(subfme)
X(subfze)
{
	int old_ca = cpu->cd.ppc.spr[SPR_XER] & PPC_XER_CA;
	uint64_t tmp = (uint32_t)(~reg(ic->arg[0]));
	uint64_t tmp2 = tmp;
	cpu->cd.ppc.spr[SPR_XER] &= ~PPC_XER_CA;
	if (old_ca)
		tmp ++;
	if ((tmp >> 32) != (tmp2 >> 32))
		cpu->cd.ppc.spr[SPR_XER] |= PPC_XER_CA;
	reg(ic->arg[2]) = (uint32_t)tmp;
}
DOT2(subfze)


/*
 *  ori, xori etc.:
 *
 *  arg[0] = pointer to source uint64_t
 *  arg[1] = immediate value (uint32_t or larger)
 *  arg[2] = pointer to destination uint64_t
 */
X(ori)  { reg(ic->arg[2]) = reg(ic->arg[0]) | (uint32_t)ic->arg[1]; }
X(xori) { reg(ic->arg[2]) = reg(ic->arg[0]) ^ (uint32_t)ic->arg[1]; }


#include "tmp_ppc_loadstore.c"


/*
 *  lfs, stfs: Load/Store Floating-point Single precision
 */
X(lfs)
{
	/*  Sync. PC in case of an exception, and remember it:  */
	uint64_t old_pc, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call);
	old_pc = cpu->pc = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) <<
	    PPC_INSTR_ALIGNMENT_SHIFT)) + (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
	if (!(cpu->cd.ppc.msr & PPC_MSR_FP)) {
		ppc_exception(cpu, PPC_EXCEPTION_FPU);
		return;
	}

	/*  Perform a 32-bit load:  */
#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [2 + 4 + 8](cpu, ic);

	if (old_pc == cpu->pc) {
		/*  The load succeeded. Widen the single to double.
		    #305: through ppc_single_widen(), because the value domain
		    cannot carry a NaN -- interpret reports only THAT a pattern
		    is a NaN, and the store canonicalizes every one of them to
		    all-ones, so a guest's qNaN 0xffc00001 used to arrive in the
		    register as 0x7fffffffffffffff: wrong sign, wrong payload.
		    Finite values still travel the (exact, #303-verified) value
		    path inside the helper.  */
		(*(uint64_t *)ic->arg[0]) &= 0xffffffff;
		(*(uint64_t *)ic->arg[0]) = ppc_single_widen(
		    (uint32_t) *(uint64_t *)ic->arg[0]);
	}
}
#ifndef PPC_STFS_EXTRACT_INCLUDED
#define PPC_STFS_EXTRACT_INCLUDED
/*
 *  ppc_stfs_extract():  #304/#305 -- the two classes where the shared store
 *  cannot spell what the ISA's SINGLE() extraction owes.  Returns 1 and fills
 *  *out when it handled the value; 0 when the legacy path is already right.
 *
 *  Book I gives SINGLE() three cases on the operand's biased exponent E:
 *
 *    E > 896            splice sign, exponent and the top 23 fraction bits --
 *                       truncation, mode-independent, never rounding.  The
 *                       shared store already reproduces this bit for bit for
 *                       finite values (measured), so it keeps that path.
 *    874 <= E <= 896    DENORMALIZE: restore the implicit 1 and shift right
 *                       until the exponent reaches the single's minimum,
 *                       truncating what falls off.  The shared store flushes
 *                       this whole band to signed zero instead (its #287/#292
 *                       policy), which is the defect #304 fixes here.
 *    E < 874            WORD is architecturally UNDEFINED; the flush stands as
 *                       this fork's policy, and the gate pins it.
 *
 *  The NaN class is #305's: exponent all-ones is part of the splice case, so a
 *  NaN's sign and top-23 payload must survive.  The shared store canonicalizes
 *  every NaN to 0x7fffffff instead -- sign and payload both lost (measured).
 *  Note what the letter does here and this code faithfully repeats: a NaN whose
 *  payload lives entirely in the discarded low bits splices to the INFINITY
 *  pattern.  That is the extraction working as specified, not a case to repair,
 *  and there is a gate row asserting exactly that byte.  Quieting belongs to
 *  frsp alone -- a store must not alter the class of what it is storing.
 */
static int ppc_stfs_extract(uint64_t d, uint32_t *out)
{
	int exp = (int) ((d >> 52) & 0x7ff);
	uint64_t frac = d & 0xfffffffffffffULL;
	uint32_t sign = (uint32_t) (d >> 63) & 1;

	if (exp == 0x7ff && frac != 0) {		/*  #305: NaN  */
		*out = (sign << 31) | 0x7f800000 |
		    (uint32_t) (frac >> 29);
		return 1;
	}

	if (exp >= 874 && exp <= 896) {			/*  #304: the band  */
		uint64_t sig = frac | (1ULL << 52);
		int shift = 29 + (896 - exp) + 1;
		/*  Truncate -- the extraction never rounds, so no guard bit is
		    consulted here, unlike frsp's path through the same band.  */
		*out = (sign << 31) | (uint32_t) (sig >> shift);
		return 1;
	}

	return 0;
}
#endif	/*  PPC_STFS_EXTRACT_INCLUDED  */


/*
 *  #310: the eight UPDATE forms of the single/double float loads and stores.
 *
 *  lfsu/lfdu/stfsu/stfdu (primary opcodes 0x31/0x33/0x35/0x37) and their
 *  indexed twins lfsux/lfdux/stfsux/stfdux (opcode 31, extended 567/631/
 *  695/759) were not defined in opcodes_ppc.h and not decoded anywhere -- the
 *  header even had blank lines where the four primary opcodes belong.  Every
 *  one of them reached `goto bad`, which stops the emulator, and all eight
 *  were measured doing exactly that on the macppc probe path before this fix
 *  (their non-update twins ran, as controls).
 *
 *  The round originally scoped four; a panel seat demanded the indexed twins
 *  be checked first, on the principle #306 established -- a compiler emits
 *  both from the same loops, so fixing half a family leaves the other half
 *  stopping the machine.  It was right, though not about which extended
 *  opcodes they are: 599 and 663 are lfdx and stfsx, which this tree already
 *  decodes.  The update forms are 567/631/695/759, and none appeared here.
 *
 *  Each is its non-update sibling plus "rA receives the effective address",
 *  which the generic load/store table already implements (the +32 index term
 *  writes the address back through arg[1]).  So these bodies differ from
 *  lfs/lfd/stfs/stfd by one array index, and the format conversion -- the
 *  part #304 and #305 corrected -- is shared unchanged.
 *
 *  rA = 0 is an invalid form for every update instruction, and the decoder
 *  rejects it before reaching here, exactly as it already does for the
 *  integer update forms.
 *
 *  The two dispatch tables are NOT the same shape: the D-form table has a
 *  zero-displacement dimension and encodes update at +32, while the
 *  indexed table has no displacement at all and encodes it at +16 in only
 *  32 entries.  Using the D-form's term for the indexed handlers reads
 *  past the end of the array; the compiler caught that here as an
 *  out-of-bounds subscript, which is the only reason it did not become a
 *  call through whatever happened to follow the table.
 */
X(lfsu)
{
	uint64_t old_pc, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call);
	old_pc = cpu->pc = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) <<
	    PPC_INSTR_ALIGNMENT_SHIFT)) + (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
	if (!(cpu->cd.ppc.msr & PPC_MSR_FP)) {
		ppc_exception(cpu, PPC_EXCEPTION_FPU);
		return;
	}

#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [2 + 4 + 8 + 32](cpu, ic);

	if (old_pc == cpu->pc) {
		(*(uint64_t *)ic->arg[0]) &= 0xffffffff;
		(*(uint64_t *)ic->arg[0]) = ppc_single_widen(
		    (uint32_t) *(uint64_t *)ic->arg[0]);
	}
}
X(lfdu)
{
	CHECK_FOR_FPU_EXCEPTION;

#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [3 + 4 + 8 + 32](cpu, ic);
}
X(stfsu)
{
	uint64_t *old_arg0 = (uint64_t *) ic->arg[0];
	struct ieee_float_value val;
	uint64_t tmp_val;
	uint32_t extracted;

	CHECK_FOR_FPU_EXCEPTION;

	if (ppc_stfs_extract(*old_arg0, &extracted)) {
		tmp_val = extracted;
	} else {
		ieee_interpret_float_value(*old_arg0, &val, IEEE_FMT_D);
		tmp_val = ieee_store_float_value(val.f, IEEE_FMT_S);
	}

	ic->arg[0] = (size_t)&tmp_val;

#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [2 + 4 + 32](cpu, ic);

	ic->arg[0] = (size_t)old_arg0;
}
X(stfdu)
{
	CHECK_FOR_FPU_EXCEPTION;

#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [3 + 4 + 32](cpu, ic);
}
X(lfsux)
{
	uint64_t old_pc, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call);
	old_pc = cpu->pc = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) <<
	    PPC_INSTR_ALIGNMENT_SHIFT)) + (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
	if (!(cpu->cd.ppc.msr & PPC_MSR_FP)) {
		ppc_exception(cpu, PPC_EXCEPTION_FPU);
		return;
	}

#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [2 + 4 + 8 + 16](cpu, ic);

	if (old_pc == cpu->pc) {
		(*(uint64_t *)ic->arg[0]) &= 0xffffffff;
		(*(uint64_t *)ic->arg[0]) = ppc_single_widen(
		    (uint32_t) *(uint64_t *)ic->arg[0]);
	}
}
X(lfdux)
{
	CHECK_FOR_FPU_EXCEPTION;

#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [3 + 4 + 8 + 16](cpu, ic);
}
X(stfsux)
{
	uint64_t *old_arg0 = (uint64_t *)ic->arg[0];
	struct ieee_float_value val;
	uint64_t tmp_val;
	uint32_t extracted;

	CHECK_FOR_FPU_EXCEPTION;

	if (ppc_stfs_extract(*old_arg0, &extracted)) {
		tmp_val = extracted;
	} else {
		ieee_interpret_float_value(*old_arg0, &val, IEEE_FMT_D);
		tmp_val = ieee_store_float_value(val.f, IEEE_FMT_S);
	}

	ic->arg[0] = (size_t)&tmp_val;

#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [2 + 4 + 16](cpu, ic);

	ic->arg[0] = (size_t)old_arg0;
}
X(stfdux)
{
	CHECK_FOR_FPU_EXCEPTION;

#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [3 + 4 + 16](cpu, ic);
}


X(lfsx)
{
	/*  Sync. PC in case of an exception, and remember it:  */
	uint64_t old_pc, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.ppc.cur_ic_page) / sizeof(struct ppc_instr_call);
	old_pc = cpu->pc = (cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1) <<
	    PPC_INSTR_ALIGNMENT_SHIFT)) + (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
	if (!(cpu->cd.ppc.msr & PPC_MSR_FP)) {
		ppc_exception(cpu, PPC_EXCEPTION_FPU);
		return;
	}

	/*  Perform a 32-bit load:  */
#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [2 + 4 + 8](cpu, ic);

	if (old_pc == cpu->pc) {
		/*  The load succeeded. Widen the single to double.
		    #305: through ppc_single_widen(), because the value domain
		    cannot carry a NaN -- interpret reports only THAT a pattern
		    is a NaN, and the store canonicalizes every one of them to
		    all-ones, so a guest's qNaN 0xffc00001 used to arrive in the
		    register as 0x7fffffffffffffff: wrong sign, wrong payload.
		    Finite values still travel the (exact, #303-verified) value
		    path inside the helper.  */
		(*(uint64_t *)ic->arg[0]) &= 0xffffffff;
		(*(uint64_t *)ic->arg[0]) = ppc_single_widen(
		    (uint32_t) *(uint64_t *)ic->arg[0]);
	}
}
X(lfd)
{
	CHECK_FOR_FPU_EXCEPTION;

	/*  Perform a 64-bit load:  */
#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [3 + 4 + 8](cpu, ic);
}
X(lfdx)
{
	CHECK_FOR_FPU_EXCEPTION;

	/*  Perform a 64-bit load:  */
#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [3 + 4 + 8](cpu, ic);
}



X(stfs)
{
	uint64_t *old_arg0 = (uint64_t *) ic->arg[0];
	struct ieee_float_value val;
	uint64_t tmp_val;
	uint32_t extracted;

	CHECK_FOR_FPU_EXCEPTION;

	if (ppc_stfs_extract(*old_arg0, &extracted)) {
		tmp_val = extracted;
	} else {
		ieee_interpret_float_value(*old_arg0, &val, IEEE_FMT_D);
		tmp_val = ieee_store_float_value(val.f, IEEE_FMT_S);
	}

	ic->arg[0] = (size_t)&tmp_val;

	/*  Perform a 32-bit store:  */
#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [2 + 4](cpu, ic);

	ic->arg[0] = (size_t)old_arg0;
}
X(stfsx)
{
	uint64_t *old_arg0 = (uint64_t *)ic->arg[0];
	struct ieee_float_value val;
	uint64_t tmp_val;
	uint32_t extracted;

	CHECK_FOR_FPU_EXCEPTION;

	/*  #304/#305: the indexed form is the same store and gets the same
	    extraction -- a fix that reached only the base form would leave every
	    indexed store on the old path, which is why the gate runs rows through
	    both.  */
	if (ppc_stfs_extract(*old_arg0, &extracted)) {
		tmp_val = extracted;
	} else {
		ieee_interpret_float_value(*old_arg0, &val, IEEE_FMT_D);
		tmp_val = ieee_store_float_value(val.f, IEEE_FMT_S);
	}

	ic->arg[0] = (size_t)&tmp_val;

	/*  Perform a 32-bit store:  */
#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [2 + 4](cpu, ic);

	ic->arg[0] = (size_t)old_arg0;
}
X(stfd)
{
	CHECK_FOR_FPU_EXCEPTION;

	/*  Perform a 64-bit store:  */
#ifdef MODE32
	ppc32_loadstore
#else
	ppc_loadstore
#endif
	    [3 + 4](cpu, ic);
}
X(stfdx)
{
	CHECK_FOR_FPU_EXCEPTION;

	/*  Perform a 64-bit store:  */
#ifdef MODE32
	ppc32_loadstore_indexed
#else
	ppc_loadstore_indexed
#endif
	    [3 + 4](cpu, ic);
}


/*
 *  lvx, stvx:  Vector (16-byte) load/store  (slow implementation)
 *
 *  arg[0] = v-register nr of rs
 *  arg[1] = pointer to ra
 *  arg[2] = pointer to rb
 */
X(lvx)
{
	MODE_uint_t addr = reg(ic->arg[1]) + reg(ic->arg[2]);
	uint8_t data[16];
	uint64_t hi, lo;
	int rs = ic->arg[0];

	if (cpu->memory_rw(cpu, cpu->mem, addr, data, sizeof(data),
	    MEM_READ, CACHE_DATA) != MEMORY_ACCESS_OK) {
		/*  exception  */
		return;
	}

	hi = ((uint64_t)data[0] << 56) +
	     ((uint64_t)data[1] << 48) +
	     ((uint64_t)data[2] << 40) +
	     ((uint64_t)data[3] << 32) +
	     ((uint64_t)data[4] << 24) +
	     ((uint64_t)data[5] << 16) +
	     ((uint64_t)data[6] << 8) +
	     ((uint64_t)data[7]);
	lo = ((uint64_t)data[8] << 56) +
	     ((uint64_t)data[9] << 48) +
	     ((uint64_t)data[10] << 40) +
	     ((uint64_t)data[11] << 32) +
	     ((uint64_t)data[12] << 24) +
	     ((uint64_t)data[13] << 16) +
	     ((uint64_t)data[14] << 8) +
	     ((uint64_t)data[15]);

	cpu->cd.ppc.vr_hi[rs] = hi; cpu->cd.ppc.vr_lo[rs] = lo;
}
X(stvx)
{
	uint8_t data[16];
	MODE_uint_t addr = reg(ic->arg[1]) + reg(ic->arg[2]);
	int rs = ic->arg[0];
	uint64_t hi = cpu->cd.ppc.vr_hi[rs], lo = cpu->cd.ppc.vr_lo[rs];

	data[0] = hi >> 56;
	data[1] = hi >> 48;
	data[2] = hi >> 40;
	data[3] = hi >> 32;
	data[4] = hi >> 24;
	data[5] = hi >> 16;
	data[6] = hi >> 8;
	data[7] = hi;
	data[8] = lo >> 56;
	data[9] = lo >> 48;
	data[10] = lo >> 40;
	data[11] = lo >> 32;
	data[12] = lo >> 24;
	data[13] = lo >> 16;
	data[14] = lo >> 8;
	data[15] = lo;

	cpu->memory_rw(cpu, cpu->mem, addr, data,
	    sizeof(data), MEM_WRITE, CACHE_DATA);
}


/*
 *  vxor:  Vector (16-byte) XOR
 *
 *  arg[0] = v-register nr of source 1
 *  arg[1] = v-register nr of source 2
 *  arg[2] = v-register nr of destination
 */
X(vxor)
{
	cpu->cd.ppc.vr_hi[ic->arg[2]] =
	    cpu->cd.ppc.vr_hi[ic->arg[0]] ^ cpu->cd.ppc.vr_hi[ic->arg[1]];
	cpu->cd.ppc.vr_lo[ic->arg[2]] =
	    cpu->cd.ppc.vr_lo[ic->arg[0]] ^ cpu->cd.ppc.vr_lo[ic->arg[1]];
}


/*
 *  tlbia:  TLB invalidate all
 */
X(tlbia)
{
	fatal("[ tlbia ]\n");
	cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
}


/*
 *  tlbie:  TLB invalidate
 */
X(tlbie)
{
	/*  fatal("[ tlbie ]\n");  */
	cpu->invalidate_translation_caches(cpu, reg(ic->arg[0]),
	    INVALIDATE_VADDR);
}


/*
 *  sc: Syscall.
 */
X(sc)
{
	/*  Synchronize the PC (pointing to _after_ this instruction)  */
	cpu->pc = (cpu->pc & ~0xfff) + ic->arg[1];

	ppc_exception(cpu, PPC_EXCEPTION_SC);

	/*  This caused an update to the PC register, so there is no need
	    to worry about the next instruction being an end_of_page.  */
}


/*
 *  openfirmware:
 */
X(openfirmware)
{
	of_emul(cpu);

	cpu->pc = cpu->cd.ppc.spr[SPR_LR];
	if (cpu->machine->show_trace_tree)
		cpu_functioncall_trace_return(cpu);

	quick_pc_to_pointers(cpu);

	if (!cpu->running) {
		cpu->n_translated_instrs --;
		cpu->cd.ppc.next_ic = &nothing_call;
	}
}


/*
 *  tlbsx_dot: TLB scan
 */
X(tlbsx_dot)
{
	/*  TODO  */
	cpu->cd.ppc.cr &= ~(0xf0000000);
	cpu->cd.ppc.cr |= 0x20000000;
	cpu->cd.ppc.cr |= ((cpu->cd.ppc.spr[SPR_XER] >> 3) & 0x10000000);
}


/*
 *  tlbli:
 */
X(tlbli)
{
	fatal("tlbli\n");
	cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
}


/*
 *  tlbld:
 */
X(tlbld)
{
	/*  MODE_uint_t vaddr = reg(ic->arg[0]);
	    MODE_uint_t paddr = cpu->cd.ppc.spr[SPR_RPA];  */

	fatal("tlbld\n");
	cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
}


/*****************************************************************************/


X(end_of_page)
{
	/*  Update the PC:  (offset 0, but on the next page)  */
	cpu->pc &= ~((PPC_IC_ENTRIES_PER_PAGE-1) << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc += (PPC_IC_ENTRIES_PER_PAGE << PPC_INSTR_ALIGNMENT_SHIFT);

	/*  Find the new physical page and update the translation pointers:  */
	quick_pc_to_pointers(cpu);

	/*  end_of_page doesn't count as an executed instruction:  */
	cpu->n_translated_instrs --;
}


/*
 *  #326: the record forms. Every floating-point instruction that defines an
 *  Rc bit gets a `_dot` twin here, generated by FDOT: run the base, then set
 *  CR field 1 from FPSCR[0:3].
 *
 *  fcmpu and mcrfs are absent ON PURPOSE. Neither defines Rc -- the low bit
 *  of their encoding is reserved -- so there is no `fcmpu.` or `mcrfs.` to
 *  implement, and an encoding with that bit set is invalid rather than a
 *  record form. The decoder keeps rejecting those two.
 */
FDOT(frsp)
FDOT(fctiw)
FDOT(fctiwz)
FDOT(fneg)
FDOT(fabs)
FDOT(fnabs)
FDOT(fmr)
FDOT(fsel)
FDOT(fadd)
FDOT(fsub)
FDOT(fmul)
FDOT(fdiv)
FDOT(fmadd)
FDOT(fmsub)
FDOT(fadds)
FDOT(fsubs)
FDOT(fmuls)
FDOT(fdivs)
FDOT(mffs)
FDOT(mtfsf)
FDOT(mtfsb0)
FDOT(mtfsb1)
FDOT(mtfsfi)


/*****************************************************************************/


/*
 *  ppc_instr_to_be_translated():
 *
 *  Translate an instruction word into a ppc_instr_call. ic is filled in with
 *  valid data for the translated instruction, or a "nothing" instruction if
 *  there was a translation failure. The newly translated instruction is then
 *  executed.
 */
X(to_be_translated)
{
	uint64_t addr, low_pc, tmp_addr;
	uint32_t iword, mask;
	unsigned char *page;
	unsigned char ib[4];
	int main_opcode, rt, rs, ra, rb, rc, aa_bit, l_bit, lk_bit, spr, sh,
	    xo, imm, load, size, update, zero, bf, bo, bi, bh, oe_bit, n64=0,
	    bfa, fp, byterev, nb, mb, me;
	void (*samepage_function)(struct cpu *, struct ppc_instr_call *);
	void (*rc_f)(struct cpu *, struct ppc_instr_call *);

	/*  Figure out the (virtual) address of the instruction:  */
	low_pc = ((size_t)ic - (size_t)cpu->cd.ppc.cur_ic_page)
	    / sizeof(struct ppc_instr_call);
	addr = cpu->pc & ~((PPC_IC_ENTRIES_PER_PAGE-1)
	    << PPC_INSTR_ALIGNMENT_SHIFT);
	addr += (low_pc << PPC_INSTR_ALIGNMENT_SHIFT);
	cpu->pc = addr;
	addr &= ~((1 << PPC_INSTR_ALIGNMENT_SHIFT) - 1);

	/*  Read the instruction word from memory:  */
#ifdef MODE32
	page = cpu->cd.ppc.host_load[((uint32_t)addr) >> 12];
#else
	{
		const uint32_t mask1 = (1 << DYNTRANS_L1N) - 1;
		const uint32_t mask2 = (1 << DYNTRANS_L2N) - 1;
		const uint32_t mask3 = (1 << DYNTRANS_L3N) - 1;
		uint32_t x1 = (addr >> (64-DYNTRANS_L1N)) & mask1;
		uint32_t x2 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N)) & mask2;
		uint32_t x3 = (addr >> (64-DYNTRANS_L1N-DYNTRANS_L2N-
		    DYNTRANS_L3N)) & mask3;
		struct DYNTRANS_L2_64_TABLE *l2 = cpu->cd.ppc.l1_64[x1];
		struct DYNTRANS_L3_64_TABLE *l3 = l2->l3[x2];
		page = l3->host_load[x3];
	}
#endif

	if (page != NULL) {
		/*  fatal("TRANSLATION HIT!\n");  */
		memcpy(ib, page + (addr & 0xfff), sizeof(ib));
	} else {
		/*  fatal("TRANSLATION MISS!\n");  */
		if (!cpu->memory_rw(cpu, cpu->mem, addr, ib,
		    sizeof(ib), MEM_READ, CACHE_INSTRUCTION)) {
			fatal("PPC to_be_translated(): "
			    "read failed: TODO\n");
			exit(1);
			/*  goto bad;  */
		}
	}

	{
		uint32_t *p = (uint32_t *) ib;
		iword = *p;
		iword = BE32_TO_HOST(iword);
	}

#define DYNTRANS_TO_BE_TRANSLATED_HEAD
#include "cpu_dyntrans.c"
#undef  DYNTRANS_TO_BE_TRANSLATED_HEAD


	/*
	 *  Translate the instruction:
	 */

	main_opcode = iword >> 26;

	switch (main_opcode) {

	case 0x04:
		if (iword == 0x12739cc4) {
			/*  vxor v19,v19,v19  */
			ic->f = instr(vxor);
			ic->arg[0] = 19;
			ic->arg[1] = 19;
			ic->arg[2] = 19;
		} else {
			if (!cpu->translation_readahead)
				fatal("[ TODO: Unimplemented ALTIVEC, iword"
				    " = 0x%08" PRIx32"x ]\n", iword);
			goto bad;
		}
		break;

	case PPC_HI6_MULLI:
		rt = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		imm = (int16_t)(iword & 0xffff);
		ic->f = instr(mulli);
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[1] = (ssize_t)imm;
		ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
		break;

	case PPC_HI6_SUBFIC:
		rt = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		imm = (int16_t)(iword & 0xffff);
		ic->f = instr(subfic);
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[1] = (ssize_t)imm;
		ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
		break;

	case PPC_HI6_CMPLI:
	case PPC_HI6_CMPI:
		bf = (iword >> 23) & 7;
		l_bit = (iword >> 21) & 1;
		ra = (iword >> 16) & 31;
		if (main_opcode == PPC_HI6_CMPLI) {
			imm = iword & 0xffff;
			if (l_bit)
				ic->f = instr(cmpldi);
			else
				ic->f = instr(cmplwi);
		} else {
			imm = (int16_t)(iword & 0xffff);
			if (l_bit)
				ic->f = instr(cmpdi);
			else {
				if (bf == 0)
					ic->f = instr(cmpwi_cr0);
				else
					ic->f = instr(cmpwi);
			}
		}
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[1] = (ssize_t)imm;
		ic->arg[2] = 28 - 4 * bf;
		break;

	case PPC_HI6_ADDIC:
	case PPC_HI6_ADDIC_DOT:
		if (cpu->cd.ppc.bits == 64) {
			if (!cpu->translation_readahead)
				fatal("addic for 64-bit: TODO\n");
			goto bad;
		}
		rt = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		imm = (int16_t)(iword & 0xffff);
		if (main_opcode == PPC_HI6_ADDIC)
			ic->f = instr(addic);
		else
			ic->f = instr(addic_dot);
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[1] = imm;
		ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
		break;

	case PPC_HI6_ADDI:
	case PPC_HI6_ADDIS:
		rt = (iword >> 21) & 31; ra = (iword >> 16) & 31;
		ic->f = instr(addi);
		if (ra == 0)
			ic->f = instr(li);
		else
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[1] = (int16_t)(iword & 0xffff);
		if (main_opcode == PPC_HI6_ADDIS)
			ic->arg[1] <<= 16;
		if (ra == 0 && ic->arg[1] == 0)
			ic->f = instr(li_0);
		ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
		break;

	case PPC_HI6_ANDI_DOT:
	case PPC_HI6_ANDIS_DOT:
		rs = (iword >> 21) & 31; ra = (iword >> 16) & 31;
		ic->f = instr(andi_dot);
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
		ic->arg[1] = iword & 0xffff;
		if (main_opcode == PPC_HI6_ANDIS_DOT)
			ic->arg[1] <<= 16;
		ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		break;

	case PPC_HI6_ORI:
	case PPC_HI6_ORIS:
	case PPC_HI6_XORI:
	case PPC_HI6_XORIS:
		rs = (iword >> 21) & 31; ra = (iword >> 16) & 31;
		if (main_opcode == PPC_HI6_ORI ||
		    main_opcode == PPC_HI6_ORIS)
			ic->f = instr(ori);
		else
			ic->f = instr(xori);
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
		ic->arg[1] = iword & 0xffff;
		if (main_opcode == PPC_HI6_ORIS ||
		    main_opcode == PPC_HI6_XORIS)
			ic->arg[1] <<= 16;
		ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		break;

	case PPC_HI6_LBZ:
	case PPC_HI6_LBZU:
	case PPC_HI6_LHZ:
	case PPC_HI6_LHZU:
	case PPC_HI6_LHA:
	case PPC_HI6_LHAU:
	case PPC_HI6_LWZ:
	case PPC_HI6_LWZU:
	case PPC_HI6_LD:
	case PPC_HI6_LFD:
	case PPC_HI6_LFDU:	/*  #310  */
	case PPC_HI6_LFS:
	case PPC_HI6_LFSU:	/*  #310  */
	case PPC_HI6_STB:
	case PPC_HI6_STBU:
	case PPC_HI6_STH:
	case PPC_HI6_STHU:
	case PPC_HI6_STW:
	case PPC_HI6_STWU:
	case PPC_HI6_STD:
	case PPC_HI6_STFD:
	case PPC_HI6_STFDU:	/*  #310  */
	case PPC_HI6_STFS:
	case PPC_HI6_STFSU:	/*  #310  */
		rs = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		imm = (int16_t)iword;
		load = 0; zero = 1; size = 0; update = 0; fp = 0;
		ic->f = NULL;
		switch (main_opcode) {
		case PPC_HI6_LBZ:  load=1; break;
		case PPC_HI6_LBZU: load=1; update=1; break;
		case PPC_HI6_LHA:  load=1; size=1; zero=0; break;
		case PPC_HI6_LHAU: load=1; size=1; zero=0; update=1; break;
		case PPC_HI6_LHZ:  load=1; size=1; break;
		case PPC_HI6_LHZU: load=1; size=1; update=1; break;
		case PPC_HI6_LWZ:  load=1; size=2; break;
		case PPC_HI6_LWZU: load=1; size=2; update=1; break;
		case PPC_HI6_LD:   load=1; size=3; break;
		case PPC_HI6_LFD:  load=1; size=3; fp=1;ic->f=instr(lfd);break;
		case PPC_HI6_LFDU: load=1; size=3; fp=1; update=1;
				   ic->f=instr(lfdu); break;	/*  #310  */
		case PPC_HI6_LFS:  load=1; size=2; fp=1;ic->f=instr(lfs);break;
		case PPC_HI6_LFSU: load=1; size=2; fp=1; update=1;
				   ic->f=instr(lfsu); break;	/*  #310  */
		case PPC_HI6_STB:  break;
		case PPC_HI6_STBU: update=1; break;
		case PPC_HI6_STH:  size=1; break;
		case PPC_HI6_STHU: size=1; update=1; break;
		case PPC_HI6_STW:  size=2; break;
		case PPC_HI6_STWU: size=2; update=1; break;
		case PPC_HI6_STD:  size=3; break;
		case PPC_HI6_STFD: size=3; fp=1; ic->f = instr(stfd); break;
		case PPC_HI6_STFDU: size=3; fp=1; update=1;
				   ic->f = instr(stfdu); break;	/*  #310  */
		case PPC_HI6_STFS: size=2; fp=1; ic->f = instr(stfs); break;
		case PPC_HI6_STFSU: size=2; fp=1; update=1;
				   ic->f = instr(stfsu); break;	/*  #310  */
		}
		if (ic->f == NULL) {
			ic->f =
#ifdef MODE32
			    ppc32_loadstore
#else
			    ppc_loadstore
#endif
			    [size + 4*zero + 8*load + (imm==0? 16 : 0)
			    + 32*update];
		}
		if (ra == 0 && update) {
			if (!cpu->translation_readahead)
				fatal("TODO: ra=0 && update?\n");
			goto bad;
		}
		if (fp)
			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rs]);
		else
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
		if (ra == 0)
			ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
		else
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[2] = (ssize_t)imm;
		break;

	case PPC_HI6_BC:
		aa_bit = (iword >> 1) & 1;
		lk_bit = iword & 1;
		bo = (iword >> 21) & 31;
		bi = (iword >> 16) & 31;
		tmp_addr = (int64_t)(int16_t)(iword & 0xfffc);
		if (aa_bit) {
			if (!cpu->translation_readahead)
				fatal("aa_bit: NOT YET\n");
			goto bad;
		}
		if (lk_bit) {
			ic->f = instr(bcl);
			samepage_function = instr(bcl_samepage);
		} else {
			ic->f = instr(bc);
			if ((bo & 0x14) == 0x04) {
				samepage_function = bo & 8?
				    instr(bc_samepage_simple1) :
				    instr(bc_samepage_simple0);
			} else
				samepage_function = instr(bc_samepage);
		}
		ic->arg[0] = (ssize_t)(tmp_addr + (addr & 0xffc));
		ic->arg[1] = bo;
		ic->arg[2] = 31-bi;
		/*  Branches are calculated as cur PC + offset.  */
		/*  Special case: branch within the same page:  */
		{
			uint64_t mask_within_page =
			    ((PPC_IC_ENTRIES_PER_PAGE-1) << 2) | 3;
			uint64_t old_pc = addr;
			uint64_t new_pc = old_pc + (int32_t)tmp_addr;
			if ((old_pc & ~mask_within_page) ==
			    (new_pc & ~mask_within_page)) {
				ic->f = samepage_function;
				ic->arg[0] = (size_t) (
				    cpu->cd.ppc.cur_ic_page +
				    ((new_pc & mask_within_page) >> 2));
			}
		}
		break;

	case PPC_HI6_SC:
		ic->arg[0] = (iword >> 5) & 0x7f;
		ic->arg[1] = (addr & 0xfff) + 4;
		if (iword == 0x44ee0002) {
			/*  Special case/magic hack for OpenFirmware emul:  */
			ic->f = instr(openfirmware);
		} else
			ic->f = instr(sc);
		break;

	case PPC_HI6_B:
		aa_bit = (iword & 2) >> 1;
		lk_bit = iword & 1;
		tmp_addr = (int64_t)(int32_t)((iword & 0x03fffffc) << 6);
		tmp_addr = (int64_t)tmp_addr >> 6;
		if (lk_bit) {
			if (cpu->machine->show_trace_tree) {
				ic->f = instr(bl_trace);
				samepage_function = instr(bl_samepage_trace);
			} else {
				ic->f = instr(bl);
				samepage_function = instr(bl_samepage);
			}
		} else {
			ic->f = instr(b);
			samepage_function = instr(b_samepage);
		}
		ic->arg[0] = (ssize_t)(tmp_addr + (addr & 0xffc));
		ic->arg[1] = (addr & 0xffc) + 4;
		/*  Branches are calculated as cur PC + offset.  */
		/*  Special case: branch within the same page:  */
		{
			uint64_t mask_within_page =
			    ((PPC_IC_ENTRIES_PER_PAGE-1) << 2) | 3;
			uint64_t old_pc = addr;
			uint64_t new_pc = old_pc + (int32_t)tmp_addr;
			if ((old_pc & ~mask_within_page) ==
			    (new_pc & ~mask_within_page)) {
				ic->f = samepage_function;
				ic->arg[0] = (size_t) (
				    cpu->cd.ppc.cur_ic_page +
				    ((new_pc & mask_within_page) >> 2));
			}
		}
		if (aa_bit) {
			if (lk_bit) {
				if (cpu->machine->show_trace_tree) {
					ic->f = instr(bla_trace);
				} else {
					ic->f = instr(bla);
				}
			} else {
				ic->f = instr(ba);
			}
			ic->arg[0] = (ssize_t)tmp_addr;
		}
		break;

	case PPC_HI6_19:
		xo = (iword >> 1) & 1023;
		switch (xo) {

		case PPC_19_BCLR:
		case PPC_19_BCCTR:
			bo = (iword >> 21) & 31;
			bi = (iword >> 16) & 31;
			bh = (iword >> 11) & 3;
			lk_bit = iword & 1;
			if (xo == PPC_19_BCLR) {
				if (lk_bit)
					ic->f = instr(bclr_l);
				else {
					ic->f = instr(bclr);
					if (!cpu->machine->show_trace_tree &&
					    (bo & 0x14) == 0x14)
						ic->f = instr(bclr_20);
				}
			} else {
				if (!(bo & 4)) {
					if (!cpu->translation_readahead)
						fatal("TODO: bclr/bcctr "
						    "bo bit 2 clear!\n");
					goto bad;
				}
				if (lk_bit)
					ic->f = instr(bcctr_l);
				else
					ic->f = instr(bcctr);
			}
			ic->arg[0] = bo;
			ic->arg[1] = 31 - bi;
			ic->arg[2] = bh;
			break;

		case PPC_19_ISYNC:
			/*  TODO  */
			ic->f = instr(nop);
			break;

		case PPC_19_RFI:
			ic->f = instr(rfi);
			break;

		case PPC_19_RFID:
			ic->f = instr(rfid);
			break;

		case PPC_19_MCRF:
			bf = (iword >> 23) & 7;
			bfa = (iword >> 18) & 7;
			ic->arg[0] = 28 - 4*bf;
			ic->arg[1] = 28 - 4*bfa;
			ic->f = instr(mcrf);
			break;

		case PPC_19_CRAND:
		case PPC_19_CRANDC:
		case PPC_19_CREQV:
		case PPC_19_CROR:
		case PPC_19_CRORC:
		case PPC_19_CRNOR:
		case PPC_19_CRXOR:
			switch (xo) {
			case PPC_19_CRAND:  ic->f = instr(crand); break;
			case PPC_19_CRANDC: ic->f = instr(crandc); break;
			case PPC_19_CREQV:  ic->f = instr(creqv); break;
			case PPC_19_CROR:   ic->f = instr(cror); break;
			case PPC_19_CRORC:  ic->f = instr(crorc); break;
			case PPC_19_CRNOR:  ic->f = instr(crnor); break;
			case PPC_19_CRXOR:  ic->f = instr(crxor); break;
			}
			ic->arg[0] = iword;
			break;

		default:goto bad;
		}
		break;

	case PPC_HI6_RLWNM:
	case PPC_HI6_RLWINM:
		ra = (iword >> 16) & 31;
		mb = (iword >> 6) & 31;
		me = (iword >> 1) & 31;   
		rc = iword & 1;
		mask = 0;
		for (;;) {
			mask |= ((uint32_t)0x80000000 >> mb);
			if (mb == me)
				break;
			mb ++; mb &= 31;
		}
		switch (main_opcode) {
		case PPC_HI6_RLWNM:
			ic->f = rc? instr(rlwnm_dot) : instr(rlwnm); break;
		case PPC_HI6_RLWINM:
			ic->f = rc? instr(rlwinm_dot) : instr(rlwinm); break;
		}
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[1] = mask;
		ic->arg[2] = (uint32_t)iword;
		break;

	case PPC_HI6_RLWIMI:
		rs = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		ic->f = instr(rlwimi);
		ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
		ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[2] = (uint32_t)iword;
		break;

	case PPC_HI6_LMW:
	case PPC_HI6_STMW:
		/*  NOTE: Loads use rt, not rs.  */
		rs = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		ic->arg[0] = rs;
		if (ra == 0)
			ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
		else
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
		ic->arg[2] = (int32_t)(int16_t)iword;
		switch (main_opcode) {
		case PPC_HI6_LMW:
			ic->f = instr(lmw);
			break;
		case PPC_HI6_STMW:
			ic->f = instr(stmw);
			break;
		}
		break;

	case PPC_HI6_30:
		xo = (iword >> 2) & 7;
		switch (xo) {

		case PPC_30_RLDICL:
		case PPC_30_RLDICR:
		case PPC_30_RLDIMI:
			switch (xo) {
			case PPC_30_RLDICL: ic->f = instr(rldicl); break;
			case PPC_30_RLDICR: ic->f = instr(rldicr); break;
			case PPC_30_RLDIMI: ic->f = instr(rldimi); break;
			}
			ic->arg[0] = iword;
			if (cpu->cd.ppc.bits == 32) {
				if (!cpu->translation_readahead)
					fatal("TODO: rld* in 32-bit mode?\n");
				goto bad;
			}
			break;

		default:goto bad;
		}
		break;

	case PPC_HI6_31:
		xo = (iword >> 1) & 1023;
		switch (xo) {

		case PPC_31_CMPL:
		case PPC_31_CMP:
			bf = (iword >> 23) & 7;
			l_bit = (iword >> 21) & 1;
			ra = (iword >> 16) & 31;
			rb = (iword >> 11) & 31;
			if (xo == PPC_31_CMPL) {
				if (l_bit)
					ic->f = instr(cmpld);
				else
					ic->f = instr(cmplw);
			} else {
				if (l_bit)
					ic->f = instr(cmpd);
				else {
					if (bf == 0)
						ic->f = instr(cmpw_cr0);
					else
						ic->f = instr(cmpw);
				}
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->arg[2] = 28 - 4*bf;
			break;

		case PPC_31_CNTLZW:
			rs = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			rc = iword & 1;
			if (rc) {
				if (!cpu->translation_readahead)
					fatal("TODO: rc\n");
				goto bad;
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->f = instr(cntlzw);
			break;

		case PPC_31_MFSPR:
			rt = (iword >> 21) & 31;
			spr = ((iword >> 6) & 0x3e0) + ((iword >> 16) & 31);
			debug_spr_usage(cpu->pc, spr);
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.spr[spr]);
			switch (spr) {
			// Reuse SPR_TB* for TBR_TB*:
			case TBR_TBL: ic->f = instr(mftb); break;
			case TBR_TBU: ic->f = instr(mftbu); break;
			case SPR_PMC1:	ic->f = instr(mfspr_pmc1); break;
			default:	ic->f = instr(mfspr);
			}
			break;

		case PPC_31_MTSPR:
			rs = (iword >> 21) & 31;
			spr = ((iword >> 6) & 0x3e0) + ((iword >> 16) & 31);
			debug_spr_usage(cpu->pc, spr);
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.spr[spr]);
			switch (spr) {
			case SPR_LR:
				ic->f = instr(mtlr);
				break;
			case SPR_CTR:
				ic->f = instr(mtctr);
				break;
			case SPR_SPRG2:
				ic->f = instr(mtspr_sprg2);
				break;
			default:ic->f = instr(mtspr);
			}
			break;

		case PPC_31_MFCR:
			rt = (iword >> 21) & 31;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			ic->f = instr(mfcr);
			break;

		case PPC_31_MFMSR:
			rt = (iword >> 21) & 31;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			ic->f = instr(mfmsr);
			break;

		case PPC_31_MTMSR:
		case PPC_31_MTMSRD:
			rs = (iword >> 21) & 31;
			l_bit = (iword >> 16) & 1;
			if (l_bit) {
				if (!cpu->translation_readahead)
					fatal("TODO: mtmsr l-bit\n");
				goto bad;
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
			ic->arg[1] = (addr & 0xfff) + 4;
			ic->arg[2] = xo == PPC_31_MTMSRD;
			ic->f = instr(mtmsr);
			break;

		case PPC_31_MTCRF:
			rs = (iword >> 21) & 31;
			{
				int i, fxm = (iword >> 12) & 255;
				uint32_t tmp = 0;
				for (i=0; i<8; i++, fxm <<= 1) {
					tmp <<= 4;
					if (fxm & 128)
						tmp |= 0xf;
				}
				ic->arg[1] = (uint32_t)tmp;
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
			ic->f = instr(mtcrf);
			break;

		case PPC_31_MFSRIN:
		case PPC_31_MTSRIN:
			rt = (iword >> 21) & 31;
			rb = (iword >> 11) & 31;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			switch (xo) {
			case PPC_31_MFSRIN: ic->f = instr(mfsrin); break;
			case PPC_31_MTSRIN: ic->f = instr(mtsrin); break;
			}
			if (cpu->cd.ppc.bits == 64) {
				if (!cpu->translation_readahead)
					fatal("Not yet for 64-bit mode\n");
				goto bad;
			}
			break;

		case PPC_31_MFSR:
		case PPC_31_MTSR:
			rt = (iword >> 21) & 31;
			ic->arg[0] = (iword >> 16) & 15;
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			switch (xo) {
			case PPC_31_MFSR:   ic->f = instr(mfsr); break;
			case PPC_31_MTSR:   ic->f = instr(mtsr); break;
			}
			if (cpu->cd.ppc.bits == 64) {
				if (!cpu->translation_readahead)
					fatal("Not yet for 64-bit mode\n");
				goto bad;
			}
			break;

		case PPC_31_SRAWI:
			rs = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			sh = (iword >> 11) & 31;
			rc = iword & 1;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[2] = sh;
			if (rc)
				ic->f = instr(srawi_dot);
			else
				ic->f = instr(srawi);
			break;

		case PPC_31_SYNC:
		case PPC_31_DSSALL:
		case PPC_31_EIEIO:
		case PPC_31_DCBST:
		case PPC_31_DCBTST:
		case PPC_31_DCBF:
		case PPC_31_DCBT:
		case PPC_31_ICBI:
			ic->f = instr(nop);
			break;

		case PPC_31_DCBZ:
			ra = (iword >> 16) & 31;
			rb = (iword >> 11) & 31;
			if (ra == 0)
				ic->arg[0] = (size_t)(&cpu->cd.ppc.zero);
			else
				ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->arg[2] = addr & 0xfff;
			ic->f = instr(dcbz);
			break;

		case PPC_31_TLBIA:
			ic->f = instr(tlbia);
			break;

		case PPC_31_TLBSYNC:
			/*  According to IBM, "Ensures that a tlbie and
			    tlbia instruction executed by one processor has
			    completed on all other processors.", which in
			    GXemul means a nop :-)  */
			ic->f = instr(nop);
			break;

		case PPC_31_TLBIE:
			/*  TODO: POWER also uses ra?  */
			rb = (iword >> 11) & 31;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->f = instr(tlbie);
			break;

		case PPC_31_TLBLD:	/*  takes an arg  */
			rb = (iword >> 11) & 31;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->f = instr(tlbld);
			break;

		case PPC_31_TLBLI:	/*  takes an arg  */
			rb = (iword >> 11) & 31;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->f = instr(tlbli);
			break;

		case PPC_31_TLBSX_DOT:
			/*  TODO  */
			ic->f = instr(tlbsx_dot);
			break;

		case PPC_31_MFTB:
			rt = (iword >> 21) & 31;
			spr = ((iword >> 6) & 0x3e0) + ((iword >> 16) & 31);
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			switch (spr) {
			case 268: ic->f = instr(mftb); break;
			case 269: ic->f = instr(mftbu); break;
			default:if (!cpu->translation_readahead)
					fatal("mftb spr=%i?\n", spr);
				goto bad;
			}
			break;

		case PPC_31_NEG:
			rt = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			rc = iword & 1;
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			if (rc)
				ic->f = instr(neg_dot);
			else
				ic->f = instr(neg);
			break;

		case PPC_31_LWARX:
		case PPC_31_LDARX:
		case PPC_31_STWCX_DOT:
		case PPC_31_STDCX_DOT:
			ic->arg[0] = iword;
			ic->f = instr(llsc);
			break;

		case PPC_31_LSWI:
		case PPC_31_STSWI:
			rs = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			nb = (iword >> 11) & 31;
			ic->arg[0] = rs;
			if (ra == 0)
				ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
			else
				ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[2] = nb == 0? 32 : nb;
			switch (xo) {
			case PPC_31_LSWI:  ic->f = instr(lswi); break;
			case PPC_31_STSWI: ic->f = instr(stswi); break;
			}
			break;

		case PPC_31_WRTEEI:
			ic->arg[0] = iword & 0x8000;
			ic->f = instr(wrteei);
			break;

		case 0x1c3:
			fatal("[ mtdcr: TODO ]\n");
			ic->f = instr(nop);
			break;

		case PPC_31_LBZX:
		case PPC_31_LBZUX:
		case PPC_31_LHAX:
		case PPC_31_LHAUX:
		case PPC_31_LHZX:
		case PPC_31_LHZUX:
		case PPC_31_LWZX:
		case PPC_31_LWZUX:
		case PPC_31_LHBRX:
		case PPC_31_LWBRX:
		case PPC_31_LFDX:
		case PPC_31_LFDUX:	/*  #310  */
		case PPC_31_LFSX:
		case PPC_31_LFSUX:	/*  #310  */
		case PPC_31_STBX:
		case PPC_31_STBUX:
		case PPC_31_STHX:
		case PPC_31_STHUX:
		case PPC_31_STWX:
		case PPC_31_STWUX:
		case PPC_31_STDX:
		case PPC_31_STDUX:
		case PPC_31_STHBRX:
		case PPC_31_STWBRX:
		case PPC_31_STFDX:
		case PPC_31_STFDUX:	/*  #310  */
		case PPC_31_STFSX:
		case PPC_31_STFSUX:	/*  #310  */
			rs = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			rb = (iword >> 11) & 31;
			if (ra == 0)
				ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
			else
				ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			load = 0; zero = 1; size = 0; update = 0;
			byterev = 0; fp = 0;
			ic->f = NULL;
			switch (xo) {
			case PPC_31_LBZX:  load = 1; break;
			case PPC_31_LBZUX: load=update=1; break;
			case PPC_31_LHAX:  size=1; load=1; zero=0; break;
			case PPC_31_LHAUX: size=1; load=update=1; zero=0; break;
			case PPC_31_LHZX:  size=1; load=1; break;
			case PPC_31_LHZUX: size=1; load=update = 1; break;
			case PPC_31_LWZX:  size=2; load=1; break;
			case PPC_31_LWZUX: size=2; load=update = 1; break;
			case PPC_31_LHBRX: size=1; load=1; byterev=1;
					   ic->f = instr(lhbrx); break;
			case PPC_31_LWBRX: size=2; load=1; byterev=1;
					   ic->f = instr(lwbrx); break;
			case PPC_31_LFDX:  size=3; load=1; fp=1;
					   ic->f = instr(lfdx); break;
			case PPC_31_LFDUX: size=3; load=1; fp=1; update=1;
					   ic->f = instr(lfdux); break;	/*  #310  */
			case PPC_31_LFSX:  size=2; load=1; fp=1;
					   ic->f = instr(lfsx); break;
			case PPC_31_LFSUX: size=2; load=1; fp=1; update=1;
					   ic->f = instr(lfsux); break;	/*  #310  */
			case PPC_31_STBX:  break;
			case PPC_31_STBUX: update = 1; break;
			case PPC_31_STHX:  size=1; break;
			case PPC_31_STHUX: size=1; update = 1; break;
			case PPC_31_STWX:  size=2; break;
			case PPC_31_STWUX: size=2; update = 1; break;
			case PPC_31_STDX:  size=3; break;
			case PPC_31_STDUX: size=3; update = 1; break;
			case PPC_31_STHBRX:size=1; byterev = 1;
					   ic->f = instr(sthbrx); break;
			case PPC_31_STWBRX:size=2; byterev = 1;
					   ic->f = instr(stwbrx); break;
			case PPC_31_STFDX: size=3; fp=1;
					   ic->f = instr(stfdx); break;
			case PPC_31_STFDUX:size=3; fp=1; update=1;
					   ic->f = instr(stfdux); break;	/*  #310  */
			case PPC_31_STFSX: size=2; fp=1;
					   ic->f = instr(stfsx); break;
			case PPC_31_STFSUX:size=2; fp=1; update=1;
					   ic->f = instr(stfsux); break;	/*  #310  */
			}
			if (fp)
				ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rs]);
			else
				ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
			if (!byterev && ic->f == NULL) {
				ic->f =
#ifdef MODE32
				    ppc32_loadstore_indexed
#else
				    ppc_loadstore_indexed
#endif
				    [size + 4*zero + 8*load + 16*update];
			}
			if (ra == 0 && update) {
				if (!cpu->translation_readahead)
					fatal("TODO: ra=0 && update?\n");
				goto bad;
			}
			break;

		case PPC_31_EXTSB:
		case PPC_31_EXTSH:
		case PPC_31_EXTSW:
		case PPC_31_SLW:
		case PPC_31_SLD:
		case PPC_31_SRAW:
		case PPC_31_SRW:
		case PPC_31_AND:
		case PPC_31_NAND:
		case PPC_31_ANDC:
		case PPC_31_NOR:
		case PPC_31_OR:
		case PPC_31_ORC:
		case PPC_31_XOR:
		case PPC_31_EQV:
			rs = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			rb = (iword >> 11) & 31;
			rc = iword & 1;
			rc_f = NULL;
			switch (xo) {
			case PPC_31_EXTSB:ic->f = instr(extsb);
					  rc_f  = instr(extsb_dot); break;
			case PPC_31_EXTSH:ic->f = instr(extsh);
					  rc_f  = instr(extsh_dot); break;
			case PPC_31_EXTSW:ic->f = instr(extsw);
					  rc_f  = instr(extsw_dot); break;
			case PPC_31_SLW:  ic->f = instr(slw);
					  rc_f  = instr(slw_dot); break;
			case PPC_31_SLD:  ic->f = instr(sld);
					  rc_f  = instr(sld_dot); break;
			case PPC_31_SRAW: ic->f = instr(sraw);
					  rc_f  = instr(sraw_dot); break;
			case PPC_31_SRW:  ic->f = instr(srw);
					  rc_f  = instr(srw_dot); break;
			case PPC_31_AND:  ic->f = instr(and);
					  rc_f  = instr(and_dot); break;
			case PPC_31_NAND: ic->f = instr(nand);
					  rc_f  = instr(nand_dot); break;
			case PPC_31_ANDC: ic->f = instr(andc);
					  rc_f  = instr(andc_dot); break;
			case PPC_31_NOR:  ic->f = instr(nor);
					  rc_f  = instr(nor_dot); break;
			case PPC_31_OR:   ic->f = rs == rb? instr(mr)
						: instr(or);
					  rc_f  = instr(or_dot); break;
			case PPC_31_ORC:  ic->f = instr(orc);
					  rc_f  = instr(orc_dot); break;
			case PPC_31_XOR:  ic->f = instr(xor);
					  rc_f  = instr(xor_dot); break;
			case PPC_31_EQV:  ic->f = instr(eqv);
					  rc_f  = instr(eqv_dot); break;
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[rs]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			if (rc)
				ic->f = rc_f;
			break;

		case PPC_31_MULLW:
		case PPC_31_MULHW:
		case PPC_31_MULHWU:
		case PPC_31_DIVW:
		case PPC_31_DIVWU:
		case PPC_31_ADD:
		case PPC_31_ADDC:
		case PPC_31_ADDE:
		case PPC_31_ADDME:
		case PPC_31_ADDZE:
		case PPC_31_SUBF:
		case PPC_31_SUBFC:
		case PPC_31_SUBFE:
		case PPC_31_SUBFME:
		case PPC_31_SUBFZE:
			rt = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			rb = (iword >> 11) & 31;
			oe_bit = (iword >> 10) & 1;
			rc = iword & 1;
			if (oe_bit) {
				if (!cpu->translation_readahead)
					fatal("oe_bit not yet implemented\n");
				goto bad;
			}
			switch (xo) {
			case PPC_31_MULLW:  ic->f = instr(mullw); break;
			case PPC_31_MULHW:  ic->f = instr(mulhw); break;
			case PPC_31_MULHWU: ic->f = instr(mulhwu); break;
			case PPC_31_DIVW:   ic->f = instr(divw); n64=1; break;
			case PPC_31_DIVWU:  ic->f = instr(divwu); n64=1; break;
			case PPC_31_ADD:    ic->f = instr(add); break;
			case PPC_31_ADDC:   ic->f = instr(addc); n64=1; break;
			case PPC_31_ADDE:   ic->f = instr(adde); n64=1; break;
			case PPC_31_ADDME:  ic->f = instr(addme); n64=1; break;
			case PPC_31_ADDZE:  ic->f = instr(addze); n64=1; break;
			case PPC_31_SUBF:   ic->f = instr(subf); break;
			case PPC_31_SUBFC:  ic->f = instr(subfc); break;
			case PPC_31_SUBFE:  ic->f = instr(subfe); n64=1; break;
			case PPC_31_SUBFME: ic->f = instr(subfme); n64=1; break;
			case PPC_31_SUBFZE: ic->f = instr(subfze); n64=1;break;
			}
			if (rc) {
				switch (xo) {
				case PPC_31_ADD:
					ic->f = instr(add_dot); break;
				case PPC_31_ADDE:
					ic->f = instr(adde_dot); break;
				case PPC_31_ADDME:
					ic->f = instr(addme_dot); break;
				case PPC_31_ADDZE:
					ic->f = instr(addze_dot); break;
				case PPC_31_DIVW:
					ic->f = instr(divw_dot); break;
				case PPC_31_DIVWU:
					ic->f = instr(divwu_dot); break;
				case PPC_31_MULLW:
					ic->f = instr(mullw_dot); break;
				case PPC_31_MULHW:
					ic->f = instr(mulhw_dot); break;
				case PPC_31_MULHWU:
					ic->f = instr(mulhwu_dot); break;
				case PPC_31_SUBF:
					ic->f = instr(subf_dot); break;
				case PPC_31_SUBFC:
					ic->f = instr(subfc_dot); break;
				case PPC_31_SUBFE:
					ic->f = instr(subfe_dot); break;
				case PPC_31_SUBFME:
					ic->f = instr(subfme_dot); break;
				case PPC_31_SUBFZE:
					ic->f = instr(subfze_dot); break;
				default:if (!cpu->translation_readahead)
						fatal("RC bit not yet "
						    "implemented\n");
					goto bad;
				}
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rt]);
			if (cpu->cd.ppc.bits == 64 && n64) {
				if (!cpu->translation_readahead)
					fatal("Not yet for 64-bit mode\n");
				goto bad;
			}
			break;

		case PPC_31_LVX:
		case PPC_31_LVXL:
		case PPC_31_STVX:
		case PPC_31_STVXL:
			load = 0;
			switch (xo) {
			case PPC_31_LVX:
			case PPC_31_LVXL:
				load = 1; break;
			}
			rs = (iword >> 21) & 31;
			ra = (iword >> 16) & 31;
			rb = (iword >> 11) & 31;
			ic->arg[0] = rs;
			if (ra == 0)
				ic->arg[1] = (size_t)(&cpu->cd.ppc.zero);
			else
				ic->arg[1] = (size_t)(&cpu->cd.ppc.gpr[ra]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.gpr[rb]);
			ic->f = load? instr(lvx) : instr(stvx);
			break;

		default:goto bad;
		}
		break;

	case PPC_HI6_59:
		xo = (iword >>  1) & 1023;
		rt = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		rb = (iword >> 11) & 31;
		rs = (iword >>  6) & 31;	/*  actually frc  */
		rc = iword & 1;

		/*
		 *  #326: Rc=1 no longer stops the emulator. Each case below
		 *  sets rc_f to its record-form twin, and the substitution is
		 *  applied once, after the switch. A case that forgets to set
		 *  rc_f leaves it NULL and still reaches `goto bad` -- so a
		 *  missed record form stays a loud halt rather than becoming a
		 *  silent no-op that executes but never writes CR1. (The
		 *  integer block uses the same rc_f shape with no such guard.)
		 */
		rc_f = NULL;

		/*  NOTE: Some floating-point instructions are selected
		    using only the lowest 5 bits, not all 10!  */
		switch (xo & 31) {
		case PPC_59_FDIVS:
		case PPC_59_FSUBS:
		case PPC_59_FADDS:
			switch (xo & 31) {
			case PPC_59_FDIVS: ic->f = instr(fdivs); rc_f = instr(fdivs_dot); break;
			case PPC_59_FSUBS: ic->f = instr(fsubs); rc_f = instr(fsubs_dot); break;
			case PPC_59_FADDS: ic->f = instr(fadds); rc_f = instr(fadds_dot); break;
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[ra]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[rb]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rt]);
			break;
		case PPC_59_FMULS:
			ic->f = instr(fmuls); rc_f = instr(fmuls_dot);
			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rs]); /* frc */
			break;
		default:/*  Use all 10 bits of xo:  */
			switch (xo) {
			default:goto bad;
			}
		}
		/*  #326: apply the record form, guarded.  */
		if (rc) {
			if (rc_f == NULL)
				goto bad;
			ic->f = rc_f;
		}
		break;

	case PPC_HI6_63:
		xo = (iword >>  1) & 1023;
		rt = (iword >> 21) & 31;
		ra = (iword >> 16) & 31;
		rb = (iword >> 11) & 31;
		rs = (iword >>  6) & 31;	/*  actually frc  */
		rc = iword & 1;

		/*  #326: see the opcode-59 block above.  */
		rc_f = NULL;

		/*  NOTE: Some floating-point instructions are selected
		    using only the lowest 5 bits, not all 10!  */
		switch (xo & 31) {
		case PPC_63_FDIV:
		case PPC_63_FSUB:
		case PPC_63_FADD:
			switch (xo & 31) {
			case PPC_63_FDIV: ic->f = instr(fdiv); rc_f = instr(fdiv_dot); break;
			case PPC_63_FSUB: ic->f = instr(fsub); rc_f = instr(fsub_dot); break;
			case PPC_63_FADD: ic->f = instr(fadd); rc_f = instr(fadd_dot); break;
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[ra]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[rb]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rt]);
			break;
		case PPC_63_FMUL:
			ic->f = instr(fmul); rc_f = instr(fmul_dot);
			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
			ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rs]); /* frc */
			break;
		case PPC_63_FMSUB:
		case PPC_63_FMADD:
			switch (xo & 31) {
			case PPC_63_FMSUB: ic->f = instr(fmsub); rc_f = instr(fmsub_dot); break;
			case PPC_63_FMADD: ic->f = instr(fmadd); rc_f = instr(fmadd_dot); break;
			}
			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
			ic->arg[2] = iword;
			break;
		case PPC_63_FSEL:	/*  #326  */
			ic->f = instr(fsel); rc_f = instr(fsel_dot);
			ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
			ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
			ic->arg[2] = iword;
			break;
		default:/*  Use all 10 bits of xo:  */
			switch (xo) {
			case PPC_63_FCMPU:
				ic->f = instr(fcmpu);
				ic->arg[0] = 28 - 4*(rt >> 2);
				ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[ra]);
				ic->arg[2] = (size_t)(&cpu->cd.ppc.fpr[rb]);
				break;
			case PPC_63_FRSP:
			case PPC_63_FCTIW:	/*  #326  */
			case PPC_63_FCTIWZ:
			case PPC_63_FNEG:
			case PPC_63_FABS:
			case PPC_63_FNABS:	/*  #326  */
			case PPC_63_FMR:
				switch (xo) {
				case PPC_63_FRSP:   ic->f = instr(frsp); rc_f = instr(frsp_dot); break;
				case PPC_63_FCTIW:  ic->f = instr(fctiw); rc_f = instr(fctiw_dot); break;
				case PPC_63_FCTIWZ: ic->f = instr(fctiwz); rc_f = instr(fctiwz_dot);break;
				case PPC_63_FNEG:   ic->f = instr(fneg); rc_f = instr(fneg_dot); break;
				case PPC_63_FABS:   ic->f = instr(fabs); rc_f = instr(fabs_dot); break;
				case PPC_63_FNABS:  ic->f = instr(fnabs); rc_f = instr(fnabs_dot); break;
				case PPC_63_FMR:    ic->f = instr(fmr); rc_f = instr(fmr_dot); break;
				}
				ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rb]);
				ic->arg[1] = (size_t)(&cpu->cd.ppc.fpr[rt]);
				break;

			/*
			 *  #326: the FPSCR control group. BT is the five-bit
			 *  rt field; BF and BFA are three bits each, sitting
			 *  at the TOP of the rt and ra fields, hence the >> 2
			 *  -- the same shape the fcmpu case above uses.
			 */
			case PPC_63_MTFSB0:
			case PPC_63_MTFSB1:
				if (xo == PPC_63_MTFSB0) {
					ic->f = instr(mtfsb0);
					rc_f  = instr(mtfsb0_dot);
				} else {
					ic->f = instr(mtfsb1);
					rc_f  = instr(mtfsb1_dot);
				}
				ic->arg[0] = rt;
				break;
			case PPC_63_MTFSFI:
				ic->f = instr(mtfsfi); rc_f = instr(mtfsfi_dot);
				ic->arg[0] = 28 - 4*(rt >> 2);
				/*  U is the four bits at ISA 16:19, which is
				    the top of the rb field.  */
				ic->arg[1] = (iword >> 12) & 0xf;
				break;
			case PPC_63_MCRFS:
				ic->f = instr(mcrfs);
				ic->arg[0] = 28 - 4*(rt >> 2);
				ic->arg[1] = 28 - 4*(ra >> 2);
				/*
				 *  Book I lists, per BFA, exactly which of the
				 *  copied bits are cleared. Four of the eight
				 *  fields clear NOTHING -- and those are the
				 *  ones that would hurt: field 4 is the FPCC,
				 *  6 the exception enables, 7 the rounding
				 *  mode. Computed here so the handler stays a
				 *  mask-and-go.
				 */
				switch (ra >> 2) {
				case 0:	/*  FX and OX; not FEX/VX  */
					ic->arg[2] = 0x90000000; break;
				case 1:	/*  UX ZX XX VXSNAN  */
					ic->arg[2] = 0x0f000000; break;
				case 2:	/*  VXISI VXIDI VXZDZ VXIMZ  */
					ic->arg[2] = 0x00f00000; break;
				case 3:	/*  VXVC only; NOT FR/FI/C  */
					ic->arg[2] = 0x00080000; break;
				case 5:	/*  VXSOFT VXSQRT VXCVI  */
					ic->arg[2] = 0x00000700; break;
				default:	/*  4, 6, 7: nothing  */
					ic->arg[2] = 0x00000000;
				}
				break;
			case PPC_63_MFFS:
				ic->f = instr(mffs); rc_f = instr(mffs_dot);
				ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rt]);
				break;
			case PPC_63_MTFSF:
				ic->f = instr(mtfsf); rc_f = instr(mtfsf_dot);
				ic->arg[0] = (size_t)(&cpu->cd.ppc.fpr[rb]);
				/*
				 *  #324: the FPSCR is eight FOUR-bit fields,
				 *  one per FM bit, so the stride here is 4.
				 *  It was 8, which spread the mask across
				 *  sixty-four bits: the first four FM bits
				 *  landed entirely above the 32-bit FPSCR and
				 *  wrote nothing at all, and the rest wrote
				 *  the wrong fields. Measured with every field
				 *  selected and a source of all ones, the
				 *  register came back 0x0f0f0f0f instead of
				 *  0xffffffff; FM=0x80 wrote nothing; and
				 *  FM=0x01 was right only by coincidence,
				 *  being the last iteration with no shift
				 *  after it.
				 */
				ic->arg[1] = 0;
				for (bi=7; bi>=0; bi--) {
					ic->arg[1] <<= 4;
					if (iword & (1 << (17+bi)))
						ic->arg[1] |= 0xf;
				}
				/*
				 *  #327: mtfsf may not write FEX or VX either
				 *  -- Book I lists it among the five that
				 *  "cannot alter FPSCR FEX / VX explicitly".
				 *  It was the last one still copying them
				 *  straight out of the source FPR, which #326
				 *  recorded as a divergence and said had to
				 *  land together with the recompute. It does,
				 *  here: masking mtfsf alone would have made
				 *  the phantom-VX state permanent, since its
				 *  unmasked write was the only escape.
				 *
				 *  FX is deliberately NOT masked. mtfsf is one
				 *  of the two instructions exempt from the
				 *  implicit-FX rule, so its FX comes from the
				 *  source and nowhere else; masking it would
				 *  break a legitimate write.
				 */
				ic->arg[1] &= ~(size_t)(PPC_FPSCR_FEX |
				    PPC_FPSCR_VX);
				break;
			default:goto bad;
			}
		}
		/*
		 *  #326: apply the record form. The NULL guard keeps the
		 *  two encodings that have no Rc bit -- fcmpu and mcrfs --
		 *  rejected when their low bit is set, because that is a
		 *  reserved encoding and not a record form.
		 */
		if (rc) {
			if (rc_f == NULL)
				goto bad;
			ic->f = rc_f;
		}
		break;

	default:goto bad;
	}


#define	DYNTRANS_TO_BE_TRANSLATED_TAIL
#include "cpu_dyntrans.c"
#undef	DYNTRANS_TO_BE_TRANSLATED_TAIL
}
