#!/usr/bin/env python3
"""mutants529k.py NAME SRC DST -- #529 KILL TABLE 11 (repair 13).

Imports table 10's mutator (every earlier mutant by name) and adds the closing-pass-7 findings plus THE CLASS CLOSURE.

*** THE CLOSURE IS GENERATED FROM THE HANDLER'S OWN CASE LABELS, NOT TRANSCRIBED. ***  The 2026-08-31 class-closure
amendment says: when two consecutive passes find breaches of ONE class, the next repair enumerates the full space FROM
THE FUNCTION'S OWN INPUTS and closes every cell in one diff, and the closing pass then VERIFIES THE ENUMERATION rather
than hunting cells.  Three passes have now found this class (pass 6 the ANNOUNCED accept-guard growth; table 10 the
WIDTH-level latch shrink `W_8r'/`W_8w'; pass 7 the PER-CELL latch shrink K1/K2/K3), so the enumeration is owed.

THE SPACE, read off `DEVICE_ACCESS(crime)' in dev_sgi_ip32.c:

    {latch}     d->warned & CRIME_W_LEN in {clear, set}
                  -- the width dispatch's own `else' arm READS this field (`if (!(d->warned & CRIME_W_LEN))'), and that
                     read is part of the fix's OWN diff.  Whether that makes it a FLOOR axis (the sgimtedepth4dead join
                     ruling) or clause-(e) debt (the ruling's RA3) is the one question still open for the adjudicator.
    {len}       4, 8            -- the two accepted widths; every other width is the declined arm itself
    {dir}       read, write     -- `writeflag'
    {label}     the SEVEN the switch actually distinguishes: CRIME_REV, CRIME_CONTROL, CRIME_INTSTAT, CRIME_INTMASK,
                CRIME_DOG, CRIME_TIME, and `default' (which is where 0x20 SOFTINT, 0x40 and +0x278 land)

    2 x 2 x 2 x 7 = 56 cells.  THE LATCH-CLEAR HALF IS ALREADY MEASURED: table 10's twelve S_* silent bypasses are
    exactly that half at the cells the ruling enumerated, all red.  **The NEW work is the 28 latch-SET cells**, which
    is what K1/K2/K3 are three instances of.

*** DO NOT READ 28 AS THE ROW DEMAND.  MUTANTS AND CELLS ARE DIFFERENT UNITS. ***  One K-form mutant covers a
(len, dir, label) triple that may span several ACCEPTS entries, and the close-7 seat's static session map
(opus_close7_20260915/scripts2/session_map2.py) derives the row side independently: of the 46 ACCEPTS entries 31 are
guest-visible, and 8 of those are ALREADY pinned post-latch, leaving 23.  A mutant at a cell no row reaches is a
measurement that teaches nothing; a row at a cell no mutant reaches is unfalsifiable.  Both lists go in PRETABLE 11
with the CHANNEL line naming, per row, the mutant it kills and the observable that differs -- **and this round's
evidence is that the CHANNEL line must be RUN, not written: the seat's first two TIME shapes were named correctly and
were VACUOUS, and one gave a FALSE RED on a control.**

Every find-text occurs EXACTLY ONCE; the driver treats MUTANT-TEXT-NOT-FOUND as a FAIL, so each find is also a
presence pin on the feature it edits.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for t in ("killtable11_20260916", "killtable10_20260915", "killtable9_20260914"):
    sys.path.insert(0, os.path.join(HERE, "..", t))
import mutants529j as J                                    # noqa: E402

M = dict(J.M)

LEN8 = "\tif (len == 8) {\n"
LEN4 = "\t} else if (len == 4) {\n"
W, R_ = "writeflag == MEM_WRITE", "writeflag == MEM_READ"

#  ---- the three the close-7 seat MEASURED, verbatim (each 157/157 against repair 12) ----------------------------
M.update({
    "K1": [(LEN4, "\t} else if (len == 4 && !(%s &&\n\t    relative_addr == CRIME_INTMASK && (d->warned & CRIME_W_LEN))) {\n" % W)],
    "K2": [(LEN4, "\t} else if (len == 4 && !(relative_addr == CRIME_REV && (d->warned & CRIME_W_LEN))) {\n")],
    "K3": [(LEN8, "\tif (len == 8 && !(%s &&\n\t    relative_addr == CRIME_CONTROL && (d->warned & CRIME_W_LEN))) {\n" % R_)],
    #  codex's TIME mutant, verbatim: the cell item 6 and the ruling's RA1 both called EQUIVALENT and which is
    #  measured guest-visible on four channels.  Killed only by the GAPPED row shape.
    "E2": J.bypass("len == 4 && relative_addr == CRIME_TIME"),
})

#  ---- THE CLOSURE, GENERATED.  28 latch-set cells; the generator IS the enumeration. ---------------------------
LABELS = (("rev", "relative_addr == CRIME_REV"),
          ("ctl", "relative_addr == CRIME_CONTROL"),
          ("ist", "relative_addr == CRIME_INTSTAT"),
          ("imk", "relative_addr == CRIME_INTMASK"),
          ("dog", "relative_addr == CRIME_DOG"),
          ("tim", "relative_addr == CRIME_TIME"),
          #  the `default' arm is the COMPLEMENT of the six, and it is written as one so the mutant cannot be
          #  satisfied by a label the switch already names -- the enumeration's own negative space.
          ("dfl", "relative_addr != CRIME_REV && relative_addr != CRIME_CONTROL &&\n\t    "
                  "relative_addr != CRIME_INTSTAT && relative_addr != CRIME_INTMASK &&\n\t    "
                  "relative_addr != CRIME_DOG && relative_addr != CRIME_TIME"))


def klatch(anchor, head, dir_expr, label_expr):
    """the K-form: keep the width guard, null its repair at ONE cell ONCE THE LATCH HAS FIRED (silent by construction,
    because the announce is what the latch suppresses)"""
    return [(anchor, "%s && !(%s && (%s) &&\n\t    (d->warned & CRIME_W_LEN))) {\n" % (head, dir_expr, label_expr))]


for lab, expr in LABELS:
    for ln, anchor, head in ((8, LEN8, "\tif (len == 8"), (4, LEN4, "\t} else if (len == 4")):
        for d, dex in (("w", W), ("r", R_)):
            name = "C_%s%d%s" % (lab, ln, d)
            if name not in M:                       # K1/K2/K3 are members of this product; do not shadow them
                M[name] = klatch(anchor, head, dex, expr)

#  K2 is the (rev, 4, both-directions) cell -- deliberately NOT direction-split, because that is the form the seat
#  MEASURED.  The generated C_rev4w / C_rev4r are its two halves and are kept: a cell whose two halves are covered
#  separately is not thereby covered jointly, and this table is the one that says so.

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    if sys.argv[1:2] == ["closure"]:                # print the enumeration so PRETABLE 11 can carry it verbatim
        gen = sorted(k for k in M if k.startswith("C_"))
        print("CLOSURE %d cells: %s" % (len(gen), " ".join(gen))); sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n)); sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
