
/*
 *  AUTOMATICALLY GENERATED! Do not edit.
 */

extern size_t dyntrans_cache_size;
#ifdef DYNTRANS_32
#define MODE32
#endif
#define DYNTRANS_FUNCTION_TRACE_DEF riscv_cpu_functioncall_trace
#include "cpu_dyntrans.c"
#undef DYNTRANS_FUNCTION_TRACE_DEF

#define DYNTRANS_INIT_TABLES riscv_cpu_init_tables
#include "cpu_dyntrans.c"
#undef DYNTRANS_INIT_TABLES

#define DYNTRANS_TC_ALLOCATE_DEFAULT_PAGE_DEF riscv_tc_allocate_default_page
#include "cpu_dyntrans.c"
#undef DYNTRANS_TC_ALLOCATE_DEFAULT_PAGE_DEF

#define DYNTRANS_INVAL_ENTRY
#include "cpu_dyntrans.c"
#undef DYNTRANS_INVAL_ENTRY

#define DYNTRANS_INVALIDATE_TC riscv_invalidate_translation_caches
#include "cpu_dyntrans.c"
#undef DYNTRANS_INVALIDATE_TC

#define DYNTRANS_INVALIDATE_TC_CODE riscv_invalidate_code_translation
#include "cpu_dyntrans.c"
#undef DYNTRANS_INVALIDATE_TC_CODE

#define DYNTRANS_UPDATE_TRANSLATION_TABLE riscv_update_translation_table
#include "cpu_dyntrans.c"
#undef DYNTRANS_UPDATE_TRANSLATION_TABLE

#define MEMORY_RW riscv_memory_rw
#define MEM_RISCV
#include "memory_rw.c"
#undef MEM_RISCV
#undef MEMORY_RW

#define DYNTRANS_PC_TO_POINTERS_FUNC riscv_pc_to_pointers
#define DYNTRANS_PC_TO_POINTERS_GENERIC riscv_pc_to_pointers_generic
#include "cpu_dyntrans.c"
#undef DYNTRANS_PC_TO_POINTERS_FUNC

#undef DYNTRANS_PC_TO_POINTERS_GENERIC

#define COMBINE_INSTRUCTIONS riscv_combine_instructions
#ifndef DYNTRANS_32
#define reg(x) (*((uint64_t *)(x)))
#define MODE_uint_t uint64_t
#define MODE_int_t int64_t
#else
#define reg(x) (*((uint32_t *)(x)))
#define MODE_uint_t uint32_t
#define MODE_int_t int32_t
#endif
#define COMBINE(n) riscv_combine_ ## n
#include "quick_pc_to_pointers.h"
#include "cpu_riscv_instr.c"

#define DYNTRANS_RUN_INSTR_DEF riscv_run_instr
#include "cpu_dyntrans.c"
#undef DYNTRANS_RUN_INSTR_DEF

#ifdef DYNTRANS_DUALMODE_32
#undef COMBINE_INSTRUCTIONS
#define COMBINE_INSTRUCTIONS riscv32_combine_instructions
#undef X
#undef instr
#undef reg
#define X(n) void riscv32_instr_ ## n(struct cpu *cpu, \
	struct riscv_instr_call *ic)
#define instr(n) riscv32_instr_ ## n
#ifdef HOST_LITTLE_ENDIAN
#define reg(x) ( *((uint32_t *)(x)) )
#else
#define reg(x) ( *((uint32_t *)(x)+1) )
#endif
#define MODE32
#undef MODE_uint_t
#undef MODE_int_t
#define MODE_uint_t uint32_t
#define MODE_int_t int32_t
#define DYNTRANS_INVAL_ENTRY
#undef DYNTRANS_INVALIDATE_TLB_ENTRY
#define DYNTRANS_INVALIDATE_TLB_ENTRY riscv32_invalidate_tlb_entry
#include "cpu_dyntrans.c"
#undef DYNTRANS_INVAL_ENTRY

#define DYNTRANS_INVALIDATE_TC riscv32_invalidate_translation_caches
#include "cpu_dyntrans.c"
#undef DYNTRANS_INVALIDATE_TC

#define DYNTRANS_INVALIDATE_TC_CODE riscv32_invalidate_code_translation
#include "cpu_dyntrans.c"
#undef DYNTRANS_INVALIDATE_TC_CODE

#define DYNTRANS_UPDATE_TRANSLATION_TABLE riscv32_update_translation_table
#include "cpu_dyntrans.c"
#undef DYNTRANS_UPDATE_TRANSLATION_TABLE

#define DYNTRANS_PC_TO_POINTERS_FUNC riscv32_pc_to_pointers
#define DYNTRANS_PC_TO_POINTERS_GENERIC riscv32_pc_to_pointers_generic
#undef DYNTRANS_PC_TO_POINTERS
#define DYNTRANS_PC_TO_POINTERS riscv32_pc_to_pointers
#include "cpu_dyntrans.c"
#undef DYNTRANS_PC_TO_POINTERS_FUNC

#undef DYNTRANS_PC_TO_POINTERS_GENERIC

#undef COMBINE
#define COMBINE(n) riscv32_combine_ ## n
#include "quick_pc_to_pointers.h"
#include "cpu_riscv_instr.c"

#undef DYNTRANS_PC_TO_POINTERS
#define DYNTRANS_PC_TO_POINTERS riscv_pc_to_pointers
#define DYNTRANS_PC_TO_POINTERS32 riscv32_pc_to_pointers

#define DYNTRANS_RUN_INSTR_DEF riscv32_run_instr
#include "cpu_dyntrans.c"
#undef DYNTRANS_RUN_INSTR_DEF

#endif /*  DYNTRANS_DUALMODE_32  */


CPU_FAMILY_INIT(riscv,"RISCV")

