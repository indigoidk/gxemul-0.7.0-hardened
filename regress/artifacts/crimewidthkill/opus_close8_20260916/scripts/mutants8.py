#!/usr/bin/env python3
"""mutants8.py <name> <src> <dst> -- #529 CLOSING PASS 8 (Opus measuring seat).

Each mutant is a list of (FIND, REPLACE, COUNT) applied to the BASELINE source.  A FIND that is not present
exactly COUNT times is a hard failure, so every mutant additionally PINS the text it edits (the multi-part rule's
presence-pin property).  Sentinel printed: APPLIED8 <name> <n edits>."""
import sys

LEN8 = "\tif (len == 8) {\n"
LEN4 = "\t} else if (len == 4) {\n"
#  the READ-side lane test, :291-294 -- `relative_addr & 4' is a partition the guarded body's OWN code induces
LANE_R = "\t\t\tif (relative_addr & 4)\n\t\t\t\todata = (int32_t)odata;\n"
#  the decline arm's tail, :318-319
DECL = "\t\t}\n\t\tgoto crime_declined;\n"
REGIX = "d->reg[relative_addr / 8]"

W, R_ = "writeflag == MEM_WRITE", "writeflag == MEM_READ"
L = "(d->warned & CRIME_W_LEN)"
DFL = ("relative_addr != CRIME_REV && relative_addr != CRIME_CONTROL &&\n\t    "
       "relative_addr != CRIME_INTSTAT && relative_addr != CRIME_INTMASK &&\n\t    "
       "relative_addr != CRIME_DOG && relative_addr != CRIME_TIME")
WIN = "((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100"


def k8(dir_expr, cell):
    return [(LEN8, "\tif (len == 8 && !(%s && (%s) &&\n\t    %s)) {\n" % (dir_expr, cell, L), 1)]


def k4(dir_expr, cell):
    return [(LEN4, "\t} else if (len == 4 && !(%s && (%s) &&\n\t    %s)) {\n" % (dir_expr, cell, L), 1)]


def laneflip(extra):
    return [(LANE_R, "\t\t\tif ((relative_addr & 4) || (%s))\n\t\t\t\todata = (int32_t)odata;\n" % extra, 1)]


M = {
    "base": [],

    # ---- GROUP L: the LANE, a body-tested partition of `relative_addr' the enumeration does not name.
    #      Satisfiable only at the default arm (the six case labels are all 8-aligned). ----
    "L_dfl4w_hi": k4(W, "!(relative_addr & 4) && " + DFL),
    "L_dfl4w_lo": k4(W, "(relative_addr & 4) && " + DFL),
    "L_dfl4r_hi": k4(R_, "!(relative_addr & 4) && " + DFL),
    "L_dfl4r_lo": k4(R_, "(relative_addr & 4) && " + DFL),

    # ---- GROUP W: the REV PROM-probe window, a body-tested partition of `cpu->pc'.  W_rev8r_out is the POSITIVE
    #      CONTROL: without it a clean sweep on the other three cannot be told from an unsatisfiable predicate. ----
    "W_rev8r_out": k8(R_, "relative_addr == CRIME_REV && !(%s)" % WIN),
    "W_rev8w_out": k8(W, "relative_addr == CRIME_REV && !(%s)" % WIN),
    "W_rev4w_out": k4(W, "relative_addr == CRIME_REV && !(%s)" % WIN),
    "W_rev4r_out": k4(R_, "relative_addr == CRIME_REV && !(%s)" % WIN),

    # ---- GROUP G: a latch-keyed LANE FLIP on the 4-byte READ.  The access stays ACCEPTED (the switch arm still
    #      runs, so every side-effect row is undisturbed); only the HALF returned changes. ----
    "G_lane_ist": laneflip("relative_addr == CRIME_INTSTAT && " + L),
    "G_lane_tim": laneflip("relative_addr == CRIME_TIME && " + L),
    "G_lane_all": laneflip(L),                       # NEGATIVE CONTROL for the two above

    # ---- GROUP D: two latch-keyed shapes whose only rows may be measured with the latch CLEAR ----
    "D1_landpost": [(DECL, "\t\t} else if (writeflag == MEM_WRITE)\n\t\t\td->reg[relative_addr / 8] = idata;\n"
                           "\t\tgoto crime_declined;\n", 1)],
    "D2_remappost": [(LEN8, "\tsize_t crime_ra8 = ((d->warned & CRIME_W_LEN) ?\n"
                            "\t    (relative_addr & 0x3f) : relative_addr) / 8;\n" + LEN8, 1),
                     (REGIX, "d->reg[crime_ra8]", 7)],
}

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
if name not in M:
    print("UNKNOWN MUTANT %s" % name)
    sys.exit(2)
text = open(src, "r", newline="").read()
for find, repl, cnt in M[name]:
    got = text.count(find)
    if got != cnt:
        print("MUTANT %s: anchor occurs %d times, wanted %d -- NOT APPLIED\n---\n%s\n---" % (name, got, cnt, find))
        sys.exit(1)
    text = text.replace(find, repl)
open(dst, "w", newline="").write(text)
print("APPLIED8 %s (%d edit(s))" % (name, len(M[name])))
