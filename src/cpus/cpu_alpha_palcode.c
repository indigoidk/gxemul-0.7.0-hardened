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
 *  Alpha PALcode-related functionality.
 *
 *  (See http://www.alphalinux.org/docs/alphaahb.html for good descriptions
 *  of many PALcode functions.)
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "console.h"
#include "cpu.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"
#include "symbol.h"

#include "thirdparty/alpha_prom.h"


/*
 *  alpha_palcode_name():
 *
 *  Return the name of a PALcode number, as a string.
 */
void alpha_palcode_name(uint32_t palcode, char *buf, size_t buflen)
{
	switch (palcode) {
	case 0x00: snprintf(buf, buflen, "PAL_halt"); break;
	case 0x01: snprintf(buf, buflen, "PAL_cflush"); break;
	case 0x02: snprintf(buf, buflen, "PAL_draina"); break;
	case 0x09: snprintf(buf, buflen, "PAL_cserve"); break;
	case 0x0a: snprintf(buf, buflen, "PAL_swppal"); break;
	case 0x0d: snprintf(buf, buflen, "PAL_ipir"); break;
	case 0x10: snprintf(buf, buflen, "PAL_OSF1_rdmces"); break;
	case 0x11: snprintf(buf, buflen, "PAL_OSF1_wrmces"); break;
	case 0x2b: snprintf(buf, buflen, "PAL_OSF1_wrfen"); break;
	case 0x2d: snprintf(buf, buflen, "PAL_OSF1_wrvptptr"); break;
	case 0x30: snprintf(buf, buflen, "PAL_OSF1_swpctx"); break;
	case 0x31: snprintf(buf, buflen, "PAL_OSF1_wrval"); break;
	case 0x32: snprintf(buf, buflen, "PAL_OSF1_rdval"); break;
	case 0x33: snprintf(buf, buflen, "PAL_OSF1_tbi"); break;
	case 0x34: snprintf(buf, buflen, "PAL_OSF1_wrent"); break;
	case 0x35: snprintf(buf, buflen, "PAL_OSF1_swpipl"); break;
	case 0x36: snprintf(buf, buflen, "PAL_rdps"); break;
	case 0x37: snprintf(buf, buflen, "PAL_OSF1_wrkgp"); break;
	case 0x38: snprintf(buf, buflen, "PAL_OSF1_wrusp"); break;
	case 0x39: snprintf(buf, buflen, "PAL_OSF1_wrperfmon"); break;
	case 0x3a: snprintf(buf, buflen, "PAL_OSF1_rdusp"); break;
	case 0x3c: snprintf(buf, buflen, "PAL_whami"); break;
	case 0x3d: snprintf(buf, buflen, "PAL_OSF1_retsys"); break;
	case 0x3e: snprintf(buf, buflen, "PAL_wtint"); break;
	case 0x3f: snprintf(buf, buflen, "PAL_OSF1_rti"); break;
	case 0x80: snprintf(buf, buflen, "PAL_bpt"); break;
	case 0x81: snprintf(buf, buflen, "PAL_bugchk"); break;
	case 0x83: snprintf(buf, buflen, "PAL_OSF1_callsys"); break;
	case 0x86: snprintf(buf, buflen, "PAL_imb"); break;
	case 0x92: snprintf(buf, buflen, "PAL_OSF1_urti"); break;
	case 0x9e: snprintf(buf, buflen, "PAL_rdunique"); break;
	case 0x9f: snprintf(buf, buflen, "PAL_wrunique"); break;
	case 0xaa: snprintf(buf, buflen, "PAL_gentrap"); break;
	case 0xae: snprintf(buf, buflen, "PAL_clrfen"); break;
	case 0x3fffffe: snprintf(buf, buflen, "GXemul_PROM"); break;
	default:snprintf(buf, buflen, "UNKNOWN 0x%" PRIx32, palcode);
	}
}


/*
 *  alpha_prom_call():
 */
void alpha_prom_call(struct cpu *cpu)
{
	uint64_t addr, a1 = cpu->cd.alpha.r[ALPHA_A1];
	uint64_t a2 = cpu->cd.alpha.r[ALPHA_A2], a3 = cpu->cd.alpha.r[ALPHA_A3];
	uint64_t len;
	const char *s = "";

	switch (cpu->cd.alpha.r[ALPHA_A0]) {

	case PROM_R_PUTS:
		/*  a1 = channel, a2 = ptr to buf, a3 = len  */
		for (addr = a2; addr < a2 + a3; addr ++) {
			unsigned char ch;
			cpu->memory_rw(cpu, cpu->mem, addr, &ch, sizeof(ch),
			    MEM_READ, CACHE_DATA | NO_EXCEPTIONS);
			console_putchar(cpu->machine->main_console_handle, ch);
		}
		cpu->cd.alpha.r[ALPHA_V0] = a3;
		break;

	case PROM_R_GETENV:
		/*  a1 = variable id, a2 = char *buf, a3 = bufsize  */
		switch (a1) {
		case PROM_E_BOOTED_DEV:
			s = "";		/*  TODO  */
			break;
		case PROM_E_BOOTED_FILE:
			s = cpu->machine->boot_kernel_filename;
			break;
		case PROM_E_BOOTED_OSFLAGS:
			s = cpu->machine->boot_string_argument;
			break;
		case PROM_E_TTY_DEV:
			s = "";		/*  TODO  */
			break;
		default:fatal("[ Alpha PALcode: GXemul PROM getenv %" PRIi64 ": TODO "
			    "]\n", (int64_t)cpu->cd.alpha.r[ALPHA_A1]);
			cpu->running = 0;
		}
		/*  Copy at most a3 bytes.  */
		len = a3;
		if (strlen(s) < len)
			len = strlen(s) + 1;
		store_buf(cpu, a2, s, len);
		break;

	default:fatal("[ Alpha PALcode: GXemul PROM call, a0=0x%" PRIx64" ]\n",
		    (uint64_t) cpu->cd.alpha.r[ALPHA_A0]);
		cpu->running = 0;
	}

	/*  Return from the PROM call.  */
	cpu->pc = cpu->cd.alpha.r[ALPHA_RA];
}


/*
 *  alpha_palcode():
 *
 *  Execute an Alpha PALcode instruction. (Most of these correspond to
 *  OSF1 palcodes, used by for example NetBSD/alpha.)
 */
void alpha_palcode(struct cpu *cpu, uint32_t palcode)
{
	uint64_t a0 = cpu->cd.alpha.r[ALPHA_A0], a1 = cpu->cd.alpha.r[ALPHA_A1];
	uint64_t userMode = cpu->cd.alpha.ps & ALPHA_PSL_USERMODE;

	/*
	 *  Only these are unprivileged, i.e. can be invoked in user mode,
	 *  according to the manual:
	 *
	 *	bpt		kernel and user
	 *	bugchk		kernel and user
	 *	callsys		user
	 *	clrfen		user
	 *	gentrap		kernel and user
	 *	imb		kernel and user
	 *	rdunique	kernel and user
	 *	urti		user
	 *	wrunique	kernel and user
	 */

	if (userMode && !(
	    palcode == 0x80 || palcode == 0x81 || palcode == 0x83 ||
	    palcode == 0xae || palcode == 0xaa || palcode == 0x86 ||
	    palcode == 0x9e || palcode == 0x92 || palcode == 0x9f)) {
		// opDec fault.
		fatal("[ Privileged Alpha PALcode called from user mode: TODO ]");
		cpu->running = 0;
		return;
	}

	switch (palcode) {
#if 0
TODO: Uncomment more again, as I progress with the emulation...
Make sure they are correct, as documented in the Manual.

	case 0x02:	/*  PAL_draina  */
		/*  TODO?  */
		break;
#endif
	case 0x10:	/*  PAL_OSF1_rdmces  */
		/*  Return Machine Check status in v0.  */
		cpu->cd.alpha.r[ALPHA_V0] = cpu->cd.alpha.mces;
		break;
	case 0x11:	/*  PAL_OSF1_wrmces  */
		/*  Clear bits 0, 1, and 2 of the Machine Check and Error status.  */
		cpu->cd.alpha.mces = ~(cpu->cd.alpha.r[ALPHA_A0] & 7);

		/*  Set bits 3 and 4 of the Machine Check and Error status.  */
		cpu->cd.alpha.mces &= ~0x18;
		cpu->cd.alpha.mces |= (cpu->cd.alpha.r[ALPHA_A0] & 0x18);
		break;
	case 0x2b:	/*  PAL_OSF1_wrfen  */
		/*  Floating point enable: a0 = 1 or 0.  */
		/*  TODO. Since clrfen is documented as:
			FEN ← 0
			(PCBB+40)<0> ← 0
		    then most likely wrfen should do the reverse.
		 */
		cpu->cd.alpha.pcb.apcb_flags = cpu->cd.alpha.r[ALPHA_A0];
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 40,
		    cpu->cd.alpha.pcb.apcb_flags);
		break;
	case 0x2d:	/*  PAL_OSF1_wrvptptr  */
		/*  Write Virtual Page Table Pointer. a0 = value  */
		cpu->cd.alpha.vptptr = a0;
		break;
	case 0x30:	/*  PAL_OSF1_swpctx  */
		/*  Save old context:  */
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 0,
		    cpu->cd.alpha.pcb.apcb_ksp);
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 8,
		    cpu->cd.alpha.pcb.apcb_usp);
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 16,
		    cpu->cd.alpha.pcb.apcb_ptbr);
		store_32bit_word(cpu, cpu->cd.alpha.ctx + 24,
		    cpu->cd.alpha.pcb.apcb_cpc);
		store_32bit_word(cpu, cpu->cd.alpha.ctx + 28,
		    cpu->cd.alpha.pcb.apcb_asn);
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 32,
		    cpu->cd.alpha.pcb.apcb_unique);
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 40,
		    cpu->cd.alpha.pcb.apcb_flags);
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 48,
		    cpu->cd.alpha.pcb.apcb_decrsv0);
		store_64bit_word(cpu, cpu->cd.alpha.ctx + 56,
		    cpu->cd.alpha.pcb.apcb_decrsv1);

		/*  Return old context in v0.  */
		/*  #514: was ALPHA_A0, contradicting the comment directly above and the
		    third-party ABI wrapper.  `alpha_pal_swpctx' (alpha_cpu.h) declares
		    `v0 __asm("$0")' as an OUTPUT, so a correct caller reads the result
		    from v0.  a0 is NOT in that asm's clobber list ($1,$22..$25,memory) --
		    it is an IN-OUT OPERAND ("=r" (a0) with input "0" (a0)), and the
		    wrapper's own comment marks it clobbered "(above)", i.e. handled as
		    that operand.  Either way the caller may not rely on a0, so the model
		    was publishing into the register the caller discards and leaving
		    untouched the one it reads.  (An earlier draft of this comment said the
		    wrapper "lists a0 as clobbered"; a pass-2 seat read the asm and showed
		    it does not.)  No a0 write is added: the architecture marks a0
		    UNPREDICTABLE, which permits it to remain unchanged.  Ordering is
		    unaffected -- `a0' at the `ctx = a0' below is the LOCAL captured at
		    function entry (`:165'), not a live register read.  Census, corrected
		    twice and stated as of AFTER this fix: no `r[ALPHA_A0] =' remains in the
		    file, and the compiled PAL returns to v0 are rdmces, this swpctx,
		    swpipl, rdps and whami -- three further v0 stores sit inside `#if 0' and
		    `:118' is alpha_prom_call, not a PAL.  */
		cpu->cd.alpha.r[ALPHA_V0] = cpu->cd.alpha.ctx;	/*  #514  */

		/*  Load new context:  */
		{
			cpu->cd.alpha.ctx = a0;
			uint64_t new_ksp =
			    load_64bit_word(cpu, cpu->cd.alpha.ctx + 0);
			uint64_t new_usp =
			    load_64bit_word(cpu, cpu->cd.alpha.ctx + 8);
			uint64_t new_ptbr =
			    load_64bit_word(cpu, cpu->cd.alpha.ctx + 16);
			uint64_t new_cpc =
			    load_32bit_word(cpu, cpu->cd.alpha.ctx + 24);
			uint64_t new_asn =
			    load_32bit_word(cpu, cpu->cd.alpha.ctx + 28);
			uint64_t new_unique =
			    load_64bit_word(cpu, cpu->cd.alpha.ctx + 32);
			uint64_t new_flags =
			    load_64bit_word(cpu, cpu->cd.alpha.ctx + 40);
			uint64_t new_decrsv0 =
			    load_64bit_word(cpu, cpu->cd.alpha.ctx + 48);
			uint64_t new_decrsv1 =
			    load_64bit_word(cpu, cpu->cd.alpha.ctx + 56);

			// Update all variables in the pcb simultaneously:
			cpu->cd.alpha.pcb.apcb_ksp = new_ksp;
			cpu->cd.alpha.pcb.apcb_usp = new_usp;
			cpu->cd.alpha.pcb.apcb_ptbr = new_ptbr;
			cpu->cd.alpha.pcb.apcb_cpc = new_cpc;
			cpu->cd.alpha.pcb.apcb_asn = new_asn;
			cpu->cd.alpha.pcb.apcb_unique = new_unique;
			/*  #507: was `apcb_ptbr = new_flags' -- a field-name transposition that
			    assigned apcb_ptbr TWICE (here and at the `apcb_ptbr = new_ptbr' four
			    lines above -- "three lines up" until 2026-09-07, corrected
			    after a pass-2 seat derived the true distance from the hunk
			    header alone and called the phrasing inconsistent) and apcb_flags NEVER,
			    while every other field in this block is assigned exactly once.  Two
			    consequences: apcb_ptbr ended up holding the flags word, and the incoming
			    context's flags were dropped -- so the NEXT save published a never-loaded
			    word back into the outgoing PCB, wiping what the guest planted.  */
			cpu->cd.alpha.pcb.apcb_flags = new_flags;	/*  #507  */
			cpu->cd.alpha.pcb.apcb_decrsv0 = new_decrsv0;
			cpu->cd.alpha.pcb.apcb_decrsv1 = new_decrsv1;

			// TODO: Don't invalidate EVERYTHING!
			cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
		}
		break;
#if 0
	case 0x31:	/*  PAL_OSF1_wrval  */
		/*  a0 = value  */
		cpu->cd.alpha.sysvalue = a0;
		break;
	case 0x32:	/*  PAL_OSF1_rdval  */
		/*  return: v0 = value  */
		cpu->cd.alpha.r[ALPHA_V0] = cpu->cd.alpha.sysvalue;
		break;
#endif
	case 0x33:	/*  PAL_OSF1_tbi  */
		/*
		 *  a0 = op, a1 = vaddr
		 *  (#520: a0 was ignored -- "a0 is ignored for now. TODO." --
		 *  until the selector test below was corrected.  It is read now,
		 *  so that line is removed rather than left to mislead.)
		 *	a0 = 1: ITB invalidate
		 *	a0 = 2: DTB invalidate
		 *	a0 = 3: both ITB and DTB
		 *	a0 = -1: invalidate everything with ASM=0.
		 *	a0 = -2: invalidate everything
		 */
		// debug("[ Alpha PALcode: PAL_OSF1_tbi: a0=%" PRIi64" a1=0x%"
		//    PRIx64" ]\n", (int64_t)a0, (uint64_t)a1);
		/*  #520 (alphatbinegsel): `a0' is a uint64_t, so the old `a0 >= 1'
		    was an UNSIGNED compare and BOTH negative selectors named in the
		    header above -- -1 and -2, the two documented as invalidate-
		    EVERYTHING -- compared GREATER than 1 and took the single-VADDR
		    branch.  A guest TBIA/TBIAP therefore flushed ONE page and left
		    every other cached translation live.  MEASURED at rung 3 BEFORE
		    this edit.  The citation names the FROZEN 7-row witness, NOT the
		    live probe, because the live probe has since grown to 13 rows and
		    a citation into a file that changes under you decays silently:
		        artifacts/alphatbinegsel/witness_agy_20260908/
		            alphatbi_probe.asrun.py  -- the 7-row instrument
		            alphatbi_committed.out   -- 5/7, both negatives RED
		            alphatbi_fixed.out       -- 7/7
		        artifacts/alphatbinegsel/fix_20260910/{HEAD,FIX520}_run1.out
		            -- the same pair replicated on a second build
		    The SHIPPED 13-row detector scores 10/13 and 13/13 on those two
		    builds (killtable_20260910/t2/probe_{HEAD,BASE}.raw).  An earlier
		    draft cited the LIVE path for the 5/7 pair, and the pass-2 review
		    caught that the named artifact had come to CONTRADICT the number
		    beside it -- the reused-log-name decay, inside product code.

		    1, 2 and 3 are the only selective ops the architecture defines,
		    so 0 and 4.. are undefined and fall to the conservative arm with
		    the negatives.  Over-invalidation cannot serve a stale
		    translation; under-invalidation can, which is this defect.

		    *** THE LOAD-BEARING PROPERTY IS THE TWO-SIDEDNESS, NOT THE
		    SIGNEDNESS, and the pass-2 panel corrected me on that. ***  The
		    casts are MEASURED REDUNDANT: `a0 >= 1 && a0 <= 3' unsigned
		    agrees with the signed form on every input, because a negative
		    selector is a huge unsigned value that fails the UPPER bound
		    exactly where the signed reading fails the LOWER one.  Checked
		    over every boundary class and 300,000 random 64-bit values,
		    zero disagreements (the kimi substitute raised it; enumerated
		    rather than argued).  The casts are KEPT because they state the
		    selector's signedness to a reader, not because they repair
		    anything -- so do not describe them as the fix.

		    WHAT THE COMPARISON'S WIDTH DOES buy is real and is ROWED:
		    narrowing either cast to 32 bits passes every selector the
		    detector drives, and diverges first at a0 = 0x100000001, where
		    the 64-bit reading invalidates everything and a 32-bit one
		    truncates to 1 and flushes a single page (deepseek, pass 2).

		    -1 and -2 differ on hardware only in whether GLOBAL entries
		    survive: -1 invalidates the ASM=0 entries and SPARES the ASM=1
		    ones, -2 invalidates both.  This model's translation cache
		    carries no ASM/ASN metadata to spare anything BY, so both map
		    to INVALIDATE_ALL -- EXACT for -2 and CONSERVATIVE for -1,
		    which is the safe direction and is not the same claim.

		    THE WINDOW'S UPPER BOUND IS NOT THIS COMMENT'S TO ASSERT.  It
		    comes from imported third-party material this round does not
		    touch -- alpha_cpu.h defines EXACTLY five selectors, and the
		    three selective ones are TBISI(1), TBISD(2) and TBIS(3), so 3
		    is the largest.  That is a better authority than the header
		    above, which this round is editing: a comment you are rewriting
		    cannot be the warrant for the rewrite.

		    NO ANNOUNCE, deliberately -- and the in-file warrant is
		    `swpipl' (case 0x35) and `wrmces' (case 0x11), NOT #514.  Those
		    two take a guest value the model cannot honour exactly and
		    SILENTLY NORMALISE it (`ps |= a0 & ALPHA_PSL_IPL_MASK', `mces
		    &= ~0x18'): same file, same function, same act -- an
		    unrepresentable guest INPUT, quietly narrowed, no diagnostic.
		    The addition licence carries the rest: an announce here has no
		    measured delta, and no OSF/1-ABI guest can even reach the
		    unrecognised region, because every caller goes through those
		    five macros.

		    AND THE DEPARTURE IS STATED RATHER THAN HIDDEN: this file has
		    FOUR sites that meet an unrecognised selector with `fatal()'
		    and `cpu->running = 0' -- the two GXemul-PROM `default:' arms,
		    the privileged-from-user check, and `wrent', which is the
		    closest structural sibling of all (an out-of-range selector in
		    a guest register, guarded by a bound, in this same switch).
		    This arm deliberately does NOT follow them, in the fork's
		    de-fatalising direction.  A reader must not conclude the file
		    has no contrary practice; it has four instances of it.

		    (Two earlier drafts of this paragraph were wrong and are
		    recorded because a wrong warrant gets reused.  The first
		    appealed to "the house latched-announce idiom", which is a
		    DEVICES one -- `(once)' appears 40 times under src/devices and
		    NOT ONCE under src/cpus.  The second cited #514, which is about
		    an architecturally UNPREDICTABLE OUTPUT the model declines to
		    define -- leaving a register nobody may read alone is not the
		    same act as silently re-interpreting a request a guest made.
		    The conclusion survived both; the warrant did not.)  */
		if ((int64_t)a0 >= 1 && (int64_t)a0 <= 3)
			cpu->invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR);
		else
			cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
		break;
	case 0x34:	/*  PAL_OSF1_wrent (Write System Entry Address)  */
		/*  a0 = new vector, a1 = vector selector  */
		if (a1 < N_ALPHA_KENTRY)
			cpu->cd.alpha.kentry[a1] = a0;
		else {
			fatal("[ Alpha PALcode: PAL_OSF1_wrent: attempt to "
			    "write to non-implemented selector %i ]\n",
			    (int)a1);
			cpu->running = 0;
		}
		break;
	case 0x35:	/*  PAL_OSF1_swpipl  */
		/*  a0 = new ipl, v0 = return old ipl  */
		cpu->cd.alpha.r[ALPHA_V0] = cpu->cd.alpha.ps & ALPHA_PSL_IPL_MASK;
		cpu->cd.alpha.ps &= ~ALPHA_PSL_IPL_MASK;
		cpu->cd.alpha.ps |= (a0 & ALPHA_PSL_IPL_MASK);
		break;
	case 0x36:	/*  PAL_rdps  */
		cpu->cd.alpha.r[ALPHA_V0] = cpu->cd.alpha.ps;
		break;
	case 0x37:	/*  PAL_OSF1_wrkgp  */
		cpu->cd.alpha.kgp = a0;
		break;
#if 0
	case 0x38:	/*  PAL_OSF1_wrusp  */
		/*  a0 = value  */
		cpu->cd.alpha.pcb.apcb_usp = a0;
		break;
	case 0x3a:	/*  PAL_OSF1_rdusp  */
		/*  return: v0 = value  */
		cpu->cd.alpha.r[ALPHA_V0] = cpu->cd.alpha.pcb.apcb_usp;
		break;
#endif
	case 0x3c:	/*  PAL_whami  */
		/*  Returns CPU id in v0:  */
		cpu->cd.alpha.r[ALPHA_V0] = cpu->cpu_id;
		break;
#if 0
	case 0x81:	/*  PAL_bugchk  */
		cpu->running = 0;
		break;
	case 0x83:	/*  PAL_OSF1_syscall  */
		fatal("[ Alpha PALcode: syscall, but no syscall handler ]\n");
		cpu->running = 0;
		break;
#endif
	case 0x86:	/*  PAL_imb  */
		/*  TODO  */
		break;
#if 0
	case 0x3fffffc:
		fatal("[ Alpha: KENTRY not set! Halting. ]");
		cpu->running = 0;
		break;
	case 0x3fffffd:
		fatal("[ Alpha PALcode: Fixup: TODO ]\n");
		/*  Return from the fixup call.  */
		cpu->cd.alpha.r[ALPHA_V0] = 0;	/*  Success?  */
		cpu->pc = cpu->cd.alpha.r[ALPHA_RA];
		break;
#endif
	case 0x3fffffe:
		alpha_prom_call(cpu);
		break;
	default:fatal("[ Alpha PALcode 0x%x unimplemented! ]\n", palcode);
		cpu->running = 0;
	}

	/*
	 *  Many PALcode instructions in the Alpha manual (and in NetBSD/Alpha
	 *  source code) are described with "clobbers t0, t8-t11", some also
	 *  with a0, and some also with a1 included.
	 *
	 *  However, it's easier to just leave the registers as they are.
	 */
}

