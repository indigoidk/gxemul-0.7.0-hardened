/*
 *  Copyright (C) 2006-2009  Anders Gavare.  All rights reserved.
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
#include <stdlib.h>
#include <string.h>

#include "cpu.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/sh4_exception.h"
#include "thirdparty/sh4_mmu.h"


/*
 *  translate_via_mmu():
 *
 *  Scan the UTLB for a matching virtual address. If a match was found, then
 *  check permission bits etc. If everything was ok, then return the physical
 *  page address, otherwise cause an exception.
 *
 *  The implementation should (hopefully) be quite complete, except for lack
 *  of "Multiple matching entries" detection. (On a real CPU, these would
 *  cause exceptions.)
 *
 *  Same return values as sh_translate_v2p().
 */
static int translate_via_mmu(struct cpu *cpu, uint32_t vaddr,
	uint64_t *return_paddr, int flags)
{
	int wf = flags & FLAG_WRITEFLAG;
	int i, urb, urc, require_asid_match, cur_asid, expevt = 0;
	uint32_t hi, lo = 0, mask = 0;
	int sh;		/*  Shared  */
	int d;		/*  Dirty bit  */
	int v;		/*  Valid bit  */
	int pr;		/*  Protection  */
	int i_start;

	cur_asid = cpu->cd.sh.pteh & SH4_PTEH_ASID_MASK;
	require_asid_match = !(cpu->cd.sh.mmucr & SH4_MMUCR_SV)
	    || !(cpu->cd.sh.sr & SH_SR_MD);

	if (!(flags & FLAG_NOEXCEPTIONS)) {
		/*
		 *  Increase URC every time the UTLB is accessed.
		 *
		 *  THE TODO THAT USED TO SIT HERE IS ANSWERED, 2026-08-22,
		 *  against a real SH7750 Hardware Manual (Rev.7.00,
		 *  REJ09B0366-0700) obtained by owner directive.  It asked
		 *  whether URC should be left alone by `ldtlb`, wondered
		 *  whether this was the right place, and floated setting it
		 *  to a random value instead.  The MMUCR field definition
		 *  settles all three:
		 *
		 *      "URC is incremented each time the UTLB is accessed.
		 *       When URB > 0, URC is reset to 0 when the condition
		 *       URC = URB occurs. ...  URC is not incremented by an
		 *       LDTLB instruction."
		 *
		 *  So the suspicion was RIGHT and the random-value idea was
		 *  WRONG -- and this code already conforms, by construction
		 *  rather than by intent: X(ldtlb) in cpu_sh_instr.c reads
		 *  URC out of MMUCR and indexes utlb_hi[]/utlb_lo[] itself,
		 *  never entering this translation path, so no increment can
		 *  happen there.  Nothing to change; the TODO simply never
		 *  knew.  The wrap below also matches the quoted text.
		 */
		urb = (cpu->cd.sh.mmucr & SH4_MMUCR_URB_MASK) >>
		    SH4_MMUCR_URB_SHIFT;
		urc = (cpu->cd.sh.mmucr & SH4_MMUCR_URC_MASK) >>
		    SH4_MMUCR_URC_SHIFT;

		/*  fatal("urc = %i  ==>  ", urc);  */
		urc ++;
		if (urc >= SH_N_UTLB_ENTRIES || (urb > 0 && urc == urb))
			urc = 0;
		/*  fatal("%i\n", urc);  */

		cpu->cd.sh.mmucr &= ~SH4_MMUCR_URC_MASK;
		cpu->cd.sh.mmucr |= (urc << SH4_MMUCR_URC_SHIFT);
	}

	/*
	 *  When doing Instruction lookups, the ITLB should be scanned first.
	 *  This is done by using negative i. (Ugly hack, but works.)
	 */
	if (flags & FLAG_INSTR)
		i_start = -SH_N_ITLB_ENTRIES;
	else
		i_start = 0;

	for (i=i_start; i<SH_N_UTLB_ENTRIES; i++) {
		if (i<0) {
			hi = cpu->cd.sh.itlb_hi[i + SH_N_ITLB_ENTRIES];
			lo = cpu->cd.sh.itlb_lo[i + SH_N_ITLB_ENTRIES];
		} else {
			hi = cpu->cd.sh.utlb_hi[i];
			lo = cpu->cd.sh.utlb_lo[i];
		}
		mask = 0xfff00000;

		v = lo & SH4_PTEL_V;
		if (!v)
			continue;

		switch (lo & SH4_PTEL_SZ_MASK) {
		case SH4_PTEL_SZ_1K:  mask = 0xfffffc00; break;
		case SH4_PTEL_SZ_4K:  mask = 0xfffff000; break;
		case SH4_PTEL_SZ_64K: mask = 0xffff0000; break;
		/*  case SH4_PTEL_SZ_1M:  mask = 0xfff00000; break;  */
		}

		if ((hi & mask) != (vaddr & mask))
			continue;

		sh = lo & SH4_PTEL_SH;

		if (!sh && require_asid_match) {
			int asid = hi & SH4_PTEH_ASID_MASK;
			if (asid != cur_asid)
				continue;
		}

		/*  Note/TODO: Check for multiple matches is not implemented. */

		break;
	}

	/*  Virtual address not found? Then it's a TLB miss.  */
	if (i == SH_N_UTLB_ENTRIES)
		goto tlb_miss;

	/*  Matching address found! Let's see whether it is
	    readable/writable, etc.:  */
	d = lo & SH4_PTEL_D? 1 : 0;
	pr = (lo & SH4_PTEL_PR_MASK) >> SH4_PTEL_PR_SHIFT;

	*return_paddr = (vaddr & ~mask) | (lo & mask & 0x1fffffff);

	if (flags & FLAG_INSTR) {
		/*
		 *  Instruction access:
		 */
#if 0
		/*  NOTE: Emulating the ITLB as exact as this is not
			necessary... so I'm disabling it for now.  */
		/*
		 *  If a matching entry wasn't found in the ITLB, but in the
		 *  UTLB, then copy it to a random place in the ITLB.
		 */
		if (i >= 0 && !(flags & FLAG_NOEXCEPTIONS)) {
			int r = random() % SH_N_ITLB_ENTRIES;

			/*  NOTE: Make sure that the old mapping for
			    that itlb entry is invalidated:  */
			cpu->invalidate_translation_caches(cpu,
			    cpu->cd.sh.itlb_hi[r] & ~0xfff, INVALIDATE_VADDR);

			cpu->invalidate_code_translation(cpu,
			    cpu->cd.sh.utlb_lo[i] & ~0xfff, INVALIDATE_PADDR);

			cpu->cd.sh.itlb_hi[r] = cpu->cd.sh.utlb_hi[i];
			cpu->cd.sh.itlb_lo[r] = cpu->cd.sh.utlb_lo[i];
		}
#endif

		/*  Permission checks:  */
		if (cpu->cd.sh.sr & SH_SR_MD)
			return 1;
		if (!(pr & 2))
			goto protection_violation;

		return 1;
	}

	/*  Data access:  */
	if (cpu->cd.sh.sr & SH_SR_MD) {
		/*  Kernel access:  */
		switch (pr) {
		case 0:
		case 2:	if (wf)
				goto protection_violation;
			return 1;
		case 1:
		case 3:	if (wf && !d)
				goto initial_write_exception;
			return 1 + d;
		}
	}

	/*  User access  */
	switch (pr) {
	case 0:
	case 1:	goto protection_violation;
	case 2:	if (wf)
			goto protection_violation;
		return 1;
	case 3:	if (wf && !d)
			goto initial_write_exception;
		return 1 + d;
	}


tlb_miss:
	expevt = wf? EXPEVT_TLB_MISS_ST : EXPEVT_TLB_MISS_LD;
	goto exception;

protection_violation:
	expevt = wf? EXPEVT_TLB_PROT_ST : EXPEVT_TLB_PROT_LD;
	goto exception;

initial_write_exception:
	expevt = EXPEVT_TLB_MOD;


exception:
	if (flags & FLAG_NOEXCEPTIONS) {
		*return_paddr = 0;
		return 2;
	}

	sh_exception(cpu, expevt, 0, vaddr);

	return 0;
}


/*
 *  sh_translate_sq_v2p():
 *
 *  #318: translate a store-queue address for the WRITE-BACK, which is the one
 *  store-queue access that goes through the UTLB.
 *
 *  sh_translate_v2p() maps the 0xe0000000..0xe3ffffff range identically and
 *  deliberately: that is how ordinary guest stores reach the modelled queue
 *  SRAM, so the range must never be routed through the MMU there. The flush
 *  triggered by `pref` is the exception to that, and it needs its own way in
 *  rather than a flag on the general entry point -- which has one caller, the
 *  dyntrans hook, whose signature is fixed.
 *
 *  #454: JUDGED AS A READ.  This paragraph used to say "Judged as a WRITE" and
 *  argue it from the dirty bit; the manual says the opposite, and it was not in
 *  this tree when that argument was made.  SH7750 Hardware Manual Rev.7.00 4.7.4
 *  "SQ Protection", p. 144 -- `_scratchpad/sh7750_hardware.txt:11744-11746`, and
 *  identically in the SH-4 programming manual 4.6.4 at
 *  `sh4_programming.txt:3561-3563`:
 *
 *	"Write type exception judgment is performed for writes to the SQs, and
 *	 read type for transfer from the SQs to external memory (PREF
 *	 instruction), and a TLB miss exception, protection violation
 *	 exception, or initial page write exception is generated."
 *
 *  The old argument had ONE false premise, and it is worth naming because a
 *  wrong reason gets reused: it assumed the PREF is the only access judged
 *  against an SQ page's entry.  4.7.4's FIRST clause supplies the other one.
 *  The dirty bit does stay meaningful, and a guest kernel does track the page --
 *  but at the STORE INTO the queue, not at the flush out of it.  4.7.4 can list
 *  the initial-page-write exception and still call the PREF a read because the
 *  sentence covers both halves; 3.6.7 defines that exception as occurring on
 *  "a data access (write)", so a read-type access cannot raise it at all.
 *
 *  *** WHAT THIS COSTS, STATED RATHER THAN GLOSSED: this emulator does not judge
 *  the write half AT ALL. ***  sh_translate_v2p() maps 0xe0000000..0xe3ffffff
 *  identically and unconditionally, because that is how an ordinary guest store
 *  reaches the modelled queue SRAM.
 *
 *  Precisely which faults go away, because an earlier draft of this paragraph
 *  said "an SQ page raises no MMU fault of any kind" and THIS ROUND'S OWN
 *  DETECTOR DISPROVES THAT -- `sq miss evt` observes a read-type TLB miss
 *  (0x040) on the fixed build.  What the PREF can still raise is the READ-side
 *  set: TLB miss, and a protection violation for a PR/privilege combination that
 *  forbids reading.  What disappears is the WRITE-side set: the initial-page-
 *  write exception (3.6.7 requires "a data access (write)", so read-type
 *  judgement cannot produce it) and write-side protection.  Those are exactly
 *  the two the store half owes, and the store half never runs.
 *
 *  Measured, with liveness and device-signature controls: a store into the
 *  window succeeds against a PR=00 read-only entry and against a clean one
 *  alike.  Filed as `sh4sqwrite`, which #454 makes the sole carrier of the
 *  WRITE-side SQ-page semantics -- not of all of them -- rather than a footnote
 *  in an archived audit.
 *
 *  (A panel seat read this as a load back when the tree had no manual, and was
 *  overruled.  It was right.)
 *
 *  Same return values as sh_translate_v2p().
 */
int sh_translate_sq_v2p(struct cpu *cpu, uint64_t vaddr, uint64_t *return_paddr,
	int flags)
{
	return translate_via_mmu(cpu, (uint32_t) vaddr, return_paddr, flags);
}


/*
 *  sh_translate_v2p():
 *
 *  Return values:
 *
 *	0	No access to the virtual address.
 *	1	return_paddr contains the physical address, the page is
 *		available as read-only.
 *	2	Same as 1, but the page is available as read/write.
 */
int sh_translate_v2p(struct cpu *cpu, uint64_t vaddr64, uint64_t *return_paddr,
	int flags)
{
	int user = cpu->cd.sh.sr & SH_SR_MD? 0 : 1;
	uint32_t vaddr = vaddr64;

	/*  U0/P0: Userspace addresses, or P3: Kernel virtual memory.  */
	if (!(vaddr & 0x80000000) ||
	    (vaddr >= 0xc0000000 && vaddr < 0xe0000000)) {
		/*  Address translation turned off?  */
		if (!(cpu->cd.sh.mmucr & SH4_MMUCR_AT)) {
			/*  Then return raw physical address:  */
			*return_paddr = vaddr & 0x1fffffff;
			return 2;
		}

		/*  Perform translation via the MMU:  */
		return translate_via_mmu(cpu, vaddr, return_paddr, flags);
	}

	/*  Store queue region:  */
	if (vaddr >= 0xe0000000 && vaddr < 0xe4000000) {
		/*  Note/TODO: Take SH4_MMUCR_SQMD into account.  */
		*return_paddr = vaddr;
		return 2;
	}

	if (user) {
		if (flags & FLAG_NOEXCEPTIONS) {
			*return_paddr = 0;
			return 2;
		}

		// Hopefully correct behavior; nbjoerg on #GXemul (FreeNode)
		// noticed that this case was easily triggered inside a
		// guest OS, by:  int main(void){ *(int *)-4 = 0; }
		sh_exception(cpu, (flags & FLAG_WRITEFLAG)?
		    EXPEVT_TLB_MISS_ST : EXPEVT_TLB_MISS_LD, 0, vaddr);
		return 0;
	}

	/*  P1,P2: Direct-mapped physical memory.  */
	if (vaddr >= 0x80000000 && vaddr < 0xc0000000) {
		*return_paddr = vaddr & 0x1fffffff;
		return 2;
	}

	if (flags & FLAG_INSTR) {
		fatal("TODO: instr at 0x%08" PRIx32"\n", (uint32_t)vaddr);
		exit(1);
	}

	/*  P4: Special registers mapped at 0xf0000000 .. 0xffffffff:  */
	if ((vaddr & 0xf0000000) == 0xf0000000) {
		*return_paddr = vaddr;
		return 2;
	}

	if (flags & FLAG_NOEXCEPTIONS) {
		*return_paddr = 0;
		return 2;
	}

	/*  TODO  */

	/*  The ugly 'if' is just here to fool Compaq CC.  */
	if (!(flags & FLAG_NOEXCEPTIONS)) {
		fatal("Unimplemented SH vaddr 0x%08" PRIx32"\n", vaddr);
		exit(1);
	}

	return 0;
}

