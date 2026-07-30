/*
 *  Copyright (C) 2004-2021  Anders Gavare.  All rights reserved.
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
 *  Floating point emulation routines.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <float.h>

#include "float_emul.h"
#include "misc.h"


/*  #define IEEE_DEBUG  */


/*
 *  #279: one-shot latches for the two "unimplemented format" diagnostics
 *  below.  Both were printed by ungated fatal() from a path a guest repeats at
 *  will: on MIPS every fmt outside {S,D,W,L} maps to 0 here (see
 *  mips_fmt_to_ieee_fmt[] in cpu_mips_coproc.c) and cpu_mips_instr.c admits PS
 *  to the slow COP1 path, so ONE add.ps produced 8 host lines -- 6 from
 *  ieee_interpret_float_value() (three sites, two operands) and 2 from
 *  ieee_store_float_value() -- measured identically on R3000 and R4000.
 *
 *  A latch, not a verbosity gate.  The guest is told nothing here: fd is
 *  silently written 0, so this line is the only record that the emulator met a
 *  format it does not model, and exactly one of them should survive into a -q
 *  run, where a VERBOSITY_DEBUG gate would be invisible.  (#276 gates its
 *  message instead -- there the guest IS answered, so the line is noise rather
 *  than a deficiency tripwire.)  fatal() is kept because neither function has
 *  a cpu or a machine pointer in scope, so debugmsg_cpu() is not available.
 *
 *  These flags are PROCESS-GLOBAL, not per-instance like #269's and #277's:
 *  float_emul.c is a stateless helper with no struct to hang state on.  The
 *  cost is that with more than one emulated machine only the first one's bad
 *  format is reported.  That is a deliberate deviation, stated here rather
 *  than left to be discovered.  One flag per distinct message and never one
 *  shared flag -- a shared flag would let whichever message fires first mask
 *  the other one for good.
 */
static int interpret_badfmt_warned = 0;
static int store_badfmt_warned = 0;


/*
 *  ieee_interpret_float_value():
 *
 *  Interprets a float value from binary IEEE format into an ieee_float_value
 *  struct.
 */
void ieee_interpret_float_value(uint64_t x, struct ieee_float_value *fvp,
	int fmt)
{
	memset(fvp, 0, sizeof(struct ieee_float_value));

	int n_frac = 0, n_exp = 0;
	int i, nan, sign = 0, exponent;
	double fraction;

	/*  n_frac and n_exp:  */
	switch (fmt) {
	case IEEE_FMT_S:	n_frac = 23; n_exp = 8; break;
	case IEEE_FMT_W:	n_frac = 31; n_exp = 0; break;
	case IEEE_FMT_D:	n_frac = 52; n_exp = 11; break;
	case IEEE_FMT_L:	n_frac = 63; n_exp = 0; break;
	default:/*  #279  */
		if (!interpret_badfmt_warned) {
			interpret_badfmt_warned = 1;
			fatal("ieee_interpret_float_value(): "
			    "unimplemented format %i\n", fmt);
		}
	}

	/*  Get the Exponent:  */
	exponent = 0;
	switch (fmt) {
	case IEEE_FMT_W:
		x &= 0xffffffffULL;
	case IEEE_FMT_L:
		break;
	case IEEE_FMT_S:
		x &= 0xffffffffULL;
		// fall through
	case IEEE_FMT_D:
		exponent = (x >> n_frac) & ((1 << n_exp) - 1);
		exponent -= (1 << (n_exp-1)) - 1;
		break;
	default:/*  #279  */
		if (!interpret_badfmt_warned) {
			interpret_badfmt_warned = 1;
			fatal("ieee_interpret_float_value(): unimplemented "
			    "format %i\n", fmt);
		}
	}

	/*  Is this a Not-A-Number?  */
	nan = 0;
	switch (fmt) {
	case IEEE_FMT_S:
		sign = (x >> 31) & 1;
		if ((x & ~0x80000000ULL) == 0x7f800000ULL) {
			fvp->f = INFINITY;
			goto zero_or_no_reasonable_result;
		}
		if ((x & 0x7f800000ULL) == 0x7f800000ULL)
			nan = 1;
		break;
	case IEEE_FMT_D:
		sign = (x >> 63) & 1;
		if ((x & ~0x8000000000000000ULL) == 0x7ff0000000000000ULL) {
			fvp->f = INFINITY;
			goto zero_or_no_reasonable_result;
		}
		if ((x & 0x7ff0000000000000ULL) == 0x7ff0000000000000ULL)
			nan = 1;
		break;
	}

	if (nan) {
		fvp->f = NAN;
		goto no_reasonable_result;
	}

	/*  Calculate the fraction:  */
	fraction = 0.0;

	switch (fmt) {

	case IEEE_FMT_W:
		{
			int32_t r_int = x;
			fraction = r_int;
		}
		break;

	case IEEE_FMT_L:
		{
			int64_t r_int = x;
			fraction = r_int;
		}
		break;

	case IEEE_FMT_S:
	case IEEE_FMT_D:
		if (x == 0 ||
		    (fmt == IEEE_FMT_D && x == 0x8000000000000000ULL) ||
		    (fmt == IEEE_FMT_S && x == 0x80000000ULL)) {
			fvp->f = 0.0;
			goto zero_or_no_reasonable_result;
		}

		fraction = 0.0;
		for (i=0; i<n_frac; i++) {
			int bit = (x >> i) & 1;
			fraction /= 2.0;
			if (bit)
				fraction += 1.0;
		}

		/*  Add implicit bit 0:  */
		fraction = (fraction / 2.0) + 1.0;
		break;

	default:/*  #279  */
		if (!interpret_badfmt_warned) {
			interpret_badfmt_warned = 1;
			fatal("ieee_interpret_float_value(): "
			    "unimplemented format %i\n", fmt);
		}
	}

	/*  form the value:  */
	fvp->f = fraction;

#ifdef IEEE_DEBUG
	fatal("{ ieee: x=%016"PRIx64" => sign=%i exponent=%i frac=%f ",
	    (uint64_t) x, sign, exponent, fraction);
#endif

	/*  TODO: this is awful for exponents of large magnitude.  */
	if (exponent > 0) {
		/*
		 *  NOTE / TODO:
		 *
		 *  This is an ulgy workaround on Alpha, where it seems that
		 *  multiplying by 2, 1024 times causes a floating point
		 *  exception. (Triggered by running for example NetBSD/pmax
		 *  2.0 emulated on an Alpha host.)
		 */
		if (exponent == 1024)
			fvp->f = INFINITY;
		else
			while (exponent-- > 0)
				fvp->f *= 2.0;
	} else if (exponent < 0) {
		while (exponent++ < 0)
			fvp->f /= 2.0;
	}

zero_or_no_reasonable_result:
	if (sign)
		fvp->f = -fvp->f;

no_reasonable_result:
	fvp->nan = nan;

#ifdef IEEE_DEBUG
	fatal("nan=%i (f=%f) }\n", nan, fvp->f);
#endif
}


/*
 *  ieee_store_float_value_rm():
 *
 *  Generates a 64-bit IEEE-formated value in a specific format, under a
 *  caller-supplied rounding mode.
 *
 *  #292: the historical entry point below truncates the fraction, which is
 *  bit-exact round-toward-zero -- measured at 0 mismatches against a
 *  round-toward-zero oracle over 2.48 million in-range doubles.  That is
 *  CORRECT for the SH-4 (whose FPSCR resets to round-to-zero) and for
 *  PowerPC stfs (architecturally a bit extraction), but WRONG for MIPS,
 *  whose default mode is round-to-nearest-even: half of all in-range
 *  single-precision stores came out 1 ulp low (measured 310438 of 619333,
 *  always low, never high).
 *
 *  The mode values 0..3 match the encoding MIPS FCSR[1:0], SH FPSCR[1:0]
 *  (which defines only 0 and 1) and PowerPC FPSCR[1:0] all share:
 *  0 nearest-even, 1 toward zero, 2 toward +Inf, 3 toward -Inf.
 *  IEEE_RM_LEGACY reproduces the historical behaviour bit for bit --
 *  truncation, but with #287's overflow-to-Infinity kept as-is -- and is
 *  what every caller that does not pass a mode still gets.
 *
 *  #294: the W and L (integer) formats honour the mode too -- the value is
 *  rounded to an integral per rm and then #273's range guards and the cast
 *  apply unchanged.  The SEPARATION lives in the caller: the MIPS decoder
 *  passes a forced toward-zero mode for trunc.w/trunc.l (architecturally
 *  mode-independent) and defers to FCSR for cvt.*, so honouring rm here
 *  cannot break trunc.  Callers using the two-argument legacy entry point
 *  get LEGACY, under which W/L behaviour is bit-identical to before.
 */
uint64_t ieee_store_float_value_rm(double nf, int fmt, int rm)
{
	int n_frac = 0, n_exp = 0, signofs = 0, i, exponent;
	uint64_t r = 0, r2;
	int64_t r3;

	/*  n_frac and n_exp:  */
	switch (fmt) {
	case IEEE_FMT_S:	n_frac = 23; n_exp = 8; signofs = 31; break;
	case IEEE_FMT_W:	n_frac = 31; n_exp = 0; signofs = 31; break;
	case IEEE_FMT_D:	n_frac = 52; n_exp = 11; signofs = 63; break;
	case IEEE_FMT_L:	n_frac = 63; n_exp = 0; signofs = 63; break;
	default:/*  #279: the missing return is the real defect here.  Without
		    it this default fell out of the switch into the SECOND
		    switch below, whose default printed a second line for the
		    same call -- measured 2.00 host lines per store call.  r is
		    still 0 and the tail below only masks it to 32 bits, so
		    returning here yields exactly what the old path returned.  */
		if (!store_badfmt_warned) {
			store_badfmt_warned = 1;
			fatal("ieee_store_float_value(): unimplemented format"
			    " %i\n", fmt);
		}
		return 0;
	}

	switch (fmt) {
	case IEEE_FMT_W:
	case IEEE_FMT_L:
		/*
		 *  This causes an implicit conversion of double to integer.
		 *  If nf < 0.0, then r2 will begin with a sequence of binary
		 *  1's, which is ok.
		 */

		/*  #294: round to an integral value per the caller's mode
		    FIRST, so #273's range guards below test the value that
		    will actually be cast.  Under RZ and LEGACY nothing is done
		    -- the cast truncates, exactly as before, which a sweep of
		    406,405 boundary-bracketing doubles confirmed bit-identical.

		    The nearest-even tie test compares against the exactly
		    representable midpoint floor(nf) + 0.5 and NOT against a
		    computed difference: nf - floor(nf) can round to exactly
		    0.5 for a value that is not a tie (nextafter(-0.5, 0) is
		    the counterexample -- its true distance is 0.5 + 2^-54).
		    For |nf| < 2^52 the midpoint is exact; at or above 2^52
		    every double is already integral and floor(nf) == nf, so
		    the branch is never entered.  rint()/nearbyint() are
		    forbidden here (they follow the HOST's rounding mode) and
		    llround() rounds ties away from zero, which is wrong.  */
		if (!isnan(nf) &&
		    rm != IEEE_RM_LEGACY && rm != IEEE_RM_RZ) {
			double fl = floor(nf);
			if (nf != fl) {
				switch (rm) {
				case IEEE_RM_RN:
					if (nf > fl + 0.5 ||
					    (nf == fl + 0.5 &&
					    fmod(fl, 2.0) != 0.0))
						fl += 1.0;
					nf = fl;
					break;
				case IEEE_RM_RP:
					nf = fl + 1.0;
					break;
				case IEEE_RM_RM:
					nf = fl;
					break;
				}
			}
		}
		/*  #273: NaN, +/-Inf and out-of-range operands must not reach
		    the cast -- (int64_t) of those is undefined in C, so the
		    guest-visible result would otherwise depend on the build
		    host (x86 yields the integer indefinite 0x8000...0, which
		    the W path below truncates to 0; aarch64 saturates
		    instead). With the Invalid trap disabled, R3010/R4010
		    return the largest positive integer for all five cases,
		    with no sign dependence. W's lower bound is deliberately
		    <= -2147483649.0 and not < -2147483648.0, because
		    trunc(-2147483648.5) is -2147483648, which IS
		    representable; L's is strict, because -2^63 is exactly
		    representable. 2^63 is spelled as a literal on purpose:
		    (double)INT64_MAX rounds UP to 2^63, which would let
		    equality through to the cast.  */
		if (fmt == IEEE_FMT_W) {
			if (isnan(nf) || nf >= 2147483648.0 ||
			    nf <= -2147483649.0)
				r3 = 0x7fffffff;
			else
				r3 = (int64_t) nf;
		} else {
			if (isnan(nf) || nf >= 9223372036854775808.0 ||
			    nf < -9223372036854775808.0)
				r3 = 0x7fffffffffffffffLL;
			else
				r3 = (int64_t) nf;
		}
		r2 = r3;
		r |= r2;
		break;
	case IEEE_FMT_S:
	case IEEE_FMT_D:
		/*  sign bit:  */
		if (signbit(nf)) {
			r |= ((uint64_t)1 << signofs);
		}

		// printf("fpclassify(nf) = %i\n", fpclassify(nf));
		switch (fpclassify(nf)) {
		case FP_INFINITE:
			if (fmt == IEEE_FMT_D)
				r |= 0x7ff0000000000000ULL;
			else
				r |= 0x7f800000ULL;
			break;
		case FP_NAN:
			if (fmt == IEEE_FMT_D)
				r |= 0x7fffffffffffffffULL;
			else
				r |= 0x7fffffffULL;
			break;
		case FP_NORMAL:
			if (signbit(nf))
				nf = -nf;

			/*
			 *  How to convert back from double to exponent + fraction:
			 *  The fraction should be 1.xxx, that is
			 *  1.0 <= fraction < 2.0
			 *
			 *  This method is very slow but should work:
			 *  (TODO: Fix the performance problem!)
			 */
			exponent = 0;
			while (nf < 1.0 && exponent > -1023) {
				nf *= 2.0;
				exponent --;
			}
			while (nf >= 2.0 && exponent < 1023) {
				nf /= 2.0;
				exponent ++;
			}

			/*  Here:   1.0 <= nf < 2.0  */
			nf -= 1.0;	/*  remove implicit first bit  */
			for (i=n_frac-1; i>=0; i--) {
				nf *= 2.0;
				if (nf >= 1.0) {
					r |= ((uint64_t)1 << i);
					nf -= 1.0;
				}
			}

			/*  #292: what remains in nf after the loop is the exact
			    remainder, in units of one ulp of the destination:
			    every step is a multiply by 2 (exact) or a subtraction
			    of 1 from a value in [1,2) (exact by Sterbenz), so
			    nf == 0.5 is a true half-way tie, exactly.  Round the
			    assembled word as a UNIT -- the carry must be allowed
			    to run out of the fraction into the exponent, or
			    2 - 2^-24 would wrap to 1.0 instead of rounding to
			    2.0.  For D the remainder is always exactly 0 (a host
			    double has exactly the 52 bits D wants), so every mode
			    is a no-op there and D results cannot change.  */
			if (rm != IEEE_RM_LEGACY && rm != IEEE_RM_RZ &&
			    nf > 0.0) {
				int negative = (r >> signofs) & 1;
				int round_up = 0;
				switch (rm) {
				case IEEE_RM_RN:
					round_up = nf > 0.5 ||
					    (nf == 0.5 && (r & 1));
					break;
				case IEEE_RM_RP:
					round_up = !negative;
					break;
				case IEEE_RM_RM:
					round_up = negative;
					break;
				}
				if (round_up) {
					uint64_t fracmask =
					    (((uint64_t)1 << n_frac) - 1);
					uint64_t frac = (r & fracmask) + 1;
					if (frac >> n_frac) {
						frac = 0;
						exponent ++;
					}
					r = (r & ~fracmask) | frac;
				}
			}

			/*  Insert the exponent into the resulting word:  */
			/*  (First bias, then make sure it's within range)  */
			exponent += (((uint64_t)1 << (n_exp-1)) - 1);
			if (exponent < 0)
				exponent = 0;
			if (exponent >= ((int64_t)1 << n_exp))
				exponent = ((int64_t)1 << n_exp) - 1;

			/*  #287: an all-ones exponent means the value overflowed
			    the DESTINATION format, and the fraction assembled
			    above has to go: exponent-max with a nonzero fraction
			    is a NaN, and mostly a SIGNALING one, where hardware
			    gives +/-Inf (1e300 stored as 0x7fbf21e4). #255 cannot
			    catch it because that gates on the class of the host
			    double, which is merely FP_NORMAL. Test the biased
			    exponent and NOT the clamp above: |x| in [2^128, 2^129)
			    reaches 255 with no clamping at all, so a clamp-scoped
			    fix would leave that whole binade storing NaNs.

			    #292: overflow is MODE-DEPENDENT (IEEE 754 s7.4).
			    Nearest carries to Infinity; toward-zero stops at the
			    largest finite value; the directed modes give Infinity
			    on the side they round toward and the largest finite
			    value on the other.  IEEE_RM_LEGACY keeps #287's
			    unconditional Infinity so the historical entry point
			    is bit-identical.  */
			if (exponent == ((int64_t)1 << n_exp) - 1) {
				int to_inf = 1;
				int negative = (r >> signofs) & 1;
				switch (rm) {
				case IEEE_RM_RZ:
					to_inf = 0;
					break;
				case IEEE_RM_RP:
					to_inf = !negative;
					break;
				case IEEE_RM_RM:
					to_inf = negative;
					break;
				}
				if (to_inf)
					r &= (uint64_t)1 << signofs;
				else {
					exponent = ((int64_t)1 << n_exp) - 2;
					r = (r & ((uint64_t)1 << signofs)) |
					    (((uint64_t)1 << n_frac) - 1);
				}
			}
			r |= (uint64_t)exponent << n_frac;

			/*  #287: exponent 0 here is UNDERFLOW, never 0.0 -- that
			    has its own FP_ZERO arm -- so flush to zero but keep
			    the sign set at the top of this arm, as the
			    FP_SUBNORMAL arm below already does (-1e-40 stored as
			    +0). Both arms are unreachable for D, whose finite
			    exponents bias into 1..2046.

			    #292: the flush-to-zero semantics are kept for every
			    mode -- MIPS routes non-flush denormal results away
			    before this store (#246), and SH FPSCR.DN flushes in
			    hardware.  The one rounding interaction that matters
			    is handled above: a fraction carry can lift biased
			    exponent 0 to 1, which is exactly FLT_MIN, the correct
			    nearest result for values just under 2^-126.  */
			if (exponent == 0)
				r &= (uint64_t)1 << signofs;
			break;
		case FP_SUBNORMAL:
			// TODO
			break;
		case FP_ZERO:
			// r already has zeros in the lowest bits. Done.
			break;
		}
		break;
	default:/*  TODO  */
		/*  #279: unreachable now that the default above returns, but
		    kept -- and latched with the same flag, so the invariant
		    holds if that return is ever removed again.  */
		if (!store_badfmt_warned) {
			store_badfmt_warned = 1;
			fatal("ieee_store_float_value(): unimplemented format"
			    " %i\n", fmt);
		}
	}

	if (fmt == IEEE_FMT_S || fmt == IEEE_FMT_W)
		r = (uint32_t) r;

	return r;
}


/*
 *  ieee_store_float_value():
 *
 *  The historical entry point.  #292: now a wrapper that selects
 *  IEEE_RM_LEGACY -- truncation (bit-exact round-toward-zero) with #287's
 *  overflow-to-Infinity -- so all 24 pre-existing single-precision call
 *  sites, and every double-precision one, keep their behaviour bit for
 *  bit.  The offline regression gate compares this entry point against
 *  unmodified upstream over 20 million inputs, so any deviation the
 *  wrapper introduced would show up there as an unexplained difference.
 */
uint64_t ieee_store_float_value(double nf, int fmt)
{
	return ieee_store_float_value_rm(nf, fmt, IEEE_RM_LEGACY);
}


/*
 *  ieee_sum_round_to_odd():
 *
 *  #299: the sum of two doubles, rounded to ODD instead of to nearest, so
 *  that a single-precision store of the result rounds CORRECTLY in every
 *  mode.  This kills the double-rounding band that gates 10 and 11 pin:
 *  computing a single-precision add in host double first rounds to 53
 *  bits (host nearest), then the store rounds to 24 -- and a residue
 *  finer than the double grid is gone before the store can see it, so
 *  1.0 + 2^-60 under toward-+Inf stored 1.0 where hardware's sticky bit
 *  rounds up, and an fmac tie-band input rounded to the WRONG side under
 *  plain nearest (measured: (0x3fc00003 * 0x33fffffc) + 1.0 gave
 *  0x3f800002 where nearest owes 0x3f800001).
 *
 *  Boldo-Melquiond: if the wide format has at least 2p+2 bits of the
 *  narrow one (53 >= 2*24+2), then round-to-odd in the wide format
 *  followed by ANY rounding to the narrow format equals the direct
 *  rounding of the exact value.  Round-to-odd of an exact sum is
 *  computable without wider arithmetic: s = a + b under host nearest,
 *  plus Knuth's 2Sum error term e (EXACT for any two doubles, six flops,
 *  no magnitude precondition -- the three-flop Fast2Sum needs |a| >= |b|
 *  and an earlier draft of this round shipped a broken hybrid of the
 *  two, refuted by every panel seat).  If e is nonzero the sum was
 *  inexact: force the result to the neighbouring double with ODD
 *  mantissa, stepping TOWARD e's sign when the lsb is even.  A plain
 *  |= 1 on the bit pattern is wrong -- it always steps away from zero,
 *  regardless of which side the exact value is on (also a panel find).
 *
 *  The intermediates cannot overflow or hit subnormals for single
 *  operands (|sum| < 2^129 and either exact or >= 2^-149-ish), which is
 *  precisely why this helper is SAFE for the single-precision arms and
 *  must NOT be reused as-is for double arithmetic -- that is the next
 *  round's fma-residual work, with mandatory overflow and subnormal
 *  handling this function deliberately does not have.
 *
 *  The rm parameter exists for ONE case round-to-odd cannot express:
 *  IEEE 754 gives x + (-x) the sign of the MODE -- +0 everywhere except
 *  toward-minus-infinity, where it is -0.  The host computes +0 under
 *  nearest, so under IEEE_RM_RM an exact zero sum from nonzero-or-
 *  opposite-signed operands is flipped to -0 here.  (+0) + (+0) stays
 *  +0 in every mode and is excluded.
 */
/*
 *  #300: directed rounding for DOUBLE-format arithmetic.
 *
 *  The D-format store is a pure re-encode -- a host double already has
 *  exactly the 52 fraction bits D wants -- so a rounding mode can only be
 *  honoured by correcting the ARITHMETIC, not the store. The host computes
 *  under round-to-nearest; these helpers recover which side of the exact
 *  result that landed on, using one fma residual (div: r = q*b - a exact by
 *  the Markstein lemma; sqrt: r = q*q - a; mul: r = a*b - p, the exact
 *  product error) or Knuth's 2Sum (add/sub), and step one ulp when the
 *  directed mode owes the other neighbour.
 *
 *  The overshoot sign convention FLIPS with the result's sign, per op --
 *  the feasibility panel predicted someone would ship it inconsistent, and
 *  the offline model sweep caught exactly that in this round's first mul
 *  draft (30114 mismatches in 160000; the div form was right because it
 *  tests against sign(a)). Every branch below is a transliteration of a
 *  Python model verified against exact rational oracles: 80000 div,
 *  160000 mul/add, 15000 sqrt cross-checks at zero mismatches, plus named
 *  rows for every overflow arm and the tiny band.
 *
 *  MANDATORY edges (the panel pre-refused a version without them):
 *  - overflow: the RN result is +/-Inf, fma on it would be NaN. Directed
 *    modes owe by mode-and-sign: RZ clamps to +/-DBL_MAX; RP gives +Inf
 *    but clamps the negative side; RM mirrors.
 *  - the accepted-nearest bands, all pinned in the offline gate. For div
 *    and sqrt the RESIDUAL's scale is set by the OPERAND (dividend or
 *    radicand), so those accept the nearest answer when that operand is
 *    below 2^-1018: the residual would underflow beneath the subnormal
 *    quantum and read as a false "exact" (two panel seats' witnesses,
 *    including one with a NORMAL result from a subnormal dividend). For
 *    mul the band is on the PRODUCT below the same threshold. Add needs
 *    no band: a nearest sum's error is exactly representable down
 *    through gradual underflow. Above the bands the correction is live
 *    INCLUDING subnormal results -- the directed step works on the
 *    sign-magnitude pattern down to and across zero, so a positive-tiny
 *    quotient under toward-+Inf correctly yields 2^-1074 stepped from
 *    the +0 pattern. Divide-by-zero infinity is EXACT and mode
 *    independent, and is explicitly excluded from the overflow clamp
 *    (a panel seat caught 1.0/+0.0 under toward-zero clamping to
 *    DBL_MAX).
 *  - non-finite operands or results pass through UNTOUCHED (the #299
 *    lesson, made structural: every entry checks isfinite first).
 */

/*  #300 panel, two passes. First: the RESULT-only band was a hole -- a
    subnormal DIVIDEND (or sqrt input) yields a normal result whose
    residual lives at the OPERAND's scale, underflows beneath the
    subnormal quantum, and reads as a false "exact" (a seat filed both
    witnesses with full traces). Second, and deeper: the first repair
    guarded at 2^-1018 from a TYPICAL-MAGNITUDE argument (~2^-53 * |a|),
    and another seat proved the correct precondition is the residual's
    QUANTUM -- a - q*b is a multiple of 2^(eq+eb-104), representable iff
    that quantum >= 2^-1074, i.e. dividend/radicand/product >= ~2^-969.
    In the 48 binades between the two bounds it CONSTRUCTED all-normal
    witnesses (significands chosen so the residual is a lone bit at
    2^-1104) that a random sweep structurally cannot hit: the tail's
    probability is ~2^-51 per draw, which is why 264000 sweep checks and
    28 gate vectors stayed green over the hole. The witnesses are named
    vectors in the offline gate now, with boundary controls at 2^-960
    proving the corrected side. The same seat showed the deleted
    result-band had been PROTECTING mul, so mul's band is the product
    below the same 2^-969 threshold.  */
#define	IEEE_DIR_OPTINY	0x1p-969

/*  overflow result by mode and sign; q is +/-Inf from finite operands  */
static double ieee_dir_overflow(double q, int rm)
{
	int neg = (q < 0.0);
	switch (rm) {
	case IEEE_RM_RZ:
		return neg ? -DBL_MAX : DBL_MAX;
	case IEEE_RM_RP:
		return neg ? -DBL_MAX : q;
	case IEEE_RM_RM:
		return neg ? q : DBL_MAX;
	}
	return q;
}

/*  one-ulp step on the sign-magnitude pattern; q finite nonzero  */
static double ieee_dir_step(double q, int toward_zero)
{
	uint64_t b;
	memcpy(&b, &q, sizeof(b));
	if (toward_zero)
		b--;
	else
		b++;
	/*  the magnitude bits carry correctly through binades in both
	    directions because sign never changes within these calls  */
	memcpy(&q, &b, sizeof(q));
	return q;
}

/*  adjust the RN result q for a directed mode, given magnitude-overshoot  */
static double ieee_dir_adjust(double q, int overshoot, int rm)
{
	/*  signbit, not < 0.0: a zero result still steps (a positive-tiny
	    quotient under toward-+Inf owes 2^-1074, stepped from the +0 bit
	    pattern), and -0.0 < 0.0 is false -- a comparison-derived sign
	    would step -0 the wrong way (a panel seat's find).  */
	int qneg = signbit(q) != 0;

	switch (rm) {
	case IEEE_RM_RZ:
		return overshoot ? ieee_dir_step(q, 1) : q;
	case IEEE_RM_RP:
		if (qneg)
			return overshoot ? ieee_dir_step(q, 1) : q;
		return overshoot ? q : ieee_dir_step(q, 0);
	case IEEE_RM_RM:
		if (qneg)
			return overshoot ? q : ieee_dir_step(q, 0);
		return overshoot ? ieee_dir_step(q, 1) : q;
	}
	return q;
}

double ieee_div_round_rm(double a, double b, int rm)
{
	double q = a / b;
	double r;

	if (rm == IEEE_RM_RN || rm == IEEE_RM_LEGACY)
		return q;
	if (!isfinite(q)) {
		/*  divide-by-zero is EXACT infinity, independent of the mode
		    -- it must not fall into the overflow clamp (a panel seat
		    caught 1.0/+0.0 under toward-zero returning DBL_MAX).  */
		if (isinf(q) && isfinite(a) && isfinite(b) && b != 0.0)
			return ieee_dir_overflow(q, rm);
		return q;
	}
	if (fabs(a) < IEEE_DIR_OPTINY)
		return q;
	r = fma(q, b, -a);
	if (r == 0.0)
		return q;
	/*  q overshot |exact| iff sign(r) == sign(a)  (r = q*b - a)  */
	return ieee_dir_adjust(q, (r > 0.0) == (a > 0.0), rm);
}

double ieee_mul_round_rm(double a, double b, int rm)
{
	double p = a * b;
	double r;

	if (rm == IEEE_RM_RN || rm == IEEE_RM_LEGACY)
		return p;
	if (!isfinite(p)) {
		if (isinf(p) && isfinite(a) && isfinite(b))
			return ieee_dir_overflow(p, rm);
		return p;
	}
	/*  a subnormal PRODUCT's residual is finer than the subnormal
	    quantum (r <= ulp(p)/2 < 2^-1074), so the accepted-nearest band
	    for mul is the result below the same 2^-1018 threshold.  */
	if (p == 0.0 || fabs(p) < IEEE_DIR_OPTINY)
		return p;
	r = fma(a, b, -p);	/*  the EXACT product error: exact = p + r  */
	if (r == 0.0)
		return p;
	/*  p overshot |exact| iff the error points back toward zero: p > 0
	    needs r < 0, p < 0 needs r > 0 -- the sign-flip the model sweep
	    caught  */
	return ieee_dir_adjust(p, (r > 0.0) != (p > 0.0), rm);
}

double ieee_sqrt_round_rm(double a, int rm)
{
	double q = sqrt(a);
	double r;

	if (rm == IEEE_RM_RN || rm == IEEE_RM_LEGACY)
		return q;
	if (!isfinite(q) || q == 0.0 || a < IEEE_DIR_OPTINY)
		return q;
	r = fma(q, q, -a);
	if (r == 0.0)
		return q;
	/*  q*q > a means q overshot; a sqrt result is never negative  */
	return ieee_dir_adjust(q, r > 0.0, rm);
}

double ieee_add_round_rm(double a, double b, int rm)
{
	double s = a + b;
	double bb, e;

	if (rm == IEEE_RM_RN || rm == IEEE_RM_LEGACY)
		return s;
	if (!isfinite(s)) {
		if (isinf(s) && isfinite(a) && isfinite(b))
			return ieee_dir_overflow(s, rm);
		return s;
	}
	bb = s - a;
	e = (a - (s - bb)) + (b - bb);	/*  Knuth 2Sum: exact = s + e  */
	if (!isfinite(e)) {
		/*  2Sum's INTERMEDIATE can overflow even when s is finite:
		    at the very overflow-tie threshold (a = 3*2^970 plus
		    -DBL_MAX gives a finite tie-to-even s while s - a is
		    -Inf), e becomes NaN -- and a NaN overshoot flag does not
		    merely miss the step, under toward-minus-Inf it stepped
		    AWAY from the exact value (a panel seat's witness,
		    anti-correction measured). Accept the nearest answer for
		    this one exclusion; the family is pinned offline.  */
		return s;
	}
	if (e == 0.0) {
		/*  IEEE: x + (-x) is -0 only toward minus infinity  */
		if (s == 0.0 && rm == IEEE_RM_RM && !signbit(s) &&
		    !(a == 0.0 && b == 0.0 && !signbit(a) && !signbit(b)))
			return -0.0;
		return s;
	}
	/*  s overshot |exact| iff e points back toward zero relative to s  */
	return ieee_dir_adjust(s, (s >= 0.0) ? (e < 0.0) : (e > 0.0), rm);
}


double ieee_sum_round_to_odd(double a, double b, int rm)
{
	double s = a + b;
	double bb = s - a;
	double e = (a - (s - bb)) + (b - bb);	/*  Knuth 2Sum  */

	/*  isfinite(s) is LOAD-BEARING, not defensive. With a NaN or Inf
	    operand the 2Sum error e is NaN, and NaN != 0.0 is TRUE in C --
	    the first version of this function claimed the opposite and let
	    Inf into the odd-force, where +Inf's even-lsb bit pattern was
	    stepped DOWN: +Inf + 1.0 became DBL_MAX (stored 0x7f7fffff under
	    toward-zero) and -Inf - 1.0 became a NEGATIVE NaN. Two panel
	    seats refuted the claim independently, one noting that
	    fsub.sds's first operand is a full double, so Inf is directly
	    reachable there; the offline gate reproduced both corruptions
	    before this guard existed and pins them now. For finite s from
	    these call sites, s == 0 with e != 0 is impossible: every
	    operand is a single (or an exact 48-bit product, or sds's
	    double) whose nonzero sums are bounded away from the double
	    underflow threshold -- a seat proved the 2^-298 quantum floor.  */
	if (isfinite(s) && e != 0.0) {
		uint64_t sb;
		memcpy(&sb, &s, sizeof(sb));
		if (!(sb & 1)) {
			/*  Step toward e's sign. On the sign-magnitude bit
			    pattern, toward +Inf is bits+1 for positive s and
			    bits-1 for negative s; toward -Inf the reverse.
			    s cannot be zero here: 2Sum's error is zero
			    whenever the sum is exactly representable, and
			    an exact sum of zero certainly is.  */
			int upward = (e > 0.0);
			int negative = (sb >> 63) != 0;
			if (upward != negative)
				sb++;
			else
				sb--;
			memcpy(&s, &sb, sizeof(sb));
		}
	} else if (s == 0.0 && rm == IEEE_RM_RM && !signbit(s) &&
	    !(a == 0.0 && b == 0.0 && !signbit(a) && !signbit(b))) {
		/*  exact zero from cancellation (or (+0)+(-0)): -0 under
		    toward-minus-infinity  */
		s = -0.0;
	}

	return s;
}

