
/*  AUTOMATICALLY GENERATED! Do not edit.  */

#include <assert.h>
#include "debugger.h"
#define DYNTRANS_MAX_VPH_TLB_ENTRIES SH_MAX_VPH_TLB_ENTRIES
#define DYNTRANS_ARCH sh
#define DYNTRANS_SH
#ifndef DYNTRANS_32
#define DYNTRANS_L2N SH_L2N
#define DYNTRANS_L3N SH_L3N
#if !defined(SH_L2N) || !defined(SH_L3N)
#error arch_L2N, and arch_L3N must be defined for this arch!
#endif
#define DYNTRANS_L2_64_TABLE sh_l2_64_table
#define DYNTRANS_L3_64_TABLE sh_l3_64_table
#endif
#ifndef DYNTRANS_PAGESIZE
#define DYNTRANS_PAGESIZE 4096
#endif
#define DYNTRANS_IC sh_instr_call
#define DYNTRANS_IC_ENTRIES_PER_PAGE SH_IC_ENTRIES_PER_PAGE
#define DYNTRANS_INSTR_ALIGNMENT_SHIFT SH_INSTR_ALIGNMENT_SHIFT
#define DYNTRANS_TC_PHYSPAGE sh_tc_physpage
#define DYNTRANS_INVALIDATE_TLB_ENTRY sh_invalidate_tlb_entry
#define DYNTRANS_ADDR_TO_PAGENR SH_ADDR_TO_PAGENR
#define DYNTRANS_PC_TO_IC_ENTRY SH_PC_TO_IC_ENTRY
#define DYNTRANS_TC_ALLOCATE sh_tc_allocate_default_page
#define DYNTRANS_TC_PHYSPAGE sh_tc_physpage
#define DYNTRANS_PC_TO_POINTERS sh_pc_to_pointers
#define DYNTRANS_PC_TO_POINTERS_GENERIC sh_pc_to_pointers_generic
#define COMBINE_INSTRUCTIONS sh_combine_instructions
#define DISASSEMBLE sh_cpu_disassemble_instr

extern bool single_step;
extern bool about_to_enter_single_step;
extern int single_step_breakpoint;
extern int old_quiet_mode;
extern int quiet_mode;

/* instr uses the same names as in cpu_sh_instr.c */
#define instr(n) sh_instr_ ## n

#ifdef DYNTRANS_DUALMODE_32
#define instr32(n) sh32_instr_ ## n

#endif


#define X(n) void sh_instr_ ## n(struct cpu *cpu, \
 struct sh_instr_call *ic)

/*
 *  nothing:  Do nothing.
 *
 *  The difference between this function and a "nop" instruction is that
 *  this function does not increase the program counter.  It is used to "get out" of running in translated
 *  mode.
 */
X(nothing)
{
	cpu->cd.sh.next_ic --;
	cpu->ninstrs --;
}

static struct sh_instr_call nothing_call = { instr(nothing), {0,0} };

