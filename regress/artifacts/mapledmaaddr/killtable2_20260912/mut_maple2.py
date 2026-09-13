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
 # -- TABLE 2 (pass 2, 2026-09-12): the survivors of the 16-row instrument --
 # a diagnostic that does not name the device (codex, glm, kimi)
 "M_TOKENFREE": (ASSIGN, T + "fatal(\"[ maple: DMAADDR read ]\\n\");\n" + ASSIGN),
 # the dominating selector weakened: single-bit masks fold 0x04|bit onto DMAADDR (codex)
 "M_ALIAS08":   ("\tswitch (relative_addr) {\n", "\tswitch (relative_addr & ~0x08ULL) {\n"),
 "M_ALIAS20":   ("\tswitch (relative_addr) {\n", "\tswitch (relative_addr & ~0x20ULL) {\n"),
 "M_ALIAS40":   ("\tswitch (relative_addr) {\n", "\tswitch (relative_addr & ~0x40ULL) {\n"),
 # grok's: every offset with bit 2 set is redirected to DMAADDR (ENABLE at 0x14 among them)
 "M_AND4":      ("\tswitch (relative_addr) {\n", "\tif (relative_addr & 4)\n\t\trelative_addr = 0x04;\n"
                                                  "\tswitch (relative_addr) {\n"),
 # the Opus pass-2 seat's MEASURED survivors (opus_pass2_20260912/mut_opus2.py, verbatim edits): declines and exits
 # keyed on the CONSUMER's partitions (maple_do_dma_xfer's `addr & 0x1f' and `!d->enable'), and a per-process read count
 "M_ALIGNDECLINE": ("\t\t} else {\n\t\t\t/*  #528:", "\t\t} else if (d->dmaaddr & 0x1f) {\n\t\t\t/*  #528:"),
 "M_ENDECLINE":    ("\t\t} else {\n\t\t\t/*  #528:", "\t\t} else if (!d->enable) {\n\t\t\t/*  #528:"),
 "M_ALIGNEXIT":    (ASSIGN, ASSIGN + T + "if (d->dmaaddr != 0 && !(d->dmaaddr & 0x1f)) { fatal(\"[ dreamcast_maple: "
                            "TODO: read from dmaaddr ]\\n\"); exit(1); }\n"),
 "M_ENEXIT":       (ASSIGN, ASSIGN + T + "if (d->enable) { fatal(\"[ dreamcast_maple: TODO: read from dmaaddr ]\\n\"); "
                            "exit(1); }\n"),
 "M_THIRDREAD":    (ASSIGN, ASSIGN + T + "{ static int n = 0; if (++n > 2) { fatal(\"[ dreamcast_maple: TODO: read "
                            "from dmaaddr ]\\n\"); exit(1); } }\n"),
 # the exit re-introduced under a width predicate (glm, kimi)
 "M_LEN":       (ASSIGN, T + "if (len != 4) {\n" + T + "\tfatal(\"[ dreamcast_maple: dmaaddr read ]\\n\");\n"
                         + T + "\texit(1);\n" + T + "}\n" + ASSIGN),
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
