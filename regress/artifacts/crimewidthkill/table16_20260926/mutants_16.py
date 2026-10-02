#!/usr/bin/env python3
"""mutants_16.py NAME SRC DST -- #529 table 16: repair 16's regression table.  Six edits, two roles:

  THE L2 CELL THE REPAIR CARRIES (the flagship seat, repair 15 pass 2, fable5_r15p2.md: "L2, the same as the DOG pair")
    H_noresetclear   the CONTROL arm's HARD_RESET branch keeps its test and its CPU stop and loses its CLEAR
                     (table15a_20260926/: the escape against the 218 rows, measured before this table)
  THE DISCLOSED SIBLING
    E_noendianclear  the arm's unconditional ENDIANESS clear deleted (never tested: clause (e) by the same seat --
                     measured here so the disclosure can say it escapes and name its score)
  MEASURED DELTAS FOR THE ADJUDICATORS' RULE QUESTIONS (the pass-2 panel's findings F3 and F4; not owed rows):
    W_istlb          INTSTAT's latch-SET decline skipped for a 1-byte READ only (the width x direction cell no
                     latch-SET row holds: `istat lb' is that session's FIRST refusal) -- glm, kimi-k3, deepseek, grok
    W_imklb          the same at INTMASK
    L_dogclr         the DOG clear skipped once the width latch is SET (glm: "a latch-gated DOG-clear")
    L_rstclr         the HARD_RESET clear skipped once the width latch is SET (the same shape at the sibling bit)

The W_ shapes are repair 14's latch_label() form (mutants_adj.frozen.py) with the label test narrowed to one width and
direction.  Exact-string edits on the BASELINE (the uncommitted #529 working set, dev_sgi_ip32.c 8c1d1545);
MUTANT-TEXT-NOT-FOUND is a hard FAIL.  No double backslash anywhere in this file.
"""
import io, sys

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = io.open(src, encoding="latin-1", newline="").read()

CLOSE_GOTO = "\t\t}\n\t\tgoto crime_declined;\n"
DOG_CLEAR = ("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"
             "\t\t\t\tidata &= ~CRIME_CONTROL_DOG_ENABLE;\n"
             "\t\t\t}\n")
RST_CLEAR = ("\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n"
             "\n"
             "\t\t\t\tidata &= ~CRIME_CONTROL_HARD_RESET;\n"
             "\t\t\t}\n")


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


def latch_cell(cond):
    sub(CLOSE_GOTO,
        ("\t\t\tgoto crime_declined;\n"
         "\t\t}\n"
         "\t\tif (!(" + cond + "))\n"
         "\t\t\tgoto crime_declined;\n"))


if name == "base":
    pass
elif name == "H_noresetclear":
    sub(RST_CLEAR, "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n\n\t\t\t}\n")
elif name == "E_noendianclear":
    sub("\t\t\tidata &= ~CRIME_CONTROL_ENDIANESS;\n\n\t\t\tif (idata != 0)\n", "\t\t\tif (idata != 0)\n")
elif name == "W_istlb":
    latch_cell("relative_addr == CRIME_INTSTAT && len == 1 && writeflag == MEM_READ")
elif name == "W_imklb":
    latch_cell("relative_addr == CRIME_INTMASK && len == 1 && writeflag == MEM_READ")
elif name == "L_dogclr":
    sub(DOG_CLEAR,
        ("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"
         "\t\t\t\tif (!(d->warned & CRIME_W_LEN))\n"
         "\t\t\t\t\tidata &= ~CRIME_CONTROL_DOG_ENABLE;\n"
         "\t\t\t}\n"))
elif name == "L_rstclr":
    sub(RST_CLEAR,
        ("\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n"
         "\n"
         "\t\t\t\tif (!(d->warned & CRIME_W_LEN))\n"
         "\t\t\t\t\tidata &= ~CRIME_CONTROL_HARD_RESET;\n"
         "\t\t\t}\n"))
elif name == "S_rst8clr":
    #  the CHANNEL check for the new `ctlrst sd halt' row: an ACCEPTED 8-byte 0x800 write with the latch CLEAR no longer
    #  stops the CPUs (the dedicated grok seat named this cell "real, and unrowed").  `sw08 halts' is 4-byte and `rst 8w'
    #  runs with the latch SET, so only the new row can see it.
    sub("\t\t\t\tfor (j=0; j<cpu->machine->ncpus; j++)\n"
        "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n",
        "\t\t\t\tif (!(len == 8 && !(d->warned & CRIME_W_LEN)))\n"
        "\t\t\t\tfor (j=0; j<cpu->machine->ncpus; j++)\n"
        "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n")
elif name == "list":
    print("base H_noresetclear E_noendianclear W_istlb W_imklb L_dogclr L_rstclr S_rst8clr")
    sys.exit(0)
else:
    sys.exit("unknown mutant %s" % name)

io.open(dst, "w", encoding="latin-1", newline="").write(s)
print("APPLIED %s" % name)
