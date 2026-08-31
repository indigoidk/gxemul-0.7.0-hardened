#!/usr/bin/env python3
#  #497 widthkillclass -- the fix, applied to a COPY of the tree.
#  opus5 compile-and-measure seat.  Never run against GXEMUL-SEC.
import re, sys

BS = chr(92)
NL = BS + "n"                      # the two chars ending a C string literal

p = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gx497impl/src/devices/dev_sgi_re.c"
s = open(p).read()
orig = s

SITES = [
    ("CRIME_RE_TLB_A",    "SGIRE_W_TLBA_LEN", None),
    ("CRIME_RE_TLB_B",    "SGIRE_W_TLBB_LEN", None),
    ("CRIME_RE_TLB_C",    "SGIRE_W_TLBC_LEN", None),
    ("CRIME_RE_TEX",      "SGIRE_W_TEX_LEN",  None),
    ("CRIME_RE_LINEAR_A", "SGIRE_W_LINA_LEN", "re_linear_b[0]"),
    ("CRIME_RE_LINEAR_B", "SGIRE_W_LINB_LEN", "de_reg[0]"),
]

# ---------------------------------------------------------------- 1. the latch
anchor = "struct sgi_re_data {"
assert s.count(anchor) == 1, "struct anchor count=%d" % s.count(anchor)

bits = "\n".join("\t%-18s= 1 << %d," % (b, i) for i, (_, b, _x) in enumerate(SITES))

enum_block = (
    "/*\n"
    " *  #497: one latch bit per WIDTH-guard site in DEVICE_ACCESS(sgi_re).\n"
    " *\n"
    " *  SIX FLAGS, NOT ONE.  dev_wdc.c's own comment adjudicates this: sharing a\n"
    " *  latch is licensed only across sites that are MUTUALLY EXCLUSIVE at\n"
    " *  runtime.  These six are six different address windows, and any driver\n"
    " *  bringing up the rendering engine walks all of them in ONE session, so a\n"
    " *  shared latch would report the first odd-width access and silence the\n"
    " *  other five.\n"
    " */\n"
    "enum {\n" + bits + "\n};\n\n"
)

s = s.replace(anchor, enum_block + anchor, 1)
s = s.replace(
    "\tuint32_t\tre_linear_b[32];\n",
    "\tuint32_t\tre_linear_b[32];\n\n"
    "\t/*  #497: width-guard decline latches; see the enum above.  */\n"
    "\tuint32_t\twarned;\n", 1)

# ------------------------------------------------- 2. the shared block comment
chain = "\tif (relative_addr >= CRIME_RE_TLB_A && relative_addr < CRIME_RE_TLB_B) {"
assert s.count(chain) == 1, "chain anchor count=%d" % s.count(chain)

block = (
    "\t/*\n"
    "\t *  #497: THE SIX WIDTH GUARDS BELOW USED TO END THE HOST PROCESS.\n"
    "\t *\n"
    "\t *  A guest choosing an access width is not an emulator error, so each\n"
    "\t *  `len != 8' arm now DECLINES the access and announces itself once.\n"
    "\t *  Three properties of the shape are load-bearing:\n"
    "\t *\n"
    "\t *  1. It is an `else if' SPLICE, not an early return.  A `return' here\n"
    "\t *     would skip this function's common tail, and `return 0' would be\n"
    "\t *     coerced to -1 by cpus/memory_rw.c and raise EXCEPTION_DBE in the\n"
    "\t *     guest -- turning a declined access into a guest bus error.\n"
    "\t *\n"
    "\t *  2. Control therefore reaches the tail, which answers a declined READ\n"
    "\t *     with odata (0).  That tail is dead code before this change: every\n"
    "\t *     read arm below still exit(1)s, so odata is never assigned today.\n"
    "\t *\n"
    "\t *  3. The guards are NOT redundant.  For TLB_A/B/C and TEX the store is a\n"
    "\t *     `for (hwi = 0; hwi < len; ...)' loop, so a narrower access simply\n"
    "\t *     runs fewer iterations and stays in bounds -- there the guard is\n"
    "\t *     modelling fidelity only.  For LINEAR_A and LINEAR_B it is not; see\n"
    "\t *     the note at those two sites.\n"
    "\t *\n"
    "\t *  Only the WIDTH kills change here.  The six `TODO: read from ...' kills\n"
    "\t *  and the final catch-all are deliberately untouched (sgirekills), as is\n"
    "\t *  DEVICE_ACCESS(sgi_de)'s own width kill, whose accept set is {4,8}\n"
    "\t *  rather than {8} (sgidewidth).\n"
    "\t */\n")

s = s.replace(chain, block + chain, 1)

# --------------------------------------------------------- 3. the six splices
LIN_NOTE = (
    "\t\t\t/*\n"
    "\t\t\t *  #497: THIS GUARD IS ALSO THE ONLY BOUNDS CHECK.  Unlike the\n"
    "\t\t\t *  TLB/TEX arms, the store below is FIXED ARITY -- it ignores len\n"
    "\t\t\t *  and always writes [tlbi] and [tlbi+1].  tlbi is\n"
    "\t\t\t *  ((relative_addr & 0x7f) >> 2) & 0x1f, so it reaches 31 and\n"
    "\t\t\t *  [tlbi+1] indexes 32 of a [32] array.  Only 8-byte ALIGNMENT\n"
    "\t\t\t *  keeps tlbi even and thus <= 30, and MIPS supplies that\n"
    "\t\t\t *  alignment (cpus/cpu_mips_instr_loadstore.c raises ADES/ADEL\n"
    "\t\t\t *  before the device is reached), so len == 8 implies it.\n"
    "\t\t\t *\n"
    "\t\t\t *  Measured, not assumed: the over-run stays INSIDE the struct --\n"
    "\t\t\t *  re_linear_a[32] IS re_linear_b[0] and re_linear_b[32] IS\n"
    "\t\t\t *  de_reg[0] (offsetof: 1760/1888/2016).  So this is undefined\n"
    "\t\t\t *  behaviour and a SILENT clobber of the adjacent register array,\n"
    "\t\t\t *  reaching a DRAWING-engine register from a rendering-engine\n"
    "\t\t\t *  write -- not a wild write outside the allocation, and not\n"
    "\t\t\t *  something plain ASAN would flag.  Declining keeps it shut.\n"
    "\t\t\t */\n")

n = 0
for sym, bit, alias in SITES:
    old = ("\t\tif (len != 8) {\n"
           '\t\t\tfatal("TODO: unimplemented len=%i for ' + sym + NL + '", len);\n'
           "\t\t\texit(1);\n"
           "\t\t}\n"
           "\n"
           "\t\tif (writeflag == MEM_WRITE) {\n")
    note = LIN_NOTE if alias else ""
    new = ("\t\tif (len != 8) {\n"
           + note +
           "\t\t\tif (!(d->warned & " + bit + ")) {\n"
           "\t\t\t\td->warned |= " + bit + ";\n"
           '\t\t\t\tfatal("[ sgi_re: unimplemented len=%i for "\n'
           '\t\t\t\t    "' + sym + ' -- declined.  (once) ]' + NL + '",\n'
           "\t\t\t\t    (int) len);\n"
           "\t\t\t}\n"
           "\t\t} else if (writeflag == MEM_WRITE) {\n")
    c = s.count(old)
    assert c == 1, "site %s: expected 1 occurrence, got %d" % (sym, c)
    s = s.replace(old, new, 1)
    n += 1

assert n == 6, n
assert s != orig
open(p, "w").write(s)

live = len(re.findall(r"^\s+exit\(1\);", s, re.M))
print("APPLIED_SITES=%d" % n)
print("live_exit1_in_file=%d" % live)
print("warned_refs=%d" % s.count("d->warned"))
print("FIX497_APPLIED_DONE")
