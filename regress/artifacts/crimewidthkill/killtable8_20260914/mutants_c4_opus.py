#!/usr/bin/env python3
"""#529 CLOSING PASS 4 (Opus seat) -- the six reading seats' predicted 131/131 survivors, built as source mutants of
dev_sgi_ip32.c.  usage: mutants_c4.py <name> <file>  (edits in place; every find-text must occur EXACTLY once, else exit 1).
"""
import sys

GOTO = "\t\tgoto crime_declined;\n"
DOGBLK = ("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"
          "\t\t\t\tidata &= ~CRIME_CONTROL_DOG_ENABLE;\n"
          "\t\t\t}\n")
FATAL = "\t\t\tfatal(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n"
INTARM = ("\tcase CRIME_INTSTAT:\t/*  0x010, Current interrupt status  */\n"
          "\tcase CRIME_INTMASK:\t/*  0x018, Current interrupt mask  */\n"
          "\t\tcrime_interrupt_reassert(d);\n"
          "\t\tbreak;\n")

ENDI = "\t\t\tidata &= ~CRIME_CONTROL_ENDIANESS;\n"
TIMECASE = "\tcase CRIME_TIME:\t/*  0x038  */\n"
REVCASE = "\tcase CRIME_REV:\t\t/*  0x000  */\n"

M = {
    "base": [],
    # claim 1 (deepseek): pre-set/re-arm keyed on an accepted CONTROL write of exactly 0x0200, inserted AFTER the
    # DOG_ENABLE clear block (where the seat believed idata==0x200 is a non-rowed accepted cell).
    "c1_deepseek": [(DOGBLK, DOGBLK + "\t\t\tif (idata == CRIME_CONTROL_DOG_ENABLE)\n\t\t\t\td->warned |= CRIME_W_LEN;\n")],
    # claim 2 (kimi-k3): a declined read answers HARDINT instead of 0.
    "c2_kimik3": [(GOTO, "\t\todata = d->reg[CRIME_HARDINT / sizeof(uint64_t)];\n" + GOTO)],
    # claim 3 (codex): the announce channel becomes debug() at offsets with bit 3 set, fatal() elsewhere.
    "c3_codex_dbg": [(FATAL, "\t\t\t(relative_addr & 8 ? debug : fatal)(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n")],
    # claim 4 (kimi CLI): a re-arm keyed on an ACCEPTED WRITE reaching the INTSTAT/INTMASK arm.
    "c4_kimicli": [(INTARM,
                    "\tcase CRIME_INTSTAT:\t/*  0x010, Current interrupt status  */\n"
                    "\tcase CRIME_INTMASK:\t/*  0x018, Current interrupt mask  */\n"
                    "\t\tif (writeflag == MEM_WRITE)\n\t\t\td->warned = 0;\n"
                    "\t\tcrime_interrupt_reassert(d);\n"
                    "\t\tbreak;\n")],
    # claim 5 (codex): a refused 2-byte store LANDS at offsets with address bit 1 set.
    "c5_codex_b1": [(GOTO,
                     "\t\tif (writeflag == MEM_WRITE && len == 2 && (relative_addr & 2))\n"
                     "\t\t\td->reg[relative_addr / sizeof(uint64_t)] = idata;\n" + GOTO)],
    # ---- batch 2: class siblings (PRETABLE2.out) ----
    "d1_rearm_dog0200": [(ENDI, ENDI + "\t\t\tif (idata == 0 && (memory_readmax64(cpu, data, len) & CRIME_CONTROL_DOG_ENABLE))\n"
                                       "\t\t\t\td->warned = 0;\n")],
    "d2_pre_dog0200": [(ENDI, ENDI + "\t\t\tif (idata == 0 && (memory_readmax64(cpu, data, len) & CRIME_CONTROL_DOG_ENABLE))\n"
                                     "\t\t\t\td->warned |= CRIME_W_LEN;\n")],
    "d3_rearm_wtime": [(TIMECASE, TIMECASE + "\t\tif (writeflag == MEM_WRITE)\n\t\t\td->warned = 0;\n")],
    "d4_pre_wistat": [(INTARM,
                       "\tcase CRIME_INTSTAT:\t/*  0x010, Current interrupt status  */\n"
                       "\tcase CRIME_INTMASK:\t/*  0x018, Current interrupt mask  */\n"
                       "\t\tif (writeflag == MEM_WRITE && relative_addr == CRIME_INTSTAT)\n\t\t\td->warned |= CRIME_W_LEN;\n"
                       "\t\tcrime_interrupt_reassert(d);\n"
                       "\t\tbreak;\n")],
    "d6_chan_len2": [(FATAL, "\t\t\t(len == 2 ? debug : fatal)(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n")],
    "d7_rearm_wrev": [(REVCASE, REVCASE + "\t\tif (writeflag == MEM_WRITE)\n\t\t\td->warned = 0;\n")],
}

if __name__ == "__main__":
    name, path = sys.argv[1], sys.argv[2]
    src = open(path).read()
    for find, repl in M[name]:
        n = src.count(find)
        if n != 1:
            print("MUTANT_TEXT_COUNT %s = %d (want 1)" % (name, n)); sys.exit(1)
        src = src.replace(find, repl)
    open(path, "w").write(src)
    print("MUTANT_APPLIED %s (%d edits)" % (name, len(M[name])))
