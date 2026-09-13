#!/usr/bin/env python3
"""mapledmaaddr (#528) kill-table mutator.  usage: mut_maple.py <SEC dev_dreamcast_maple.c> <out> <LEG>

Every leg edits the FIXED read arm (or, for M_HOIST, the declaration above the switch).  Each find-text must occur
EXACTLY ONCE or the leg is REFUSED, so a find-text doubles as a presence pin.  HEAD is not built here -- the driver
takes it from `git show HEAD:`.
"""
import io, sys

ASSIGN = "\t\t\todata = d->dmaaddr;\n"
DECL = "\tuint64_t idata = 0, odata = 0;\n"
T = "\t\t\t"

LEGS = {
 # the diagnostic reinstated, verbatim / reworded / latched (house idiom), with no exit: the silence row's legs
 "M_KEEPFATAL": (ASSIGN, T + "fatal(\"[ dreamcast_maple: TODO: read from dmaaddr ]\\n\");\n" + ASSIGN),
 "M_REWORD":    (ASSIGN, T + "fatal(\"[ dreamcast_maple: read from dmaaddr ]\\n\");\n" + ASSIGN),
 "M_LATCHED":   (ASSIGN, T + "{ static int w = 0; if (!w) { w = 1; fatal(\"[ dreamcast_maple: "
                             "DMAADDR read (once) ]\\n\"); } }\n" + ASSIGN),
 # the exit alone
 "M_EXITONLY":  (ASSIGN, ASSIGN + T + "exit(1);\n"),
 # the FAULT idiom and DECLINE
 "M_RET0":      (ASSIGN, T + "return 0;\n"),
 "M_DECLINE":   (ASSIGN, T + "/*  declined  */\n"),
 # the read hoisted out of its relative_addr == 0x04 guard (the arm itself emptied)
 "M_HOIST":     None,
 # read-to-clear
 "M_READCLEAR": (ASSIGN, ASSIGN + T + "d->dmaaddr = 0;\n"),
 # value-keyed exits: clause (e) cells, each pinned by one L1 row
 "M_EQ4":       (ASSIGN, ASSIGN + T + "if (d->dmaaddr == 0x04)\n" + T + "\texit(1);\n"),
 "M_BIT30":     (ASSIGN, ASSIGN + T + "if (d->dmaaddr & 0x40000000)\n" + T + "\texit(1);\n"),
 "M_ZEROEXIT":  (ASSIGN, ASSIGN + T + "if (d->dmaaddr == 0)\n" + T + "\texit(1);\n"),
 # masking of the low five bits (the alignment the DMA path wants, applied to the read)
 "M_MASKLOW":   (ASSIGN, T + "odata = d->dmaaddr & ~(uint64_t)0x1f;\n"),
}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg not in LEGS:
    sys.exit("unknown leg %s -- REFUSING" % leg)
if leg == "M_HOIST":
    edits = [(DECL, "\tuint64_t idata = 0, odata = d->dmaaddr;\n"), (ASSIGN, T + "/*  hoisted above the switch  */\n")]
else:
    edits = [LEGS[leg]]
for old, new in edits:
    if t.count(old) != 1:
        sys.stderr.write("find-text for %s occurs %d times -- REFUSING\n" % (leg, t.count(old)))
        sys.exit(3)
    t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
