#!/usr/bin/env python3
"""mutants529h.py NAME SRC DST -- #529 kill table 8: repair 10 (the kind x label cross, the gate answer, the 2W bit-1
landing, the free-running channel).  Imports table 7's mutator (every earlier mutant by name), the fourth-closing Opus
seat's (exec'd, its M only), and adds eight mutants that SAMPLE the new cross.  Every find-text occurs EXACTLY ONCE."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for t in ("killtable7_20260913", "killtable6_20260913", "killtable5_20260913", "killtable4_20260913",
          "killtable3_20260913", "killtable2_20260913"):
    sys.path.insert(0, os.path.join(HERE, "..", t))
import mutants529g as G                                    # noqa: E402

M = dict(G.M)
_ns = {}
exec(io.open(os.path.join(HERE, "mutants_c4_opus.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
M.update({k: v for k, v in _ns["M"].items() if k != "base"})

FATAL = "\t\t\tfatal(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n"
REVCASE = "\tcase CRIME_REV:\t\t/*  0x000  */\n"
TIMECASE = "\tcase CRIME_TIME:\t/*  0x038  */\n"
DOGCASE = "\tcase CRIME_DOG:\t\t/*  0x030  */\n"
DEFAULT = "\tdefault:\n\t\tif (writeflag==MEM_READ) {\n"
ENDI = "\t\t\tidata &= ~CRIME_CONTROL_ENDIANESS;\n"

M.update({
    "x_pre_dog4w":   [(DOGCASE, DOGCASE + "\t\tif (writeflag == MEM_WRITE && len == 4)\n\t\t\td->warned |= CRIME_W_LEN;\n")],
    "x_rearm_rev8r": [(REVCASE, REVCASE + "\t\tif (writeflag == MEM_READ && len == 8)\n\t\t\td->warned = 0;\n")],
    "x_pre_time4r":  [(TIMECASE, TIMECASE + "\t\tif (writeflag == MEM_READ && len == 4)\n\t\t\td->warned |= CRIME_W_LEN;\n")],
    "x_rearm_ctl8w0200": [(ENDI, ENDI + "\t\t\tif (len == 8 && idata == 0 && (memory_readmax64(cpu, data, len) & "
                                        "CRIME_CONTROL_DOG_ENABLE))\n\t\t\t\td->warned = 0;\n")],
    "x_chan_rev":    [(FATAL, "\t\t\t(relative_addr == CRIME_REV ? debug : fatal)(\"[ crime: unimplemented len=%i at 0x%x "
                              "-- declined.\"\n")],
    "x_chan_write":  [(FATAL, "\t\t\t(writeflag == MEM_WRITE ? debug : fatal)(\"[ crime: unimplemented len=%i at 0x%x "
                              "-- declined.\"\n")],
    "x_rearm_defhi": [(DEFAULT, "\tdefault:\n\t\tif (writeflag == MEM_WRITE && len == 4 && !(relative_addr & 4))\n"
                                "\t\t\td->warned = 0;\n\t\tif (writeflag==MEM_READ) {\n")],
    "x_pre_rev_wp":  [(REVCASE, REVCASE + "\t\tif (writeflag == MEM_WRITE && ((uint32_t)cpu->pc & 0xffffff00) == "
                                          "(uint32_t)0xbfc05100)\n\t\t\td->warned |= CRIME_W_LEN;\n")],
})

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
