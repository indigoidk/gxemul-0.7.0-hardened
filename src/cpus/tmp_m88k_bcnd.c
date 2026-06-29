
/*  AUTOMATICALLY GENERATED! Do not edit.  */


X(bcnd_gt0)
{
	if ((int32_t)reg(ic->arg[0]) > 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_eq0)
{
	if ((int32_t)reg(ic->arg[0]) == 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_ge0)
{
	if ((int32_t)reg(ic->arg[0]) >= 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_not_maxneg_nor_zero)
{
	if ((uint32_t)reg(ic->arg[0]) != 0x80000000UL && (int32_t)reg(ic->arg[0]) != 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_not_maxneg)
{
	if ((uint32_t)reg(ic->arg[0]) != 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_maxneg)
{
	if ((uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_lt0)
{
	if ((int32_t)reg(ic->arg[0]) < 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_ne0)
{
	if ((int32_t)reg(ic->arg[0]) != 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_le0)
{
	if ((int32_t)reg(ic->arg[0]) <= 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_n_gt0)
{
	int cond = (int32_t)reg(ic->arg[0]) > 0;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_eq0)
{
	int cond = (int32_t)reg(ic->arg[0]) == 0;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_ge0)
{
	int cond = (int32_t)reg(ic->arg[0]) >= 0;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_not_maxneg_nor_zero)
{
	int cond = (uint32_t)reg(ic->arg[0]) != 0x80000000UL && (int32_t)reg(ic->arg[0]) != 0;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_not_maxneg)
{
	int cond = (uint32_t)reg(ic->arg[0]) != 0x80000000UL;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_maxneg)
{
	int cond = (uint32_t)reg(ic->arg[0]) == 0x80000000UL;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_lt0)
{
	int cond = (int32_t)reg(ic->arg[0]) < 0;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_ne0)
{
	int cond = (int32_t)reg(ic->arg[0]) != 0;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_n_le0)
{
	int cond = (int32_t)reg(ic->arg[0]) <= 0;
	SYNCH_PC;
	if (cond)
		cpu->cd.m88k.delay_target = (cpu->pc
			& ~((M88K_IC_ENTRIES_PER_PAGE-1) << M88K_INSTR_ALIGNMENT_SHIFT))
			+ ic->arg[2];
	else
		cpu->cd.m88k.delay_target = cpu->pc + 8;
	cpu->delay_slot = TO_BE_DELAYED;
	ic[1].f(cpu, ic+1);
	cpu->n_translated_instrs ++;
	if (!(cpu->delay_slot & EXCEPTION_IN_DELAY_SLOT)) {
		cpu->delay_slot = NOT_DELAYED;
		if (cond) {
			cpu->pc = cpu->cd.m88k.delay_target;
			quick_pc_to_pointers(cpu);
		} else
			cpu->cd.m88k.next_ic ++;
	} else
		cpu->delay_slot = NOT_DELAYED;
}


X(bcnd_samepage_gt0)
{
	if ((int32_t)reg(ic->arg[0]) > 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_eq0)
{
	if ((int32_t)reg(ic->arg[0]) == 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_ge0)
{
	if ((int32_t)reg(ic->arg[0]) >= 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_not_maxneg_nor_zero)
{
	if ((uint32_t)reg(ic->arg[0]) != 0x80000000UL && (int32_t)reg(ic->arg[0]) != 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_not_maxneg)
{
	if ((uint32_t)reg(ic->arg[0]) != 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_maxneg)
{
	if ((uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_lt0)
{
	if ((int32_t)reg(ic->arg[0]) < 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_ne0)
{
	if ((int32_t)reg(ic->arg[0]) != 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_le0)
{
	if ((int32_t)reg(ic->arg[0]) <= 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}



void (*m88k_bcnd[32 * 2 * 2])(struct cpu *, struct m88k_instr_call *) = {
NULL,
m88k_instr_bcnd_gt0,
m88k_instr_bcnd_eq0,
m88k_instr_bcnd_ge0,
NULL,
m88k_instr_bcnd_not_maxneg_nor_zero,
NULL,
m88k_instr_bcnd_not_maxneg,
m88k_instr_bcnd_maxneg,
NULL,
NULL,
NULL,
m88k_instr_bcnd_lt0,
m88k_instr_bcnd_ne0,
m88k_instr_bcnd_le0,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
m88k_instr_bcnd_n_gt0,
m88k_instr_bcnd_n_eq0,
m88k_instr_bcnd_n_ge0,
NULL,
m88k_instr_bcnd_n_not_maxneg_nor_zero,
NULL,
m88k_instr_bcnd_n_not_maxneg,
m88k_instr_bcnd_n_maxneg,
NULL,
NULL,
NULL,
m88k_instr_bcnd_n_lt0,
m88k_instr_bcnd_n_ne0,
m88k_instr_bcnd_n_le0,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
m88k_instr_bcnd_samepage_gt0,
m88k_instr_bcnd_samepage_eq0,
m88k_instr_bcnd_samepage_ge0,
NULL,
m88k_instr_bcnd_samepage_not_maxneg_nor_zero,
NULL,
m88k_instr_bcnd_samepage_not_maxneg,
m88k_instr_bcnd_samepage_maxneg,
NULL,
NULL,
NULL,
m88k_instr_bcnd_samepage_lt0,
m88k_instr_bcnd_samepage_ne0,
m88k_instr_bcnd_samepage_le0,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL,
NULL };
