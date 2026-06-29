
/*  AUTOMATICALLY GENERATED! Do not edit.  */

#include <assert.h>
#include "debugger.h"
#define DYNTRANS_MAX_VPH_TLB_ENTRIES I960_MAX_VPH_TLB_ENTRIES
#define DYNTRANS_ARCH i960
#define DYNTRANS_I960
#ifndef DYNTRANS_32
#define DYNTRANS_L2N I960_L2N
#define DYNTRANS_L3N I960_L3N
#if !defined(I960_L2N) || !defined(I960_L3N)
#error arch_L2N, and arch_L3N must be defined for this arch!
#endif
#define DYNTRANS_L2_64_TABLE i960_l2_64_table
#define DYNTRANS_L3_64_TABLE i960_l3_64_table
#endif
#ifndef DYNTRANS_PAGESIZE
#define DYNTRANS_PAGESIZE 4096
#endif
#define DYNTRANS_IC i960_instr_call
#define DYNTRANS_IC_ENTRIES_PER_PAGE I960_IC_ENTRIES_PER_PAGE
#define DYNTRANS_INSTR_ALIGNMENT_SHIFT I960_INSTR_ALIGNMENT_SHIFT
#define DYNTRANS_TC_PHYSPAGE i960_tc_physpage
#define DYNTRANS_INVALIDATE_TLB_ENTRY i960_invalidate_tlb_entry
#define DYNTRANS_ADDR_TO_PAGENR I960_ADDR_TO_PAGENR
#define DYNTRANS_PC_TO_IC_ENTRY I960_PC_TO_IC_ENTRY
#define DYNTRANS_TC_ALLOCATE i960_tc_allocate_default_page
#define DYNTRANS_TC_PHYSPAGE i960_tc_physpage
#define DYNTRANS_PC_TO_POINTERS i960_pc_to_pointers
#define DYNTRANS_PC_TO_POINTERS_GENERIC i960_pc_to_pointers_generic
#define COMBINE_INSTRUCTIONS i960_combine_instructions
#define DISASSEMBLE i960_cpu_disassemble_instr

extern bool single_step;
extern bool about_to_enter_single_step;
extern int single_step_breakpoint;
extern int old_quiet_mode;
extern int quiet_mode;

/* instr uses the same names as in cpu_i960_instr.c */
#define instr(n) i960_instr_ ## n

#ifdef DYNTRANS_DUALMODE_32
#define instr32(n) i96032_instr_ ## n

#endif


#define X(n) void i960_instr_ ## n(struct cpu *cpu, \
 struct i960_instr_call *ic)

/*
 *  nothing:  Do nothing.
 *
 *  The difference between this function and a "nop" instruction is that
 *  this function does not increase the program counter.  It is used to "get out" of running in translated
 *  mode.
 */
X(nothing)
{
	cpu->cd.i960.next_ic --;
	cpu->ninstrs --;
}

static struct i960_instr_call nothing_call = { instr(nothing), {0,0,0} };

