
/*  AUTOMATICALLY GENERATED! Do not edit.  */


X(bcnd_m00)
{
	if (0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_gt0)
{
	if ((int32_t)reg(ic->arg[0]) > 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_eq0)
{
	if (reg(ic->arg[0]) == 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_ge0)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m04)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_not_maxneg_nor_zero)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m06)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_not_maxneg)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
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


X(bcnd_m09)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m0a)
{
	if (reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m0b)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_lt0)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_ne0)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_le0)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m0f)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m10)
{
	if (0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m11)
{
	if ((int32_t)reg(ic->arg[0]) > 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m12)
{
	if (reg(ic->arg[0]) == 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m13)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m14)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m15)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m16)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m17)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m18)
{
	if ((uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m19)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m1a)
{
	if (reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m1b)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m1c)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m1d)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m1e)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_m1f)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->pc = (cpu->pc & 0xfffff000) + (int32_t)ic->arg[2];
		quick_pc_to_pointers(cpu);
	}
}


X(bcnd_n_m00)
{
	int cond = (0);
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


X(bcnd_n_gt0)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0);
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
	int cond = (reg(ic->arg[0]) == 0);
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
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0);
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


X(bcnd_n_m04)
{
	int cond = (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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


X(bcnd_n_m06)
{
	int cond = (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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
	int cond = ((uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m09)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m0a)
{
	int cond = (reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m0b)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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
	int cond = (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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
	int cond = (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m0f)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m10)
{
	int cond = (0);
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


X(bcnd_n_m11)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0);
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


X(bcnd_n_m12)
{
	int cond = (reg(ic->arg[0]) == 0);
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


X(bcnd_n_m13)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0);
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


X(bcnd_n_m14)
{
	int cond = (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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


X(bcnd_n_m15)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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


X(bcnd_n_m16)
{
	int cond = (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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


X(bcnd_n_m17)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL));
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


X(bcnd_n_m18)
{
	int cond = ((uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m19)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m1a)
{
	int cond = (reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m1b)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m1c)
{
	int cond = (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m1d)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m1e)
{
	int cond = (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_n_m1f)
{
	int cond = ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL);
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


X(bcnd_samepage_m00)
{
	if (0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_gt0)
{
	if ((int32_t)reg(ic->arg[0]) > 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_eq0)
{
	if (reg(ic->arg[0]) == 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_ge0)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m04)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_not_maxneg_nor_zero)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m06)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_not_maxneg)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_maxneg)
{
	if ((uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m09)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m0a)
{
	if (reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m0b)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_lt0)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_ne0)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_le0)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m0f)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m10)
{
	if (0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m11)
{
	if ((int32_t)reg(ic->arg[0]) > 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m12)
{
	if (reg(ic->arg[0]) == 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m13)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m14)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m15)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m16)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m17)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL)) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m18)
{
	if ((uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m19)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m1a)
{
	if (reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m1b)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m1c)
{
	if (((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m1d)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m1e)
{
	if (reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}


X(bcnd_samepage_m1f)
{
	if ((int32_t)reg(ic->arg[0]) > 0 || reg(ic->arg[0]) == 0 || ((int32_t)reg(ic->arg[0]) < 0 &&
	    (uint32_t)reg(ic->arg[0]) != 0x80000000UL) || (uint32_t)reg(ic->arg[0]) == 0x80000000UL) {
		cpu->cd.m88k.next_ic = (struct m88k_instr_call *) ic->arg[2];
	}
}



void (*m88k_bcnd[32 * 2 * 2])(struct cpu *, struct m88k_instr_call *) = {
m88k_instr_bcnd_m00,
m88k_instr_bcnd_gt0,
m88k_instr_bcnd_eq0,
m88k_instr_bcnd_ge0,
m88k_instr_bcnd_m04,
m88k_instr_bcnd_not_maxneg_nor_zero,
m88k_instr_bcnd_m06,
m88k_instr_bcnd_not_maxneg,
m88k_instr_bcnd_maxneg,
m88k_instr_bcnd_m09,
m88k_instr_bcnd_m0a,
m88k_instr_bcnd_m0b,
m88k_instr_bcnd_lt0,
m88k_instr_bcnd_ne0,
m88k_instr_bcnd_le0,
m88k_instr_bcnd_m0f,
m88k_instr_bcnd_m10,
m88k_instr_bcnd_m11,
m88k_instr_bcnd_m12,
m88k_instr_bcnd_m13,
m88k_instr_bcnd_m14,
m88k_instr_bcnd_m15,
m88k_instr_bcnd_m16,
m88k_instr_bcnd_m17,
m88k_instr_bcnd_m18,
m88k_instr_bcnd_m19,
m88k_instr_bcnd_m1a,
m88k_instr_bcnd_m1b,
m88k_instr_bcnd_m1c,
m88k_instr_bcnd_m1d,
m88k_instr_bcnd_m1e,
m88k_instr_bcnd_m1f,
m88k_instr_bcnd_n_m00,
m88k_instr_bcnd_n_gt0,
m88k_instr_bcnd_n_eq0,
m88k_instr_bcnd_n_ge0,
m88k_instr_bcnd_n_m04,
m88k_instr_bcnd_n_not_maxneg_nor_zero,
m88k_instr_bcnd_n_m06,
m88k_instr_bcnd_n_not_maxneg,
m88k_instr_bcnd_n_maxneg,
m88k_instr_bcnd_n_m09,
m88k_instr_bcnd_n_m0a,
m88k_instr_bcnd_n_m0b,
m88k_instr_bcnd_n_lt0,
m88k_instr_bcnd_n_ne0,
m88k_instr_bcnd_n_le0,
m88k_instr_bcnd_n_m0f,
m88k_instr_bcnd_n_m10,
m88k_instr_bcnd_n_m11,
m88k_instr_bcnd_n_m12,
m88k_instr_bcnd_n_m13,
m88k_instr_bcnd_n_m14,
m88k_instr_bcnd_n_m15,
m88k_instr_bcnd_n_m16,
m88k_instr_bcnd_n_m17,
m88k_instr_bcnd_n_m18,
m88k_instr_bcnd_n_m19,
m88k_instr_bcnd_n_m1a,
m88k_instr_bcnd_n_m1b,
m88k_instr_bcnd_n_m1c,
m88k_instr_bcnd_n_m1d,
m88k_instr_bcnd_n_m1e,
m88k_instr_bcnd_n_m1f,
m88k_instr_bcnd_samepage_m00,
m88k_instr_bcnd_samepage_gt0,
m88k_instr_bcnd_samepage_eq0,
m88k_instr_bcnd_samepage_ge0,
m88k_instr_bcnd_samepage_m04,
m88k_instr_bcnd_samepage_not_maxneg_nor_zero,
m88k_instr_bcnd_samepage_m06,
m88k_instr_bcnd_samepage_not_maxneg,
m88k_instr_bcnd_samepage_maxneg,
m88k_instr_bcnd_samepage_m09,
m88k_instr_bcnd_samepage_m0a,
m88k_instr_bcnd_samepage_m0b,
m88k_instr_bcnd_samepage_lt0,
m88k_instr_bcnd_samepage_ne0,
m88k_instr_bcnd_samepage_le0,
m88k_instr_bcnd_samepage_m0f,
m88k_instr_bcnd_samepage_m10,
m88k_instr_bcnd_samepage_m11,
m88k_instr_bcnd_samepage_m12,
m88k_instr_bcnd_samepage_m13,
m88k_instr_bcnd_samepage_m14,
m88k_instr_bcnd_samepage_m15,
m88k_instr_bcnd_samepage_m16,
m88k_instr_bcnd_samepage_m17,
m88k_instr_bcnd_samepage_m18,
m88k_instr_bcnd_samepage_m19,
m88k_instr_bcnd_samepage_m1a,
m88k_instr_bcnd_samepage_m1b,
m88k_instr_bcnd_samepage_m1c,
m88k_instr_bcnd_samepage_m1d,
m88k_instr_bcnd_samepage_m1e,
m88k_instr_bcnd_samepage_m1f,
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
