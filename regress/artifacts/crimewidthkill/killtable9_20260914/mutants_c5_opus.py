#!/usr/bin/env python3
"""mutate2.py NAME SRC DST -- panel (P1..P7) mutants for Opus close-5.  Each find-text must occur EXACTLY ONCE."""
import io, sys

REVCASE = "\tcase CRIME_REV:\t\t/*  0x000  */\n"
PCLINE = "\t\t\tcpu->pc = cpu->cd.mips.gpr[MIPS_GPR_RA];\n"
ENDI = "\t\t\tidata &= ~CRIME_CONTROL_ENDIANESS;\n"
FATAL = "\t\t\tfatal(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n"
GOTO = "\t\tgoto crime_declined;\n"
WLINE = "\t\t\td->warned |= CRIME_W_LEN;\n"
GOTOSW = "\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {\n"

M = {
    "base": [],
    # P1: re-arm inside the PROM-window if, keyed on 8R (ldP -- absent from ACCEPTS)
    "P1_win8r_rearm": [(PCLINE, "\t\t\tif (len == 8 && writeflag == MEM_READ) d->warned = 0;\n" + PCLINE)],
    # P1b: pre-set twin
    "P1b_win8r_preset": [(PCLINE, "\t\t\tif (len == 8 && writeflag == MEM_READ) d->warned |= CRIME_W_LEN;\n" + PCLINE)],
    # P2: re-arm on an accepted CONTROL write carrying ENDIANESS (0x100)
    "P2_ctl_endi_rearm": [(ENDI, "\t\t\tif (idata & CRIME_CONTROL_ENDIANESS) d->warned = 0;\n" + ENDI)],
    # P2b: pre-set twin
    "P2b_ctl_endi_preset": [(ENDI, "\t\t\tif (idata & CRIME_CONTROL_ENDIANESS) d->warned |= CRIME_W_LEN;\n" + ENDI)],
    # P3: channel joint -- INTSTAT and len==2 -> debug
    "P3_chan_istat2": [(FATAL, "\t\t\t(relative_addr == CRIME_INTSTAT && len == 2 ? debug : fatal)(\"[ crime: "
                               "unimplemented len=%i at 0x%x -- declined.\"\n")],
    # P4: answer source = SOFTINT
    "P4_ans_softint": [(GOTO, "\t\todata = d->reg[CRIME_SOFTINT / sizeof(uint64_t)];\n" + GOTO)],
    # P5: answer source = use_fb (machine config, 0 here)
    "P5_ans_usefb": [(GOTO, "\t\todata = d->use_fb;\n" + GOTO)],
    # P6: pre-set on an accepted READ, in the accepted path before the switch
    "P6_pre_read_accpath": [(GOTOSW, "\t\tgoto crime_declined;\n\t}\n\n\tif (writeflag == MEM_READ)\n"
                                     "\t\td->warned |= CRIME_W_LEN;\n\n\tswitch (relative_addr) {\n")],
    # P7: latch bit shifted by address parity
    "P7_latch_addrparity": [(WLINE, "\t\t\td->warned |= CRIME_W_LEN << (relative_addr & 1);\n")],
}

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n)); sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
