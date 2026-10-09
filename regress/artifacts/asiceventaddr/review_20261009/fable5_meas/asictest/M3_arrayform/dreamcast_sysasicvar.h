/*  GXemul: $Id: dreamcast_sysasicvar.h,v 1.2 2006-10-28 01:37:54 debug Exp $  */
/*  $NetBSD: sysasicvar.h,v 1.5 2005/12/24 23:24:00 perry Exp $  */

/*
 *  Extended with useful macros and also some more event definitions
 *  described in KOS comments by Dan Potter (kos/kernel/arch/dreamcast
 *  /hardware/asic.c).
 */

#ifndef _DREAMCAST_SYSASICVAR_H_
#define	_DREAMCAST_SYSASICVAR_H_

/*-
 * Copyright (c) 2001 The NetBSD Foundation, Inc.
 * All rights reserved.
 *
 * This code is derived from software contributed to The NetBSD Foundation
 * by 
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 *        This product includes software developed by the NetBSD
 *        Foundation, Inc. and its contributors.
 * 4. Neither the name of The NetBSD Foundation nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE NETBSD FOUNDATION, INC. AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#define	SYSASIC_BASE		0x5f6900
#define	SYSASIC_SIZE		   0x100

#define	SYSASIC_EVENT_RENDERDONE	2	/*  Render Completed  */
#define	SYSASIC_EVENT_PVR_SCANINT1	3	/*  Scanline interrupt 1  */
#define	SYSASIC_EVENT_PVR_SCANINT2	4	/*  Scanline interrupt 2  */
#define	SYSASIC_EVENT_VBLINT		5	/*  VBlank interrupt  */
#define	SYSASIC_EVENT_OPAQUEDONE	7	/*  Opaque list complete  */
#define	SYSASIC_EVENT_OPAQUEMODDONE	8	/*  Opaque modifiers complete */
#define	SYSASIC_EVENT_TRANSDONE		9	/*  Transparent list complete */
#define	SYSASIC_EVENT_TRANSMODDONE	10	/*  Trans. modifiers complete */
#define SYSASIC_EVENT_MAPLE_DMADONE	12	/*  Maple DMA complete  */
#define SYSASIC_EVENT_MAPLE_ERROR	13	/*  Maple error  */
#define	SYSASIC_EVENT_GDROM_DMA		14	/*  GD-ROM DMA Complete  */
#define	SYSASIC_EVENT_SPU_DMA		15	/*  SPU DMA Complete  */
#define	SYSASIC_EVENT_SPU_IRQ		17	/*  SPU Interrupt  */
#define	SYSASIC_EVENT_PVR_DMA		19	/*  PVR DMA Complete  */
#define	SYSASIC_EVENT_PVR_PTDONE	21	/*  Punch-through complete  */
#define SYSASIC_EVENT_GDROM		32	/*  GD-ROM Command status  */
#define SYSASIC_EVENT_AICA		33	/*  AICA (?)  */
#define SYSASIC_EVENT_8BIT		34	/*  Modem/Lan adapter  */
#define SYSASIC_EVENT_EXT		35	/*  PCI/BBA IRQ  */
#define	SYSASIC_EVENT_PRIMOUTOFMEM	66	/*  Out of primitive mem  */
#define	SYSASIC_EVENT_MATOUTOFMEM	67	/*  Out of matrix mem  */

/*  #466/#468: THIS MACRO IS CORRECT ONLY FOR e IN [0,95], AND IT IS NOW ENFORCED
    AT COMPILE TIME -- see SYSASIC_EVENT_RANGE_OK below.

    #466 shipped this as a COMMENT ONLY, on the rationale that _Static_assert is
    C11 while this tree is C99, and that an assert can only name terms that
    already exist -- so a new #define would add a name it does not mention and
    compile clean.  *** BOTH LEGS WERE REFUTED BY MEASUREMENT on #466's pass 2,
    independently by two seats, one of which BUILT ALL FOUR VARIANTS: ***
      - the C11 leg ruled out one SPELLING, not compile-time checking.  The
        negative-width bitfield idiom below needs only C89, and is clean under
        -std=c89 -pedantic-errors -Wall -Wextra.  (The build compiler in fact
        reports __STDC_VERSION__ 202311L, so "this tree is C99" was a
        portability policy, not a fact about what compiles.)
      - the shape leg analysed the wrong placement.  A STANDALONE assert does
        compile clean on the feared edit -- MEASURED.  A check INSIDE the macro
        does not: it fires at the RAISE, so it cannot be bypassed by adding a
        name.  MEASURED: `#define SYSASIC_EVENT_FOO 96` plus a raise is a hard
        compile error, while all 21 real events keep BYTE-IDENTICAL addresses.

    HONEST CONTRACT: the guard fires at a CALL SITE, not at a definition.  A
    define of 96 that is never raised still compiles -- which is benign by
    construction, since an event never passed to this macro cannot reach the
    defect.  That is a STRONGER domain than a name-based assert, not weaker.

    STRUCTURALLY: the macro treats the event's high bits as a word index into the
    WHOLE 64-word register file, when only words 0..2 -- the pending_irq group --
    are what it means to address.  Enumerated over [0,8192) against the real
    switch:
         0..95   +0x00/04/08  CORRECT   pending_irq[0..2]
        96..127  +0x0c        DROPPED   r == 3, falls to default:
       128..223  +0x10/14/18  CLOBBER   mask_13[0..2]
       224..255  +0x1c        DROPPED
       256..351  +0x20/24/28  CLOBBER   mask_11[0..2]
       352..383  +0x2c        DROPPED
       384..479  +0x30/34/38  CLOBBER   mask_9[0..2]
       480..2047              DROPPED
        >= 2048  +0x100 up    leaves the device window (>= 6144 reaches MAPLE)
    THE CLOBBER DOMAIN IS e IN [128,479] -- 352 values across NINE mask words.
    A clobber is worse than a drop: the raise both FAILS and DESTROYS the guest's
    programmed IRQ mask, because the mask cases carry no hack-bit discrimination
    and the store is a wholesale replacement, with the tick called immediately.
    No bounds check can see it -- the offset is VALID and only the MEANING is wrong.

    Max over the 21 defines above is 67 (67>>5 == 2), so this is LATENT.
    Adding an event >= 96 makes it live.  See dev_dreamcast_asic.c's #463
    invariant comment, which reasons about the r == 3 half from the other
    side.  Filed as `asiceventaddr`.  */
/*  #468/#469: evaluates to 0 for a legal event and fails to COMPILE otherwise.  The
    domain is [0,95] and BOTH ENDS are enforced.

    *** #468 GUARDED ONLY THE UPPER END, AND A PASS-2 SEAT MEASURED THE HOLE
    WITHIN THE HOUR. ***  The first form tested `(e) < 96`, which -1 satisfies,
    so `SYSASIC_EVENT_TO_ADDR(-1)` COMPILED CLEAN and produced 0x005f68fc --
    four bytes BELOW SYSASIC_BASE, because `4*((-1)>>5)` is -4.  Reproduced
    here before fixing: the guard passed and the address was out of range.

    A guard written from the DEFECT (events too large) rather than from the
    DOMAIN ([0,95]) covers one end and reads as if it covers both.  The
    bitfield form is preferred over a negative-size array because a runtime
    variable `e` silently degrades an array to a VLA, while a bitfield width
    must be an integer constant and hard-errors.  */
#define	SYSASIC_EVENT_RANGE_OK(e)				\
	((int)sizeof(char[\
		((e) >= 0 && (e) < 96) ? 1 : -1]) * 0)

#define	SYSASIC_EVENT_TO_ADDR(e)				\
	(SYSASIC_BASE + 4*((e)>>5) + SYSASIC_EVENT_RANGE_OK(e))
#define	SYSASIC_EVENT_TO_BITMASK(e)	(1 << ((e) & 31))

#define	SYSASIC_TRIGGER_EVENT(e)	{				\
	uint8_t buf[8];							\
	uint64_t tmp1 = SYSASIC_EVENT_TO_ADDR(e);			\
	uint64_t tmp2 = SYSASIC_EVENT_TO_BITMASK(e);			\
	tmp2 |= 0x100000000ULL;		/*  Internal GXemul hack  */	\
	memory_writemax64(cpu, buf, 8, tmp2);				\
	cpu->memory_rw(cpu, cpu->mem, tmp1, buf, 8,			\
	    MEM_WRITE, PHYSICAL);					\
	}


#if 0
const char *__pure sysasic_intr_string(int /*ipl*/) __attribute__((const));
void	*sysasic_intr_establish(int /*event*/, int /*ipl*/,
	    int (*ih_fun)(void *), void *);
void	sysasic_intr_disestablish(void *);
void	sysasic_intr_enable(void *, int /*on*/);
#endif

#endif /* !_DREAMCAST_SYSASICVAR_H_ */
