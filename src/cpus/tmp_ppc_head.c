
/*  AUTOMATICALLY GENERATED! Do not edit.  */

#include <assert.h>
#include "debugger.h"
#define DYNTRANS_MAX_VPH_TLB_ENTRIES PPC_MAX_VPH_TLB_ENTRIES
#define DYNTRANS_ARCH ppc
#define DYNTRANS_PPC
#ifndef DYNTRANS_32
#define DYNTRANS_L2N PPC_L2N
#define DYNTRANS_L3N PPC_L3N
#if !defined(PPC_L2N) || !defined(PPC_L3N)
#error arch_L2N, and arch_L3N must be defined for this arch!
#endif
#define DYNTRANS_L2_64_TABLE ppc_l2_64_table
#define DYNTRANS_L3_64_TABLE ppc_l3_64_table
#endif
#ifndef DYNTRANS_PAGESIZE
#define DYNTRANS_PAGESIZE 4096
#endif
#define DYNTRANS_IC ppc_instr_call
#define DYNTRANS_IC_ENTRIES_PER_PAGE PPC_IC_ENTRIES_PER_PAGE
#define DYNTRANS_INSTR_ALIGNMENT_SHIFT PPC_INSTR_ALIGNMENT_SHIFT
#define DYNTRANS_TC_PHYSPAGE ppc_tc_physpage
#define DYNTRANS_INVALIDATE_TLB_ENTRY ppc_invalidate_tlb_entry
#define DYNTRANS_ADDR_TO_PAGENR PPC_ADDR_TO_PAGENR
#define DYNTRANS_PC_TO_IC_ENTRY PPC_PC_TO_IC_ENTRY
#define DYNTRANS_TC_ALLOCATE ppc_tc_allocate_default_page
#define DYNTRANS_TC_PHYSPAGE ppc_tc_physpage
#define DYNTRANS_PC_TO_POINTERS ppc_pc_to_pointers
#define DYNTRANS_PC_TO_POINTERS_GENERIC ppc_pc_to_pointers_generic
#define COMBINE_INSTRUCTIONS ppc_combine_instructions
#define DISASSEMBLE ppc_cpu_disassemble_instr

extern bool single_step;
extern bool about_to_enter_single_step;
extern int single_step_breakpoint;
extern int old_quiet_mode;
extern int quiet_mode;

/* instr uses the same names as in cpu_ppc_instr.c */
#define instr(n) ppc_instr_ ## n

#ifdef DYNTRANS_DUALMODE_32
#define instr32(n) ppc32_instr_ ## n

#endif


#define X(n) void ppc_instr_ ## n(struct cpu *cpu, \
 struct ppc_instr_call *ic)

/*
 *  nothing:  Do nothing.
 *
 *  The difference between this function and a "nop" instruction is that
 *  this function does not increase the program counter.  It is used to "get out" of running in translated
 *  mode.
 */
X(nothing)
{
	cpu->cd.ppc.next_ic --;
	cpu->ninstrs --;
}

static struct ppc_instr_call nothing_call = { instr(nothing), {0,0,0} };

