/*
 *  DO NOT EDIT! AUTOMATICALLY GENERATED!
 */

#include <stdio.h>
#include <stdlib.h>
#include "cpu.h"
#include "misc.h"


uint32_t arm_r_r0_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[0] << 10;
}
uint32_t arm_r_r1_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[1] << 10;
}
uint32_t arm_r_r2_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[2] << 10;
}
uint32_t arm_r_r3_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[3] << 10;
}
uint32_t arm_r_r4_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[4] << 10;
}
uint32_t arm_r_r5_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[5] << 10;
}
uint32_t arm_r_r6_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[6] << 10;
}
uint32_t arm_r_r7_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[7] << 10;
}
uint32_t arm_r_r8_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[8] << 10;
}
uint32_t arm_r_r9_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[9] << 10;
}
uint32_t arm_r_r10_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[10] << 10;
}
uint32_t arm_r_r11_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[11] << 10;
}
uint32_t arm_r_r12_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[12] << 10;
}
uint32_t arm_r_r13_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[13] << 10;
}
uint32_t arm_r_r14_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[14] << 10;
}
uint32_t arm_r_r15_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
	return tmp << 10;
}
uint32_t arm_r_r0_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[0];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r1_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[1];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r2_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[2];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r3_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[3];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r4_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[4];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r5_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[5];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r6_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[6];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r7_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[7];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r8_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[8];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r9_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[9];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r10_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[10];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r11_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[11];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r12_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[12];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r13_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[13];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r14_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[14];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r15_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =tmp;
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r0_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[0] >> 10;
}
uint32_t arm_r_r1_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[1] >> 10;
}
uint32_t arm_r_r2_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[2] >> 10;
}
uint32_t arm_r_r3_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[3] >> 10;
}
uint32_t arm_r_r4_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[4] >> 10;
}
uint32_t arm_r_r5_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[5] >> 10;
}
uint32_t arm_r_r6_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[6] >> 10;
}
uint32_t arm_r_r7_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[7] >> 10;
}
uint32_t arm_r_r8_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[8] >> 10;
}
uint32_t arm_r_r9_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[9] >> 10;
}
uint32_t arm_r_r10_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[10] >> 10;
}
uint32_t arm_r_r11_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[11] >> 10;
}
uint32_t arm_r_r12_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[12] >> 10;
}
uint32_t arm_r_r13_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[13] >> 10;
}
uint32_t arm_r_r14_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[14] >> 10;
}
uint32_t arm_r_r15_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
	return tmp >> 10;
}
uint32_t arm_r_r0_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[0]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r1_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[1]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r2_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[2]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r3_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[3]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r4_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[4]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r5_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[5]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r6_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[6]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r7_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[7]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r8_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[8]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r9_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[9]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r10_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[10]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r11_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[11]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r12_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[12]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r13_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[13]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r14_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[14]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r15_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=tmp; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r0_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[0] >> 10;
}
uint32_t arm_r_r1_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[1] >> 10;
}
uint32_t arm_r_r2_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[2] >> 10;
}
uint32_t arm_r_r3_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[3] >> 10;
}
uint32_t arm_r_r4_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[4] >> 10;
}
uint32_t arm_r_r5_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[5] >> 10;
}
uint32_t arm_r_r6_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[6] >> 10;
}
uint32_t arm_r_r7_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[7] >> 10;
}
uint32_t arm_r_r8_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[8] >> 10;
}
uint32_t arm_r_r9_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[9] >> 10;
}
uint32_t arm_r_r10_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[10] >> 10;
}
uint32_t arm_r_r11_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[11] >> 10;
}
uint32_t arm_r_r12_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[12] >> 10;
}
uint32_t arm_r_r13_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[13] >> 10;
}
uint32_t arm_r_r14_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[14] >> 10;
}
uint32_t arm_r_r15_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
return (int32_t)tmp >> 10;
}
uint32_t arm_r_r0_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[0]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r1_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[1]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r2_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[2]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r3_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[3]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r4_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[4]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r5_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[5]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r6_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[6]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r7_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[7]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r8_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[8]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r9_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[9]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r10_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[10]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r11_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[11]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r12_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[12]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r13_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[13]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r14_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[14]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r15_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=tmp; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r0_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[0]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r1_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[1]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r2_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[2]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r3_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[3]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r4_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[4]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r5_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[5]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r6_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[6]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r7_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[7]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r8_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[8]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r9_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[9]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r10_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[10]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r11_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[11]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r12_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[12]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r13_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[13]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r14_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[14]; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r15_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint64_t x=tmp; x |= (x << 32); return x >> 10; }
}
uint32_t arm_r_r0_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[0]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r1_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[1]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r2_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[2]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r3_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[3]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r4_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[4]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r5_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[5]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r6_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[6]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r7_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[7]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r8_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[8]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r9_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[9]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r10_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[10]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r11_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[11]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r12_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[12]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r13_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[13]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r14_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[14]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r15_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=tmp; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r0_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[0] << 11;
}
uint32_t arm_r_r1_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[1] << 11;
}
uint32_t arm_r_r2_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[2] << 11;
}
uint32_t arm_r_r3_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[3] << 11;
}
uint32_t arm_r_r4_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[4] << 11;
}
uint32_t arm_r_r5_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[5] << 11;
}
uint32_t arm_r_r6_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[6] << 11;
}
uint32_t arm_r_r7_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[7] << 11;
}
uint32_t arm_r_r8_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[8] << 11;
}
uint32_t arm_r_r9_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[9] << 11;
}
uint32_t arm_r_r10_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[10] << 11;
}
uint32_t arm_r_r11_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[11] << 11;
}
uint32_t arm_r_r12_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[12] << 11;
}
uint32_t arm_r_r13_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[13] << 11;
}
uint32_t arm_r_r14_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[14] << 11;
}
uint32_t arm_r_r15_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
	return tmp << 11;
}
uint32_t arm_r_r0_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[0];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r1_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[1];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r2_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[2];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r3_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[3];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r4_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[4];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r5_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[5];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r6_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[6];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r7_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[7];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r8_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[8];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r9_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[9];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r10_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[10];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r11_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[11];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r12_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[12];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r13_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[13];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r14_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =cpu->cd.arm.r[14];
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r15_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t y = cpu->cd.arm.r[5] & 255;
  uint32_t x =tmp;
if (y > 31) return 0; else x <<= y;
return x; }
}
uint32_t arm_r_r0_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[0] >> 11;
}
uint32_t arm_r_r1_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[1] >> 11;
}
uint32_t arm_r_r2_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[2] >> 11;
}
uint32_t arm_r_r3_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[3] >> 11;
}
uint32_t arm_r_r4_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[4] >> 11;
}
uint32_t arm_r_r5_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[5] >> 11;
}
uint32_t arm_r_r6_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[6] >> 11;
}
uint32_t arm_r_r7_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[7] >> 11;
}
uint32_t arm_r_r8_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[8] >> 11;
}
uint32_t arm_r_r9_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[9] >> 11;
}
uint32_t arm_r_r10_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[10] >> 11;
}
uint32_t arm_r_r11_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[11] >> 11;
}
uint32_t arm_r_r12_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[12] >> 11;
}
uint32_t arm_r_r13_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[13] >> 11;
}
uint32_t arm_r_r14_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	return cpu->cd.arm.r[14] >> 11;
}
uint32_t arm_r_r15_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
	return tmp >> 11;
}
uint32_t arm_r_r0_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[0]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r1_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[1]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r2_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[2]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r3_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[3]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r4_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[4]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r5_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[5]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r6_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[6]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r7_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[7]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r8_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[8]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r9_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[9]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r10_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[10]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r11_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[11]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r12_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[12]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r13_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[13]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r14_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=cpu->cd.arm.r[14]; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r15_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t y=cpu->cd.arm.r[5]&255;
uint32_t x=tmp; if (y>=32) return 0;
return x >> y; } }
uint32_t arm_r_r0_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[0] >> 11;
}
uint32_t arm_r_r1_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[1] >> 11;
}
uint32_t arm_r_r2_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[2] >> 11;
}
uint32_t arm_r_r3_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[3] >> 11;
}
uint32_t arm_r_r4_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[4] >> 11;
}
uint32_t arm_r_r5_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[5] >> 11;
}
uint32_t arm_r_r6_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[6] >> 11;
}
uint32_t arm_r_r7_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[7] >> 11;
}
uint32_t arm_r_r8_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[8] >> 11;
}
uint32_t arm_r_r9_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[9] >> 11;
}
uint32_t arm_r_r10_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[10] >> 11;
}
uint32_t arm_r_r11_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[11] >> 11;
}
uint32_t arm_r_r12_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[12] >> 11;
}
uint32_t arm_r_r13_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[13] >> 11;
}
uint32_t arm_r_r14_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
return (int32_t)cpu->cd.arm.r[14] >> 11;
}
uint32_t arm_r_r15_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
return (int32_t)tmp >> 11;
}
uint32_t arm_r_r0_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[0]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r1_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[1]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r2_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[2]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r3_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[3]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r4_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[4]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r5_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[5]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r6_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[6]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r7_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[7]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r8_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[8]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r9_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[9]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r10_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[10]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r11_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[11]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r12_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[12]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r13_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[13]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r14_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=cpu->cd.arm.r[14]; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r15_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int32_t y=cpu->cd.arm.r[5]&255;
int32_t x=tmp; if (y>=31) return (x<0)?0xffffffff:0;
return (int32_t)x >> y; } }
uint32_t arm_r_r0_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[0]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r1_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[1]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r2_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[2]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r3_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[3]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r4_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[4]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r5_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[5]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r6_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[6]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r7_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[7]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r8_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[8]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r9_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[9]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r10_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[10]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r11_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[11]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r12_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[12]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r13_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[13]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r14_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x=cpu->cd.arm.r[14]; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r15_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint64_t x=tmp; x |= (x << 32); return x >> 11; }
}
uint32_t arm_r_r0_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[0]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r1_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[1]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r2_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[2]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r3_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[3]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r4_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[4]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r5_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[5]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r6_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[6]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r7_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[7]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r8_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[8]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r9_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[9]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r10_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[10]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r11_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[11]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r12_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[12]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r13_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[13]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r14_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=cpu->cd.arm.r[14]; x |= (x << 32); return (x >> y); } }
uint32_t arm_r_r15_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int y=cpu->cd.arm.r[5]&31;
uint64_t x=tmp; x |= (x << 32); return (x >> y); } }
uint32_t arm_rs_r0_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r1_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r2_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r3_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r4_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r5_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r6_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r7_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r8_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r9_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r10_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r11_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r12_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r13_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r14_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r15_t0_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 10;
 return x; }
}
uint32_t arm_rs_r0_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r1_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r2_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r3_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r4_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r5_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r6_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r7_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r8_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r9_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r10_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r11_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r12_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r13_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r14_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r15_t1_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp;
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r0_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r1_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r2_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r3_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r4_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r5_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r6_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r7_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r8_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r9_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r10_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r11_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r12_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r13_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r14_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r15_t2_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r0_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r1_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r2_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r3_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r4_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r5_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r6_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r7_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r8_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r9_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r10_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r11_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r12_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r13_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r14_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r15_t3_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp,y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r0_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[0];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r1_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[1];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r2_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[2];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r3_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[3];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r4_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[4];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r5_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[5];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r6_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[6];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r7_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[7];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r8_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[8];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r9_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[9];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r10_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[10];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r11_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[11];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r12_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[12];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r13_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[13];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r14_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[14];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r15_t4_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int32_t x = tmp;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 10;
 return x; }
}
uint32_t arm_rs_r0_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[0],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r1_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[1],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r2_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[2],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r3_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[3],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r4_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[4],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r5_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[5],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r6_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[6],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r7_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[7],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r8_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[8],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r9_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[9],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r10_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[10],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r11_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[11],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r12_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[12],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r13_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[13],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r14_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[14],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r15_t5_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int32_t x = tmp,y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r0_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[0]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r1_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[1]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r2_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[2]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r3_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[3]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r4_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[4]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r5_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[5]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r6_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[6]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r7_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[7]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r8_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[8]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r9_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[9]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r10_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[10]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r11_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[11]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r12_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[12]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r13_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[13]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r14_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[14]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r15_t6_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint64_t x = tmp; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 10; }
}
uint32_t arm_rs_r0_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[0]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r1_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[1]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r2_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[2]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r3_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[3]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r4_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[4]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r5_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[5]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r6_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[6]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r7_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[7]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r8_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[8]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r9_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[9]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r10_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[10]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r11_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[11]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r12_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[12]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r13_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[13]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r14_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[14]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r15_t7_c10(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint64_t x = tmp; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r0_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r1_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r2_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r3_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r4_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r5_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r6_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r7_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r8_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r9_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r10_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r11_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r12_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r13_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r14_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r15_t0_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x200000)
	cpu->cd.arm.flags |= ARM_F_C;
x <<= 11;
 return x; }
}
uint32_t arm_rs_r0_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r1_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r2_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r3_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r4_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r5_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r6_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r7_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r8_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r9_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r10_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r11_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r12_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r13_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r14_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14];
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r15_t1_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp;
  uint32_t y = cpu->cd.arm.r[5] & 255;
  if (y != 0) {
    cpu->cd.arm.flags &= ~ARM_F_C;
    if (y >= 32) return 0;
    x <<= (y - 1);
    if (x & 0x80000000)
	cpu->cd.arm.flags |= ARM_F_C;
    x <<= 1;
 }
 return x; }
}
uint32_t arm_rs_r0_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r1_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r2_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r3_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r4_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r5_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r6_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r7_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r8_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r9_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r10_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r11_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r12_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r13_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r14_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r15_t2_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r0_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[0],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r1_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[1],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r2_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[2],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r3_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[3],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r4_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[4],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r5_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[5],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r6_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[6],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r7_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[7],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r8_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[8],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r9_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[9],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r10_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[10],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r11_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[11],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r12_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[12],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r13_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[13],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r14_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint32_t x = cpu->cd.arm.r[14],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r15_t3_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint32_t x = tmp,y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=32;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r0_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[0];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r1_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[1];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r2_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[2];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r3_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[3];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r4_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[4];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r5_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[5];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r6_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[6];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r7_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[7];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r8_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[8];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r9_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[9];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r10_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[10];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r11_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[11];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r12_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[12];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r13_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[13];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r14_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[14];
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r15_t4_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int32_t x = tmp;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
x >>= 11;
 return x; }
}
uint32_t arm_rs_r0_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[0],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r1_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[1],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r2_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[2],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r3_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[3],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r4_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[4],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r5_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[5],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r6_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[6],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r7_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[7],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r8_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[8],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r9_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[9],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r10_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[10],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r11_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[11],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r12_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[12],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r13_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[13],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r14_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ int32_t x = cpu->cd.arm.r[14],y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r15_t5_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ int32_t x = tmp,y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
cpu->cd.arm.flags &= ~ARM_F_C;
if(y>31) y=31;
y--; x >>= y;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return (int32_t)x >> 1; }
}
uint32_t arm_rs_r0_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[0]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r1_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[1]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r2_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[2]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r3_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[3]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r4_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[4]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r5_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[5]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r6_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[6]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r7_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[7]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r8_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[8]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r9_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[9]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r10_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[10]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r11_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[11]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r12_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[12]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r13_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[13]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r14_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[14]; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r15_t6_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint64_t x = tmp; x |= (x << 32);
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 0x400)
	cpu->cd.arm.flags |= ARM_F_C;
 return x >> 11; }
}
uint32_t arm_rs_r0_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[0]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r1_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[1]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r2_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[2]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r3_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[3]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r4_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[4]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r5_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[5]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r6_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[6]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r7_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[7]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r8_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[8]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r9_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[9]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r10_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[10]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r11_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[11]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r12_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[12]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r13_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[13]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r14_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
{ uint64_t x = cpu->cd.arm.r[14]; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
uint32_t arm_rs_r15_t7_c11(struct cpu *cpu, struct arm_instr_call *ic) {
	uint32_t tmp, low_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page)/sizeof(struct arm_instr_call);
	tmp = cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1) <<
	    ARM_INSTR_ALIGNMENT_SHIFT);
	tmp += (low_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 8;
{ uint64_t x = tmp; int y=cpu->cd.arm.r[5]&255;
if(y==0) return x;
y --; y &= 31; x >>= y;
cpu->cd.arm.flags &= ~ARM_F_C;
if (x & 1) cpu->cd.arm.flags |= ARM_F_C;
 return x >> 1; }
}
