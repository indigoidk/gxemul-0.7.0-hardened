#!/usr/bin/env python3
"""#529 CLOSING PASS 3 (Opus seat) -- mutants of dev_sgi_ip32.c aimed at the CLASS ENUMERATIONS the repair claims closed.
usage: mutants_c3.py <name> <file>   (edits in place; every find-text must occur EXACTLY once, else exit 1)
Predictions: PRETABLE.out (written before any build).
"""
import sys

GOTO = "\t\tgoto crime_declined;\n"
CTLCASE = "\tcase CRIME_CONTROL:\t/*  0x008  */\n"
DOGIF = ("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"
         "\t\t\t\tidata &= ~CRIME_CONTROL_DOG_ENABLE;\n"
         "\t\t\t}\n")
TXT = ("\t\t\tif (idata != 0)\n"
       "\t\t\t\tfatal(\"[ CRIME_CONTROL: unimplemented \"\n"
       "\t\t\t\t    \"control 0x%016llx ]\\n\", (long long)idata);\n")
ISTAT = "\tcase CRIME_INTSTAT:\t/*  0x010, Current interrupt status  */\n"
REVBR = "\t\t\tcpu->pc = cpu->cd.mips.gpr[MIPS_GPR_RA];\n"
LTEST = "\t\tif (!(d->warned & CRIME_W_LEN)) {\n"


def g(stmt):
    return [(GOTO, "\t\t" + stmt + "\n" + GOTO)]


M = {
    "base": [],
    "rearm_ctlrd": [(CTLCASE, CTLCASE + "\t\tif (writeflag == MEM_READ) d->warned = 0;\n")],
    "rearm_dogclr": [(DOGIF, DOGIF[:-1] + " else\n\t\t\t\td->warned = 0;\n")],
    "rearm_ctl0": [(TXT, TXT + "\t\t\telse\n\t\t\t\td->warned = 0;\n")],
    "pre_istat": [(ISTAT, ISTAT + "\t\td->warned |= CRIME_W_LEN;\n")],
    "pre_revbr": [(REVBR, REVBR + "\t\t\td->warned |= CRIME_W_LEN;\n")],
    "pre_dogbr": [(DOGIF, DOGIF.replace("\t\t\t}\n", "\t\t\t\td->warned |= CRIME_W_LEN;\n\t\t\t}\n"))],
    "byp_rev": [(LTEST, "\t\tif (!(d->warned & CRIME_W_LEN) || relative_addr == CRIME_REV) {\n")],
    "byp_time": [(LTEST, "\t\tif (!(d->warned & CRIME_W_LEN) || relative_addr == CRIME_TIME) {\n")],
    "ans_hi32_b5": g("if (!(relative_addr & 0x20)) odata = d->reg[relative_addr / 8] >> 32;"),
    "land_b4clr": g("if (writeflag == MEM_WRITE && !(relative_addr & 0x10)) d->reg[relative_addr / 8] = idata;"),
    "ans_ctl_lb": g("if (len == 1 && relative_addr == CRIME_CONTROL) odata = 1;"),
    "pre_ctlrd": [(CTLCASE, CTLCASE + "\t\tif (writeflag == MEM_READ) d->warned |= CRIME_W_LEN;\n")],
}

if __name__ == "__main__":
    name, path = sys.argv[1], sys.argv[2]
    src = open(path).read()
    for find, repl in M[name]:
        n = src.count(find)
        if n != 1:
            print("MUTANT_TEXT_COUNT %s = %d (want 1)" % (name, n))
            sys.exit(1)
        src = src.replace(find, repl)
    open(path, "w").write(src)
    print("MUTANT_APPLIED %s (%d edits)" % (name, len(M[name])))
