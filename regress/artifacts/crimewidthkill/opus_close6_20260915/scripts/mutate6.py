#!/usr/bin/env python3
"""mutate6.py NAME SRC DST -- #529 closing pass 6, Opus seat.  Each find-text must occur EXACTLY ONCE (a missing
find-text is a FAIL, so every mutant also pins the presence of what it edits)."""
import io, sys

LEN8 = "\tif (len == 8) {\n"
LEN4 = "\t} else if (len == 4) {\n"
FATAL = "\t\t\tfatal(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n"
GOTO = "\t\tgoto crime_declined;\n"
GOTOSW = "\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {\n"

M = {
    "base": [],
    # C1 (codex): the accepted 4R at CRIME_CONTROL declined
    "C1_ctl4r": [(LEN4, "\t} else if (len == 4 && (relative_addr != CRIME_CONTROL || writeflag != MEM_READ)) {\n")],
    # C2 (glm): the announce channel keyed on the PROM-window pc
    "C2_chan_win": [(FATAL, "\t\t\t(((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100 ? debug : fatal)"
                            "(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n")],
    # C3 (kimi-k3): pre-set on an accepted access with address bit 7 or 8, before the switch
    "C3p_pre_b78": [(GOTOSW, "\t\tgoto crime_declined;\n\t}\n\n\tif (relative_addr & 0x180)\n"
                             "\t\td->warned |= CRIME_W_LEN;\n\n\tswitch (relative_addr) {\n")],
    # C3r: the re-arm twin
    "C3r_rearm_b78": [(GOTOSW, "\t\tgoto crime_declined;\n\t}\n\n\tif (relative_addr & 0x180)\n"
                               "\t\td->warned = 0;\n\n\tswitch (relative_addr) {\n")],
    # C4 (minimax): a declined read answers relative_addr & 7
    "C4_ans_ra7": [(GOTO, "\t\todata = (relative_addr & 7);\n" + GOTO)],
    # C5 (kimi CLI): a declined read answers idata
    "C5_ans_idata": [(GOTO, "\t\todata = idata;\n" + GOTO)],
    # G1 (own hunt): the 8-byte accept guard narrowed at CRIME_CONTROL (8W and 8R there declined)
    "G1_acc8_ctl": [(LEN8, "\tif (len == 8 && relative_addr != CRIME_CONTROL) {\n")],
    # G2: the 8-byte accept guard narrowed at CRIME_INTSTAT
    "G2_acc8_istat": [(LEN8, "\tif (len == 8 && relative_addr != CRIME_INTSTAT) {\n")],
    # G3: the 4-byte accept guard narrowed at CRIME_TIME
    "G3_acc4_time": [(LEN4, "\t} else if (len == 4 && relative_addr != CRIME_TIME) {\n")],
    # G4: the 4-byte accept guard narrowed at CRIME_REV writes (sw +0x00, swP -- the window's redirect)
    "G4_acc4w_rev": [(LEN4, "\t} else if (len == 4 && (relative_addr != CRIME_REV || writeflag != MEM_WRITE)) {\n")],
    # G5: the 4-byte accept guard narrowed at CRIME_INTMASK writes
    "G5_acc4w_imask": [(LEN4, "\t} else if (len == 4 && (relative_addr != CRIME_INTMASK || writeflag != MEM_WRITE)) {\n")],
    # G6: a SILENT accept-set shrink (a bypass, not guard growth): 8-byte CONTROL skips to the tail, no announce
    "G6_skip8_ctl": [(LEN8, "\tif (len == 8 && relative_addr == CRIME_CONTROL)\n\t\tgoto crime_declined;\n\n" + LEN8)],
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
