#ifndef	TIMER_H
#define	TIMER_H

/*
 *  Copyright (C) 2006-2010  Anders Gavare.  All rights reserved.
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

struct timer;

#define	TIMER_BASE_FREQUENCY	65.0	/*  Hz  */

/*
 *  #427: the frequency DOMAIN, and the catch-up BOUND.  Both are here rather than in
 *  timer.c so a test can READ them instead of transcribing them -- a transcribed constant
 *  is the shape that let a gate grade a value the run never used.
 *
 *  TIMER_MIN_FREQUENCY was already the shipped low clamp.  TIMER_MAX_FREQUENCY is DERIVED,
 *  not chosen: machine->emulated_hz is an int (machine.h), so INT_MAX bounds every
 *  legitimate request in the tree.  It is nearly worthless on its own, because at
 *  TIMER_BASE_FREQUENCY it still permits 33 million catch-up iterations per signal.  THE
 *  CAP BELOW IS THE ACTUAL PROTECTION; the domain is normalisation.
 *
 *  CORRECTION (review of 2026-08-16).  The premise first written here -- "every rate
 *  derived from it divides by at least one" -- IS FALSE, and two seats found the site:
 *  dev_footbridge.c's reload_timer_value() divides emulated_hz by a guest-written
 *  timer_load that TIMER_1_LOAD accepts as ZERO, giving +INF.  The CONCLUSION survives and
 *  is in fact stronger than the premise was: before this clamp, +INF made interval 0.0 and
 *  the catch-up loop never advanced -- a guest-reachable HANG inside the signal handler.
 *  The clamp turns that into a bounded 68 MHz.  (The same guest write reaches a division
 *  by zero at dev_footbridge.c:141, which is filed separately; this clamp does not fix it.)
 *
 *  TIMER_MAX_CATCHUP is derived from both sides, MEASURED: 65536 breaks a legitimate
 *  40 MHz timer (its delivered rate collapses to 0.1065 of real time), while an iteration
 *  costs 2.16-2.82 ns, so 2^22 would fill 59-77% of a 15.38 ms period.  2^20 is the
 *  smallest power of two that leaves every legitimate case bit-identical to the old
 *  behaviour while holding the handler under a fifth of its own period.
 *
 *  THE BOUND IS PER TIMER PER SIGNAL, AND THAT DERIVATION ASSUMED ONE TIMER.  Two seats
 *  caught it and one MEASURED the cost: four timers at the ceiling take 10.65-10.74 ms of
 *  a 15.38 ms period -- 69%, inside the very band that reasoning rejected 2^22 for -- and
 *  dev_footbridge has exactly four guest-controllable timers.  The label on the #define is
 *  accurate; the "under a fifth" figure above is the SINGLE-timer case and nothing more.
 *  Making the budget global across one signal is filed as its own question.
 *
 *  THE BACKLOG IS RETAINED when the cap is hit, never dropped: catch-up IS how any timer
 *  faster than TIMER_BASE_FREQUENCY is delivered, so dropping ticks caps EVERY timer at
 *  65 Hz -- measured, a 100 Hz timer falls to 0.65 of real time with no burst at all.
 *  Retention is right for a RECOVERABLE backlog, which is the case it was designed for.
 *  It does not rescue an UNSERVICEABLE rate: above TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY
 *  = 68,157,440 Hz the debt grows without bound and "delivered by the signals that follow"
 *  is simply untrue -- measured, a timer at the domain ceiling sits 0.9683 s behind after
 *  one simulated second and falls further every period.  The domain admits 32x more than
 *  the cap can ever serve.  That gap is real, it is not made worse by this change (the old
 *  code spun 33 million iterations per signal at the same rate), and closing it is a policy
 *  question filed rather than answered here.
 */
#define	TIMER_MIN_FREQUENCY	0.00000001	/*  Hz  */
#define	TIMER_MAX_FREQUENCY	2147483647.0	/*  Hz; INT_MAX, see above  */
#define	TIMER_MAX_CATCHUP	1048576		/*  ticks per timer per signal  */

struct timer *timer_add(double freq, void (*timer_tick)(struct timer *timer,
	void *extra), void *extra);
void timer_remove(struct timer *t);

void timer_update_frequency(struct timer *t, double new_freq);

void timer_start(void);
void timer_stop(void);

void timer_init(void);


#endif	/*  TIMER_H  */
