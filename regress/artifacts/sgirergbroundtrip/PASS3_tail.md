
---

## The questions

**Q1 — IS `rgb tiled` SOUND, or does it merely look sound?** It reports the value I expect, but it
took two corrections to get there and both failure modes were *silent declines* that produced a
plausible-looking wrong value. **What third way could this row be measuring something other than a
tiled RGB GET and still read `0xaabbcc00`?** Specifically: is there any path on which the tiled setup
partially fails and the destination still ends up holding the right word — for instance because the
LIN_A destination retains a value from an earlier session, or because the copy silently falls back?

**Q2 — IS THE FLOOR NOW CLOSED, or is there a third axis?** Two axes were found by seats and both
were floor breaches: **transfer width** (`bufdepth`) and **addressing mode** (`linear`). The guarded
body reads `buf[0..2]`, `bufdepth`, `color_mode`, `tileptr` and `ofs`; the dominating predicates are
`color_mode`'s switch, the `!linear` coordinate guard, the `tlb_mode <= 2 && tile_nr >= 256` bound and
the `!(tileptr & 0x80000000)` validity gate. **Enumerate the cells and tell me which are unrowed.**
`ofs` was measured and dies; `color_mode` conditioning was measured and dies. **What is left?**

**Q3 — THE CLOSING ZERO NEEDS A DENOMINATOR.** If your answer is "no further breaches", say **which
cells you swept** to reach it. A bare zero does not close this chain; a zero with an enumeration does.

**Q4 — IS THE CONTRACT HONEST NOW?** The detector claims to catch edits that move RGB channel bytes,
at transfer widths 4 and 8, in both GET and PUT directions, and under both linear and tiled
addressing. **What does it still NOT catch that a reader would assume it does?** One known and
unavoidable gap: a PUT/GET pair that swap channel bytes *consistently* round-trips by construction and
no round-trip oracle can see it. **Is that the only one?**

**Q5 — SHOULD ANY OF THE NINE ROWS GO?** Row demand is bounded per enumerated mutant, never per
attribution need, and this detector grew from six to nine in one round. **Is any row now redundant —
killed only by mutants another row already kills?** I would rather drop a row than carry one whose
only defence is that it exists.

**Q6 — THE SMALLEST EDIT, once more.** Name the row you expect to stay green.

## What I am not asking

Do not run anything and do not rewrite the fix. The product diff is one line and has been stable since
pass 1; what changed is the detector.

**If, while verifying a claim, you found something ELSE — say so.**
