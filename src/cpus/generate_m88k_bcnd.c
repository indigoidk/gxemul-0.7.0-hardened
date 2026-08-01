/*
 *  Copyright (C) 2007-2021  Anders Gavare.  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 *  SUCH DAMAGE.
 */

#include <stdio.h>
#include <string.h>


void print_function_name(int samepage, int n_bit, int m5)
{
	printf("bcnd_");

	if (n_bit)
		printf("n_");

	if (samepage)
		printf("samepage_");

	switch (m5) {
	case 0x1: printf("gt0"); break;
	case 0x2: printf("eq0"); break;
	case 0x3: printf("ge0"); break;
	case 0x5: printf("not_maxneg_nor_zero"); break;
	case 0x7: printf("not_maxneg"); break;
	case 0x8: printf("maxneg"); break;
	case 0xc: printf("lt0"); break;
	case 0xd: printf("ne0"); break;
	case 0xe: printf("le0"); break;

	/*
	 *  #323: every other mask value. These are legal encodings that the
	 *  assembler has no mnemonic for, and until now they had no handler
	 *  either -- the table entry stayed NULL and the decoder answered
	 *  `goto bad`, which stops the emulator.
	 */
	default:  printf("m%02x", m5); break;
	}
}


/*
 *  #323: the condition as the manual states it -- a MASK over four mutually
 *  exclusive classes of the source register, not a list of named comparisons:
 *
 *	bit 0	> 0
 *	bit 1	== 0
 *	bit 2	< 0, excluding the most negative value
 *	bit 3	== 0x80000000 (the most negative value, its own class)
 *
 *  Bit 4 is reserved and matches no class, so it simply never contributes.
 *  This is the same reading `tcnd` was given in #307, and it reproduces all
 *  nine of the previously-named cases exactly: 0x3 is gt0|eq0 = ">= 0", 0xc is
 *  maxneg|lt0 = "< 0", 0xd is those plus gt0 = "!= 0", and so on. Writing it
 *  once replaces the enumeration rather than sitting beside it.
 */
void print_condition(int m5)
{
	const char *sep = "";

	printf("(");

	if (m5 & 1) {
		printf("%s(int32_t)reg(ic->arg[0]) > 0", sep);
		sep = " || ";
	}
	if (m5 & 2) {
		printf("%sreg(ic->arg[0]) == 0", sep);
		sep = " || ";
	}
	if (m5 & 4) {
		printf("%s((int32_t)reg(ic->arg[0]) < 0 &&\n\t    "
		    "(uint32_t)reg(ic->arg[0]) != 0x80000000UL)", sep);
		sep = " || ";
	}
	if (m5 & 8) {
		printf("%s(uint32_t)reg(ic->arg[0]) == 0x80000000UL", sep);
		sep = " || ";
	}

	/*  A mask selecting no class at all never branches.  */
	if (sep[0] == '\0')
		printf("0");

	printf(")");
}


/*
 *  #323: print_operator() lived here. It enumerated a comparison per named
 *  mask and is gone rather than left beside its replacement -- the nine cases
 *  it covered are exactly what print_condition() derives from the mask, and
 *  keeping both would leave two answers to the same question.
 */


void bcnd(int samepage, int n_bit, int m5)
{
	if (samepage && n_bit)
		return;

	printf("\nX(");
	print_function_name(samepage, n_bit, m5);
	printf(")\n{\n");

	/*  Easiest case is without the n_bit:  */
	if (!n_bit) {
		printf("\tif ");
		print_condition(m5);
		printf(" {\n");

		if (samepage)
			printf("\t\tcpu->cd.m88k.next_ic = (struct m88k_"
			    "instr_call *) ic->arg[2];\n");
		else
			printf("\t\tcpu->pc = (cpu->pc & 0xfffff000) + "
			    "(int32_t)ic->arg[2];\n\t\tquick_pc_to_"
			    "pointers(cpu);\n");

		printf("\t}\n");
	} else {
		/*  n_bit, i.e. delay slot:  */
		printf("\tint cond = ");
		print_condition(m5);
		printf(";\n");

		printf("\tSYNCH_PC;\n");

		printf("\tif (cond)\n");
		printf("\t\tcpu->cd.m88k.delay_target = (cpu->pc\n");
		printf("\t\t\t& ~((M88K_IC_ENTRIES_PER_PAGE-1)"
		    " << M88K_INSTR_ALIGNMENT_SHIFT))\n");
		printf("\t\t\t+ ic->arg[2];\n");
		printf("\telse\n");
		printf("\t\tcpu->cd.m88k.delay_target = cpu->pc + 8;\n");

		printf("\tcpu->delay_slot = TO_BE_DELAYED;\n");
		printf("\tic[1].f(cpu, ic+1);\n");
		printf("\tcpu->n_translated_instrs ++;\n");

		printf("\tif (!(cpu->delay_slot & EXCEPTION_IN_"
		    "DELAY_SLOT)) {\n");
		printf("\t\tcpu->delay_slot = NOT_DELAYED;\n");
		printf("\t\tif (cond) {\n");

		printf("\t\t\tcpu->pc = cpu->cd.m88k.delay_target;\n");
		printf("\t\t\tquick_pc_to_pointers(cpu);\n");

		printf("\t\t} else\n");
		printf("\t\t\tcpu->cd.m88k.next_ic ++;\n");
		printf("\t} else\n");
		printf("\t\tcpu->delay_slot = NOT_DELAYED;\n");

	}

	printf("}\n\n");
}


int main(int argc, char *argv[])
{
	int samepage, n_bit, m5;

	printf("\n/*  AUTOMATICALLY GENERATED! Do not edit.  */\n\n");

	for (samepage=0; samepage<=1; samepage++)
		for (n_bit=0; n_bit<=1; n_bit++)
			for (m5=0; m5<=31; m5++) {
				/*  #323: every mask, not just the nine the
				    assembler has names for.  */
				bcnd(samepage, n_bit, m5);
			}

	/*  Array of pointers to all the functions:  */
	printf("\n\nvoid (*m88k_bcnd[32 * 2 * 2])(struct cpu *, struct "
	    "m88k_instr_call *) = {\n");
	for (samepage=0; samepage<=1; samepage++)
		for (n_bit=0; n_bit<=1; n_bit++)
			for (m5=0; m5<=31; m5++) {
				if (m5 || n_bit || samepage)
					printf(",\n");

				/*
				 *  #323: a slot is NULL now only for the
				 *  samepage+delay-slot combination, which has
				 *  no handler by construction. Every mask
				 *  value has one; leaving twenty-three of them
				 *  NULL is what sent a legal encoding to
				 *  `goto bad` and stopped the emulator.
				 */
				if (samepage && n_bit)
					printf("NULL");
				else {
					printf("m88k_instr_");
					print_function_name(samepage,
					    n_bit, m5);
				}
			}
	printf(" };\n");

	return 0;
}

