# A DETECTOR ROW THAT COULD NOT FAIL -- found by asking why a mutant would not die

## What happened
`mnolatch` (the clause-(d) form: keep the latch TEST, delete the `d->warned |=`
that sets it, so the decline announces every time) scored **14/14 -- a clean
sweep** against a detector whose `msg once` row exists precisely to catch it.

Three explanations are possible (carrier): the mutant is mis-built, the target
is dead, or the row is mis-cut.  Each was checked rather than guessed:

  * MIS-BUILT?  No.  `diff` of the generated sources shows exactly the two
    `d->warned |= ...;` lines removed, and all nine variant binaries have
    DISTINCT md5s with clean build logs.
  * TARGET DEAD?  No.  Measured directly: three unmapped writes give
    `fix` -> 1 message, `mnolatch` -> 3.
  * ROW MIS-CUT?  **Yes**, and the cause was in the instrument.

## The instrument bug
`gxprobe.Emu` caches register assignments and skips redundant ones.  `step'
advances pc, but the cache still holds the OLD pc.  A driver that calls
`send("step")` DIRECTLY -- instead of going through gxprobe's `_exec_at()`,
which pops the stale pc -- therefore has its SECOND `set_reg("pc", a)` silently
SKIPPED whenever the same instruction word is reused.

The transcript is unambiguous: the first access has a `pc=' line, the second
and third have none, and they execute
    ffffffff80010044: 00000000   nop
    ffffffff80010048: 00000000   nop
So the row performed ONE device access and two nops.  It could not count to
two, so it could not fail.

Note it bit only rows reusing ONE instruction word: `latch fresh' uses `sw'
then `sd', which are different words at different pool addresses, so its pc
assignment was a cache MISS and that row worked -- which is why eight of nine
variants scored plausibly and nothing looked wrong.

## Why this is worth reporting
It is the carrier's check-that-cannot-fail class, in a probe rather than in
prose, and it was invisible to every score: a vacuous row reads exactly like a
passing row.  What surfaced it was a mutant that refused to die -- the
"a mutant that will not die is a RESULT, not noise" rule paying for itself.

## The fix
    e._reg_cache.pop("pc", None)      # before set_reg("pc", ...)
    ...
    e._reg_cache.pop("pc", None)      # after send("step")

## The general rule for this harness
**Any driver that steps without going through `_exec_at()` must invalidate the
pc cache itself.**  Safer still: construct the session with `cache_regs=False`
for any row that repeats an access, and pay the extra debugger round-trips.
