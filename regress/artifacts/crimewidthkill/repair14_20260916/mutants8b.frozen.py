#!/usr/bin/env python3
"""mutants8b.py <name> <src> <dst> -- #529 closing pass 8, SUPPLEMENTARY: the CONTROL-4R equivalence measurement.

The contract puts CONTROL 4R in its TEN EQUIVALENT cells on a DERIVATION -- "a 4-byte read at +0x08 takes the HIGH
lane, which is 0 either way".  Table 11's C_ctl4r leg scored 188/188, and the coordinator's deepseek seat showed that
leg is VACUOUS: no post-latch session issues a 4-byte READ at +0x08 at all, so nothing drove the cell.  A derivation
is not a measurement.  This builds the binaries that settle it:

    C_ctl4r      the table-11 cell, re-derived here and cmp'd byte-for-byte against killtable11's own diff
    G_lane_ctl   THE LIVENESS CONTROL: keep the access ACCEPTED and flip which LANE it answers, post-latch.  Base
                 answers the high half of 0x100 (= 0); this answers the low half (= 0x100).  If the probe's new row
                 does not move under THIS, the row does not drive the cell and C_ctl4r's non-difference proves
                 nothing -- which is the exact failure the vacuity floor's clause (c) exists to catch.

Sentinel: APPLIED8B <name> <n edits>."""
import sys

LEN8 = "\tif (len == 8) {\n"
LEN4 = "\t} else if (len == 4) {\n"
LANE_R = "\t\t\tif (relative_addr & 4)\n\t\t\t\todata = (int32_t)odata;\n"
R_ = "writeflag == MEM_READ"
L = "(d->warned & CRIME_W_LEN)"

M = {
    "base": [],
    #  *** THE glm SEAT'S CANDIDATE: the MIRROR of the K-class -- a SILENT bypass conditioned on the latch being
    #  CLEAR, at TIME 4W/4R.  Repair 13 rows that cell ONLY post-latch (`p t4w gap' and `p t4r gap' each open with a
    #  refused lb, which is the entire point of them), and table 10's twelve S_* bypasses never covered TIME 4-byte
    #  at all -- their only TIME cell is 8W.  Closing pass 7 measured this cell guest-visible with NO refusal
    #  anywhere in the sequence, so the cell is known-observable in exactly the state no row occupies. ***
    "G_glm_tim4clear": [(LEN8,
                         "\tif (len == 4 && relative_addr == CRIME_TIME && !%s)\n"
                         "\t\tgoto crime_declined;\n\n" % L + LEN8,
                         1)],
    "C_ctl4r": [(LEN4,
                 "\t} else if (len == 4 && !(%s && (relative_addr == CRIME_CONTROL) &&\n\t    %s)) {\n" % (R_, L),
                 1)],
    "G_lane_ctl": [(LANE_R,
                    "\t\t\tif ((relative_addr & 4) || (relative_addr == CRIME_CONTROL && %s))\n"
                    "\t\t\t\todata = (int32_t)odata;\n" % L,
                    1)],
}


def clr(cell):
    """the MIRROR of the K-form: a SILENT bypass that fires only while the latch is CLEAR.  Same shape as the glm
    seat's mutant, at one (dir, label) cell of the 4-byte arm."""
    return [(LEN8, "\tif (len == 4 && %s && !%s)\n\t\tgoto crime_declined;\n\n" % (cell, L) + LEN8, 1)]


#  *** THE REST OF THE CLASS.  scripts/preclear8.py + scripts/sessrows.py derive it: of the twelve 4-byte cells at a
#  named label, FOUR are driven with the latch CLEAR by `latch x5' (session #40) ALONE, and latch x5's only three
#  rows are `latch x5' / `latch surv' / `latch said' -- two announce COUNTS and a RAM round trip, every one of them
#  blind to a SILENT decline.  glm named one of the four.  A class closure measures all of them. ***
M.update({
    "G_clr_ist4r": clr("%s && relative_addr == CRIME_INTSTAT" % R_),    # guest-visible: skips crime_interrupt_reassert
    "G_clr_ctl4r": clr("%s && relative_addr == CRIME_CONTROL" % R_),    # the class's own NEGATIVE control: equivalent
    "G_clr_imk4r": clr("%s && relative_addr == CRIME_INTMASK" % R_),    # driven by session #20 too -- may be caught
})

#  *** THE codex SEAT'S CELL, at BOTH accepted widths as it asked.  This is a LATCH-SET shrink (the K-form), so it
#  is inside table 11's own half of the product -- but narrowed by an idata bit the guarded body TESTS.  The
#  2026-09-04 generating-set clause makes that the FLOOR, not debt: "at each floor cell, every idata bit the guarded
#  body TESTS is written both clear and set".  Post-latch the probe writes CONTROL with 0x01, 0x0001 and 0x0201 --
#  HARD_RESET (0x800) CLEAR in all three -- and the one session that does write 0x800 (`sw08 halts', session #2)
#  writes it BEFORE any refusal.  So the bit is never set in the latch-SET state at either width. ***
W_ = "writeflag == MEM_WRITE"
RST = "(idata & CRIME_CONTROL_HARD_RESET)"
M.update({
    "K_ctl4w_reset_post": [(LEN4,
                            "\t} else if (len == 4 && !(%s && relative_addr == CRIME_CONTROL && %s &&\n\t    %s)) {\n"
                            % (W_, RST, L), 1)],
    "K_ctl8w_reset_post": [(LEN8,
                            "\tif (len == 8 && !(%s && relative_addr == CRIME_CONTROL && %s &&\n\t    %s)) {\n"
                            % (W_, RST, L), 1)],
})

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
if name not in M:
    print("UNKNOWN MUTANT %s" % name)
    sys.exit(2)
text = open(src, "r", newline="").read()
for find, repl, cnt in M[name]:
    got = text.count(find)
    if got != cnt:
        print("MUTANT %s: anchor occurs %d times, wanted %d -- NOT APPLIED" % (name, got, cnt))
        sys.exit(1)
    text = text.replace(find, repl)
open(dst, "w", newline="").write(text)
print("APPLIED8B %s (%d edit(s))" % (name, len(M[name])))
