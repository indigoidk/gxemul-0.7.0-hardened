
/*  AUTOMATICALLY GENERATED! Do not edit.  */

#include <assert.h>
#include "debugger.h"
#define DYNTRANS_MAX_VPH_TLB_ENTRIES M88K_MAX_VPH_TLB_ENTRIES
#define DYNTRANS_ARCH m88k
#define DYNTRANS_M88K
#ifndef DYNTRANS_32
#define DYNTRANS_L2N M88K_L2N
#define DYNTRANS_L3N M88K_L3N
#if !defined(M88K_L2N) || !defined(M88K_L3N)
#error arch_L2N, and arch_L3N must be defined for this arch!
#endif
#define DYNTRANS_L2_64_TABLE m88k_l2_64_table
#define DYNTRANS_L3_64_TABLE m88k_l3_64_table
#endif
#ifndef DYNTRANS_PAGESIZE
#define DYNTRANS_PAGESIZE 4096
#endif
#define DYNTRANS_IC m88k_instr_call
#define DYNTRANS_IC_ENTRIES_PER_PAGE M88K_IC_ENTRIES_PER_PAGE
#define DYNTRANS_INSTR_ALIGNMENT_SHIFT M88K_INSTR_ALIGNMENT_SHIFT
#define DYNTRANS_TC_PHYSPAGE m88k_tc_physpage
#define DYNTRANS_INVALIDATE_TLB_ENTRY m88k_invalidate_tlb_entry
#define DYNTRANS_ADDR_TO_PAGENR M88K_ADDR_TO_PAGENR
#define DYNTRANS_PC_TO_IC_ENTRY M88K_PC_TO_IC_ENTRY
#define DYNTRANS_TC_ALLOCATE m88k_tc_allocate_default_page
#define DYNTRANS_TC_PHYSPAGE m88k_tc_physpage
#define DYNTRANS_PC_TO_POINTERS m88k_pc_to_pointers
#define DYNTRANS_PC_TO_POINTERS_GENERIC m88k_pc_to_pointers_generic
#define COMBINE_INSTRUCTIONS m88k_combine_instructions
#define DISASSEMBLE m88k_cpu_disassemble_instr

extern bool single_step;
extern bool about_to_enter_single_step;
extern int single_step_breakpoint;
extern int old_quiet_mode;
extern int quiet_mode;

/* instr uses the same names as in cpu_m88k_instr.c */
#define instr(n) m88k_instr_ ## n

#ifdef DYNTRANS_DUALMODE_32
#define instr32(n) m88k32_instr_ ## n

#endif


#define X(n) void m88k_instr_ ## n(struct cpu *cpu, \
 struct m88k_instr_call *ic)

/*
 *  nothing:  Do nothing.
 *
 *  The difference between this function and a "nop" instruction is that
 *  this function does not increase the program counter.  It is used to "get out" of running in translated
 *  mode.
 */
X(nothing)
{
	cpu->cd.m88k.next_ic --;
	cpu->ninstrs --;
}

static struct m88k_instr_call nothing_call = { instr(nothing), {0,0,0} };

