LOGS FROM OTHER MEASUREMENTS THAT WERE COPIED INTO THIS DIRECTORY BY MISTAKE.

They were swept in by a `cp /tmp/gxann/*.out /tmp/gxpol/*.out /tmp/gxp5/*.out` that
did not check what it was collecting.  None belongs to #478's kill table, and their
row counts say so plainly:

    _base.out  Mnolatch.out  Mstatic.out    60 rows -- the announce-latch table
    curcmd.out  phaseonly.out               57 rows -- #477's pass-2 mutants

*** THE HAZARD IS NOT UNTIDINESS. ***  A reader who greps this directory for a
baseline finds FOUR different row counts and no way to tell which measurement any
log belongs to.  The `names its log` rule says a claim must cite the artifact that
produced it; that is worth nothing if one directory holds four artifacts and the
citation is a bare filename.

Moved rather than deleted: they are real measurements, and a deleted log cannot be
re-read by someone checking a number.
