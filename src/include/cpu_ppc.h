#ifndef	CPU_PPC_H
#define	CPU_PPC_H

/*
 *  Copyright (C) 2005-2021  Anders Gavare.  All rights reserved.
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
 *
 *
 *  POWER and PowerPC CPU definitions.
 */

#include "misc.h"


struct cpu_family;

#define	MODE_PPC		0
#define	MODE_POWER		1

/*  PPC CPU types:  */
struct ppc_cpu_type_def { 
	const char	*name;
	int		pvr;
	int		bits;
	int		flags;
	int		icache_shift;
	int		ilinesize;
	int		iway;
	int		dcache_shift;
	int		dlinesize;
	int		dway;
	int		l2cache_shift;
	int		l2linesize;
	int		l2way;
	int		altivec;

	/*  TODO: POWER vs PowerPC?  */
};

/*  Flags:  */
#define	PPC_NOFP		1
#define	PPC_601			2
#define	PPC_603			4
#define	PPC_NO_DEC		8	/*  No DEC (decrementer) SPR  */
/*  #174: (Codex/Fable) capability flag for the extended BATs 4-7 of the
    MPC7445/7455; see ppc_bat() in memory_ppc.c.  */
#define	PPC_HIGH_BAT		16

/*
 *  TODO: Most of these just bogus
 */

#define PPC_CPU_TYPE_DEFS	{					\
	{ "PPC405GP",	0x40110000, 32, PPC_NOFP|PPC_NO_DEC,		\
					13,5,2, 13,5,2, 0,5,1, 0 },	\
	{ "PPC601",	0,          32, PPC_601, 14,5,4, 14,5,4, 0,0,0, 0 },\
	{ "PPC603",	0x00030302, 32, PPC_603, 14,5,4, 14,5,4, 0,0,0, 0 },\
	{ "PPC603e",	0x00060104, 32, PPC_603, 14,5,4, 14,5,4, 0,0,0, 0 },\
	{ "PPC604",	0x00040304, 32, 0, 15,5,4, 15,5,4, 0,0,0, 0 },	\
	{ "PPC620",	0x00140000, 64, 0, 15,5,4, 15,5,4, 0,0,0, 0 },	\
	{ "MPC7400",	0x000c0000, 32, 0, 15,5,2, 15,5,2, 19,5,1, 1 },	\
	{ "MPC7455",	0x80010000, 32, PPC_HIGH_BAT, 15,5,8, 15,5,8, 18,5,8, 1 },	\
	{ "PPC750",	0x00084202, 32, 0, 15,5,2, 15,5,2, 20,5,1, 0 },	\
	{ "G4e",	0,          32, 0, 15,5,8, 15,5,8, 18,5,8, 1 },	\
	{ "PPC970",	0x00390000, 64, 0, 16,7,1, 15,7,2, 19,7,1, 1 },	\
	{ NULL,		0,          0,0,0,0,0,0,0,0,0,0,0,0 }		\
	}

#define	PPC_NGPRS		32
#define	PPC_NFPRS		32
#define	PPC_NVRS		32
#define	PPC_N_TGPRS		4

#define	PPC_N_IC_ARGS			3
#define	PPC_INSTR_ALIGNMENT_SHIFT	2
#define	PPC_IC_ENTRIES_SHIFT		10
#define	PPC_IC_ENTRIES_PER_PAGE		(1 << PPC_IC_ENTRIES_SHIFT)
#define	PPC_PC_TO_IC_ENTRY(a)		(((a)>>PPC_INSTR_ALIGNMENT_SHIFT) \
					& (PPC_IC_ENTRIES_PER_PAGE-1))
#define	PPC_ADDR_TO_PAGENR(a)		((a) >> (PPC_IC_ENTRIES_SHIFT \
					+ PPC_INSTR_ALIGNMENT_SHIFT))

#define	PPC_L2N			17
#define	PPC_L3N			18

DYNTRANS_MISC_DECLARATIONS(ppc,PPC,uint64_t)
DYNTRANS_MISC64_DECLARATIONS(ppc,PPC,uint8_t)

#define	PPC_MAX_VPH_TLB_ENTRIES		128


struct ppc_cpu {
	struct ppc_cpu_type_def cpu_type;

	uint64_t	of_emul_addr;

	int		mode;		/*  MODE_PPC or MODE_POWER  */
	int		bits;		/*  32 or 64  */

	int		irq_asserted;	/*  External Interrupt flag  */
	int		dec_intr_pending;/* Decrementer interrupt pending  */
	uint64_t	zero;		/*  A zero register  */

	uint32_t	cr;		/*  Condition Register  */
	uint32_t	fpscr;		/*  FP Status and Control Register  */
	uint64_t	gpr[PPC_NGPRS];	/*  General Purpose Registers  */
	uint64_t	fpr[PPC_NFPRS];	/*  Floating-Point Registers  */

	uint64_t	vr_hi[PPC_NVRS];/*  128-bit Vector registers  */
	uint64_t	vr_lo[PPC_NVRS];/*  (Hi and lo 64-bit parts)  */

	uint64_t	msr;		/*  Machine state register  */
	uint64_t	tgpr[PPC_N_TGPRS];/*Temporary gpr 0..3  */

	uint32_t	sr[16];		/*  Segment registers.  */
	uint64_t	spr[1024];

	uint64_t	ll_addr;	/*  Load-linked / store-conditional  */
	int		ll_bit;


	/*
	 *  Instruction translation cache and Virtual->Physical->Host
	 *  address translation:
	 */
	DYNTRANS_ITC(ppc)
	VPH_TLBS(ppc,PPC)
	VPH32(ppc,PPC)
	VPH64(ppc,PPC)
};


/*  Machine status word bits: (according to Book 3)  */
#define	PPC_MSR_SF	(1ULL << 63)	/*  Sixty-Four-Bit Mode  */
/*  bits 62..61 are reserved  */
#define	PPC_MSR_HV	(1ULL << 60)	/*  Hypervisor  */
/*  bits 59..17  are reserved  */
#define	PPC_MSR_VEC	(1 << 25)	/*  Altivec Enable  */
#define	PPC_MSR_TGPR	(1 << 17)	/*  Temporary gpr0..3  */
#define	PPC_MSR_ILE	(1 << 16)	/*  Interrupt Little-Endian Mode  */
#define	PPC_MSR_EE	(1 << 15)	/*  External Interrupt Enable  */
#define	PPC_MSR_PR	(1 << 14)	/*  Problem/Privilege State  */
#define	PPC_MSR_FP	(1 << 13)	/*  Floating-Point Available  */
#define	PPC_MSR_ME	(1 << 12)	/*  Machine Check Interrupt Enable  */
#define	PPC_MSR_FE0	(1 << 11)	/*  Floating-Point Exception Mode 0  */
#define	PPC_MSR_SE	(1 << 10)	/*  Single-Step Trace Enable  */
#define	PPC_MSR_BE	(1 << 9)	/*  Branch Trace Enable  */
#define	PPC_MSR_FE1	(1 << 8)	/*  Floating-Point Exception Mode 1  */
#define	PPC_MSR_IP	(1 << 6)	/*  Vector Table at 0xfff00000  */
#define	PPC_MSR_IR	(1 << 5)	/*  Instruction Relocate  */
#define	PPC_MSR_DR	(1 << 4)	/*  Data Relocate  */
#define	PPC_MSR_PMM	(1 << 2)	/*  Performance Monitor Mark  */
#define	PPC_MSR_RI	(1 << 1)	/*  Recoverable Interrupt  */
#define	PPC_MSR_LE	(1)		/*  Little-Endian Mode  */

/*  Floating-point Status:  */
#define	PPC_FPSCR_FX	(1U << 31)	/*  Exception summary  */
#define	PPC_FPSCR_FEX	(1 << 30)	/*  Enabled Exception summary  */
#define	PPC_FPSCR_VX	(1 << 29)	/*  Invalid Operation summary  */
/*
 *  #327: the rest of the FPSCR, from Book I's bit table. ISA numbering is
 *  big-endian (bit 0 is the MSB), so a bit at ISA position n lives at host
 *  position 31-n -- which is why FX, the ISA's bit 0, is (1U << 31) above (unsigned:
 *  1 << 31 is undefined for a signed int).
 *
 *  ISA bit 20 is RESERVED, between VXVC and VXSOFT. It is deliberately absent
 *  here: the nine Invalid Operation causes are ISA 7:12 and 21:23, and a
 *  contiguous-looking mask over 7:12+20:23 would fold that reserved bit into
 *  the VX summary.
 */
#define	PPC_FPSCR_OX	(1 << 28)	/*  Overflow  */
#define	PPC_FPSCR_UX	(1 << 27)	/*  Underflow  */
#define	PPC_FPSCR_ZX	(1 << 26)	/*  Zero divide  */
#define	PPC_FPSCR_XX	(1 << 25)	/*  Inexact  */
#define	PPC_FPSCR_VXNAN	(1 << 24)	/*  Invalid: SNaN  */
#define	PPC_FPSCR_VXISI	(1 << 23)	/*  Invalid: Inf - Inf  */
#define	PPC_FPSCR_VXIDI	(1 << 22)	/*  Invalid: Inf / Inf  */
#define	PPC_FPSCR_VXZDZ	(1 << 21)	/*  Invalid: 0 / 0  */
#define	PPC_FPSCR_VXIMZ	(1 << 20)	/*  Invalid: Inf * 0  */
#define	PPC_FPSCR_VXVC	(1 << 19)	/*  Invalid: compare  */
#define	PPC_FPSCR_FR	(1 << 18)	/*  Fraction Rounded  */
#define	PPC_FPSCR_FI	(1 << 17)	/*  Fraction Inexact  */
#define	PPC_FPSCR_VXSOFT (1 << 10)	/*  Invalid: software request  */
#define	PPC_FPSCR_VXSQRT (1 << 9)	/*  Invalid: square root  */
#define	PPC_FPSCR_VXCVI	(1 << 8)	/*  Invalid: integer convert  */
#define	PPC_FPSCR_VE	(1 << 7)	/*  Invalid enable  */
#define	PPC_FPSCR_OE	(1 << 6)	/*  Overflow enable  */
#define	PPC_FPSCR_UE	(1 << 5)	/*  Underflow enable  */
#define	PPC_FPSCR_ZE	(1 << 4)	/*  Zero divide enable  */
#define	PPC_FPSCR_XE	(1 << 3)	/*  Inexact enable  */
#define	PPC_FPSCR_NI	(1 << 2)	/*  Non-IEEE mode  */

/*
 *  The nine Invalid Operation causes. VX is defined by Book I as the OR of
 *  exactly these -- it is derived, not stored, and no instruction may write
 *  it directly.
 */
#define	PPC_FPSCR_VX_CAUSES	(PPC_FPSCR_VXNAN | PPC_FPSCR_VXISI | \
				 PPC_FPSCR_VXIDI | PPC_FPSCR_VXZDZ | \
				 PPC_FPSCR_VXIMZ | PPC_FPSCR_VXVC | \
				 PPC_FPSCR_VXSOFT | PPC_FPSCR_VXSQRT | \
				 PPC_FPSCR_VXCVI)
#define	PPC_FPSCR_FPCC	0x0000f000
#define	PPC_FPSCR_FPCC_SHIFT	12
#define	PPC_FPSCR_FL	(1 << 15)	/*  Less than  */
#define	PPC_FPSCR_FG	(1 << 14)	/*  Greater than  */
#define	PPC_FPSCR_FE	(1 << 13)	/*  Equal or Zero  */
#define	PPC_FPSCR_FU	(1 << 12)	/*  Unordered or NaN  */
/*  #304: the rounding-control field, FPSCR[30:31] in IBM numbering -- the two
    LOWEST bits of the register.  The encoding (0 nearest, 1 toward zero,
    2 toward +Inf, 3 toward -Inf) is numerically identical to this project's
    IEEE_RM_* values, so `fpscr & PPC_FPSCR_RN_MASK` may be passed straight to
    float_emul's mode-aware entry points.  The register was guest-writable and
    decoded NOWHERE before #304: `frsp` narrowed with a host cast, which always
    rounds to nearest, so three of the four architected modes were unreachable.  */
#define	PPC_FPSCR_RN_MASK	0x3

/*  Exceptions:  */
#define	PPC_EXCEPTION_DSI	0x3	/*  Data Storage Interrupt  */
#define	PPC_EXCEPTION_ISI	0x4	/*  Instruction Storage Interrupt  */
#define	PPC_EXCEPTION_EI	0x5	/*  External interrupt  */
#define	PPC_EXCEPTION_FPU	0x8	/*  Floating-Point unavailable  */
#define	PPC_EXCEPTION_DEC	0x9	/*  Decrementer  */
#define	PPC_EXCEPTION_SC	0xc	/*  Syscall  */

/*  XER bits:  */
#define	PPC_XER_SO	(1UL << 31)	/*  Summary Overflow  */
#define	PPC_XER_OV	(1 << 30)	/*  Overflow  */
#define	PPC_XER_CA	(1 << 29)	/*  Carry  */


/*  cpu_ppc.c:  */
int ppc_run_instr(struct cpu *cpu);
int ppc32_run_instr(struct cpu *cpu);
void ppc_exception(struct cpu *cpu, int exception_nr);
void ppc_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
	unsigned char *host_page, int writeflag, uint64_t paddr_page);
void ppc32_update_translation_table(struct cpu *cpu, uint64_t vaddr_page,
	unsigned char *host_page, int writeflag, uint64_t paddr_page);
void ppc_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void ppc32_invalidate_translation_caches(struct cpu *cpu, uint64_t, int);
void ppc_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
void ppc32_invalidate_code_translation(struct cpu *cpu, uint64_t, int);
void ppc_init_64bit_dummy_tables(struct cpu *cpu);
int ppc_memory_rw(struct cpu *cpu, struct memory *mem, uint64_t vaddr,
	unsigned char *data, size_t len, int writeflag, int cache_flags);
void ppc_cpu_family_init(struct cpu_family *);

/*  memory_ppc.c:  */
int ppc_translate_v2p(struct cpu *cpu, uint64_t vaddr,
	uint64_t *return_addr, int flags);

#endif	/*  CPU_PPC_H  */
