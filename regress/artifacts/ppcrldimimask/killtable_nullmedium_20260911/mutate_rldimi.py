#!/usr/bin/env python3
"""
mutate_rldimi.py -- Mutator for ppcrldimimask NULL_MEDIUM kill table leg.
"""

import sys

if len(sys.argv) < 5:
    print("usage: mutate_rldimi.py <leg> <tgt> <baseline> <headfile>")
    sys.exit(2)

leg = sys.argv[1]
tgt = sys.argv[2]
baseline = sys.argv[3]
headfile = sys.argv[4]

with open(baseline, "r") as f:
    base_content = f.read()

FIXED_BLOCK = """\tuint32_t iw = ic->arg[0];
\tint rs = (iw >> 21) & 31, ra = (iw >> 16) & 31;
\tint sh = ((iw >> 11) & 31) | ((iw & 2) << 4);
\tint mb = ((iw >> 6) & 31) | (iw & 0x20);
\tint rc = ic->arg[0] & 1;
\tint m, n = sh;
\tuint64_t tmp, s = cpu->cd.ppc.gpr[rs];
\t/*  TODO: Fix this, its performance is awful:  */
\twhile (n-- != 0) {
\t\tint b = (s >> 63) & 1;
\t\ts = (s << 1) | b;
\t}
\tm = mb; tmp = 0;
\tdo {
\t\ttmp |= ((uint64_t)1 << (63-m));
\t\tm = (m + 1) & 63;
\t} while (m != ((64 - sh) & 63));
\tcpu->cd.ppc.gpr[ra] &= ~tmp;
\tcpu->cd.ppc.gpr[ra] |= (tmp & s);"""

NULL_MEDIUM_BLOCK = """\t/*  NULL MEDIUM: decode and retire, insert nothing.  */
\tuint32_t iw = ic->arg[0];
\tint ra = (iw >> 16) & 31;
\tint rc = iw & 1;

\tcpu->cd.ppc.gpr[ra] = cpu->cd.ppc.gpr[ra];"""

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
else:
    print("ERROR: unknown leg %s" % leg)
    sys.exit(1)

new_content = base_content.replace(FIXED_BLOCK, replacement)
with open(tgt, "w") as f:
    f.write(new_content)

print("MUTATION %s: successfully applied" % leg)
sys.exit(0)
