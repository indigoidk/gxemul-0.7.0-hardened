#!/usr/bin/env python3
"""mutants529.py NAME SRC DST -- write the #529 post-fix dev_sgi_ip32.c with one mutant applied.

Every find-text must occur EXACTLY ONCE in the source, or the script refuses (a mutant whose text is not found is a
FAIL, never a silent no-op -- so each mutant also pins the presence of what it edits).  Baseline = the #529 working
set (GXEMUL-SEC/src/devices/dev_sgi_ip32.c with the fix), never HEAD.
"""
import sys

GOTO = "\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {"
ARM8 = "\tif (len == 8) {\n\t\tif (writeflag == MEM_WRITE)\n\t\t\td->reg[relative_addr / 8] = idata;"
ARM4 = "\t} else if (len == 4) {\n\t\tif (writeflag == MEM_WRITE) {"
LATCH_SET = "\t\t\td->warned |= CRIME_W_LEN;\n"
LATCH_TEST = "\t\tif (!(d->warned & CRIME_W_LEN)) {"
FMT_ARGS = "(int) len, (int) relative_addr);"
DECL_BODY = ("\t\tif (!(d->warned & CRIME_W_LEN)) {\n"
             "\t\t\td->warned |= CRIME_W_LEN;\n"
             "\t\t\tfatal(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n"
             "\t\t\t    \"  (once) ]\\n\", (int) len, (int) relative_addr);\n"
             "\t\t}\n"
             "\t\tgoto crime_declined;\n")


def g(repl):
    return GOTO.replace("goto crime_declined;", repl, 1)


def a4(cond):
    return ARM4.replace("len == 4", "len == 4 && " + cond, 1)


M = {
    "base":     [],
    # floor (b): the removed kill, verbatim, at the width arm
    "revert":   [(DECL_BODY, "\t\tfatal(\"crime access len = %i!\\n\", len);\n\t\texit(1);\n")],
    # member 5: FAULT
    "fault":    [(GOTO, g("return 0;"))],
    # death with status 0 after the announce (the exit0oracle shape)
    "exit0":    [(GOTO, g("exit(0);"))],
    # fall-through into the register switch, whole and per cell
    "fallsw":   [(GOTO, g("/* goto crime_declined; */"))],
    "len1only": [(GOTO, g("if (len == 1) goto crime_declined;"))],
    "len2only": [(GOTO, g("if (len == 2) goto crime_declined;"))],
    "readonly": [(GOTO, g("if (writeflag == MEM_READ) goto crime_declined;"))],
    "wronly":   [(GOTO, g("if (writeflag == MEM_WRITE) goto crime_declined;"))],
    # disclosed EQUIVALENT (memory_rw pre-zeroes the read buffer, #95)
    "return1":  [(GOTO, g("return 1;"))],
    # latch
    "nolatch":  [(LATCH_SET, "")],
    "latchinv": [(LATCH_TEST, "\t\tif (d->warned & CRIME_W_LEN) {")],
    # announce text (contract 6)
    "fmtswap":  [(FMT_ARGS, "(int) relative_addr, (int) len);")],
    # accept-set growth, one cell each (de-escalation clause)
    "acc8w":    [(ARM8, ARM8.replace("len == 8", "len == 8 && writeflag == MEM_READ", 1))],
    "acc8r":    [(ARM8, ARM8.replace("len == 8", "len == 8 && writeflag == MEM_WRITE", 1))],
    "acc4wlo":  [(ARM4, a4("!(writeflag == MEM_WRITE && (relative_addr & 4))"))],
    "acc4whi":  [(ARM4, a4("!(writeflag == MEM_WRITE && !(relative_addr & 4))"))],
    "acc4rlo":  [(ARM4, a4("!(writeflag == MEM_READ && (relative_addr & 4))"))],
    "acc4rhi":  [(ARM4, a4("!(writeflag == MEM_READ && !(relative_addr & 4))"))],
}

if __name__ == "__main__":
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    if name == "list":
        print(" ".join(M))
        sys.exit(0)
    s = open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n))
            sys.exit(2)
        s = s.replace(find, repl, 1)
    open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
