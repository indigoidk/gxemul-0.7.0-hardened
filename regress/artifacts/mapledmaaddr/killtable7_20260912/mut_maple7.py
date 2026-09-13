#!/usr/bin/env python3
"""mapledmaaddr (#528) kill-table mutator.  usage: mut_maple7.py <SEC dev_dreamcast_maple.c> <out> <LEG>

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
 # -- TABLE 3 (the §F2 adjudication pass, 2026-09-12): survivors of the 29-row instrument --
 # the low selector bits folded: a mov.b at 0x05 / mov.w at 0x06 reaches the device and lands on DMAADDR (kimi)
 "M_ALIAS01":   ("\tswitch (relative_addr) {\n", "\tswitch (relative_addr & ~0x01ULL) {\n"),
 "M_ALIAS02":   ("\tswitch (relative_addr) {\n", "\tswitch (relative_addr & ~0x02ULL) {\n"),
 # a case label stacked on DMAADDR's (codex)
 "M_CASE00":    ("\tcase 0x04:\t/*  MAPLE_DMAADDR  */\n", "\tcase 0x00:\n\tcase 0x04:\t/*  MAPLE_DMAADDR  */\n"),
 # a diagnostic whose only line is a bare hex value -- the SHAPE of a `print' answer (codex)
 "M_HEXDIAG":   (ASSIGN, T + "fatal(\"0x%08x\\n\", (unsigned)d->dmaaddr);\n" + ASSIGN),
 # a decline in the JOINT cell of the consumer's partitions only: enabled AND aligned (codex)
 "M_JOINTDECLINE": ("\t\t} else {\n\t\t\t/*  #528:", "\t\t} else if (!d->enable || (d->dmaaddr & 0x1f)) {\n\t\t\t/*  #528:"),
 # the read arm also writes a sibling field (kimi)
 "M_SIBLING":   (ASSIGN, ASSIGN + T + "d->enable = 1;\n"),
 # the exit re-introduced under an 8-bit access, silently (kimi: len == 1)
 "M_LEN1":      (ASSIGN, T + "if (len == 1)\n" + T + "\texit(1);\n" + ASSIGN),
 # -- TABLE 4: diagnostics in the grammar's shape-free members (grok: a blank line) and a prompt-shaped line --
 "M_BLANKDIAG":  (ASSIGN, T + "fatal(\"\\n\");\n" + ASSIGN),
 "M_CRDIAG":     (ASSIGN, T + "fatal(\"\\r\");\n" + ASSIGN),
 "M_PROMPTDIAG": (ASSIGN, T + "fatal(\"GXemul> \\n\");\n" + ASSIGN),
 # -- TABLE 5 (Fable pass 2): the two predicted survivors of table 4's oracle, the unmeasured selector bits, and the
 # single-bit read side effects --
 # a newline-less prompt-shaped diagnostic: glued onto the front of the next prompt line
 "M_GLUEPROMPT": (ASSIGN, T + "fatal(\"GXemul> \");\n" + ASSIGN),
 # the text the table-4 prompt count EXEMPTED
 "M_QUITLINE":   (ASSIGN, T + "fatal(\"GXemul> quit\\n\");\n" + ASSIGN),
 # the two single-bit narrowings of the selector never built as legs
 "M_ALIAS10":    ("\tswitch (relative_addr) {\n", "\tswitch (relative_addr & ~0x10ULL) {\n"),
 "M_ALIAS04":    ("\tswitch (relative_addr) {\n", "\tswitch (relative_addr & ~0x04ULL) {\n"),
 # a read that SETS a bit VAL_A already holds / CLEARS a bit VAL_A does not hold
 "M_ORBIT31":    (ASSIGN, ASSIGN + T + "d->dmaaddr |= 0x80000000U;\n"),
 "M_ANDBIT30":   (ASSIGN, ASSIGN + T + "d->dmaaddr &= ~0x40000000U;\n"),
 # -- TABLE 6 (the closing pass): the Opus seat's MEASURED survivor of table 5's pre-quit snapshot, verbatim from
 # ../opus_close_20260912/M_ATEXIT.diff -- the read registers an exit-time diagnostic (two edits, one leg) --
 "M_ATEXIT":     [("DEVICE_ACCESS(dreamcast_maple)\n",
                   "static int maple_ax_reg = 0;\nstatic void maple_dmaaddr_atexit(void)\n{\n"
                   "\tfatal(\"[ dreamcast_maple: DMAADDR was read ]\\n\");\n}\n\n\nDEVICE_ACCESS(dreamcast_maple)\n"),
                  (ASSIGN, ASSIGN + T + "if (!maple_ax_reg) { maple_ax_reg = 1; atexit(maple_dmaaddr_atexit); }\n")],
}

# -- TABLE 7 (the final pass): the Opus seat's two MEASURED exit-time survivors (verbatim from
# ../opus_final_20260912/mut_final3.py), its measured tick-window survivor as a DISCLOSED-window control, and codex's
# two predicted forms.  Built with chr(92) for every backslash that must reach the C file (carrier rule). --
BS = chr(92)
NL = BS + "n"
HDR = "DEVICE_ACCESS(dreamcast_maple)\n"
TICKHEAD = ("DEVICE_TICK(maple)\n{\n\tstruct dreamcast_maple_data *d = (struct dreamcast_maple_data *) extra;\n"
            "\tint key;\n")


def deferred(body, keyed):
    cond = "d->dmaaddr != 0 && " if keyed else ""
    return [(HDR, "static int maple_q_reg = 0;\nstatic void maple_q_die(void)\n{\n\t" + body + "\n}\n\n\n" + HDR),
            (ASSIGN, ASSIGN + T + "if (" + cond + "!maple_q_reg) { maple_q_reg = 1; atexit(maple_q_die); }\n")]


LEGS.update({
 # the exit(1) half of the removed defect moved to process exit, keyed on a nonzero field (Opus, 37/37 on FROZEN6)
 "M_EXITATQUIT":  deferred("_Exit(1);", True),
 "M_ABORTATQUIT": deferred("abort();", True),
 # codex: a crash at exit keyed on ONE session's value
 "M_ABORTAT4":    [(HDR, "static int maple_q_reg = 0;\nstatic void maple_q_die(void)\n{\n\tabort();\n}\n\n\n" + HDR),
                   (ASSIGN, ASSIGN + T + "if (d->dmaaddr == 4 && !maple_q_reg) { maple_q_reg = 1; "
                                         "atexit(maple_q_die); }\n")],
 # codex/kimi/deepseek: an exit handler that waits past the post-quit cap, then speaks -- keyed on the value 4
 "M_SLOWATEXIT4": [("#include <sys/time.h>\n", "#include <sys/time.h>\n#include <unistd.h>\n"),
                   (HDR, "static int maple_q_reg = 0;\nstatic void maple_q_die(void)\n{\n\tsleep(11);\n"
                         "\tfatal(\"[ dreamcast_maple: DMAADDR was read ]" + NL + "\");\n}\n\n\n" + HDR),
                   (ASSIGN, ASSIGN + T + "if (d->dmaaddr == 4 && !maple_q_reg) { maple_q_reg = 1; "
                                         "atexit(maple_q_die); }\n")],
 # codex: the read replaces the disassembler, which then prints `addr:  opcode DMAADDR read' for every stepped
 # instruction -- the old matcher compared address + opcode only
 "M_DISASMHOOK":  [(HDR, "static int maple_note_disasm(struct cpu *c, unsigned char *p, int running, uint64_t addr)\n"
                         "{\n\tunsigned word = c->byte_order == EMUL_BIG_ENDIAN ? ((unsigned)p[0] << 8) | p[1]\n"
                         "\t    : ((unsigned)p[1] << 8) | p[0];\n"
                         "\tfatal(\"%08x:  %04x DMAADDR read" + NL + "\", (unsigned)(uint32_t)(running ? c->pc : addr),"
                         " word);\n\treturn 2;\n}\n\n\n" + HDR),
                   (ASSIGN, ASSIGN + T + "cpu->cpu_family->disassemble_instr = maple_note_disasm;\n")],
 # the DISCLOSED window (Opus, 37/37): a periodic summary on every 4th device tick -- a session spans at most three
 # (the first-step tick + the two cpu_run_deinit() ticks).  Expected to SURVIVE both instruments: a measurement of
 # the stated window, never a kill.
 "M_TICKPERIODIC4": [(TICKHEAD, "static int maple_rd_count = 0, maple_tick_n = 0;\n" + TICKHEAD
                      + "\tif (++maple_tick_n % 4 == 0 && maple_rd_count) { fatal(\"[ dreamcast_maple: DMAADDR was"
                      + " read (%i times) ]" + NL + "\", maple_rd_count); maple_rd_count = 0; }\n"),
                     (ASSIGN, ASSIGN + T + "maple_rd_count++;\n")],
})

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg not in LEGS:
    sys.exit("unknown leg %s -- REFUSING" % leg)
if leg == "M_HOIST":
    edits = [(DECL, "\tuint64_t idata = 0, odata = d->dmaaddr;\n"), (ASSIGN, T + "/*  hoisted above the switch  */\n")]
else:
    edits = LEGS[leg] if isinstance(LEGS[leg], list) else [LEGS[leg]]
for old, new in edits:
    if t.count(old) != 1:
        sys.stderr.write("find-text for %s occurs %d times -- REFUSING\n" % (leg, t.count(old)))
        sys.exit(3)
    t = t.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
