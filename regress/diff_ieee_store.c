/*
 *  Offline differential of ieee_store_float_value(), upstream against SHIPPED (#287).
 *
 *  IMPORTANT -- what is under test here. The "new" side is the REAL
 *  src/core/float_emul.c, compiled and linked into this driver by gate_offline.sh, which
 *  first proves that file is byte-identical to the committed one. The "old" side is
 *  store_old() below, a transcription of the pre-#287 upstream arm -- that code no longer
 *  exists in the tree, so it has to be carried here.
 *
 *  The first version of this gate transcribed BOTH sides and differentialled the copy
 *  against itself. It never compiled, linked or executed float_emul.c at all, so deleting
 *  #287 from the shipped source left the gate green. That is the same defect as the
 *  20-machine smoke this harness retired, one level of indirection further back, and it
 *  was caught in review rather than by the gate.
 *
 *  Why offline at all: the function is pure, so it can be exercised over tens of millions
 *  of inputs in seconds with no emulator in the loop. The boot test it replaced executed
 *  no FP store whatsoever.
 *
 *  The gate asserts a CLOSED FORM for the change-set, which is what makes an intended
 *  correction distinguishable from a regression. It is an EQUIVALENCE, checked in both
 *  directions, and the two extra predicates are not decoration -- each excludes a real
 *  class of input where the two implementations legitimately agree:
 *
 *      old(x) != new(x)  <=>  (isnormal(x) && |x| >= 2^128 && frac23(x) != 0)
 *                         ||  (isnormal(x) && 0 < |x| < 2^-126 && signbit(x))
 *
 *  and for IEEE_FMT_D the change-set must be EMPTY.
 *
 *  Why each direction is needed:
 *
 *    CONTAINMENT  (=>)  no difference may appear outside those classes. Catches a change
 *                       that perturbs ordinary in-range arithmetic.
 *    COMPLETENESS (<=)  every input inside those classes MUST differ. Without it the gate
 *                       only proves "the differences I saw were allowed", which a mutant
 *                       that fixes overflow for negative values but not positive ones
 *                       satisfies perfectly: overflow and underflow classes are both
 *                       non-empty, nothing is unexplained, and every positive overflow is
 *                       still broken.
 *
 *  The two exclusions, both measured rather than reasoned about:
 *
 *    "frac23(x) != 0"      the function TRUNCATES the fraction to 23 bits, so any double
 *                          whose leading 23 fraction bits are zero assembles an all-zero
 *                          mantissa and #287's clear is a no-op -- both versions encode
 *                          +/-Inf. Stating this as "not an exact power of two" is too
 *                          narrow, and the gate produced the counter-example itself:
 *                          -1.1960164410049153e+198 stores as ff800000 under both.
 *    "isnormal"            a host double below 2^-1022 takes the FP_SUBNORMAL arm, where
 *                          both versions return signed zero, even though it satisfies
 *                          0 < |x| < 2^-126 && signbit(x).
 *
 *  It also checks ABSOLUTE answers, not only agreement. A purely relative differential
 *  passes when both sides are wrong the same way; the absolute table pins the values that
 *  #287 exists to produce (+/-Inf on overflow, signed zero on underflow).
 *
 *  Two thresholds sit close together here and were once conflated in a review brief. They
 *  are NOT the same number, and both are measured rather than asserted:
 *
 *      exp255-at  2^128   the stored exponent field reaches 255 (bias 127, so e >= 128).
 *                         This governs the change-set, because #287 clears the mantissa
 *                         whenever the exponent is 255.
 *      clamp-at   2^129   the statement `if (exponent >= 256) exponent = 255` actually
 *                         fires. Values in [2^128, 2^129) reach 255 WITHOUT the clamp,
 *                         which is why the old code emitted Inf-with-garbage-mantissa
 *                         there and the bug was never merely a clamping oversight.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdarg.h>
#include <math.h>
#include <string.h>

#include "float_emul.h"		/*  the REAL ieee_store_float_value()  */

/*
 *  float_emul.c's only external dependency. Kept quiet: the reserved-format arms call it
 *  deliberately and a 20-million-sample sweep would otherwise bury the results.
 */
void fatal(const char *fmt, ...)
{
	(void) fmt;
}

/*
 *  Transcription of the UPSTREAM (pre-#287) S/D arm, from 39748e3. `clamped` and `exp255`
 *  report which threshold the OLD code crossed, so the two can be located empirically.
 */
static uint64_t store_old(double nf, int fmt, int *clamped, int *exp255)
{
	int n_frac = 0, n_exp = 0, signofs = 0, i, exponent;
	uint64_t r = 0;

	if (clamped != NULL) *clamped = 0;
	if (exp255  != NULL) *exp255  = 0;

	switch (fmt) {
	case IEEE_FMT_S: n_frac = 23; n_exp = 8;  signofs = 31; break;
	case IEEE_FMT_D: n_frac = 52; n_exp = 11; signofs = 63; break;
	default: return 0;
	}

	if (signbit(nf))
		r |= ((uint64_t)1 << signofs);

	switch (fpclassify(nf)) {
	case FP_INFINITE:
		r |= (fmt == IEEE_FMT_D) ? 0x7ff0000000000000ULL : 0x7f800000ULL;
		break;
	case FP_NAN:
		r |= (fmt == IEEE_FMT_D) ? 0x7fffffffffffffffULL : 0x7fffffffULL;
		break;
	case FP_NORMAL:
		if (signbit(nf))
			nf = -nf;
		exponent = 0;
		while (nf < 1.0 && exponent > -1023) { nf *= 2.0; exponent--; }
		while (nf >= 2.0 && exponent < 1023) { nf /= 2.0; exponent++; }
		nf -= 1.0;
		for (i = n_frac - 1; i >= 0; i--) {
			nf *= 2.0;
			if (nf >= 1.0) { r |= ((uint64_t)1 << i); nf -= 1.0; }
		}
		exponent += (((uint64_t)1 << (n_exp - 1)) - 1);
		if (exponent < 0)
			exponent = 0;
		if (exponent >= ((int64_t)1 << n_exp)) {
			if (clamped != NULL) *clamped = 1;
			exponent = ((int64_t)1 << n_exp) - 1;
		}
		if (exponent == ((int64_t)1 << n_exp) - 1 && exp255 != NULL)
			*exp255 = 1;

		r |= (uint64_t)exponent << n_frac;
		if (exponent == 0)
			r = 0;
		break;
	case FP_SUBNORMAL:
		break;
	case FP_ZERO:
		break;
	}

	/*  the real function's trailing narrowing, carried for exactness  */
	if (fmt == IEEE_FMT_S || fmt == IEEE_FMT_W)
		r = (uint32_t) r;
	return r;
}

static uint64_t rng_s = 0x243f6a8885a308d3ULL;
static uint64_t rnd(void)
{
	rng_s ^= rng_s << 13; rng_s ^= rng_s >> 7; rng_s ^= rng_s << 17;
	return rng_s;
}

/*
 *  Smallest binade at which `probe` first reports true, as an exponent.
 *
 *  The probe value is 1.5 * 2^e and NOT 2^e, which matters and was got wrong once. At an
 *  exact power of two the assembled fraction is all zeros, so the old and new arms agree
 *  even at 2^128 -- both produce 0x7f800000 -- and a sweep over exact powers reports "no
 *  difference anywhere". 1.5 carries a nonzero mantissa, which is the case #287 actually
 *  changes. It also normalises to the same exponent (1.5 is already in [1,2)), so the
 *  clamp and exponent-255 thresholds it reports are unchanged.
 */
static int first_binade(int (*probe)(double))
{
	int e;
	for (e = -200; e <= 1023; e++)
		if (probe(ldexp(1.5, e)))
			return e;
	return 9999;
}

static int p_clamped(double x) { int c, s; store_old(x, IEEE_FMT_S, &c, &s); return c; }
static int p_exp255(double x)  { int c, s; store_old(x, IEEE_FMT_S, &c, &s); return s; }

/*  First power of two where the SHIPPED function departs from upstream.  */
static int p_differs(double x)
{
	return store_old(x, IEEE_FMT_S, NULL, NULL) !=
	    ieee_store_float_value(x, IEEE_FMT_S);
}

struct abs_case { double v; int fmt; uint64_t want; const char *name; };

/*
 *  Does the S-format fraction assemble to all zeros?
 *
 *  #287 clears the mantissa when the exponent is 255. If the mantissa was already zero
 *  the correction is a no-op there and the two implementations legitimately agree, so
 *  such inputs must be excluded from the completeness requirement.
 *
 *  The obvious predicate -- "x is an exact power of two" -- is TOO NARROW, and the gate
 *  found the counter-example itself: -1.1960164410049153e+198 stores as ff800000 under
 *  both versions and is not a power of two. The real condition follows from how the
 *  function builds the fraction: it TRUNCATES to 23 bits. Any double whose leading 23
 *  fraction bits are zero -- with however many nonzero bits below them -- assembles the
 *  same all-zero mantissa. Exact powers of two are just the special case.
 */
static int frac23_is_zero(double x)
{
	int e;
	double m = frexp(fabs(x), &e) * 2.0;	/*  m in [1,2)  */
	return floor((m - 1.0) * 8388608.0) == 0.0;	/*  2^23  */
}

/*  The COMPLETENESS side: inputs that MUST differ between the two implementations.  */
static int must_differ(double x)
{
	const double TWO128   = 340282366920938463463374607431768211456.0;
	const double TWO_M126 = 1.1754943508222875e-38;

	if (fpclassify(x) != FP_NORMAL)
		return 0;
	if (fabs(x) >= TWO128 && !frac23_is_zero(x))
		return 1;			/*  overflow: mantissa must be cleared  */
	if (fabs(x) > 0.0 && fabs(x) < TWO_M126 && signbit(x))
		return 1;			/*  underflow: sign must be kept  */
	return 0;
}

int main(void)
{
	const double TWO128   = 340282366920938463463374607431768211456.0;
	const double TWO_M126 = 1.1754943508222875e-38;
	long long n = 0, dS = 0, dD = 0, unexplained = 0, ovf = 0, und = 0;
	long long inrange_diff = 0;
	long long should_differ = 0, missed = 0;
	int i, e_clamp, e_255, e_diff, abs_bad = 0;

	/*
	 *  0. ABSOLUTE answers from the real function. A differential alone is relative:
	 *     it passes when both sides are wrong in the same way. These pin the values
	 *     #287 exists to produce.
	 */
	struct abs_case cases[] = {
	    { 1.0,    IEEE_FMT_S, 0x3f800000ULL,         "1.0 -> S" },
	    { -2.0,   IEEE_FMT_S, 0xc0000000ULL,         "-2.0 -> S" },
	    { 1e300,  IEEE_FMT_S, 0x7f800000ULL,         "1e300 -> S is +Inf" },
	    { -1e300, IEEE_FMT_S, 0xff800000ULL,         "-1e300 -> S is -Inf" },
	    { -1e-40, IEEE_FMT_S, 0x80000000ULL,         "-1e-40 -> S is -0" },
	    { 1e-40,  IEEE_FMT_S, 0x00000000ULL,         "1e-40 -> S is +0" },
	    { -2.0,   IEEE_FMT_D, 0xc000000000000000ULL, "-2.0 -> D" },
	    { 1e300,  IEEE_FMT_D, 0x7e37e43c8800759cULL, "1e300 -> D is finite" },
	};
	for (i = 0; i < (int)(sizeof(cases)/sizeof(cases[0])); i++) {
		uint64_t got = ieee_store_float_value(cases[i].v, cases[i].fmt);
		if (got != cases[i].want) {
			abs_bad++;
			printf("  ABSOLUTE MISMATCH %-22s got 0x%016llx want 0x%016llx\n",
			    cases[i].name, (unsigned long long)got,
			    (unsigned long long)cases[i].want);
		}
	}
	printf("absolute-answer cases         : %d\n",
	    (int)(sizeof(cases)/sizeof(cases[0])));
	printf("absolute-answer failures      : %d\n", abs_bad);

	/*  Locate the thresholds empirically rather than asserting them.  */
	e_clamp = first_binade(p_clamped);
	e_255   = first_binade(p_exp255);
	e_diff  = first_binade(p_differs);
	printf("clamp-at                      : 2^%d\n", e_clamp);
	printf("exp255-at                     : 2^%d\n", e_255);
	printf("first-difference-at           : 2^%d\n", e_diff);

	/*  1. structured sweep straddling the S overflow boundary  */
	for (i = -4000; i <= 4000; i++) {
		double x = ldexp(1.0, 128) * (1.0 + i * 1e-4);
		double v[2]; int k;
		v[0] = x; v[1] = -x;
		for (k = 0; k < 2; k++) {
			uint64_t a = store_old(v[k], IEEE_FMT_S, NULL, NULL);
			uint64_t b = ieee_store_float_value(v[k], IEEE_FMT_S);
			n++;
			if (a != b) { dS++;
				if (isfinite(v[k]) && fabs(v[k]) >= TWO128) ovf++;
				else if (fabs(v[k]) > 0 && fabs(v[k]) < TWO_M126 && signbit(v[k])) und++;
				else { unexplained++;
					if (unexplained < 5)
						printf("  UNEXPLAINED %.17g: %08llx -> %08llx\n",
						    v[k], (unsigned long long)a, (unsigned long long)b);
				}
			}
			if (must_differ(v[k])) {
				should_differ++;
				if (a == b) { missed++;
					if (missed < 5)
						printf("  MISSED (should have differed) %.17g: %08llx\n",
						    v[k], (unsigned long long)a);
				}
			}
		}
	}

	/*  2. random doubles, full bit-pattern population  */
	for (i = 0; i < 20000000; i++) {
		uint64_t bits = rnd();
		double x; memcpy(&x, &bits, 8);
		uint64_t a, b;

		a = store_old(x, IEEE_FMT_S, NULL, NULL);
		b = ieee_store_float_value(x, IEEE_FMT_S);
		n++;
		if (a != b) {
			dS++;
			if (isfinite(x) && fabs(x) >= TWO128) ovf++;
			else if (fabs(x) > 0 && fabs(x) < TWO_M126 && signbit(x)) und++;
			else { unexplained++;
				if (unexplained < 5)
					printf("  UNEXPLAINED %.17g: %08llx -> %08llx\n",
					    x, (unsigned long long)a, (unsigned long long)b);
			}
		}
		/*  in-range S values must NEVER move  */
		if (isfinite(x) && fabs(x) < TWO128 && fabs(x) >= TWO_M126 && a != b)
			inrange_diff++;

		/*  COMPLETENESS: values inside the predicted classes must ALL move  */
		if (must_differ(x)) {
			should_differ++;
			if (a == b) { missed++;
				if (missed < 5)
					printf("  MISSED (should have differed) %.17g: %08llx\n",
					    x, (unsigned long long)a);
			}
		}

		/*  D format: the change-set must be EMPTY  */
		a = store_old(x, IEEE_FMT_D, NULL, NULL);
		b = ieee_store_float_value(x, IEEE_FMT_D);
		if (a != b) {
			dD++;
			if (dD < 5)
				printf("  D DIFFERS %.17g: %016llx -> %016llx\n",
				    x, (unsigned long long)a, (unsigned long long)b);
		}
	}

	printf("samples                       : %lld\n", n);
	printf("S-format differences          : %lld\n", dS);
	printf("  of which overflow |x|>=2^128: %lld\n", ovf);
	printf("  of which negative underflow : %lld\n", und);
	printf("UNEXPLAINED                   : %lld\n", unexplained);
	printf("in-range S diffs              : %lld\n", inrange_diff);
	printf("D-format diffs                : %lld\n", dD);
	printf("must-differ population        : %lld\n", should_differ);
	printf("MISSED                        : %lld\n", missed);

	if (abs_bad == 0 && unexplained == 0 && missed == 0 && should_differ > 0 &&
	    inrange_diff == 0 && dD == 0 && dS > 0 &&
	    e_clamp == 129 && e_255 == 128 && e_diff == 128)
		printf("DIFF_PASS -- change-set is exactly the two predicted classes.\n");
	else
		printf("DIFF_FAIL\n");
	return 0;
}
