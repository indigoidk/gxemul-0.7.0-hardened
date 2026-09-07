# DESIGN BRIEF pass 1 — `sgimtedepth4dead`: a dead branch whose repair CHANGES BEHAVIOUR

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
one that agrees.

**Three briefs of mine this week stated false premises** — a variable's declared *type*, which of two
arms is authoritative, and what a sibling probe's oracle actually asserts. Each was caught by a seat
reading the code instead of my description of it. **If a premise below is wrong, that is the most
valuable thing you can tell me.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.** Do not read
`GXEMUL-SEC/regress/artifacts/` or `GXEMUL-SEC/tools/pipeline/ledger.json`.

**Where this brief states an ARITHMETIC claim, ENUMERATE it rather than reasoning about it.**

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — THE DEAD BRANCH.** In `do_mte_transfer()`:

```c
	int depth = 8 << ((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT);
	...
	uint32_t src_mode = (src_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);
	uint32_t dst_mode = (dst_tlb << 10) + (((mode & MTE_MODE_DEPTH_MASK) >> MTE_DEPTH_SHIFT) << 8);

	// Hack. The MTE perhaps doesn't deal with colors per se,
	// but this makes sure that we copy 32 bits when doing 32-bit
	// transfers.
	if (depth == 4) {
		src_mode |= DE_MODE_TYPE_RGBA;
		dst_mode |= DE_MODE_TYPE_RGBA;
	}
```

`MTE_MODE_DEPTH_MASK` is `0x300` and `MTE_DEPTH_SHIFT` is `8`, so the field is 0–3 and
**`depth` ∈ {8, 16, 32, 64}. It is never 4, so the branch never executes.** Two seats have separately
confirmed the branch is unreachable, one of them unprompted while answering a different question.

**S2 — THE CONSEQUENCE.** Because the branch never fires, the type nibble of both constructed modes
stays `0x00` = `DE_MODE_TYPE_CI`. Every MTE transfer therefore runs `horrible_getputpixel()` through
its **CI** arms — `buf[0] = *color` on PUT and `*color = buf[0]` on GET — **one byte** — while the
transfer LENGTH is `bufdepth = 1 << ((mode >> 8) & 3)`, which the same construction sets from the
same field and which is 1, 2, 4 or 8.

So at MTE depth 16/32/64 the PUT writes `bufdepth` bytes with **only `buf[0]` assigned**, and
`buf` is a fresh uninitialised local on every call. That is the mechanism of `sgirebufuninit`'s
strongest reachability, not a separate curiosity.

**S3 — THE `|=` IS SAFE TODAY, and I checked because a seat flagged it.** A seat warned that
`src_mode |= DE_MODE_TYPE_RGBA` yields ABGR (`0x30`) rather than RGBA if the type nibble already
holds RGB (`0x10`), and honestly said it could not settle it from its packet. It is safe:
`(src_tlb << 10)` occupies bits ≥ 10 and the depth term occupies bits 8–9, so **the type nibble is
always zero** and `|= 0x20` yields exactly RGBA. **The conditional is sound and its antecedent is
false** — but it becomes live the moment that construction gains a type field.

---

## The questions

**Q1 — WHAT WAS THE INTENDED CONDITION?** The comment says the branch exists so that *"we copy 32
bits when doing 32-bit transfers"*. `depth` is in BITS and `depth / 8` is used three lines above as a
byte width. So the intended test looks like `depth == 32` (equivalently `depth / 8 == 4`). **Is that
right, or is there a reading on which the author meant something else?** Note that the very next
depth test in the same function is `if (depth != 8)`, which is a *bits* comparison — so the function
mixes the two units and I want that checked rather than assumed.

**Q2 — *** THE REAL QUESTION: REPAIRING THIS CHANGES BEHAVIOUR. *** ** Making the branch live means
every 32-bit MTE transfer stops using the CI arms and starts using RGBA. That is not a bug fix in the
usual sense — it is **enabling a code path that has never executed in this fork**. This is a hardening
fork, and its addition licence says changes are warranted by a MEASURED DELTA or a TRANSFERRED
WARRANT, never by "it looks like what the author meant".

  * **What breaks if the branch goes live?** Enumerate what changes for a 32-bit MTE copy.
  * **Is enabling it actually the right disposition**, or is the right one to *delete the dead branch
    and fix the width defect where it lives* — i.e. in `horrible_getputpixel`, so a CI transfer never
    ships unassigned bytes regardless of who calls it?
  * **A third option I have not costed: leave it dead and say so in the comment.** The comment
    currently asserts a behaviour the code does not have, which is a wrong record in product code.

**Q3 — WHICH DEFECT OWNS WHICH BYTES?** `sgirebufuninit` is filed separately: `buf[4..7]` are never
assigned by any arm, and at `bufdepth` 1 or 2 the multi-byte GETs read `buf[2..3]` unfilled. This row
is about the *type nibble* being wrong. **Draw the boundary**: if this branch were repaired, which of
`sgirebufuninit`'s exposures would remain? I would rather two rows with a clean boundary than one
round that claims to close both and closes neither.

**Q4 — SEQUENCING.** Three open rows touch this function: this one, `sgirebufuninit`, and
`sgirandomcolour` (the colour-mode PUT default writing `random()` bytes). **Does fixing them in some
orders create work that a different order avoids?** Specifically, does repairing this branch change
which bytes the other two are about?

**Q5 — THE SMALLEST EDIT.** Whatever disposition you argue for, what is the smallest edit that breaks
it and still passes a detector built for it? Name the row you expect to stay green.

## What I am not asking

Do not write a patch and do not run anything. I want the disposition argued, because this is the rare
case where the "obvious fix" is a behaviour change in a fork whose whole premise is minimal surgical
correction.

**If, while verifying a claim, you found something ELSE — say so.**
