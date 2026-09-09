# `armbfiwidth` fix design — the third site of an idiom `#510` fixed twice

**VERDICT LINE FIRST.**  **The tree is `GXEMUL-SEC/src/`** — ignore the 2021 copy at the project root.

**Please do not simply ratify.** Section 2 states a difference between this site and the two already
fixed; if that difference is wrong, the whole design question dissolves. **Check it.**

## 1. THE SITE

`src/cpus/cpu_arm_instr.c`, `X(bfi)` at `:1450`:

```c
X(bfi)
{
	uint32_t x = reg(ic->arg[1]);

	int lsb = (uint8_t)ic->arg[2];
	int msb = ic->arg[2] >> 16;
	int width = msb - lsb + 1;

	x <<= lsb;

	uint32_t mask = (1 << width) - 1;      /*  <-- undefined over most of its domain  */

	mask <<= lsb;
```

The decoder gives `msb` and `lsb` **independently, each 0..31**, so `width` ranges over
**[-30, 32]** and `1 << width` is undefined three separate ways: a negative count and a count `>=`
the promoted width (C99 6.5.7p3), and at `width == 31`, `1` is `int` so `2^31` is not representable
(6.5.7p4).

## 2. THE DIFFERENCE FROM THE TWO SITES `#510` ALREADY FIXED — verify this

`#510` repaired the SAME expression at `X(ubfx)` and `X(sbfx)` fifty lines above, shipping:

```c
	uint32_t mask = (width == 32) ? 0xffffffffU : ((1U << width) - 1);
```

`1U` defends `width == 31`; the `== 32` guard defends `width == 32`.

> **BUT AT THOSE TWO SITES `width` CANNOT BE NEGATIVE, AND AT `bfi` IT CAN.**  UBFX/SBFX encode
> **widthm1**, so width is `1 + ((iword >> 16) & 31)` ∈ [1, 32] — confirmed in the disassembler at
> `cpu_arm.c:2382`, `debug(",%i", 1 + ((iw >> 16) & 31))`. **BFI encodes MSB**, so
> `width = msb - lsb + 1` and `msb < lsb` gives a nonpositive width.

**So `#510`'s form does NOT transfer unchanged: its `== 32` guard covers none of the negative
widths.**  `#510` deliberately left this site out of scope under the one-site rule and disclosed it.

**THE DENOMINATOR:** of the **1024** encodable (msb, lsb) pairs, **468** reach an undefined shift,
and **465 of those also have architecturally invalid field ordering** (`msb < lsb`) — the two sets
**overlap** rather than being disjoint.

## 3. A LIMIT I CANNOT REMOVE, and it bounds what this brief can ask

**There is NO local manual covering BFI.**  `_scratchpad/ddi0100i.txt` is DDI 0100I, which predates
ARMv6T2 — `grep -c -w BFI` returns **0**. So *what value BFI should produce when `msb < lsb`* is
**not answerable from any primary source I hold**, and I will not take it from recollection.

**What IS fully settled without a manual: the shift must be made DEFINED.** That is a C99 question
and the tree has already answered it twice, fifty lines up.

## 4. QUESTIONS

**Q1. What is the minimal defined-shift repair here?** Give the expression. It must cover
`width <= 0`, `width == 31` and `width == 32`. **Does it change any guest-visible value for the
architecturally VALID pairs (`msb >= lsb`)?** If it does, that is a behaviour change and not a
definedness repair, and the round must say so.

**Q2. For `msb < lsb` — what should the model DO?** ARM calls that encoding UNPREDICTABLE, and I
have no local text to cite. **Options: produce no change to the destination; produce whatever the
defined arithmetic yields; or announce once.** Say which, and **say plainly if you cannot settle it
without the ARM ARM** — that is a real answer and it makes this a definedness-only round with the
value question disclosed.

**Q3. Does the tree's own precedent settle Q2?** `#510`'s sites cannot reach the case, so they say
nothing about it. **Is there another ARM handler in this file that faces an UNPREDICTABLE encoding,
and what does it do?** Grep before reasoning.

**Q4. What observable distinguishes a correct repair from an incomplete one?** Note `#510`'s own
finding: `1 << 31` and `1U << 31` give the SAME mask after `- 1`, so **no guest-value row can kill a
`1U` → `1` regression** — only UBSAN or a source pin can. **What should a regression row assert
here, given that?**

**Q5. Is a witness achievable?** `#510` shipped with definedness escapes disclosed for exactly this
reason. **Say plainly if the honest answer is "no guest-value witness is possible; this needs the
sanitizer lane".**
