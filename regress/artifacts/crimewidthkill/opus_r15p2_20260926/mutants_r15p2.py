#!/usr/bin/env python3
"""mutants_r15p2.py NAME SRC DST -- #529 repair-15 PASS 2, the Opus measuring seat's candidate escapes.

Exact-string edits on the BASELINE dev_sgi_ip32.c 8c1d1545 (the uncommitted #529 working set).  MUTANT-TEXT-NOT-FOUND is
a hard FAIL.  Two shapes, both built on the SAME anchor table 13a's latch_label() used (CLOSE_GOTO):

  P_<...>  LATCH-SET form (the M3/M5/M6/M7/M8 shape, narrowed): the first refusal (latch CLEAR) is declined inside the
           latch block exactly as before; a LATER refusal (latch SET) falls into the register switch iff COND.
  C_<...>  LATCH-CLEAR form (the mirror): the first refusal announces and falls into the switch iff COND; every later
           refusal (latch SET) is declined.

  census   NOT a mutant: the base with a file log of every CRIME access and every TIME update (for the premise checks).
"""
import io, sys

name = sys.argv[1]
if name != "list":
    src, dst = sys.argv[2], sys.argv[3]
    s = io.open(src, encoding="latin-1", newline="").read()

CLOSE_GOTO = "\t\t}\n\t\tgoto crime_declined;\n"


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


def latch_set(cond):
    sub(CLOSE_GOTO,
        "\t\t\tgoto crime_declined;\n"
        "\t\t}\n"
        "\t\tif (!(" + cond + "))\n"
        "\t\t\tgoto crime_declined;\n")


def latch_clear(cond):
    sub(CLOSE_GOTO,
        "\t\t\tif (!(" + cond + "))\n"
        "\t\t\t\tgoto crime_declined;\n"
        "\t\t} else\n"
        "\t\t\tgoto crime_declined;\n")


MUTS = {
    # latch SET, one width x direction cell: the 1R cell at INTSTAT / INTMASK (the cell PRETABLE14's sibling-parity
    # check named and disposed as clause (e))
    "P_ist1r_set": lambda: latch_set("relative_addr == CRIME_INTSTAT && len == 1 && writeflag == MEM_READ"),
    "P_imk1r_set": lambda: latch_set("relative_addr == CRIME_INTMASK && len == 1 && writeflag == MEM_READ"),
    # latch CLEAR, single-axis narrowings at INTSTAT / INTMASK (no session's FIRST refusal there is anything but lb)
    "C_istW_clr": lambda: latch_clear("relative_addr == CRIME_INTSTAT && writeflag == MEM_WRITE"),
    "C_imk2_clr": lambda: latch_clear("relative_addr == CRIME_INTMASK && len == 2"),
    "C_ist2_clr": lambda: latch_clear("relative_addr == CRIME_INTSTAT && len == 2"),
    "C_imkW_clr": lambda: latch_clear("relative_addr == CRIME_INTMASK && writeflag == MEM_WRITE"),
    # POSITIVE CONTROL for the latch-CLEAR shape: the same construction landing on a ROWED cell (istat lb is the
    # istat session's FIRST refusal), so it must be killed -- if it is not, the C_ escapes above mean nothing
    "C_ist1r_clr": lambda: latch_clear("relative_addr == CRIME_INTSTAT && len == 1 && writeflag == MEM_READ"),
    # latch SET, CONTROL, 2-byte write, HARD_RESET CLEAR (the arm's tested bit, clear side, at the 2W latch-SET cell)
    "P_ctl2wrc_set": lambda: latch_set("relative_addr == CRIME_CONTROL && len == 2 && writeflag == MEM_WRITE"
                                       " && !(idata & CRIME_CONTROL_HARD_RESET)"),
    # latch SET, INTSTAT, only while the line is ALREADY asserted (the reassert's DEASSERT direction)
    "P_istprev_set": lambda: latch_set("relative_addr == CRIME_INTSTAT && d->prev_asserted"),
    # the plain latch-SET label swaps, re-derived here as controls for this file's own shape (identical in effect to
    # M6_istlatch / M7_intmasklatch; not identical in text: `!(relative_addr == L)' vs `relative_addr != L')
    "P_ist_set": lambda: latch_set("relative_addr == CRIME_INTSTAT"),
    "P_imk_set": lambda: latch_set("relative_addr == CRIME_INTMASK"),
    # Q1(d): the CONTROL arm's DOG partition -- the DOG branch's clear conditioned on a second axis
    "D_doglatch": lambda: sub("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n",
                              "\t\t\tif ((idata & CRIME_CONTROL_DOG_ENABLE) && !(d->warned & CRIME_W_LEN)) {\n"),
    "D_dogbit0": lambda: sub("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n",
                             "\t\t\tif ((idata & CRIME_CONTROL_DOG_ENABLE) && !(idata & 1)) {\n"),
    "D_doglen8": lambda: sub("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n",
                             "\t\t\tif ((idata & CRIME_CONTROL_DOG_ENABLE) && len == 8) {\n"),
    # PRETABLE14's own example of `DOG -> stop': the HARD_RESET test widened to DOG|HARD_RESET
    "D_dogstopwiden": lambda: sub("\t\t\tif (idata & CRIME_CONTROL_HARD_RESET) {\n",
                                  "\t\t\tif (idata & (CRIME_CONTROL_HARD_RESET | CRIME_CONTROL_DOG_ENABLE)) {\n"),
}


def census():
    sub("#include <sys/time.h>\n", "#include <sys/time.h>\n#include <unistd.h>\n")
    sub("DEVICE_TICK(crime)\n{\n\tstruct crime_data *d = (struct crime_data *) extra;\n\n"
        "\tcrime_update_crime_time(d);\n",
        "DEVICE_TICK(crime)\n{\n\tstruct crime_data *d = (struct crime_data *) extra;\n\n"
        "\tcensus_in_tick = 1;\n\tcrime_update_crime_time(d);\n\tcensus_in_tick = 0;\n")
    sub("void crime_update_crime_time(struct crime_data* d)\n{\n",
        "static int census_in_tick = 0;\n"
        "static FILE *census_fp(void)\n{\n"
        "\tstatic FILE *f = NULL;\n"
        "\tif (f == NULL) {\n"
        "\t\tf = fopen(\"/tmp/gxopus_r15p2_census.log\", \"a\");\n"
        "\t\tif (f != NULL)\n\t\t\tsetvbuf(f, NULL, _IOLBF, 0);\n"
        "\t}\n\treturn f;\n}\n\n"
        "void crime_update_crime_time(struct crime_data* d)\n{\n"
        "\tuint64_t census_t0 = d->reg[CRIME_TIME / sizeof(uint64_t)];\n"
        "\tuint64_t census_l0 = d->last_microseconds;\n")
    sub("\t\td->last_microseconds = microseconds;\n\t}\n}\n",
        "\t\td->last_microseconds = microseconds;\n\t}\n"
        "\tif (census_fp() != NULL)\n"
        "\t\tfprintf(census_fp(), \"T %d %s last0=%llu now=%llu t0=%llu t1=%llu\\n\", (int) getpid(),\n"
        "\t\t    census_in_tick ? \"tick\" : \"acc\", (unsigned long long) census_l0,\n"
        "\t\t    (unsigned long long) microseconds, (unsigned long long) census_t0,\n"
        "\t\t    (unsigned long long) d->reg[CRIME_TIME / sizeof(uint64_t)]);\n"
        "}\n")
    sub("\tif (writeflag == MEM_WRITE)\n\t\tidata = memory_readmax64(cpu, data, len);\n\n\t/*\n\t *  Set crime",
        "\tif (writeflag == MEM_WRITE)\n\t\tidata = memory_readmax64(cpu, data, len);\n\n"
        "\tif (census_fp() != NULL)\n"
        "\t\tfprintf(census_fp(), \"A %d %c len=%d rel=0x%x idata=0x%llx latch=%d prev=%d soft=0x%llx \"\n"
        "\t\t    \"mask=0x%llx hard=0x%llx time=0x%llx pc=0x%llx\\n\", (int) getpid(),\n"
        "\t\t    writeflag == MEM_WRITE ? 'W' : 'R', (int) len, (int) relative_addr,\n"
        "\t\t    (unsigned long long) idata, !!(d->warned & CRIME_W_LEN), d->prev_asserted,\n"
        "\t\t    (unsigned long long) d->reg[CRIME_SOFTINT / sizeof(uint64_t)],\n"
        "\t\t    (unsigned long long) d->reg[CRIME_INTMASK / sizeof(uint64_t)],\n"
        "\t\t    (unsigned long long) d->reg[CRIME_HARDINT / sizeof(uint64_t)],\n"
        "\t\t    (unsigned long long) d->reg[CRIME_TIME / sizeof(uint64_t)],\n"
        "\t\t    (unsigned long long) cpu->pc);\n\n"
        "\t/*\n\t *  Set crime")


if name == "base":
    pass
elif name == "census":
    census()
elif name == "list":
    print(" ".join(["base", "census"] + sorted(MUTS)))
    sys.exit(0)
elif name in MUTS:
    MUTS[name]()
else:
    sys.exit("unknown mutant %s" % name)

io.open(dst, "w", encoding="latin-1", newline="").write(s)
print("APPLIED %s" % name)
