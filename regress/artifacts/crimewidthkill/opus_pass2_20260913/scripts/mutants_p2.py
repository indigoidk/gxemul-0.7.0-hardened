#!/usr/bin/env python3
"""mutants_p2.py NAME SRC DST -- #529 pass-2 Opus seat: the post-fix dev_sgi_ip32.c with one mutant applied.

Same discipline as mutants529.py: every find-text must occur EXACTLY ONCE or the script refuses (exit 2).
Baseline = the #529 working set (GXEMUL-SEC/src/devices/dev_sgi_ip32.c md5 5919a5a7...), never HEAD.
Shapes NOT swept by kill table 1: address-conditioned fall-throughs, the tail, the latch/announce, and
accept-arm edits at cells the rows do not reach.
"""
import sys

GOTO = "\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {"
ARM8 = "\tif (len == 8) {\n\t\tif (writeflag == MEM_WRITE)\n\t\t\td->reg[relative_addr / 8] = idata;"
ARM4 = "\t} else if (len == 4) {\n\t\tif (writeflag == MEM_WRITE) {"
LATCH = "\t\tif (!(d->warned & CRIME_W_LEN)) {\n\t\t\td->warned |= CRIME_W_LEN;\n"
ONCE = "\"  (once) ]\\n\", (int) len, (int) relative_addr);"
TAIL = (" crime_declined:\n"
        "\t/*  #529: a declined access jumps here, skipping the register switch,\n"
        "\t    and is still answered.  */\n"
        "\td->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;\n"
        "\td->reg[CRIME_INTSTAT / sizeof(uint64_t)] =\n"
        "\t\t(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |\n"
        "\t\td->reg[CRIME_HARDINT / sizeof(uint64_t)]);\n"
        "\n"
        "\tif (writeflag == MEM_READ)\n"
        "\t\tmemory_writemax64(cpu, data, len, odata);\n"
        "\n"
        "\treturn 1;\n")
SEXT = "\t\t\tif (relative_addr & 4)\n\t\t\t\todata = (int32_t)odata;\n\t\t\telse\n\t\t\t\todata = (int32_t)(odata >> 32);"


def g(repl):
    return GOTO.replace("goto crime_declined;", repl, 1)


M = {
    "base": [],
    # (1) ADDRESS-conditioned fall-throughs into the register switch
    "a_ctl":   [(GOTO, g("if (relative_addr != CRIME_CONTROL) goto crime_declined;"))],
    "a_rev":   [(GOTO, g("if (relative_addr != CRIME_REV) goto crime_declined;"))],
    "a_al8":   [(GOTO, g("if (relative_addr & 7) goto crime_declined;"))],
    "a_lo10":  [(GOTO, g("if (relative_addr < CRIME_INTSTAT) goto crime_declined;"))],
    "a_imask": [(GOTO, g("if (relative_addr != CRIME_INTMASK) goto crime_declined;"))],
    "a_istat": [(GOTO, g("if (relative_addr != CRIME_INTSTAT) goto crime_declined;"))],
    "a_time":  [(GOTO, g("if (relative_addr != CRIME_TIME) goto crime_declined;"))],
    "a_revw":  [(GOTO, g("if (writeflag == MEM_READ || relative_addr != CRIME_REV) goto crime_declined;"))],
    # (3) the tail: label moved below the HARDINT restore / INTSTAT recompute; label moved to the return
    "t_nohint": [(TAIL, TAIL.replace(" crime_declined:\n", "", 1)
                  .replace("\tif (writeflag == MEM_READ)\n", " crime_declined:\n\tif (writeflag == MEM_READ)\n", 1))],
    "t_ret":    [(TAIL, TAIL.replace(" crime_declined:\n", "", 1)
                  .replace("\treturn 1;\n", " crime_declined:\n\treturn 1;\n", 1))],
    # (4) the latch / announce
    "l_noonce":   [(ONCE, "\" ]\\n\", (int) len, (int) relative_addr);")],
    "l_assign":   [(LATCH, "\t\tif (!(d->warned & CRIME_W_LEN)) {\n\t\t\td->warned = CRIME_W_LEN;\n")],
    "l_static":   [(LATCH, "\t\tstatic int w529 = 0;\n\t\tif (!w529) {\n\t\t\tw529 = 1;\n")],
    "l_addrmask": [(ONCE, "\"  (once) ]\\n\", (int) len, (int) (relative_addr & 0x3f));")],
    # (5) accept-arm edits at cells the rows do not reach
    "x_mc4":  [(ARM4, ARM4.replace("len == 4", "len == 4 && relative_addr < 0x200", 1))],
    "x_mc8":  [(ARM8, ARM8.replace("len == 8", "len == 8 && relative_addr < 0x200", 1))],
    "x_sext": [(SEXT, SEXT.replace("(int32_t)", "(uint32_t)"))],
}

if __name__ == "__main__":
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    if name == "list":
        print(" ".join(k for k in M if k != "base"))
        sys.exit(0)
    s = open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n))
            sys.exit(2)
        if repl == find:
            sys.stderr.write("MUTANT %s: replacement identical to find-text\n" % name)
            sys.exit(2)
        s = s.replace(find, repl, 1)
    open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
