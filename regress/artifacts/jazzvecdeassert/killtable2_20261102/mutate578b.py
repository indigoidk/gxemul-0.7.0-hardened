#!/usr/bin/env python3
"""mutate578b.py <mutant> <path-to-dev_jazz.c> -- one #578 table-2 mutant applied to the DELETION form: the removed deassert is
re-introduced under a different predicate right after the #578 comment (whose last line is the presence pin, unique in the file)."""
import io
import sys

T = chr(9)
NL = chr(10)
m, p = sys.argv[1], sys.argv[2]
s = io.open(p, encoding="utf-8").read()
PIN = T + "    tree's other interrupt controllers.  */" + NL
assert s.count(PIN) == 1, s.count(PIN)
D = T + T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + NL
forms = {
    "M_b":       T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + NL,
    "M_offs0":   T + "if (relative_addr == 0)" + NL + D,
    "M_offsne0": T + "if (relative_addr != 0)" + NL + D,
    "M_rd":      T + "if (writeflag == MEM_READ)" + NL + D,
    "M_wr":      T + "if (writeflag == MEM_WRITE)" + NL + D,
    "M_offs2":   T + "if (relative_addr == 2)" + NL + D,
    "M_cond":    T + "if (!((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3)))" + NL + D,
    "M_uart":    T + "if (!(d->int_asserted & 0x0300))" + NL + D,
}
if m not in forms:
    sys.exit("unknown mutant " + m)
io.open(p, "w", encoding="utf-8", newline=NL).write(s.replace(PIN, PIN + forms[m]))
print("applied", m)
