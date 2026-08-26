# `wdcflood` kill table 1 — 14 rows. SUPERSEDED, preserved as evidence.

Measured against the **14-row** `wdc_flood_probe.py`, before pass 2 forced seven more
rows. Cited numbers from this table are only meaningful against 14 as the denominator.

    base 14/14   Mb1 12/14   M1 12/14   M2 11/14
    M3   13/14   M4  13/14   M5 13/14   M6 14/14  <-- ESCAPED

**`M6` is why table 2 exists.** It swaps the latch operand for the guest-resettable
`d->seccnt`, and every row here fires its site twice with nothing in between, so
nothing ever puts the operand back and the mutant looks latched. A seat predicted it on
pass 2; this table measured it.

The other seven all died where intended, and three died on ONE row each — `M3` on
`unimpl 2op`, `M4` on `abrt 2nd`, `M5` on `overread -1`. Those rows exist for exactly
those escapes and nothing else covers them.

Preserved under a stamped directory because the driver reuses `probe_<mutant>.raw` on
every run: a record citing a reused name is true only until the next run, and then it
is worse than uncited, because the named log says something else.
