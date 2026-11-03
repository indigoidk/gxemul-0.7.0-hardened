#!/usr/bin/env python3
"""mutate578.py <mutant> <path-to-dev_jazz.c> -- one #578 kill-table mutant applied to the FIXED jazzio tail (scratch clone only).
Find-texts must occur exactly once (a presence pin).  The fixed tail is:
    if (!((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3)))
        INTERRUPT_DEASSERT(d->mips_irq_3);
"""
import io
import sys

T = chr(9)
NL = chr(10)
m, p = sys.argv[1], sys.argv[2]
s = io.open(p, encoding="utf-8").read()
# The two conditional lines ALSO occur verbatim in jazz_interrupt_deassert() (:153-154), so the pin is anchored on the last line of the
# fix's own comment, which precedes them only at the tail.  (The first table run was refused by the pin with count 2 -- recorded in
# PRETABLE_CORRECTION.out; the pin working is the point of having it.)
CMT = T + "    old comment describes behaves as before.  */" + NL
COND = (T + "if (!((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3)))" + NL +
        T + T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + NL)
FIX = CMT + COND
assert s.count(FIX) == 1, s.count(FIX)
DEASSERT = T + T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + NL
if m == "M_b":          # (b) the unconditional deassert reinstated verbatim
    s = s.replace(FIX, CMT + T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + NL)
elif m == "M_del":      # (e) the deassert deleted outright (option 2 of the brief): the equivalence measurement
    s = s.replace(FIX, CMT)
elif m == "M_nomask":   # (d) the int_enable_mask term dropped
    s = s.replace(FIX, CMT + T + "if (!(d->int_asserted & 0x7fff))" + NL + DEASSERT)
elif m == "M_lowbits":  # (d) the line mask narrowed so lines 8-14 fall outside
    s = s.replace(FIX, CMT + T + "if (!((d->int_asserted & 0x00ff) && (d->int_enable_mask & R4030_EXT_IP3)))" + NL + DEASSERT)
elif m == "M_ip6":      # (d) the wrong enable bit
    s = s.replace(FIX, CMT + T + "if (!((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP6)))" + NL + DEASSERT)
elif m == "M_timer":    # (d) the timer line instead of the local-bus lines
    s = s.replace(FIX, CMT + T + "if (!((d->int_asserted & PICA_TIMER_IRQ_MASK) && (d->int_enable_mask & R4030_EXT_IP3)))" + NL + DEASSERT)
elif m == "M_inv":      # (d) the predicate inverted
    s = s.replace(FIX, CMT + T + "if ((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3))" + NL + DEASSERT)
else:
    sys.exit("unknown mutant " + m)
io.open(p, "w", encoding="utf-8", newline=NL).write(s)
print("applied", m)
