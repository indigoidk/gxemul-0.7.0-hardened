# PANEL PASS 3 — `#505`: the REPAIR made in response to pass 2 owes its own pass

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** **Pass 2 of this round refuted four of my claims**
— a mutant I called a mirror that measured nothing, a "same script" pair that was two scripts, a gate
comment I had copied that was false, and a warrant that smuggled in three unstated facts. Every one
came from a seat reading the packet's own arithmetic. **Assume this brief can be wrong the same way.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies sit under the
project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**VERDICT LINE FIRST.**

---

## Why there is a pass 3 at all

The repair-chain rule: *a repair made in response to a pass 2 owes its own pass 2*, because the
obligation follows the **material**, not the narrative. Pass 2 produced two floor breaches; repairing
them produced **new floor-bound material** — two new rows and a materially different detector — and
"the round already had its pass 2" is a fact about the story, not about what shipped.

**The stop condition, so this does not become an unbounded chain:** one pass per floor-bound diff,
closing on the first pass that finds **zero breaches** — where a closing zero must be a *valid* pass
(the diff actually delivered, the roster complete or its misses named) and must carry **its
denominator**: which cells, which mutant shapes, were swept. *"Zero found"* and *"zero looked for"*
must not render the same.

---

## §C — WHAT PASS 2 FOUND AND WHAT WAS DONE ABOUT IT

**B1 — `M6_cond` swept the 6-row detector 6/6.** Guard kept, repair conditioned on `bufdepth == 4`;
every session then used `BUFDEPTH_32`, so the mutant's fix branch was the only one the detector ever
executed. **Repaired** by `rgb depth64`, a session at `BUFDEPTH_64`.

**B2 — `M12_linear` swept the 8-row detector 8/8.** Guard kept, repair conditioned on `linear`
(`tlb_mode > 3`); every row drove LIN_A. `linear` dominates the edited lines through
`if (!linear && (x < 0 || …)) return;`, so it is inside the DEPENDS-ON closure — a floor breach, not
debt. **Repaired** by `rgb tiled`, a session with a **TLB_A source** (destination left LIN_A on
purpose: the arm under test is the GET, whose `linear` comes from `src_mode`).

**B3 — my "mirror" mutant measured nothing.** `M7_cond8` (`bufdepth != 8`) and `M6_cond`
(`bufdepth == 4`) are the **same function** over the only two widths any row drives. The true mirror
is `M9_truemirror` (`bufdepth == 8`), which scores 5/8 — exactly what the seat derived from the packet.

**B4 — the "same script" pair was two scripts.** `4/`**`6`** → `8/`**`8`**. The shipped detector run
against pre-fix source is the genuine pair.

**B5 — a gate comment I copied was false.** A row name ≥ 16 chars does *not* silently stay green; the
pattern matches nothing, `check` compares 0 against a wanted 1, and it **FAILs**. Corrected in both
the new block and the sibling it was copied from.

## §C2 — TWO DEVICE FACTS THE NEW ROW COST, because they bear on whether it is sound

Building `rgb tiled` took two corrections, and it reported both by reading `0x77665544` — `FG_VAL`,
which the probe's own `DE_FG` comment names as *"what a declined GET leaves"*:

1. **`re_tlb_a` is `uint16_t[256]` filled by a halfword loop**, not `uint32_t[32]` like
   `re_linear_a`. An 8-byte store fills `[0..3]` from four big-endian halfwords, so `[0]` comes from
   bits 63..48 — the `<< 32` shift that is *correct* for LINEAR_A lands in `re_tlb_a[2]`.
2. **A tiled tile pointer must carry its own valid bit.** `if (!(tileptr & 0x80000000)) return;`
   gates every access; LIN_A sets that bit *explicitly*, so a probe built from the linear path never
   learns the requirement exists. TLB_A takes it from the stored value, and `re_tlb_a` being
   `uint16_t` means bit 31 of `tileptr` **is bit 15 of the register**. Fixed by `re_tlb_a[0] = 0x8002`.

## §C3 — KILL TABLE 5, the AUTHORITATIVE one: every mutant against the SHIPPED 9-row detector

Tables 1-4 scored 6- and 8-row detectors and are kept as the record of what was measured when.
This one scores the detector that ships, because a table scoring a different detector is a
wrong record -- adding rows perturbs other mutants' scores.

| run | score | shape |
|---|---|---|
| `base` | 9/9 | |
| `M1_verbatim` | 4/9 | |
| `M2_off1` | 5/9 | |
| `M3_pad` | 6/9 | |
| `M4_or` | 9/9 | |
| `M5_rev` | 5/9 | |
| `M6_cond` | 8/9 | |
| `M9_truemirror` | 5/9 | |
| `M10_ofs` | 4/9 | |
| `M11_cmode` | 8/9 | |
| `M12_linear` | 8/9 | |
| `prefix9row` | 4/9 | |

Null medium: SGIRGB_RESULT=1/9

## THE PRODUCT DIFF, inlined verbatim (unchanged since pass 1)

```diff
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 2a81d79..b3239b4 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -324,7 +324,30 @@ void horrible_getputpixel(int put, struct cpu* cpu, struct sgi_re_data* d,
 			*color = buf[0];
 			break;
 		case DE_MODE_TYPE_RGB:
-			*color = (buf[1] << 24) + (buf[2] << 16) + (buf[3] << 8);
+			/*  #505: this read buf[1..3] while the PUT arm above
+			    writes the three channels at buf[0..2] and an
+			    explicit pad at buf[3] -- so an RGB pixel did not
+			    survive its own round trip, shifting one byte left
+			    with a zero fill on every RGB source read.
+
+			    The PUT arm is the authoritative one, and the
+			    warrant is OUTSIDE this function: dev_sgi_gbe.c's
+			    scanout reads the same tile memory back for display
+			    as (buf[0]<<24)+(buf[1]<<16)+(buf[2]<<8)+buf[3],
+			    then CRMFB_MODE_TYP_RGB8 takes R,G,B from bits
+			    31..24, 23..16 and 15..8 -- byte 0 is R and byte 3
+			    is UNUSED.  So the pad sits at buf[3] because the
+			    consumer ignores buf[3], not because PUT writes a
+			    zero there; that is what makes this non-circular.
+			    The RGBA and ABGR PUT arms independently agree --
+			    both lay [R,G,B,x] in memory despite opposite
+			    register word orders -- which leaves this GET the
+			    lone container outlier among the 32-bit arms.
+
+			    The low byte stays ZERO on purpose: RGB carries
+			    three channels, so a corrected read of 0xaabbccdd
+			    yields 0xaabbcc00, NOT the source word.  */
+			*color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8);
 			break;
 		case DE_MODE_TYPE_RGBA:
 			*color = (buf[0] << 24) + (buf[1] << 16) + (buf[2] << 8) + buf[3];
```

## THE DETECTOR, its nine rows as shipped

```
307:row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
312:row("devsig", printed(t, "v0") if alive else "died", DE_STAT,
321:row("copy lin_a", printed(t, "v0") if alive else "died", "0x%x" % SRC_VAL,
342:row("rgb chan", got_rgb, "0x%x" % RGB_FIXED,
349:row("rgb not corrupt", got_rgb, "0x%x" % RGB_CORRUPT,
352:row("rgb alive", "alive" if alive else "died", "alive",
377:row("rgb samemode", got_same, "0x%x" % RGB_FIXED,
409:row("rgb depth64", got_d64, "0x%x" % RGB_FIXED,
438:row("rgb tiled", got_tiled, "0x%x" % RGB_FIXED,
```

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
