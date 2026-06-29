
/*  AUTOMATICALLY GENERATED! Do not edit.  */

#include <stdio.h>
#include <stdlib.h>
#include "cpu.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"
#define DYNTRANS_PC_TO_POINTERS arm_pc_to_pointers
#include "quick_pc_to_pointers.h"
#define reg(x) (*((uint32_t *)(x)))
extern void arm_instr_nop(struct cpu *, struct arm_instr_call *);
extern void arm_instr_nothing(struct cpu *, struct arm_instr_call *);
extern void arm_instr_invalid(struct cpu *, struct arm_instr_call *);
extern void arm_pc_to_pointers(struct cpu *);
void arm_instr_store_w0_word_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_word_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_word_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_word_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_word_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_word_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_word_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_word_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_word_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w0_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w0_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_store_w1_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);void arm_instr_load_w1_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);

	void (*arm_load_store_instr[1024])(struct cpu *,
		struct arm_instr_call *) = {
	arm_instr_store_w0_word_u0_p0_imm__eq,
	arm_instr_store_w0_word_u0_p0_imm__ne,
	arm_instr_store_w0_word_u0_p0_imm__cs,
	arm_instr_store_w0_word_u0_p0_imm__cc,
	arm_instr_store_w0_word_u0_p0_imm__mi,
	arm_instr_store_w0_word_u0_p0_imm__pl,
	arm_instr_store_w0_word_u0_p0_imm__vs,
	arm_instr_store_w0_word_u0_p0_imm__vc,
	arm_instr_store_w0_word_u0_p0_imm__hi,
	arm_instr_store_w0_word_u0_p0_imm__ls,
	arm_instr_store_w0_word_u0_p0_imm__ge,
	arm_instr_store_w0_word_u0_p0_imm__lt,
	arm_instr_store_w0_word_u0_p0_imm__gt,
	arm_instr_store_w0_word_u0_p0_imm__le,
	arm_instr_store_w0_word_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p0_imm__eq,
	arm_instr_load_w0_word_u0_p0_imm__ne,
	arm_instr_load_w0_word_u0_p0_imm__cs,
	arm_instr_load_w0_word_u0_p0_imm__cc,
	arm_instr_load_w0_word_u0_p0_imm__mi,
	arm_instr_load_w0_word_u0_p0_imm__pl,
	arm_instr_load_w0_word_u0_p0_imm__vs,
	arm_instr_load_w0_word_u0_p0_imm__vc,
	arm_instr_load_w0_word_u0_p0_imm__hi,
	arm_instr_load_w0_word_u0_p0_imm__ls,
	arm_instr_load_w0_word_u0_p0_imm__ge,
	arm_instr_load_w0_word_u0_p0_imm__lt,
	arm_instr_load_w0_word_u0_p0_imm__gt,
	arm_instr_load_w0_word_u0_p0_imm__le,
	arm_instr_load_w0_word_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p0_imm__eq,
	arm_instr_store_w1_word_u0_p0_imm__ne,
	arm_instr_store_w1_word_u0_p0_imm__cs,
	arm_instr_store_w1_word_u0_p0_imm__cc,
	arm_instr_store_w1_word_u0_p0_imm__mi,
	arm_instr_store_w1_word_u0_p0_imm__pl,
	arm_instr_store_w1_word_u0_p0_imm__vs,
	arm_instr_store_w1_word_u0_p0_imm__vc,
	arm_instr_store_w1_word_u0_p0_imm__hi,
	arm_instr_store_w1_word_u0_p0_imm__ls,
	arm_instr_store_w1_word_u0_p0_imm__ge,
	arm_instr_store_w1_word_u0_p0_imm__lt,
	arm_instr_store_w1_word_u0_p0_imm__gt,
	arm_instr_store_w1_word_u0_p0_imm__le,
	arm_instr_store_w1_word_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p0_imm__eq,
	arm_instr_load_w1_word_u0_p0_imm__ne,
	arm_instr_load_w1_word_u0_p0_imm__cs,
	arm_instr_load_w1_word_u0_p0_imm__cc,
	arm_instr_load_w1_word_u0_p0_imm__mi,
	arm_instr_load_w1_word_u0_p0_imm__pl,
	arm_instr_load_w1_word_u0_p0_imm__vs,
	arm_instr_load_w1_word_u0_p0_imm__vc,
	arm_instr_load_w1_word_u0_p0_imm__hi,
	arm_instr_load_w1_word_u0_p0_imm__ls,
	arm_instr_load_w1_word_u0_p0_imm__ge,
	arm_instr_load_w1_word_u0_p0_imm__lt,
	arm_instr_load_w1_word_u0_p0_imm__gt,
	arm_instr_load_w1_word_u0_p0_imm__le,
	arm_instr_load_w1_word_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p0_imm__eq,
	arm_instr_store_w0_byte_u0_p0_imm__ne,
	arm_instr_store_w0_byte_u0_p0_imm__cs,
	arm_instr_store_w0_byte_u0_p0_imm__cc,
	arm_instr_store_w0_byte_u0_p0_imm__mi,
	arm_instr_store_w0_byte_u0_p0_imm__pl,
	arm_instr_store_w0_byte_u0_p0_imm__vs,
	arm_instr_store_w0_byte_u0_p0_imm__vc,
	arm_instr_store_w0_byte_u0_p0_imm__hi,
	arm_instr_store_w0_byte_u0_p0_imm__ls,
	arm_instr_store_w0_byte_u0_p0_imm__ge,
	arm_instr_store_w0_byte_u0_p0_imm__lt,
	arm_instr_store_w0_byte_u0_p0_imm__gt,
	arm_instr_store_w0_byte_u0_p0_imm__le,
	arm_instr_store_w0_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p0_imm__eq,
	arm_instr_load_w0_byte_u0_p0_imm__ne,
	arm_instr_load_w0_byte_u0_p0_imm__cs,
	arm_instr_load_w0_byte_u0_p0_imm__cc,
	arm_instr_load_w0_byte_u0_p0_imm__mi,
	arm_instr_load_w0_byte_u0_p0_imm__pl,
	arm_instr_load_w0_byte_u0_p0_imm__vs,
	arm_instr_load_w0_byte_u0_p0_imm__vc,
	arm_instr_load_w0_byte_u0_p0_imm__hi,
	arm_instr_load_w0_byte_u0_p0_imm__ls,
	arm_instr_load_w0_byte_u0_p0_imm__ge,
	arm_instr_load_w0_byte_u0_p0_imm__lt,
	arm_instr_load_w0_byte_u0_p0_imm__gt,
	arm_instr_load_w0_byte_u0_p0_imm__le,
	arm_instr_load_w0_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p0_imm__eq,
	arm_instr_store_w1_byte_u0_p0_imm__ne,
	arm_instr_store_w1_byte_u0_p0_imm__cs,
	arm_instr_store_w1_byte_u0_p0_imm__cc,
	arm_instr_store_w1_byte_u0_p0_imm__mi,
	arm_instr_store_w1_byte_u0_p0_imm__pl,
	arm_instr_store_w1_byte_u0_p0_imm__vs,
	arm_instr_store_w1_byte_u0_p0_imm__vc,
	arm_instr_store_w1_byte_u0_p0_imm__hi,
	arm_instr_store_w1_byte_u0_p0_imm__ls,
	arm_instr_store_w1_byte_u0_p0_imm__ge,
	arm_instr_store_w1_byte_u0_p0_imm__lt,
	arm_instr_store_w1_byte_u0_p0_imm__gt,
	arm_instr_store_w1_byte_u0_p0_imm__le,
	arm_instr_store_w1_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p0_imm__eq,
	arm_instr_load_w1_byte_u0_p0_imm__ne,
	arm_instr_load_w1_byte_u0_p0_imm__cs,
	arm_instr_load_w1_byte_u0_p0_imm__cc,
	arm_instr_load_w1_byte_u0_p0_imm__mi,
	arm_instr_load_w1_byte_u0_p0_imm__pl,
	arm_instr_load_w1_byte_u0_p0_imm__vs,
	arm_instr_load_w1_byte_u0_p0_imm__vc,
	arm_instr_load_w1_byte_u0_p0_imm__hi,
	arm_instr_load_w1_byte_u0_p0_imm__ls,
	arm_instr_load_w1_byte_u0_p0_imm__ge,
	arm_instr_load_w1_byte_u0_p0_imm__lt,
	arm_instr_load_w1_byte_u0_p0_imm__gt,
	arm_instr_load_w1_byte_u0_p0_imm__le,
	arm_instr_load_w1_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p0_imm__eq,
	arm_instr_store_w0_word_u1_p0_imm__ne,
	arm_instr_store_w0_word_u1_p0_imm__cs,
	arm_instr_store_w0_word_u1_p0_imm__cc,
	arm_instr_store_w0_word_u1_p0_imm__mi,
	arm_instr_store_w0_word_u1_p0_imm__pl,
	arm_instr_store_w0_word_u1_p0_imm__vs,
	arm_instr_store_w0_word_u1_p0_imm__vc,
	arm_instr_store_w0_word_u1_p0_imm__hi,
	arm_instr_store_w0_word_u1_p0_imm__ls,
	arm_instr_store_w0_word_u1_p0_imm__ge,
	arm_instr_store_w0_word_u1_p0_imm__lt,
	arm_instr_store_w0_word_u1_p0_imm__gt,
	arm_instr_store_w0_word_u1_p0_imm__le,
	arm_instr_store_w0_word_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p0_imm__eq,
	arm_instr_load_w0_word_u1_p0_imm__ne,
	arm_instr_load_w0_word_u1_p0_imm__cs,
	arm_instr_load_w0_word_u1_p0_imm__cc,
	arm_instr_load_w0_word_u1_p0_imm__mi,
	arm_instr_load_w0_word_u1_p0_imm__pl,
	arm_instr_load_w0_word_u1_p0_imm__vs,
	arm_instr_load_w0_word_u1_p0_imm__vc,
	arm_instr_load_w0_word_u1_p0_imm__hi,
	arm_instr_load_w0_word_u1_p0_imm__ls,
	arm_instr_load_w0_word_u1_p0_imm__ge,
	arm_instr_load_w0_word_u1_p0_imm__lt,
	arm_instr_load_w0_word_u1_p0_imm__gt,
	arm_instr_load_w0_word_u1_p0_imm__le,
	arm_instr_load_w0_word_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p0_imm__eq,
	arm_instr_store_w1_word_u1_p0_imm__ne,
	arm_instr_store_w1_word_u1_p0_imm__cs,
	arm_instr_store_w1_word_u1_p0_imm__cc,
	arm_instr_store_w1_word_u1_p0_imm__mi,
	arm_instr_store_w1_word_u1_p0_imm__pl,
	arm_instr_store_w1_word_u1_p0_imm__vs,
	arm_instr_store_w1_word_u1_p0_imm__vc,
	arm_instr_store_w1_word_u1_p0_imm__hi,
	arm_instr_store_w1_word_u1_p0_imm__ls,
	arm_instr_store_w1_word_u1_p0_imm__ge,
	arm_instr_store_w1_word_u1_p0_imm__lt,
	arm_instr_store_w1_word_u1_p0_imm__gt,
	arm_instr_store_w1_word_u1_p0_imm__le,
	arm_instr_store_w1_word_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p0_imm__eq,
	arm_instr_load_w1_word_u1_p0_imm__ne,
	arm_instr_load_w1_word_u1_p0_imm__cs,
	arm_instr_load_w1_word_u1_p0_imm__cc,
	arm_instr_load_w1_word_u1_p0_imm__mi,
	arm_instr_load_w1_word_u1_p0_imm__pl,
	arm_instr_load_w1_word_u1_p0_imm__vs,
	arm_instr_load_w1_word_u1_p0_imm__vc,
	arm_instr_load_w1_word_u1_p0_imm__hi,
	arm_instr_load_w1_word_u1_p0_imm__ls,
	arm_instr_load_w1_word_u1_p0_imm__ge,
	arm_instr_load_w1_word_u1_p0_imm__lt,
	arm_instr_load_w1_word_u1_p0_imm__gt,
	arm_instr_load_w1_word_u1_p0_imm__le,
	arm_instr_load_w1_word_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p0_imm__eq,
	arm_instr_store_w0_byte_u1_p0_imm__ne,
	arm_instr_store_w0_byte_u1_p0_imm__cs,
	arm_instr_store_w0_byte_u1_p0_imm__cc,
	arm_instr_store_w0_byte_u1_p0_imm__mi,
	arm_instr_store_w0_byte_u1_p0_imm__pl,
	arm_instr_store_w0_byte_u1_p0_imm__vs,
	arm_instr_store_w0_byte_u1_p0_imm__vc,
	arm_instr_store_w0_byte_u1_p0_imm__hi,
	arm_instr_store_w0_byte_u1_p0_imm__ls,
	arm_instr_store_w0_byte_u1_p0_imm__ge,
	arm_instr_store_w0_byte_u1_p0_imm__lt,
	arm_instr_store_w0_byte_u1_p0_imm__gt,
	arm_instr_store_w0_byte_u1_p0_imm__le,
	arm_instr_store_w0_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p0_imm__eq,
	arm_instr_load_w0_byte_u1_p0_imm__ne,
	arm_instr_load_w0_byte_u1_p0_imm__cs,
	arm_instr_load_w0_byte_u1_p0_imm__cc,
	arm_instr_load_w0_byte_u1_p0_imm__mi,
	arm_instr_load_w0_byte_u1_p0_imm__pl,
	arm_instr_load_w0_byte_u1_p0_imm__vs,
	arm_instr_load_w0_byte_u1_p0_imm__vc,
	arm_instr_load_w0_byte_u1_p0_imm__hi,
	arm_instr_load_w0_byte_u1_p0_imm__ls,
	arm_instr_load_w0_byte_u1_p0_imm__ge,
	arm_instr_load_w0_byte_u1_p0_imm__lt,
	arm_instr_load_w0_byte_u1_p0_imm__gt,
	arm_instr_load_w0_byte_u1_p0_imm__le,
	arm_instr_load_w0_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p0_imm__eq,
	arm_instr_store_w1_byte_u1_p0_imm__ne,
	arm_instr_store_w1_byte_u1_p0_imm__cs,
	arm_instr_store_w1_byte_u1_p0_imm__cc,
	arm_instr_store_w1_byte_u1_p0_imm__mi,
	arm_instr_store_w1_byte_u1_p0_imm__pl,
	arm_instr_store_w1_byte_u1_p0_imm__vs,
	arm_instr_store_w1_byte_u1_p0_imm__vc,
	arm_instr_store_w1_byte_u1_p0_imm__hi,
	arm_instr_store_w1_byte_u1_p0_imm__ls,
	arm_instr_store_w1_byte_u1_p0_imm__ge,
	arm_instr_store_w1_byte_u1_p0_imm__lt,
	arm_instr_store_w1_byte_u1_p0_imm__gt,
	arm_instr_store_w1_byte_u1_p0_imm__le,
	arm_instr_store_w1_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p0_imm__eq,
	arm_instr_load_w1_byte_u1_p0_imm__ne,
	arm_instr_load_w1_byte_u1_p0_imm__cs,
	arm_instr_load_w1_byte_u1_p0_imm__cc,
	arm_instr_load_w1_byte_u1_p0_imm__mi,
	arm_instr_load_w1_byte_u1_p0_imm__pl,
	arm_instr_load_w1_byte_u1_p0_imm__vs,
	arm_instr_load_w1_byte_u1_p0_imm__vc,
	arm_instr_load_w1_byte_u1_p0_imm__hi,
	arm_instr_load_w1_byte_u1_p0_imm__ls,
	arm_instr_load_w1_byte_u1_p0_imm__ge,
	arm_instr_load_w1_byte_u1_p0_imm__lt,
	arm_instr_load_w1_byte_u1_p0_imm__gt,
	arm_instr_load_w1_byte_u1_p0_imm__le,
	arm_instr_load_w1_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_word_u0_p1_imm__eq,
	arm_instr_store_w0_word_u0_p1_imm__ne,
	arm_instr_store_w0_word_u0_p1_imm__cs,
	arm_instr_store_w0_word_u0_p1_imm__cc,
	arm_instr_store_w0_word_u0_p1_imm__mi,
	arm_instr_store_w0_word_u0_p1_imm__pl,
	arm_instr_store_w0_word_u0_p1_imm__vs,
	arm_instr_store_w0_word_u0_p1_imm__vc,
	arm_instr_store_w0_word_u0_p1_imm__hi,
	arm_instr_store_w0_word_u0_p1_imm__ls,
	arm_instr_store_w0_word_u0_p1_imm__ge,
	arm_instr_store_w0_word_u0_p1_imm__lt,
	arm_instr_store_w0_word_u0_p1_imm__gt,
	arm_instr_store_w0_word_u0_p1_imm__le,
	arm_instr_store_w0_word_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p1_imm__eq,
	arm_instr_load_w0_word_u0_p1_imm__ne,
	arm_instr_load_w0_word_u0_p1_imm__cs,
	arm_instr_load_w0_word_u0_p1_imm__cc,
	arm_instr_load_w0_word_u0_p1_imm__mi,
	arm_instr_load_w0_word_u0_p1_imm__pl,
	arm_instr_load_w0_word_u0_p1_imm__vs,
	arm_instr_load_w0_word_u0_p1_imm__vc,
	arm_instr_load_w0_word_u0_p1_imm__hi,
	arm_instr_load_w0_word_u0_p1_imm__ls,
	arm_instr_load_w0_word_u0_p1_imm__ge,
	arm_instr_load_w0_word_u0_p1_imm__lt,
	arm_instr_load_w0_word_u0_p1_imm__gt,
	arm_instr_load_w0_word_u0_p1_imm__le,
	arm_instr_load_w0_word_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p1_imm__eq,
	arm_instr_store_w1_word_u0_p1_imm__ne,
	arm_instr_store_w1_word_u0_p1_imm__cs,
	arm_instr_store_w1_word_u0_p1_imm__cc,
	arm_instr_store_w1_word_u0_p1_imm__mi,
	arm_instr_store_w1_word_u0_p1_imm__pl,
	arm_instr_store_w1_word_u0_p1_imm__vs,
	arm_instr_store_w1_word_u0_p1_imm__vc,
	arm_instr_store_w1_word_u0_p1_imm__hi,
	arm_instr_store_w1_word_u0_p1_imm__ls,
	arm_instr_store_w1_word_u0_p1_imm__ge,
	arm_instr_store_w1_word_u0_p1_imm__lt,
	arm_instr_store_w1_word_u0_p1_imm__gt,
	arm_instr_store_w1_word_u0_p1_imm__le,
	arm_instr_store_w1_word_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p1_imm__eq,
	arm_instr_load_w1_word_u0_p1_imm__ne,
	arm_instr_load_w1_word_u0_p1_imm__cs,
	arm_instr_load_w1_word_u0_p1_imm__cc,
	arm_instr_load_w1_word_u0_p1_imm__mi,
	arm_instr_load_w1_word_u0_p1_imm__pl,
	arm_instr_load_w1_word_u0_p1_imm__vs,
	arm_instr_load_w1_word_u0_p1_imm__vc,
	arm_instr_load_w1_word_u0_p1_imm__hi,
	arm_instr_load_w1_word_u0_p1_imm__ls,
	arm_instr_load_w1_word_u0_p1_imm__ge,
	arm_instr_load_w1_word_u0_p1_imm__lt,
	arm_instr_load_w1_word_u0_p1_imm__gt,
	arm_instr_load_w1_word_u0_p1_imm__le,
	arm_instr_load_w1_word_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p1_imm__eq,
	arm_instr_store_w0_byte_u0_p1_imm__ne,
	arm_instr_store_w0_byte_u0_p1_imm__cs,
	arm_instr_store_w0_byte_u0_p1_imm__cc,
	arm_instr_store_w0_byte_u0_p1_imm__mi,
	arm_instr_store_w0_byte_u0_p1_imm__pl,
	arm_instr_store_w0_byte_u0_p1_imm__vs,
	arm_instr_store_w0_byte_u0_p1_imm__vc,
	arm_instr_store_w0_byte_u0_p1_imm__hi,
	arm_instr_store_w0_byte_u0_p1_imm__ls,
	arm_instr_store_w0_byte_u0_p1_imm__ge,
	arm_instr_store_w0_byte_u0_p1_imm__lt,
	arm_instr_store_w0_byte_u0_p1_imm__gt,
	arm_instr_store_w0_byte_u0_p1_imm__le,
	arm_instr_store_w0_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p1_imm__eq,
	arm_instr_load_w0_byte_u0_p1_imm__ne,
	arm_instr_load_w0_byte_u0_p1_imm__cs,
	arm_instr_load_w0_byte_u0_p1_imm__cc,
	arm_instr_load_w0_byte_u0_p1_imm__mi,
	arm_instr_load_w0_byte_u0_p1_imm__pl,
	arm_instr_load_w0_byte_u0_p1_imm__vs,
	arm_instr_load_w0_byte_u0_p1_imm__vc,
	arm_instr_load_w0_byte_u0_p1_imm__hi,
	arm_instr_load_w0_byte_u0_p1_imm__ls,
	arm_instr_load_w0_byte_u0_p1_imm__ge,
	arm_instr_load_w0_byte_u0_p1_imm__lt,
	arm_instr_load_w0_byte_u0_p1_imm__gt,
	arm_instr_load_w0_byte_u0_p1_imm__le,
	arm_instr_load_w0_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p1_imm__eq,
	arm_instr_store_w1_byte_u0_p1_imm__ne,
	arm_instr_store_w1_byte_u0_p1_imm__cs,
	arm_instr_store_w1_byte_u0_p1_imm__cc,
	arm_instr_store_w1_byte_u0_p1_imm__mi,
	arm_instr_store_w1_byte_u0_p1_imm__pl,
	arm_instr_store_w1_byte_u0_p1_imm__vs,
	arm_instr_store_w1_byte_u0_p1_imm__vc,
	arm_instr_store_w1_byte_u0_p1_imm__hi,
	arm_instr_store_w1_byte_u0_p1_imm__ls,
	arm_instr_store_w1_byte_u0_p1_imm__ge,
	arm_instr_store_w1_byte_u0_p1_imm__lt,
	arm_instr_store_w1_byte_u0_p1_imm__gt,
	arm_instr_store_w1_byte_u0_p1_imm__le,
	arm_instr_store_w1_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p1_imm__eq,
	arm_instr_load_w1_byte_u0_p1_imm__ne,
	arm_instr_load_w1_byte_u0_p1_imm__cs,
	arm_instr_load_w1_byte_u0_p1_imm__cc,
	arm_instr_load_w1_byte_u0_p1_imm__mi,
	arm_instr_load_w1_byte_u0_p1_imm__pl,
	arm_instr_load_w1_byte_u0_p1_imm__vs,
	arm_instr_load_w1_byte_u0_p1_imm__vc,
	arm_instr_load_w1_byte_u0_p1_imm__hi,
	arm_instr_load_w1_byte_u0_p1_imm__ls,
	arm_instr_load_w1_byte_u0_p1_imm__ge,
	arm_instr_load_w1_byte_u0_p1_imm__lt,
	arm_instr_load_w1_byte_u0_p1_imm__gt,
	arm_instr_load_w1_byte_u0_p1_imm__le,
	arm_instr_load_w1_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p1_imm__eq,
	arm_instr_store_w0_word_u1_p1_imm__ne,
	arm_instr_store_w0_word_u1_p1_imm__cs,
	arm_instr_store_w0_word_u1_p1_imm__cc,
	arm_instr_store_w0_word_u1_p1_imm__mi,
	arm_instr_store_w0_word_u1_p1_imm__pl,
	arm_instr_store_w0_word_u1_p1_imm__vs,
	arm_instr_store_w0_word_u1_p1_imm__vc,
	arm_instr_store_w0_word_u1_p1_imm__hi,
	arm_instr_store_w0_word_u1_p1_imm__ls,
	arm_instr_store_w0_word_u1_p1_imm__ge,
	arm_instr_store_w0_word_u1_p1_imm__lt,
	arm_instr_store_w0_word_u1_p1_imm__gt,
	arm_instr_store_w0_word_u1_p1_imm__le,
	arm_instr_store_w0_word_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p1_imm__eq,
	arm_instr_load_w0_word_u1_p1_imm__ne,
	arm_instr_load_w0_word_u1_p1_imm__cs,
	arm_instr_load_w0_word_u1_p1_imm__cc,
	arm_instr_load_w0_word_u1_p1_imm__mi,
	arm_instr_load_w0_word_u1_p1_imm__pl,
	arm_instr_load_w0_word_u1_p1_imm__vs,
	arm_instr_load_w0_word_u1_p1_imm__vc,
	arm_instr_load_w0_word_u1_p1_imm__hi,
	arm_instr_load_w0_word_u1_p1_imm__ls,
	arm_instr_load_w0_word_u1_p1_imm__ge,
	arm_instr_load_w0_word_u1_p1_imm__lt,
	arm_instr_load_w0_word_u1_p1_imm__gt,
	arm_instr_load_w0_word_u1_p1_imm__le,
	arm_instr_load_w0_word_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p1_imm__eq,
	arm_instr_store_w1_word_u1_p1_imm__ne,
	arm_instr_store_w1_word_u1_p1_imm__cs,
	arm_instr_store_w1_word_u1_p1_imm__cc,
	arm_instr_store_w1_word_u1_p1_imm__mi,
	arm_instr_store_w1_word_u1_p1_imm__pl,
	arm_instr_store_w1_word_u1_p1_imm__vs,
	arm_instr_store_w1_word_u1_p1_imm__vc,
	arm_instr_store_w1_word_u1_p1_imm__hi,
	arm_instr_store_w1_word_u1_p1_imm__ls,
	arm_instr_store_w1_word_u1_p1_imm__ge,
	arm_instr_store_w1_word_u1_p1_imm__lt,
	arm_instr_store_w1_word_u1_p1_imm__gt,
	arm_instr_store_w1_word_u1_p1_imm__le,
	arm_instr_store_w1_word_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p1_imm__eq,
	arm_instr_load_w1_word_u1_p1_imm__ne,
	arm_instr_load_w1_word_u1_p1_imm__cs,
	arm_instr_load_w1_word_u1_p1_imm__cc,
	arm_instr_load_w1_word_u1_p1_imm__mi,
	arm_instr_load_w1_word_u1_p1_imm__pl,
	arm_instr_load_w1_word_u1_p1_imm__vs,
	arm_instr_load_w1_word_u1_p1_imm__vc,
	arm_instr_load_w1_word_u1_p1_imm__hi,
	arm_instr_load_w1_word_u1_p1_imm__ls,
	arm_instr_load_w1_word_u1_p1_imm__ge,
	arm_instr_load_w1_word_u1_p1_imm__lt,
	arm_instr_load_w1_word_u1_p1_imm__gt,
	arm_instr_load_w1_word_u1_p1_imm__le,
	arm_instr_load_w1_word_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p1_imm__eq,
	arm_instr_store_w0_byte_u1_p1_imm__ne,
	arm_instr_store_w0_byte_u1_p1_imm__cs,
	arm_instr_store_w0_byte_u1_p1_imm__cc,
	arm_instr_store_w0_byte_u1_p1_imm__mi,
	arm_instr_store_w0_byte_u1_p1_imm__pl,
	arm_instr_store_w0_byte_u1_p1_imm__vs,
	arm_instr_store_w0_byte_u1_p1_imm__vc,
	arm_instr_store_w0_byte_u1_p1_imm__hi,
	arm_instr_store_w0_byte_u1_p1_imm__ls,
	arm_instr_store_w0_byte_u1_p1_imm__ge,
	arm_instr_store_w0_byte_u1_p1_imm__lt,
	arm_instr_store_w0_byte_u1_p1_imm__gt,
	arm_instr_store_w0_byte_u1_p1_imm__le,
	arm_instr_store_w0_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p1_imm__eq,
	arm_instr_load_w0_byte_u1_p1_imm__ne,
	arm_instr_load_w0_byte_u1_p1_imm__cs,
	arm_instr_load_w0_byte_u1_p1_imm__cc,
	arm_instr_load_w0_byte_u1_p1_imm__mi,
	arm_instr_load_w0_byte_u1_p1_imm__pl,
	arm_instr_load_w0_byte_u1_p1_imm__vs,
	arm_instr_load_w0_byte_u1_p1_imm__vc,
	arm_instr_load_w0_byte_u1_p1_imm__hi,
	arm_instr_load_w0_byte_u1_p1_imm__ls,
	arm_instr_load_w0_byte_u1_p1_imm__ge,
	arm_instr_load_w0_byte_u1_p1_imm__lt,
	arm_instr_load_w0_byte_u1_p1_imm__gt,
	arm_instr_load_w0_byte_u1_p1_imm__le,
	arm_instr_load_w0_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p1_imm__eq,
	arm_instr_store_w1_byte_u1_p1_imm__ne,
	arm_instr_store_w1_byte_u1_p1_imm__cs,
	arm_instr_store_w1_byte_u1_p1_imm__cc,
	arm_instr_store_w1_byte_u1_p1_imm__mi,
	arm_instr_store_w1_byte_u1_p1_imm__pl,
	arm_instr_store_w1_byte_u1_p1_imm__vs,
	arm_instr_store_w1_byte_u1_p1_imm__vc,
	arm_instr_store_w1_byte_u1_p1_imm__hi,
	arm_instr_store_w1_byte_u1_p1_imm__ls,
	arm_instr_store_w1_byte_u1_p1_imm__ge,
	arm_instr_store_w1_byte_u1_p1_imm__lt,
	arm_instr_store_w1_byte_u1_p1_imm__gt,
	arm_instr_store_w1_byte_u1_p1_imm__le,
	arm_instr_store_w1_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p1_imm__eq,
	arm_instr_load_w1_byte_u1_p1_imm__ne,
	arm_instr_load_w1_byte_u1_p1_imm__cs,
	arm_instr_load_w1_byte_u1_p1_imm__cc,
	arm_instr_load_w1_byte_u1_p1_imm__mi,
	arm_instr_load_w1_byte_u1_p1_imm__pl,
	arm_instr_load_w1_byte_u1_p1_imm__vs,
	arm_instr_load_w1_byte_u1_p1_imm__vc,
	arm_instr_load_w1_byte_u1_p1_imm__hi,
	arm_instr_load_w1_byte_u1_p1_imm__ls,
	arm_instr_load_w1_byte_u1_p1_imm__ge,
	arm_instr_load_w1_byte_u1_p1_imm__lt,
	arm_instr_load_w1_byte_u1_p1_imm__gt,
	arm_instr_load_w1_byte_u1_p1_imm__le,
	arm_instr_load_w1_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_word_u0_p0_reg__eq,
	arm_instr_store_w0_word_u0_p0_reg__ne,
	arm_instr_store_w0_word_u0_p0_reg__cs,
	arm_instr_store_w0_word_u0_p0_reg__cc,
	arm_instr_store_w0_word_u0_p0_reg__mi,
	arm_instr_store_w0_word_u0_p0_reg__pl,
	arm_instr_store_w0_word_u0_p0_reg__vs,
	arm_instr_store_w0_word_u0_p0_reg__vc,
	arm_instr_store_w0_word_u0_p0_reg__hi,
	arm_instr_store_w0_word_u0_p0_reg__ls,
	arm_instr_store_w0_word_u0_p0_reg__ge,
	arm_instr_store_w0_word_u0_p0_reg__lt,
	arm_instr_store_w0_word_u0_p0_reg__gt,
	arm_instr_store_w0_word_u0_p0_reg__le,
	arm_instr_store_w0_word_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p0_reg__eq,
	arm_instr_load_w0_word_u0_p0_reg__ne,
	arm_instr_load_w0_word_u0_p0_reg__cs,
	arm_instr_load_w0_word_u0_p0_reg__cc,
	arm_instr_load_w0_word_u0_p0_reg__mi,
	arm_instr_load_w0_word_u0_p0_reg__pl,
	arm_instr_load_w0_word_u0_p0_reg__vs,
	arm_instr_load_w0_word_u0_p0_reg__vc,
	arm_instr_load_w0_word_u0_p0_reg__hi,
	arm_instr_load_w0_word_u0_p0_reg__ls,
	arm_instr_load_w0_word_u0_p0_reg__ge,
	arm_instr_load_w0_word_u0_p0_reg__lt,
	arm_instr_load_w0_word_u0_p0_reg__gt,
	arm_instr_load_w0_word_u0_p0_reg__le,
	arm_instr_load_w0_word_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p0_reg__eq,
	arm_instr_store_w1_word_u0_p0_reg__ne,
	arm_instr_store_w1_word_u0_p0_reg__cs,
	arm_instr_store_w1_word_u0_p0_reg__cc,
	arm_instr_store_w1_word_u0_p0_reg__mi,
	arm_instr_store_w1_word_u0_p0_reg__pl,
	arm_instr_store_w1_word_u0_p0_reg__vs,
	arm_instr_store_w1_word_u0_p0_reg__vc,
	arm_instr_store_w1_word_u0_p0_reg__hi,
	arm_instr_store_w1_word_u0_p0_reg__ls,
	arm_instr_store_w1_word_u0_p0_reg__ge,
	arm_instr_store_w1_word_u0_p0_reg__lt,
	arm_instr_store_w1_word_u0_p0_reg__gt,
	arm_instr_store_w1_word_u0_p0_reg__le,
	arm_instr_store_w1_word_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p0_reg__eq,
	arm_instr_load_w1_word_u0_p0_reg__ne,
	arm_instr_load_w1_word_u0_p0_reg__cs,
	arm_instr_load_w1_word_u0_p0_reg__cc,
	arm_instr_load_w1_word_u0_p0_reg__mi,
	arm_instr_load_w1_word_u0_p0_reg__pl,
	arm_instr_load_w1_word_u0_p0_reg__vs,
	arm_instr_load_w1_word_u0_p0_reg__vc,
	arm_instr_load_w1_word_u0_p0_reg__hi,
	arm_instr_load_w1_word_u0_p0_reg__ls,
	arm_instr_load_w1_word_u0_p0_reg__ge,
	arm_instr_load_w1_word_u0_p0_reg__lt,
	arm_instr_load_w1_word_u0_p0_reg__gt,
	arm_instr_load_w1_word_u0_p0_reg__le,
	arm_instr_load_w1_word_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p0_reg__eq,
	arm_instr_store_w0_byte_u0_p0_reg__ne,
	arm_instr_store_w0_byte_u0_p0_reg__cs,
	arm_instr_store_w0_byte_u0_p0_reg__cc,
	arm_instr_store_w0_byte_u0_p0_reg__mi,
	arm_instr_store_w0_byte_u0_p0_reg__pl,
	arm_instr_store_w0_byte_u0_p0_reg__vs,
	arm_instr_store_w0_byte_u0_p0_reg__vc,
	arm_instr_store_w0_byte_u0_p0_reg__hi,
	arm_instr_store_w0_byte_u0_p0_reg__ls,
	arm_instr_store_w0_byte_u0_p0_reg__ge,
	arm_instr_store_w0_byte_u0_p0_reg__lt,
	arm_instr_store_w0_byte_u0_p0_reg__gt,
	arm_instr_store_w0_byte_u0_p0_reg__le,
	arm_instr_store_w0_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p0_reg__eq,
	arm_instr_load_w0_byte_u0_p0_reg__ne,
	arm_instr_load_w0_byte_u0_p0_reg__cs,
	arm_instr_load_w0_byte_u0_p0_reg__cc,
	arm_instr_load_w0_byte_u0_p0_reg__mi,
	arm_instr_load_w0_byte_u0_p0_reg__pl,
	arm_instr_load_w0_byte_u0_p0_reg__vs,
	arm_instr_load_w0_byte_u0_p0_reg__vc,
	arm_instr_load_w0_byte_u0_p0_reg__hi,
	arm_instr_load_w0_byte_u0_p0_reg__ls,
	arm_instr_load_w0_byte_u0_p0_reg__ge,
	arm_instr_load_w0_byte_u0_p0_reg__lt,
	arm_instr_load_w0_byte_u0_p0_reg__gt,
	arm_instr_load_w0_byte_u0_p0_reg__le,
	arm_instr_load_w0_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p0_reg__eq,
	arm_instr_store_w1_byte_u0_p0_reg__ne,
	arm_instr_store_w1_byte_u0_p0_reg__cs,
	arm_instr_store_w1_byte_u0_p0_reg__cc,
	arm_instr_store_w1_byte_u0_p0_reg__mi,
	arm_instr_store_w1_byte_u0_p0_reg__pl,
	arm_instr_store_w1_byte_u0_p0_reg__vs,
	arm_instr_store_w1_byte_u0_p0_reg__vc,
	arm_instr_store_w1_byte_u0_p0_reg__hi,
	arm_instr_store_w1_byte_u0_p0_reg__ls,
	arm_instr_store_w1_byte_u0_p0_reg__ge,
	arm_instr_store_w1_byte_u0_p0_reg__lt,
	arm_instr_store_w1_byte_u0_p0_reg__gt,
	arm_instr_store_w1_byte_u0_p0_reg__le,
	arm_instr_store_w1_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p0_reg__eq,
	arm_instr_load_w1_byte_u0_p0_reg__ne,
	arm_instr_load_w1_byte_u0_p0_reg__cs,
	arm_instr_load_w1_byte_u0_p0_reg__cc,
	arm_instr_load_w1_byte_u0_p0_reg__mi,
	arm_instr_load_w1_byte_u0_p0_reg__pl,
	arm_instr_load_w1_byte_u0_p0_reg__vs,
	arm_instr_load_w1_byte_u0_p0_reg__vc,
	arm_instr_load_w1_byte_u0_p0_reg__hi,
	arm_instr_load_w1_byte_u0_p0_reg__ls,
	arm_instr_load_w1_byte_u0_p0_reg__ge,
	arm_instr_load_w1_byte_u0_p0_reg__lt,
	arm_instr_load_w1_byte_u0_p0_reg__gt,
	arm_instr_load_w1_byte_u0_p0_reg__le,
	arm_instr_load_w1_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p0_reg__eq,
	arm_instr_store_w0_word_u1_p0_reg__ne,
	arm_instr_store_w0_word_u1_p0_reg__cs,
	arm_instr_store_w0_word_u1_p0_reg__cc,
	arm_instr_store_w0_word_u1_p0_reg__mi,
	arm_instr_store_w0_word_u1_p0_reg__pl,
	arm_instr_store_w0_word_u1_p0_reg__vs,
	arm_instr_store_w0_word_u1_p0_reg__vc,
	arm_instr_store_w0_word_u1_p0_reg__hi,
	arm_instr_store_w0_word_u1_p0_reg__ls,
	arm_instr_store_w0_word_u1_p0_reg__ge,
	arm_instr_store_w0_word_u1_p0_reg__lt,
	arm_instr_store_w0_word_u1_p0_reg__gt,
	arm_instr_store_w0_word_u1_p0_reg__le,
	arm_instr_store_w0_word_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p0_reg__eq,
	arm_instr_load_w0_word_u1_p0_reg__ne,
	arm_instr_load_w0_word_u1_p0_reg__cs,
	arm_instr_load_w0_word_u1_p0_reg__cc,
	arm_instr_load_w0_word_u1_p0_reg__mi,
	arm_instr_load_w0_word_u1_p0_reg__pl,
	arm_instr_load_w0_word_u1_p0_reg__vs,
	arm_instr_load_w0_word_u1_p0_reg__vc,
	arm_instr_load_w0_word_u1_p0_reg__hi,
	arm_instr_load_w0_word_u1_p0_reg__ls,
	arm_instr_load_w0_word_u1_p0_reg__ge,
	arm_instr_load_w0_word_u1_p0_reg__lt,
	arm_instr_load_w0_word_u1_p0_reg__gt,
	arm_instr_load_w0_word_u1_p0_reg__le,
	arm_instr_load_w0_word_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p0_reg__eq,
	arm_instr_store_w1_word_u1_p0_reg__ne,
	arm_instr_store_w1_word_u1_p0_reg__cs,
	arm_instr_store_w1_word_u1_p0_reg__cc,
	arm_instr_store_w1_word_u1_p0_reg__mi,
	arm_instr_store_w1_word_u1_p0_reg__pl,
	arm_instr_store_w1_word_u1_p0_reg__vs,
	arm_instr_store_w1_word_u1_p0_reg__vc,
	arm_instr_store_w1_word_u1_p0_reg__hi,
	arm_instr_store_w1_word_u1_p0_reg__ls,
	arm_instr_store_w1_word_u1_p0_reg__ge,
	arm_instr_store_w1_word_u1_p0_reg__lt,
	arm_instr_store_w1_word_u1_p0_reg__gt,
	arm_instr_store_w1_word_u1_p0_reg__le,
	arm_instr_store_w1_word_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p0_reg__eq,
	arm_instr_load_w1_word_u1_p0_reg__ne,
	arm_instr_load_w1_word_u1_p0_reg__cs,
	arm_instr_load_w1_word_u1_p0_reg__cc,
	arm_instr_load_w1_word_u1_p0_reg__mi,
	arm_instr_load_w1_word_u1_p0_reg__pl,
	arm_instr_load_w1_word_u1_p0_reg__vs,
	arm_instr_load_w1_word_u1_p0_reg__vc,
	arm_instr_load_w1_word_u1_p0_reg__hi,
	arm_instr_load_w1_word_u1_p0_reg__ls,
	arm_instr_load_w1_word_u1_p0_reg__ge,
	arm_instr_load_w1_word_u1_p0_reg__lt,
	arm_instr_load_w1_word_u1_p0_reg__gt,
	arm_instr_load_w1_word_u1_p0_reg__le,
	arm_instr_load_w1_word_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p0_reg__eq,
	arm_instr_store_w0_byte_u1_p0_reg__ne,
	arm_instr_store_w0_byte_u1_p0_reg__cs,
	arm_instr_store_w0_byte_u1_p0_reg__cc,
	arm_instr_store_w0_byte_u1_p0_reg__mi,
	arm_instr_store_w0_byte_u1_p0_reg__pl,
	arm_instr_store_w0_byte_u1_p0_reg__vs,
	arm_instr_store_w0_byte_u1_p0_reg__vc,
	arm_instr_store_w0_byte_u1_p0_reg__hi,
	arm_instr_store_w0_byte_u1_p0_reg__ls,
	arm_instr_store_w0_byte_u1_p0_reg__ge,
	arm_instr_store_w0_byte_u1_p0_reg__lt,
	arm_instr_store_w0_byte_u1_p0_reg__gt,
	arm_instr_store_w0_byte_u1_p0_reg__le,
	arm_instr_store_w0_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p0_reg__eq,
	arm_instr_load_w0_byte_u1_p0_reg__ne,
	arm_instr_load_w0_byte_u1_p0_reg__cs,
	arm_instr_load_w0_byte_u1_p0_reg__cc,
	arm_instr_load_w0_byte_u1_p0_reg__mi,
	arm_instr_load_w0_byte_u1_p0_reg__pl,
	arm_instr_load_w0_byte_u1_p0_reg__vs,
	arm_instr_load_w0_byte_u1_p0_reg__vc,
	arm_instr_load_w0_byte_u1_p0_reg__hi,
	arm_instr_load_w0_byte_u1_p0_reg__ls,
	arm_instr_load_w0_byte_u1_p0_reg__ge,
	arm_instr_load_w0_byte_u1_p0_reg__lt,
	arm_instr_load_w0_byte_u1_p0_reg__gt,
	arm_instr_load_w0_byte_u1_p0_reg__le,
	arm_instr_load_w0_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p0_reg__eq,
	arm_instr_store_w1_byte_u1_p0_reg__ne,
	arm_instr_store_w1_byte_u1_p0_reg__cs,
	arm_instr_store_w1_byte_u1_p0_reg__cc,
	arm_instr_store_w1_byte_u1_p0_reg__mi,
	arm_instr_store_w1_byte_u1_p0_reg__pl,
	arm_instr_store_w1_byte_u1_p0_reg__vs,
	arm_instr_store_w1_byte_u1_p0_reg__vc,
	arm_instr_store_w1_byte_u1_p0_reg__hi,
	arm_instr_store_w1_byte_u1_p0_reg__ls,
	arm_instr_store_w1_byte_u1_p0_reg__ge,
	arm_instr_store_w1_byte_u1_p0_reg__lt,
	arm_instr_store_w1_byte_u1_p0_reg__gt,
	arm_instr_store_w1_byte_u1_p0_reg__le,
	arm_instr_store_w1_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p0_reg__eq,
	arm_instr_load_w1_byte_u1_p0_reg__ne,
	arm_instr_load_w1_byte_u1_p0_reg__cs,
	arm_instr_load_w1_byte_u1_p0_reg__cc,
	arm_instr_load_w1_byte_u1_p0_reg__mi,
	arm_instr_load_w1_byte_u1_p0_reg__pl,
	arm_instr_load_w1_byte_u1_p0_reg__vs,
	arm_instr_load_w1_byte_u1_p0_reg__vc,
	arm_instr_load_w1_byte_u1_p0_reg__hi,
	arm_instr_load_w1_byte_u1_p0_reg__ls,
	arm_instr_load_w1_byte_u1_p0_reg__ge,
	arm_instr_load_w1_byte_u1_p0_reg__lt,
	arm_instr_load_w1_byte_u1_p0_reg__gt,
	arm_instr_load_w1_byte_u1_p0_reg__le,
	arm_instr_load_w1_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_word_u0_p1_reg__eq,
	arm_instr_store_w0_word_u0_p1_reg__ne,
	arm_instr_store_w0_word_u0_p1_reg__cs,
	arm_instr_store_w0_word_u0_p1_reg__cc,
	arm_instr_store_w0_word_u0_p1_reg__mi,
	arm_instr_store_w0_word_u0_p1_reg__pl,
	arm_instr_store_w0_word_u0_p1_reg__vs,
	arm_instr_store_w0_word_u0_p1_reg__vc,
	arm_instr_store_w0_word_u0_p1_reg__hi,
	arm_instr_store_w0_word_u0_p1_reg__ls,
	arm_instr_store_w0_word_u0_p1_reg__ge,
	arm_instr_store_w0_word_u0_p1_reg__lt,
	arm_instr_store_w0_word_u0_p1_reg__gt,
	arm_instr_store_w0_word_u0_p1_reg__le,
	arm_instr_store_w0_word_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p1_reg__eq,
	arm_instr_load_w0_word_u0_p1_reg__ne,
	arm_instr_load_w0_word_u0_p1_reg__cs,
	arm_instr_load_w0_word_u0_p1_reg__cc,
	arm_instr_load_w0_word_u0_p1_reg__mi,
	arm_instr_load_w0_word_u0_p1_reg__pl,
	arm_instr_load_w0_word_u0_p1_reg__vs,
	arm_instr_load_w0_word_u0_p1_reg__vc,
	arm_instr_load_w0_word_u0_p1_reg__hi,
	arm_instr_load_w0_word_u0_p1_reg__ls,
	arm_instr_load_w0_word_u0_p1_reg__ge,
	arm_instr_load_w0_word_u0_p1_reg__lt,
	arm_instr_load_w0_word_u0_p1_reg__gt,
	arm_instr_load_w0_word_u0_p1_reg__le,
	arm_instr_load_w0_word_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p1_reg__eq,
	arm_instr_store_w1_word_u0_p1_reg__ne,
	arm_instr_store_w1_word_u0_p1_reg__cs,
	arm_instr_store_w1_word_u0_p1_reg__cc,
	arm_instr_store_w1_word_u0_p1_reg__mi,
	arm_instr_store_w1_word_u0_p1_reg__pl,
	arm_instr_store_w1_word_u0_p1_reg__vs,
	arm_instr_store_w1_word_u0_p1_reg__vc,
	arm_instr_store_w1_word_u0_p1_reg__hi,
	arm_instr_store_w1_word_u0_p1_reg__ls,
	arm_instr_store_w1_word_u0_p1_reg__ge,
	arm_instr_store_w1_word_u0_p1_reg__lt,
	arm_instr_store_w1_word_u0_p1_reg__gt,
	arm_instr_store_w1_word_u0_p1_reg__le,
	arm_instr_store_w1_word_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p1_reg__eq,
	arm_instr_load_w1_word_u0_p1_reg__ne,
	arm_instr_load_w1_word_u0_p1_reg__cs,
	arm_instr_load_w1_word_u0_p1_reg__cc,
	arm_instr_load_w1_word_u0_p1_reg__mi,
	arm_instr_load_w1_word_u0_p1_reg__pl,
	arm_instr_load_w1_word_u0_p1_reg__vs,
	arm_instr_load_w1_word_u0_p1_reg__vc,
	arm_instr_load_w1_word_u0_p1_reg__hi,
	arm_instr_load_w1_word_u0_p1_reg__ls,
	arm_instr_load_w1_word_u0_p1_reg__ge,
	arm_instr_load_w1_word_u0_p1_reg__lt,
	arm_instr_load_w1_word_u0_p1_reg__gt,
	arm_instr_load_w1_word_u0_p1_reg__le,
	arm_instr_load_w1_word_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p1_reg__eq,
	arm_instr_store_w0_byte_u0_p1_reg__ne,
	arm_instr_store_w0_byte_u0_p1_reg__cs,
	arm_instr_store_w0_byte_u0_p1_reg__cc,
	arm_instr_store_w0_byte_u0_p1_reg__mi,
	arm_instr_store_w0_byte_u0_p1_reg__pl,
	arm_instr_store_w0_byte_u0_p1_reg__vs,
	arm_instr_store_w0_byte_u0_p1_reg__vc,
	arm_instr_store_w0_byte_u0_p1_reg__hi,
	arm_instr_store_w0_byte_u0_p1_reg__ls,
	arm_instr_store_w0_byte_u0_p1_reg__ge,
	arm_instr_store_w0_byte_u0_p1_reg__lt,
	arm_instr_store_w0_byte_u0_p1_reg__gt,
	arm_instr_store_w0_byte_u0_p1_reg__le,
	arm_instr_store_w0_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p1_reg__eq,
	arm_instr_load_w0_byte_u0_p1_reg__ne,
	arm_instr_load_w0_byte_u0_p1_reg__cs,
	arm_instr_load_w0_byte_u0_p1_reg__cc,
	arm_instr_load_w0_byte_u0_p1_reg__mi,
	arm_instr_load_w0_byte_u0_p1_reg__pl,
	arm_instr_load_w0_byte_u0_p1_reg__vs,
	arm_instr_load_w0_byte_u0_p1_reg__vc,
	arm_instr_load_w0_byte_u0_p1_reg__hi,
	arm_instr_load_w0_byte_u0_p1_reg__ls,
	arm_instr_load_w0_byte_u0_p1_reg__ge,
	arm_instr_load_w0_byte_u0_p1_reg__lt,
	arm_instr_load_w0_byte_u0_p1_reg__gt,
	arm_instr_load_w0_byte_u0_p1_reg__le,
	arm_instr_load_w0_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p1_reg__eq,
	arm_instr_store_w1_byte_u0_p1_reg__ne,
	arm_instr_store_w1_byte_u0_p1_reg__cs,
	arm_instr_store_w1_byte_u0_p1_reg__cc,
	arm_instr_store_w1_byte_u0_p1_reg__mi,
	arm_instr_store_w1_byte_u0_p1_reg__pl,
	arm_instr_store_w1_byte_u0_p1_reg__vs,
	arm_instr_store_w1_byte_u0_p1_reg__vc,
	arm_instr_store_w1_byte_u0_p1_reg__hi,
	arm_instr_store_w1_byte_u0_p1_reg__ls,
	arm_instr_store_w1_byte_u0_p1_reg__ge,
	arm_instr_store_w1_byte_u0_p1_reg__lt,
	arm_instr_store_w1_byte_u0_p1_reg__gt,
	arm_instr_store_w1_byte_u0_p1_reg__le,
	arm_instr_store_w1_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p1_reg__eq,
	arm_instr_load_w1_byte_u0_p1_reg__ne,
	arm_instr_load_w1_byte_u0_p1_reg__cs,
	arm_instr_load_w1_byte_u0_p1_reg__cc,
	arm_instr_load_w1_byte_u0_p1_reg__mi,
	arm_instr_load_w1_byte_u0_p1_reg__pl,
	arm_instr_load_w1_byte_u0_p1_reg__vs,
	arm_instr_load_w1_byte_u0_p1_reg__vc,
	arm_instr_load_w1_byte_u0_p1_reg__hi,
	arm_instr_load_w1_byte_u0_p1_reg__ls,
	arm_instr_load_w1_byte_u0_p1_reg__ge,
	arm_instr_load_w1_byte_u0_p1_reg__lt,
	arm_instr_load_w1_byte_u0_p1_reg__gt,
	arm_instr_load_w1_byte_u0_p1_reg__le,
	arm_instr_load_w1_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p1_reg__eq,
	arm_instr_store_w0_word_u1_p1_reg__ne,
	arm_instr_store_w0_word_u1_p1_reg__cs,
	arm_instr_store_w0_word_u1_p1_reg__cc,
	arm_instr_store_w0_word_u1_p1_reg__mi,
	arm_instr_store_w0_word_u1_p1_reg__pl,
	arm_instr_store_w0_word_u1_p1_reg__vs,
	arm_instr_store_w0_word_u1_p1_reg__vc,
	arm_instr_store_w0_word_u1_p1_reg__hi,
	arm_instr_store_w0_word_u1_p1_reg__ls,
	arm_instr_store_w0_word_u1_p1_reg__ge,
	arm_instr_store_w0_word_u1_p1_reg__lt,
	arm_instr_store_w0_word_u1_p1_reg__gt,
	arm_instr_store_w0_word_u1_p1_reg__le,
	arm_instr_store_w0_word_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p1_reg__eq,
	arm_instr_load_w0_word_u1_p1_reg__ne,
	arm_instr_load_w0_word_u1_p1_reg__cs,
	arm_instr_load_w0_word_u1_p1_reg__cc,
	arm_instr_load_w0_word_u1_p1_reg__mi,
	arm_instr_load_w0_word_u1_p1_reg__pl,
	arm_instr_load_w0_word_u1_p1_reg__vs,
	arm_instr_load_w0_word_u1_p1_reg__vc,
	arm_instr_load_w0_word_u1_p1_reg__hi,
	arm_instr_load_w0_word_u1_p1_reg__ls,
	arm_instr_load_w0_word_u1_p1_reg__ge,
	arm_instr_load_w0_word_u1_p1_reg__lt,
	arm_instr_load_w0_word_u1_p1_reg__gt,
	arm_instr_load_w0_word_u1_p1_reg__le,
	arm_instr_load_w0_word_u1_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p1_reg__eq,
	arm_instr_store_w1_word_u1_p1_reg__ne,
	arm_instr_store_w1_word_u1_p1_reg__cs,
	arm_instr_store_w1_word_u1_p1_reg__cc,
	arm_instr_store_w1_word_u1_p1_reg__mi,
	arm_instr_store_w1_word_u1_p1_reg__pl,
	arm_instr_store_w1_word_u1_p1_reg__vs,
	arm_instr_store_w1_word_u1_p1_reg__vc,
	arm_instr_store_w1_word_u1_p1_reg__hi,
	arm_instr_store_w1_word_u1_p1_reg__ls,
	arm_instr_store_w1_word_u1_p1_reg__ge,
	arm_instr_store_w1_word_u1_p1_reg__lt,
	arm_instr_store_w1_word_u1_p1_reg__gt,
	arm_instr_store_w1_word_u1_p1_reg__le,
	arm_instr_store_w1_word_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p1_reg__eq,
	arm_instr_load_w1_word_u1_p1_reg__ne,
	arm_instr_load_w1_word_u1_p1_reg__cs,
	arm_instr_load_w1_word_u1_p1_reg__cc,
	arm_instr_load_w1_word_u1_p1_reg__mi,
	arm_instr_load_w1_word_u1_p1_reg__pl,
	arm_instr_load_w1_word_u1_p1_reg__vs,
	arm_instr_load_w1_word_u1_p1_reg__vc,
	arm_instr_load_w1_word_u1_p1_reg__hi,
	arm_instr_load_w1_word_u1_p1_reg__ls,
	arm_instr_load_w1_word_u1_p1_reg__ge,
	arm_instr_load_w1_word_u1_p1_reg__lt,
	arm_instr_load_w1_word_u1_p1_reg__gt,
	arm_instr_load_w1_word_u1_p1_reg__le,
	arm_instr_load_w1_word_u1_p1_reg,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p1_reg__eq,
	arm_instr_store_w0_byte_u1_p1_reg__ne,
	arm_instr_store_w0_byte_u1_p1_reg__cs,
	arm_instr_store_w0_byte_u1_p1_reg__cc,
	arm_instr_store_w0_byte_u1_p1_reg__mi,
	arm_instr_store_w0_byte_u1_p1_reg__pl,
	arm_instr_store_w0_byte_u1_p1_reg__vs,
	arm_instr_store_w0_byte_u1_p1_reg__vc,
	arm_instr_store_w0_byte_u1_p1_reg__hi,
	arm_instr_store_w0_byte_u1_p1_reg__ls,
	arm_instr_store_w0_byte_u1_p1_reg__ge,
	arm_instr_store_w0_byte_u1_p1_reg__lt,
	arm_instr_store_w0_byte_u1_p1_reg__gt,
	arm_instr_store_w0_byte_u1_p1_reg__le,
	arm_instr_store_w0_byte_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p1_reg__eq,
	arm_instr_load_w0_byte_u1_p1_reg__ne,
	arm_instr_load_w0_byte_u1_p1_reg__cs,
	arm_instr_load_w0_byte_u1_p1_reg__cc,
	arm_instr_load_w0_byte_u1_p1_reg__mi,
	arm_instr_load_w0_byte_u1_p1_reg__pl,
	arm_instr_load_w0_byte_u1_p1_reg__vs,
	arm_instr_load_w0_byte_u1_p1_reg__vc,
	arm_instr_load_w0_byte_u1_p1_reg__hi,
	arm_instr_load_w0_byte_u1_p1_reg__ls,
	arm_instr_load_w0_byte_u1_p1_reg__ge,
	arm_instr_load_w0_byte_u1_p1_reg__lt,
	arm_instr_load_w0_byte_u1_p1_reg__gt,
	arm_instr_load_w0_byte_u1_p1_reg__le,
	arm_instr_load_w0_byte_u1_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p1_reg__eq,
	arm_instr_store_w1_byte_u1_p1_reg__ne,
	arm_instr_store_w1_byte_u1_p1_reg__cs,
	arm_instr_store_w1_byte_u1_p1_reg__cc,
	arm_instr_store_w1_byte_u1_p1_reg__mi,
	arm_instr_store_w1_byte_u1_p1_reg__pl,
	arm_instr_store_w1_byte_u1_p1_reg__vs,
	arm_instr_store_w1_byte_u1_p1_reg__vc,
	arm_instr_store_w1_byte_u1_p1_reg__hi,
	arm_instr_store_w1_byte_u1_p1_reg__ls,
	arm_instr_store_w1_byte_u1_p1_reg__ge,
	arm_instr_store_w1_byte_u1_p1_reg__lt,
	arm_instr_store_w1_byte_u1_p1_reg__gt,
	arm_instr_store_w1_byte_u1_p1_reg__le,
	arm_instr_store_w1_byte_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p1_reg__eq,
	arm_instr_load_w1_byte_u1_p1_reg__ne,
	arm_instr_load_w1_byte_u1_p1_reg__cs,
	arm_instr_load_w1_byte_u1_p1_reg__cc,
	arm_instr_load_w1_byte_u1_p1_reg__mi,
	arm_instr_load_w1_byte_u1_p1_reg__pl,
	arm_instr_load_w1_byte_u1_p1_reg__vs,
	arm_instr_load_w1_byte_u1_p1_reg__vc,
	arm_instr_load_w1_byte_u1_p1_reg__hi,
	arm_instr_load_w1_byte_u1_p1_reg__ls,
	arm_instr_load_w1_byte_u1_p1_reg__ge,
	arm_instr_load_w1_byte_u1_p1_reg__lt,
	arm_instr_load_w1_byte_u1_p1_reg__gt,
	arm_instr_load_w1_byte_u1_p1_reg__le,
	arm_instr_load_w1_byte_u1_p1_reg,
	arm_instr_nop
};


	void (*arm_load_store_instr_pc[1024])(struct cpu *,
		struct arm_instr_call *) = {
	arm_instr_store_w0_word_u0_p0_imm_pc__eq,
	arm_instr_store_w0_word_u0_p0_imm_pc__ne,
	arm_instr_store_w0_word_u0_p0_imm_pc__cs,
	arm_instr_store_w0_word_u0_p0_imm_pc__cc,
	arm_instr_store_w0_word_u0_p0_imm_pc__mi,
	arm_instr_store_w0_word_u0_p0_imm_pc__pl,
	arm_instr_store_w0_word_u0_p0_imm_pc__vs,
	arm_instr_store_w0_word_u0_p0_imm_pc__vc,
	arm_instr_store_w0_word_u0_p0_imm_pc__hi,
	arm_instr_store_w0_word_u0_p0_imm_pc__ls,
	arm_instr_store_w0_word_u0_p0_imm_pc__ge,
	arm_instr_store_w0_word_u0_p0_imm_pc__lt,
	arm_instr_store_w0_word_u0_p0_imm_pc__gt,
	arm_instr_store_w0_word_u0_p0_imm_pc__le,
	arm_instr_store_w0_word_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p0_imm_pc__eq,
	arm_instr_load_w0_word_u0_p0_imm_pc__ne,
	arm_instr_load_w0_word_u0_p0_imm_pc__cs,
	arm_instr_load_w0_word_u0_p0_imm_pc__cc,
	arm_instr_load_w0_word_u0_p0_imm_pc__mi,
	arm_instr_load_w0_word_u0_p0_imm_pc__pl,
	arm_instr_load_w0_word_u0_p0_imm_pc__vs,
	arm_instr_load_w0_word_u0_p0_imm_pc__vc,
	arm_instr_load_w0_word_u0_p0_imm_pc__hi,
	arm_instr_load_w0_word_u0_p0_imm_pc__ls,
	arm_instr_load_w0_word_u0_p0_imm_pc__ge,
	arm_instr_load_w0_word_u0_p0_imm_pc__lt,
	arm_instr_load_w0_word_u0_p0_imm_pc__gt,
	arm_instr_load_w0_word_u0_p0_imm_pc__le,
	arm_instr_load_w0_word_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p0_imm_pc__eq,
	arm_instr_store_w1_word_u0_p0_imm_pc__ne,
	arm_instr_store_w1_word_u0_p0_imm_pc__cs,
	arm_instr_store_w1_word_u0_p0_imm_pc__cc,
	arm_instr_store_w1_word_u0_p0_imm_pc__mi,
	arm_instr_store_w1_word_u0_p0_imm_pc__pl,
	arm_instr_store_w1_word_u0_p0_imm_pc__vs,
	arm_instr_store_w1_word_u0_p0_imm_pc__vc,
	arm_instr_store_w1_word_u0_p0_imm_pc__hi,
	arm_instr_store_w1_word_u0_p0_imm_pc__ls,
	arm_instr_store_w1_word_u0_p0_imm_pc__ge,
	arm_instr_store_w1_word_u0_p0_imm_pc__lt,
	arm_instr_store_w1_word_u0_p0_imm_pc__gt,
	arm_instr_store_w1_word_u0_p0_imm_pc__le,
	arm_instr_store_w1_word_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p0_imm_pc__eq,
	arm_instr_load_w1_word_u0_p0_imm_pc__ne,
	arm_instr_load_w1_word_u0_p0_imm_pc__cs,
	arm_instr_load_w1_word_u0_p0_imm_pc__cc,
	arm_instr_load_w1_word_u0_p0_imm_pc__mi,
	arm_instr_load_w1_word_u0_p0_imm_pc__pl,
	arm_instr_load_w1_word_u0_p0_imm_pc__vs,
	arm_instr_load_w1_word_u0_p0_imm_pc__vc,
	arm_instr_load_w1_word_u0_p0_imm_pc__hi,
	arm_instr_load_w1_word_u0_p0_imm_pc__ls,
	arm_instr_load_w1_word_u0_p0_imm_pc__ge,
	arm_instr_load_w1_word_u0_p0_imm_pc__lt,
	arm_instr_load_w1_word_u0_p0_imm_pc__gt,
	arm_instr_load_w1_word_u0_p0_imm_pc__le,
	arm_instr_load_w1_word_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p0_imm_pc__eq,
	arm_instr_store_w0_byte_u0_p0_imm_pc__ne,
	arm_instr_store_w0_byte_u0_p0_imm_pc__cs,
	arm_instr_store_w0_byte_u0_p0_imm_pc__cc,
	arm_instr_store_w0_byte_u0_p0_imm_pc__mi,
	arm_instr_store_w0_byte_u0_p0_imm_pc__pl,
	arm_instr_store_w0_byte_u0_p0_imm_pc__vs,
	arm_instr_store_w0_byte_u0_p0_imm_pc__vc,
	arm_instr_store_w0_byte_u0_p0_imm_pc__hi,
	arm_instr_store_w0_byte_u0_p0_imm_pc__ls,
	arm_instr_store_w0_byte_u0_p0_imm_pc__ge,
	arm_instr_store_w0_byte_u0_p0_imm_pc__lt,
	arm_instr_store_w0_byte_u0_p0_imm_pc__gt,
	arm_instr_store_w0_byte_u0_p0_imm_pc__le,
	arm_instr_store_w0_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p0_imm_pc__eq,
	arm_instr_load_w0_byte_u0_p0_imm_pc__ne,
	arm_instr_load_w0_byte_u0_p0_imm_pc__cs,
	arm_instr_load_w0_byte_u0_p0_imm_pc__cc,
	arm_instr_load_w0_byte_u0_p0_imm_pc__mi,
	arm_instr_load_w0_byte_u0_p0_imm_pc__pl,
	arm_instr_load_w0_byte_u0_p0_imm_pc__vs,
	arm_instr_load_w0_byte_u0_p0_imm_pc__vc,
	arm_instr_load_w0_byte_u0_p0_imm_pc__hi,
	arm_instr_load_w0_byte_u0_p0_imm_pc__ls,
	arm_instr_load_w0_byte_u0_p0_imm_pc__ge,
	arm_instr_load_w0_byte_u0_p0_imm_pc__lt,
	arm_instr_load_w0_byte_u0_p0_imm_pc__gt,
	arm_instr_load_w0_byte_u0_p0_imm_pc__le,
	arm_instr_load_w0_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p0_imm_pc__eq,
	arm_instr_store_w1_byte_u0_p0_imm_pc__ne,
	arm_instr_store_w1_byte_u0_p0_imm_pc__cs,
	arm_instr_store_w1_byte_u0_p0_imm_pc__cc,
	arm_instr_store_w1_byte_u0_p0_imm_pc__mi,
	arm_instr_store_w1_byte_u0_p0_imm_pc__pl,
	arm_instr_store_w1_byte_u0_p0_imm_pc__vs,
	arm_instr_store_w1_byte_u0_p0_imm_pc__vc,
	arm_instr_store_w1_byte_u0_p0_imm_pc__hi,
	arm_instr_store_w1_byte_u0_p0_imm_pc__ls,
	arm_instr_store_w1_byte_u0_p0_imm_pc__ge,
	arm_instr_store_w1_byte_u0_p0_imm_pc__lt,
	arm_instr_store_w1_byte_u0_p0_imm_pc__gt,
	arm_instr_store_w1_byte_u0_p0_imm_pc__le,
	arm_instr_store_w1_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p0_imm_pc__eq,
	arm_instr_load_w1_byte_u0_p0_imm_pc__ne,
	arm_instr_load_w1_byte_u0_p0_imm_pc__cs,
	arm_instr_load_w1_byte_u0_p0_imm_pc__cc,
	arm_instr_load_w1_byte_u0_p0_imm_pc__mi,
	arm_instr_load_w1_byte_u0_p0_imm_pc__pl,
	arm_instr_load_w1_byte_u0_p0_imm_pc__vs,
	arm_instr_load_w1_byte_u0_p0_imm_pc__vc,
	arm_instr_load_w1_byte_u0_p0_imm_pc__hi,
	arm_instr_load_w1_byte_u0_p0_imm_pc__ls,
	arm_instr_load_w1_byte_u0_p0_imm_pc__ge,
	arm_instr_load_w1_byte_u0_p0_imm_pc__lt,
	arm_instr_load_w1_byte_u0_p0_imm_pc__gt,
	arm_instr_load_w1_byte_u0_p0_imm_pc__le,
	arm_instr_load_w1_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p0_imm_pc__eq,
	arm_instr_store_w0_word_u1_p0_imm_pc__ne,
	arm_instr_store_w0_word_u1_p0_imm_pc__cs,
	arm_instr_store_w0_word_u1_p0_imm_pc__cc,
	arm_instr_store_w0_word_u1_p0_imm_pc__mi,
	arm_instr_store_w0_word_u1_p0_imm_pc__pl,
	arm_instr_store_w0_word_u1_p0_imm_pc__vs,
	arm_instr_store_w0_word_u1_p0_imm_pc__vc,
	arm_instr_store_w0_word_u1_p0_imm_pc__hi,
	arm_instr_store_w0_word_u1_p0_imm_pc__ls,
	arm_instr_store_w0_word_u1_p0_imm_pc__ge,
	arm_instr_store_w0_word_u1_p0_imm_pc__lt,
	arm_instr_store_w0_word_u1_p0_imm_pc__gt,
	arm_instr_store_w0_word_u1_p0_imm_pc__le,
	arm_instr_store_w0_word_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p0_imm_pc__eq,
	arm_instr_load_w0_word_u1_p0_imm_pc__ne,
	arm_instr_load_w0_word_u1_p0_imm_pc__cs,
	arm_instr_load_w0_word_u1_p0_imm_pc__cc,
	arm_instr_load_w0_word_u1_p0_imm_pc__mi,
	arm_instr_load_w0_word_u1_p0_imm_pc__pl,
	arm_instr_load_w0_word_u1_p0_imm_pc__vs,
	arm_instr_load_w0_word_u1_p0_imm_pc__vc,
	arm_instr_load_w0_word_u1_p0_imm_pc__hi,
	arm_instr_load_w0_word_u1_p0_imm_pc__ls,
	arm_instr_load_w0_word_u1_p0_imm_pc__ge,
	arm_instr_load_w0_word_u1_p0_imm_pc__lt,
	arm_instr_load_w0_word_u1_p0_imm_pc__gt,
	arm_instr_load_w0_word_u1_p0_imm_pc__le,
	arm_instr_load_w0_word_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p0_imm_pc__eq,
	arm_instr_store_w1_word_u1_p0_imm_pc__ne,
	arm_instr_store_w1_word_u1_p0_imm_pc__cs,
	arm_instr_store_w1_word_u1_p0_imm_pc__cc,
	arm_instr_store_w1_word_u1_p0_imm_pc__mi,
	arm_instr_store_w1_word_u1_p0_imm_pc__pl,
	arm_instr_store_w1_word_u1_p0_imm_pc__vs,
	arm_instr_store_w1_word_u1_p0_imm_pc__vc,
	arm_instr_store_w1_word_u1_p0_imm_pc__hi,
	arm_instr_store_w1_word_u1_p0_imm_pc__ls,
	arm_instr_store_w1_word_u1_p0_imm_pc__ge,
	arm_instr_store_w1_word_u1_p0_imm_pc__lt,
	arm_instr_store_w1_word_u1_p0_imm_pc__gt,
	arm_instr_store_w1_word_u1_p0_imm_pc__le,
	arm_instr_store_w1_word_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p0_imm_pc__eq,
	arm_instr_load_w1_word_u1_p0_imm_pc__ne,
	arm_instr_load_w1_word_u1_p0_imm_pc__cs,
	arm_instr_load_w1_word_u1_p0_imm_pc__cc,
	arm_instr_load_w1_word_u1_p0_imm_pc__mi,
	arm_instr_load_w1_word_u1_p0_imm_pc__pl,
	arm_instr_load_w1_word_u1_p0_imm_pc__vs,
	arm_instr_load_w1_word_u1_p0_imm_pc__vc,
	arm_instr_load_w1_word_u1_p0_imm_pc__hi,
	arm_instr_load_w1_word_u1_p0_imm_pc__ls,
	arm_instr_load_w1_word_u1_p0_imm_pc__ge,
	arm_instr_load_w1_word_u1_p0_imm_pc__lt,
	arm_instr_load_w1_word_u1_p0_imm_pc__gt,
	arm_instr_load_w1_word_u1_p0_imm_pc__le,
	arm_instr_load_w1_word_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p0_imm_pc__eq,
	arm_instr_store_w0_byte_u1_p0_imm_pc__ne,
	arm_instr_store_w0_byte_u1_p0_imm_pc__cs,
	arm_instr_store_w0_byte_u1_p0_imm_pc__cc,
	arm_instr_store_w0_byte_u1_p0_imm_pc__mi,
	arm_instr_store_w0_byte_u1_p0_imm_pc__pl,
	arm_instr_store_w0_byte_u1_p0_imm_pc__vs,
	arm_instr_store_w0_byte_u1_p0_imm_pc__vc,
	arm_instr_store_w0_byte_u1_p0_imm_pc__hi,
	arm_instr_store_w0_byte_u1_p0_imm_pc__ls,
	arm_instr_store_w0_byte_u1_p0_imm_pc__ge,
	arm_instr_store_w0_byte_u1_p0_imm_pc__lt,
	arm_instr_store_w0_byte_u1_p0_imm_pc__gt,
	arm_instr_store_w0_byte_u1_p0_imm_pc__le,
	arm_instr_store_w0_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p0_imm_pc__eq,
	arm_instr_load_w0_byte_u1_p0_imm_pc__ne,
	arm_instr_load_w0_byte_u1_p0_imm_pc__cs,
	arm_instr_load_w0_byte_u1_p0_imm_pc__cc,
	arm_instr_load_w0_byte_u1_p0_imm_pc__mi,
	arm_instr_load_w0_byte_u1_p0_imm_pc__pl,
	arm_instr_load_w0_byte_u1_p0_imm_pc__vs,
	arm_instr_load_w0_byte_u1_p0_imm_pc__vc,
	arm_instr_load_w0_byte_u1_p0_imm_pc__hi,
	arm_instr_load_w0_byte_u1_p0_imm_pc__ls,
	arm_instr_load_w0_byte_u1_p0_imm_pc__ge,
	arm_instr_load_w0_byte_u1_p0_imm_pc__lt,
	arm_instr_load_w0_byte_u1_p0_imm_pc__gt,
	arm_instr_load_w0_byte_u1_p0_imm_pc__le,
	arm_instr_load_w0_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p0_imm_pc__eq,
	arm_instr_store_w1_byte_u1_p0_imm_pc__ne,
	arm_instr_store_w1_byte_u1_p0_imm_pc__cs,
	arm_instr_store_w1_byte_u1_p0_imm_pc__cc,
	arm_instr_store_w1_byte_u1_p0_imm_pc__mi,
	arm_instr_store_w1_byte_u1_p0_imm_pc__pl,
	arm_instr_store_w1_byte_u1_p0_imm_pc__vs,
	arm_instr_store_w1_byte_u1_p0_imm_pc__vc,
	arm_instr_store_w1_byte_u1_p0_imm_pc__hi,
	arm_instr_store_w1_byte_u1_p0_imm_pc__ls,
	arm_instr_store_w1_byte_u1_p0_imm_pc__ge,
	arm_instr_store_w1_byte_u1_p0_imm_pc__lt,
	arm_instr_store_w1_byte_u1_p0_imm_pc__gt,
	arm_instr_store_w1_byte_u1_p0_imm_pc__le,
	arm_instr_store_w1_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p0_imm_pc__eq,
	arm_instr_load_w1_byte_u1_p0_imm_pc__ne,
	arm_instr_load_w1_byte_u1_p0_imm_pc__cs,
	arm_instr_load_w1_byte_u1_p0_imm_pc__cc,
	arm_instr_load_w1_byte_u1_p0_imm_pc__mi,
	arm_instr_load_w1_byte_u1_p0_imm_pc__pl,
	arm_instr_load_w1_byte_u1_p0_imm_pc__vs,
	arm_instr_load_w1_byte_u1_p0_imm_pc__vc,
	arm_instr_load_w1_byte_u1_p0_imm_pc__hi,
	arm_instr_load_w1_byte_u1_p0_imm_pc__ls,
	arm_instr_load_w1_byte_u1_p0_imm_pc__ge,
	arm_instr_load_w1_byte_u1_p0_imm_pc__lt,
	arm_instr_load_w1_byte_u1_p0_imm_pc__gt,
	arm_instr_load_w1_byte_u1_p0_imm_pc__le,
	arm_instr_load_w1_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_word_u0_p1_imm_pc__eq,
	arm_instr_store_w0_word_u0_p1_imm_pc__ne,
	arm_instr_store_w0_word_u0_p1_imm_pc__cs,
	arm_instr_store_w0_word_u0_p1_imm_pc__cc,
	arm_instr_store_w0_word_u0_p1_imm_pc__mi,
	arm_instr_store_w0_word_u0_p1_imm_pc__pl,
	arm_instr_store_w0_word_u0_p1_imm_pc__vs,
	arm_instr_store_w0_word_u0_p1_imm_pc__vc,
	arm_instr_store_w0_word_u0_p1_imm_pc__hi,
	arm_instr_store_w0_word_u0_p1_imm_pc__ls,
	arm_instr_store_w0_word_u0_p1_imm_pc__ge,
	arm_instr_store_w0_word_u0_p1_imm_pc__lt,
	arm_instr_store_w0_word_u0_p1_imm_pc__gt,
	arm_instr_store_w0_word_u0_p1_imm_pc__le,
	arm_instr_store_w0_word_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p1_imm_pc__eq,
	arm_instr_load_w0_word_u0_p1_imm_pc__ne,
	arm_instr_load_w0_word_u0_p1_imm_pc__cs,
	arm_instr_load_w0_word_u0_p1_imm_pc__cc,
	arm_instr_load_w0_word_u0_p1_imm_pc__mi,
	arm_instr_load_w0_word_u0_p1_imm_pc__pl,
	arm_instr_load_w0_word_u0_p1_imm_pc__vs,
	arm_instr_load_w0_word_u0_p1_imm_pc__vc,
	arm_instr_load_w0_word_u0_p1_imm_pc__hi,
	arm_instr_load_w0_word_u0_p1_imm_pc__ls,
	arm_instr_load_w0_word_u0_p1_imm_pc__ge,
	arm_instr_load_w0_word_u0_p1_imm_pc__lt,
	arm_instr_load_w0_word_u0_p1_imm_pc__gt,
	arm_instr_load_w0_word_u0_p1_imm_pc__le,
	arm_instr_load_w0_word_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p1_imm_pc__eq,
	arm_instr_store_w1_word_u0_p1_imm_pc__ne,
	arm_instr_store_w1_word_u0_p1_imm_pc__cs,
	arm_instr_store_w1_word_u0_p1_imm_pc__cc,
	arm_instr_store_w1_word_u0_p1_imm_pc__mi,
	arm_instr_store_w1_word_u0_p1_imm_pc__pl,
	arm_instr_store_w1_word_u0_p1_imm_pc__vs,
	arm_instr_store_w1_word_u0_p1_imm_pc__vc,
	arm_instr_store_w1_word_u0_p1_imm_pc__hi,
	arm_instr_store_w1_word_u0_p1_imm_pc__ls,
	arm_instr_store_w1_word_u0_p1_imm_pc__ge,
	arm_instr_store_w1_word_u0_p1_imm_pc__lt,
	arm_instr_store_w1_word_u0_p1_imm_pc__gt,
	arm_instr_store_w1_word_u0_p1_imm_pc__le,
	arm_instr_store_w1_word_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p1_imm_pc__eq,
	arm_instr_load_w1_word_u0_p1_imm_pc__ne,
	arm_instr_load_w1_word_u0_p1_imm_pc__cs,
	arm_instr_load_w1_word_u0_p1_imm_pc__cc,
	arm_instr_load_w1_word_u0_p1_imm_pc__mi,
	arm_instr_load_w1_word_u0_p1_imm_pc__pl,
	arm_instr_load_w1_word_u0_p1_imm_pc__vs,
	arm_instr_load_w1_word_u0_p1_imm_pc__vc,
	arm_instr_load_w1_word_u0_p1_imm_pc__hi,
	arm_instr_load_w1_word_u0_p1_imm_pc__ls,
	arm_instr_load_w1_word_u0_p1_imm_pc__ge,
	arm_instr_load_w1_word_u0_p1_imm_pc__lt,
	arm_instr_load_w1_word_u0_p1_imm_pc__gt,
	arm_instr_load_w1_word_u0_p1_imm_pc__le,
	arm_instr_load_w1_word_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p1_imm_pc__eq,
	arm_instr_store_w0_byte_u0_p1_imm_pc__ne,
	arm_instr_store_w0_byte_u0_p1_imm_pc__cs,
	arm_instr_store_w0_byte_u0_p1_imm_pc__cc,
	arm_instr_store_w0_byte_u0_p1_imm_pc__mi,
	arm_instr_store_w0_byte_u0_p1_imm_pc__pl,
	arm_instr_store_w0_byte_u0_p1_imm_pc__vs,
	arm_instr_store_w0_byte_u0_p1_imm_pc__vc,
	arm_instr_store_w0_byte_u0_p1_imm_pc__hi,
	arm_instr_store_w0_byte_u0_p1_imm_pc__ls,
	arm_instr_store_w0_byte_u0_p1_imm_pc__ge,
	arm_instr_store_w0_byte_u0_p1_imm_pc__lt,
	arm_instr_store_w0_byte_u0_p1_imm_pc__gt,
	arm_instr_store_w0_byte_u0_p1_imm_pc__le,
	arm_instr_store_w0_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p1_imm_pc__eq,
	arm_instr_load_w0_byte_u0_p1_imm_pc__ne,
	arm_instr_load_w0_byte_u0_p1_imm_pc__cs,
	arm_instr_load_w0_byte_u0_p1_imm_pc__cc,
	arm_instr_load_w0_byte_u0_p1_imm_pc__mi,
	arm_instr_load_w0_byte_u0_p1_imm_pc__pl,
	arm_instr_load_w0_byte_u0_p1_imm_pc__vs,
	arm_instr_load_w0_byte_u0_p1_imm_pc__vc,
	arm_instr_load_w0_byte_u0_p1_imm_pc__hi,
	arm_instr_load_w0_byte_u0_p1_imm_pc__ls,
	arm_instr_load_w0_byte_u0_p1_imm_pc__ge,
	arm_instr_load_w0_byte_u0_p1_imm_pc__lt,
	arm_instr_load_w0_byte_u0_p1_imm_pc__gt,
	arm_instr_load_w0_byte_u0_p1_imm_pc__le,
	arm_instr_load_w0_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p1_imm_pc__eq,
	arm_instr_store_w1_byte_u0_p1_imm_pc__ne,
	arm_instr_store_w1_byte_u0_p1_imm_pc__cs,
	arm_instr_store_w1_byte_u0_p1_imm_pc__cc,
	arm_instr_store_w1_byte_u0_p1_imm_pc__mi,
	arm_instr_store_w1_byte_u0_p1_imm_pc__pl,
	arm_instr_store_w1_byte_u0_p1_imm_pc__vs,
	arm_instr_store_w1_byte_u0_p1_imm_pc__vc,
	arm_instr_store_w1_byte_u0_p1_imm_pc__hi,
	arm_instr_store_w1_byte_u0_p1_imm_pc__ls,
	arm_instr_store_w1_byte_u0_p1_imm_pc__ge,
	arm_instr_store_w1_byte_u0_p1_imm_pc__lt,
	arm_instr_store_w1_byte_u0_p1_imm_pc__gt,
	arm_instr_store_w1_byte_u0_p1_imm_pc__le,
	arm_instr_store_w1_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p1_imm_pc__eq,
	arm_instr_load_w1_byte_u0_p1_imm_pc__ne,
	arm_instr_load_w1_byte_u0_p1_imm_pc__cs,
	arm_instr_load_w1_byte_u0_p1_imm_pc__cc,
	arm_instr_load_w1_byte_u0_p1_imm_pc__mi,
	arm_instr_load_w1_byte_u0_p1_imm_pc__pl,
	arm_instr_load_w1_byte_u0_p1_imm_pc__vs,
	arm_instr_load_w1_byte_u0_p1_imm_pc__vc,
	arm_instr_load_w1_byte_u0_p1_imm_pc__hi,
	arm_instr_load_w1_byte_u0_p1_imm_pc__ls,
	arm_instr_load_w1_byte_u0_p1_imm_pc__ge,
	arm_instr_load_w1_byte_u0_p1_imm_pc__lt,
	arm_instr_load_w1_byte_u0_p1_imm_pc__gt,
	arm_instr_load_w1_byte_u0_p1_imm_pc__le,
	arm_instr_load_w1_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p1_imm_pc__eq,
	arm_instr_store_w0_word_u1_p1_imm_pc__ne,
	arm_instr_store_w0_word_u1_p1_imm_pc__cs,
	arm_instr_store_w0_word_u1_p1_imm_pc__cc,
	arm_instr_store_w0_word_u1_p1_imm_pc__mi,
	arm_instr_store_w0_word_u1_p1_imm_pc__pl,
	arm_instr_store_w0_word_u1_p1_imm_pc__vs,
	arm_instr_store_w0_word_u1_p1_imm_pc__vc,
	arm_instr_store_w0_word_u1_p1_imm_pc__hi,
	arm_instr_store_w0_word_u1_p1_imm_pc__ls,
	arm_instr_store_w0_word_u1_p1_imm_pc__ge,
	arm_instr_store_w0_word_u1_p1_imm_pc__lt,
	arm_instr_store_w0_word_u1_p1_imm_pc__gt,
	arm_instr_store_w0_word_u1_p1_imm_pc__le,
	arm_instr_store_w0_word_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p1_imm_pc__eq,
	arm_instr_load_w0_word_u1_p1_imm_pc__ne,
	arm_instr_load_w0_word_u1_p1_imm_pc__cs,
	arm_instr_load_w0_word_u1_p1_imm_pc__cc,
	arm_instr_load_w0_word_u1_p1_imm_pc__mi,
	arm_instr_load_w0_word_u1_p1_imm_pc__pl,
	arm_instr_load_w0_word_u1_p1_imm_pc__vs,
	arm_instr_load_w0_word_u1_p1_imm_pc__vc,
	arm_instr_load_w0_word_u1_p1_imm_pc__hi,
	arm_instr_load_w0_word_u1_p1_imm_pc__ls,
	arm_instr_load_w0_word_u1_p1_imm_pc__ge,
	arm_instr_load_w0_word_u1_p1_imm_pc__lt,
	arm_instr_load_w0_word_u1_p1_imm_pc__gt,
	arm_instr_load_w0_word_u1_p1_imm_pc__le,
	arm_instr_load_w0_word_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p1_imm_pc__eq,
	arm_instr_store_w1_word_u1_p1_imm_pc__ne,
	arm_instr_store_w1_word_u1_p1_imm_pc__cs,
	arm_instr_store_w1_word_u1_p1_imm_pc__cc,
	arm_instr_store_w1_word_u1_p1_imm_pc__mi,
	arm_instr_store_w1_word_u1_p1_imm_pc__pl,
	arm_instr_store_w1_word_u1_p1_imm_pc__vs,
	arm_instr_store_w1_word_u1_p1_imm_pc__vc,
	arm_instr_store_w1_word_u1_p1_imm_pc__hi,
	arm_instr_store_w1_word_u1_p1_imm_pc__ls,
	arm_instr_store_w1_word_u1_p1_imm_pc__ge,
	arm_instr_store_w1_word_u1_p1_imm_pc__lt,
	arm_instr_store_w1_word_u1_p1_imm_pc__gt,
	arm_instr_store_w1_word_u1_p1_imm_pc__le,
	arm_instr_store_w1_word_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p1_imm_pc__eq,
	arm_instr_load_w1_word_u1_p1_imm_pc__ne,
	arm_instr_load_w1_word_u1_p1_imm_pc__cs,
	arm_instr_load_w1_word_u1_p1_imm_pc__cc,
	arm_instr_load_w1_word_u1_p1_imm_pc__mi,
	arm_instr_load_w1_word_u1_p1_imm_pc__pl,
	arm_instr_load_w1_word_u1_p1_imm_pc__vs,
	arm_instr_load_w1_word_u1_p1_imm_pc__vc,
	arm_instr_load_w1_word_u1_p1_imm_pc__hi,
	arm_instr_load_w1_word_u1_p1_imm_pc__ls,
	arm_instr_load_w1_word_u1_p1_imm_pc__ge,
	arm_instr_load_w1_word_u1_p1_imm_pc__lt,
	arm_instr_load_w1_word_u1_p1_imm_pc__gt,
	arm_instr_load_w1_word_u1_p1_imm_pc__le,
	arm_instr_load_w1_word_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p1_imm_pc__eq,
	arm_instr_store_w0_byte_u1_p1_imm_pc__ne,
	arm_instr_store_w0_byte_u1_p1_imm_pc__cs,
	arm_instr_store_w0_byte_u1_p1_imm_pc__cc,
	arm_instr_store_w0_byte_u1_p1_imm_pc__mi,
	arm_instr_store_w0_byte_u1_p1_imm_pc__pl,
	arm_instr_store_w0_byte_u1_p1_imm_pc__vs,
	arm_instr_store_w0_byte_u1_p1_imm_pc__vc,
	arm_instr_store_w0_byte_u1_p1_imm_pc__hi,
	arm_instr_store_w0_byte_u1_p1_imm_pc__ls,
	arm_instr_store_w0_byte_u1_p1_imm_pc__ge,
	arm_instr_store_w0_byte_u1_p1_imm_pc__lt,
	arm_instr_store_w0_byte_u1_p1_imm_pc__gt,
	arm_instr_store_w0_byte_u1_p1_imm_pc__le,
	arm_instr_store_w0_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p1_imm_pc__eq,
	arm_instr_load_w0_byte_u1_p1_imm_pc__ne,
	arm_instr_load_w0_byte_u1_p1_imm_pc__cs,
	arm_instr_load_w0_byte_u1_p1_imm_pc__cc,
	arm_instr_load_w0_byte_u1_p1_imm_pc__mi,
	arm_instr_load_w0_byte_u1_p1_imm_pc__pl,
	arm_instr_load_w0_byte_u1_p1_imm_pc__vs,
	arm_instr_load_w0_byte_u1_p1_imm_pc__vc,
	arm_instr_load_w0_byte_u1_p1_imm_pc__hi,
	arm_instr_load_w0_byte_u1_p1_imm_pc__ls,
	arm_instr_load_w0_byte_u1_p1_imm_pc__ge,
	arm_instr_load_w0_byte_u1_p1_imm_pc__lt,
	arm_instr_load_w0_byte_u1_p1_imm_pc__gt,
	arm_instr_load_w0_byte_u1_p1_imm_pc__le,
	arm_instr_load_w0_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p1_imm_pc__eq,
	arm_instr_store_w1_byte_u1_p1_imm_pc__ne,
	arm_instr_store_w1_byte_u1_p1_imm_pc__cs,
	arm_instr_store_w1_byte_u1_p1_imm_pc__cc,
	arm_instr_store_w1_byte_u1_p1_imm_pc__mi,
	arm_instr_store_w1_byte_u1_p1_imm_pc__pl,
	arm_instr_store_w1_byte_u1_p1_imm_pc__vs,
	arm_instr_store_w1_byte_u1_p1_imm_pc__vc,
	arm_instr_store_w1_byte_u1_p1_imm_pc__hi,
	arm_instr_store_w1_byte_u1_p1_imm_pc__ls,
	arm_instr_store_w1_byte_u1_p1_imm_pc__ge,
	arm_instr_store_w1_byte_u1_p1_imm_pc__lt,
	arm_instr_store_w1_byte_u1_p1_imm_pc__gt,
	arm_instr_store_w1_byte_u1_p1_imm_pc__le,
	arm_instr_store_w1_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p1_imm_pc__eq,
	arm_instr_load_w1_byte_u1_p1_imm_pc__ne,
	arm_instr_load_w1_byte_u1_p1_imm_pc__cs,
	arm_instr_load_w1_byte_u1_p1_imm_pc__cc,
	arm_instr_load_w1_byte_u1_p1_imm_pc__mi,
	arm_instr_load_w1_byte_u1_p1_imm_pc__pl,
	arm_instr_load_w1_byte_u1_p1_imm_pc__vs,
	arm_instr_load_w1_byte_u1_p1_imm_pc__vc,
	arm_instr_load_w1_byte_u1_p1_imm_pc__hi,
	arm_instr_load_w1_byte_u1_p1_imm_pc__ls,
	arm_instr_load_w1_byte_u1_p1_imm_pc__ge,
	arm_instr_load_w1_byte_u1_p1_imm_pc__lt,
	arm_instr_load_w1_byte_u1_p1_imm_pc__gt,
	arm_instr_load_w1_byte_u1_p1_imm_pc__le,
	arm_instr_load_w1_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_word_u0_p0_reg_pc__eq,
	arm_instr_store_w0_word_u0_p0_reg_pc__ne,
	arm_instr_store_w0_word_u0_p0_reg_pc__cs,
	arm_instr_store_w0_word_u0_p0_reg_pc__cc,
	arm_instr_store_w0_word_u0_p0_reg_pc__mi,
	arm_instr_store_w0_word_u0_p0_reg_pc__pl,
	arm_instr_store_w0_word_u0_p0_reg_pc__vs,
	arm_instr_store_w0_word_u0_p0_reg_pc__vc,
	arm_instr_store_w0_word_u0_p0_reg_pc__hi,
	arm_instr_store_w0_word_u0_p0_reg_pc__ls,
	arm_instr_store_w0_word_u0_p0_reg_pc__ge,
	arm_instr_store_w0_word_u0_p0_reg_pc__lt,
	arm_instr_store_w0_word_u0_p0_reg_pc__gt,
	arm_instr_store_w0_word_u0_p0_reg_pc__le,
	arm_instr_store_w0_word_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p0_reg_pc__eq,
	arm_instr_load_w0_word_u0_p0_reg_pc__ne,
	arm_instr_load_w0_word_u0_p0_reg_pc__cs,
	arm_instr_load_w0_word_u0_p0_reg_pc__cc,
	arm_instr_load_w0_word_u0_p0_reg_pc__mi,
	arm_instr_load_w0_word_u0_p0_reg_pc__pl,
	arm_instr_load_w0_word_u0_p0_reg_pc__vs,
	arm_instr_load_w0_word_u0_p0_reg_pc__vc,
	arm_instr_load_w0_word_u0_p0_reg_pc__hi,
	arm_instr_load_w0_word_u0_p0_reg_pc__ls,
	arm_instr_load_w0_word_u0_p0_reg_pc__ge,
	arm_instr_load_w0_word_u0_p0_reg_pc__lt,
	arm_instr_load_w0_word_u0_p0_reg_pc__gt,
	arm_instr_load_w0_word_u0_p0_reg_pc__le,
	arm_instr_load_w0_word_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p0_reg_pc__eq,
	arm_instr_store_w1_word_u0_p0_reg_pc__ne,
	arm_instr_store_w1_word_u0_p0_reg_pc__cs,
	arm_instr_store_w1_word_u0_p0_reg_pc__cc,
	arm_instr_store_w1_word_u0_p0_reg_pc__mi,
	arm_instr_store_w1_word_u0_p0_reg_pc__pl,
	arm_instr_store_w1_word_u0_p0_reg_pc__vs,
	arm_instr_store_w1_word_u0_p0_reg_pc__vc,
	arm_instr_store_w1_word_u0_p0_reg_pc__hi,
	arm_instr_store_w1_word_u0_p0_reg_pc__ls,
	arm_instr_store_w1_word_u0_p0_reg_pc__ge,
	arm_instr_store_w1_word_u0_p0_reg_pc__lt,
	arm_instr_store_w1_word_u0_p0_reg_pc__gt,
	arm_instr_store_w1_word_u0_p0_reg_pc__le,
	arm_instr_store_w1_word_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p0_reg_pc__eq,
	arm_instr_load_w1_word_u0_p0_reg_pc__ne,
	arm_instr_load_w1_word_u0_p0_reg_pc__cs,
	arm_instr_load_w1_word_u0_p0_reg_pc__cc,
	arm_instr_load_w1_word_u0_p0_reg_pc__mi,
	arm_instr_load_w1_word_u0_p0_reg_pc__pl,
	arm_instr_load_w1_word_u0_p0_reg_pc__vs,
	arm_instr_load_w1_word_u0_p0_reg_pc__vc,
	arm_instr_load_w1_word_u0_p0_reg_pc__hi,
	arm_instr_load_w1_word_u0_p0_reg_pc__ls,
	arm_instr_load_w1_word_u0_p0_reg_pc__ge,
	arm_instr_load_w1_word_u0_p0_reg_pc__lt,
	arm_instr_load_w1_word_u0_p0_reg_pc__gt,
	arm_instr_load_w1_word_u0_p0_reg_pc__le,
	arm_instr_load_w1_word_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p0_reg_pc__eq,
	arm_instr_store_w0_byte_u0_p0_reg_pc__ne,
	arm_instr_store_w0_byte_u0_p0_reg_pc__cs,
	arm_instr_store_w0_byte_u0_p0_reg_pc__cc,
	arm_instr_store_w0_byte_u0_p0_reg_pc__mi,
	arm_instr_store_w0_byte_u0_p0_reg_pc__pl,
	arm_instr_store_w0_byte_u0_p0_reg_pc__vs,
	arm_instr_store_w0_byte_u0_p0_reg_pc__vc,
	arm_instr_store_w0_byte_u0_p0_reg_pc__hi,
	arm_instr_store_w0_byte_u0_p0_reg_pc__ls,
	arm_instr_store_w0_byte_u0_p0_reg_pc__ge,
	arm_instr_store_w0_byte_u0_p0_reg_pc__lt,
	arm_instr_store_w0_byte_u0_p0_reg_pc__gt,
	arm_instr_store_w0_byte_u0_p0_reg_pc__le,
	arm_instr_store_w0_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p0_reg_pc__eq,
	arm_instr_load_w0_byte_u0_p0_reg_pc__ne,
	arm_instr_load_w0_byte_u0_p0_reg_pc__cs,
	arm_instr_load_w0_byte_u0_p0_reg_pc__cc,
	arm_instr_load_w0_byte_u0_p0_reg_pc__mi,
	arm_instr_load_w0_byte_u0_p0_reg_pc__pl,
	arm_instr_load_w0_byte_u0_p0_reg_pc__vs,
	arm_instr_load_w0_byte_u0_p0_reg_pc__vc,
	arm_instr_load_w0_byte_u0_p0_reg_pc__hi,
	arm_instr_load_w0_byte_u0_p0_reg_pc__ls,
	arm_instr_load_w0_byte_u0_p0_reg_pc__ge,
	arm_instr_load_w0_byte_u0_p0_reg_pc__lt,
	arm_instr_load_w0_byte_u0_p0_reg_pc__gt,
	arm_instr_load_w0_byte_u0_p0_reg_pc__le,
	arm_instr_load_w0_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p0_reg_pc__eq,
	arm_instr_store_w1_byte_u0_p0_reg_pc__ne,
	arm_instr_store_w1_byte_u0_p0_reg_pc__cs,
	arm_instr_store_w1_byte_u0_p0_reg_pc__cc,
	arm_instr_store_w1_byte_u0_p0_reg_pc__mi,
	arm_instr_store_w1_byte_u0_p0_reg_pc__pl,
	arm_instr_store_w1_byte_u0_p0_reg_pc__vs,
	arm_instr_store_w1_byte_u0_p0_reg_pc__vc,
	arm_instr_store_w1_byte_u0_p0_reg_pc__hi,
	arm_instr_store_w1_byte_u0_p0_reg_pc__ls,
	arm_instr_store_w1_byte_u0_p0_reg_pc__ge,
	arm_instr_store_w1_byte_u0_p0_reg_pc__lt,
	arm_instr_store_w1_byte_u0_p0_reg_pc__gt,
	arm_instr_store_w1_byte_u0_p0_reg_pc__le,
	arm_instr_store_w1_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p0_reg_pc__eq,
	arm_instr_load_w1_byte_u0_p0_reg_pc__ne,
	arm_instr_load_w1_byte_u0_p0_reg_pc__cs,
	arm_instr_load_w1_byte_u0_p0_reg_pc__cc,
	arm_instr_load_w1_byte_u0_p0_reg_pc__mi,
	arm_instr_load_w1_byte_u0_p0_reg_pc__pl,
	arm_instr_load_w1_byte_u0_p0_reg_pc__vs,
	arm_instr_load_w1_byte_u0_p0_reg_pc__vc,
	arm_instr_load_w1_byte_u0_p0_reg_pc__hi,
	arm_instr_load_w1_byte_u0_p0_reg_pc__ls,
	arm_instr_load_w1_byte_u0_p0_reg_pc__ge,
	arm_instr_load_w1_byte_u0_p0_reg_pc__lt,
	arm_instr_load_w1_byte_u0_p0_reg_pc__gt,
	arm_instr_load_w1_byte_u0_p0_reg_pc__le,
	arm_instr_load_w1_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p0_reg_pc__eq,
	arm_instr_store_w0_word_u1_p0_reg_pc__ne,
	arm_instr_store_w0_word_u1_p0_reg_pc__cs,
	arm_instr_store_w0_word_u1_p0_reg_pc__cc,
	arm_instr_store_w0_word_u1_p0_reg_pc__mi,
	arm_instr_store_w0_word_u1_p0_reg_pc__pl,
	arm_instr_store_w0_word_u1_p0_reg_pc__vs,
	arm_instr_store_w0_word_u1_p0_reg_pc__vc,
	arm_instr_store_w0_word_u1_p0_reg_pc__hi,
	arm_instr_store_w0_word_u1_p0_reg_pc__ls,
	arm_instr_store_w0_word_u1_p0_reg_pc__ge,
	arm_instr_store_w0_word_u1_p0_reg_pc__lt,
	arm_instr_store_w0_word_u1_p0_reg_pc__gt,
	arm_instr_store_w0_word_u1_p0_reg_pc__le,
	arm_instr_store_w0_word_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p0_reg_pc__eq,
	arm_instr_load_w0_word_u1_p0_reg_pc__ne,
	arm_instr_load_w0_word_u1_p0_reg_pc__cs,
	arm_instr_load_w0_word_u1_p0_reg_pc__cc,
	arm_instr_load_w0_word_u1_p0_reg_pc__mi,
	arm_instr_load_w0_word_u1_p0_reg_pc__pl,
	arm_instr_load_w0_word_u1_p0_reg_pc__vs,
	arm_instr_load_w0_word_u1_p0_reg_pc__vc,
	arm_instr_load_w0_word_u1_p0_reg_pc__hi,
	arm_instr_load_w0_word_u1_p0_reg_pc__ls,
	arm_instr_load_w0_word_u1_p0_reg_pc__ge,
	arm_instr_load_w0_word_u1_p0_reg_pc__lt,
	arm_instr_load_w0_word_u1_p0_reg_pc__gt,
	arm_instr_load_w0_word_u1_p0_reg_pc__le,
	arm_instr_load_w0_word_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p0_reg_pc__eq,
	arm_instr_store_w1_word_u1_p0_reg_pc__ne,
	arm_instr_store_w1_word_u1_p0_reg_pc__cs,
	arm_instr_store_w1_word_u1_p0_reg_pc__cc,
	arm_instr_store_w1_word_u1_p0_reg_pc__mi,
	arm_instr_store_w1_word_u1_p0_reg_pc__pl,
	arm_instr_store_w1_word_u1_p0_reg_pc__vs,
	arm_instr_store_w1_word_u1_p0_reg_pc__vc,
	arm_instr_store_w1_word_u1_p0_reg_pc__hi,
	arm_instr_store_w1_word_u1_p0_reg_pc__ls,
	arm_instr_store_w1_word_u1_p0_reg_pc__ge,
	arm_instr_store_w1_word_u1_p0_reg_pc__lt,
	arm_instr_store_w1_word_u1_p0_reg_pc__gt,
	arm_instr_store_w1_word_u1_p0_reg_pc__le,
	arm_instr_store_w1_word_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p0_reg_pc__eq,
	arm_instr_load_w1_word_u1_p0_reg_pc__ne,
	arm_instr_load_w1_word_u1_p0_reg_pc__cs,
	arm_instr_load_w1_word_u1_p0_reg_pc__cc,
	arm_instr_load_w1_word_u1_p0_reg_pc__mi,
	arm_instr_load_w1_word_u1_p0_reg_pc__pl,
	arm_instr_load_w1_word_u1_p0_reg_pc__vs,
	arm_instr_load_w1_word_u1_p0_reg_pc__vc,
	arm_instr_load_w1_word_u1_p0_reg_pc__hi,
	arm_instr_load_w1_word_u1_p0_reg_pc__ls,
	arm_instr_load_w1_word_u1_p0_reg_pc__ge,
	arm_instr_load_w1_word_u1_p0_reg_pc__lt,
	arm_instr_load_w1_word_u1_p0_reg_pc__gt,
	arm_instr_load_w1_word_u1_p0_reg_pc__le,
	arm_instr_load_w1_word_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p0_reg_pc__eq,
	arm_instr_store_w0_byte_u1_p0_reg_pc__ne,
	arm_instr_store_w0_byte_u1_p0_reg_pc__cs,
	arm_instr_store_w0_byte_u1_p0_reg_pc__cc,
	arm_instr_store_w0_byte_u1_p0_reg_pc__mi,
	arm_instr_store_w0_byte_u1_p0_reg_pc__pl,
	arm_instr_store_w0_byte_u1_p0_reg_pc__vs,
	arm_instr_store_w0_byte_u1_p0_reg_pc__vc,
	arm_instr_store_w0_byte_u1_p0_reg_pc__hi,
	arm_instr_store_w0_byte_u1_p0_reg_pc__ls,
	arm_instr_store_w0_byte_u1_p0_reg_pc__ge,
	arm_instr_store_w0_byte_u1_p0_reg_pc__lt,
	arm_instr_store_w0_byte_u1_p0_reg_pc__gt,
	arm_instr_store_w0_byte_u1_p0_reg_pc__le,
	arm_instr_store_w0_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p0_reg_pc__eq,
	arm_instr_load_w0_byte_u1_p0_reg_pc__ne,
	arm_instr_load_w0_byte_u1_p0_reg_pc__cs,
	arm_instr_load_w0_byte_u1_p0_reg_pc__cc,
	arm_instr_load_w0_byte_u1_p0_reg_pc__mi,
	arm_instr_load_w0_byte_u1_p0_reg_pc__pl,
	arm_instr_load_w0_byte_u1_p0_reg_pc__vs,
	arm_instr_load_w0_byte_u1_p0_reg_pc__vc,
	arm_instr_load_w0_byte_u1_p0_reg_pc__hi,
	arm_instr_load_w0_byte_u1_p0_reg_pc__ls,
	arm_instr_load_w0_byte_u1_p0_reg_pc__ge,
	arm_instr_load_w0_byte_u1_p0_reg_pc__lt,
	arm_instr_load_w0_byte_u1_p0_reg_pc__gt,
	arm_instr_load_w0_byte_u1_p0_reg_pc__le,
	arm_instr_load_w0_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p0_reg_pc__eq,
	arm_instr_store_w1_byte_u1_p0_reg_pc__ne,
	arm_instr_store_w1_byte_u1_p0_reg_pc__cs,
	arm_instr_store_w1_byte_u1_p0_reg_pc__cc,
	arm_instr_store_w1_byte_u1_p0_reg_pc__mi,
	arm_instr_store_w1_byte_u1_p0_reg_pc__pl,
	arm_instr_store_w1_byte_u1_p0_reg_pc__vs,
	arm_instr_store_w1_byte_u1_p0_reg_pc__vc,
	arm_instr_store_w1_byte_u1_p0_reg_pc__hi,
	arm_instr_store_w1_byte_u1_p0_reg_pc__ls,
	arm_instr_store_w1_byte_u1_p0_reg_pc__ge,
	arm_instr_store_w1_byte_u1_p0_reg_pc__lt,
	arm_instr_store_w1_byte_u1_p0_reg_pc__gt,
	arm_instr_store_w1_byte_u1_p0_reg_pc__le,
	arm_instr_store_w1_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p0_reg_pc__eq,
	arm_instr_load_w1_byte_u1_p0_reg_pc__ne,
	arm_instr_load_w1_byte_u1_p0_reg_pc__cs,
	arm_instr_load_w1_byte_u1_p0_reg_pc__cc,
	arm_instr_load_w1_byte_u1_p0_reg_pc__mi,
	arm_instr_load_w1_byte_u1_p0_reg_pc__pl,
	arm_instr_load_w1_byte_u1_p0_reg_pc__vs,
	arm_instr_load_w1_byte_u1_p0_reg_pc__vc,
	arm_instr_load_w1_byte_u1_p0_reg_pc__hi,
	arm_instr_load_w1_byte_u1_p0_reg_pc__ls,
	arm_instr_load_w1_byte_u1_p0_reg_pc__ge,
	arm_instr_load_w1_byte_u1_p0_reg_pc__lt,
	arm_instr_load_w1_byte_u1_p0_reg_pc__gt,
	arm_instr_load_w1_byte_u1_p0_reg_pc__le,
	arm_instr_load_w1_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_word_u0_p1_reg_pc__eq,
	arm_instr_store_w0_word_u0_p1_reg_pc__ne,
	arm_instr_store_w0_word_u0_p1_reg_pc__cs,
	arm_instr_store_w0_word_u0_p1_reg_pc__cc,
	arm_instr_store_w0_word_u0_p1_reg_pc__mi,
	arm_instr_store_w0_word_u0_p1_reg_pc__pl,
	arm_instr_store_w0_word_u0_p1_reg_pc__vs,
	arm_instr_store_w0_word_u0_p1_reg_pc__vc,
	arm_instr_store_w0_word_u0_p1_reg_pc__hi,
	arm_instr_store_w0_word_u0_p1_reg_pc__ls,
	arm_instr_store_w0_word_u0_p1_reg_pc__ge,
	arm_instr_store_w0_word_u0_p1_reg_pc__lt,
	arm_instr_store_w0_word_u0_p1_reg_pc__gt,
	arm_instr_store_w0_word_u0_p1_reg_pc__le,
	arm_instr_store_w0_word_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u0_p1_reg_pc__eq,
	arm_instr_load_w0_word_u0_p1_reg_pc__ne,
	arm_instr_load_w0_word_u0_p1_reg_pc__cs,
	arm_instr_load_w0_word_u0_p1_reg_pc__cc,
	arm_instr_load_w0_word_u0_p1_reg_pc__mi,
	arm_instr_load_w0_word_u0_p1_reg_pc__pl,
	arm_instr_load_w0_word_u0_p1_reg_pc__vs,
	arm_instr_load_w0_word_u0_p1_reg_pc__vc,
	arm_instr_load_w0_word_u0_p1_reg_pc__hi,
	arm_instr_load_w0_word_u0_p1_reg_pc__ls,
	arm_instr_load_w0_word_u0_p1_reg_pc__ge,
	arm_instr_load_w0_word_u0_p1_reg_pc__lt,
	arm_instr_load_w0_word_u0_p1_reg_pc__gt,
	arm_instr_load_w0_word_u0_p1_reg_pc__le,
	arm_instr_load_w0_word_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u0_p1_reg_pc__eq,
	arm_instr_store_w1_word_u0_p1_reg_pc__ne,
	arm_instr_store_w1_word_u0_p1_reg_pc__cs,
	arm_instr_store_w1_word_u0_p1_reg_pc__cc,
	arm_instr_store_w1_word_u0_p1_reg_pc__mi,
	arm_instr_store_w1_word_u0_p1_reg_pc__pl,
	arm_instr_store_w1_word_u0_p1_reg_pc__vs,
	arm_instr_store_w1_word_u0_p1_reg_pc__vc,
	arm_instr_store_w1_word_u0_p1_reg_pc__hi,
	arm_instr_store_w1_word_u0_p1_reg_pc__ls,
	arm_instr_store_w1_word_u0_p1_reg_pc__ge,
	arm_instr_store_w1_word_u0_p1_reg_pc__lt,
	arm_instr_store_w1_word_u0_p1_reg_pc__gt,
	arm_instr_store_w1_word_u0_p1_reg_pc__le,
	arm_instr_store_w1_word_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u0_p1_reg_pc__eq,
	arm_instr_load_w1_word_u0_p1_reg_pc__ne,
	arm_instr_load_w1_word_u0_p1_reg_pc__cs,
	arm_instr_load_w1_word_u0_p1_reg_pc__cc,
	arm_instr_load_w1_word_u0_p1_reg_pc__mi,
	arm_instr_load_w1_word_u0_p1_reg_pc__pl,
	arm_instr_load_w1_word_u0_p1_reg_pc__vs,
	arm_instr_load_w1_word_u0_p1_reg_pc__vc,
	arm_instr_load_w1_word_u0_p1_reg_pc__hi,
	arm_instr_load_w1_word_u0_p1_reg_pc__ls,
	arm_instr_load_w1_word_u0_p1_reg_pc__ge,
	arm_instr_load_w1_word_u0_p1_reg_pc__lt,
	arm_instr_load_w1_word_u0_p1_reg_pc__gt,
	arm_instr_load_w1_word_u0_p1_reg_pc__le,
	arm_instr_load_w1_word_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u0_p1_reg_pc__eq,
	arm_instr_store_w0_byte_u0_p1_reg_pc__ne,
	arm_instr_store_w0_byte_u0_p1_reg_pc__cs,
	arm_instr_store_w0_byte_u0_p1_reg_pc__cc,
	arm_instr_store_w0_byte_u0_p1_reg_pc__mi,
	arm_instr_store_w0_byte_u0_p1_reg_pc__pl,
	arm_instr_store_w0_byte_u0_p1_reg_pc__vs,
	arm_instr_store_w0_byte_u0_p1_reg_pc__vc,
	arm_instr_store_w0_byte_u0_p1_reg_pc__hi,
	arm_instr_store_w0_byte_u0_p1_reg_pc__ls,
	arm_instr_store_w0_byte_u0_p1_reg_pc__ge,
	arm_instr_store_w0_byte_u0_p1_reg_pc__lt,
	arm_instr_store_w0_byte_u0_p1_reg_pc__gt,
	arm_instr_store_w0_byte_u0_p1_reg_pc__le,
	arm_instr_store_w0_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u0_p1_reg_pc__eq,
	arm_instr_load_w0_byte_u0_p1_reg_pc__ne,
	arm_instr_load_w0_byte_u0_p1_reg_pc__cs,
	arm_instr_load_w0_byte_u0_p1_reg_pc__cc,
	arm_instr_load_w0_byte_u0_p1_reg_pc__mi,
	arm_instr_load_w0_byte_u0_p1_reg_pc__pl,
	arm_instr_load_w0_byte_u0_p1_reg_pc__vs,
	arm_instr_load_w0_byte_u0_p1_reg_pc__vc,
	arm_instr_load_w0_byte_u0_p1_reg_pc__hi,
	arm_instr_load_w0_byte_u0_p1_reg_pc__ls,
	arm_instr_load_w0_byte_u0_p1_reg_pc__ge,
	arm_instr_load_w0_byte_u0_p1_reg_pc__lt,
	arm_instr_load_w0_byte_u0_p1_reg_pc__gt,
	arm_instr_load_w0_byte_u0_p1_reg_pc__le,
	arm_instr_load_w0_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u0_p1_reg_pc__eq,
	arm_instr_store_w1_byte_u0_p1_reg_pc__ne,
	arm_instr_store_w1_byte_u0_p1_reg_pc__cs,
	arm_instr_store_w1_byte_u0_p1_reg_pc__cc,
	arm_instr_store_w1_byte_u0_p1_reg_pc__mi,
	arm_instr_store_w1_byte_u0_p1_reg_pc__pl,
	arm_instr_store_w1_byte_u0_p1_reg_pc__vs,
	arm_instr_store_w1_byte_u0_p1_reg_pc__vc,
	arm_instr_store_w1_byte_u0_p1_reg_pc__hi,
	arm_instr_store_w1_byte_u0_p1_reg_pc__ls,
	arm_instr_store_w1_byte_u0_p1_reg_pc__ge,
	arm_instr_store_w1_byte_u0_p1_reg_pc__lt,
	arm_instr_store_w1_byte_u0_p1_reg_pc__gt,
	arm_instr_store_w1_byte_u0_p1_reg_pc__le,
	arm_instr_store_w1_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u0_p1_reg_pc__eq,
	arm_instr_load_w1_byte_u0_p1_reg_pc__ne,
	arm_instr_load_w1_byte_u0_p1_reg_pc__cs,
	arm_instr_load_w1_byte_u0_p1_reg_pc__cc,
	arm_instr_load_w1_byte_u0_p1_reg_pc__mi,
	arm_instr_load_w1_byte_u0_p1_reg_pc__pl,
	arm_instr_load_w1_byte_u0_p1_reg_pc__vs,
	arm_instr_load_w1_byte_u0_p1_reg_pc__vc,
	arm_instr_load_w1_byte_u0_p1_reg_pc__hi,
	arm_instr_load_w1_byte_u0_p1_reg_pc__ls,
	arm_instr_load_w1_byte_u0_p1_reg_pc__ge,
	arm_instr_load_w1_byte_u0_p1_reg_pc__lt,
	arm_instr_load_w1_byte_u0_p1_reg_pc__gt,
	arm_instr_load_w1_byte_u0_p1_reg_pc__le,
	arm_instr_load_w1_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_word_u1_p1_reg_pc__eq,
	arm_instr_store_w0_word_u1_p1_reg_pc__ne,
	arm_instr_store_w0_word_u1_p1_reg_pc__cs,
	arm_instr_store_w0_word_u1_p1_reg_pc__cc,
	arm_instr_store_w0_word_u1_p1_reg_pc__mi,
	arm_instr_store_w0_word_u1_p1_reg_pc__pl,
	arm_instr_store_w0_word_u1_p1_reg_pc__vs,
	arm_instr_store_w0_word_u1_p1_reg_pc__vc,
	arm_instr_store_w0_word_u1_p1_reg_pc__hi,
	arm_instr_store_w0_word_u1_p1_reg_pc__ls,
	arm_instr_store_w0_word_u1_p1_reg_pc__ge,
	arm_instr_store_w0_word_u1_p1_reg_pc__lt,
	arm_instr_store_w0_word_u1_p1_reg_pc__gt,
	arm_instr_store_w0_word_u1_p1_reg_pc__le,
	arm_instr_store_w0_word_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_word_u1_p1_reg_pc__eq,
	arm_instr_load_w0_word_u1_p1_reg_pc__ne,
	arm_instr_load_w0_word_u1_p1_reg_pc__cs,
	arm_instr_load_w0_word_u1_p1_reg_pc__cc,
	arm_instr_load_w0_word_u1_p1_reg_pc__mi,
	arm_instr_load_w0_word_u1_p1_reg_pc__pl,
	arm_instr_load_w0_word_u1_p1_reg_pc__vs,
	arm_instr_load_w0_word_u1_p1_reg_pc__vc,
	arm_instr_load_w0_word_u1_p1_reg_pc__hi,
	arm_instr_load_w0_word_u1_p1_reg_pc__ls,
	arm_instr_load_w0_word_u1_p1_reg_pc__ge,
	arm_instr_load_w0_word_u1_p1_reg_pc__lt,
	arm_instr_load_w0_word_u1_p1_reg_pc__gt,
	arm_instr_load_w0_word_u1_p1_reg_pc__le,
	arm_instr_load_w0_word_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_word_u1_p1_reg_pc__eq,
	arm_instr_store_w1_word_u1_p1_reg_pc__ne,
	arm_instr_store_w1_word_u1_p1_reg_pc__cs,
	arm_instr_store_w1_word_u1_p1_reg_pc__cc,
	arm_instr_store_w1_word_u1_p1_reg_pc__mi,
	arm_instr_store_w1_word_u1_p1_reg_pc__pl,
	arm_instr_store_w1_word_u1_p1_reg_pc__vs,
	arm_instr_store_w1_word_u1_p1_reg_pc__vc,
	arm_instr_store_w1_word_u1_p1_reg_pc__hi,
	arm_instr_store_w1_word_u1_p1_reg_pc__ls,
	arm_instr_store_w1_word_u1_p1_reg_pc__ge,
	arm_instr_store_w1_word_u1_p1_reg_pc__lt,
	arm_instr_store_w1_word_u1_p1_reg_pc__gt,
	arm_instr_store_w1_word_u1_p1_reg_pc__le,
	arm_instr_store_w1_word_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_word_u1_p1_reg_pc__eq,
	arm_instr_load_w1_word_u1_p1_reg_pc__ne,
	arm_instr_load_w1_word_u1_p1_reg_pc__cs,
	arm_instr_load_w1_word_u1_p1_reg_pc__cc,
	arm_instr_load_w1_word_u1_p1_reg_pc__mi,
	arm_instr_load_w1_word_u1_p1_reg_pc__pl,
	arm_instr_load_w1_word_u1_p1_reg_pc__vs,
	arm_instr_load_w1_word_u1_p1_reg_pc__vc,
	arm_instr_load_w1_word_u1_p1_reg_pc__hi,
	arm_instr_load_w1_word_u1_p1_reg_pc__ls,
	arm_instr_load_w1_word_u1_p1_reg_pc__ge,
	arm_instr_load_w1_word_u1_p1_reg_pc__lt,
	arm_instr_load_w1_word_u1_p1_reg_pc__gt,
	arm_instr_load_w1_word_u1_p1_reg_pc__le,
	arm_instr_load_w1_word_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_byte_u1_p1_reg_pc__eq,
	arm_instr_store_w0_byte_u1_p1_reg_pc__ne,
	arm_instr_store_w0_byte_u1_p1_reg_pc__cs,
	arm_instr_store_w0_byte_u1_p1_reg_pc__cc,
	arm_instr_store_w0_byte_u1_p1_reg_pc__mi,
	arm_instr_store_w0_byte_u1_p1_reg_pc__pl,
	arm_instr_store_w0_byte_u1_p1_reg_pc__vs,
	arm_instr_store_w0_byte_u1_p1_reg_pc__vc,
	arm_instr_store_w0_byte_u1_p1_reg_pc__hi,
	arm_instr_store_w0_byte_u1_p1_reg_pc__ls,
	arm_instr_store_w0_byte_u1_p1_reg_pc__ge,
	arm_instr_store_w0_byte_u1_p1_reg_pc__lt,
	arm_instr_store_w0_byte_u1_p1_reg_pc__gt,
	arm_instr_store_w0_byte_u1_p1_reg_pc__le,
	arm_instr_store_w0_byte_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_byte_u1_p1_reg_pc__eq,
	arm_instr_load_w0_byte_u1_p1_reg_pc__ne,
	arm_instr_load_w0_byte_u1_p1_reg_pc__cs,
	arm_instr_load_w0_byte_u1_p1_reg_pc__cc,
	arm_instr_load_w0_byte_u1_p1_reg_pc__mi,
	arm_instr_load_w0_byte_u1_p1_reg_pc__pl,
	arm_instr_load_w0_byte_u1_p1_reg_pc__vs,
	arm_instr_load_w0_byte_u1_p1_reg_pc__vc,
	arm_instr_load_w0_byte_u1_p1_reg_pc__hi,
	arm_instr_load_w0_byte_u1_p1_reg_pc__ls,
	arm_instr_load_w0_byte_u1_p1_reg_pc__ge,
	arm_instr_load_w0_byte_u1_p1_reg_pc__lt,
	arm_instr_load_w0_byte_u1_p1_reg_pc__gt,
	arm_instr_load_w0_byte_u1_p1_reg_pc__le,
	arm_instr_load_w0_byte_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_byte_u1_p1_reg_pc__eq,
	arm_instr_store_w1_byte_u1_p1_reg_pc__ne,
	arm_instr_store_w1_byte_u1_p1_reg_pc__cs,
	arm_instr_store_w1_byte_u1_p1_reg_pc__cc,
	arm_instr_store_w1_byte_u1_p1_reg_pc__mi,
	arm_instr_store_w1_byte_u1_p1_reg_pc__pl,
	arm_instr_store_w1_byte_u1_p1_reg_pc__vs,
	arm_instr_store_w1_byte_u1_p1_reg_pc__vc,
	arm_instr_store_w1_byte_u1_p1_reg_pc__hi,
	arm_instr_store_w1_byte_u1_p1_reg_pc__ls,
	arm_instr_store_w1_byte_u1_p1_reg_pc__ge,
	arm_instr_store_w1_byte_u1_p1_reg_pc__lt,
	arm_instr_store_w1_byte_u1_p1_reg_pc__gt,
	arm_instr_store_w1_byte_u1_p1_reg_pc__le,
	arm_instr_store_w1_byte_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_byte_u1_p1_reg_pc__eq,
	arm_instr_load_w1_byte_u1_p1_reg_pc__ne,
	arm_instr_load_w1_byte_u1_p1_reg_pc__cs,
	arm_instr_load_w1_byte_u1_p1_reg_pc__cc,
	arm_instr_load_w1_byte_u1_p1_reg_pc__mi,
	arm_instr_load_w1_byte_u1_p1_reg_pc__pl,
	arm_instr_load_w1_byte_u1_p1_reg_pc__vs,
	arm_instr_load_w1_byte_u1_p1_reg_pc__vc,
	arm_instr_load_w1_byte_u1_p1_reg_pc__hi,
	arm_instr_load_w1_byte_u1_p1_reg_pc__ls,
	arm_instr_load_w1_byte_u1_p1_reg_pc__ge,
	arm_instr_load_w1_byte_u1_p1_reg_pc__lt,
	arm_instr_load_w1_byte_u1_p1_reg_pc__gt,
	arm_instr_load_w1_byte_u1_p1_reg_pc__le,
	arm_instr_load_w1_byte_u1_p1_reg_pc,
	arm_instr_nop
};

void arm_instr_store_w0_signed_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_imm_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p0_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u0_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_byte_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w0_signed_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w0_signed_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_store_w1_signed_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__eq(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__ne(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__cs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__cc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__mi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__pl(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__vs(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__vc(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__hi(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__ls(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__ge(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__lt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__gt(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__le(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg(struct cpu *, struct arm_instr_call *);
void arm_instr_load_w1_signed_halfword_u1_p1_reg_pc(struct cpu *, struct arm_instr_call *);

	void (*arm_load_store_instr_3[2048])(struct cpu *,
		struct arm_instr_call *) = {
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p0_imm__eq,
	arm_instr_store_w0_signed_byte_u0_p0_imm__ne,
	arm_instr_store_w0_signed_byte_u0_p0_imm__cs,
	arm_instr_store_w0_signed_byte_u0_p0_imm__cc,
	arm_instr_store_w0_signed_byte_u0_p0_imm__mi,
	arm_instr_store_w0_signed_byte_u0_p0_imm__pl,
	arm_instr_store_w0_signed_byte_u0_p0_imm__vs,
	arm_instr_store_w0_signed_byte_u0_p0_imm__vc,
	arm_instr_store_w0_signed_byte_u0_p0_imm__hi,
	arm_instr_store_w0_signed_byte_u0_p0_imm__ls,
	arm_instr_store_w0_signed_byte_u0_p0_imm__ge,
	arm_instr_store_w0_signed_byte_u0_p0_imm__lt,
	arm_instr_store_w0_signed_byte_u0_p0_imm__gt,
	arm_instr_store_w0_signed_byte_u0_p0_imm__le,
	arm_instr_store_w0_signed_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p0_imm__eq,
	arm_instr_load_w0_signed_byte_u0_p0_imm__ne,
	arm_instr_load_w0_signed_byte_u0_p0_imm__cs,
	arm_instr_load_w0_signed_byte_u0_p0_imm__cc,
	arm_instr_load_w0_signed_byte_u0_p0_imm__mi,
	arm_instr_load_w0_signed_byte_u0_p0_imm__pl,
	arm_instr_load_w0_signed_byte_u0_p0_imm__vs,
	arm_instr_load_w0_signed_byte_u0_p0_imm__vc,
	arm_instr_load_w0_signed_byte_u0_p0_imm__hi,
	arm_instr_load_w0_signed_byte_u0_p0_imm__ls,
	arm_instr_load_w0_signed_byte_u0_p0_imm__ge,
	arm_instr_load_w0_signed_byte_u0_p0_imm__lt,
	arm_instr_load_w0_signed_byte_u0_p0_imm__gt,
	arm_instr_load_w0_signed_byte_u0_p0_imm__le,
	arm_instr_load_w0_signed_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p0_imm__eq,
	arm_instr_store_w1_signed_byte_u0_p0_imm__ne,
	arm_instr_store_w1_signed_byte_u0_p0_imm__cs,
	arm_instr_store_w1_signed_byte_u0_p0_imm__cc,
	arm_instr_store_w1_signed_byte_u0_p0_imm__mi,
	arm_instr_store_w1_signed_byte_u0_p0_imm__pl,
	arm_instr_store_w1_signed_byte_u0_p0_imm__vs,
	arm_instr_store_w1_signed_byte_u0_p0_imm__vc,
	arm_instr_store_w1_signed_byte_u0_p0_imm__hi,
	arm_instr_store_w1_signed_byte_u0_p0_imm__ls,
	arm_instr_store_w1_signed_byte_u0_p0_imm__ge,
	arm_instr_store_w1_signed_byte_u0_p0_imm__lt,
	arm_instr_store_w1_signed_byte_u0_p0_imm__gt,
	arm_instr_store_w1_signed_byte_u0_p0_imm__le,
	arm_instr_store_w1_signed_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p0_imm__eq,
	arm_instr_load_w1_signed_byte_u0_p0_imm__ne,
	arm_instr_load_w1_signed_byte_u0_p0_imm__cs,
	arm_instr_load_w1_signed_byte_u0_p0_imm__cc,
	arm_instr_load_w1_signed_byte_u0_p0_imm__mi,
	arm_instr_load_w1_signed_byte_u0_p0_imm__pl,
	arm_instr_load_w1_signed_byte_u0_p0_imm__vs,
	arm_instr_load_w1_signed_byte_u0_p0_imm__vc,
	arm_instr_load_w1_signed_byte_u0_p0_imm__hi,
	arm_instr_load_w1_signed_byte_u0_p0_imm__ls,
	arm_instr_load_w1_signed_byte_u0_p0_imm__ge,
	arm_instr_load_w1_signed_byte_u0_p0_imm__lt,
	arm_instr_load_w1_signed_byte_u0_p0_imm__gt,
	arm_instr_load_w1_signed_byte_u0_p0_imm__le,
	arm_instr_load_w1_signed_byte_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm__le,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm__le,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__eq,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__ne,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__cs,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__cc,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__mi,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__pl,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__vs,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__vc,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__hi,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__ls,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__ge,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__lt,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__gt,
	arm_instr_store_w0_signed_halfword_u0_p0_imm__le,
	arm_instr_store_w0_signed_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__eq,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__ne,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__cs,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__cc,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__mi,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__pl,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__vs,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__vc,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__hi,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__ls,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__ge,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__lt,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__gt,
	arm_instr_load_w0_signed_halfword_u0_p0_imm__le,
	arm_instr_load_w0_signed_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm__le,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm__le,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__eq,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__ne,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__cs,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__cc,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__mi,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__pl,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__vs,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__vc,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__hi,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__ls,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__ge,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__lt,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__gt,
	arm_instr_store_w1_signed_halfword_u0_p0_imm__le,
	arm_instr_store_w1_signed_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__eq,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__ne,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__cs,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__cc,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__mi,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__pl,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__vs,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__vc,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__hi,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__ls,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__ge,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__lt,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__gt,
	arm_instr_load_w1_signed_halfword_u0_p0_imm__le,
	arm_instr_load_w1_signed_halfword_u0_p0_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p0_imm__eq,
	arm_instr_store_w0_signed_byte_u1_p0_imm__ne,
	arm_instr_store_w0_signed_byte_u1_p0_imm__cs,
	arm_instr_store_w0_signed_byte_u1_p0_imm__cc,
	arm_instr_store_w0_signed_byte_u1_p0_imm__mi,
	arm_instr_store_w0_signed_byte_u1_p0_imm__pl,
	arm_instr_store_w0_signed_byte_u1_p0_imm__vs,
	arm_instr_store_w0_signed_byte_u1_p0_imm__vc,
	arm_instr_store_w0_signed_byte_u1_p0_imm__hi,
	arm_instr_store_w0_signed_byte_u1_p0_imm__ls,
	arm_instr_store_w0_signed_byte_u1_p0_imm__ge,
	arm_instr_store_w0_signed_byte_u1_p0_imm__lt,
	arm_instr_store_w0_signed_byte_u1_p0_imm__gt,
	arm_instr_store_w0_signed_byte_u1_p0_imm__le,
	arm_instr_store_w0_signed_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p0_imm__eq,
	arm_instr_load_w0_signed_byte_u1_p0_imm__ne,
	arm_instr_load_w0_signed_byte_u1_p0_imm__cs,
	arm_instr_load_w0_signed_byte_u1_p0_imm__cc,
	arm_instr_load_w0_signed_byte_u1_p0_imm__mi,
	arm_instr_load_w0_signed_byte_u1_p0_imm__pl,
	arm_instr_load_w0_signed_byte_u1_p0_imm__vs,
	arm_instr_load_w0_signed_byte_u1_p0_imm__vc,
	arm_instr_load_w0_signed_byte_u1_p0_imm__hi,
	arm_instr_load_w0_signed_byte_u1_p0_imm__ls,
	arm_instr_load_w0_signed_byte_u1_p0_imm__ge,
	arm_instr_load_w0_signed_byte_u1_p0_imm__lt,
	arm_instr_load_w0_signed_byte_u1_p0_imm__gt,
	arm_instr_load_w0_signed_byte_u1_p0_imm__le,
	arm_instr_load_w0_signed_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p0_imm__eq,
	arm_instr_store_w1_signed_byte_u1_p0_imm__ne,
	arm_instr_store_w1_signed_byte_u1_p0_imm__cs,
	arm_instr_store_w1_signed_byte_u1_p0_imm__cc,
	arm_instr_store_w1_signed_byte_u1_p0_imm__mi,
	arm_instr_store_w1_signed_byte_u1_p0_imm__pl,
	arm_instr_store_w1_signed_byte_u1_p0_imm__vs,
	arm_instr_store_w1_signed_byte_u1_p0_imm__vc,
	arm_instr_store_w1_signed_byte_u1_p0_imm__hi,
	arm_instr_store_w1_signed_byte_u1_p0_imm__ls,
	arm_instr_store_w1_signed_byte_u1_p0_imm__ge,
	arm_instr_store_w1_signed_byte_u1_p0_imm__lt,
	arm_instr_store_w1_signed_byte_u1_p0_imm__gt,
	arm_instr_store_w1_signed_byte_u1_p0_imm__le,
	arm_instr_store_w1_signed_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p0_imm__eq,
	arm_instr_load_w1_signed_byte_u1_p0_imm__ne,
	arm_instr_load_w1_signed_byte_u1_p0_imm__cs,
	arm_instr_load_w1_signed_byte_u1_p0_imm__cc,
	arm_instr_load_w1_signed_byte_u1_p0_imm__mi,
	arm_instr_load_w1_signed_byte_u1_p0_imm__pl,
	arm_instr_load_w1_signed_byte_u1_p0_imm__vs,
	arm_instr_load_w1_signed_byte_u1_p0_imm__vc,
	arm_instr_load_w1_signed_byte_u1_p0_imm__hi,
	arm_instr_load_w1_signed_byte_u1_p0_imm__ls,
	arm_instr_load_w1_signed_byte_u1_p0_imm__ge,
	arm_instr_load_w1_signed_byte_u1_p0_imm__lt,
	arm_instr_load_w1_signed_byte_u1_p0_imm__gt,
	arm_instr_load_w1_signed_byte_u1_p0_imm__le,
	arm_instr_load_w1_signed_byte_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm__le,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm__le,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__eq,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__ne,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__cs,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__cc,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__mi,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__pl,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__vs,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__vc,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__hi,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__ls,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__ge,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__lt,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__gt,
	arm_instr_store_w0_signed_halfword_u1_p0_imm__le,
	arm_instr_store_w0_signed_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__eq,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__ne,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__cs,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__cc,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__mi,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__pl,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__vs,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__vc,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__hi,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__ls,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__ge,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__lt,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__gt,
	arm_instr_load_w0_signed_halfword_u1_p0_imm__le,
	arm_instr_load_w0_signed_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm__le,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm__le,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__eq,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__ne,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__cs,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__cc,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__mi,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__pl,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__vs,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__vc,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__hi,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__ls,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__ge,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__lt,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__gt,
	arm_instr_store_w1_signed_halfword_u1_p0_imm__le,
	arm_instr_store_w1_signed_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__eq,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__ne,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__cs,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__cc,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__mi,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__pl,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__vs,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__vc,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__hi,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__ls,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__ge,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__lt,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__gt,
	arm_instr_load_w1_signed_halfword_u1_p0_imm__le,
	arm_instr_load_w1_signed_halfword_u1_p0_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p1_imm__eq,
	arm_instr_store_w0_signed_byte_u0_p1_imm__ne,
	arm_instr_store_w0_signed_byte_u0_p1_imm__cs,
	arm_instr_store_w0_signed_byte_u0_p1_imm__cc,
	arm_instr_store_w0_signed_byte_u0_p1_imm__mi,
	arm_instr_store_w0_signed_byte_u0_p1_imm__pl,
	arm_instr_store_w0_signed_byte_u0_p1_imm__vs,
	arm_instr_store_w0_signed_byte_u0_p1_imm__vc,
	arm_instr_store_w0_signed_byte_u0_p1_imm__hi,
	arm_instr_store_w0_signed_byte_u0_p1_imm__ls,
	arm_instr_store_w0_signed_byte_u0_p1_imm__ge,
	arm_instr_store_w0_signed_byte_u0_p1_imm__lt,
	arm_instr_store_w0_signed_byte_u0_p1_imm__gt,
	arm_instr_store_w0_signed_byte_u0_p1_imm__le,
	arm_instr_store_w0_signed_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p1_imm__eq,
	arm_instr_load_w0_signed_byte_u0_p1_imm__ne,
	arm_instr_load_w0_signed_byte_u0_p1_imm__cs,
	arm_instr_load_w0_signed_byte_u0_p1_imm__cc,
	arm_instr_load_w0_signed_byte_u0_p1_imm__mi,
	arm_instr_load_w0_signed_byte_u0_p1_imm__pl,
	arm_instr_load_w0_signed_byte_u0_p1_imm__vs,
	arm_instr_load_w0_signed_byte_u0_p1_imm__vc,
	arm_instr_load_w0_signed_byte_u0_p1_imm__hi,
	arm_instr_load_w0_signed_byte_u0_p1_imm__ls,
	arm_instr_load_w0_signed_byte_u0_p1_imm__ge,
	arm_instr_load_w0_signed_byte_u0_p1_imm__lt,
	arm_instr_load_w0_signed_byte_u0_p1_imm__gt,
	arm_instr_load_w0_signed_byte_u0_p1_imm__le,
	arm_instr_load_w0_signed_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p1_imm__eq,
	arm_instr_store_w1_signed_byte_u0_p1_imm__ne,
	arm_instr_store_w1_signed_byte_u0_p1_imm__cs,
	arm_instr_store_w1_signed_byte_u0_p1_imm__cc,
	arm_instr_store_w1_signed_byte_u0_p1_imm__mi,
	arm_instr_store_w1_signed_byte_u0_p1_imm__pl,
	arm_instr_store_w1_signed_byte_u0_p1_imm__vs,
	arm_instr_store_w1_signed_byte_u0_p1_imm__vc,
	arm_instr_store_w1_signed_byte_u0_p1_imm__hi,
	arm_instr_store_w1_signed_byte_u0_p1_imm__ls,
	arm_instr_store_w1_signed_byte_u0_p1_imm__ge,
	arm_instr_store_w1_signed_byte_u0_p1_imm__lt,
	arm_instr_store_w1_signed_byte_u0_p1_imm__gt,
	arm_instr_store_w1_signed_byte_u0_p1_imm__le,
	arm_instr_store_w1_signed_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p1_imm__eq,
	arm_instr_load_w1_signed_byte_u0_p1_imm__ne,
	arm_instr_load_w1_signed_byte_u0_p1_imm__cs,
	arm_instr_load_w1_signed_byte_u0_p1_imm__cc,
	arm_instr_load_w1_signed_byte_u0_p1_imm__mi,
	arm_instr_load_w1_signed_byte_u0_p1_imm__pl,
	arm_instr_load_w1_signed_byte_u0_p1_imm__vs,
	arm_instr_load_w1_signed_byte_u0_p1_imm__vc,
	arm_instr_load_w1_signed_byte_u0_p1_imm__hi,
	arm_instr_load_w1_signed_byte_u0_p1_imm__ls,
	arm_instr_load_w1_signed_byte_u0_p1_imm__ge,
	arm_instr_load_w1_signed_byte_u0_p1_imm__lt,
	arm_instr_load_w1_signed_byte_u0_p1_imm__gt,
	arm_instr_load_w1_signed_byte_u0_p1_imm__le,
	arm_instr_load_w1_signed_byte_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm__le,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm__le,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__eq,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__ne,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__cs,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__cc,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__mi,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__pl,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__vs,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__vc,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__hi,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__ls,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__ge,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__lt,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__gt,
	arm_instr_store_w0_signed_halfword_u0_p1_imm__le,
	arm_instr_store_w0_signed_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__eq,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__ne,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__cs,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__cc,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__mi,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__pl,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__vs,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__vc,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__hi,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__ls,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__ge,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__lt,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__gt,
	arm_instr_load_w0_signed_halfword_u0_p1_imm__le,
	arm_instr_load_w0_signed_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm__le,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm__le,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__eq,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__ne,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__cs,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__cc,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__mi,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__pl,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__vs,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__vc,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__hi,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__ls,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__ge,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__lt,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__gt,
	arm_instr_store_w1_signed_halfword_u0_p1_imm__le,
	arm_instr_store_w1_signed_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__eq,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__ne,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__cs,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__cc,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__mi,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__pl,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__vs,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__vc,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__hi,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__ls,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__ge,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__lt,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__gt,
	arm_instr_load_w1_signed_halfword_u0_p1_imm__le,
	arm_instr_load_w1_signed_halfword_u0_p1_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p1_imm__eq,
	arm_instr_store_w0_signed_byte_u1_p1_imm__ne,
	arm_instr_store_w0_signed_byte_u1_p1_imm__cs,
	arm_instr_store_w0_signed_byte_u1_p1_imm__cc,
	arm_instr_store_w0_signed_byte_u1_p1_imm__mi,
	arm_instr_store_w0_signed_byte_u1_p1_imm__pl,
	arm_instr_store_w0_signed_byte_u1_p1_imm__vs,
	arm_instr_store_w0_signed_byte_u1_p1_imm__vc,
	arm_instr_store_w0_signed_byte_u1_p1_imm__hi,
	arm_instr_store_w0_signed_byte_u1_p1_imm__ls,
	arm_instr_store_w0_signed_byte_u1_p1_imm__ge,
	arm_instr_store_w0_signed_byte_u1_p1_imm__lt,
	arm_instr_store_w0_signed_byte_u1_p1_imm__gt,
	arm_instr_store_w0_signed_byte_u1_p1_imm__le,
	arm_instr_store_w0_signed_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p1_imm__eq,
	arm_instr_load_w0_signed_byte_u1_p1_imm__ne,
	arm_instr_load_w0_signed_byte_u1_p1_imm__cs,
	arm_instr_load_w0_signed_byte_u1_p1_imm__cc,
	arm_instr_load_w0_signed_byte_u1_p1_imm__mi,
	arm_instr_load_w0_signed_byte_u1_p1_imm__pl,
	arm_instr_load_w0_signed_byte_u1_p1_imm__vs,
	arm_instr_load_w0_signed_byte_u1_p1_imm__vc,
	arm_instr_load_w0_signed_byte_u1_p1_imm__hi,
	arm_instr_load_w0_signed_byte_u1_p1_imm__ls,
	arm_instr_load_w0_signed_byte_u1_p1_imm__ge,
	arm_instr_load_w0_signed_byte_u1_p1_imm__lt,
	arm_instr_load_w0_signed_byte_u1_p1_imm__gt,
	arm_instr_load_w0_signed_byte_u1_p1_imm__le,
	arm_instr_load_w0_signed_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p1_imm__eq,
	arm_instr_store_w1_signed_byte_u1_p1_imm__ne,
	arm_instr_store_w1_signed_byte_u1_p1_imm__cs,
	arm_instr_store_w1_signed_byte_u1_p1_imm__cc,
	arm_instr_store_w1_signed_byte_u1_p1_imm__mi,
	arm_instr_store_w1_signed_byte_u1_p1_imm__pl,
	arm_instr_store_w1_signed_byte_u1_p1_imm__vs,
	arm_instr_store_w1_signed_byte_u1_p1_imm__vc,
	arm_instr_store_w1_signed_byte_u1_p1_imm__hi,
	arm_instr_store_w1_signed_byte_u1_p1_imm__ls,
	arm_instr_store_w1_signed_byte_u1_p1_imm__ge,
	arm_instr_store_w1_signed_byte_u1_p1_imm__lt,
	arm_instr_store_w1_signed_byte_u1_p1_imm__gt,
	arm_instr_store_w1_signed_byte_u1_p1_imm__le,
	arm_instr_store_w1_signed_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p1_imm__eq,
	arm_instr_load_w1_signed_byte_u1_p1_imm__ne,
	arm_instr_load_w1_signed_byte_u1_p1_imm__cs,
	arm_instr_load_w1_signed_byte_u1_p1_imm__cc,
	arm_instr_load_w1_signed_byte_u1_p1_imm__mi,
	arm_instr_load_w1_signed_byte_u1_p1_imm__pl,
	arm_instr_load_w1_signed_byte_u1_p1_imm__vs,
	arm_instr_load_w1_signed_byte_u1_p1_imm__vc,
	arm_instr_load_w1_signed_byte_u1_p1_imm__hi,
	arm_instr_load_w1_signed_byte_u1_p1_imm__ls,
	arm_instr_load_w1_signed_byte_u1_p1_imm__ge,
	arm_instr_load_w1_signed_byte_u1_p1_imm__lt,
	arm_instr_load_w1_signed_byte_u1_p1_imm__gt,
	arm_instr_load_w1_signed_byte_u1_p1_imm__le,
	arm_instr_load_w1_signed_byte_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm__le,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm__le,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__eq,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__ne,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__cs,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__cc,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__mi,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__pl,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__vs,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__vc,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__hi,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__ls,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__ge,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__lt,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__gt,
	arm_instr_store_w0_signed_halfword_u1_p1_imm__le,
	arm_instr_store_w0_signed_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__eq,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__ne,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__cs,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__cc,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__mi,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__pl,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__vs,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__vc,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__hi,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__ls,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__ge,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__lt,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__gt,
	arm_instr_load_w0_signed_halfword_u1_p1_imm__le,
	arm_instr_load_w0_signed_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm__le,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm__le,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__eq,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__ne,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__cs,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__cc,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__mi,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__pl,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__vs,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__vc,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__hi,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__ls,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__ge,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__lt,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__gt,
	arm_instr_store_w1_signed_halfword_u1_p1_imm__le,
	arm_instr_store_w1_signed_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__eq,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__ne,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__cs,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__cc,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__mi,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__pl,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__vs,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__vc,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__hi,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__ls,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__ge,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__lt,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__gt,
	arm_instr_load_w1_signed_halfword_u1_p1_imm__le,
	arm_instr_load_w1_signed_halfword_u1_p1_imm,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p0_reg__eq,
	arm_instr_store_w0_signed_byte_u0_p0_reg__ne,
	arm_instr_store_w0_signed_byte_u0_p0_reg__cs,
	arm_instr_store_w0_signed_byte_u0_p0_reg__cc,
	arm_instr_store_w0_signed_byte_u0_p0_reg__mi,
	arm_instr_store_w0_signed_byte_u0_p0_reg__pl,
	arm_instr_store_w0_signed_byte_u0_p0_reg__vs,
	arm_instr_store_w0_signed_byte_u0_p0_reg__vc,
	arm_instr_store_w0_signed_byte_u0_p0_reg__hi,
	arm_instr_store_w0_signed_byte_u0_p0_reg__ls,
	arm_instr_store_w0_signed_byte_u0_p0_reg__ge,
	arm_instr_store_w0_signed_byte_u0_p0_reg__lt,
	arm_instr_store_w0_signed_byte_u0_p0_reg__gt,
	arm_instr_store_w0_signed_byte_u0_p0_reg__le,
	arm_instr_store_w0_signed_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p0_reg__eq,
	arm_instr_load_w0_signed_byte_u0_p0_reg__ne,
	arm_instr_load_w0_signed_byte_u0_p0_reg__cs,
	arm_instr_load_w0_signed_byte_u0_p0_reg__cc,
	arm_instr_load_w0_signed_byte_u0_p0_reg__mi,
	arm_instr_load_w0_signed_byte_u0_p0_reg__pl,
	arm_instr_load_w0_signed_byte_u0_p0_reg__vs,
	arm_instr_load_w0_signed_byte_u0_p0_reg__vc,
	arm_instr_load_w0_signed_byte_u0_p0_reg__hi,
	arm_instr_load_w0_signed_byte_u0_p0_reg__ls,
	arm_instr_load_w0_signed_byte_u0_p0_reg__ge,
	arm_instr_load_w0_signed_byte_u0_p0_reg__lt,
	arm_instr_load_w0_signed_byte_u0_p0_reg__gt,
	arm_instr_load_w0_signed_byte_u0_p0_reg__le,
	arm_instr_load_w0_signed_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p0_reg__eq,
	arm_instr_store_w1_signed_byte_u0_p0_reg__ne,
	arm_instr_store_w1_signed_byte_u0_p0_reg__cs,
	arm_instr_store_w1_signed_byte_u0_p0_reg__cc,
	arm_instr_store_w1_signed_byte_u0_p0_reg__mi,
	arm_instr_store_w1_signed_byte_u0_p0_reg__pl,
	arm_instr_store_w1_signed_byte_u0_p0_reg__vs,
	arm_instr_store_w1_signed_byte_u0_p0_reg__vc,
	arm_instr_store_w1_signed_byte_u0_p0_reg__hi,
	arm_instr_store_w1_signed_byte_u0_p0_reg__ls,
	arm_instr_store_w1_signed_byte_u0_p0_reg__ge,
	arm_instr_store_w1_signed_byte_u0_p0_reg__lt,
	arm_instr_store_w1_signed_byte_u0_p0_reg__gt,
	arm_instr_store_w1_signed_byte_u0_p0_reg__le,
	arm_instr_store_w1_signed_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p0_reg__eq,
	arm_instr_load_w1_signed_byte_u0_p0_reg__ne,
	arm_instr_load_w1_signed_byte_u0_p0_reg__cs,
	arm_instr_load_w1_signed_byte_u0_p0_reg__cc,
	arm_instr_load_w1_signed_byte_u0_p0_reg__mi,
	arm_instr_load_w1_signed_byte_u0_p0_reg__pl,
	arm_instr_load_w1_signed_byte_u0_p0_reg__vs,
	arm_instr_load_w1_signed_byte_u0_p0_reg__vc,
	arm_instr_load_w1_signed_byte_u0_p0_reg__hi,
	arm_instr_load_w1_signed_byte_u0_p0_reg__ls,
	arm_instr_load_w1_signed_byte_u0_p0_reg__ge,
	arm_instr_load_w1_signed_byte_u0_p0_reg__lt,
	arm_instr_load_w1_signed_byte_u0_p0_reg__gt,
	arm_instr_load_w1_signed_byte_u0_p0_reg__le,
	arm_instr_load_w1_signed_byte_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg__le,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg__le,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__eq,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__ne,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__cs,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__cc,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__mi,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__pl,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__vs,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__vc,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__hi,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__ls,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__ge,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__lt,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__gt,
	arm_instr_store_w0_signed_halfword_u0_p0_reg__le,
	arm_instr_store_w0_signed_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__eq,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__ne,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__cs,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__cc,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__mi,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__pl,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__vs,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__vc,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__hi,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__ls,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__ge,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__lt,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__gt,
	arm_instr_load_w0_signed_halfword_u0_p0_reg__le,
	arm_instr_load_w0_signed_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg__le,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg__le,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__eq,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__ne,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__cs,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__cc,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__mi,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__pl,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__vs,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__vc,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__hi,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__ls,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__ge,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__lt,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__gt,
	arm_instr_store_w1_signed_halfword_u0_p0_reg__le,
	arm_instr_store_w1_signed_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__eq,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__ne,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__cs,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__cc,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__mi,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__pl,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__vs,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__vc,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__hi,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__ls,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__ge,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__lt,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__gt,
	arm_instr_load_w1_signed_halfword_u0_p0_reg__le,
	arm_instr_load_w1_signed_halfword_u0_p0_reg,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p0_reg__eq,
	arm_instr_store_w0_signed_byte_u1_p0_reg__ne,
	arm_instr_store_w0_signed_byte_u1_p0_reg__cs,
	arm_instr_store_w0_signed_byte_u1_p0_reg__cc,
	arm_instr_store_w0_signed_byte_u1_p0_reg__mi,
	arm_instr_store_w0_signed_byte_u1_p0_reg__pl,
	arm_instr_store_w0_signed_byte_u1_p0_reg__vs,
	arm_instr_store_w0_signed_byte_u1_p0_reg__vc,
	arm_instr_store_w0_signed_byte_u1_p0_reg__hi,
	arm_instr_store_w0_signed_byte_u1_p0_reg__ls,
	arm_instr_store_w0_signed_byte_u1_p0_reg__ge,
	arm_instr_store_w0_signed_byte_u1_p0_reg__lt,
	arm_instr_store_w0_signed_byte_u1_p0_reg__gt,
	arm_instr_store_w0_signed_byte_u1_p0_reg__le,
	arm_instr_store_w0_signed_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p0_reg__eq,
	arm_instr_load_w0_signed_byte_u1_p0_reg__ne,
	arm_instr_load_w0_signed_byte_u1_p0_reg__cs,
	arm_instr_load_w0_signed_byte_u1_p0_reg__cc,
	arm_instr_load_w0_signed_byte_u1_p0_reg__mi,
	arm_instr_load_w0_signed_byte_u1_p0_reg__pl,
	arm_instr_load_w0_signed_byte_u1_p0_reg__vs,
	arm_instr_load_w0_signed_byte_u1_p0_reg__vc,
	arm_instr_load_w0_signed_byte_u1_p0_reg__hi,
	arm_instr_load_w0_signed_byte_u1_p0_reg__ls,
	arm_instr_load_w0_signed_byte_u1_p0_reg__ge,
	arm_instr_load_w0_signed_byte_u1_p0_reg__lt,
	arm_instr_load_w0_signed_byte_u1_p0_reg__gt,
	arm_instr_load_w0_signed_byte_u1_p0_reg__le,
	arm_instr_load_w0_signed_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p0_reg__eq,
	arm_instr_store_w1_signed_byte_u1_p0_reg__ne,
	arm_instr_store_w1_signed_byte_u1_p0_reg__cs,
	arm_instr_store_w1_signed_byte_u1_p0_reg__cc,
	arm_instr_store_w1_signed_byte_u1_p0_reg__mi,
	arm_instr_store_w1_signed_byte_u1_p0_reg__pl,
	arm_instr_store_w1_signed_byte_u1_p0_reg__vs,
	arm_instr_store_w1_signed_byte_u1_p0_reg__vc,
	arm_instr_store_w1_signed_byte_u1_p0_reg__hi,
	arm_instr_store_w1_signed_byte_u1_p0_reg__ls,
	arm_instr_store_w1_signed_byte_u1_p0_reg__ge,
	arm_instr_store_w1_signed_byte_u1_p0_reg__lt,
	arm_instr_store_w1_signed_byte_u1_p0_reg__gt,
	arm_instr_store_w1_signed_byte_u1_p0_reg__le,
	arm_instr_store_w1_signed_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p0_reg__eq,
	arm_instr_load_w1_signed_byte_u1_p0_reg__ne,
	arm_instr_load_w1_signed_byte_u1_p0_reg__cs,
	arm_instr_load_w1_signed_byte_u1_p0_reg__cc,
	arm_instr_load_w1_signed_byte_u1_p0_reg__mi,
	arm_instr_load_w1_signed_byte_u1_p0_reg__pl,
	arm_instr_load_w1_signed_byte_u1_p0_reg__vs,
	arm_instr_load_w1_signed_byte_u1_p0_reg__vc,
	arm_instr_load_w1_signed_byte_u1_p0_reg__hi,
	arm_instr_load_w1_signed_byte_u1_p0_reg__ls,
	arm_instr_load_w1_signed_byte_u1_p0_reg__ge,
	arm_instr_load_w1_signed_byte_u1_p0_reg__lt,
	arm_instr_load_w1_signed_byte_u1_p0_reg__gt,
	arm_instr_load_w1_signed_byte_u1_p0_reg__le,
	arm_instr_load_w1_signed_byte_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg__le,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg__le,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__eq,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__ne,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__cs,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__cc,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__mi,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__pl,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__vs,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__vc,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__hi,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__ls,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__ge,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__lt,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__gt,
	arm_instr_store_w0_signed_halfword_u1_p0_reg__le,
	arm_instr_store_w0_signed_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__eq,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__ne,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__cs,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__cc,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__mi,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__pl,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__vs,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__vc,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__hi,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__ls,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__ge,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__lt,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__gt,
	arm_instr_load_w0_signed_halfword_u1_p0_reg__le,
	arm_instr_load_w0_signed_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg__le,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg__le,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__eq,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__ne,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__cs,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__cc,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__mi,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__pl,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__vs,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__vc,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__hi,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__ls,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__ge,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__lt,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__gt,
	arm_instr_store_w1_signed_halfword_u1_p0_reg__le,
	arm_instr_store_w1_signed_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__eq,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__ne,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__cs,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__cc,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__mi,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__pl,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__vs,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__vc,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__hi,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__ls,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__ge,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__lt,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__gt,
	arm_instr_load_w1_signed_halfword_u1_p0_reg__le,
	arm_instr_load_w1_signed_halfword_u1_p0_reg,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p1_reg__eq,
	arm_instr_store_w0_signed_byte_u0_p1_reg__ne,
	arm_instr_store_w0_signed_byte_u0_p1_reg__cs,
	arm_instr_store_w0_signed_byte_u0_p1_reg__cc,
	arm_instr_store_w0_signed_byte_u0_p1_reg__mi,
	arm_instr_store_w0_signed_byte_u0_p1_reg__pl,
	arm_instr_store_w0_signed_byte_u0_p1_reg__vs,
	arm_instr_store_w0_signed_byte_u0_p1_reg__vc,
	arm_instr_store_w0_signed_byte_u0_p1_reg__hi,
	arm_instr_store_w0_signed_byte_u0_p1_reg__ls,
	arm_instr_store_w0_signed_byte_u0_p1_reg__ge,
	arm_instr_store_w0_signed_byte_u0_p1_reg__lt,
	arm_instr_store_w0_signed_byte_u0_p1_reg__gt,
	arm_instr_store_w0_signed_byte_u0_p1_reg__le,
	arm_instr_store_w0_signed_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p1_reg__eq,
	arm_instr_load_w0_signed_byte_u0_p1_reg__ne,
	arm_instr_load_w0_signed_byte_u0_p1_reg__cs,
	arm_instr_load_w0_signed_byte_u0_p1_reg__cc,
	arm_instr_load_w0_signed_byte_u0_p1_reg__mi,
	arm_instr_load_w0_signed_byte_u0_p1_reg__pl,
	arm_instr_load_w0_signed_byte_u0_p1_reg__vs,
	arm_instr_load_w0_signed_byte_u0_p1_reg__vc,
	arm_instr_load_w0_signed_byte_u0_p1_reg__hi,
	arm_instr_load_w0_signed_byte_u0_p1_reg__ls,
	arm_instr_load_w0_signed_byte_u0_p1_reg__ge,
	arm_instr_load_w0_signed_byte_u0_p1_reg__lt,
	arm_instr_load_w0_signed_byte_u0_p1_reg__gt,
	arm_instr_load_w0_signed_byte_u0_p1_reg__le,
	arm_instr_load_w0_signed_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p1_reg__eq,
	arm_instr_store_w1_signed_byte_u0_p1_reg__ne,
	arm_instr_store_w1_signed_byte_u0_p1_reg__cs,
	arm_instr_store_w1_signed_byte_u0_p1_reg__cc,
	arm_instr_store_w1_signed_byte_u0_p1_reg__mi,
	arm_instr_store_w1_signed_byte_u0_p1_reg__pl,
	arm_instr_store_w1_signed_byte_u0_p1_reg__vs,
	arm_instr_store_w1_signed_byte_u0_p1_reg__vc,
	arm_instr_store_w1_signed_byte_u0_p1_reg__hi,
	arm_instr_store_w1_signed_byte_u0_p1_reg__ls,
	arm_instr_store_w1_signed_byte_u0_p1_reg__ge,
	arm_instr_store_w1_signed_byte_u0_p1_reg__lt,
	arm_instr_store_w1_signed_byte_u0_p1_reg__gt,
	arm_instr_store_w1_signed_byte_u0_p1_reg__le,
	arm_instr_store_w1_signed_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p1_reg__eq,
	arm_instr_load_w1_signed_byte_u0_p1_reg__ne,
	arm_instr_load_w1_signed_byte_u0_p1_reg__cs,
	arm_instr_load_w1_signed_byte_u0_p1_reg__cc,
	arm_instr_load_w1_signed_byte_u0_p1_reg__mi,
	arm_instr_load_w1_signed_byte_u0_p1_reg__pl,
	arm_instr_load_w1_signed_byte_u0_p1_reg__vs,
	arm_instr_load_w1_signed_byte_u0_p1_reg__vc,
	arm_instr_load_w1_signed_byte_u0_p1_reg__hi,
	arm_instr_load_w1_signed_byte_u0_p1_reg__ls,
	arm_instr_load_w1_signed_byte_u0_p1_reg__ge,
	arm_instr_load_w1_signed_byte_u0_p1_reg__lt,
	arm_instr_load_w1_signed_byte_u0_p1_reg__gt,
	arm_instr_load_w1_signed_byte_u0_p1_reg__le,
	arm_instr_load_w1_signed_byte_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg__le,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg__le,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__eq,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__ne,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__cs,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__cc,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__mi,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__pl,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__vs,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__vc,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__hi,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__ls,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__ge,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__lt,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__gt,
	arm_instr_store_w0_signed_halfword_u0_p1_reg__le,
	arm_instr_store_w0_signed_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__eq,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__ne,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__cs,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__cc,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__mi,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__pl,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__vs,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__vc,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__hi,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__ls,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__ge,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__lt,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__gt,
	arm_instr_load_w0_signed_halfword_u0_p1_reg__le,
	arm_instr_load_w0_signed_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg__le,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg__le,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__eq,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__ne,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__cs,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__cc,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__mi,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__pl,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__vs,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__vc,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__hi,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__ls,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__ge,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__lt,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__gt,
	arm_instr_store_w1_signed_halfword_u0_p1_reg__le,
	arm_instr_store_w1_signed_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__eq,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__ne,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__cs,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__cc,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__mi,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__pl,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__vs,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__vc,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__hi,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__ls,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__ge,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__lt,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__gt,
	arm_instr_load_w1_signed_halfword_u0_p1_reg__le,
	arm_instr_load_w1_signed_halfword_u0_p1_reg,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p1_reg__eq,
	arm_instr_store_w0_signed_byte_u1_p1_reg__ne,
	arm_instr_store_w0_signed_byte_u1_p1_reg__cs,
	arm_instr_store_w0_signed_byte_u1_p1_reg__cc,
	arm_instr_store_w0_signed_byte_u1_p1_reg__mi,
	arm_instr_store_w0_signed_byte_u1_p1_reg__pl,
	arm_instr_store_w0_signed_byte_u1_p1_reg__vs,
	arm_instr_store_w0_signed_byte_u1_p1_reg__vc,
	arm_instr_store_w0_signed_byte_u1_p1_reg__hi,
	arm_instr_store_w0_signed_byte_u1_p1_reg__ls,
	arm_instr_store_w0_signed_byte_u1_p1_reg__ge,
	arm_instr_store_w0_signed_byte_u1_p1_reg__lt,
	arm_instr_store_w0_signed_byte_u1_p1_reg__gt,
	arm_instr_store_w0_signed_byte_u1_p1_reg__le,
	arm_instr_store_w0_signed_byte_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p1_reg__eq,
	arm_instr_load_w0_signed_byte_u1_p1_reg__ne,
	arm_instr_load_w0_signed_byte_u1_p1_reg__cs,
	arm_instr_load_w0_signed_byte_u1_p1_reg__cc,
	arm_instr_load_w0_signed_byte_u1_p1_reg__mi,
	arm_instr_load_w0_signed_byte_u1_p1_reg__pl,
	arm_instr_load_w0_signed_byte_u1_p1_reg__vs,
	arm_instr_load_w0_signed_byte_u1_p1_reg__vc,
	arm_instr_load_w0_signed_byte_u1_p1_reg__hi,
	arm_instr_load_w0_signed_byte_u1_p1_reg__ls,
	arm_instr_load_w0_signed_byte_u1_p1_reg__ge,
	arm_instr_load_w0_signed_byte_u1_p1_reg__lt,
	arm_instr_load_w0_signed_byte_u1_p1_reg__gt,
	arm_instr_load_w0_signed_byte_u1_p1_reg__le,
	arm_instr_load_w0_signed_byte_u1_p1_reg,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p1_reg__eq,
	arm_instr_store_w1_signed_byte_u1_p1_reg__ne,
	arm_instr_store_w1_signed_byte_u1_p1_reg__cs,
	arm_instr_store_w1_signed_byte_u1_p1_reg__cc,
	arm_instr_store_w1_signed_byte_u1_p1_reg__mi,
	arm_instr_store_w1_signed_byte_u1_p1_reg__pl,
	arm_instr_store_w1_signed_byte_u1_p1_reg__vs,
	arm_instr_store_w1_signed_byte_u1_p1_reg__vc,
	arm_instr_store_w1_signed_byte_u1_p1_reg__hi,
	arm_instr_store_w1_signed_byte_u1_p1_reg__ls,
	arm_instr_store_w1_signed_byte_u1_p1_reg__ge,
	arm_instr_store_w1_signed_byte_u1_p1_reg__lt,
	arm_instr_store_w1_signed_byte_u1_p1_reg__gt,
	arm_instr_store_w1_signed_byte_u1_p1_reg__le,
	arm_instr_store_w1_signed_byte_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p1_reg__eq,
	arm_instr_load_w1_signed_byte_u1_p1_reg__ne,
	arm_instr_load_w1_signed_byte_u1_p1_reg__cs,
	arm_instr_load_w1_signed_byte_u1_p1_reg__cc,
	arm_instr_load_w1_signed_byte_u1_p1_reg__mi,
	arm_instr_load_w1_signed_byte_u1_p1_reg__pl,
	arm_instr_load_w1_signed_byte_u1_p1_reg__vs,
	arm_instr_load_w1_signed_byte_u1_p1_reg__vc,
	arm_instr_load_w1_signed_byte_u1_p1_reg__hi,
	arm_instr_load_w1_signed_byte_u1_p1_reg__ls,
	arm_instr_load_w1_signed_byte_u1_p1_reg__ge,
	arm_instr_load_w1_signed_byte_u1_p1_reg__lt,
	arm_instr_load_w1_signed_byte_u1_p1_reg__gt,
	arm_instr_load_w1_signed_byte_u1_p1_reg__le,
	arm_instr_load_w1_signed_byte_u1_p1_reg,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg__le,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg__le,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__eq,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__ne,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__cs,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__cc,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__mi,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__pl,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__vs,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__vc,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__hi,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__ls,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__ge,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__lt,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__gt,
	arm_instr_store_w0_signed_halfword_u1_p1_reg__le,
	arm_instr_store_w0_signed_halfword_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__eq,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__ne,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__cs,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__cc,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__mi,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__pl,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__vs,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__vc,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__hi,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__ls,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__ge,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__lt,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__gt,
	arm_instr_load_w0_signed_halfword_u1_p1_reg__le,
	arm_instr_load_w0_signed_halfword_u1_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg__le,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg__le,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__eq,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__ne,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__cs,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__cc,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__mi,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__pl,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__vs,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__vc,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__hi,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__ls,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__ge,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__lt,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__gt,
	arm_instr_store_w1_signed_halfword_u1_p1_reg__le,
	arm_instr_store_w1_signed_halfword_u1_p1_reg,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__eq,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__ne,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__cs,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__cc,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__mi,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__pl,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__vs,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__vc,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__hi,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__ls,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__ge,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__lt,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__gt,
	arm_instr_load_w1_signed_halfword_u1_p1_reg__le,
	arm_instr_load_w1_signed_halfword_u1_p1_reg,
	arm_instr_nop
};


	void (*arm_load_store_instr_3_pc[2048])(struct cpu *,
		struct arm_instr_call *) = {
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__eq,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__ne,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__cs,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__cc,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__mi,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__pl,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__vs,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__vc,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__hi,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__ls,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__ge,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__lt,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__gt,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc__le,
	arm_instr_store_w0_signed_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__eq,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__ne,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__cs,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__cc,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__mi,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__pl,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__vs,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__vc,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__hi,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__ls,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__ge,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__lt,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__gt,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc__le,
	arm_instr_load_w0_signed_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__eq,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__ne,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__cs,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__cc,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__mi,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__pl,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__vs,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__vc,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__hi,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__ls,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__ge,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__lt,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__gt,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc__le,
	arm_instr_store_w1_signed_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__eq,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__ne,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__cs,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__cc,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__mi,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__pl,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__vs,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__vc,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__hi,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__ls,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__ge,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__lt,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__gt,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc__le,
	arm_instr_load_w1_signed_byte_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc__le,
	arm_instr_store_w0_unsigned_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc__le,
	arm_instr_load_w0_unsigned_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__eq,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__ne,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__cs,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__cc,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__mi,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__pl,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__vs,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__vc,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__hi,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__ls,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__ge,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__lt,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__gt,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc__le,
	arm_instr_store_w0_signed_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__eq,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__ne,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__cs,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__cc,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__mi,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__pl,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__vs,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__vc,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__hi,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__ls,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__ge,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__lt,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__gt,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc__le,
	arm_instr_load_w0_signed_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc__le,
	arm_instr_store_w1_unsigned_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc__le,
	arm_instr_load_w1_unsigned_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__eq,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__ne,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__cs,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__cc,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__mi,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__pl,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__vs,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__vc,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__hi,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__ls,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__ge,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__lt,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__gt,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc__le,
	arm_instr_store_w1_signed_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__eq,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__ne,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__cs,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__cc,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__mi,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__pl,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__vs,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__vc,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__hi,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__ls,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__ge,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__lt,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__gt,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc__le,
	arm_instr_load_w1_signed_halfword_u0_p0_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__eq,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__ne,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__cs,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__cc,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__mi,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__pl,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__vs,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__vc,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__hi,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__ls,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__ge,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__lt,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__gt,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc__le,
	arm_instr_store_w0_signed_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__eq,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__ne,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__cs,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__cc,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__mi,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__pl,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__vs,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__vc,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__hi,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__ls,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__ge,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__lt,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__gt,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc__le,
	arm_instr_load_w0_signed_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__eq,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__ne,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__cs,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__cc,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__mi,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__pl,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__vs,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__vc,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__hi,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__ls,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__ge,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__lt,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__gt,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc__le,
	arm_instr_store_w1_signed_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__eq,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__ne,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__cs,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__cc,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__mi,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__pl,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__vs,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__vc,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__hi,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__ls,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__ge,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__lt,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__gt,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc__le,
	arm_instr_load_w1_signed_byte_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc__le,
	arm_instr_store_w0_unsigned_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc__le,
	arm_instr_load_w0_unsigned_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__eq,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__ne,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__cs,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__cc,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__mi,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__pl,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__vs,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__vc,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__hi,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__ls,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__ge,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__lt,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__gt,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc__le,
	arm_instr_store_w0_signed_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__eq,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__ne,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__cs,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__cc,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__mi,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__pl,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__vs,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__vc,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__hi,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__ls,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__ge,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__lt,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__gt,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc__le,
	arm_instr_load_w0_signed_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc__le,
	arm_instr_store_w1_unsigned_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc__le,
	arm_instr_load_w1_unsigned_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__eq,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__ne,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__cs,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__cc,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__mi,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__pl,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__vs,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__vc,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__hi,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__ls,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__ge,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__lt,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__gt,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc__le,
	arm_instr_store_w1_signed_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__eq,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__ne,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__cs,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__cc,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__mi,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__pl,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__vs,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__vc,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__hi,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__ls,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__ge,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__lt,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__gt,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc__le,
	arm_instr_load_w1_signed_halfword_u1_p0_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__eq,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__ne,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__cs,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__cc,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__mi,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__pl,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__vs,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__vc,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__hi,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__ls,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__ge,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__lt,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__gt,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc__le,
	arm_instr_store_w0_signed_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__eq,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__ne,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__cs,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__cc,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__mi,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__pl,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__vs,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__vc,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__hi,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__ls,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__ge,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__lt,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__gt,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc__le,
	arm_instr_load_w0_signed_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__eq,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__ne,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__cs,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__cc,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__mi,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__pl,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__vs,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__vc,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__hi,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__ls,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__ge,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__lt,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__gt,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc__le,
	arm_instr_store_w1_signed_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__eq,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__ne,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__cs,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__cc,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__mi,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__pl,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__vs,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__vc,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__hi,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__ls,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__ge,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__lt,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__gt,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc__le,
	arm_instr_load_w1_signed_byte_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc__le,
	arm_instr_store_w0_unsigned_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc__le,
	arm_instr_load_w0_unsigned_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__eq,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__ne,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__cs,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__cc,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__mi,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__pl,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__vs,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__vc,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__hi,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__ls,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__ge,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__lt,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__gt,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc__le,
	arm_instr_store_w0_signed_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__eq,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__ne,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__cs,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__cc,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__mi,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__pl,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__vs,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__vc,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__hi,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__ls,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__ge,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__lt,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__gt,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc__le,
	arm_instr_load_w0_signed_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc__le,
	arm_instr_store_w1_unsigned_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc__le,
	arm_instr_load_w1_unsigned_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__eq,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__ne,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__cs,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__cc,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__mi,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__pl,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__vs,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__vc,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__hi,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__ls,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__ge,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__lt,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__gt,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc__le,
	arm_instr_store_w1_signed_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__eq,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__ne,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__cs,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__cc,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__mi,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__pl,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__vs,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__vc,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__hi,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__ls,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__ge,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__lt,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__gt,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc__le,
	arm_instr_load_w1_signed_halfword_u0_p1_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__eq,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__ne,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__cs,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__cc,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__mi,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__pl,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__vs,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__vc,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__hi,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__ls,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__ge,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__lt,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__gt,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc__le,
	arm_instr_store_w0_signed_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__eq,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__ne,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__cs,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__cc,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__mi,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__pl,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__vs,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__vc,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__hi,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__ls,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__ge,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__lt,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__gt,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc__le,
	arm_instr_load_w0_signed_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__eq,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__ne,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__cs,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__cc,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__mi,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__pl,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__vs,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__vc,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__hi,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__ls,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__ge,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__lt,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__gt,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc__le,
	arm_instr_store_w1_signed_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__eq,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__ne,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__cs,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__cc,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__mi,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__pl,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__vs,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__vc,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__hi,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__ls,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__ge,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__lt,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__gt,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc__le,
	arm_instr_load_w1_signed_byte_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc__le,
	arm_instr_store_w0_unsigned_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc__le,
	arm_instr_load_w0_unsigned_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__eq,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__ne,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__cs,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__cc,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__mi,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__pl,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__vs,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__vc,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__hi,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__ls,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__ge,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__lt,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__gt,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc__le,
	arm_instr_store_w0_signed_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__eq,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__ne,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__cs,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__cc,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__mi,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__pl,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__vs,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__vc,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__hi,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__ls,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__ge,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__lt,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__gt,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc__le,
	arm_instr_load_w0_signed_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc__le,
	arm_instr_store_w1_unsigned_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc__le,
	arm_instr_load_w1_unsigned_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__eq,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__ne,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__cs,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__cc,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__mi,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__pl,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__vs,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__vc,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__hi,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__ls,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__ge,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__lt,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__gt,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc__le,
	arm_instr_store_w1_signed_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__eq,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__ne,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__cs,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__cc,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__mi,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__pl,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__vs,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__vc,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__hi,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__ls,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__ge,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__lt,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__gt,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc__le,
	arm_instr_load_w1_signed_halfword_u1_p1_imm_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__eq,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__ne,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__cs,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__cc,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__mi,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__pl,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__vs,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__vc,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__hi,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__ls,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__ge,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__lt,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__gt,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc__le,
	arm_instr_store_w0_signed_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__eq,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__ne,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__cs,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__cc,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__mi,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__pl,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__vs,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__vc,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__hi,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__ls,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__ge,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__lt,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__gt,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc__le,
	arm_instr_load_w0_signed_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__eq,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__ne,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__cs,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__cc,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__mi,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__pl,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__vs,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__vc,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__hi,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__ls,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__ge,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__lt,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__gt,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc__le,
	arm_instr_store_w1_signed_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__eq,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__ne,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__cs,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__cc,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__mi,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__pl,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__vs,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__vc,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__hi,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__ls,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__ge,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__lt,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__gt,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc__le,
	arm_instr_load_w1_signed_byte_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc__le,
	arm_instr_store_w0_unsigned_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc__le,
	arm_instr_load_w0_unsigned_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__eq,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__ne,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__cs,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__cc,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__mi,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__pl,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__vs,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__vc,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__hi,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__ls,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__ge,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__lt,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__gt,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc__le,
	arm_instr_store_w0_signed_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__eq,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__ne,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__cs,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__cc,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__mi,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__pl,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__vs,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__vc,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__hi,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__ls,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__ge,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__lt,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__gt,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc__le,
	arm_instr_load_w0_signed_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc__le,
	arm_instr_store_w1_unsigned_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc__le,
	arm_instr_load_w1_unsigned_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__eq,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__ne,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__cs,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__cc,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__mi,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__pl,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__vs,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__vc,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__hi,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__ls,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__ge,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__lt,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__gt,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc__le,
	arm_instr_store_w1_signed_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__eq,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__ne,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__cs,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__cc,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__mi,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__pl,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__vs,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__vc,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__hi,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__ls,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__ge,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__lt,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__gt,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc__le,
	arm_instr_load_w1_signed_halfword_u0_p0_reg_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__eq,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__ne,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__cs,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__cc,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__mi,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__pl,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__vs,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__vc,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__hi,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__ls,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__ge,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__lt,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__gt,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc__le,
	arm_instr_store_w0_signed_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__eq,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__ne,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__cs,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__cc,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__mi,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__pl,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__vs,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__vc,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__hi,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__ls,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__ge,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__lt,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__gt,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc__le,
	arm_instr_load_w0_signed_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__eq,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__ne,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__cs,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__cc,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__mi,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__pl,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__vs,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__vc,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__hi,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__ls,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__ge,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__lt,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__gt,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc__le,
	arm_instr_store_w1_signed_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__eq,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__ne,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__cs,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__cc,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__mi,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__pl,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__vs,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__vc,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__hi,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__ls,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__ge,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__lt,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__gt,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc__le,
	arm_instr_load_w1_signed_byte_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc__le,
	arm_instr_store_w0_unsigned_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc__le,
	arm_instr_load_w0_unsigned_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__eq,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__ne,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__cs,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__cc,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__mi,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__pl,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__vs,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__vc,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__hi,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__ls,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__ge,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__lt,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__gt,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc__le,
	arm_instr_store_w0_signed_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__eq,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__ne,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__cs,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__cc,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__mi,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__pl,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__vs,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__vc,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__hi,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__ls,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__ge,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__lt,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__gt,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc__le,
	arm_instr_load_w0_signed_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc__le,
	arm_instr_store_w1_unsigned_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc__le,
	arm_instr_load_w1_unsigned_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__eq,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__ne,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__cs,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__cc,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__mi,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__pl,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__vs,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__vc,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__hi,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__ls,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__ge,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__lt,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__gt,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc__le,
	arm_instr_store_w1_signed_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__eq,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__ne,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__cs,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__cc,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__mi,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__pl,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__vs,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__vc,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__hi,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__ls,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__ge,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__lt,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__gt,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc__le,
	arm_instr_load_w1_signed_halfword_u1_p0_reg_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__eq,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__ne,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__cs,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__cc,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__mi,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__pl,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__vs,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__vc,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__hi,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__ls,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__ge,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__lt,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__gt,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc__le,
	arm_instr_store_w0_signed_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__eq,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__ne,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__cs,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__cc,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__mi,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__pl,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__vs,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__vc,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__hi,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__ls,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__ge,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__lt,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__gt,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc__le,
	arm_instr_load_w0_signed_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__eq,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__ne,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__cs,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__cc,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__mi,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__pl,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__vs,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__vc,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__hi,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__ls,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__ge,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__lt,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__gt,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc__le,
	arm_instr_store_w1_signed_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__eq,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__ne,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__cs,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__cc,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__mi,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__pl,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__vs,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__vc,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__hi,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__ls,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__ge,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__lt,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__gt,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc__le,
	arm_instr_load_w1_signed_byte_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc__le,
	arm_instr_store_w0_unsigned_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc__le,
	arm_instr_load_w0_unsigned_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__eq,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__ne,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__cs,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__cc,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__mi,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__pl,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__vs,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__vc,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__hi,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__ls,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__ge,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__lt,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__gt,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc__le,
	arm_instr_store_w0_signed_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__eq,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__ne,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__cs,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__cc,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__mi,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__pl,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__vs,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__vc,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__hi,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__ls,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__ge,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__lt,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__gt,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc__le,
	arm_instr_load_w0_signed_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc__le,
	arm_instr_store_w1_unsigned_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc__le,
	arm_instr_load_w1_unsigned_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__eq,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__ne,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__cs,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__cc,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__mi,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__pl,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__vs,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__vc,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__hi,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__ls,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__ge,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__lt,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__gt,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc__le,
	arm_instr_store_w1_signed_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__eq,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__ne,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__cs,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__cc,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__mi,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__pl,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__vs,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__vc,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__hi,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__ls,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__ge,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__lt,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__gt,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc__le,
	arm_instr_load_w1_signed_halfword_u0_p1_reg_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__eq,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__ne,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__cs,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__cc,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__mi,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__pl,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__vs,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__vc,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__hi,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__ls,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__ge,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__lt,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__gt,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc__le,
	arm_instr_store_w0_signed_byte_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__eq,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__ne,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__cs,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__cc,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__mi,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__pl,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__vs,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__vc,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__hi,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__ls,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__ge,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__lt,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__gt,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc__le,
	arm_instr_load_w0_signed_byte_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_invalid,
	arm_instr_nop,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__eq,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__ne,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__cs,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__cc,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__mi,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__pl,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__vs,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__vc,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__hi,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__ls,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__ge,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__lt,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__gt,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc__le,
	arm_instr_store_w1_signed_byte_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__eq,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__ne,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__cs,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__cc,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__mi,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__pl,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__vs,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__vc,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__hi,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__ls,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__ge,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__lt,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__gt,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc__le,
	arm_instr_load_w1_signed_byte_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__eq,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__ne,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__cs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__cc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__mi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__pl,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__vs,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__vc,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__hi,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__ls,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__ge,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__lt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__gt,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc__le,
	arm_instr_store_w0_unsigned_halfword_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__eq,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__ne,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__cs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__cc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__mi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__pl,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__vs,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__vc,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__hi,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__ls,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__ge,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__lt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__gt,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc__le,
	arm_instr_load_w0_unsigned_halfword_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__eq,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__ne,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__cs,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__cc,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__mi,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__pl,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__vs,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__vc,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__hi,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__ls,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__ge,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__lt,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__gt,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc__le,
	arm_instr_store_w0_signed_halfword_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__eq,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__ne,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__cs,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__cc,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__mi,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__pl,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__vs,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__vc,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__hi,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__ls,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__ge,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__lt,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__gt,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc__le,
	arm_instr_load_w0_signed_halfword_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__eq,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__ne,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__cs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__cc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__mi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__pl,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__vs,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__vc,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__hi,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__ls,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__ge,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__lt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__gt,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc__le,
	arm_instr_store_w1_unsigned_halfword_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__eq,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__ne,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__cs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__cc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__mi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__pl,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__vs,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__vc,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__hi,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__ls,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__ge,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__lt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__gt,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc__le,
	arm_instr_load_w1_unsigned_halfword_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__eq,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__ne,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__cs,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__cc,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__mi,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__pl,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__vs,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__vc,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__hi,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__ls,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__ge,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__lt,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__gt,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc__le,
	arm_instr_store_w1_signed_halfword_u1_p1_reg_pc,
	arm_instr_nop,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__eq,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__ne,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__cs,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__cc,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__mi,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__pl,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__vs,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__vc,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__hi,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__ls,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__ge,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__lt,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__gt,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc__le,
	arm_instr_load_w1_signed_halfword_u1_p1_reg_pc,
	arm_instr_nop
};

