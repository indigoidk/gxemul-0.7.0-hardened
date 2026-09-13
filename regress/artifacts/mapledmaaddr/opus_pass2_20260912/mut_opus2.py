#!/usr/bin/env python3
"""mapledmaaddr (#528) pass-2 measuring-seat mutator (Opus 5).  usage: mut_opus2.py <SEC maple.c> <out> <LEG>

Every leg edits the FIXED read arm.  Each find-text must occur EXACTLY ONCE or the leg is REFUSED.
Legs are drawn from the partitions the field's CONSUMER tests (maple_do_dma_xfer: `!d->enable', `addr & 0x1f'),
from the (d) form `if (X)' -> `if (X && Y)' on the dominating read-arm predicate, from the silence row's key
text, and from `len' (disclosed) and a per-process read count (structural: <= 2 reads per session).
"""
import io, sys

ASSIGN = "\t\t\todata = d->dmaaddr;\n"
ELSE = "\t\t} else {\n\t\t\t/*  #528:"
T = "\t\t\t"
FX = "fatal(\"[ dreamcast_maple: TODO: read from dmaaddr ]\\n\"); exit(1);"

LEGS = {
 # (d) if (X) -> if (X && Y) on the dominating else-arm, Y = the consumer's alignment partition: aligned nonzero
 #     values are silently DECLINED (odata stays 0); zero still reads 0
 "M_ALIGNDECLINE": (ELSE, "\t\t} else if (d->dmaaddr & 0x1f) {\n\t\t\t/*  #528:"),
 # the same, Y = the consumer's enable partition
 "M_ENDECLINE":    (ELSE, "\t\t} else if (!d->enable) {\n\t\t\t/*  #528:"),
 # the removed fatal()+exit(1) re-introduced under the consumer's alignment predicate (nonzero, 32-byte aligned)
 "M_ALIGNEXIT":    (ASSIGN, ASSIGN + T + "if (d->dmaaddr != 0 && !(d->dmaaddr & 0x1f)) { " + FX + " }\n"),
 # ... and under the consumer's enable predicate
 "M_ENEXIT":       (ASSIGN, ASSIGN + T + "if (d->enable) { " + FX + " }\n"),
 # the diagnostic reworded WITHOUT the device name (in-file precedent: `[ maple_do_dma_xfer: not enabled? ]')
 "M_NOPREFIX":     (ASSIGN, T + "fatal(\"[ maple: TODO: read from dmaaddr ]\\n\");\n" + ASSIGN),
 # width: exit on a non-32-bit read (DISCLOSED by the contract -- measured as a control of the disclosure)
 "M_LENEXIT":      (ASSIGN, T + "if (len != sizeof(uint32_t)) { " + FX + " }\n" + ASSIGN),
 # a per-process read count: exit on the third DMAADDR read (every session makes at most two)
 "M_THIRDREAD":    (ASSIGN, ASSIGN + T + "{ static int n = 0; if (++n > 2) { " + FX + " } }\n"),
}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg not in LEGS:
    sys.exit("unknown leg %s -- REFUSING" % leg)
old, new = LEGS[leg]
if t.count(old) != 1:
    sys.stderr.write("find-text for %s occurs %d times -- REFUSING\n" % (leg, t.count(old)))
    sys.exit(3)
t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
