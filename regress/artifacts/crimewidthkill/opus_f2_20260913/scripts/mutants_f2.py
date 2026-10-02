#!/usr/bin/env python3
"""mutants_f2.py NAME SRC DST -- #529 F2 adjudication pass, Opus seat: the post-fix dev_sgi_ip32.c with one mutant.

Every find-text must occur EXACTLY ONCE or the script refuses (exit 2).  Baseline = GXEMUL-SEC working set
(md5 8c1d1545eeddd12fd49f52ccede60262, the file kill table 2 measured).
"""
import sys

GOTO = "\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {"
SET = "\t\t\td->warned |= CRIME_W_LEN;\n"
BRACE = ("(int) len, (int) relative_addr);\n\t\t}\n\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {")


def g(repl):
    return GOTO.replace("goto crime_declined;", repl, 1)


M = {
    "base": [],
    # spot-checks of the pass-2 seat's own escapes against the shipped 71-row detector
    "a_lo10":  [(GOTO, g("if (relative_addr < CRIME_INTSTAT) goto crime_declined;"))],
    "a_imask": [(GOTO, g("if (relative_addr != CRIME_INTMASK) goto crime_declined;"))],
    # width x label joints the repair did not row (it rowed lb/sb only at 0x10/0x18/0x38)
    "h_imask": [(GOTO, g("if (len == 1 || relative_addr != CRIME_INTMASK) goto crime_declined;"))],
    "h_lbl":   [(GOTO, g("if (len == 1 || (relative_addr != CRIME_INTSTAT && relative_addr != CRIME_INTMASK"
                         " && relative_addr != CRIME_TIME)) goto crime_declined;"))],
    # latch shapes
    "lt_len":  [(SET, "\t\t\td->warned |= len;\n")],
    "lt_addr": [(SET, "\t\t\td->warned |= relative_addr;\n")],
    "lt_wset": [(SET, "\t\t\td->warned |= CRIME_W_LEN << writeflag;\n")],
    "l_brace": [(BRACE, "(int) len, (int) relative_addr);\n\t\t\tgoto crime_declined;\n\t\t}\n\t}\n\n"
                        "\tswitch (relative_addr) {")],
    # label x idata-bit joint: fall through at CRIME_CONTROL only when the write carries DOG_ENABLE (the CONTROL arm
    # TESTS that bit; no refused row ever writes it set)
    "c_dog":   [(GOTO, g("if (relative_addr != CRIME_CONTROL || !(idata & CRIME_CONTROL_DOG_ENABLE))"
                         " goto crime_declined;"))],
    # fall-through at an unlabelled, unrowed offset (the default arm)
    "sft":     [(GOTO, g("if (relative_addr != CRIME_SOFTINT) goto crime_declined;"))],
    # a refused store that LANDS, narrowed to memory control (the keeps rows sit at CRIME_DOG only)
    "wst_mc":  [(GOTO, g("if (writeflag == MEM_WRITE && relative_addr >= 0x200) d->reg[relative_addr / 8] = idata;"
                         " goto crime_declined;"))],
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
