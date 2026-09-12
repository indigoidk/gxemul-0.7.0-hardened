#!/usr/bin/env python3
"""
mutate_rlwimi.py -- Mutator for ppcrlwimiwidth kill table.
"""

import sys

if len(sys.argv) < 5:
    print("usage: mutate_rlwimi.py <leg> <tgt> <baseline> <headfile>")
    sys.exit(2)

leg = sys.argv[1]
tgt = sys.argv[2]
baseline = sys.argv[3]
headfile = sys.argv[4]

with open(baseline, "r") as f:
    base_content = f.read()

NULL_MEDIUM_BLOCK = """	/*  NULL MEDIUM: decode and retire, insert nothing.  */
	MODE_uint_t ra = reg(ic->arg[1]);
	uint32_t iword = ic->arg[2];
	int rc = iword & 1;"""

FIXED_BLOCK = """\tuint32_t tmp = (uint32_t)reg(ic->arg[0]);
\tMODE_uint_t ra = reg(ic->arg[1]);
\tuint32_t iword = ic->arg[2];
\tint sh = (iword >> 11) & 31;
\tint mb = (iword >> 6) & 31;
\tint me = (iword >> 1) & 31;   
\tint rc = iword & 1;

\ttmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

\t/*  A wrapping MASK(MB+32, ME+32) includes the high word.  */
\tif (mb > me)
\t\tra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);

\tfor (;;) {
\t\tuint64_t mask;
\t\tmask = (uint64_t)1 << (31-mb);
\t\tra &= ~mask;
\t\tra |= (tmp & mask);
\t\tif (mb == me)
\t\t\tbreak;
\t\tmb ++;
\t\tif (mb == 32)
\t\t\tmb = 0;
\t}"""

M_REV_COND_BLOCK = """\tuint32_t tmp = (uint32_t)reg(ic->arg[0]);
\tMODE_uint_t ra = reg(ic->arg[1]);
\tuint32_t iword = ic->arg[2];
\tint sh = (iword >> 11) & 31;
\tint mb = (iword >> 6) & 31;
\tint me = (iword >> 1) & 31;   
\tint rc = iword & 1;

\ttmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

\t/*  A wrapping MASK(MB+32, ME+32) includes the high word.  */
\tif (mb < me)
\t\tra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);

\tfor (;;) {
\t\tuint64_t mask;
\t\tmask = (uint64_t)1 << (31-mb);
\t\tra &= ~mask;
\t\tra |= (tmp & mask);
\t\tif (mb == me)
\t\t\tbreak;
\t\tmb ++;
\t\tif (mb == 32)
\t\t\tmb = 0;
\t}"""

M_ONLY_CAST_BLOCK = """\tuint32_t tmp = (uint32_t)reg(ic->arg[0]);
\tMODE_uint_t ra = reg(ic->arg[1]);
\tuint32_t iword = ic->arg[2];
\tint sh = (iword >> 11) & 31;
\tint mb = (iword >> 6) & 31;
\tint me = (iword >> 1) & 31;   
\tint rc = iword & 1;

\ttmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

\tfor (;;) {
\t\tuint64_t mask;
\t\tmask = (uint64_t)1 << (31-mb);
\t\tra &= ~mask;
\t\tra |= (tmp & mask);
\t\tif (mb == me)
\t\t\tbreak;
\t\tmb ++;
\t\tif (mb == 32)
\t\t\tmb = 0;
\t}"""

M_ONLY_HIGH_BLOCK = """\tMODE_uint_t tmp = reg(ic->arg[0]), ra = reg(ic->arg[1]);
\tuint32_t iword = ic->arg[2];
\tint sh = (iword >> 11) & 31;
\tint mb = (iword >> 6) & 31;
\tint me = (iword >> 1) & 31;   
\tint rc = iword & 1;

\ttmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

\t/*  A wrapping MASK(MB+32, ME+32) includes the high word.  */
\tif (mb > me)
\t\tra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);

\tfor (;;) {
\t\tuint64_t mask;
\t\tmask = (uint64_t)1 << (31-mb);
\t\tra &= ~mask;
\t\tra |= (tmp & mask);
\t\tif (mb == me)
\t\t\tbreak;
\t\tmb ++;
\t\tif (mb == 32)
\t\t\tmb = 0;
\t}"""

M_POST_LOOP_BLOCK = """\tuint32_t tmp = (uint32_t)reg(ic->arg[0]);
\tMODE_uint_t ra = reg(ic->arg[1]);
\tuint32_t iword = ic->arg[2];
\tint sh = (iword >> 11) & 31;
\tint mb = (iword >> 6) & 31;
\tint me = (iword >> 1) & 31;   
\tint rc = iword & 1;

\ttmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

\tfor (;;) {
\t\tuint64_t mask;
\t\tmask = (uint64_t)1 << (31-mb);
\t\tra &= ~mask;
\t\tra |= (tmp & mask);
\t\tif (mb == me)
\t\t\tbreak;
\t\tmb ++;
\t\tif (mb == 32)
\t\t\tmb = 0;
\t}

\t/*  Ordering mutant: placed after loop where mb == me always  */
\tif (mb > me)
\t\tra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);"""

M_ORIG_BLOCK = """\tMODE_uint_t tmp = reg(ic->arg[0]), ra = reg(ic->arg[1]);
\tuint32_t iword = ic->arg[2];
\tint sh = (iword >> 11) & 31;
\tint mb = (iword >> 6) & 31;
\tint me = (iword >> 1) & 31;   
\tint rc = iword & 1;

\ttmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

\tfor (;;) {
\t\tuint64_t mask;
\t\tmask = (uint64_t)1 << (31-mb);
\t\tra &= ~mask;
\t\tra |= (tmp & mask);
\t\tif (mb == me)
\t\t\tbreak;
\t\tmb ++;
\t\tif (mb == 32)
\t\t\tmb = 0;
\t}"""

if leg == "HEAD":
    with open(headfile, "r") as f:
        head_content = f.read()
    with open(tgt, "w") as f:
        f.write(head_content)
    print("MUTATION HEAD: replaced with whole-file HEAD")
    sys.exit(0)

if FIXED_BLOCK not in base_content:
    print("ERROR: FIXED_BLOCK not found in baseline")
    sys.exit(1)

replacement = None
if leg in ("BASE", "RESTORED"):
    replacement = FIXED_BLOCK
elif leg in ("NULL_MEDIUM", "M_IDENTITY"):
    replacement = NULL_MEDIUM_BLOCK
elif leg == "M_REV_COND":
    replacement = M_REV_COND_BLOCK
elif leg == "M_ONLY_CAST":
    replacement = M_ONLY_CAST_BLOCK
elif leg == "M_ONLY_HIGH":
    replacement = M_ONLY_HIGH_BLOCK
elif leg == "M_POST_LOOP":
    replacement = M_POST_LOOP_BLOCK
elif leg == "M_ORIG":
    replacement = M_ORIG_BLOCK
else:
    print("ERROR: unknown leg %s" % leg)
    sys.exit(1)

new_content = base_content.replace(FIXED_BLOCK, replacement)
with open(tgt, "w") as f:
    f.write(new_content)

print("MUTATION %s: successfully applied" % leg)
sys.exit(0)
