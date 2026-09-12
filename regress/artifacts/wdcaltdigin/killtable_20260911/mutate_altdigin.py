#!/usr/bin/env python3
"""Mutation driver for wdcaltdigin kill table."""
import sys

LEG = sys.argv[1]
TARGET = sys.argv[2]
HEAD_REF = sys.argv[3]

with open(HEAD_REF, "r", encoding="latin1") as f:
    orig = f.read()

ANCHOR = """\tif (writeflag==MEM_READ)
\t\tdebug("[ wdc: read from ALTSTATUS: 0x%02x ]\\n",
\t\t    (int)odata);
\telse if (relative_addr != 0) {"""

if ANCHOR not in orig:
    sys.exit("ERROR: ANCHOR not found in reference dev_wdc.c")

MUTANTS = {
    "HEAD": ANCHOR,

    "BASE": """\tif (writeflag == MEM_READ) {
\t\tif (relative_addr != 0) {
\t\t\t/*  Declined read convention: emulator policy pre-zeroes
\t\t\t    registered-device read buffers (#95); return 0 here
\t\t\t    for unmapped offset 1 (Drive Address register / digin).  */
\t\t\todata = 0;
\t\t} else {
\t\t\tdebug("[ wdc: read from ALTSTATUS: 0x%02x ]\\n",
\t\t\t    (int)odata);
\t\t}
\t} else if (relative_addr != 0) {""",

    "M_NULL_EFFECT": """\tif (writeflag == MEM_READ) {
\t\tif (relative_addr != 0) {
\t\t\t/*  B-null-effect: relative_addr decoded but odata = 0 omitted  */
\t\t} else {
\t\t\tdebug("[ wdc: read from ALTSTATUS: 0x%02x ]\\n",
\t\t\t    (int)odata);
\t\t}
\t} else if (relative_addr != 0) {""",

    "M_REINSTATE": """\tif (writeflag == MEM_READ)
\t\tdebug("[ wdc: read from ALTSTATUS: 0x%02x ]\\n",
\t\t    (int)odata);
\telse if (relative_addr != 0) {""",

    "M_NULL_MEDIUM": """\tif (writeflag == MEM_READ) {
\t\tdata[0] = 0;
\t\treturn 1;
\t} else if (relative_addr != 0) {""",
}

if LEG not in MUTANTS:
    sys.exit(f"ERROR: Unknown leg {LEG}")

replacement = MUTANTS[LEG]
mutated = orig.replace(ANCHOR, replacement, 1)

with open(TARGET, "w", encoding="latin1") as f:
    f.write(mutated)

print(f"[MUTATE] Successfully applied mutation for leg {LEG}")
