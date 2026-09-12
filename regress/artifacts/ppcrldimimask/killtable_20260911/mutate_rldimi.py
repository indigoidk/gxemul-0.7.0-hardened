#!/usr/bin/env python3
"""
mutate_rldimi.py -- Mutator for ppcrldimimask kill table.
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

FIXED_BLOCK = """\tint m, n = sh;
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

M_ORIG_BLOCK = """\tint m;
\tuint64_t tmp, s = cpu->cd.ppc.gpr[rs];
\t/*  TODO: Fix this, its performance is awful:  */
\twhile (sh-- != 0) {
\t\tint b = (s >> 63) & 1;
\t\ts = (s << 1) | b;
\t}
\tm = mb; tmp = 0;
\tdo {
\t\ttmp |= ((uint64_t)1 << (63-m));
\t\tm ++;
\t} while (m != 63 - sh);
\tcpu->cd.ppc.gpr[ra] &= ~tmp;
\tcpu->cd.ppc.gpr[ra] |= (tmp & s);"""

M_MUT63_BLOCK = """\tint m, n = sh;
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
\t} while (m != ((63 - sh) & 63));
\tcpu->cd.ppc.gpr[ra] &= ~tmp;
\tcpu->cd.ppc.gpr[ra] |= (tmp & s);"""

M_NOWRAP_BLOCK = """\tint m, n = sh;
\tuint64_t tmp, s = cpu->cd.ppc.gpr[rs];
\t/*  TODO: Fix this, its performance is awful:  */
\twhile (n-- != 0) {
\t\tint b = (s >> 63) & 1;
\t\ts = (s << 1) | b;
\t}
\tm = mb; tmp = 0;
\tdo {
\t\ttmp |= ((uint64_t)1 << (63-m));
\t\tm ++;
\t} while (m < 64 - sh);
\tcpu->cd.ppc.gpr[ra] &= ~tmp;
\tcpu->cd.ppc.gpr[ra] |= (tmp & s);"""

M_NOKEEP_SH_BLOCK = """\tint m;
\tuint64_t tmp, s = cpu->cd.ppc.gpr[rs];
\t/*  TODO: Fix this, its performance is awful:  */
\twhile (sh-- != 0) {
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

M_NOCIRC_BLOCK = """\tint m, n = sh;
\tuint64_t tmp, s = cpu->cd.ppc.gpr[rs];
\t/*  TODO: Fix this, its performance is awful:  */
\twhile (n-- != 0) {
\t\tint b = (s >> 63) & 1;
\t\ts = (s << 1) | b;
\t}
\tm = mb; tmp = 0;
\tdo {
\t\ttmp |= ((uint64_t)1 << (63-m));
\t\tm ++;
\t} while (m != ((64 - sh) & 63));
\tcpu->cd.ppc.gpr[ra] &= ~tmp;
\tcpu->cd.ppc.gpr[ra] |= (tmp & s);"""

M_NO_MERGE_BLOCK = """\tint m, n = sh;
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
\tcpu->cd.ppc.gpr[ra] = (tmp & s);"""

mutants = {
    "BASE": FIXED_BLOCK,
    "M_ORIG": M_ORIG_BLOCK,
    "M_MUT63": M_MUT63_BLOCK,
    "M_NOWRAP": M_NOWRAP_BLOCK,
    "M_NOKEEP_SH": M_NOKEEP_SH_BLOCK,
    "M_NOCIRC": M_NOCIRC_BLOCK,
    "M_NO_MERGE": M_NO_MERGE_BLOCK,
}

if leg == "HEAD":
    with open(headfile, "r") as f:
        content = f.read()
    with open(tgt, "w") as f:
        f.write(content)
    print(f"HEAD applied from {headfile}")
    sys.exit(0)

if leg in mutants:
    if FIXED_BLOCK not in base_content:
        print("ERROR: FIXED_BLOCK not found in baseline")
        sys.exit(1)
    new_content = base_content.replace(FIXED_BLOCK, mutants[leg], 1)
    with open(tgt, "w") as f:
        f.write(new_content)
    print(f"Mutant {leg} applied successfully")
    sys.exit(0)

print(f"ERROR: unknown leg {leg}")
sys.exit(2)
