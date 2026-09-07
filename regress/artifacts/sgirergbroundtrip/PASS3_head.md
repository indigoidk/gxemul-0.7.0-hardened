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
