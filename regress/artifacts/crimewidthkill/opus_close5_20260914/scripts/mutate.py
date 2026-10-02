#!/usr/bin/env python3
"""mutate.py NAME SRC DST -- apply one Opus close-5 mutant.  Each find-text must occur EXACTLY ONCE."""
import io, sys

REVCASE = "\tcase CRIME_REV:\t\t/*  0x000  */\n"
DOGCASE = "\tcase CRIME_DOG:\t\t/*  0x030  */\n"
DEFAULT = "\tdefault:\n\t\tif (writeflag==MEM_READ) {\n"
FATAL = "\t\t\tfatal(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n"
GOTO = "\t\tgoto crime_declined;\n"

M = {
    "base": [],
    # candidate GAP: re-arm INSIDE the REV pc-window branch keyed on an 8R (ldP) -- ACCEPTS has no 8R-from-window.
    "j_win8r": [(REVCASE, REVCASE +
                 "\t\tif (((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100 && len == 8 && writeflag == MEM_READ)\n"
                 "\t\t\td->warned = 0;\n")],
    # novel single-axis: notice channel keyed on the DOG label (table 8 did chan_rev, not chan_dog).
    "n_chan_dog": [(FATAL, "\t\t\t(relative_addr == CRIME_DOG ? debug : fatal)(\"[ crime: unimplemented len=%i at 0x%x "
                           "-- declined.\"\n")],
    # novel answer-source: a refused read answers relative_addr (no pass built this exact source).
    "n_ans_ra": [(GOTO, "\t\todata = relative_addr;\n" + GOTO)],
    # novel: re-arm on a default-arm 4W in the LOW lane (table 8 did rearm_defhi = HIGH lane).
    "n_rearm_deflo": [(DEFAULT, "\tdefault:\n\t\tif (writeflag == MEM_WRITE && len == 4 && (relative_addr & 4))\n"
                                "\t\t\td->warned = 0;\n\t\tif (writeflag==MEM_READ) {\n")],
    # novel answer-source: a refused read answers len (1 or 2), caught at +0x07.
    "n_ans_len": [(GOTO, "\t\todata = len;\n" + GOTO)],
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
