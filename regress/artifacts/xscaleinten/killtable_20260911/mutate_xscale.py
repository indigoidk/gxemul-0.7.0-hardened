#!/usr/bin/env python3
"""
mutate_xscale.py -- Mutator for xscaleinten kill table.
"""

import sys

if len(sys.argv) < 5:
    print("usage: mutate_xscale.py <leg> <tgt> <baseline> <headfile>")
    sys.exit(2)

leg = sys.argv[1]
tgt = sys.argv[2]
baseline = sys.argv[3]
headfile = sys.argv[4]

with open(baseline, "r") as f:
    base_content = f.read()

ORIG_BLOCK = """\t\tcase 0:\tif (l_bit) {
\t\t\t\tcpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
\t\t\t\tfatal("TODO: XScale read from inten?\\n");
\t\t\t\texit(1);
\t\t\t} else
\t\t\t\tcpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
\t\t\tbreak;"""

FIXED_BLOCK = """\t\tcase 0:\tif (l_bit) {
\t\t\t\tcpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
\t\t\t} else
\t\t\t\tcpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
\t\t\tbreak;"""

M1_BLOCK = """\t\tcase 0:\tif (l_bit) {
\t\t\t\tcpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
\t\t\t\tif (cpu->cd.arm.i80321_isrc != 0) {
\t\t\t\t\tfatal("TODO: XScale read from inten with isrc!=0\\n");
\t\t\t\t\texit(1);
\t\t\t\t}
\t\t\t} else
\t\t\t\tcpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
\t\t\tbreak;"""

M5_BLOCK = """\t\tcase 0:\tif (l_bit) {
\t\t\t\tcpu->cd.arm.r[rd] = cpu->cd.arm.i80321_isteer;
\t\t\t} else
\t\t\t\tcpu->cd.arm.i80321_isteer = cpu->cd.arm.r[rd];
\t\t\tbreak;"""

M_OPCODE2_BLOCK = """\t\tcase 0:\tif (opcode2 != 0) {
\t\t\t\tfatal("TODO: XScale inten bad opcode2\\n");
\t\t\t\texit(1);
\t\t\t}
\t\t\tif (l_bit) {
\t\t\t\tcpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
\t\t\t} else
\t\t\t\tcpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
\t\t\tbreak;"""

M_RD15_BLOCK = """\t\tcase 0:\tif (l_bit) {
\t\t\t\tif (rd == 15) {
\t\t\t\t\tfatal("TODO: XScale inten to r15 refused\\n");
\t\t\t\t\texit(1);
\t\t\t\t}
\t\t\t\tcpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
\t\t\t} else
\t\t\t\tcpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
\t\t\tbreak;"""

M_NREAD_BLOCK = """\t\tcase 0:\tif (l_bit) {
\t\t\t\tstatic int nread = 0;
\t\t\t\tif (++nread > 4) {
\t\t\t\t\tfatal("TODO: XScale inten nread > 4\\n");
\t\t\t\t\texit(1);
\t\t\t\t}
\t\t\t\tcpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
\t\t\t} else
\t\t\t\tcpu->cd.arm.i80321_inten = cpu->cd.arm.r[rd];
\t\t\tbreak;"""

mutants = {
    "BASE": FIXED_BLOCK,
    "HEAD": ORIG_BLOCK,
    "M1": M1_BLOCK,
    "M5": M5_BLOCK,
    "M_OPCODE2": M_OPCODE2_BLOCK,
    "M_RD15": M_RD15_BLOCK,
    "M_NREAD": M_NREAD_BLOCK,
}

if leg == "HEAD":
    with open(headfile, "r") as f:
        content = f.read()
    with open(tgt, "w") as f:
        f.write(content)
    print(f"HEAD applied from {headfile}")
    sys.exit(0)

if leg in mutants:
    # Determine whether baseline currently has ORIG_BLOCK or FIXED_BLOCK
    if ORIG_BLOCK in base_content:
        target_template = ORIG_BLOCK
    elif FIXED_BLOCK in base_content:
        target_template = FIXED_BLOCK
    else:
        print("ERROR: neither ORIG_BLOCK nor FIXED_BLOCK found in baseline")
        sys.exit(1)
    new_content = base_content.replace(target_template, mutants[leg], 1)
    with open(tgt, "w") as f:
        f.write(new_content)
    print(f"Mutant {leg} applied successfully")
    sys.exit(0)

print(f"ERROR: unknown leg {leg}")
sys.exit(2)
