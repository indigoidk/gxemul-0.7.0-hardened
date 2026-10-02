#!/usr/bin/env python3
"""apply_variant.py <variant> <src_in> <src_out>

Builds one candidate disposition of the crimewidthkill guard in DEVICE_ACCESS(crime).
variants:
  fault    member 5: `return 0;' in place of fatal()+exit(1) -> memory_rw raises EXCEPTION_DBE
  decline  member 3: latched (once) announce, then SKIP the switch and reach the common tail (odata stays 0)
  delete   member 1: remove the else-arm entirely, so a narrow access falls into the switch with no store/load
Each replacement must match exactly once or the script fails (a missing find-text is a FAIL, never a no-op).
"""
import sys

variant, src_in, src_out = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src_in).read()

GUARD = (
    "\t} else {\n"
    "\t\tfatal(\"crime access len = %i!" + chr(92) + "n\", len);\n"
    "\t\texit(1);\n"
    "\t}\n"
)
TAIL = "\td->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;\n"
FIELD = "\tint\t\t\tuse_fb;\n};\n"


def rep(s, old, new):
    n = s.count(old)
    if n != 1:
        sys.stderr.write("FIND-TEXT count %d (want 1) for: %r\n" % (n, old[:60]))
        sys.exit(3)
    return s.replace(old, new)


if variant == "fault":
    s = rep(s, GUARD,
            "\t} else {\n"
            "\t\treturn 0;\n"
            "\t}\n")
elif variant == "decline":
    s = rep(s, FIELD, "\tint\t\t\tuse_fb;\n\tint\t\t\twarned_len;\n};\n")
    s = rep(s, GUARD,
            "\t} else {\n"
            "\t\tif (!d->warned_len) {\n"
            "\t\t\td->warned_len = 1;\n"
            "\t\t\tfatal(\"[ sgi_crime: unimplemented len=%i -- declined.  (once) ]" + chr(92) + "n\", (int) len);\n"
            "\t\t}\n"
            "\t\tgoto crime_common_tail;\n"
            "\t}\n")
    s = rep(s, TAIL, "crime_common_tail:\n" + TAIL)
elif variant == "return1":
    # candidate MUTANT of `decline': same latch, but `return 1;' skips the common tail instead of reaching it
    s = rep(s, FIELD, "\tint\t\t\tuse_fb;\n\tint\t\t\twarned_len;\n};\n")
    s = rep(s, GUARD,
            "\t} else {\n"
            "\t\tif (!d->warned_len) {\n"
            "\t\t\td->warned_len = 1;\n"
            "\t\t\tfatal(\"[ sgi_crime: unimplemented len=%i -- declined.  (once) ]" + chr(92) + "n\", (int) len);\n"
            "\t\t}\n"
            "\t\treturn 1;\n"
            "\t}\n")
elif variant == "fallsw":
    # candidate MUTANT of `decline': same latch, but NO goto -- the refused access falls into the switch
    s = rep(s, FIELD, "\tint\t\t\tuse_fb;\n\tint\t\t\twarned_len;\n};\n")
    s = rep(s, GUARD,
            "\t} else {\n"
            "\t\tif (!d->warned_len) {\n"
            "\t\t\td->warned_len = 1;\n"
            "\t\t\tfatal(\"[ sgi_crime: unimplemented len=%i -- declined.  (once) ]" + chr(92) + "n\", (int) len);\n"
            "\t\t}\n"
            "\t}\n")
elif variant == "nolatch":
    # candidate MUTANT of `decline': the latch is never set, so every refused access announces
    s = rep(s, FIELD, "\tint\t\t\tuse_fb;\n\tint\t\t\twarned_len;\n};\n")
    s = rep(s, GUARD,
            "\t} else {\n"
            "\t\tif (!d->warned_len) {\n"
            "\t\t\tfatal(\"[ sgi_crime: unimplemented len=%i -- declined.  (once) ]" + chr(92) + "n\", (int) len);\n"
            "\t\t}\n"
            "\t\tgoto crime_common_tail;\n"
            "\t}\n")
    s = rep(s, TAIL, "crime_common_tail:\n" + TAIL)
elif variant in ("len1only", "readonly"):
    # clause-(d) MUTANTS of `decline': the decline is CONDITIONED on one width / one direction; the other
    # cells fall into the switch with no store and no load (delete-shaped for those cells)
    cond = "len == 1" if variant == "len1only" else "writeflag == MEM_READ"
    s = rep(s, FIELD, "\tint\t\t\tuse_fb;\n\tint\t\t\twarned_len;\n};\n")
    s = rep(s, GUARD,
            "\t} else if (" + cond + ") {\n"
            "\t\tif (!d->warned_len) {\n"
            "\t\t\td->warned_len = 1;\n"
            "\t\t\tfatal(\"[ sgi_crime: unimplemented len=%i -- declined.  (once) ]" + chr(92) + "n\", (int) len);\n"
            "\t\t}\n"
            "\t\tgoto crime_common_tail;\n"
            "\t}\n")
    s = rep(s, TAIL, "crime_common_tail:\n" + TAIL)
elif variant == "delete":
    s = rep(s, GUARD, "\t}\n")
else:
    sys.stderr.write("unknown variant\n")
    sys.exit(2)

open(src_out, "w").write(s)
print("APPLIED %s" % variant)
