
/*  AUTOMATICALLY GENERATED! Do not edit.  */

#include <stdio.h>
#include <stdlib.h>
#include "cpu.h"
#include "misc.h"
#define DYNTRANS_PC_TO_POINTERS arm_pc_to_pointers
#include "quick_pc_to_pointers.h"
#include "arm_tmphead_1.h"

#define instr(x) arm_instr_ ## x
extern void arm_pc_to_pointers(struct cpu *);
extern void arm_instr_nop(struct cpu *, struct arm_instr_call *);
extern void arm_instr_bdt_load(struct cpu *, struct arm_instr_call *);
extern void arm_instr_bdt_store(struct cpu *, struct arm_instr_call *);



void arm_instr_multi_0x092ddff0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x28 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-10] = cpu->cd.arm.r[4];
		p[-9] = cpu->cd.arm.r[5];
		p[-8] = cpu->cd.arm.r[6];
		p[-7] = cpu->cd.arm.r[7];
		p[-6] = cpu->cd.arm.r[8];
		p[-5] = cpu->cd.arm.r[9];
		p[-4] = cpu->cd.arm.r[10];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 44;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092ddff0)

void arm_instr_multi_0x091baff0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x24 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-9];
		cpu->cd.arm.r[5] = p[-8];
		cpu->cd.arm.r[6] = p[-7];
		cpu->cd.arm.r[7] = p[-6];
		cpu->cd.arm.r[8] = p[-5];
		cpu->cd.arm.r[9] = p[-4];
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091baff0)

void arm_instr_multi_0x08110003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[-1];
		cpu->cd.arm.r[1] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08110003)

void arm_instr_multi_0x092dd8f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x1c && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-7] = cpu->cd.arm.r[4];
		p[-6] = cpu->cd.arm.r[5];
		p[-5] = cpu->cd.arm.r[6];
		p[-4] = cpu->cd.arm.r[7];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 32;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092dd8f0)

void arm_instr_multi_0x091ba8f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x18 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-6];
		cpu->cd.arm.r[5] = p[-5];
		cpu->cd.arm.r[6] = p[-4];
		cpu->cd.arm.r[7] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091ba8f0)

void arm_instr_multi_0x092d4000(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 4;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d4000)

void arm_instr_multi_0x08bd8000(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->pc = p[0];
		cpu->cd.arm.r[13] += 4;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd8000)

void arm_instr_multi_0x08ac000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[2];
		p[1] = cpu->cd.arm.r[3];
		cpu->cd.arm.r[12] += 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08ac000c)

void arm_instr_multi_0x092dd830(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x14 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-5] = cpu->cd.arm.r[4];
		p[-4] = cpu->cd.arm.r[5];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 24;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092dd830)

void arm_instr_multi_0x092dddf0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x24 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-9] = cpu->cd.arm.r[4];
		p[-8] = cpu->cd.arm.r[5];
		p[-7] = cpu->cd.arm.r[6];
		p[-6] = cpu->cd.arm.r[7];
		p[-5] = cpu->cd.arm.r[8];
		p[-4] = cpu->cd.arm.r[10];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 40;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092dddf0)

void arm_instr_multi_0x092dd9f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x20 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-8] = cpu->cd.arm.r[4];
		p[-7] = cpu->cd.arm.r[5];
		p[-6] = cpu->cd.arm.r[6];
		p[-5] = cpu->cd.arm.r[7];
		p[-4] = cpu->cd.arm.r[8];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 36;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092dd9f0)

void arm_instr_multi_0x091badf0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x20 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-8];
		cpu->cd.arm.r[5] = p[-7];
		cpu->cd.arm.r[6] = p[-6];
		cpu->cd.arm.r[7] = p[-5];
		cpu->cd.arm.r[8] = p[-4];
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091badf0)

void arm_instr_multi_0x091ba830(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x10 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-4];
		cpu->cd.arm.r[5] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091ba830)

void arm_instr_multi_0x091ba9f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x1c && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-7];
		cpu->cd.arm.r[5] = p[-6];
		cpu->cd.arm.r[6] = p[-5];
		cpu->cd.arm.r[7] = p[-4];
		cpu->cd.arm.r[8] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091ba9f0)

void arm_instr_multi_0x08930003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08930003)

void arm_instr_multi_0x09040003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[0];
		p[0] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09040003)

void arm_instr_multi_0x08b051f8(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
		cpu->cd.arm.r[5] = p[2];
		cpu->cd.arm.r[6] = p[3];
		cpu->cd.arm.r[7] = p[4];
		cpu->cd.arm.r[8] = p[5];
		cpu->cd.arm.r[12] = p[6];
		cpu->cd.arm.r[14] = p[7];
		cpu->cd.arm.r[0] += 32;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08b051f8)

void arm_instr_multi_0x08a151f8(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
		p[2] = cpu->cd.arm.r[5];
		p[3] = cpu->cd.arm.r[6];
		p[4] = cpu->cd.arm.r[7];
		p[5] = cpu->cd.arm.r[8];
		p[6] = cpu->cd.arm.r[12];
		p[7] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[1] += 32;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a151f8)

void arm_instr_multi_0x092dd810(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x10 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-4] = cpu->cd.arm.r[4];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 20;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092dd810)

void arm_instr_multi_0x091ba810(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091ba810)

void arm_instr_multi_0x08930006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08930006)

void arm_instr_multi_0x092d4010(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[4];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d4010)

void arm_instr_multi_0x092dd800(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092dd800)

void arm_instr_multi_0x08830006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08830006)

void arm_instr_multi_0x08920018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08920018)

void arm_instr_multi_0x08a051f8(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
		p[2] = cpu->cd.arm.r[5];
		p[3] = cpu->cd.arm.r[6];
		p[4] = cpu->cd.arm.r[7];
		p[5] = cpu->cd.arm.r[8];
		p[6] = cpu->cd.arm.r[12];
		p[7] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[0] += 32;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a051f8)

void arm_instr_multi_0x08820018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08820018)

void arm_instr_multi_0x08bd8010(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->pc = p[1];
		cpu->cd.arm.r[13] += 8;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd8010)

void arm_instr_multi_0x08a05018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
		p[2] = cpu->cd.arm.r[12];
		p[3] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[0] += 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a05018)

void arm_instr_multi_0x08b15018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
		cpu->cd.arm.r[12] = p[2];
		cpu->cd.arm.r[14] = p[3];
		cpu->cd.arm.r[1] += 16;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08b15018)

void arm_instr_multi_0x092dd870(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x18 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-6] = cpu->cd.arm.r[4];
		p[-5] = cpu->cd.arm.r[5];
		p[-4] = cpu->cd.arm.r[6];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 28;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092dd870)

void arm_instr_multi_0x091ba870(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x14 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-5];
		cpu->cd.arm.r[5] = p[-4];
		cpu->cd.arm.r[6] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091ba870)

void arm_instr_multi_0x092d41f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x14 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-5] = cpu->cd.arm.r[4];
		p[-4] = cpu->cd.arm.r[5];
		p[-3] = cpu->cd.arm.r[6];
		p[-2] = cpu->cd.arm.r[7];
		p[-1] = cpu->cd.arm.r[8];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 24;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d41f0)

void arm_instr_multi_0x08bd81f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->cd.arm.r[8] = p[4];
		cpu->pc = p[5];
		cpu->cd.arm.r[13] += 24;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd81f0)

void arm_instr_multi_0x08971040(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[6] = p[0];
		cpu->cd.arm.r[12] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08971040)

void arm_instr_multi_0x08040006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[1];
		p[0] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08040006)

void arm_instr_multi_0x08130018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[-1];
		cpu->cd.arm.r[4] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08130018)

void arm_instr_multi_0x091ba800(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091ba800)

void arm_instr_multi_0x088d1fff(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfcc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
		p[2] = cpu->cd.arm.r[2];
		p[3] = cpu->cd.arm.r[3];
		p[4] = cpu->cd.arm.r[4];
		p[5] = cpu->cd.arm.r[5];
		p[6] = cpu->cd.arm.r[6];
		p[7] = cpu->cd.arm.r[7];
		p[8] = cpu->cd.arm.r[8];
		p[9] = cpu->cd.arm.r[9];
		p[10] = cpu->cd.arm.r[10];
		p[11] = cpu->cd.arm.r[11];
		p[12] = cpu->cd.arm.r[12];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d1fff)

void arm_instr_multi_0x091b6800(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b6800)

void arm_instr_multi_0x08950006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08950006)

void arm_instr_multi_0x0911000f(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[-3];
		cpu->cd.arm.r[1] = p[-2];
		cpu->cd.arm.r[2] = p[-1];
		cpu->cd.arm.r[3] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0911000f)

void arm_instr_multi_0x090d000f(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-3] = cpu->cd.arm.r[0];
		p[-2] = cpu->cd.arm.r[1];
		p[-1] = cpu->cd.arm.r[2];
		p[0] = cpu->cd.arm.r[3];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x090d000f)

void arm_instr_multi_0x08850006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08850006)

void arm_instr_multi_0x092d4070(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-3] = cpu->cd.arm.r[4];
		p[-2] = cpu->cd.arm.r[5];
		p[-1] = cpu->cd.arm.r[6];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d4070)

void arm_instr_multi_0x08bd8070(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->pc = p[3];
		cpu->cd.arm.r[13] += 16;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd8070)

void arm_instr_multi_0x08900006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08900006)

void arm_instr_multi_0x08800006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08800006)

void arm_instr_multi_0x089e0018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089e0018)

void arm_instr_multi_0x08870006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08870006)

void arm_instr_multi_0x088e0018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088e0018)

void arm_instr_multi_0x08b00fc0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[6] = p[0];
		cpu->cd.arm.r[7] = p[1];
		cpu->cd.arm.r[8] = p[2];
		cpu->cd.arm.r[9] = p[3];
		cpu->cd.arm.r[10] = p[4];
		cpu->cd.arm.r[11] = p[5];
		cpu->cd.arm.r[0] += 24;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08b00fc0)

void arm_instr_multi_0x08b000c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[6] = p[0];
		cpu->cd.arm.r[7] = p[1];
		cpu->cd.arm.r[0] += 8;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08b000c0)

void arm_instr_multi_0x08970006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08970006)

void arm_instr_multi_0x08930060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[0];
		cpu->cd.arm.r[6] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08930060)

void arm_instr_multi_0x091b6ff0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x24 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-9];
		cpu->cd.arm.r[5] = p[-8];
		cpu->cd.arm.r[6] = p[-7];
		cpu->cd.arm.r[7] = p[-6];
		cpu->cd.arm.r[8] = p[-5];
		cpu->cd.arm.r[9] = p[-4];
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b6ff0)

void arm_instr_multi_0x092d4030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-2] = cpu->cd.arm.r[4];
		p[-1] = cpu->cd.arm.r[5];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 12;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d4030)

void arm_instr_multi_0x08bd8030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->pc = p[2];
		cpu->cd.arm.r[13] += 12;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd8030)

void arm_instr_multi_0x091b6830(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x10 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-4];
		cpu->cd.arm.r[5] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b6830)

void arm_instr_multi_0x092ddc30(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x18 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-6] = cpu->cd.arm.r[4];
		p[-5] = cpu->cd.arm.r[5];
		p[-4] = cpu->cd.arm.r[10];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 28;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092ddc30)

void arm_instr_multi_0x091bac30(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x14 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-5];
		cpu->cd.arm.r[5] = p[-4];
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091bac30)

void arm_instr_multi_0x092d4001(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[0];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d4001)

void arm_instr_multi_0x08bd8001(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->pc = p[1];
		cpu->cd.arm.r[13] += 8;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd8001)

void arm_instr_multi_0x09205018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-3] = cpu->cd.arm.r[3];
		p[-2] = cpu->cd.arm.r[4];
		p[-1] = cpu->cd.arm.r[12];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[0] -= 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09205018)

void arm_instr_multi_0x09315018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[-3];
		cpu->cd.arm.r[4] = p[-2];
		cpu->cd.arm.r[12] = p[-1];
		cpu->cd.arm.r[14] = p[0];
		cpu->cd.arm.r[1] -= 16;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09315018)

void arm_instr_multi_0x092ddbf0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x24 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-9] = cpu->cd.arm.r[4];
		p[-8] = cpu->cd.arm.r[5];
		p[-7] = cpu->cd.arm.r[6];
		p[-6] = cpu->cd.arm.r[7];
		p[-5] = cpu->cd.arm.r[8];
		p[-4] = cpu->cd.arm.r[9];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 40;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092ddbf0)

void arm_instr_multi_0x091babf0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x20 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-8];
		cpu->cd.arm.r[5] = p[-7];
		cpu->cd.arm.r[6] = p[-6];
		cpu->cd.arm.r[7] = p[-5];
		cpu->cd.arm.r[8] = p[-4];
		cpu->cd.arm.r[9] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091babf0)

void arm_instr_multi_0x091bac70(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x18 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-6];
		cpu->cd.arm.r[5] = p[-5];
		cpu->cd.arm.r[6] = p[-4];
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091bac70)

void arm_instr_multi_0x092ddc70(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x1c && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-7] = cpu->cd.arm.r[4];
		p[-6] = cpu->cd.arm.r[5];
		p[-5] = cpu->cd.arm.r[6];
		p[-4] = cpu->cd.arm.r[10];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 32;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092ddc70)

void arm_instr_multi_0x080c0030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[4];
		p[0] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x080c0030)

void arm_instr_multi_0x092ddcf0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x20 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-8] = cpu->cd.arm.r[4];
		p[-7] = cpu->cd.arm.r[5];
		p[-6] = cpu->cd.arm.r[6];
		p[-5] = cpu->cd.arm.r[7];
		p[-4] = cpu->cd.arm.r[10];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 36;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092ddcf0)

void arm_instr_multi_0x091bacf0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x1c && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-7];
		cpu->cd.arm.r[5] = p[-6];
		cpu->cd.arm.r[6] = p[-5];
		cpu->cd.arm.r[7] = p[-4];
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091bacf0)

void arm_instr_multi_0x0892000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[2] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0892000c)

void arm_instr_multi_0x08930180(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[7] = p[0];
		cpu->cd.arm.r[8] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08930180)

void arm_instr_multi_0x08150003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[-1];
		cpu->cd.arm.r[1] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08150003)

void arm_instr_multi_0x08020003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[0];
		p[0] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08020003)

void arm_instr_multi_0x08920006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08920006)

void arm_instr_multi_0x0817000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[2] = p[-1];
		cpu->cd.arm.r[3] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0817000c)

void arm_instr_multi_0x09870018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09870018)

void arm_instr_multi_0x099c0180(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[7] = p[0];
		cpu->cd.arm.r[8] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x099c0180)

void arm_instr_multi_0x091b69f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x1c && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-7];
		cpu->cd.arm.r[5] = p[-6];
		cpu->cd.arm.r[6] = p[-5];
		cpu->cd.arm.r[7] = p[-4];
		cpu->cd.arm.r[8] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b69f0)

void arm_instr_multi_0x08950003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08950003)

void arm_instr_multi_0x088c0060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[5];
		p[1] = cpu->cd.arm.r[6];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088c0060)

void arm_instr_multi_0x0891000e(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
		cpu->cd.arm.r[3] = p[2];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0891000e)

void arm_instr_multi_0x08bd0400(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[10] = p[0];
		cpu->cd.arm.r[13] += 4;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd0400)

void arm_instr_multi_0x092d0030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[4];
		p[0] = cpu->cd.arm.r[5];
		cpu->cd.arm.r[13] -= 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d0030)

void arm_instr_multi_0x08bd0030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[13] += 8;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd0030)

void arm_instr_multi_0x08810018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08810018)

void arm_instr_multi_0x08880018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[8];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08880018)

void arm_instr_multi_0x08820003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08820003)

void arm_instr_multi_0x08980060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[8];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[0];
		cpu->cd.arm.r[6] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08980060)

void arm_instr_multi_0x08bd0010(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[13] += 4;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd0010)

void arm_instr_multi_0x092d0010(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		cpu->cd.arm.r[13] -= 4;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d0010)

void arm_instr_multi_0x08bd4010(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[14] = p[1];
		cpu->cd.arm.r[13] += 8;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd4010)

void arm_instr_multi_0x08100009(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[-1];
		cpu->cd.arm.r[3] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08100009)

void arm_instr_multi_0x08910003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08910003)

void arm_instr_multi_0x08830030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08830030)

void arm_instr_multi_0x08980018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[8];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08980018)

void arm_instr_multi_0x08930018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08930018)

void arm_instr_multi_0x08880006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[8];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08880006)

void arm_instr_multi_0x088c0018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088c0018)

void arm_instr_multi_0x08910006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08910006)

void arm_instr_multi_0x08940003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08940003)

void arm_instr_multi_0x08850003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08850003)

void arm_instr_multi_0x08890006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08890006)

void arm_instr_multi_0x092d40f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x10 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-4] = cpu->cd.arm.r[4];
		p[-3] = cpu->cd.arm.r[5];
		p[-2] = cpu->cd.arm.r[6];
		p[-1] = cpu->cd.arm.r[7];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 20;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d40f0)

void arm_instr_multi_0x08840003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08840003)

void arm_instr_multi_0x08820030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08820030)

void arm_instr_multi_0x09160060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[-1];
		cpu->cd.arm.r[6] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09160060)

void arm_instr_multi_0x08930600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[9] = p[0];
		cpu->cd.arm.r[10] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08930600)

void arm_instr_multi_0x092d0ff0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x1c && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-7] = cpu->cd.arm.r[4];
		p[-6] = cpu->cd.arm.r[5];
		p[-5] = cpu->cd.arm.r[6];
		p[-4] = cpu->cd.arm.r[7];
		p[-3] = cpu->cd.arm.r[8];
		p[-2] = cpu->cd.arm.r[9];
		p[-1] = cpu->cd.arm.r[10];
		p[0] = cpu->cd.arm.r[11];
		cpu->cd.arm.r[13] -= 32;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d0ff0)

void arm_instr_multi_0x08bd0ff0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->cd.arm.r[8] = p[4];
		cpu->cd.arm.r[9] = p[5];
		cpu->cd.arm.r[10] = p[6];
		cpu->cd.arm.r[11] = p[7];
		cpu->cd.arm.r[13] += 32;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd0ff0)

void arm_instr_multi_0x089e000a(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089e000a)

void arm_instr_multi_0x09930006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09930006)

void arm_instr_multi_0x080c0003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[0];
		p[0] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x080c0003)

void arm_instr_multi_0x0804000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[2];
		p[0] = cpu->cd.arm.r[3];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x0804000c)

void arm_instr_multi_0x08830060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[5];
		p[1] = cpu->cd.arm.r[6];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08830060)

void arm_instr_multi_0x08130003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[-1];
		cpu->cd.arm.r[1] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08130003)

void arm_instr_multi_0x09830006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09830006)

void arm_instr_multi_0x08b00300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[8] = p[0];
		cpu->cd.arm.r[9] = p[1];
		cpu->cd.arm.r[0] += 8;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08b00300)

void arm_instr_multi_0x088e1002(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[12];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088e1002)

void arm_instr_multi_0x0894000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[2] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0894000c)

void arm_instr_multi_0x0885000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[2];
		p[1] = cpu->cd.arm.r[3];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x0885000c)

void arm_instr_multi_0x08840600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[9];
		p[1] = cpu->cd.arm.r[10];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08840600)

void arm_instr_multi_0x091b6df0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x20 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-8];
		cpu->cd.arm.r[5] = p[-7];
		cpu->cd.arm.r[6] = p[-6];
		cpu->cd.arm.r[7] = p[-5];
		cpu->cd.arm.r[8] = p[-4];
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b6df0)

void arm_instr_multi_0x088c0006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088c0006)

void arm_instr_multi_0x092d47f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x1c && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-7] = cpu->cd.arm.r[4];
		p[-6] = cpu->cd.arm.r[5];
		p[-5] = cpu->cd.arm.r[6];
		p[-4] = cpu->cd.arm.r[7];
		p[-3] = cpu->cd.arm.r[8];
		p[-2] = cpu->cd.arm.r[9];
		p[-1] = cpu->cd.arm.r[10];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 32;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d47f0)

void arm_instr_multi_0x08bd87f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->cd.arm.r[8] = p[4];
		cpu->cd.arm.r[9] = p[5];
		cpu->cd.arm.r[10] = p[6];
		cpu->pc = p[7];
		cpu->cd.arm.r[13] += 32;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd87f0)

void arm_instr_multi_0x08800018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08800018)

void arm_instr_multi_0x099b0030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x099b0030)

void arm_instr_multi_0x08a100c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[6];
		p[1] = cpu->cd.arm.r[7];
		cpu->cd.arm.r[1] += 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a100c0)

void arm_instr_multi_0x089c0006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089c0006)

void arm_instr_multi_0x099b0180(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[7] = p[0];
		cpu->cd.arm.r[8] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x099b0180)

void arm_instr_multi_0x08910030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08910030)

void arm_instr_multi_0x09150018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[-1];
		cpu->cd.arm.r[4] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09150018)

void arm_instr_multi_0x091a0600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[10];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[9] = p[-1];
		cpu->cd.arm.r[10] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091a0600)

void arm_instr_multi_0x090a0300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[10];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[8];
		p[0] = cpu->cd.arm.r[9];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x090a0300)

void arm_instr_multi_0x08bd40f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfec && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->cd.arm.r[14] = p[4];
		cpu->cd.arm.r[13] += 20;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd40f0)

void arm_instr_multi_0x089c0300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[8] = p[0];
		cpu->cd.arm.r[9] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089c0300)

void arm_instr_multi_0x09150006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[-1];
		cpu->cd.arm.r[2] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09150006)

void arm_instr_multi_0x08a10300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[8];
		p[1] = cpu->cd.arm.r[9];
		cpu->cd.arm.r[1] += 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a10300)

void arm_instr_multi_0x08a01008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[12];
		cpu->cd.arm.r[0] += 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a01008)

void arm_instr_multi_0x08b11008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[12] = p[1];
		cpu->cd.arm.r[1] += 8;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08b11008)

void arm_instr_multi_0x08bd80f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfec && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->pc = p[4];
		cpu->cd.arm.r[13] += 20;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd80f0)

void arm_instr_multi_0x08a05008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[12];
		p[2] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[0] += 12;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a05008)

void arm_instr_multi_0x08b15008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[12] = p[1];
		cpu->cd.arm.r[14] = p[2];
		cpu->cd.arm.r[1] += 12;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08b15008)

void arm_instr_multi_0x08900018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08900018)

void arm_instr_multi_0x092ddc00(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	uint32_t tmp_pc = ((size_t)ic - (size_t)
	    cpu->cd.arm.cur_ic_page) / sizeof(struct arm_instr_call);
	tmp_pc = ((cpu->pc & ~((ARM_IC_ENTRIES_PER_PAGE-1)
	    << ARM_INSTR_ALIGNMENT_SHIFT)))
	    + (tmp_pc << ARM_INSTR_ALIGNMENT_SHIFT) + 12;
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x10 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-4] = cpu->cd.arm.r[10];
		p[-3] = cpu->cd.arm.r[11];
		p[-2] = cpu->cd.arm.r[12];
		p[-1] = cpu->cd.arm.r[14];
		p[0] = tmp_pc;
		cpu->cd.arm.r[13] -= 20;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092ddc00)

void arm_instr_multi_0x088c0003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088c0003)

void arm_instr_multi_0x08830600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[9];
		p[1] = cpu->cd.arm.r[10];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08830600)

void arm_instr_multi_0x08920003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08920003)

void arm_instr_multi_0x088d1100(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[8];
		p[1] = cpu->cd.arm.r[12];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d1100)

void arm_instr_multi_0x09900120(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[0];
		cpu->cd.arm.r[8] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09900120)

void arm_instr_multi_0x091bac00(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[10] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->pc = p[0];
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091bac00)

void arm_instr_multi_0x092d45f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x18 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-6] = cpu->cd.arm.r[4];
		p[-5] = cpu->cd.arm.r[5];
		p[-4] = cpu->cd.arm.r[6];
		p[-3] = cpu->cd.arm.r[7];
		p[-2] = cpu->cd.arm.r[8];
		p[-1] = cpu->cd.arm.r[10];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 28;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d45f0)

void arm_instr_multi_0x08bd85f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->cd.arm.r[8] = p[4];
		cpu->cd.arm.r[10] = p[5];
		cpu->pc = p[6];
		cpu->cd.arm.r[13] += 28;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd85f0)

void arm_instr_multi_0x09940018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09940018)

void arm_instr_multi_0x09850014(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[2];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09850014)

void arm_instr_multi_0x08860006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08860006)

void arm_instr_multi_0x09120006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[-1];
		cpu->cd.arm.r[2] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09120006)

void arm_instr_multi_0x089c0018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089c0018)

void arm_instr_multi_0x091b6870(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x14 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-5];
		cpu->cd.arm.r[5] = p[-4];
		cpu->cd.arm.r[6] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b6870)

void arm_instr_multi_0x08950030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08950030)

void arm_instr_multi_0x09900018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09900018)

void arm_instr_multi_0x098d0030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x098d0030)

void arm_instr_multi_0x088d0088(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[7];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d0088)

void arm_instr_multi_0x08900060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[0];
		cpu->cd.arm.r[6] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08900060)

void arm_instr_multi_0x08900003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08900003)

void arm_instr_multi_0x08990018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08990018)

void arm_instr_multi_0x08810600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[9];
		p[1] = cpu->cd.arm.r[10];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08810600)

void arm_instr_multi_0x092d0c1f(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x18 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-6] = cpu->cd.arm.r[0];
		p[-5] = cpu->cd.arm.r[1];
		p[-4] = cpu->cd.arm.r[2];
		p[-3] = cpu->cd.arm.r[3];
		p[-2] = cpu->cd.arm.r[4];
		p[-1] = cpu->cd.arm.r[10];
		p[0] = cpu->cd.arm.r[11];
		cpu->cd.arm.r[13] -= 28;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d0c1f)

void arm_instr_multi_0x08bd4c1f(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
		cpu->cd.arm.r[2] = p[2];
		cpu->cd.arm.r[3] = p[3];
		cpu->cd.arm.r[4] = p[4];
		cpu->cd.arm.r[10] = p[5];
		cpu->cd.arm.r[11] = p[6];
		cpu->cd.arm.r[14] = p[7];
		cpu->cd.arm.r[13] += 32;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd4c1f)

void arm_instr_multi_0x088d1010(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[12];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d1010)

void arm_instr_multi_0x09311008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[-1];
		cpu->cd.arm.r[12] = p[0];
		cpu->cd.arm.r[1] -= 8;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09311008)

void arm_instr_multi_0x09201008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[3];
		p[0] = cpu->cd.arm.r[12];
		cpu->cd.arm.r[0] -= 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09201008)

void arm_instr_multi_0x08a10f00(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[8];
		p[1] = cpu->cd.arm.r[9];
		p[2] = cpu->cd.arm.r[10];
		p[3] = cpu->cd.arm.r[11];
		cpu->cd.arm.r[1] += 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a10f00)

void arm_instr_multi_0x08931008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[12] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08931008)

void arm_instr_multi_0x098b0003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x098b0003)

void arm_instr_multi_0x08820180(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[7];
		p[1] = cpu->cd.arm.r[8];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08820180)

void arm_instr_multi_0x08830300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[8];
		p[1] = cpu->cd.arm.r[9];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08830300)

void arm_instr_multi_0x08800030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08800030)

void arm_instr_multi_0x09315008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[-2];
		cpu->cd.arm.r[12] = p[-1];
		cpu->cd.arm.r[14] = p[0];
		cpu->cd.arm.r[1] -= 12;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09315008)

void arm_instr_multi_0x09205008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-2] = cpu->cd.arm.r[3];
		p[-1] = cpu->cd.arm.r[12];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[0] -= 12;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09205008)

void arm_instr_multi_0x08970300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[8] = p[0];
		cpu->cd.arm.r[9] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08970300)

void arm_instr_multi_0x08970030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08970030)

void arm_instr_multi_0x08920030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08920030)

void arm_instr_multi_0x08970600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[9] = p[0];
		cpu->cd.arm.r[10] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08970600)

void arm_instr_multi_0x08160060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[-1];
		cpu->cd.arm.r[6] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08160060)

void arm_instr_multi_0x08807ff0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfd4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
		p[2] = cpu->cd.arm.r[6];
		p[3] = cpu->cd.arm.r[7];
		p[4] = cpu->cd.arm.r[8];
		p[5] = cpu->cd.arm.r[9];
		p[6] = cpu->cd.arm.r[10];
		p[7] = cpu->cd.arm.r[11];
		p[8] = cpu->cd.arm.r[12];
		p[9] = cpu->cd.arm.r[13];
		p[10] = cpu->cd.arm.r[14];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08807ff0)

void arm_instr_multi_0x092d0070(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-2] = cpu->cd.arm.r[4];
		p[-1] = cpu->cd.arm.r[5];
		p[0] = cpu->cd.arm.r[6];
		cpu->cd.arm.r[13] -= 12;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d0070)

void arm_instr_multi_0x08bd0070(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[13] += 12;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd0070)

void arm_instr_multi_0x08800180(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[7];
		p[1] = cpu->cd.arm.r[8];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08800180)

void arm_instr_multi_0x088e000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[2];
		p[1] = cpu->cd.arm.r[3];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088e000c)

void arm_instr_multi_0x088d0030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d0030)

void arm_instr_multi_0x08830003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08830003)

void arm_instr_multi_0x089e0030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089e0030)

void arm_instr_multi_0x091b6810(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b6810)

void arm_instr_multi_0x08970180(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[7];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[7] = p[0];
		cpu->cd.arm.r[8] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08970180)

void arm_instr_multi_0x0896000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[2] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0896000c)

void arm_instr_multi_0x089200c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[6] = p[0];
		cpu->cd.arm.r[7] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089200c0)

void arm_instr_multi_0x088e00c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[6];
		p[1] = cpu->cd.arm.r[7];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088e00c0)

void arm_instr_multi_0x08940012(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08940012)

void arm_instr_multi_0x089100c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[6] = p[0];
		cpu->cd.arm.r[7] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089100c0)

void arm_instr_multi_0x0813000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[2] = p[-1];
		cpu->cd.arm.r[3] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0813000c)

void arm_instr_multi_0x089c000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[2] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089c000c)

void arm_instr_multi_0x09920003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09920003)

void arm_instr_multi_0x08950060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[0];
		cpu->cd.arm.r[6] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08950060)

void arm_instr_multi_0x09860006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09860006)

void arm_instr_multi_0x088d4010(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[14];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d4010)

void arm_instr_multi_0x09160006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[-1];
		cpu->cd.arm.r[2] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09160006)

void arm_instr_multi_0x08990600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[9] = p[0];
		cpu->cd.arm.r[10] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08990600)

void arm_instr_multi_0x08980006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[8];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08980006)

void arm_instr_multi_0x091c0006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[-1];
		cpu->cd.arm.r[2] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091c0006)

void arm_instr_multi_0x080c0600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[9];
		p[0] = cpu->cd.arm.r[10];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x080c0600)

void arm_instr_multi_0x0894000a(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0894000a)

void arm_instr_multi_0x09311038(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[-3];
		cpu->cd.arm.r[4] = p[-2];
		cpu->cd.arm.r[5] = p[-1];
		cpu->cd.arm.r[12] = p[0];
		cpu->cd.arm.r[1] -= 16;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09311038)

void arm_instr_multi_0x09205030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-3] = cpu->cd.arm.r[4];
		p[-2] = cpu->cd.arm.r[5];
		p[-1] = cpu->cd.arm.r[12];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[0] -= 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09205030)

void arm_instr_multi_0x08850018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[5];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08850018)

void arm_instr_multi_0x09190300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[8] = p[-1];
		cpu->cd.arm.r[9] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09190300)

void arm_instr_multi_0x088d0180(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[7];
		p[1] = cpu->cd.arm.r[8];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d0180)

void arm_instr_multi_0x08980003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[8];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08980003)

void arm_instr_multi_0x098d000e(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
		p[2] = cpu->cd.arm.r[3];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x098d000e)

void arm_instr_multi_0x098c0006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[1];
		p[1] = cpu->cd.arm.r[2];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x098c0006)

void arm_instr_multi_0x09010018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[3];
		p[0] = cpu->cd.arm.r[4];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09010018)

void arm_instr_multi_0x09860030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x09860030)

void arm_instr_multi_0x092d4400(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-1] = cpu->cd.arm.r[10];
		p[0] = cpu->cd.arm.r[14];
		cpu->cd.arm.r[13] -= 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d4400)

void arm_instr_multi_0x08bd8400(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[10] = p[0];
		cpu->pc = p[1];
		cpu->cd.arm.r[13] += 8;
		quick_pc_to_pointers(cpu);
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd8400)

void arm_instr_multi_0x089e0060(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[5] = p[0];
		cpu->cd.arm.r[6] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089e0060)

void arm_instr_multi_0x088c00c8(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[3];
		p[1] = cpu->cd.arm.r[6];
		p[2] = cpu->cd.arm.r[7];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088c00c8)

void arm_instr_multi_0x0893000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[2] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x0893000c)

void arm_instr_multi_0x09110003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[1];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[-1];
		cpu->cd.arm.r[1] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09110003)

void arm_instr_multi_0x08ac000f(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
		p[2] = cpu->cd.arm.r[2];
		p[3] = cpu->cd.arm.r[3];
		cpu->cd.arm.r[12] += 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08ac000f)

void arm_instr_multi_0x08be000f(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[14];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
		cpu->cd.arm.r[2] = p[2];
		cpu->cd.arm.r[3] = p[3];
		cpu->cd.arm.r[14] += 16;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08be000f)

void arm_instr_multi_0x08940018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[4] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08940018)

void arm_instr_multi_0x091b68f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[11];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x18 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[-6];
		cpu->cd.arm.r[5] = p[-5];
		cpu->cd.arm.r[6] = p[-4];
		cpu->cd.arm.r[7] = p[-3];
		cpu->cd.arm.r[11] = p[-2];
		cpu->cd.arm.r[13] = p[-1];
		cpu->cd.arm.r[14] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x091b68f0)

void arm_instr_multi_0x09140018(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	addr -= 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0x4 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[-1];
		cpu->cd.arm.r[4] = p[0];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09140018)

void arm_instr_multi_0x08940009(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[4];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[3] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08940009)

void arm_instr_multi_0x08bd41f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xfe8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->cd.arm.r[8] = p[4];
		cpu->cd.arm.r[14] = p[5];
		cpu->cd.arm.r[13] += 24;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd41f0)

void arm_instr_multi_0x08a20600(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[9];
		p[1] = cpu->cd.arm.r[10];
		cpu->cd.arm.r[2] += 8;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08a20600)

void arm_instr_multi_0x08990003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08990003)

void arm_instr_multi_0x09904008(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[0];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[3] = p[0];
		cpu->cd.arm.r[14] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x09904008)

void arm_instr_multi_0x098c0003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[0];
		p[1] = cpu->cd.arm.r[1];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x098c0003)

void arm_instr_multi_0x088900c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[6];
		p[1] = cpu->cd.arm.r[7];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088900c0)

void arm_instr_multi_0x088200c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[2];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[6];
		p[1] = cpu->cd.arm.r[7];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088200c0)

void arm_instr_multi_0x088300c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[6];
		p[1] = cpu->cd.arm.r[7];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088300c0)

void arm_instr_multi_0x089300c0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[3];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[6] = p[0];
		cpu->cd.arm.r[7] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089300c0)

void arm_instr_multi_0x092d00f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	addr -= 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr >= 0xc && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[-3] = cpu->cd.arm.r[4];
		p[-2] = cpu->cd.arm.r[5];
		p[-1] = cpu->cd.arm.r[6];
		p[0] = cpu->cd.arm.r[7];
		cpu->cd.arm.r[13] -= 16;
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x092d00f0)

void arm_instr_multi_0x08bd00f0(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff0 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
		cpu->cd.arm.r[6] = p[2];
		cpu->cd.arm.r[7] = p[3];
		cpu->cd.arm.r[13] += 16;
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08bd00f0)

void arm_instr_multi_0x08960030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[6];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[4] = p[0];
		cpu->cd.arm.r[5] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08960030)

void arm_instr_multi_0x08980300(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[8];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[8] = p[0];
		cpu->cd.arm.r[9] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08980300)

void arm_instr_multi_0x089c5000(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[12];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[12] = p[0];
		cpu->cd.arm.r[14] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x089c5000)

void arm_instr_multi_0x088d1020(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[13];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[5];
		p[1] = cpu->cd.arm.r[12];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x088d1020)

void arm_instr_multi_0x08990006(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[1] = p[0];
		cpu->cd.arm.r[2] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x08990006)

void arm_instr_multi_0x08890030(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[4];
		p[1] = cpu->cd.arm.r[5];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x08890030)

void arm_instr_multi_0x099a0003(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[10];
	addr += 4;
	page = cpu->cd.arm.host_load[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		cpu->cd.arm.r[0] = p[0];
		cpu->cd.arm.r[1] = p[1];
	} else
		instr(bdt_load)(cpu, ic);
}
Y(multi_0x099a0003)

void arm_instr_multi_0x0989000c(struct cpu *cpu, struct arm_instr_call *ic) {
	unsigned char *page;
	uint32_t addr = cpu->cd.arm.r[9];
	addr += 4;
	page = cpu->cd.arm.host_store[addr >> 12];
	addr &= 0xffc;
	if (addr <= 0xff8 && page != NULL) {
		uint32_t *p = (uint32_t *) (page + addr);
		p[0] = cpu->cd.arm.r[2];
		p[1] = cpu->cd.arm.r[3];
	} else
		instr(bdt_store)(cpu, ic);
}
Y(multi_0x0989000c)

uint32_t multi_opcode_0[4] = {
	0x08020003,
	0x09201008,
	0x09205008,
0 };

uint32_t multi_opcode_1[1] = {
0 };

uint32_t multi_opcode_2[3] = {
	0x09205018,
	0x09205030,
0 };

uint32_t multi_opcode_3[1] = {
0 };

uint32_t multi_opcode_4[1] = {
0 };

uint32_t multi_opcode_5[1] = {
0 };

uint32_t multi_opcode_6[1] = {
0 };

uint32_t multi_opcode_7[1] = {
0 };

uint32_t multi_opcode_8[2] = {
	0x090a0300,
0 };

uint32_t multi_opcode_9[1] = {
0 };

uint32_t multi_opcode_10[1] = {
0 };

uint32_t multi_opcode_11[1] = {
0 };

uint32_t multi_opcode_12[1] = {
0 };

uint32_t multi_opcode_13[1] = {
0 };

uint32_t multi_opcode_14[1] = {
0 };

uint32_t multi_opcode_15[1] = {
0 };

uint32_t multi_opcode_16[1] = {
0 };

uint32_t multi_opcode_17[1] = {
0 };

uint32_t multi_opcode_18[2] = {
	0x09010018,
0 };

uint32_t multi_opcode_19[1] = {
0 };

uint32_t multi_opcode_20[1] = {
0 };

uint32_t multi_opcode_21[1] = {
0 };

uint32_t multi_opcode_22[1] = {
0 };

uint32_t multi_opcode_23[1] = {
0 };

uint32_t multi_opcode_24[1] = {
0 };

uint32_t multi_opcode_25[1] = {
0 };

uint32_t multi_opcode_26[1] = {
0 };

uint32_t multi_opcode_27[1] = {
0 };

uint32_t multi_opcode_28[1] = {
0 };

uint32_t multi_opcode_29[1] = {
0 };

uint32_t multi_opcode_30[1] = {
0 };

uint32_t multi_opcode_31[1] = {
0 };

uint32_t multi_opcode_32[4] = {
	0x09040003,
	0x080c0003,
	0x080c0600,
0 };

uint32_t multi_opcode_33[3] = {
	0x08040006,
	0x0804000c,
0 };

uint32_t multi_opcode_34[2] = {
	0x080c0030,
0 };

uint32_t multi_opcode_35[1] = {
0 };

uint32_t multi_opcode_36[1] = {
0 };

uint32_t multi_opcode_37[1] = {
0 };

uint32_t multi_opcode_38[1] = {
0 };

uint32_t multi_opcode_39[1] = {
0 };

uint32_t multi_opcode_40[1] = {
0 };

uint32_t multi_opcode_41[1] = {
0 };

uint32_t multi_opcode_42[1] = {
0 };

uint32_t multi_opcode_43[1] = {
0 };

uint32_t multi_opcode_44[1] = {
0 };

uint32_t multi_opcode_45[1] = {
0 };

uint32_t multi_opcode_46[1] = {
0 };

uint32_t multi_opcode_47[1] = {
0 };

uint32_t multi_opcode_48[6] = {
	0x092d4000,
	0x092dd800,
	0x092d4001,
	0x092ddc00,
	0x092d4400,
0 };

uint32_t multi_opcode_49[2] = {
	0x090d000f,
0 };

uint32_t multi_opcode_50[8] = {
	0x092dd830,
	0x092dd810,
	0x092d4010,
	0x092d4030,
	0x092ddc30,
	0x092d0030,
	0x092d0010,
0 };

uint32_t multi_opcode_51[2] = {
	0x092d0c1f,
0 };

uint32_t multi_opcode_52[1] = {
0 };

uint32_t multi_opcode_53[1] = {
0 };

uint32_t multi_opcode_54[9] = {
	0x092dd8f0,
	0x092dd870,
	0x092d4070,
	0x092ddc70,
	0x092ddcf0,
	0x092d40f0,
	0x092d0070,
	0x092d00f0,
0 };

uint32_t multi_opcode_55[1] = {
0 };

uint32_t multi_opcode_56[1] = {
0 };

uint32_t multi_opcode_57[1] = {
0 };

uint32_t multi_opcode_58[1] = {
0 };

uint32_t multi_opcode_59[1] = {
0 };

uint32_t multi_opcode_60[1] = {
0 };

uint32_t multi_opcode_61[1] = {
0 };

uint32_t multi_opcode_62[9] = {
	0x092ddff0,
	0x092dddf0,
	0x092dd9f0,
	0x092d41f0,
	0x092ddbf0,
	0x092d0ff0,
	0x092d47f0,
	0x092d45f0,
0 };

uint32_t multi_opcode_63[1] = {
0 };

uint32_t multi_opcode_64[3] = {
	0x08100009,
	0x091a0600,
0 };

uint32_t multi_opcode_65[2] = {
	0x09120006,
0 };

uint32_t multi_opcode_66[1] = {
0 };

uint32_t multi_opcode_67[1] = {
0 };

uint32_t multi_opcode_68[1] = {
0 };

uint32_t multi_opcode_69[1] = {
0 };

uint32_t multi_opcode_70[1] = {
0 };

uint32_t multi_opcode_71[1] = {
0 };

uint32_t multi_opcode_72[1] = {
0 };

uint32_t multi_opcode_73[1] = {
0 };

uint32_t multi_opcode_74[1] = {
0 };

uint32_t multi_opcode_75[1] = {
0 };

uint32_t multi_opcode_76[1] = {
0 };

uint32_t multi_opcode_77[1] = {
0 };

uint32_t multi_opcode_78[1] = {
0 };

uint32_t multi_opcode_79[1] = {
0 };

uint32_t multi_opcode_80[9] = {
	0x08110003,
	0x091ba800,
	0x091b6800,
	0x08130003,
	0x091bac00,
	0x09311008,
	0x09315008,
	0x09110003,
0 };

uint32_t multi_opcode_81[3] = {
	0x0911000f,
	0x0813000c,
0 };

uint32_t multi_opcode_82[9] = {
	0x091ba830,
	0x091ba810,
	0x08130018,
	0x091b6830,
	0x091bac30,
	0x09315018,
	0x091b6810,
	0x09311038,
0 };

uint32_t multi_opcode_83[1] = {
0 };

uint32_t multi_opcode_84[1] = {
0 };

uint32_t multi_opcode_85[1] = {
0 };

uint32_t multi_opcode_86[7] = {
	0x091ba8f0,
	0x091ba870,
	0x091bac70,
	0x091bacf0,
	0x091b6870,
	0x091b68f0,
0 };

uint32_t multi_opcode_87[1] = {
0 };

uint32_t multi_opcode_88[2] = {
	0x09190300,
0 };

uint32_t multi_opcode_89[1] = {
0 };

uint32_t multi_opcode_90[1] = {
0 };

uint32_t multi_opcode_91[1] = {
0 };

uint32_t multi_opcode_92[1] = {
0 };

uint32_t multi_opcode_93[1] = {
0 };

uint32_t multi_opcode_94[8] = {
	0x091baff0,
	0x091badf0,
	0x091ba9f0,
	0x091b6ff0,
	0x091babf0,
	0x091b69f0,
	0x091b6df0,
0 };

uint32_t multi_opcode_95[1] = {
0 };

uint32_t multi_opcode_96[1] = {
0 };

uint32_t multi_opcode_97[3] = {
	0x09160006,
	0x091c0006,
0 };

uint32_t multi_opcode_98[2] = {
	0x09140018,
0 };

uint32_t multi_opcode_99[1] = {
0 };

uint32_t multi_opcode_100[3] = {
	0x09160060,
	0x08160060,
0 };

uint32_t multi_opcode_101[1] = {
0 };

uint32_t multi_opcode_102[1] = {
0 };

uint32_t multi_opcode_103[1] = {
0 };

uint32_t multi_opcode_104[1] = {
0 };

uint32_t multi_opcode_105[1] = {
0 };

uint32_t multi_opcode_106[1] = {
0 };

uint32_t multi_opcode_107[1] = {
0 };

uint32_t multi_opcode_108[1] = {
0 };

uint32_t multi_opcode_109[1] = {
0 };

uint32_t multi_opcode_110[1] = {
0 };

uint32_t multi_opcode_111[1] = {
0 };

uint32_t multi_opcode_112[2] = {
	0x08150003,
0 };

uint32_t multi_opcode_113[3] = {
	0x0817000c,
	0x09150006,
0 };

uint32_t multi_opcode_114[2] = {
	0x09150018,
0 };

uint32_t multi_opcode_115[1] = {
0 };

uint32_t multi_opcode_116[1] = {
0 };

uint32_t multi_opcode_117[1] = {
0 };

uint32_t multi_opcode_118[1] = {
0 };

uint32_t multi_opcode_119[1] = {
0 };

uint32_t multi_opcode_120[1] = {
0 };

uint32_t multi_opcode_121[1] = {
0 };

uint32_t multi_opcode_122[1] = {
0 };

uint32_t multi_opcode_123[1] = {
0 };

uint32_t multi_opcode_124[1] = {
0 };

uint32_t multi_opcode_125[1] = {
0 };

uint32_t multi_opcode_126[1] = {
0 };

uint32_t multi_opcode_127[1] = {
0 };

uint32_t multi_opcode_128[5] = {
	0x08820003,
	0x08a01008,
	0x08a05008,
	0x08a20600,
0 };

uint32_t multi_opcode_129[3] = {
	0x08800006,
	0x08880006,
0 };

uint32_t multi_opcode_130[7] = {
	0x08820018,
	0x08a05018,
	0x08880018,
	0x08820030,
	0x08800018,
	0x08800030,
0 };

uint32_t multi_opcode_131[1] = {
0 };

uint32_t multi_opcode_132[2] = {
	0x088200c0,
0 };

uint32_t multi_opcode_133[1] = {
0 };

uint32_t multi_opcode_134[1] = {
0 };

uint32_t multi_opcode_135[1] = {
0 };

uint32_t multi_opcode_136[3] = {
	0x08820180,
	0x08800180,
0 };

uint32_t multi_opcode_137[1] = {
0 };

uint32_t multi_opcode_138[1] = {
0 };

uint32_t multi_opcode_139[1] = {
0 };

uint32_t multi_opcode_140[1] = {
0 };

uint32_t multi_opcode_141[1] = {
0 };

uint32_t multi_opcode_142[3] = {
	0x08a051f8,
	0x08807ff0,
0 };

uint32_t multi_opcode_143[1] = {
0 };

uint32_t multi_opcode_144[5] = {
	0x08830600,
	0x08810600,
	0x098b0003,
	0x08830003,
0 };

uint32_t multi_opcode_145[5] = {
	0x08830006,
	0x08890006,
	0x09830006,
	0x0989000c,
0 };

uint32_t multi_opcode_146[4] = {
	0x08810018,
	0x08830030,
	0x08890030,
0 };

uint32_t multi_opcode_147[1] = {
0 };

uint32_t multi_opcode_148[5] = {
	0x08830060,
	0x08a100c0,
	0x088900c0,
	0x088300c0,
0 };

uint32_t multi_opcode_149[1] = {
0 };

uint32_t multi_opcode_150[1] = {
0 };

uint32_t multi_opcode_151[1] = {
0 };

uint32_t multi_opcode_152[4] = {
	0x08a10300,
	0x08a10f00,
	0x08830300,
0 };

uint32_t multi_opcode_153[1] = {
0 };

uint32_t multi_opcode_154[1] = {
0 };

uint32_t multi_opcode_155[1] = {
0 };

uint32_t multi_opcode_156[1] = {
0 };

uint32_t multi_opcode_157[1] = {
0 };

uint32_t multi_opcode_158[2] = {
	0x08a151f8,
0 };

uint32_t multi_opcode_159[1] = {
0 };

uint32_t multi_opcode_160[6] = {
	0x08840003,
	0x088e1002,
	0x08840600,
	0x088c0003,
	0x098c0003,
0 };

uint32_t multi_opcode_161[8] = {
	0x08ac000c,
	0x088c0006,
	0x08860006,
	0x088e000c,
	0x09860006,
	0x098c0006,
	0x08ac000f,
0 };

uint32_t multi_opcode_162[4] = {
	0x088e0018,
	0x088c0018,
	0x09860030,
0 };

uint32_t multi_opcode_163[1] = {
0 };

uint32_t multi_opcode_164[4] = {
	0x088c0060,
	0x088e00c0,
	0x088c00c8,
0 };

uint32_t multi_opcode_165[1] = {
0 };

uint32_t multi_opcode_166[1] = {
0 };

uint32_t multi_opcode_167[1] = {
0 };

uint32_t multi_opcode_168[1] = {
0 };

uint32_t multi_opcode_169[1] = {
0 };

uint32_t multi_opcode_170[1] = {
0 };

uint32_t multi_opcode_171[1] = {
0 };

uint32_t multi_opcode_172[1] = {
0 };

uint32_t multi_opcode_173[1] = {
0 };

uint32_t multi_opcode_174[1] = {
0 };

uint32_t multi_opcode_175[1] = {
0 };

uint32_t multi_opcode_176[4] = {
	0x08850003,
	0x088d0088,
	0x088d1020,
0 };

uint32_t multi_opcode_177[5] = {
	0x08850006,
	0x08870006,
	0x0885000c,
	0x098d000e,
0 };

uint32_t multi_opcode_178[7] = {
	0x09870018,
	0x098d0030,
	0x088d1010,
	0x088d0030,
	0x088d4010,
	0x08850018,
0 };

uint32_t multi_opcode_179[2] = {
	0x09850014,
0 };

uint32_t multi_opcode_180[1] = {
0 };

uint32_t multi_opcode_181[1] = {
0 };

uint32_t multi_opcode_182[1] = {
0 };

uint32_t multi_opcode_183[1] = {
0 };

uint32_t multi_opcode_184[3] = {
	0x088d1100,
	0x088d0180,
0 };

uint32_t multi_opcode_185[1] = {
0 };

uint32_t multi_opcode_186[1] = {
0 };

uint32_t multi_opcode_187[1] = {
0 };

uint32_t multi_opcode_188[1] = {
0 };

uint32_t multi_opcode_189[1] = {
0 };

uint32_t multi_opcode_190[1] = {
0 };

uint32_t multi_opcode_191[2] = {
	0x088d1fff,
0 };

uint32_t multi_opcode_192[7] = {
	0x08920003,
	0x08900003,
	0x09920003,
	0x08980003,
	0x09904008,
	0x099a0003,
0 };

uint32_t multi_opcode_193[5] = {
	0x08900006,
	0x0892000c,
	0x08920006,
	0x08980006,
0 };

uint32_t multi_opcode_194[6] = {
	0x08920018,
	0x08980018,
	0x08900018,
	0x09900018,
	0x08920030,
0 };

uint32_t multi_opcode_195[1] = {
0 };

uint32_t multi_opcode_196[5] = {
	0x08b000c0,
	0x08980060,
	0x08900060,
	0x089200c0,
0 };

uint32_t multi_opcode_197[1] = {
0 };

uint32_t multi_opcode_198[1] = {
0 };

uint32_t multi_opcode_199[1] = {
0 };

uint32_t multi_opcode_200[4] = {
	0x08b00300,
	0x09900120,
	0x08980300,
0 };

uint32_t multi_opcode_201[1] = {
0 };

uint32_t multi_opcode_202[1] = {
0 };

uint32_t multi_opcode_203[1] = {
0 };

uint32_t multi_opcode_204[2] = {
	0x08b00fc0,
0 };

uint32_t multi_opcode_205[1] = {
0 };

uint32_t multi_opcode_206[2] = {
	0x08b051f8,
0 };

uint32_t multi_opcode_207[1] = {
0 };

uint32_t multi_opcode_208[9] = {
	0x08930003,
	0x08910003,
	0x08930600,
	0x08b11008,
	0x08b15008,
	0x08931008,
	0x08990600,
	0x08990003,
0 };

uint32_t multi_opcode_209[7] = {
	0x08930006,
	0x0891000e,
	0x08910006,
	0x09930006,
	0x0893000c,
	0x08990006,
0 };

uint32_t multi_opcode_210[6] = {
	0x08b15018,
	0x08930018,
	0x099b0030,
	0x08910030,
	0x08990018,
0 };

uint32_t multi_opcode_211[1] = {
0 };

uint32_t multi_opcode_212[4] = {
	0x08930060,
	0x089100c0,
	0x089300c0,
0 };

uint32_t multi_opcode_213[1] = {
0 };

uint32_t multi_opcode_214[1] = {
0 };

uint32_t multi_opcode_215[1] = {
0 };

uint32_t multi_opcode_216[3] = {
	0x08930180,
	0x099b0180,
0 };

uint32_t multi_opcode_217[1] = {
0 };

uint32_t multi_opcode_218[1] = {
0 };

uint32_t multi_opcode_219[1] = {
0 };

uint32_t multi_opcode_220[1] = {
0 };

uint32_t multi_opcode_221[1] = {
0 };

uint32_t multi_opcode_222[1] = {
0 };

uint32_t multi_opcode_223[1] = {
0 };

uint32_t multi_opcode_224[6] = {
	0x08940003,
	0x089e000a,
	0x0894000a,
	0x08940009,
	0x089c5000,
0 };

uint32_t multi_opcode_225[6] = {
	0x0894000c,
	0x089c0006,
	0x0896000c,
	0x089c000c,
	0x08be000f,
0 };

uint32_t multi_opcode_226[8] = {
	0x089e0018,
	0x09940018,
	0x089c0018,
	0x089e0030,
	0x08940012,
	0x08940018,
	0x08960030,
0 };

uint32_t multi_opcode_227[1] = {
0 };

uint32_t multi_opcode_228[2] = {
	0x089e0060,
0 };

uint32_t multi_opcode_229[1] = {
0 };

uint32_t multi_opcode_230[1] = {
0 };

uint32_t multi_opcode_231[1] = {
0 };

uint32_t multi_opcode_232[3] = {
	0x099c0180,
	0x089c0300,
0 };

uint32_t multi_opcode_233[1] = {
0 };

uint32_t multi_opcode_234[1] = {
0 };

uint32_t multi_opcode_235[1] = {
0 };

uint32_t multi_opcode_236[1] = {
0 };

uint32_t multi_opcode_237[1] = {
0 };

uint32_t multi_opcode_238[1] = {
0 };

uint32_t multi_opcode_239[1] = {
0 };

uint32_t multi_opcode_240[7] = {
	0x08bd8000,
	0x08bd8001,
	0x08950003,
	0x08bd0400,
	0x08970600,
	0x08bd8400,
0 };

uint32_t multi_opcode_241[3] = {
	0x08950006,
	0x08970006,
0 };

uint32_t multi_opcode_242[8] = {
	0x08bd8010,
	0x08bd8030,
	0x08bd0030,
	0x08bd0010,
	0x08bd4010,
	0x08950030,
	0x08970030,
0 };

uint32_t multi_opcode_243[2] = {
	0x08bd4c1f,
0 };

uint32_t multi_opcode_244[3] = {
	0x08971040,
	0x08950060,
0 };

uint32_t multi_opcode_245[1] = {
0 };

uint32_t multi_opcode_246[6] = {
	0x08bd8070,
	0x08bd40f0,
	0x08bd80f0,
	0x08bd0070,
	0x08bd00f0,
0 };

uint32_t multi_opcode_247[1] = {
0 };

uint32_t multi_opcode_248[3] = {
	0x08970300,
	0x08970180,
0 };

uint32_t multi_opcode_249[1] = {
0 };

uint32_t multi_opcode_250[1] = {
0 };

uint32_t multi_opcode_251[1] = {
0 };

uint32_t multi_opcode_252[1] = {
0 };

uint32_t multi_opcode_253[1] = {
0 };

uint32_t multi_opcode_254[6] = {
	0x08bd81f0,
	0x08bd0ff0,
	0x08bd87f0,
	0x08bd85f0,
	0x08bd41f0,
0 };

uint32_t multi_opcode_255[1] = {
0 };
void (*multi_opcode_f_0[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08020003__eq,
	arm_instr_multi_0x08020003__ne,
	arm_instr_multi_0x08020003__cs,
	arm_instr_multi_0x08020003__cc,
	arm_instr_multi_0x08020003__mi,
	arm_instr_multi_0x08020003__pl,
	arm_instr_multi_0x08020003__vs,
	arm_instr_multi_0x08020003__vc,
	arm_instr_multi_0x08020003__hi,
	arm_instr_multi_0x08020003__ls,
	arm_instr_multi_0x08020003__ge,
	arm_instr_multi_0x08020003__lt,
	arm_instr_multi_0x08020003__gt,
	arm_instr_multi_0x08020003__le,
	arm_instr_multi_0x08020003,
	arm_instr_nop,
	arm_instr_multi_0x09201008__eq,
	arm_instr_multi_0x09201008__ne,
	arm_instr_multi_0x09201008__cs,
	arm_instr_multi_0x09201008__cc,
	arm_instr_multi_0x09201008__mi,
	arm_instr_multi_0x09201008__pl,
	arm_instr_multi_0x09201008__vs,
	arm_instr_multi_0x09201008__vc,
	arm_instr_multi_0x09201008__hi,
	arm_instr_multi_0x09201008__ls,
	arm_instr_multi_0x09201008__ge,
	arm_instr_multi_0x09201008__lt,
	arm_instr_multi_0x09201008__gt,
	arm_instr_multi_0x09201008__le,
	arm_instr_multi_0x09201008,
	arm_instr_nop,
	arm_instr_multi_0x09205008__eq,
	arm_instr_multi_0x09205008__ne,
	arm_instr_multi_0x09205008__cs,
	arm_instr_multi_0x09205008__cc,
	arm_instr_multi_0x09205008__mi,
	arm_instr_multi_0x09205008__pl,
	arm_instr_multi_0x09205008__vs,
	arm_instr_multi_0x09205008__vc,
	arm_instr_multi_0x09205008__hi,
	arm_instr_multi_0x09205008__ls,
	arm_instr_multi_0x09205008__ge,
	arm_instr_multi_0x09205008__lt,
	arm_instr_multi_0x09205008__gt,
	arm_instr_multi_0x09205008__le,
	arm_instr_multi_0x09205008,
	arm_instr_nop,
};
void (*multi_opcode_f_2[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09205018__eq,
	arm_instr_multi_0x09205018__ne,
	arm_instr_multi_0x09205018__cs,
	arm_instr_multi_0x09205018__cc,
	arm_instr_multi_0x09205018__mi,
	arm_instr_multi_0x09205018__pl,
	arm_instr_multi_0x09205018__vs,
	arm_instr_multi_0x09205018__vc,
	arm_instr_multi_0x09205018__hi,
	arm_instr_multi_0x09205018__ls,
	arm_instr_multi_0x09205018__ge,
	arm_instr_multi_0x09205018__lt,
	arm_instr_multi_0x09205018__gt,
	arm_instr_multi_0x09205018__le,
	arm_instr_multi_0x09205018,
	arm_instr_nop,
	arm_instr_multi_0x09205030__eq,
	arm_instr_multi_0x09205030__ne,
	arm_instr_multi_0x09205030__cs,
	arm_instr_multi_0x09205030__cc,
	arm_instr_multi_0x09205030__mi,
	arm_instr_multi_0x09205030__pl,
	arm_instr_multi_0x09205030__vs,
	arm_instr_multi_0x09205030__vc,
	arm_instr_multi_0x09205030__hi,
	arm_instr_multi_0x09205030__ls,
	arm_instr_multi_0x09205030__ge,
	arm_instr_multi_0x09205030__lt,
	arm_instr_multi_0x09205030__gt,
	arm_instr_multi_0x09205030__le,
	arm_instr_multi_0x09205030,
	arm_instr_nop,
};
void (*multi_opcode_f_8[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x090a0300__eq,
	arm_instr_multi_0x090a0300__ne,
	arm_instr_multi_0x090a0300__cs,
	arm_instr_multi_0x090a0300__cc,
	arm_instr_multi_0x090a0300__mi,
	arm_instr_multi_0x090a0300__pl,
	arm_instr_multi_0x090a0300__vs,
	arm_instr_multi_0x090a0300__vc,
	arm_instr_multi_0x090a0300__hi,
	arm_instr_multi_0x090a0300__ls,
	arm_instr_multi_0x090a0300__ge,
	arm_instr_multi_0x090a0300__lt,
	arm_instr_multi_0x090a0300__gt,
	arm_instr_multi_0x090a0300__le,
	arm_instr_multi_0x090a0300,
	arm_instr_nop,
};
void (*multi_opcode_f_18[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09010018__eq,
	arm_instr_multi_0x09010018__ne,
	arm_instr_multi_0x09010018__cs,
	arm_instr_multi_0x09010018__cc,
	arm_instr_multi_0x09010018__mi,
	arm_instr_multi_0x09010018__pl,
	arm_instr_multi_0x09010018__vs,
	arm_instr_multi_0x09010018__vc,
	arm_instr_multi_0x09010018__hi,
	arm_instr_multi_0x09010018__ls,
	arm_instr_multi_0x09010018__ge,
	arm_instr_multi_0x09010018__lt,
	arm_instr_multi_0x09010018__gt,
	arm_instr_multi_0x09010018__le,
	arm_instr_multi_0x09010018,
	arm_instr_nop,
};
void (*multi_opcode_f_32[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09040003__eq,
	arm_instr_multi_0x09040003__ne,
	arm_instr_multi_0x09040003__cs,
	arm_instr_multi_0x09040003__cc,
	arm_instr_multi_0x09040003__mi,
	arm_instr_multi_0x09040003__pl,
	arm_instr_multi_0x09040003__vs,
	arm_instr_multi_0x09040003__vc,
	arm_instr_multi_0x09040003__hi,
	arm_instr_multi_0x09040003__ls,
	arm_instr_multi_0x09040003__ge,
	arm_instr_multi_0x09040003__lt,
	arm_instr_multi_0x09040003__gt,
	arm_instr_multi_0x09040003__le,
	arm_instr_multi_0x09040003,
	arm_instr_nop,
	arm_instr_multi_0x080c0003__eq,
	arm_instr_multi_0x080c0003__ne,
	arm_instr_multi_0x080c0003__cs,
	arm_instr_multi_0x080c0003__cc,
	arm_instr_multi_0x080c0003__mi,
	arm_instr_multi_0x080c0003__pl,
	arm_instr_multi_0x080c0003__vs,
	arm_instr_multi_0x080c0003__vc,
	arm_instr_multi_0x080c0003__hi,
	arm_instr_multi_0x080c0003__ls,
	arm_instr_multi_0x080c0003__ge,
	arm_instr_multi_0x080c0003__lt,
	arm_instr_multi_0x080c0003__gt,
	arm_instr_multi_0x080c0003__le,
	arm_instr_multi_0x080c0003,
	arm_instr_nop,
	arm_instr_multi_0x080c0600__eq,
	arm_instr_multi_0x080c0600__ne,
	arm_instr_multi_0x080c0600__cs,
	arm_instr_multi_0x080c0600__cc,
	arm_instr_multi_0x080c0600__mi,
	arm_instr_multi_0x080c0600__pl,
	arm_instr_multi_0x080c0600__vs,
	arm_instr_multi_0x080c0600__vc,
	arm_instr_multi_0x080c0600__hi,
	arm_instr_multi_0x080c0600__ls,
	arm_instr_multi_0x080c0600__ge,
	arm_instr_multi_0x080c0600__lt,
	arm_instr_multi_0x080c0600__gt,
	arm_instr_multi_0x080c0600__le,
	arm_instr_multi_0x080c0600,
	arm_instr_nop,
};
void (*multi_opcode_f_33[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08040006__eq,
	arm_instr_multi_0x08040006__ne,
	arm_instr_multi_0x08040006__cs,
	arm_instr_multi_0x08040006__cc,
	arm_instr_multi_0x08040006__mi,
	arm_instr_multi_0x08040006__pl,
	arm_instr_multi_0x08040006__vs,
	arm_instr_multi_0x08040006__vc,
	arm_instr_multi_0x08040006__hi,
	arm_instr_multi_0x08040006__ls,
	arm_instr_multi_0x08040006__ge,
	arm_instr_multi_0x08040006__lt,
	arm_instr_multi_0x08040006__gt,
	arm_instr_multi_0x08040006__le,
	arm_instr_multi_0x08040006,
	arm_instr_nop,
	arm_instr_multi_0x0804000c__eq,
	arm_instr_multi_0x0804000c__ne,
	arm_instr_multi_0x0804000c__cs,
	arm_instr_multi_0x0804000c__cc,
	arm_instr_multi_0x0804000c__mi,
	arm_instr_multi_0x0804000c__pl,
	arm_instr_multi_0x0804000c__vs,
	arm_instr_multi_0x0804000c__vc,
	arm_instr_multi_0x0804000c__hi,
	arm_instr_multi_0x0804000c__ls,
	arm_instr_multi_0x0804000c__ge,
	arm_instr_multi_0x0804000c__lt,
	arm_instr_multi_0x0804000c__gt,
	arm_instr_multi_0x0804000c__le,
	arm_instr_multi_0x0804000c,
	arm_instr_nop,
};
void (*multi_opcode_f_34[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x080c0030__eq,
	arm_instr_multi_0x080c0030__ne,
	arm_instr_multi_0x080c0030__cs,
	arm_instr_multi_0x080c0030__cc,
	arm_instr_multi_0x080c0030__mi,
	arm_instr_multi_0x080c0030__pl,
	arm_instr_multi_0x080c0030__vs,
	arm_instr_multi_0x080c0030__vc,
	arm_instr_multi_0x080c0030__hi,
	arm_instr_multi_0x080c0030__ls,
	arm_instr_multi_0x080c0030__ge,
	arm_instr_multi_0x080c0030__lt,
	arm_instr_multi_0x080c0030__gt,
	arm_instr_multi_0x080c0030__le,
	arm_instr_multi_0x080c0030,
	arm_instr_nop,
};
void (*multi_opcode_f_48[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x092d4000__eq,
	arm_instr_multi_0x092d4000__ne,
	arm_instr_multi_0x092d4000__cs,
	arm_instr_multi_0x092d4000__cc,
	arm_instr_multi_0x092d4000__mi,
	arm_instr_multi_0x092d4000__pl,
	arm_instr_multi_0x092d4000__vs,
	arm_instr_multi_0x092d4000__vc,
	arm_instr_multi_0x092d4000__hi,
	arm_instr_multi_0x092d4000__ls,
	arm_instr_multi_0x092d4000__ge,
	arm_instr_multi_0x092d4000__lt,
	arm_instr_multi_0x092d4000__gt,
	arm_instr_multi_0x092d4000__le,
	arm_instr_multi_0x092d4000,
	arm_instr_nop,
	arm_instr_multi_0x092dd800__eq,
	arm_instr_multi_0x092dd800__ne,
	arm_instr_multi_0x092dd800__cs,
	arm_instr_multi_0x092dd800__cc,
	arm_instr_multi_0x092dd800__mi,
	arm_instr_multi_0x092dd800__pl,
	arm_instr_multi_0x092dd800__vs,
	arm_instr_multi_0x092dd800__vc,
	arm_instr_multi_0x092dd800__hi,
	arm_instr_multi_0x092dd800__ls,
	arm_instr_multi_0x092dd800__ge,
	arm_instr_multi_0x092dd800__lt,
	arm_instr_multi_0x092dd800__gt,
	arm_instr_multi_0x092dd800__le,
	arm_instr_multi_0x092dd800,
	arm_instr_nop,
	arm_instr_multi_0x092d4001__eq,
	arm_instr_multi_0x092d4001__ne,
	arm_instr_multi_0x092d4001__cs,
	arm_instr_multi_0x092d4001__cc,
	arm_instr_multi_0x092d4001__mi,
	arm_instr_multi_0x092d4001__pl,
	arm_instr_multi_0x092d4001__vs,
	arm_instr_multi_0x092d4001__vc,
	arm_instr_multi_0x092d4001__hi,
	arm_instr_multi_0x092d4001__ls,
	arm_instr_multi_0x092d4001__ge,
	arm_instr_multi_0x092d4001__lt,
	arm_instr_multi_0x092d4001__gt,
	arm_instr_multi_0x092d4001__le,
	arm_instr_multi_0x092d4001,
	arm_instr_nop,
	arm_instr_multi_0x092ddc00__eq,
	arm_instr_multi_0x092ddc00__ne,
	arm_instr_multi_0x092ddc00__cs,
	arm_instr_multi_0x092ddc00__cc,
	arm_instr_multi_0x092ddc00__mi,
	arm_instr_multi_0x092ddc00__pl,
	arm_instr_multi_0x092ddc00__vs,
	arm_instr_multi_0x092ddc00__vc,
	arm_instr_multi_0x092ddc00__hi,
	arm_instr_multi_0x092ddc00__ls,
	arm_instr_multi_0x092ddc00__ge,
	arm_instr_multi_0x092ddc00__lt,
	arm_instr_multi_0x092ddc00__gt,
	arm_instr_multi_0x092ddc00__le,
	arm_instr_multi_0x092ddc00,
	arm_instr_nop,
	arm_instr_multi_0x092d4400__eq,
	arm_instr_multi_0x092d4400__ne,
	arm_instr_multi_0x092d4400__cs,
	arm_instr_multi_0x092d4400__cc,
	arm_instr_multi_0x092d4400__mi,
	arm_instr_multi_0x092d4400__pl,
	arm_instr_multi_0x092d4400__vs,
	arm_instr_multi_0x092d4400__vc,
	arm_instr_multi_0x092d4400__hi,
	arm_instr_multi_0x092d4400__ls,
	arm_instr_multi_0x092d4400__ge,
	arm_instr_multi_0x092d4400__lt,
	arm_instr_multi_0x092d4400__gt,
	arm_instr_multi_0x092d4400__le,
	arm_instr_multi_0x092d4400,
	arm_instr_nop,
};
void (*multi_opcode_f_49[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x090d000f__eq,
	arm_instr_multi_0x090d000f__ne,
	arm_instr_multi_0x090d000f__cs,
	arm_instr_multi_0x090d000f__cc,
	arm_instr_multi_0x090d000f__mi,
	arm_instr_multi_0x090d000f__pl,
	arm_instr_multi_0x090d000f__vs,
	arm_instr_multi_0x090d000f__vc,
	arm_instr_multi_0x090d000f__hi,
	arm_instr_multi_0x090d000f__ls,
	arm_instr_multi_0x090d000f__ge,
	arm_instr_multi_0x090d000f__lt,
	arm_instr_multi_0x090d000f__gt,
	arm_instr_multi_0x090d000f__le,
	arm_instr_multi_0x090d000f,
	arm_instr_nop,
};
void (*multi_opcode_f_50[112])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x092dd830__eq,
	arm_instr_multi_0x092dd830__ne,
	arm_instr_multi_0x092dd830__cs,
	arm_instr_multi_0x092dd830__cc,
	arm_instr_multi_0x092dd830__mi,
	arm_instr_multi_0x092dd830__pl,
	arm_instr_multi_0x092dd830__vs,
	arm_instr_multi_0x092dd830__vc,
	arm_instr_multi_0x092dd830__hi,
	arm_instr_multi_0x092dd830__ls,
	arm_instr_multi_0x092dd830__ge,
	arm_instr_multi_0x092dd830__lt,
	arm_instr_multi_0x092dd830__gt,
	arm_instr_multi_0x092dd830__le,
	arm_instr_multi_0x092dd830,
	arm_instr_nop,
	arm_instr_multi_0x092dd810__eq,
	arm_instr_multi_0x092dd810__ne,
	arm_instr_multi_0x092dd810__cs,
	arm_instr_multi_0x092dd810__cc,
	arm_instr_multi_0x092dd810__mi,
	arm_instr_multi_0x092dd810__pl,
	arm_instr_multi_0x092dd810__vs,
	arm_instr_multi_0x092dd810__vc,
	arm_instr_multi_0x092dd810__hi,
	arm_instr_multi_0x092dd810__ls,
	arm_instr_multi_0x092dd810__ge,
	arm_instr_multi_0x092dd810__lt,
	arm_instr_multi_0x092dd810__gt,
	arm_instr_multi_0x092dd810__le,
	arm_instr_multi_0x092dd810,
	arm_instr_nop,
	arm_instr_multi_0x092d4010__eq,
	arm_instr_multi_0x092d4010__ne,
	arm_instr_multi_0x092d4010__cs,
	arm_instr_multi_0x092d4010__cc,
	arm_instr_multi_0x092d4010__mi,
	arm_instr_multi_0x092d4010__pl,
	arm_instr_multi_0x092d4010__vs,
	arm_instr_multi_0x092d4010__vc,
	arm_instr_multi_0x092d4010__hi,
	arm_instr_multi_0x092d4010__ls,
	arm_instr_multi_0x092d4010__ge,
	arm_instr_multi_0x092d4010__lt,
	arm_instr_multi_0x092d4010__gt,
	arm_instr_multi_0x092d4010__le,
	arm_instr_multi_0x092d4010,
	arm_instr_nop,
	arm_instr_multi_0x092d4030__eq,
	arm_instr_multi_0x092d4030__ne,
	arm_instr_multi_0x092d4030__cs,
	arm_instr_multi_0x092d4030__cc,
	arm_instr_multi_0x092d4030__mi,
	arm_instr_multi_0x092d4030__pl,
	arm_instr_multi_0x092d4030__vs,
	arm_instr_multi_0x092d4030__vc,
	arm_instr_multi_0x092d4030__hi,
	arm_instr_multi_0x092d4030__ls,
	arm_instr_multi_0x092d4030__ge,
	arm_instr_multi_0x092d4030__lt,
	arm_instr_multi_0x092d4030__gt,
	arm_instr_multi_0x092d4030__le,
	arm_instr_multi_0x092d4030,
	arm_instr_nop,
	arm_instr_multi_0x092ddc30__eq,
	arm_instr_multi_0x092ddc30__ne,
	arm_instr_multi_0x092ddc30__cs,
	arm_instr_multi_0x092ddc30__cc,
	arm_instr_multi_0x092ddc30__mi,
	arm_instr_multi_0x092ddc30__pl,
	arm_instr_multi_0x092ddc30__vs,
	arm_instr_multi_0x092ddc30__vc,
	arm_instr_multi_0x092ddc30__hi,
	arm_instr_multi_0x092ddc30__ls,
	arm_instr_multi_0x092ddc30__ge,
	arm_instr_multi_0x092ddc30__lt,
	arm_instr_multi_0x092ddc30__gt,
	arm_instr_multi_0x092ddc30__le,
	arm_instr_multi_0x092ddc30,
	arm_instr_nop,
	arm_instr_multi_0x092d0030__eq,
	arm_instr_multi_0x092d0030__ne,
	arm_instr_multi_0x092d0030__cs,
	arm_instr_multi_0x092d0030__cc,
	arm_instr_multi_0x092d0030__mi,
	arm_instr_multi_0x092d0030__pl,
	arm_instr_multi_0x092d0030__vs,
	arm_instr_multi_0x092d0030__vc,
	arm_instr_multi_0x092d0030__hi,
	arm_instr_multi_0x092d0030__ls,
	arm_instr_multi_0x092d0030__ge,
	arm_instr_multi_0x092d0030__lt,
	arm_instr_multi_0x092d0030__gt,
	arm_instr_multi_0x092d0030__le,
	arm_instr_multi_0x092d0030,
	arm_instr_nop,
	arm_instr_multi_0x092d0010__eq,
	arm_instr_multi_0x092d0010__ne,
	arm_instr_multi_0x092d0010__cs,
	arm_instr_multi_0x092d0010__cc,
	arm_instr_multi_0x092d0010__mi,
	arm_instr_multi_0x092d0010__pl,
	arm_instr_multi_0x092d0010__vs,
	arm_instr_multi_0x092d0010__vc,
	arm_instr_multi_0x092d0010__hi,
	arm_instr_multi_0x092d0010__ls,
	arm_instr_multi_0x092d0010__ge,
	arm_instr_multi_0x092d0010__lt,
	arm_instr_multi_0x092d0010__gt,
	arm_instr_multi_0x092d0010__le,
	arm_instr_multi_0x092d0010,
	arm_instr_nop,
};
void (*multi_opcode_f_51[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x092d0c1f__eq,
	arm_instr_multi_0x092d0c1f__ne,
	arm_instr_multi_0x092d0c1f__cs,
	arm_instr_multi_0x092d0c1f__cc,
	arm_instr_multi_0x092d0c1f__mi,
	arm_instr_multi_0x092d0c1f__pl,
	arm_instr_multi_0x092d0c1f__vs,
	arm_instr_multi_0x092d0c1f__vc,
	arm_instr_multi_0x092d0c1f__hi,
	arm_instr_multi_0x092d0c1f__ls,
	arm_instr_multi_0x092d0c1f__ge,
	arm_instr_multi_0x092d0c1f__lt,
	arm_instr_multi_0x092d0c1f__gt,
	arm_instr_multi_0x092d0c1f__le,
	arm_instr_multi_0x092d0c1f,
	arm_instr_nop,
};
void (*multi_opcode_f_54[128])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x092dd8f0__eq,
	arm_instr_multi_0x092dd8f0__ne,
	arm_instr_multi_0x092dd8f0__cs,
	arm_instr_multi_0x092dd8f0__cc,
	arm_instr_multi_0x092dd8f0__mi,
	arm_instr_multi_0x092dd8f0__pl,
	arm_instr_multi_0x092dd8f0__vs,
	arm_instr_multi_0x092dd8f0__vc,
	arm_instr_multi_0x092dd8f0__hi,
	arm_instr_multi_0x092dd8f0__ls,
	arm_instr_multi_0x092dd8f0__ge,
	arm_instr_multi_0x092dd8f0__lt,
	arm_instr_multi_0x092dd8f0__gt,
	arm_instr_multi_0x092dd8f0__le,
	arm_instr_multi_0x092dd8f0,
	arm_instr_nop,
	arm_instr_multi_0x092dd870__eq,
	arm_instr_multi_0x092dd870__ne,
	arm_instr_multi_0x092dd870__cs,
	arm_instr_multi_0x092dd870__cc,
	arm_instr_multi_0x092dd870__mi,
	arm_instr_multi_0x092dd870__pl,
	arm_instr_multi_0x092dd870__vs,
	arm_instr_multi_0x092dd870__vc,
	arm_instr_multi_0x092dd870__hi,
	arm_instr_multi_0x092dd870__ls,
	arm_instr_multi_0x092dd870__ge,
	arm_instr_multi_0x092dd870__lt,
	arm_instr_multi_0x092dd870__gt,
	arm_instr_multi_0x092dd870__le,
	arm_instr_multi_0x092dd870,
	arm_instr_nop,
	arm_instr_multi_0x092d4070__eq,
	arm_instr_multi_0x092d4070__ne,
	arm_instr_multi_0x092d4070__cs,
	arm_instr_multi_0x092d4070__cc,
	arm_instr_multi_0x092d4070__mi,
	arm_instr_multi_0x092d4070__pl,
	arm_instr_multi_0x092d4070__vs,
	arm_instr_multi_0x092d4070__vc,
	arm_instr_multi_0x092d4070__hi,
	arm_instr_multi_0x092d4070__ls,
	arm_instr_multi_0x092d4070__ge,
	arm_instr_multi_0x092d4070__lt,
	arm_instr_multi_0x092d4070__gt,
	arm_instr_multi_0x092d4070__le,
	arm_instr_multi_0x092d4070,
	arm_instr_nop,
	arm_instr_multi_0x092ddc70__eq,
	arm_instr_multi_0x092ddc70__ne,
	arm_instr_multi_0x092ddc70__cs,
	arm_instr_multi_0x092ddc70__cc,
	arm_instr_multi_0x092ddc70__mi,
	arm_instr_multi_0x092ddc70__pl,
	arm_instr_multi_0x092ddc70__vs,
	arm_instr_multi_0x092ddc70__vc,
	arm_instr_multi_0x092ddc70__hi,
	arm_instr_multi_0x092ddc70__ls,
	arm_instr_multi_0x092ddc70__ge,
	arm_instr_multi_0x092ddc70__lt,
	arm_instr_multi_0x092ddc70__gt,
	arm_instr_multi_0x092ddc70__le,
	arm_instr_multi_0x092ddc70,
	arm_instr_nop,
	arm_instr_multi_0x092ddcf0__eq,
	arm_instr_multi_0x092ddcf0__ne,
	arm_instr_multi_0x092ddcf0__cs,
	arm_instr_multi_0x092ddcf0__cc,
	arm_instr_multi_0x092ddcf0__mi,
	arm_instr_multi_0x092ddcf0__pl,
	arm_instr_multi_0x092ddcf0__vs,
	arm_instr_multi_0x092ddcf0__vc,
	arm_instr_multi_0x092ddcf0__hi,
	arm_instr_multi_0x092ddcf0__ls,
	arm_instr_multi_0x092ddcf0__ge,
	arm_instr_multi_0x092ddcf0__lt,
	arm_instr_multi_0x092ddcf0__gt,
	arm_instr_multi_0x092ddcf0__le,
	arm_instr_multi_0x092ddcf0,
	arm_instr_nop,
	arm_instr_multi_0x092d40f0__eq,
	arm_instr_multi_0x092d40f0__ne,
	arm_instr_multi_0x092d40f0__cs,
	arm_instr_multi_0x092d40f0__cc,
	arm_instr_multi_0x092d40f0__mi,
	arm_instr_multi_0x092d40f0__pl,
	arm_instr_multi_0x092d40f0__vs,
	arm_instr_multi_0x092d40f0__vc,
	arm_instr_multi_0x092d40f0__hi,
	arm_instr_multi_0x092d40f0__ls,
	arm_instr_multi_0x092d40f0__ge,
	arm_instr_multi_0x092d40f0__lt,
	arm_instr_multi_0x092d40f0__gt,
	arm_instr_multi_0x092d40f0__le,
	arm_instr_multi_0x092d40f0,
	arm_instr_nop,
	arm_instr_multi_0x092d0070__eq,
	arm_instr_multi_0x092d0070__ne,
	arm_instr_multi_0x092d0070__cs,
	arm_instr_multi_0x092d0070__cc,
	arm_instr_multi_0x092d0070__mi,
	arm_instr_multi_0x092d0070__pl,
	arm_instr_multi_0x092d0070__vs,
	arm_instr_multi_0x092d0070__vc,
	arm_instr_multi_0x092d0070__hi,
	arm_instr_multi_0x092d0070__ls,
	arm_instr_multi_0x092d0070__ge,
	arm_instr_multi_0x092d0070__lt,
	arm_instr_multi_0x092d0070__gt,
	arm_instr_multi_0x092d0070__le,
	arm_instr_multi_0x092d0070,
	arm_instr_nop,
	arm_instr_multi_0x092d00f0__eq,
	arm_instr_multi_0x092d00f0__ne,
	arm_instr_multi_0x092d00f0__cs,
	arm_instr_multi_0x092d00f0__cc,
	arm_instr_multi_0x092d00f0__mi,
	arm_instr_multi_0x092d00f0__pl,
	arm_instr_multi_0x092d00f0__vs,
	arm_instr_multi_0x092d00f0__vc,
	arm_instr_multi_0x092d00f0__hi,
	arm_instr_multi_0x092d00f0__ls,
	arm_instr_multi_0x092d00f0__ge,
	arm_instr_multi_0x092d00f0__lt,
	arm_instr_multi_0x092d00f0__gt,
	arm_instr_multi_0x092d00f0__le,
	arm_instr_multi_0x092d00f0,
	arm_instr_nop,
};
void (*multi_opcode_f_62[128])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x092ddff0__eq,
	arm_instr_multi_0x092ddff0__ne,
	arm_instr_multi_0x092ddff0__cs,
	arm_instr_multi_0x092ddff0__cc,
	arm_instr_multi_0x092ddff0__mi,
	arm_instr_multi_0x092ddff0__pl,
	arm_instr_multi_0x092ddff0__vs,
	arm_instr_multi_0x092ddff0__vc,
	arm_instr_multi_0x092ddff0__hi,
	arm_instr_multi_0x092ddff0__ls,
	arm_instr_multi_0x092ddff0__ge,
	arm_instr_multi_0x092ddff0__lt,
	arm_instr_multi_0x092ddff0__gt,
	arm_instr_multi_0x092ddff0__le,
	arm_instr_multi_0x092ddff0,
	arm_instr_nop,
	arm_instr_multi_0x092dddf0__eq,
	arm_instr_multi_0x092dddf0__ne,
	arm_instr_multi_0x092dddf0__cs,
	arm_instr_multi_0x092dddf0__cc,
	arm_instr_multi_0x092dddf0__mi,
	arm_instr_multi_0x092dddf0__pl,
	arm_instr_multi_0x092dddf0__vs,
	arm_instr_multi_0x092dddf0__vc,
	arm_instr_multi_0x092dddf0__hi,
	arm_instr_multi_0x092dddf0__ls,
	arm_instr_multi_0x092dddf0__ge,
	arm_instr_multi_0x092dddf0__lt,
	arm_instr_multi_0x092dddf0__gt,
	arm_instr_multi_0x092dddf0__le,
	arm_instr_multi_0x092dddf0,
	arm_instr_nop,
	arm_instr_multi_0x092dd9f0__eq,
	arm_instr_multi_0x092dd9f0__ne,
	arm_instr_multi_0x092dd9f0__cs,
	arm_instr_multi_0x092dd9f0__cc,
	arm_instr_multi_0x092dd9f0__mi,
	arm_instr_multi_0x092dd9f0__pl,
	arm_instr_multi_0x092dd9f0__vs,
	arm_instr_multi_0x092dd9f0__vc,
	arm_instr_multi_0x092dd9f0__hi,
	arm_instr_multi_0x092dd9f0__ls,
	arm_instr_multi_0x092dd9f0__ge,
	arm_instr_multi_0x092dd9f0__lt,
	arm_instr_multi_0x092dd9f0__gt,
	arm_instr_multi_0x092dd9f0__le,
	arm_instr_multi_0x092dd9f0,
	arm_instr_nop,
	arm_instr_multi_0x092d41f0__eq,
	arm_instr_multi_0x092d41f0__ne,
	arm_instr_multi_0x092d41f0__cs,
	arm_instr_multi_0x092d41f0__cc,
	arm_instr_multi_0x092d41f0__mi,
	arm_instr_multi_0x092d41f0__pl,
	arm_instr_multi_0x092d41f0__vs,
	arm_instr_multi_0x092d41f0__vc,
	arm_instr_multi_0x092d41f0__hi,
	arm_instr_multi_0x092d41f0__ls,
	arm_instr_multi_0x092d41f0__ge,
	arm_instr_multi_0x092d41f0__lt,
	arm_instr_multi_0x092d41f0__gt,
	arm_instr_multi_0x092d41f0__le,
	arm_instr_multi_0x092d41f0,
	arm_instr_nop,
	arm_instr_multi_0x092ddbf0__eq,
	arm_instr_multi_0x092ddbf0__ne,
	arm_instr_multi_0x092ddbf0__cs,
	arm_instr_multi_0x092ddbf0__cc,
	arm_instr_multi_0x092ddbf0__mi,
	arm_instr_multi_0x092ddbf0__pl,
	arm_instr_multi_0x092ddbf0__vs,
	arm_instr_multi_0x092ddbf0__vc,
	arm_instr_multi_0x092ddbf0__hi,
	arm_instr_multi_0x092ddbf0__ls,
	arm_instr_multi_0x092ddbf0__ge,
	arm_instr_multi_0x092ddbf0__lt,
	arm_instr_multi_0x092ddbf0__gt,
	arm_instr_multi_0x092ddbf0__le,
	arm_instr_multi_0x092ddbf0,
	arm_instr_nop,
	arm_instr_multi_0x092d0ff0__eq,
	arm_instr_multi_0x092d0ff0__ne,
	arm_instr_multi_0x092d0ff0__cs,
	arm_instr_multi_0x092d0ff0__cc,
	arm_instr_multi_0x092d0ff0__mi,
	arm_instr_multi_0x092d0ff0__pl,
	arm_instr_multi_0x092d0ff0__vs,
	arm_instr_multi_0x092d0ff0__vc,
	arm_instr_multi_0x092d0ff0__hi,
	arm_instr_multi_0x092d0ff0__ls,
	arm_instr_multi_0x092d0ff0__ge,
	arm_instr_multi_0x092d0ff0__lt,
	arm_instr_multi_0x092d0ff0__gt,
	arm_instr_multi_0x092d0ff0__le,
	arm_instr_multi_0x092d0ff0,
	arm_instr_nop,
	arm_instr_multi_0x092d47f0__eq,
	arm_instr_multi_0x092d47f0__ne,
	arm_instr_multi_0x092d47f0__cs,
	arm_instr_multi_0x092d47f0__cc,
	arm_instr_multi_0x092d47f0__mi,
	arm_instr_multi_0x092d47f0__pl,
	arm_instr_multi_0x092d47f0__vs,
	arm_instr_multi_0x092d47f0__vc,
	arm_instr_multi_0x092d47f0__hi,
	arm_instr_multi_0x092d47f0__ls,
	arm_instr_multi_0x092d47f0__ge,
	arm_instr_multi_0x092d47f0__lt,
	arm_instr_multi_0x092d47f0__gt,
	arm_instr_multi_0x092d47f0__le,
	arm_instr_multi_0x092d47f0,
	arm_instr_nop,
	arm_instr_multi_0x092d45f0__eq,
	arm_instr_multi_0x092d45f0__ne,
	arm_instr_multi_0x092d45f0__cs,
	arm_instr_multi_0x092d45f0__cc,
	arm_instr_multi_0x092d45f0__mi,
	arm_instr_multi_0x092d45f0__pl,
	arm_instr_multi_0x092d45f0__vs,
	arm_instr_multi_0x092d45f0__vc,
	arm_instr_multi_0x092d45f0__hi,
	arm_instr_multi_0x092d45f0__ls,
	arm_instr_multi_0x092d45f0__ge,
	arm_instr_multi_0x092d45f0__lt,
	arm_instr_multi_0x092d45f0__gt,
	arm_instr_multi_0x092d45f0__le,
	arm_instr_multi_0x092d45f0,
	arm_instr_nop,
};
void (*multi_opcode_f_64[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08100009__eq,
	arm_instr_multi_0x08100009__ne,
	arm_instr_multi_0x08100009__cs,
	arm_instr_multi_0x08100009__cc,
	arm_instr_multi_0x08100009__mi,
	arm_instr_multi_0x08100009__pl,
	arm_instr_multi_0x08100009__vs,
	arm_instr_multi_0x08100009__vc,
	arm_instr_multi_0x08100009__hi,
	arm_instr_multi_0x08100009__ls,
	arm_instr_multi_0x08100009__ge,
	arm_instr_multi_0x08100009__lt,
	arm_instr_multi_0x08100009__gt,
	arm_instr_multi_0x08100009__le,
	arm_instr_multi_0x08100009,
	arm_instr_nop,
	arm_instr_multi_0x091a0600__eq,
	arm_instr_multi_0x091a0600__ne,
	arm_instr_multi_0x091a0600__cs,
	arm_instr_multi_0x091a0600__cc,
	arm_instr_multi_0x091a0600__mi,
	arm_instr_multi_0x091a0600__pl,
	arm_instr_multi_0x091a0600__vs,
	arm_instr_multi_0x091a0600__vc,
	arm_instr_multi_0x091a0600__hi,
	arm_instr_multi_0x091a0600__ls,
	arm_instr_multi_0x091a0600__ge,
	arm_instr_multi_0x091a0600__lt,
	arm_instr_multi_0x091a0600__gt,
	arm_instr_multi_0x091a0600__le,
	arm_instr_multi_0x091a0600,
	arm_instr_nop,
};
void (*multi_opcode_f_65[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09120006__eq,
	arm_instr_multi_0x09120006__ne,
	arm_instr_multi_0x09120006__cs,
	arm_instr_multi_0x09120006__cc,
	arm_instr_multi_0x09120006__mi,
	arm_instr_multi_0x09120006__pl,
	arm_instr_multi_0x09120006__vs,
	arm_instr_multi_0x09120006__vc,
	arm_instr_multi_0x09120006__hi,
	arm_instr_multi_0x09120006__ls,
	arm_instr_multi_0x09120006__ge,
	arm_instr_multi_0x09120006__lt,
	arm_instr_multi_0x09120006__gt,
	arm_instr_multi_0x09120006__le,
	arm_instr_multi_0x09120006,
	arm_instr_nop,
};
void (*multi_opcode_f_80[128])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08110003__eq,
	arm_instr_multi_0x08110003__ne,
	arm_instr_multi_0x08110003__cs,
	arm_instr_multi_0x08110003__cc,
	arm_instr_multi_0x08110003__mi,
	arm_instr_multi_0x08110003__pl,
	arm_instr_multi_0x08110003__vs,
	arm_instr_multi_0x08110003__vc,
	arm_instr_multi_0x08110003__hi,
	arm_instr_multi_0x08110003__ls,
	arm_instr_multi_0x08110003__ge,
	arm_instr_multi_0x08110003__lt,
	arm_instr_multi_0x08110003__gt,
	arm_instr_multi_0x08110003__le,
	arm_instr_multi_0x08110003,
	arm_instr_nop,
	arm_instr_multi_0x091ba800__eq,
	arm_instr_multi_0x091ba800__ne,
	arm_instr_multi_0x091ba800__cs,
	arm_instr_multi_0x091ba800__cc,
	arm_instr_multi_0x091ba800__mi,
	arm_instr_multi_0x091ba800__pl,
	arm_instr_multi_0x091ba800__vs,
	arm_instr_multi_0x091ba800__vc,
	arm_instr_multi_0x091ba800__hi,
	arm_instr_multi_0x091ba800__ls,
	arm_instr_multi_0x091ba800__ge,
	arm_instr_multi_0x091ba800__lt,
	arm_instr_multi_0x091ba800__gt,
	arm_instr_multi_0x091ba800__le,
	arm_instr_multi_0x091ba800,
	arm_instr_nop,
	arm_instr_multi_0x091b6800__eq,
	arm_instr_multi_0x091b6800__ne,
	arm_instr_multi_0x091b6800__cs,
	arm_instr_multi_0x091b6800__cc,
	arm_instr_multi_0x091b6800__mi,
	arm_instr_multi_0x091b6800__pl,
	arm_instr_multi_0x091b6800__vs,
	arm_instr_multi_0x091b6800__vc,
	arm_instr_multi_0x091b6800__hi,
	arm_instr_multi_0x091b6800__ls,
	arm_instr_multi_0x091b6800__ge,
	arm_instr_multi_0x091b6800__lt,
	arm_instr_multi_0x091b6800__gt,
	arm_instr_multi_0x091b6800__le,
	arm_instr_multi_0x091b6800,
	arm_instr_nop,
	arm_instr_multi_0x08130003__eq,
	arm_instr_multi_0x08130003__ne,
	arm_instr_multi_0x08130003__cs,
	arm_instr_multi_0x08130003__cc,
	arm_instr_multi_0x08130003__mi,
	arm_instr_multi_0x08130003__pl,
	arm_instr_multi_0x08130003__vs,
	arm_instr_multi_0x08130003__vc,
	arm_instr_multi_0x08130003__hi,
	arm_instr_multi_0x08130003__ls,
	arm_instr_multi_0x08130003__ge,
	arm_instr_multi_0x08130003__lt,
	arm_instr_multi_0x08130003__gt,
	arm_instr_multi_0x08130003__le,
	arm_instr_multi_0x08130003,
	arm_instr_nop,
	arm_instr_multi_0x091bac00__eq,
	arm_instr_multi_0x091bac00__ne,
	arm_instr_multi_0x091bac00__cs,
	arm_instr_multi_0x091bac00__cc,
	arm_instr_multi_0x091bac00__mi,
	arm_instr_multi_0x091bac00__pl,
	arm_instr_multi_0x091bac00__vs,
	arm_instr_multi_0x091bac00__vc,
	arm_instr_multi_0x091bac00__hi,
	arm_instr_multi_0x091bac00__ls,
	arm_instr_multi_0x091bac00__ge,
	arm_instr_multi_0x091bac00__lt,
	arm_instr_multi_0x091bac00__gt,
	arm_instr_multi_0x091bac00__le,
	arm_instr_multi_0x091bac00,
	arm_instr_nop,
	arm_instr_multi_0x09311008__eq,
	arm_instr_multi_0x09311008__ne,
	arm_instr_multi_0x09311008__cs,
	arm_instr_multi_0x09311008__cc,
	arm_instr_multi_0x09311008__mi,
	arm_instr_multi_0x09311008__pl,
	arm_instr_multi_0x09311008__vs,
	arm_instr_multi_0x09311008__vc,
	arm_instr_multi_0x09311008__hi,
	arm_instr_multi_0x09311008__ls,
	arm_instr_multi_0x09311008__ge,
	arm_instr_multi_0x09311008__lt,
	arm_instr_multi_0x09311008__gt,
	arm_instr_multi_0x09311008__le,
	arm_instr_multi_0x09311008,
	arm_instr_nop,
	arm_instr_multi_0x09315008__eq,
	arm_instr_multi_0x09315008__ne,
	arm_instr_multi_0x09315008__cs,
	arm_instr_multi_0x09315008__cc,
	arm_instr_multi_0x09315008__mi,
	arm_instr_multi_0x09315008__pl,
	arm_instr_multi_0x09315008__vs,
	arm_instr_multi_0x09315008__vc,
	arm_instr_multi_0x09315008__hi,
	arm_instr_multi_0x09315008__ls,
	arm_instr_multi_0x09315008__ge,
	arm_instr_multi_0x09315008__lt,
	arm_instr_multi_0x09315008__gt,
	arm_instr_multi_0x09315008__le,
	arm_instr_multi_0x09315008,
	arm_instr_nop,
	arm_instr_multi_0x09110003__eq,
	arm_instr_multi_0x09110003__ne,
	arm_instr_multi_0x09110003__cs,
	arm_instr_multi_0x09110003__cc,
	arm_instr_multi_0x09110003__mi,
	arm_instr_multi_0x09110003__pl,
	arm_instr_multi_0x09110003__vs,
	arm_instr_multi_0x09110003__vc,
	arm_instr_multi_0x09110003__hi,
	arm_instr_multi_0x09110003__ls,
	arm_instr_multi_0x09110003__ge,
	arm_instr_multi_0x09110003__lt,
	arm_instr_multi_0x09110003__gt,
	arm_instr_multi_0x09110003__le,
	arm_instr_multi_0x09110003,
	arm_instr_nop,
};
void (*multi_opcode_f_81[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x0911000f__eq,
	arm_instr_multi_0x0911000f__ne,
	arm_instr_multi_0x0911000f__cs,
	arm_instr_multi_0x0911000f__cc,
	arm_instr_multi_0x0911000f__mi,
	arm_instr_multi_0x0911000f__pl,
	arm_instr_multi_0x0911000f__vs,
	arm_instr_multi_0x0911000f__vc,
	arm_instr_multi_0x0911000f__hi,
	arm_instr_multi_0x0911000f__ls,
	arm_instr_multi_0x0911000f__ge,
	arm_instr_multi_0x0911000f__lt,
	arm_instr_multi_0x0911000f__gt,
	arm_instr_multi_0x0911000f__le,
	arm_instr_multi_0x0911000f,
	arm_instr_nop,
	arm_instr_multi_0x0813000c__eq,
	arm_instr_multi_0x0813000c__ne,
	arm_instr_multi_0x0813000c__cs,
	arm_instr_multi_0x0813000c__cc,
	arm_instr_multi_0x0813000c__mi,
	arm_instr_multi_0x0813000c__pl,
	arm_instr_multi_0x0813000c__vs,
	arm_instr_multi_0x0813000c__vc,
	arm_instr_multi_0x0813000c__hi,
	arm_instr_multi_0x0813000c__ls,
	arm_instr_multi_0x0813000c__ge,
	arm_instr_multi_0x0813000c__lt,
	arm_instr_multi_0x0813000c__gt,
	arm_instr_multi_0x0813000c__le,
	arm_instr_multi_0x0813000c,
	arm_instr_nop,
};
void (*multi_opcode_f_82[128])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x091ba830__eq,
	arm_instr_multi_0x091ba830__ne,
	arm_instr_multi_0x091ba830__cs,
	arm_instr_multi_0x091ba830__cc,
	arm_instr_multi_0x091ba830__mi,
	arm_instr_multi_0x091ba830__pl,
	arm_instr_multi_0x091ba830__vs,
	arm_instr_multi_0x091ba830__vc,
	arm_instr_multi_0x091ba830__hi,
	arm_instr_multi_0x091ba830__ls,
	arm_instr_multi_0x091ba830__ge,
	arm_instr_multi_0x091ba830__lt,
	arm_instr_multi_0x091ba830__gt,
	arm_instr_multi_0x091ba830__le,
	arm_instr_multi_0x091ba830,
	arm_instr_nop,
	arm_instr_multi_0x091ba810__eq,
	arm_instr_multi_0x091ba810__ne,
	arm_instr_multi_0x091ba810__cs,
	arm_instr_multi_0x091ba810__cc,
	arm_instr_multi_0x091ba810__mi,
	arm_instr_multi_0x091ba810__pl,
	arm_instr_multi_0x091ba810__vs,
	arm_instr_multi_0x091ba810__vc,
	arm_instr_multi_0x091ba810__hi,
	arm_instr_multi_0x091ba810__ls,
	arm_instr_multi_0x091ba810__ge,
	arm_instr_multi_0x091ba810__lt,
	arm_instr_multi_0x091ba810__gt,
	arm_instr_multi_0x091ba810__le,
	arm_instr_multi_0x091ba810,
	arm_instr_nop,
	arm_instr_multi_0x08130018__eq,
	arm_instr_multi_0x08130018__ne,
	arm_instr_multi_0x08130018__cs,
	arm_instr_multi_0x08130018__cc,
	arm_instr_multi_0x08130018__mi,
	arm_instr_multi_0x08130018__pl,
	arm_instr_multi_0x08130018__vs,
	arm_instr_multi_0x08130018__vc,
	arm_instr_multi_0x08130018__hi,
	arm_instr_multi_0x08130018__ls,
	arm_instr_multi_0x08130018__ge,
	arm_instr_multi_0x08130018__lt,
	arm_instr_multi_0x08130018__gt,
	arm_instr_multi_0x08130018__le,
	arm_instr_multi_0x08130018,
	arm_instr_nop,
	arm_instr_multi_0x091b6830__eq,
	arm_instr_multi_0x091b6830__ne,
	arm_instr_multi_0x091b6830__cs,
	arm_instr_multi_0x091b6830__cc,
	arm_instr_multi_0x091b6830__mi,
	arm_instr_multi_0x091b6830__pl,
	arm_instr_multi_0x091b6830__vs,
	arm_instr_multi_0x091b6830__vc,
	arm_instr_multi_0x091b6830__hi,
	arm_instr_multi_0x091b6830__ls,
	arm_instr_multi_0x091b6830__ge,
	arm_instr_multi_0x091b6830__lt,
	arm_instr_multi_0x091b6830__gt,
	arm_instr_multi_0x091b6830__le,
	arm_instr_multi_0x091b6830,
	arm_instr_nop,
	arm_instr_multi_0x091bac30__eq,
	arm_instr_multi_0x091bac30__ne,
	arm_instr_multi_0x091bac30__cs,
	arm_instr_multi_0x091bac30__cc,
	arm_instr_multi_0x091bac30__mi,
	arm_instr_multi_0x091bac30__pl,
	arm_instr_multi_0x091bac30__vs,
	arm_instr_multi_0x091bac30__vc,
	arm_instr_multi_0x091bac30__hi,
	arm_instr_multi_0x091bac30__ls,
	arm_instr_multi_0x091bac30__ge,
	arm_instr_multi_0x091bac30__lt,
	arm_instr_multi_0x091bac30__gt,
	arm_instr_multi_0x091bac30__le,
	arm_instr_multi_0x091bac30,
	arm_instr_nop,
	arm_instr_multi_0x09315018__eq,
	arm_instr_multi_0x09315018__ne,
	arm_instr_multi_0x09315018__cs,
	arm_instr_multi_0x09315018__cc,
	arm_instr_multi_0x09315018__mi,
	arm_instr_multi_0x09315018__pl,
	arm_instr_multi_0x09315018__vs,
	arm_instr_multi_0x09315018__vc,
	arm_instr_multi_0x09315018__hi,
	arm_instr_multi_0x09315018__ls,
	arm_instr_multi_0x09315018__ge,
	arm_instr_multi_0x09315018__lt,
	arm_instr_multi_0x09315018__gt,
	arm_instr_multi_0x09315018__le,
	arm_instr_multi_0x09315018,
	arm_instr_nop,
	arm_instr_multi_0x091b6810__eq,
	arm_instr_multi_0x091b6810__ne,
	arm_instr_multi_0x091b6810__cs,
	arm_instr_multi_0x091b6810__cc,
	arm_instr_multi_0x091b6810__mi,
	arm_instr_multi_0x091b6810__pl,
	arm_instr_multi_0x091b6810__vs,
	arm_instr_multi_0x091b6810__vc,
	arm_instr_multi_0x091b6810__hi,
	arm_instr_multi_0x091b6810__ls,
	arm_instr_multi_0x091b6810__ge,
	arm_instr_multi_0x091b6810__lt,
	arm_instr_multi_0x091b6810__gt,
	arm_instr_multi_0x091b6810__le,
	arm_instr_multi_0x091b6810,
	arm_instr_nop,
	arm_instr_multi_0x09311038__eq,
	arm_instr_multi_0x09311038__ne,
	arm_instr_multi_0x09311038__cs,
	arm_instr_multi_0x09311038__cc,
	arm_instr_multi_0x09311038__mi,
	arm_instr_multi_0x09311038__pl,
	arm_instr_multi_0x09311038__vs,
	arm_instr_multi_0x09311038__vc,
	arm_instr_multi_0x09311038__hi,
	arm_instr_multi_0x09311038__ls,
	arm_instr_multi_0x09311038__ge,
	arm_instr_multi_0x09311038__lt,
	arm_instr_multi_0x09311038__gt,
	arm_instr_multi_0x09311038__le,
	arm_instr_multi_0x09311038,
	arm_instr_nop,
};
void (*multi_opcode_f_86[96])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x091ba8f0__eq,
	arm_instr_multi_0x091ba8f0__ne,
	arm_instr_multi_0x091ba8f0__cs,
	arm_instr_multi_0x091ba8f0__cc,
	arm_instr_multi_0x091ba8f0__mi,
	arm_instr_multi_0x091ba8f0__pl,
	arm_instr_multi_0x091ba8f0__vs,
	arm_instr_multi_0x091ba8f0__vc,
	arm_instr_multi_0x091ba8f0__hi,
	arm_instr_multi_0x091ba8f0__ls,
	arm_instr_multi_0x091ba8f0__ge,
	arm_instr_multi_0x091ba8f0__lt,
	arm_instr_multi_0x091ba8f0__gt,
	arm_instr_multi_0x091ba8f0__le,
	arm_instr_multi_0x091ba8f0,
	arm_instr_nop,
	arm_instr_multi_0x091ba870__eq,
	arm_instr_multi_0x091ba870__ne,
	arm_instr_multi_0x091ba870__cs,
	arm_instr_multi_0x091ba870__cc,
	arm_instr_multi_0x091ba870__mi,
	arm_instr_multi_0x091ba870__pl,
	arm_instr_multi_0x091ba870__vs,
	arm_instr_multi_0x091ba870__vc,
	arm_instr_multi_0x091ba870__hi,
	arm_instr_multi_0x091ba870__ls,
	arm_instr_multi_0x091ba870__ge,
	arm_instr_multi_0x091ba870__lt,
	arm_instr_multi_0x091ba870__gt,
	arm_instr_multi_0x091ba870__le,
	arm_instr_multi_0x091ba870,
	arm_instr_nop,
	arm_instr_multi_0x091bac70__eq,
	arm_instr_multi_0x091bac70__ne,
	arm_instr_multi_0x091bac70__cs,
	arm_instr_multi_0x091bac70__cc,
	arm_instr_multi_0x091bac70__mi,
	arm_instr_multi_0x091bac70__pl,
	arm_instr_multi_0x091bac70__vs,
	arm_instr_multi_0x091bac70__vc,
	arm_instr_multi_0x091bac70__hi,
	arm_instr_multi_0x091bac70__ls,
	arm_instr_multi_0x091bac70__ge,
	arm_instr_multi_0x091bac70__lt,
	arm_instr_multi_0x091bac70__gt,
	arm_instr_multi_0x091bac70__le,
	arm_instr_multi_0x091bac70,
	arm_instr_nop,
	arm_instr_multi_0x091bacf0__eq,
	arm_instr_multi_0x091bacf0__ne,
	arm_instr_multi_0x091bacf0__cs,
	arm_instr_multi_0x091bacf0__cc,
	arm_instr_multi_0x091bacf0__mi,
	arm_instr_multi_0x091bacf0__pl,
	arm_instr_multi_0x091bacf0__vs,
	arm_instr_multi_0x091bacf0__vc,
	arm_instr_multi_0x091bacf0__hi,
	arm_instr_multi_0x091bacf0__ls,
	arm_instr_multi_0x091bacf0__ge,
	arm_instr_multi_0x091bacf0__lt,
	arm_instr_multi_0x091bacf0__gt,
	arm_instr_multi_0x091bacf0__le,
	arm_instr_multi_0x091bacf0,
	arm_instr_nop,
	arm_instr_multi_0x091b6870__eq,
	arm_instr_multi_0x091b6870__ne,
	arm_instr_multi_0x091b6870__cs,
	arm_instr_multi_0x091b6870__cc,
	arm_instr_multi_0x091b6870__mi,
	arm_instr_multi_0x091b6870__pl,
	arm_instr_multi_0x091b6870__vs,
	arm_instr_multi_0x091b6870__vc,
	arm_instr_multi_0x091b6870__hi,
	arm_instr_multi_0x091b6870__ls,
	arm_instr_multi_0x091b6870__ge,
	arm_instr_multi_0x091b6870__lt,
	arm_instr_multi_0x091b6870__gt,
	arm_instr_multi_0x091b6870__le,
	arm_instr_multi_0x091b6870,
	arm_instr_nop,
	arm_instr_multi_0x091b68f0__eq,
	arm_instr_multi_0x091b68f0__ne,
	arm_instr_multi_0x091b68f0__cs,
	arm_instr_multi_0x091b68f0__cc,
	arm_instr_multi_0x091b68f0__mi,
	arm_instr_multi_0x091b68f0__pl,
	arm_instr_multi_0x091b68f0__vs,
	arm_instr_multi_0x091b68f0__vc,
	arm_instr_multi_0x091b68f0__hi,
	arm_instr_multi_0x091b68f0__ls,
	arm_instr_multi_0x091b68f0__ge,
	arm_instr_multi_0x091b68f0__lt,
	arm_instr_multi_0x091b68f0__gt,
	arm_instr_multi_0x091b68f0__le,
	arm_instr_multi_0x091b68f0,
	arm_instr_nop,
};
void (*multi_opcode_f_88[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09190300__eq,
	arm_instr_multi_0x09190300__ne,
	arm_instr_multi_0x09190300__cs,
	arm_instr_multi_0x09190300__cc,
	arm_instr_multi_0x09190300__mi,
	arm_instr_multi_0x09190300__pl,
	arm_instr_multi_0x09190300__vs,
	arm_instr_multi_0x09190300__vc,
	arm_instr_multi_0x09190300__hi,
	arm_instr_multi_0x09190300__ls,
	arm_instr_multi_0x09190300__ge,
	arm_instr_multi_0x09190300__lt,
	arm_instr_multi_0x09190300__gt,
	arm_instr_multi_0x09190300__le,
	arm_instr_multi_0x09190300,
	arm_instr_nop,
};
void (*multi_opcode_f_94[112])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x091baff0__eq,
	arm_instr_multi_0x091baff0__ne,
	arm_instr_multi_0x091baff0__cs,
	arm_instr_multi_0x091baff0__cc,
	arm_instr_multi_0x091baff0__mi,
	arm_instr_multi_0x091baff0__pl,
	arm_instr_multi_0x091baff0__vs,
	arm_instr_multi_0x091baff0__vc,
	arm_instr_multi_0x091baff0__hi,
	arm_instr_multi_0x091baff0__ls,
	arm_instr_multi_0x091baff0__ge,
	arm_instr_multi_0x091baff0__lt,
	arm_instr_multi_0x091baff0__gt,
	arm_instr_multi_0x091baff0__le,
	arm_instr_multi_0x091baff0,
	arm_instr_nop,
	arm_instr_multi_0x091badf0__eq,
	arm_instr_multi_0x091badf0__ne,
	arm_instr_multi_0x091badf0__cs,
	arm_instr_multi_0x091badf0__cc,
	arm_instr_multi_0x091badf0__mi,
	arm_instr_multi_0x091badf0__pl,
	arm_instr_multi_0x091badf0__vs,
	arm_instr_multi_0x091badf0__vc,
	arm_instr_multi_0x091badf0__hi,
	arm_instr_multi_0x091badf0__ls,
	arm_instr_multi_0x091badf0__ge,
	arm_instr_multi_0x091badf0__lt,
	arm_instr_multi_0x091badf0__gt,
	arm_instr_multi_0x091badf0__le,
	arm_instr_multi_0x091badf0,
	arm_instr_nop,
	arm_instr_multi_0x091ba9f0__eq,
	arm_instr_multi_0x091ba9f0__ne,
	arm_instr_multi_0x091ba9f0__cs,
	arm_instr_multi_0x091ba9f0__cc,
	arm_instr_multi_0x091ba9f0__mi,
	arm_instr_multi_0x091ba9f0__pl,
	arm_instr_multi_0x091ba9f0__vs,
	arm_instr_multi_0x091ba9f0__vc,
	arm_instr_multi_0x091ba9f0__hi,
	arm_instr_multi_0x091ba9f0__ls,
	arm_instr_multi_0x091ba9f0__ge,
	arm_instr_multi_0x091ba9f0__lt,
	arm_instr_multi_0x091ba9f0__gt,
	arm_instr_multi_0x091ba9f0__le,
	arm_instr_multi_0x091ba9f0,
	arm_instr_nop,
	arm_instr_multi_0x091b6ff0__eq,
	arm_instr_multi_0x091b6ff0__ne,
	arm_instr_multi_0x091b6ff0__cs,
	arm_instr_multi_0x091b6ff0__cc,
	arm_instr_multi_0x091b6ff0__mi,
	arm_instr_multi_0x091b6ff0__pl,
	arm_instr_multi_0x091b6ff0__vs,
	arm_instr_multi_0x091b6ff0__vc,
	arm_instr_multi_0x091b6ff0__hi,
	arm_instr_multi_0x091b6ff0__ls,
	arm_instr_multi_0x091b6ff0__ge,
	arm_instr_multi_0x091b6ff0__lt,
	arm_instr_multi_0x091b6ff0__gt,
	arm_instr_multi_0x091b6ff0__le,
	arm_instr_multi_0x091b6ff0,
	arm_instr_nop,
	arm_instr_multi_0x091babf0__eq,
	arm_instr_multi_0x091babf0__ne,
	arm_instr_multi_0x091babf0__cs,
	arm_instr_multi_0x091babf0__cc,
	arm_instr_multi_0x091babf0__mi,
	arm_instr_multi_0x091babf0__pl,
	arm_instr_multi_0x091babf0__vs,
	arm_instr_multi_0x091babf0__vc,
	arm_instr_multi_0x091babf0__hi,
	arm_instr_multi_0x091babf0__ls,
	arm_instr_multi_0x091babf0__ge,
	arm_instr_multi_0x091babf0__lt,
	arm_instr_multi_0x091babf0__gt,
	arm_instr_multi_0x091babf0__le,
	arm_instr_multi_0x091babf0,
	arm_instr_nop,
	arm_instr_multi_0x091b69f0__eq,
	arm_instr_multi_0x091b69f0__ne,
	arm_instr_multi_0x091b69f0__cs,
	arm_instr_multi_0x091b69f0__cc,
	arm_instr_multi_0x091b69f0__mi,
	arm_instr_multi_0x091b69f0__pl,
	arm_instr_multi_0x091b69f0__vs,
	arm_instr_multi_0x091b69f0__vc,
	arm_instr_multi_0x091b69f0__hi,
	arm_instr_multi_0x091b69f0__ls,
	arm_instr_multi_0x091b69f0__ge,
	arm_instr_multi_0x091b69f0__lt,
	arm_instr_multi_0x091b69f0__gt,
	arm_instr_multi_0x091b69f0__le,
	arm_instr_multi_0x091b69f0,
	arm_instr_nop,
	arm_instr_multi_0x091b6df0__eq,
	arm_instr_multi_0x091b6df0__ne,
	arm_instr_multi_0x091b6df0__cs,
	arm_instr_multi_0x091b6df0__cc,
	arm_instr_multi_0x091b6df0__mi,
	arm_instr_multi_0x091b6df0__pl,
	arm_instr_multi_0x091b6df0__vs,
	arm_instr_multi_0x091b6df0__vc,
	arm_instr_multi_0x091b6df0__hi,
	arm_instr_multi_0x091b6df0__ls,
	arm_instr_multi_0x091b6df0__ge,
	arm_instr_multi_0x091b6df0__lt,
	arm_instr_multi_0x091b6df0__gt,
	arm_instr_multi_0x091b6df0__le,
	arm_instr_multi_0x091b6df0,
	arm_instr_nop,
};
void (*multi_opcode_f_97[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09160006__eq,
	arm_instr_multi_0x09160006__ne,
	arm_instr_multi_0x09160006__cs,
	arm_instr_multi_0x09160006__cc,
	arm_instr_multi_0x09160006__mi,
	arm_instr_multi_0x09160006__pl,
	arm_instr_multi_0x09160006__vs,
	arm_instr_multi_0x09160006__vc,
	arm_instr_multi_0x09160006__hi,
	arm_instr_multi_0x09160006__ls,
	arm_instr_multi_0x09160006__ge,
	arm_instr_multi_0x09160006__lt,
	arm_instr_multi_0x09160006__gt,
	arm_instr_multi_0x09160006__le,
	arm_instr_multi_0x09160006,
	arm_instr_nop,
	arm_instr_multi_0x091c0006__eq,
	arm_instr_multi_0x091c0006__ne,
	arm_instr_multi_0x091c0006__cs,
	arm_instr_multi_0x091c0006__cc,
	arm_instr_multi_0x091c0006__mi,
	arm_instr_multi_0x091c0006__pl,
	arm_instr_multi_0x091c0006__vs,
	arm_instr_multi_0x091c0006__vc,
	arm_instr_multi_0x091c0006__hi,
	arm_instr_multi_0x091c0006__ls,
	arm_instr_multi_0x091c0006__ge,
	arm_instr_multi_0x091c0006__lt,
	arm_instr_multi_0x091c0006__gt,
	arm_instr_multi_0x091c0006__le,
	arm_instr_multi_0x091c0006,
	arm_instr_nop,
};
void (*multi_opcode_f_98[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09140018__eq,
	arm_instr_multi_0x09140018__ne,
	arm_instr_multi_0x09140018__cs,
	arm_instr_multi_0x09140018__cc,
	arm_instr_multi_0x09140018__mi,
	arm_instr_multi_0x09140018__pl,
	arm_instr_multi_0x09140018__vs,
	arm_instr_multi_0x09140018__vc,
	arm_instr_multi_0x09140018__hi,
	arm_instr_multi_0x09140018__ls,
	arm_instr_multi_0x09140018__ge,
	arm_instr_multi_0x09140018__lt,
	arm_instr_multi_0x09140018__gt,
	arm_instr_multi_0x09140018__le,
	arm_instr_multi_0x09140018,
	arm_instr_nop,
};
void (*multi_opcode_f_100[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09160060__eq,
	arm_instr_multi_0x09160060__ne,
	arm_instr_multi_0x09160060__cs,
	arm_instr_multi_0x09160060__cc,
	arm_instr_multi_0x09160060__mi,
	arm_instr_multi_0x09160060__pl,
	arm_instr_multi_0x09160060__vs,
	arm_instr_multi_0x09160060__vc,
	arm_instr_multi_0x09160060__hi,
	arm_instr_multi_0x09160060__ls,
	arm_instr_multi_0x09160060__ge,
	arm_instr_multi_0x09160060__lt,
	arm_instr_multi_0x09160060__gt,
	arm_instr_multi_0x09160060__le,
	arm_instr_multi_0x09160060,
	arm_instr_nop,
	arm_instr_multi_0x08160060__eq,
	arm_instr_multi_0x08160060__ne,
	arm_instr_multi_0x08160060__cs,
	arm_instr_multi_0x08160060__cc,
	arm_instr_multi_0x08160060__mi,
	arm_instr_multi_0x08160060__pl,
	arm_instr_multi_0x08160060__vs,
	arm_instr_multi_0x08160060__vc,
	arm_instr_multi_0x08160060__hi,
	arm_instr_multi_0x08160060__ls,
	arm_instr_multi_0x08160060__ge,
	arm_instr_multi_0x08160060__lt,
	arm_instr_multi_0x08160060__gt,
	arm_instr_multi_0x08160060__le,
	arm_instr_multi_0x08160060,
	arm_instr_nop,
};
void (*multi_opcode_f_112[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08150003__eq,
	arm_instr_multi_0x08150003__ne,
	arm_instr_multi_0x08150003__cs,
	arm_instr_multi_0x08150003__cc,
	arm_instr_multi_0x08150003__mi,
	arm_instr_multi_0x08150003__pl,
	arm_instr_multi_0x08150003__vs,
	arm_instr_multi_0x08150003__vc,
	arm_instr_multi_0x08150003__hi,
	arm_instr_multi_0x08150003__ls,
	arm_instr_multi_0x08150003__ge,
	arm_instr_multi_0x08150003__lt,
	arm_instr_multi_0x08150003__gt,
	arm_instr_multi_0x08150003__le,
	arm_instr_multi_0x08150003,
	arm_instr_nop,
};
void (*multi_opcode_f_113[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x0817000c__eq,
	arm_instr_multi_0x0817000c__ne,
	arm_instr_multi_0x0817000c__cs,
	arm_instr_multi_0x0817000c__cc,
	arm_instr_multi_0x0817000c__mi,
	arm_instr_multi_0x0817000c__pl,
	arm_instr_multi_0x0817000c__vs,
	arm_instr_multi_0x0817000c__vc,
	arm_instr_multi_0x0817000c__hi,
	arm_instr_multi_0x0817000c__ls,
	arm_instr_multi_0x0817000c__ge,
	arm_instr_multi_0x0817000c__lt,
	arm_instr_multi_0x0817000c__gt,
	arm_instr_multi_0x0817000c__le,
	arm_instr_multi_0x0817000c,
	arm_instr_nop,
	arm_instr_multi_0x09150006__eq,
	arm_instr_multi_0x09150006__ne,
	arm_instr_multi_0x09150006__cs,
	arm_instr_multi_0x09150006__cc,
	arm_instr_multi_0x09150006__mi,
	arm_instr_multi_0x09150006__pl,
	arm_instr_multi_0x09150006__vs,
	arm_instr_multi_0x09150006__vc,
	arm_instr_multi_0x09150006__hi,
	arm_instr_multi_0x09150006__ls,
	arm_instr_multi_0x09150006__ge,
	arm_instr_multi_0x09150006__lt,
	arm_instr_multi_0x09150006__gt,
	arm_instr_multi_0x09150006__le,
	arm_instr_multi_0x09150006,
	arm_instr_nop,
};
void (*multi_opcode_f_114[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09150018__eq,
	arm_instr_multi_0x09150018__ne,
	arm_instr_multi_0x09150018__cs,
	arm_instr_multi_0x09150018__cc,
	arm_instr_multi_0x09150018__mi,
	arm_instr_multi_0x09150018__pl,
	arm_instr_multi_0x09150018__vs,
	arm_instr_multi_0x09150018__vc,
	arm_instr_multi_0x09150018__hi,
	arm_instr_multi_0x09150018__ls,
	arm_instr_multi_0x09150018__ge,
	arm_instr_multi_0x09150018__lt,
	arm_instr_multi_0x09150018__gt,
	arm_instr_multi_0x09150018__le,
	arm_instr_multi_0x09150018,
	arm_instr_nop,
};
void (*multi_opcode_f_128[64])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08820003__eq,
	arm_instr_multi_0x08820003__ne,
	arm_instr_multi_0x08820003__cs,
	arm_instr_multi_0x08820003__cc,
	arm_instr_multi_0x08820003__mi,
	arm_instr_multi_0x08820003__pl,
	arm_instr_multi_0x08820003__vs,
	arm_instr_multi_0x08820003__vc,
	arm_instr_multi_0x08820003__hi,
	arm_instr_multi_0x08820003__ls,
	arm_instr_multi_0x08820003__ge,
	arm_instr_multi_0x08820003__lt,
	arm_instr_multi_0x08820003__gt,
	arm_instr_multi_0x08820003__le,
	arm_instr_multi_0x08820003,
	arm_instr_nop,
	arm_instr_multi_0x08a01008__eq,
	arm_instr_multi_0x08a01008__ne,
	arm_instr_multi_0x08a01008__cs,
	arm_instr_multi_0x08a01008__cc,
	arm_instr_multi_0x08a01008__mi,
	arm_instr_multi_0x08a01008__pl,
	arm_instr_multi_0x08a01008__vs,
	arm_instr_multi_0x08a01008__vc,
	arm_instr_multi_0x08a01008__hi,
	arm_instr_multi_0x08a01008__ls,
	arm_instr_multi_0x08a01008__ge,
	arm_instr_multi_0x08a01008__lt,
	arm_instr_multi_0x08a01008__gt,
	arm_instr_multi_0x08a01008__le,
	arm_instr_multi_0x08a01008,
	arm_instr_nop,
	arm_instr_multi_0x08a05008__eq,
	arm_instr_multi_0x08a05008__ne,
	arm_instr_multi_0x08a05008__cs,
	arm_instr_multi_0x08a05008__cc,
	arm_instr_multi_0x08a05008__mi,
	arm_instr_multi_0x08a05008__pl,
	arm_instr_multi_0x08a05008__vs,
	arm_instr_multi_0x08a05008__vc,
	arm_instr_multi_0x08a05008__hi,
	arm_instr_multi_0x08a05008__ls,
	arm_instr_multi_0x08a05008__ge,
	arm_instr_multi_0x08a05008__lt,
	arm_instr_multi_0x08a05008__gt,
	arm_instr_multi_0x08a05008__le,
	arm_instr_multi_0x08a05008,
	arm_instr_nop,
	arm_instr_multi_0x08a20600__eq,
	arm_instr_multi_0x08a20600__ne,
	arm_instr_multi_0x08a20600__cs,
	arm_instr_multi_0x08a20600__cc,
	arm_instr_multi_0x08a20600__mi,
	arm_instr_multi_0x08a20600__pl,
	arm_instr_multi_0x08a20600__vs,
	arm_instr_multi_0x08a20600__vc,
	arm_instr_multi_0x08a20600__hi,
	arm_instr_multi_0x08a20600__ls,
	arm_instr_multi_0x08a20600__ge,
	arm_instr_multi_0x08a20600__lt,
	arm_instr_multi_0x08a20600__gt,
	arm_instr_multi_0x08a20600__le,
	arm_instr_multi_0x08a20600,
	arm_instr_nop,
};
void (*multi_opcode_f_129[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08800006__eq,
	arm_instr_multi_0x08800006__ne,
	arm_instr_multi_0x08800006__cs,
	arm_instr_multi_0x08800006__cc,
	arm_instr_multi_0x08800006__mi,
	arm_instr_multi_0x08800006__pl,
	arm_instr_multi_0x08800006__vs,
	arm_instr_multi_0x08800006__vc,
	arm_instr_multi_0x08800006__hi,
	arm_instr_multi_0x08800006__ls,
	arm_instr_multi_0x08800006__ge,
	arm_instr_multi_0x08800006__lt,
	arm_instr_multi_0x08800006__gt,
	arm_instr_multi_0x08800006__le,
	arm_instr_multi_0x08800006,
	arm_instr_nop,
	arm_instr_multi_0x08880006__eq,
	arm_instr_multi_0x08880006__ne,
	arm_instr_multi_0x08880006__cs,
	arm_instr_multi_0x08880006__cc,
	arm_instr_multi_0x08880006__mi,
	arm_instr_multi_0x08880006__pl,
	arm_instr_multi_0x08880006__vs,
	arm_instr_multi_0x08880006__vc,
	arm_instr_multi_0x08880006__hi,
	arm_instr_multi_0x08880006__ls,
	arm_instr_multi_0x08880006__ge,
	arm_instr_multi_0x08880006__lt,
	arm_instr_multi_0x08880006__gt,
	arm_instr_multi_0x08880006__le,
	arm_instr_multi_0x08880006,
	arm_instr_nop,
};
void (*multi_opcode_f_130[96])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08820018__eq,
	arm_instr_multi_0x08820018__ne,
	arm_instr_multi_0x08820018__cs,
	arm_instr_multi_0x08820018__cc,
	arm_instr_multi_0x08820018__mi,
	arm_instr_multi_0x08820018__pl,
	arm_instr_multi_0x08820018__vs,
	arm_instr_multi_0x08820018__vc,
	arm_instr_multi_0x08820018__hi,
	arm_instr_multi_0x08820018__ls,
	arm_instr_multi_0x08820018__ge,
	arm_instr_multi_0x08820018__lt,
	arm_instr_multi_0x08820018__gt,
	arm_instr_multi_0x08820018__le,
	arm_instr_multi_0x08820018,
	arm_instr_nop,
	arm_instr_multi_0x08a05018__eq,
	arm_instr_multi_0x08a05018__ne,
	arm_instr_multi_0x08a05018__cs,
	arm_instr_multi_0x08a05018__cc,
	arm_instr_multi_0x08a05018__mi,
	arm_instr_multi_0x08a05018__pl,
	arm_instr_multi_0x08a05018__vs,
	arm_instr_multi_0x08a05018__vc,
	arm_instr_multi_0x08a05018__hi,
	arm_instr_multi_0x08a05018__ls,
	arm_instr_multi_0x08a05018__ge,
	arm_instr_multi_0x08a05018__lt,
	arm_instr_multi_0x08a05018__gt,
	arm_instr_multi_0x08a05018__le,
	arm_instr_multi_0x08a05018,
	arm_instr_nop,
	arm_instr_multi_0x08880018__eq,
	arm_instr_multi_0x08880018__ne,
	arm_instr_multi_0x08880018__cs,
	arm_instr_multi_0x08880018__cc,
	arm_instr_multi_0x08880018__mi,
	arm_instr_multi_0x08880018__pl,
	arm_instr_multi_0x08880018__vs,
	arm_instr_multi_0x08880018__vc,
	arm_instr_multi_0x08880018__hi,
	arm_instr_multi_0x08880018__ls,
	arm_instr_multi_0x08880018__ge,
	arm_instr_multi_0x08880018__lt,
	arm_instr_multi_0x08880018__gt,
	arm_instr_multi_0x08880018__le,
	arm_instr_multi_0x08880018,
	arm_instr_nop,
	arm_instr_multi_0x08820030__eq,
	arm_instr_multi_0x08820030__ne,
	arm_instr_multi_0x08820030__cs,
	arm_instr_multi_0x08820030__cc,
	arm_instr_multi_0x08820030__mi,
	arm_instr_multi_0x08820030__pl,
	arm_instr_multi_0x08820030__vs,
	arm_instr_multi_0x08820030__vc,
	arm_instr_multi_0x08820030__hi,
	arm_instr_multi_0x08820030__ls,
	arm_instr_multi_0x08820030__ge,
	arm_instr_multi_0x08820030__lt,
	arm_instr_multi_0x08820030__gt,
	arm_instr_multi_0x08820030__le,
	arm_instr_multi_0x08820030,
	arm_instr_nop,
	arm_instr_multi_0x08800018__eq,
	arm_instr_multi_0x08800018__ne,
	arm_instr_multi_0x08800018__cs,
	arm_instr_multi_0x08800018__cc,
	arm_instr_multi_0x08800018__mi,
	arm_instr_multi_0x08800018__pl,
	arm_instr_multi_0x08800018__vs,
	arm_instr_multi_0x08800018__vc,
	arm_instr_multi_0x08800018__hi,
	arm_instr_multi_0x08800018__ls,
	arm_instr_multi_0x08800018__ge,
	arm_instr_multi_0x08800018__lt,
	arm_instr_multi_0x08800018__gt,
	arm_instr_multi_0x08800018__le,
	arm_instr_multi_0x08800018,
	arm_instr_nop,
	arm_instr_multi_0x08800030__eq,
	arm_instr_multi_0x08800030__ne,
	arm_instr_multi_0x08800030__cs,
	arm_instr_multi_0x08800030__cc,
	arm_instr_multi_0x08800030__mi,
	arm_instr_multi_0x08800030__pl,
	arm_instr_multi_0x08800030__vs,
	arm_instr_multi_0x08800030__vc,
	arm_instr_multi_0x08800030__hi,
	arm_instr_multi_0x08800030__ls,
	arm_instr_multi_0x08800030__ge,
	arm_instr_multi_0x08800030__lt,
	arm_instr_multi_0x08800030__gt,
	arm_instr_multi_0x08800030__le,
	arm_instr_multi_0x08800030,
	arm_instr_nop,
};
void (*multi_opcode_f_132[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x088200c0__eq,
	arm_instr_multi_0x088200c0__ne,
	arm_instr_multi_0x088200c0__cs,
	arm_instr_multi_0x088200c0__cc,
	arm_instr_multi_0x088200c0__mi,
	arm_instr_multi_0x088200c0__pl,
	arm_instr_multi_0x088200c0__vs,
	arm_instr_multi_0x088200c0__vc,
	arm_instr_multi_0x088200c0__hi,
	arm_instr_multi_0x088200c0__ls,
	arm_instr_multi_0x088200c0__ge,
	arm_instr_multi_0x088200c0__lt,
	arm_instr_multi_0x088200c0__gt,
	arm_instr_multi_0x088200c0__le,
	arm_instr_multi_0x088200c0,
	arm_instr_nop,
};
void (*multi_opcode_f_136[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08820180__eq,
	arm_instr_multi_0x08820180__ne,
	arm_instr_multi_0x08820180__cs,
	arm_instr_multi_0x08820180__cc,
	arm_instr_multi_0x08820180__mi,
	arm_instr_multi_0x08820180__pl,
	arm_instr_multi_0x08820180__vs,
	arm_instr_multi_0x08820180__vc,
	arm_instr_multi_0x08820180__hi,
	arm_instr_multi_0x08820180__ls,
	arm_instr_multi_0x08820180__ge,
	arm_instr_multi_0x08820180__lt,
	arm_instr_multi_0x08820180__gt,
	arm_instr_multi_0x08820180__le,
	arm_instr_multi_0x08820180,
	arm_instr_nop,
	arm_instr_multi_0x08800180__eq,
	arm_instr_multi_0x08800180__ne,
	arm_instr_multi_0x08800180__cs,
	arm_instr_multi_0x08800180__cc,
	arm_instr_multi_0x08800180__mi,
	arm_instr_multi_0x08800180__pl,
	arm_instr_multi_0x08800180__vs,
	arm_instr_multi_0x08800180__vc,
	arm_instr_multi_0x08800180__hi,
	arm_instr_multi_0x08800180__ls,
	arm_instr_multi_0x08800180__ge,
	arm_instr_multi_0x08800180__lt,
	arm_instr_multi_0x08800180__gt,
	arm_instr_multi_0x08800180__le,
	arm_instr_multi_0x08800180,
	arm_instr_nop,
};
void (*multi_opcode_f_142[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08a051f8__eq,
	arm_instr_multi_0x08a051f8__ne,
	arm_instr_multi_0x08a051f8__cs,
	arm_instr_multi_0x08a051f8__cc,
	arm_instr_multi_0x08a051f8__mi,
	arm_instr_multi_0x08a051f8__pl,
	arm_instr_multi_0x08a051f8__vs,
	arm_instr_multi_0x08a051f8__vc,
	arm_instr_multi_0x08a051f8__hi,
	arm_instr_multi_0x08a051f8__ls,
	arm_instr_multi_0x08a051f8__ge,
	arm_instr_multi_0x08a051f8__lt,
	arm_instr_multi_0x08a051f8__gt,
	arm_instr_multi_0x08a051f8__le,
	arm_instr_multi_0x08a051f8,
	arm_instr_nop,
	arm_instr_multi_0x08807ff0__eq,
	arm_instr_multi_0x08807ff0__ne,
	arm_instr_multi_0x08807ff0__cs,
	arm_instr_multi_0x08807ff0__cc,
	arm_instr_multi_0x08807ff0__mi,
	arm_instr_multi_0x08807ff0__pl,
	arm_instr_multi_0x08807ff0__vs,
	arm_instr_multi_0x08807ff0__vc,
	arm_instr_multi_0x08807ff0__hi,
	arm_instr_multi_0x08807ff0__ls,
	arm_instr_multi_0x08807ff0__ge,
	arm_instr_multi_0x08807ff0__lt,
	arm_instr_multi_0x08807ff0__gt,
	arm_instr_multi_0x08807ff0__le,
	arm_instr_multi_0x08807ff0,
	arm_instr_nop,
};
void (*multi_opcode_f_144[64])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08830600__eq,
	arm_instr_multi_0x08830600__ne,
	arm_instr_multi_0x08830600__cs,
	arm_instr_multi_0x08830600__cc,
	arm_instr_multi_0x08830600__mi,
	arm_instr_multi_0x08830600__pl,
	arm_instr_multi_0x08830600__vs,
	arm_instr_multi_0x08830600__vc,
	arm_instr_multi_0x08830600__hi,
	arm_instr_multi_0x08830600__ls,
	arm_instr_multi_0x08830600__ge,
	arm_instr_multi_0x08830600__lt,
	arm_instr_multi_0x08830600__gt,
	arm_instr_multi_0x08830600__le,
	arm_instr_multi_0x08830600,
	arm_instr_nop,
	arm_instr_multi_0x08810600__eq,
	arm_instr_multi_0x08810600__ne,
	arm_instr_multi_0x08810600__cs,
	arm_instr_multi_0x08810600__cc,
	arm_instr_multi_0x08810600__mi,
	arm_instr_multi_0x08810600__pl,
	arm_instr_multi_0x08810600__vs,
	arm_instr_multi_0x08810600__vc,
	arm_instr_multi_0x08810600__hi,
	arm_instr_multi_0x08810600__ls,
	arm_instr_multi_0x08810600__ge,
	arm_instr_multi_0x08810600__lt,
	arm_instr_multi_0x08810600__gt,
	arm_instr_multi_0x08810600__le,
	arm_instr_multi_0x08810600,
	arm_instr_nop,
	arm_instr_multi_0x098b0003__eq,
	arm_instr_multi_0x098b0003__ne,
	arm_instr_multi_0x098b0003__cs,
	arm_instr_multi_0x098b0003__cc,
	arm_instr_multi_0x098b0003__mi,
	arm_instr_multi_0x098b0003__pl,
	arm_instr_multi_0x098b0003__vs,
	arm_instr_multi_0x098b0003__vc,
	arm_instr_multi_0x098b0003__hi,
	arm_instr_multi_0x098b0003__ls,
	arm_instr_multi_0x098b0003__ge,
	arm_instr_multi_0x098b0003__lt,
	arm_instr_multi_0x098b0003__gt,
	arm_instr_multi_0x098b0003__le,
	arm_instr_multi_0x098b0003,
	arm_instr_nop,
	arm_instr_multi_0x08830003__eq,
	arm_instr_multi_0x08830003__ne,
	arm_instr_multi_0x08830003__cs,
	arm_instr_multi_0x08830003__cc,
	arm_instr_multi_0x08830003__mi,
	arm_instr_multi_0x08830003__pl,
	arm_instr_multi_0x08830003__vs,
	arm_instr_multi_0x08830003__vc,
	arm_instr_multi_0x08830003__hi,
	arm_instr_multi_0x08830003__ls,
	arm_instr_multi_0x08830003__ge,
	arm_instr_multi_0x08830003__lt,
	arm_instr_multi_0x08830003__gt,
	arm_instr_multi_0x08830003__le,
	arm_instr_multi_0x08830003,
	arm_instr_nop,
};
void (*multi_opcode_f_145[64])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08830006__eq,
	arm_instr_multi_0x08830006__ne,
	arm_instr_multi_0x08830006__cs,
	arm_instr_multi_0x08830006__cc,
	arm_instr_multi_0x08830006__mi,
	arm_instr_multi_0x08830006__pl,
	arm_instr_multi_0x08830006__vs,
	arm_instr_multi_0x08830006__vc,
	arm_instr_multi_0x08830006__hi,
	arm_instr_multi_0x08830006__ls,
	arm_instr_multi_0x08830006__ge,
	arm_instr_multi_0x08830006__lt,
	arm_instr_multi_0x08830006__gt,
	arm_instr_multi_0x08830006__le,
	arm_instr_multi_0x08830006,
	arm_instr_nop,
	arm_instr_multi_0x08890006__eq,
	arm_instr_multi_0x08890006__ne,
	arm_instr_multi_0x08890006__cs,
	arm_instr_multi_0x08890006__cc,
	arm_instr_multi_0x08890006__mi,
	arm_instr_multi_0x08890006__pl,
	arm_instr_multi_0x08890006__vs,
	arm_instr_multi_0x08890006__vc,
	arm_instr_multi_0x08890006__hi,
	arm_instr_multi_0x08890006__ls,
	arm_instr_multi_0x08890006__ge,
	arm_instr_multi_0x08890006__lt,
	arm_instr_multi_0x08890006__gt,
	arm_instr_multi_0x08890006__le,
	arm_instr_multi_0x08890006,
	arm_instr_nop,
	arm_instr_multi_0x09830006__eq,
	arm_instr_multi_0x09830006__ne,
	arm_instr_multi_0x09830006__cs,
	arm_instr_multi_0x09830006__cc,
	arm_instr_multi_0x09830006__mi,
	arm_instr_multi_0x09830006__pl,
	arm_instr_multi_0x09830006__vs,
	arm_instr_multi_0x09830006__vc,
	arm_instr_multi_0x09830006__hi,
	arm_instr_multi_0x09830006__ls,
	arm_instr_multi_0x09830006__ge,
	arm_instr_multi_0x09830006__lt,
	arm_instr_multi_0x09830006__gt,
	arm_instr_multi_0x09830006__le,
	arm_instr_multi_0x09830006,
	arm_instr_nop,
	arm_instr_multi_0x0989000c__eq,
	arm_instr_multi_0x0989000c__ne,
	arm_instr_multi_0x0989000c__cs,
	arm_instr_multi_0x0989000c__cc,
	arm_instr_multi_0x0989000c__mi,
	arm_instr_multi_0x0989000c__pl,
	arm_instr_multi_0x0989000c__vs,
	arm_instr_multi_0x0989000c__vc,
	arm_instr_multi_0x0989000c__hi,
	arm_instr_multi_0x0989000c__ls,
	arm_instr_multi_0x0989000c__ge,
	arm_instr_multi_0x0989000c__lt,
	arm_instr_multi_0x0989000c__gt,
	arm_instr_multi_0x0989000c__le,
	arm_instr_multi_0x0989000c,
	arm_instr_nop,
};
void (*multi_opcode_f_146[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08810018__eq,
	arm_instr_multi_0x08810018__ne,
	arm_instr_multi_0x08810018__cs,
	arm_instr_multi_0x08810018__cc,
	arm_instr_multi_0x08810018__mi,
	arm_instr_multi_0x08810018__pl,
	arm_instr_multi_0x08810018__vs,
	arm_instr_multi_0x08810018__vc,
	arm_instr_multi_0x08810018__hi,
	arm_instr_multi_0x08810018__ls,
	arm_instr_multi_0x08810018__ge,
	arm_instr_multi_0x08810018__lt,
	arm_instr_multi_0x08810018__gt,
	arm_instr_multi_0x08810018__le,
	arm_instr_multi_0x08810018,
	arm_instr_nop,
	arm_instr_multi_0x08830030__eq,
	arm_instr_multi_0x08830030__ne,
	arm_instr_multi_0x08830030__cs,
	arm_instr_multi_0x08830030__cc,
	arm_instr_multi_0x08830030__mi,
	arm_instr_multi_0x08830030__pl,
	arm_instr_multi_0x08830030__vs,
	arm_instr_multi_0x08830030__vc,
	arm_instr_multi_0x08830030__hi,
	arm_instr_multi_0x08830030__ls,
	arm_instr_multi_0x08830030__ge,
	arm_instr_multi_0x08830030__lt,
	arm_instr_multi_0x08830030__gt,
	arm_instr_multi_0x08830030__le,
	arm_instr_multi_0x08830030,
	arm_instr_nop,
	arm_instr_multi_0x08890030__eq,
	arm_instr_multi_0x08890030__ne,
	arm_instr_multi_0x08890030__cs,
	arm_instr_multi_0x08890030__cc,
	arm_instr_multi_0x08890030__mi,
	arm_instr_multi_0x08890030__pl,
	arm_instr_multi_0x08890030__vs,
	arm_instr_multi_0x08890030__vc,
	arm_instr_multi_0x08890030__hi,
	arm_instr_multi_0x08890030__ls,
	arm_instr_multi_0x08890030__ge,
	arm_instr_multi_0x08890030__lt,
	arm_instr_multi_0x08890030__gt,
	arm_instr_multi_0x08890030__le,
	arm_instr_multi_0x08890030,
	arm_instr_nop,
};
void (*multi_opcode_f_148[64])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08830060__eq,
	arm_instr_multi_0x08830060__ne,
	arm_instr_multi_0x08830060__cs,
	arm_instr_multi_0x08830060__cc,
	arm_instr_multi_0x08830060__mi,
	arm_instr_multi_0x08830060__pl,
	arm_instr_multi_0x08830060__vs,
	arm_instr_multi_0x08830060__vc,
	arm_instr_multi_0x08830060__hi,
	arm_instr_multi_0x08830060__ls,
	arm_instr_multi_0x08830060__ge,
	arm_instr_multi_0x08830060__lt,
	arm_instr_multi_0x08830060__gt,
	arm_instr_multi_0x08830060__le,
	arm_instr_multi_0x08830060,
	arm_instr_nop,
	arm_instr_multi_0x08a100c0__eq,
	arm_instr_multi_0x08a100c0__ne,
	arm_instr_multi_0x08a100c0__cs,
	arm_instr_multi_0x08a100c0__cc,
	arm_instr_multi_0x08a100c0__mi,
	arm_instr_multi_0x08a100c0__pl,
	arm_instr_multi_0x08a100c0__vs,
	arm_instr_multi_0x08a100c0__vc,
	arm_instr_multi_0x08a100c0__hi,
	arm_instr_multi_0x08a100c0__ls,
	arm_instr_multi_0x08a100c0__ge,
	arm_instr_multi_0x08a100c0__lt,
	arm_instr_multi_0x08a100c0__gt,
	arm_instr_multi_0x08a100c0__le,
	arm_instr_multi_0x08a100c0,
	arm_instr_nop,
	arm_instr_multi_0x088900c0__eq,
	arm_instr_multi_0x088900c0__ne,
	arm_instr_multi_0x088900c0__cs,
	arm_instr_multi_0x088900c0__cc,
	arm_instr_multi_0x088900c0__mi,
	arm_instr_multi_0x088900c0__pl,
	arm_instr_multi_0x088900c0__vs,
	arm_instr_multi_0x088900c0__vc,
	arm_instr_multi_0x088900c0__hi,
	arm_instr_multi_0x088900c0__ls,
	arm_instr_multi_0x088900c0__ge,
	arm_instr_multi_0x088900c0__lt,
	arm_instr_multi_0x088900c0__gt,
	arm_instr_multi_0x088900c0__le,
	arm_instr_multi_0x088900c0,
	arm_instr_nop,
	arm_instr_multi_0x088300c0__eq,
	arm_instr_multi_0x088300c0__ne,
	arm_instr_multi_0x088300c0__cs,
	arm_instr_multi_0x088300c0__cc,
	arm_instr_multi_0x088300c0__mi,
	arm_instr_multi_0x088300c0__pl,
	arm_instr_multi_0x088300c0__vs,
	arm_instr_multi_0x088300c0__vc,
	arm_instr_multi_0x088300c0__hi,
	arm_instr_multi_0x088300c0__ls,
	arm_instr_multi_0x088300c0__ge,
	arm_instr_multi_0x088300c0__lt,
	arm_instr_multi_0x088300c0__gt,
	arm_instr_multi_0x088300c0__le,
	arm_instr_multi_0x088300c0,
	arm_instr_nop,
};
void (*multi_opcode_f_152[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08a10300__eq,
	arm_instr_multi_0x08a10300__ne,
	arm_instr_multi_0x08a10300__cs,
	arm_instr_multi_0x08a10300__cc,
	arm_instr_multi_0x08a10300__mi,
	arm_instr_multi_0x08a10300__pl,
	arm_instr_multi_0x08a10300__vs,
	arm_instr_multi_0x08a10300__vc,
	arm_instr_multi_0x08a10300__hi,
	arm_instr_multi_0x08a10300__ls,
	arm_instr_multi_0x08a10300__ge,
	arm_instr_multi_0x08a10300__lt,
	arm_instr_multi_0x08a10300__gt,
	arm_instr_multi_0x08a10300__le,
	arm_instr_multi_0x08a10300,
	arm_instr_nop,
	arm_instr_multi_0x08a10f00__eq,
	arm_instr_multi_0x08a10f00__ne,
	arm_instr_multi_0x08a10f00__cs,
	arm_instr_multi_0x08a10f00__cc,
	arm_instr_multi_0x08a10f00__mi,
	arm_instr_multi_0x08a10f00__pl,
	arm_instr_multi_0x08a10f00__vs,
	arm_instr_multi_0x08a10f00__vc,
	arm_instr_multi_0x08a10f00__hi,
	arm_instr_multi_0x08a10f00__ls,
	arm_instr_multi_0x08a10f00__ge,
	arm_instr_multi_0x08a10f00__lt,
	arm_instr_multi_0x08a10f00__gt,
	arm_instr_multi_0x08a10f00__le,
	arm_instr_multi_0x08a10f00,
	arm_instr_nop,
	arm_instr_multi_0x08830300__eq,
	arm_instr_multi_0x08830300__ne,
	arm_instr_multi_0x08830300__cs,
	arm_instr_multi_0x08830300__cc,
	arm_instr_multi_0x08830300__mi,
	arm_instr_multi_0x08830300__pl,
	arm_instr_multi_0x08830300__vs,
	arm_instr_multi_0x08830300__vc,
	arm_instr_multi_0x08830300__hi,
	arm_instr_multi_0x08830300__ls,
	arm_instr_multi_0x08830300__ge,
	arm_instr_multi_0x08830300__lt,
	arm_instr_multi_0x08830300__gt,
	arm_instr_multi_0x08830300__le,
	arm_instr_multi_0x08830300,
	arm_instr_nop,
};
void (*multi_opcode_f_158[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08a151f8__eq,
	arm_instr_multi_0x08a151f8__ne,
	arm_instr_multi_0x08a151f8__cs,
	arm_instr_multi_0x08a151f8__cc,
	arm_instr_multi_0x08a151f8__mi,
	arm_instr_multi_0x08a151f8__pl,
	arm_instr_multi_0x08a151f8__vs,
	arm_instr_multi_0x08a151f8__vc,
	arm_instr_multi_0x08a151f8__hi,
	arm_instr_multi_0x08a151f8__ls,
	arm_instr_multi_0x08a151f8__ge,
	arm_instr_multi_0x08a151f8__lt,
	arm_instr_multi_0x08a151f8__gt,
	arm_instr_multi_0x08a151f8__le,
	arm_instr_multi_0x08a151f8,
	arm_instr_nop,
};
void (*multi_opcode_f_160[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08840003__eq,
	arm_instr_multi_0x08840003__ne,
	arm_instr_multi_0x08840003__cs,
	arm_instr_multi_0x08840003__cc,
	arm_instr_multi_0x08840003__mi,
	arm_instr_multi_0x08840003__pl,
	arm_instr_multi_0x08840003__vs,
	arm_instr_multi_0x08840003__vc,
	arm_instr_multi_0x08840003__hi,
	arm_instr_multi_0x08840003__ls,
	arm_instr_multi_0x08840003__ge,
	arm_instr_multi_0x08840003__lt,
	arm_instr_multi_0x08840003__gt,
	arm_instr_multi_0x08840003__le,
	arm_instr_multi_0x08840003,
	arm_instr_nop,
	arm_instr_multi_0x088e1002__eq,
	arm_instr_multi_0x088e1002__ne,
	arm_instr_multi_0x088e1002__cs,
	arm_instr_multi_0x088e1002__cc,
	arm_instr_multi_0x088e1002__mi,
	arm_instr_multi_0x088e1002__pl,
	arm_instr_multi_0x088e1002__vs,
	arm_instr_multi_0x088e1002__vc,
	arm_instr_multi_0x088e1002__hi,
	arm_instr_multi_0x088e1002__ls,
	arm_instr_multi_0x088e1002__ge,
	arm_instr_multi_0x088e1002__lt,
	arm_instr_multi_0x088e1002__gt,
	arm_instr_multi_0x088e1002__le,
	arm_instr_multi_0x088e1002,
	arm_instr_nop,
	arm_instr_multi_0x08840600__eq,
	arm_instr_multi_0x08840600__ne,
	arm_instr_multi_0x08840600__cs,
	arm_instr_multi_0x08840600__cc,
	arm_instr_multi_0x08840600__mi,
	arm_instr_multi_0x08840600__pl,
	arm_instr_multi_0x08840600__vs,
	arm_instr_multi_0x08840600__vc,
	arm_instr_multi_0x08840600__hi,
	arm_instr_multi_0x08840600__ls,
	arm_instr_multi_0x08840600__ge,
	arm_instr_multi_0x08840600__lt,
	arm_instr_multi_0x08840600__gt,
	arm_instr_multi_0x08840600__le,
	arm_instr_multi_0x08840600,
	arm_instr_nop,
	arm_instr_multi_0x088c0003__eq,
	arm_instr_multi_0x088c0003__ne,
	arm_instr_multi_0x088c0003__cs,
	arm_instr_multi_0x088c0003__cc,
	arm_instr_multi_0x088c0003__mi,
	arm_instr_multi_0x088c0003__pl,
	arm_instr_multi_0x088c0003__vs,
	arm_instr_multi_0x088c0003__vc,
	arm_instr_multi_0x088c0003__hi,
	arm_instr_multi_0x088c0003__ls,
	arm_instr_multi_0x088c0003__ge,
	arm_instr_multi_0x088c0003__lt,
	arm_instr_multi_0x088c0003__gt,
	arm_instr_multi_0x088c0003__le,
	arm_instr_multi_0x088c0003,
	arm_instr_nop,
	arm_instr_multi_0x098c0003__eq,
	arm_instr_multi_0x098c0003__ne,
	arm_instr_multi_0x098c0003__cs,
	arm_instr_multi_0x098c0003__cc,
	arm_instr_multi_0x098c0003__mi,
	arm_instr_multi_0x098c0003__pl,
	arm_instr_multi_0x098c0003__vs,
	arm_instr_multi_0x098c0003__vc,
	arm_instr_multi_0x098c0003__hi,
	arm_instr_multi_0x098c0003__ls,
	arm_instr_multi_0x098c0003__ge,
	arm_instr_multi_0x098c0003__lt,
	arm_instr_multi_0x098c0003__gt,
	arm_instr_multi_0x098c0003__le,
	arm_instr_multi_0x098c0003,
	arm_instr_nop,
};
void (*multi_opcode_f_161[112])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08ac000c__eq,
	arm_instr_multi_0x08ac000c__ne,
	arm_instr_multi_0x08ac000c__cs,
	arm_instr_multi_0x08ac000c__cc,
	arm_instr_multi_0x08ac000c__mi,
	arm_instr_multi_0x08ac000c__pl,
	arm_instr_multi_0x08ac000c__vs,
	arm_instr_multi_0x08ac000c__vc,
	arm_instr_multi_0x08ac000c__hi,
	arm_instr_multi_0x08ac000c__ls,
	arm_instr_multi_0x08ac000c__ge,
	arm_instr_multi_0x08ac000c__lt,
	arm_instr_multi_0x08ac000c__gt,
	arm_instr_multi_0x08ac000c__le,
	arm_instr_multi_0x08ac000c,
	arm_instr_nop,
	arm_instr_multi_0x088c0006__eq,
	arm_instr_multi_0x088c0006__ne,
	arm_instr_multi_0x088c0006__cs,
	arm_instr_multi_0x088c0006__cc,
	arm_instr_multi_0x088c0006__mi,
	arm_instr_multi_0x088c0006__pl,
	arm_instr_multi_0x088c0006__vs,
	arm_instr_multi_0x088c0006__vc,
	arm_instr_multi_0x088c0006__hi,
	arm_instr_multi_0x088c0006__ls,
	arm_instr_multi_0x088c0006__ge,
	arm_instr_multi_0x088c0006__lt,
	arm_instr_multi_0x088c0006__gt,
	arm_instr_multi_0x088c0006__le,
	arm_instr_multi_0x088c0006,
	arm_instr_nop,
	arm_instr_multi_0x08860006__eq,
	arm_instr_multi_0x08860006__ne,
	arm_instr_multi_0x08860006__cs,
	arm_instr_multi_0x08860006__cc,
	arm_instr_multi_0x08860006__mi,
	arm_instr_multi_0x08860006__pl,
	arm_instr_multi_0x08860006__vs,
	arm_instr_multi_0x08860006__vc,
	arm_instr_multi_0x08860006__hi,
	arm_instr_multi_0x08860006__ls,
	arm_instr_multi_0x08860006__ge,
	arm_instr_multi_0x08860006__lt,
	arm_instr_multi_0x08860006__gt,
	arm_instr_multi_0x08860006__le,
	arm_instr_multi_0x08860006,
	arm_instr_nop,
	arm_instr_multi_0x088e000c__eq,
	arm_instr_multi_0x088e000c__ne,
	arm_instr_multi_0x088e000c__cs,
	arm_instr_multi_0x088e000c__cc,
	arm_instr_multi_0x088e000c__mi,
	arm_instr_multi_0x088e000c__pl,
	arm_instr_multi_0x088e000c__vs,
	arm_instr_multi_0x088e000c__vc,
	arm_instr_multi_0x088e000c__hi,
	arm_instr_multi_0x088e000c__ls,
	arm_instr_multi_0x088e000c__ge,
	arm_instr_multi_0x088e000c__lt,
	arm_instr_multi_0x088e000c__gt,
	arm_instr_multi_0x088e000c__le,
	arm_instr_multi_0x088e000c,
	arm_instr_nop,
	arm_instr_multi_0x09860006__eq,
	arm_instr_multi_0x09860006__ne,
	arm_instr_multi_0x09860006__cs,
	arm_instr_multi_0x09860006__cc,
	arm_instr_multi_0x09860006__mi,
	arm_instr_multi_0x09860006__pl,
	arm_instr_multi_0x09860006__vs,
	arm_instr_multi_0x09860006__vc,
	arm_instr_multi_0x09860006__hi,
	arm_instr_multi_0x09860006__ls,
	arm_instr_multi_0x09860006__ge,
	arm_instr_multi_0x09860006__lt,
	arm_instr_multi_0x09860006__gt,
	arm_instr_multi_0x09860006__le,
	arm_instr_multi_0x09860006,
	arm_instr_nop,
	arm_instr_multi_0x098c0006__eq,
	arm_instr_multi_0x098c0006__ne,
	arm_instr_multi_0x098c0006__cs,
	arm_instr_multi_0x098c0006__cc,
	arm_instr_multi_0x098c0006__mi,
	arm_instr_multi_0x098c0006__pl,
	arm_instr_multi_0x098c0006__vs,
	arm_instr_multi_0x098c0006__vc,
	arm_instr_multi_0x098c0006__hi,
	arm_instr_multi_0x098c0006__ls,
	arm_instr_multi_0x098c0006__ge,
	arm_instr_multi_0x098c0006__lt,
	arm_instr_multi_0x098c0006__gt,
	arm_instr_multi_0x098c0006__le,
	arm_instr_multi_0x098c0006,
	arm_instr_nop,
	arm_instr_multi_0x08ac000f__eq,
	arm_instr_multi_0x08ac000f__ne,
	arm_instr_multi_0x08ac000f__cs,
	arm_instr_multi_0x08ac000f__cc,
	arm_instr_multi_0x08ac000f__mi,
	arm_instr_multi_0x08ac000f__pl,
	arm_instr_multi_0x08ac000f__vs,
	arm_instr_multi_0x08ac000f__vc,
	arm_instr_multi_0x08ac000f__hi,
	arm_instr_multi_0x08ac000f__ls,
	arm_instr_multi_0x08ac000f__ge,
	arm_instr_multi_0x08ac000f__lt,
	arm_instr_multi_0x08ac000f__gt,
	arm_instr_multi_0x08ac000f__le,
	arm_instr_multi_0x08ac000f,
	arm_instr_nop,
};
void (*multi_opcode_f_162[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x088e0018__eq,
	arm_instr_multi_0x088e0018__ne,
	arm_instr_multi_0x088e0018__cs,
	arm_instr_multi_0x088e0018__cc,
	arm_instr_multi_0x088e0018__mi,
	arm_instr_multi_0x088e0018__pl,
	arm_instr_multi_0x088e0018__vs,
	arm_instr_multi_0x088e0018__vc,
	arm_instr_multi_0x088e0018__hi,
	arm_instr_multi_0x088e0018__ls,
	arm_instr_multi_0x088e0018__ge,
	arm_instr_multi_0x088e0018__lt,
	arm_instr_multi_0x088e0018__gt,
	arm_instr_multi_0x088e0018__le,
	arm_instr_multi_0x088e0018,
	arm_instr_nop,
	arm_instr_multi_0x088c0018__eq,
	arm_instr_multi_0x088c0018__ne,
	arm_instr_multi_0x088c0018__cs,
	arm_instr_multi_0x088c0018__cc,
	arm_instr_multi_0x088c0018__mi,
	arm_instr_multi_0x088c0018__pl,
	arm_instr_multi_0x088c0018__vs,
	arm_instr_multi_0x088c0018__vc,
	arm_instr_multi_0x088c0018__hi,
	arm_instr_multi_0x088c0018__ls,
	arm_instr_multi_0x088c0018__ge,
	arm_instr_multi_0x088c0018__lt,
	arm_instr_multi_0x088c0018__gt,
	arm_instr_multi_0x088c0018__le,
	arm_instr_multi_0x088c0018,
	arm_instr_nop,
	arm_instr_multi_0x09860030__eq,
	arm_instr_multi_0x09860030__ne,
	arm_instr_multi_0x09860030__cs,
	arm_instr_multi_0x09860030__cc,
	arm_instr_multi_0x09860030__mi,
	arm_instr_multi_0x09860030__pl,
	arm_instr_multi_0x09860030__vs,
	arm_instr_multi_0x09860030__vc,
	arm_instr_multi_0x09860030__hi,
	arm_instr_multi_0x09860030__ls,
	arm_instr_multi_0x09860030__ge,
	arm_instr_multi_0x09860030__lt,
	arm_instr_multi_0x09860030__gt,
	arm_instr_multi_0x09860030__le,
	arm_instr_multi_0x09860030,
	arm_instr_nop,
};
void (*multi_opcode_f_164[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x088c0060__eq,
	arm_instr_multi_0x088c0060__ne,
	arm_instr_multi_0x088c0060__cs,
	arm_instr_multi_0x088c0060__cc,
	arm_instr_multi_0x088c0060__mi,
	arm_instr_multi_0x088c0060__pl,
	arm_instr_multi_0x088c0060__vs,
	arm_instr_multi_0x088c0060__vc,
	arm_instr_multi_0x088c0060__hi,
	arm_instr_multi_0x088c0060__ls,
	arm_instr_multi_0x088c0060__ge,
	arm_instr_multi_0x088c0060__lt,
	arm_instr_multi_0x088c0060__gt,
	arm_instr_multi_0x088c0060__le,
	arm_instr_multi_0x088c0060,
	arm_instr_nop,
	arm_instr_multi_0x088e00c0__eq,
	arm_instr_multi_0x088e00c0__ne,
	arm_instr_multi_0x088e00c0__cs,
	arm_instr_multi_0x088e00c0__cc,
	arm_instr_multi_0x088e00c0__mi,
	arm_instr_multi_0x088e00c0__pl,
	arm_instr_multi_0x088e00c0__vs,
	arm_instr_multi_0x088e00c0__vc,
	arm_instr_multi_0x088e00c0__hi,
	arm_instr_multi_0x088e00c0__ls,
	arm_instr_multi_0x088e00c0__ge,
	arm_instr_multi_0x088e00c0__lt,
	arm_instr_multi_0x088e00c0__gt,
	arm_instr_multi_0x088e00c0__le,
	arm_instr_multi_0x088e00c0,
	arm_instr_nop,
	arm_instr_multi_0x088c00c8__eq,
	arm_instr_multi_0x088c00c8__ne,
	arm_instr_multi_0x088c00c8__cs,
	arm_instr_multi_0x088c00c8__cc,
	arm_instr_multi_0x088c00c8__mi,
	arm_instr_multi_0x088c00c8__pl,
	arm_instr_multi_0x088c00c8__vs,
	arm_instr_multi_0x088c00c8__vc,
	arm_instr_multi_0x088c00c8__hi,
	arm_instr_multi_0x088c00c8__ls,
	arm_instr_multi_0x088c00c8__ge,
	arm_instr_multi_0x088c00c8__lt,
	arm_instr_multi_0x088c00c8__gt,
	arm_instr_multi_0x088c00c8__le,
	arm_instr_multi_0x088c00c8,
	arm_instr_nop,
};
void (*multi_opcode_f_176[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08850003__eq,
	arm_instr_multi_0x08850003__ne,
	arm_instr_multi_0x08850003__cs,
	arm_instr_multi_0x08850003__cc,
	arm_instr_multi_0x08850003__mi,
	arm_instr_multi_0x08850003__pl,
	arm_instr_multi_0x08850003__vs,
	arm_instr_multi_0x08850003__vc,
	arm_instr_multi_0x08850003__hi,
	arm_instr_multi_0x08850003__ls,
	arm_instr_multi_0x08850003__ge,
	arm_instr_multi_0x08850003__lt,
	arm_instr_multi_0x08850003__gt,
	arm_instr_multi_0x08850003__le,
	arm_instr_multi_0x08850003,
	arm_instr_nop,
	arm_instr_multi_0x088d0088__eq,
	arm_instr_multi_0x088d0088__ne,
	arm_instr_multi_0x088d0088__cs,
	arm_instr_multi_0x088d0088__cc,
	arm_instr_multi_0x088d0088__mi,
	arm_instr_multi_0x088d0088__pl,
	arm_instr_multi_0x088d0088__vs,
	arm_instr_multi_0x088d0088__vc,
	arm_instr_multi_0x088d0088__hi,
	arm_instr_multi_0x088d0088__ls,
	arm_instr_multi_0x088d0088__ge,
	arm_instr_multi_0x088d0088__lt,
	arm_instr_multi_0x088d0088__gt,
	arm_instr_multi_0x088d0088__le,
	arm_instr_multi_0x088d0088,
	arm_instr_nop,
	arm_instr_multi_0x088d1020__eq,
	arm_instr_multi_0x088d1020__ne,
	arm_instr_multi_0x088d1020__cs,
	arm_instr_multi_0x088d1020__cc,
	arm_instr_multi_0x088d1020__mi,
	arm_instr_multi_0x088d1020__pl,
	arm_instr_multi_0x088d1020__vs,
	arm_instr_multi_0x088d1020__vc,
	arm_instr_multi_0x088d1020__hi,
	arm_instr_multi_0x088d1020__ls,
	arm_instr_multi_0x088d1020__ge,
	arm_instr_multi_0x088d1020__lt,
	arm_instr_multi_0x088d1020__gt,
	arm_instr_multi_0x088d1020__le,
	arm_instr_multi_0x088d1020,
	arm_instr_nop,
};
void (*multi_opcode_f_177[64])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08850006__eq,
	arm_instr_multi_0x08850006__ne,
	arm_instr_multi_0x08850006__cs,
	arm_instr_multi_0x08850006__cc,
	arm_instr_multi_0x08850006__mi,
	arm_instr_multi_0x08850006__pl,
	arm_instr_multi_0x08850006__vs,
	arm_instr_multi_0x08850006__vc,
	arm_instr_multi_0x08850006__hi,
	arm_instr_multi_0x08850006__ls,
	arm_instr_multi_0x08850006__ge,
	arm_instr_multi_0x08850006__lt,
	arm_instr_multi_0x08850006__gt,
	arm_instr_multi_0x08850006__le,
	arm_instr_multi_0x08850006,
	arm_instr_nop,
	arm_instr_multi_0x08870006__eq,
	arm_instr_multi_0x08870006__ne,
	arm_instr_multi_0x08870006__cs,
	arm_instr_multi_0x08870006__cc,
	arm_instr_multi_0x08870006__mi,
	arm_instr_multi_0x08870006__pl,
	arm_instr_multi_0x08870006__vs,
	arm_instr_multi_0x08870006__vc,
	arm_instr_multi_0x08870006__hi,
	arm_instr_multi_0x08870006__ls,
	arm_instr_multi_0x08870006__ge,
	arm_instr_multi_0x08870006__lt,
	arm_instr_multi_0x08870006__gt,
	arm_instr_multi_0x08870006__le,
	arm_instr_multi_0x08870006,
	arm_instr_nop,
	arm_instr_multi_0x0885000c__eq,
	arm_instr_multi_0x0885000c__ne,
	arm_instr_multi_0x0885000c__cs,
	arm_instr_multi_0x0885000c__cc,
	arm_instr_multi_0x0885000c__mi,
	arm_instr_multi_0x0885000c__pl,
	arm_instr_multi_0x0885000c__vs,
	arm_instr_multi_0x0885000c__vc,
	arm_instr_multi_0x0885000c__hi,
	arm_instr_multi_0x0885000c__ls,
	arm_instr_multi_0x0885000c__ge,
	arm_instr_multi_0x0885000c__lt,
	arm_instr_multi_0x0885000c__gt,
	arm_instr_multi_0x0885000c__le,
	arm_instr_multi_0x0885000c,
	arm_instr_nop,
	arm_instr_multi_0x098d000e__eq,
	arm_instr_multi_0x098d000e__ne,
	arm_instr_multi_0x098d000e__cs,
	arm_instr_multi_0x098d000e__cc,
	arm_instr_multi_0x098d000e__mi,
	arm_instr_multi_0x098d000e__pl,
	arm_instr_multi_0x098d000e__vs,
	arm_instr_multi_0x098d000e__vc,
	arm_instr_multi_0x098d000e__hi,
	arm_instr_multi_0x098d000e__ls,
	arm_instr_multi_0x098d000e__ge,
	arm_instr_multi_0x098d000e__lt,
	arm_instr_multi_0x098d000e__gt,
	arm_instr_multi_0x098d000e__le,
	arm_instr_multi_0x098d000e,
	arm_instr_nop,
};
void (*multi_opcode_f_178[96])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09870018__eq,
	arm_instr_multi_0x09870018__ne,
	arm_instr_multi_0x09870018__cs,
	arm_instr_multi_0x09870018__cc,
	arm_instr_multi_0x09870018__mi,
	arm_instr_multi_0x09870018__pl,
	arm_instr_multi_0x09870018__vs,
	arm_instr_multi_0x09870018__vc,
	arm_instr_multi_0x09870018__hi,
	arm_instr_multi_0x09870018__ls,
	arm_instr_multi_0x09870018__ge,
	arm_instr_multi_0x09870018__lt,
	arm_instr_multi_0x09870018__gt,
	arm_instr_multi_0x09870018__le,
	arm_instr_multi_0x09870018,
	arm_instr_nop,
	arm_instr_multi_0x098d0030__eq,
	arm_instr_multi_0x098d0030__ne,
	arm_instr_multi_0x098d0030__cs,
	arm_instr_multi_0x098d0030__cc,
	arm_instr_multi_0x098d0030__mi,
	arm_instr_multi_0x098d0030__pl,
	arm_instr_multi_0x098d0030__vs,
	arm_instr_multi_0x098d0030__vc,
	arm_instr_multi_0x098d0030__hi,
	arm_instr_multi_0x098d0030__ls,
	arm_instr_multi_0x098d0030__ge,
	arm_instr_multi_0x098d0030__lt,
	arm_instr_multi_0x098d0030__gt,
	arm_instr_multi_0x098d0030__le,
	arm_instr_multi_0x098d0030,
	arm_instr_nop,
	arm_instr_multi_0x088d1010__eq,
	arm_instr_multi_0x088d1010__ne,
	arm_instr_multi_0x088d1010__cs,
	arm_instr_multi_0x088d1010__cc,
	arm_instr_multi_0x088d1010__mi,
	arm_instr_multi_0x088d1010__pl,
	arm_instr_multi_0x088d1010__vs,
	arm_instr_multi_0x088d1010__vc,
	arm_instr_multi_0x088d1010__hi,
	arm_instr_multi_0x088d1010__ls,
	arm_instr_multi_0x088d1010__ge,
	arm_instr_multi_0x088d1010__lt,
	arm_instr_multi_0x088d1010__gt,
	arm_instr_multi_0x088d1010__le,
	arm_instr_multi_0x088d1010,
	arm_instr_nop,
	arm_instr_multi_0x088d0030__eq,
	arm_instr_multi_0x088d0030__ne,
	arm_instr_multi_0x088d0030__cs,
	arm_instr_multi_0x088d0030__cc,
	arm_instr_multi_0x088d0030__mi,
	arm_instr_multi_0x088d0030__pl,
	arm_instr_multi_0x088d0030__vs,
	arm_instr_multi_0x088d0030__vc,
	arm_instr_multi_0x088d0030__hi,
	arm_instr_multi_0x088d0030__ls,
	arm_instr_multi_0x088d0030__ge,
	arm_instr_multi_0x088d0030__lt,
	arm_instr_multi_0x088d0030__gt,
	arm_instr_multi_0x088d0030__le,
	arm_instr_multi_0x088d0030,
	arm_instr_nop,
	arm_instr_multi_0x088d4010__eq,
	arm_instr_multi_0x088d4010__ne,
	arm_instr_multi_0x088d4010__cs,
	arm_instr_multi_0x088d4010__cc,
	arm_instr_multi_0x088d4010__mi,
	arm_instr_multi_0x088d4010__pl,
	arm_instr_multi_0x088d4010__vs,
	arm_instr_multi_0x088d4010__vc,
	arm_instr_multi_0x088d4010__hi,
	arm_instr_multi_0x088d4010__ls,
	arm_instr_multi_0x088d4010__ge,
	arm_instr_multi_0x088d4010__lt,
	arm_instr_multi_0x088d4010__gt,
	arm_instr_multi_0x088d4010__le,
	arm_instr_multi_0x088d4010,
	arm_instr_nop,
	arm_instr_multi_0x08850018__eq,
	arm_instr_multi_0x08850018__ne,
	arm_instr_multi_0x08850018__cs,
	arm_instr_multi_0x08850018__cc,
	arm_instr_multi_0x08850018__mi,
	arm_instr_multi_0x08850018__pl,
	arm_instr_multi_0x08850018__vs,
	arm_instr_multi_0x08850018__vc,
	arm_instr_multi_0x08850018__hi,
	arm_instr_multi_0x08850018__ls,
	arm_instr_multi_0x08850018__ge,
	arm_instr_multi_0x08850018__lt,
	arm_instr_multi_0x08850018__gt,
	arm_instr_multi_0x08850018__le,
	arm_instr_multi_0x08850018,
	arm_instr_nop,
};
void (*multi_opcode_f_179[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x09850014__eq,
	arm_instr_multi_0x09850014__ne,
	arm_instr_multi_0x09850014__cs,
	arm_instr_multi_0x09850014__cc,
	arm_instr_multi_0x09850014__mi,
	arm_instr_multi_0x09850014__pl,
	arm_instr_multi_0x09850014__vs,
	arm_instr_multi_0x09850014__vc,
	arm_instr_multi_0x09850014__hi,
	arm_instr_multi_0x09850014__ls,
	arm_instr_multi_0x09850014__ge,
	arm_instr_multi_0x09850014__lt,
	arm_instr_multi_0x09850014__gt,
	arm_instr_multi_0x09850014__le,
	arm_instr_multi_0x09850014,
	arm_instr_nop,
};
void (*multi_opcode_f_184[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x088d1100__eq,
	arm_instr_multi_0x088d1100__ne,
	arm_instr_multi_0x088d1100__cs,
	arm_instr_multi_0x088d1100__cc,
	arm_instr_multi_0x088d1100__mi,
	arm_instr_multi_0x088d1100__pl,
	arm_instr_multi_0x088d1100__vs,
	arm_instr_multi_0x088d1100__vc,
	arm_instr_multi_0x088d1100__hi,
	arm_instr_multi_0x088d1100__ls,
	arm_instr_multi_0x088d1100__ge,
	arm_instr_multi_0x088d1100__lt,
	arm_instr_multi_0x088d1100__gt,
	arm_instr_multi_0x088d1100__le,
	arm_instr_multi_0x088d1100,
	arm_instr_nop,
	arm_instr_multi_0x088d0180__eq,
	arm_instr_multi_0x088d0180__ne,
	arm_instr_multi_0x088d0180__cs,
	arm_instr_multi_0x088d0180__cc,
	arm_instr_multi_0x088d0180__mi,
	arm_instr_multi_0x088d0180__pl,
	arm_instr_multi_0x088d0180__vs,
	arm_instr_multi_0x088d0180__vc,
	arm_instr_multi_0x088d0180__hi,
	arm_instr_multi_0x088d0180__ls,
	arm_instr_multi_0x088d0180__ge,
	arm_instr_multi_0x088d0180__lt,
	arm_instr_multi_0x088d0180__gt,
	arm_instr_multi_0x088d0180__le,
	arm_instr_multi_0x088d0180,
	arm_instr_nop,
};
void (*multi_opcode_f_191[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x088d1fff__eq,
	arm_instr_multi_0x088d1fff__ne,
	arm_instr_multi_0x088d1fff__cs,
	arm_instr_multi_0x088d1fff__cc,
	arm_instr_multi_0x088d1fff__mi,
	arm_instr_multi_0x088d1fff__pl,
	arm_instr_multi_0x088d1fff__vs,
	arm_instr_multi_0x088d1fff__vc,
	arm_instr_multi_0x088d1fff__hi,
	arm_instr_multi_0x088d1fff__ls,
	arm_instr_multi_0x088d1fff__ge,
	arm_instr_multi_0x088d1fff__lt,
	arm_instr_multi_0x088d1fff__gt,
	arm_instr_multi_0x088d1fff__le,
	arm_instr_multi_0x088d1fff,
	arm_instr_nop,
};
void (*multi_opcode_f_192[96])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08920003__eq,
	arm_instr_multi_0x08920003__ne,
	arm_instr_multi_0x08920003__cs,
	arm_instr_multi_0x08920003__cc,
	arm_instr_multi_0x08920003__mi,
	arm_instr_multi_0x08920003__pl,
	arm_instr_multi_0x08920003__vs,
	arm_instr_multi_0x08920003__vc,
	arm_instr_multi_0x08920003__hi,
	arm_instr_multi_0x08920003__ls,
	arm_instr_multi_0x08920003__ge,
	arm_instr_multi_0x08920003__lt,
	arm_instr_multi_0x08920003__gt,
	arm_instr_multi_0x08920003__le,
	arm_instr_multi_0x08920003,
	arm_instr_nop,
	arm_instr_multi_0x08900003__eq,
	arm_instr_multi_0x08900003__ne,
	arm_instr_multi_0x08900003__cs,
	arm_instr_multi_0x08900003__cc,
	arm_instr_multi_0x08900003__mi,
	arm_instr_multi_0x08900003__pl,
	arm_instr_multi_0x08900003__vs,
	arm_instr_multi_0x08900003__vc,
	arm_instr_multi_0x08900003__hi,
	arm_instr_multi_0x08900003__ls,
	arm_instr_multi_0x08900003__ge,
	arm_instr_multi_0x08900003__lt,
	arm_instr_multi_0x08900003__gt,
	arm_instr_multi_0x08900003__le,
	arm_instr_multi_0x08900003,
	arm_instr_nop,
	arm_instr_multi_0x09920003__eq,
	arm_instr_multi_0x09920003__ne,
	arm_instr_multi_0x09920003__cs,
	arm_instr_multi_0x09920003__cc,
	arm_instr_multi_0x09920003__mi,
	arm_instr_multi_0x09920003__pl,
	arm_instr_multi_0x09920003__vs,
	arm_instr_multi_0x09920003__vc,
	arm_instr_multi_0x09920003__hi,
	arm_instr_multi_0x09920003__ls,
	arm_instr_multi_0x09920003__ge,
	arm_instr_multi_0x09920003__lt,
	arm_instr_multi_0x09920003__gt,
	arm_instr_multi_0x09920003__le,
	arm_instr_multi_0x09920003,
	arm_instr_nop,
	arm_instr_multi_0x08980003__eq,
	arm_instr_multi_0x08980003__ne,
	arm_instr_multi_0x08980003__cs,
	arm_instr_multi_0x08980003__cc,
	arm_instr_multi_0x08980003__mi,
	arm_instr_multi_0x08980003__pl,
	arm_instr_multi_0x08980003__vs,
	arm_instr_multi_0x08980003__vc,
	arm_instr_multi_0x08980003__hi,
	arm_instr_multi_0x08980003__ls,
	arm_instr_multi_0x08980003__ge,
	arm_instr_multi_0x08980003__lt,
	arm_instr_multi_0x08980003__gt,
	arm_instr_multi_0x08980003__le,
	arm_instr_multi_0x08980003,
	arm_instr_nop,
	arm_instr_multi_0x09904008__eq,
	arm_instr_multi_0x09904008__ne,
	arm_instr_multi_0x09904008__cs,
	arm_instr_multi_0x09904008__cc,
	arm_instr_multi_0x09904008__mi,
	arm_instr_multi_0x09904008__pl,
	arm_instr_multi_0x09904008__vs,
	arm_instr_multi_0x09904008__vc,
	arm_instr_multi_0x09904008__hi,
	arm_instr_multi_0x09904008__ls,
	arm_instr_multi_0x09904008__ge,
	arm_instr_multi_0x09904008__lt,
	arm_instr_multi_0x09904008__gt,
	arm_instr_multi_0x09904008__le,
	arm_instr_multi_0x09904008,
	arm_instr_nop,
	arm_instr_multi_0x099a0003__eq,
	arm_instr_multi_0x099a0003__ne,
	arm_instr_multi_0x099a0003__cs,
	arm_instr_multi_0x099a0003__cc,
	arm_instr_multi_0x099a0003__mi,
	arm_instr_multi_0x099a0003__pl,
	arm_instr_multi_0x099a0003__vs,
	arm_instr_multi_0x099a0003__vc,
	arm_instr_multi_0x099a0003__hi,
	arm_instr_multi_0x099a0003__ls,
	arm_instr_multi_0x099a0003__ge,
	arm_instr_multi_0x099a0003__lt,
	arm_instr_multi_0x099a0003__gt,
	arm_instr_multi_0x099a0003__le,
	arm_instr_multi_0x099a0003,
	arm_instr_nop,
};
void (*multi_opcode_f_193[64])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08900006__eq,
	arm_instr_multi_0x08900006__ne,
	arm_instr_multi_0x08900006__cs,
	arm_instr_multi_0x08900006__cc,
	arm_instr_multi_0x08900006__mi,
	arm_instr_multi_0x08900006__pl,
	arm_instr_multi_0x08900006__vs,
	arm_instr_multi_0x08900006__vc,
	arm_instr_multi_0x08900006__hi,
	arm_instr_multi_0x08900006__ls,
	arm_instr_multi_0x08900006__ge,
	arm_instr_multi_0x08900006__lt,
	arm_instr_multi_0x08900006__gt,
	arm_instr_multi_0x08900006__le,
	arm_instr_multi_0x08900006,
	arm_instr_nop,
	arm_instr_multi_0x0892000c__eq,
	arm_instr_multi_0x0892000c__ne,
	arm_instr_multi_0x0892000c__cs,
	arm_instr_multi_0x0892000c__cc,
	arm_instr_multi_0x0892000c__mi,
	arm_instr_multi_0x0892000c__pl,
	arm_instr_multi_0x0892000c__vs,
	arm_instr_multi_0x0892000c__vc,
	arm_instr_multi_0x0892000c__hi,
	arm_instr_multi_0x0892000c__ls,
	arm_instr_multi_0x0892000c__ge,
	arm_instr_multi_0x0892000c__lt,
	arm_instr_multi_0x0892000c__gt,
	arm_instr_multi_0x0892000c__le,
	arm_instr_multi_0x0892000c,
	arm_instr_nop,
	arm_instr_multi_0x08920006__eq,
	arm_instr_multi_0x08920006__ne,
	arm_instr_multi_0x08920006__cs,
	arm_instr_multi_0x08920006__cc,
	arm_instr_multi_0x08920006__mi,
	arm_instr_multi_0x08920006__pl,
	arm_instr_multi_0x08920006__vs,
	arm_instr_multi_0x08920006__vc,
	arm_instr_multi_0x08920006__hi,
	arm_instr_multi_0x08920006__ls,
	arm_instr_multi_0x08920006__ge,
	arm_instr_multi_0x08920006__lt,
	arm_instr_multi_0x08920006__gt,
	arm_instr_multi_0x08920006__le,
	arm_instr_multi_0x08920006,
	arm_instr_nop,
	arm_instr_multi_0x08980006__eq,
	arm_instr_multi_0x08980006__ne,
	arm_instr_multi_0x08980006__cs,
	arm_instr_multi_0x08980006__cc,
	arm_instr_multi_0x08980006__mi,
	arm_instr_multi_0x08980006__pl,
	arm_instr_multi_0x08980006__vs,
	arm_instr_multi_0x08980006__vc,
	arm_instr_multi_0x08980006__hi,
	arm_instr_multi_0x08980006__ls,
	arm_instr_multi_0x08980006__ge,
	arm_instr_multi_0x08980006__lt,
	arm_instr_multi_0x08980006__gt,
	arm_instr_multi_0x08980006__le,
	arm_instr_multi_0x08980006,
	arm_instr_nop,
};
void (*multi_opcode_f_194[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08920018__eq,
	arm_instr_multi_0x08920018__ne,
	arm_instr_multi_0x08920018__cs,
	arm_instr_multi_0x08920018__cc,
	arm_instr_multi_0x08920018__mi,
	arm_instr_multi_0x08920018__pl,
	arm_instr_multi_0x08920018__vs,
	arm_instr_multi_0x08920018__vc,
	arm_instr_multi_0x08920018__hi,
	arm_instr_multi_0x08920018__ls,
	arm_instr_multi_0x08920018__ge,
	arm_instr_multi_0x08920018__lt,
	arm_instr_multi_0x08920018__gt,
	arm_instr_multi_0x08920018__le,
	arm_instr_multi_0x08920018,
	arm_instr_nop,
	arm_instr_multi_0x08980018__eq,
	arm_instr_multi_0x08980018__ne,
	arm_instr_multi_0x08980018__cs,
	arm_instr_multi_0x08980018__cc,
	arm_instr_multi_0x08980018__mi,
	arm_instr_multi_0x08980018__pl,
	arm_instr_multi_0x08980018__vs,
	arm_instr_multi_0x08980018__vc,
	arm_instr_multi_0x08980018__hi,
	arm_instr_multi_0x08980018__ls,
	arm_instr_multi_0x08980018__ge,
	arm_instr_multi_0x08980018__lt,
	arm_instr_multi_0x08980018__gt,
	arm_instr_multi_0x08980018__le,
	arm_instr_multi_0x08980018,
	arm_instr_nop,
	arm_instr_multi_0x08900018__eq,
	arm_instr_multi_0x08900018__ne,
	arm_instr_multi_0x08900018__cs,
	arm_instr_multi_0x08900018__cc,
	arm_instr_multi_0x08900018__mi,
	arm_instr_multi_0x08900018__pl,
	arm_instr_multi_0x08900018__vs,
	arm_instr_multi_0x08900018__vc,
	arm_instr_multi_0x08900018__hi,
	arm_instr_multi_0x08900018__ls,
	arm_instr_multi_0x08900018__ge,
	arm_instr_multi_0x08900018__lt,
	arm_instr_multi_0x08900018__gt,
	arm_instr_multi_0x08900018__le,
	arm_instr_multi_0x08900018,
	arm_instr_nop,
	arm_instr_multi_0x09900018__eq,
	arm_instr_multi_0x09900018__ne,
	arm_instr_multi_0x09900018__cs,
	arm_instr_multi_0x09900018__cc,
	arm_instr_multi_0x09900018__mi,
	arm_instr_multi_0x09900018__pl,
	arm_instr_multi_0x09900018__vs,
	arm_instr_multi_0x09900018__vc,
	arm_instr_multi_0x09900018__hi,
	arm_instr_multi_0x09900018__ls,
	arm_instr_multi_0x09900018__ge,
	arm_instr_multi_0x09900018__lt,
	arm_instr_multi_0x09900018__gt,
	arm_instr_multi_0x09900018__le,
	arm_instr_multi_0x09900018,
	arm_instr_nop,
	arm_instr_multi_0x08920030__eq,
	arm_instr_multi_0x08920030__ne,
	arm_instr_multi_0x08920030__cs,
	arm_instr_multi_0x08920030__cc,
	arm_instr_multi_0x08920030__mi,
	arm_instr_multi_0x08920030__pl,
	arm_instr_multi_0x08920030__vs,
	arm_instr_multi_0x08920030__vc,
	arm_instr_multi_0x08920030__hi,
	arm_instr_multi_0x08920030__ls,
	arm_instr_multi_0x08920030__ge,
	arm_instr_multi_0x08920030__lt,
	arm_instr_multi_0x08920030__gt,
	arm_instr_multi_0x08920030__le,
	arm_instr_multi_0x08920030,
	arm_instr_nop,
};
void (*multi_opcode_f_196[64])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08b000c0__eq,
	arm_instr_multi_0x08b000c0__ne,
	arm_instr_multi_0x08b000c0__cs,
	arm_instr_multi_0x08b000c0__cc,
	arm_instr_multi_0x08b000c0__mi,
	arm_instr_multi_0x08b000c0__pl,
	arm_instr_multi_0x08b000c0__vs,
	arm_instr_multi_0x08b000c0__vc,
	arm_instr_multi_0x08b000c0__hi,
	arm_instr_multi_0x08b000c0__ls,
	arm_instr_multi_0x08b000c0__ge,
	arm_instr_multi_0x08b000c0__lt,
	arm_instr_multi_0x08b000c0__gt,
	arm_instr_multi_0x08b000c0__le,
	arm_instr_multi_0x08b000c0,
	arm_instr_nop,
	arm_instr_multi_0x08980060__eq,
	arm_instr_multi_0x08980060__ne,
	arm_instr_multi_0x08980060__cs,
	arm_instr_multi_0x08980060__cc,
	arm_instr_multi_0x08980060__mi,
	arm_instr_multi_0x08980060__pl,
	arm_instr_multi_0x08980060__vs,
	arm_instr_multi_0x08980060__vc,
	arm_instr_multi_0x08980060__hi,
	arm_instr_multi_0x08980060__ls,
	arm_instr_multi_0x08980060__ge,
	arm_instr_multi_0x08980060__lt,
	arm_instr_multi_0x08980060__gt,
	arm_instr_multi_0x08980060__le,
	arm_instr_multi_0x08980060,
	arm_instr_nop,
	arm_instr_multi_0x08900060__eq,
	arm_instr_multi_0x08900060__ne,
	arm_instr_multi_0x08900060__cs,
	arm_instr_multi_0x08900060__cc,
	arm_instr_multi_0x08900060__mi,
	arm_instr_multi_0x08900060__pl,
	arm_instr_multi_0x08900060__vs,
	arm_instr_multi_0x08900060__vc,
	arm_instr_multi_0x08900060__hi,
	arm_instr_multi_0x08900060__ls,
	arm_instr_multi_0x08900060__ge,
	arm_instr_multi_0x08900060__lt,
	arm_instr_multi_0x08900060__gt,
	arm_instr_multi_0x08900060__le,
	arm_instr_multi_0x08900060,
	arm_instr_nop,
	arm_instr_multi_0x089200c0__eq,
	arm_instr_multi_0x089200c0__ne,
	arm_instr_multi_0x089200c0__cs,
	arm_instr_multi_0x089200c0__cc,
	arm_instr_multi_0x089200c0__mi,
	arm_instr_multi_0x089200c0__pl,
	arm_instr_multi_0x089200c0__vs,
	arm_instr_multi_0x089200c0__vc,
	arm_instr_multi_0x089200c0__hi,
	arm_instr_multi_0x089200c0__ls,
	arm_instr_multi_0x089200c0__ge,
	arm_instr_multi_0x089200c0__lt,
	arm_instr_multi_0x089200c0__gt,
	arm_instr_multi_0x089200c0__le,
	arm_instr_multi_0x089200c0,
	arm_instr_nop,
};
void (*multi_opcode_f_200[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08b00300__eq,
	arm_instr_multi_0x08b00300__ne,
	arm_instr_multi_0x08b00300__cs,
	arm_instr_multi_0x08b00300__cc,
	arm_instr_multi_0x08b00300__mi,
	arm_instr_multi_0x08b00300__pl,
	arm_instr_multi_0x08b00300__vs,
	arm_instr_multi_0x08b00300__vc,
	arm_instr_multi_0x08b00300__hi,
	arm_instr_multi_0x08b00300__ls,
	arm_instr_multi_0x08b00300__ge,
	arm_instr_multi_0x08b00300__lt,
	arm_instr_multi_0x08b00300__gt,
	arm_instr_multi_0x08b00300__le,
	arm_instr_multi_0x08b00300,
	arm_instr_nop,
	arm_instr_multi_0x09900120__eq,
	arm_instr_multi_0x09900120__ne,
	arm_instr_multi_0x09900120__cs,
	arm_instr_multi_0x09900120__cc,
	arm_instr_multi_0x09900120__mi,
	arm_instr_multi_0x09900120__pl,
	arm_instr_multi_0x09900120__vs,
	arm_instr_multi_0x09900120__vc,
	arm_instr_multi_0x09900120__hi,
	arm_instr_multi_0x09900120__ls,
	arm_instr_multi_0x09900120__ge,
	arm_instr_multi_0x09900120__lt,
	arm_instr_multi_0x09900120__gt,
	arm_instr_multi_0x09900120__le,
	arm_instr_multi_0x09900120,
	arm_instr_nop,
	arm_instr_multi_0x08980300__eq,
	arm_instr_multi_0x08980300__ne,
	arm_instr_multi_0x08980300__cs,
	arm_instr_multi_0x08980300__cc,
	arm_instr_multi_0x08980300__mi,
	arm_instr_multi_0x08980300__pl,
	arm_instr_multi_0x08980300__vs,
	arm_instr_multi_0x08980300__vc,
	arm_instr_multi_0x08980300__hi,
	arm_instr_multi_0x08980300__ls,
	arm_instr_multi_0x08980300__ge,
	arm_instr_multi_0x08980300__lt,
	arm_instr_multi_0x08980300__gt,
	arm_instr_multi_0x08980300__le,
	arm_instr_multi_0x08980300,
	arm_instr_nop,
};
void (*multi_opcode_f_204[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08b00fc0__eq,
	arm_instr_multi_0x08b00fc0__ne,
	arm_instr_multi_0x08b00fc0__cs,
	arm_instr_multi_0x08b00fc0__cc,
	arm_instr_multi_0x08b00fc0__mi,
	arm_instr_multi_0x08b00fc0__pl,
	arm_instr_multi_0x08b00fc0__vs,
	arm_instr_multi_0x08b00fc0__vc,
	arm_instr_multi_0x08b00fc0__hi,
	arm_instr_multi_0x08b00fc0__ls,
	arm_instr_multi_0x08b00fc0__ge,
	arm_instr_multi_0x08b00fc0__lt,
	arm_instr_multi_0x08b00fc0__gt,
	arm_instr_multi_0x08b00fc0__le,
	arm_instr_multi_0x08b00fc0,
	arm_instr_nop,
};
void (*multi_opcode_f_206[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08b051f8__eq,
	arm_instr_multi_0x08b051f8__ne,
	arm_instr_multi_0x08b051f8__cs,
	arm_instr_multi_0x08b051f8__cc,
	arm_instr_multi_0x08b051f8__mi,
	arm_instr_multi_0x08b051f8__pl,
	arm_instr_multi_0x08b051f8__vs,
	arm_instr_multi_0x08b051f8__vc,
	arm_instr_multi_0x08b051f8__hi,
	arm_instr_multi_0x08b051f8__ls,
	arm_instr_multi_0x08b051f8__ge,
	arm_instr_multi_0x08b051f8__lt,
	arm_instr_multi_0x08b051f8__gt,
	arm_instr_multi_0x08b051f8__le,
	arm_instr_multi_0x08b051f8,
	arm_instr_nop,
};
void (*multi_opcode_f_208[128])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08930003__eq,
	arm_instr_multi_0x08930003__ne,
	arm_instr_multi_0x08930003__cs,
	arm_instr_multi_0x08930003__cc,
	arm_instr_multi_0x08930003__mi,
	arm_instr_multi_0x08930003__pl,
	arm_instr_multi_0x08930003__vs,
	arm_instr_multi_0x08930003__vc,
	arm_instr_multi_0x08930003__hi,
	arm_instr_multi_0x08930003__ls,
	arm_instr_multi_0x08930003__ge,
	arm_instr_multi_0x08930003__lt,
	arm_instr_multi_0x08930003__gt,
	arm_instr_multi_0x08930003__le,
	arm_instr_multi_0x08930003,
	arm_instr_nop,
	arm_instr_multi_0x08910003__eq,
	arm_instr_multi_0x08910003__ne,
	arm_instr_multi_0x08910003__cs,
	arm_instr_multi_0x08910003__cc,
	arm_instr_multi_0x08910003__mi,
	arm_instr_multi_0x08910003__pl,
	arm_instr_multi_0x08910003__vs,
	arm_instr_multi_0x08910003__vc,
	arm_instr_multi_0x08910003__hi,
	arm_instr_multi_0x08910003__ls,
	arm_instr_multi_0x08910003__ge,
	arm_instr_multi_0x08910003__lt,
	arm_instr_multi_0x08910003__gt,
	arm_instr_multi_0x08910003__le,
	arm_instr_multi_0x08910003,
	arm_instr_nop,
	arm_instr_multi_0x08930600__eq,
	arm_instr_multi_0x08930600__ne,
	arm_instr_multi_0x08930600__cs,
	arm_instr_multi_0x08930600__cc,
	arm_instr_multi_0x08930600__mi,
	arm_instr_multi_0x08930600__pl,
	arm_instr_multi_0x08930600__vs,
	arm_instr_multi_0x08930600__vc,
	arm_instr_multi_0x08930600__hi,
	arm_instr_multi_0x08930600__ls,
	arm_instr_multi_0x08930600__ge,
	arm_instr_multi_0x08930600__lt,
	arm_instr_multi_0x08930600__gt,
	arm_instr_multi_0x08930600__le,
	arm_instr_multi_0x08930600,
	arm_instr_nop,
	arm_instr_multi_0x08b11008__eq,
	arm_instr_multi_0x08b11008__ne,
	arm_instr_multi_0x08b11008__cs,
	arm_instr_multi_0x08b11008__cc,
	arm_instr_multi_0x08b11008__mi,
	arm_instr_multi_0x08b11008__pl,
	arm_instr_multi_0x08b11008__vs,
	arm_instr_multi_0x08b11008__vc,
	arm_instr_multi_0x08b11008__hi,
	arm_instr_multi_0x08b11008__ls,
	arm_instr_multi_0x08b11008__ge,
	arm_instr_multi_0x08b11008__lt,
	arm_instr_multi_0x08b11008__gt,
	arm_instr_multi_0x08b11008__le,
	arm_instr_multi_0x08b11008,
	arm_instr_nop,
	arm_instr_multi_0x08b15008__eq,
	arm_instr_multi_0x08b15008__ne,
	arm_instr_multi_0x08b15008__cs,
	arm_instr_multi_0x08b15008__cc,
	arm_instr_multi_0x08b15008__mi,
	arm_instr_multi_0x08b15008__pl,
	arm_instr_multi_0x08b15008__vs,
	arm_instr_multi_0x08b15008__vc,
	arm_instr_multi_0x08b15008__hi,
	arm_instr_multi_0x08b15008__ls,
	arm_instr_multi_0x08b15008__ge,
	arm_instr_multi_0x08b15008__lt,
	arm_instr_multi_0x08b15008__gt,
	arm_instr_multi_0x08b15008__le,
	arm_instr_multi_0x08b15008,
	arm_instr_nop,
	arm_instr_multi_0x08931008__eq,
	arm_instr_multi_0x08931008__ne,
	arm_instr_multi_0x08931008__cs,
	arm_instr_multi_0x08931008__cc,
	arm_instr_multi_0x08931008__mi,
	arm_instr_multi_0x08931008__pl,
	arm_instr_multi_0x08931008__vs,
	arm_instr_multi_0x08931008__vc,
	arm_instr_multi_0x08931008__hi,
	arm_instr_multi_0x08931008__ls,
	arm_instr_multi_0x08931008__ge,
	arm_instr_multi_0x08931008__lt,
	arm_instr_multi_0x08931008__gt,
	arm_instr_multi_0x08931008__le,
	arm_instr_multi_0x08931008,
	arm_instr_nop,
	arm_instr_multi_0x08990600__eq,
	arm_instr_multi_0x08990600__ne,
	arm_instr_multi_0x08990600__cs,
	arm_instr_multi_0x08990600__cc,
	arm_instr_multi_0x08990600__mi,
	arm_instr_multi_0x08990600__pl,
	arm_instr_multi_0x08990600__vs,
	arm_instr_multi_0x08990600__vc,
	arm_instr_multi_0x08990600__hi,
	arm_instr_multi_0x08990600__ls,
	arm_instr_multi_0x08990600__ge,
	arm_instr_multi_0x08990600__lt,
	arm_instr_multi_0x08990600__gt,
	arm_instr_multi_0x08990600__le,
	arm_instr_multi_0x08990600,
	arm_instr_nop,
	arm_instr_multi_0x08990003__eq,
	arm_instr_multi_0x08990003__ne,
	arm_instr_multi_0x08990003__cs,
	arm_instr_multi_0x08990003__cc,
	arm_instr_multi_0x08990003__mi,
	arm_instr_multi_0x08990003__pl,
	arm_instr_multi_0x08990003__vs,
	arm_instr_multi_0x08990003__vc,
	arm_instr_multi_0x08990003__hi,
	arm_instr_multi_0x08990003__ls,
	arm_instr_multi_0x08990003__ge,
	arm_instr_multi_0x08990003__lt,
	arm_instr_multi_0x08990003__gt,
	arm_instr_multi_0x08990003__le,
	arm_instr_multi_0x08990003,
	arm_instr_nop,
};
void (*multi_opcode_f_209[96])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08930006__eq,
	arm_instr_multi_0x08930006__ne,
	arm_instr_multi_0x08930006__cs,
	arm_instr_multi_0x08930006__cc,
	arm_instr_multi_0x08930006__mi,
	arm_instr_multi_0x08930006__pl,
	arm_instr_multi_0x08930006__vs,
	arm_instr_multi_0x08930006__vc,
	arm_instr_multi_0x08930006__hi,
	arm_instr_multi_0x08930006__ls,
	arm_instr_multi_0x08930006__ge,
	arm_instr_multi_0x08930006__lt,
	arm_instr_multi_0x08930006__gt,
	arm_instr_multi_0x08930006__le,
	arm_instr_multi_0x08930006,
	arm_instr_nop,
	arm_instr_multi_0x0891000e__eq,
	arm_instr_multi_0x0891000e__ne,
	arm_instr_multi_0x0891000e__cs,
	arm_instr_multi_0x0891000e__cc,
	arm_instr_multi_0x0891000e__mi,
	arm_instr_multi_0x0891000e__pl,
	arm_instr_multi_0x0891000e__vs,
	arm_instr_multi_0x0891000e__vc,
	arm_instr_multi_0x0891000e__hi,
	arm_instr_multi_0x0891000e__ls,
	arm_instr_multi_0x0891000e__ge,
	arm_instr_multi_0x0891000e__lt,
	arm_instr_multi_0x0891000e__gt,
	arm_instr_multi_0x0891000e__le,
	arm_instr_multi_0x0891000e,
	arm_instr_nop,
	arm_instr_multi_0x08910006__eq,
	arm_instr_multi_0x08910006__ne,
	arm_instr_multi_0x08910006__cs,
	arm_instr_multi_0x08910006__cc,
	arm_instr_multi_0x08910006__mi,
	arm_instr_multi_0x08910006__pl,
	arm_instr_multi_0x08910006__vs,
	arm_instr_multi_0x08910006__vc,
	arm_instr_multi_0x08910006__hi,
	arm_instr_multi_0x08910006__ls,
	arm_instr_multi_0x08910006__ge,
	arm_instr_multi_0x08910006__lt,
	arm_instr_multi_0x08910006__gt,
	arm_instr_multi_0x08910006__le,
	arm_instr_multi_0x08910006,
	arm_instr_nop,
	arm_instr_multi_0x09930006__eq,
	arm_instr_multi_0x09930006__ne,
	arm_instr_multi_0x09930006__cs,
	arm_instr_multi_0x09930006__cc,
	arm_instr_multi_0x09930006__mi,
	arm_instr_multi_0x09930006__pl,
	arm_instr_multi_0x09930006__vs,
	arm_instr_multi_0x09930006__vc,
	arm_instr_multi_0x09930006__hi,
	arm_instr_multi_0x09930006__ls,
	arm_instr_multi_0x09930006__ge,
	arm_instr_multi_0x09930006__lt,
	arm_instr_multi_0x09930006__gt,
	arm_instr_multi_0x09930006__le,
	arm_instr_multi_0x09930006,
	arm_instr_nop,
	arm_instr_multi_0x0893000c__eq,
	arm_instr_multi_0x0893000c__ne,
	arm_instr_multi_0x0893000c__cs,
	arm_instr_multi_0x0893000c__cc,
	arm_instr_multi_0x0893000c__mi,
	arm_instr_multi_0x0893000c__pl,
	arm_instr_multi_0x0893000c__vs,
	arm_instr_multi_0x0893000c__vc,
	arm_instr_multi_0x0893000c__hi,
	arm_instr_multi_0x0893000c__ls,
	arm_instr_multi_0x0893000c__ge,
	arm_instr_multi_0x0893000c__lt,
	arm_instr_multi_0x0893000c__gt,
	arm_instr_multi_0x0893000c__le,
	arm_instr_multi_0x0893000c,
	arm_instr_nop,
	arm_instr_multi_0x08990006__eq,
	arm_instr_multi_0x08990006__ne,
	arm_instr_multi_0x08990006__cs,
	arm_instr_multi_0x08990006__cc,
	arm_instr_multi_0x08990006__mi,
	arm_instr_multi_0x08990006__pl,
	arm_instr_multi_0x08990006__vs,
	arm_instr_multi_0x08990006__vc,
	arm_instr_multi_0x08990006__hi,
	arm_instr_multi_0x08990006__ls,
	arm_instr_multi_0x08990006__ge,
	arm_instr_multi_0x08990006__lt,
	arm_instr_multi_0x08990006__gt,
	arm_instr_multi_0x08990006__le,
	arm_instr_multi_0x08990006,
	arm_instr_nop,
};
void (*multi_opcode_f_210[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08b15018__eq,
	arm_instr_multi_0x08b15018__ne,
	arm_instr_multi_0x08b15018__cs,
	arm_instr_multi_0x08b15018__cc,
	arm_instr_multi_0x08b15018__mi,
	arm_instr_multi_0x08b15018__pl,
	arm_instr_multi_0x08b15018__vs,
	arm_instr_multi_0x08b15018__vc,
	arm_instr_multi_0x08b15018__hi,
	arm_instr_multi_0x08b15018__ls,
	arm_instr_multi_0x08b15018__ge,
	arm_instr_multi_0x08b15018__lt,
	arm_instr_multi_0x08b15018__gt,
	arm_instr_multi_0x08b15018__le,
	arm_instr_multi_0x08b15018,
	arm_instr_nop,
	arm_instr_multi_0x08930018__eq,
	arm_instr_multi_0x08930018__ne,
	arm_instr_multi_0x08930018__cs,
	arm_instr_multi_0x08930018__cc,
	arm_instr_multi_0x08930018__mi,
	arm_instr_multi_0x08930018__pl,
	arm_instr_multi_0x08930018__vs,
	arm_instr_multi_0x08930018__vc,
	arm_instr_multi_0x08930018__hi,
	arm_instr_multi_0x08930018__ls,
	arm_instr_multi_0x08930018__ge,
	arm_instr_multi_0x08930018__lt,
	arm_instr_multi_0x08930018__gt,
	arm_instr_multi_0x08930018__le,
	arm_instr_multi_0x08930018,
	arm_instr_nop,
	arm_instr_multi_0x099b0030__eq,
	arm_instr_multi_0x099b0030__ne,
	arm_instr_multi_0x099b0030__cs,
	arm_instr_multi_0x099b0030__cc,
	arm_instr_multi_0x099b0030__mi,
	arm_instr_multi_0x099b0030__pl,
	arm_instr_multi_0x099b0030__vs,
	arm_instr_multi_0x099b0030__vc,
	arm_instr_multi_0x099b0030__hi,
	arm_instr_multi_0x099b0030__ls,
	arm_instr_multi_0x099b0030__ge,
	arm_instr_multi_0x099b0030__lt,
	arm_instr_multi_0x099b0030__gt,
	arm_instr_multi_0x099b0030__le,
	arm_instr_multi_0x099b0030,
	arm_instr_nop,
	arm_instr_multi_0x08910030__eq,
	arm_instr_multi_0x08910030__ne,
	arm_instr_multi_0x08910030__cs,
	arm_instr_multi_0x08910030__cc,
	arm_instr_multi_0x08910030__mi,
	arm_instr_multi_0x08910030__pl,
	arm_instr_multi_0x08910030__vs,
	arm_instr_multi_0x08910030__vc,
	arm_instr_multi_0x08910030__hi,
	arm_instr_multi_0x08910030__ls,
	arm_instr_multi_0x08910030__ge,
	arm_instr_multi_0x08910030__lt,
	arm_instr_multi_0x08910030__gt,
	arm_instr_multi_0x08910030__le,
	arm_instr_multi_0x08910030,
	arm_instr_nop,
	arm_instr_multi_0x08990018__eq,
	arm_instr_multi_0x08990018__ne,
	arm_instr_multi_0x08990018__cs,
	arm_instr_multi_0x08990018__cc,
	arm_instr_multi_0x08990018__mi,
	arm_instr_multi_0x08990018__pl,
	arm_instr_multi_0x08990018__vs,
	arm_instr_multi_0x08990018__vc,
	arm_instr_multi_0x08990018__hi,
	arm_instr_multi_0x08990018__ls,
	arm_instr_multi_0x08990018__ge,
	arm_instr_multi_0x08990018__lt,
	arm_instr_multi_0x08990018__gt,
	arm_instr_multi_0x08990018__le,
	arm_instr_multi_0x08990018,
	arm_instr_nop,
};
void (*multi_opcode_f_212[48])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08930060__eq,
	arm_instr_multi_0x08930060__ne,
	arm_instr_multi_0x08930060__cs,
	arm_instr_multi_0x08930060__cc,
	arm_instr_multi_0x08930060__mi,
	arm_instr_multi_0x08930060__pl,
	arm_instr_multi_0x08930060__vs,
	arm_instr_multi_0x08930060__vc,
	arm_instr_multi_0x08930060__hi,
	arm_instr_multi_0x08930060__ls,
	arm_instr_multi_0x08930060__ge,
	arm_instr_multi_0x08930060__lt,
	arm_instr_multi_0x08930060__gt,
	arm_instr_multi_0x08930060__le,
	arm_instr_multi_0x08930060,
	arm_instr_nop,
	arm_instr_multi_0x089100c0__eq,
	arm_instr_multi_0x089100c0__ne,
	arm_instr_multi_0x089100c0__cs,
	arm_instr_multi_0x089100c0__cc,
	arm_instr_multi_0x089100c0__mi,
	arm_instr_multi_0x089100c0__pl,
	arm_instr_multi_0x089100c0__vs,
	arm_instr_multi_0x089100c0__vc,
	arm_instr_multi_0x089100c0__hi,
	arm_instr_multi_0x089100c0__ls,
	arm_instr_multi_0x089100c0__ge,
	arm_instr_multi_0x089100c0__lt,
	arm_instr_multi_0x089100c0__gt,
	arm_instr_multi_0x089100c0__le,
	arm_instr_multi_0x089100c0,
	arm_instr_nop,
	arm_instr_multi_0x089300c0__eq,
	arm_instr_multi_0x089300c0__ne,
	arm_instr_multi_0x089300c0__cs,
	arm_instr_multi_0x089300c0__cc,
	arm_instr_multi_0x089300c0__mi,
	arm_instr_multi_0x089300c0__pl,
	arm_instr_multi_0x089300c0__vs,
	arm_instr_multi_0x089300c0__vc,
	arm_instr_multi_0x089300c0__hi,
	arm_instr_multi_0x089300c0__ls,
	arm_instr_multi_0x089300c0__ge,
	arm_instr_multi_0x089300c0__lt,
	arm_instr_multi_0x089300c0__gt,
	arm_instr_multi_0x089300c0__le,
	arm_instr_multi_0x089300c0,
	arm_instr_nop,
};
void (*multi_opcode_f_216[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08930180__eq,
	arm_instr_multi_0x08930180__ne,
	arm_instr_multi_0x08930180__cs,
	arm_instr_multi_0x08930180__cc,
	arm_instr_multi_0x08930180__mi,
	arm_instr_multi_0x08930180__pl,
	arm_instr_multi_0x08930180__vs,
	arm_instr_multi_0x08930180__vc,
	arm_instr_multi_0x08930180__hi,
	arm_instr_multi_0x08930180__ls,
	arm_instr_multi_0x08930180__ge,
	arm_instr_multi_0x08930180__lt,
	arm_instr_multi_0x08930180__gt,
	arm_instr_multi_0x08930180__le,
	arm_instr_multi_0x08930180,
	arm_instr_nop,
	arm_instr_multi_0x099b0180__eq,
	arm_instr_multi_0x099b0180__ne,
	arm_instr_multi_0x099b0180__cs,
	arm_instr_multi_0x099b0180__cc,
	arm_instr_multi_0x099b0180__mi,
	arm_instr_multi_0x099b0180__pl,
	arm_instr_multi_0x099b0180__vs,
	arm_instr_multi_0x099b0180__vc,
	arm_instr_multi_0x099b0180__hi,
	arm_instr_multi_0x099b0180__ls,
	arm_instr_multi_0x099b0180__ge,
	arm_instr_multi_0x099b0180__lt,
	arm_instr_multi_0x099b0180__gt,
	arm_instr_multi_0x099b0180__le,
	arm_instr_multi_0x099b0180,
	arm_instr_nop,
};
void (*multi_opcode_f_224[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08940003__eq,
	arm_instr_multi_0x08940003__ne,
	arm_instr_multi_0x08940003__cs,
	arm_instr_multi_0x08940003__cc,
	arm_instr_multi_0x08940003__mi,
	arm_instr_multi_0x08940003__pl,
	arm_instr_multi_0x08940003__vs,
	arm_instr_multi_0x08940003__vc,
	arm_instr_multi_0x08940003__hi,
	arm_instr_multi_0x08940003__ls,
	arm_instr_multi_0x08940003__ge,
	arm_instr_multi_0x08940003__lt,
	arm_instr_multi_0x08940003__gt,
	arm_instr_multi_0x08940003__le,
	arm_instr_multi_0x08940003,
	arm_instr_nop,
	arm_instr_multi_0x089e000a__eq,
	arm_instr_multi_0x089e000a__ne,
	arm_instr_multi_0x089e000a__cs,
	arm_instr_multi_0x089e000a__cc,
	arm_instr_multi_0x089e000a__mi,
	arm_instr_multi_0x089e000a__pl,
	arm_instr_multi_0x089e000a__vs,
	arm_instr_multi_0x089e000a__vc,
	arm_instr_multi_0x089e000a__hi,
	arm_instr_multi_0x089e000a__ls,
	arm_instr_multi_0x089e000a__ge,
	arm_instr_multi_0x089e000a__lt,
	arm_instr_multi_0x089e000a__gt,
	arm_instr_multi_0x089e000a__le,
	arm_instr_multi_0x089e000a,
	arm_instr_nop,
	arm_instr_multi_0x0894000a__eq,
	arm_instr_multi_0x0894000a__ne,
	arm_instr_multi_0x0894000a__cs,
	arm_instr_multi_0x0894000a__cc,
	arm_instr_multi_0x0894000a__mi,
	arm_instr_multi_0x0894000a__pl,
	arm_instr_multi_0x0894000a__vs,
	arm_instr_multi_0x0894000a__vc,
	arm_instr_multi_0x0894000a__hi,
	arm_instr_multi_0x0894000a__ls,
	arm_instr_multi_0x0894000a__ge,
	arm_instr_multi_0x0894000a__lt,
	arm_instr_multi_0x0894000a__gt,
	arm_instr_multi_0x0894000a__le,
	arm_instr_multi_0x0894000a,
	arm_instr_nop,
	arm_instr_multi_0x08940009__eq,
	arm_instr_multi_0x08940009__ne,
	arm_instr_multi_0x08940009__cs,
	arm_instr_multi_0x08940009__cc,
	arm_instr_multi_0x08940009__mi,
	arm_instr_multi_0x08940009__pl,
	arm_instr_multi_0x08940009__vs,
	arm_instr_multi_0x08940009__vc,
	arm_instr_multi_0x08940009__hi,
	arm_instr_multi_0x08940009__ls,
	arm_instr_multi_0x08940009__ge,
	arm_instr_multi_0x08940009__lt,
	arm_instr_multi_0x08940009__gt,
	arm_instr_multi_0x08940009__le,
	arm_instr_multi_0x08940009,
	arm_instr_nop,
	arm_instr_multi_0x089c5000__eq,
	arm_instr_multi_0x089c5000__ne,
	arm_instr_multi_0x089c5000__cs,
	arm_instr_multi_0x089c5000__cc,
	arm_instr_multi_0x089c5000__mi,
	arm_instr_multi_0x089c5000__pl,
	arm_instr_multi_0x089c5000__vs,
	arm_instr_multi_0x089c5000__vc,
	arm_instr_multi_0x089c5000__hi,
	arm_instr_multi_0x089c5000__ls,
	arm_instr_multi_0x089c5000__ge,
	arm_instr_multi_0x089c5000__lt,
	arm_instr_multi_0x089c5000__gt,
	arm_instr_multi_0x089c5000__le,
	arm_instr_multi_0x089c5000,
	arm_instr_nop,
};
void (*multi_opcode_f_225[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x0894000c__eq,
	arm_instr_multi_0x0894000c__ne,
	arm_instr_multi_0x0894000c__cs,
	arm_instr_multi_0x0894000c__cc,
	arm_instr_multi_0x0894000c__mi,
	arm_instr_multi_0x0894000c__pl,
	arm_instr_multi_0x0894000c__vs,
	arm_instr_multi_0x0894000c__vc,
	arm_instr_multi_0x0894000c__hi,
	arm_instr_multi_0x0894000c__ls,
	arm_instr_multi_0x0894000c__ge,
	arm_instr_multi_0x0894000c__lt,
	arm_instr_multi_0x0894000c__gt,
	arm_instr_multi_0x0894000c__le,
	arm_instr_multi_0x0894000c,
	arm_instr_nop,
	arm_instr_multi_0x089c0006__eq,
	arm_instr_multi_0x089c0006__ne,
	arm_instr_multi_0x089c0006__cs,
	arm_instr_multi_0x089c0006__cc,
	arm_instr_multi_0x089c0006__mi,
	arm_instr_multi_0x089c0006__pl,
	arm_instr_multi_0x089c0006__vs,
	arm_instr_multi_0x089c0006__vc,
	arm_instr_multi_0x089c0006__hi,
	arm_instr_multi_0x089c0006__ls,
	arm_instr_multi_0x089c0006__ge,
	arm_instr_multi_0x089c0006__lt,
	arm_instr_multi_0x089c0006__gt,
	arm_instr_multi_0x089c0006__le,
	arm_instr_multi_0x089c0006,
	arm_instr_nop,
	arm_instr_multi_0x0896000c__eq,
	arm_instr_multi_0x0896000c__ne,
	arm_instr_multi_0x0896000c__cs,
	arm_instr_multi_0x0896000c__cc,
	arm_instr_multi_0x0896000c__mi,
	arm_instr_multi_0x0896000c__pl,
	arm_instr_multi_0x0896000c__vs,
	arm_instr_multi_0x0896000c__vc,
	arm_instr_multi_0x0896000c__hi,
	arm_instr_multi_0x0896000c__ls,
	arm_instr_multi_0x0896000c__ge,
	arm_instr_multi_0x0896000c__lt,
	arm_instr_multi_0x0896000c__gt,
	arm_instr_multi_0x0896000c__le,
	arm_instr_multi_0x0896000c,
	arm_instr_nop,
	arm_instr_multi_0x089c000c__eq,
	arm_instr_multi_0x089c000c__ne,
	arm_instr_multi_0x089c000c__cs,
	arm_instr_multi_0x089c000c__cc,
	arm_instr_multi_0x089c000c__mi,
	arm_instr_multi_0x089c000c__pl,
	arm_instr_multi_0x089c000c__vs,
	arm_instr_multi_0x089c000c__vc,
	arm_instr_multi_0x089c000c__hi,
	arm_instr_multi_0x089c000c__ls,
	arm_instr_multi_0x089c000c__ge,
	arm_instr_multi_0x089c000c__lt,
	arm_instr_multi_0x089c000c__gt,
	arm_instr_multi_0x089c000c__le,
	arm_instr_multi_0x089c000c,
	arm_instr_nop,
	arm_instr_multi_0x08be000f__eq,
	arm_instr_multi_0x08be000f__ne,
	arm_instr_multi_0x08be000f__cs,
	arm_instr_multi_0x08be000f__cc,
	arm_instr_multi_0x08be000f__mi,
	arm_instr_multi_0x08be000f__pl,
	arm_instr_multi_0x08be000f__vs,
	arm_instr_multi_0x08be000f__vc,
	arm_instr_multi_0x08be000f__hi,
	arm_instr_multi_0x08be000f__ls,
	arm_instr_multi_0x08be000f__ge,
	arm_instr_multi_0x08be000f__lt,
	arm_instr_multi_0x08be000f__gt,
	arm_instr_multi_0x08be000f__le,
	arm_instr_multi_0x08be000f,
	arm_instr_nop,
};
void (*multi_opcode_f_226[112])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x089e0018__eq,
	arm_instr_multi_0x089e0018__ne,
	arm_instr_multi_0x089e0018__cs,
	arm_instr_multi_0x089e0018__cc,
	arm_instr_multi_0x089e0018__mi,
	arm_instr_multi_0x089e0018__pl,
	arm_instr_multi_0x089e0018__vs,
	arm_instr_multi_0x089e0018__vc,
	arm_instr_multi_0x089e0018__hi,
	arm_instr_multi_0x089e0018__ls,
	arm_instr_multi_0x089e0018__ge,
	arm_instr_multi_0x089e0018__lt,
	arm_instr_multi_0x089e0018__gt,
	arm_instr_multi_0x089e0018__le,
	arm_instr_multi_0x089e0018,
	arm_instr_nop,
	arm_instr_multi_0x09940018__eq,
	arm_instr_multi_0x09940018__ne,
	arm_instr_multi_0x09940018__cs,
	arm_instr_multi_0x09940018__cc,
	arm_instr_multi_0x09940018__mi,
	arm_instr_multi_0x09940018__pl,
	arm_instr_multi_0x09940018__vs,
	arm_instr_multi_0x09940018__vc,
	arm_instr_multi_0x09940018__hi,
	arm_instr_multi_0x09940018__ls,
	arm_instr_multi_0x09940018__ge,
	arm_instr_multi_0x09940018__lt,
	arm_instr_multi_0x09940018__gt,
	arm_instr_multi_0x09940018__le,
	arm_instr_multi_0x09940018,
	arm_instr_nop,
	arm_instr_multi_0x089c0018__eq,
	arm_instr_multi_0x089c0018__ne,
	arm_instr_multi_0x089c0018__cs,
	arm_instr_multi_0x089c0018__cc,
	arm_instr_multi_0x089c0018__mi,
	arm_instr_multi_0x089c0018__pl,
	arm_instr_multi_0x089c0018__vs,
	arm_instr_multi_0x089c0018__vc,
	arm_instr_multi_0x089c0018__hi,
	arm_instr_multi_0x089c0018__ls,
	arm_instr_multi_0x089c0018__ge,
	arm_instr_multi_0x089c0018__lt,
	arm_instr_multi_0x089c0018__gt,
	arm_instr_multi_0x089c0018__le,
	arm_instr_multi_0x089c0018,
	arm_instr_nop,
	arm_instr_multi_0x089e0030__eq,
	arm_instr_multi_0x089e0030__ne,
	arm_instr_multi_0x089e0030__cs,
	arm_instr_multi_0x089e0030__cc,
	arm_instr_multi_0x089e0030__mi,
	arm_instr_multi_0x089e0030__pl,
	arm_instr_multi_0x089e0030__vs,
	arm_instr_multi_0x089e0030__vc,
	arm_instr_multi_0x089e0030__hi,
	arm_instr_multi_0x089e0030__ls,
	arm_instr_multi_0x089e0030__ge,
	arm_instr_multi_0x089e0030__lt,
	arm_instr_multi_0x089e0030__gt,
	arm_instr_multi_0x089e0030__le,
	arm_instr_multi_0x089e0030,
	arm_instr_nop,
	arm_instr_multi_0x08940012__eq,
	arm_instr_multi_0x08940012__ne,
	arm_instr_multi_0x08940012__cs,
	arm_instr_multi_0x08940012__cc,
	arm_instr_multi_0x08940012__mi,
	arm_instr_multi_0x08940012__pl,
	arm_instr_multi_0x08940012__vs,
	arm_instr_multi_0x08940012__vc,
	arm_instr_multi_0x08940012__hi,
	arm_instr_multi_0x08940012__ls,
	arm_instr_multi_0x08940012__ge,
	arm_instr_multi_0x08940012__lt,
	arm_instr_multi_0x08940012__gt,
	arm_instr_multi_0x08940012__le,
	arm_instr_multi_0x08940012,
	arm_instr_nop,
	arm_instr_multi_0x08940018__eq,
	arm_instr_multi_0x08940018__ne,
	arm_instr_multi_0x08940018__cs,
	arm_instr_multi_0x08940018__cc,
	arm_instr_multi_0x08940018__mi,
	arm_instr_multi_0x08940018__pl,
	arm_instr_multi_0x08940018__vs,
	arm_instr_multi_0x08940018__vc,
	arm_instr_multi_0x08940018__hi,
	arm_instr_multi_0x08940018__ls,
	arm_instr_multi_0x08940018__ge,
	arm_instr_multi_0x08940018__lt,
	arm_instr_multi_0x08940018__gt,
	arm_instr_multi_0x08940018__le,
	arm_instr_multi_0x08940018,
	arm_instr_nop,
	arm_instr_multi_0x08960030__eq,
	arm_instr_multi_0x08960030__ne,
	arm_instr_multi_0x08960030__cs,
	arm_instr_multi_0x08960030__cc,
	arm_instr_multi_0x08960030__mi,
	arm_instr_multi_0x08960030__pl,
	arm_instr_multi_0x08960030__vs,
	arm_instr_multi_0x08960030__vc,
	arm_instr_multi_0x08960030__hi,
	arm_instr_multi_0x08960030__ls,
	arm_instr_multi_0x08960030__ge,
	arm_instr_multi_0x08960030__lt,
	arm_instr_multi_0x08960030__gt,
	arm_instr_multi_0x08960030__le,
	arm_instr_multi_0x08960030,
	arm_instr_nop,
};
void (*multi_opcode_f_228[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x089e0060__eq,
	arm_instr_multi_0x089e0060__ne,
	arm_instr_multi_0x089e0060__cs,
	arm_instr_multi_0x089e0060__cc,
	arm_instr_multi_0x089e0060__mi,
	arm_instr_multi_0x089e0060__pl,
	arm_instr_multi_0x089e0060__vs,
	arm_instr_multi_0x089e0060__vc,
	arm_instr_multi_0x089e0060__hi,
	arm_instr_multi_0x089e0060__ls,
	arm_instr_multi_0x089e0060__ge,
	arm_instr_multi_0x089e0060__lt,
	arm_instr_multi_0x089e0060__gt,
	arm_instr_multi_0x089e0060__le,
	arm_instr_multi_0x089e0060,
	arm_instr_nop,
};
void (*multi_opcode_f_232[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x099c0180__eq,
	arm_instr_multi_0x099c0180__ne,
	arm_instr_multi_0x099c0180__cs,
	arm_instr_multi_0x099c0180__cc,
	arm_instr_multi_0x099c0180__mi,
	arm_instr_multi_0x099c0180__pl,
	arm_instr_multi_0x099c0180__vs,
	arm_instr_multi_0x099c0180__vc,
	arm_instr_multi_0x099c0180__hi,
	arm_instr_multi_0x099c0180__ls,
	arm_instr_multi_0x099c0180__ge,
	arm_instr_multi_0x099c0180__lt,
	arm_instr_multi_0x099c0180__gt,
	arm_instr_multi_0x099c0180__le,
	arm_instr_multi_0x099c0180,
	arm_instr_nop,
	arm_instr_multi_0x089c0300__eq,
	arm_instr_multi_0x089c0300__ne,
	arm_instr_multi_0x089c0300__cs,
	arm_instr_multi_0x089c0300__cc,
	arm_instr_multi_0x089c0300__mi,
	arm_instr_multi_0x089c0300__pl,
	arm_instr_multi_0x089c0300__vs,
	arm_instr_multi_0x089c0300__vc,
	arm_instr_multi_0x089c0300__hi,
	arm_instr_multi_0x089c0300__ls,
	arm_instr_multi_0x089c0300__ge,
	arm_instr_multi_0x089c0300__lt,
	arm_instr_multi_0x089c0300__gt,
	arm_instr_multi_0x089c0300__le,
	arm_instr_multi_0x089c0300,
	arm_instr_nop,
};
void (*multi_opcode_f_240[96])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08bd8000__eq,
	arm_instr_multi_0x08bd8000__ne,
	arm_instr_multi_0x08bd8000__cs,
	arm_instr_multi_0x08bd8000__cc,
	arm_instr_multi_0x08bd8000__mi,
	arm_instr_multi_0x08bd8000__pl,
	arm_instr_multi_0x08bd8000__vs,
	arm_instr_multi_0x08bd8000__vc,
	arm_instr_multi_0x08bd8000__hi,
	arm_instr_multi_0x08bd8000__ls,
	arm_instr_multi_0x08bd8000__ge,
	arm_instr_multi_0x08bd8000__lt,
	arm_instr_multi_0x08bd8000__gt,
	arm_instr_multi_0x08bd8000__le,
	arm_instr_multi_0x08bd8000,
	arm_instr_nop,
	arm_instr_multi_0x08bd8001__eq,
	arm_instr_multi_0x08bd8001__ne,
	arm_instr_multi_0x08bd8001__cs,
	arm_instr_multi_0x08bd8001__cc,
	arm_instr_multi_0x08bd8001__mi,
	arm_instr_multi_0x08bd8001__pl,
	arm_instr_multi_0x08bd8001__vs,
	arm_instr_multi_0x08bd8001__vc,
	arm_instr_multi_0x08bd8001__hi,
	arm_instr_multi_0x08bd8001__ls,
	arm_instr_multi_0x08bd8001__ge,
	arm_instr_multi_0x08bd8001__lt,
	arm_instr_multi_0x08bd8001__gt,
	arm_instr_multi_0x08bd8001__le,
	arm_instr_multi_0x08bd8001,
	arm_instr_nop,
	arm_instr_multi_0x08950003__eq,
	arm_instr_multi_0x08950003__ne,
	arm_instr_multi_0x08950003__cs,
	arm_instr_multi_0x08950003__cc,
	arm_instr_multi_0x08950003__mi,
	arm_instr_multi_0x08950003__pl,
	arm_instr_multi_0x08950003__vs,
	arm_instr_multi_0x08950003__vc,
	arm_instr_multi_0x08950003__hi,
	arm_instr_multi_0x08950003__ls,
	arm_instr_multi_0x08950003__ge,
	arm_instr_multi_0x08950003__lt,
	arm_instr_multi_0x08950003__gt,
	arm_instr_multi_0x08950003__le,
	arm_instr_multi_0x08950003,
	arm_instr_nop,
	arm_instr_multi_0x08bd0400__eq,
	arm_instr_multi_0x08bd0400__ne,
	arm_instr_multi_0x08bd0400__cs,
	arm_instr_multi_0x08bd0400__cc,
	arm_instr_multi_0x08bd0400__mi,
	arm_instr_multi_0x08bd0400__pl,
	arm_instr_multi_0x08bd0400__vs,
	arm_instr_multi_0x08bd0400__vc,
	arm_instr_multi_0x08bd0400__hi,
	arm_instr_multi_0x08bd0400__ls,
	arm_instr_multi_0x08bd0400__ge,
	arm_instr_multi_0x08bd0400__lt,
	arm_instr_multi_0x08bd0400__gt,
	arm_instr_multi_0x08bd0400__le,
	arm_instr_multi_0x08bd0400,
	arm_instr_nop,
	arm_instr_multi_0x08970600__eq,
	arm_instr_multi_0x08970600__ne,
	arm_instr_multi_0x08970600__cs,
	arm_instr_multi_0x08970600__cc,
	arm_instr_multi_0x08970600__mi,
	arm_instr_multi_0x08970600__pl,
	arm_instr_multi_0x08970600__vs,
	arm_instr_multi_0x08970600__vc,
	arm_instr_multi_0x08970600__hi,
	arm_instr_multi_0x08970600__ls,
	arm_instr_multi_0x08970600__ge,
	arm_instr_multi_0x08970600__lt,
	arm_instr_multi_0x08970600__gt,
	arm_instr_multi_0x08970600__le,
	arm_instr_multi_0x08970600,
	arm_instr_nop,
	arm_instr_multi_0x08bd8400__eq,
	arm_instr_multi_0x08bd8400__ne,
	arm_instr_multi_0x08bd8400__cs,
	arm_instr_multi_0x08bd8400__cc,
	arm_instr_multi_0x08bd8400__mi,
	arm_instr_multi_0x08bd8400__pl,
	arm_instr_multi_0x08bd8400__vs,
	arm_instr_multi_0x08bd8400__vc,
	arm_instr_multi_0x08bd8400__hi,
	arm_instr_multi_0x08bd8400__ls,
	arm_instr_multi_0x08bd8400__ge,
	arm_instr_multi_0x08bd8400__lt,
	arm_instr_multi_0x08bd8400__gt,
	arm_instr_multi_0x08bd8400__le,
	arm_instr_multi_0x08bd8400,
	arm_instr_nop,
};
void (*multi_opcode_f_241[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08950006__eq,
	arm_instr_multi_0x08950006__ne,
	arm_instr_multi_0x08950006__cs,
	arm_instr_multi_0x08950006__cc,
	arm_instr_multi_0x08950006__mi,
	arm_instr_multi_0x08950006__pl,
	arm_instr_multi_0x08950006__vs,
	arm_instr_multi_0x08950006__vc,
	arm_instr_multi_0x08950006__hi,
	arm_instr_multi_0x08950006__ls,
	arm_instr_multi_0x08950006__ge,
	arm_instr_multi_0x08950006__lt,
	arm_instr_multi_0x08950006__gt,
	arm_instr_multi_0x08950006__le,
	arm_instr_multi_0x08950006,
	arm_instr_nop,
	arm_instr_multi_0x08970006__eq,
	arm_instr_multi_0x08970006__ne,
	arm_instr_multi_0x08970006__cs,
	arm_instr_multi_0x08970006__cc,
	arm_instr_multi_0x08970006__mi,
	arm_instr_multi_0x08970006__pl,
	arm_instr_multi_0x08970006__vs,
	arm_instr_multi_0x08970006__vc,
	arm_instr_multi_0x08970006__hi,
	arm_instr_multi_0x08970006__ls,
	arm_instr_multi_0x08970006__ge,
	arm_instr_multi_0x08970006__lt,
	arm_instr_multi_0x08970006__gt,
	arm_instr_multi_0x08970006__le,
	arm_instr_multi_0x08970006,
	arm_instr_nop,
};
void (*multi_opcode_f_242[112])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08bd8010__eq,
	arm_instr_multi_0x08bd8010__ne,
	arm_instr_multi_0x08bd8010__cs,
	arm_instr_multi_0x08bd8010__cc,
	arm_instr_multi_0x08bd8010__mi,
	arm_instr_multi_0x08bd8010__pl,
	arm_instr_multi_0x08bd8010__vs,
	arm_instr_multi_0x08bd8010__vc,
	arm_instr_multi_0x08bd8010__hi,
	arm_instr_multi_0x08bd8010__ls,
	arm_instr_multi_0x08bd8010__ge,
	arm_instr_multi_0x08bd8010__lt,
	arm_instr_multi_0x08bd8010__gt,
	arm_instr_multi_0x08bd8010__le,
	arm_instr_multi_0x08bd8010,
	arm_instr_nop,
	arm_instr_multi_0x08bd8030__eq,
	arm_instr_multi_0x08bd8030__ne,
	arm_instr_multi_0x08bd8030__cs,
	arm_instr_multi_0x08bd8030__cc,
	arm_instr_multi_0x08bd8030__mi,
	arm_instr_multi_0x08bd8030__pl,
	arm_instr_multi_0x08bd8030__vs,
	arm_instr_multi_0x08bd8030__vc,
	arm_instr_multi_0x08bd8030__hi,
	arm_instr_multi_0x08bd8030__ls,
	arm_instr_multi_0x08bd8030__ge,
	arm_instr_multi_0x08bd8030__lt,
	arm_instr_multi_0x08bd8030__gt,
	arm_instr_multi_0x08bd8030__le,
	arm_instr_multi_0x08bd8030,
	arm_instr_nop,
	arm_instr_multi_0x08bd0030__eq,
	arm_instr_multi_0x08bd0030__ne,
	arm_instr_multi_0x08bd0030__cs,
	arm_instr_multi_0x08bd0030__cc,
	arm_instr_multi_0x08bd0030__mi,
	arm_instr_multi_0x08bd0030__pl,
	arm_instr_multi_0x08bd0030__vs,
	arm_instr_multi_0x08bd0030__vc,
	arm_instr_multi_0x08bd0030__hi,
	arm_instr_multi_0x08bd0030__ls,
	arm_instr_multi_0x08bd0030__ge,
	arm_instr_multi_0x08bd0030__lt,
	arm_instr_multi_0x08bd0030__gt,
	arm_instr_multi_0x08bd0030__le,
	arm_instr_multi_0x08bd0030,
	arm_instr_nop,
	arm_instr_multi_0x08bd0010__eq,
	arm_instr_multi_0x08bd0010__ne,
	arm_instr_multi_0x08bd0010__cs,
	arm_instr_multi_0x08bd0010__cc,
	arm_instr_multi_0x08bd0010__mi,
	arm_instr_multi_0x08bd0010__pl,
	arm_instr_multi_0x08bd0010__vs,
	arm_instr_multi_0x08bd0010__vc,
	arm_instr_multi_0x08bd0010__hi,
	arm_instr_multi_0x08bd0010__ls,
	arm_instr_multi_0x08bd0010__ge,
	arm_instr_multi_0x08bd0010__lt,
	arm_instr_multi_0x08bd0010__gt,
	arm_instr_multi_0x08bd0010__le,
	arm_instr_multi_0x08bd0010,
	arm_instr_nop,
	arm_instr_multi_0x08bd4010__eq,
	arm_instr_multi_0x08bd4010__ne,
	arm_instr_multi_0x08bd4010__cs,
	arm_instr_multi_0x08bd4010__cc,
	arm_instr_multi_0x08bd4010__mi,
	arm_instr_multi_0x08bd4010__pl,
	arm_instr_multi_0x08bd4010__vs,
	arm_instr_multi_0x08bd4010__vc,
	arm_instr_multi_0x08bd4010__hi,
	arm_instr_multi_0x08bd4010__ls,
	arm_instr_multi_0x08bd4010__ge,
	arm_instr_multi_0x08bd4010__lt,
	arm_instr_multi_0x08bd4010__gt,
	arm_instr_multi_0x08bd4010__le,
	arm_instr_multi_0x08bd4010,
	arm_instr_nop,
	arm_instr_multi_0x08950030__eq,
	arm_instr_multi_0x08950030__ne,
	arm_instr_multi_0x08950030__cs,
	arm_instr_multi_0x08950030__cc,
	arm_instr_multi_0x08950030__mi,
	arm_instr_multi_0x08950030__pl,
	arm_instr_multi_0x08950030__vs,
	arm_instr_multi_0x08950030__vc,
	arm_instr_multi_0x08950030__hi,
	arm_instr_multi_0x08950030__ls,
	arm_instr_multi_0x08950030__ge,
	arm_instr_multi_0x08950030__lt,
	arm_instr_multi_0x08950030__gt,
	arm_instr_multi_0x08950030__le,
	arm_instr_multi_0x08950030,
	arm_instr_nop,
	arm_instr_multi_0x08970030__eq,
	arm_instr_multi_0x08970030__ne,
	arm_instr_multi_0x08970030__cs,
	arm_instr_multi_0x08970030__cc,
	arm_instr_multi_0x08970030__mi,
	arm_instr_multi_0x08970030__pl,
	arm_instr_multi_0x08970030__vs,
	arm_instr_multi_0x08970030__vc,
	arm_instr_multi_0x08970030__hi,
	arm_instr_multi_0x08970030__ls,
	arm_instr_multi_0x08970030__ge,
	arm_instr_multi_0x08970030__lt,
	arm_instr_multi_0x08970030__gt,
	arm_instr_multi_0x08970030__le,
	arm_instr_multi_0x08970030,
	arm_instr_nop,
};
void (*multi_opcode_f_243[16])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08bd4c1f__eq,
	arm_instr_multi_0x08bd4c1f__ne,
	arm_instr_multi_0x08bd4c1f__cs,
	arm_instr_multi_0x08bd4c1f__cc,
	arm_instr_multi_0x08bd4c1f__mi,
	arm_instr_multi_0x08bd4c1f__pl,
	arm_instr_multi_0x08bd4c1f__vs,
	arm_instr_multi_0x08bd4c1f__vc,
	arm_instr_multi_0x08bd4c1f__hi,
	arm_instr_multi_0x08bd4c1f__ls,
	arm_instr_multi_0x08bd4c1f__ge,
	arm_instr_multi_0x08bd4c1f__lt,
	arm_instr_multi_0x08bd4c1f__gt,
	arm_instr_multi_0x08bd4c1f__le,
	arm_instr_multi_0x08bd4c1f,
	arm_instr_nop,
};
void (*multi_opcode_f_244[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08971040__eq,
	arm_instr_multi_0x08971040__ne,
	arm_instr_multi_0x08971040__cs,
	arm_instr_multi_0x08971040__cc,
	arm_instr_multi_0x08971040__mi,
	arm_instr_multi_0x08971040__pl,
	arm_instr_multi_0x08971040__vs,
	arm_instr_multi_0x08971040__vc,
	arm_instr_multi_0x08971040__hi,
	arm_instr_multi_0x08971040__ls,
	arm_instr_multi_0x08971040__ge,
	arm_instr_multi_0x08971040__lt,
	arm_instr_multi_0x08971040__gt,
	arm_instr_multi_0x08971040__le,
	arm_instr_multi_0x08971040,
	arm_instr_nop,
	arm_instr_multi_0x08950060__eq,
	arm_instr_multi_0x08950060__ne,
	arm_instr_multi_0x08950060__cs,
	arm_instr_multi_0x08950060__cc,
	arm_instr_multi_0x08950060__mi,
	arm_instr_multi_0x08950060__pl,
	arm_instr_multi_0x08950060__vs,
	arm_instr_multi_0x08950060__vc,
	arm_instr_multi_0x08950060__hi,
	arm_instr_multi_0x08950060__ls,
	arm_instr_multi_0x08950060__ge,
	arm_instr_multi_0x08950060__lt,
	arm_instr_multi_0x08950060__gt,
	arm_instr_multi_0x08950060__le,
	arm_instr_multi_0x08950060,
	arm_instr_nop,
};
void (*multi_opcode_f_246[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08bd8070__eq,
	arm_instr_multi_0x08bd8070__ne,
	arm_instr_multi_0x08bd8070__cs,
	arm_instr_multi_0x08bd8070__cc,
	arm_instr_multi_0x08bd8070__mi,
	arm_instr_multi_0x08bd8070__pl,
	arm_instr_multi_0x08bd8070__vs,
	arm_instr_multi_0x08bd8070__vc,
	arm_instr_multi_0x08bd8070__hi,
	arm_instr_multi_0x08bd8070__ls,
	arm_instr_multi_0x08bd8070__ge,
	arm_instr_multi_0x08bd8070__lt,
	arm_instr_multi_0x08bd8070__gt,
	arm_instr_multi_0x08bd8070__le,
	arm_instr_multi_0x08bd8070,
	arm_instr_nop,
	arm_instr_multi_0x08bd40f0__eq,
	arm_instr_multi_0x08bd40f0__ne,
	arm_instr_multi_0x08bd40f0__cs,
	arm_instr_multi_0x08bd40f0__cc,
	arm_instr_multi_0x08bd40f0__mi,
	arm_instr_multi_0x08bd40f0__pl,
	arm_instr_multi_0x08bd40f0__vs,
	arm_instr_multi_0x08bd40f0__vc,
	arm_instr_multi_0x08bd40f0__hi,
	arm_instr_multi_0x08bd40f0__ls,
	arm_instr_multi_0x08bd40f0__ge,
	arm_instr_multi_0x08bd40f0__lt,
	arm_instr_multi_0x08bd40f0__gt,
	arm_instr_multi_0x08bd40f0__le,
	arm_instr_multi_0x08bd40f0,
	arm_instr_nop,
	arm_instr_multi_0x08bd80f0__eq,
	arm_instr_multi_0x08bd80f0__ne,
	arm_instr_multi_0x08bd80f0__cs,
	arm_instr_multi_0x08bd80f0__cc,
	arm_instr_multi_0x08bd80f0__mi,
	arm_instr_multi_0x08bd80f0__pl,
	arm_instr_multi_0x08bd80f0__vs,
	arm_instr_multi_0x08bd80f0__vc,
	arm_instr_multi_0x08bd80f0__hi,
	arm_instr_multi_0x08bd80f0__ls,
	arm_instr_multi_0x08bd80f0__ge,
	arm_instr_multi_0x08bd80f0__lt,
	arm_instr_multi_0x08bd80f0__gt,
	arm_instr_multi_0x08bd80f0__le,
	arm_instr_multi_0x08bd80f0,
	arm_instr_nop,
	arm_instr_multi_0x08bd0070__eq,
	arm_instr_multi_0x08bd0070__ne,
	arm_instr_multi_0x08bd0070__cs,
	arm_instr_multi_0x08bd0070__cc,
	arm_instr_multi_0x08bd0070__mi,
	arm_instr_multi_0x08bd0070__pl,
	arm_instr_multi_0x08bd0070__vs,
	arm_instr_multi_0x08bd0070__vc,
	arm_instr_multi_0x08bd0070__hi,
	arm_instr_multi_0x08bd0070__ls,
	arm_instr_multi_0x08bd0070__ge,
	arm_instr_multi_0x08bd0070__lt,
	arm_instr_multi_0x08bd0070__gt,
	arm_instr_multi_0x08bd0070__le,
	arm_instr_multi_0x08bd0070,
	arm_instr_nop,
	arm_instr_multi_0x08bd00f0__eq,
	arm_instr_multi_0x08bd00f0__ne,
	arm_instr_multi_0x08bd00f0__cs,
	arm_instr_multi_0x08bd00f0__cc,
	arm_instr_multi_0x08bd00f0__mi,
	arm_instr_multi_0x08bd00f0__pl,
	arm_instr_multi_0x08bd00f0__vs,
	arm_instr_multi_0x08bd00f0__vc,
	arm_instr_multi_0x08bd00f0__hi,
	arm_instr_multi_0x08bd00f0__ls,
	arm_instr_multi_0x08bd00f0__ge,
	arm_instr_multi_0x08bd00f0__lt,
	arm_instr_multi_0x08bd00f0__gt,
	arm_instr_multi_0x08bd00f0__le,
	arm_instr_multi_0x08bd00f0,
	arm_instr_nop,
};
void (*multi_opcode_f_248[32])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08970300__eq,
	arm_instr_multi_0x08970300__ne,
	arm_instr_multi_0x08970300__cs,
	arm_instr_multi_0x08970300__cc,
	arm_instr_multi_0x08970300__mi,
	arm_instr_multi_0x08970300__pl,
	arm_instr_multi_0x08970300__vs,
	arm_instr_multi_0x08970300__vc,
	arm_instr_multi_0x08970300__hi,
	arm_instr_multi_0x08970300__ls,
	arm_instr_multi_0x08970300__ge,
	arm_instr_multi_0x08970300__lt,
	arm_instr_multi_0x08970300__gt,
	arm_instr_multi_0x08970300__le,
	arm_instr_multi_0x08970300,
	arm_instr_nop,
	arm_instr_multi_0x08970180__eq,
	arm_instr_multi_0x08970180__ne,
	arm_instr_multi_0x08970180__cs,
	arm_instr_multi_0x08970180__cc,
	arm_instr_multi_0x08970180__mi,
	arm_instr_multi_0x08970180__pl,
	arm_instr_multi_0x08970180__vs,
	arm_instr_multi_0x08970180__vc,
	arm_instr_multi_0x08970180__hi,
	arm_instr_multi_0x08970180__ls,
	arm_instr_multi_0x08970180__ge,
	arm_instr_multi_0x08970180__lt,
	arm_instr_multi_0x08970180__gt,
	arm_instr_multi_0x08970180__le,
	arm_instr_multi_0x08970180,
	arm_instr_nop,
};
void (*multi_opcode_f_254[80])(struct cpu *, struct arm_instr_call *) = {
	arm_instr_multi_0x08bd81f0__eq,
	arm_instr_multi_0x08bd81f0__ne,
	arm_instr_multi_0x08bd81f0__cs,
	arm_instr_multi_0x08bd81f0__cc,
	arm_instr_multi_0x08bd81f0__mi,
	arm_instr_multi_0x08bd81f0__pl,
	arm_instr_multi_0x08bd81f0__vs,
	arm_instr_multi_0x08bd81f0__vc,
	arm_instr_multi_0x08bd81f0__hi,
	arm_instr_multi_0x08bd81f0__ls,
	arm_instr_multi_0x08bd81f0__ge,
	arm_instr_multi_0x08bd81f0__lt,
	arm_instr_multi_0x08bd81f0__gt,
	arm_instr_multi_0x08bd81f0__le,
	arm_instr_multi_0x08bd81f0,
	arm_instr_nop,
	arm_instr_multi_0x08bd0ff0__eq,
	arm_instr_multi_0x08bd0ff0__ne,
	arm_instr_multi_0x08bd0ff0__cs,
	arm_instr_multi_0x08bd0ff0__cc,
	arm_instr_multi_0x08bd0ff0__mi,
	arm_instr_multi_0x08bd0ff0__pl,
	arm_instr_multi_0x08bd0ff0__vs,
	arm_instr_multi_0x08bd0ff0__vc,
	arm_instr_multi_0x08bd0ff0__hi,
	arm_instr_multi_0x08bd0ff0__ls,
	arm_instr_multi_0x08bd0ff0__ge,
	arm_instr_multi_0x08bd0ff0__lt,
	arm_instr_multi_0x08bd0ff0__gt,
	arm_instr_multi_0x08bd0ff0__le,
	arm_instr_multi_0x08bd0ff0,
	arm_instr_nop,
	arm_instr_multi_0x08bd87f0__eq,
	arm_instr_multi_0x08bd87f0__ne,
	arm_instr_multi_0x08bd87f0__cs,
	arm_instr_multi_0x08bd87f0__cc,
	arm_instr_multi_0x08bd87f0__mi,
	arm_instr_multi_0x08bd87f0__pl,
	arm_instr_multi_0x08bd87f0__vs,
	arm_instr_multi_0x08bd87f0__vc,
	arm_instr_multi_0x08bd87f0__hi,
	arm_instr_multi_0x08bd87f0__ls,
	arm_instr_multi_0x08bd87f0__ge,
	arm_instr_multi_0x08bd87f0__lt,
	arm_instr_multi_0x08bd87f0__gt,
	arm_instr_multi_0x08bd87f0__le,
	arm_instr_multi_0x08bd87f0,
	arm_instr_nop,
	arm_instr_multi_0x08bd85f0__eq,
	arm_instr_multi_0x08bd85f0__ne,
	arm_instr_multi_0x08bd85f0__cs,
	arm_instr_multi_0x08bd85f0__cc,
	arm_instr_multi_0x08bd85f0__mi,
	arm_instr_multi_0x08bd85f0__pl,
	arm_instr_multi_0x08bd85f0__vs,
	arm_instr_multi_0x08bd85f0__vc,
	arm_instr_multi_0x08bd85f0__hi,
	arm_instr_multi_0x08bd85f0__ls,
	arm_instr_multi_0x08bd85f0__ge,
	arm_instr_multi_0x08bd85f0__lt,
	arm_instr_multi_0x08bd85f0__gt,
	arm_instr_multi_0x08bd85f0__le,
	arm_instr_multi_0x08bd85f0,
	arm_instr_nop,
	arm_instr_multi_0x08bd41f0__eq,
	arm_instr_multi_0x08bd41f0__ne,
	arm_instr_multi_0x08bd41f0__cs,
	arm_instr_multi_0x08bd41f0__cc,
	arm_instr_multi_0x08bd41f0__mi,
	arm_instr_multi_0x08bd41f0__pl,
	arm_instr_multi_0x08bd41f0__vs,
	arm_instr_multi_0x08bd41f0__vc,
	arm_instr_multi_0x08bd41f0__hi,
	arm_instr_multi_0x08bd41f0__ls,
	arm_instr_multi_0x08bd41f0__ge,
	arm_instr_multi_0x08bd41f0__lt,
	arm_instr_multi_0x08bd41f0__gt,
	arm_instr_multi_0x08bd41f0__le,
	arm_instr_multi_0x08bd41f0,
	arm_instr_nop,
};

uint32_t *multi_opcode[256] = {
 multi_opcode_0,
 multi_opcode_1, multi_opcode_2, multi_opcode_3, multi_opcode_4,
 multi_opcode_5, multi_opcode_6, multi_opcode_7, multi_opcode_8,
 multi_opcode_9, multi_opcode_10, multi_opcode_11, multi_opcode_12,
 multi_opcode_13, multi_opcode_14, multi_opcode_15, multi_opcode_16,
 multi_opcode_17, multi_opcode_18, multi_opcode_19, multi_opcode_20,
 multi_opcode_21, multi_opcode_22, multi_opcode_23, multi_opcode_24,
 multi_opcode_25, multi_opcode_26, multi_opcode_27, multi_opcode_28,
 multi_opcode_29, multi_opcode_30, multi_opcode_31, multi_opcode_32,
 multi_opcode_33, multi_opcode_34, multi_opcode_35, multi_opcode_36,
 multi_opcode_37, multi_opcode_38, multi_opcode_39, multi_opcode_40,
 multi_opcode_41, multi_opcode_42, multi_opcode_43, multi_opcode_44,
 multi_opcode_45, multi_opcode_46, multi_opcode_47, multi_opcode_48,
 multi_opcode_49, multi_opcode_50, multi_opcode_51, multi_opcode_52,
 multi_opcode_53, multi_opcode_54, multi_opcode_55, multi_opcode_56,
 multi_opcode_57, multi_opcode_58, multi_opcode_59, multi_opcode_60,
 multi_opcode_61, multi_opcode_62, multi_opcode_63, multi_opcode_64,
 multi_opcode_65, multi_opcode_66, multi_opcode_67, multi_opcode_68,
 multi_opcode_69, multi_opcode_70, multi_opcode_71, multi_opcode_72,
 multi_opcode_73, multi_opcode_74, multi_opcode_75, multi_opcode_76,
 multi_opcode_77, multi_opcode_78, multi_opcode_79, multi_opcode_80,
 multi_opcode_81, multi_opcode_82, multi_opcode_83, multi_opcode_84,
 multi_opcode_85, multi_opcode_86, multi_opcode_87, multi_opcode_88,
 multi_opcode_89, multi_opcode_90, multi_opcode_91, multi_opcode_92,
 multi_opcode_93, multi_opcode_94, multi_opcode_95, multi_opcode_96,
 multi_opcode_97, multi_opcode_98, multi_opcode_99, multi_opcode_100,
 multi_opcode_101, multi_opcode_102, multi_opcode_103, multi_opcode_104,
 multi_opcode_105, multi_opcode_106, multi_opcode_107, multi_opcode_108,
 multi_opcode_109, multi_opcode_110, multi_opcode_111, multi_opcode_112,
 multi_opcode_113, multi_opcode_114, multi_opcode_115, multi_opcode_116,
 multi_opcode_117, multi_opcode_118, multi_opcode_119, multi_opcode_120,
 multi_opcode_121, multi_opcode_122, multi_opcode_123, multi_opcode_124,
 multi_opcode_125, multi_opcode_126, multi_opcode_127, multi_opcode_128,
 multi_opcode_129, multi_opcode_130, multi_opcode_131, multi_opcode_132,
 multi_opcode_133, multi_opcode_134, multi_opcode_135, multi_opcode_136,
 multi_opcode_137, multi_opcode_138, multi_opcode_139, multi_opcode_140,
 multi_opcode_141, multi_opcode_142, multi_opcode_143, multi_opcode_144,
 multi_opcode_145, multi_opcode_146, multi_opcode_147, multi_opcode_148,
 multi_opcode_149, multi_opcode_150, multi_opcode_151, multi_opcode_152,
 multi_opcode_153, multi_opcode_154, multi_opcode_155, multi_opcode_156,
 multi_opcode_157, multi_opcode_158, multi_opcode_159, multi_opcode_160,
 multi_opcode_161, multi_opcode_162, multi_opcode_163, multi_opcode_164,
 multi_opcode_165, multi_opcode_166, multi_opcode_167, multi_opcode_168,
 multi_opcode_169, multi_opcode_170, multi_opcode_171, multi_opcode_172,
 multi_opcode_173, multi_opcode_174, multi_opcode_175, multi_opcode_176,
 multi_opcode_177, multi_opcode_178, multi_opcode_179, multi_opcode_180,
 multi_opcode_181, multi_opcode_182, multi_opcode_183, multi_opcode_184,
 multi_opcode_185, multi_opcode_186, multi_opcode_187, multi_opcode_188,
 multi_opcode_189, multi_opcode_190, multi_opcode_191, multi_opcode_192,
 multi_opcode_193, multi_opcode_194, multi_opcode_195, multi_opcode_196,
 multi_opcode_197, multi_opcode_198, multi_opcode_199, multi_opcode_200,
 multi_opcode_201, multi_opcode_202, multi_opcode_203, multi_opcode_204,
 multi_opcode_205, multi_opcode_206, multi_opcode_207, multi_opcode_208,
 multi_opcode_209, multi_opcode_210, multi_opcode_211, multi_opcode_212,
 multi_opcode_213, multi_opcode_214, multi_opcode_215, multi_opcode_216,
 multi_opcode_217, multi_opcode_218, multi_opcode_219, multi_opcode_220,
 multi_opcode_221, multi_opcode_222, multi_opcode_223, multi_opcode_224,
 multi_opcode_225, multi_opcode_226, multi_opcode_227, multi_opcode_228,
 multi_opcode_229, multi_opcode_230, multi_opcode_231, multi_opcode_232,
 multi_opcode_233, multi_opcode_234, multi_opcode_235, multi_opcode_236,
 multi_opcode_237, multi_opcode_238, multi_opcode_239, multi_opcode_240,
 multi_opcode_241, multi_opcode_242, multi_opcode_243, multi_opcode_244,
 multi_opcode_245, multi_opcode_246, multi_opcode_247, multi_opcode_248,
 multi_opcode_249, multi_opcode_250, multi_opcode_251, multi_opcode_252,
 multi_opcode_253, multi_opcode_254, multi_opcode_255,};

void (**multi_opcode_f[256])(struct cpu *, struct arm_instr_call *) = {
 multi_opcode_f_0,
 NULL, multi_opcode_f_2, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_8,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, multi_opcode_f_18, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_32,
 multi_opcode_f_33, multi_opcode_f_34, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_48,
 multi_opcode_f_49, multi_opcode_f_50, multi_opcode_f_51, NULL,
 NULL, multi_opcode_f_54, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, multi_opcode_f_62, NULL, multi_opcode_f_64,
 multi_opcode_f_65, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_80,
 multi_opcode_f_81, multi_opcode_f_82, NULL, NULL,
 NULL, multi_opcode_f_86, NULL, multi_opcode_f_88,
 NULL, NULL, NULL, NULL,
 NULL, multi_opcode_f_94, NULL, NULL,
 multi_opcode_f_97, multi_opcode_f_98, NULL, multi_opcode_f_100,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_112,
 multi_opcode_f_113, multi_opcode_f_114, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_128,
 multi_opcode_f_129, multi_opcode_f_130, NULL, multi_opcode_f_132,
 NULL, NULL, NULL, multi_opcode_f_136,
 NULL, NULL, NULL, NULL,
 NULL, multi_opcode_f_142, NULL, multi_opcode_f_144,
 multi_opcode_f_145, multi_opcode_f_146, NULL, multi_opcode_f_148,
 NULL, NULL, NULL, multi_opcode_f_152,
 NULL, NULL, NULL, NULL,
 NULL, multi_opcode_f_158, NULL, multi_opcode_f_160,
 multi_opcode_f_161, multi_opcode_f_162, NULL, multi_opcode_f_164,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_176,
 multi_opcode_f_177, multi_opcode_f_178, multi_opcode_f_179, NULL,
 NULL, NULL, NULL, multi_opcode_f_184,
 NULL, NULL, NULL, NULL,
 NULL, NULL, multi_opcode_f_191, multi_opcode_f_192,
 multi_opcode_f_193, multi_opcode_f_194, NULL, multi_opcode_f_196,
 NULL, NULL, NULL, multi_opcode_f_200,
 NULL, NULL, NULL, multi_opcode_f_204,
 NULL, multi_opcode_f_206, NULL, multi_opcode_f_208,
 multi_opcode_f_209, multi_opcode_f_210, NULL, multi_opcode_f_212,
 NULL, NULL, NULL, multi_opcode_f_216,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_224,
 multi_opcode_f_225, multi_opcode_f_226, NULL, multi_opcode_f_228,
 NULL, NULL, NULL, multi_opcode_f_232,
 NULL, NULL, NULL, NULL,
 NULL, NULL, NULL, multi_opcode_f_240,
 multi_opcode_f_241, multi_opcode_f_242, multi_opcode_f_243, multi_opcode_f_244,
 NULL, multi_opcode_f_246, NULL, multi_opcode_f_248,
 NULL, NULL, NULL, NULL,
 NULL, multi_opcode_f_254, NULL,};
