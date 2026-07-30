#ifndef	FLOAT_EMUL_H
#define	FLOAT_EMUL_H

/*
 *  Copyright (C) 2005-2018  Anders Gavare.  All rights reserved.
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
 *  Floating point emulation. See src/float_emul.c for the details.
 */

#include <math.h>

#include "misc.h"

struct ieee_float_value {
	double		f;
	int		nan;
};

#define	IEEE_FMT_S		1	/*  single, 32-bit float  */
#define	IEEE_FMT_D		2	/*  double, 64-bit float  */
#define	IEEE_FMT_W		3	/*  word, 32-bit integer  */
#define	IEEE_FMT_L		4	/*  long, 64-bit integer  */

/*  #292: rounding modes for ieee_store_float_value_rm().  0..3 match the
    encoding MIPS FCSR[1:0], SH FPSCR[1:0] and PowerPC FPSCR[1:0] share, so
    a caller can pass its status-register field through directly.  LEGACY
    reproduces the historical behaviour bit for bit (truncation, with
    #287's overflow-to-Infinity) and is what the two-argument entry point
    uses.  #294: the W/L integer formats honour the mode as well; the
    caller is responsible for forcing toward-zero for trunc-style
    instructions (the MIPS decoder does).  */
#define	IEEE_RM_RN		0	/*  to nearest, ties to even  */
#define	IEEE_RM_RZ		1	/*  toward zero  */
#define	IEEE_RM_RP		2	/*  toward +Inf  */
#define	IEEE_RM_RM		3	/*  toward -Inf  */
#define	IEEE_RM_LEGACY		4	/*  truncate; overflow to Inf  */

void ieee_interpret_float_value(uint64_t x, struct ieee_float_value *fvp, int fmt);
uint64_t ieee_store_float_value(double nf, int fmt);
uint64_t ieee_store_float_value_rm(double nf, int fmt, int rm);

/*  #299: exact sum of two doubles, rounded to ODD, so that a subsequent
    SINGLE-precision store rounds correctly in every mode (Boldo-Melquiond,
    53 >= 2*24+2). For the single-precision add/sub/fmac arms ONLY -- the
    intermediates are then overflow- and subnormal-free by construction.
    rm is consulted for one case round-to-odd cannot express: the sign of
    an exact zero under toward-minus-infinity.  */
double ieee_sum_round_to_odd(double a, double b, int rm);

/*  #300: DOUBLE-format arithmetic under a directed rounding mode. The D
    store is a pure re-encode, so the mode is honoured by correcting the
    arithmetic: one fma residual (or 2Sum) recovers which neighbour the
    host's nearest-mode result landed on. RN and LEGACY return the plain
    host result; non-finite operands and results pass through untouched;
    the |result| < 2^-900 band deliberately accepts the nearest answer
    (residual lemmas are proven for normals only) and is pinned in the
    offline gate.  */
double ieee_add_round_rm(double a, double b, int rm);
double ieee_mul_round_rm(double a, double b, int rm);
double ieee_div_round_rm(double a, double b, int rm);
double ieee_sqrt_round_rm(double a, int rm);

#endif	/*  FLOAT_EMUL_H  */
